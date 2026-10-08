<template>
  <section class="run-detail" aria-label="脚本作业运行详情">
    <div class="run-heading">
      <div><h3>{{ run.configSnapshot.name }}</h3><div class="muted run-id">运行编号：{{ run.executionId }}</div></div>
      <a-tag :color="status.color">{{ status.label }}</a-tag>
    </div>
    <a-descriptions size="small" :column="2" bordered>
      <a-descriptions-item label="冻结节点">{{ nodeName || run.environmentId }}</a-descriptions-item>
      <a-descriptions-item label="退出码">{{ run.exitCode ?? '—' }}</a-descriptions-item>
      <a-descriptions-item label="创建时间">{{ time(run.createdAt) }}</a-descriptions-item>
      <a-descriptions-item label="开始时间">{{ time(run.startedAt) }}</a-descriptions-item>
      <a-descriptions-item label="结束时间">{{ time(run.completedAt) }}</a-descriptions-item>
      <a-descriptions-item label="耗时 / 超时上限">{{ run.durationSeconds == null ? '—' : `${run.durationSeconds} 秒` }} / {{ run.configSnapshot.timeoutSeconds }} 秒</a-descriptions-item>
    </a-descriptions>
    <a-alert v-if="run.status === 'pending' && !unknown" type="info" show-icon :message="nodeOnline === false ? '已进入队列，等待节点连接。' : '已进入队列，等待控制端派发和 Agent 确认。'" />
    <a-alert v-if="run.cancelRequested && active" type="warning" show-icon message="取消请求已提交；正在等待 Agent 确认进程停止。" />
    <a-alert v-if="run.errorMessage" :message="run.errorMessage" :type="unknown ? 'warning' : 'error'" show-icon />
    <a-alert v-if="error" :message="error" type="error" show-icon />
    <a-alert v-if="run.closedAt" type="warning" show-icon :message="`此记录已人工关闭（${time(run.closedAt)}），执行结果仍为未知。`" />
    <div class="run-actions">
      <a-button :loading="busy" @click="emit('refresh')">刷新状态</a-button>
      <a-button v-if="active" danger :loading="busy" :disabled="run.cancelRequested" @click="emit('cancel', run.executionId)">取消本次运行</a-button>
    </div>
    <div v-if="unknown" class="unknown-panel">
      <a-alert type="warning" show-icon message="执行状态未知，请先到冻结节点核对。不要直接重跑。关闭记录不会终止节点进程，也不代表执行成功。" />
      <a-checkbox v-model:checked="confirmed" :disabled="busy">我已核对节点，确认本次任务从未启动，或它及所有子进程均已停止</a-checkbox>
      <a-input v-model:value="reason" :maxlength="500" :disabled="busy" placeholder="核对说明（可选）" aria-label="核对说明" />
      <a-button danger :disabled="!confirmed || busy" :loading="busy" @click="emit('resolve', run.executionId, confirmed, reason)">核对后关闭</a-button>
    </div>
    <a-collapse>
      <a-collapse-panel key="config" :header="`本次运行的冻结配置${run.configSnapshot.revision ? ' · v' + run.configSnapshot.revision : ''}`">
        <a-descriptions size="small" :column="1">
          <a-descriptions-item label="方式">{{ run.configSnapshot.mode }}</a-descriptions-item>
          <a-descriptions-item label="节点 ID">{{ run.environmentId }}</a-descriptions-item>
          <a-descriptions-item label="工作目录">{{ run.configSnapshot.workDir || '本次运行的隔离目录' }}</a-descriptions-item>
        </a-descriptions>
        <a-textarea :value="frozenPreview.code" readonly :rows="8" class="code-input" aria-label="本次运行的冻结脚本或命令" />
        <div class="frozen-arguments">
          <span>冻结参数（按顺序传入）</span>
          <a-textarea v-if="frozenPreview.args" :value="frozenPreview.args" readonly :rows="4" class="code-input" aria-label="本次运行的冻结参数" />
          <span v-else class="muted">无参数</span>
        </div>
      </a-collapse-panel>
    </a-collapse>
    <div class="log-heading"><h3>执行日志</h3><a-button size="small" :loading="logLoading" @click="logs.refresh">刷新日志</a-button></div>
    <a-alert :type="logStatus.type" :message="logStatus.message" show-icon />
    <a-alert v-if="logDeliveryWarning" type="warning" show-icon :message="logDeliveryWarning" />
    <RawLogDownload :key="run.executionId" :target="downloadTarget" />
    <BoundedLogViewer :records="records" height="min(55vh, 560px)" />
  </section>
</template>
<script setup lang="ts">
import { computed, watch } from 'vue'
import { scriptRunPath, type ScriptJobRun } from '@/api/scriptJobs'
import RawLogDownload from '@/components/ExecutionLogs/RawLogDownload.vue'
import BoundedLogViewer from '@/components/ExecutionLogs/BoundedLogViewer.vue'
import { useScriptJobLogs } from './useScriptJobLogs'
import { isActiveRun, isUnknownRun, runStatus } from './scriptJobState'
import { useUnknownRunConfirmation } from './useUnknownRunConfirmation'
import { frozenScriptPreview, scriptLogDeliveryWarning } from './scriptJobPresentation'
const props = defineProps<{ run: ScriptJobRun; nodeName?: string; nodeOnline?: boolean; busy: boolean; error: string }>()
const emit = defineEmits<{ cancel: [executionId: string]; resolve: [executionId: string, confirmed: boolean, reason: string]; refresh: [] }>()
const active = computed(() => isActiveRun(props.run)), unknown = computed(() => isUnknownRun(props.run)), status = computed(() => runStatus(props.run))
const { confirmed, reason } = useUnknownRunConfirmation(() => props.run)
const time = (value: string | null) => value ? new Date(value).toLocaleString('zh-CN') : '—'
const frozenPreview = computed(() => frozenScriptPreview(props.run.configSnapshot))
const logDeliveryWarning = computed(() => scriptLogDeliveryWarning(props.run.logDelivery))
const downloadTarget = computed(() => ({ endpoint: `${scriptRunPath(props.run.jobId, props.run.executionId)}/logs/export`, filename: `script-${props.run.executionId}` }))
const logs = useScriptJobLogs()
const { records, loading: logLoading, status: logStatus } = logs
watch(() => [props.run.jobId, props.run.executionId], () => {
  // A terminal result can precede the last durable log-spool delivery.
  logs.open({ jobId: props.run.jobId, executionId: props.run.executionId, live: true })
}, { immediate: true, flush: 'sync' })
</script>
<style scoped>
.run-detail { display: flex; flex-direction: column; gap: 12px; min-width: 0; }
.run-heading, .log-heading { display: flex; align-items: center; justify-content: space-between; gap: 12px; }
h3 { font-size: 16px; font-weight: 600; margin: 0; }
.run-id { overflow-wrap: anywhere; font-size: 12px; }
.muted { color: var(--ms-text-secondary); }
.run-actions { display: flex; gap: 8px; }
.unknown-panel { display: flex; align-items: flex-start; flex-direction: column; gap: 12px; padding: 12px; border: 1px solid var(--ms-border); border-radius: 4px; }
.code-input { font-family: monospace; }
.frozen-arguments { display: flex; flex-direction: column; gap: 6px; margin-top: 12px; }
</style>
