<template>
<a-space direction="vertical" style="width:100%">
  <a-space v-if="!hideFollow"><a-button :loading="busy" @click="toggleFollow">{{followed?'取消关注':'关注用例'}}</a-button><span>{{followCount}} 人关注</span></a-space>
  <CaseRichText v-model="content" :project-id="projectId" :disabled="busy||uploading" label="讨论意见" :upload-image="uploadImage" :select-image="selectImage" @uploading="(value:boolean)=>uploading=value" />
  <a-space><a-button :disabled="busy||uploading" @click="selectFiles">文件库附件</a-button><a-button type="primary" :loading="busy" :disabled="!content.trim()||uploading||content.length>10000" @click="post">发表评论</a-button></a-space>
  <p v-for="file in files" :key="file.id">{{file.fileName}} <a-button type="link" :disabled="busy||uploading" @click="files=files.filter(f=>f.id!==file.id)">取消选择</a-button></p>
  <a-alert v-if="error" type="error" :message="error" /><a-button v-if="error" @click="load">重试读取</a-button>
  <a-list :data-source="comments"><template #renderItem="{item}"><a-list-item><a-list-item-meta :title="`${item.authorId===user.user?.id?'我':item.authorId} · ${item.createdAt}`"><template #description><CaseRichText :model-value="item.content" readonly /><p v-for="file in item.files" :key="file.id"><a @click="download(file)">{{file.fileName}}</a></p></template></a-list-item-meta><template #actions><a-popconfirm v-if="item.canDelete" title="删除这条评论？" @confirm="remove(item.id)"><a-button type="link" danger :disabled="busy||uploading">删除</a-button></a-popconfirm></template></a-list-item></template></a-list>
  <FileLibraryPicker ref="picker" :project-id="projectId" />
</a-space>
</template>
<script setup lang="ts">
import {ref,watch,onMounted,onBeforeUnmount} from 'vue'
import {message,Modal} from 'ant-design-vue'
import {caseFeaturesApi as api,saveCaseBlob,type CaseComment} from '@/api/caseFeatures'
import {fileLibraryApi,type LibraryFile} from '@/api/fileLibrary'
import {useUserStore} from '@/stores/user'
import CaseRichText from './CaseRichText.vue'
import FileLibraryPicker from './FileLibraryPicker.vue'
const props=defineProps<{projectId:string;caseId:string;hideFollow?:boolean}>(),emit=defineEmits<{changed:[]}>(),user=useUserStore()
const busy=ref(false),uploading=ref(false),content=ref(''),files=ref<LibraryFile[]>([]),comments=ref<CaseComment[]>([]),followed=ref(false),followCount=ref(0),error=ref(''),picker=ref<InstanceType<typeof FileLibraryPicker>>()
let sequence=0;const scope=()=>`${props.projectId}:${props.caseId}`
async function load(){const current=++sequence,p=props.projectId,c=props.caseId;error.value='';try{const [rows,state]=await Promise.all([api.comments(p,c),api.followState(p,c)]);if(current===sequence&&scope()===`${p}:${c}`){comments.value=rows;followed.value=state.followed;followCount.value=state.count}}catch(failure){if(current===sequence)error.value='加载讨论失败，请重试'}}
async function run(task:(p:string,c:string)=>Promise<unknown>){if(busy.value||uploading.value)return;busy.value=true;const expected=scope(),p=props.projectId,c=props.caseId;try{await task(p,c);if(scope()===expected){await load();emit('changed')}}catch(failure){if(scope()===expected)message.error('保存失败，讨论草稿保留')}finally{busy.value=false}}
async function toggleFollow(){const value=!followed.value;await run((p,c)=>api.follow(p,c,value))}
async function post(){if(!content.value.trim()||content.value.length>10000)return;const expected=scope(),submitted=content.value.trim(),ids=files.value.map(f=>f.id);await run(async(p,c)=>{await api.comment(p,c,submitted,ids);if(scope()===expected){content.value='';files.value=[]}})}
async function remove(id:string){await run((p,c)=>api.deleteComment(p,c,id))}
async function uploadImage(file:File){const row=await fileLibraryApi.upload(props.projectId,file,{image:true});return{src:row.src!,fileName:row.fileName}}
async function selectImage(){const rows=await picker.value?.pick({imagesOnly:true,limit:1});const row=rows?.[0];return row?.src?{src:row.src,fileName:row.fileName}:undefined}
async function selectFiles(){if(busy.value||uploading.value)return;uploading.value=true;try{const rows=await picker.value?.pick();if(rows?.length)files.value=rows}finally{uploading.value=false}}
async function download(file:LibraryFile){const p=props.projectId;try{saveCaseBlob(await fileLibraryApi.download(p,file.id),file.fileName)}catch(failure){message.error('下载失败')}}
async function beforeClose(){if(busy.value||uploading.value){message.warning('请等待讨论提交或素材操作完成');return false}if(!content.value&&!files.value.length)return true;return new Promise<boolean>(resolve=>Modal.confirm({title:'放弃未发布的讨论和附件？',onOk(){content.value='';files.value=[];resolve(true)},onCancel(){resolve(false)}}))}
function beforeUnload(event:BeforeUnloadEvent){if(content.value||files.value.length||busy.value||uploading.value){event.preventDefault();event.returnValue=''}}
watch(()=>[props.projectId,props.caseId,user.user?.id],()=>{++sequence;content.value='';files.value=[];comments.value=[];followed.value=false;followCount.value=0;void load()},{immediate:true})
onMounted(()=>window.addEventListener('beforeunload',beforeUnload));onBeforeUnmount(()=>{++sequence;window.removeEventListener('beforeunload',beforeUnload)})
defineExpose({beforeClose})
</script>
