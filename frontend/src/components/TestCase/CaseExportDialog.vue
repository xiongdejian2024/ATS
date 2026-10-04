<template>
  <a-modal
    :open="open"
    title="导出用例"
    :confirm-loading="busy"
    @ok="submit"
    @cancel="emit('update:open', false)"
  >
    <a-form layout="vertical"
      ><a-form-item label="导出格式"
        ><a-radio-group v-model:value="format"
          ><a-radio value="xlsx">Excel</a-radio
          ><a-radio value="xmind">XMind</a-radio></a-radio-group
        ></a-form-item
      ><a-alert
        :message="
          selectedCount
            ? `导出勾选的 ${selectedCount} 条用例。`
            : '导出当前模块、搜索与组合筛选匹配的全部用例。'
        "
        type="info"
        show-icon
      />
      <template v-if="format === 'xlsx'"
        ><a-form-item label="布局" style="margin-top: 16px"
          ><a-radio-group v-model:value="layout"
            ><a-radio value="case">一行一条用例</a-radio
            ><a-radio value="step">一行一个步骤</a-radio></a-radio-group
          ></a-form-item
        ><a-form-item label="导出字段"
          ><a-checkbox-group
            v-model:value="fields"
            :options="fieldOptions"
            class="export-fields" /></a-form-item
      ></template>
    </a-form>
  </a-modal>
</template>
<script setup lang="ts">
import { ref, watch } from "vue";
import { message } from "ant-design-vue";
const props = defineProps<{
    open: boolean;
    initialFormat: string;
    selectedCount: number;
    busy: boolean;
  }>(),
  emit = defineEmits<{
    "update:open": [value: boolean];
    export: [options: { format: string; layout: string; fields: string }];
  }>();
const format = ref("xlsx"),
  layout = ref("case"),
  fields = ref<string[]>([
    "caseCode",
    "name",
    "priority",
    "type",
    "precondition",
    "steps",
    "requirementRef",
    "tags",
    "modulePath",
    "templateId",
    "customFields",
  ]);
const fieldOptions = [
  ["caseCode", "编号"],
  ["name", "名称"],
  ["priority", "优先级"],
  ["type", "类型"],
  ["reviewResult", "评审结果"],
  ["status", "执行结果"],
  ["modulePath", "模块"],
  ["tags", "标签"],
  ["isAutomated", "自动化"],
  ["createdBy", "创建人"],
  ["createdAt", "创建时间"],
  ["updatedBy", "更新人"],
  ["updatedAt", "更新时间"],
  ["precondition", "前置条件"],
  ["steps", "步骤与预期"],
  ["requirementRef", "需求引用"],
  ["templateId", "模板"],
  ["customFields", "自定义字段"],
].map(([value, label]) => ({ value, label }));
function submit() {
  if (format.value === "xlsx" && !fields.value.length)
    return message.warning("请至少选择一个字段");
  emit("export", {
    format: format.value,
    layout: layout.value,
    fields: fields.value.join(","),
  });
}
watch(
  () => props.open,
  (open) => {
    if (open) format.value = props.initialFormat === "xmind" ? "xmind" : "xlsx";
  },
);
</script>
<style scoped>
.export-fields {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}
@media (max-width: 600px) {
  .export-fields {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>
