import type { ScriptJobRun } from '@/api/scriptJobs'

export function frozenScriptPreview(snapshot: ScriptJobRun['configSnapshot']) {
  return {
    code: snapshot.mode === 'command' ? snapshot.command : snapshot.script,
    args: snapshot.args.map((argument, index) => `参数 ${index + 1}: ${JSON.stringify(argument)}`).join('\n'),
  }
}

/** Node-wide spool diagnostics do not change or prove this run's execution result. */
export function scriptLogDeliveryWarning(delivery: ScriptJobRun['logDelivery']): string {
  const reason = typeof delivery?.blocked_reason === 'string' ? delivery.blocked_reason : ''
  if (delivery?.backpressured !== true && !reason) return ''
  // Bound the displayed diagnostic independently of the backend's length limit.
  const detail = reason.slice(0, 256).replace(/[\uD800-\uDBFF]$/, '') + (reason.length > 256 ? '…' : '')
  return `节点日志传输受阻；当前历史可能尚未完整到达，仅显示服务器已接收内容。未确认记录保留在 Agent。${detail ? ` ${detail}` : ''}`
}
