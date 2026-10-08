import { shallowRef, onScopeDispose } from 'vue';
import { appendLog, boundedLogs, normalizeLogs, type LogRecord } from './boundedLogs';

export function useBoundedLogs() {
  const records = shallowRef<LogRecord[]>([]);
  let pending: LogRecord[] = [], timer: ReturnType<typeof setTimeout> | undefined;
  // A request owns only live changes received after it started, never the old viewport.
  let snapshotUpdates: LogRecord[] | undefined;
  function flush() {
    timer = undefined;
    for (const record of pending) records.value = appendLog(records.value, record);
    pending = [];
  }
  function append(record: LogRecord) {
    pending = appendLog(pending, record);
    if (snapshotUpdates) snapshotUpdates = appendLog(snapshotUpdates, record);
    if (timer === undefined) timer = setTimeout(flush, 100);
  }
  function beginSnapshot() { snapshotUpdates = []; }
  function cancelSnapshot() { snapshotUpdates = undefined; }
  function clear() {
    if (timer !== undefined) clearTimeout(timer);
    timer = undefined; pending = []; records.value = []; cancelSnapshot();
  }
  function replace(input: any[]) {
    let history = normalizeLogs(input);
    // The HTTP snapshot supplies authoritative record membership/order. Replay only
    // bounded live changes received during that request, even if already rendered.
    const key = (record: LogRecord) => record.execution_id || record.id;
    for (const record of snapshotUpdates ?? pending) {
      const index = history.findIndex(existing => key(existing) === key(record));
      if (index >= 0) history[index] = appendLog([history[index]], record)[0];
      else history.push(record);
    }
    // A queued pre-snapshot live frame can arrive late. Order before applying the
    // record limit so that such a frame cannot evict a newer authoritative row.
    history.sort((a, b) => a.timestamp.localeCompare(b.timestamp) || (a.id || '').localeCompare(b.id || ''));
    if (timer !== undefined) clearTimeout(timer);
    timer = undefined; pending = []; records.value = boundedLogs(history); cancelSnapshot();
  }
  onScopeDispose(clear);
  return { records, append, clear, replace, beginSnapshot, cancelSnapshot };
}
