<template>
  <a-space wrap
    ><a-button v-if="!disabled" :disabled="groups.length >= 100" @click="add"
      >添加后置操作：参数提取</a-button
    ><a-button
      v-if="caseId"
      :disabled="false"
      :loading="loadingResponse"
      @click="loadResponse"
      >刷新实际响应</a-button
    ></a-space
  >
  <p class="hint">临时参数可用 ${变量名} 引用，在本次用例或场景步骤中传递。</p>
  <a-alert v-if="responseError" type="error" :message="responseError" />
  <a-alert v-if="error" type="error" :message="error" />
  <a-empty v-if="!groups.length" description="暂无后置操作" />
  <div v-else class="post-layout">
    <VueDraggable
      v-model="groups"
      class="post-nav"
      handle=".drag-handle"
      :disabled="disabled"
      @end="publish"
    >
      <div
        v-for="g in groups"
        :key="g.id"
        class="post-item"
        :class="{ active: g.id === selected }"
      >
        <span v-if="!disabled" class="drag-handle">⋮⋮</span
        ><button class="processor-select" @click="selected = g.id">
          {{ g.name }}</button
        ><a-switch
          :checked="g.enable"
          :disabled="disabled"
          size="small"
          aria-label="启用后置提取器"
          @change="
            g.enable = $event === true;
            publish();
          "
        />
        <a-dropdown v-if="!disabled"
          ><a-button type="text" aria-label="后置提取器操作">···</a-button
          ><template #overlay
            ><a-menu @click="groupAction(g, String($event.key))"
              ><a-menu-item key="copy">复制</a-menu-item
              ><a-menu-item key="delete">删除</a-menu-item></a-menu
            ></template
          ></a-dropdown
        >
      </div>
    </VueDraggable>
    <div v-if="current" class="post-content">
      <a-input
        :value="current.name"
        :disabled="disabled"
        :maxlength="255"
        aria-label="后置提取器名称"
        class="processor-name"
        @change="
          current.name = $event.target.value;
          publish();
        "
      />
      <a-table
        :data-source="current.extractors"
        :columns="columns"
        :pagination="false"
        :scroll="{ x: 1150 }"
        row-key="id"
        size="small"
      >
        <template #headerCell="{ column }"
          ><a-checkbox
            v-if="column.key === 'enable'"
            :checked="
              current.extractors.length > 0 &&
              current.extractors.every((r) => r.enable)
            "
            :indeterminate="
              current.extractors.some((r) => r.enable) &&
              !current.extractors.every((r) => r.enable)
            "
            :disabled="disabled"
            aria-label="启用全部提取参数"
            @change="
              current.extractors.forEach(
                (r) => (r.enable = $event.target.checked),
              );
              publish();
            "
        /></template>
        <template #bodyCell="{ column, record }">
          <a-checkbox
            v-if="column.key === 'enable'"
            :checked="record.enable"
            :disabled="disabled"
            aria-label="启用提取参数"
            @change="
              record.enable = $event.target.checked;
              publish();
            "
          />
          <a-input
            v-else-if="
              column.key === 'variableName' || column.key === 'description'
            "
            :value="record[column.key]"
            :maxlength="column.key === 'variableName' ? 100 : 1000"
            :disabled="disabled"
            :aria-label="
              column.key === 'variableName' ? '提取变量名' : '提取描述'
            "
            @change="
              record[column.key] = $event.target.value;
              publish();
            "
          />
          <a-select
            v-else-if="column.key === 'variableType'"
            :value="record.variableType"
            :disabled="disabled"
            :options="[
              { value: 'TEMPORARY', label: '临时参数' },
              {
                value: 'ENVIRONMENT',
                label: '环境参数（待接入）',
                disabled: true,
              },
            ]"
            aria-label="提取参数类型"
            style="width: 100%"
          />
          <a-select
            v-else-if="column.key === 'extractType'"
            :value="record.extractType"
            :disabled="disabled"
            :options="extractModes"
            aria-label="提取模式"
            style="width: 100%"
            @change="
              record.extractType = $event;
              publish();
            "
          />
          <a-select
            v-else-if="column.key === 'extractScope'"
            :value="record.extractScope"
            :disabled="disabled || record.extractType !== 'REGEX'"
            :options="extractScopes"
            aria-label="提取范围"
            style="width: 100%"
            @change="
              record.extractScope = $event;
              publish();
            "
          />
          <a-space-compact v-else-if="column.key === 'expression'"
            ><a-input
              :value="record.expression"
              :maxlength="200"
              :disabled="disabled"
              aria-label="提取表达式"
              @change="
                record.expression = $event.target.value;
                publish();
              "
            /><a-tooltip
              :title="
                source?.available
                  ? '快速提取'
                  : source?.message || '请先执行请求取得响应'
              "
              ><a-button
                :disabled="disabled || !source?.available"
                aria-label="快速提取"
                @click="openFast(record)"
                >ϟ</a-button
              ></a-tooltip
            ></a-space-compact
          >
          <a-space v-else-if="column.key === 'operation'"
            ><a-button
              type="link"
              :disabled="false"
              aria-label="提取更多设置"
              @click="settings(record)"
              >设置</a-button
            ><a-dropdown v-if="!disabled"
              ><a-button type="text" aria-label="提取参数操作">···</a-button
              ><template #overlay
                ><a-menu @click="rowAction(record, String($event.key))"
                  ><a-menu-item key="copy">复制</a-menu-item
                  ><a-menu-item key="delete">删除</a-menu-item></a-menu
                ></template
              ></a-dropdown
            ></a-space
          >
        </template>
      </a-table>
      <a-button
        v-if="!disabled"
        :disabled="total >= 200"
        class="add-row"
        @click="
          current.extractors.push(newExtractor());
          publish();
        "
        >添加提取参数</a-button
      >
    </div>
  </div>
  <a-drawer
    :open="settingOpen"
    title="更多设置"
    width="min(480px, 100vw)"
    @close="settingOpen = false"
  >
    <a-form v-if="draft" layout="vertical"
      ><NativeExtractorSettings v-model="draft" :disabled="disabled"
    /></a-form>
    <template #footer
      ><a-space
        ><a-button :disabled="false" @click="settingOpen = false">取消</a-button
        ><a-button v-if="!disabled" type="primary" @click="apply(draft!)"
          >应用</a-button
        ></a-space
      ></template
    >
  </a-drawer>
  <NativeFastExtractionDrawer
    v-if="draft && source && fastOpen"
    :open="fastOpen"
    :rule="draft"
    :source="source"
    :project-id="projectId || ''"
    :case-id="caseId || ''"
    :disabled="disabled"
    @close="fastOpen = false"
    @apply="apply"
  />
</template>
<script setup lang="ts">
import { computed, ref, watch, onUnmounted } from "vue";
import { VueDraggable } from "vue-draggable-plus";
import {
  extractionApi,
  type ExtractionResponse,
} from "@/api/nativeExtractions";
import {
  clone,
  readProcessors,
  newExtractor,
  newProcessor,
  extractModes,
  extractScopes,
  type ExtractProcessor,
  type Extractor,
} from "./nativeExtractions";
import NativeExtractorSettings from "./NativeExtractorSettings.vue";
import NativeFastExtractionDrawer from "./NativeFastExtractionDrawer.vue";
const props = defineProps<{
  modelValue: string;
  projectId?: string;
  caseId?: string;
  disabled?: boolean;
}>();
const emit = defineEmits<{ "update:modelValue": [value: string] }>();
const groups = ref<ExtractProcessor[]>([]),
  selected = ref(""),
  error = ref(""),
  draft = ref<Extractor>(),
  settingOpen = ref(false),
  fastOpen = ref(false),
  source = ref<ExtractionResponse>(),
  loadingResponse = ref(false),
  responseError = ref("");
let output = "",
  generation = 0,
  active = true;
onUnmounted(() => {
  active = false;
  generation++;
});
watch(
  () => props.modelValue,
  (value) => {
    if (value === output) return;
    try {
      groups.value = readProcessors(value);
      selected.value = groups.value[0]?.id || "";
      error.value = "";
      settingOpen.value = false;
      fastOpen.value = false;
    } catch (exception) {
      console.error("加载后置提取器失败", exception);
      error.value =
        exception instanceof Error ? exception.message : "后置配置无效";
    }
  },
  { immediate: true },
);
watch(
  () => [props.projectId, props.caseId],
  () => {
    source.value = undefined;
    loadResponse();
  },
  { immediate: true },
);
const current = computed(() =>
  groups.value.find((g) => g.id === selected.value),
);
const total = computed(() =>
  groups.value.reduce((n, g) => n + g.extractors.length, 0),
);
const columns = [
  { key: "enable", width: 40 },
  { title: "变量名", key: "variableName", width: 150 },
  { title: "描述", key: "description", width: 150 },
  { title: "类型", key: "variableType", width: 150 },
  { title: "模式", key: "extractType", width: 120 },
  { title: "范围", key: "extractScope", width: 190 },
  { title: "表达式", key: "expression", width: 250 },
  { key: "operation", width: 100, fixed: "right" as const },
];
function publish() {
  if (props.disabled) return;
  output = JSON.stringify({ processors: groups.value });
  try {
    readProcessors(output);
    error.value = "";
  } catch (exception) {
    console.error("后置提取草稿未完成", exception);
    error.value =
      exception instanceof Error ? exception.message : "后置配置无效";
  }
  emit("update:modelValue", output);
}
function add() {
  if (props.disabled) return;
  const g = newProcessor();
  groups.value.push(g);
  selected.value = g.id;
  publish();
}
function groupAction(g: ExtractProcessor, action: string) {
  if (props.disabled) return;
  if (
    action === "copy" &&
    groups.value.length < 100 &&
    total.value + g.extractors.length <= 200
  ) {
    const copy = clone(g);
    copy.id = crypto.randomUUID();
    copy.extractors.forEach((r) => (r.id = crypto.randomUUID()));
    groups.value.splice(groups.value.indexOf(g) + 1, 0, copy);
    selected.value = copy.id;
  } else if (action === "delete") {
    groups.value = groups.value.filter((p) => p.id !== g.id);
    selected.value = groups.value[0]?.id || "";
  }
  publish();
}
function rowAction(row: Extractor, action: string) {
  if (props.disabled || !current.value) return;
  const rows = current.value.extractors;
  if (action === "copy" && total.value < 200)
    rows.splice(rows.indexOf(row) + 1, 0, { ...row, id: crypto.randomUUID() });
  else if (action === "delete")
    current.value.extractors = rows.filter((r) => r.id !== row.id);
  publish();
}
function settings(row: Extractor) {
  draft.value = clone(row);
  settingOpen.value = true;
}
function openFast(row: Extractor) {
  if (props.disabled || !source.value?.available) return;
  draft.value = clone(row);
  fastOpen.value = true;
}
function apply(row: Extractor) {
  if (props.disabled || !current.value) return;
  const index = current.value.extractors.findIndex((r) => r.id === row.id);
  if (index < 0) return;
  current.value.extractors[index] = clone(row);
  settingOpen.value = false;
  fastOpen.value = false;
  publish();
}
async function loadResponse() {
  const ticket = ++generation;
  const project = props.projectId,
    id = props.caseId;
  if (!project || !id) return;
  loadingResponse.value = true;
  responseError.value = "";
  try {
    const result = await extractionApi.response(project, id);
    if (active && ticket === generation) source.value = result;
  } catch (exception) {
    console.error("读取提取器历史响应失败", exception);
    if (active && ticket === generation) {
      source.value = undefined;
      responseError.value =
        exception instanceof Error ? exception.message : "读取响应失败";
    }
  } finally {
    if (active && ticket === generation) loadingResponse.value = false;
  }
}
</script>
<style scoped>
.hint {
  color: #86909c;
  font-size: 12px;
  margin: 12px 0;
}
.post-layout {
  display: flex;
  gap: 16px;
  margin-top: 16px;
}
.post-nav {
  width: 200px;
  flex-shrink: 0;
}
.post-item {
  display: flex;
  gap: 6px;
  align-items: center;
  padding: 8px;
  border: 1px solid #e5e6eb;
}
.post-item.active {
  background: #e8f3ff;
}
.post-item .processor-select {
  border: 0;
  background: none;
  text-align: left;
  min-width: 0;
  flex: 1;
  overflow-wrap: anywhere;
  cursor: pointer;
}
.drag-handle {
  cursor: grab;
  color: #86909c;
}
.post-content {
  min-width: 0;
  flex: 1;
}
.processor-name {
  max-width: 320px;
  margin-bottom: 12px;
}
.add-row {
  margin-top: 12px;
}
@media (max-width: 700px) {
  .post-layout {
    flex-direction: column;
  }
  .post-nav {
    width: 100%;
  }
}
</style>
