import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { effectScope, shallowRef } from 'vue'
vi.mock('@/utils/api', () => ({ apiClient: {} }))
vi.mock('@/stores/user', () => ({ useUserStore: () => ({ accessToken: 'test' }) }))
import { useScriptJobLogs } from './useScriptJobLogs'
import { useUnknownRunConfirmation } from './useUnknownRunConfirmation'
import { fixtureRun as run, deferred } from './scriptJobFixtures'
import { LOG_LIMITS } from '@/components/ExecutionLogs/boundedLogs'
import type { ScriptLogPage } from '@/api/scriptJobs'
import type { ScriptLogEvent, ScriptLogTarget } from './scriptJobSocket'

const row = (message: string, endOffset = Array.from(message).length, id = 'run-a') => ({ id: 'log-' + id, execution_id: id, message, endOffset, timestamp: '2026-10-08T01:00:00Z' })
const event = (message: string, endOffset?: number): ScriptLogEvent => ({ type: 'script_job_log', job_id: 'job-a', execution_id: 'run-a', data: row(message, endOffset) })
function setup() {
  let handler: (event: ScriptLogEvent) => void = () => {}
  const transport = { connect: vi.fn((_target: ScriptLogTarget, callback: typeof handler) => { handler = callback }), disconnect: vi.fn() }
  const requests: ReturnType<typeof deferred<ScriptLogPage>>[] = []
  const fetch = vi.fn(() => { const pending = deferred<ScriptLogPage>(); requests.push(pending); return pending.promise })
  const scope = effectScope(), stream = scope.run(() => useScriptJobLogs({ transport, fetch }))!
  const emit = (message: ScriptLogEvent) => handler(message)
  const snapshot = async (index: number, message: string, endOffset?: number) => {
    requests[index].resolve({ items: [row(message, endOffset)], skip: 0, limit: 20, total: 1 })
    await vi.advanceTimersByTimeAsync(0)
  }
  return { scope, stream, transport, requests, fetch, emit, snapshot }
}
beforeEach(() => { vi.useFakeTimers() })
afterEach(() => { vi.useRealTimers() })

describe('脚本作业有界实时日志', () => {
  it('authoritative subscribe snapshot supersedes pre-subscribe history and merges Unicode offsets', async () => {
    const { stream, emit, snapshot, scope } = setup()
    stream.open({ jobId: 'job-a', executionId: 'run-a', live: true })
    emit({ type: 'connected', job_id: 'job-a', execution_id: 'run-a' })
    emit(event('😀实时', 6))
    await snapshot(1, '开始\n😀', 4)
    await snapshot(0, 'stale', 100)
    expect(stream.records.value[0].message).toBe('开始\n😀实时')
    scope.stop()
  })
  it('reconnects with history backfill and refuses to hide incomplete snapshots on later live frames', async () => {
    const { stream, emit, snapshot, requests, scope } = setup()
    stream.open({ jobId: 'job-a', executionId: 'run-a', live: true }); emit({ type: 'connected' })
    await snapshot(1, 'first')
    emit({ type: 'disconnected', reconnecting: true })
    expect(stream.status.value.message).toContain('可能有遗漏')
    emit({ type: 'connected' }); requests[2].reject(new Error('unavailable')); await vi.advanceTimersByTimeAsync(0)
    emit(event('live', 100)); await vi.advanceTimersByTimeAsync(100)
    expect(stream.status.value.type).toBe('error')
    const refresh = stream.refresh(); await snapshot(3, 'recovered', 110); await refresh
    expect(stream.status.value.type).toBe('info')
    scope.stop()
  })
  it('ignores late history and frames after close/reopen or switching immutable runs', async () => {
    const { stream, emit, snapshot, transport, scope } = setup()
    stream.open({ jobId: 'job-a', executionId: 'run-a', live: true })
    const oldHandler = transport.connect.mock.calls[0][1]
    stream.close(); stream.open({ jobId: 'job-a', executionId: 'run-b', live: true })
    oldHandler(event('stale socket'))
    emit(event('wrong run'))
    await snapshot(0, 'stale history')
    expect(stream.records.value).toEqual([])
    scope.stop()
    expect(transport.disconnect).toHaveBeenCalledTimes(4)
  })
  it('keeps a selected historical/terminal run subscribed for late spool delivery and bounds output', async () => {
    const { stream, emit, snapshot, scope } = setup()
    // Terminal status is intentionally not a reason to stop an open viewer subscription.
    stream.open({ jobId: 'job-a', executionId: 'run-a', live: true }); emit({ type: 'connected' })
    await snapshot(1, 'terminal arrived')
    emit(event(('late spool output 😀\n').repeat(40000), 800000)); await vi.advanceTimersByTimeAsync(100)
    expect(stream.records.value[0].truncated).toBe(true)
    expect(new TextEncoder().encode(stream.records.value.map(record => record.message).join('')).length).toBeLessThanOrEqual(LOG_LIMITS.bytes)
    expect(stream.records.value.flatMap(record => record.message.split('\n')).length).toBeLessThanOrEqual(LOG_LIMITS.lines)
    scope.stop()
  })
  it('authorization rejection stops implicit retry but manual refresh can reconnect', async () => {
    const { stream, emit, transport, scope } = setup()
    stream.open({ jobId: 'job-a', executionId: 'run-a', live: true })
    emit({ type: 'disconnected', closeCode: 1008, reconnecting: false })
    expect(stream.status.value.message).toContain('已停止重连')
    void stream.refresh()
    expect(transport.connect).toHaveBeenCalledTimes(2)
    scope.stop()
  })
  it('invalidates confirmation after unknown → running → unknown, and on run switches', () => {
    const selected = shallowRef(run('run-a', { deliveryState: 'unknown' })), scope = effectScope()
    const confirmation = scope.run(() => useUnknownRunConfirmation(() => selected.value))!
    confirmation.confirmed.value = true; confirmation.reason.value = 'old check'
    selected.value = run()
    selected.value = run('run-a', { deliveryState: 'unknown' })
    expect(confirmation.confirmed.value).toBe(false)
    expect(confirmation.reason.value).toBe('')
    confirmation.confirmed.value = true
    selected.value = run('run-b', { deliveryState: 'unknown' })
    expect(confirmation.confirmed.value).toBe(false)
    scope.stop()
  })
})
