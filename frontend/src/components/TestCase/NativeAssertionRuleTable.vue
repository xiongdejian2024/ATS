<template>
  <div class="assertion-rules-scroll">
    <table class="assertion-rules" :class="{ matching }">
      <thead>
        <tr>
          <th aria-label="排序"></th>
          <th aria-label="启用">
            <a-checkbox
              v-if="mode === 'VARIABLE'"
              :checked="allEnabled"
              :indeterminate="partEnabled"
              :disabled="disabled || !rows.some(filled)"
              aria-label="变量断言启用全部"
              @change="toggleAll($event.target.checked)"
            />
          </th>
          <th>
            {{
              mode === "VARIABLE"
                ? "变量名"
                : mode === "HEADER"
                  ? "响应头"
                  : "表达式"
            }}
          </th>
          <th v-if="matching">匹配条件</th>
          <th v-if="matching">匹配值</th>
          <th></th>
        </tr>
      </thead>
      <VueDraggable
        v-model="rows"
        tag="tbody"
        handle=".rule-drag"
        :disabled="disabled"
        :animation="150"
        @end="publish"
      >
        <tr v-for="(row, index) in rows" :key="row.uid">
          <td>
            <HolderOutlined
              v-if="index < rows.length - 1 && !disabled"
              class="rule-drag"
              :aria-label="`${mode}拖动断言行${index + 1}`"
            />
          </td>
          <td>
            <a-checkbox
              v-model:checked="row.enable"
              :disabled="disabled"
              :aria-label="`${mode}启用断言行${index + 1}`"
              @change="publish"
            />
          </td>
          <td>
            <a-auto-complete
              v-if="mode === 'HEADER'"
              v-model:value="row.header"
              :options="headerNames"
              :disabled="disabled"
              style="width: 100%"
              :aria-label="`响应头断言名称${index + 1}`"
              @change="publish"
            /><a-input
              v-else-if="mode === 'VARIABLE'"
              v-model:value="row.variableName"
              :disabled="disabled"
              :maxlength="255"
              placeholder="请输入变量名"
              :aria-label="`变量断言名称${index + 1}`"
              @change="publish"
            /><a-input
              v-else
              v-model:value="row.expression"
              :disabled="disabled"
              :maxlength="255"
              placeholder="请输入"
              :aria-label="`${mode}断言表达式${index + 1}`"
              @change="publish"
            />
          </td>
          <td v-if="matching">
            <a-select
              v-model:value="row.condition"
              :disabled="disabled"
              :options="mode === 'HEADER' ? headerConditions : conditions"
              :aria-label="`${mode}断言匹配条件${index + 1}`"
              @change="changeCondition(row)"
            />
          </td>
          <td v-if="matching">
            <a-input
              v-model:value="row.expectedValue"
              :disabled="
                disabled ||
                ['UNCHECK', 'EMPTY', 'NOT_EMPTY'].includes(row.condition || '')
              "
              :maxlength="20000"
              :aria-label="`${mode}断言匹配值${index + 1}`"
              @change="publish"
            />
          </td>
          <td>
            <a-space v-if="index < rows.length - 1 && !disabled" :size="0"
              ><a-dropdown v-if="mode !== 'HEADER'" :trigger="['click']"
                ><a-button
                  type="text"
                  :aria-label="`${mode}断言行更多${index + 1}`"
                  ><MoreOutlined /></a-button
                ><template #overlay
                  ><a-menu @click="copy(index)"
                    ><a-menu-item key="copy">复制</a-menu-item></a-menu
                  ></template
                ></a-dropdown
              ><a-button
                type="text"
                :aria-label="`${mode}删除断言行${index + 1}`"
                @click="remove(index)"
                ><DeleteOutlined /></a-button
            ></a-space>
          </td>
        </tr>
      </VueDraggable>
    </table>
  </div>
</template>
<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { VueDraggable } from "vue-draggable-plus";
import {
  HolderOutlined,
  DeleteOutlined,
  MoreOutlined,
} from "@ant-design/icons-vue";
import {
  blankRule,
  conditions,
  matchConditions,
  headerNames,
  type AssertionRule,
  type RuleMode,
} from "./nativeResponseAssertions";
const props = defineProps<{
  modelValue: AssertionRule[];
  mode: RuleMode;
  disabled?: boolean;
}>();
const emit = defineEmits<{ "update:modelValue": [value: AssertionRule[]] }>();
const matching = computed(
  () =>
    props.mode === "HEADER" ||
    props.mode === "JSON_PATH" ||
    props.mode === "VARIABLE",
);
const headerConditions = matchConditions.map(
  (value) => conditions.find((c) => c.value === value)!,
);
type Row = AssertionRule & { uid: number };
const rows = ref<Row[]>([]);
const allEnabled = computed(() => {
  const current = rows.value.filter(filled);
  return current.length > 0 && current.every((r) => r.enable);
});
const partEnabled = computed(
  () => !allEnabled.value && rows.value.some((r) => filled(r) && r.enable),
);
let identity = 0,
  output = "",
  outputMode = props.mode;
const row = (value: AssertionRule): Row => ({ ...value, uid: ++identity });
watch(
  () => [JSON.stringify(props.modelValue), props.mode],
  () => {
    const value = JSON.stringify(props.modelValue);
    if (value === output && props.mode === outputMode) return;
    outputMode = props.mode;
    rows.value = [...props.modelValue.map(row), row(blankRule(props.mode))];
  },
  { immediate: true },
);
function filled(r: AssertionRule) {
  return !!(r.variableName || r.header || r.expression || r.expectedValue);
}
function publish() {
  if (props.disabled) return;
  if (!rows.value.length || filled(rows.value.at(-1)!))
    rows.value.push(row(blankRule(props.mode)));
  const value = rows.value.filter(filled).map(({ uid, ...r }) => r);
  output = JSON.stringify(value);
  emit("update:modelValue", value);
}
function changeCondition(r: AssertionRule) {
  if (["UNCHECK", "EMPTY", "NOT_EMPTY"].includes(r.condition || ""))
    r.expectedValue = "";
  publish();
}
function toggleAll(enabled: boolean) {
  if (props.disabled) return;
  rows.value.filter(filled).forEach((r) => (r.enable = enabled));
  publish();
}
function remove(index: number) {
  rows.value.splice(index, 1);
  publish();
}
function copy(index: number) {
  rows.value.splice(
    index + 1,
    0,
    row(structuredClone({ ...rows.value[index] })),
  );
  publish();
}
</script>
<style scoped>
.assertion-rules-scroll {
  overflow-x: auto;
  max-width: 100%;
}
.assertion-rules {
  width: 100%;
  min-width: 440px;
  table-layout: fixed;
  border-collapse: collapse;
}
.assertion-rules.matching {
  min-width: 660px;
}
th {
  padding: 10px 6px;
  text-align: left;
  background: #f7f8fa;
  font-weight: 500;
}
td {
  padding: 6px;
  border-bottom: 1px solid #e5e6eb;
}
th:first-child {
  width: 28px;
}
th:nth-child(2) {
  width: 30px;
}
th:last-child {
  width: 72px;
}
.matching th:nth-child(4) {
  width: 150px;
}
.rule-drag {
  cursor: grab;
  color: #86909c;
}
:deep(.ant-select) {
  width: 100%;
}
</style>
