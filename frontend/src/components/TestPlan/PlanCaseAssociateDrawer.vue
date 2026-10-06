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
    <div class="source-project">
      <span>来源项目</span>
      <a-select
        v-model:value="sourceProjectId"
        aria-label="关联来源项目"
        show-search
        option-filter-prop="label"
        :disabled="locked || projectsLoading"
        :loading="projectsLoading"
        :options="sourceProjects.map((p) => ({ value: p.id, label: p.name }))"
        @change="switchProject"
      />
      <span class="source-hint">切换项目将清空已选用例和筛选条件</span>
    </div>
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
    <a-radio-group
      v-if="activeCategory === 'api'"
      v-model:value="resourceType"
      :disabled="locked"
      class="category-switch"
      aria-label="接口关联模式"
      @change="resetCategory"
    >
      <a-radio-button value="API">关联接口</a-radio-button>
      <a-radio-button value="CASE">关联接口用例</a-radio-button>
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
          <a-checkbox
            aria-label="勾选全部关联模块"
            :checked="selection.modules?.checked('all')"
            :indeterminate="selection.modules?.halfChecked('all')"
            :disabled="moduleSelectionDisabled"
            @change="
              (event: any) => selection.checkModule('all', event.target.checked)
            "
          />
          <a-button :disabled="locked" type="text" @click="selectFolder('all')"
            >全部{{ definitionMode ? "接口" : "用例" }} ({{
              data?.counts.all || 0
            }})</a-button
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
          :disabled="moduleSelectionDisabled"
          checkable
          check-strictly
          :checked-keys="selection.modules?.treeChecked.value"
          @check="
            (_keys: unknown, info: any) =>
              selection.checkModule(String(info.node.key), info.checked)
          "
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
        <div class="folder-unassigned">
          <a-checkbox
            aria-label="勾选未分配关联模块"
            :checked="selection.modules?.checked('unassigned')"
            :indeterminate="selection.modules?.halfChecked('unassigned')"
            :disabled="moduleSelectionDisabled"
            @change="
              (event: any) =>
                selection.checkModule('unassigned', event.target.checked)
            "
          />
          <a-button
            :disabled="locked"
            type="text"
            @click="selectFolder('unassigned')"
            >未分配模块 ({{ data?.counts.unassigned || 0 }})</a-button
          >
        </div>
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
            v-if="!advanced && !definitionMode"
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
            :key="`${planId}:${activeCategory}:${sourceProjectId}:${resourceType}`"
            mode="association"
            :plan-id="planId"
            :project-id="project.id"
            :project-name="project.name"
            :category="activeCategory"
            :resource-type="definitionMode ? 'API' : 'CASE'"
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
        <a-alert
          v-if="selection.error.value"
          type="error"
          show-icon
          :message="selection.error.value"
          class="selection-feedback"
        >
          <template #action
            ><a-button :disabled="locked || loading" @click="selection.preview"
              >重试范围核对</a-button
            ></template
          >
        </a-alert>
        <a-table
          v-if="!failed"
          :key="`${activeCategory}:${resourceType}:${sourceProjectId}`"
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
                @click="
                  definitionMode
                    ? (definitionId = record.id)
                    : (nativeCaseId = record.id)
                "
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
            ><template v-else-if="column.dataIndex === 'createdAt'">{{
              record.createdAt
                ? dayjs(record.createdAt).format("YYYY-MM-DD HH:mm:ss")
                : "—"
            }}</template
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
              :disabled="!!minderDraft"
              allow-clear
              placeholder="默认测试集"
              :tree-data="caseFolderTree(data?.collections || [])"
              :field-names="{ label: 'title', value: 'key' }"
          /></a-form-item>
          <a-form-item
            v-if="data?.usesTree && automatedCount"
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
        <a-form
          v-if="activeCategory === 'functional' && syncCase && data?.usesTree"
          :disabled="locked"
          layout="vertical"
        >
          <a-form-item
            v-for="kind in ['api', 'scenario'] as const"
            :key="kind"
            v-show="selection.summary.value?.sync?.[kind].count"
            :label="`${kind === 'api' ? '接口' : '场景'}同步测试套`"
            required
          >
            <a-select
              :value="syncSuites[kind]"
              allow-clear
              :aria-label="`${kind === 'api' ? '接口' : '场景'}同步测试套`"
              placeholder="选择包含同步用例的当前计划测试套"
              :options="
                syncCompatibleSuites(kind).map((s) => ({
                  label: s.name,
                  value: s.id,
                }))
              "
              @update:value="
                (value: string | undefined) => (syncSuites[kind] = value)
              "
            />
          </a-form-item>
        </a-form>
        <a-alert
          v-if="
            selection.hasSelection.value && !data?.usesTree && automatedCount
          "
          type="info"
          show-icon
          message="自动化用例需在测试套中配置执行命令和节点后才能执行。"
        />
        <a-alert
          v-if="data?.usesTree && automatedCount && !compatibleSuites.length"
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
    <NativeDefinitionDrawer
      v-if="definitionId && sourceProjectId"
      :open="!!definitionId"
      :project-id="sourceProjectId"
      :definition-id="definitionId"
      :modules="data?.modules || []"
      @update:open="definitionId = ''"
      @saving="nativeSaving = $event"
      @saved="load"
    />
    <template #footer
      ><div class="associate-footer">
        <div v-if="activeCategory === 'functional'" class="sync-controls">
          <a-switch
            v-model:checked="syncCase"
            size="small"
            :disabled="locked || !canEdit"
            aria-label="同步添加功能用例的关联用例"
          />
          <a-tooltip title="自动添加已关联的接口用例、场景用例"
            ><span>同步添加功能用例的关联用例</span></a-tooltip
          >
          <template v-if="syncCase">
            <a-tree-select
              v-model:value="apiCaseCollectionId"
              allow-clear
              :disabled="locked || loading || failed"
              aria-label="接口同步测试集"
              placeholder="接口测试集"
              :tree-data="caseFolderTree(data?.syncCollections.api || [])"
              :field-names="{ label: 'title', value: 'key' }"
            />
            <a-tree-select
              v-model:value="apiScenarioCollectionId"
              allow-clear
              :disabled="locked || loading || failed"
              aria-label="场景同步测试集"
              placeholder="场景测试集"
              :tree-data="caseFolderTree(data?.syncCollections.scenario || [])"
              :field-names="{ label: 'title', value: 'key' }"
            />
            <span v-if="selection.summary.value?.sync"
              >同步接口 {{ selection.summary.value.sync.api.count }} 条、场景
              {{ selection.summary.value.sync.scenario.count }} 条</span
            >
          </template>
        </div>
        <span v-if="selection.loading.value">正在核对选择范围…</span>
        <span v-else-if="selection.error.value">选择范围待核对</span>
        <span v-else
          >已选择 {{ selectedResourceCount }} 个{{
            definitionMode ? "接口" : "用例"
          }}<span v-if="definitionMode"
            >，将关联 {{ selection.summary.value?.count || 0 }} 个接口用例</span
          ><span v-if="selection.selectAll.value"
            >（全选所有页，排除
            {{
              selection.summary.value?.excludedCount ??
              selection.excluded.value.length
            }}
            个）</span
          ></span
        >
        <a-button
          :disabled="locked || !selection.hasSelection.value"
          @click="selection.clear"
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
import NativeDefinitionDrawer from "@/components/TestCase/NativeDefinitionDrawer.vue";
import dayjs from "dayjs";
import NativeCaseConfigDrawer from "@/components/TestCase/NativeCaseConfigDrawer.vue";
import { nativeStateOptions, nativeReportOptions } from "@/api/nativeCase";
import { computed, h, ref, watch, toRef, reactive, nextTick } from "vue";
import { cloneDeep } from "lodash-es";
import { onBeforeRouteLeave, onBeforeRouteUpdate } from "vue-router";
import PlanCaseFilters from "./PlanCaseFilters.vue";
import type {
  FilterCondition,
  FilterLogic,
} from "@/components/TestCase/advancedFilter";
import type { CaseFolder } from "@/api/planCaseWorkspace";
import { message } from "ant-design-vue";
import { FolderOpenOutlined } from "@ant-design/icons-vue";
import type { PlanCandidateRow } from "@/api/planCaseWorkspace";
import {
  planCaseWorkspaceApi,
  type PlanAssociateListing,
  type CandidateCondition,
  type PlanAssociation,
  type CandidateSelectionPreview,
} from "@/api/planCaseWorkspace";
import { planMinderApi, type MinderSave } from "@/api/planMinder";
import { caseFolderTree } from "./planCaseFolders";
import { usePlanCandidateSelection } from "./planCandidateSelection";
import ReviewSelectionHeader from "@/components/CaseReview/ReviewSelectionHeader.vue";
const props = defineProps<{
    open: boolean;
    planId: string;
    canEdit: boolean;
    category?: "functional" | "api" | "scenario";
    collectionId?: string | null;
    minderDraft?: MinderSave;
    initialAssociation?: PlanAssociation;
  }>(),
  emit = defineEmits<{
    "update:open": [value: boolean];
    associated: [];
    staged: [request: PlanAssociation, summary: CandidateSelectionPreview];
  }>();
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
  collectionId = ref<string>(),
  suiteId = ref<string>();
const resourceType = ref<"API" | "CASE">("API");
const definitionMode = computed(
  () => activeCategory.value === "api" && resourceType.value === "API",
);
const selectedResourceCount = computed(() =>
  definitionMode.value
    ? selection.summary.value?.selectedDefinitionCount || 0
    : selection.summary.value?.count || 0,
);
const definitionId = ref("");
const sourceProjectId = ref<string>(),
  sourceProjects = ref<{ id: string; name: string }[]>([]),
  projectsLoading = ref(false);
const nativeCaseId = ref(""),
  nativeSaving = ref(false);
const syncCase = ref(false),
  apiCaseCollectionId = ref<string>(),
  apiScenarioCollectionId = ref<string>();
const syncSuites = reactive<{ api?: string; scenario?: string }>({});
const syncRequest = computed(() =>
  definitionMode.value
    ? { resourceType: "API" as const }
    : activeCategory.value === "functional" && syncCase.value
      ? {
          syncCase: true,
          apiCaseCollectionId: apiCaseCollectionId.value,
          apiScenarioCollectionId: apiScenarioCollectionId.value,
        }
      : {},
);
function resetSync() {
  syncCase.value = false;
  apiCaseCollectionId.value = apiScenarioCollectionId.value = undefined;
  syncSuites.api = syncSuites.scenario = undefined;
}
watch(syncCase, (value) => {
  if (value) {
    apiCaseCollectionId.value = data.value?.syncCollections.api[0]?.id;
    apiScenarioCollectionId.value = data.value?.syncCollections.scenario[0]?.id;
  } else {
    apiCaseCollectionId.value = apiScenarioCollectionId.value = undefined;
    syncSuites.api = syncSuites.scenario = undefined;
  }
});
const locked = computed(
  () => saving.value || filterSaving.value || nativeSaving.value,
);
const advanced = computed(() => filterScope.value !== undefined);
const appliedCondition = ref<CandidateCondition>({});
const selectablePageIds = computed(() =>
  (data.value?.items || [])
    .filter(
      (row) =>
        definitionMode.value || data.value?.usesTree || !row.alreadyLinked,
    )
    .map((row) => row.id),
);
const selection = usePlanCandidateSelection(
  toRef(props, "planId"),
  activeCategory,
  appliedCondition,
  selectablePageIds,
  {
    enabled: computed(() => !advanced.value),
    modules: computed(() => data.value?.modules || []),
    rows: computed(() =>
      (data.value?.items || []).filter(
        (row) =>
          definitionMode.value || data.value?.usesTree || !row.alreadyLinked,
      ),
    ),
  },
  sourceProjectId,
  syncRequest,
  (id, body) =>
    props.minderDraft
      ? planMinderApi.previewCandidates(id, props.minderDraft, body)
      : planCaseWorkspaceApi.previewCandidates(id, body),
);
const moduleSelectionDisabled = computed(
  () =>
    locked.value ||
    loading.value ||
    failed.value ||
    selection.loading.value ||
    !props.canEdit,
);
watch(
  locked,
  (value) => {
    selection.working.value = value;
  },
  { flush: "sync" },
);
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
  definitionMode.value
    ? [
        { title: "ID", dataIndex: "id", width: 160, ellipsis: true },
        { title: "接口名称", key: "name", width: 220 },
        { title: "请求方式", dataIndex: "method", width: 100 },
        { title: "路径", dataIndex: "path", width: 220 },
        { title: "标签", key: "tags", width: 150 },
        { title: "用例数", dataIndex: "caseTotal", width: 80 },
        { title: "创建人", dataIndex: "createdByName", width: 100 },
        { title: "创建时间", dataIndex: "createdAt", width: 180 },
      ]
    : activeCategory.value === "functional"
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
const automatedCount = computed(
    () =>
      selection.summary.value?.requiresSuiteCount ??
      selection.summary.value?.automatedCount ??
      0,
  ),
  compatibleSuites = computed(() =>
    (data.value?.suites || []).filter((suite) =>
      selection.summary.value?.compatibleSuiteIds.includes(suite.id),
    ),
  );
const canSave = computed(
  () =>
    props.canEdit &&
    !locked.value &&
    !failed.value &&
    !loading.value &&
    selection.ready.value &&
    (!data.value?.usesTree ||
      !syncCase.value ||
      (["api", "scenario"] as const).every(
        (kind) =>
          !selection.summary.value?.sync?.[kind].count ||
          syncCompatibleSuites(kind).some((s) => s.id === syncSuites[kind]),
      )) &&
    (!data.value?.usesTree ||
      !automatedCount.value ||
      !!compatibleSuites.value.find((item) => item.id === suiteId.value)),
);
function syncCompatibleSuites(kind: "api" | "scenario") {
  return (data.value?.suites || []).filter((s) =>
    selection.summary.value?.sync?.[kind].compatibleSuiteIds.includes(s.id),
  );
}
const rowSelection = computed(() => ({
  fixed: true,
  selectedRowKeys: selection.pageSelected.value,
  columnWidth: 56,
  columnTitle: () =>
    h(ReviewSelectionHeader, {
      count: selection.moduleMode.value
        ? selection.pageSelected.value.length
        : selectedResourceCount.value,
      total: selection.moduleMode.value
        ? selectablePageIds.value.length
        : data.value?.total || 0,
      all: selection.scopeAll.value,
      excludedCount: selection.moduleMode.value
        ? 0
        : selection.excluded.value.length,
      disabled:
        locked.value ||
        loading.value ||
        failed.value ||
        !props.canEdit ||
        (!selectablePageIds.value.length && !selection.hasSelection.value),
      onTogglePage: selection.togglePage,
      onCurrent: selection.current,
      onAll: selection.all,
      onClear: selection.clear,
    }),
  preserveSelectedRowKeys: true,
  onChange: selectRows,
  getCheckboxProps: (row: PlanCandidateRow) => ({
    disabled:
      locked.value ||
      loading.value ||
      !props.canEdit ||
      (!definitionMode.value && !data.value?.usesTree && row.alreadyLinked),
  }),
}));
function selectRows(keys: (string | number)[]) {
  if (locked.value || loading.value) return;
  if (keys.length > 10000) {
    message.warning("一次最多关联10000个用例");
    return;
  }
  selection.keysChanged(keys.map(String));
}
let sequence = 0;
async function load() {
  if (!props.open) return;
  const request = ++sequence;
  loading.value = true;
  failed.value = false;
  const sourceId = sourceProjectId.value;
  const condition: CandidateCondition = cloneDeep({
    search: search.value,
    folder: folder.value,
    priority: priority.value,
    filters: filterScope.value,
    mine: viewId.value === "system:my",
  });
  try {
    if (!sourceProjects.value.length) {
      projectsLoading.value = true;
      const projects = await planCaseWorkspaceApi.candidateProjects(
        props.planId,
      );
      if (request !== sequence) return;
      sourceProjects.value = projects;
      projectsLoading.value = false;
    }
    const result = await planCaseWorkspaceApi.candidates(props.planId, {
      category: activeCategory.value,
      resourceType: definitionMode.value ? "API" : "CASE",
      projectId: sourceId,
      ...condition,
      page: page.value,
      size: size.value,
      filters:
        condition.filters === undefined
          ? undefined
          : JSON.stringify(condition.filters),
    });
    if (request === sequence) {
      sourceProjectId.value = result.projectId;
      data.value = props.minderDraft
        ? {
            ...result,
            collections: props.minderDraft.points
              .filter((p) => p.category === activeCategory.value)
              .map((p) => ({
                ...p,
                parentId: p.parentId || undefined,
                count: 0,
              })),
            syncCollections: Object.fromEntries(
              (["api", "scenario"] as const).map((kind) => [
                kind,
                [
                  { id: "default", name: "默认测试集", count: 0 },
                  ...props
                    .minderDraft!.points.filter((p) => p.category === kind)
                    .map((p) => ({
                      ...p,
                      parentId: p.parentId || undefined,
                      count: 0,
                    })),
                ],
              ]),
            ) as PlanAssociateListing["syncCollections"],
          }
        : result;
      appliedCondition.value = condition;
      project.value = { id: result.projectId, name: result.projectName };
      planOptions.value = result.plans;
      filterModules.value = result.modules;
      void selection.preview();
    }
  } catch (error) {
    console.error("加载计划关联候选用例失败", error);
    if (request === sequence) {
      data.value = undefined;
      failed.value = true;
    }
  } finally {
    if (request === sequence) {
      loading.value = false;
      projectsLoading.value = false;
    }
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
function switchProject() {
  ++sequence;
  definitionId.value = "";
  nativeCaseId.value = "";
  data.value = undefined;
  project.value = undefined;
  planOptions.value = [];
  filterModules.value = [];
  expanded.value = [];
  moduleSearch.value = "";
  appliedCondition.value = {};
  resetCategory();
  console.info("计划关联来源项目已切换", {
    planId: props.planId,
    projectId: sourceProjectId.value,
  });
}
function resetCategory() {
  resetSync();
  definitionId.value = "";
  nativeCaseId.value = "";
  filterScope.value = undefined;
  viewId.value = undefined;
  selection.clear();
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
  if (!canSave.value || !selection.request.value) return;
  const body = cloneDeep(selection.request.value);
  saving.value = true;
  const plan = props.planId,
    category = activeCategory.value;
  try {
    const association: PlanAssociation = {
      ...body,
      collectionId: collectionId.value || null,
      suiteId: suiteId.value || null,
      syncApiSuiteId: syncCase.value ? syncSuites.api || null : null,
      syncScenarioSuiteId: syncCase.value ? syncSuites.scenario || null : null,
    };
    if (props.minderDraft && selection.summary.value) {
      emit("staged", association, cloneDeep(selection.summary.value));
      emit("update:open", false);
      return;
    }
    await planCaseWorkspaceApi.associate(plan, association);
    if (
      plan !== props.planId ||
      category !== activeCategory.value ||
      !props.open
    )
      return;
    message.success("用例已关联到计划");
    emit("associated");
    emit("update:open", false);
  } catch (error: any) {
    console.error("保存计划批量用例关联失败", error);
    message.error(
      typeof error.response?.data?.detail === "string"
        ? error.response.data.detail
        : "关联失败，已保留选择，请核对分类、测试集和测试套范围",
    );
  } finally {
    saving.value = false;
    if (props.open) void selection.preview();
  }
}
watch(
  () => [props.open, props.planId, props.category],
  () => {
    sequence++;
    sourceProjectId.value = undefined;
    resetSync();
    sourceProjects.value = [];
    definitionId.value = "";
    nativeCaseId.value = "";
    data.value = undefined;
    project.value = undefined;
    planOptions.value = [];
    filterModules.value = [];
    filterScope.value = undefined;
    viewId.value = undefined;
    selection.clear();
    appliedCondition.value = {};
    collectionId.value = props.collectionId || undefined;
    suiteId.value = undefined;
    search.value = "";
    moduleSearch.value = "";
    priority.value = undefined;
    folder.value = "all";
    page.value = 1;
    expanded.value = [];
    activeCategory.value = props.category || "functional";
    resourceType.value = props.initialAssociation
      ? props.initialAssociation.resourceType || "CASE"
      : "API";
    if (props.open) void restoreAndLoad();
  },
  { immediate: true },
);
async function restoreAndLoad() {
  const initial = cloneDeep(props.initialAssociation);
  const request = sequence + 1;
  if (initial) {
    sourceProjectId.value = initial.projectId;
    search.value = initial.condition?.search || "";
    priority.value = initial.condition?.priority;
    folder.value = initial.condition?.folder || "all";
    filterScope.value = initial.condition?.filters;
    viewId.value = initial.condition?.mine ? "system:my" : undefined;
  }
  await load();
  if (!initial || !props.open || failed.value || request !== sequence) return;
  await nextTick();
  if (!props.open || request !== sequence) return;
  syncCase.value = !!initial.syncCase;
  await nextTick();
  if (!props.open || request !== sequence) return;
  apiCaseCollectionId.value = initial.apiCaseCollectionId;
  apiScenarioCollectionId.value = initial.apiScenarioCollectionId;
  syncSuites.api = initial.syncApiSuiteId || undefined;
  syncSuites.scenario = initial.syncScenarioSuiteId || undefined;
  suiteId.value = initial.suiteId || undefined;
  selection.restore(initial);
}
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
.source-project {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 16px;
}
.source-project :deep(.ant-select) {
  width: 240px;
  max-width: 100%;
}
.source-hint {
  color: var(--ms-text-secondary);
  font-size: 12px;
}
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
  align-items: center;
  margin-top: 8px;
}
.folder-unassigned {
  display: flex;
  align-items: center;
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
.selection-feedback {
  margin-bottom: 12px;
}
.associate-footer {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}
.sync-controls {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
  width: 100%;
}
.sync-controls :deep(.ant-select) {
  width: 200px;
  max-width: 100%;
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
