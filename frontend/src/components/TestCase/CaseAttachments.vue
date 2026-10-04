<template>
  <a-card title="附件" size="small">
    <template #extra
      ><a-upload
        v-if="caseId && !readOnly"
        :before-upload="upload"
        :show-upload-list="false"
        ><a-button :loading="busy">上传附件</a-button></a-upload
      ></template
    >
    <a-alert
      v-if="!caseId"
      message="请先保存用例，再上传附件。"
      type="info"
      show-icon
    />
    <a-alert v-if="failed" type="error" message="附件加载失败"
      ><template #action
        ><a-button size="small" @click="load">重试</a-button></template
      ></a-alert
    >
    <a-spin :spinning="loading"
      ><a-list v-if="files.length" :data-source="files"
        ><template #renderItem="{ item }"
          ><a-list-item>
            <a-list-item-meta
              :title="item.fileName"
              :description="`${(item.fileSize / 1024).toFixed(1)} KB · ${item.uploadTime}`"
            />
            <template #actions
              ><a-button
                v-if="previewable(item)"
                type="link"
                :loading="previewBusy === item.id"
                @click="preview(item)"
                >预览</a-button
              ><a-button type="link" @click="download(item)">下载</a-button
              ><a-popconfirm
                v-if="!readOnly"
                title="删除此附件？"
                @confirm="remove(item)"
                ><a-button type="link" danger>删除</a-button></a-popconfirm
              ></template
            >
          </a-list-item></template
        ></a-list
      ><a-empty
        v-else-if="caseId && !failed && !loading"
        description="暂无附件"
    /></a-spin>
    <a-modal
      :open="!!previewUrl"
      :title="previewName"
      :footer="null"
      width="min(800px,100vw)"
      @cancel="closePreview"
      ><a-image
        v-if="previewUrl"
        :src="previewUrl"
        :alt="previewName"
        :preview="false"
        class="attachment-preview"
    /></a-modal>
  </a-card>
</template>
<script setup lang="ts">
import { ref, watch, onBeforeUnmount } from "vue";
import { message } from "ant-design-vue";
import {
  caseFeaturesApi as api,
  saveCaseBlob,
  type CaseFile,
} from "@/api/caseFeatures";
const props = defineProps<{
  projectId: string;
  caseId?: string;
  readOnly?: boolean;
}>();
const files = ref<CaseFile[]>([]),
  loading = ref(false),
  failed = ref(false),
  busy = ref(false),
  previewBusy = ref(""),
  previewUrl = ref(""),
  previewName = ref("");
let sequence = 0,
  previewSequence = 0;
const scope = () => `${props.projectId}:${props.caseId}`;
const previewable = (file: CaseFile) =>
  /\.(png|jpe?g|gif|webp)$/i.test(file.fileName);
function closePreview() {
  ++previewSequence;
  if (previewUrl.value) URL.revokeObjectURL(previewUrl.value);
  previewUrl.value = "";
  previewName.value = "";
}
async function load() {
  const current = ++sequence;
  files.value = [];
  closePreview();
  previewBusy.value = "";
  failed.value = false;
  loading.value = false;
  if (!props.caseId) return;
  loading.value = true;
  try {
    const items = await api.attachments(props.projectId, props.caseId);
    if (current === sequence) files.value = items;
  } catch (error) {
    console.error("加载用例附件失败", error);
    if (current === sequence) failed.value = true;
  } finally {
    if (current === sequence) loading.value = false;
  }
}
async function upload(file: File) {
  if (!props.caseId || props.readOnly || busy.value) return false;
  const expected = scope(),
    project = props.projectId,
    caseId = props.caseId;
  busy.value = true;
  try {
    const item = await api.upload(project, caseId, file);
    if (scope() === expected) {
      files.value.push(item);
      message.success("附件已上传");
    }
  } catch (error) {
    console.error("上传用例附件失败", error);
    message.error("附件上传失败");
  } finally {
    busy.value = false;
  }
  return false;
}
async function preview(item: CaseFile) {
  const current = sequence;
  closePreview();
  const previewRequest = previewSequence;
  previewBusy.value = item.id;
  try {
    const blob = await api.download(props.projectId, item.id);
    if (current !== sequence || previewRequest !== previewSequence) return;
    previewName.value = item.fileName;
    previewUrl.value = URL.createObjectURL(blob);
  } catch (error) {
    console.error("预览用例附件失败", error);
    message.error("附件预览失败");
  } finally {
    if (current === sequence && previewRequest === previewSequence)
      previewBusy.value = "";
  }
}
async function download(item: CaseFile) {
  const current = sequence;
  try {
    const blob = await api.download(props.projectId, item.id);
    if (current === sequence) saveCaseBlob(blob, item.fileName);
  } catch (error) {
    console.error("下载用例附件失败", error);
    message.error("附件下载失败");
  }
}
async function remove(item: CaseFile) {
  if (props.readOnly) return;
  const current = sequence;
  try {
    await api.deleteAttachment(props.projectId, item.id);
    if (current === sequence)
      files.value = files.value.filter((file) => file.id !== item.id);
    message.success("附件已删除");
  } catch (error) {
    console.error("删除用例附件失败", error);
    message.error("附件删除失败");
  }
}
watch(() => [props.projectId, props.caseId], load, { immediate: true });
onBeforeUnmount(() => {
  ++sequence;
  closePreview();
});
</script>
<style scoped>
.attachment-preview {
  max-width: 100%;
  max-height: 70vh;
  object-fit: contain;
}
</style>
