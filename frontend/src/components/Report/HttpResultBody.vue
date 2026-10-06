<template>
  <a-space wrap class="body-controls">
    <a-select
      v-model:value="charset"
      aria-label="响应字符集"
      :options="charsets"
      style="width: 130px"
    />
    <a-radio-group v-model:value="mode" aria-label="响应正文显示方式"
      ><a-radio-button value="text">原文</a-radio-button
      ><a-radio-button v-if="json" value="json">JSON</a-radio-button
      ><a-radio-button v-if="previewable" value="preview">{{
        isPdf ? "PDF" : "图片"
      }}</a-radio-button></a-radio-group
    >
    <a-button aria-label="复制实际正文" @click="copy">复制</a-button
    ><a-button aria-label="下载实际正文" @click="download">{{
      body.truncated ? "下载已捕获内容" : "下载"
    }}</a-button>
  </a-space>
  <a-alert
    v-if="body.truncated"
    type="warning"
    :message="`正文${body.byteLength}字节，本次捕获${body.capturedBytes}字节；下面及下载仅包含已捕获内容`"
  />
  <a-alert
    v-if="error || decoded.error"
    type="error"
    :message="error || decoded.error"
  />
  <img
    v-if="mode === 'preview' && !isPdf"
    :src="blobUrl"
    alt="实际响应图片"
    class="response-image"
  />
  <object
    v-else-if="mode === 'preview' && isPdf"
    :data="blobUrl"
    type="application/pdf"
    class="response-pdf"
    aria-label="实际响应PDF"
  />
  <pre v-else class="response-body" aria-label="实际响应正文">{{
    display
  }}</pre>
</template>
<script setup lang="ts">
import { computed, ref, watch, onUnmounted } from "vue";
import { message } from "ant-design-vue";
import { bytes, decodeBody, type HttpBody } from "@/api/nativeHttpReport";
const props = defineProps<{ body: HttpBody }>();
const charset = ref("utf-8"),
  mode = ref("text"),
  error = ref(""),
  blobUrl = ref("");
const charsets = computed(() =>
  [
    ...new Set([
      props.body.charset || "utf-8",
      "utf-8",
      "gb18030",
      "iso-8859-1",
      "utf-16le",
    ]),
  ].map((value) => ({ value, label: value })),
);
const decoded = computed(() => {
  try {
    return { text: decodeBody(props.body, charset.value), error: "" };
  } catch (exception) {
    console.error("实际HTTP正文解码失败", exception);
    return { text: "", error: "字符集解码失败，请切换字符集或下载实际字节" };
  }
});
const json = computed(() =>
  props.body.contentType.toLowerCase().includes("json"),
);
const isPdf = computed(() =>
  props.body.contentType.toLowerCase().includes("application/pdf"),
);
const previewable = computed(
  () =>
    !props.body.truncated &&
    (isPdf.value || props.body.contentType.toLowerCase().startsWith("image/")),
);
const display = computed(() => {
  if (mode.value !== "json") return decoded.value.text;
  try {
    return JSON.stringify(JSON.parse(decoded.value.text), null, 2);
  } catch (exception) {
    console.error("实际HTTP正文JSON格式化失败，保留原文", exception);
    return decoded.value.text;
  }
});
watch(
  () => props.body,
  (value) => {
    charset.value = value.charset || "utf-8";
    mode.value = previewable.value ? "preview" : "text";
    error.value = "";
    if (blobUrl.value) URL.revokeObjectURL(blobUrl.value);
    blobUrl.value = URL.createObjectURL(
      new Blob([bytes(value)], {
        type: value.contentType || "application/octet-stream",
      }),
    );
  },
  { immediate: true },
);
onUnmounted(() => {
  if (blobUrl.value) URL.revokeObjectURL(blobUrl.value);
});
async function copy() {
  try {
    await navigator.clipboard.writeText(display.value);
    message.success("实际正文已复制");
  } catch (exception) {
    console.error("复制实际HTTP正文失败", exception);
    error.value = "复制失败，请检查浏览器剪贴板权限";
  }
}
function download() {
  const link = document.createElement("a");
  link.href = blobUrl.value;
  link.download = isPdf.value ? "response.pdf" : "response.bin";
  link.click();
}
</script>
<style scoped>
.body-controls {
  margin-bottom: 12px;
}
.response-body {
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  max-height: 440px;
  overflow: auto;
  padding: 12px;
  background: #f7f8fa;
  margin-top: 12px;
}
.response-image {
  max-width: 100%;
  max-height: 480px;
  object-fit: contain;
}
.response-pdf {
  width: 100%;
  height: 480px;
}
</style>
