<template>
  <div class="request-file-picker">
    <div
      v-for="(file, index) in modelValue"
      :key="file.fileId"
      class="selected-file"
    >
      <a-input
        v-if="showAlias"
        :value="
          file.fileAlias || metadata[file.fileId]?.fileName || file.fileId
        "
        :disabled="disabled"
        :maxlength="255"
        :aria-label="`请求文件别名${index + 1}`"
        @change="alias(index, $event.target.value)"
      />
      <span v-else>{{ metadata[file.fileId]?.fileName || file.fileId }}</span>
      <a-button
        type="link"
        :aria-label="`下载请求文件${index + 1}`"
        @click="download(file.fileId)"
        >下载</a-button
      >
      <a-button
        type="text"
        :disabled="disabled"
        :aria-label="`移除请求文件引用${index + 1}`"
        @click="unlink(index)"
        ><CloseOutlined
      /></a-button>
    </div>
    <a-button
      :disabled="disabled || !projectId"
      @click="
        open = true;
        load();
      "
      >添加文件</a-button
    >
    <a-alert v-if="error" :message="error" type="error" />
    <a-modal
      v-model:open="open"
      title="添加文件"
      width="min(760px,100vw)"
      :ok-button-props="{ disabled: disabled || busy || !selected.length }"
      @ok="apply"
    >
      <a-alert
        v-if="error"
        :message="error"
        type="error"
        class="file-toolbar"
      />
      <a-space wrap class="file-toolbar"
        ><a-input-search
          v-model:value="search"
          placeholder="搜索文件名称"
          aria-label="搜索请求文件"
          @search="
            page = 1;
            load();
          "
        /><a-upload
          :multiple="multiple"
          :show-upload-list="false"
          :before-upload="upload"
          ><a-button :disabled="disabled || busy">上传文件</a-button></a-upload
        ><span
          >单文件最大 {{ (maxSize / 1024 / 1024).toFixed(0) }} MB</span
        ></a-space
      >
      <a-table
        :columns="columns"
        :data-source="items"
        row-key="fileId"
        :loading="busy"
        size="small"
        :scroll="{ x: 600 }"
        :row-selection="{
          type: multiple ? 'checkbox' : 'radio',
          selectedRowKeys: selected,
          onChange: selection,
        }"
        :pagination="{
          current: page,
          pageSize: 50,
          total,
          showSizeChanger: false,
          onChange: (p: number) => {
            page = p;
            load();
          },
        }"
      >
        <template #bodyCell="{ column, record }"
          ><template v-if="column.key === 'size'"
            >{{ record.byteLength }} bytes</template
          ><template v-if="column.key === 'actions'"
            ><a-button type="link" @click="download(record.fileId)"
              >下载</a-button
            ><a-popconfirm
              title="从项目文件中移除？已冻结的执行仍保留原文件。"
              @confirm="remove(record.fileId)"
              ><a-button type="link" danger :disabled="disabled"
                >移除</a-button
              ></a-popconfirm
            ></template
          ></template
        >
      </a-table>
    </a-modal>
  </div>
</template>
<script setup lang="ts">
import { ref, reactive, watch } from "vue";
import { CloseOutlined } from "@ant-design/icons-vue";
import type { Key } from "ant-design-vue/es/_util/type";
import {
  nativeRequestFilesApi,
  type FileReference,
  type RequestFile,
} from "@/api/nativeRequestFiles";
const props = defineProps<{
  modelValue: FileReference[];
  projectId: string;
  multiple?: boolean;
  showAlias?: boolean;
  disabled?: boolean;
}>();
const emit = defineEmits<{ "update:modelValue": [value: FileReference[]] }>();
const open = ref(false),
  busy = ref(false),
  error = ref(""),
  search = ref(""),
  page = ref(1),
  total = ref(0),
  maxSize = ref(10 * 1024 * 1024),
  selected = ref<Key[]>([]),
  items = ref<RequestFile[]>([]),
  metadata = reactive<Record<string, RequestFile>>({});
let listSequence = 0,
  metadataSequence = 0;
let uploadQueue: Promise<void> = Promise.resolve();
let uploadCount = 0;
const columns = [
  { title: "文件名称", dataIndex: "fileName" },
  { title: "文件大小", key: "size", width: 130 },
  { title: "操作", key: "actions", width: 140 },
];
function selection(keys: Key[]) {
  selected.value = keys;
}
async function load() {
  if (!props.projectId) return;
  const current = ++listSequence;
  busy.value = true;
  error.value = "";
  try {
    const data = await nativeRequestFilesApi.list(props.projectId, {
      page: page.value,
      size: 50,
      search: search.value,
    });
    if (current !== listSequence) return;
    items.value = data.items;
    total.value = data.total;
    maxSize.value = data.maxFileSize;
    for (const f of data.items) metadata[f.fileId] = f;
  } catch (exception) {
    console.error("读取请求文件列表失败", exception);
    if (current === listSequence) error.value = "读取文件失败，请重试";
  } finally {
    if (current === listSequence) busy.value = uploadCount > 0;
  }
}
function upload(file: File) {
  if (props.disabled || !props.projectId) return false;
  if (file.size > maxSize.value) {
    error.value = "文件超过上传大小限制";
    return false;
  }
  const project = props.projectId;
  uploadCount++;
  busy.value = true;
  uploadQueue = uploadQueue.then(async () => {
    try {
      const result = await nativeRequestFilesApi.upload(project, file);
      if (project !== props.projectId) return;
      metadata[result.fileId] = result;
      selected.value = props.multiple
        ? [...selected.value, result.fileId]
        : [result.fileId];
      await load();
      console.info("请求文件上传完成", {
        文件: result.fileId,
        字节: result.byteLength,
      });
    } catch (exception) {
      console.error("请求文件上传失败", exception);
      if (project === props.projectId) error.value = "上传失败，请重试";
    } finally {
      uploadCount--;
      busy.value = uploadCount > 0;
    }
  });
  return false;
}
function apply() {
  if (props.disabled || busy.value || !selected.value.length) return;
  const next = selected.value.map((k) => ({ fileId: String(k) }));
  const files = props.multiple
    ? [
        ...props.modelValue,
        ...next.filter(
          (f) => !props.modelValue.some((old) => old.fileId === f.fileId),
        ),
      ]
    : next.slice(0, 1);
  if (files.length > 20) {
    error.value = "每个参数最多选择20个文件";
    return;
  }
  emit("update:modelValue", files);
  open.value = false;
  selected.value = [];
}
function unlink(index: number) {
  if (!props.disabled)
    emit(
      "update:modelValue",
      props.modelValue.filter((_, i) => i !== index),
    );
}
function alias(index: number, value: string) {
  if (!props.disabled)
    emit(
      "update:modelValue",
      props.modelValue.map((f, i) =>
        i === index ? { ...f, fileAlias: value } : f,
      ),
    );
}
async function download(id: string) {
  try {
    const blob = await nativeRequestFilesApi.download(props.projectId, id);
    const url = URL.createObjectURL(blob),
      a = document.createElement("a");
    a.href = url;
    a.download = metadata[id]?.fileName || "request.bin";
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  } catch (exception) {
    console.error("下载请求文件失败", exception);
    error.value = "下载失败，文件可能已移除";
  }
}
async function remove(id: string) {
  if (props.disabled) return;
  try {
    await nativeRequestFilesApi.remove(props.projectId, id);
    selected.value = selected.value.filter((k) => k !== id);
    await load();
  } catch (exception) {
    console.error("移除请求文件失败", exception);
    error.value = "移除失败，请重试";
  }
}
watch(
  () => props.projectId,
  () => {
    listSequence++;
    metadataSequence++;
    open.value = false;
    items.value = [];
    selected.value = [];
    page.value = 1;
    for (const key of Object.keys(metadata)) delete metadata[key];
  },
);
watch(
  () => [props.projectId, JSON.stringify(props.modelValue)],
  async () => {
    const current = ++metadataSequence;
    error.value = "";
    for (const f of props.modelValue) {
      if (metadata[f.fileId]) continue;
      try {
        const m = await nativeRequestFilesApi.metadata(
          props.projectId,
          f.fileId,
        );
        if (current === metadataSequence) metadata[m.fileId] = m;
      } catch (exception) {
        console.error("读取已选请求文件元数据失败", exception);
        if (current === metadataSequence)
          error.value = "已选文件可能已移除，请重新选择";
      }
    }
  },
  { immediate: true },
);
</script>
<style scoped>
.selected-file {
  display: flex;
  gap: 4px;
  align-items: center;
  margin-bottom: 6px;
  min-width: 0;
}
.selected-file > span {
  overflow-wrap: anywhere;
}
.selected-file :deep(.ant-input) {
  min-width: 80px;
}
.file-toolbar {
  margin-bottom: 12px;
}
.request-file-picker {
  min-width: 0;
}
</style>
