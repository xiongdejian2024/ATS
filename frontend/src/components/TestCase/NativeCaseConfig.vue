<template>
  <a-spin class="native-case-config" :spinning="loading">
    <a-alert v-if="error" :message="error" type="error" show-icon
      ><template #action
        ><a-button :disabled="saving" @click="load(true)"
          >重新加载</a-button
        ></template
      ></a-alert
    >
    <a-form
      v-if="config && catalog"
      layout="vertical"
      :disabled="loading || saving || readonly || !config.canEdit"
    >
      <a-form-item :label="category === 'api' ? '用例状态' : '场景状态'"
        ><a-select
          v-model:value="state"
          aria-label="原生用例状态"
          :options="nativeStateOptions(category)"
          placeholder="请选择状态"
      /></a-form-item>
      <a-descriptions size="small" :column="1"
        ><a-descriptions-item label="最近执行结果">{{
          nativeReportOptions.find((o) => o.value === config?.lastReportStatus)
            ?.label ||
          config.lastReportStatus ||
          "未执行"
        }}</a-descriptions-item
        ><a-descriptions-item v-if="category === 'scenario'" label="步骤数">{{
          config.stepTotal
        }}</a-descriptions-item></a-descriptions
      >
      <template v-if="category === 'api'">
        <a-form-item label="关联接口"
          ><a-space wrap
            ><a-select
              v-model:value="definitionId"
              aria-label="关联接口定义"
              allow-clear
              show-search
              option-filter-prop="label"
              :options="
                catalog.definitions.map((d) => ({ label: d.name, value: d.id }))
              "
              style="width: 280px; max-width: 100%"
              @change="selectDefinition"
            /><a-button
              v-if="!readonly && catalog.canCreate"
              @click="editEntity('definition')"
              >新建接口</a-button
            ><a-button
              v-if="!readonly && catalog.canEdit && definition"
              @click="editEntity('definition', definition)"
              >编辑接口</a-button
            ></a-space
          ></a-form-item
        >
        <a-descriptions v-if="definition" size="small" :column="1"
          ><a-descriptions-item label="协议">{{
            definition.protocol
          }}</a-descriptions-item
          ><a-descriptions-item label="请求路径">{{
            definition.path
          }}</a-descriptions-item
          ><a-descriptions-item label="接口参数变更">{{
            definitionId !== config.apiDefinitionId || config.apiChange === null
              ? "—"
              : config.apiChange
                ? "有变更"
                : "无变更"
          }}</a-descriptions-item></a-descriptions
        >
        <a-form-item label="请求参数"
          ><a-textarea
            v-model:value="parametersText"
            aria-label="用例请求参数"
            :rows="5"
        /></a-form-item>
        <a-button
          v-if="!readonly && definition"
          :disabled="saving || !config.canEdit"
          @click="syncParameters"
          >同步接口参数</a-button
        >
      </template>
      <NativeExecutionEditor
        v-if="
          category === 'scenario' ||
          ['HTTP', 'HTTPS'].includes(definition?.protocol || '')
        "
        :key="projectId + ':' + caseId + ':' + config.revision"
        v-model="parametersText"
        :category="category"
        :api-cases="catalog.apiCases || []"
        :disabled="loading || saving || readonly || !config.canEdit"
        @draft="editorDraft = $event"
        @error="editorError = $event"
      />
      <a-form-item :label="category === 'api' ? '用例环境' : '场景环境'"
        ><a-space wrap
          ><a-select
            v-model:value="environmentId"
            aria-label="原生用例环境"
            allow-clear
            :options="
              catalog.environments.map((e) => ({ label: e.name, value: e.id }))
            "
            style="width: 280px; max-width: 100%"
          /><a-button
            v-if="!readonly && catalog.canCreate"
            @click="editEntity('environment')"
            >新建环境</a-button
          ><a-button
            v-if="!readonly && catalog.canEdit && environment"
            @click="editEntity('environment', environment)"
            >编辑环境</a-button
          ></a-space
        ></a-form-item
      >
      <a-button
        v-if="!readonly && config.canEdit"
        type="primary"
        :loading="saving"
        :disabled="loading || !!loadError || !!editorError"
        aria-label="保存原生用例配置"
        @click="save"
        >保存配置</a-button
      >
    </a-form>
    <a-modal
      v-model:open="entityOpen"
      :title="
        entityKind === 'definition'
          ? entityId
            ? '编辑接口'
            : '新建接口'
          : entityId
            ? '编辑环境'
            : '新建环境'
      "
      :confirm-loading="saving"
      :closable="!saving"
      :keyboard="!saving"
      :mask-closable="!saving"
      :cancel-button-props="{ disabled: saving }"
      @ok="saveEntity"
    >
      <a-form layout="vertical" :disabled="saving"
        ><a-form-item label="名称" required
          ><a-input
            v-model:value="entityName"
            aria-label="原生配置名称"
            :maxlength="255" /></a-form-item
        ><template v-if="entityKind === 'definition'"
          ><a-form-item label="协议" required
            ><a-input
              v-model:value="protocol"
              aria-label="接口协议"
              :maxlength="50" /></a-form-item
          ><a-form-item label="请求路径" required
            ><a-input
              v-model:value="path"
              aria-label="接口请求路径"
              :maxlength="500" /></a-form-item
          ><a-form-item label="参数结构"
            ><a-textarea
              v-model:value="definitionParameters"
              aria-label="接口参数结构"
              :rows="5" /></a-form-item></template
        ><a-form-item v-else label="环境地址" required
          ><a-input
            v-model:value="address"
            aria-label="接口环境地址"
            :maxlength="500" /></a-form-item></a-form
      ><a-alert v-if="entityError" :message="entityError" type="error" show-icon
        ><template #action
          ><a-button :disabled="saving" @click="retryEntity"
            >重新加载版本</a-button
          ></template
        ></a-alert
      >
    </a-modal>
  </a-spin>
</template>
<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { message, Modal } from "ant-design-vue";
import { onBeforeRouteLeave, onBeforeRouteUpdate } from "vue-router";
import NativeExecutionEditor from "./NativeExecutionEditor.vue";
import {
  nativeCaseApi as api,
  nativeStateOptions,
  nativeReportOptions,
  type NativeConfig,
  type NativeCatalog,
  type NativeDefinition,
  type NativeEnvironment,
} from "@/api/nativeCase";
const props = defineProps<{
  projectId: string;
  caseId: string;
  category: string;
  readonly?: boolean;
}>();
const emit = defineEmits<{
  saving: [value: boolean];
  saved: [];
  dirty: [value: boolean];
}>();
const config = ref<NativeConfig>(),
  catalog = ref<NativeCatalog>(),
  loading = ref(false),
  saving = ref(false),
  error = ref(""),
  loadError = ref(false);
const state = ref<string>(),
  definitionId = ref<string>(),
  environmentId = ref<string>(),
  parametersText = ref("{}"),
  sync = ref(false);
const editorDraft = ref(""),
  editorError = ref("");
const definition = computed(() =>
  catalog.value?.definitions.find((d) => d.id === definitionId.value),
);
const environment = computed(() =>
  catalog.value?.environments.find((e) => e.id === environmentId.value),
);
let sequence = 0;
const original = ref("");
const draftSignature = () =>
  JSON.stringify([
    state.value,
    definitionId.value,
    environmentId.value,
    parametersText.value,
    sync.value,
    editorDraft.value,
  ]);
const dirty = computed(
  () => !!config.value && original.value !== draftSignature(),
);
watch(dirty, (value) => emit("dirty", value));
function adopt(value: NativeConfig) {
  editorDraft.value = "";
  editorError.value = "";
  config.value = value;
  state.value = value.state || undefined;
  definitionId.value = value.apiDefinitionId || undefined;
  environmentId.value = value.environmentId || undefined;
  parametersText.value = JSON.stringify(value.parameters, null, 2);
  sync.value = false;
  original.value = draftSignature();
}
async function load(keepDraft = false) {
  const draft =
    keepDraft && config.value
      ? {
          state: state.value,
          definitionId: definitionId.value,
          environmentId: environmentId.value,
          parameters: parametersText.value,
          sync: sync.value,
        }
      : undefined;
  const current = ++sequence;
  loading.value = true;
  error.value = "";
  loadError.value = false;
  try {
    const [cat, value] = await Promise.all([
      api.catalog(props.projectId),
      api.config(props.projectId, props.caseId),
    ]);
    if (current === sequence) {
      catalog.value = cat;
      adopt(value);
      if (draft) {
        state.value = draft.state;
        definitionId.value = draft.definitionId;
        environmentId.value = draft.environmentId;
        parametersText.value = draft.parameters;
        sync.value = draft.sync;
      }
    }
  } catch (failure) {
    console.error("加载原生用例配置失败", failure);
    if (current === sequence) {
      error.value = "配置加载失败，请重试；编辑草稿保留";
      loadError.value = true;
    }
  } finally {
    if (current === sequence) loading.value = false;
  }
}
function selectDefinition() {
  if (definition.value) {
    parametersText.value = JSON.stringify(definition.value.parameters, null, 2);
    sync.value = true;
  }
}
function syncParameters() {
  selectDefinition();
  message.info("已加载当前接口参数，保存后生效");
}
function jsonObject(raw: string) {
  const value = JSON.parse(raw);
  if (!value || typeof value !== "object" || Array.isArray(value))
    throw new Error("请求参数必须是JSON对象");
  return value;
}
function setSaving(value: boolean) {
  saving.value = value;
  emit("saving", value);
}
async function save() {
  if (
    !config.value?.canEdit ||
    saving.value ||
    props.readonly ||
    loadError.value
  )
    return;
  const context = props.projectId + ":" + props.caseId;
  setSaving(true);
  error.value = "";
  try {
    const value = await api.saveConfig(props.projectId, props.caseId, {
      state: state.value,
      environmentId: environmentId.value || null,
      apiDefinitionId: definitionId.value || null,
      parameters: jsonObject(parametersText.value),
      syncDefinition: sync.value,
      expectedRevision: config.value.revision,
      expectedDefinitionRevision:
        props.category === "api" ? definition.value?.revision : null,
    });
    if (context !== props.projectId + ":" + props.caseId) return;
    adopt(value);
    message.success("原生用例配置已保存");
    emit("saved");
  } catch (failure) {
    console.error("保存原生用例配置失败，保留草稿", failure);
    error.value = "保存失败，请核对状态、参数和配置版本；草稿保留";
  } finally {
    setSaving(false);
  }
}
const entityOpen = ref(false),
  entityKind = ref<"definition" | "environment">("definition"),
  entityId = ref<string>(),
  entityRevision = ref(0),
  entityName = ref(""),
  protocol = ref("HTTP"),
  path = ref(""),
  address = ref(""),
  definitionParameters = ref("{}"),
  entityError = ref("");
function editEntity(
  kind: "definition" | "environment",
  value?: NativeDefinition | NativeEnvironment,
) {
  entityKind.value = kind;
  entityId.value = value?.id;
  entityRevision.value = value?.revision || 0;
  entityName.value = value?.name || "";
  protocol.value = (value as NativeDefinition)?.protocol || "HTTP";
  path.value = (value as NativeDefinition)?.path || "";
  address.value = (value as NativeEnvironment)?.address || "";
  definitionParameters.value = JSON.stringify(
    (value as NativeDefinition)?.parameters || {},
    null,
    2,
  );
  entityError.value = "";
  entityOpen.value = true;
}
async function retryEntity() {
  const context = props.projectId + ":" + props.caseId;
  setSaving(true);
  try {
    const value = await api.catalog(props.projectId);
    if (context !== props.projectId + ":" + props.caseId) return;
    const current = (
      entityKind.value === "definition" ? value.definitions : value.environments
    ).find((row) => row.id === entityId.value);
    if (entityId.value && !current) throw new Error("原配置已不存在");
    catalog.value = value;
    entityRevision.value = current?.revision || 0;
    entityError.value = "";
    message.info("配置版本已刷新，编辑草稿保留");
  } catch (failure) {
    console.error("重载原生配置版本失败", failure);
    entityError.value = "重新加载失败，草稿保留，请重试";
  } finally {
    setSaving(false);
  }
}
async function saveEntity() {
  if (saving.value) return;
  const context = props.projectId + ":" + props.caseId;
  setSaving(true);
  entityError.value = "";
  try {
    const common = {
      name: entityName.value.trim(),
      expectedRevision: entityRevision.value,
    };
    const value =
      entityKind.value === "definition"
        ? await api.saveDefinition(
            props.projectId,
            {
              ...common,
              protocol: protocol.value.trim().toUpperCase(),
              path: path.value.trim(),
              parameters: jsonObject(definitionParameters.value),
            },
            entityId.value,
          )
        : await api.saveEnvironment(
            props.projectId,
            { ...common, address: address.value.trim() },
            entityId.value,
          );
    if (context !== props.projectId + ":" + props.caseId) return;
    catalog.value = value;
    const current = await api.config(props.projectId, props.caseId);
    if (context !== props.projectId + ":" + props.caseId) return;
    if (config.value) config.value.apiChange = current.apiChange;
    entityOpen.value = false;
    message.success("配置已保存");
    emit("saved");
  } catch (failure) {
    console.error("保存接口或环境配置失败，保留草稿", failure);
    entityError.value = "保存失败，请核对名称、参数或配置版本；草稿保留";
  } finally {
    setSaving(false);
  }
}
watch(
  () => [props.projectId, props.caseId],
  () => {
    ++sequence;
    config.value = undefined;
    catalog.value = undefined;
    entityOpen.value = false;
    void load();
  },
  { immediate: true },
);
function canLeave() {
  if (saving.value) return false;
  if (!dirty.value) return true;
  return new Promise<boolean>((resolve) =>
    Modal.confirm({
      title: "配置尚未保存",
      content: "离开后将丢失编辑草稿，是否继续？",
      okText: "离开",
      cancelText: "继续编辑",
      onOk: () => resolve(true),
      onCancel: () => resolve(false),
    }),
  );
}
onBeforeRouteLeave(canLeave);
onBeforeRouteUpdate(canLeave);
</script>

<style scoped>
.native-case-config {
  min-width: 0;
}
.native-case-config :deep(.ant-descriptions-item-content) {
  overflow-wrap: anywhere;
}
</style>
