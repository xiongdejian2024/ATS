<template>
  <a-form layout="vertical">
    <a-form-item label="启用本地静态 Mock"><a-switch :checked="value.enable" :disabled="disabled" aria-label="启用本地静态Mock" @change="change('enable', $event)" /></a-form-item>
    <p>Mock 在执行节点内返回配置的响应，不访问目标地址；执行报告明确标记 Mock。</p>
    <a-form-item label="响应状态码"><a-input-number :value="value.statusCode" :min="200" :max="599" :precision="0" :disabled="disabled" aria-label="Mock状态码" @update:value="change('statusCode', $event)" /></a-form-item>
    <a-form-item label="响应头（JSON）"><a-textarea :value="headers" :rows="3" :disabled="disabled" aria-label="Mock响应头" @update:value="changeHeaders" /></a-form-item>
    <a-form-item label="响应正文"><a-textarea :value="value.body" :rows="6" :maxlength="131072" :disabled="disabled" aria-label="Mock响应正文" @update:value="change('body', $event)" /></a-form-item>
    <a-form-item label="响应延迟（毫秒）"><a-input-number :value="value.delayMs" :min="0" :max="3000" :precision="0" :disabled="disabled" aria-label="Mock响应延迟" @update:value="change('delayMs', $event)" /></a-form-item>
    <a-alert v-if="error" type="error" :message="error" show-icon />
  </a-form>
</template>
<script setup lang="ts">
import { ref, watch } from 'vue';
import { readMockResponse } from './nativeMock';
const props=defineProps<{modelValue:string;disabled?:boolean}>();
const emit=defineEmits<{ 'update:modelValue':[value:string] }>();
const value=ref(readMockResponse('{}')), headers=ref('{}'), error=ref('');
let output='';
watch(()=>props.modelValue,raw=>{if(raw===output)return;output=raw;try{value.value=readMockResponse(raw);headers.value=JSON.stringify(value.value.headers,null,2);error.value='';}catch{value.value=readMockResponse('{}');headers.value='{}';error.value='Mock配置无效，请在高级配置中修正';}}, {immediate:true,flush:'sync'});
function publish(){let parsed:unknown;try{parsed=JSON.parse(headers.value);}catch{parsed=headers.value;}output=JSON.stringify({...value.value,headers:parsed});try{readMockResponse(output);error.value='';}catch{error.value='请检查Mock响应配置';}emit('update:modelValue',output);}
function change(field:string,item:unknown){if(props.disabled)return;(value.value as any)[field]=item;try{publish();}catch{error.value='响应头JSON无效';}}
function changeHeaders(raw:string){if(props.disabled)return;headers.value=raw;publish();}
</script>
