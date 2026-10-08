<template>
<a-modal :open="open" title="项目文件库" width="min(950px,100vw)" :mask-closable="!busy&&!folderOpen" :closable="!busy&&!folderOpen" :keyboard="!busy&&!folderOpen" :confirm-loading="busy" :ok-button-props="{disabled:!selected.length||busy||loading||folderOpen}" @ok="accept" @cancel="cancel">
  <a-alert message="主动上传到项目库的文件对项目成员可见。图片草稿在提交引用前仅上传人可见；归档保留历史字节和引用。" type="info" />
  <a-space wrap style="margin:12px 0"><a-select :value="folderId||''" style="width:230px" :disabled="busy" :options="folderOptions" @change="changeFolder" /><a-input v-model:value="search" placeholder="文件名" :disabled="busy" @press-enter="searchFiles" /><a-button :disabled="busy" @click="searchFiles">查询</a-button><a-upload :before-upload="upload" :show-upload-list="false" :disabled="busy"><a-button :loading="busy">上传到项目库</a-button></a-upload><a-button v-if="canManage" :disabled="busy" @click="newFolder">新建目录</a-button><a-button v-if="canManage&&folderId" :disabled="busy" @click="editFolder">编辑目录</a-button><a-checkbox v-if="canManage" v-model:checked="archived" :disabled="busy" @change="searchFiles">已归档</a-checkbox></a-space>
  <a-alert v-if="error" type="error" :message="error" />
  <a-table :loading="loading" :data-source="files" :columns="columns" row-key="id" :row-selection="{selectedRowKeys:selected,onChange:select,preserveSelectedRowKeys:true,getCheckboxProps:(r:LibraryFile)=>({disabled:r.archived||busy})}" :pagination="{current:page,pageSize:20,total,showSizeChanger:false}" @change="paginate" :scroll="{x:560}">
    <template #bodyCell="{column,record}"><template v-if="column.key==='name'">{{record.fileName}} <a-tag v-if="!record.published">私人草稿</a-tag></template><template v-else-if="column.key==='size'">{{(record.fileSize/1024).toFixed(1)}} KB</template><template v-else-if="column.key==='actions'"><a-button type="link" :disabled="busy" @click="download(record)">下载</a-button><a-button v-if="canManage" type="link" :disabled="busy" @click="archive(record)">{{record.archived?'恢复':'归档'}}</a-button></template></template>
  </a-table>
  <p>已选择 {{selected.length}} / {{limit}} 个文件</p>
  <a-modal :open="folderOpen" title="文件目录" :confirm-loading="busy" :closable="!busy" :mask-closable="!busy" :keyboard="!busy" :cancel-button-props="{disabled:busy}" @ok="saveFolder" @cancel="folderOpen=false"><a-input v-model:value="folderName" :maxlength="255" placeholder="目录名" :disabled="busy" /><a-select v-model:value="parentId" style="width:100%;margin-top:12px" :options="folderOptions" :disabled="busy" /></a-modal>
</a-modal>
</template>
<script setup lang="ts">
import {ref,computed,watch,onBeforeUnmount} from 'vue'
import {fileLibraryApi as api,type LibraryFile,type LibraryFolder} from '@/api/fileLibrary'
import {saveCaseBlob} from '@/api/caseFeatures'
import {useUserStore} from '@/stores/user'
const user=useUserStore()
import {message} from 'ant-design-vue'
import type {Key} from 'ant-design-vue/es/_util/type'
const props=defineProps<{projectId:string}>()
const open=ref(false),busy=ref(false),loading=ref(false),error=ref(''),folders=ref<LibraryFolder[]>([]),files=ref<LibraryFile[]>([]),folderId=ref(''),search=ref(''),page=ref(1),total=ref(0),archived=ref(false),canManage=ref(false),selected=ref<string[]>([]),limit=ref(50),imagesOnly=ref(false)
const chosen=new Map<string,LibraryFile>();let finish:((rows:LibraryFile[])=>void)|undefined,sequence=0
const folderOpen=ref(false),folderName=ref(''),parentId=ref(''),editing=ref('')
const columns=[{title:'文件名',key:'name'},{title:'大小',key:'size',width:110},{title:'操作',key:'actions',width:170}]
const folderOptions=computed(()=>[{label:'根目录',value:''},...folders.value.map(row=>{let text=row.name,parent=row.parentId;const seen=new Set([row.id]);while(parent){const item=folders.value.find(f=>f.id===parent);if(!item||seen.has(parent))break;seen.add(parent);text=item.name+' / '+text;parent=item.parentId}return{label:text,value:row.id}})])
async function load(){const current=++sequence,p=props.projectId;loading.value=true;error.value='';try{const [tree,data]=await Promise.all([api.folders(p),api.files(p,{folderId:folderId.value||undefined,search:search.value,page:page.value,archived:archived.value,imagesOnly:imagesOnly.value})]);if(current!==sequence||p!==props.projectId||!open.value)return;folders.value=tree;files.value=data.items;total.value=data.total;canManage.value=data.canManage;for(const r of data.items)if(selected.value.includes(r.id))chosen.set(r.id,r)}catch(failure){if(current===sequence)error.value='读取文件库失败，请重试'}finally{if(current===sequence)loading.value=false}}
function pick(options:{imagesOnly?:boolean;limit?:number}={}){if(busy.value||open.value)return Promise.resolve([] as LibraryFile[]);open.value=true;imagesOnly.value=!!options.imagesOnly;limit.value=options.limit||50;folderId.value='';search.value='';archived.value=false;selected.value=[];chosen.clear();page.value=1;void load();return new Promise<LibraryFile[]>(resolve=>{finish=resolve})}
function cancel(){if(busy.value)return;open.value=false;folderOpen.value=false;++sequence;finish?.([]);finish=undefined}
function accept(){if(busy.value||loading.value||folderOpen.value)return;const rows=selected.value.map(id=>chosen.get(id)).filter((r):r is LibraryFile=>!!r&&!r.archived);if(rows.length!==selected.value.length){message.warning('文件选择已变化，请重新选择');return}open.value=false;++sequence;finish?.(rows);finish=undefined}
function select(keys:Key[],rows:LibraryFile[]){if(keys.length>limit.value){message.warning(`最多选择${limit.value}个文件`);return}selected.value=keys.map(String);for(const row of rows)chosen.set(row.id,row)}
function changeFolder(id:string){folderId.value=id;page.value=1;void load()}
function searchFiles(){page.value=1;void load()}
function paginate(p:{current?:number}){page.value=p.current||1;void load()}
async function mutate(task:(p:string)=>Promise<unknown>){if(busy.value)return;busy.value=true;const p=props.projectId,current=sequence;try{await task(p);if(p===props.projectId&&current===sequence&&open.value)await load();return true}catch(failure){if(p===props.projectId)message.error('文件库操作失败，当前选择保留');return false}finally{busy.value=false}}
async function upload(file:File){await mutate(p=>api.upload(p,file,{folderId:folderId.value||undefined,image:imagesOnly.value,published:true}));return false}
async function archive(row:LibraryFile){const success=await mutate(p=>api.archive(p,row.id,!row.archived));if(success&&row.archived===false){selected.value=selected.value.filter(id=>id!==row.id);chosen.delete(row.id)}}
async function download(row:LibraryFile){const p=props.projectId;try{saveCaseBlob(await api.download(p,row.id),row.fileName)}catch(failure){message.error('下载失败')}}
function newFolder(){editing.value='';folderName.value='';parentId.value=folderId.value;folderOpen.value=true}
function editFolder(){const row=folders.value.find(f=>f.id===folderId.value);if(row){editing.value=row.id;folderName.value=row.name;parentId.value=row.parentId||'';folderOpen.value=true}}
async function saveFolder(){if(await mutate(p=>api.saveFolder(p,{name:folderName.value,parentId:parentId.value||undefined},editing.value||undefined)))folderOpen.value=false}
watch(()=>[props.projectId,user.user?.id],()=>{open.value=false;folderOpen.value=false;++sequence;finish?.([]);finish=undefined;selected.value=[];chosen.clear()})
onBeforeUnmount(()=>{++sequence;finish?.([]);finish=undefined})
defineExpose({pick,isBusy:()=>busy.value})
</script>
