import { describe, expect, it, vi } from 'vitest'
import { effectScope } from 'vue'
vi.mock('@/utils/api', () => ({ apiClient: { post: vi.fn() } }))
import { useRawLogDownload, type LogChunk, type LogWriter, type RawLogTarget } from './useRawLogDownload'
type Fetch = (target: RawLogTarget, cursor: string | null, signal: AbortSignal) => Promise<LogChunk>

const target = { endpoint: '/test-plans/suites/suite/logs/export', filename: 'suite', executionId: 'frozen-run' }
const chunk = (part: number, complete = true, content = '  😀中\r\n\t'): LogChunk => ({
  part, complete, content, nextCursor: complete ? null : `cursor-${part}`, recordCount: 2, snapshotAt: '2026-10-08', maxChunkBytes: 262144,
})
function deferred<T>() {
  let resolve!: (value: T) => void
  const promise = new Promise<T>(yes => { resolve = yes })
  return { resolve, promise }
}
function setup(fetch = vi.fn<Parameters<Fetch>, ReturnType<Fetch>>(async () => chunk(1))) {
  const savePart = vi.fn(), scope = effectScope()
  const download = scope.run(() => useRawLogDownload({ fetch, savePart }))!
  download.open(target)
  return { download, fetch, savePart, scope }
}
function file() {
  const writer = { write: vi.fn(async (_value: Uint8Array) => {}), close: vi.fn(async () => {}), abort: vi.fn(async () => {}) }
  const picker = vi.fn(async () => ({ createWritable: vi.fn(async () => writer as LogWriter) }))
  return { writer, picker }
}

describe('bounded raw log download', () => {
  it('writes scalar-safe chunks sequentially with file backpressure, preserving raw whitespace', async () => {
    const first = chunk(1, false), second = chunk(2, true, 'END \n\n')
    const state = setup(vi.fn().mockResolvedValueOnce(first).mockResolvedValueOnce(second))
    const { writer, picker } = file(), pause = deferred<void>()
    writer.write.mockImplementationOnce(() => pause.promise)
    const result = state.download.saveFull(picker)
    await vi.waitFor(() => expect(writer.write).toHaveBeenCalledTimes(1))
    expect(state.fetch).toHaveBeenCalledTimes(1)
    pause.resolve(); await result
    expect(state.fetch.mock.calls[1][1]).toBe('cursor-1')
    expect(writer.write.mock.calls.map(call => new TextDecoder().decode(call[0]))).toEqual([first.content, second.content])
    expect(writer.close).toHaveBeenCalledOnce()
    expect(writer.abort).not.toHaveBeenCalled()
    expect(state.download.complete.value).toBe(true)
    expect(state.savePart).not.toHaveBeenCalled()
    state.scope.stop()
  })

  it('downloads one bounded numbered part per click and retries an error at the same cursor', async () => {
    const fetch = vi.fn().mockResolvedValueOnce(chunk(1, false)).mockRejectedValueOnce(new Error('offline')).mockResolvedValueOnce(chunk(2))
    const state = setup(fetch)
    await state.download.nextPart()
    expect(fetch).toHaveBeenCalledTimes(1)
    expect(state.savePart.mock.calls[0][1]).toBe('suite-20261008.part000001.log')
    expect(new TextDecoder().decode(state.savePart.mock.calls[0][0])).toBe(chunk(1).content)
    await state.download.nextPart()
    expect(state.download.parts.value).toBe(1)
    expect(state.download.complete.value).toBe(false)
    await state.download.nextPart()
    expect(fetch.mock.calls.slice(1).map(call => call[1])).toEqual(['cursor-1', 'cursor-1'])
    expect(state.savePart.mock.calls[1][1]).toBe('suite-20261008.part000002.log')
    expect(state.download.complete.value).toBe(true)
    await state.download.nextPart()
    expect(fetch).toHaveBeenCalledTimes(3)
    state.scope.stop()
  })

  it('aborts and ignores old responses after closing or switching the selected execution', async () => {
    const pending = deferred<LogChunk>(), fetch = vi.fn<Parameters<Fetch>, ReturnType<Fetch>>(() => pending.promise)
    const state = setup(fetch)
    const saving = state.download.nextPart()
    const signal = fetch.mock.calls[0][2] as AbortSignal
    state.download.open({ ...target, executionId: 'new-run' })
    expect(signal.aborted).toBe(true)
    pending.resolve(chunk(1)); await saving
    expect(state.savePart).not.toHaveBeenCalled()
    expect(state.download.parts.value).toBe(0)
    state.scope.stop()
  })

  it('suppresses repeated clicks and aborts a writer on component disposal', async () => {
    const pending = deferred<LogChunk>(), fetch = vi.fn<Parameters<Fetch>, ReturnType<Fetch>>(() => pending.promise)
    const state = setup(fetch), { writer, picker } = file()
    const saving = state.download.saveFull(picker)
    await vi.waitFor(() => expect(fetch).toHaveBeenCalledOnce())
    await state.download.saveFull(picker); await state.download.nextPart()
    expect(picker).toHaveBeenCalledOnce()
    state.scope.stop(); pending.resolve(chunk(1)); await saving
    expect(writer.abort).toHaveBeenCalledOnce()
    expect(writer.write).not.toHaveBeenCalled()
    expect(writer.close).not.toHaveBeenCalled()
  })

  it('resets a previous success before a failed repeat and can then fall back to parts', async () => {
    const fetch = vi.fn().mockResolvedValueOnce(chunk(1)).mockRejectedValueOnce(new Error('lost connection')).mockResolvedValueOnce(chunk(1))
    const state = setup(fetch), first = file(), second = file()
    await state.download.saveFull(first.picker)
    expect(state.download.complete.value).toBe(true)
    await state.download.saveFull(second.picker)
    expect(second.writer.abort).toHaveBeenCalledOnce()
    expect(state.download.complete.value).toBe(false)
    expect(state.download.parts.value).toBe(0)
    expect(state.download.error.value).toBe('lost connection')
    await state.download.nextPart()
    expect(state.savePart.mock.calls[0][1]).toBe('suite-20261008.part000001.log')
    state.scope.stop()
  })

  it('clears prior completeness when the browser denies a repeated picker', async () => {
    const state = setup(), destination = file()
    await state.download.saveFull(destination.picker)
    expect(state.download.complete.value).toBe(true)
    await state.download.saveFull(async () => { throw new DOMException('picker denied', 'SecurityError') })
    expect(state.download.complete.value).toBe(false)
    expect(state.download.parts.value).toBe(0)
    expect(state.download.error.value).toBe('picker denied')
    await state.download.nextPart()
    expect(state.savePart).toHaveBeenCalledOnce()
    state.scope.stop()
  })

  it('does not issue a request after cancelling the file picker or changing selection while it is pending', async () => {
    const state = setup(), picked = deferred<Awaited<ReturnType<ReturnType<typeof file>['picker']>>>()
    const saving = state.download.saveFull(() => picked.promise)
    state.download.open(null)
    picked.resolve(await file().picker()); await saving
    expect(state.fetch).not.toHaveBeenCalled()
    state.download.open(target)
    await state.download.saveFull(async () => { throw new DOMException('cancelled', 'AbortError') })
    expect(state.download.error.value).toBe('')
    expect(state.download.busy.value).toBe(false)
    state.scope.stop()
  })

  it.each([chunk(2), chunk(1, true, '😀'.repeat(65537)), { ...chunk(1, false), nextCursor: null }])('rejects invalid, oversized or incomplete-success chunks', async response => {
    const state = setup(vi.fn<Parameters<Fetch>, ReturnType<Fetch>>(async () => response))
    await state.download.nextPart()
    expect(state.savePart).not.toHaveBeenCalled()
    expect(state.download.complete.value).toBe(false)
    expect(state.download.error.value).not.toBe('')
    state.scope.stop()
  })

  it('rejects an accidental snapshot switch between numbered parts', async () => {
    const state = setup(vi.fn().mockResolvedValueOnce(chunk(1, false)).mockResolvedValueOnce({ ...chunk(2), snapshotAt: 'another-snapshot' }))
    await state.download.nextPart(); await state.download.nextPart()
    expect(state.savePart).toHaveBeenCalledOnce()
    expect(state.download.complete.value).toBe(false)
    expect(state.download.parts.value).toBe(1)
    state.scope.stop()
  })
})
