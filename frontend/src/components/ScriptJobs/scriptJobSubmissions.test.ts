import { afterEach, describe, expect, it, vi } from 'vitest'
import { createRequestId } from '@/utils/requestId'
import { createSubmissionStore } from './scriptJobSubmissions'
afterEach(() => { vi.unstubAllGlobals() })
describe('bounded idempotency identities', () => {
  it('works without crypto on an HTTP origin and keeps generated intents distinct', () => {
    vi.stubGlobal('crypto', undefined)
    const first = createRequestId(), second = createRequestId()
    expect(first).toMatch(/^req_/)
    expect(second).not.toBe(first)
  })
  it('restores only bounded identities as uncertain, never an in-flight spinner', () => {
    const rows = Array.from({ length: 100 }, (_, i) => [`["user","project","job-${i}"]`, `request-${i}`])
    const store = createSubmissionStore({ getItem: () => JSON.stringify(rows), setItem: vi.fn() })
    expect(store.entries.size).toBe(64)
    expect([...store.entries.values()].every(item => item.uncertain && !item.busy)).toBe(true)
  })
  it('reports unavailable persistence instead of promising reload protection', () => {
    const store = createSubmissionStore({ getItem: () => null, setItem: () => { throw new DOMException('blocked') } })
    store.entries.set('identity', { requestId: 'request', busy: true, uncertain: false }); store.save()
    expect(store.persistent.value).toBe(false)
    expect(store.entries.get('identity')?.requestId).toBe('request')
  })
})
