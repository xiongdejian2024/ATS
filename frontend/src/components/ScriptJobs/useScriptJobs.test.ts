import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { effectScope } from 'vue'
vi.mock('@/utils/api', () => ({ apiClient: {} }))
import { useScriptJobs } from './useScriptJobs'
import { createSubmissionStore } from './scriptJobSubmissions'
import { fixtureJob as job, fixtureRun as run, fixtureNode as node, deferred } from './scriptJobFixtures'
import type { ScriptJob, ScriptJobRun, ScriptPage } from '@/api/scriptJobs'

function setup(store = createSubmissionStore(), owner = 'user-a') {
  const api = {
    list: vi.fn(async (id: string) => ({ items: [job('job-a', id)], total: 1, page: 1, size: 20 })),
    nodes: vi.fn(async () => ({ items: [node()] })),
    get: vi.fn(async (id: string) => job(id)),
    history: vi.fn(async () => ({ items: [run()], total: 1, page: 1, size: 20 })),
    getRun: vi.fn(async (_jobId: string, id: string) => run(id)),
    run: vi.fn(async () => run()), cancel: vi.fn(async () => run('run-a', { cancelRequested: true })),
    resolve: vi.fn(async () => run('run-a', { status: 'failed', deliveryState: 'terminal', result: 'unknown', closedAt: '2026-10-08T02:00:00Z' })),
  }
  const scope = effectScope(), state = scope.run(() => useScriptJobs(api as any, store, owner))!
  state.setProject('project-a')
  return { api, scope, state, store }
}
beforeEach(() => { vi.useFakeTimers() })
afterEach(() => { vi.useRealTimers(); vi.unstubAllGlobals() })

describe('脚本作业请求隔离与运行控制', () => {
  it('ignores a late project list and aborts it when changing project', async () => {
    const { state, api, scope } = setup(), slow = deferred<ScriptPage<ScriptJob>>()
    await Promise.resolve()
    api.list.mockReturnValueOnce(slow.promise)
    const first = state.refresh(), signal = (api.list.mock.calls.at(-1) as any)[2]
    state.setProject('project-b')
    expect(signal.aborted).toBe(true)
    await vi.advanceTimersByTimeAsync(0)
    slow.resolve({ items: [job('old')], total: 1, page: 1, size: 20 }); await first
    expect(state.jobs.value[0].projectId).toBe('project-b')
    scope.stop()
  })
  it('suppresses repeated clicks and preserves request identity across failed retries without randomUUID', async () => {
    vi.stubGlobal('crypto', { getRandomValues: (bytes: Uint8Array) => bytes.fill(11) })
    const { state, api, scope } = setup(), pending = deferred<ScriptJobRun>()
    api.run.mockReturnValueOnce(pending.promise)
    const first = state.submit(job())
    await state.submit(job())
    expect(api.run).toHaveBeenCalledOnce()
    const requestId = (api.run.mock.calls[0] as any)[1]
    expect(requestId).toMatch(/^req_/)
    pending.reject(new Error('connection lost')); await first
    expect(state.submission('job-a')?.uncertain).toBe(true)
    expect(state.error.value).toContain('不会自动重跑')
    await state.submit(job())
    expect((api.run.mock.calls[1] as any)[1]).toBe(requestId)
    expect(state.submission('job-a')).toBeUndefined()
    scope.stop()
  })
  it('persists ambiguous identities through reload and isolates different authenticated users', async () => {
    let saved = ''
    const storage = { getItem: () => saved, setItem: (_key: string, value: string) => { saved = value } }
    const first = setup(createSubmissionStore(storage))
    first.api.run.mockRejectedValueOnce(new Error('lost acknowledgement'))
    await first.state.submit(job()); first.scope.stop()
    const original = (first.api.run.mock.calls[0] as any)[1]
    expect(saved).not.toContain('echo hello')
    const second = setup(createSubmissionStore(storage))
    expect(second.state.submission('job-a')?.uncertain).toBe(true)
    await second.state.submit(job())
    expect((second.api.run.mock.calls[0] as any)[1]).toBe(original)
    const other = setup(first.store, 'user-b')
    expect(other.state.submission('job-a')).toBeUndefined()
    second.scope.stop(); other.scope.stop()
  })
  it('does not reopen an old run after navigation, but settles its retry identity', async () => {
    const { state, api, scope } = setup(), pending = deferred<ScriptJobRun>()
    api.run.mockReturnValueOnce(pending.promise)
    const submitting = state.submit(job())
    await state.selectJob('job-b')
    pending.resolve(run())
    expect(await submitting).toBeUndefined()
    expect(state.job.value?.id).toBe('job-b')
    expect(state.submission('job-a')).toBeUndefined()
    scope.stop()
  })
  it('keeps frozen job/run identity for cancellation despite current job edits and ignores late cancel responses', async () => {
    const { state, api, scope } = setup(), cancellation = deferred<ScriptJobRun>()
    await state.selectJob('job-a'); await state.selectRun('run-a')
    state.job.value = { ...job(), environmentId: 'node-new', revision: 2 }
    api.cancel.mockReturnValueOnce(cancellation.promise)
    const pending = state.act('cancel')
    await state.act('cancel')
    expect(api.cancel).toHaveBeenCalledOnce()
    expect(api.cancel).toHaveBeenCalledWith('job-a', 'run-a')
    await state.selectRun('run-b')
    cancellation.resolve(run('run-a', { cancelRequested: true })); await pending
    expect(state.run.value?.executionId).toBe('run-b')
    expect(state.run.value?.cancelRequested).toBe(false)
    scope.stop()
  })
  it('requires explicit confirmation to close an unknown run and preserves unknown result', async () => {
    const { state, api, scope } = setup()
    await state.selectJob('job-a'); await state.selectRun('run-a')
    state.run.value = run('run-a', { deliveryState: 'unknown' })
    await state.act('resolve', false)
    expect(api.resolve).not.toHaveBeenCalled()
    await state.act('resolve', true, '节点进程已停止')
    expect(api.resolve).toHaveBeenCalledWith('job-a', 'run-a', '节点进程已停止')
    expect(state.run.value?.result).toBe('unknown')
    expect(state.run.value?.status).toBe('failed')
    scope.stop()
  })
  it('rejects stale history/detail after close, reopen, or run switches', async () => {
    const { state, api, scope } = setup(), old = deferred<ScriptJobRun>()
    await state.selectJob('job-a')
    api.getRun.mockReturnValueOnce(old.promise)
    const reading = state.selectRun('run-old'), signal = (api.getRun.mock.calls.at(-1) as any)[2]
    state.closeJob(); await state.selectJob('job-a'); await state.selectRun('run-new')
    expect(signal.aborted).toBe(true)
    old.resolve(run('run-old')); await reading
    expect(state.run.value?.executionId).toBe('run-new')
    scope.stop()
  })
  it('an older poll cannot erase a confirmed cancel request', async () => {
    const { state, api, scope } = setup(), old = deferred<ScriptJobRun>()
    await state.selectJob('job-a'); await state.selectRun('run-a')
    api.getRun.mockReturnValueOnce(old.promise)
    const poll = state.refreshRun()
    await state.act('cancel')
    old.resolve(run()); await poll
    expect(state.run.value?.cancelRequested).toBe(true)
    scope.stop()
  })
  it('fails closed when a deep-linked job belongs to another project', async () => {
    const { state, api, scope } = setup()
    api.get.mockResolvedValueOnce(job('cross-project', 'other-project'))
    await state.selectJob('cross-project')
    expect(state.job.value).toBeNull()
    expect(state.historyError.value).toContain('不属于当前项目')
    expect(api.history).not.toHaveBeenCalled()
    scope.stop()
  })
})
