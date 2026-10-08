import { describe, expect, it } from 'vitest';
import { appendLog, boundedLogs, LOG_LIMITS, utf8Tail, scalarTail } from './boundedLogs';
import { displayLogLines } from './logPresentation';
const row = (message: string, execution_id = 'run') => ({ message, execution_id, timestamp: '2026-10-08T03:00:00.000Z' });
describe('bounded compressed log presentation', () => {
  it('folds only adjacent equal lines within one execution and keeps raw evidence', () => {
    const records = [row('repeat\nrepeat\nother\nrepeat'), row('repeat', 'other-run')];
    const before = JSON.stringify(records);
    expect(displayLogLines(records, true).map(r => r.count)).toEqual([2, 1, 1, 1]);
    expect(displayLogLines(records, false)).toHaveLength(5);
    expect(JSON.stringify(records)).toBe(before);
  });
  it('enforces UTF-8 bytes for multilingual and emoji output without corrupting scalars', () => {
    const rows = boundedLogs([row(('中文😀'.repeat(1800) + '\n').repeat(500))]);
    expect(rows.reduce((n,r) => n + new TextEncoder().encode(r.message).length, 0)).toBeLessThanOrEqual(LOG_LIMITS.bytes);
    expect(rows[0].truncated).toBe(true);
    expect(rows[0].message).not.toContain('\ufffd');
    expect(utf8Tail('A😀中文', 7)).toBe('中文');
  });
  it('compresses the bounded viewport, and unfolding never expands beyond its raw limit', () => {
    const rows = boundedLogs([row('same\n'.repeat(100000))]);
    expect(displayLogLines(rows, false).length).toBeLessThanOrEqual(LOG_LIMITS.lines);
    expect(displayLogLines(rows, true).length).toBeLessThanOrEqual(2);
  });
});

it('does not split emoji at earlier UTF-16 line/global/append clipping boundaries', () => {
  expect(scalarTail('😀' + 'a'.repeat(8191), 8192)).toBe('a'.repeat(8191));
  for (const length of [8191, LOG_LIMITS.chars - 1]) {
    const text = '😀' + 'a'.repeat(length);
    for (const rows of [boundedLogs([row(text)]), appendLog([], row(text))]) {
      expect(rows[0].message).not.toContain('\ufffd');
      expect(rows[0].message).not.toMatch(/[\ud800-\udfff]/);
    }
  }
});
