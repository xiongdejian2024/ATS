import { shallowRef, onScopeDispose } from 'vue';
import { appendLog, normalizeLogs, type LogRecord } from './boundedLogs';

export function useBoundedLogs() {
  const records = shallowRef<LogRecord[]>([]);
  let pending: LogRecord[] = [], timer: ReturnType<typeof setTimeout> | undefined;
  function flush() {
    timer = undefined;
    for (const record of pending) records.value = appendLog(records.value, record);
    pending = [];
  }
  function append(record: LogRecord) {
    pending = appendLog(pending, record);
    if (timer === undefined) timer = setTimeout(flush, 100);
  }
  function clear() {
    if (timer !== undefined) clearTimeout(timer);
    timer = undefined; pending = []; records.value = [];
  }
  function replace(input: any[]) {
    let history = normalizeLogs(input);
    // 快照和实时增量按服务器字符位置合并，刷新期间的新消息不会被覆盖。
    for (const record of [...records.value, ...pending]) history = appendLog(history, record);
    if (timer !== undefined) clearTimeout(timer);
    timer = undefined; pending = []; records.value = history;
  }
  onScopeDispose(clear);
  return { records, append, clear, replace };
}
