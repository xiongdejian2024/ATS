<template>
  <a-card title="提及内容">
    <a-spin v-if="loading" />
    <a-alert v-else-if="error" type="error" :message="error" />
    <template v-else-if="source"><p>{{new Date(source.createdAt).toLocaleString('zh-CN')}}</p><CaseRichText v-if="source.contentFormat==='rich'" :model-value="source.content" readonly /><p v-else style="white-space:pre-wrap">{{source.content}}</p><a-button style="margin-top:20px" @click="openContext">打开相关协作页面</a-button></template>
    <a-button v-if="error" style="margin-top:12px" @click="load">重试</a-button>
  </a-card>
</template>
<script setup lang="ts">
import {ref,watch,onBeforeUnmount} from 'vue'
import {useRoute,useRouter} from 'vue-router'
import {notificationApi,type MentionSource} from '@/api/notification'
import {useUserStore} from '@/stores/user'
import CaseRichText from '@/components/TestCase/CaseRichText.vue'
const route=useRoute(),router=useRouter(),user=useUserStore(),source=ref<MentionSource>(),loading=ref(false),error=ref('')
let sequence=0
async function load(){const current=++sequence,id=String(route.params.notificationId||'');source.value=undefined;loading.value=true;error.value='';try{const data=await notificationApi.source(id);if(current===sequence)source.value=data}catch(failure){if(current===sequence)error.value='提及来源已不可用或当前没有访问权限'}finally{if(current===sequence)loading.value=false}}
async function openContext(){if(!source.value)return;const current=sequence;try{const latest=await notificationApi.source(String(route.params.notificationId||''));if(current===sequence)await router.push(latest.route)}catch(failure){if(current===sequence){source.value=undefined;error.value='提及来源已不可用或当前没有访问权限'}}}
watch(()=>[route.params.notificationId,user.user?.id],load,{immediate:true})
onBeforeUnmount(()=>++sequence)
</script>
