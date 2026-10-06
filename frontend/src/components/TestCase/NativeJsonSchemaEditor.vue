<template>
  <div class="native-json-schema">
    <div class="schema-toolbar">
      <a-space wrap
        ><a-button v-if="!disabled" :disabled="busy" @click="openBatch"
          >批量添加</a-button
        ><span>JSON Schema</span></a-space
      >
      <a-space wrap
        ><a-button :loading="busy" @click="preview">预览</a-button
        ><a-popover trigger="click" placement="bottomRight"
          ><template #content
            ><a-checkbox-group
              v-model:value="visibleFields"
              :options="optionalFields"
              aria-label="Schema显示列" /></template
          ><a-button aria-label="Schema列设置">列设置</a-button></a-popover
        ></a-space
      >
    </div>
    <a-alert v-if="error" :message="error" type="error" show-icon />
    <a-table
      :data-source="[root]"
      :columns="columns"
      row-key="id"
      :pagination="false"
      :scroll="{ x: tableWidth }"
      :expanded-row-keys="expanded"
      size="small"
      @expand="expand"
    >
      <template #headerCell="{ column }"
        ><a-checkbox
          v-if="column.key === 'enable'"
          :checked="allEnabled"
          :disabled="disabled"
          aria-label="启用全部Schema节点"
          @change="selectAll($event.target.checked)"
      /></template>
      <template #bodyCell="{ column, record }">
        <a-checkbox
          v-if="column.key === 'enable'"
          :checked="record.enable !== false"
          :disabled="disabled"
          :aria-label="`启用Schema节点 ${record.title}`"
          @change="select(record, $event.target.checked)"
        />
        <template v-else-if="column.key === 'title'"
          ><span v-if="record.id === 'root' || isArrayChild(record)">{{
            record.id === "root" ? "root" : record.title
          }}</span
          ><a-input
            v-else
            v-model:value="record.title"
            :maxlength="255"
            :disabled="disabled"
            :aria-label="`Schema属性名称 ${record.title}`"
            @change="nameChanged(record)"
        /></template>
        <template v-else-if="column.key === 'type'"
          ><div class="schema-type">
            <a-button
              v-if="record.id !== 'root'"
              type="text"
              size="small"
              :disabled="disabled"
              :aria-label="`Schema必填 ${record.title}`"
              :title="record.required ? '必填' : '非必填'"
              :class="{ required: record.required }"
              @click="
                record.required = !record.required;
                changed();
              "
              >*</a-button
            ><a-select
              v-model:value="record.type"
              :disabled="disabled"
              :options="
                (record.id === 'root' ? ['object', 'array'] : schemaTypes).map(
                  (value) => ({ value, label: value }),
                )
              "
              :aria-label="`Schema类型 ${record.title}`"
              @change="typeChanged(record)"
            /></div
        ></template>
        <template v-else-if="column.key === 'example'"
          ><div
            v-if="!['object', 'array', 'null'].includes(record.type)"
            class="schema-example"
          >
            <NativeSchemaField
              :record="record"
              field="example"
              :label="`Schema示例 ${record.title}`"
              :disabled="disabled"
              @change="changed"
            /><a-button
              v-if="!disabled"
              size="small"
              :aria-label="`多行编辑示例 ${record.title}`"
              @click="
                quickRow = record;
                quickValue = record.example || '';
                quickOpen = true;
              "
              >…</a-button
            >
          </div>
          <span v-else>-</span></template
        >
        <template v-else-if="column.key === 'operation'"
          ><a-space :size="2"
            ><a-button
              type="text"
              size="small"
              :aria-label="`Schema高级设置 ${record.title}`"
              @click="
                settingRow = record;
                setting = JSON.parse(JSON.stringify(record));
                settingOpen = true;
              "
              >设置</a-button
            ><a-button
              v-if="!disabled && ['object', 'array'].includes(record.type)"
              type="text"
              size="small"
              :aria-label="`添加Schema子节点 ${record.title}`"
              @click="addChild(record)"
              >+</a-button
            ><a-button
              v-if="!disabled && record.id !== 'root'"
              type="text"
              size="small"
              :aria-label="`删除Schema节点 ${record.title}`"
              @click="remove(record)"
              >删除</a-button
            ></a-space
          ></template
        >
        <NativeSchemaField
          v-else
          :record="record"
          :field="column.key"
          :label="`${column.title} ${record.title}`"
          :disabled="disabled"
          compact
          @change="changed"
        />
      </template>
    </a-table>
    <a-drawer
      v-model:open="settingOpen"
      title="JSON Schema高级设置"
      width="min(600px, 100vw)"
      :destroy-on-close="true"
      class="schema-drawer"
    >
      <template v-if="setting"
        ><a-form layout="vertical"
          ><a-form-item label="名称" required
            ><a-input
              v-model:value="setting.title"
              :disabled="
                disabled || setting.id === 'root' || isArrayChild(settingRow!)
              "
              :maxlength="255"
              aria-label="Schema高级名称" /></a-form-item
          ><a-form-item
            v-for="field in settingsFields"
            :key="field.value"
            :label="field.label"
            ><NativeSchemaField
              :record="setting"
              :field="field.value"
              :label="`Schema高级${field.label}`"
              :disabled="disabled" /></a-form-item
        ></a-form>
        <p>节点Schema预览</p>
        <a-textarea
          :value="settingPreview"
          readonly
          :rows="12"
          aria-label="Schema节点预览"
      /></template>
      <template #footer
        ><a-space
          ><a-button @click="settingOpen = false">取消</a-button
          ><a-button v-if="!disabled" type="primary" @click="applySetting"
            >应用</a-button
          ></a-space
        ></template
      >
    </a-drawer>
    <a-modal
      v-model:open="quickOpen"
      title="编辑示例值"
      width="min(680px, calc(100vw - 32px))"
      :ok-button-props="{ disabled: !quickValue }"
      ok-text="应用"
      @ok="applyQuick"
      ><a-textarea
        v-model:value="quickValue"
        :rows="12"
        :maxlength="20000"
        aria-label="Schema多行示例"
    /></a-modal>
    <a-drawer
      v-model:open="batchOpen"
      title="批量添加"
      width="min(600px, 100vw)"
      class="schema-drawer"
      ><a-radio-group
        v-model:value="batchType"
        option-type="button"
        :options="[
          { value: 'json', label: 'Json' },
          { value: 'schema', label: 'JsonSchema' },
        ]"
        aria-label="Schema批量格式"
      /><a-textarea
        v-model:value="batchDrafts[batchType]"
        :rows="20"
        aria-label="Schema批量内容"
      /><a-alert
        v-if="batchError"
        :message="batchError"
        type="error"
        show-icon
      /><template #footer
        ><a-space
          ><a-button @click="batchOpen = false">取消</a-button
          ><a-button type="primary" :disabled="disabled" @click="applyBatch"
            >应用</a-button
          ></a-space
        ></template
      ></a-drawer
    >
    <a-drawer
      v-model:open="previewOpen"
      title="预览"
      width="min(600px, 100vw)"
      class="schema-drawer"
      @after-open-change="!$event && (previewType = 'json')"
      ><a-radio-group
        v-model:value="previewType"
        option-type="button"
        :options="[
          { value: 'json', label: 'Json' },
          { value: 'schema', label: 'JsonSchema' },
        ]"
        aria-label="Schema预览格式" /><a-spin :spinning="busy"
        ><a-textarea
          :value="previewValues[previewType]"
          readonly
          :rows="20"
          aria-label="Schema预览内容" /></a-spin
    ></a-drawer>
  </div>
</template>
<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { message } from "ant-design-vue";
import NativeSchemaField from "./NativeSchemaField.vue";
import { convertJsonSchema } from "@/api/nativeJsonSchema";
import {
  newSchemaRow,
  readJsonSchema,
  rowsToSchema,
  schemaToRows,
  jsonToSchema,
  walkSchema,
  schemaTypes,
  type SchemaRow,
} from "./nativeJsonSchema";
const props = defineProps<{
  modelValue: string;
  projectId: string;
  disabled?: boolean;
}>();
const emit = defineEmits<{ "update:modelValue": [value: string] }>();
const root = ref<SchemaRow>(schemaToRows({ type: "object", properties: {} })),
  error = ref(""),
  busy = ref(false),
  expanded = ref<string[]>(["root"]);
let output = "";
watch(
  () => props.modelValue,
  (value) => {
    if (value === output) return;
    try {
      root.value = schemaToRows(readJsonSchema(value));
      error.value = "";
      expanded.value = ["root"];
    } catch (exception) {
      console.error("加载Schema草稿失败", exception);
      error.value = "Schema草稿无效";
    }
  },
  { immediate: true },
);
const optionalFields = [
  { value: "description", label: "描述" },
  { value: "minLength", label: "最小长度" },
  { value: "maxLength", label: "最大长度" },
  { value: "minimum", label: "最小值" },
  { value: "maximum", label: "最大值" },
  { value: "minItems", label: "最小元素数" },
  { value: "maxItems", label: "最大元素数" },
  { value: "defaultValue", label: "默认值" },
  { value: "enumValues", label: "枚举" },
  { value: "pattern", label: "正则表达式" },
  { value: "format", label: "格式" },
];
const visibleFields = ref(["description"]);
const columns = computed(() => [
  { title: "", key: "enable", width: 40 },
  { title: "名称", key: "title", width: 240 },
  { title: "类型", key: "type", width: 160 },
  { title: "示例值", key: "example", width: 240 },
  ...optionalFields
    .filter((f) => visibleFields.value.includes(f.value))
    .map((f) => ({ title: f.label, key: f.value, width: 200 })),
  { title: "", key: "operation", width: 150 },
]);
const tableWidth = computed(() =>
  columns.value.reduce((n, c) => n + c.width, 0),
);
function expand(open: boolean, row: SchemaRow) {
  expanded.value = open
    ? [...expanded.value, row.id]
    : expanded.value.filter((id) => id !== row.id);
}
function parent(row: SchemaRow) {
  let result: SchemaRow | undefined;
  walkSchema(root.value, (n) => {
    if (n.children?.some((c) => c.id === row.id)) result = n;
  });
  return result;
}
function isArrayChild(row: SchemaRow) {
  return !!row && parent(row)?.type === "array";
}
function currentSchema() {
  return readJsonSchema(JSON.stringify(rowsToSchema(root.value)));
}
function changed() {
  if (props.disabled) return;
  try {
    output = JSON.stringify(currentSchema());
    error.value = "";
    emit("update:modelValue", output);
  } catch (exception) {
    console.error("Schema校验失败，保留当前树形草稿", exception);
    error.value = exception instanceof Error ? exception.message : "Schema无效";
    output = "{Schema草稿未完成";
    emit("update:modelValue", output);
  }
}
function addChild(row: SchemaRow) {
  if (props.disabled) return;
  row.children ||= [];
  row.children.push(
    newSchemaRow(row.type === "array" ? String(row.children.length) : ""),
  );
  if (!expanded.value.includes(row.id)) expanded.value.push(row.id);
  changed();
}
function nameChanged(row: SchemaRow) {
  const p = parent(row);
  if (
    row.title &&
    p?.id === "root" &&
    p.type === "object" &&
    p.children?.at(-1)?.id === row.id
  )
    addChild(p);
  else changed();
}
function typeChanged(row: SchemaRow) {
  if (["object", "array"].includes(row.type)) {
    row.children ||= [];
    if (row.type === "array")
      row.children.forEach((c, i) => (c.title = String(i)));
  } else delete row.children;
  changed();
}
function remove(row: SchemaRow) {
  const p = parent(row);
  if (!p || props.disabled) return;
  p.children = p.children?.filter((c) => c.id !== row.id);
  if (p.type === "array") p.children?.forEach((c, i) => (c.title = String(i)));
  changed();
}
const allEnabled = computed(() => {
  let yes = true;
  walkSchema(root.value, (n) => {
    if (n.enable === false) yes = false;
  });
  return yes;
});
function select(row: SchemaRow, enabled: boolean) {
  row.enable = enabled;
  if (enabled) walkSchema(row, (n) => (n.enable = true));
  changed();
}
function selectAll(enabled: boolean) {
  walkSchema(root.value, (n) => (n.enable = enabled));
  changed();
}
const settingOpen = ref(false),
  settingRow = ref<SchemaRow>(),
  setting = ref<SchemaRow>();
const settingsFields = computed(() =>
  optionalFields.filter(
    (f) =>
      f.value === "description" ||
      (setting.value?.type === "string" &&
        [
          "minLength",
          "maxLength",
          "defaultValue",
          "enumValues",
          "pattern",
          "format",
        ].includes(f.value)) ||
      (["number", "integer"].includes(setting.value?.type || "") &&
        ["minimum", "maximum", "defaultValue", "enumValues"].includes(
          f.value,
        )) ||
      (setting.value?.type === "array" &&
        ["minItems", "maxItems"].includes(f.value)) ||
      (setting.value?.type === "boolean" && f.value === "defaultValue"),
  ),
);
const settingPreview = computed(() => {
  try {
    return setting.value
      ? JSON.stringify(rowsToSchema(setting.value), null, 2)
      : "";
  } catch (exception) {
    console.error("Schema节点预览转换失败", exception);
    return "Schema节点尚未完成，请先修正属性名称";
  }
});
function applySetting() {
  const draft = setting.value,
    row = settingRow.value;
  if (!draft || !row || props.disabled) return;
  try {
    if (!draft.title.trim()) throw new Error("名称不能为空");
    const siblings = parent(row)?.children || [];
    if (siblings.some((c) => c.id !== row.id && c.title === draft.title))
      throw new Error("同层名称不能重复");
    const copied = JSON.parse(JSON.stringify(root.value));
    let target: SchemaRow | undefined;
    walkSchema(copied, (n) => {
      if (n.id === row.id) target = n;
    });
    Object.assign(target!, draft);
    readJsonSchema(JSON.stringify(rowsToSchema(copied)));
    Object.assign(row, draft);
    settingOpen.value = false;
    changed();
  } catch (exception) {
    console.error("应用Schema高级设置失败", exception);
    message.error(exception instanceof Error ? exception.message : "设置无效");
  }
}
const quickOpen = ref(false),
  quickRow = ref<SchemaRow>(),
  quickValue = ref("");
function applyQuick() {
  if (quickRow.value && !props.disabled) {
    quickRow.value.example = quickValue.value;
    changed();
  }
  quickOpen.value = false;
}
const batchOpen = ref(false),
  batchType = ref<"json" | "schema">("json"),
  batchDrafts = ref({ json: "", schema: "" }),
  batchError = ref("");
async function convert(action: "preview" | "generate") {
  if (!props.projectId) throw new Error("请先选择项目");
  const schema = currentSchema();
  return (await convertJsonSchema(props.projectId, schema, action)).jsonValue;
}
async function openBatch() {
  busy.value = true;
  try {
    batchDrafts.value.schema = JSON.stringify(currentSchema(), null, 2);
    batchDrafts.value.json = await convert("preview");
    batchError.value = "";
    batchOpen.value = true;
  } catch (exception) {
    console.error("打开Schema批量添加失败", exception);
    message.error("请先修正Schema后重试");
  } finally {
    busy.value = false;
  }
}
function applyBatch() {
  try {
    const schema =
      batchType.value === "json"
        ? jsonToSchema(batchDrafts.value.json)
        : readJsonSchema(batchDrafts.value.schema);
    root.value = schemaToRows(schema);
    expanded.value = ["root"];
    changed();
    batchOpen.value = false;
  } catch (exception) {
    console.error("批量转换Schema失败，保留原树与输入", exception);
    batchError.value =
      exception instanceof Error ? exception.message : "批量格式无效";
  }
}
const previewOpen = ref(false),
  previewType = ref<"json" | "schema">("json"),
  previewValues = ref({ json: "", schema: "" });
async function preview() {
  busy.value = true;
  try {
    previewValues.value.schema = JSON.stringify(currentSchema(), null, 2);
    previewValues.value.json = await convert("preview");
    previewOpen.value = true;
  } catch (exception) {
    console.error("预览Schema失败", exception);
    message.error("Schema预览失败，请修正配置后重试");
  } finally {
    busy.value = false;
  }
}
</script>
<style scoped>
.native-json-schema {
  margin-top: 16px;
}
.schema-toolbar {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 12px;
}
.schema-type,
.schema-example {
  display: flex;
  align-items: center;
  gap: 4px;
}
.schema-type .ant-select {
  flex: 1;
  min-width: 90px;
}
.required {
  color: #f53f3f;
}
.native-json-schema :deep(.ant-table-wrapper) {
  max-width: 100%;
}
.schema-drawer :deep(.ant-radio-group) {
  margin-bottom: 16px;
}
.native-json-schema :deep(.ant-alert) {
  margin-bottom: 12px;
}
</style>
