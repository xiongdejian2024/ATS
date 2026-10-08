<template>
  <div class="script-jobs-page">
    <header class="page-heading">
      <div><h1>脚本作业</h1><p>编写脚本，交给节点队列执行，实时查看日志。</p></div>
      <a-space><a-button :loading="loading" @click="state.refresh">刷新</a-button><a-button type="primary" :disabled="!projectId" @click="openEditor(null)">新建作业</a-button></a-space>
    </header>
    <a-alert v-if="!projectId" type="info" show-icon message="请在顶部选择项目，查看或创建该项目的脚本作业。" />
    <template v-else>
      <a-alert v-if="error" type="error" show-icon :message="error" />
      <a-alert v-if="nodeError" type="error" show-icon :message="`节点列表读取失败：${nodeError}`" />
      <a-alert v-if="!persistentRequests" type="warning" show-icon message="浏览器无法保留提交编号。提交中断时，请在刷新或关闭此页前先核对执行历史。" />
      <a-table :columns="columns" :data-source="jobs" row-key="id" :loading="loading" :pagination="false" :scroll="{ x: 850 }">
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'name'"><a @click="openHistory(record.id)">{{ record.name }}</a><div class="muted">配置 v{{ record.revision }}</div></template>
          <template v-else-if="column.key === 'node'"><span>{{ nodeFor(record.environmentId)?.name || record.environmentId }}</span><div class="muted" :class="{ warning: !nodeFor(record.environmentId)?.isOnline }">{{ nodeStatus(record.environmentId) }}</div></template>
          <template v-else-if="column.key === 'mode'"><a-tag>{{ modeLabel(record.mode) }}</a-tag><div class="muted">超时 {{ record.timeoutSeconds }} 秒</div></template>
          <template v-else-if="column.key === 'updated'">{{ time(record.updatedAt) }}</template>
          <template v-else-if="column.key === 'actions'">
            <a-space wrap>
              <a-tooltip :title="state.submission(record.id) ? '使用同一请求编号确认提交结果' : nodeBlock(nodeFor(record.environmentId)) || undefined">
                <a-button type="primary" size="small" :loading="state.submission(record.id)?.busy"
                  :disabled="!!state.submission(record.id)?.busy || (!state.submission(record.id) && !!nodeBlock(nodeFor(record.environmentId)))" @click="runNow(record)">
                  {{ state.submission(record.id)?.uncertain ? '重试确认提交' : '运行' }}
                </a-button>
              </a-tooltip>
              <a-button size="small" @click="openEditor(record)">编辑</a-button>
              <a-button size="small" @click="openHistory(record.id)">历史与日志</a-button>
            </a-space>
          </template>
        </template>
        <template #emptyText><a-empty description="还没有脚本作业。新建一个 Shell、Python 或命令作业即可开始。" /></template>
      </a-table>
      <a-pagination :current="page" :total="total" :page-size="20" :show-size-changer="false" @change="changePage" />
    </template>
    <ScriptJobEditor :open="editorOpen" :project-id="projectId" :job="editingJob" :nodes="nodes" @close="closeEditor" @saved="saved" />
    <a-drawer :open="!!queryJobId" :title="`${job?.name || '脚本作业'} · 历史与日志`" :width="drawerWidth" :destroy-on-close="true" @close="closeHistory">
      <a-alert v-if="historyError" :message="historyError" type="error" show-icon />
      <a-alert v-if="runError" :message="runError" type="error" show-icon />
      <div class="history-layout">
        <section class="history-list" aria-label="作业运行历史">
          <div class="history-heading"><h3>运行历史</h3><a-button size="small" :loading="historyLoading" @click="state.refreshHistory">刷新</a-button></div>
          <a-spin :spinning="historyLoading && !runs.length">
            <button v-for="item in runs" :key="item.executionId" class="history-item" :class="{ selected: queryRunId === item.executionId }" @click="openHistory(item.jobId, item.executionId)">
              <a-tag :color="runStatus(item).color">{{ runStatus(item).label }}</a-tag>
              <span>{{ time(item.createdAt) }}</span>
              <span class="muted">{{ item.executionId }}</span>
            </button>
            <a-empty v-if="!historyLoading && !runs.length" description="暂无运行记录" />
          </a-spin>
          <a-pagination :current="historyPage" :total="historyTotal" :page-size="20" :show-size-changer="false" size="small" simple @change="changeHistoryPage" />
        </section>
        <div class="history-detail">
          <ScriptJobRunDetail v-if="run" :key="run.executionId" :run="run" :node-name="nodeFor(run.environmentId)?.name" :node-online="nodeFor(run.environmentId)?.isOnline"
            :busy="actionBusy" :error="actionError" @refresh="state.refreshRun" @cancel="cancelRun" @resolve="resolveRun" />
          <a-empty v-else :description="queryRunId ? '正在读取本次运行；读取失败时可重新选择记录。' : '选择一条运行记录查看状态、冻结配置和日志。'" />
        </div>
      </div>
    </a-drawer>
  </div>
</template>
<script setup lang="ts">
import { computed, onScopeDispose, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useWindowSize } from '@vueuse/core'
import { useProjectStore } from '@/stores/project'
import { useUserStore } from '@/stores/user'
import { scriptJobsApi, type ScriptJob, type ScriptMode } from '@/api/scriptJobs'
import ScriptJobEditor from '@/components/ScriptJobs/ScriptJobEditor.vue'
import ScriptJobRunDetail from '@/components/ScriptJobs/ScriptJobRunDetail.vue'
import { useScriptJobs } from '@/components/ScriptJobs/useScriptJobs'
import { scriptJobSubmissions } from '@/components/ScriptJobs/scriptJobSubmissions'
import { nodeBlock, runStatus } from '@/components/ScriptJobs/scriptJobState'
const route = useRoute(), router = useRouter(), projects = useProjectStore(), user = useUserStore()
const queryString = (value: unknown) => typeof value === 'string' ? value : ''
const projectId = computed(() => queryString(route.query.projectId) || projects.currentProject?.id || '')
const queryJobId = computed(() => queryString(route.query.jobId)), queryRunId = computed(() => queryString(route.query.runId))
const state = useScriptJobs(scriptJobsApi, scriptJobSubmissions, user.user?.id || '')
const { jobs, nodes, page, total, loading, error, nodeError, job, runs, run, historyPage, historyTotal, historyLoading, historyError, runError, actionBusy, actionError, persistentRequests } = state
const { width } = useWindowSize(), drawerWidth = computed(() => Math.min(Math.max(width.value - 24, 300), 1250))
const editorOpen = ref(false), editingJob = ref<ScriptJob | null>(null)
let navigation = 0, interaction = 0
const columns = [{ title: '作业名称', key: 'name' }, { title: '执行节点', key: 'node' }, { title: '执行方式', key: 'mode' }, { title: '更新于', key: 'updated' }, { title: '操作', key: 'actions', width: 280 }]
const nodeFor = (id: string) => nodes.value.find(node => node.id === id)
const nodeStatus = (id: string) => { const node = nodeFor(id); return !node ? '不可用或无访问权限' : !node.isOnline ? '离线 · 提交后等待连接' : node.supportsScriptJobs ? '在线 · 支持脚本作业' : '需要升级 Agent' }
const modeLabel = (mode: ScriptMode) => ({ shell: 'Shell', python: 'Python', command: '命令 + 参数' })[mode]
const time = (value: string) => new Date(value).toLocaleString('zh-CN')
function openEditor(selected: ScriptJob | null) { interaction++; editingJob.value = selected; editorOpen.value = true }
function closeEditor() { interaction++; editorOpen.value = false; editingJob.value = null }
function saved() { closeEditor(); void state.refresh() }
function openHistory(jobId: string, runId?: string) { interaction++; return router.push({ path: '/script-jobs', query: { projectId: projectId.value, jobId, ...(runId ? { runId } : {}) } }) }
function closeHistory() { interaction++; return router.push({ path: '/script-jobs', query: { projectId: projectId.value } }) }
function changePage(value: number) { interaction++; page.value = value; void state.refresh() }
function changeHistoryPage(value: number) { historyPage.value = value; void state.refreshHistory() }
async function runNow(selected: ScriptJob) {
  const current = interaction
  const result = await state.submit(selected)
  if (result && current === interaction) { void state.refresh(); await openHistory(result.jobId, result.executionId) }
}
function cancelRun(executionId: string) { if (run.value?.executionId === executionId) void state.act('cancel') }
function resolveRun(executionId: string, confirmed: boolean, reason: string) { if (run.value?.executionId === executionId) void state.act('resolve', confirmed, reason) }
watch(() => [projectId.value, queryJobId.value, queryRunId.value], async () => {
  const current = ++navigation
  closeEditor()
  if (state.projectId.value !== projectId.value) state.setProject(projectId.value)
  if (!queryJobId.value) { state.closeJob(); return }
  if (job.value?.id !== queryJobId.value) await state.selectJob(queryJobId.value)
  if (current !== navigation) return
  if (!queryRunId.value) state.closeRun()
  else if (run.value?.executionId !== queryRunId.value) await state.selectRun(queryRunId.value)
}, { immediate: true, flush: 'sync' })
onScopeDispose(() => { navigation++; interaction++ })
</script>
<style scoped>
.script-jobs-page { display: flex; flex-direction: column; gap: 16px; background: #fff; border: 1px solid var(--ms-border); border-radius: 4px; padding: 20px; min-height: 100%; }
.page-heading, .history-heading { display: flex; justify-content: space-between; align-items: center; gap: 16px; }
h1 { color: var(--ms-text); font-size: 20px; font-weight: 600; margin: 0 0 4px; }
h3 { font-size: 15px; margin: 0; }
.page-heading p, .muted { color: var(--ms-text-secondary); font-size: 12px; margin: 0; }
.warning { color: var(--warning-gradient); }
.history-layout { display: grid; grid-template-columns: 240px minmax(0, 1fr); gap: 20px; }
.history-list { display: flex; flex-direction: column; gap: 12px; min-width: 0; }
.history-item { display: flex; flex-direction: column; align-items: flex-start; gap: 4px; width: 100%; background: #fff; border: 1px solid var(--ms-border); border-radius: 4px; padding: 12px; margin-bottom: 8px; cursor: pointer; text-align: left; overflow-wrap: anywhere; color: var(--ms-text); }
.history-item:hover, .history-item:focus-visible { border-color: var(--primary-color); }
.history-item.selected { background: var(--ms-primary-soft); border-color: var(--primary-color); }
.history-detail { min-width: 0; }
@media (max-width: 850px) { .history-layout { grid-template-columns: 1fr; } .history-list :deep(.ant-spin-container) { max-height: 240px; overflow: auto; } .script-jobs-page { padding: 12px; } .page-heading { align-items: flex-start; flex-wrap: wrap; } }
</style>
