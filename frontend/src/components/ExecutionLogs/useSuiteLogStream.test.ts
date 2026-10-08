import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { effectScope } from 'vue'
import type { LogMessage, LogMessageHandler } from '@/utils/logWebSocket'
import { LOG_LIMITS } from './boundedLogs'

vi.mock('@/api/testSuite', () => ({ testSuiteApi: { getSuiteLogs: vi.fn() } }))
vi.mock('@/utils/logWebSocket', () => ({ logWebSocketManager: {} }))
import { useSuiteLogStream } from './useSuiteLogStream'

function deferred<T>() {
  let resolve!: (value: T) => void, reject!: (error: Error) => void
  const promise = new Promise<T>((yes, no) => { resolve = yes; reject = no })
  return { promise, resolve, reject }
}
function setup() {
  const handlers = new Set<LogMessageHandler>()
  const requests: ReturnType<typeof deferred<{ items: ReturnType<typeof row>[] }>>[] = []
  const transport = {
    on: vi.fn((handler: LogMessageHandler) => handlers.add(handler)),
    off: vi.fn((handler: LogMessageHandler) => handlers.delete(handler)),
    connect: vi.fn(async () => true), disconnect: vi.fn(),
  }
  const fetchHistory = vi.fn(() => {
    const result = deferred<{ items: ReturnType<typeof row>[] }>()
    requests.push(result)
    return result.promise
  })
  const scope = effectScope()
  const stream = scope.run(() => useSuiteLogStream({ transport, fetchHistory: fetchHistory as any }))!
  const emit = (event: LogMessage) => handlers.forEach(handler => handler(event))
  return { scope, stream, requests, transport, fetchHistory, emit }
}
const row = (message: string, endOffset = Array.from(message).length, execution_id = 'run-1') => ({
  id: `log-${execution_id}`, execution_id, message, endOffset, timestamp: '2026-10-08T01:00:00',
})
const history = async (request: ReturnType<typeof setup>['requests'][number], text: string, endOffset?: number) => {
  request.resolve({ items: [row(text, endOffset)] })
  await vi.advanceTimersByTimeAsync(0)
}
const connected = { type: 'connected' } as const
const disconnected = { type: 'disconnected', suite_id: 'suite-1', closeCode: 1013, reconnecting: true } as const
const log = (message: string, endOffset?: number): LogMessage => ({ type: 'test_suite_log', suite_id: 'suite-1', data: row(message, endOffset) })
beforeEach(() => { vi.useFakeTimers() })
afterEach(() => { vi.useRealTimers(); vi.restoreAllMocks() })

describe('日志重连历史恢复', () => {
  it('服务端确认连接后重读历史，忽略订阅前快照，并合并中文emoji实时后缀而不重复', async () => {
    const { scope, stream, requests, emit } = setup()
    expect(stream.status.value).toBeNull()
    stream.open({ suiteId: 'suite-1', live: true })
    expect(stream.status.value?.message).toContain('正在连接')
    emit(connected)
    expect(requests).toHaveLength(2)
    emit(log('😀实时', 6))
    await history(requests[1], '开始\n😀', 4)
    expect(stream.records.value[0].message).toBe('开始\n😀实时')
    await history(requests[0], '过期内容', 999)
    expect(stream.records.value[0].message).toBe('开始\n😀实时')
    emit(log('😀实时', 6)); vi.advanceTimersByTime(100)
    expect(stream.records.value[0].message).toBe('开始\n😀实时')
    scope.stop()
  })

  it('慢订阅断开立即显示遗漏警告，每次重连均同步历史且重复重连不重复文本', async () => {
    const { scope, stream, requests, emit } = setup()
    stream.open({ suiteId: 'suite-1', live: true }); emit(connected)
    await history(requests[1], '开始')
    emit(disconnected)
    expect(stream.status.value?.type).toBe('warning')
    expect(stream.status.value?.message).toContain('可能有遗漏')
    emit(connected)
    expect(stream.loading.value).toBe(true)
    expect(stream.status.value?.message).toContain('重新同步')
    emit(log('最新😀', 11))
    await history(requests[2], '开始\n断开期间\n最新😀', 11)
    expect(stream.records.value[0].message).toBe('开始\n断开期间\n最新😀')
    expect(stream.status.value?.message).toContain('最近历史已重新同步')
    emit(disconnected); emit(connected)
    await history(requests[3], '开始\n断开期间\n最新😀', 11)
    expect(stream.records.value[0].message).toBe('开始\n断开期间\n最新😀')
    scope.stop()
  })

  it('重同步失败保持显式错误，后续实时帧不能把不完整视窗标为已恢复', async () => {
    vi.spyOn(console, 'error').mockImplementation(() => {})
    const { scope, stream, requests, emit } = setup()
    stream.open({ suiteId: 'suite-1', live: true }); emit(connected)
    await history(requests[1], '开始')
    emit(disconnected); emit(connected)
    requests[2].reject(new Error('HTTP unavailable')); await vi.advanceTimersByTimeAsync(0)
    emit(log('后续', 999)); vi.advanceTimersByTime(100)
    expect(stream.status.value?.type).toBe('error')
    expect(stream.status.value?.message).toContain('可能不完整')
    const refresh = stream.refresh()
    await history(requests[3], '恢复后的历史', 1000); await refresh
    expect(stream.status.value?.message).toContain('最近历史已重新同步')
    scope.stop()
  })

  it('HTTP返回期间再次断开时不撤销恢复警告，也不接受该旧快照', async () => {
    const { scope, stream, requests, emit } = setup()
    stream.open({ suiteId: 'suite-1', live: true }); emit(connected)
    emit(disconnected)
    await history(requests[1], '已过期')
    expect(stream.records.value).toEqual([])
    expect(stream.status.value?.type).toBe('warning')
    expect(stream.loading.value).toBe(false)
    scope.stop()
  })

  it('切换同套的执行或新测试套时隔离旧回调、旧HTTP和筛选不匹配的日志', async () => {
    const { scope, stream, requests, emit, transport, fetchHistory } = setup()
    stream.open({ suiteId: 'suite-1', executionId: 'run-1', live: true })
    const oldHandler = transport.on.mock.calls[0][0]
    emit(connected)
    stream.open({ suiteId: 'suite-1', executionId: 'run-2', live: true })
    emit(connected)
    oldHandler(log('旧连接', 100))
    emit(log('旧执行', 100))
    await history(requests[1], '旧快照', 100)
    requests[3].resolve({ items: [row('新执行', 3, 'run-2')] }); await vi.advanceTimersByTimeAsync(0)
    expect(stream.records.value.map(r => r.message)).toEqual(['新执行'])
    expect(fetchHistory.mock.calls).toHaveLength(4)
    stream.open({ suiteId: 'suite-2', logId: 'chosen-log', live: true })
    oldHandler(connected)
    emit(log('其他测试套', 200))
    expect(requests).toHaveLength(5)
    expect(stream.records.value).toEqual([])
    expect(fetchHistory).toHaveBeenLastCalledWith('suite-2', { skip: 0, limit: 20, logId: 'chosen-log' })
    scope.stop()
  })

  it('清空、关闭、卸载后忽略尚未完成的HTTP成功或失败，取消有界缓冲定时器', async () => {
    const error = vi.spyOn(console, 'error').mockImplementation(() => {})
    const { scope, stream, requests, emit, transport } = setup()
    stream.open({ suiteId: 'suite-1', live: true }); emit(connected)
    stream.clear(); await history(requests[1], '清空前')
    expect(stream.records.value).toEqual([])
    void stream.refresh(); stream.close()
    requests[2].reject(new Error('closed')); await vi.advanceTimersByTimeAsync(0)
    expect(error).not.toHaveBeenCalled()
    expect(stream.status.value).toBeNull()
    stream.open({ suiteId: 'suite-1', live: true }); emit(connected)
    emit(log('尚未刷新', 5))
    const lateHandler = transport.on.mock.calls[1][0]
    scope.stop(); await history(requests[4], '卸载前')
    lateHandler(connected); vi.runAllTimers()
    expect(stream.records.value).toEqual([])
    expect(requests).toHaveLength(5)
    expect(vi.getTimerCount()).toBe(0)
  })

  it('重试耗尽可手动重连；离线HTTP成功不会伪装为实时恢复', async () => {
    const { scope, stream, requests, emit, transport } = setup()
    stream.open({ suiteId: 'suite-1', live: true }); emit(connected)
    emit({ ...disconnected, reconnecting: false })
    expect(stream.status.value?.type).toBe('error')
    const refresh = stream.refresh()
    expect(transport.connect).toHaveBeenCalledTimes(2)
    emit({ ...disconnected, reconnecting: false })
    await history(requests[2], '离线快照'); await refresh
    expect(stream.status.value?.message).toContain('连接不可用')
    scope.stop()
  })

  it('非实时历史不连接socket，超长恢复历史仍保留有界尾部', async () => {
    const { scope, stream, requests, transport } = setup()
    stream.open({ suiteId: 'suite-1', live: false })
    const text = Array.from({ length: 10000 }, (_, i) => `日志${i}`).join('\n')
    await history(requests[0], text)
    expect(transport.connect).not.toHaveBeenCalled()
    expect(stream.records.value[0].message.split('\n')).toHaveLength(LOG_LIMITS.lines)
    expect(stream.records.value[0].message.endsWith('日志9999')).toBe(true)
    expect(stream.records.value[0].truncated).toBe(true)
    scope.stop()
  })
  it('重连快照的20个新执行替换20个旧执行，同时保留HTTP期间已刷新的新实时执行', async () => {
    const { scope, stream, requests, emit } = setup()
    stream.open({ suiteId: 'suite-1', live: true }); emit(connected)
    requests[1].resolve({ items: Array.from({ length: 20 }, (_, i) => row(`旧${i}`, 3, `old-${i}`)) })
    await vi.advanceTimersByTimeAsync(0)
    emit(disconnected); emit(connected)
    requests[2].resolve({ items: Array.from({ length: 20 }, (_, i) => ({ ...row(`新${i}`, 3, `new-${i}`), timestamp: `2026-10-08T01:00:00.${String(i).padStart(3, '0')}` })) })
    await vi.advanceTimersByTimeAsync(0)
    expect(stream.records.value.map(record => record.execution_id)).toEqual(Array.from({ length: 20 }, (_, i) => `new-${i}`))
    emit(disconnected); emit(connected)
    emit({ type: 'test_suite_log', suite_id: 'suite-1', data: { ...row('排队延迟的旧执行', 50, 'old-0'), timestamp: '2026-10-08T00:59:00' } })
    emit({ type: 'test_suite_log', suite_id: 'suite-1', data: { ...row('HTTP期间的最新日志', 20, 'newest'), timestamp: '2026-10-08T01:01:00' } })
    await vi.advanceTimersByTimeAsync(100)
    requests[3].resolve({ items: Array.from({ length: 20 }, (_, i) => ({ ...row(`新${i}`, 3, `new-${i}`), timestamp: `2026-10-08T01:00:00.${String(i).padStart(3, '0')}` })) })
    await vi.advanceTimersByTimeAsync(0)
    expect(stream.records.value.map(record => record.execution_id)).toEqual([...Array.from({ length: 19 }, (_, i) => `new-${i + 1}`), 'newest'])
    expect(stream.records.value[19].message).toBe('HTTP期间的最新日志')
    scope.stop()
  })

  it('权限拒绝明确显示停止自动重连，用户刷新才会重新尝试', async () => {
    const { scope, stream, emit, transport } = setup()
    stream.open({ suiteId: 'suite-1', live: true })
    emit({ ...disconnected, closeCode: 1008, reconnecting: false })
    expect(stream.status.value?.type).toBe('error')
    expect(stream.status.value?.message).toContain('访问被拒绝')
    expect(stream.status.value?.message).toContain('停止自动重连')
    await vi.advanceTimersByTimeAsync(30000)
    expect(transport.connect).toHaveBeenCalledTimes(1)
    void stream.refresh()
    expect(transport.connect).toHaveBeenCalledTimes(2)
    scope.stop()
  })

})
