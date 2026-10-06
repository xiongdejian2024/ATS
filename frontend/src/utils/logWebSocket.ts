import { useUserStore } from '@/stores/user'

export interface LogMessage {
  type: 'test_suite_log' | 'connected' | 'ping' | 'pong'
  suite_id?: string
  data?: { id: string; message: string; timestamp: string; execution_id?: string; endOffset?: number; truncated?: boolean }
  message?: string
}
export type LogMessageHandler = (message: LogMessage) => void

export class LogWebSocketManager {
  private ws: WebSocket | null = null
  private suiteId: string | null = null
  private handlers = new Set<LogMessageHandler>()
  private reconnectAttempts = 0
  private reconnectTimer: ReturnType<typeof setTimeout> | undefined
  private pending: Promise<boolean> | undefined
  private generation = 0

  async connect(suiteId: string): Promise<boolean> {
    if (this.suiteId === suiteId && this.ws?.readyState === WebSocket.OPEN) return true
    if (this.suiteId === suiteId && this.ws?.readyState === WebSocket.CONNECTING && this.pending) return this.pending
    this.closeSocket()
    this.suiteId = suiteId
    const generation = this.generation
    const token = useUserStore().accessToken
    if (!token) { console.error('日志连接失败：缺少登录凭据'); return false }
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const url = `${protocol}//${window.location.host}/ws/client?token=${encodeURIComponent(token)}&suite_id=${encodeURIComponent(suiteId)}`
    this.pending = new Promise(resolve => {
      try {
        const socket = new WebSocket(url)
        this.ws = socket
        const current = () => generation === this.generation && socket === this.ws
        const timeout = setTimeout(() => { if (current() && socket.readyState === WebSocket.CONNECTING) socket.close(); resolve(false) }, 10000)
        socket.onopen = () => {
          clearTimeout(timeout)
          if (!current()) { resolve(false); return }
          this.reconnectAttempts = 0
          console.info('实时日志连接成功', suiteId)
          resolve(true)
        }
        socket.onmessage = event => {
          if (!current()) return
          try {
            // 服务端单条最多32768字符；异常大帧拒绝解析，避免额外JSON内存分配。
            if (typeof event.data !== 'string' || event.data.length > 256 * 1024) throw new Error('日志帧超过视窗传输上限')
            const message = JSON.parse(event.data) as LogMessage
            this.handlers.forEach(handler => {
              try { handler(message) } catch (error) { console.error('处理实时日志失败:', error) }
            })
          } catch (error) { console.error('解析实时日志失败:', error) }
        }
        socket.onerror = error => { clearTimeout(timeout); console.error('实时日志连接错误:', error); resolve(false) }
        socket.onclose = () => {
          clearTimeout(timeout); resolve(false)
          if (!current()) return
          this.ws = null; this.pending = undefined
          if (this.suiteId && this.reconnectAttempts < 5) {
            this.reconnectAttempts++
            console.info('实时日志重连', this.reconnectAttempts)
            this.reconnectTimer = setTimeout(() => {
              this.reconnectTimer = undefined
              if (generation === this.generation && this.suiteId) void this.connect(this.suiteId)
            }, 3000)
          }
        }
      } catch (error) { console.error('建立实时日志连接失败:', error); resolve(false) }
    })
    return this.pending
  }
  private closeSocket() {
    this.generation++
    if (this.reconnectTimer !== undefined) clearTimeout(this.reconnectTimer)
    this.reconnectTimer = undefined
    const previous = this.ws
    this.ws = null; this.pending = undefined
    previous?.close()
  }
  disconnect() { this.closeSocket(); this.suiteId = null; this.reconnectAttempts = 0; this.handlers.clear() }
  on(handler: LogMessageHandler) { this.handlers.add(handler) }
  off(handler: LogMessageHandler) { this.handlers.delete(handler) }
  isConnected(): boolean { return this.ws?.readyState === WebSocket.OPEN }
  getCurrentSuiteId(): string | null { return this.suiteId }
}
export const logWebSocketManager = new LogWebSocketManager()
