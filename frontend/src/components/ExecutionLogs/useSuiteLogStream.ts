import { computed, onScopeDispose, ref, shallowRef } from 'vue'
import { testSuiteApi } from '@/api/testSuite'
import { logWebSocketManager, type LogMessageHandler } from '@/utils/logWebSocket'
import { useBoundedLogs } from './useBoundedLogs'

interface LogTarget {
  suiteId: string
  executionId?: string
  logId?: string
  live: boolean
}
type ConnectionState = 'idle' | 'connecting' | 'connected' | 'reconnecting' | 'unavailable' | 'denied'
type HistoryState = 'idle' | 'loading' | 'ready' | 'error'
interface StreamDependencies {
  transport: Pick<typeof logWebSocketManager, 'on' | 'off' | 'connect' | 'disconnect'>
  fetchHistory: typeof testSuiteApi.getSuiteLogs
}

/** 每次服务端确认订阅后重读权威历史，再按字符位置合并有界实时尾部。 */
export function useSuiteLogStream(dependencies: StreamDependencies = {
  transport: logWebSocketManager, fetchHistory: testSuiteApi.getSuiteLogs,
}) {
  const buffer = useBoundedLogs()
  const connection = ref<ConnectionState>('idle')
  const history = ref<HistoryState>('idle')
  const interrupted = ref(false)
  const target = shallowRef<LogTarget>()
  let handler: LogMessageHandler | undefined
  let session = 0, request = 0
  let disposed = false
  const loading = computed(() => history.value === 'loading')
  const status = computed<{ type: 'info' | 'warning' | 'error'; message: string } | null>(() => {
    if (!target.value) return null
    if (connection.value === 'reconnecting') return { type: 'warning', message: '实时日志连接中断，可能有遗漏；正在重连，连接后将重新读取服务器历史。' }
    if (connection.value === 'denied') return { type: 'error', message: '实时日志访问被拒绝，已停止自动重连；请确认登录状态和测试套读取权限后点击刷新重试。' }
    if (connection.value === 'unavailable') return { type: 'error', message: '实时日志连接不可用，当前视窗可能不完整；请点击刷新重试，服务器历史仅包含已接收的日志。' }
    if (history.value === 'error') return { type: 'error', message: '历史日志同步失败，当前视窗可能不完整；请点击刷新重试。服务器历史仅包含已接收的日志。' }
    if (connection.value === 'connecting') return { type: 'info', message: '正在连接实时日志并读取服务器历史…' }
    if (history.value === 'loading') return { type: 'info', message: interrupted.value ? '实时连接已恢复，正在重新同步服务器历史尾部…' : '正在同步服务器历史日志…' }
    if (connection.value === 'connected' && history.value === 'ready') return { type: 'info', message: interrupted.value ? '实时连接已恢复，最近历史已重新同步；视窗仅显示有界尾部，已接收日志保留在服务器历史中。' : '实时连接已建立，最近历史已同步；视窗仅显示有界尾部。' }
    if (connection.value === 'connected') return { type: 'warning', message: '视窗已清空，当前仅显示新的实时日志；点击刷新可重新同步历史尾部。' }
    return null
  })

  async function loadHistory() {
    if (!target.value || disposed) return
    const currentTarget = target.value, currentSession = session, currentRequest = ++request
    const current = () => !disposed && currentSession === session && currentRequest === request
    buffer.beginSnapshot()
    history.value = 'loading'
    try {
      const response = await dependencies.fetchHistory(currentTarget.suiteId, {
        skip: 0, limit: 20,
        ...(currentTarget.logId ? { logId: currentTarget.logId } : { executionId: currentTarget.executionId }),
      })
      if (!current()) return
      buffer.replace(response.items || [])
      history.value = 'ready'
    } catch (error) {
      if (!current()) return
      console.error('加载测试套日志失败:', error)
      buffer.cancelSnapshot()
      history.value = 'error'
    }
  }

  async function connect() {
    if (!target.value?.live || disposed) return
    const currentSession = session
    connection.value = 'connecting'
    const connected = await dependencies.transport.connect(target.value.suiteId)
    // A close notification may already have scheduled a retry. Never hide it.
    if (!disposed && currentSession === session && !connected && connection.value === 'connecting') connection.value = 'unavailable'
  }

  function close() {
    session++; request++
    if (handler) {
      dependencies.transport.off(handler)
      handler = undefined
      dependencies.transport.disconnect()
    }
    target.value = undefined
    connection.value = 'idle'; history.value = 'idle'; interrupted.value = false
    buffer.clear()
  }

  function open(next: LogTarget) {
    if (disposed) return
    close()
    target.value = { ...next }
    const currentSession = session
    if (next.live) {
      handler = event => {
        if (disposed || currentSession !== session || !target.value) return
        if (event.suite_id && event.suite_id !== target.value.suiteId) return
        if (event.type === 'connected') {
          connection.value = 'connected'
          // Invalidates any earlier HTTP snapshot, including one started before subscribing.
          void loadHistory()
        } else if (event.type === 'disconnected') {
          request++
          buffer.cancelSnapshot()
          history.value = 'idle'
          interrupted.value = true
          connection.value = event.closeCode === 1008 ? 'denied' : event.reconnecting ? 'reconnecting' : 'unavailable'
        } else if (event.type === 'test_suite_log' && event.suite_id === target.value.suiteId && event.data
          && (!target.value.executionId || event.data.execution_id === target.value.executionId)
          && (!target.value.logId || event.data.id === target.value.logId)) {
          buffer.append(event.data)
        }
      }
      dependencies.transport.on(handler)
      void connect()
    }
    // Keep persisted history available even if the live connection never succeeds.
    void loadHistory()
  }

  async function refresh() {
    if (target.value?.live && (connection.value === 'unavailable' || connection.value === 'denied')) void connect()
    await loadHistory()
  }
  function clear() {
    request++
    history.value = 'idle'
    buffer.clear()
  }
  onScopeDispose(() => { close(); disposed = true })
  return { records: buffer.records, loading, status, open, close, refresh, clear }
}
