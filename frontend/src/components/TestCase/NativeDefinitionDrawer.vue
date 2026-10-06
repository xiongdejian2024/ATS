<template>
  <a-drawer
    :open="open"
    title="接口详情"
    width="min(720px,100vw)"
    :closable="!saving"
    :keyboard="!saving"
    :mask-closable="!saving"
    @close="close"
  >
    <a-spin :spinning="loading">
      <a-alert v-if="error" :message="error" type="error" show-icon>
        <template #action
          ><a-button :disabled="saving" @click="load(true)"
            >重新加载版本</a-button
          ></template
        >
      </a-alert>
      <a-form
        v-if="definition"
        layout="vertical"
        :disabled="saving || loading || !canEdit"
      >
        <a-form-item label="接口名称" required
          ><a-input
            v-model:value="name"
            :maxlength="255"
            aria-label="接口定义名称"
        /></a-form-item>
        <a-form-item label="所属模块"
          ><a-tree-select
            v-model:value="moduleId"
            allow-clear
            placeholder="未分配模块"
            :tree-data="caseFolderTree(modules)"
            :field-names="{ label: 'title', value: 'key' }"
            aria-label="接口定义所属模块"
        /></a-form-item>
        <a-form-item label="协议" required
          ><a-input
            v-model:value="protocol"
            :maxlength="50"
            aria-label="接口定义协议"
        /></a-form-item>
        <a-form-item label="路径" required
          ><a-input
            v-model:value="path"
            :maxlength="500"
            aria-label="接口定义路径"
        /></a-form-item>
        <a-form-item label="状态"
          ><a-select
            v-model:value="state"
            allow-clear
            :options="nativeStateOptions('api')"
            placeholder="未设置"
            aria-label="接口定义状态"
        /></a-form-item>
        <a-form-item label="标签"
          ><a-select
            v-model:value="tags"
            mode="tags"
            :token-separators="[',']"
            aria-label="接口定义标签"
        /></a-form-item>
        <NativeExecutionEditor
          v-if="['HTTP', 'HTTPS'].includes(protocol)"
          :key="definition.id"
          v-model="parameters"
          category="api"
          :api-cases="[]"
          :disabled="saving || loading || !canEdit"
          @draft="editorDraft = $event"
          @error="editorError = $event"
        />
        <details>
          <summary>高级配置</summary>
          <a-form-item label="请求参数结构"
            ><a-textarea
              v-model:value="parameters"
              :rows="8"
              aria-label="接口定义参数结构"
          /></a-form-item>
        </details>
      </a-form>
    </a-spin>
    <template #footer
      ><a-space
        ><a-button :disabled="saving" @click="close">关闭</a-button
        ><a-button
          v-if="canEdit"
          type="primary"
          :loading="saving"
          :disabled="loading || !definition || !dirty || !!editorError"
          @click="save"
          >保存</a-button
        ></a-space
      ></template
    >
  </a-drawer>
</template>
<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { Modal, message } from "ant-design-vue";
import {
  nativeCaseApi,
  nativeStateOptions,
  type NativeDefinition,
} from "@/api/nativeCase";
import type { CaseFolder } from "@/api/planCaseWorkspace";
import { caseFolderTree } from "@/components/TestPlan/planCaseFolders";
import NativeExecutionEditor from "./NativeExecutionEditor.vue";
const props = defineProps<{
  open: boolean;
  projectId: string;
  definitionId: string;
  modules: CaseFolder[];
}>();
const emit = defineEmits<{
  "update:open": [value: boolean];
  saving: [value: boolean];
  saved: [];
}>();
const definition = ref<NativeDefinition>(),
  loading = ref(false),
  saving = ref(false),
  error = ref(""),
  canEdit = ref(false);
const name = ref(""),
  moduleId = ref<string>(),
  protocol = ref(""),
  path = ref(""),
  state = ref<string>(),
  tags = ref<string[]>([]),
  parameters = ref("{}"),
  original = ref(""),
  editorDraft = ref(""),
  editorError = ref("");
const snapshot = () =>
  JSON.stringify([
    name.value,
    moduleId.value,
    protocol.value,
    path.value,
    state.value,
    tags.value,
    parameters.value,
    editorDraft.value,
  ]);
const dirty = computed(
  () => !!definition.value && snapshot() !== original.value,
);
let sequence = 0;
async function load(preserve = false) {
  const current = ++sequence;
  loading.value = true;
  try {
    const catalog = await nativeCaseApi.catalog(props.projectId);
    if (current !== sequence || !props.open) return;
    const row = catalog.definitions.find((d) => d.id === props.definitionId);
    if (!row) throw new Error("接口已删除或来源项目已改变");
    definition.value = row;
    canEdit.value = catalog.canEdit;
    if (!preserve || !original.value) {
      name.value = row.name;
      moduleId.value = row.module_id || undefined;
      protocol.value = row.protocol;
      path.value = row.path;
      state.value = row.state || undefined;
      tags.value = [...(row.tags || [])];
      parameters.value = JSON.stringify(row.parameters, null, 2);
      editorDraft.value = editorError.value = "";
      original.value = snapshot();
    }
    error.value = "";
  } catch (exception: any) {
    console.error("加载接口详情失败，保留编辑草稿", exception);
    if (current === sequence)
      error.value =
        exception.response?.data?.detail || "接口详情加载失败，请重试";
  } finally {
    if (current === sequence) loading.value = false;
  }
}
async function save() {
  if (
    !definition.value ||
    !canEdit.value ||
    loading.value ||
    saving.value ||
    editorError.value
  )
    return;
  saving.value = true;
  emit("saving", true);
  try {
    const structure = JSON.parse(parameters.value);
    if (!structure || Array.isArray(structure) || typeof structure !== "object")
      throw new Error("参数结构须为JSON对象");
    await nativeCaseApi.saveDefinition(
      props.projectId,
      {
        name: name.value.trim(),
        module_id: moduleId.value || null,
        protocol: protocol.value.trim().toUpperCase(),
        path: path.value.trim(),
        state: state.value || null,
        tags: tags.value,
        parameters: structure,
        expectedRevision: definition.value.revision,
      },
      definition.value.id,
    );
    console.info("接口定义已保存", {
      projectId: props.projectId,
      definitionId: definition.value.id,
    });
    message.success("接口已保存");
    original.value = snapshot();
    emit("saved");
    emit("update:open", false);
  } catch (exception: any) {
    console.error("保存接口详情失败，保留编辑草稿", exception);
    error.value =
      typeof exception.response?.data?.detail === "string"
        ? exception.response.data.detail
        : exception.message || "保存失败，请重试";
  } finally {
    saving.value = false;
    emit("saving", false);
  }
}
function close() {
  if (saving.value) return;
  if (!dirty.value) {
    ++sequence;
    emit("update:open", false);
    return;
  }
  Modal.confirm({
    title: "接口尚未保存",
    content: "关闭后将丢失编辑草稿，是否继续？",
    okText: "关闭",
    cancelText: "继续编辑",
    onOk: () => {
      ++sequence;
      emit("update:open", false);
    },
  });
}
watch(
  () => [props.open, props.projectId, props.definitionId],
  () => {
    ++sequence;
    definition.value = undefined;
    error.value = "";
    original.value = "";
    if (props.open) void load();
  },
  { immediate: true },
);
</script>
