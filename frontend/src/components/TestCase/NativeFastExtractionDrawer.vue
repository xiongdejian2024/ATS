<template>
  <a-drawer
    :open="open"
    title="快速提取"
    width="min(720px, 100vw)"
    @close="emit('close')"
  >
    <a-alert type="info" :message="`历史实际响应 · ${source.executionId}`" />
    <div class="response-picker">
      <a-tree
        v-if="paths.length"
        :tree-data="paths"
        default-expand-all
        @select="selectPath"
      />
      <pre v-else>{{ responseText }}</pre>
    </div>
    <a-alert v-if="pathError" type="warning" :message="pathError" />
    <a-form layout="vertical">
      <a-form-item
        :label="
          draft.extractType === 'REGEX'
            ? '正则表达式'
            : draft.extractType === 'JSON_PATH'
              ? 'JSONPath'
              : 'XPath'
        "
        required
      >
        <a-space-compact class="expression-input"
          ><a-input
            v-model:value="draft.expression"
            :maxlength="200"
            :disabled="disabled"
            aria-label="快速提取表达式"
          /><a-button
            :disabled="!draft.expression.trim() || busy"
            :loading="busy"
            @click="test"
            >测试</a-button
          ></a-space-compact
        >
      </a-form-item>
      <div class="match-results">
        <strong>匹配结果</strong>
        <pre>{{
          tested
            ? values.length
              ? values.join("\n")
              : "未匹配到结果"
            : "请测试表达式"
        }}</pre>
      </div>
      <a-collapse :bordered="false"
        ><a-collapse-panel key="setting" header="更多设置"
          ><NativeExtractorSettings
            v-model="draft"
            :disabled="disabled" /></a-collapse-panel
      ></a-collapse>
    </a-form>
    <a-alert v-if="error" type="error" :message="error" />
    <template #footer
      ><a-space
        ><a-button :disabled="false" @click="emit('close')">取消</a-button
        ><a-button
          v-if="!disabled"
          type="primary"
          :disabled="!draft.expression.trim() || busy"
          @click="emit('apply', draft)"
          >应用</a-button
        ></a-space
      ></template
    >
  </a-drawer>
</template>
<script setup lang="ts">
import { ref, watch, onUnmounted } from "vue";
import {
  extractionApi,
  type ExtractionResponse,
} from "@/api/nativeExtractions";
import { decodeBody } from "@/api/nativeHttpReport";
import {
  clone,
  jsonPaths,
  xmlPaths,
  type PathNode,
  type Extractor,
} from "./nativeExtractions";
import NativeExtractorSettings from "./NativeExtractorSettings.vue";
const props = defineProps<{
  open: boolean;
  rule: Extractor;
  source: ExtractionResponse;
  projectId: string;
  caseId: string;
  disabled?: boolean;
}>();
const emit = defineEmits<{ close: []; apply: [value: Extractor] }>();
const draft = ref<Extractor>(clone(props.rule)),
  responseText = ref(""),
  paths = ref<PathNode[]>([]),
  pathError = ref(""),
  error = ref(""),
  busy = ref(false),
  values = ref<string[]>([]),
  tested = ref(false);
let generation = 0,
  active = true;
onUnmounted(() => {
  active = false;
  generation++;
});
watch(
  () => [props.open, props.rule, props.source],
  () => {
    generation++;
    busy.value = false;
    error.value = "";
    tested.value = false;
    values.value = [];
    draft.value = clone(props.rule);
    paths.value = [];
    pathError.value = "";
    if (!props.open || !props.source.response?.response) return;
    try {
      responseText.value = decodeBody(props.source.response.response.body);
      paths.value =
        draft.value.extractType === "JSON_PATH"
          ? jsonPaths(responseText.value)
          : draft.value.extractType === "X_PATH"
            ? xmlPaths(responseText.value, draft.value.responseFormat)
            : [];
    } catch (exception) {
      console.error("构建快速提取响应路径失败", exception);
      pathError.value =
        exception instanceof Error ? exception.message : "响应路径无法解析";
    }
  },
  { immediate: true },
);
watch(
  () => JSON.stringify(draft.value),
  () => {
    generation++;
    busy.value = false;
    tested.value = false;
    values.value = [];
    error.value = "";
  },
);
function selectPath(keys: (string | number)[]) {
  if (!props.disabled && keys.length) draft.value.expression = String(keys[0]);
}
async function test() {
  const ticket = ++generation;
  const rule = clone(draft.value),
    execution = props.source.executionId;
  if (!execution) return;
  busy.value = true;
  error.value = "";
  try {
    const result = await extractionApi.preview(
      props.projectId,
      props.caseId,
      rule,
      execution,
    );
    if (active && props.open && ticket === generation) {
      values.value = result.values;
      tested.value = true;
    }
  } catch (exception) {
    console.error("快速提取表达式测试失败", exception);
    if (active && props.open && ticket === generation)
      error.value =
        exception instanceof Error ? exception.message : "表达式测试失败";
  } finally {
    if (active && ticket === generation) busy.value = false;
  }
}
</script>
<style scoped>
.response-picker {
  margin: 16px 0;
  max-height: 336px;
  overflow: auto;
  border: 1px solid #e5e6eb;
  padding: 8px;
}
.response-picker pre,
.match-results pre {
  white-space: pre-wrap;
  word-break: break-all;
}
.expression-input {
  width: 100%;
}
.match-results {
  background: #f2f3f5;
  padding: 12px;
  margin-bottom: 16px;
  max-height: 240px;
  overflow: auto;
}
</style>
