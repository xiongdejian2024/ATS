<template>
  <section class="plan-page">
    <header class="plan-heading">
      <a-button @click="back"><ArrowLeftOutlined /> 返回计划列表</a-button>
      <template v-if="plan"><a-tag :color="plan.status==='completed'?'green':'blue'">{{statusText}}</a-tag><h2>[{{plan.planNumber}}] {{plan.name}}</h2>
        <a-space wrap><a-button v-if="editable" @click="editOpen=true">编辑</a-button><a-button v-if="plan.capabilities?.execute&&!metadata?.archived" @click="executeOpen=true">执行</a-button><a-button v-if="plan.capabilities?.copy" :loading="busy" @click="copyPlan">复制</a-button><a-button :loading="busy" @click="follow">{{metadata?.followed?'取消关注':'关注'}}</a-button>
          <a-dropdown v-if="plan.capabilities?.edit||plan.capabilities?.delete" :trigger="['click']"><a-button>更多</a-button><template #overlay><a-menu @click="more"><a-menu-item v-if="editable" key="settings">执行配置</a-menu-item><a-menu-item v-if="plan.capabilities?.edit" key="archive">{{metadata?.archived?'取消归档':'归档'}}</a-menu-item><a-menu-item v-if="plan.capabilities?.delete" key="delete" danger>删除</a-menu-item></a-menu></template></a-dropdown>
        </a-space>
      </template>
    </header>
    <a-alert v-if="!projectId" message="请选择项目" type="info" />
    <a-spin v-else :spinning="loading"><a-result v-if="failed" status="error" title="计划不可用" sub-title="请检查当前项目、计划链接和访问权限。"><template #extra><a-button @click="load">重试</a-button></template></a-result>
      <template v-else-if="plan"><a-alert v-if="metadata?.archived" message="计划已归档" type="info" class="archive-notice" />
        <div class="plan-progress"><span>全部用例 <b>{{plan.totalCases||0}}</b></span><span>已执行 <b>{{plan.executedCases||0}}</b></span><span>通过 <b>{{plan.caseStatusCounts?.pass||0}}</b></span><span>失败 <b>{{plan.caseStatusCounts?.fail||0}}</b></span><a-progress :percent="progress" :style="{width:'180px'}" /></div>
        <TestPlanDetail :key="`${projectId}:${plan.id}`" ref="workspace" :plan="plan" :can-edit="editable" :run-id="String(route.query.runId||'')" @changed="load" />
      </template>
    </a-spin>
    <a-drawer v-model:open="editOpen" title="编辑测试计划" width="min(800px,100vw)" destroy-on-close><TestPlanEdit v-if="plan&&editOpen" :plan-id="plan.id" :project-id="plan.projectId" @save="saved" @cancel="editOpen=false" /></a-drawer>
    <a-modal v-model:open="executeOpen" title="执行测试计划" :confirm-loading="busy" @ok="execute"><a-form layout="vertical"><a-form-item label="执行说明"><a-textarea v-model:value="notes" :maxlength="1000" /></a-form-item></a-form><p>将使用计划关联的执行环境和已保存的执行配置创建新批次。</p></a-modal>
  </section>
</template>
<script setup lang="ts">
import {computed,ref,watch} from 'vue'
import {useRoute,useRouter} from 'vue-router'
import {message,Modal} from 'ant-design-vue'
import {ArrowLeftOutlined} from '@ant-design/icons-vue'
import {useProjectStore} from '@/stores/project'
import {testPlanApi} from '@/api/testPlan'
import {planWorkspaceApi,type PlanMetadata} from '@/api/planWorkspace'
import type {TestPlan} from '@/types'
import TestPlanDetail from '@/components/TestPlan/TestPlanDetail.vue'
import TestPlanEdit from '@/components/TestPlan/TestPlanEdit.vue'
const route=useRoute(),router=useRouter(),projectStore=useProjectStore()
const projectId=computed(()=>typeof route.query.projectId==='string'?route.query.projectId:projectStore.currentProject?.id)
const planId=computed(()=>String(route.params.planId||'')),plan=ref<TestPlan>(),metadata=ref<PlanMetadata>(),workspace=ref<InstanceType<typeof TestPlanDetail>>()
const loading=ref(false),failed=ref(false),busy=ref(false),editOpen=ref(false),executeOpen=ref(false),notes=ref('')
const editable=computed(()=>!!plan.value?.capabilities?.edit&&!metadata.value?.archived)
const statusText=computed(()=>(({not_started:'未开始',running:'进行中',paused:'已暂停',completed:'已完成',overdue:'已逾期'} as Record<string,string>)[plan.value?.status||'']||plan.value?.status))
const progress=computed(()=>plan.value?.totalCases?Math.round(100*(plan.value.executedCases||0)/plan.value.totalCases):0)
let sequence=0
async function load(){const current=++sequence;failed.value=false;if(!projectId.value){plan.value=undefined;metadata.value=undefined;loading.value=false;return}loading.value=true
  try{const result=await testPlanApi.getTestPlan(planId.value,projectId.value);const meta=await planWorkspaceApi.metadata(result.id);if(current===sequence){plan.value=result;metadata.value=meta}}
  catch(error){console.error('加载独立计划详情失败',error);if(current===sequence){plan.value=undefined;metadata.value=undefined;failed.value=true}}
  finally{if(current===sequence)loading.value=false}}
const back=()=>router.push({name:'TestPlans',query:{projectId:projectId.value}})
async function saved(){editOpen.value=false;await load()}
async function follow(){if(!plan.value)return;busy.value=true;try{await planWorkspaceApi.follow(plan.value.id,!metadata.value?.followed);await load()}catch(error){console.error('更新计划关注失败',error);message.error('关注操作失败')}finally{busy.value=false}}
async function copyPlan(){if(!plan.value?.capabilities?.copy)return;busy.value=true;try{const copy=await testPlanApi.clonePlan(plan.value.projectId,plan.value.id);message.success('计划已复制');await router.push({name:'TestPlanDetailPage',params:{planId:copy.id},query:{projectId:projectId.value}})}catch(error){console.error('复制计划失败',error);message.error('复制失败')}finally{busy.value=false}}
async function execute(){if(!plan.value?.capabilities?.execute||metadata.value?.archived)return;busy.value=true;try{await testPlanApi.executePlan(plan.value.id,undefined,notes.value);executeOpen.value=false;message.success('执行批次已创建');await load();await router.replace({query:{...route.query,tab:'executeHistory'}})}catch(error){console.error('执行计划失败',error);message.error('执行失败')}finally{busy.value=false}}
function more({key}:{key:string|number}){if(key==='settings'){workspace.value?.openSettings();return}if(key==='archive'&&plan.value?.capabilities?.edit){const id=plan.value.id;Modal.confirm({title:metadata.value?.archived?'取消归档此计划？':'归档此计划？',async onOk(){try{await planWorkspaceApi.saveMetadata(id,{archived:!metadata.value?.archived});await load()}catch(error){console.error('更新计划归档失败',error);message.error('归档操作失败');throw error}}})}if(key==='delete'&&plan.value?.capabilities?.delete){const id=plan.value.id;Modal.confirm({title:'删除此测试计划？',content:'请确认已不再需要此计划。',okType:'danger',async onOk(){try{await testPlanApi.deletePlan(id);message.success('计划已删除');await back()}catch(error){console.error('删除计划失败',error);message.error('删除失败');throw error}}})}}
watch(()=>[projectId.value,planId.value],()=>{plan.value=undefined;metadata.value=undefined;editOpen.value=false;executeOpen.value=false;void load()},{immediate:true})
</script>
<style scoped>.plan-page{background:white;min-width:0;padding:16px;min-height:100%}.plan-heading{display:flex;align-items:center;flex-wrap:wrap;gap:12px;margin-bottom:16px}.plan-heading h2{font-size:18px;flex:1;margin:0;overflow-wrap:anywhere}.plan-progress{display:flex;flex-wrap:wrap;align-items:center;gap:24px;padding:16px;background:var(--ms-surface-muted,#f7f8fa);margin-bottom:16px}.archive-notice{margin-bottom:12px}@media(max-width:768px){.plan-page{padding:12px}.plan-heading h2{flex-basis:100%}.plan-progress{gap:12px}}</style>
