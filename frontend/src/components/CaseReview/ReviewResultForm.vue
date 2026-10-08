<template>
  <div class="review-result-form">
    <a-radio-group
      v-model:value="decision"
      :disabled="locked"
      @change="changeDecision"
    >
      <a-radio value="approved">通过</a-radio>
      <a-radio value="rejected">不通过</a-radio>
      <a-radio value="suggestion"
        ><a-tooltip title="建议不改变已有有效通过或不通过结论"
          >建议</a-tooltip
        ></a-radio
      >
    </a-radio-group>
    <template v-if="inlineReason">
      <p class="reason-label">
        评审理由<span v-if="decision !== 'approved'">（必填）</span>
      </p>
      <CaseRichText v-model="reason" :disabled="locked" label="批量评审理由" :upload-image="projectId ? uploadImage : undefined" :select-image="projectId ? selectImage : undefined" @uploading="setUploading" />
    </template>
    <a-button
      v-else
      class="reason-button"
      size="small"
      :disabled="locked"
      @click="reasonOpen = true"
      >＋ 评审理由</a-button
    >
    <p v-if="reason.length > 10000" class="reason-error">
      评审理由不能超过10000字符
    </p>
    <a-alert v-if="error" :message="error" type="error" show-icon />
    <template v-if="projectId"><a-button :disabled="locked" @click="selectFiles">文件库附件</a-button><p v-for="file in files" :key="file.id">{{file.fileName}} <a-button type="link" :disabled="locked" @click="files=files.filter(f=>f.id!==file.id)">取消选择</a-button></p></template>
    <FileLibraryPicker v-if="projectId" ref="picker" :project-id="projectId" />
    <a-button
      class="submit-button"
      type="primary"
      :loading="saving"
      :disabled="submitDisabled"
      @click="submit"
      >提交评审</a-button
    >
    <a-modal
      v-model:open="reasonOpen"
      title="评审理由"
      :width="680"
      :closable="!saving && !uploading"
      :mask-closable="!saving && !uploading"
      :keyboard="!saving && !uploading"
      :cancel-button-props="{ disabled: saving || uploading }"
      :ok-button-props="{ disabled: submitDisabled }"
      :confirm-loading="saving"
      ok-text="提交评审"
      destroy-on-close
      @ok="submit"
    >
      <CaseRichText v-model="reason" :disabled="locked" label="评审理由" :upload-image="projectId ? uploadImage : undefined" :select-image="projectId ? selectImage : undefined" @uploading="setUploading" />
      <p v-if="decision !== 'approved'" class="reason-label">
        不通过或建议必须填写评审理由
      </p>
      <p v-if="reason.length > 10000" class="reason-error">
        评审理由不能超过10000字符
      </p>
      <a-alert v-if="error" :message="error" type="error" show-icon />
    </a-modal>
  </div>
</template>
<script setup lang="ts">
import { computed, ref, onMounted, onBeforeUnmount } from "vue";
import {Modal,message} from 'ant-design-vue';
import FileLibraryPicker from '@/components/TestCase/FileLibraryPicker.vue';
import {fileLibraryApi,type LibraryFile} from '@/api/fileLibrary';
import CaseRichText from "@/components/TestCase/CaseRichText.vue";
export type ReviewDecision = "approved" | "rejected" | "suggestion";
const props = defineProps<{
  disabled?: boolean;
  projectId?: string;
  inlineReason?: boolean;
  submitResult: (decision: ReviewDecision, reason: string, fileIds: string[]) => Promise<void>;
}>();
const emit=defineEmits<{uploading:[value:boolean]}>();
const picker=ref<InstanceType<typeof FileLibraryPicker>>(),files=ref<LibraryFile[]>([]),uploading=ref(false);
function setUploading(value:boolean){uploading.value=value;emit('uploading',value)}
async function uploadImage(file:File){const row=await fileLibraryApi.upload(props.projectId!,file,{image:true});return {src:row.src!,fileName:row.fileName}}
async function selectImage(){const rows=await picker.value?.pick({imagesOnly:true,limit:1});const row=rows?.[0];return row?.src?{src:row.src,fileName:row.fileName}:undefined}
async function selectFiles(){if(locked.value)return;setUploading(true);try{const rows=await picker.value?.pick({limit:50});if(rows?.length)files.value=rows}finally{setUploading(false)}}
const decision = ref<ReviewDecision>("approved"),
  reason = ref(""),
  reasonOpen = ref(false),
  saving = ref(false),
  error = ref("");
const locked = computed(() => !!props.disabled || saving.value || uploading.value);
function hasReason(value: string) {
  if (!/<\/?[a-z][\s\S]*>/i.test(value))
    return !!value.replace(/[\u200b\ufeff]/g, "").trim();
  const doc = new DOMParser().parseFromString(value, "text/html");
  doc
    .querySelectorAll("script, style, template")
    .forEach((node) => node.remove());
  return (
    !!doc.body.textContent?.replace(/[\u200b\ufeff]/g, "").trim() ||
    [...doc.querySelectorAll("img")].some(
      (image) => !!image.getAttribute("src")?.trim(),
    )
  );
}
const submitDisabled = computed(
  () =>
    locked.value ||
    reason.value.length > 10000 ||
    (decision.value !== "approved" && !hasReason(reason.value)),
);
function changeDecision() {
  error.value = "";
  if (!props.inlineReason && decision.value !== "approved")
    reasonOpen.value = true;
}
async function submit() {
  if (submitDisabled.value) return;
  saving.value = true;
  error.value = "";
  try {
    await props.submitResult(decision.value, reason.value.trim(),files.value.map(f=>f.id));
    reasonOpen.value = false;
    reason.value = "";files.value=[];
    decision.value = "approved";
  } catch (failure) {
    console.error("提交评审结论失败，理由草稿保留", failure);
    error.value = "提交评审失败，请保留理由并重试";
  } finally {
    saving.value = false;
  }
}
async function beforeClose(){if(saving.value||uploading.value){message.warning('请等待评审素材或提交操作完成');return false}if(!reason.value&&!files.value.length)return true;return new Promise<boolean>(resolve=>Modal.confirm({title:'放弃未提交的评审理由和附件？',onOk(){reason.value='';files.value=[];resolve(true)},onCancel(){resolve(false)}}))}
function beforeUnload(event:BeforeUnloadEvent){if(reason.value||files.value.length||saving.value||uploading.value){event.preventDefault();event.returnValue=''}}
onMounted(()=>window.addEventListener('beforeunload',beforeUnload));onBeforeUnmount(()=>window.removeEventListener('beforeunload',beforeUnload));
defineExpose({beforeClose})
</script>
<style scoped>
.review-result-form {
  margin-top: 16px;
}
.reason-button {
  display: block;
  margin-top: 8px;
}
.submit-button {
  margin-top: 12px;
}
.reason-label {
  margin: 12px 0 8px;
  color: var(--ms-text-secondary);
}
.reason-error {
  margin: 8px 0;
  color: #f53f3f;
}
.review-result-form :deep(.ant-alert) {
  margin-top: 12px;
}
</style>
