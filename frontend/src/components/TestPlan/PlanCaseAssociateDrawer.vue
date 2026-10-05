<template>
  <a-drawer
    :open="open"
    title="关联用例"
    width="min(1200px,100vw)"
    destroy-on-close
    :closable="!locked"
    :keyboard="!locked"
    :mask-closable="!locked"
    @close="close"
  >
    <a-radio-group
      v-if="!category"
      v-model:value="activeCategory"
      :disabled="locked"
      class="category-switch"
      @change="resetCategory"
    >
      <a-radio-button value="functional">功能用例</a-radio-button
      ><a-radio-button value="api">API 用例</a-radio-button
      ><a-radio-button value="scenario">API 场景</a-radio-button>
    </a-radio-group>
    <div class="associate-layout">
      <aside v-if="!advanced">
        <a-input
          :disabled="locked"
          v-model:value="moduleSearch"
          placeholder="搜索模块"
          allow-clear
          :maxlength="255"
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
                : (data?.modules || []).map((item) => item.id)
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
            allow-clear
            placeholder="等级"
            :options="
              ['P0', 'P1', 'P2', 'P3'].map((value) => ({ value, label: value }))
            "
            @change="resetPage"
          /><PlanCaseFilters
            v-if="project"
            :key="`${planId}:${activeCategory}`"
            mode="association"
            :plan-id="planId"
            :project-id="project.id"
            :project-name="project.name"
            :category="activeCategory"
            :plans="planOptions"
            :collections="[]"
            :modules="filterModules"
            :conditions="filterScope?.conditions"
            :logic="filterScope?.logic || 'and'"
            :view-id="viewId"
            :busy="locked || loading"
            @apply="applyAdvanced"
            @saving="(value) => (filterSaving = value)"
          />
          <a-button :disabled="locked" :loading="loading" @click="load"
            >刷新</a-button
          >
        </div>
        <a-alert
          v-if="failed"
          type="error"
          message="关联用例列表加载失败，请重试"
          show-icon
        />
        <a-table
          v-else
          :data-source="data?.items || []"
          :columns="columns"
          row-key="id"
          size="small"
          :loading="loading"
          :pagination="pagination"
          :scroll="{ x: 780, y: 390 }"
          :row-selection="rowSelection"
          @change="tableChange"
        >
          <template #bodyCell="{ column, record }"
            ><template v-if="column.key === 'name'"
              ><a
                v-if="activeCategory !== 'functional'"
                @click="nativeCaseId = record.id"
                >{{ record.name }}</a
              ><template v-else>{{ record.name }}</template
              ><a-tag v-if="record.alreadyLinked" color="green"
                >已关联</a-tag
              ></template
            ><template v-else-if="column.key === 'nativeState'">{{
              nativeStateOptions(activeCategory).find(
                (o) => o.value === record.nativeState,
              )?.label || "—"
            }}</template
            ><template v-else-if="column.key === 'lastReportStatus'">{{
              nativeReportOptions.find(
                (o) => o.value === record.lastReportStatus,
              )?.label ||
              record.lastReportStatus ||
              "未执行"
            }}</template
            ><template v-else-if="column.key === 'apiChange'">{{
              record.apiChange === null
                ? "—"
                : record.apiChange
                  ? "有变更"
                  : "无变更"
            }}</template
            ><a-tag v-else-if="column.key === 'priority'">{{
              record.priority
            }}</a-tag
            ><a-space v-else-if="column.key === 'tags'" wrap
              ><a-tag v-for="tag in record.tags" :key="tag">{{
                tag
              }}</a-tag></a-space
            ></template
          >
        </a-table>
        <a-form :disabled="locked" layout="vertical" class="target-form">
          <a-form-item label="关联到测试集"
            ><a-tree-select
              v-model:value="collectionId"
              allow-clear
              placeholder="默认测试集"
              :tree-data="caseFolderTree(data?.collections || [])"
              :field-names="{ label: 'title', value: 'key' }"
          /></a-form-item>
          <a-form-item
            v-if="data?.usesTree && automatedSelected.length"
            label="自动化测试套（须包含所选自动化用例）"
            required
            ><a-select
              v-model:value="suiteId"
              allow-clear
              placeholder="选择当前计划测试套"
              :options="
                compatibleSuites.map((item) => ({
                  value: item.id,
                  label: item.name,
                }))
              "
          /></a-form-item>
        </a-form>
        <a-alert
          v-if="selected.size && !data?.usesTree && automatedSelected.length"
          type="info"
          show-icon
          message="自动化用例需在测试套中配置执行命令和节点后才能执行。"
        />
        <a-alert
          v-if="
            data?.usesTree &&
            automatedSelected.length &&
            !compatibleSuites.length
          "
          type="warning"
          show-icon
          message="当前没有包含全部已选自动化用例的测试套，请调整选择或先配置测试套。"
        />
      </main>
    </div>
    <NativeCaseConfigDrawer
      v-if="project"
      :open="!!nativeCaseId"
      :project-id="project.id"
      :case-id="nativeCaseId"
      :category="activeCategory"
      @update:open="
        (value) => {
          if (!value) nativeCaseId = '';
        }
      "
      @saving="(value) => (nativeSaving = value)"
      @saved="load"
    />
    <template #footer
      ><div class="associate-footer">
        <span>已选择 {{ selected.size }} 个用例</span
        ><a-button
          :disabled="locked || !selected.size"
          @click="selected.clear()"
          >清空选择</a-button
        ><a-space
          ><a-button :disabled="locked" @click="close">取消</a-button
          ><a-button
            type="primary"
            :loading="saving"
            :disabled="!canSave"
            @click="save"
            >关联</a-button
          ></a-space
        >
      </div></template
    >
  </a-drawer>
</template>
<script setup lang="ts">
import NativeCaseConfigDrawer from "@/components/TestCase/NativeCaseConfigDrawer.vue";
import { nativeStateOptions, nativeReportOptions } from "@/api/nativeCase";
import { computed, ref, watch } from "vue";
import { onBeforeRouteLeave, onBeforeRouteUpdate } from "vue-router";
import PlanCaseFilters from "./PlanCaseFilters.vue";
import type {
  FilterCondition,
  FilterLogic,
} from "@/components/TestCase/advancedFilter";
import type { CaseFolder } from "@/api/planCaseWorkspace";
import { message } from "ant-design-vue";
import { FolderOpenOutlined } from "@ant-design/icons-vue";
import type { TestCase } from "@/types";
import {
  planCaseWorkspaceApi,
  type PlanAssociateListing,
} from "@/api/planCaseWorkspace";
import { caseFolderTree } from "./planCaseFolders";
import { mergeCaseSelection } from "./planCaseSelection";
const props = defineProps<{
    open: boolean;
    planId: string;
    canEdit: boolean;
    category?: "functional" | "api" | "scenario";
    collectionId?: string | null;
  }>(),
  emit = defineEmits<{ "update:open": [value: boolean]; associated: [] }>();
const activeCategory = ref<"functional" | "api" | "scenario">(
    props.category || "functional",
  ),
  data = ref<PlanAssociateListing>(),
  project = ref<{ id: string; name: string }>(),
  planOptions = ref<{ id: string; name: string }[]>([]),
  filterModules = ref<CaseFolder[]>([]),
  filterScope = ref<{ conditions: FilterCondition[]; logic: FilterLogic }>(),
  viewId = ref<string>(),
  filterSaving = ref(false),
  loading = ref(false),
  saving = ref(false),
  failed = ref(false),
  search = ref(""),
  moduleSearch = ref(""),
  priority = ref<string>(),
  folder = ref("all"),
  page = ref(1),
  size = ref(20),
  expanded = ref<string[]>([]),
  selected = ref(new Map<string, TestCase>()),
  collectionId = ref<string>(),
  suiteId = ref<string>();
const nativeCaseId = ref(""),
  nativeSaving = ref(false);
const locked = computed(
  () => saving.value || filterSaving.value || nativeSaving.value,
);
const advanced = computed(() => filterScope.value !== undefined);
function applyAdvanced(
  conditions: FilterCondition[] | undefined,
  logic: FilterLogic,
  id?: string,
) {
  filterScope.value =
    conditions === undefined ? undefined : { conditions, logic };
  viewId.value = id;
  search.value = "";
  priority.value = undefined;
  folder.value = "all";
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
const baseColumns = [
  { title: "ID", dataIndex: "caseCode", width: 130 },
  { title: "名称", key: "name", width: 240 },
  { title: "等级", key: "priority", width: 70 },
  { title: "标签", key: "tags", width: 150 },
  { title: "所属模块", dataIndex: "moduleName", width: 190 },
];
const columns = computed(() =>
  activeCategory.value === "functional"
    ? baseColumns
    : [
        ...baseColumns.filter((c) => c.key !== "tags"),
        {
          title: activeCategory.value === "api" ? "用例状态" : "场景状态",
          key: "nativeState",
          width: 100,
        },
        { title: "最近执行结果", key: "lastReportStatus", width: 110 },
        { title: "环境", dataIndex: "environmentLabel", width: 150 },
        ...(activeCategory.value === "api"
          ? [
              { title: "协议", dataIndex: "protocol", width: 100 },
              { title: "请求路径", dataIndex: "path", width: 200 },
              { title: "接口参数变更", key: "apiChange", width: 120 },
            ]
          : [{ title: "步骤数", dataIndex: "stepTotal", width: 80 }]),
      ],
);
const automatedSelected = computed(() =>
    Array.from(selected.value.values()).filter((item) => item.isAutomated),
  ),
  compatibleSuites = computed(() =>
    (data.value?.suites || []).filter((suite) =>
      automatedSelected.value.every((item) => suite.caseIds.includes(item.id)),
    ),
  );
const canSave = computed(
  () =>
    props.canEdit &&
    !locked.value &&
    !failed.value &&
    !loading.value &&
    selected.value.size > 0 &&
    selected.value.size <= 500 &&
    (!data.value?.usesTree ||
      !automatedSelected.value.length ||
      !!compatibleSuites.value.find((item) => item.id === suiteId.value)),
);
const rowSelection = computed(() => ({
  selectedRowKeys: Array.from(selected.value.keys()),
  preserveSelectedRowKeys: true,
  onChange: selectRows,
  getCheckboxProps: (row: TestCase & { alreadyLinked: boolean }) => ({
    disabled:
      locked.value ||
      loading.value ||
      (!data.value?.usesTree && row.alreadyLinked),
  }),
}));
function selectRows(keys: (string | number)[]) {
  if (locked.value || loading.value) return;
  const ids = new Set(keys.map(String));
  if (ids.size > 500) {
    message.warning("一次最多关联500个用例");
    return;
  }
  selected.value = mergeCaseSelection(
    selected.value,
    keys,
    data.value?.items || [],
  );
}
let sequence = 0;
async function load() {
  if (!props.open) return;
  const request = ++sequence;
  loading.value = true;
  failed.value = false;
  try {
    const result = await planCaseWorkspaceApi.candidates(props.planId, {
      category: activeCategory.value,
      search: search.value,
      folder: folder.value,
      priority: priority.value,
      page: page.value,
      size: size.value,
      filters:
        filterScope.value === undefined
          ? undefined
          : JSON.stringify(filterScope.value),
      mine: viewId.value === "system:my",
    });
    if (request === sequence) {
      data.value = result;
      project.value = { id: result.projectId, name: result.projectName };
      planOptions.value = result.plans;
      filterModules.value = result.modules;
      if (
        suiteId.value &&
        !compatibleSuites.value.some((item) => item.id === suiteId.value)
      )
        suiteId.value = undefined;
    }
  } catch (error) {
    console.error("加载计划关联候选用例失败", error);
    if (request === sequence) {
      data.value = undefined;
      failed.value = true;
    }
  } finally {
    if (request === sequence) loading.value = false;
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
  if (locked.value) return;
  page.value = p.current;
  size.value = p.pageSize;
  void load();
}
function resetCategory() {
  nativeCaseId.value = "";
  filterScope.value = undefined;
  viewId.value = undefined;
  selected.value.clear();
  suiteId.value = undefined;
  folder.value = "all";
  search.value = "";
  priority.value = undefined;
  resetPage();
}
function close() {
  if (locked.value) return;
  sequence++;
  emit("update:open", false);
}
async function save() {
  if (!canSave.value) return;
  saving.value = true;
  const plan = props.planId,
    category = activeCategory.value;
  try {
    await planCaseWorkspaceApi.associate(plan, {
      category: activeCategory.value,
      caseIds: Array.from(selected.value.keys()),
      collectionId: collectionId.value || null,
      suiteId: suiteId.value || null,
    });
    if (
      plan !== props.planId ||
      category !== activeCategory.value ||
      !props.open
    )
      return;
    message.success("用例已关联到计划");
    emit("associated");
    emit("update:open", false);
  } catch (error) {
    console.error("保存计划批量用例关联失败", error);
    message.error("关联失败，请核对分类、测试集和测试套范围");
  } finally {
    saving.value = false;
  }
}
watch(
  () => [props.open, props.planId, props.category],
  () => {
    sequence++;
    nativeCaseId.value = "";
    data.value = undefined;
    project.value = undefined;
    planOptions.value = [];
    filterModules.value = [];
    filterScope.value = undefined;
    viewId.value = undefined;
    selected.value.clear();
    collectionId.value = props.collectionId || undefined;
    suiteId.value = undefined;
    search.value = "";
    moduleSearch.value = "";
    priority.value = undefined;
    folder.value = "all";
    page.value = 1;
    expanded.value = [];
    activeCategory.value = props.category || "functional";
    if (props.open) void load();
  },
  { immediate: true },
);
function allowNavigation() {
  if (locked.value) {
    message.info("关联或视图保存中，请稍候");
    return false;
  }
  return true;
}
onBeforeRouteLeave(allowNavigation);
onBeforeRouteUpdate(allowNavigation);
</script>
<style scoped>
.category-switch {
  margin-bottom: 16px;
}
.associate-layout {
  display: flex;
  min-width: 0;
  min-height: 500px;
}
.associate-layout aside {
  width: 292px;
  flex-shrink: 0;
  padding-right: 16px;
  border-right: 1px solid var(--ms-border);
}
.associate-layout main {
  min-width: 0;
  flex: 1;
  padding-left: 16px;
}
.folder-all {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
}
.module-count {
  float: right;
  color: var(--primary-color);
}
.search-toolbar {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
  margin-bottom: 16px;
}
.search-toolbar :deep(.ant-input-search) {
  width: 250px;
}
.search-toolbar :deep(.ant-select) {
  width: 90px;
}
.target-form {
  margin-top: 16px;
}
.associate-footer {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}
.associate-footer :deep(.ant-space) {
  margin-left: auto;
}
@media (max-width: 768px) {
  .associate-layout {
    flex-direction: column;
  }
  .associate-layout aside {
    width: 100%;
    max-height: 220px;
    overflow: auto;
    border-right: 0;
    border-bottom: 1px solid var(--ms-border);
    padding: 0 0 12px;
  }
  .associate-layout main {
    padding: 12px 0;
  }
  .search-toolbar :deep(.ant-input-search) {
    max-width: 100%;
  }
}
</style>
