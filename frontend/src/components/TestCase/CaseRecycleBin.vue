<template>
  <component
    :is="embedded ? 'section' : Drawer"
    v-if="open"
    class="case-recycle-bin"
    v-bind="
      embedded ? {} : { open, title: '用例回收站', width: 'min(1000px, 96vw)' }
    "
    :closable="!mutating"
    :mask-closable="!mutating"
    :keyboard="!mutating"
    @close="!mutating && emit('update:open', false)"
  >
    <header v-if="embedded" class="recycle-header">
      <h3>回收站（{{ total }}）</h3>
      <a-button :disabled="mutating" @click="emit('close')">返回用例</a-button>
    </header>
    <a-alert
      message="恢复后重新进入用例库。彻底删除无法撤销；有执行历史的用例会被系统阻止删除。"
      type="info"
      show-icon
    />
    <a-input-search
      v-model:value="search"
      placeholder="搜索编号、名称或标签"
      :disabled="mutating"
      style="margin: 16px 0"
      @search="
        page = 1;
        load();
      "
    />
    <a-space wrap style="margin-bottom: 12px">
      <a-button :disabled="mutating" @click="filterOpen = true"
        >高级筛选（{{ conditions.length }}）</a-button
      >
      <a-button :disabled="mutating" @click="clearFilters">清除筛选</a-button>
      <a-popover trigger="click" title="显示列"
        ><template #content
          ><a-checkbox-group
            v-model:value="columnKeys"
            :options="columnOptions" /></template
        ><a-button>显示列</a-button></a-popover
      >
    </a-space>
    <a-alert v-if="readError" type="error" :message="readError" show-icon
      ><template #action
        ><a-button @click="load">重试</a-button></template
      ></a-alert
    >
    <a-space v-if="selectedIds.length" class="recycle-batch" wrap>
      <span>已选择 {{ selectedIds.length }} 条</span>
      <a-button :loading="mutating" @click="batch('restore')">恢复</a-button>
      <a-popconfirm
        :title="`彻底删除所选 ${selectedIds.length} 条用例？不可撤销。`"
        @confirm="batch('purge')"
        ><a-button danger :disabled="mutating">彻底删除</a-button></a-popconfirm
      >
      <a-button type="text" :disabled="mutating" @click="selectedIds = []"
        >清空</a-button
      >
    </a-space>
    <a-table
      :columns="columns"
      :data-source="rows"
      :loading="busy"
      row-key="id"
      :scroll="{ x: 650 }"
      :row-selection="{
        selectedRowKeys: selectedIds,
        preserveSelectedRowKeys: true,
        getCheckboxProps: () => ({ disabled: mutating }),
        onChange: (ids: any[]) => !mutating && (selectedIds = ids.map(String)),
      }"
      :pagination="{ current: page, pageSize: 20, total }"
      @change="tableChange"
    >
      <template #bodyCell="{ column, record }"
        ><template v-if="column.key === 'actions'"
          ><a-space
            ><a-button :disabled="mutating" @click="restore(record.id)"
              >恢复</a-button
            ><a-popconfirm
              :title="`彻底删除 ${record.name}？不可撤销。`"
              @confirm="purge(record.id)"
              ><a-button danger :disabled="mutating"
                >彻底删除</a-button
              ></a-popconfirm
            ></a-space
          ></template
        ></template
      >
    </a-table>
    <TestCaseFilter
      :key="projectId + String(user.user?.id)"
      v-model:visible="filterOpen"
      :available-fields="filterFields"
      :module-tree-data="moduleTree"
      :conditions="conditions"
      :logic="logic"
      :metadata-loading="metadataLoading"
      :metadata-error="metadataError"
      @retry-fields="loadMetadata"
      @apply="applyFilters"
    />
  </component>
</template>
<script setup lang="ts">
import { ref, watch, computed, onBeforeUnmount } from "vue";
import dayjs from "dayjs";
import { Drawer, message } from "ant-design-vue";
import { caseFeaturesApi as api } from "@/api/caseFeatures";
import type { TestCase } from "@/types";
import { testCaseApi } from "@/api/testCase";
import { projectApi } from "@/api/project";
import { caseGovernanceApi } from "@/api/caseGovernance";
import { useUserStore } from "@/stores/user";
import TestCaseFilter from "./TestCaseFilter.vue";
import { filterFieldCatalog } from "./filterFieldCatalog";
import { buildCaseMindMap } from "./caseMindMap";
import type {
  FilterCondition,
  FilterLogic,
  FilterField,
} from "./advancedFilter";
const props = defineProps<{
    projectId: string;
    open: boolean;
    embedded?: boolean;
  }>(),
  emit = defineEmits<{
    "update:open": [value: boolean];
    changed: [];
    total: [value: number];
    close: [];
  }>();
const selectedIds = ref<string[]>([]),
  mutating = ref(false);
const user = useUserStore(),
  filterOpen = ref(false),
  conditions = ref<FilterCondition[]>([]),
  logic = ref<FilterLogic>("and"),
  filterFields = ref<FilterField[]>([]),
  moduleTree = ref<any[]>([]),
  metadataLoading = ref(false),
  metadataError = ref(""),
  readError = ref("");
const sortBy = ref("deletedAt"),
  sortOrder = ref("desc"),
  columnKeys = ref<string[]>(["caseCode", "name", "deletedAt"]);
const rows = ref<TestCase[]>([]),
  total = ref(0),
  page = ref(1),
  search = ref(""),
  busy = ref(false);
const columnOptions = computed(() => [
  { label: "编号", value: "caseCode" },
  { label: "名称", value: "name" },
  { label: "优先级", value: "priority" },
  { label: "类型", value: "type" },
  { label: "模块路径", value: "modulePath" },
  { label: "标签", value: "tags" },
  { label: "执行结果", value: "status" },
  { label: "创建人", value: "createdBy" },
  { label: "创建时间", value: "createdAt" },
  { label: "更新人", value: "updatedBy" },
  { label: "更新时间", value: "updatedAt" },
  { label: "删除时间", value: "deletedAt" },
  ...filterFields.value
    .filter((f) => f.key.startsWith("customFields."))
    .map((f) => ({ label: f.label, value: f.key })),
]);
const columns = computed(() => [
  ...columnOptions.value
    .filter((o) => columnKeys.value.includes(o.value))
    .map((o) => ({
      title: o.label,
      key: o.value,
      dataIndex: o.value.startsWith("customFields.")
        ? ["customFields", o.value.slice(13)]
        : o.value,
      sorter: [
        "caseCode",
        "name",
        "priority",
        "type",
        "status",
        "createdAt",
        "updatedAt",
        "deletedAt",
      ].includes(o.value),
      customRender: ({ text }: { text: any }) =>
        o.value.endsWith("At")
          ? text
            ? dayjs(text).format("YYYY-MM-DD HH:mm:ss")
            : "-"
          : Array.isArray(text)
            ? text.join("、")
            : typeof text === "boolean"
              ? text
                ? "是"
                : "否"
              : (text ?? "-"),
    })),
  { title: "操作", key: "actions" },
]);
let loadSequence = 0,
  metadataSequence = 0,
  scopeSequence = 0;
let columnScopeKey = "",
  restoringColumns = false;
function columnStorageKey() {
  return (
    "ats.recycle.columns.v1." +
    encodeURIComponent(String(user.user?.id || "")) +
    "." +
    encodeURIComponent(props.projectId)
  );
}
function restoreColumns() {
  restoringColumns = true;
  columnScopeKey = columnStorageKey();
  columnKeys.value = ["caseCode", "name", "deletedAt"];
  try {
    const saved = JSON.parse(localStorage.getItem(columnScopeKey) || "null");
    if (
      Array.isArray(saved) &&
      saved.length <= 100 &&
      saved.every((k) => typeof k === "string" && k.length <= 200)
    )
      columnKeys.value = saved;
  } catch {
  } finally {
    restoringColumns = false;
  }
}
watch(
  columnKeys,
  (keys) => {
    if (restoringColumns || !columnScopeKey) return;
    try {
      localStorage.setItem(columnScopeKey, JSON.stringify(keys));
    } catch {}
  },
  { deep: true, flush: "sync" },
);
async function loadMetadata() {
  if (!props.open) return;
  const mine = ++metadataSequence,
    project = props.projectId;
  metadataLoading.value = true;
  metadataError.value = "";
  const results = await Promise.allSettled([
    testCaseApi.getFilterFields(project),
    api.templates(project),
    caseGovernanceApi.reviewers(project),
    projectApi.getModules(project),
  ]);
  if (mine !== metadataSequence) return;
  const labels = ["系统字段", "模板字段", "项目成员", "模块"];
  const failures = results.flatMap((r, i) =>
    r.status === "rejected" ? [labels[i]] : [],
  );
  if (results[0].status === "fulfilled") {
    const templates = results[1].status === "fulfilled" ? results[1].value : [],
      members = results[2].status === "fulfilled" ? results[2].value : [];
    filterFields.value = [
      ...filterFieldCatalog(results[0].value, templates, members),
      { key: "deletedAt", label: "删除时间", type: "date" },
    ];
  }
  if (results[3].status === "fulfilled")
    moduleTree.value = [
      { key: "__unassigned__", title: "未规划用例", nodeType: "module" },
      ...(
        buildCaseMindMap([], results[3].value.modules || results[3].value)
          .children || []
      ).map(function node(m: any): any {
        return {
          key: m.moduleId,
          title: m.name,
          nodeType: "module",
          children: (m.children || []).map(node),
        };
      }),
    ];
  metadataError.value = failures.length
    ? failures.join("、") + "加载失败，请重试"
    : "";
  metadataLoading.value = false;
}
function applyFilters(next: FilterCondition[], nextLogic: FilterLogic) {
  if (mutating.value) return;
  conditions.value = next;
  logic.value = nextLogic;
  selectedIds.value = [];
  page.value = 1;
  load();
}
function clearFilters() {
  if (mutating.value) return;
  conditions.value = [];
  logic.value = "and";
  search.value = "";
  selectedIds.value = [];
  page.value = 1;
  load();
}
function tableChange(p: any, _filters: any, sorter: any) {
  if (mutating.value) return;
  page.value = p.current || 1;
  sortBy.value = sorter?.order ? String(sorter.columnKey) : "deletedAt";
  sortOrder.value = sorter?.order === "ascend" ? "asc" : "desc";
  load();
}
async function load() {
  if (!props.open || !props.projectId) return;
  const sequence = ++loadSequence;
  const projectId = props.projectId;
  busy.value = true;
  readError.value = "";
  try {
    const data = await api.recycle(projectId, {
      page: page.value,
      size: 20,
      search: search.value,
      filters: JSON.stringify({
        conditions: conditions.value,
        logic: logic.value,
      }),
      sort_by: sortBy.value,
      sort_order: sortOrder.value,
    });
    if (sequence !== loadSequence || projectId !== props.projectId) return;
    rows.value = data.items;
    total.value = data.total;
    emit("total", data.total);
  } catch (error) {
    if (sequence === loadSequence)
      readError.value = "加载回收站失败，请重试或调整筛选";
  } finally {
    if (sequence === loadSequence) busy.value = false;
  }
}
async function batch(action: "restore" | "purge") {
  if (mutating.value || !selectedIds.value.length) return;
  mutating.value = true;
  const ids = [...selectedIds.value];
  const projectId = props.projectId,
    scope = scopeSequence;
  try {
    const results = await Promise.allSettled(
      ids.map((id) => api[action](projectId, id)),
    );
    const failed = results.filter((result) => result.status === "rejected");
    for (const result of failed)
      if (result.status === "rejected")
        console.error(
          `批量${action === "restore" ? "恢复" : "彻底删除"}用例失败`,
          result.reason,
        );
    const count = results.length - failed.length;
    if (scope !== scopeSequence) return;
    selectedIds.value = ids.filter((_, i) => results[i].status === "rejected");
    if (failed.length)
      message.warning(
        `成功 ${count} 条，失败 ${failed.length} 条${action === "purge" ? "；有历史引用的用例无法彻底删除" : "，请重试或检查权限"}`,
      );
    else
      message.success(
        `已${action === "restore" ? "恢复" : "彻底删除"} ${count} 条用例`,
      );
    console.info("回收站批量操作已结束", {
      action,
      projectId: props.projectId,
      success: count,
      failed: failed.length,
    });
    if (count) emit("changed");
    await load();
  } catch (error) {
    console.error("执行回收站批量操作失败", error);
    message.error("批量操作失败，请重试");
  } finally {
    if (scope === scopeSequence) mutating.value = false;
  }
}
async function restore(id: string) {
  await single("restore", id);
}
async function purge(id: string) {
  await single("purge", id);
}
async function single(action: "restore" | "purge", id: string) {
  if (mutating.value) return;
  const project = props.projectId,
    scope = scopeSequence;
  mutating.value = true;
  try {
    await api[action](project, id);
    if (scope !== scopeSequence) return;
    selectedIds.value = selectedIds.value.filter((value) => value !== id);
    message.success(action === "restore" ? "用例已恢复" : "用例已彻底删除");
    emit("changed");
    await load();
  } catch (error) {
    if (scope === scopeSequence)
      message.error("操作失败，请重试或检查权限；历史引用会阻止彻底删除");
  } finally {
    if (scope === scopeSequence) mutating.value = false;
  }
}
watch(
  () => [props.projectId, props.open, user.user?.id],
  () => {
    ++scopeSequence;
    ++loadSequence;
    ++metadataSequence;
    busy.value = false;
    mutating.value = false;
    metadataLoading.value = false;
    rows.value = [];
    total.value = 0;
    readError.value = "";
    metadataError.value = "";
    filterFields.value = [];
    moduleTree.value = [];
    conditions.value = [];
    logic.value = "and";
    filterOpen.value = false;
    search.value = "";
    sortBy.value = "deletedAt";
    sortOrder.value = "desc";
    restoreColumns();
    page.value = 1;
    selectedIds.value = [];
    load();
    loadMetadata();
  },
  { immediate: true },
);
onBeforeUnmount(() => {
  ++scopeSequence;
  ++loadSequence;
  ++metadataSequence;
});
</script>

<style scoped>
.case-recycle-bin {
  background: #fff;
}
.recycle-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}
.recycle-header h3 {
  font-size: 14px;
  font-weight: 500;
}
.recycle-batch {
  margin-bottom: 12px;
}
</style>
