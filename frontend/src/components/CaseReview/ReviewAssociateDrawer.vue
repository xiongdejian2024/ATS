<template>
  <a-drawer
    :open="open"
    title="关联用例"
    width="min(1200px,100vw)"
    destroy-on-close
    @close="close"
    :mask-closable="!locked"
    :closable="!locked"
  >
    <a-radio-group :disabled="locked" value="functional" class="category"
      ><a-radio-button value="functional"
        >功能用例</a-radio-button
      ></a-radio-group
    >
    <a-alert
      v-if="saveError"
      class="save-error"
      type="error"
      :message="saveError"
      show-icon
    />
    <div class="associate-layout">
      <aside v-if="!advanced">
        <a-input
          :disabled="locked"
          v-model:value="moduleSearch"
          placeholder="搜索模块"
          allow-clear
        />
        <div class="folder-all">
          <a-button :disabled="locked" type="text" @click="selectFolder('all')"
            >全部用例 ({{ data?.counts.all || 0 }})</a-button
          ><a-button
            :disabled="locked"
            aria-label="展开或收起关联模块"
            type="text"
            @click="
              expanded = expanded.length
                ? []
                : (data?.modules || []).map((m) => m.id)
            "
            ><FolderOpenOutlined
          /></a-button>
        </div>
        <a-tree
          :disabled="locked"
          :tree-data="moduleTree"
          :selected-keys="[folder]"
          :expanded-keys="expanded"
          block-node
          @expand="(keys: (string | number)[]) => (expanded = keys.map(String))"
          @select="
            (keys: (string | number)[]) =>
              selectFolder(String(keys[0] || 'all'))
          "
          ><template #title="node"
            ><span>{{ node.name }}</span
            ><span class="module-count">{{ node.count }}</span></template
          ></a-tree
        >
        <a-button
          :disabled="locked"
          type="text"
          @click="selectFolder('unassigned')"
          >未分配模块 ({{ data?.counts.unassigned || 0 }})</a-button
        >
      </aside>
      <main>
        <div class="search-toolbar">
          <a-input-search
            v-if="!advanced"
            :disabled="locked"
            v-model:value="search"
            placeholder="通过 ID / 名称搜索"
            :maxlength="255"
            allow-clear
            @search="resetPage"
          /><a-select
            v-if="!advanced"
            :disabled="locked"
            v-model:value="priority"
            placeholder="等级"
            allow-clear
            :options="
              ['P0', 'P1', 'P2', 'P3'].map((value) => ({ value, label: value }))
            "
            @change="resetPage"
          /><a-button :disabled="locked" :loading="loading" @click="load"
            >刷新</a-button
          ><ReviewCandidateFilters
            v-if="open"
            ref="filterEditor"
            :key="identity"
            :project-id="projectId"
            :modules="data?.modules || []"
            :conditions="conditions"
            :logic="logic"
            :view-id="viewId"
            :mine="mine"
            :busy="locked"
            @apply="applyFilters"
            @saving="filterSaving = $event"
          />
          <a-button
            :disabled="locked"
            aria-label="评审关联表格设置"
            @click="settingsOpen = true"
            ><SettingOutlined
          /></a-button>
        </div>
        <a-alert
          v-if="failed"
          type="error"
          message="关联用例列表加载失败，请重试"
          show-icon
        />
        <div class="selection-toolbar">
          <span>已选择 {{ selected.size }} 个用例</span
          ><a-button
            type="link"
            :loading="selecting"
            :disabled="locked || loading || failed || !data?.total"
            @click="selectAll"
            >全选筛选结果</a-button
          ><a-button
            type="link"
            :disabled="!selected.size || locked"
            @click="selected.clear()"
            >清空选择</a-button
          >
        </div>
        <a-table
          :columns="columns"
          :data-source="data?.items || []"
          :loading="loading"
          row-key="id"
          :row-selection="rowSelection"
          :pagination="pagination"
          :scroll="{ x: 800, y: 400 }"
          @change="tableChange"
          @resize-column="resizeColumn"
          ><template #bodyCell="{ column, record }"
            ><template v-if="column.key === 'name'"
              >{{ record.name
              }}<a-tag
                v-if="
                  excluded.includes(record.id) || scopedIds.includes(record.id)
                "
                >{{ saveSelection ? "已关联" : "已选择" }}</a-tag
              ></template
            ><a-tag v-else-if="column.key === 'priority'">{{
              record.priority
            }}</a-tag
            ><a-space v-else-if="column.key === 'tags'" wrap
              ><a-tag v-for="tag in record.tags" :key="tag">{{
                tag
              }}</a-tag></a-space
            ></template
          ></a-table
        >
      </main>
    </div>
    <template #footer
      ><div class="associate-footer">
        <a-form layout="inline"
          ><a-form-item label="评审人" required
            ><a-select
              :disabled="locked"
              v-model:value="reviewers"
              mode="multiple"
              show-search
              option-filter-prop="label"
              :options="members.map((m) => ({ value: m.id, label: m.name }))"
              placeholder="请选择评审人"
              :max-tag-count="2"
              style="width: 290px" /></a-form-item></a-form
        ><a-space
          ><a-button :disabled="locked" @click="close">取消</a-button
          ><a-button
            type="primary"
            :loading="saving"
            :disabled="
              !selected.size || !reviewers.length || failed || loading || locked
            "
            @click="confirm"
            >关联 ({{ selected.size }})</a-button
          ></a-space
        >
      </div></template
    >
  </a-drawer>
  <TableDisplaySettings
    :open="settingsOpen"
    :definitions="definitions"
    :columns="display.columns"
    :page-size="display.pageSize"
    :include-descendants="true"
    :show-descendants="false"
    :show-mode="false"
    :error="settingsError"
    @close="saveColumns"
    @page-size-change="savePageSize"
  />
</template>
<script setup lang="ts">
import { ref, computed, watch, onBeforeUnmount } from "vue";
import { message } from "ant-design-vue";
import { FolderOpenOutlined, SettingOutlined } from "@ant-design/icons-vue";
import {
  reviewWorkspaceApi,
  type ReviewCandidates,
} from "@/api/reviewWorkspace";
import { caseFolderTree } from "@/components/TestPlan/planCaseFolders";
import { caseGovernanceApi, type CaseSelection } from "@/api/caseGovernance";
import { useUserStore } from "@/stores/user";
import ReviewCandidateFilters from "./ReviewCandidateFilters.vue";
import TableDisplaySettings from "@/components/Table/TableDisplaySettings.vue";
import {
  normalizeDisplay,
  readDisplay,
  displayStorageKey,
  resizableColumn,
  type TableDisplay,
  type ColumnVisibility,
} from "@/components/Table/tableDisplay";
import { useTableColumnResize } from "@/components/Table/useTableColumnResize";
import type {
  FilterCondition,
  FilterLogic,
} from "@/components/TestCase/advancedFilter";
const props = defineProps<{
  open: boolean;
  projectId: string;
  excluded: string[];
  defaultReviewers: string[];
  members: { id: string; name: string }[];
  selectionScope?: CaseSelection;
  saveSelection?: (data: {
    caseIds: string[];
    reviewerIds: string[];
  }) => Promise<void>;
}>();
const emit = defineEmits<{
  "update:open": [boolean];
  confirm: [{ caseIds: string[]; reviewerIds: string[] }];
}>();
const data = ref<ReviewCandidates>(),
  loading = ref(false),
  failed = ref(false),
  selecting = ref(false),
  saving = ref(false),
  saveError = ref(""),
  search = ref(""),
  priority = ref<string>(),
  folder = ref("all"),
  moduleSearch = ref(""),
  expanded = ref<string[]>([]),
  page = ref(1),
  size = ref(20),
  selected = ref(new Set<string>()),
  reviewers = ref<string[]>([]);
const scopedIds = ref<string[]>([]);
const user = useUserStore();
const identity = computed(() =>
  JSON.stringify([props.open, props.projectId, user.user?.id]),
);
const conditions = ref<FilterCondition[]>(),
  logic = ref<FilterLogic>("and"),
  viewId = ref<string>();
const mine = ref(false);
const advanced = computed(
  () => conditions.value !== undefined || viewId.value === "system:my",
);
const filterSaving = ref(false),
  settingsOpen = ref(false),
  settingsError = ref("");
const filterEditor = ref<{ beforeClose: () => Promise<boolean> }>();
const locked = computed(
  () => selecting.value || saving.value || filterSaving.value,
);
function filterParams() {
  return advanced.value
    ? {
        filters: { conditions: conditions.value || [], logic: logic.value },
        mine: mine.value || viewId.value === "system:my",
      }
    : {};
}
function applyFilters(
  next: FilterCondition[] | undefined,
  nextLogic: FilterLogic,
  nextView?: string,
  nextMine = false,
) {
  if (selecting.value || saving.value) return;
  conditions.value = next;
  logic.value = nextLogic;
  viewId.value = nextView;
  mine.value = nextMine || nextView === "system:my";
  resetPage();
}
const moduleTree = computed(() =>
  caseFolderTree(data.value?.modules || [], moduleSearch.value),
);
const pagination = computed(() => ({
  current: page.value,
  pageSize: size.value,
  total: data.value?.total || 0,
  showSizeChanger: true,
  showTotal: (total: number) => `共 ${total} 条`,
}));
const allColumns = [
  { title: "ID", key: "caseCode", dataIndex: "caseCode", width: 130 },
  { title: "名称", key: "name", width: 240 },
  { title: "等级", key: "priority", width: 70 },
  { title: "标签", key: "tags", width: 160 },
  { title: "所属模块", key: "moduleName", dataIndex: "moduleName", width: 200 },
];
const definitions = allColumns.map((column) => ({
  key: column.key,
  title: column.title,
  required: ["caseCode", "name"].includes(column.key),
}));
const storageKey = computed(() =>
  displayStorageKey(
    String(user.user?.id || "anonymous"),
    props.projectId,
    "review-associate",
  ),
);
const display = ref(normalizeDisplay(undefined, definitions));
const columns = computed(() =>
  display.value.columns
    .filter((preference) => preference.visible)
    .map((preference) =>
      resizableColumn(
        allColumns.find((column) => column.key === preference.key)!,
        preference,
      ),
    ),
);
function persistDisplay(next: TableDisplay) {
  try {
    const normalized = normalizeDisplay(next, definitions);
    localStorage.setItem(storageKey.value, JSON.stringify(normalized));
    display.value = normalized;
    settingsError.value = "";
    return true;
  } catch (error) {
    console.error("保存关联表格配置失败", error);
    settingsError.value = "保存失败，请重试；当前修改保留";
    return false;
  }
}
function saveColumns(next: ColumnVisibility[]) {
  if (persistDisplay({ ...display.value, columns: next }))
    settingsOpen.value = false;
}
function savePageSize(next: number) {
  if (!live || locked.value) return;
  if (persistDisplay({ ...display.value, pageSize: next })) {
    size.value = next;
    resetPage();
  }
}
const resizeColumn = useTableColumnResize(display, storageKey, persistDisplay);
watch(
  storageKey,
  () => {
    display.value = readDisplay(localStorage, storageKey.value, definitions);
    size.value = display.value.pageSize;
    settingsOpen.value = false;
    settingsError.value = "";
  },
  { immediate: true, flush: "sync" },
);
const rowSelection = computed(() => ({
  selectedRowKeys: [...selected.value],
  preserveSelectedRowKeys: true,
  getCheckboxProps: (row: { id: string }) => ({
    disabled:
      props.excluded.includes(row.id) ||
      scopedIds.value.includes(row.id) ||
      locked.value ||
      loading.value,
  }),
  onChange: (keys: (string | number)[]) => {
    if (keys.length + props.excluded.length > 10000)
      return void message.warning("一个评审最多关联10000个用例");
    selected.value = new Set(keys.map(String));
  },
}));
let sequence = 0,
  live = true;
onBeforeUnmount(() => {
  live = false;
  ++sequence;
});
async function load() {
  if (!live || !props.open || !props.projectId) return;
  const current = ++sequence,
    p = props.projectId,
    scope = identity.value;
  loading.value = true;
  failed.value = false;
  try {
    const result = await reviewWorkspaceApi.candidates(p, {
      search: search.value,
      priority: priority.value,
      folder: folder.value,
      page: page.value,
      size: size.value,
      ...filterParams(),
      ...(advanced.value
        ? { filters: JSON.stringify(filterParams().filters) }
        : {}),
    });
    if (current !== sequence || scope !== identity.value) return;
    const membership = props.selectionScope
      ? await caseGovernanceApi.selectionMembership(
          p,
          props.selectionScope,
          result.items.map((row) => row.id),
        )
      : { caseIds: [] };
    if (current === sequence && scope === identity.value && props.open) {
      data.value = result;
      scopedIds.value = membership.caseIds;
    }
  } catch (error) {
    console.error("加载评审关联候选失败", error);
    if (current === sequence && scope === identity.value) {
      data.value = undefined;
      failed.value = true;
    }
  } finally {
    if (current === sequence && scope === identity.value) loading.value = false;
  }
}
function resetPage() {
  page.value = 1;
  void load();
}
function selectFolder(id: string) {
  folder.value = id;
  resetPage();
}
function tableChange(p: { current: number; pageSize: number }) {
  if (!live || locked.value) return;
  if (
    p.pageSize !== size.value &&
    !persistDisplay({ ...display.value, pageSize: p.pageSize })
  )
    return;
  page.value = p.current;
  size.value = display.value.pageSize;
  void load();
}
async function selectAll() {
  if (!live || locked.value || loading.value || failed.value) return;
  const p = props.projectId,
    current = sequence,
    scope = identity.value;
  selecting.value = true;
  try {
    const result = await reviewWorkspaceApi.selectCandidates(p, {
      search: search.value,
      folder: folder.value,
      priority: priority.value,
      ...filterParams(),
      excludeIds: [...new Set([...props.excluded, ...selected.value])],
      ...(props.selectionScope ? { selectionScope: props.selectionScope } : {}),
    });
    if (
      !live ||
      scope !== identity.value ||
      !props.open ||
      current !== sequence
    )
      return;
    selected.value = new Set([...selected.value, ...result.caseIds]);
    console.info("评审草稿已全选筛选结果", {
      projectId: p,
      count: result.total,
    });
  } catch (error) {
    console.error("评审关联全选失败", error);
  } finally {
    if (live && scope === identity.value) selecting.value = false;
  }
}
async function close() {
  if (!live || locked.value || settingsOpen.value) return;
  const scope = identity.value;
  if (filterEditor.value && !(await filterEditor.value.beforeClose())) return;
  if (!live || locked.value || scope !== identity.value) return;
  emit("update:open", false);
}
async function confirm() {
  if (!live || !reviewers.value.length || !selected.value.size || locked.value)
    return;
  const scope = identity.value;
  if (
    settingsOpen.value ||
    (filterEditor.value && !(await filterEditor.value.beforeClose()))
  )
    return;
  if (!live || scope !== identity.value || locked.value) return;
  const data = {
    caseIds: [...selected.value],
    reviewerIds: [...reviewers.value],
  };
  saving.value = true;
  saveError.value = "";
  try {
    if (props.saveSelection) await props.saveSelection(data);
    else emit("confirm", data);
    if (!live || scope !== identity.value) return;
    emit("update:open", false);
    console.info(
      props.saveSelection ? "评审关联已保存" : "关联选择已加入评审草稿",
      { projectId: props.projectId, count: data.caseIds.length },
    );
  } catch (error) {
    console.error("保存评审关联失败，保留当前选择", error);
    if (live && scope === identity.value)
      saveError.value = "关联失败，请根据提示修正后重试，或刷新列表重新选择";
  } finally {
    if (live && scope === identity.value) saving.value = false;
  }
}
watch(
  identity,
  () => {
    ++sequence;
    selecting.value = false;
    saving.value = false;
    filterSaving.value = false;
    conditions.value = undefined;
    logic.value = "and";
    viewId.value = undefined;
    mine.value = false;
    settingsOpen.value = false;
    data.value = undefined;
    scopedIds.value = [];
    selected.value = new Set();
    reviewers.value = [...props.defaultReviewers];
    search.value = "";
    priority.value = undefined;
    folder.value = "all";
    moduleSearch.value = "";
    expanded.value = [];
    page.value = 1;
    loading.value = false;
    failed.value = false;
    saveError.value = "";
    void load();
  },
  { immediate: true, flush: "sync" },
);
</script>
<style scoped>
.save-error {
  margin-bottom: 16px;
}
.category {
  margin-bottom: 20px;
}
.associate-layout {
  display: flex;
  gap: 24px;
}
.associate-layout aside {
  width: 240px;
  flex: none;
  border-right: 1px solid #e5e6eb;
  padding-right: 16px;
}
.associate-layout main {
  flex: 1;
  min-width: 0;
}
.folder-all,
.selection-toolbar,
.associate-footer {
  display: flex;
  align-items: center;
  gap: 8px;
}
.folder-all,
.associate-footer {
  justify-content: space-between;
}
.module-count {
  float: right;
  color: #86909c;
}
.search-toolbar {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}
.search-toolbar .ant-input-search {
  flex: 1;
}
.search-toolbar .ant-select {
  width: 100px;
}
.selection-toolbar {
  margin-bottom: 8px;
}
.associate-footer {
  flex-wrap: wrap;
  gap: 16px;
}
@media (max-width: 700px) {
  .associate-layout {
    display: block;
  }
  .associate-layout aside {
    width: 100%;
    max-height: 180px;
    overflow: auto;
    border-right: 0;
    margin-bottom: 16px;
  }
  .search-toolbar {
    flex-wrap: wrap;
  }
  .associate-footer :deep(.ant-select) {
    max-width: 75vw;
  }
}
</style>
