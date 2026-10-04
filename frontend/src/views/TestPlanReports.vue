<template>
  <section class="report-list">
    <a-alert v-if="!projectId" message="请选择项目" type="info" />
    <template v-else>
      <div class="report-toolbar">
        <a-space wrap><span>全部报告 <strong>{{ total }}</strong></span><a-button @click="expanded = !expanded" :aria-expanded="expanded">高级筛选</a-button></a-space>
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
      <a-table :data-source="items" :columns="columns" :loading="loading" :row-key="rowKey" :scroll="{x:1400}" size="small"
        :pagination="{current:page,pageSize:size,total,showSizeChanger:true,pageSizeOptions:['10','20','50','100'],showTotal:(n:number)=>`共 ${n} 条`}"
        @change="tableChange">
        <template #bodyCell="{column,record}">
          <a v-if="column.key==='name'" :href="reportHref(record)" @click.prevent="openReport(record)">{{ record.name }}</a>
          <a-tag v-else-if="column.key==='kind'" :color="record.kind==='GROUP'?'blue':'default'">{{record.kind==='GROUP'?'集成报告':'普通报告'}}</a-tag>
          <a-tag v-else-if="column.key==='resultStatus'" :color="reportResultColor(record.resultStatus)">{{reportResultLabel(record.resultStatus)}}</a-tag>
          <span v-else-if="column.key==='passRate'">{{record.passRate === null ? '—' : `${record.passRate}%`}}</span>
          <span v-else-if="column.key==='triggerMode'">{{record.triggerMode==='cron'?'定时触发':'手动触发'}}</span>
          <span v-else-if="column.key==='createTime'">{{dayjs(record.createTime).format('YYYY-MM-DD HH:mm:ss')}}</span>
          <a-button v-else-if="column.key==='operation'" type="link" size="small" @click="openReport(record)">查看</a-button>
        </template>
      </a-table>
    </template>
  </section>
</template>
<script setup lang="ts">
import {computed,ref,reactive,watch} from 'vue'
import {useRoute,useRouter} from 'vue-router'
import {message} from 'ant-design-vue'
import {ReloadOutlined} from '@ant-design/icons-vue'
import dayjs, {type Dayjs} from 'dayjs'
import {useProjectStore} from '@/stores/project'
import {planReportsApi,reportResultOptions,reportResultLabel,reportResultColor,type PlanReportEntry} from '@/api/planReports'
const route=useRoute(),router=useRouter(),projectStore=useProjectStore()
const projectId=computed(()=>typeof route.query.projectId==='string'?route.query.projectId:projectStore.currentProject?.id)
const items=ref<PlanReportEntry[]>([]),total=ref(0),page=ref(1),size=ref(20),loading=ref(false),failed=ref(false),expanded=ref(false),search=ref('')
const filters=reactive<{plan_name?:string;kind?:string;result_status?:string;trigger_mode?:string;operator?:string;min_rate?:number;max_rate?:number}>({})
const dates=ref<[Dayjs,Dayjs]>(),sort=ref('created_at'),direction=ref('desc'),applied=ref<Record<string,unknown>>({})
const columns=[{title:'报告名称',dataIndex:'name',key:'name',width:220,ellipsis:true},{title:'报告类型',key:'kind',width:130},
  {title:'所属计划',dataIndex:'planName',width:220,ellipsis:true},{title:'结果',key:'resultStatus',width:130,sorter:true},
  {title:'通过率',key:'passRate',width:110,sorter:true},{title:'触发方式',key:'triggerMode',width:130},
  {title:'操作人',dataIndex:'createUserName',width:160,ellipsis:true},{title:'操作时间',key:'createTime',width:190,sorter:true,defaultSortOrder:'descend'},
  {title:'操作',key:'operation',width:90,fixed:'right' as const}]
const rowKey=(row:PlanReportEntry)=>`${row.kind}:${row.id}`
const reportHref=(row:PlanReportEntry)=>router.resolve({name:'TestPlanReportDetail',params:{runId:row.id},query:{projectId:projectId.value,kind:row.kind}}).href
const openReport=(row:PlanReportEntry)=>router.push(reportHref(row))
let sequence=0
async function load(){const current=++sequence;if(!projectId.value){items.value=[];total.value=0;loading.value=false;return}loading.value=true;failed.value=false
  try{const result=await planReportsApi.list(projectId.value,{page:page.value,size:size.value,sort:sort.value,direction:direction.value,...applied.value});if(current!==sequence)return;items.value=result.items;total.value=result.total}
  catch(error){console.error('加载计划报告列表失败',error);if(current===sequence){failed.value=true;items.value=[];total.value=0}}
  finally{if(current===sequence)loading.value=false}}
function apply(){if(filters.min_rate!==undefined && filters.max_rate!==undefined && filters.min_rate>filters.max_rate){message.warning('最小通过率不能大于最大通过率');return}
  applied.value={...filters,search:search.value.trim()||undefined,start_time:dates.value?.[0].format('YYYY-MM-DDTHH:mm:ss'),end_time:dates.value?.[1].format('YYYY-MM-DDTHH:mm:ss')};page.value=1;void load()}
function reset(){Object.keys(filters).forEach(key=>delete filters[key as keyof typeof filters]);search.value='';dates.value=undefined;applied.value={};page.value=1;void load()}
function tableChange(p:{current?:number;pageSize?:number},_filters:unknown,s:{columnKey?:string;order?:string}){page.value=p.current||1;size.value=p.pageSize||20;sort.value=({createTime:'created_at',passRate:'pass_rate',resultStatus:'result_status'}[s.columnKey||'']||'created_at');direction.value=s.order==='ascend'?'asc':'desc';void load()}
watch(projectId,()=>{items.value=[];total.value=0;page.value=1;reset()},{immediate:true})
</script>
<style scoped>
.report-list{background:white;min-height:100%;padding:16px;min-width:0}.report-toolbar{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-bottom:16px}.report-toolbar :deep(.ant-input-search){width:240px}.report-filters{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:0 16px;background:var(--ms-page-bg);padding:16px;margin-bottom:16px}.report-filters .ant-form-item{margin-bottom:12px}.date-filter{grid-column:span 2}.date-filter :deep(.ant-picker){width:100%}.filter-actions{align-self:end;margin-bottom:12px}.load-error{margin-bottom:12px}
@media(max-width:768px){.report-list{padding:12px}.report-toolbar :deep(.ant-input-search){width:230px}.report-filters{grid-template-columns:minmax(0,1fr)}.date-filter{grid-column:auto}}
</style>
