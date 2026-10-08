<template>
  <a-drawer
    :open="true"
    title="缺陷模板与自定义字段"
    width="min(900px,100vw)"
    :mask-closable="!busy"
    :closable="!busy"
    @close="beforeClose"
    ><a-alert
      message="模板用于新缺陷默认内容，修改不会覆盖既有缺陷；字段变更须兼容已保存的值。"
      type="info"
    /><a-alert v-if="error" type="error" :message="error" /><a-space
      wrap
      class="toolbar"
      ><a-select
        :value="id || ''"
        style="width: 250px"
        :options="[
          { value: '', label: '新增模板' },
          ...templates.map((t) => ({
            value: t.id,
            label: t.name + (t.isDefault ? '（默认）' : ''),
          })),
        ]"
        :disabled="busy || loading"
        @change="select"
      /><a-button :loading="loading" :disabled="busy" @click="reload"
        >刷新</a-button
      ><a-button
        v-if="canUpdate"
        type="primary"
        :loading="busy"
        :disabled="busy || loading"
        @click="save"
        >保存模板</a-button
      ><a-button
        v-if="canUpdate && id"
        danger
        :disabled="busy || loading"
        @click="remove"
        >删除模板</a-button
      ></a-space
    >
    <a-form layout="vertical" :disabled="busy || loading || !canUpdate"
      ><a-form-item label="模板名称" required
        ><a-input v-model:value="form.name" :maxlength="100" /></a-form-item
      ><a-form-item label="项目默认模板"
        ><a-switch v-model:checked="form.isDefault" /></a-form-item
      ><a-row :gutter="16"
        ><a-col :xs="24" :sm="12"
          ><a-form-item label="默认状态"
            ><a-select
              v-model:value="form.defaults.status"
              :options="[
                { value: 'open', label: '待处理' },
                { value: 'in_progress', label: '处理中' },
                { value: 'resolved', label: '已解决' },
                { value: 'closed', label: '已关闭' },
              ]" /></a-form-item></a-col
        ><a-col :xs="24" :sm="12"
          ><a-form-item label="默认外部引用"
            ><a-input
              v-model:value="form.defaults.externalRef"
              :maxlength="500" /></a-form-item></a-col></a-row
      ><a-form-item label="默认描述（纯文本）"
        ><a-textarea
          v-model:value="form.defaults.description"
          :maxlength="30000"
          :rows="3"
      /></a-form-item>
      <a-card
        v-for="(field, index) in form.fields"
        :key="index"
        size="small"
        class="field"
        ><template #title>自定义字段 {{ index + 1 }}</template
        ><template #extra
          ><a-button
            :disabled="busy || loading || !canUpdate"
            danger
            @click="removeField(index)"
            >移除</a-button
          ></template
        ><a-row :gutter="12"
          ><a-col :xs="24" :sm="8"
            ><a-form-item label="字段键"
              ><a-input
                v-model:value="field.key"
                :maxlength="50"
                placeholder="稳定英文键" /></a-form-item></a-col
          ><a-col :xs="24" :sm="8"
            ><a-form-item label="显示名称"
              ><a-input
                v-model:value="field.name"
                :maxlength="100" /></a-form-item></a-col
          ><a-col :xs="24" :sm="8"
            ><a-form-item label="类型"
              ><a-select
                :value="field.type"
                :options="types"
                @change="
                  changeType(index, $event)
                " /></a-form-item></a-col></a-row
        ><a-form-item label="必填"
          ><a-switch v-model:checked="field.required" /></a-form-item
        ><a-form-item
          v-if="field.type === 'select' || field.type === 'multiselect'"
          label="候选项"
          ><a-select
            :value="field.options"
            mode="tags"
            @change="setOptions(index, $event)" /></a-form-item
        ><CaseCustomFields
          :fields="[{ ...field, name: '默认值', required: false }]"
          :model-value="{ [field.key]: field.default }"
          :readonly="busy || loading || !canUpdate"
          @update:model-value="field.default = $event[field.key]" /></a-card
      ><a-button
        v-if="canUpdate"
        :disabled="busy || loading || form.fields.length >= 50"
        @click="addField"
        >添加字段（{{ form.fields.length }} / 50）</a-button
      ></a-form
    >
  </a-drawer>
</template>
<script setup lang="ts">
import {
  ref,
  reactive,
  computed,
  watch,
  onMounted,
  onBeforeUnmount,
} from "vue";
import { Modal, message } from "ant-design-vue";
import { onBeforeRouteLeave, onBeforeRouteUpdate } from "vue-router";
import { useUserStore } from "@/stores/user";
import { defectsApi as api, type DefectTemplate } from "@/api/defects";
import type { CaseCustomField } from "@/api/caseFeatures";
import CaseCustomFields from "./CaseCustomFields.vue";
const props = defineProps<{ projectId: string }>(),
  emit = defineEmits<{ closed: [] }>(),
  user = useUserStore();
const blank = () => ({
  name: "",
  fields: [] as CaseCustomField[],
  defaults: { status: "open", description: "", externalRef: "" },
  isDefault: false,
  expectedRevision: 0,
});
const form = reactive(blank());
const templates = ref<DefectTemplate[]>([]),
  id = ref(""),
  baseline = ref(""),
  busy = ref(false),
  loading = ref(false),
  error = ref(""),
  canUpdate = ref(false);
let epoch = 0,
  sequence = 0,
  live = true,
  closing = false;
const current = (mine: number) => live && mine === epoch;
const body = () =>
  JSON.parse(JSON.stringify(form)) as Omit<
    DefectTemplate,
    "id" | "revision"
  > & { expectedRevision: number };
const dirty = computed(
  () => !!baseline.value && JSON.stringify(body()) !== baseline.value,
);
const types = [
  ["text", "单行文本"],
  ["textarea", "多行文本"],
  ["number", "数字"],
  ["boolean", "开关"],
  ["date", "日期"],
  ["select", "单选"],
  ["multiselect", "多选"],
].map(([value, label]) => ({ value, label }));
function choose(identifier: string) {
  const template = templates.value.find((t) => t.id === identifier);
  id.value = identifier;
  Object.assign(
    form,
    blank(),
    template
      ? {
          name: template.name,
          fields: JSON.parse(JSON.stringify(template.fields)),
          defaults: { ...blank().defaults, ...template.defaults },
          isDefault: template.isDefault,
          expectedRevision: template.revision,
        }
      : {},
  );
  baseline.value = JSON.stringify(body());
  error.value = "";
}
async function load(keepDraft = false) {
  const mine = epoch,
    ticket = ++sequence,
    captured = JSON.stringify(body()),
    capturedId = id.value;
  loading.value = true;
  try {
    const data = await api.templates(props.projectId);
    if (!current(mine) || ticket !== sequence) return;
    templates.value = data.items;
    canUpdate.value = data.canUpdate;
    if (
      !keepDraft &&
      id.value === capturedId &&
      JSON.stringify(body()) === captured
    ) {
      choose(
        id.value && data.items.some((t) => t.id === id.value)
          ? id.value
          : data.items[0]?.id || "",
      );
    }
  } catch (failure) {
    if (current(mine) && ticket === sequence) {
      error.value = "模板读取失败，请核对项目权限后重试";
      canUpdate.value = false;
    }
  } finally {
    if (current(mine) && ticket === sequence) loading.value = false;
  }
}
watch(
  () => [props.projectId, user.user?.id],
  () => {
    ++epoch;
    ++sequence;
    closing = false;
    id.value = "";
    busy.value = loading.value = false;
    canUpdate.value = false;
    templates.value = [];
    Object.assign(form, blank());
    baseline.value = JSON.stringify(body());
    void load();
  },
  { immediate: true, flush: "sync" },
);
async function discard() {
  if (!live || busy.value || closing) return false;
  if (!dirty.value) return true;
  const mine = epoch,
    captured = JSON.stringify(body());
  closing = true;
  try {
    return await new Promise<boolean>((resolve) =>
      Modal.confirm({
        title: "放弃未保存的模板修改？",
        okText: "丢弃草稿",
        cancelText: "继续编辑",
        onOk() {
          resolve(
            current(mine) && !busy.value && captured === JSON.stringify(body()),
          );
        },
        onCancel() {
          resolve(false);
        },
      }),
    );
  } finally {
    if (current(mine)) closing = false;
  }
}
async function beforeClose() {
  const mine = epoch;
  if (!(await discard()) || !current(mine) || busy.value) return false;
  emit("closed");
  return true;
}
async function select(identifier: string) {
  const mine = epoch;
  if (loading.value || !(await discard()) || !current(mine) || busy.value)
    return;
  choose(identifier);
}
async function reload() {
  const mine = epoch;
  if (!(await discard()) || !current(mine) || busy.value) return;
  await load();
}
function addField() {
  if (
    !canUpdate.value ||
    busy.value ||
    loading.value ||
    form.fields.length >= 50
  )
    return;
  let number = form.fields.length + 1;
  while (form.fields.some((f) => f.key === "field" + number)) ++number;
  form.fields.push({
    key: "field" + number,
    name: "新字段",
    type: "text",
    required: false,
    options: [],
    default: null,
  });
}
function removeField(index: number) {
  if (canUpdate.value && !busy.value && !loading.value)
    form.fields.splice(index, 1);
}
function changeType(index: number, type: CaseCustomField["type"]) {
  if (!canUpdate.value || busy.value || loading.value) return;
  form.fields[index].type = type;
  form.fields[index].default = null;
  form.fields[index].options = [];
}
function setOptions(index: number, options: string[]) {
  if (!canUpdate.value || busy.value || loading.value) return;
  if (options.length > 100 || options.some((v) => v.length > 1000)) {
    error.value = "每字段最多100个候选项，每项最多1000字";
    return;
  }
  form.fields[index].options = [...new Set(options)];
}
async function save() {
  if (!canUpdate.value || busy.value || loading.value || closing) return;
  const mine = epoch,
    project = props.projectId,
    identifier = id.value,
    input = body();
  if (!input.name.trim()) {
    error.value = "请填写模板名称";
    return;
  }
  busy.value = true;
  error.value = "";
  try {
    const data = await api.saveTemplate(
      project,
      input,
      identifier || undefined,
    );
    if (!current(mine)) return;
    id.value = data.id;
    form.expectedRevision = data.revision;
    baseline.value = JSON.stringify({
      ...input,
      expectedRevision: data.revision,
    });
    templates.value = templates.value
      .filter((t) => t.id !== data.id)
      .concat(data);
    message.success("缺陷模板已保存");
    if (!dirty.value) choose(data.id);
    // Switching the default also changes the other template's version.
    // Refresh the catalog while keeping any draft typed during the save.
    await load(true);
  } catch (failure) {
    if (current(mine))
      error.value = "模板保存失败、版本冲突或字段与现有值不兼容，草稿已保留";
  } finally {
    if (current(mine)) busy.value = false;
  }
}
function remove() {
  if (!canUpdate.value || !id.value || busy.value || loading.value) return;
  const mine = epoch,
    project = props.projectId,
    identifier = id.value,
    revision = form.expectedRevision;
  Modal.confirm({
    title: "删除此缺陷模板？",
    content: "已被缺陷使用的模板会拒绝删除。",
    async onOk() {
      if (
        !current(mine) ||
        busy.value ||
        !canUpdate.value ||
        id.value !== identifier ||
        form.expectedRevision !== revision
      )
        return;
      if (!(await discard()) || !current(mine) || busy.value) return;
      busy.value = true;
      try {
        await api.removeTemplate(project, identifier, revision);
        if (!current(mine)) return;
        id.value = "";
        await load();
        if (current(mine)) message.success("缺陷模板已删除");
      } catch (failure) {
        if (current(mine))
          error.value = "删除失败、模板被引用或版本冲突，请核对后重试";
      } finally {
        if (current(mine)) busy.value = false;
      }
    },
  });
}
function beforeUnload(event: BeforeUnloadEvent) {
  if (dirty.value || busy.value) {
    event.preventDefault();
    event.returnValue = "";
  }
}
onMounted(() => window.addEventListener("beforeunload", beforeUnload));
onBeforeUnmount(() => {
  live = false;
  ++epoch;
  ++sequence;
  window.removeEventListener("beforeunload", beforeUnload);
});
onBeforeRouteLeave(beforeClose);
onBeforeRouteUpdate(beforeClose);
defineExpose({ beforeClose });
</script>
<style scoped>
.toolbar {
  margin: 16px 0;
}
.field {
  margin: 12px 0;
}
.ant-select {
  width: 100%;
}
</style>
