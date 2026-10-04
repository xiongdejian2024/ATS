<template>
  <div>
    <a-space wrap><a-tag :color="reportResultColor(run.report.outcome)">{{reportResultLabel(run.report.outcome)}}</a-tag><span>批次 {{run.id}}</span>
      <a-button @click="emit('refresh')">刷新</a-button><a-button :loading="busy" @click="pdf">导出 PDF</a-button><a-button @click="shareOpen=true">分享报告</a-button></a-space>
    <a-row :gutter="16" class="stats"><a-col :xs="12" :md="6"><a-statistic title="执行项" :value="run.report.total" /></a-col><a-col :xs="12" :md="6"><a-statistic title="通过" :value="run.report.counts.passed" /></a-col><a-col :xs="12" :md="6"><a-statistic title="失败 / 错误" :value="(run.report.counts.failed||0)+(run.report.counts.error||0)" /></a-col><a-col :xs="12" :md="6"><a-statistic title="通过率" :value="run.report.passRate" suffix="%" /></a-col></a-row>
    <a-tabs>
      <a-tab-pane key="plans" tab="计划结果"><a-table :data-source="run.children" :columns="planColumns" row-key="id" size="small" :scroll="{x:650}">
        <template #bodyCell="{column,record}"><a v-if="column.key==='name'" :href="childHref(record.id)" @click.prevent="router.push(childHref(record.id))">{{record.planName}}</a><a-tag v-else-if="column.key==='result'" :color="reportResultColor(record.report.outcome)">{{reportResultLabel(record.report.outcome)}}</a-tag><span v-else-if="column.key==='rate'">{{record.report.passRate}}%</span></template>
      </a-table></a-tab-pane>
      <a-tab-pane key="cases" tab="用例结果"><a-table :data-source="run.report.cases" :columns="caseColumns" :row-key="caseKey" size="small" :scroll="{x:650}"><template #bodyCell="{column,record}"><a-tag v-if="column.key==='result'">{{caseResultLabel(record.result)}}</a-tag></template></a-table></a-tab-pane>
      <a-tab-pane key="summary" tab="报告总结"><a-form layout="vertical"><a-form-item label="测试结论"><a-textarea v-model:value="summary.conclusion" :rows="3" :maxlength="10000" /></a-form-item><a-form-item label="风险与遗留问题"><a-textarea v-model:value="summary.risk" :rows="3" :maxlength="10000" /></a-form-item><a-form-item label="备注"><a-textarea v-model:value="summary.notes" :rows="3" :maxlength="10000" /></a-form-item><a-button type="primary" :loading="busy" @click="save">保存总结</a-button></a-form></a-tab-pane>
    </a-tabs>
  </div>
  <a-modal v-model:open="shareOpen" title="限时只读报告分享" :footer="null"><a-space wrap><span>有效期（小时）</span><a-input-number v-model:value="expiresHours" :min="1" :max="720" /><a-button type="primary" :loading="busy" @click="share">创建分享链接</a-button></a-space>
    <template v-if="shareLink"><a-input :value="shareLink" readonly style="margin:16px 0" /><a-space><a-button @click="copyShare">复制链接</a-button><a-button danger :loading="busy" @click="revoke">撤销此分享</a-button></a-space></template>
  </a-modal>
</template>
<script setup lang="ts">
import {reactive,ref,watch} from 'vue'
import {useRouter} from 'vue-router'
import {message} from 'ant-design-vue'
import {planGroupApi,type GroupRun} from '@/api/planGroup'
import {reportResultLabel,reportResultColor} from '@/api/planReports'
const props=defineProps<{run:GroupRun;projectId:string}>(),emit=defineEmits<{refresh:[]}>(),router=useRouter()
const busy=ref(false),shareOpen=ref(false),expiresHours=ref(24),shareLink=ref(''),shareId=ref('')
const summary=reactive({conclusion:'',risk:'',notes:''})
watch(()=>props.run,run=>Object.assign(summary,{conclusion:'',risk:'',notes:''},run.summary),{immediate:true})
const planColumns=[{title:'计划名称',key:'name'},{title:'结果',key:'result'},{title:'通过率',key:'rate'}]
const caseColumns=[{title:'计划名称',dataIndex:'planName'},{title:'用例名称',dataIndex:'caseName'},{title:'结果',key:'result'},{title:'说明',dataIndex:'notes'}]
const caseKey=(row:any)=>`${row.planRunId}:${row.executionId||'manual'}:${row.associationId||row.caseId}`
const caseLabels:Record<string,string>={passed:'通过',failed:'失败',pending:'未执行',error:'错误',skipped:'跳过',cancelled:'取消'}
const caseResultLabel=(value:string)=>caseLabels[value]||value
const childHref=(id:string)=>router.resolve({name:'TestPlanReportDetail',params:{runId:id},query:{projectId:props.projectId,kind:'PLAN'}}).href
async function operation(task:()=>Promise<void>){busy.value=true;try{await task()}catch(error){console.error('计划组报告操作失败',error);message.error('操作失败，请重试')}finally{busy.value=false}}
async function save(){await operation(async()=>{await planGroupApi.summary(props.run.id,summary);message.success('总结已保存');emit('refresh')})}
async function pdf(){await operation(async()=>{const url=URL.createObjectURL(await planGroupApi.pdf(props.run.id));const a=document.createElement('a');a.href=url;a.download=`ATS-计划组报告-${props.run.id}.pdf`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)})}
async function share(){await operation(async()=>{const result=await planGroupApi.share(props.run.id,expiresHours.value);shareLink.value=new URL(result.path,location.origin).href;shareId.value=result.id})}
async function copyShare(){try{await navigator.clipboard.writeText(shareLink.value);message.success('链接已复制')}catch(error){console.error('复制计划组报告链接失败',error);message.error('复制失败，可从输入框复制')}}
async function revoke(){await operation(async()=>{await planGroupApi.revoke(props.run.id,shareId.value);shareLink.value='';shareId.value='';message.success('分享已撤销')})}
</script>
<style scoped>.stats{margin:20px 0}.stats .ant-col{margin-bottom:12px}</style>
