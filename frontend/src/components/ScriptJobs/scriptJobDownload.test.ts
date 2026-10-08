import { describe, expect, it, vi } from 'vitest'
import { effectScope } from 'vue'
vi.mock('@/utils/api', () => ({ apiClient: { post: vi.fn() } }))
import { scriptRunPath } from '@/api/scriptJobs'
import { useRawLogDownload, type LogChunk, type RawLogTarget } from '@/components/ExecutionLogs/useRawLogDownload'
import { deferred } from './scriptJobFixtures'

describe('script run frozen raw-log export', () => {
  it('aborts an interrupted file write when switching runs and cannot report stale success', async () => {
    const pending = deferred<void>(), chunk: LogChunk = { content: 'exact\r\n  output', part: 1, nextCursor: null, complete: true, recordCount: 1, snapshotAt: '2026-10-08', maxChunkBytes: 262144 }
    const fetch = vi.fn(async (_target: RawLogTarget, _cursor: string | null, _signal: AbortSignal) => chunk)
    const writer = { write: vi.fn(() => pending.promise), close: vi.fn(async () => {}), abort: vi.fn(async () => {}) }
    const picker = vi.fn(async () => ({ createWritable: async () => writer }))
    const scope = effectScope(), download = scope.run(() => useRawLogDownload({ fetch, savePart: vi.fn() }))!
    const old = { endpoint: `${scriptRunPath('job', 'old-run')}/logs/export`, filename: 'script-old-run' }
    download.open(old)
    const saving = download.saveFull(picker)
    await vi.waitFor(() => expect(writer.write).toHaveBeenCalledOnce())
    expect(fetch.mock.calls[0][0]).toEqual(old)
    download.open({ endpoint: `${scriptRunPath('job', 'new-run')}/logs/export`, filename: 'script-new-run' })
    expect(fetch.mock.calls[0][2].aborted).toBe(true)
    expect(writer.abort).toHaveBeenCalledOnce()
    pending.resolve(); await saving
    expect(writer.close).not.toHaveBeenCalled()
    expect(download.complete.value).toBe(false)
    expect(download.parts.value).toBe(0)
    scope.stop()
  })
})
