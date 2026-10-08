import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
vi.mock('@/stores/user', () => ({ useUserStore: () => ({ accessToken: 'auth-test' }) }))
import { ScriptJobSocket, type ScriptLogEvent } from './scriptJobSocket'

class Socket {
  static all: Socket[] = []
  onopen: (() => void) | null = null
  onclose: ((event: { code: number }) => void) | null = null
  onmessage: ((event: { data: unknown }) => void) | null = null
  onerror: (() => void) | null = null
  send = vi.fn()
  close = vi.fn((code = 1000) => this.onclose?.({ code }))
  constructor(public url: string) { Socket.all.push(this) }
  event(data: unknown) { this.onmessage?.({ data: JSON.stringify(data) }) }
}
beforeEach(() => {
  vi.useFakeTimers(); Socket.all = []
  vi.stubGlobal('WebSocket', Socket); vi.stubGlobal('window', { location: { protocol: 'http:', host: 'ats.local' } })
})
afterEach(() => { vi.useRealTimers(); vi.unstubAllGlobals() })
const target = { jobId: 'job/a', executionId: 'run/a', live: true }
describe('脚本日志连接生命周期', () => {
  it('uses encoded immutable identity and requires subscription acknowledgement after socket open', async () => {
    const transport = new ScriptJobSocket(), received = vi.fn<[ScriptLogEvent], void>()
    transport.connect(target, received)
    const socket = Socket.all[0]
    expect(socket.url).toContain('job_id=job%2Fa&execution_id=run%2Fa')
    socket.onopen?.()
    await vi.advanceTimersByTimeAsync(10000)
    expect(socket.close).toHaveBeenCalled()
    expect(received).toHaveBeenCalledWith(expect.objectContaining({ type: 'disconnected', reconnecting: true }))
    await vi.advanceTimersByTimeAsync(3000)
    expect(Socket.all).toHaveLength(2)
    transport.disconnect()
  })
  it('uses server pings for liveness and reconnects a silently lost socket', async () => {
    const transport = new ScriptJobSocket()
    transport.connect(target, vi.fn())
    const socket = Socket.all[0]
    socket.event({ type: 'connected', job_id: target.jobId, execution_id: target.executionId })
    await vi.advanceTimersByTimeAsync(30000); socket.event({ type: 'ping' })
    expect(socket.send).toHaveBeenCalledWith('{"type":"pong"}')
    await vi.advanceTimersByTimeAsync(60000)
    expect(socket.close).not.toHaveBeenCalled()
    await vi.advanceTimersByTimeAsync(30000)
    expect(socket.close).toHaveBeenCalled()
    transport.disconnect()
  })
  it('does not retry denied subscriptions and clears reconnect timers after dismissal', async () => {
    const transport = new ScriptJobSocket()
    transport.connect(target, vi.fn()); Socket.all[0].close(1008)
    await vi.advanceTimersByTimeAsync(30000)
    expect(Socket.all).toHaveLength(1)
    transport.connect(target, vi.fn()); Socket.all[1].close(1013)
    transport.disconnect(); await vi.advanceTimersByTimeAsync(30000)
    expect(Socket.all).toHaveLength(2)
  })
  it('rejects oversized frames before parsing and ignores old sockets after selection changes', () => {
    const transport = new ScriptJobSocket(), handler = vi.fn()
    transport.connect(target, handler)
    const first = Socket.all[0]
    first.onmessage?.({ data: 'x'.repeat(256 * 1024 + 1) })
    expect(first.close).toHaveBeenCalled()
    transport.connect({ ...target, executionId: 'run-b' }, handler)
    handler.mockClear(); first.event({ type: 'script_job_log' })
    expect(handler).not.toHaveBeenCalled()
    transport.disconnect()
  })
})
