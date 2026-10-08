<template>
 <div class="native-processors">
  <p>SQL 仅查询本次声明的合成表。脚本钩子引用当前项目的 Python、Shell 或命令作业，运行时冻结版本并使用父执行槽与日志。</p>
  <section v-for="(row,index) in rows" :key="row.id" class="processor">
   <a-space wrap><a-switch :checked="row.enable" :disabled="disabled" aria-label="启用处理器" @change="change(index,'enable',$event)" /><a-input :value="row.name" :disabled="disabled" :maxlength="255" aria-label="处理器名称" @update:value="change(index,'name',$event)" /><a-button :disabled="disabled||index===0" @click="move(index,-1)">上移</a-button><a-button :disabled="disabled||index===rows.length-1" @click="move(index,1)">下移</a-button><a-button danger :disabled="disabled" @click="remove(index)">移除</a-button></a-space>
   <template v-if="row.type === 'sql'">
   <a-form-item label="只读 SQL"><a-textarea :value="row.query" :rows="4" :maxlength="8192" :disabled="disabled" aria-label="只读合成SQL" @update:value="change(index,'query',$event)" /></a-form-item>
   <a-form-item label="绑定参数（JSON对象）"><a-textarea :value="row.parametersText" :rows="2" :disabled="disabled" aria-label="SQL绑定参数" @update:value="change(index,'parametersText',$event)" /></a-form-item>
   <a-form-item label="合成表（JSON数组）"><a-textarea :value="row.tablesText" :rows="5" :disabled="disabled" aria-label="SQL合成表" @update:value="change(index,'tablesText',$event)" /></a-form-item>
   <a-form-item label="结果绑定（JSON数组）"><a-textarea :value="row.bindingsText" :rows="3" :disabled="disabled" aria-label="SQL结果变量绑定" @update:value="change(index,'bindingsText',$event)" /></a-form-item>
   <a-space wrap><a-form-item label="最多结果行"><a-input-number :value="row.maxRows" :min="1" :max="1000" :precision="0" :disabled="disabled" @update:value="change(index,'maxRows',$event)" /></a-form-item><a-form-item label="执行上限（毫秒）"><a-input-number :value="row.timeoutMs" :min="50" :max="2000" :precision="0" :disabled="disabled" @update:value="change(index,'timeoutMs',$event)" /></a-form-item></a-space>
   </template>
   <template v-else><a-form-item label="脚本作业引用"><a-input :value="row.jobId" :disabled="disabled" :maxlength="36" aria-label="脚本作业ID" @update:value="change(index,'jobId',$event)" /></a-form-item><a-form-item label="要求作业版本（留空采用冻结时版本）"><a-input-number :value="row.expectedRevision" :disabled="disabled" :min="1" :precision="0" aria-label="脚本引用版本" @update:value="change(index,'expectedRevision',$event)" /></a-form-item></template>
  </section>
  <a-button :disabled="disabled||rows.length>=10" @click="add">添加只读 SQL</a-button>
  <a-button :disabled="disabled||rows.length>=10" @click="addScript">添加脚本引用</a-button>
  <a-space v-if="projectId" wrap><a-button :disabled="disabled||loading" @click="loadJobs(1)">浏览项目脚本</a-button><a-select :value="selected" :options="jobs.map(j=>({value:j.id,label:j.name+' · v'+j.revision}))" :disabled="disabled||loading" aria-label="项目脚本作业" style="min-width:220px" @update:value="selected=$event" /><a-button :disabled="disabled||!selected||rows.length>=10" @click="addSelected">引用所选版本</a-button><a-button :disabled="disabled||loading||page<=1" @click="loadJobs(page-1)">上一页</a-button><a-button :disabled="disabled||loading||page*20>=total" @click="loadJobs(page+1)">下一页</a-button><span>{{page}} 页 · {{total}} 项</span></a-space>
  <a-alert v-if="loadError" type="warning" :message="loadError" />
  <a-alert v-if="error" type="error" :message="error" show-icon />
 </div>
</template>
<script setup lang="ts">
import { ref,watch,onBeforeUnmount } from 'vue';
import { readNativeProcessors,type NativeSqlProcessor,type NativeScriptHook,type NativeProcessor } from './nativeProcessors';
import { scriptJobsApi,type ScriptJob } from '@/api/scriptJobs';
import { useUserStore } from '@/stores/user';
import { createRequestId } from '@/utils/requestId';
const props=defineProps<{modelValue:string;disabled?:boolean;projectId?:string}>();
const emit=defineEmits<{'update:modelValue':[value:string]}>();
type Draft=(NativeSqlProcessor & {parametersText:string;tablesText:string;bindingsText:string})|NativeScriptHook;
const rows=ref<Draft[]>([]),error=ref('');let output='';
const adopt=(row:NativeProcessor):Draft=>row.type==='script'?{...row}:{...row,parametersText:JSON.stringify(row.parameters,null,2),tablesText:JSON.stringify(row.tables,null,2),bindingsText:JSON.stringify(row.bindings,null,2)};
watch(()=>props.modelValue,raw=>{if(raw===output)return;output=raw;try{rows.value=readNativeProcessors(raw).map(adopt);error.value='';}catch{rows.value=[];error.value='处理器配置无效，请在高级配置中修正';}}, {immediate:true,flush:'sync'});
function parsed(raw:string){try{return JSON.parse(raw);}catch{return raw;}}
function publish(){output=JSON.stringify(rows.value.map(item=>{if(item.type==='script')return item;const {parametersText,tablesText,bindingsText,...row}=item;return {...row,parameters:parsed(parametersText),tables:parsed(tablesText),bindings:parsed(bindingsText)};}));try{readNativeProcessors(output);error.value='';}catch{error.value='请检查处理器与脚本引用草稿';}emit('update:modelValue',output);}
function change(index:number,field:string,value:unknown){if(props.disabled||!rows.value[index])return;(rows.value[index] as any)[field]=value;publish();}
function add(){if(props.disabled||rows.value.length>=10)return;rows.value.push(adopt({type:'sql',id:createRequestId(),name:'只读合成SQL',enable:true,query:'SELECT 1 AS value',parameters:{},tables:[],bindings:[],maxRows:100,timeoutMs:1000}));publish();}
function addScript(){if(props.disabled||rows.value.length>=10)return;rows.value.push({type:'script',id:createRequestId(),name:'脚本钩子',enable:true,jobId:'',expectedRevision:null});publish();}
function remove(index:number){if(props.disabled)return;rows.value.splice(index,1);publish();}
function move(index:number,by:number){if(props.disabled||index+by<0||index+by>=rows.value.length)return;const [row]=rows.value.splice(index,1);rows.value.splice(index+by,0,row);publish();}
const user=useUserStore(),jobs=ref<ScriptJob[]>([]),selected=ref(''),page=ref(1),total=ref(0),loading=ref(false),loadError=ref('');
let epoch=0,alive=true,request:AbortController|undefined;
const context=()=>[props.projectId,user.user?.id].join(':');
watch(context,()=>{epoch++;request?.abort();jobs.value=[];selected.value='';page.value=1;total.value=0;loading.value=false;loadError.value='';},{flush:'sync'});
async function loadJobs(next:number){if(props.disabled||!props.projectId||!user.user?.id||next<1)return;request?.abort();request=new AbortController();const token=++epoch,scope=context();loading.value=true;loadError.value='';try{const result=await scriptJobsApi.list(props.projectId,next,request.signal);if(!alive||token!==epoch||scope!==context())return;jobs.value=result.items.slice(0,20);selected.value='';page.value=result.page;total.value=result.total;}catch{if(alive&&token===epoch&&scope===context())loadError.value='无法读取当前项目脚本，请核对权限后重试';}finally{if(alive&&token===epoch)loading.value=false;}}
function addSelected(){if(props.disabled||rows.value.length>=10)return;const job=jobs.value.find(j=>j.id===selected.value&&j.projectId===props.projectId);if(!job)return;rows.value.push({type:'script',id:createRequestId(),name:job.name,enable:true,jobId:job.id,expectedRevision:job.revision});publish();}
onBeforeUnmount(()=>{alive=false;epoch++;request?.abort();});
</script>
<style scoped>.processor{border:1px solid #e5e6eb;border-radius:4px;padding:16px;margin-bottom:12px;}</style>
