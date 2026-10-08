import { describe, it, expect, vi, afterEach } from 'vitest'
vi.mock('@/stores/user', () => ({ useUserStore: () => ({ accessToken: '隔离凭据' }) }))
import { LogWebSocketManager } from './logWebSocket'
class Socket {
  static OPEN = 1; static CONNECTING = 0; static instances: Socket[] = []
  readyState = 0; onopen?: () => void; onclose?: (event?: { code: number; reason: string }) => void; onerror?: (e: Error) => void; onmessage?: (e: {data: string}) => void
  constructor(public url: string) { Socket.instances.push(this) }
  close(code = 1006, reason = '') { this.readyState = 3; this.onclose?.({ code, reason }) }
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
    next.onmessage?.({data:JSON.stringify({type:'connected'})}); expect(handler).toHaveBeenCalledTimes(2)
    manager.disconnect(); const timeout = manager.connect('超时套'); vi.advanceTimersByTime(10000); expect(await timeout).toBe(false)
    manager.disconnect(); expect(vi.getTimerCount()).toBe(0)
  })
})

describe('功能日志丢帧可见性', () => {
  it('1013慢订阅关闭传递恢复状态，断开前的旧socket事件不能影响重连', async () => {
    vi.useFakeTimers(); vi.stubGlobal('window', { location: { protocol: 'http:', host: '隔离.test' } }); vi.stubGlobal('WebSocket', Socket)
    const manager = new LogWebSocketManager(), handler = vi.fn(); manager.on(handler)
    const connected = manager.connect('功能套'); const old = Socket.instances[0]; old.open(); await connected
    old.close(1013, 'Log buffer full; reconnect and reload history')
    expect(handler).toHaveBeenLastCalledWith({ type: 'disconnected', suite_id: '功能套', closeCode: 1013,
      message: 'Log buffer full; reconnect and reload history', reconnecting: true })
    vi.advanceTimersByTime(3000); Socket.instances[1].open()
    old.onmessage?.({ data: JSON.stringify({ type: 'connected' }) }); old.onclose?.()
    expect(handler).toHaveBeenCalledTimes(1)
    manager.disconnect()
  })
  it('连续重连失败达到上限时显式报告不可用', async () => {
    vi.useFakeTimers(); vi.stubGlobal('window', { location: { protocol: 'http:', host: '隔离.test' } }); vi.stubGlobal('WebSocket', Socket)
    const manager = new LogWebSocketManager(), handler = vi.fn(); manager.on(handler)
    void manager.connect('功能套')
    for (let i = 0; i < 6; i++) { Socket.instances[i].close(); vi.advanceTimersByTime(3000) }
    expect(Socket.instances).toHaveLength(6)
    expect(handler).toHaveBeenLastCalledWith(expect.objectContaining({ type: 'disconnected', reconnecting: false }))
    manager.disconnect(); expect(vi.getTimerCount()).toBe(0)
  })
  it('异常大帧触发重连和历史恢复而不是静默漏日志', async () => {
    vi.useFakeTimers(); vi.stubGlobal('window', { location: { protocol: 'http:', host: '隔离.test' } }); vi.stubGlobal('WebSocket', Socket)
    const error = vi.spyOn(console, 'error').mockImplementation(() => {})
    const manager = new LogWebSocketManager(), handler = vi.fn(); manager.on(handler)
    const connected = manager.connect('功能套'); Socket.instances[0].open(); await connected
    Socket.instances[0].onmessage?.({ data: 'x'.repeat(256 * 1024 + 1) })
    expect(handler).toHaveBeenLastCalledWith(expect.objectContaining({ type: 'disconnected', reconnecting: true, closeCode: 4000 }))
    manager.disconnect(); error.mockRestore()
  })
  it('重连时构造socket失败会停止等待并显式报告不可用', async () => {
    vi.useFakeTimers(); vi.stubGlobal('window', { location: { protocol: 'http:', host: '隔离.test' } }); vi.stubGlobal('WebSocket', Socket)
    const error = vi.spyOn(console, 'error').mockImplementation(() => {})
    const manager = new LogWebSocketManager(), handler = vi.fn(); manager.on(handler)
    const connected = manager.connect('功能套'); Socket.instances[0].open(); await connected
    Socket.instances[0].close(1013)
    vi.stubGlobal('WebSocket', class { static OPEN = 1; static CONNECTING = 0; constructor() { throw new Error('WebSocket unavailable') } })
    vi.advanceTimersByTime(3000)
    expect(handler).toHaveBeenLastCalledWith({ type: 'disconnected', suite_id: '功能套', reconnecting: false })
    manager.disconnect(); error.mockRestore()
  })

  it('升级成功后1008拒绝鉴权也不自动重试，需用户重新尝试', async () => {
    vi.useFakeTimers(); vi.stubGlobal('window', { location: { protocol: 'http:', host: '隔离.test' } }); vi.stubGlobal('WebSocket', Socket)
    const manager = new LogWebSocketManager(), handler = vi.fn(); manager.on(handler)
    const connected = manager.connect('功能套'); Socket.instances[0].open(); await connected
    Socket.instances[0].close(1008, 'Suite not found or access denied')
    vi.advanceTimersByTime(60000)
    expect(Socket.instances).toHaveLength(1)
    expect(handler).toHaveBeenLastCalledWith(expect.objectContaining({ type: 'disconnected', closeCode: 1008, reconnecting: false }))
    manager.disconnect()
  })
  it('仅升级成功、未收到服务端订阅确认时也受重试上限约束', async () => {
    vi.useFakeTimers(); vi.stubGlobal('window', { location: { protocol: 'http:', host: '隔离.test' } }); vi.stubGlobal('WebSocket', Socket)
    const manager = new LogWebSocketManager(), handler = vi.fn(); manager.on(handler)
    void manager.connect('功能套')
    for (let i = 0; i < 6; i++) { Socket.instances[i].open(); Socket.instances[i].close(1013); vi.advanceTimersByTime(3000) }
    expect(Socket.instances).toHaveLength(6)
    expect(handler).toHaveBeenLastCalledWith(expect.objectContaining({ type: 'disconnected', reconnecting: false }))
    manager.disconnect()
  })

})
