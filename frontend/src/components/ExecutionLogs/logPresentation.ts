import type { LogRecord } from './boundedLogs';
export interface DisplayLogLine { text: string; timestamp: string; lastTimestamp: string; count: number; execution: string; }
/** Presentation only: never mutates records or the server's raw evidence. */
export function displayLogLines(records: LogRecord[], fold: boolean): DisplayLogLine[] {
  const result: DisplayLogLine[] = [];
  for (const record of records) {
    const execution = record.execution_id || record.id || '';
    const timestamp = record.timestamp.slice(11, 23);
    for (const text of record.message.split('\n')) {
      const previous = result.at(-1);
      if (fold && previous && previous.text === text && previous.execution === execution) {
        previous.count++; previous.lastTimestamp = timestamp;
      } else result.push({ text, timestamp, lastTimestamp: timestamp, count: 1, execution });
    }
  }
  return result;
}
