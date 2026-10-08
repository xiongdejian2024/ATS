import { useUserStore } from '@/stores/user'
import type { LogRecord } from '@/components/ExecutionLogs/boundedLogs'

export interface ScriptLogEvent {
  type: 'connected' | 'disconnected' | 'script_job_log' | 'ping' | 'pong'
  job_id?: string
  execution_id?: string
  data?: LogRecord
  closeCode?: number
  reconnecting?: boolean
}
export interface ScriptLogTarget { jobId: string; executionId: string; live: boolean }
export interface ScriptLogTransport {
  connect(target: ScriptLogTarget, handler: (event: ScriptLogEvent) => void): void
  disconnect(): void
}
/** A socket belongs to one viewer and one immutable run; it cannot steal suite subscriptions. */
export class ScriptJobSocket implements ScriptLogTransport {
  private socket: WebSocket | null = null
  private retry: ReturnType<typeof setTimeout> | undefined
  private timeout: ReturnType<typeof setTimeout> | undefined
  private generation = 0
  connect(target: ScriptLogTarget, handler: (event: ScriptLogEvent) => void) {
    this.disconnect()
    const generation = this.generation
    let attempts = 0
    const start = () => {
      if (generation !== this.generation) return
      const token = useUserStore().accessToken
      if (!token) { handler({ type: 'disconnected', closeCode: 1008, reconnecting: false }); return }
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
      const query = new URLSearchParams({ token, job_id: target.jobId, execution_id: target.executionId })
      try {
        const socket = new WebSocket(`${protocol}//${window.location.host}/ws/script-jobs?${query}`)
        let subscribed = false
        this.socket = socket
        const current = () => generation === this.generation && this.socket === socket
        const watchdog = (milliseconds: number) => {
          if (this.timeout) clearTimeout(this.timeout)
          this.timeout = setTimeout(() => { if (current()) socket.close(4000, 'Log subscription timed out'); }, milliseconds)
        }
        // Opening TCP/WebSocket does not establish an authorized subscription.
        watchdog(10000)
        socket.onmessage = event => {
          if (!current()) return
          try {
            if (typeof event.data !== 'string' || event.data.length > 256 * 1024) throw new Error('Oversized frame')
            const message = JSON.parse(event.data) as ScriptLogEvent
            if (message.type === 'ping') { if (subscribed) watchdog(90000); socket.send(JSON.stringify({ type: 'pong' })); return }
            if (message.type === 'connected') {
              if (message.job_id !== target.jobId || message.execution_id !== target.executionId) throw new Error('Unexpected subscription')
              subscribed = true; attempts = 0; watchdog(90000)
            }
            if (message.type === 'script_job_log' && subscribed) watchdog(90000)
            handler(message)
          } catch { socket.close(4000, 'Reload bounded log history') }
        }
        socket.onerror = () => { if (current()) socket.close() }
        socket.onclose = event => {
          if (!current()) return
          if (this.timeout) clearTimeout(this.timeout)
          this.socket = null
          const reconnecting = event.code !== 1008 && attempts < 5
          handler({ type: 'disconnected', closeCode: event.code, reconnecting })
          if (reconnecting) { attempts++; this.retry = setTimeout(start, 3000) }
        }
      } catch { handler({ type: 'disconnected', reconnecting: false }) }
    }
    start()
  }
  disconnect() {
    this.generation++
    if (this.retry) clearTimeout(this.retry)
    if (this.timeout) clearTimeout(this.timeout)
    this.retry = undefined; this.timeout = undefined
    const previous = this.socket; this.socket = null
    previous?.close()
  }
}
