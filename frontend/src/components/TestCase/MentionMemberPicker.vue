<template>
  <a-modal :open="open" title="提及项目成员" :footer="null" @cancel="cancel">
    <a-space><a-input v-model:value="search" :maxlength="100" placeholder="姓名或用户名" @press-enter="searchMembers" /><a-button @click="searchMembers">查询</a-button></a-space>
    <a-alert v-if="error" type="error" :message="error" style="margin-top:12px" />
    <a-list :loading="loading" :data-source="members" style="margin-top:12px"><template #renderItem="{item}"><a-list-item><span>{{item.label}} <small>({{item.username}})</small></span><template #actions><a-button :disabled="loading" type="link" @click="choose(item)">提及</a-button></template></a-list-item></template></a-list>
    <a-pagination :current="page" :total="total" :page-size="20" :show-size-changer="false" @change="paginate" />
  </a-modal>
</template>
<script setup lang="ts">
import {ref,watch,onBeforeUnmount} from 'vue'
import {mentionsApi as api,type MentionMember} from '@/api/mentions'
import {useUserStore} from '@/stores/user'
const props=defineProps<{projectId:string;context:'case'|'plan'|'defect'}>(),user=useUserStore()
const open=ref(false),loading=ref(false),search=ref(''),page=ref(1),total=ref(0),members=ref<MentionMember[]>([]),error=ref('')
let sequence=0,finish:((member:MentionMember|undefined)=>void)|undefined
async function load(){const current=++sequence,project=props.projectId,context=props.context;loading.value=true;error.value='';members.value=[];try{const data=await api.members(project,{context,search:search.value,page:page.value});if(current===sequence&&open.value){members.value=data.items;total.value=data.total}}catch(failure){if(current===sequence){error.value='读取成员失败，请重试';total.value=0}}finally{if(current===sequence)loading.value=false}}
function pick(){if(open.value)return Promise.resolve(undefined);open.value=true;search.value='';page.value=1;total.value=0;void load();return new Promise<MentionMember|undefined>(resolve=>finish=resolve)}
function cancel(){open.value=false;++sequence;finish?.(undefined);finish=undefined}
function choose(member:MentionMember){if(loading.value||!members.value.some(r=>r.id===member.id))return;open.value=false;++sequence;finish?.({...member});finish=undefined}
function searchMembers(){page.value=1;void load()}
function paginate(value:number){page.value=value;void load()}
watch(()=>[props.projectId,props.context,user.user?.id],cancel)
onBeforeUnmount(cancel)
defineExpose({pick})
</script>
