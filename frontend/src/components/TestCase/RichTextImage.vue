<template>
  <NodeViewWrapper class="rich-text-image" contenteditable="false">
    <a-spin :spinning="loading">
      <a-image
        v-if="imageUrl"
        :src="imageUrl"
        :alt="String(node.attrs.alt || '图片')"
      />
      <a-alert v-else-if="failed" type="error" message="图片加载失败"
        ><template #action
          ><a-button size="small" @click="load">重试</a-button></template
        ></a-alert
      >
      <span v-else>图片</span>
    </a-spin>
    <a-button v-if="privatePath" type="link" size="small" @click="download"
      >下载图片</a-button
    >
  </NodeViewWrapper>
</template>
<script setup lang="ts">
import { computed, onBeforeUnmount, ref, watch } from "vue";
import { NodeViewWrapper, nodeViewProps } from "@tiptap/vue-3";
import { apiClient } from "@/utils/api";
import { privateImagePath } from "@/api/planCaseMedia";
import { saveCaseBlob } from "@/api/caseFeatures";
import { message } from "ant-design-vue";
const props = defineProps(nodeViewProps),
  imageUrl = ref(""),
  loading = ref(false),
  failed = ref(false);
const privatePath = computed(() =>
  privateImagePath(String(props.node.attrs.src || "")),
);
let sequence = 0,
  ownedUrl = "";
function release() {
  if (ownedUrl) {
    URL.revokeObjectURL(ownedUrl);
    ownedUrl = "";
  }
  imageUrl.value = "";
}
async function load() {
  const current = ++sequence;
  release();
  failed.value = false;
  const source = String(props.node.attrs.src || ""),
    path = privatePath.value;
  if (!path) {
    imageUrl.value = /^https?:\/\//.test(source) ? source : "";
    failed.value = !imageUrl.value;
    loading.value = false;
    return;
  }
  loading.value = true;
  try {
    const response = await apiClient
      .getInstance()
      .get<Blob>(path, { responseType: "blob" });
    if (current !== sequence) return;
    ownedUrl = URL.createObjectURL(response.data);
    imageUrl.value = ownedUrl;
  } catch (error) {
    console.error("加载富文本图片失败", error);
    if (current === sequence) failed.value = true;
  } finally {
    if (current === sequence) loading.value = false;
  }
}
async function download() {
  if (!privatePath.value) return;
  try {
    const response = await apiClient
      .getInstance()
      .get<Blob>(privatePath.value.replace(/\/preview$/, "/download"), {
        responseType: "blob",
      });
    saveCaseBlob(response.data, String(props.node.attrs.alt || "图片"));
  } catch (error) {
    console.error("下载富文本图片失败", error);
    message.error("图片下载失败");
  }
}
watch(() => props.node.attrs.src, load, { immediate: true });
onBeforeUnmount(() => {
  ++sequence;
  release();
});
</script>
<style scoped>
.rich-text-image {
  max-width: 100%;
  margin: 8px 0;
}
.rich-text-image :deep(img) {
  max-width: 100%;
  max-height: 420px;
  object-fit: contain;
}
.rich-text-image :deep(.ant-image) {
  max-width: 100%;
}
</style>
