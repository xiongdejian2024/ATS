import type { ScriptJobConfig, ScriptJobRun, ScriptNode } from '@/api/scriptJobs'

export const emptyScriptJob = (projectId: string): ScriptJobConfig => ({ projectId, name: '', environmentId: '', mode: 'shell', script: '', command: '', args: [], workDir: '', timeoutSeconds: 3600 })
export function validateScriptJob(config: ScriptJobConfig): string {
  if (!config.projectId) return '请先选择项目。'
  if (!config.name.trim() || config.name.length > 255) return '请输入 1–255 字的作业名称。'
  if (!config.environmentId) return '请选择执行节点。'
  if (!Number.isInteger(config.timeoutSeconds) || config.timeoutSeconds < 1 || config.timeoutSeconds > 86400) return '超时必须为 1–86400 秒的整数。'
  if (config.workDir.includes('\0') || /^[\\/]|^[a-z]:/i.test(config.workDir) || config.workDir.split(/[\\/]/).includes('..')) return '工作目录必须在节点工作空间内，不能使用绝对路径或 ..。'
  if (config.workDir.length > 500) return '工作目录不能超过 500 字符。'
  if (config.mode === 'command' && (!config.command.trim() || config.command.includes('\0'))) return '请输入可执行文件路径或名称。'
  if (config.mode !== 'command' && !config.script.trim()) return '请输入脚本内容。'
  if (config.script.includes('\0')) return '脚本不能包含空字符。'
  if (new TextEncoder().encode(config.script).length > 65536) return '脚本不能超过 64 KiB。'
  if (config.command.length > 4096 || config.args.length > 128 || config.args.some(arg => arg.length > 8192)) return '命令最多 4096 字符，参数最多 128 个，每个参数最多 8192 字符。'
  if (config.args.some(arg => arg.includes('\0'))) return '参数不能包含空字符。'
  if (new TextEncoder().encode(JSON.stringify({ script: config.script, command: config.command, args: config.args, workDir: config.workDir })).length > 128 * 1024) return '脚本、命令、参数和目录合计不能超过 128 KiB。'
  return ''
}
export const isUnknownRun = (run: ScriptJobRun) => run.deliveryState === 'unknown' && !run.closedAt
export const isActiveRun = (run: ScriptJobRun) => !run.closedAt && (isUnknownRun(run) || run.status === 'pending' || run.status === 'running')
export function runStatus(run: ScriptJobRun): { label: string; color: string } {
  if (isUnknownRun(run)) return { label: '状态未知 · 待核对', color: 'orange' }
  if (run.closedAt && run.result === 'unknown') return { label: '异常关闭 · 结果未知', color: 'orange' }
  if (run.cancelRequested && isActiveRun(run)) return { label: '取消请求待确认', color: 'orange' }
  if (run.result === 'timeout') return { label: '执行超时', color: 'red' }
  return ({ pending: { label: '排队中', color: 'default' }, running: { label: '执行中', color: 'blue' }, completed: { label: '已完成', color: 'green' }, failed: { label: '失败', color: 'red' }, cancelled: { label: '已取消', color: 'default' } })[run.status]
}
export function nodeLabel(node: ScriptNode): string {
  return `${node.name} · ${!node.isOnline ? '离线，提交后等待连接' : node.supportsScriptJobs ? '在线' : '不支持脚本作业，请升级 Agent'}`
}
export function nodeBlock(node: ScriptNode | undefined): string {
  if (!node) return '节点不可用或无访问权限，请检查作业配置。'
  return node.isOnline && !node.supportsScriptJobs ? '此节点不支持脚本作业，请升级 Agent。' : ''
}
export function scriptJobError(reason: unknown): string {
  const error = reason as { response?: { status?: number; data?: { detail?: unknown; message?: string } }; message?: string }
  const detail = error?.response?.data?.detail
  if (typeof detail === 'string') return detail
  if (detail && typeof detail === 'object' && 'message' in detail && typeof detail.message === 'string') return detail.message
  if (error?.response?.status === 403) return '没有此项目或节点的操作权限。'
  return error?.response?.data?.message || error?.message || '请求失败，请刷新后重试。'
}
