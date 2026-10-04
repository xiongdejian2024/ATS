<template>
  <div>
    <a-space wrap class="toolbar"
      ><a-button
        v-if="canEdit"
        type="primary"
        @click="
          form.caseId = caseId;
          open = true;
        "
        >新建缺陷</a-button
      ><a-input-search
        v-model:value="search"
        placeholder="搜索缺陷标题"
        allow-clear
      /><a-button :loading="loading" @click="load">刷新</a-button></a-space
    >
    <a-alert v-if="failed" type="error" message="缺陷列表加载失败" />
    <a-table
      :data-source="filtered"
      :columns="columns"
      row-key="id"
      :loading="loading"
      size="small"
      :scroll="{ x: 800 }"
      ><template #bodyCell="{ column, record }"
        ><a v-if="column.key === 'title'" @click="view = record">{{
          record.title
        }}</a
        ><span v-else-if="column.key === 'cases'">{{
          record.cases.map((item: any) => item.name).join("、")
        }}</span
        ><a-tag v-else-if="column.key === 'status'">{{
          statusLabels[record.status] || record.status
        }}</a-tag></template
      ></a-table
    >
  </div>
  <a-modal
    v-model:open="open"
    title="新建计划缺陷"
    :confirm-loading="saving"
    @ok="save"
    ><a-form layout="vertical"
      ><a-form-item label="缺陷标题" required
        ><a-input v-model:value="form.title" :maxlength="300" /></a-form-item
      ><a-form-item label="关联用例" required
        ><a-select
          v-model:value="form.caseId"
          :options="
            cases
              .filter((item) => !caseId || item.id === caseId)
              .map((item) => ({ value: item.id, label: item.name }))
          "
          show-search
          option-filter-prop="label"
          placeholder="选择计划内用例" /></a-form-item
      ><a-form-item label="描述"
        ><a-textarea
          v-model:value="form.description"
          :rows="4"
          :maxlength="20000" /></a-form-item></a-form
  ></a-modal>
  <a-drawer
    :open="!!view"
    title="缺陷详情"
    width="min(640px,100vw)"
    @close="view = undefined"
    ><template v-if="view"
      ><h3>{{ view.title }}</h3>
      <a-tag>{{ statusLabels[view.status] || view.status }}</a-tag>
      <p class="description">{{ view.description || "无描述" }}</p>
      <p>
        关联用例：{{ view.cases.map((item) => item.name).join("、") }}
      </p></template
    ></a-drawer
  >
</template>
<script setup lang="ts">
import { computed, ref, reactive, watch } from "vue";
import { message } from "ant-design-vue";
import { apiClient } from "@/utils/api";
import type { CaseIssue } from "@/api/caseFeatures";
const props = defineProps<{
    planId: string;
    editable: boolean;
    caseId?: string;
  }>(),
  emit = defineEmits<{ changed: [] }>();
type Defect = CaseIssue & {
  cases: { id: string; name: string; linkId: string }[];
};
const items = ref<Defect[]>([]),
  cases = ref<{ id: string; name: string }[]>([]),
  loading = ref(false),
  failed = ref(false),
  permission = ref(false),
  search = ref(""),
  open = ref(false),
  saving = ref(false),
  view = ref<Defect>();
const canEdit = computed(() => props.editable && permission.value),
  form = reactive({
    title: "",
    caseId: undefined as string | undefined,
    description: "",
  });
const filtered = computed(() =>
  items.value.filter(
    (item) =>
      item.title.includes(search.value.trim()) &&
      (!props.caseId ||
        item.cases.some((caseItem) => caseItem.id === props.caseId)),
  ),
);
const statusLabels: Record<string, string> = {
  open: "待处理",
  in_progress: "处理中",
  resolved: "已解决",
  closed: "已关闭",
};
const columns = [
  { title: "缺陷标题", key: "title", width: 240 },
  { title: "状态", key: "status", width: 110 },
  { title: "关联用例", key: "cases", width: 250 },
  { title: "创建时间", dataIndex: "createdAt", width: 190 },
];
let sequence = 0;
async function load() {
  const current = ++sequence;
  loading.value = true;
  failed.value = false;
  try {
    const result = await apiClient.get<{
      items: Defect[];
      cases: { id: string; name: string }[];
      canEdit: boolean;
    }>(`/plan-orchestration/plans/${props.planId}/defects`);
    if (current === sequence) {
      items.value = result.items;
      cases.value = result.cases;
      permission.value = result.canEdit;
    }
  } catch (error) {
    console.error("加载计划缺陷失败", error);
    if (current === sequence) {
      failed.value = true;
      items.value = [];
      permission.value = false;
    }
  } finally {
    if (current === sequence) loading.value = false;
  }
}
async function save() {
  if (!form.title.trim() || !form.caseId) {
    message.warning("请填写标题并选择计划内用例");
    return;
  }
  saving.value = true;
  try {
    await apiClient.post(
      `/plan-orchestration/plans/${props.planId}/defects`,
      form,
    );
    open.value = false;
    Object.assign(form, { title: "", caseId: undefined, description: "" });
    await load();
    emit("changed");
    message.success("缺陷已创建并关联");
  } catch (error) {
    console.error("创建计划缺陷失败", error);
    message.error("创建失败，请核对用例及权限");
  } finally {
    saving.value = false;
  }
}
watch(
  () => props.planId,
  () => {
    items.value = [];
    permission.value = false;
    open.value = false;
    view.value = undefined;
    void load();
  },
  { immediate: true },
);
</script>
<style scoped>
.toolbar {
  margin-bottom: 16px;
}
.toolbar :deep(.ant-input-search) {
  width: 240px;
}
.description {
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  margin-top: 16px;
}
</style>
