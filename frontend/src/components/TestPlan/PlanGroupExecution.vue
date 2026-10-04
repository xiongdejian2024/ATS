<template>
  <a-space wrap v-if="groupId">
    <a-button @click="openSettings">组执行配置</a-button>
    <a-popconfirm title="按保存的策略执行组内全部计划？" @confirm="execute"><a-button type="primary" :loading="busy">执行计划组</a-button></a-popconfirm>
    <a-button @click="openSchedule">组定时任务</a-button>
    <a-button @click="openHistory">组执行报告</a-button>
  </a-space>
  <a-modal v-model:open="settingsOpen" title="计划组执行配置" :confirm-loading="busy" @ok="saveSettings">
    <a-form layout="vertical">
      <a-form-item label="计划执行方式"><a-radio-group v-model:value="policy.executionMode"><a-radio value="serial">串行</a-radio><a-radio value="parallel">并行</a-radio></a-radio-group></a-form-item>
      <a-form-item label="失败后停止后续计划"><a-switch v-model:checked="policy.stopOnFailure" /></a-form-item>
      <a-form-item label="组报告通过阈值"><a-input-number v-model:value="policy.passThreshold" :min="0" :max="100" /> %</a-form-item>
      <a-form-item label="计划执行顺序"><div v-for="(member,index) in policy.members" :key="member.id" class="member-order"><span>{{index+1}}. {{member.name}}</span><a-space><a-button size="small" :disabled="index===0" @click="moveMember(index,-1)">上移</a-button><a-button size="small" :disabled="index===(policy.members?.length || 0)-1" @click="moveMember(index,1)">下移</a-button></a-space></div></a-form-item>
      <p>执行时冻结组内各计划的用例与配置，报告按全部执行项汇总。正在运行的计划仍等待节点确认结果。</p>
    </a-form>
  </a-modal>
  <a-modal v-model:open="scheduleOpen" title="创建计划组定时任务" :confirm-loading="busy" @ok="saveSchedule">
    <a-form layout="vertical"><a-form-item label="名称"><a-input v-model:value="schedule.name" /></a-form-item><a-form-item label="Cron（分 时 日 月 周）"><a-input v-model:value="schedule.cron" placeholder="0 9 * * 1-5" /></a-form-item><a-form-item label="时区"><a-select v-model:value="schedule.timezone" :options="[{value:'Asia/Shanghai',label:'中国标准时间'},{value:'UTC',label:'UTC'}]" /></a-form-item></a-form>
    <a-alert message="保存后保持停用，可在任务中心查看下次执行时间并启用。" type="info" />
  </a-modal>
  <a-drawer v-model:open="historyOpen" title="计划组执行历史" width="min(900px, 96vw)">
    <a-button @click="loadHistory">刷新</a-button>
    <a-table :data-source="history" :columns="historyColumns" row-key="id" :pagination="{current: page, total, pageSize:20}" :scroll="{x:620}" @change="onPage">
      <template #bodyCell="{column,record}"><template v-if="column.key==='status'">{{ label(record.status) }}</template><template v-else-if="column.key==='actions'"><a-button type="link" @click="openReport(record.id)">查看聚合报告</a-button></template></template>
    </a-table>
  </a-drawer>
  <a-modal v-model:open="reportOpen" :title="`${run?.groupName || '计划组'} · 聚合报告`" width="min(1080px, 96vw)" :footer="null">
    <template v-if="run">
      <a-space wrap><a-tag>{{ label(run.status) }}</a-tag><span>执行项 {{run.report.total}} · 通过率 {{run.report.passRate}}%</span><a-button @click="openReport(run.id)">刷新报告</a-button><a-button @click="download">导出 PDF</a-button><a-button @click="shareOpen=true">分享报告</a-button><a-popconfirm v-if="active(run.status)" title="取消组内尚未结束的计划？" @confirm="cancel"><a-button danger>取消组执行</a-button></a-popconfirm></a-space>
      <a-divider />
      <a-table :data-source="run.children" :columns="childColumns" row-key="id" size="small" :scroll="{x:600}">
        <template #bodyCell="{column,record}"><template v-if="column.key==='name'"><a @click="openChild(record)">{{record.planName}}</a></template><template v-else-if="column.key==='status'">{{label(record.status)}}</template><template v-else-if="column.key==='rate'">{{record.report.passRate}}%</template></template>
      </a-table>
      <a-form layout="vertical"><a-form-item label="报告结论"><a-textarea v-model:value="summary.conclusion" :rows="2" /></a-form-item><a-form-item label="风险"><a-textarea v-model:value="summary.risk" :rows="2" /></a-form-item><a-form-item label="补充说明"><a-textarea v-model:value="summary.notes" :rows="2" /></a-form-item><a-button :loading="busy" @click="saveSummary">保存报告总结</a-button></a-form>
    </template>
  </a-modal>
  <a-modal v-model:open="shareOpen" title="分享聚合报告" :footer="null">
    <a-space><span>有效期（小时）</span><a-input-number v-model:value="expiresHours" :min="1" :max="720" /><a-button :loading="busy" @click="createShare">生成链接</a-button></a-space>
    <template v-if="shareLink"><a-input :value="shareLink" readonly style="margin-top:16px" /><p>拥有链接的人可在有效期内查看 PDF。</p><a-space><a-button @click="copyShare">复制链接</a-button><a-button danger @click="revokeShare">撤销此分享</a-button></a-space></template>
  </a-modal>
</template>
<script setup lang="ts">
import { reactive, ref, watch } from 'vue'
import { message } from 'ant-design-vue'
import { useRouter } from 'vue-router'
import { planGroupApi, type GroupPolicy, type GroupRun } from '@/api/planGroup'
import { taskCenterApi } from '@/api/taskCenter'
import type { PlanRun } from '@/api/planOrchestration'
const props=defineProps<{groupId?:string;projectId:string;groupName?:string;runId?:string}>()
const router=useRouter(), busy=ref(false),settingsOpen=ref(false),scheduleOpen=ref(false),historyOpen=ref(false),reportOpen=ref(false),shareOpen=ref(false)
const policy=ref<GroupPolicy>({executionMode:'serial',stopOnFailure:false,passThreshold:100,planOrder:[]})
const schedule=reactive({name:'',cron:'0 9 * * 1-5',timezone:'Asia/Shanghai'})
const history=ref<GroupRun[]>([]),run=ref<GroupRun>(),page=ref(1),total=ref(0),requestId=ref('')
const summary=reactive({conclusion:'',risk:'',notes:''}),expiresHours=ref(24),shareLink=ref(''),shareId=ref('')
const historyColumns=[{title:'创建时间',dataIndex:'startedAt'},{title:'状态',key:'status'},{title:'操作',key:'actions'}]
const childColumns=[{title:'计划',key:'name'},{title:'状态',key:'status'},{title:'通过率',key:'rate'}]
const label=(s:string)=>({group_waiting:'等待前序计划',queued:'排队中',running:'执行中',needs_confirmation:'待核对节点',cancelling:'取消中',cancelled:'已取消',completed:'已通过',failed:'失败',skipped:'跳过'}[s]||s)
const active=(s:string)=>!['completed','failed','cancelled','skipped'].includes(s)
function moveMember(index:number,delta:number){const members=policy.value.members;if(!members || index+delta<0 || index+delta>=members.length)return;const [member]=members.splice(index,1);members.splice(index+delta,0,member);policy.value.planOrder=members.map(p=>p.id)}
async function operation(task:()=>Promise<void>){busy.value=true;try{await task()}catch(error){console.error('计划组操作失败',error);message.error('操作失败，请检查配置或服务提示')}finally{busy.value=false}}
async function openSettings(){if(!props.groupId)return;await operation(async()=>{policy.value=await planGroupApi.settings(props.groupId!);settingsOpen.value=true})}
async function saveSettings(){if(!props.groupId)return;await operation(async()=>{policy.value=await planGroupApi.save(props.groupId!,policy.value);settingsOpen.value=false;message.success('计划组配置已保存')})}
async function execute(){if(!props.groupId)return;await operation(async()=>{requestId.value ||= crypto.randomUUID();const value=await planGroupApi.execute(props.groupId!,requestId.value);requestId.value='';await openReport(value.id);message.success('计划组已创建执行批次')})}
function openSchedule(){schedule.name=`${props.groupName || '计划组'}定时执行`;scheduleOpen.value=true}
async function saveSchedule(){if(!props.groupId)return;await operation(async()=>{await taskCenterApi.create({projectId:props.projectId,name:schedule.name,targetType:'group',targetId:props.groupId!,cronExpression:schedule.cron,timezone:schedule.timezone});scheduleOpen.value=false;message.success('已保存，请在任务中心启用')})}
async function loadHistory(){if(!props.groupId)return;await operation(async()=>{const data=await planGroupApi.history(props.groupId!,page.value);history.value=data.items;total.value=data.total})}
async function openHistory(){historyOpen.value=true;page.value=1;await loadHistory()}
async function onPage(p:{current?:number}){page.value=p.current || 1;await loadHistory()}
async function openReport(id:string){await operation(async()=>{run.value=await planGroupApi.run(id);Object.assign(summary,{conclusion:'',risk:'',notes:''},run.value.summary);reportOpen.value=true})}
async function saveSummary(){if(!run.value)return;await operation(async()=>{run.value=await planGroupApi.summary(run.value!.id,summary);message.success('报告总结已保存')})}
async function cancel(){if(!run.value)return;await operation(async()=>{run.value=await planGroupApi.cancel(run.value!.id);message.success('已请求取消计划组')})}
function openChild(child:PlanRun){reportOpen.value=false;historyOpen.value=false;router.push({path:'/test-plans',query:{planId:child.planId,runId:child.id}})}
async function download(){if(!run.value)return;await operation(async()=>{const blob=await planGroupApi.pdf(run.value!.id);const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=`ATS-计划组报告-${run.value!.id}.pdf`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)})}
async function createShare(){if(!run.value)return;await operation(async()=>{const data=await planGroupApi.share(run.value!.id,expiresHours.value);shareId.value=data.id;shareLink.value=new URL(data.path,location.origin).href})}
async function copyShare(){try{await navigator.clipboard.writeText(shareLink.value);message.success('分享链接已复制')}catch(error){console.error('复制分享链接失败',error);message.warning('请选中上方链接手动复制')}}
async function revokeShare(){if(!run.value || !shareId.value)return;await operation(async()=>{await planGroupApi.revoke(run.value!.id,shareId.value);shareLink.value='';shareId.value='';message.success('分享已撤销')})}
watch(()=>props.runId,id=>{if(id)void openReport(id)},{immediate:true})
watch(()=>props.groupId,()=>{historyOpen.value=false;settingsOpen.value=false;requestId.value=''})
defineExpose({openReport})
</script>
<style scoped>.member-order{display:flex;justify-content:space-between;gap:12px;margin-bottom:8px}.member-order span{overflow-wrap:anywhere}</style>
