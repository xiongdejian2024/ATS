import { onScopeDispose, ref } from 'vue'
import { apiClient } from '@/utils/api'

export interface RawLogTarget { endpoint: string; filename: string; executionId?: string; logId?: string }
export interface LogChunk {
  content: string; nextCursor: string | null; complete: boolean; part: number
  recordCount: number; snapshotAt: string; maxChunkBytes: number
}
export interface LogWriter { write(data: Uint8Array): Promise<void>; close(): Promise<void>; abort(): Promise<void> }
export type LogFilePicker = (options: { suggestedName: string }) => Promise<{ createWritable(): Promise<LogWriter> }>
const MAX_CHUNK_BYTES = 256 * 1024

function savePart(bytes: Uint8Array, filename: string) {
  const url = URL.createObjectURL(new Blob([bytes], { type: 'text/plain;charset=utf-8' }))
  const link = document.createElement('a')
  link.href = url; link.download = filename; link.click()
  // Release this part before another interaction; never retain an array of parts.
  setTimeout(() => URL.revokeObjectURL(url), 0)
}

const defaults = {
  fetch: (target: RawLogTarget, cursor: string | null, signal: AbortSignal): Promise<LogChunk> =>
    apiClient.post(target.endpoint, cursor ? { cursor } : { executionId: target.executionId, logId: target.logId }, { signal }),
  savePart,
}

/** One bounded response at a time, backpressure from the destination file writer. */
export function useRawLogDownload(dependencies = defaults) {
  const busy = ref(false), complete = ref(false), parts = ref(0), snapshotAt = ref(''), error = ref('')
  let target: RawLogTarget | null = null, cursor: string | null = null, generation = 0
  let request: AbortController | null = null, writer: LogWriter | null = null

  function cancel() {
    generation++; request?.abort(); request = null
    const pendingWriter = writer; writer = null
    if (pendingWriter) void pendingWriter.abort().catch(() => {})
    busy.value = false
  }
  function open(value: RawLogTarget | null) {
    cancel(); target = value ? { ...value } : null; cursor = null
    complete.value = false; parts.value = 0; snapshotAt.value = ''; error.value = ''
  }
  function fail(reason: any) {
    const detail = reason?.response?.data?.detail
    error.value = (typeof detail === 'string' ? detail : detail?.message) || reason?.message || '下载失败，请重试当前分段。'
  }
  function validate(chunk: LogChunk, expected: number) {
    if (typeof chunk.content !== 'string' || chunk.content.length > MAX_CHUNK_BYTES || chunk.part !== expected
        || !chunk.snapshotAt || (expected > 1 && chunk.snapshotAt !== snapshotAt.value)
        || (!chunk.complete && !chunk.nextCursor) || (chunk.complete && chunk.nextCursor)) {
      throw new Error('日志分段顺序或大小异常，下载已中止。')
    }
    const bytes = new TextEncoder().encode(chunk.content)
    if (bytes.byteLength > MAX_CHUNK_BYTES) throw new Error('日志分段超出大小上限，下载已中止。')
    return bytes
  }

  async function nextPart() {
    if (!target || busy.value || complete.value) return
    const selected = { ...target }, current = generation
    request = new AbortController(); busy.value = true; error.value = ''
    try {
      const chunk = await dependencies.fetch(selected, cursor, request.signal)
      if (current !== generation) return
      const bytes = validate(chunk, parts.value + 1)
      const stamp = chunk.snapshotAt.replace(/[^0-9]/g, '')
      dependencies.savePart(bytes, `${selected.filename}-${stamp}.part${String(chunk.part).padStart(6, '0')}.log`)
      cursor = chunk.nextCursor; complete.value = chunk.complete; parts.value = chunk.part; snapshotAt.value = chunk.snapshotAt
    } catch (reason) { if (current === generation) fail(reason) }
    finally { if (current === generation) { busy.value = false; request = null } }
  }

  async function saveFull(picker: LogFilePicker) {
    if (!target || busy.value) return
    const selected = { ...target }, current = generation
    busy.value = true; error.value = ''
    complete.value = false; parts.value = 0; snapshotAt.value = ''; cursor = null
    let destination: LogWriter | null = null
    try {
      // The picker is called directly from the click, before any network await.
      const handle = await picker({ suggestedName: `${selected.filename}.log` })
      if (current !== generation) return
      destination = await handle.createWritable()
      if (current !== generation) { await destination.abort(); return }
      complete.value = false; parts.value = 0; snapshotAt.value = ''; cursor = null
      writer = destination; request = new AbortController()
      let next: string | null = null, expected = 1
      do {
        const chunk: LogChunk = await dependencies.fetch(selected, next, request.signal)
        if (current !== generation) return
        await destination.write(validate(chunk, expected))
        if (current !== generation) return
        parts.value = chunk.part; snapshotAt.value = chunk.snapshotAt
        next = chunk.nextCursor; expected++
      } while (next)
      await destination.close()
      if (current === generation) { writer = null; complete.value = true; cursor = null }
    } catch (reason: any) {
      if (destination && current === generation) { await destination.abort().catch(() => {}); writer = null }
      if (current === generation && destination) {
        complete.value = false; parts.value = 0; snapshotAt.value = ''; cursor = null
      }
      if (current === generation && reason?.name !== 'AbortError') fail(reason)
    } finally { if (current === generation) { busy.value = false; request = null } }
  }

  onScopeDispose(cancel)
  return { busy, complete, parts, snapshotAt, error, open, cancel, nextPart, saveFull }
}
