<template>
  <section class="native-workspace">
    <aside v-if="!advanced" class="native-folders">
      <a-radio-group
        v-model:value="treeType"
        button-style="solid"
        :disabled="mutating"
        @change="chooseFolder('all')"
      >
        <a-radio-button value="COLLECTION">测试集</a-radio-button
        ><a-radio-button value="MODULE">模块</a-radio-button>
      </a-radio-group>
      <a-input
        v-model:value="folderSearch"
        :disabled="mutating"
        :placeholder="treeType === 'COLLECTION' ? '搜索测试集' : '搜索模块'"
        allow-clear
        :maxlength="255"
      />
      <div
        v-if="category === 'api' && protocolOptions.length"
        class="protocols"
      >
        <span>协议</span
        ><a-checkbox-group
          :value="protocols ?? protocolOptions"
          :options="protocolOptions"
          @change="changeProtocols"
        />
      </div>
      <div class="folder-heading">
        <a-button type="text" @click="chooseFolder('all')"
          >{{ title }} ({{ data?.counts.all || 0 }})</a-button
        >
        <a-space :size="0"
          ><a-button
            type="text"
            :aria-label="expanded.length ? '收起所有目录' : '展开所有目录'"
            @click="toggleExpanded"
            ><FolderOpenOutlined
          /></a-button>
          <a-button
            v-if="canEdit && treeType === 'COLLECTION'"
            type="text"
            aria-label="新建测试集"
            @click="newCollection"
            ><PlusOutlined /></a-button
        ></a-space>
      </div>
      <a-tree
        :tree-data="tree"
        :selected-keys="[folder]"
        :expanded-keys="expanded"
        block-node
        @expand="(keys: (string | number)[]) => (expanded = keys.map(String))"
        @select="
          (keys: (string | number)[]) => chooseFolder(String(keys[0] || 'all'))
        "
      >
        <template #title="node"
          ><span>{{ node.name }}</span
          ><span class="folder-count">{{ node.count }}</span></template
        >
      </a-tree>
      <a-button
        type="text"
        class="default-folder"
        @click="
          chooseFolder(treeType === 'COLLECTION' ? 'default' : 'unassigned')
        "
        >{{ treeType === "COLLECTION" ? "默认测试集" : "未分配模块" }} ({{
          treeType === "COLLECTION"
            ? data?.counts.default || 0
            : data?.counts.unassigned || 0
        }})</a-button
      >
    </aside>
    <div class="native-list">
      <div class="native-toolbar">
        <a-space
          ><strong>{{ folderTitle }} ({{ data?.total || 0 }})</strong
          ><a-button
            type="text"
            :aria-label="`${title}表格设置`"
            :disabled="mutating"
            @click="settingsOpen = true"
            ><SettingOutlined /></a-button
        ></a-space>
        <a-space wrap>
          <a-input-search
            v-if="!advanced"
            v-model:value="search"
            :disabled="mutating"
            placeholder="通过 ID / 名称搜索"
            allow-clear
            :maxlength="255"
            @search="reload"
          />
          <PlanCaseFilters
            :key="contextKey"
            :category="category"
            :plan-id="plan.id"
            :project-id="plan.projectId"
            :project-name="projectName"
            :collections="selectableCollections"
            :modules="data?.modules || []"
            :projects="data?.projects"
            :native-options="data?.nativeOptions"
            :conditions="filterScope?.conditions"
            :logic="filterScope?.logic || 'and'"
            :view-id="viewId"
            :busy="loading || mutating"
            @apply="applyAdvanced"
            @saving="filterSaving = $event"
          />
          <a-button
            :loading="loading"
            :aria-label="`刷新${title}`"
            :disabled="mutating"
            @click="load"
            ><ReloadOutlined
          /></a-button>
          <a-button
            v-if="canEdit"
            :disabled="mutating"
            @click="associateOpen = true"
            >{{ category === "api" ? "关联用例" : "关联场景" }}</a-button
          >
        </a-space>
      </div>
      <a-alert v-if="loadError" :message="loadError" type="error" show-icon
        ><template #action
          ><a-button @click="load">重试</a-button></template
        ></a-alert
      >
      <a-table
        :columns="columns"
        :data-source="data?.items || []"
        :loading="loading"
        row-key="id"
        size="small"
        :pagination="pagination"
        :scroll="{ x: tableWidth }"
        :row-selection="rowSelection"
        @resizeColumn="resizeColumn"
        @change="tableChange"
      >
        <template #bodyCell="{ column, record }">
          <a
            v-if="['caseCode', 'name'].includes(column.key)"
            @click="detail = record"
            >{{ record[column.key] }}</a
          >
          <a-tag v-else-if="column.key === 'priority'">{{
            record.priority
          }}</a-tag>
          <a-tag v-else-if="column.key === 'nativeState'">{{
            states.find((s) => s.value === record.nativeState)?.label ||
            record.nativeState ||
            "-"
          }}</a-tag>
          <a-tag v-else-if="column.key === 'protocol'" color="blue">{{
            record.protocol || "-"
          }}</a-tag>
          <template v-else-if="column.key === 'nativeResult'"
            ><a v-if="record.runId" @click="reportId = record.runId"
              ><a-tag :color="resultColor(record.nativeResult)">{{
                resultLabel(record.nativeResult)
              }}</a-tag></a
            ><a-tag v-else :color="resultColor(record.nativeResult)">{{
              resultLabel(record.nativeResult)
            }}</a-tag></template
          >
          <template
            v-else-if="['createdAt', 'updatedAt'].includes(column.key)"
            >{{ formatTime(record[column.key]) }}</template
          >
          <a
            v-else-if="column.key === 'bugCount'"
            @click="defectCase = record"
            >{{ record.bugCount }}</a
          >
          <template v-else-if="column.key === 'actions' && !record.grouped"
            ><a-button
              v-if="canExecute"
              type="link"
              size="small"
              :disabled="mutating || loading"
              @click="executeRange(record)"
              >执行</a-button
            ><a-popconfirm
              v-if="canEdit"
              :title="`确认取消关联 ${record.name}？`"
              description="主用例及历史报告将保留。"
              :disabled="mutating"
              @confirm="unlink([record])"
              ><a-button type="link" size="small" :disabled="mutating"
                >取消关联</a-button
              ></a-popconfirm
            ></template
          >
          <template v-else>{{ record[column.dataIndex] ?? "-" }}</template>
        </template>
      </a-table>
      <a-alert
        v-if="selection.error.value"
        :message="selection.error.value"
        type="error"
        show-icon
      >
        <template #action
          ><a-button :disabled="mutating" @click="selection.preview"
            >重试核对</a-button
          ></template
        >
      </a-alert>
      <a-alert
        v-if="executionError"
        :message="executionError"
        type="error"
        show-icon
      />
      <div v-if="selection.hasSelection.value" class="native-batch">
        <span
          >{{
            selection.loading.value
              ? "正在核对选择范围…"
              : selection.summary.value
                ? `已选 ${selection.summary.value.count} 条`
                : "选择范围待核对"
          }}<template
            v-if="selection.selectAll.value && selection.summary.value"
            >（全选所有页，已排除
            {{ selection.summary.value.excludedCount }} 条）</template
          ></span
        >
        <a-button :disabled="mutating" @click="selection.clear"
          >清空选择</a-button
        >
        <a-button
          v-if="canExecute"
          :disabled="!executeReady"
          :loading="mutating"
          @click="executeRange()"
          >执行</a-button
        >
        <a-button
          v-if="canEdit && treeType === 'COLLECTION'"
          :disabled="!batchReady"
          @click="
            moveTarget = undefined;
            mutationError = '';
            moveOpen = true;
          "
          >移动</a-button
        >
        <a-button
          v-if="canEdit"
          danger
          :disabled="!batchReady"
          @click="
            mutationError = '';
            unlinkOpen = true;
          "
          >取消关联</a-button
        >
      </div>
    </div>
  </section>
  <TableDisplaySettings
    :open="settingsOpen"
    :definitions="definitions"
    :columns="display.columns"
    :page-size="display.pageSize"
    :include-descendants="display.includeDescendants"
    :error="settingsError"
    @close="saveColumns"
    @page-size-change="setPageSize"
    @descendants-change="setDescendants"
  />
  <PlanCaseAssociateDrawer
    v-model:open="associateOpen"
    :plan-id="plan.id"
    :category="category"
    :can-edit="canEdit"
    :collection-id="
      treeType === 'COLLECTION' &&
      selectableCollections.some((c) => c.id === folder)
        ? folder
        : undefined
    "
    @associated="changed"
  />
  <a-modal
    v-model:open="moveOpen"
    title="批量移动"
    :confirm-loading="mutating"
    :closable="!mutating"
    :mask-closable="!mutating"
    :cancel-button-props="{ disabled: mutating }"
    :keyboard="!mutating"
    :ok-button-props="{ disabled: !batchReady }"
    @ok="move"
    ><a-alert
      v-if="mutationError"
      :message="mutationError"
      type="error"
      show-icon />
    <p>将 {{ selection.summary.value?.count || 0 }} 条关联移动到</p>
    <a-tree-select
      v-model:value="moveTarget"
      :disabled="mutating"
      :tree-data="moveTree"
      :field-names="{ label: 'title', value: 'key' }"
      allow-clear
      placeholder="默认测试集"
      style="width: 100%"
  /></a-modal>
  <a-modal
    v-model:open="unlinkOpen"
    title="确认取消所选关联？"
    :confirm-loading="mutating"
    :closable="!mutating"
    :mask-closable="!mutating"
    :keyboard="!mutating"
    :cancel-button-props="{ disabled: mutating }"
    :ok-button-props="{ disabled: !batchReady }"
    @ok="unlinkRange"
  >
    <p>
      取消
      {{ selection.summary.value?.count || 0 }} 条关联，主用例及历史报告将保留。
    </p>
    <a-alert
      v-if="mutationError"
      :message="mutationError"
      type="error"
      show-icon
    />
  </a-modal>
  <a-modal
    v-model:open="collectionOpen"
    title="新建测试集"
    :confirm-loading="mutating"
    :closable="!mutating"
    :mask-closable="!mutating"
    :cancel-button-props="{ disabled: mutating }"
    @ok="createCollection"
    ><a-alert
      v-if="mutationError"
      :message="mutationError"
      type="error"
      show-icon /><a-form layout="vertical"
      ><a-form-item label="名称" required
        ><a-input
          v-model:value="collectionName"
          :maxlength="255" /></a-form-item></a-form
  ></a-modal>
  <a-drawer
    :open="!!detail"
    :title="detail?.name"
    width="min(860px,100vw)"
    destroy-on-close
    @close="detail = undefined"
    ><TestCaseDetail
      v-if="detail"
      :case-id="detail.caseId"
      :project-id="detail.projectId"
      read-only
  /></a-drawer>
  <a-drawer
    :open="!!reportId"
    title="执行报告"
    width="min(100vw,1000px)"
    destroy-on-close
    @close="reportId = ''"
    ><PlanRunReport
      v-if="reportId"
      :run-id="reportId"
      :project-id="plan.projectId"
      @changed="load"
  /></a-drawer>
  <a-drawer
    :open="!!defectCase"
    title="关联缺陷"
    width="min(800px,100vw)"
    destroy-on-close
    @close="defectCase = undefined"
    ><PlanDefects
      v-if="defectCase"
      :plan-id="plan.id"
      :case-id="defectCase.caseId"
      :editable="canEdit"
      @changed="load"
  /></a-drawer>
</template>
<script setup lang="ts">
import { computed, ref, watch, onBeforeUnmount, h } from "vue";
import { onBeforeRouteLeave, onBeforeRouteUpdate, useRoute } from "vue-router";
import { useMediaQuery } from "@vueuse/core";
import { message } from "ant-design-vue";
import {
  FolderOpenOutlined,
  PlusOutlined,
  SettingOutlined,
  ReloadOutlined,
} from "@ant-design/icons-vue";
import dayjs from "dayjs";
import type { TestPlan } from "@/types";
import { useUserStore } from "@/stores/user";
import { useProjectStore } from "@/stores/project";
import {
  planCaseWorkspaceApi,
  type PlanCaseEntry,
  type PlanCaseListing,
  type NativeWorkspaceCondition,
} from "@/api/planCaseWorkspace";
import { planTreeApi } from "@/api/planTree";
import { nativeStateOptions } from "@/api/nativeCase";
import type {
  FilterCondition,
  FilterLogic,
} from "@/components/TestCase/advancedFilter";
import {
  readDisplay,
  normalizeDisplay,
  resizableColumn,
  displayStorageKey,
  type TableDisplay,
  type ColumnVisibility,
} from "@/components/Table/tableDisplay";
import { useTableColumnResize } from "@/components/Table/useTableColumnResize";
import TableDisplaySettings from "@/components/Table/TableDisplaySettings.vue";
import TestCaseDetail from "@/components/TestCase/TestCaseDetail.vue";
import PlanCaseAssociateDrawer from "./PlanCaseAssociateDrawer.vue";
import PlanCaseFilters from "./PlanCaseFilters.vue";
import PlanDefects from "./PlanDefects.vue";
import PlanRunReport from "./PlanRunReport.vue";
import ReviewSelectionHeader from "@/components/CaseReview/ReviewSelectionHeader.vue";
import { usePlanNativeSelection } from "./planNativeSelection";
import { caseFolderTree } from "./planCaseFolders";
import {
  planNativeColumns,
  planNativeResultOptions,
} from "./planNativeWorkspaceFields";
const props = defineProps<{
  plan: TestPlan;
  category: "api" | "scenario";
  canEdit: boolean;
}>();
const emit = defineEmits<{ changed: [] }>();
const user = useUserStore(),
  projects = useProjectStore();
const contextKey = computed(() => `${props.plan.id}:${props.category}`);
const title = computed(() =>
  props.category === "api" ? "API用例" : "API场景",
);
const projectName = computed(
  () =>
    projects.projects.find((p) => p.id === props.plan.projectId)?.name ||
    "当前项目",
);
const states = computed(() => nativeStateOptions(props.category));
const data = ref<PlanCaseListing>(),
  loading = ref(false),
  loadError = ref(""),
  mutating = ref(false),
  mutationError = ref(""),
  filterSaving = ref(false);
const page = ref(1),
  treeType = ref<"COLLECTION" | "MODULE">("COLLECTION"),
  folder = ref("all"),
  folderSearch = ref(""),
  search = ref(""),
  expanded = ref<string[]>([]),
  protocols = ref<string[]>();
const sort = ref("createdAt"),
  direction = ref<"asc" | "desc">("desc"),
  priorities = ref<string[]>([]),
  results = ref<string[]>([]);
const filterScope = ref<{
    conditions: FilterCondition[];
    logic: FilterLogic;
  }>(),
  viewId = ref<string>();
const advanced = computed(() => filterScope.value !== undefined);
watch(treeType, () => {
  expanded.value = [];
  folderSearch.value = "";
});
const definitionColumns = computed(() => planNativeColumns(props.category));
const definitions = computed(() =>
  definitionColumns.value.map((c) => ({
    key: c.key,
    title: c.title,
    required: c.required,
    defaultVisible: c.defaultVisible,
  })),
);
const storageKey = computed(() =>
  displayStorageKey(
    user.user?.id || "",
    props.plan.projectId,
    `plan-${props.category}`,
  ),
);
const display = ref(
    readDisplay(localStorage, storageKey.value, definitions.value),
  ),
  settingsOpen = ref(false),
  settingsError = ref("");
const narrow = useMediaQuery("(max-width:768px)");
const columns = computed(() => [
  ...display.value.columns
    .filter((c) => c.visible)
    .map((c) => {
      const definition = definitionColumns.value.find((d) => d.key === c.key)!;
      return {
        ...resizableColumn(definition, c),
        filters: advanced.value
          ? undefined
          : c.key === "priority"
            ? ["P0", "P1", "P2", "P3"].map((v) => ({ text: v, value: v }))
            : c.key === "nativeResult"
              ? planNativeResultOptions.map((o) => ({
                  text: o.label,
                  value: o.value,
                }))
              : undefined,
        filteredValue:
          c.key === "priority"
            ? priorities.value
            : c.key === "nativeResult"
              ? results.value
              : undefined,
        sortOrder:
          definition.sorter && c.key === sort.value
            ? direction.value === "asc"
              ? ("ascend" as const)
              : ("descend" as const)
            : null,
      };
    }),
  {
    key: "actions",
    title: "操作",
    width: 150,
    dataIndex: "actions",
    fixed: narrow.value ? undefined : ("right" as const),
  },
]);
const tableWidth = computed(() =>
  columns.value.reduce((sum, c) => sum + c.width, 50),
);
const folders = computed(() =>
  treeType.value === "COLLECTION"
    ? data.value?.collections || []
    : data.value?.modules || [],
);
const selectableCollections = computed(() =>
  (data.value?.collections || []).filter(
    (c) => !c.category || c.category === props.category,
  ),
);
const moveTree = computed(() => caseFolderTree(selectableCollections.value));
const tree = computed(() => caseFolderTree(folders.value, folderSearch.value));
const protocolOptions = computed(
  () => data.value?.nativeOptions?.protocols || [],
);
const folderTitle = computed(() =>
  folder.value === "all"
    ? title.value
    : folder.value === "default"
      ? "默认测试集"
      : folder.value === "unassigned"
        ? "未分配模块"
        : folders.value.find((c) => c.id === folder.value)?.name || title.value,
);
const query = computed<NativeWorkspaceCondition>(() => ({
  tree_type: treeType.value,
  folder: folder.value,
  search: search.value,
  protocols: protocols.value?.join(","),
  priority: priorities.value.join(","),
  result: results.value.join(","),
  include_descendants: display.value.includeDescendants,
  filters: filterScope.value,
  mine: viewId.value === "system:my",
}));
const selection = usePlanNativeSelection(
  computed(() => props.plan.id),
  computed(() => props.category),
  query,
  computed(() =>
    (data.value?.items || [])
      .filter((row) => !row.grouped)
      .map((row) => row.id),
  ),
);
const canExecute = computed(() => !!data.value?.canExecute);
const executeReady = computed(
  () =>
    selection.executeReady.value &&
    !loading.value &&
    !loadError.value &&
    !mutating.value,
);
const batchReady = computed(
  () =>
    selection.ready.value &&
    !loading.value &&
    !loadError.value &&
    !mutating.value,
);
const rowSelection = computed(() =>
  props.canEdit || canExecute.value
    ? {
        selectedRowKeys: selection.pageSelected.value,
        preserveSelectedRowKeys: true,
        columnWidth: 64,
        columnTitle: h(ReviewSelectionHeader, {
          count: selection.summary.value?.count || 0,
          total: data.value?.selectableTotal || 0,
          all: selection.selectAll.value,
          excludedCount: selection.summary.value?.excludedCount || 0,
          disabled:
            loading.value || mutating.value || !data.value?.selectableTotal,
          onTogglePage: selection.togglePage,
          onCurrent: selection.current,
          onAll: selection.all,
          onClear: selection.clear,
        }),
        onChange: selection.keysChanged,
        getCheckboxProps: (row: PlanCaseEntry) => ({
          disabled: row.grouped || mutating.value || loading.value,
        }),
      }
    : undefined,
);
const route = useRoute();
watch(
  () => route.query.tab,
  () => {
    if (!mutating.value) selection.clear();
  },
);
const pagination = computed(() => ({
  current: page.value,
  pageSize: display.value.pageSize,
  total: data.value?.total || 0,
  showSizeChanger: false,
  showTotal: (total: number) => `共 ${total} 条`,
}));
function persist(next: TableDisplay): boolean {
  try {
    const normalized = normalizeDisplay(next, definitions.value);
    localStorage.setItem(storageKey.value, JSON.stringify(normalized));
    display.value = normalized;
    settingsError.value = "";
    return true;
  } catch (error) {
    console.error("保存计划原生表格显示设置失败", error);
    settingsError.value = "显示设置保存失败，请检查浏览器存储后重试";
    message.error(settingsError.value);
    return false;
  }
}
const resizeColumn = useTableColumnResize(display, storageKey, persist);
function saveColumns(columns: ColumnVisibility[]) {
  if (persist({ ...display.value, columns })) settingsOpen.value = false;
}
function setPageSize(pageSize: number) {
  if (mutating.value) return;
  if (persist({ ...display.value, pageSize })) reload();
}
function setDescendants(includeDescendants: boolean) {
  if (mutating.value) return;
  if (persist({ ...display.value, includeDescendants })) reload();
}
watch(storageKey, () => {
  display.value = readDisplay(
    localStorage,
    storageKey.value,
    definitions.value,
  );
  settingsOpen.value = false;
});
function resultLabel(value: string) {
  return (
    planNativeResultOptions.find((o) => o.value === value)?.label ||
    value ||
    "未执行"
  );
}
function resultColor(value: string) {
  return value === "SUCCESS"
    ? "green"
    : value === "ERROR"
      ? "red"
      : value === "FAKE_ERROR"
        ? "orange"
        : "default";
}
const formatTime = (value: string) =>
  value ? dayjs(value).format("YYYY-MM-DD HH:mm:ss") : "-";
let sequence = 0;
async function load() {
  const current = ++sequence;
  loading.value = true;
  loadError.value = "";
  try {
    const response = await planCaseWorkspaceApi.list(props.plan.id, {
      category: props.category,
      tree_type: treeType.value,
      folder: folder.value,
      search: search.value,
      protocols: protocols.value?.join(","),
      priority: priorities.value.join(","),
      result: results.value.join(","),
      include_descendants: display.value.includeDescendants,
      page: page.value,
      size: display.value.pageSize,
      sort: sort.value,
      direction: direction.value,
      filters: filterScope.value
        ? JSON.stringify(filterScope.value)
        : undefined,
      mine: viewId.value === "system:my",
    });
    if (current === sequence) {
      data.value = response;
      if (selection.hasSelection.value) void selection.preview();
    }
  } catch (error) {
    console.error("加载计划原生分类工作区失败", error);
    if (current === sequence) {
      loadError.value = "列表加载失败，请重试或重置筛选";
      data.value = undefined;
    }
  } finally {
    if (current === sequence) loading.value = false;
  }
}
function reload() {
  page.value = 1;
  void load();
}
function chooseFolder(value: string) {
  if (mutating.value) return;
  folder.value = value;
  reload();
}
function changeProtocols(values: (string | number | boolean)[]) {
  if (mutating.value) return;
  protocols.value = values.map(String);
  reload();
}
function toggleExpanded() {
  expanded.value = expanded.value.length ? [] : folders.value.map((c) => c.id);
}
function tableChange(p: any, f: any, s: any) {
  if (mutating.value) return;
  page.value = p.current || 1;
  priorities.value = (f.priority || []).map(String);
  results.value = (f.nativeResult || []).map(String);
  sort.value = s?.order ? s.columnKey : "createdAt";
  direction.value = s?.order === "ascend" ? "asc" : "desc";
  void load();
}
function applyAdvanced(
  conditions: FilterCondition[] | undefined,
  logic: FilterLogic,
  id?: string,
) {
  if (mutating.value) return;
  filterScope.value =
    conditions === undefined ? undefined : { conditions, logic };
  viewId.value = id;
  folder.value = "all";
  search.value = "";
  priorities.value = [];
  results.value = [];
  protocols.value = undefined;
  expanded.value = [];
  reload();
}
const associateOpen = ref(false),
  moveOpen = ref(false),
  unlinkOpen = ref(false),
  moveTarget = ref<string>(),
  collectionOpen = ref(false),
  collectionName = ref("");
const detail = ref<PlanCaseEntry>(),
  defectCase = ref<PlanCaseEntry>(),
  reportId = ref("");
const executionError = ref("");
let executionRequest: { identity: string; requestId: string } | undefined;
async function executeRange(row?: PlanCaseEntry) {
  if (
    mutating.value ||
    loading.value ||
    !canExecute.value ||
    (!row && !executeReady.value)
  )
    return;
  const body = row
    ? { category: props.category, selectIds: [row.id] }
    : selection.request.value;
  if (!body) return;
  const identity = JSON.stringify([props.plan.id, body]);
  if (executionRequest?.identity !== identity)
    executionRequest = { identity, requestId: crypto.randomUUID() };
  mutating.value = selection.working.value = true;
  executionError.value = "";
  try {
    const run = await planCaseWorkspaceApi.runNativeRange(props.plan.id, {
      ...body,
      requestId: executionRequest.requestId,
    });
    console.info("原生计划所选实例已创建执行任务", {
      计划: props.plan.id,
      批次: run.id,
      分类: props.category,
      实际数量: run.report.total,
    });
    message.success({
      content: h("span", [
        "执行任务已创建，",
        h("a", { onClick: () => (reportId.value = run.id) }, "查看任务"),
      ]),
      duration: 5,
    });
    executionRequest = undefined;
    selection.clear();
    await changed();
  } catch (exception: any) {
    console.error("原生计划范围执行失败，保留选择及重试请求ID", exception);
    executionError.value =
      typeof exception.response?.data?.detail === "string"
        ? exception.response.data.detail
        : "创建执行任务失败，请重试；选择范围已保留";
  } finally {
    mutating.value = selection.working.value = false;
  }
}
async function changed() {
  page.value = 1;
  await load();
  emit("changed");
}
async function batch(action: "move" | "unlink", rows: PlanCaseEntry[]) {
  if (mutating.value || !rows.length) return false;
  mutating.value = selection.working.value = true;
  mutationError.value = "";
  try {
    await planCaseWorkspaceApi.batch(props.plan.id, {
      category: props.category,
      action,
      selections: rows.map((r) => ({ source: r.source, id: r.associationId })),
      collectionId: action === "move" ? moveTarget.value || null : undefined,
    });
    console.info("计划原生关联批量操作完成", {
      计划: props.plan.id,
      分类: props.category,
      操作: action,
      数量: rows.length,
    });
    selection.clear();
    await changed();
    return true;
  } catch (error) {
    console.error("计划原生关联批量操作失败，保留选择", error);
    mutationError.value = "操作失败，请重试；原选择和目标保留";
    message.error(mutationError.value);
    return false;
  } finally {
    mutating.value = selection.working.value = false;
  }
}
async function unlink(rows: PlanCaseEntry[]) {
  await batch("unlink", rows);
}
async function batchRange(action: "move" | "unlink") {
  if (!batchReady.value || !selection.request.value) return false;
  mutating.value = selection.working.value = true;
  mutationError.value = "";
  try {
    const result = await planCaseWorkspaceApi.nativeBatch(props.plan.id, {
      ...selection.request.value,
      action,
      ...(action === "move" ? { collectionId: moveTarget.value || null } : {}),
    });
    console.info("原生计划范围批量操作完成", {
      计划: props.plan.id,
      分类: props.category,
      操作: action,
      实际数量: result.updated,
    });
    selection.clear();
    await changed();
    return true;
  } catch (error) {
    console.error("原生计划范围批量操作失败，保留选择和目标", error);
    mutationError.value = "操作失败，请重试；原选择和目标保留";
    return false;
  } finally {
    mutating.value = selection.working.value = false;
  }
}
async function move() {
  if (await batchRange("move")) moveOpen.value = false;
}
async function unlinkRange() {
  if (await batchRange("unlink")) unlinkOpen.value = false;
}
function newCollection() {
  if (mutating.value) return;
  collectionName.value = "";
  mutationError.value = "";
  collectionOpen.value = true;
}
async function createCollection() {
  if (mutating.value) return;
  const name = collectionName.value.trim();
  if (!name) {
    mutationError.value = "请输入测试集名称";
    return;
  }
  mutating.value = true;
  try {
    await planTreeApi.create(props.plan.id, {
      name,
      nodeType: "point",
      category: props.category,
      parentId: selectableCollections.value.some((c) => c.id === folder.value)
        ? folder.value
        : null,
    });
    collectionOpen.value = false;
    console.info("计划原生测试集已创建", {
      计划: props.plan.id,
      分类: props.category,
      名称: name,
    });
    await changed();
  } catch (error) {
    console.error("创建计划原生测试集失败", error);
    mutationError.value = "创建失败，请重试";
  } finally {
    mutating.value = selection.working.value = false;
  }
}
const navigationGuard = () => {
  if (mutating.value || filterSaving.value) {
    message.warning("正在保存，请稍候");
    return false;
  }
};
onBeforeRouteLeave(navigationGuard);
onBeforeRouteUpdate(navigationGuard);
watch(
  contextKey,
  () => {
    sequence++;
    executionRequest = undefined;
    executionError.value = "";
    selection.clear();
    moveOpen.value = unlinkOpen.value = false;
    data.value = undefined;
    filterScope.value = undefined;
    viewId.value = undefined;
    folder.value = "all";
    treeType.value = "COLLECTION";
    search.value = "";
    protocols.value = undefined;
    priorities.value = [];
    results.value = [];
    expanded.value = [];
    page.value = 1;
    detail.value = defectCase.value = undefined;
    reportId.value = "";
    associateOpen.value = false;
    void load();
  },
  { immediate: true },
);
watch(
  () => props.plan.updatedAt,
  () => void load(),
);
onBeforeUnmount(() => {
  sequence++;
});
</script>
<style scoped>
.native-workspace {
  display: flex;
  min-height: 500px;
  background: #fff;
  border-top: 1px solid #e5e6eb;
}
.native-folders {
  width: 300px;
  flex-shrink: 0;
  padding: 16px;
  border-right: 1px solid #e5e6eb;
}
.native-folders > .ant-radio-group {
  display: flex;
  width: 100%;
  margin-bottom: 16px;
}
.native-folders :deep(.ant-radio-button-wrapper) {
  flex: 1;
  text-align: center;
}
.native-folders > .ant-input-affix-wrapper {
  margin-bottom: 12px;
}
.folder-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 12px;
}
.folder-count {
  float: right;
  color: #999;
  padding-left: 8px;
}
.default-folder {
  width: 100%;
  text-align: left;
  margin-top: 12px;
}
.protocols {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.native-list {
  min-width: 0;
  flex: 1;
  padding: 16px;
}
.native-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}
.native-toolbar :deep(.ant-input-search) {
  width: 187px;
}
.native-batch {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #fff;
  padding: 12px;
  border-top: 1px solid #e5e6eb;
  flex-wrap: wrap;
  position: sticky;
  bottom: 0;
  z-index: 5;
}
@media (max-width: 1200px) {
  .native-folders {
    width: 240px;
  }
}
@media (max-width: 768px) {
  .native-workspace {
    display: block;
  }
  .native-folders {
    width: 100%;
    border-right: 0;
    border-bottom: 1px solid #e5e6eb;
  }
  .native-list {
    padding: 16px;
  }
  .native-toolbar {
    align-items: flex-start;
  }
  .native-toolbar :deep(.ant-space) {
    flex-wrap: wrap;
  }
}
</style>
