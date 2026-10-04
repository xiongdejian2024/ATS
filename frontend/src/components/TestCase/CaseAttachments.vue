<template>
  <a-card title="附件" size="small">
    <template #extra
      ><a-upload v-if="caseId" :before-upload="upload" :show-upload-list="false"
        ><a-button :loading="busy">上传附件</a-button></a-upload
      ></template
    >
    <a-alert
      v-if="!caseId"
      message="请先保存用例，再上传附件。"
      type="info"
      show-icon
    />
    <a-spin :spinning="loading"
      ><a-list v-if="files.length" :data-source="files"
        ><template #renderItem="{ item }"
          ><a-list-item
            ><a-list-item-meta
              :title="item.fileName"
              :description="`${(item.fileSize / 1024).toFixed(1)} KB · ${item.uploadTime}`"
            /><template #actions
              ><a-button type="link" @click="download(item)">下载</a-button
              ><a-popconfirm title="删除此附件？" @confirm="remove(item)"
                ><a-button type="link" danger>删除</a-button></a-popconfirm
              ></template
            ></a-list-item
          ></template
        ></a-list
      ><a-empty v-else-if="caseId" description="暂无附件"
    /></a-spin>
  </a-card>
</template>
<script setup lang="ts">
import { ref, watch } from "vue";
import { message } from "ant-design-vue";
import {
  caseFeaturesApi as api,
  saveCaseBlob,
  type CaseFile,
} from "@/api/caseFeatures";
const props = defineProps<{ projectId: string; caseId?: string }>();
const files = ref<CaseFile[]>([]),
  loading = ref(false),
  busy = ref(false);
async function load() {
  files.value = [];
  if (!props.caseId) return;
  loading.value = true;
  try {
    files.value = await api.attachments(props.projectId, props.caseId);
  } catch (error) {
    console.error("加载用例附件失败", error);
  } finally {
    loading.value = false;
  }
}
async function upload(file: File) {
  if (!props.caseId) return false;
  busy.value = true;
  try {
    const item = await api.upload(props.projectId, props.caseId, file);
    files.value.push(item);
    message.success("附件已上传");
  } catch (error) {
    console.error("上传用例附件失败", error);
  } finally {
    busy.value = false;
  }
  return false;
}
async function download(item: CaseFile) {
  try {
    saveCaseBlob(await api.download(props.projectId, item.id), item.fileName);
  } catch (error) {
    console.error("下载用例附件失败", error);
  }
}
async function remove(item: CaseFile) {
  try {
    await api.deleteAttachment(props.projectId, item.id);
    files.value = files.value.filter((f) => f.id !== item.id);
    message.success("附件已删除");
  } catch (error) {
    console.error("删除用例附件失败", error);
  }
}
watch(() => [props.projectId, props.caseId], load, { immediate: true });
</script>
