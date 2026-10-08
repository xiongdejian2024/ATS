<template>
  <div class="plan-detail">
    <a-tabs :active-key="tab" @change="changeTab">
      <a-tab-pane key="plan" tab="测试规划">
        <PlanPlanningMinder :plan="plan" :can-edit="canEdit" @changed="emit('changed')" @configure-plan="policyOpen=true" />
      </a-tab-pane>
      <a-tab-pane v-if="plan.categoryCounts?.functional" key="featureCase" :tab="`功能用例 (${plan.categoryCounts.functional})`"><PlanCategoryWorkspace :plan="plan" category="functional" :can-edit="canEdit" @changed="emit('changed')" /></a-tab-pane>
      <a-tab-pane v-if="plan.categoryCounts?.api" key="apiCase" :tab="`API 用例 (${plan.categoryCounts.api})`"><PlanCategoryWorkspace :plan="plan" category="api" :can-edit="canEdit" @changed="emit('changed')" /></a-tab-pane>
      <a-tab-pane v-if="plan.categoryCounts?.scenario" key="apiScenario" :tab="`API 场景 (${plan.categoryCounts.scenario})`"><PlanCategoryWorkspace :plan="plan" category="scenario" :can-edit="canEdit" @changed="emit('changed')" /></a-tab-pane>
      <a-tab-pane key="defectList" tab="缺陷列表"><PlanDefects :plan-id="plan.id" :editable="canEdit" /></a-tab-pane>
      <a-tab-pane key="executeHistory" tab="执行历史">
        <a-button :loading="loading" style="margin-bottom:12px" @click="loadRuns">刷新执行历史</a-button>
        <a-alert message="每次执行独立保存用例和策略快照，报告按该批次实际结果统计。通过率以全部用例执行项为分母，跳过与未执行不算通过。" type="info" show-icon />
        <a-table :columns="runColumns" :data-source="runs" :loading="loading" row-key="id" size="small" :pagination="pagination" :scroll="{ x: 650 }" @change="onPage">
          <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'status'"><a-tag :color="color(record.status)">{{ label(record.status) }}</a-tag></template>
            <template v-else-if="column.key === 'startedAt'">{{ formatTime(record.startedAt) }}</template>
            <template v-else-if="column.key === 'rate'">{{ record.report.passRate }}% / {{ record.report.passThreshold }}%</template>
            <template v-else-if="column.key === 'actions'">
              <a-space><a-button type="link" size="small" :disabled="record.reportDeleted" @click="openReport(record.id)">报告</a-button><a-button type="link" size="small" @click="openLogs(record.id)">日志</a-button>
                <a-popconfirm v-if="plan.capabilities?.execute && record.status === 'needs_confirmation'" title="请先检查 Agent，确认任务未执行或已经停止。确认后会将该批次记为失败，不自动重试。" @confirm="resolveRun(record.id)"><a-button type="link" danger size="small">确认已停止</a-button></a-popconfirm>
                <a-popconfirm v-else-if="plan.capabilities?.execute && active(record.status)" title="取消该批次尚未完成的执行？" @confirm="cancel(record.id)"><a-button type="link" danger size="small">取消</a-button></a-popconfirm>
              </a-space>
            </template>
          </template>
        </a-table>
      </a-tab-pane>
    </a-tabs>
    <a-drawer v-model:open="policyOpen" title="执行配置" width="min(720px,100vw)">
        <a-form layout="vertical" class="policy-form">
          <a-form-item label="所属计划组"><a-select v-model:value="policy.groupId" allow-clear placeholder="未分组" :options="groups.map(g => ({ label: g.name, value: g.id }))" /></a-form-item>
          <a-form-item label="测试套执行方式"><a-radio-group v-model:value="policy.executionMode"><a-radio value="serial">串行</a-radio><a-radio value="parallel">并行</a-radio></a-radio-group></a-form-item>
          <a-form-item label="失败停止"><a-switch v-model:checked="policy.stopOnFailure" /> <span class="muted">任一测试套失败后停止后续等待项；已在运行的测试套继续回传结果。</span></a-form-item>
          <a-form-item label="通过阈值"><a-input-number v-model:value="policy.passThreshold" :min="0" :max="100" :precision="1" /> %</a-form-item>
          <a-form-item label="测试套顺序">
            <a-empty v-if="!orderedSuites.length" description="暂无测试套，可在计划执行工作区添加；手工用例可直接创建批次。" />
            <div v-for="(suite, index) in orderedSuites" :key="suite.id" class="suite-row"><span>{{ index + 1 }}. {{ suite.name }}</span><a-space><a-button size="small" :disabled="index === 0" @click="move(index, -1)">上移</a-button><a-button size="small" :disabled="index === orderedSuites.length - 1" @click="move(index, 1)">下移</a-button></a-space></div>
          </a-form-item>
          <a-alert message="保存后的策略应用于下一执行批次；正在执行和历史批次的配置保持原快照。并行度仍受各 Agent 节点容量限制。" type="info" />
          <a-button type="primary" :loading="saving" @click="save">保存执行配置</a-button>
        </a-form>
    </a-drawer>
    <a-modal v-model:open="logsOpen" title="批次执行日志" width="min(850px,96vw)" :footer="null"><PlanRunLogs v-if="logsOpen && logRunId" :plan-id="plan.id" :run-id="logRunId" /></a-modal>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { message } from 'ant-design-vue'
import PlanPlanningMinder from './PlanPlanningMinder.vue'
import PlanCategoryWorkspace from './PlanCategoryWorkspace.vue'
import PlanDefects from './PlanDefects.vue'
import PlanRunLogs from '@/components/ExecutionLogs/PlanRunLogs.vue'
import {useRouter,useRoute} from 'vue-router'
import type { TestPlan } from '@/types'
import { testPlanApi } from '@/api/testPlan'
import { testSuiteApi, type TestSuite } from '@/api/testSuite'
import { planOrchestrationApi, type PlanGroup, type PlanPolicy, type PlanRun } from '@/api/planOrchestration'
const props = defineProps<{ plan: TestPlan; runId?: string;canEdit:boolean }>()
const emit = defineEmits<{changed:[]}>(),router=useRouter(),route=useRoute()
const loading = ref(false), saving = ref(false), policyOpen = ref(false), logsOpen = ref(false)
const tab=computed(()=>{const key=String(route.query.tab||'plan');const allowed=['plan','defectList','executeHistory'];if(props.plan.categoryCounts?.functional)allowed.push('featureCase');if(props.plan.categoryCounts?.api)allowed.push('apiCase');if(props.plan.categoryCounts?.scenario)allowed.push('apiScenario');return allowed.includes(key)?key:'plan'})
function changeTab(key:string|number){void router.replace({query:{...route.query,tab:String(key)}})}
const runs = ref<PlanRun[]>([]), groups = ref<PlanGroup[]>([]), suites = ref<TestSuite[]>([])
const policy = ref<PlanPolicy>({ groupId: null, executionMode: 'serial', stopOnFailure: false, passThreshold: 100, suiteOrder: [] })
const logRunId = ref('')
const pagination = ref({ current: 1, pageSize: 10, total: 0 })
const orderedSuites = computed(() => [...suites.value].sort((a, b) => {
  const index = (id: string) => { const i = policy.value.suiteOrder.indexOf(id); return i < 0 ? 99999 : i }
  return index(a.id) - index(b.id)
}))
const runColumns = [{ title: '发起时间', key: 'startedAt', width: 180 }, { title: '状态', key: 'status', width: 90 }, { title: '通过率 / 阈值', key: 'rate', width: 140 }, { title: '操作', key: 'actions', width: 200 }]
const active = (s: string) => ['group_waiting', 'queued', 'running', 'cancelling'].includes(s)
const label = (s: string) => ({ group_waiting: '等待计划组前序', queued: '排队中', pending: '未执行', waiting: '等待前序', running: '进行中', needs_confirmation: '等待核对节点', cancelling: '取消中', cancelled: '已取消', completed: '已通过', passed: '通过', failed: '失败', error: '错误', skipped: '跳过' }[s] || s)
const color = (s: string) => ['passed', 'completed'].includes(s) ? 'green' : ['failed', 'error'].includes(s) ? 'red' : active(s) ? 'blue' : 'default'
const formatTime = (value: string) => value ? new Date(value).toLocaleString('zh-CN') : '-'
async function loadRuns() {
  loading.value = true
  try { const data = await testPlanApi.getPlanExecutions(props.plan.id, { page: pagination.value.current, size: pagination.value.pageSize }); runs.value = data.items; pagination.value.total = data.total }
  catch (error) { console.error('加载计划批次失败', error); message.error('加载执行历史失败') }
  finally { loading.value = false }
}
async function load() {
  try { const [p, g, s] = await Promise.all([planOrchestrationApi.settings(props.plan.id), planOrchestrationApi.groups(props.plan.projectId), testSuiteApi.getTestSuites(props.plan.id, { limit: 1000 })]); policy.value = p; groups.value = g; suites.value = s.items }
  catch (error) { console.error('加载计划配置失败', error); message.error('加载执行配置失败') }
  await loadRuns()
  if (props.runId) await openReport(props.runId)
}
function move(index: number, delta: number) { const ids = orderedSuites.value.map(s => s.id); [ids[index], ids[index + delta]] = [ids[index + delta], ids[index]]; policy.value.suiteOrder = ids }
async function save() { if(!props.canEdit)return;saving.value = true; try { policy.value = await planOrchestrationApi.saveSettings(props.plan.id, { ...policy.value, groupId: policy.value.groupId || null }); message.success('执行配置已保存');emit('changed') } catch (error) { console.error('保存计划策略失败', error); message.error('保存失败') } finally { saving.value = false } }
async function openReport(id: string) { await router.push({name:'TestPlanReportDetail',params:{runId:id},query:{projectId:props.plan.projectId,kind:'PLAN'}}) }
function openLogs(id: string) { logRunId.value = id; logsOpen.value = true }
async function resolveRun(id: string) { try { await planOrchestrationApi.resolve(id); message.success('已按核对结果终止批次'); await loadRuns() } catch (error) { console.error('确认执行状态失败', error); message.error('确认失败') } }
async function cancel(id: string) { try { await planOrchestrationApi.cancel(id); message.success('已请求取消'); await loadRuns() } catch (error) { console.error('取消计划批次失败', error); message.error('取消失败') } }
function onPage(p: any) { pagination.value.current = p.current; pagination.value.pageSize = p.pageSize; loadRuns() }
watch(tab, key => { if (key === 'executeHistory') void loadRuns() })
onMounted(load)
watch(() => props.plan.id, () => { logsOpen.value = false; logRunId.value = ''; pagination.value.current = 1; load() })
defineExpose({ refresh: loadRuns,openSettings:()=>{if(props.canEdit)policyOpen.value=true} })
</script>

<style scoped>
.plan-detail { display: flex; flex-direction: column; gap: 20px; }
.plan-information{margin-bottom:16px}
.policy-form { max-width: 640px; }
.policy-form > .ant-btn { margin-top: 16px; }
.suite-row { display: flex; justify-content: space-between; gap: 8px; padding: 8px 0; border-bottom: 1px solid #eee; }
.muted { color: #666; font-size: 12px; }
.report-stats { margin: 20px 0; }
.execution-log { white-space: pre-wrap; max-height: 65vh; overflow: auto; background: #141820; color: #d7e2ed; padding: 16px; }
</style>
