<template>
  <a-drawer
    :open="open"
    title="用例模板与自定义字段"
    width="min(1000px, 96vw)"
    @close="emit('update:open', false)"
  >
    <a-alert
      message="项目默认模板用于新建用例；修改模板不会自动覆盖已有用例内容。已有用例使用的模板不能删除。"
      type="info"
      show-icon
    />
    <a-card title="评审设置" size="small" style="margin-top: 16px"
      ><a-space
        ><a-switch
          v-model:checked="autoResubmit"
          :loading="busy"
          @change="saveSettings"
        /><span>用例内容变更时自动重新提审</span></a-space
      >
      <p style="color: #667085; margin: 8px 0 0">
        启用后生成新评审轮次，旧轮次及其结论仍可查阅。
      </p></a-card
    >
    <a-space style="margin: 16px 0" wrap
      ><a-select
        v-model:value="selectedId"
        placeholder="选择模板"
        style="width: 260px"
        :options="
          templates.map((t) => ({
            label: t.name + (t.isDefault ? '（默认）' : ''),
            value: t.id,
          }))
        "
        @change="selectTemplate"
      /><a-button @click="reset">新增模板</a-button
      ><a-popconfirm v-if="selectedId" title="删除此模板？" @confirm="remove"
        ><a-button danger>删除模板</a-button></a-popconfirm
      ></a-space
    >
    <a-form layout="vertical">
      <a-row :gutter="16"
        ><a-col :span="16"
          ><a-form-item label="模板名称" required
            ><a-input
              v-model:value="form.name"
              :maxlength="100" /></a-form-item></a-col
        ><a-col :span="8"
          ><a-form-item label="项目默认模板"
            ><a-switch v-model:checked="form.isDefault" /></a-form-item></a-col
      ></a-row>
      <a-card title="默认用例内容" size="small"
        ><a-row :gutter="12"
          ><a-col :span="8"
            ><a-form-item label="优先级"
              ><a-select
                v-model:value="form.defaults.priority"
                :options="
                  ['P0', 'P1', 'P2', 'P3'].map((value) => ({ value }))
                " /></a-form-item></a-col
          ><a-col :span="8"
            ><a-form-item label="类型"
              ><a-select
                v-model:value="form.defaults.type"
                :options="types" /></a-form-item></a-col
          ><a-col :span="8"
            ><a-form-item label="自动化"
              ><a-switch
                v-model:checked="
                  form.defaults.is_automated
                " /></a-form-item></a-col></a-row
        ><a-form-item label="前置条件"
          ><a-textarea
            v-model:value="form.defaults.precondition"
            :rows="3" /></a-form-item
        ><a-form-item label="标签"
          ><a-select v-model:value="form.defaults.tags" mode="tags"
        /></a-form-item>
        <div v-for="(step, i) in form.defaults.steps" :key="i" class="step">
          <span>{{ i + 1 }}</span
          ><a-input
            v-model:value="step.action"
            placeholder="操作步骤"
          /><a-input
            v-model:value="step.expected"
            placeholder="预期结果"
          /><a-button danger @click="form.defaults.steps.splice(i, 1)"
            >删除</a-button
          >
        </div>
        <a-button
          @click="
            form.defaults.steps.push({
              step: form.defaults.steps.length + 1,
              action: '',
              expected: '',
            })
          "
          >添加默认步骤</a-button
        ></a-card
      >
      <a-divider>自定义字段</a-divider>
      <a-card
        v-for="(field, index) in form.fields"
        :key="index"
        size="small"
        style="margin-bottom: 12px"
      >
        <template #title>字段 {{ index + 1 }}</template
        ><template #extra
          ><a-button type="text" danger @click="form.fields.splice(index, 1)"
            >删除字段</a-button
          ></template
        >
        <a-row :gutter="12"
          ><a-col :span="8"
            ><a-form-item label="名称" required
              ><a-input v-model:value="field.name" /></a-form-item></a-col
          ><a-col :span="8"
            ><a-form-item label="字段标识（英文字母开头）" required
              ><a-input
                v-model:value="field.key"
                placeholder="如 vehicle_model" /></a-form-item></a-col
          ><a-col :span="8"
            ><a-form-item label="类型"
              ><a-select
                v-model:value="field.type"
                :options="fieldTypes"
                @change="field.default = null" /></a-form-item></a-col
        ></a-row>
        <a-form-item
          v-if="['select', 'multiselect'].includes(field.type)"
          label="可选项"
          ><a-select v-model:value="field.options" mode="tags"
        /></a-form-item>
        <a-checkbox v-model:checked="field.required">必填</a-checkbox>
        <a-form layout="vertical" style="margin-top: 12px"
          ><CaseCustomFields
            :fields="[{ ...field, name: '默认值', required: false }]"
            :model-value="{ [field.key]: field.default }"
            @update:model-value="field.default = $event[field.key]"
        /></a-form>
      </a-card>
      <a-space
        ><a-button
          @click="
            form.fields.push({
              key: '',
              name: '',
              type: 'text',
              required: false,
              options: [],
              default: null,
            })
          "
          >添加字段</a-button
        ><a-button type="primary" :loading="busy" @click="save"
          >保存模板</a-button
        ></a-space
      >
    </a-form>
  </a-drawer>
</template>
<script setup lang="ts">
import { ref, reactive, watch } from "vue";
import { message } from "ant-design-vue";
import { caseFeaturesApi as api, type CaseTemplate } from "@/api/caseFeatures";
import CaseCustomFields from "./CaseCustomFields.vue";
const props = defineProps<{ projectId: string; open: boolean }>(),
  emit = defineEmits<{ "update:open": [value: boolean]; changed: [] }>();
const autoResubmit = ref(false);
const templates = ref<CaseTemplate[]>([]),
  selectedId = ref<string>(),
  busy = ref(false);
const blank = () => ({
  name: "默认用例模板",
  fields: [] as CaseTemplate["fields"],
  defaults: {
    type: "functional",
    priority: "P2",
    precondition: "",
    tags: [],
    is_automated: false,
    steps: [],
  } as Record<string, any>,
  isDefault: true,
});
const form = reactive(blank());
const types = [
  { value: "functional", label: "功能测试" },
  { value: "interface", label: "接口测试" },
  { value: "ui", label: "UI测试" },
  { value: "performance", label: "性能测试" },
  { value: "security", label: "安全测试" },
];
const fieldTypes = [
  ["text", "单行文本"],
  ["textarea", "多行文本"],
  ["number", "数字"],
  ["boolean", "开关"],
  ["date", "日期"],
  ["select", "单选"],
  ["multiselect", "多选"],
].map(([value, label]) => ({ value, label }));
async function load() {
  try {
    [templates.value, { autoResubmit: autoResubmit.value }] = await Promise.all(
      [api.templates(props.projectId), api.settings(props.projectId)],
    );
    if (!selectedId.value && templates.value.length) {
      selectedId.value =
        templates.value.find((t) => t.isDefault)?.id || templates.value[0].id;
      selectTemplate();
    }
  } catch (error) {
    console.error("加载用例模板失败", error);
  }
}
function reset() {
  selectedId.value = undefined;
  Object.assign(form, blank(), {
    name: "新模板",
    isDefault: !templates.value.length,
  });
}
function selectTemplate() {
  const t = templates.value.find((t) => t.id === selectedId.value);
  if (t) {
    Object.assign(form, {
      name: t.name,
      isDefault: t.isDefault,
      fields: JSON.parse(JSON.stringify(t.fields)),
      defaults: {
        ...blank().defaults,
        ...JSON.parse(JSON.stringify(t.defaults)),
      },
    });
  }
}
async function save() {
  if (!form.name.trim()) return message.warning("请输入模板名称");
  busy.value = true;
  try {
    const saved = await api.saveTemplate(
      props.projectId,
      {
        ...form,
        name: form.name.trim(),
        defaults: {
          ...form.defaults,
          steps: form.defaults.steps.map((s: any, i: number) => ({
            ...s,
            step: i + 1,
          })),
        },
      },
      selectedId.value,
    );
    selectedId.value = saved.id;
    await load();
    emit("changed");
    message.success("模板已保存");
  } catch (error) {
    console.error("保存用例模板失败", error);
  } finally {
    busy.value = false;
  }
}
async function saveSettings() {
  busy.value = true;
  try {
    await api.saveSettings(props.projectId, autoResubmit.value);
    message.success("评审设置已保存");
  } catch (error) {
    console.error("保存评审设置失败", error);
    autoResubmit.value = !autoResubmit.value;
  } finally {
    busy.value = false;
  }
}
async function remove() {
  if (!selectedId.value) return;
  try {
    await api.deleteTemplate(props.projectId, selectedId.value);
    reset();
    await load();
    emit("changed");
    message.success("模板已删除");
  } catch (error) {
    console.error("删除用例模板失败", error);
  }
}
watch(
  () => [props.projectId, props.open],
  () => {
    if (props.open) {
      selectedId.value = undefined;
      load();
    }
  },
  { immediate: true },
);
</script>
<style scoped>
.step {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
  align-items: center;
}
</style>
