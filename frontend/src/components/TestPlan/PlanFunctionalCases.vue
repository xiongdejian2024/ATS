<template>
  <section class="functional-workspace">
    <aside v-if="!advanced" class="case-folders">
      <a-radio-group
        v-model:value="treeType"
        class="folder-switch"
        @change="resetFolder"
        ><a-radio-button value="COLLECTION">测试集</a-radio-button
        ><a-radio-button value="MODULE">模块</a-radio-button></a-radio-group
      >
      <a-input
        v-model:value="folderSearch"
        :placeholder="treeType === 'COLLECTION' ? '搜索测试集' : '搜索模块'"
        allow-clear
        :maxlength="255"
      />
      <div class="folder-all">
        <a-button type="text" @click="chooseFolder('all')"
          >功能用例 <span>({{ data?.counts.all || 0 }})</span></a-button
        ><a-button
          type="text"
          :aria-label="expanded.length ? '收起所有目录' : '展开所有目录'"
          @click="toggleExpanded"
          ><FolderOpenOutlined
        /></a-button>
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
        ><template #title="node"
          ><span>{{ node.name }}</span
          ><span class="folder-count">{{ node.count }}</span></template
        ></a-tree
      >
      <a-button
        type="text"
        class="default-folder"
        @click="
          chooseFolder(treeType === 'COLLECTION' ? 'default' : 'unassigned')
        "
        >{{ treeType === "COLLECTION" ? "默认测试集" : "未分配模块" }}
        <span
          >({{
            treeType === "COLLECTION"
              ? data?.counts.default || 0
              : data?.counts.unassigned || 0
          }})</span
        ></a-button
      >
    </aside>
    <div class="case-list">
      <div class="case-toolbar">
        <strong
          >{{ folderTitle }} <span>({{ data?.total || 0 }})</span></strong
        ><a-space wrap
          ><a-input-search
            v-model:value="search"
            placeholder="通过 ID / 名称搜索"
            allow-clear
            :maxlength="255"
            @search="resetPage" /><a-button @click="toggleAdvanced"
            >高级筛选</a-button
          ><a-radio-group v-model:value="showType"
            ><a-radio-button value="list" aria-label="列表"
              ><UnorderedListOutlined /></a-radio-button
            ><a-radio-button value="mind" aria-label="脑图"
              ><ApartmentOutlined /></a-radio-button></a-radio-group
          ><a-button :loading="loading" aria-label="刷新功能用例" @click="load"
            ><ReloadOutlined /></a-button
        ></a-space>
      </div>
      <a-form
        v-if="advanced"
        :model="filters"
        layout="inline"
        class="advanced-filter"
        @finish="resetPage"
        ><a-form-item label="等级"
          ><a-select
            v-model:value="filters.priority"
            allow-clear
            :options="priorities"
            style="width: 95px" /></a-form-item
        ><a-form-item label="执行结果"
          ><a-select
            v-model:value="filters.result"
            allow-clear
            :options="resultOptions"
            style="width: 115px" /></a-form-item
        ><a-form-item label="执行人"
          ><a-select
            v-model:value="filters.executor"
            allow-clear
            :options="
              executors.map((item) => ({ value: item.id, label: item.name }))
            "
            style="width: 140px" /></a-form-item
        ><a-form-item label="标签"
          ><a-input
            v-model:value="filters.tag"
            style="width: 120px" /></a-form-item
        ><a-button html-type="submit" type="primary">查询</a-button
        ><a-button @click="resetFilters">重置</a-button></a-form
      >
      <a-alert
        v-if="failed"
        type="error"
        message="功能用例列表加载失败，请重试"
        show-icon
      />
      <template v-else>
        <CaseMindMap
          v-if="showType === 'mind'"
          :cases="mindCases"
          :modules="mindModules"
          readonly
          @select="selectMind"
        />
        <a-table
          v-else
          :data-source="data?.items || []"
          :columns="columns"
          :loading="loading"
          row-key="id"
          size="small"
          :pagination="pagination"
          :scroll="{ x: 1850 }"
          :row-selection="
            canEdit || data?.canExecute
              ? {
                  selectedRowKeys: selected,
                  onChange: (keys: (string | number)[]) =>
                    (selected = keys.map(String)),
                  getCheckboxProps: (row: PlanCaseEntry) => ({
                    disabled: row.grouped,
                  }),
                }
              : undefined
          "
          @change="tableChange"
        >
          <template #bodyCell="{ column, record }">
            <a
              v-if="column.key === 'caseCode'"
              @click="openExecution(record)"
              >{{ record.caseCode }}</a
            >
            <template v-else-if="column.key === 'name'"
              ><span>{{ record.name }}</span
              ><a-tag v-if="record.recycled" color="red"
                >已回收</a-tag
              ></template
            >
            <a-tag
              v-else-if="column.key === 'priority'"
              :color="
                record.priority === 'P0'
                  ? 'red'
                  : record.priority === 'P1'
                    ? 'orange'
                    : 'blue'
              "
              >{{ record.priority }}</a-tag
            >
            <a-space v-else-if="column.key === 'tags'" wrap
              ><a-tag v-for="tag in record.tags" :key="tag">{{
                tag
              }}</a-tag></a-space
            >
            <template v-else-if="column.key === 'result'">
              <a-select
                v-if="data?.canExecute && !record.grouped && !record.recycled"
                :value="record.result"
                :disabled="executing.has(record.id)"
                :options="[
                  { value: 'pending', label: '未执行' },
                  ...functionalResults,
                ]"
                style="width: 100%"
                @change="(value: unknown) => inlineResult(record, value)"
              />
              <a-tag v-else :color="resultColor(record.result)">{{
                resultLabels[record.result] || record.result
              }}</a-tag>
            </template>
            <span v-else-if="['createdAt', 'updatedAt'].includes(column.key)">{{
              formatTime(record[column.key])
            }}</span>
            <a
              v-else-if="column.key === 'bugCount'"
              @click="openDefects(record)"
              >{{ record.bugCount }}</a
            >
            <a-space v-else-if="column.key === 'actions'"
              ><a-button
                type="link"
                size="small"
                @click="openExecution(record)"
                >{{ data?.canExecute ? "执行" : "查看" }}</a-button
              ><a-popconfirm
                v-if="canEdit && !record.grouped"
                :title="`取消关联用例“${record.name}”？`"
                description="只取消本计划关联，原用例和历史执行快照保留。"
                @confirm="unlink([record])"
                ><a-button type="link" size="small"
                  >取消关联</a-button
                ></a-popconfirm
              ></a-space
            >
          </template>
        </a-table>
      </template>
      <div
        v-if="selected.length && (canEdit || data?.canExecute)"
        class="selection-toolbar"
      >
        <span>已选择 {{ selected.length }} 项</span
        ><a-button
          v-if="data?.canExecute"
          @click="openExecuteBatch"
          :disabled="selectedRows.some((row) => row.recycled || row.grouped)"
          >执行</a-button
        ><a-button v-if="canEdit" @click="openBatch('assign')"
          >修改执行人</a-button
        ><a-button
          v-if="canEdit && treeType === 'COLLECTION'"
          @click="openBatch('move')"
          >移动</a-button
        ><a-popconfirm
          v-if="canEdit"
          title="取消已选用例的计划关联？"
          @confirm="unlink(selectedRows)"
          ><a-button>取消关联</a-button></a-popconfirm
        ><a-button type="text" @click="selected = []">取消选择</a-button>
      </div>
    </div>
  </section>
  <a-modal
    v-model:open="executeBatchOpen"
    title="批量执行"
    width="min(800px,100vw)"
    :confirm-loading="executeSaving"
    :mask-closable="!executeSaving && !executeMediaUploading"
    :closable="!executeSaving && !executeMediaUploading"
    :ok-button-props="{ disabled: executeMediaUploading }"
    :cancel-button-props="{ disabled: executeSaving || executeMediaUploading }"
    ok-text="提交结果"
    @ok="executeBatch"
    ><p>已选择 {{ executeTargets.length }} 个用例</p>
    <PlanCaseExecuteForm
      v-model:result="executeResult"
      v-model:description="executeDescription"
      :disabled="executeSaving"
      :plan-id="plan.id"
      v-model:uploading="executeMediaUploading"
  /></a-modal>
  <a-modal
    v-model:open="batchOpen"
    :title="batchAction === 'assign' ? '修改执行人' : '移动到测试集'"
    :confirm-loading="saving"
    @ok="saveBatch"
    ><p>已选择 {{ selected.length }} 个关联</p>
    <a-select
      v-if="batchAction === 'assign'"
      v-model:value="assignedTo"
      allow-clear
      placeholder="未分配"
      :options="executors.map((item) => ({ value: item.id, label: item.name }))"
      style="width: 100%" /><a-tree-select
      v-else
      v-model:value="collectionId"
      allow-clear
      placeholder="默认测试集"
      :tree-data="caseFolderTree(data?.collections || [])"
      :field-names="{ label: 'title', value: 'key' }"
      style="width: 100%"
  /></a-modal>
  <a-drawer
    v-model:open="defectsOpen"
    title="关联缺陷"
    width="min(800px,100vw)"
    destroy-on-close
    ><PlanDefects
      v-if="current && defectsOpen"
      :plan-id="plan.id"
      :case-id="current.caseId"
      :editable="canEdit"
      @changed="load"
  /></a-drawer>
</template>
<script setup lang="ts">
import { ref, computed, reactive, watch } from "vue";
import {
  onBeforeRouteLeave,
  onBeforeRouteUpdate,
  useRoute,
  useRouter,
} from "vue-router";
import { message } from "ant-design-vue";
import {
  FolderOpenOutlined,
  UnorderedListOutlined,
  ApartmentOutlined,
  ReloadOutlined,
} from "@ant-design/icons-vue";
import dayjs from "dayjs";
import type { TestPlan, TestCase } from "@/types";
import {
  planCaseWorkspaceApi,
  type PlanCaseListing,
  type PlanCaseEntry,
} from "@/api/planCaseWorkspace";
import { planTreeApi } from "@/api/planTree";
import { caseFolderTree } from "./planCaseFolders";
import CaseMindMap from "@/components/TestCase/CaseMindMap.vue";
import PlanDefects from "./PlanDefects.vue";
import PlanCaseExecuteForm from "./PlanCaseExecuteForm.vue";
import {
  functionalResults,
  functionalListingState,
} from "./functionalExecution";
const props = defineProps<{ plan: TestPlan; canEdit: boolean }>(),
  emit = defineEmits<{ changed: [] }>(),
  route = useRoute(),
  router = useRouter();
const initialListing = functionalListingState(route.query);
const data = ref<PlanCaseListing>(),
  loading = ref(false),
  failed = ref(false),
  search = ref(initialListing.search),
  folderSearch = ref(""),
  showType = ref("list"),
  advanced = ref(initialListing.advanced),
  expanded = ref<string[]>([]),
  selected = ref<string[]>([]),
  executors = ref<{ id: string; name: string }[]>([]);
const treeType = ref<"COLLECTION" | "MODULE">(
    route.query.caseTree === "MODULE" ? "MODULE" : "COLLECTION",
  ),
  folder = ref(String(route.query.caseFolder || "all"));
const filters = reactive({
    priority: initialListing.priority,
    result: initialListing.result,
    executor: initialListing.executor,
    tag: initialListing.tag,
  }),
  page = ref(initialListing.page),
  size = ref(initialListing.size),
  sort = ref(initialListing.sort),
  direction = ref(initialListing.direction);
const folders = computed(() =>
    treeType.value === "COLLECTION"
      ? data.value?.collections || []
      : data.value?.modules || [],
  ),
  tree = computed(() => caseFolderTree(folders.value, folderSearch.value));
const folderTitle = computed(() =>
  folder.value === "all"
    ? "功能用例"
    : folder.value === "default"
      ? "默认测试集"
      : folder.value === "unassigned"
        ? "未分配模块"
        : folders.value.find((item) => item.id === folder.value)?.name ||
          "功能用例",
);
const pagination = computed(() => ({
  current: page.value,
  pageSize: size.value,
  total: data.value?.total || 0,
  showSizeChanger: true,
  showTotal: (total: number) => `共 ${total} 条`,
}));
const priorities = ["P0", "P1", "P2", "P3"].map((value) => ({
    value,
    label: value,
  })),
  resultLabels: Record<string, string> = {
    pending: "未执行",
    passed: "通过",
    failed: "失败",
    blocked: "阻塞",
    error: "错误",
    skipped: "跳过",
    cancelled: "已取消",
  };
const resultOptions = Object.entries(resultLabels).map(([value, label]) => ({
    value,
    label,
  })),
  resultColor = (result: string) =>
    result === "passed"
      ? "green"
      : ["failed", "error"].includes(result)
        ? "red"
        : "default";
const formatTime = (value: string) =>
  value ? dayjs(value).format("YYYY-MM-DD HH:mm:ss") : "-";
const columns = computed(() => [
  {
    title: "ID",
    key: "caseCode",
    dataIndex: "caseCode",
    width: 100,
    sorter: true,
  },
  {
    title: "用例名称",
    key: "name",
    dataIndex: "name",
    width: 180,
    sorter: true,
  },
  { title: "测试集", dataIndex: "collectionName", width: 150 },
  { title: "等级", key: "priority", width: 150 },
  { title: "标签", key: "tags", width: 140 },
  { title: "创建时间", key: "createdAt", width: 200, sorter: true },
  { title: "更新时间", key: "updatedAt", width: 200, sorter: true },
  { title: "执行结果", key: "result", width: 150 },
  { title: "所属模块", dataIndex: "moduleName", width: 200 },
  { title: "缺陷数", key: "bugCount", width: 100 },
  { title: "创建人", dataIndex: "createdByName", width: 150 },
  { title: "执行人", dataIndex: "executorName", width: 150 },
  { title: "操作", key: "actions", width: 170, fixed: "right" as const },
]);
const selectedRows = computed(() =>
  (data.value?.items || []).filter((item) => selected.value.includes(item.id)),
);
const mindCases = computed(() =>
  (data.value?.items || []).map(
    (item) =>
      ({
        ...item,
        steps: (item.steps || []).map((step, index) => ({
          ...step,
          step: index + 1,
        })),
        id: item.id,
        moduleId:
          treeType.value === "COLLECTION" ? item.collectionId : item.moduleId,
        name: `[${resultLabels[item.result] || item.result}] ${item.name}`,
      }) as Partial<TestCase>,
  ),
);
const mindModules = computed(() =>
  folders.value.map((item) => ({
    id: item.id,
    name: item.name,
    parentId: item.parentId,
  })),
);
let sequence = 0;
async function load() {
  const current = ++sequence;
  loading.value = true;
  failed.value = false;
  selected.value = [];
  try {
    const result = await planCaseWorkspaceApi.list(props.plan.id, {
      category: "functional",
      tree_type: treeType.value,
      folder: folder.value,
      search: search.value,
      ...filters,
      page: page.value,
      size: size.value,
      sort: sort.value,
      direction: direction.value,
      view: showType.value,
    });
    if (current === sequence) data.value = result;
  } catch (error) {
    console.error("加载计划功能用例列表失败", error);
    if (current === sequence) {
      data.value = undefined;
      failed.value = true;
    }
  } finally {
    if (current === sequence) loading.value = false;
  }
}
async function loadExecutors() {
  try {
    executors.value = await planTreeApi.executors(props.plan.id);
  } catch (error) {
    console.error("加载计划执行人失败", error);
  }
}
async function chooseFolder(id: string) {
  folder.value = id;
  page.value = 1;
  await router.replace({
    query: { ...route.query, caseTree: treeType.value, caseFolder: id },
  });
  await load();
}
function toggleAdvanced() {
  advanced.value = !advanced.value;
  if (advanced.value) void chooseFolder("all");
}
function resetFolder() {
  folderSearch.value = "";
  expanded.value = [];
  void chooseFolder("all");
}
function toggleExpanded() {
  expanded.value = expanded.value.length
    ? []
    : folders.value.map((item) => item.id);
}
function resetPage() {
  page.value = 1;
  void load();
}
function resetFilters() {
  Object.assign(filters, {
    priority: undefined,
    result: undefined,
    executor: undefined,
    tag: "",
  });
  search.value = "";
  resetPage();
}
function tableChange(p: any, _filters: any, sorter: any) {
  page.value = p.current;
  size.value = p.pageSize;
  if (sorter?.columnKey) {
    sort.value = String(sorter.columnKey);
    direction.value = sorter.order === "ascend" ? "asc" : "desc";
  }
  void load();
}
const defectsOpen = ref(false),
  current = ref<PlanCaseEntry>();
function openExecution(row: PlanCaseEntry) {
  void router.push({
    name: "PlanFunctionalExecution",
    params: { planId: props.plan.id },
    query: {
      ...route.query,
      source: row.source,
      associationId: row.associationId,
      caseId: row.caseId,
      casePage: String(page.value),
      caseSize: String(size.value),
      caseSearch: search.value,
      casePriority: filters.priority,
      caseResult: filters.result,
      caseExecutor: filters.executor,
      caseTag: filters.tag,
      caseSort: sort.value,
      caseDirection: direction.value,
      caseAdvanced: advanced.value ? "1" : "0",
    },
  });
}
const executing = ref(new Set<string>()),
  executeBatchOpen = ref(false),
  executeSaving = ref(false),
  executeMediaUploading = ref(false),
  executeResult = ref("passed"),
  executeDescription = ref(""),
  executeTargets = ref<PlanCaseEntry[]>([]);
function allowNavigation() {
  if (executeMediaUploading.value || executeSaving.value) {
    message.info("图片上传或结果提交中，请稍候");
    return false;
  }
  return true;
}
onBeforeRouteLeave(allowNavigation);
onBeforeRouteUpdate(allowNavigation);
async function inlineResult(row: PlanCaseEntry, value: unknown) {
  if (
    !data.value?.canExecute ||
    typeof value !== "string" ||
    executing.value.has(row.id)
  )
    return;
  executing.value = new Set([...executing.value, row.id]);
  try {
    await planCaseWorkspaceApi.execute(props.plan.id, {
      requestId: crypto.randomUUID(),
      selections: selection([row]),
      result: value,
    });
    await load();
    emit("changed");
    message.success("执行结果已更新");
  } catch (error) {
    console.error("更新计划行内执行结果失败", error);
    message.error("结果提交失败，请刷新检查");
    await load();
  } finally {
    const next = new Set(executing.value);
    next.delete(row.id);
    executing.value = next;
  }
}
function openExecuteBatch() {
  executeTargets.value = [...selectedRows.value];
  executeResult.value = "passed";
  executeDescription.value = "";
  executeBatchOpen.value = true;
}
async function executeBatch() {
  if (!data.value?.canExecute || executeMediaUploading.value) return;
  executeSaving.value = true;
  try {
    await planCaseWorkspaceApi.execute(props.plan.id, {
      requestId: crypto.randomUUID(),
      selections: selection(executeTargets.value),
      result: executeResult.value,
      description: executeDescription.value,
    });
    executeBatchOpen.value = false;
    await load();
    emit("changed");
    message.success("批量执行结果已提交");
  } catch (error) {
    console.error("提交计划批量执行结果失败", error);
    message.error("批量结果提交失败，请检查关联和执行状态");
  } finally {
    executeSaving.value = false;
  }
}
function openDefects(row: PlanCaseEntry) {
  current.value = row;
  defectsOpen.value = true;
}
function selectMind(row: Partial<TestCase>) {
  const item = data.value?.items.find((item) => item.id === row.id);
  if (item) openExecution(item);
}
const batchOpen = ref(false),
  batchAction = ref<"assign" | "move">("assign"),
  assignedTo = ref<string>(),
  collectionId = ref<string>(),
  saving = ref(false);
function openBatch(action: "assign" | "move") {
  batchAction.value = action;
  assignedTo.value = undefined;
  collectionId.value = undefined;
  batchOpen.value = true;
}
const selection = (rows: PlanCaseEntry[]) =>
  rows.map((item) => ({ source: item.source, id: item.associationId }));
async function saveBatch() {
  if (!props.canEdit) return;
  saving.value = true;
  try {
    await planCaseWorkspaceApi.batch(props.plan.id, {
      action: batchAction.value,
      selections: selection(selectedRows.value),
      assignedTo: assignedTo.value || null,
      collectionId: collectionId.value || null,
    });
    batchOpen.value = false;
    await load();
    emit("changed");
    message.success("计划关联已更新");
  } catch (error) {
    console.error("批量更新计划关联失败", error);
    message.error("更新失败，请核对关联范围");
  } finally {
    saving.value = false;
  }
}
async function unlink(rows: PlanCaseEntry[]) {
  if (!props.canEdit) return;
  try {
    await planCaseWorkspaceApi.batch(props.plan.id, {
      action: "unlink",
      selections: selection(rows),
    });
    await load();
    emit("changed");
    message.success("已取消计划关联");
  } catch (error) {
    console.error("取消计划用例关联失败", error);
    message.error("取消关联失败");
  }
}
watch(
  () => [route.query.caseTree, route.query.caseFolder],
  () => {
    const nextTree =
        route.query.caseTree === "MODULE" ? "MODULE" : "COLLECTION",
      nextFolder = String(route.query.caseFolder || "all");
    if (nextTree !== treeType.value || nextFolder !== folder.value) {
      treeType.value = nextTree;
      folder.value = nextFolder;
      page.value = 1;
      void load();
    }
  },
);
watch(showType, () => {
  void load();
});
watch(
  () => props.plan.id,
  () => {
    data.value = undefined;
    selected.value = [];
    executeBatchOpen.value = false;
    executeTargets.value = [];
    void load();
    void loadExecutors();
  },
  { immediate: true },
);
</script>
<style scoped>
.functional-workspace {
  display: flex;
  min-width: 0;
  background: white;
  min-height: 480px;
}
.case-folders {
  width: 300px;
  flex-shrink: 0;
  padding: 16px;
  border-right: 1px solid var(--ms-border);
}
.folder-switch {
  display: flex;
  width: 100%;
  margin-bottom: 16px;
}
.folder-switch :deep(.ant-radio-button-wrapper) {
  flex: 1;
  text-align: center;
}
.folder-all {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
}
.folder-count {
  float: right;
  color: var(--primary-color);
}
.default-folder {
  width: 100%;
  text-align: left;
}
.case-list {
  padding: 16px;
  min-width: 0;
  flex: 1;
}
.case-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}
.case-toolbar strong span {
  font-weight: 400;
  color: var(--ms-text-secondary);
}
.case-toolbar :deep(.ant-input-search) {
  width: 220px;
}
.advanced-filter {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}
.selection-toolbar {
  position: sticky;
  bottom: 0;
  background: white;
  border-top: 1px solid var(--ms-border);
  padding: 12px;
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}
@media (max-width: 768px) {
  .functional-workspace {
    flex-direction: column;
  }
  .case-folders {
    width: 100%;
    border-right: 0;
    border-bottom: 1px solid var(--ms-border);
    max-height: 250px;
    overflow: auto;
    padding: 12px;
  }
  .case-list {
    padding: 12px;
  }
  .case-list :deep(.ant-table-cell-fix-right) {
    position: static !important;
  }
}
</style>
