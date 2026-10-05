<template>
  <a-drawer
    :open="visible"
    width="min(600px, 100vw)"
    :mask="false"
    :closable="!saving"
    :keyboard="!saving"
    placement="right"
    class="advanced-filter-drawer"
    @close="close"
  >
    <template #title
      ><a-input
        v-if="newView || editingName"
        v-model:value="draftName"
        placeholder="请输入视图名称"
        :maxlength="255"
        :disabled="saving"
        aria-label="视图名称" /><a-space v-else
        ><span>{{ view?.name || "全部数据" }}</span
        ><a-button
          v-if="view?.id"
          type="text"
          aria-label="修改视图名称"
          :disabled="saving"
          @click="editingName = true"
          ><EditOutlined /></a-button></a-space
    ></template>
    <a-alert
      message="筛选条件支持系统字段及自定义字段。"
      type="info"
      closable
      class="filter-tip"
    />
    <a-select
      v-model:value="draftLogic"
      :disabled="saving"
      aria-label="组合条件逻辑"
      class="filter-logic"
      :options="[
        { label: '符合以下所有条件', value: 'and' },
        { label: '符合以下任一条件', value: 'or' },
      ]"
    />
    <div v-for="(condition, index) in draft" :key="index" class="filter-row">
      <a-select
        v-model:value="condition.field"
        :disabled="saving"
        :aria-label="`条件${index + 1}字段`"
        show-search
        option-filter-prop="label"
        placeholder="选择字段"
        :options="fieldOptions(index)"
        @change="fieldChanged(index)"
      />
      <a-select
        v-model:value="condition.operator"
        :disabled="saving || !condition.field"
        :aria-label="`条件${index + 1}运算符`"
        :options="operatorsFor(field(condition.field), condition.operator)"
        @change="condition.value = undefined"
      />
      <a-tree-select
        v-if="field(condition.field)?.type === 'module'"
        :value="
          selectionValues(condition.value).map((value: string) => ({ value }))
        "
        :disabled="disabledValue(condition)"
        :aria-label="`条件${index + 1}值`"
        :tree-data="moduleOptions"
        :field-names="{ value: 'key', label: 'title', children: 'children' }"
        tree-checkable
        tree-check-strictly
        label-in-value
        show-search
        tree-node-filter-prop="title"
        placeholder="请选择"
        allow-clear
        @change="normalizeModules(index, $event)"
      />
      <a-input-number
        v-else-if="
          field(condition.field)?.type === 'number' ||
          ['count_gt', 'count_lt'].includes(condition.operator)
        "
        v-model:value="condition.value"
        :disabled="disabledValue(condition)"
        :min="condition.operator.startsWith('count_') ? 0 : undefined"
        :precision="condition.operator.startsWith('count_') ? 0 : undefined"
        :aria-label="`条件${index + 1}值`"
        placeholder="请输入"
      />
      <a-range-picker
        v-else-if="
          field(condition.field)?.type === 'date' &&
          condition.operator === 'between'
        "
        v-model:value="condition.value"
        :disabled="disabledValue(condition)"
        show-time
        value-format="YYYY-MM-DDTHH:mm:ss.SSSZ"
        :placeholder="['开始时间', '结束时间']"
      />
      <a-date-picker
        v-else-if="field(condition.field)?.type === 'date'"
        v-model:value="condition.value"
        :disabled="disabledValue(condition)"
        show-time
        value-format="YYYY-MM-DDTHH:mm:ss.SSSZ"
        placeholder="请选择时间"
      />
      <a-select
        v-else-if="
          ['select', 'tags'].includes(field(condition.field)?.type || '')
        "
        v-model:value="condition.value"
        :disabled="disabledValue(condition)"
        :aria-label="`条件${index + 1}值`"
        :mode="
          field(condition.field)?.type === 'tags'
            ? 'tags'
            : collectionValue(condition.operator)
              ? 'multiple'
              : undefined
        "
        :options="field(condition.field)?.options || []"
        placeholder="请选择"
        allow-clear
      />
      <a-input
        v-else
        v-model:value="condition.value"
        :disabled="disabledValue(condition)"
        :aria-label="`条件${index + 1}值`"
        placeholder="请输入"
        :maxlength="255"
        allow-clear
      />
      <a-button
        :disabled="saving"
        :aria-label="`删除条件${index + 1}`"
        @click="draft.splice(index, 1)"
        ><MinusCircleOutlined
      /></a-button>
    </div>
    <a-button
      type="text"
      :disabled="saving || draft.length >= availableFields.length"
      @click="draft.push({ field: '', operator: '', value: undefined })"
      ><PlusOutlined />添加条件</a-button
    >
    <a-alert
      v-if="error"
      :message="error"
      type="error"
      show-icon
      class="filter-error"
    />
    <template #footer>
      <a-space v-if="copyMode" wrap
        ><a-input
          v-model:value="copyName"
          placeholder="请输入新视图名称"
          :maxlength="255"
          :disabled="saving"
          aria-label="另存视图名称"
        /><a-button
          aria-label="保存视图副本"
          type="primary"
          :loading="saving"
          @click="save('copy')"
          >保存</a-button
        ><a-button
          :disabled="saving"
          @click="
            copyMode = false;
            copyName = '';
          "
          >取消</a-button
        ></a-space
      >
      <a-space v-else wrap
        ><a-button
          type="primary"
          :disabled="saving"
          :loading="saving && newView"
          :aria-label="newView ? '保存新视图并筛选' : '应用高级筛选'"
          @click="newView ? save('create') : apply()"
          >{{ newView ? "保存并筛选" : "筛选" }}</a-button
        ><a-button aria-label="重置筛选草稿" :disabled="saving" @click="reset"
          >重置</a-button
        ><a-button
          v-if="view?.id && !newView"
          aria-label="保存当前视图"
          type="text"
          :loading="saving"
          @click="save('update')"
          >保存</a-button
        ><a-button
          v-if="!newView && saveView"
          aria-label="另存为视图"
          type="text"
          :disabled="saving || cannotAdd"
          @click="
            copyMode = true;
            copyName = '';
          "
          >另存为视图</a-button
        ></a-space
      >
    </template>
  </a-drawer>
</template>
<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { cloneDeep } from "lodash-es";
import {
  EditOutlined,
  MinusCircleOutlined,
  PlusOutlined,
} from "@ant-design/icons-vue";
import {
  operatorsFor,
  noValue,
  collectionValue,
  initialConditions,
  effectiveConditions,
  nextUnnamedView,
  selectionValues,
  type FilterCondition,
  type FilterField,
  type FilterLogic,
  type ViewSaveMode,
} from "./advancedFilter";
const props = withDefaults(
  defineProps<{
    visible: boolean;
    availableFields: FilterField[];
    moduleTreeData?: any[];
    conditions?: FilterCondition[];
    logic?: FilterLogic;
    view?: { id: string; name: string; filters: Record<string, any> };
    viewNames?: string[];
    newView?: boolean;
    cannotAdd?: boolean;
    saveView?: (
      name: string,
      conditions: FilterCondition[],
      logic: FilterLogic,
      mode: ViewSaveMode,
    ) => Promise<void>;
  }>(),
  {
    moduleTreeData: () => [],
    conditions: () => [],
    logic: "and",
    viewNames: () => [],
    newView: false,
    cannotAdd: false,
  },
);
const emit = defineEmits<{
  "update:visible": [value: boolean];
  apply: [conditions: FilterCondition[], logic: FilterLogic];
  saving: [value: boolean];
}>();
const draft = ref<FilterCondition[]>([]),
  draftLogic = ref<FilterLogic>("and"),
  draftName = ref(""),
  editingName = ref(false),
  copyMode = ref(false),
  copyName = ref(""),
  saving = ref(false),
  error = ref("");
let original: FilterCondition[] = [],
  originalLogic: FilterLogic = "and",
  originalName = "";
const field = (key: string) => props.availableFields.find((f) => f.key === key);
const disabledValue = (c: FilterCondition) =>
  saving.value || !c.field || noValue(c.operator);
function fieldOptions(index: number) {
  return props.availableFields
    .filter((f) =>
      draft.value.every((c, i) => i === index || c.field !== f.key),
    )
    .map((f) => ({ value: f.key, label: f.label }));
}
function onlyModules(nodes: any[]): any[] {
  return nodes
    .filter((n) => n.nodeType === "module")
    .map((n) => ({ ...n, children: onlyModules(n.children || []) }));
}
const moduleOptions = computed(() => onlyModules(props.moduleTreeData));
function normalizeModules(index: number, value: any) {
  draft.value[index].value = (Array.isArray(value) ? value : [value])
    .filter((v) => v !== undefined && v !== null)
    .map((v) => (typeof v === "object" ? v.value : v));
}
function fieldChanged(index: number) {
  const c = draft.value[index];
  c.operator = operatorsFor(field(c.field))[0]?.value || "";
  c.value = undefined;
}
function reset() {
  draft.value = cloneDeep(original);
  draftLogic.value = originalLogic;
  draftName.value = originalName;
  editingName.value = props.newView;
  error.value = "";
}
function validate() {
  error.value = "";
  if (
    draft.value.some(
      (c) =>
        !field(c.field) ||
        !operatorsFor(field(c.field), c.operator).some(
          (op) => op.value === c.operator,
        ),
    )
  ) {
    error.value = "请选择完整的字段和运算符";
    return false;
  }
  return true;
}
function apply() {
  if (saving.value || !validate()) return;
  emit("apply", effectiveConditions(draft.value), draftLogic.value);
  emit("update:visible", false);
}
async function save(mode: ViewSaveMode) {
  if (saving.value || !props.saveView || !validate()) return;
  const name = (mode === "copy" ? copyName.value : draftName.value).trim();
  if (!name || name.length > 255) {
    error.value = "请填写1至255字符的视图名称";
    return;
  }
  if (
    props.viewNames.includes(name) &&
    (mode !== "update" || name !== props.view?.name)
  ) {
    error.value = "视图名称已存在";
    return;
  }
  if (mode !== "update" && props.cannotAdd) {
    error.value = "最多创建10个个人视图";
    return;
  }
  saving.value = true;
  emit("saving", true);
  try {
    await props.saveView(
      name,
      effectiveConditions(draft.value),
      draftLogic.value,
      mode,
    );
    if (mode === "copy") {
      copyMode.value = false;
      copyName.value = "";
    } else {
      original = cloneDeep(draft.value);
      originalLogic = draftLogic.value;
      originalName = name;
      editingName.value = false;
    }
    if (mode === "create") {
      emit("apply", effectiveConditions(draft.value), draftLogic.value);
      emit("update:visible", false);
    }
  } catch (failure) {
    console.error("保存筛选视图失败，保留条件及名称草稿", failure);
    error.value = "保存视图失败，请保留草稿并重试";
  } finally {
    saving.value = false;
    emit("saving", false);
  }
}
function close() {
  if (!saving.value) emit("update:visible", false);
}
watch(
  () => props.visible,
  (visible) => {
    if (visible) {
      const saved = props.newView ? undefined : props.view?.filters;
      original = props.newView
        ? [{ field: "", operator: "", value: undefined }]
        : initialConditions(props.availableFields, saved?.filterConditions);
      originalLogic = saved?.filterLogic === "or" ? "or" : "and";
      originalName = props.newView
        ? nextUnnamedView(props.viewNames)
        : props.view?.name || "全部数据";
      copyMode.value = false;
      copyName.value = "";
      reset();
      if (!saved && !props.newView && props.conditions.length) {
        draft.value = cloneDeep(props.conditions);
        draftLogic.value = props.logic;
      }
    }
  },
);
defineExpose({ isSaving: () => saving.value });
</script>
<style scoped>
.filter-tip {
  margin-bottom: 12px;
}
.filter-logic {
  width: 190px;
  margin-bottom: 12px;
}
.filter-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 105px minmax(0, 1.5fr) 32px;
  align-items: start;
  gap: 8px;
  margin-bottom: 16px;
}
.filter-row :deep(.ant-picker),
.filter-row :deep(.ant-input-number) {
  width: 100%;
  min-width: 0;
}
.filter-error {
  margin-top: 12px;
}
.advanced-filter-drawer :deep(.ant-drawer-content-wrapper) {
  max-width: 100vw;
}
.advanced-filter-drawer :deep(.ant-drawer-body) {
  padding: 16px 24px;
}
@media (max-width: 600px) {
  .filter-row {
    grid-template-columns: minmax(0, 1fr) 105px 32px;
  }
  .filter-row > :nth-child(3) {
    grid-column: 1 / 3;
    grid-row: 2;
  }
  .filter-row > :nth-child(4) {
    grid-column: 3;
    grid-row: 1;
  }
  .advanced-filter-drawer :deep(.ant-drawer-header) {
    padding: 12px;
  }
  .advanced-filter-drawer :deep(.ant-drawer-body) {
    padding: 12px;
  }
}
</style>
