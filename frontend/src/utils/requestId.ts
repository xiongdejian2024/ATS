let sequence = 0
/** An idempotency key, not a credential. Also works on an intranet HTTP origin. */
export function createRequestId(): string {
  if (typeof globalThis.crypto?.randomUUID === 'function') return globalThis.crypto.randomUUID()
  if (typeof globalThis.crypto?.getRandomValues === 'function') {
    const bytes = globalThis.crypto.getRandomValues(new Uint8Array(16))
    return `req_${Array.from(bytes, byte => byte.toString(16).padStart(2, '0')).join('')}`
  }
  return `req_${Date.now().toString(36)}_${++sequence}_${Math.random().toString(36).slice(2)}`
}
