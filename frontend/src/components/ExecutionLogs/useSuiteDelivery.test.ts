import { effectScope } from 'vue'
import { describe, it, expect, vi, afterEach } from 'vitest'
import { useSuiteDelivery } from './useSuiteDelivery'
import type { SuiteDeliveryState } from '@/api/testSuite'
vi.mock('@/api/testSuite', () => ({ testSuiteApi: {} }))
function deferred<T>() { let resolve!: (v: T) => void; const promise = new Promise<T>(r => { resolve = r }); return { resolve, promise } }
const state = (id: string, phase = 'unknown'): SuiteDeliveryState => ({ executionId: id, suiteId: 'suite', environmentId: 'node', status: phase === 'terminal' ? 'failed' : 'running', deliveryState: phase, canResolve: phase === 'unknown', managedBy: 'suite' })
const tick = async () => { await Promise.resolve(); await Promise.resolve() }
afterEach(() => { vi.useRealTimers() })
describe('普通测试套未知执行人工核对', () => {
  it('换运行忽略旧读取，确认和理由不能跨选择复用', async () => {
    const first = deferred<SuiteDeliveryState>(), second = deferred<SuiteDeliveryState>()
    const api = { getDeliveryState: vi.fn().mockReturnValueOnce(first.promise).mockReturnValueOnce(second.promise), resolveDelivery: vi.fn() }
    const scope = effectScope(); const form = scope.run(() => useSuiteDelivery(api as any))!
    form.open('suite', 'old'); form.confirmed.value = true; form.reason.value = 'old proof'
    form.open('suite', 'new'); second.resolve(state('new')); await tick(); first.resolve(state('old')); await tick()
    expect(form.delivery.value?.executionId).toBe('new'); expect(form.confirmed.value).toBe(false); expect(form.reason.value).toBe('')
    scope.stop()
  })
  it('必须明确核对，冻结提交目标并阻止重复点击和迟到轮询覆盖', async () => {
    vi.useFakeTimers()
    const poll = deferred<SuiteDeliveryState>(), mutation = deferred<SuiteDeliveryState>()
    const api = { getDeliveryState: vi.fn().mockResolvedValueOnce(state('run')).mockReturnValueOnce(poll.promise), resolveDelivery: vi.fn().mockReturnValue(mutation.promise) }
    const scope = effectScope(); const form = scope.run(() => useSuiteDelivery(api as any))!
    form.open('suite', 'run'); await tick(); expect(await form.resolve()).toBe(false)
    form.confirmed.value = true; form.reason.value = ' all stopped '
    await vi.advanceTimersByTimeAsync(5000)
    const saving = form.resolve(); expect(await form.resolve()).toBe(false)
    mutation.resolve({ ...state('run', 'terminal'), closedBy: 'operator' }); expect(await saving).toBe(true)
    poll.resolve(state('run')); await tick()
    expect(form.delivery.value?.closedBy).toBe('operator'); expect(api.resolveDelivery).toHaveBeenCalledTimes(1); expect(api.resolveDelivery).toHaveBeenCalledWith('suite', 'run', 'all stopped')
    scope.stop(); await vi.advanceTimersByTimeAsync(10000); expect(api.getDeliveryState).toHaveBeenCalledTimes(2)
  })
  it('切换期间旧关闭结果不能覆盖新运行或报告成功', async () => {
    const mutation = deferred<SuiteDeliveryState>()
    const api = { getDeliveryState: vi.fn().mockResolvedValue(state('run')), resolveDelivery: vi.fn().mockReturnValue(mutation.promise) }
    const scope = effectScope(); const form = scope.run(() => useSuiteDelivery(api as any))!
    form.open('suite', 'run'); await tick(); form.confirmed.value = true; form.reason.value = 'proof'
    const pending = form.resolve(); form.open('suite', 'other'); await tick(); mutation.resolve(state('run', 'terminal'))
    expect(await pending).toBe(false); expect(form.delivery.value?.deliveryState).toBe('unknown'); scope.stop()
  })
})
