import { describe, it, expect, vi, afterEach } from 'vitest'
vi.mock('@/stores/user', () => ({ useUserStore: () => ({ accessToken: '隔离凭据' }) }))
import { LogWebSocketManager } from './logWebSocket'
class Socket {
  static OPEN = 1; static CONNECTING = 0; static instances: Socket[] = []
  readyState = 0; onopen?: () => void; onclose?: () => void; onerror?: (e: Error) => void; onmessage?: (e: {data: string}) => void
  constructor(public url: string) { Socket.instances.push(this) }
  close() { this.readyState = 3; this.onclose?.() }
  open() { this.readyState = 1; this.onopen?.() }
}
afterEach(() => { vi.unstubAllGlobals(); vi.useRealTimers(); Socket.instances = [] })
describe('功能日志连接生命周期', () => {
  it('预注册接收器不丢失，旧socket关闭不清理新连接', async () => {
    vi.useFakeTimers(); vi.stubGlobal('window', {location: {protocol:'http:',host:'隔离.test'}}); vi.stubGlobal('WebSocket', Socket)
    const manager = new LogWebSocketManager(); const handler = vi.fn(); manager.on(handler)
    const first = manager.connect('旧套'); const old = Socket.instances[0]
    const second = manager.connect('新套'); const current = Socket.instances[1]; current.open()
    expect(await first).toBe(false); expect(await second).toBe(true)
    old.onclose?.(); expect(manager.isConnected()).toBe(true)
    current.onmessage?.({data:JSON.stringify({type:'test_suite_log',suite_id:'新套',data:{message:'功能日志'}})})
    expect(handler).toHaveBeenCalledTimes(1)
    current.close(); manager.disconnect(); vi.advanceTimersByTime(30000)
    expect(Socket.instances).toHaveLength(2); expect(manager.getCurrentSuiteId()).toBeNull()
  })
  it('重连保留接收器并在连接超时后结束等待', async () => {
    vi.useFakeTimers(); vi.stubGlobal('window', {location: {protocol:'http:',host:'隔离.test'}}); vi.stubGlobal('WebSocket', Socket)
    const manager = new LogWebSocketManager(); const handler = vi.fn(); manager.on(handler)
    const connected = manager.connect('功能套'); Socket.instances[0].open(); expect(await connected).toBe(true)
    Socket.instances[0].close(); vi.advanceTimersByTime(3000); const next = Socket.instances[1]; next.open()
    next.onmessage?.({data:JSON.stringify({type:'connected'})}); expect(handler).toHaveBeenCalledTimes(1)
    manager.disconnect(); const timeout = manager.connect('超时套'); vi.advanceTimersByTime(10000); expect(await timeout).toBe(false)
    manager.disconnect(); expect(vi.getTimerCount()).toBe(0)
  })
})
