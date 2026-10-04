<template>
  <a-alert type="info" show-icon message="测试点树存在用例或测试套时，执行范围以此树为准。用例可重复关联；父测试点的环境、资源池和串并行配置可由子节点覆盖。" />
  <a-space wrap style="margin:12px 0">
    <a-button type="primary" @click="edit()">新建测试点</a-button><a-button @click="addCase">关联用例</a-button><a-button @click="addSuite">关联场景测试套</a-button>
    <a-select v-model:value="assignTo" allow-clear placeholder="批量分配执行人" style="width:170px" :options="executors.map(e=>({value:e.id,label:e.name}))" /><a-button :disabled="!selected.length" @click="assign">分配已选节点</a-button>
    <a-button @click="load">刷新</a-button>
  </a-space>
  <a-table :data-source="hierarchy" :columns="columns" row-key="id" size="small" :pagination="false" :row-selection="{selectedRowKeys:selected,onChange:(keys:any[])=>selected=keys.map(String),getCheckboxProps:(n:PlanNode)=>({disabled:n.nodeType==='point'})}" :scroll="{x:800}">
    <template #bodyCell="{column,record}">
      <template v-if="column.key==='name'"><strong>{{record.name}}</strong><a-tag style="margin-left:6px">{{categoryLabel[record.category]}}</a-tag></template>
      <template v-else-if="column.key==='type'">{{record.nodeType==='point'?'测试点':record.nodeType==='suite'?'场景套':'用例关联'}}</template>
      <template v-else-if="column.key==='config'">{{configText(record.effectiveConfig)}}</template>
      <template v-else-if="column.key==='owner'">{{executors.find(e=>e.id===record.assignedTo)?.name || '未分配'}}</template>
      <template v-else-if="column.key==='actions'"><a-space><a-button size="small" type="link" @click="edit(record)">编辑</a-button><a-popconfirm title="删除此节点及子节点？已有批次快照保留。" @confirm="remove(record.id)"><a-button size="small" type="link" danger>移除</a-button></a-popconfirm></a-space></template>
    </template>
  </a-table>
  <a-modal v-model:open="open" :title="editingId?'编辑测试点/关联':'新增测试点/关联'" width="720px" @ok="save" :confirm-loading="saving">
    <a-form layout="vertical">
      <a-form-item label="名称" required><a-input v-model:value="form.name" :maxlength="255" /></a-form-item>
      <a-row :gutter="12"><a-col :span="12"><a-form-item label="节点类型"><a-select v-model:value="form.nodeType" :disabled="!!editingId" :options="[{value:'point',label:'测试点'},{value:'case',label:'用例关联'},{value:'suite',label:'场景测试套'}]" /></a-form-item></a-col><a-col :span="12"><a-form-item label="分类"><a-select v-model:value="form.category" :options="categories" /></a-form-item></a-col></a-row>
      <a-form-item label="父测试点"><a-tree-select v-model:value="form.parentId" :tree-data="pointTree" allow-clear style="width:100%" /></a-form-item>
      <a-form-item v-if="form.nodeType==='case'" label="关联用例（重复选择将创建独立关联）" required><a-select v-model:value="form.caseId" show-search :filter-option="false" @search="searchCases" @change="chooseCase" :options="cases.map(c=>({value:c.id,label:c.caseCode+' '+c.name}))" /></a-form-item>
      <a-form-item v-if="form.nodeType!=='point'" label="测试套（自动化必选；手工留空）"><a-select v-model:value="form.suiteId" allow-clear :options="suites.map(s=>({value:s.id,label:s.name}))" /></a-form-item>
      <a-form-item v-if="form.nodeType!=='point'" label="自动化结果更新功能用例"><a-select v-model:value="form.linkedFunctionalId" allow-clear :options="nodes.filter(n=>n.category==='functional' && n.nodeType==='case' && !n.case?.isAutomated && n.id!==editingId).map(n=>({value:n.id,label:n.name}))" /></a-form-item>
      <a-form-item label="执行人"><a-select v-model:value="form.assignedTo" allow-clear :options="executors.map(e=>({value:e.id,label:e.name}))" /></a-form-item>
      <a-row :gutter="12"><a-col :span="12"><a-form-item label="子节点执行方式"><a-select v-model:value="form.config.executionMode" allow-clear placeholder="继承父配置" :options="[{value:'serial',label:'串行'},{value:'parallel',label:'并行'}]" /></a-form-item></a-col><a-col :span="12"><a-form-item label="同级顺序"><a-input-number v-model:value="form.position" :min="0" /></a-form-item></a-col></a-row>
      <a-form-item label="执行环境"><a-select v-model:value="form.config.environmentId" allow-clear placeholder="继承父环境或采用测试套配置" :options="environments.map(e=>({value:e.id,label:e.name}))" @change="form.config.resourcePool=[]" /></a-form-item>
      <a-form-item label="资源池（ATS Agent环境，按可用槽选择）"><a-select v-model:value="form.config.resourcePool" mode="multiple" placeholder="留空继承" :options="environments.map(e=>({value:e.id,label:e.name}))" @change="form.config.environmentId=null" /></a-form-item>
    </a-form>
  </a-modal>
</template>
<script setup lang="ts">
import { ref,reactive,computed,onMounted,watch } from 'vue'
import {message} from 'ant-design-vue'
import type {TestCase,Environment} from '@/types'
import {planTreeApi,type PlanNode,type NodeConfig} from '@/api/planTree'
import {testCaseApi} from '@/api/testCase'
import {testSuiteApi,type TestSuite} from '@/api/testSuite'
import {environmentApi} from '@/api/environment'
const props=defineProps<{planId:string;projectId:string}>()
const nodes=ref<PlanNode[]>([]),cases=ref<TestCase[]>([]),suites=ref<TestSuite[]>([]),environments=ref<Environment[]>([]),executors=ref<{id:string;name:string}[]>([])
const selected=ref<string[]>([]),assignTo=ref<string>(),open=ref(false),editingId=ref(''),saving=ref(false)
const categoryLabel:Record<string,string>={functional:'功能',api:'API',scenario:'场景'}
const categories=Object.entries(categoryLabel).map(([value,label])=>({value,label}))
const columns=[{title:'测试点 / 用例',key:'name',width:220},{title:'类型',key:'type',width:90},{title:'有效配置',key:'config',width:220},{title:'执行人',key:'owner',width:100},{title:'操作',key:'actions',width:140}]
const blank=()=>({name:'',nodeType:'point' as PlanNode['nodeType'],category:'functional' as PlanNode['category'],parentId:null as string|null,caseId:null as string|null,suiteId:null as string|null,assignedTo:null as string|null,linkedFunctionalId:null as string|null,position:0,config:{} as NodeConfig})
const form=reactive(blank())
function build(parent:string|null=null):any[]{return nodes.value.filter(n=>(n.parentId||null)===parent).map(n=>({...n,children:build(n.id).length?build(n.id):undefined}))}
const hierarchy=computed(()=>build())
const pointTree=computed(()=>{const convert=(parent:string|null=null):any[]=>nodes.value.filter(n=>(n.parentId||null)===parent && n.nodeType==='point' && n.id!==editingId.value).map(n=>({value:n.id,key:n.id,title:n.name,children:convert(n.id)}));return convert()})
function configText(config:NodeConfig){return [config.executionMode==='parallel'?'并行':config.executionMode==='serial'?'串行':'继承计划策略',config.environmentId?environments.value.find(e=>e.id===config.environmentId)?.name:config.resourcePool?.length?`${config.resourcePool.length} 个节点资源池`:'测试套环境'].join(' · ')}
async function searchCases(search=''){try{const result=await testCaseApi.getTestCases(props.projectId,{page:1,size:100,search});cases.value=result.items}catch(error){console.error('搜索计划关联用例失败',error)}}
async function load(){try{const [n,s,e,u]=await Promise.all([planTreeApi.list(props.planId),testSuiteApi.getTestSuites(props.planId,{limit:1000}),environmentApi.getEnvironments({size:100}),planTreeApi.executors(props.planId)]);nodes.value=n;suites.value=s.items;environments.value=e.items;executors.value=u;await searchCases()}catch(error){console.error('加载计划测试点失败',error);message.error('加载测试点失败')}}
function edit(node?:PlanNode){editingId.value=node?.id||'';Object.assign(form,blank(),node?JSON.parse(JSON.stringify(node)):{});open.value=true}
function addCase(){edit();form.nodeType='case'}
function addSuite(){edit();form.nodeType='suite';form.category='scenario'}
function chooseCase(id:string){const selected=cases.value.find(c=>c.id===id);if(selected){form.name=selected.name;form.category=selected.isAutomated?'api':'functional'}}
async function save(){saving.value=true;try{const payload={...form,config:Object.fromEntries(Object.entries(form.config).filter(([_,v])=>v!==undefined && v!==null && (!Array.isArray(v)||v.length)))};if(editingId.value)await planTreeApi.update(editingId.value,payload);else await planTreeApi.create(props.planId,payload);open.value=false;await load();message.success('测试点已保存')}catch(error){console.error('保存计划测试点失败',error);message.error('保存失败，请检查节点、用例及配置')}finally{saving.value=false}}
async function remove(id:string){try{await planTreeApi.remove(id);await load()}catch(error){console.error('删除测试点失败',error);message.error('删除失败')}}
async function assign(){try{await planTreeApi.assign(props.planId,selected.value,assignTo.value);await load();message.success('执行人已分配')}catch(error){console.error('分配执行人失败',error);message.error('分配失败')}}
onMounted(load);watch(()=>props.planId,load)
</script>
