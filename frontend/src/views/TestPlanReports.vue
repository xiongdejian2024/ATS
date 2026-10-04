<template>
  <section class="report-list">
    <a-alert v-if="!projectId" message="请选择项目" type="info" />
    <template v-else>
      <div class="report-toolbar">
        <a-space wrap><a-radio-group v-model:value="showType" @change="changeType"><a-radio-button value="ALL">全部</a-radio-button><a-radio-button value="PLAN">测试计划报告</a-radio-button><a-radio-button value="GROUP">测试计划组报告</a-radio-button></a-radio-group><a-button @click="expanded = !expanded" :aria-expanded="expanded">高级筛选</a-button></a-space>
        <a-space wrap><a-input-search v-model:value="search" placeholder="搜索报告名称" allow-clear @search="apply" /><a-button aria-label="刷新报告列表" :loading="loading" @click="load"><ReloadOutlined /></a-button></a-space>
      </div>
      <a-form v-if="expanded" :model="filters" class="report-filters" layout="vertical" @finish="apply">
        <a-form-item label="所属计划"><a-input v-model:value="filters.plan_name" placeholder="计划或计划组名称" /></a-form-item>
        <a-form-item label="报告类型"><a-select v-model:value="filters.kind" allow-clear placeholder="全部类型" :options="[{value:'PLAN',label:'普通报告'},{value:'GROUP',label:'集成报告'}]" /></a-form-item>
        <a-form-item label="结果"><a-select v-model:value="filters.result_status" allow-clear placeholder="全部结果" :options="reportResultOptions" /></a-form-item>
        <a-form-item label="触发方式"><a-select v-model:value="filters.trigger_mode" allow-clear placeholder="全部方式" :options="[{value:'manual',label:'手动触发'},{value:'cron',label:'定时触发'}]" /></a-form-item>
        <a-form-item label="操作人"><a-input v-model:value="filters.operator" placeholder="操作人姓名" /></a-form-item>
        <a-form-item label="通过率"><a-space><a-input-number v-model:value="filters.min_rate" :min="0" :max="100" placeholder="最小 %" /><span>～</span><a-input-number v-model:value="filters.max_rate" :min="0" :max="100" placeholder="最大 %" /></a-space></a-form-item>
        <a-form-item label="操作时间" class="date-filter"><a-range-picker v-model:value="dates" show-time format="YYYY-MM-DD HH:mm" /></a-form-item>
        <a-space class="filter-actions"><a-button type="primary" html-type="submit">查询</a-button><a-button @click="reset">重置</a-button></a-space>
      </a-form>
      <a-alert v-if="failed" type="error" show-icon message="报告加载失败" class="load-error"><template #action><a-button size="small" @click="load">重试</a-button></template></a-alert>
      <a-space v-if="canDelete && selected.length" class="batch-toolbar"><span>已选择 {{selected.length}} 条</span><a-button danger :loading="busy" @click="deleteSelected">批量删除</a-button><a-button @click="selected=[]">取消选择</a-button></a-space>
      <a-table :data-source="items" :columns="columns" :loading="loading" :row-key="rowKey" :scroll="{x:1600}" size="small"
        :row-selection="canDelete?{selectedRowKeys:selected,onChange:(keys:any)=>selected=keys}:undefined"
        :pagination="{current:page,pageSize:size,total,showSizeChanger:true,pageSizeOptions:['10','20','50','100'],showTotal:(n:number)=>`共 ${n} 条`}"
        @change="tableChange">
        <template #bodyCell="{column,record}">
          <div v-if="column.key==='name'" class="report-name">
            <template v-if="editing===rowKey(record)"><a-input v-model:value="editName" :maxlength="255" aria-label="报告新名称" :disabled="busy" @press-enter="rename(record)" @keydown.esc="editing=''" /><a-button type="text" size="small" aria-label="保存报告名称" :loading="busy" @click="rename(record)"><CheckOutlined /></a-button><a-button type="text" size="small" aria-label="取消重命名" :disabled="busy" @click="editing=''">×</a-button></template>
            <template v-else><a :href="reportHref(record)" :title="record.name" @click.prevent="openReport(record)">{{ record.name }}</a><a-button v-if="canRename" type="text" size="small" class="rename-button" :aria-label="`重命名${record.name}`" @click="editing=rowKey(record);editName=record.name"><EditOutlined /></a-button></template>
          </div>
          <a-tag v-else-if="column.key==='kind'" :color="record.kind==='GROUP'?'blue':'default'">{{record.kind==='GROUP'?'集成报告':'普通报告'}}</a-tag>
          <a-tag v-else-if="column.key==='resultStatus'" :color="reportResultColor(record.resultStatus)">{{reportResultLabel(record.resultStatus)}}</a-tag>
          <span v-else-if="column.key==='passRate'">{{record.passRate === null ? '—' : `${record.passRate}%`}}</span>
          <span v-else-if="column.key==='triggerMode'">{{record.triggerMode==='cron'?'定时触发':'手动触发'}}</span>
          <span v-else-if="column.key==='createTime'">{{dayjs(record.createTime).format('YYYY-MM-DD HH:mm:ss')}}</span>
          <a-space v-else-if="column.key==='operation'" :size="0"><a-button v-if="canDelete" type="link" size="small" :disabled="busy" @click="deleteOne(record)">删除</a-button><a-button type="link" size="small" :disabled="busy" @click="exportPdf(record)">导出</a-button></a-space>
        </template>
      </a-table>
    </template>
  </section>
</template>
<script setup lang="ts">
import {computed,ref,reactive,watch} from 'vue'
import {useRoute,useRouter} from 'vue-router'
import {message,Modal} from 'ant-design-vue'
import {ReloadOutlined,EditOutlined,CheckOutlined} from '@ant-design/icons-vue'
import dayjs, {type Dayjs} from 'dayjs'
import {useProjectStore} from '@/stores/project'
import {planReportsApi,reportResultOptions,reportResultLabel,reportResultColor,type PlanReportEntry,type ReportKind} from '@/api/planReports'
import {downloadPlanFile} from '@/api/planCollaboration'
import {planGroupApi} from '@/api/planGroup'
const route=useRoute(),router=useRouter(),projectStore=useProjectStore()
const projectId=computed(()=>typeof route.query.projectId==='string'?route.query.projectId:projectStore.currentProject?.id)
const items=ref<PlanReportEntry[]>([]),total=ref(0),page=ref(1),size=ref(20),loading=ref(false),failed=ref(false),expanded=ref(false),search=ref('')
const filters=reactive<{plan_name?:string;kind?:string;result_status?:string;trigger_mode?:string;operator?:string;min_rate?:number;max_rate?:number}>({})
const dates=ref<[Dayjs,Dayjs]>(),sort=ref('created_at'),direction=ref('desc'),applied=ref<Record<string,unknown>>({})
const canRename=ref(false),canDelete=ref(false),selected=ref<string[]>([]),editing=ref(''),editName=ref(''),busy=ref(false),showType=ref('ALL')
const columns=[{title:'报告名称',dataIndex:'name',key:'name',width:200},{title:'报告类型',key:'kind',width:150},
  {title:'所属计划',dataIndex:'planName',width:200,ellipsis:true},{title:'结果',key:'resultStatus',width:150,sorter:true},
  {title:'通过率',key:'passRate',width:200,sorter:true},{title:'触发方式',key:'triggerMode',width:150},
  {title:'操作人',dataIndex:'createUserName',width:300,ellipsis:true},{title:'操作时间',key:'createTime',width:180,sorter:true,defaultSortOrder:'descend'},
  {title:'操作',key:'operation',width:130,fixed:'right' as const}]
const rowKey=(row:PlanReportEntry)=>`${row.kind}:${row.id}`
const reportHref=(row:PlanReportEntry)=>router.resolve({name:'TestPlanReportDetail',params:{runId:row.id},query:{projectId:projectId.value,kind:row.kind}}).href
const openReport=(row:PlanReportEntry)=>router.push(reportHref(row))
let sequence=0
async function load(){const current=++sequence;if(!projectId.value){items.value=[];total.value=0;loading.value=false;return}loading.value=true;failed.value=false
  try{const result=await planReportsApi.list(projectId.value,{page:page.value,size:size.value,sort:sort.value,direction:direction.value,...applied.value});if(current!==sequence)return;items.value=result.items;total.value=result.total;canRename.value=result.canRename;canDelete.value=result.canDelete}
  catch(error){console.error('加载计划报告列表失败',error);if(current===sequence){failed.value=true;items.value=[];total.value=0;canRename.value=false;canDelete.value=false}}
  finally{if(current===sequence)loading.value=false}}
function apply(){if(filters.min_rate!==undefined && filters.max_rate!==undefined && filters.min_rate>filters.max_rate){message.warning('最小通过率不能大于最大通过率');return}
  showType.value=filters.kind||'ALL';applied.value={...filters,search:search.value.trim()||undefined,start_time:dates.value?.[0].format('YYYY-MM-DDTHH:mm:ss'),end_time:dates.value?.[1].format('YYYY-MM-DDTHH:mm:ss')};page.value=1;void load()}
function reset(){Object.keys(filters).forEach(key=>delete filters[key as keyof typeof filters]);search.value='';dates.value=undefined;applied.value={};showType.value='ALL';selected.value=[];editing.value='';page.value=1;void load()}
function changeType(){filters.kind=showType.value==='ALL'?undefined:showType.value;selected.value=[];apply()}
async function rename(row:PlanReportEntry){if(!projectId.value||busy.value)return;if(!editName.value.trim()){message.warning('报告名称不能为空');return}busy.value=true;const target=projectId.value;try{await planReportsApi.rename(target,row,editName.value);editing.value='';message.success('报告名称已保存');await load()}catch(error){console.error('重命名报告失败',error);message.error('重命名失败')}finally{busy.value=false}}
function confirmDelete(reports:{kind:ReportKind;id:string}[],name?:string){const target=projectId.value;if(!target)return;Modal.confirm({title:name?`删除报告“${name}”？`:`删除选中的 ${reports.length} 条报告？`,content:'删除后报告分享链接失效，执行历史和结果快照保留。',okText:'删除',okType:'danger',cancelText:'取消',async onOk(){busy.value=true;try{await planReportsApi.batchRemove(target,reports);if(target===projectId.value){selected.value=[];editing.value='';if(items.value.length===reports.length&&page.value>1)page.value--;await load()}message.success('报告已删除')}catch(error){console.error('删除报告失败',error);message.error('删除失败，请确认执行已结束及操作权限');throw error}finally{busy.value=false}}})}
function deleteOne(row:PlanReportEntry){confirmDelete([{kind:row.kind,id:row.id}],row.name)}
function deleteSelected(){confirmDelete(selected.value.map(key=>{const [kind,id]=key.split(':');return {kind:kind as ReportKind,id}}))}
async function exportPdf(row:PlanReportEntry){busy.value=true;try{if(row.kind==='PLAN')await downloadPlanFile(`runs/${row.id}/pdf`,`${row.name}.pdf`);else{const url=URL.createObjectURL(await planGroupApi.pdf(row.id));const a=document.createElement('a');a.href=url;a.download=`${row.name}.pdf`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)}}catch(error){console.error('导出列表报告失败',error);message.error('导出失败')}finally{busy.value=false}}
function tableChange(p:{current?:number;pageSize?:number},_filters:unknown,s:{columnKey?:string;order?:string}){page.value=p.current||1;size.value=p.pageSize||20;sort.value=({createTime:'created_at',passRate:'pass_rate',resultStatus:'result_status'}[s.columnKey||'']||'created_at');direction.value=s.order==='ascend'?'asc':'desc';void load()}
watch(projectId,()=>{items.value=[];total.value=0;canRename.value=false;canDelete.value=false;page.value=1;reset()},{immediate:true})
</script>
<style scoped>
.report-list{background:white;min-height:100%;padding:16px;min-width:0}.report-toolbar{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-bottom:16px}.report-toolbar :deep(.ant-input-search){width:240px}.report-filters{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:0 16px;background:var(--ms-page-bg);padding:16px;margin-bottom:16px}.report-filters .ant-form-item{margin-bottom:12px}.date-filter{grid-column:span 2}.date-filter :deep(.ant-picker){width:100%}.filter-actions{align-self:end;margin-bottom:12px}.load-error{margin-bottom:12px}
.report-name{display:flex;align-items:center;min-width:0;gap:4px}.report-name>a{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;flex:1}.report-name .rename-button{opacity:0;flex-shrink:0}.report-name:hover .rename-button,.rename-button:focus-visible{opacity:1}.batch-toolbar{margin-bottom:12px}
@media(max-width:768px){.report-list{padding:12px}.report-toolbar :deep(.ant-input-search){width:230px}.report-filters{grid-template-columns:minmax(0,1fr)}.date-filter{grid-column:auto}}
</style>
