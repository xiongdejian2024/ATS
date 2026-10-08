import { computed, onScopeDispose, ref } from 'vue'
import { scriptJobsApi } from '@/api/scriptJobs'
import { useBoundedLogs } from '@/components/ExecutionLogs/useBoundedLogs'
import { ScriptJobSocket, type ScriptLogTarget, type ScriptLogTransport } from './scriptJobSocket'

export function useScriptJobLogs(dependencies: { transport: ScriptLogTransport; fetch: typeof scriptJobsApi.logs } = { transport: new ScriptJobSocket(), fetch: scriptJobsApi.logs }) {
  const buffer = useBoundedLogs(), loading = ref(false), connection = ref('idle'), history = ref('idle')
  let target: ScriptLogTarget | null = null, generation = 0, revision = 0, request: AbortController | undefined, disposed = false
  const status = computed(() => {
    if (connection.value === 'denied') return { type: 'error' as const, message: '实时日志访问被拒绝，已停止重连；请检查登录与项目权限后刷新。' }
    if (connection.value === 'reconnecting') return { type: 'warning' as const, message: '实时连接中断，可能有遗漏；恢复连接后将重新同步服务器日志。' }
    if (connection.value === 'unavailable') return { type: 'error' as const, message: '实时日志连接不可用，当前视窗可能不完整。请刷新重试。' }
    if (history.value === 'error') return { type: 'error' as const, message: '服务器日志同步失败，当前视窗可能不完整。请刷新重试。' }
    if (loading.value || connection.value === 'connecting') return { type: 'info' as const, message: '正在连接并同步服务器日志…' }
    return { type: 'info' as const, message: target?.live ? '日志实时更新；仅显示有界尾部，完整已接收日志可逐段保存。' : '本次执行的历史日志；仅显示有界尾部，完整已接收日志可逐段保存。' }
  })
  async function load() {
    if (!target || disposed) return
    request?.abort(); request = new AbortController()
    const selected = target, current = generation, currentRevision = ++revision
    buffer.beginSnapshot(); loading.value = true; history.value = 'loading'
    try {
      const data = await dependencies.fetch(selected.jobId, selected.executionId, request.signal)
      if (disposed || current !== generation || currentRevision !== revision) return
      buffer.replace(data.items); history.value = 'ready'
    } catch {
      if (disposed || current !== generation || currentRevision !== revision) return
      buffer.cancelSnapshot(); history.value = 'error'
    } finally { if (!disposed && current === generation && currentRevision === revision) loading.value = false }
  }
  function connect() {
    if (!target?.live || disposed) return
    const current = generation
    connection.value = 'connecting'
    dependencies.transport.connect(target, event => {
      if (disposed || current !== generation || !target) return
      if (event.job_id && event.job_id !== target.jobId || event.execution_id && event.execution_id !== target.executionId) return
      if (event.type === 'connected') { connection.value = 'connected'; void load() }
      else if (event.type === 'disconnected') {
        revision++; request?.abort(); buffer.cancelSnapshot(); loading.value = false
        connection.value = event.closeCode === 1008 ? 'denied' : event.reconnecting ? 'reconnecting' : 'unavailable'
      } else if (event.type === 'script_job_log' && event.job_id === target.jobId && event.execution_id === target.executionId && event.data
        && (!event.data.execution_id || event.data.execution_id === target.executionId)) buffer.append(event.data)
    })
  }
  function close() {
    generation++; revision++; request?.abort(); request = undefined; dependencies.transport.disconnect()
    target = null; loading.value = false; connection.value = 'idle'; history.value = 'idle'; buffer.clear()
  }
  function open(value: ScriptLogTarget) {
    if (disposed) return
    close(); target = { ...value }; connect(); void load()
  }
  async function refresh() {
    if (['denied', 'unavailable'].includes(connection.value)) connect()
    await load()
  }
  onScopeDispose(() => { close(); disposed = true })
  return { records: buffer.records, loading, status, open, close, refresh }
}
