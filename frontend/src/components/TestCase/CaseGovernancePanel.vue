<template>
  <a-space wrap class="case-governance-toolbar">
    <a-select v-model:value="viewId" placeholder="我的筛选视图" allow-clear style="width: 180px" @change="applyView">
      <a-select-option v-for="v in views" :key="v.id" :value="v.id">{{ v.name }}</a-select-option>
    </a-select>
    <a-button @click="saveVisible = true">保存当前筛选</a-button>
    <a-popconfirm v-if="viewId" title="删除这个个人视图？" @confirm="removeView"><a-button>删除视图</a-button></a-popconfirm>
    <a-button :disabled="!selectedIds.length" @click="batchVisible = true">批量更新属性（{{ selectedIds.length }}）</a-button>
    <a-button :disabled="!selectedIds.length" @click="openCreateReview">发起评审</a-button>
    <a-button @click="openReviews">评审中心</a-button>
  </a-space>

  <a-modal v-model:open="saveVisible" title="保存个人筛选视图" :confirm-loading="busy" @ok="saveView">
    <a-input v-model:value="viewName" placeholder="视图名称" :maxlength="100" />
  </a-modal>
  <a-modal v-model:open="batchVisible" title="批量更新所选用例" :confirm-loading="busy" @ok="batchUpdate">
    <a-alert message="未填写的字段保持原值；每个修改后的用例会保留版本。" type="info" show-icon />
    <a-form layout="vertical" style="margin-top: 16px">
      <a-form-item label="优先级"><a-select v-model:value="batchPriority" allow-clear :options="['P0','P1','P2','P3'].map(v=>({label:v,value:v}))" /></a-form-item>
      <a-form-item label="替换标签（留空不修改）"><a-select v-model:value="batchTags" mode="tags" /></a-form-item>
      <a-form-item label="是否自动化"><a-select v-model:value="batchAutomated" allow-clear :options="[{label:'是',value:'yes'},{label:'否',value:'no'}]" /></a-form-item>
    </a-form>
  </a-modal>
  <a-modal v-model:open="createVisible" title="发起版本评审" :confirm-loading="busy" @ok="createReview">
    <a-form layout="vertical">
      <a-form-item label="评审名称" required><a-input v-model:value="reviewName" :maxlength="200" /></a-form-item>
      <a-form-item label="评审人" required><a-select v-model:value="reviewerIds" mode="multiple" :options="members.map(m=>({label:m.name,value:m.id}))" /></a-form-item>
      <a-form-item label="通过规则"><a-radio-group v-model:value="policy"><a-radio value="all">所有评审人通过</a-radio><a-radio value="any">任意评审人通过</a-radio></a-radio-group></a-form-item>
      <a-alert :message="`将锁定所选 ${selectedIds.length} 条用例的当前版本。后续编辑不会改变评审内容。`" type="info" show-icon />
    </a-form>
  </a-modal>
  <a-modal v-model:open="organizeVisible" :title="organizeMode === 'move' ? '批量移动到模块' : '批量复制到模块'" :confirm-loading="busy" @ok="organize">
    <a-form layout="vertical"><a-form-item label="目标模块"><a-select v-model:value="targetModule" :options="[{label:'未规划',value:'__unassigned__'}, ...modules.map(m=>({label:m.name,value:m.id}))]" /></a-form-item></a-form>
    <a-alert :message="`操作仅限当前项目，影响所选 ${selectedIds.length} 条用例。`" type="info" show-icon />
  </a-modal>

  <a-drawer v-model:open="versionsVisible" title="用例版本与比较" width="min(900px, 96vw)">
    <a-spin :spinning="busy">
      <a-empty v-if="!versions.length" description="这条历史用例尚无版本；下次编辑或提交评审时会保存原始版本。" />
      <template v-else>
        <a-space wrap>
          <a-select v-model:value="beforeVersion" placeholder="旧版本" style="width: 130px" :options="versionOptions" />
          <a-select v-model:value="afterVersion" placeholder="新版本" style="width: 130px" :options="versionOptions" />
          <a-button @click="compare">比较版本</a-button>
        </a-space>
        <a-alert v-if="compared && !changes.length" message="两个版本内容相同" type="info" style="margin-top: 16px" />
        <a-table v-if="changes.length" :columns="diffColumns" :data-source="changes" :pagination="false" row-key="field" style="margin-top: 16px" :scroll="{x:600}">
          <template #bodyCell="{column, record}"><pre v-if="column.key !== 'field'" class="snapshot-text">{{ display(record[column.key]) }}</pre><span v-else>{{ fieldName(record.field) }}</span></template>
        </a-table>
        <a-list :data-source="versions" style="margin-top: 16px">
          <template #renderItem="{item}"><a-list-item><a-list-item-meta :title="`v${item.version} · ${item.snapshot.name}`" :description="`${item.reason} · ${item.createdAt}`" />
            <template #actions><a-button type="link" @click="previewVersion = item">查看快照</a-button><a-button v-if="item.id !== versions[0].id" type="link" @click="restoreTarget = item; restoreReason = ''; restoreVisible = true">恢复此版本</a-button></template>
          </a-list-item></template>
        </a-list>
        <a-card v-if="previewVersion" :title="`版本 v${previewVersion.version} 快照`"><pre class="snapshot-text">{{ display(previewVersion.snapshot) }}</pre></a-card>
      </template>
    </a-spin>
  </a-drawer>
  <a-modal v-model:open="restoreVisible" title="恢复历史版本" :confirm-loading="busy" @ok="restore">
    <a-alert type="warning" show-icon message="恢复将创建一个新版本；当前及历史内容都会保留。若有人同时修改，操作会被拒绝。" />
    <a-textarea v-model:value="restoreReason" placeholder="请填写恢复原因" :maxlength="500" style="margin-top: 16px" />
  </a-modal>

  <a-drawer v-model:open="reviewsVisible" title="用例评审中心" width="min(980px, 96vw)">
    <a-spin :spinning="busy">
      <a-select v-model:value="activeReviewId" placeholder="选择评审单" style="width:100%" :options="reviews.map(r=>({label:`${r.name} · ${statusName(r.status)}`,value:r.id}))" />
      <a-empty v-if="!reviews.length" description="请先勾选用例并发起评审" />
      <template v-if="activeReview">
        <a-space wrap style="margin:16px 0"><a-tag>{{ statusName(activeReview.status) }}</a-tag><span>{{ activeReview.policy === 'all' ? '所有评审人通过' : '任意评审人通过' }}</span>
          <a-popconfirm v-if="activeReview.status === 'pending' && activeReview.createdBy === currentUserId" title="取消此评审？" @confirm="cancelReview"><a-button>取消评审</a-button></a-popconfirm>
        </a-space>
        <a-collapse>
          <a-collapse-panel v-for="item in activeReview.items" :key="item.id" :header="`${item.snapshot.name} · v${item.version} · ${statusName(item.status)}`">
            <a-alert v-if="item.outdated" message="用例当前内容已变化或已删除。本评审结论只适用于以下历史快照。" type="warning" show-icon style="margin-bottom: 12px" />
            <a-descriptions :column="1" bordered size="small"><a-descriptions-item label="前置条件">{{ item.snapshot.precondition || '无' }}</a-descriptions-item><a-descriptions-item label="优先级">{{ item.snapshot.priority }}</a-descriptions-item></a-descriptions>
            <a-table :data-source="item.snapshot.steps || []" :columns="stepColumns" :pagination="false" size="small" style="margin: 12px 0" />
            <a-list :data-source="item.decisions"><template #renderItem="{item: decision}"><a-list-item>{{ memberName(decision.reviewerId) }}：{{ statusName(decision.decision) }} — {{ decision.comment }}</a-list-item></template></a-list>
            <template v-if="canVote(item)"><a-textarea v-model:value="voteComments[item.id]" placeholder="评审结论说明（必填）" :maxlength="10000" /><a-space style="margin-top: 10px"><a-button type="primary" :loading="busy" @click="vote(item, 'approved')">通过</a-button><a-button danger :loading="busy" @click="vote(item, 'rejected')">驳回</a-button></a-space></template>
          </a-collapse-panel>
        </a-collapse>
        <a-divider>讨论意见</a-divider>
        <a-list :data-source="activeReview.comments"><template #renderItem="{item}"><a-list-item>{{ memberName(item.authorId) }}：{{ item.content }}</a-list-item></template></a-list>
        <a-textarea v-model:value="discussion" placeholder="添加讨论意见" :maxlength="10000" />
        <a-button style="margin-top: 12px" :loading="busy" @click="addComment">发表意见</a-button>
      </template>
    </a-spin>
  </a-drawer>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { message } from 'ant-design-vue'
import { useUserStore } from '@/stores/user'
import { projectApi } from '@/api/project'
import { caseGovernanceApi as api, type CaseVersion, type CaseReview, type CaseSavedView, type ReviewItem } from '@/api/caseGovernance'
const props = defineProps<{projectId: string; selectedIds: string[]; filters: Record<string, any>}>()
const emit = defineEmits<{(e:'changed'): void; (e:'apply-view', filters: Record<string, any>): void}>()
const userStore = useUserStore()
const currentUserId = computed(()=> String(userStore.user?.id || ''))
const busy = ref(false)
const views = ref<CaseSavedView[]>([]), viewId = ref<string>(), viewName = ref(''), saveVisible = ref(false)
const batchVisible = ref(false), batchPriority = ref<string>(), batchTags = ref<string[]>([]), batchAutomated = ref<string>()
const organizeVisible = ref(false), organizeMode = ref<'move'|'copy'>('move'), targetModule = ref('__unassigned__'), modules = ref<{id:string;name:string}[]>([])
const createVisible = ref(false), reviewName = ref(''), reviewerIds = ref<string[]>([]), policy = ref('all')
const members = ref<{id:string;name:string}[]>([]), reviews = ref<CaseReview[]>([]), activeReviewId = ref<string>(), reviewsVisible = ref(false)
const activeReview = computed(()=>reviews.value.find(r=>r.id === activeReviewId.value))
const voteComments = ref<Record<string,string>>({}), discussion = ref('')
const versionsVisible = ref(false), versions = ref<CaseVersion[]>([]), activeCaseId = ref(''), beforeVersion = ref<number>(), afterVersion = ref<number>()
const previewVersion = ref<CaseVersion>(), restoreTarget = ref<CaseVersion>(), restoreVisible = ref(false), restoreReason = ref('')
const compared = ref(false), changes = ref<{field:string;before:any;after:any}[]>([])
const versionOptions = computed(()=>versions.value.map(v=>({label:`v${v.version}`,value:v.version})))
const diffColumns = [{title:'字段',dataIndex:'field',key:'field'},{title:'旧内容',key:'before'},{title:'新内容',key:'after'}]
const stepColumns = [{title:'步骤',dataIndex:'step'},{title:'操作',dataIndex:'action'},{title:'预期结果',dataIndex:'expected'}]
const statusName = (v:string)=>({pending:'待评审',approved:'通过',rejected:'驳回',cancelled:'已取消'}[v] || v)
const fieldName = (v:string)=>({case_code:'用例编号',name:'名称',type:'用例类型',priority:'优先级',level:'用例等级',steps:'步骤',precondition:'前置条件',tags:'标签',is_automated:'是否自动化',module_id:'模块',module_path:'模块路径',executor_id:'执行人',requirement_ref:'需求关联'}[v] || v)
const display = (value:any)=> typeof value === 'string' ? value : JSON.stringify(value, null, 2)
const memberName = (id:string)=>members.value.find(m=>m.id === id)?.name || id
async function run(work:()=>Promise<void>) {busy.value=true; try {await work()} catch(error:any) {console.error('用例治理操作失败',error); message.error(error.response?.data?.detail || '操作失败，请重试')} finally {busy.value=false}}
watch(()=>props.projectId, async p=>{views.value=[];viewId.value=undefined;versionsVisible.value=false;reviewsVisible.value=false; if(p) await run(async()=>{views.value=await api.views(p)})},{immediate:true})
function applyView(id?:string) {const view=views.value.find(v=>v.id===id); if(view) emit('apply-view',JSON.parse(JSON.stringify(view.filters)))}
async function saveView(){if(!viewName.value.trim())return message.warning('请填写视图名称');await run(async()=>{const view=await api.saveView(props.projectId,viewName.value.trim(),props.filters);views.value.unshift(view);viewId.value=view.id;saveVisible.value=false;viewName.value='';message.success('个人筛选视图已保存')})}
async function removeView(){if(!viewId.value)return;await run(async()=>{await api.deleteView(props.projectId,viewId.value!);views.value=views.value.filter(v=>v.id!==viewId.value);viewId.value=undefined})}
async function batchUpdate(){const data:Record<string,any>={caseIds:props.selectedIds};if(batchPriority.value)data.priority=batchPriority.value;if(batchTags.value.length)data.tags=batchTags.value;if(batchAutomated.value)data.isAutomated=batchAutomated.value==='yes';if(Object.keys(data).length===1)return message.warning('请选择需要修改的属性');await run(async()=>{const result=await api.batch(props.projectId,data);batchVisible.value=false;emit('changed');message.success(`已更新 ${result.updated} 条用例`)})}
async function openOrganize(mode:'move'|'copy'){organizeMode.value=mode;await run(async()=>{modules.value=await projectApi.getModules(props.projectId);targetModule.value='__unassigned__';organizeVisible.value=true})}
async function organize(){await run(async()=>{const moduleId=targetModule.value==='__unassigned__'?null:targetModule.value;if(organizeMode.value==='move')await api.batch(props.projectId,{caseIds:props.selectedIds,moduleId});else await api.copy(props.projectId,props.selectedIds,moduleId);organizeVisible.value=false;emit('changed');message.success(organizeMode.value==='move'?'所选用例已移动':'所选用例已复制')})}
async function openCreateReview(){await run(async()=>{members.value=await api.reviewers(props.projectId);reviewerIds.value=members.value.some(m=>m.id===currentUserId.value)?[currentUserId.value]:[];reviewName.value='';createVisible.value=true})}
async function createReview(){if(!reviewName.value.trim()||!reviewerIds.value.length)return message.warning('请填写名称并选择评审人');await run(async()=>{const review=await api.createReview(props.projectId,{name:reviewName.value.trim(),caseIds:props.selectedIds,reviewerIds:reviewerIds.value,policy:policy.value});reviews.value=await api.reviews(props.projectId);activeReviewId.value=review.id;createVisible.value=false;reviewsVisible.value=true;emit('changed')})}
async function openReviews(){await run(async()=>{[reviews.value,members.value]=await Promise.all([api.reviews(props.projectId),api.reviewers(props.projectId)]);activeReviewId.value=reviews.value[0]?.id;reviewsVisible.value=true})}
function canVote(item:ReviewItem){return activeReview.value?.status==='pending' && activeReview.value.reviewerIds.includes(currentUserId.value) && item.status==='pending' && !item.decisions.some(d=>d.reviewerId===currentUserId.value)}
function replaceReview(review:CaseReview){reviews.value=reviews.value.map(r=>r.id===review.id?review:r);emit('changed')}
async function vote(item:ReviewItem,decision:string){const text=voteComments.value[item.id]?.trim();if(!text)return message.warning('请填写评审结论说明');await run(async()=>{replaceReview(await api.vote(props.projectId,activeReviewId.value!,item.id,decision,text));voteComments.value[item.id]=''})}
async function addComment(){if(!discussion.value.trim())return message.warning('请填写意见');await run(async()=>{replaceReview(await api.comment(props.projectId,activeReviewId.value!,discussion.value.trim()));discussion.value=''})}
async function cancelReview(){await run(async()=>replaceReview(await api.cancel(props.projectId,activeReviewId.value!)))}
async function openVersions(caseId:string){activeCaseId.value=caseId;compared.value=false;changes.value=[];previewVersion.value=undefined;await run(async()=>{versions.value=await api.versions(props.projectId,caseId);afterVersion.value=versions.value[0]?.version;beforeVersion.value=versions.value[1]?.version ?? afterVersion.value;versionsVisible.value=true})}
async function compare(){if(!beforeVersion.value||!afterVersion.value)return;await run(async()=>{changes.value=(await api.compare(props.projectId,activeCaseId.value,beforeVersion.value!,afterVersion.value!)).changes;compared.value=true})}
async function restore(){if(!restoreReason.value.trim()||!restoreTarget.value)return message.warning('请填写恢复原因');await run(async()=>{await api.restore(props.projectId,activeCaseId.value,restoreTarget.value!.id,versions.value[0].version,restoreReason.value.trim());versions.value=await api.versions(props.projectId,activeCaseId.value);afterVersion.value=versions.value[0]?.version;changes.value=[];compared.value=false;restoreVisible.value=false;emit('changed');message.success('已恢复并创建新版本')})}
defineExpose({openVersions,openOrganize,openBatch:()=>{batchVisible.value=true}})
</script>

<style scoped>
.case-governance-toolbar{padding:8px 0;width:100%}.snapshot-text{white-space:pre-wrap;overflow-wrap:anywhere;max-width:100%;max-height:360px;overflow:auto;font-size:12px;margin:0}
</style>
