import { describe, expect, it } from 'vitest'
import { frozenScriptPreview, scriptLogDeliveryWarning } from './scriptJobPresentation'
import { fixtureRun as run } from './scriptJobFixtures'
import { runStatus } from './scriptJobState'
import type { ScriptMode } from '@/api/scriptJobs'

describe('script run diagnostics and frozen arguments', () => {
  it.each<ScriptMode>(['shell', 'python', 'command'])('shows frozen exact arguments for %s without folding them into executable code', mode => {
    const snapshot = { ...run().configSnapshot, mode, script: 'print("script")', command: 'python3', args: ['first', '', ' hello world ', 'line\nbreak'] }
    const preview = frozenScriptPreview(snapshot)
    expect(preview.code).toBe(mode === 'command' ? 'python3' : 'print("script")')
    expect(preview.args.split('\n')).toEqual(['参数 1: "first"', '参数 2: ""', '参数 3: " hello world "', '参数 4: "line\\nbreak"'])
  })
  it.each([{ blocked_reason: 'disk full' }, { backpressured: true }])('shows node spool blockage regardless of a successful execution result: %j', logDelivery => {
    const value = run('run-success', { status: 'completed', deliveryState: 'terminal', result: 'success', logDelivery })
    const before = runStatus(value)
    expect(scriptLogDeliveryWarning(value.logDelivery)).toContain('当前历史可能尚未完整到达')
    expect(scriptLogDeliveryWarning(value.logDelivery)).toContain('未确认记录保留在 Agent')
    expect(runStatus(value)).toEqual(before)
    expect(value.result).toBe('success')
  })
  it('bounds server diagnostic text and does not infer lost-log counts from node spool totals', () => {
    const warning = scriptLogDeliveryWarning({ blocked_reason: 'x'.repeat(100000), bytes: 1000000, records: 40 })
    expect(warning.length).toBeLessThan(400)
    expect(warning.endsWith('…')).toBe(true)
    expect(warning).not.toContain('1000000')
    expect(scriptLogDeliveryWarning(null)).toBe('')
    expect(scriptLogDeliveryWarning({ bytes: 5, records: 1, backpressured: false })).toBe('')
  })
  it('keeps timeout status distinct from log-delivery diagnostics', () => {
    const value = run('run-timeout', { status: 'failed', deliveryState: 'terminal', result: 'timeout', logDelivery: { backpressured: true } })
    expect(scriptLogDeliveryWarning(value.logDelivery)).not.toBe('')
    expect(runStatus(value).label).toBe('执行超时')
  })
})
