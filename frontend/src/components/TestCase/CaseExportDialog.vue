<template>
  <a-modal
    :open="open"
    title="导出用例"
    :confirm-loading="busy"
    :closable="!busy"
    :mask-closable="!busy"
    :keyboard="!busy"
    :cancel-button-props="{ disabled: busy }"
    :ok-button-props="{ disabled: busy }"
    @ok="submit"
    @cancel="!busy && emit('update:open', false)"
  >
    <a-form layout="vertical"
      ><a-form-item label="导出格式"
        ><a-radio-group v-model:value="format" :disabled="busy"
          ><a-radio value="xlsx">Excel</a-radio
          ><a-radio value="xmind">XMind</a-radio></a-radio-group
        ></a-form-item
      ><a-alert
        :message="
          selectedCount
            ? `导出勾选的 ${selectedCount} 条用例。`
            : '导出当前检索范围匹配的全部用例。'
        "
        type="info"
        show-icon
      />
      <template v-if="format === 'xlsx'"
        ><a-form-item label="布局" style="margin-top: 16px"
          ><a-radio-group v-model:value="layout" :disabled="busy"
            ><a-radio value="case">一行一条用例</a-radio
            ><a-radio value="step">一行一个步骤</a-radio></a-radio-group
          ></a-form-item
        ></template
      >
      <a-form-item
        v-for="group in groups"
        :key="group.key"
        :label="group.label"
      >
        <a-checkbox-group
          :value="fields"
          :disabled="busy"
          :options="group.options"
          class="export-fields"
          @update:value="
            (value: any[]) =>
              selectGroup(
                group.options.map((o) => o.value),
                value.map(String),
              )
          "
        />
      </a-form-item>
      <p v-if="format === 'xmind'">
        XMind
        名称为必选。取消编号后再次导入会作为新用例；未选择字段不会写入隐藏属性。
      </p>
    </a-form>
  </a-modal>
</template>
<script setup lang="ts">
import { ref, watch, computed } from "vue";
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
    "caseEditType",
    "textDescription",
    "expectedResult",
    "description",
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
  ["caseEditType", "描述方式"],
  ["textDescription", "文本描述"],
  ["expectedResult", "文本预期结果"],
  ["description", "备注"],
  ["requirementRef", "需求引用"],
  ["templateId", "模板"],
  ["customFields", "自定义字段"],
].map(([value, label]) => ({ value, label }));
const xmindFields = new Set([
  "caseCode",
  "name",
  "priority",
  "type",
  "modulePath",
  "tags",
  "isAutomated",
  "precondition",
  "steps",
  "caseEditType",
  "textDescription",
  "expectedResult",
  "description",
  "requirementRef",
  "templateId",
  "customFields",
]);
const groups = computed(() =>
  [
    {
      key: "basic",
      label: "基本信息",
      keys: [
        "caseCode",
        "name",
        "priority",
        "type",
        "modulePath",
        "tags",
        "isAutomated",
        "reviewResult",
        "status",
      ],
    },
    {
      key: "content",
      label: "用例内容",
      keys: [
        "precondition",
        "steps",
        "caseEditType",
        "textDescription",
        "expectedResult",
        "description",
        "requirementRef",
      ],
    },
    {
      key: "metadata",
      label: "模板与记录信息",
      keys: [
        "templateId",
        "customFields",
        "createdBy",
        "createdAt",
        "updatedBy",
        "updatedAt",
      ],
    },
  ].map((group) => ({
    ...group,
    options: fieldOptions
      .filter(
        (o) =>
          group.keys.includes(o.value) &&
          (format.value === "xlsx" || xmindFields.has(o.value)),
      )
      .map((o) => ({
        ...o,
        disabled: format.value === "xmind" && o.value === "name",
      })),
  })),
);
function selectGroup(keys: string[], selected: string[]) {
  fields.value = [
    ...fields.value.filter((key) => !keys.includes(key)),
    ...selected,
  ];
  if (format.value === "xmind" && !fields.value.includes("name"))
    fields.value.push("name");
}
function submit() {
  if (props.busy) return;
  const selected = fields.value.filter(
    (key) => format.value === "xlsx" || xmindFields.has(key),
  );
  if (!selected.length) return message.warning("请至少选择一个字段");
  if (format.value === "xmind" && !selected.includes("name"))
    return message.warning("XMind须包含用例名称");
  emit("export", {
    format: format.value,
    layout: layout.value,
    fields: selected.join(","),
  });
}
watch(
  () => props.open,
  (open) => {
    if (open) format.value = props.initialFormat === "xmind" ? "xmind" : "xlsx";
  },
  { immediate: true },
);
watch(format, (value) => {
  if (value === "xmind" && !fields.value.includes("name"))
    fields.value.push("name");
});
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
