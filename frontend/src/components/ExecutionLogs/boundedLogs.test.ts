import { describe, it, expect, vi, afterEach } from 'vitest'
import { effectScope } from 'vue'
import { appendLog, boundedLogs, normalizeLogs, LOG_LIMITS } from './boundedLogs'
import { useBoundedLogs } from './useBoundedLogs'
const record = (message: string, endOffset?: number) => ({ message, timestamp: '2026-10-06T16:00:00', execution_id: '功能执行', endOffset })
function limits(rows: ReturnType<typeof boundedLogs>) {
  expect(rows.length).toBeLessThanOrEqual(LOG_LIMITS.records)
  expect(rows.reduce((n, r) => n + r.message.length, 0)).toBeLessThanOrEqual(LOG_LIMITS.chars)
  expect(rows.reduce((n, r) => n + r.message.split('\n').length, 0)).toBeLessThanOrEqual(LOG_LIMITS.lines)
  expect(rows.every(r => r.message.split('\n').every(line => line.length <= LOG_LIMITS.lineChars))).toBe(true)
}
afterEach(() => { vi.useRealTimers() })
describe('功能执行日志有界视窗', () => {
  it('十万行仅保留最近2000行，保留最新输出并提示省略', () => {
    const rows = boundedLogs([record(Array.from({length: 100000}, (_, i) => `功能用例${i}`).join('\n'))])
    limits(rows); expect(rows[0].message.endsWith('功能用例99999')).toBe(true); expect(rows[0].truncated).toBe(true)
  })
  it('前导换行和恰好2000行不会多计一行', () => {
    const text = '\n' + '行\n'.repeat(1998) + '尾'
    const rows = boundedLogs([record(text)])
    limits(rows); expect(rows[0].message).toBe(text); expect(rows[0].truncated).toBe(false)
  })
  it('多个执行与超长行均受总量限制', () => {
    const rows = boundedLogs(Array.from({ length: 100 }, (_, i) => ({ ...record('长'.repeat(1000000)), execution_id: String(i) })))
    limits(rows); expect(rows.at(-1)?.execution_id).toBe('99'); expect(rows[0].truncated).toBe(true)
  })
  it('连续20000个增量不增长记录/字符/行数量', () => {
    let rows = [] as ReturnType<typeof boundedLogs>
    for (let i = 0; i < 20000; i++) rows = appendLog(rows, record(`输出${i}`))
    limits(rows); expect(rows[0].message.endsWith('输出19999')).toBe(true)
  })
  it('快照与中文emoji增量按Unicode位置合并，重放不重复', () => {
    let rows = normalizeLogs([{ ...record('中文😀'), executionId: '功能执行', totalChars: 3 }])
    rows = appendLog(rows, record('新增😀', 7))
    expect(rows[0].message).toBe('中文😀\n新增😀')
    expect(appendLog(rows, record('新增😀', 7))).toBe(rows)
    expect(appendLog(rows, record('旧', 2))).toBe(rows)
  })
  it('快照包含部分实时数据时只补后缀，断线缺口明确提示', () => {
    const rows = appendLog([record('甲\n乙', 3)], record('甲\n乙\n丙', 5))
    expect(rows[0].message).toBe('甲\n乙\n丙')
    const gap = appendLog(rows, record('末尾', 100))
    expect(gap[0].message).toBe('末尾'); expect(gap[0].truncated).toBe(true)
  })
  it('无execution_id的不同历史记录通过主键区分', () => {
    expect(appendLog([{ ...record('甲'), execution_id: undefined, id: '甲' }], { ...record('乙'), execution_id: undefined, id: '乙' })).toHaveLength(2)
  })
  it('100ms内只刷新一次；历史返回不覆盖实时消息；销毁取消刷新', () => {
    vi.useFakeTimers()
    const scope = effectScope(); const buffer = scope.run(() => useBoundedLogs())!
    buffer.replace([record('开始', 2)])
    buffer.append(record('实时😀', 6)); expect(buffer.records.value[0].message).toBe('开始')
    buffer.replace([record('开始', 2)]); expect(buffer.records.value[0].message).toBe('开始\n实时😀')
    buffer.append(record('结束', 9)); vi.advanceTimersByTime(99); expect(buffer.records.value[0].endOffset).toBe(6)
    vi.advanceTimersByTime(1); expect(buffer.records.value[0].message.endsWith('结束')).toBe(true)
    buffer.append(record('销毁后', 13)); scope.stop(); vi.runAllTimers(); expect(buffer.records.value).toEqual([])
  })
})
