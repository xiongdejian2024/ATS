<template>
  <a-spin :spinning="loading">
    <template v-if="run">
      <a-space wrap><a-tag>{{label(run.status)}}</a-tag><span>批次 {{run.id}}</span><a-button @click="load">刷新</a-button><a-button @click="exportJson">JSON</a-button><a-button @click="pdf">导出 PDF</a-button><a-button @click="shareOpen=true;loadShares()">分享报告</a-button></a-space>
      <a-row :gutter="16" class="stats"><a-col :span="6"><a-statistic title="执行项" :value="run.report.total" /></a-col><a-col :span="6"><a-statistic title="通过" :value="run.report.counts.passed" /></a-col><a-col :span="6"><a-statistic title="失败 / 错误" :value="run.report.counts.failed+run.report.counts.error" /></a-col><a-col :span="6"><a-statistic title="通过率" :value="run.report.passRate" suffix="%" /></a-col></a-row>
      <a-tabs>
        <a-tab-pane key="results" tab="用例与步骤执行">
          <a-space wrap class="result-filters" style="margin:8px 0"><a-select v-model:value="category" allow-clear placeholder="全部分类" style="width:120px" :options="[{value:'functional',label:'功能'},{value:'api',label:'API'},{value:'scenario',label:'场景'}]" /><a-select v-model:value="resultFilter" allow-clear placeholder="全部结果" style="width:120px" :options="resultOptions" /><a-radio-group v-model:value="view"><a-radio-button value="table">列表</a-radio-button><a-radio-button value="mind">脑图执行</a-radio-button></a-radio-group></a-space>
          <CaseMindMap v-if="view==='mind'" :cases="mindCases" :modules="mindModules" readonly @select="selectMind" />
          <a-table v-else :data-source="filtered" :columns="columns" :row-key="rowKey" size="small" :scroll="{x:650}"><template #bodyCell="{column,record}"><template v-if="column.key==='result'"><a-tag>{{label(record.result)}}</a-tag></template><template v-else-if="column.key==='actions'"><a-button type="link" size="small" @click="openCase(record)">{{canFill(record)?'执行 / 逐步骤回填':'查看步骤 / 协作'}}</a-button></template></template></a-table>
        </a-tab-pane>
        <a-tab-pane key="segments" tab="分类统计"><a-table :data-source="segments" :columns="segmentColumns" :pagination="false" row-key="category" size="small" /></a-tab-pane>
        <a-tab-pane key="summary" tab="报告总结"><a-form layout="vertical"><a-form-item label="测试结论"><a-textarea v-model:value="summary.conclusion" :rows="3" /></a-form-item><a-form-item label="风险与遗留问题"><a-textarea v-model:value="summary.risk" :rows="3" /></a-form-item><a-form-item label="备注"><a-textarea v-model:value="summary.notes" :rows="3" /></a-form-item><a-button type="primary" @click="saveSummary">保存总结</a-button></a-form></a-tab-pane>
      </a-tabs>
    </template>
  </a-spin>
  <a-drawer v-model:open="caseOpen" :title="current?.caseName" width="min(100vw,900px)">
    <template v-if="current">
      <a-alert v-if="current.linkedAutomation" type="info" message="该功能用例的结果由关联自动化批次更新。" />
      <p>前置条件：{{current.snapshot?.precondition || '无'}}</p>
      <a-table :data-source="stepRows" :columns="stepColumns" row-key="index" :pagination="false" size="small" :scroll="{x:700}">
        <template #bodyCell="{column,record}">
          <template v-if="column.key==='index'">{{record.index+1}}</template>
          <template v-else-if="column.key==='result'"><a-select v-model:value="record.result" :disabled="!canFill(current)" :options="resultOptions" style="width:95px" /></template>
          <template v-else-if="column.key==='actual'"><a-textarea v-model:value="record.actual" :disabled="!canFill(current)" :rows="2" placeholder="记录实际结果" /></template>
          <template v-else-if="column.key==='evidence'"><a-select v-model:value="record.defectIds" mode="multiple" :disabled="!canFill(current)" style="width:160px" placeholder="关联缺陷" :options="defects.map(d=>({value:d.id,label:d.title}))" /><a-select v-model:value="record.attachments" mode="multiple" :disabled="!canFill(current)" style="width:160px;margin-top:6px" placeholder="关联附件" :options="collab.attachments.map(a=>({value:a.id,label:a.name}))" /></template>
        </template>
      </a-table>
      <a-empty v-if="!stepRows.length" description="此用例未定义步骤，可回填整体结果" />
      <a-space style="margin:16px 0"><span>整体结果</span><a-select v-model:value="manual.result" :disabled="!canFill(current)" :options="resultOptions" style="width:130px" /><a-button v-if="canFill(current)" type="primary" @click="saveResult">保存步骤和结果</a-button></a-space>
      <a-textarea v-model:value="manual.notes" :disabled="!canFill(current)" placeholder="实际结果与说明" :rows="3" />
      <a-divider>证据与缺陷</a-divider>
      <a-space wrap><a-upload :before-upload="upload" :show-upload-list="false"><a-button>上传附件（≤5MB）</a-button></a-upload><a-input v-model:value="defectTitle" placeholder="新缺陷标题" style="width:230px" /><a-button @click="createDefect">创建缺陷</a-button></a-space>
      <p v-for="attachment in collab.attachments" :key="attachment.id"><a @click="downloadAttachment(attachment)">{{attachment.name}}</a></p>
      <a-divider>执行讨论</a-divider>
      <a-list :data-source="collab.comments" size="small"><template #renderItem="{item}"><a-list-item><div><small>{{item.authorId}} · {{new Date(item.createdAt).toLocaleString('zh-CN')}}</small><p style="white-space:pre-wrap">{{item.content}}</p></div></a-list-item></template></a-list>
      <a-textarea v-model:value="comment" placeholder="添加执行评论" :rows="2" /><a-button style="margin-top:8px" @click="sendComment">发布评论</a-button>
    </template>
  </a-drawer>
  <a-modal v-model:open="shareOpen" title="限时只读报告分享" :footer="null">
    <a-space><span>有效期（小时）</span><a-input-number v-model:value="expiresHours" :min="1" :max="2160" /><a-button type="primary" @click="createShare">创建分享链接</a-button></a-space>
    <a-input v-if="shareUrl" :value="shareUrl" readonly style="margin:16px 0" /><p v-if="shareUrl">链接直接打开 PDF，只在有效期内可访问。</p>
    <a-list :data-source="shares"><template #renderItem="{item}"><a-list-item><span>{{new Date(item.expiresAt).toLocaleString('zh-CN')}} 到期 · {{item.revoked?'已撤销':'可访问'}}</span><a-button v-if="!item.revoked" danger size="small" @click="revoke(item.id)">撤销</a-button></a-list-item></template></a-list>
  </a-modal>
</template>
<script setup lang="ts">
import {ref,reactive,computed,onMounted,watch} from 'vue'
import {message} from 'ant-design-vue'
import type {TestCase} from '@/types'
import CaseMindMap from '@/components/TestCase/CaseMindMap.vue'
import {planCollaborationApi,downloadPlanFile,type ReportRun,type ReportCase,type StepResult} from '@/api/planCollaboration'
import {caseFeaturesApi,type CaseIssue} from '@/api/caseFeatures'
const props=defineProps<{runId:string;projectId:string}>(),emit=defineEmits<{changed:[]}>()
const run=ref<ReportRun>(),loading=ref(false),category=ref<string>(),resultFilter=ref<string>(),view=ref('table')
const labels:Record<string,string>={group_waiting:'等待计划组前序',queued:'排队中',running:'执行中',cancelling:'取消中',needs_confirmation:'等待核对',cancelled:'已取消',completed:'已完成',passed:'通过',failed:'失败',error:'错误',skipped:'跳过',pending:'未执行'}
const label=(s:string)=>labels[s]||s
const resultOptions=['pending','passed','failed','error','skipped'].map(value=>({value,label:label(value)}))
const columns=[{title:'用例',dataIndex:'caseName'},{title:'测试套',dataIndex:'suiteName'},{title:'结果',key:'result'},{title:'说明',dataIndex:'notes'},{title:'操作',key:'actions'}]
const segmentColumns=[{title:'分类',dataIndex:'category'},{title:'执行项',dataIndex:'total'},{title:'通过',dataIndex:'passed'},{title:'失败/错误',dataIndex:'failed'},{title:'通过率',dataIndex:'rate'}]
const categoryName:Record<string,string>={functional:'功能',api:'API',scenario:'场景'}
const filtered=computed(()=>((run.value?.report.cases||[]) as ReportCase[]).filter(row=>(!category.value || row.category===category.value)&&(!resultFilter.value || row.result===resultFilter.value)))
const segments=computed(()=>Object.entries(run.value?.report.categories||{}).map(([category,c])=>({category:categoryName[category]||category,total:c.total,passed:c.counts.passed||0,failed:(c.counts.failed||0)+(c.counts.error||0),rate:(100*(c.counts.passed||0)/c.total).toFixed(1)+'%'})))
const rowKey=(row:ReportCase)=>`${row.executionId||'manual'}:${row.associationId||row.caseId}:${row.caseId}`
const mindCases=computed(()=>filtered.value.map(row=>({id:rowKey(row),name:`[${label(row.result)}] ${row.caseName}`,moduleId:row.category||'functional',precondition:row.snapshot?.precondition,steps:row.snapshot?.steps||[],status:row.result} as Partial<TestCase>)))
const mindModules=Object.entries(categoryName).map(([id,name])=>({id,name}))
function selectMind(c:Partial<TestCase>){const row=filtered.value.find(row=>rowKey(row)===c.id);if(row)void openCase(row)}
const summary=reactive({conclusion:'',risk:'',notes:''})
async function load(){loading.value=true;try{run.value=await planCollaborationApi.report(props.runId);Object.assign(summary,{conclusion:'',risk:'',notes:''},run.value.summary)}catch(error){console.error('读取计划报告失败',error);message.error('读取报告失败')}finally{loading.value=false}}
async function saveSummary(){try{await planCollaborationApi.summary(props.runId,summary);message.success('总结已保存')}catch(error){console.error('保存计划总结失败',error);message.error('保存失败')}}
async function pdf(){try{await downloadPlanFile(`runs/${props.runId}/pdf`,`ATS-计划报告-${props.runId}.pdf`)}catch(error){console.error('导出PDF失败',error);message.error('导出PDF失败')}}
function exportJson(){const url=URL.createObjectURL(new Blob([JSON.stringify(run.value,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download=`ATS-计划报告-${props.runId}.json`;a.click();URL.revokeObjectURL(url)}
const caseOpen=ref(false),current=ref<ReportCase>(),stepRows=ref<(StepResult & {action:string;expected:string})[]>([]),manual=reactive({result:'passed',notes:''}),comment=ref(''),defectTitle=ref(''),defects=ref<CaseIssue[]>([])
const collab=reactive<{comments:{id:string;content:string;authorId:string;createdAt:string}[];attachments:{id:string;name:string}[]}>({comments:[],attachments:[]})
const stepColumns=[{title:'#',key:'index',width:40},{title:'步骤',dataIndex:'action',width:140},{title:'预期',dataIndex:'expected',width:140},{title:'结果',key:'result',width:110},{title:'实际结果',key:'actual',width:170},{title:'缺陷 / 附件',key:'evidence',width:180}]
const canFill=(row:ReportCase)=>!row.executionId && !row.linkedAutomation && ['queued','running'].includes(run.value?.status||'')
const association=()=>current.value?.associationId||current.value?.caseId||''
async function reloadCollab(){Object.assign(collab,await planCollaborationApi.collaboration(props.runId,association()));defects.value=await caseFeaturesApi.issues(props.projectId,{kind:'defect'})}
async function openCase(row:ReportCase){current.value=row;manual.result=row.result==='pending'?'passed':row.result;manual.notes=row.notes||'';stepRows.value=(row.snapshot?.steps||[]).map((step,index)=>({index,action:step.action||'',expected:step.expected||'',result:'pending',actual:'',notes:'',defectIds:[],attachments:[],...(row.stepResults||[]).find(s=>s.index===index)}));caseOpen.value=true;try{await reloadCollab()}catch(error){console.error('读取计划执行协作失败',error);message.error('读取执行协作失败')}}
async function saveResult(){try{await planCollaborationApi.result(props.runId,association(),{...manual,stepResults:stepRows.value.map(({action,expected,...step})=>step)});message.success('执行结果已保存');caseOpen.value=false;await load();emit('changed')}catch(error){console.error('保存步骤执行结果失败',error);message.error('保存失败，请核对步骤结果')}}
async function upload(file:File){if(file.size>5*1024*1024){message.error('附件超过5MB');return false}try{const encoded=await new Promise<string>((resolve,reject)=>{const reader=new FileReader();reader.onload=()=>resolve(String(reader.result).split(',')[1]);reader.onerror=()=>reject(reader.error);reader.readAsDataURL(file)});await planCollaborationApi.attachment(props.runId,association(),{name:file.name,mimeType:file.type,contentBase64:encoded});await reloadCollab();message.success('附件已保存，可关联到步骤')}catch(error){console.error('上传计划附件失败',error);message.error('上传失败')}return false}
async function downloadAttachment(file:{id:string;name:string}){try{await downloadPlanFile(`attachments/${file.id}`,file.name)}catch(error){console.error('下载计划附件失败',error);message.error('下载失败')}}
async function sendComment(){if(!comment.value.trim())return;try{await planCollaborationApi.comment(props.runId,association(),comment.value);comment.value='';await reloadCollab()}catch(error){console.error('发布计划评论失败',error);message.error('发布失败')}}
async function createDefect(){if(!defectTitle.value.trim())return;try{const defect=await caseFeaturesApi.saveIssue(props.projectId,{kind:'defect',title:defectTitle.value,description:`计划批次 ${props.runId} / ${current.value?.caseName}`,status:'open'});defectTitle.value='';await reloadCollab();if(stepRows.value.length)stepRows.value[0].defectIds.push(defect.id);message.success('缺陷已创建，请保存步骤关联')}catch(error){console.error('创建执行缺陷失败',error);message.error('创建缺陷失败')}}
const shareOpen=ref(false),expiresHours=ref(24),shareUrl=ref(''),shares=ref<{id:string;expiresAt:string;revoked:boolean}[]>([])
async function loadShares(){try{shares.value=await planCollaborationApi.shares(props.runId)}catch(error){console.error('读取报告分享失败',error);message.error('读取分享失败')}}
async function createShare(){try{const result=await planCollaborationApi.share(props.runId,expiresHours.value);shareUrl.value=new URL(result.path,window.location.origin).href;await loadShares()}catch(error){console.error('创建报告分享失败',error);message.error('创建分享失败')}}
async function revoke(id:string){try{await planCollaborationApi.revoke(id);await loadShares()}catch(error){console.error('撤销报告分享失败',error);message.error('撤销失败')}}
onMounted(load);watch(()=>props.runId,load)
</script>
<style scoped>.stats{margin:20px 0}.result-filters :deep(.ant-radio-group){white-space:nowrap}.result-filters :deep(.ant-space-item){flex-shrink:0}</style>
