<template>
  <section class="report-list">
    <a-alert v-if="!projectId" message="请选择项目" type="info" />
    <template v-else>
      <div class="report-toolbar">
        <a-space wrap
          ><a-radio-group
            :value="showType"
            :disabled="busy || filterSaving"
            @change="handleTypeEvent"
            ><a-radio-button value="ALL">全部</a-radio-button
            ><a-radio-button value="PLAN">测试计划报告</a-radio-button
            ><a-radio-button value="GROUP"
              >测试计划组报告</a-radio-button
            ></a-radio-group
          ><a-button
            v-if="advancedConditions === undefined"
            @click="expanded = !expanded"
            :aria-expanded="expanded"
            >筛选</a-button
          ></a-space
        >
        <a-space wrap
          ><a-input-search
            v-if="advancedConditions === undefined"
            v-model:value="search"
            placeholder="搜索报告名称"
            allow-clear
            @search="apply" /><a-button
            aria-label="刷新报告列表"
            :loading="loading"
            @click="refresh"
            ><ReloadOutlined /></a-button
        ></a-space>
      </div>
      <WorkspaceAdvancedFilters
        ref="filterEditor"
        :key="identity"
        :project-id="projectId"
        namespace="report-index"
        label="报告首页视图"
        :initial-fields="['name', 'planName']"
        :modules="[]"
        :api="reportIndexViewApi"
        :load-fields="loadFields"
        :conditions="advancedConditions"
        :logic="advancedLogic"
        :view-id="advancedViewId"
        :busy="busy || !!editing || settingsVisible"
        @apply="applyAdvanced"
        @saving="filterSaving = $event"
      />
      <a-button
        aria-label="报告表格设置"
        :disabled="busy || filterSaving || !!editing"
        @click="settingsVisible = true"
        >表格设置</a-button
      >
      <a-form
        v-if="expanded && advancedConditions === undefined"
        :model="filters"
        class="report-filters"
        layout="vertical"
        @finish="apply"
      >
        <a-form-item label="所属计划"
          ><a-input
            v-model:value="filters.plan_name"
            placeholder="计划或计划组名称"
        /></a-form-item>
        <a-form-item label="报告类型"
          ><a-select
            v-model:value="filters.kind"
            allow-clear
            placeholder="全部类型"
            :options="[
              { value: 'PLAN', label: '普通报告' },
              { value: 'GROUP', label: '集成报告' },
            ]"
        /></a-form-item>
        <a-form-item label="结果"
          ><a-select
            v-model:value="filters.result_status"
            allow-clear
            placeholder="全部结果"
            :options="reportResultOptions"
        /></a-form-item>
        <a-form-item label="触发方式"
          ><a-select
            v-model:value="filters.trigger_mode"
            allow-clear
            placeholder="全部方式"
            :options="[
              { value: 'manual', label: '手动触发' },
              { value: 'cron', label: '定时触发' },
            ]"
        /></a-form-item>
        <a-form-item label="操作人"
          ><a-input v-model:value="filters.operator" placeholder="操作人姓名"
        /></a-form-item>
        <a-form-item label="通过率"
          ><a-space
            ><a-input-number
              v-model:value="filters.min_rate"
              :min="0"
              :max="100"
              placeholder="最小 %" /><span>～</span
            ><a-input-number
              v-model:value="filters.max_rate"
              :min="0"
              :max="100"
              placeholder="最大 %" /></a-space
        ></a-form-item>
        <a-form-item label="操作时间" class="date-filter"
          ><a-range-picker
            v-model:value="dates"
            show-time
            format="YYYY-MM-DD HH:mm"
        /></a-form-item>
        <a-space class="filter-actions"
          ><a-button type="primary" html-type="submit">查询</a-button
          ><a-button @click="reset">重置</a-button></a-space
        >
      </a-form>
      <a-alert
        v-if="failed"
        type="error"
        show-icon
        message="报告加载失败"
        class="load-error"
        ><template #action
          ><a-button size="small" @click="refresh">重试</a-button></template
        ></a-alert
      >
      <a-space v-if="canDelete && selected.length" class="batch-toolbar"
        ><span>已选择 {{ selected.length }} 条</span
        ><a-button danger :loading="busy" @click="deleteSelected"
          >批量删除</a-button
        ><a-button :disabled="busy || filterSaving" @click="selected = []"
          >取消选择</a-button
        ></a-space
      >
      <a-table
        :data-source="items"
        :columns="columns"
        :loading="loading"
        :row-key="rowKey"
        :scroll="{ x: 1600 }"
        size="small"
        :row-selection="
          canDelete
            ? {
                selectedRowKeys: selected,
                onChange: selectionChanged,
                getCheckboxProps: () => ({ disabled: busy || filterSaving }),
              }
            : undefined
        "
        :pagination="{
          current: page,
          pageSize: size,
          total,
          showSizeChanger: true,
          pageSizeOptions: reportPageSizes.map(String),
          showTotal: (n: number) => `共 ${n} 条`,
        }"
        @change="tableChange"
        @resizeColumn="resizeColumn"
      >
        <template #bodyCell="{ column, record }">
          <div v-if="column.key === 'name'" class="report-name">
            <template v-if="editing === rowKey(record)"
              ><a-input
                v-model:value="editName"
                :maxlength="255"
                aria-label="报告新名称"
                :disabled="busy"
                @press-enter="rename(record)"
                @keydown.esc="cancelRename"
              /><a-button
                type="text"
                size="small"
                aria-label="保存报告名称"
                :loading="busy"
                @click="rename(record)"
                ><CheckOutlined /></a-button
              ><a-button
                type="text"
                size="small"
                aria-label="取消重命名"
                :disabled="busy"
                @click="cancelRename"
                >×</a-button
              ></template
            >
            <template v-else
              ><a
                :href="reportHref(record)"
                :title="record.name"
                @click.prevent="openReport(record)"
                >{{ record.name }}</a
              ><a-button
                v-if="canRename"
                type="text"
                size="small"
                class="rename-button"
                :aria-label="`重命名${record.name}`"
                @click="beginRename(record)"
                ><EditOutlined /></a-button
            ></template>
          </div>
          <a-tag
            v-else-if="column.key === 'kind'"
            :color="record.kind === 'GROUP' ? 'blue' : 'default'"
            >{{ record.kind === "GROUP" ? "集成报告" : "普通报告" }}</a-tag
          >
          <a-tag
            v-else-if="column.key === 'resultStatus'"
            :color="reportResultColor(record.resultStatus)"
            >{{ reportResultLabel(record.resultStatus) }}</a-tag
          >
          <span v-else-if="column.key === 'passRate'">{{
            record.passRate === null ? "—" : `${record.passRate}%`
          }}</span>
          <span v-else-if="column.key === 'triggerMode'">{{
            record.triggerMode === "cron" ? "定时触发" : "手动触发"
          }}</span>
          <span v-else-if="column.key === 'createTime'">{{
            dayjs(record.createTime).format("YYYY-MM-DD HH:mm:ss")
          }}</span>
          <a-space v-else-if="column.key === 'operation'" :size="0"
            ><a-button
              v-if="canDelete"
              type="link"
              size="small"
              :disabled="busy"
              @click="deleteOne(record)"
              >删除</a-button
            ><a-button
              type="link"
              size="small"
              :disabled="busy"
              @click="exportPdf(record)"
              >导出</a-button
            ></a-space
          >
        </template>
      </a-table>
      <TableDisplaySettings
        :key="identity"
        :open="settingsVisible"
        :definitions="reportColumnDefinitions"
        :columns="display.columns"
        :page-size="display.pageSize"
        :include-descendants="true"
        :show-descendants="false"
        :available-page-sizes="reportPageSizes"
        :error="settingsError"
        @close="saveColumns"
        @page-size-change="saveSize"
      />
    </template>
  </section>
</template>
<script setup lang="ts">
import {
  computed,
  ref,
  reactive,
  watch,
  onBeforeUnmount,
  onMounted,
} from "vue";
import {
  useRoute,
  useRouter,
  onBeforeRouteLeave,
  onBeforeRouteUpdate,
} from "vue-router";
import { message, Modal } from "ant-design-vue";
import {
  ReloadOutlined,
  EditOutlined,
  CheckOutlined,
} from "@ant-design/icons-vue";
import dayjs, { type Dayjs } from "dayjs";
import { useProjectStore } from "@/stores/project";
import { useUserStore } from "@/stores/user";
import {
  planReportsApi,
  reportIndexViewApi,
  reportResultOptions,
  reportResultLabel,
  reportResultColor,
  type PlanReportEntry,
  type ReportKind,
} from "@/api/planReports";
import { downloadPlanFile } from "@/api/planCollaboration";
import { planGroupApi } from "@/api/planGroup";
import { planWorkspaceApi } from "@/api/planWorkspace";
import WorkspaceAdvancedFilters from "@/components/Table/WorkspaceAdvancedFilters.vue";
import TableDisplaySettings from "@/components/Table/TableDisplaySettings.vue";
import type {
  FilterCondition,
  FilterLogic,
} from "@/components/TestCase/advancedFilter";
import { reportIndexFilterFields } from "@/components/TestPlan/reportIndexFilterFields";
import {
  reportColumnDefinitions,
  reportColumnCatalog,
  reportPageSizes,
  normalizeReportDisplay,
  readReportDisplay,
} from "@/components/Table/reportColumns";
import {
  displayStorageKey,
  resizableColumn,
  type ColumnVisibility,
  type TableDisplay,
} from "@/components/Table/tableDisplay";
import { useTableColumnResize } from "@/components/Table/useTableColumnResize";
const route = useRoute(),
  router = useRouter(),
  projectStore = useProjectStore(),
  user = useUserStore();
const projectId = computed(() =>
  typeof route.query.projectId === "string"
    ? route.query.projectId
    : projectStore.currentProject?.id,
);
const identity = computed(() =>
  JSON.stringify([projectId.value, user.user?.id]),
);
let epoch = 0,
  live = true,
  sequence = 0,
  operation = 0;
const scopeSnapshot = () => JSON.stringify([epoch, identity.value]);
const items = ref<PlanReportEntry[]>([]),
  total = ref(0),
  page = ref(1),
  size = ref(20),
  loading = ref(false),
  failed = ref(false),
  expanded = ref(false),
  search = ref("");
const filters = reactive<{
  plan_name?: string;
  kind?: string;
  result_status?: string;
  trigger_mode?: string;
  operator?: string;
  min_rate?: number;
  max_rate?: number;
}>({});
const dates = ref<[Dayjs, Dayjs]>(),
  sort = ref("created_at"),
  direction = ref("desc"),
  applied = ref<Record<string, unknown>>({});
const canRename = ref(false),
  canDelete = ref(false),
  selected = ref<string[]>([]),
  editing = ref(""),
  editName = ref(""),
  editBaseline = ref(""),
  busy = ref(false),
  showType = ref("ALL");
const advancedConditions = ref<FilterCondition[]>(),
  advancedLogic = ref<FilterLogic>("and"),
  advancedViewId = ref<string>(),
  filterSaving = ref(false);
const filterEditor = ref<{ beforeClose: () => Promise<boolean> }>();
const settingsVisible = ref(false),
  settingsError = ref(""),
  display = ref(normalizeReportDisplay(undefined));
const displayKey = computed(() =>
  displayStorageKey(
    user.user?.id || "anonymous",
    projectId.value || "",
    "plan-report-index",
  ),
);
const columns = computed(() =>
  display.value.columns
    .filter((p) => p.visible)
    .flatMap((p) => {
      const column = reportColumnCatalog.find((c) => c.key === p.key);
      return column ? [resizableColumn(column, p)] : [];
    }),
);
function persist(value: TableDisplay) {
  if (!live) return false;
  const normalized = normalizeReportDisplay(value);
  try {
    localStorage.setItem(displayKey.value, JSON.stringify(normalized));
    display.value = normalized;
    settingsError.value = "";
    return true;
  } catch (error) {
    console.error("保存报告显示配置失败", error);
    settingsError.value = "无法保存表格设置，请释放浏览器存储后重试";
    message.error(settingsError.value);
    return false;
  }
}
function saveColumns(columns: ColumnVisibility[]) {
  const normalized = normalizeReportDisplay({ ...display.value, columns });
  if (
    JSON.stringify(normalized.columns) === JSON.stringify(display.value.columns)
  ) {
    settingsVisible.value = false;
    settingsError.value = "";
    return;
  }
  if (persist(normalized)) settingsVisible.value = false;
}
function saveSize(value: number) {
  if (!persist({ ...display.value, pageSize: value })) return;
  size.value = display.value.pageSize;
  page.value = 1;
  void load();
}
const resizeColumn = useTableColumnResize(display, displayKey, persist);
async function loadFields(project: string) {
  return reportIndexFilterFields(await planWorkspaceApi.members(project));
}
let closing = false;
async function beforeNavigation() {
  const scope = scopeSnapshot(),
    draft = JSON.stringify([editing.value, editName.value, editBaseline.value]);
  if (!live || closing || busy.value || filterSaving.value) return false;
  closing = true;
  try {
    if (settingsVisible.value) {
      message.warning("请先关闭表格设置并保存修改");
      return false;
    }
    if (
      !((await filterEditor.value?.beforeClose()) ?? true) ||
      !live ||
      scope !== scopeSnapshot() ||
      busy.value ||
      filterSaving.value ||
      draft !==
        JSON.stringify([editing.value, editName.value, editBaseline.value])
    )
      return false;
    if (editing.value && editName.value !== editBaseline.value) {
      const accepted = await new Promise<boolean>((resolve) =>
        Modal.confirm({
          title: "放弃报告名称草稿？",
          onOk: () => resolve(true),
          onCancel: () => resolve(false),
        }),
      );
      if (
        !accepted ||
        !live ||
        scope !== scopeSnapshot() ||
        busy.value ||
        filterSaving.value ||
        draft !==
          JSON.stringify([editing.value, editName.value, editBaseline.value])
      )
        return false;
    }
    editing.value = "";
    return true;
  } finally {
    if (live && scope === scopeSnapshot()) closing = false;
  }
}
const navigationCurrent = (scope: string) =>
  live && scope === scopeSnapshot() && !busy.value && !filterSaving.value;
async function refresh() {
  const scope = scopeSnapshot();
  if ((await beforeNavigation()) && navigationCurrent(scope)) await load();
}
onBeforeRouteLeave(beforeNavigation);
onBeforeRouteUpdate(beforeNavigation);
function beforeUnload(event: BeforeUnloadEvent) {
  if (
    busy.value ||
    filterSaving.value ||
    settingsVisible.value ||
    (editing.value && editName.value !== editBaseline.value)
  ) {
    event.preventDefault();
    event.returnValue = "";
  }
}
onMounted(() => {
  if (typeof window !== "undefined")
    window.addEventListener("beforeunload", beforeUnload);
});
onBeforeUnmount(() => {
  live = false;
  ++epoch;
  ++sequence;
  ++operation;
  if (typeof window !== "undefined")
    window.removeEventListener("beforeunload", beforeUnload);
});
const rowKey = (row: PlanReportEntry) => `${row.kind}:${row.id}`;
const reportHref = (row: PlanReportEntry) =>
  router.resolve({
    name: "TestPlanReportDetail",
    params: { runId: row.id },
    query: { projectId: projectId.value, kind: row.kind },
  }).href;
async function openReport(row: PlanReportEntry) {
  const scope = scopeSnapshot();
  if ((await beforeNavigation()) && navigationCurrent(scope))
    await router.push(reportHref(row));
}
const query = computed(() =>
  advancedConditions.value === undefined
    ? applied.value
    : {
        filters: JSON.stringify({
          conditions: advancedConditions.value,
          logic: advancedLogic.value,
        }),
        kind: showType.value === "ALL" ? undefined : showType.value,
      },
);
async function load() {
  const current = ++sequence,
    scope = scopeSnapshot(),
    project = projectId.value;
  if (!project) {
    items.value = [];
    total.value = 0;
    loading.value = false;
    return;
  }
  loading.value = true;
  failed.value = false;
  try {
    const result = await planReportsApi.list(project, {
      page: page.value,
      size: size.value,
      sort: sort.value,
      direction: direction.value,
      ...query.value,
    });
    if (!live || scope !== scopeSnapshot() || current !== sequence) return;
    items.value = result.items;
    total.value = result.total;
    canRename.value = result.canRename;
    canDelete.value = result.canDelete;
  } catch (error) {
    console.error("加载计划报告列表失败", error);
    if (live && scope === scopeSnapshot() && current === sequence) {
      failed.value = true;
      items.value = [];
      total.value = 0;
      canRename.value = false;
      canDelete.value = false;
    }
  } finally {
    if (live && scope === scopeSnapshot() && current === sequence)
      loading.value = false;
  }
}
function clearBasic() {
  Object.keys(filters).forEach(
    (key) => delete filters[key as keyof typeof filters],
  );
  search.value = "";
  dates.value = undefined;
  applied.value = {};
  showType.value = "ALL";
  expanded.value = false;
}
function applyAdvanced(
  conditions: FilterCondition[] | undefined,
  logic: FilterLogic,
  viewId?: string,
) {
  if (!live || busy.value) return;
  clearBasic();
  advancedConditions.value = conditions;
  advancedLogic.value = logic;
  advancedViewId.value = viewId;
  selected.value = [];
  page.value = 1;
  void load();
}
async function apply() {
  const scope = scopeSnapshot();
  if (!(await beforeNavigation()) || !navigationCurrent(scope)) return;
  if (
    filters.min_rate !== undefined &&
    filters.max_rate !== undefined &&
    filters.min_rate > filters.max_rate
  ) {
    message.warning("最小通过率不能大于最大通过率");
    return;
  }
  advancedConditions.value = undefined;
  advancedViewId.value = undefined;
  showType.value = filters.kind || "ALL";
  applied.value = {
    ...filters,
    search: search.value.trim() || undefined,
    start_time: dates.value?.[0].format("YYYY-MM-DDTHH:mm:ss"),
    end_time: dates.value?.[1].format("YYYY-MM-DDTHH:mm:ss"),
  };
  page.value = 1;
  void load();
}
async function reset() {
  const scope = scopeSnapshot();
  if (!(await beforeNavigation()) || !navigationCurrent(scope)) return;
  clearBasic();
  advancedConditions.value = undefined;
  advancedViewId.value = undefined;
  selected.value = [];
  page.value = 1;
  void load();
}
function handleTypeEvent(event: { target: { value: string } }) {
  void changeType(event.target.value);
}
async function changeType(value: string) {
  const scope = scopeSnapshot();
  if (!(await beforeNavigation()) || !navigationCurrent(scope)) return;
  showType.value = value;
  selected.value = [];
  advancedViewId.value = undefined;
  page.value = 1;
  if (advancedConditions.value === undefined) {
    filters.kind = value === "ALL" ? undefined : value;
    applied.value = { ...applied.value, kind: filters.kind };
  }
  void load();
}
async function beginRename(row: PlanReportEntry) {
  const scope = scopeSnapshot();
  if (
    !canRename.value ||
    !(await beforeNavigation()) ||
    !navigationCurrent(scope) ||
    !canRename.value
  )
    return;
  editing.value = rowKey(row);
  editName.value = row.name;
  editBaseline.value = row.name;
}
async function cancelRename() {
  const scope = scopeSnapshot();
  if ((await beforeNavigation()) && navigationCurrent(scope))
    editing.value = "";
}
async function rename(row: PlanReportEntry) {
  if (!projectId.value || !canRename.value || busy.value || filterSaving.value)
    return;
  if (!editName.value.trim()) {
    message.warning("报告名称不能为空");
    return;
  }
  const scope = scopeSnapshot(),
    request = ++operation,
    target = projectId.value,
    name = editName.value,
    selectedKey = rowKey(row);
  busy.value = true;
  try {
    const response = await planReportsApi.rename(target, row, name);
    if (!live || scope !== scopeSnapshot() || request !== operation) return;
    if (editing.value === selectedKey && editName.value === name) {
      editing.value = "";
      editBaseline.value = response.name;
    }
    message.success("报告名称已保存");
    if (!editing.value) await load();
    else {
      items.value = items.value.map((item) =>
        rowKey(item) === selectedKey ? { ...item, name: response.name } : item,
      );
      editBaseline.value = response.name;
    }
  } catch (error) {
    console.error("重命名报告失败", error);
    if (live && scope === scopeSnapshot() && request === operation)
      message.error("重命名失败，草稿保留");
  } finally {
    if (live && scope === scopeSnapshot() && request === operation)
      busy.value = false;
  }
}
function confirmDelete(
  reports: { kind: ReportKind; id: string }[],
  name?: string,
) {
  const target = projectId.value,
    scope = scopeSnapshot(),
    frozen = reports.map((r) => ({ ...r }));
  if (!target || !live || busy.value || filterSaving.value || !canDelete.value)
    return;
  const confirmation = Modal.confirm({
    title: name
      ? `删除报告“${name}”？`
      : `删除选中的 ${frozen.length} 条报告？`,
    content: "删除后报告分享链接失效，执行历史和结果快照保留。",
    okText: "删除",
    okType: "danger",
    cancelText: "取消",
    async onOk() {
      if (
        !live ||
        scope !== scopeSnapshot() ||
        busy.value ||
        filterSaving.value ||
        !(await beforeNavigation()) ||
        !navigationCurrent(scope) ||
        !canDelete.value
      )
        throw new Error("项目已切换或操作进行中");
      const request = ++operation;
      busy.value = true;
      confirmation.update({ cancelButtonProps: { disabled: true } });
      try {
        await planReportsApi.batchRemove(target, frozen);
        if (!live || scope !== scopeSnapshot() || request !== operation) return;
        selected.value = [];
        if (items.value.length === frozen.length && page.value > 1)
          page.value--;
        await load();
        if (live && scope === scopeSnapshot() && request === operation)
          message.success("报告已删除");
      } catch (error) {
        console.error("删除报告失败", error);
        if (live && scope === scopeSnapshot() && request === operation)
          message.error("删除失败，请确认执行已结束及操作权限");
        throw error;
      } finally {
        confirmation.update({ cancelButtonProps: { disabled: false } });
        if (live && scope === scopeSnapshot() && request === operation)
          busy.value = false;
      }
    },
  });
}
function selectionChanged(keys: (string | number)[]) {
  if (!busy.value && !filterSaving.value) selected.value = keys.map(String);
}
function deleteOne(row: PlanReportEntry) {
  confirmDelete([{ kind: row.kind, id: row.id }], row.name);
}
function deleteSelected() {
  confirmDelete(
    selected.value.map((key) => {
      const [kind, id] = key.split(":");
      return { kind: kind as ReportKind, id };
    }),
  );
}
async function exportPdf(row: PlanReportEntry) {
  const scope = scopeSnapshot();
  if (!(await beforeNavigation()) || !navigationCurrent(scope)) return;
  const request = ++operation;
  busy.value = true;
  try {
    if (row.kind === "PLAN")
      await downloadPlanFile(
        `runs/${row.id}/pdf`,
        `${row.name}.pdf`,
        () => live && scope === scopeSnapshot() && request === operation,
      );
    else {
      const blob = await planGroupApi.pdf(row.id);
      if (!live || scope !== scopeSnapshot() || request !== operation) return;
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${row.name}.pdf`;
      a.click();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
    }
  } catch (error) {
    console.error("导出列表报告失败", error);
    if (live && scope === scopeSnapshot() && request === operation)
      message.error("导出失败");
  } finally {
    if (live && scope === scopeSnapshot() && request === operation)
      busy.value = false;
  }
}
async function tableChange(
  p: { current?: number; pageSize?: number },
  _filters: unknown,
  s: { columnKey?: string; order?: string },
) {
  const scope = scopeSnapshot();
  if (!(await beforeNavigation()) || !navigationCurrent(scope)) return;
  const nextSize = p.pageSize || 20;
  if (
    nextSize !== display.value.pageSize &&
    !persist({ ...display.value, pageSize: nextSize })
  )
    return;
  page.value = p.current || 1;
  size.value = display.value.pageSize;
  sort.value =
    {
      createTime: "created_at",
      passRate: "pass_rate",
      resultStatus: "result_status",
    }[s.columnKey || ""] || "created_at";
  direction.value = s.order === "ascend" ? "asc" : "desc";
  void load();
}
watch(
  identity,
  () => {
    ++epoch;
    closing = false;
    ++sequence;
    ++operation;
    items.value = [];
    total.value = 0;
    canRename.value = false;
    canDelete.value = false;
    page.value = 1;
    selected.value = [];
    editing.value = "";
    editName.value = "";
    editBaseline.value = "";
    busy.value = false;
    filterSaving.value = false;
    settingsVisible.value = false;
    settingsError.value = "";
    display.value = readReportDisplay(localStorage, displayKey.value);
    size.value = display.value.pageSize;
    advancedConditions.value = undefined;
    advancedLogic.value = "and";
    advancedViewId.value = undefined;
    clearBasic();
    void load();
  },
  { immediate: true, flush: "sync" },
);
</script>
<style scoped>
.report-list {
  background: white;
  min-height: 100%;
  padding: 16px;
  min-width: 0;
}
.report-toolbar {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}
.report-toolbar :deep(.ant-input-search) {
  width: 240px;
}
.report-filters {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0 16px;
  background: var(--ms-page-bg);
  padding: 16px;
  margin-bottom: 16px;
}
.report-filters .ant-form-item {
  margin-bottom: 12px;
}
.date-filter {
  grid-column: span 2;
}
.date-filter :deep(.ant-picker) {
  width: 100%;
}
.filter-actions {
  align-self: end;
  margin-bottom: 12px;
}
.load-error {
  margin-bottom: 12px;
}
.report-name {
  display: flex;
  align-items: center;
  min-width: 0;
  gap: 4px;
}
.report-name > a {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
}
.report-name .rename-button {
  opacity: 0;
  flex-shrink: 0;
}
.report-name:hover .rename-button,
.rename-button:focus-visible {
  opacity: 1;
}
.batch-toolbar {
  margin-bottom: 12px;
}
@media (max-width: 768px) {
  .report-list {
    padding: 12px;
  }
  .report-toolbar :deep(.ant-input-search) {
    width: 230px;
  }
  .report-filters {
    grid-template-columns: minmax(0, 1fr);
  }
  .date-filter {
    grid-column: auto;
  }
}
</style>
