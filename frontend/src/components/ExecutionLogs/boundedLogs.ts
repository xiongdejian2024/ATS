/** 实时视窗有界；完整日志仍由服务器保存，界面明确显示已省略的前段。 */
export const LOG_LIMITS = { records: 20, chars: 512 * 1024, lines: 2000, lineChars: 8192 };
export interface LogRecord {
  id?: string;
  endOffset?: number;
  message: string;
  timestamp: string;
  execution_id?: string;
  truncated?: boolean;
}
function ownedText(value: string): string {
  // 避免V8子串长期引用一个远大于视窗的原字符串。
  return new TextDecoder().decode(new TextEncoder().encode(value));
}
export function boundedLogs(input: LogRecord[]): LogRecord[] {
  const result: LogRecord[] = [];
  let chars = LOG_LIMITS.chars, lines = LOG_LIMITS.lines;
  for (let i = input.length - 1; i >= 0 && chars > 0 && lines > 0 && result.length < LOG_LIMITS.records; i--) {
    const record = input[i];
    if (typeof record.message !== 'string') continue;
    let text = record.message.slice(-chars), count = 1, position = text.length;
    while (position > 0 && count <= lines) {
      const found = text.lastIndexOf('\n', position - 1);
      if (found < 0) break;
      if (count === lines) { text = text.slice(found + 1); break; }
      position = found; count++;
    }
    const shortened = text.length < record.message.length;
    text = text.split('\n').map(line => line.length > LOG_LIMITS.lineChars ? line.slice(-LOG_LIMITS.lineChars) : line).join('\n');
    chars -= text.length; lines -= count;
    result.unshift({ id: record.id, endOffset: record.endOffset, message: ownedText(text), timestamp: record.timestamp, execution_id: record.execution_id, truncated: record.truncated || shortened || text.length < record.message.length });
  }
  if (result.length && result.length < input.length) result[0].truncated = true;
  return result;
}
export function appendLog(records: LogRecord[], delta: LogRecord): LogRecord[] {
  const copy = records.map(r => ({ ...r }));
  const key = (r: LogRecord) => r.execution_id || r.id;
  const index = key(delta) ? copy.findIndex(r => key(r) === key(delta)) : copy.length - 1;
  if (index >= 0 && key(copy[index]) === key(delta)) {
    const previous = copy[index];
    let suffix = delta.message.slice(-LOG_LIMITS.chars), separator = '\n', gap = false;
    if (previous.endOffset !== undefined && delta.endOffset !== undefined) {
      const added = delta.endOffset - previous.endOffset;
      if (added <= 0) return records;
      const points = Array.from(suffix);
      if (added <= points.length) { suffix = points.slice(-added).join(''); separator = ''; }
      else if (added > points.length + 1) gap = true;
    }
    copy.splice(index, 1);
    copy.push({ ...delta, message: gap ? suffix : previous.message + separator + suffix,
      truncated: previous.truncated || delta.truncated || gap || delta.message.length > LOG_LIMITS.chars });
  } else copy.push({ ...delta, message: delta.message.slice(-LOG_LIMITS.chars), truncated: delta.truncated || delta.message.length > LOG_LIMITS.chars });
  return boundedLogs(copy);
}
export function normalizeLogs(input: any[]): LogRecord[] {
  return boundedLogs(input.slice(-LOG_LIMITS.records).map(r => ({ id: r.id, endOffset: r.endOffset ?? r.totalChars,
    message: typeof r.message === 'string' ? r.message : '', timestamp: r.timestamp || r.createdAt || '',
    execution_id: r.execution_id || r.executionId, truncated: !!r.truncated })));
}
