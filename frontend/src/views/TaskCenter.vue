<template>
  <div class="task-center">
    <div class="heading">
      <div><h2>任务中心</h2><p>统一安排测试套与计划，追踪每一次执行。</p></div>
      <a-space wrap>
        <a-select v-model:value="projectId" placeholder="选择项目" class="project-select" :options="projects" />
        <a-button :loading="loading" @click="refresh">刷新</a-button>
        <a-button type="primary" :disabled="!projectId" @click="openCreate">新建任务</a-button>
      </a-space>
    </div>
    <a-alert message="新任务默认关闭定时执行。启用后按所选时区调度；停用只停止后续触发，正在执行的任务请在历史中取消。" type="info" show-icon class="notice" />
    <a-table :columns="columns" :data-source="items" row-key="id" :loading="loading" :scroll="{ x: 960 }" :pagination="{ pageSize: 10 }">
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'name'"><a @click="showHistory(record)">{{ record.name }}</a><div class="hint">{{ targetName(record) }}</div></template>
        <template v-else-if="column.key === 'cron'"><span>{{ record.cronExpression || '仅手动触发' }}</span><div class="hint">{{ record.timezone }}</div></template>
        <template v-else-if="column.key === 'enabled'"><a-switch :checked="record.enabled" :disabled="!record.cronExpression || busy.has(record.id)" @change="toggle(record, $event)" /></template>
        <template v-else-if="column.key === 'next'">{{ formatTime(record.nextRunAt) }}</template>
        <template v-else-if="column.key === 'actions'">
          <a-space wrap>
            <a-button size="small" type="primary" :loading="busy.has(record.id)" @click="runNow(record)">立即执行</a-button>
            <a-button size="small" @click="openEdit(record)">编辑</a-button>
            <a-button size="small" @click="showHistory(record)">历史</a-button>
          </a-space>
        </template>
      </template>
    </a-table>
    <a-modal v-model:open="editorOpen" :title="editingId ? '编辑任务' : '新建任务'" :confirm-loading="saving" @ok="save">
      <a-form layout="vertical">
        <a-form-item label="任务名称" required><a-input v-model:value="form.name" :maxlength="255" /></a-form-item>
        <a-form-item label="执行类型" required><a-radio-group v-model:value="form.targetType" :disabled="!!editingId" @change="form.targetId = ''"><a-radio value="suite">测试套</a-radio><a-radio value="plan">测试计划</a-radio></a-radio-group></a-form-item>
        <a-form-item label="执行目标" required><a-select v-model:value="form.targetId" :disabled="!!editingId" :options="targetOptions" placeholder="请选择已配置的测试套或计划" /></a-form-item>
        <a-form-item label="Cron 表达式" extra="留空为手动任务。例如：0 9 * * 1-5 表示周一至周五 09:00。"><a-input v-model:value="form.cronExpression" placeholder="分 时 日 月 周" :maxlength="100" /></a-form-item>
        <a-form-item label="时区"><a-select v-model:value="form.timezone" :options="[{ value: 'Asia/Shanghai', label: '中国标准时间（Asia/Shanghai）' }, { value: 'UTC', label: 'UTC' }]" /></a-form-item>
      </a-form>
    </a-modal>
    <a-drawer v-model:open="historyOpen" :title="`${selected?.name || ''} · 执行历史`" :width="drawerWidth">
      <a-button @click="loadHistory" :loading="historyLoading">刷新历史</a-button>
      <a-list :data-source="runs" :loading="historyLoading" item-layout="vertical">
        <template #renderItem="{ item }"><a-list-item>
          <a-space><a-tag :color="statusColor(item.status)">{{ statusText(item.status) }}</a-tag><span>{{ item.triggerType === 'manual' ? '手动执行' : '定时执行' }}</span></a-space>
          <p>{{ formatTime(item.createdAt) }}</p>
          <div class="run-id">执行编号：{{ item.executionId || item.planRunId || item.id }}</div>
          <a-alert v-if="item.errorMessage" type="error" :message="item.errorMessage" show-icon />
          <a-space class="run-actions">
            <a-button v-if="['queued', 'running', 'cancelling'].includes(item.status)" danger size="small" :disabled="item.status === 'cancelling'" @click="cancel(item)">取消执行</a-button>
            <a-popconfirm v-if="item.status === 'needs_confirmation' && !item.planRunId" title="已确认节点未执行或已停止？此操作将记录为异常结束，不会终止节点进程。" ok-text="已核对，结束记录" cancel-text="继续核对" @confirm="resolve(item)"><a-button danger size="small">人工确认结束</a-button></a-popconfirm>
            <a-button v-if="item.planRunId" size="small" @click="openPlan(item)">计划批次详情</a-button>
            <a-button v-if="item.executionId && selected?.targetType === 'suite'" size="small" @click="openLogs(item)">查看日志</a-button>
          </a-space>
        </a-list-item></template>
      </a-list>
      <a-pagination v-model:current="historyPage" :total="historyTotal" :page-size="20" :show-size-changer="false" @change="loadHistory" />
    </a-drawer>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, reactive, ref, watch } from 'vue'
import { useWindowSize } from '@vueuse/core'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { useProjectStore } from '@/stores/project'
import { taskCenterApi, type TaskSchedule, type ScheduleRun, type TargetOption, type ScheduleForm } from '@/api/taskCenter'

const router = useRouter()
const projectStore = useProjectStore()
const projectId = ref('')
const projects = computed(() => projectStore.projects.map(p => ({ value: p.id, label: p.name })))
const items = ref<TaskSchedule[]>([])
const targets = ref<{ plans: TargetOption[]; suites: TargetOption[] }>({ plans: [], suites: [] })
const loading = ref(false)
const busy = reactive(new Set<string>())
const pendingRequests = new Map<string, string>()
const editorOpen = ref(false)
const saving = ref(false)
const editingId = ref('')
const form = reactive<ScheduleForm>({ projectId: '', name: '', targetType: 'suite', targetId: '', cronExpression: '', timezone: 'Asia/Shanghai' })
const targetOptions = computed(() => targets.value[form.targetType === 'suite' ? 'suites' : 'plans'].map(t => ({ value: t.id, label: t.name })))
const columns = [
  { title: '任务 / 目标', key: 'name' }, { title: '执行周期', key: 'cron' },
  { title: '定时启用', key: 'enabled' }, { title: '下次执行', key: 'next' }, { title: '操作', key: 'actions' },
]
const selected = ref<TaskSchedule | null>(null)
const historyOpen = ref(false)
const historyLoading = ref(false)
const historyPage = ref(1)
const historyTotal = ref(0)
const runs = ref<ScheduleRun[]>([])
const { width } = useWindowSize()
const drawerWidth = computed(() => Math.min(width.value - 24, 640))
const formatTime = (value: string | null) => value ? new Date(value).toLocaleString('zh-CN') : '—'
const statusText = (value: string) => ({ queued: '排队中', running: '执行中', cancelling: '取消中', completed: '已完成', failed: '失败', cancelled: '已取消', needs_confirmation: '派发待确认' }[value] || value)
const statusColor = (value: string) => ({ queued: 'default', running: 'blue', cancelling: 'orange', completed: 'green', failed: 'red', cancelled: 'default', needs_confirmation: 'orange' }[value] || 'default')
const targetName = (row: TaskSchedule) => (row.targetType === 'suite' ? '测试套：' : '计划：') + (targets.value[row.targetType === 'suite' ? 'suites' : 'plans'].find(t => t.id === row.targetId)?.name || '目标已删除')
const reportError = (error: unknown) => console.error('任务中心操作失败', error)

async function refresh() {
  if (!projectId.value) return
  const current = projectId.value
  loading.value = true
  try {
    const [list, options] = await Promise.all([taskCenterApi.list(current), taskCenterApi.targets(current)])
    if (current !== projectId.value) return
    items.value = list.items; targets.value = options
  } catch (error) { reportError(error) } finally { loading.value = false }
}
function openCreate() {
  editingId.value = ''
  Object.assign(form, { projectId: projectId.value, name: '', targetType: 'suite', targetId: '', cronExpression: '', timezone: 'Asia/Shanghai' })
  editorOpen.value = true
}
function openEdit(row: TaskSchedule) {
  editingId.value = row.id
  Object.assign(form, row)
  editorOpen.value = true
}
async function save() {
  if (!form.name.trim() || !form.targetId) { message.warning('请填写名称并选择执行目标'); return }
  saving.value = true
  try {
    const data = { name: form.name.trim(), cronExpression: form.cronExpression || null, timezone: form.timezone }
    if (editingId.value) await taskCenterApi.update(editingId.value, data)
    else await taskCenterApi.create({ ...data, projectId: projectId.value, targetType: form.targetType, targetId: form.targetId })
    editorOpen.value = false; message.success('任务已保存'); await refresh()
  } catch (error) { reportError(error) } finally { saving.value = false }
}
async function toggle(row: TaskSchedule, enabled: unknown) {
  busy.add(row.id)
  try { await taskCenterApi.enable(row.id, Boolean(enabled)); await refresh() } catch (error) { reportError(error) } finally { busy.delete(row.id) }
}
async function runNow(row: TaskSchedule) {
  if (busy.has(row.id)) return
  busy.add(row.id)
  try {
    // 请求超时后重试沿用请求号，避免服务已入队但响应丢失导致重复运行。
    const requestId = pendingRequests.get(row.id) || crypto.randomUUID()
    pendingRequests.set(row.id, requestId)
    await taskCenterApi.run(row.id, requestId)
    pendingRequests.delete(row.id)
    message.success('执行已加入队列'); await showHistory(row)
  } catch (error) { reportError(error) } finally { busy.delete(row.id) }
}
async function showHistory(row: TaskSchedule) { selected.value = row; historyPage.value = 1; historyOpen.value = true; await loadHistory() }
async function loadHistory() {
  if (!selected.value) return
  historyLoading.value = true
  try { const data = await taskCenterApi.history(selected.value.id, historyPage.value); runs.value = data.items; historyTotal.value = data.total }
  catch (error) { reportError(error) } finally { historyLoading.value = false }
}
async function cancel(run: ScheduleRun) {
  if (!selected.value) return
  try { await taskCenterApi.cancel(selected.value.id, run.id); await loadHistory() } catch (error) { reportError(error) }
}
async function resolve(run: ScheduleRun) {
  if (!selected.value) return
  try { await taskCenterApi.resolve(selected.value.id, run.id); await loadHistory() } catch (error) { reportError(error) }
}
function openLogs(run: ScheduleRun) {
  router.push({ path: '/test-suites/execution-log', query: { suiteId: selected.value?.targetId, executionId: run.executionId || undefined } })
}
function openPlan(run: ScheduleRun) {
  router.push({ path: '/test-plans', query: { planId: selected.value?.targetId, runId: run.planRunId || undefined } })
}
watch(projectId, () => { historyOpen.value = false; selected.value = null; items.value = []; refresh() })
let timer: ReturnType<typeof setInterval> | undefined
onMounted(async () => {
  await projectStore.fetchProjects()
  projectId.value = projectStore.currentProject?.id || projectStore.projects[0]?.id || ''
  timer = setInterval(() => { if (historyOpen.value && !historyLoading.value) loadHistory() }, 3000)
})
onUnmounted(() => { if (timer) clearInterval(timer) })
</script>

<style scoped>
.task-center { padding: 24px; min-height: 100%; background: #fff; }
.heading { display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap; margin-bottom: 20px; }
h2 { margin: 0 0 6px; } .heading p, .hint { color: #667085; } .heading p { margin: 0; }
.hint { font-size: 12px; margin-top: 6px; } .project-select { width: 220px; }
.notice { margin-bottom: 20px; } .run-id { overflow-wrap: anywhere; color: #667085; font-size: 12px; }
.run-actions { margin-top: 12px; }
@media (max-width: 600px) { .task-center { padding: 12px; } .project-select { width: 180px; } }
</style>
