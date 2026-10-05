<template>
  <section class="review-cases">
    <aside class="case-modules">
      <div class="tree-heading">
        <strong>用例模块</strong
        ><a-button
          type="text"
          size="small"
          @click="expanded = expanded.length ? [] : modules.map((m) => m.id)"
          >{{ expanded.length ? "收起" : "展开" }}</a-button
        >
      </div>
      <a-input-search
        v-model:value="moduleSearch"
        placeholder="请输入模块名称"
        allow-clear
      />
      <a-tree
        :tree-data="tree"
        v-model:expandedKeys="expanded"
        :selected-keys="[folder]"
        block-node
        @select="selectFolder"
      >
        <template #title="node"
          ><span class="module-name">{{ node.title }}</span
          ><span class="module-count">{{ node.count }}</span></template
        >
      </a-tree>
    </aside>
    <main class="case-list">
      <div class="case-toolbar">
        <a-space wrap
          ><a-radio-group v-model:value="mode"
            ><a-radio-button value="list">列表</a-radio-button
            ><a-radio-button value="mind">脑图</a-radio-button></a-radio-group
          ><slot name="actions"
        /></a-space>
        <a-space
          ><a-input-search
            v-model:value="search"
            placeholder="通过 ID/名称/标签搜索"
            allow-clear
            @search="applySearch"
            @change="searchCleared" /><a-button
            aria-label="表格设置"
            @click="settings = true"
            ><SettingOutlined /></a-button
          ><a-button
            aria-label="刷新用例列表"
            :disabled="loading"
            @click="load()"
            ><ReloadOutlined /></a-button
        ></a-space>
      </div>
      <div class="case-filters">
        <a-select
          v-model:value="priority"
          placeholder="用例等级"
          allow-clear
          :options="priorities"
        />
        <a-select
          v-model:value="selectedStates"
          mode="multiple"
          placeholder="评审结果"
          aria-label="筛选评审结果"
          allow-clear
          :max-tag-count="1"
          :options="states"
        />
        <a-select
          v-model:value="reviewerId"
          placeholder="评审人"
          allow-clear
          show-search
          option-filter-prop="label"
          :options="people"
        />
        <a-select
          v-model:value="creatorId"
          placeholder="创建人"
          allow-clear
          show-search
          option-filter-prop="label"
          :options="people"
        />
        <a-checkbox v-model:checked="onlyMine">仅看我的评审</a-checkbox>
        <a-button type="text" @click="clearFilters">重置</a-button>
      </div>
      <div v-if="selectedCount || allSelected" class="selection-bar">
        <span v-if="selectionLoading">正在核对选择范围…</span>
        <span v-else-if="selectionError">选择范围核对失败</span>
        <span v-else
          >已选择 {{ selectedCount }} 条<span v-if="allSelected"
            >（所有页，已排除 {{ selectionInfo?.excludedCount || 0 }} 条）</span
          ></span
        >
        <a-button
          v-if="selectionError"
          type="link"
          :disabled="disabled"
          @click="previewSelection"
          >重试</a-button
        >
        <a-button type="link" :disabled="disabled" @click="clearSelection"
          >清空选择</a-button
        >
        <a-button
          v-if="canManage"
          type="link"
          :disabled="
            disabled ||
            loading ||
            selectionLoading ||
            !selectedCount ||
            !!selectionError ||
            !!error
          "
          @click="openPeople"
          >修改评审人</a-button
        >
        <a-button
          v-if="canManage"
          type="link"
          :disabled="
            disabled ||
            loading ||
            selectionLoading ||
            !selectedCount ||
            !!selectionError ||
            !!error
          "
          @click="openUnlink()"
          >取消关联</a-button
        >
        <a-button
          v-if="canManage"
          type="link"
          :disabled="disabled || loading || !canReReviewSelection"
          @click="openReReview"
          >重新提审</a-button
        >
      </div>
      <a-alert v-if="error" :message="error" type="error" show-icon
        ><template #action
          ><a-button size="small" @click="load()">重试</a-button></template
        ></a-alert
      >
      <a-spin :spinning="loading">
        <CaseMindMap
          v-if="mode === 'mind'"
          :cases="mindCases"
          readonly
          @select="selectMind"
        />
        <a-table
          v-else
          class="review-case-table"
          :columns="columns"
          :data-source="rows"
          row-key="id"
          :pagination="false"
          :row-selection="selection"
          :scroll="{ x: 950, y: 'max(240px, calc(100vh - 510px))' }"
          @change="sortChanged"
        >
          <template #bodyCell="{ column, record }">
            <a v-if="column.key === 'caseCode'" @click="openItem(record.id)">{{
              record.caseCode
            }}</a>
            <a v-else-if="column.key === 'name'" @click="openItem(record.id)">{{
              record.name
            }}</a>
            <ReviewersCell
              v-else-if="column.key === 'reviewers'"
              :reviewer-ids="record.reviewerIds || []"
              :members="members"
              :name="record.name"
              :editable="canManage"
              :disabled="disabled || loading"
              :save-reviewers="
                (people: string[]) => saveInlineReviewers(record.id, people)
              "
            />
            <a-tag
              v-else-if="column.key === 'result'"
              :color="
                record.reviewState === 'approved'
                  ? 'green'
                  : record.reviewState === 'rejected'
                    ? 'red'
                    : 'blue'
              "
              >{{ stateName(record.reviewState) }}</a-tag
            >
            <a-space v-else-if="column.key === 'operation'" :size="0"
              ><a-button
                type="link"
                :disabled="disabled || loading"
                @click="openItem(record.id)"
                >{{ record.canVote ? "评审" : "查看" }}</a-button
              ><a-button
                v-if="canManage"
                type="link"
                :disabled="disabled || loading"
                @click="openUnlink([record.id])"
                >取消关联</a-button
              ></a-space
            >
          </template>
        </a-table>
      </a-spin>
      <div v-if="mode === 'list'" class="case-pagination">
        <a-pagination
          :current="page"
          :page-size="display.pageSize"
          :total="total"
          :show-size-changer="false"
          :show-total="(n: number) => `共 ${n} 条`"
          @change="changePage"
        />
      </div>
      <p v-else-if="total > rows.length" class="mind-limit">
        当前脑图显示前 {{ rows.length }} 条，共 {{ total }} 条；请进一步筛选。
      </p>
    </main>
    <a-modal
      destroy-on-close
      :open="peopleOpen"
      title="修改评审人"
      :width="480"
      :footer="null"
      :closable="!managementSaving"
      :mask-closable="!managementSaving"
      :keyboard="!managementSaving"
      @cancel="peopleOpen = false"
    >
      <a-alert
        v-if="managementError"
        :message="managementError"
        type="error"
        show-icon
      />
      <a-form layout="vertical"
        ><a-form-item label="选择评审人" required>
          <a-select
            v-model:value="draftPeople"
            mode="multiple"
            :options="people"
            show-search
            option-filter-prop="label"
            :disabled="managementSaving"
            placeholder="请选择评审人"
          /> </a-form-item
      ></a-form>
      <div class="management-footer">
        <a-space
          ><a-switch
            v-model:checked="appendPeople"
            size="small"
            :disabled="managementSaving"
            aria-label="追加评审人" /><span>追加</span
          ><a-tooltip title="开启：新增评审人；关闭：更新评审人"
            ><QuestionCircleOutlined /></a-tooltip></a-space
        ><a-space
          ><a-button :disabled="managementSaving" @click="peopleOpen = false"
            >取消</a-button
          ><a-button
            type="primary"
            :loading="managementSaving"
            :disabled="!draftPeople.length"
            @click="savePeople"
            >保存</a-button
          ></a-space
        >
      </div>
    </a-modal>
    <a-modal
      destroy-on-close
      :open="unlinkOpen"
      title="确认取消关联关系吗？"
      :width="480"
      :closable="!managementSaving"
      :mask-closable="!managementSaving"
      :keyboard="!managementSaving"
      :confirm-loading="managementSaving"
      :cancel-button-props="{ disabled: managementSaving }"
      ok-text="确认"
      cancel-text="取消"
      @cancel="unlinkOpen = false"
      @ok="saveUnlink"
    >
      <a-alert
        v-if="managementError"
        :message="managementError"
        type="error"
        show-icon
      />
      <p>取消后，再次关联，评审结果为：未评审</p>
      <p>已选择 {{ pendingCount }} 条用例</p>
    </a-modal>
    <a-modal
      destroy-on-close
      :open="reReviewOpen"
      :title="`重新提审（已选择 ${pendingCount} 条用例）`"
      :width="680"
      :closable="!managementSaving"
      :mask-closable="false"
      :keyboard="!managementSaving"
      :confirm-loading="managementSaving"
      :cancel-button-props="{ disabled: managementSaving }"
      :ok-button-props="{ disabled: reReviewReason.length > 10000 }"
      ok-text="重新提审"
      cancel-text="取消"
      @cancel="reReviewOpen = false"
      @ok="saveReReview"
    >
      <p>评审理由</p>
      <CaseRichText
        v-model="reReviewReason"
        :disabled="managementSaving"
        label="重新提审理由"
      />
      <p v-if="reReviewReason.length > 10000" class="reason-error">
        评审理由不能超过10000字符
      </p>
      <a-alert
        v-if="managementError"
        :message="managementError"
        type="error"
        show-icon
      />
    </a-modal>
    <TableDisplaySettings
      :open="settings"
      :definitions="definitions"
      :columns="display.columns"
      :page-size="display.pageSize"
      :include-descendants="display.includeDescendants"
      @close="closeSettings"
      @page-size-change="setPageSize"
      @descendants-change="setDescendants"
    />
  </section>
</template>
<script setup lang="ts">
import { ref, computed, watch, onBeforeUnmount, reactive, h } from "vue";
import { message } from "ant-design-vue";
import { useWindowSize } from "@vueuse/core";
import {
  SettingOutlined,
  ReloadOutlined,
  QuestionCircleOutlined,
} from "@ant-design/icons-vue";
import {
  reviewWorkspaceApi,
  type ReviewCaseEntry,
  type ReviewItemSelection,
  type ReviewSelectionSummary,
} from "@/api/reviewWorkspace";
import type { CaseFolder } from "@/api/planCaseWorkspace";
import type { TestCase } from "@/types";
import { useUserStore } from "@/stores/user";
import { caseFolderTree } from "@/components/TestPlan/planCaseFolders";
import ReviewersCell from "./ReviewersCell.vue";
import CaseRichText from "@/components/TestCase/CaseRichText.vue";
import CaseMindMap from "@/components/TestCase/CaseMindMap.vue";
import TableDisplaySettings from "@/components/Table/TableDisplaySettings.vue";
import {
  displayStorageKey,
  readDisplay,
  type ColumnVisibility,
} from "@/components/Table/tableDisplay";
import {
  readingScope as readScope,
  selectedReviewStates,
  reviewStates,
} from "./reviewReading";
import ReviewSelectionHeader from "./ReviewSelectionHeader.vue";
import { pageExclusions, selectedPageIds } from "./reviewSelection";
const props = defineProps<{
  projectId: string;
  reviewId: string;
  members: { id: string; name: string }[];
  revision: number;
  selected: string[];
  disabled: boolean;
  canManage: boolean;
  initialScope?: unknown;
}>();
const emit = defineEmits<{
  select: [id: string];
  "update:selected": [keys: string[]];
  saving: [value: boolean];
  selectionSummary: [value: ReviewSelectionSummary];
  changed: [];
}>();
const user = useUserStore();
const { width: viewportWidth } = useWindowSize();
const definitions = [
  { key: "caseCode", title: "ID", required: true },
  { key: "name", title: "用例名称", required: true },
  { key: "priority", title: "用例等级" },
  { key: "reviewers", title: "评审人" },
  { key: "result", title: "评审结果" },
  { key: "creator", title: "创建人" },
  { key: "operation", title: "操作" },
];
const storageKey = computed(() =>
  displayStorageKey(
    String(user.user?.id || ""),
    props.projectId,
    "review-cases",
  ),
);
const display = ref(readDisplay(localStorage, storageKey.value, definitions));
const initial = props.initialScope ? readScope(props.initialScope) : undefined;
if (initial) {
  display.value.pageSize = initial.size;
  if (typeof initial.includeDescendants === "boolean")
    display.value.includeDescendants = initial.includeDescendants;
}
const rows = ref<ReviewCaseEntry[]>([]),
  modules = ref<CaseFolder[]>([]),
  total = ref(0),
  counts = ref({ all: 0, unassigned: 0 });
const page = ref(initial?.page || 1),
  folder = ref(initial?.folder || "all"),
  moduleSearch = ref(""),
  expanded = ref<string[]>([]),
  search = ref(initial?.search || ""),
  appliedSearch = ref(initial?.search || "");
const priority = ref<string | undefined>(initial?.priority),
  selectedStates = ref<string[]>(selectedReviewStates(initial || {})),
  reviewerId = ref<string | undefined>(initial?.reviewerId),
  creatorId = ref<string | undefined>(initial?.creatorId),
  onlyMine = ref(initial?.onlyMine || false);
const mode = ref("list"),
  sort = ref(initial?.sort || "caseCode"),
  order = ref(initial?.order || "asc"),
  loading = ref(false),
  error = ref(""),
  settings = ref(false);
const selectedRows = reactive(new Map<string, ReviewCaseEntry>());
const allSelected = ref(false),
  excludeIds = ref<string[]>([]),
  selectionInfo = ref<ReviewSelectionSummary>(),
  selectionLoading = ref(false),
  selectionError = ref("");
let selectionSequence = 0;
const selectedCount = computed(() =>
  allSelected.value ? selectionInfo.value?.count || 0 : props.selected.length,
);
const selectedSummary = computed<ReviewSelectionSummary>(() =>
  allSelected.value
    ? {
        count: selectedCount.value,
        excludedCount: selectionInfo.value?.excludedCount || 0,
        canVote:
          !error.value &&
          !loading.value &&
          !selectionError.value &&
          !selectionLoading.value &&
          !!selectionInfo.value?.canVote,
        canReReview:
          !error.value &&
          !loading.value &&
          !selectionError.value &&
          !selectionLoading.value &&
          !!selectionInfo.value?.canReReview,
        loading: selectionLoading.value || loading.value,
      }
    : {
        count: props.selected.length,
        excludedCount: 0,
        canVote:
          !error.value &&
          !loading.value &&
          !!props.selected.length &&
          props.selected.every((id) => selectedRows.get(id)?.canVote),
        canReReview:
          !error.value &&
          !loading.value &&
          !!props.selected.length &&
          props.selected.every((id) => selectedRows.get(id)?.canReReview),
        loading: loading.value,
      },
);
function selectionRequest(): ReviewItemSelection {
  if (!allSelected.value) return { itemIds: [...props.selected] };
  return {
    selectAll: true,
    excludeIds: [...excludeIds.value],
    condition: {
      search: appliedSearch.value,
      folder: folder.value,
      includeDescendants: display.value.includeDescendants,
      priority: priority.value,
      states: [...selectedStates.value],
      reviewerId: reviewerId.value,
      creatorId: creatorId.value,
      onlyMine: onlyMine.value,
    },
  };
}
async function previewSelection() {
  if (!allSelected.value) return;
  const sequence = ++selectionSequence,
    project = props.projectId,
    review = props.reviewId;
  selectionLoading.value = true;
  selectionError.value = "";
  selectionInfo.value = undefined;
  try {
    const info = await reviewWorkspaceApi.selection(
      project,
      review,
      selectionRequest(),
    );
    if (
      sequence === selectionSequence &&
      project === props.projectId &&
      review === props.reviewId
    )
      selectionInfo.value = info;
  } catch (error) {
    console.error("核对评审全部筛选范围失败，保留排除项", error);
    if (sequence === selectionSequence)
      selectionError.value = "选择范围核对失败，请重试";
  } finally {
    if (sequence === selectionSequence) selectionLoading.value = false;
  }
}
function chooseAll() {
  if (props.disabled || loading.value) return;
  allSelected.value = true;
  excludeIds.value = [];
  selectedRows.clear();
  emit("update:selected", []);
  void previewSelection();
}
function selectableRows() {
  return rows.value
    .filter((row) => row.canVote || props.canManage)
    .map((row) => row.id);
}
function chooseCurrent() {
  clearSelection();
  const keys = selectableRows();
  for (const row of rows.value)
    if (keys.includes(row.id)) selectedRows.set(row.id, row);
  emit("update:selected", keys);
}
function updateSelectedKeys(keys: string[]) {
  if (allSelected.value) {
    excludeIds.value = pageExclusions(excludeIds.value, selectableRows(), keys);
    void previewSelection();
    return;
  }
  if (keys.length > 10000) return void message.info("每批最多选择10000条用例");
  for (const row of rows.value)
    if (keys.includes(row.id)) selectedRows.set(row.id, row);
  for (const key of selectedRows.keys())
    if (!keys.includes(key)) selectedRows.delete(key);
  emit("update:selected", keys);
}
function togglePage() {
  const current = selectableRows(),
    selected = allSelected.value
      ? selectedPageIds(current, excludeIds.value)
      : props.selected;
  const keys = current.every((id) => selected.includes(id))
    ? selected.filter((id) => !current.includes(id))
    : [...new Set([...selected, ...current])];
  updateSelectedKeys(keys);
}
const peopleOpen = ref(false),
  unlinkOpen = ref(false),
  managementSaving = ref(false),
  managementError = ref(""),
  draftPeople = ref<string[]>([]),
  appendPeople = ref(false),
  pendingSelection = ref<ReviewItemSelection>({ itemIds: [] }),
  pendingCount = ref(0);
const reReviewOpen = ref(false),
  reReviewReason = ref("");
const canReReviewSelection = computed(() => selectedSummary.value.canReReview);
function openReReview() {
  if (!canReReviewSelection.value) return;
  pendingSelection.value = selectionRequest();
  pendingCount.value = selectedCount.value;
  reReviewReason.value = "";
  managementError.value = "";
  reReviewOpen.value = true;
}
async function saveReReview() {
  if (managementSaving.value || reReviewReason.value.length > 10000) return;
  try {
    await performManagement(() =>
      reviewWorkspaceApi.reReview(props.projectId, props.reviewId, {
        ...pendingSelection.value,
        comment: reReviewReason.value.trim(),
      }),
    );
    reReviewOpen.value = false;
    reReviewReason.value = "";
    message.success("重新提审成功");
  } catch (err) {
    console.error("重新提审未完成，保留理由和选择", err);
  }
}
function openPeople() {
  pendingSelection.value = selectionRequest();
  pendingCount.value = selectedCount.value;
  draftPeople.value = [];
  appendPeople.value = false;
  managementError.value = "";
  peopleOpen.value = true;
}
function openUnlink(ids?: string[]) {
  pendingSelection.value = ids ? { itemIds: [...ids] } : selectionRequest();
  pendingCount.value = ids?.length || selectedCount.value;
  managementError.value = "";
  unlinkOpen.value = true;
}
async function performManagement(operation: () => Promise<unknown>) {
  if (managementSaving.value || !props.canManage)
    throw new Error("当前评审不能修改关联用例");
  managementSaving.value = true;
  emit("saving", true);
  managementError.value = "";
  try {
    await operation();
    clearSelection();
    await load();
    emit("changed");
  } catch (err) {
    console.error("修改评审关联用例失败", err);
    managementError.value = "操作失败，请重试";
    throw err;
  } finally {
    managementSaving.value = false;
    emit("saving", false);
  }
}
async function saveInlineReviewers(id: string, people: string[]) {
  await performManagement(() =>
    reviewWorkspaceApi.changeItemReviewers(props.projectId, props.reviewId, {
      itemIds: [id],
      reviewerIds: people,
      append: false,
    }),
  );
  message.success("评审人已更新");
}
async function savePeople() {
  if (
    !draftPeople.value.length ||
    !pendingCount.value ||
    managementSaving.value
  )
    return;
  try {
    await performManagement(() =>
      reviewWorkspaceApi.changeItemReviewers(props.projectId, props.reviewId, {
        ...pendingSelection.value,
        reviewerIds: [...draftPeople.value],
        append: appendPeople.value,
      }),
    );
    peopleOpen.value = false;
    message.success("评审人已更新");
  } catch (err) {
    console.error("批量修改评审人未完成，保留选择", err);
  }
}
async function saveUnlink() {
  if (!pendingCount.value || managementSaving.value) return;
  try {
    await performManagement(() =>
      reviewWorkspaceApi.disassociate(
        props.projectId,
        props.reviewId,
        pendingSelection.value,
      ),
    );
    unlinkOpen.value = false;
    message.success("取消关联成功");
  } catch (err) {
    console.error("取消关联未完成，保留确认窗口", err);
  }
}
const priorities = ["P0", "P1", "P2", "P3"].map((value) => ({
  value,
  label: value,
}));
const states = reviewStates;
const stateName = (value: string) =>
  states.find((s) => s.value === value)?.label || value;
const people = computed(() =>
  props.members.map((m) => ({ value: m.id, label: m.name })),
);
const tree = computed(() => [
  { key: "all", title: "全部用例", count: counts.value.all },
  { key: "unassigned", title: "未分配模块", count: counts.value.unassigned },
  ...caseFolderTree(modules.value, moduleSearch.value),
]);
const columns = computed(() =>
  display.value.columns
    .filter((c) => c.visible)
    .map((c) => {
      const definition = definitions.find((d) => d.key === c.key)!;
      return {
        key: c.key,
        title: definition.title,
        dataIndex: c.key,
        ellipsis: c.key !== "operation",
        width: (
          {
            caseCode: 100,
            name: 150,
            priority: 100,
            reviewers: 150,
            result: 110,
            creator: 150,
            operation: 140,
          } as Record<string, number>
        )[c.key],
        sorter: ["name", "caseCode"].includes(c.key),
        sortOrder:
          c.key === sort.value
            ? ((order.value === "asc" ? "ascend" : "descend") as
                | "ascend"
                | "descend")
            : undefined,
        fixed:
          c.key === "operation" && viewportWidth.value >= 900
            ? ("right" as const)
            : undefined,
      };
    }),
);
const mindCases = computed(
  () =>
    rows.value.map((row) => ({
      ...row.snapshot,
      id: row.caseId,
      name: row.name,
      caseCode: row.caseCode,
      moduleId: row.moduleId,
      status:
        row.reviewState === "approved"
          ? "passed"
          : row.reviewState === "rejected"
            ? "failed"
            : "not_executed",
    })) as Partial<TestCase>[],
);
const selection = computed(() => ({
  selectedRowKeys: allSelected.value
    ? selectedPageIds(
        rows.value.map((row) => row.id),
        excludeIds.value,
      )
    : props.selected,
  columnWidth: 56,
  columnTitle: () =>
    h(ReviewSelectionHeader, {
      count: selectedCount.value,
      total: total.value,
      all: allSelected.value,
      excludedCount: selectionInfo.value?.excludedCount || 0,
      disabled:
        props.disabled ||
        loading.value ||
        selectionLoading.value ||
        (!total.value && !allSelected.value),
      onTogglePage: togglePage,
      onCurrent: chooseCurrent,
      onAll: chooseAll,
      onClear: clearSelection,
    }),
  preserveSelectedRowKeys: true,
  getCheckboxProps: (row: ReviewCaseEntry) => ({
    disabled:
      props.disabled ||
      loading.value ||
      selectionLoading.value ||
      (!row.canVote && !props.canManage),
  }),
  onChange: (keys: (string | number)[]) => {
    updateSelectedKeys(keys.map(String));
  },
}));
let sequence = 0;
async function load() {
  const request = ++sequence,
    p = props.projectId,
    id = props.reviewId;
  loading.value = true;
  error.value = "";
  try {
    const result = await reviewWorkspaceApi.items(p, id, {
      page: page.value,
      size: display.value.pageSize,
      folder: folder.value,
      includeDescendants: display.value.includeDescendants,
      search: appliedSearch.value,
      priority: priority.value,
      states: selectedStates.value.length
        ? selectedStates.value.join(",")
        : undefined,
      reviewerId: reviewerId.value,
      creatorId: creatorId.value,
      onlyMine: onlyMine.value,
      sort: sort.value,
      order: order.value,
      view: mode.value,
    });
    if (request !== sequence || p !== props.projectId || id !== props.reviewId)
      return;
    if (
      mode.value === "list" &&
      page.value > 1 &&
      (page.value - 1) * display.value.pageSize >= result.total
    ) {
      page.value = Math.max(
        1,
        Math.ceil(result.total / display.value.pageSize),
      );
      await load();
      return;
    }
    rows.value = result.items;
    modules.value = result.modules;
    counts.value = result.counts;
    total.value = result.total;
    for (const row of rows.value)
      if (props.selected.includes(row.id)) selectedRows.set(row.id, row);
    if (allSelected.value) await previewSelection();
  } catch (err) {
    console.error("加载评审关联用例失败", err);
    if (request === sequence) {
      rows.value = [];
      error.value = "加载用例失败，请重试";
    }
  } finally {
    if (request === sequence) loading.value = false;
  }
}
function selectFolder(keys: (string | number)[]) {
  if (keys.length) folder.value = String(keys[0]);
}
function applySearch() {
  appliedSearch.value = search.value.trim();
}
function searchCleared() {
  if (!search.value) appliedSearch.value = "";
}
function clearFilters() {
  search.value = "";
  appliedSearch.value = "";
  priority.value = reviewerId.value = creatorId.value = undefined;
  selectedStates.value = [];
  onlyMine.value = false;
}
function clearSelection() {
  ++selectionSequence;
  allSelected.value = false;
  excludeIds.value = [];
  selectionInfo.value = undefined;
  selectionLoading.value = false;
  selectionError.value = "";
  selectedRows.clear();
  emit("update:selected", []);
}
function sortChanged(_p: unknown, _f: unknown, sorter: any) {
  sort.value = sorter.order ? sorter.columnKey : "caseCode";
  order.value = sorter.order === "descend" ? "desc" : "asc";
}
function changePage(value: number) {
  page.value = value;
  void load();
}
function persist() {
  try {
    localStorage.setItem(storageKey.value, JSON.stringify(display.value));
  } catch (err) {
    console.error("保存评审表格配置失败", err);
    message.error("显示设置保存失败");
  }
}
function closeSettings(columns: ColumnVisibility[]) {
  display.value.columns = columns;
  persist();
  settings.value = false;
}
function setPageSize(value: number) {
  display.value.pageSize = value;
  persist();
}
function setDescendants(value: boolean) {
  display.value.includeDescendants = value;
  persist();
}
function openItem(id: string) {
  if (!loading.value && !props.disabled) emit("select", id);
}
function selectMind(row: Partial<TestCase>) {
  const item = rows.value.find((i) => i.caseId === row.id);
  if (item) openItem(item.id);
}
async function navigate(id: string, direction: number) {
  if (loading.value || error.value)
    return void message.info("请等待列表加载完成后再切换");
  let index = rows.value.findIndex((r) => r.id === id);
  if (index < 0)
    return void message.info("当前用例不在筛选结果中，请从列表选择");
  let target = rows.value[index + direction];
  if (!target && mode.value === "list") {
    const next = page.value + direction;
    if (next >= 1 && (next - 1) * display.value.pageSize < total.value) {
      page.value = next;
      await load();
      if (error.value) return;
      target =
        direction > 0 ? rows.value[0] : rows.value[rows.value.length - 1];
    }
  }
  if (target) emit("select", target.id);
  else message.info(direction > 0 ? "已是最后一条" : "已是第一条");
}
watch(
  [
    folder,
    appliedSearch,
    priority,
    selectedStates,
    reviewerId,
    creatorId,
    onlyMine,
    mode,
    sort,
    order,
    () => display.value.pageSize,
    () => display.value.includeDescendants,
  ],
  () => {
    page.value = 1;
    clearSelection();
    void load();
  },
);
watch(
  () => props.revision,
  () => void load(),
);
watch(
  () => props.selected,
  (keys) => {
    for (const key of selectedRows.keys())
      if (!keys.includes(key)) selectedRows.delete(key);
  },
);
let firstScope = true;
watch(
  () => props.reviewId,
  () => {
    page.value = firstScope && initial ? initial.page : 1;
    firstScope = false;
    clearSelection();
    void load();
  },
  { immediate: true },
);
watch(moduleSearch, (keyword) => {
  if (keyword) expanded.value = modules.value.map((m) => m.id);
});
onBeforeUnmount(() => {
  ++sequence;
  ++selectionSequence;
});
watch(selectedSummary, (value) => emit("selectionSummary", value), {
  immediate: true,
});
defineExpose({
  navigate,
  readingScope: () => ({
    page: page.value,
    size: display.value.pageSize,
    search: appliedSearch.value,
    folder: folder.value,
    includeDescendants: display.value.includeDescendants,
    priority: priority.value,
    states: [...selectedStates.value],
    reviewerId: reviewerId.value,
    creatorId: creatorId.value,
    onlyMine: onlyMine.value,
    sort: sort.value,
    order: order.value,
  }),
  refresh: load,
  clearSelection,
  selectionRequest,
  canReviewSelection: () => selectedSummary.value.canVote,
  selectedCaseIds: async () => {
    if (allSelected.value)
      return (
        await reviewWorkspaceApi.selectionCaseIds(
          props.projectId,
          props.reviewId,
          selectionRequest(),
        )
      ).caseIds;
    const identifiers = props.selected.map(
      (id) => selectedRows.get(id)?.caseId,
    );
    if (identifiers.some((id) => !id))
      throw new Error("选择记录已失效，请重新选择用例后重试");
    return identifiers as string[];
  },
});
</script>
<style scoped>
.reason-error {
  color: #f53f3f;
}
.review-cases {
  display: grid;
  grid-template-columns: 220px minmax(0, 1fr);
  margin-top: 16px;
  border-top: 1px solid var(--ms-border);
}
.case-modules {
  padding: 16px 16px 16px 0;
  border-right: 1px solid var(--ms-border);
  min-width: 0;
}
.tree-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}
.case-modules :deep(.ant-tree) {
  margin-top: 12px;
  max-height: calc(100vh - 408px);
  min-height: 180px;
  overflow: auto;
}
.case-modules :deep(.ant-tree-title) {
  display: flex;
  gap: 8px;
  justify-content: space-between;
}
.module-name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.module-count {
  color: var(--ms-text-muted);
}
.case-list {
  min-width: 0;
  padding: 16px 0 16px 16px;
}
.case-toolbar {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}
.case-toolbar :deep(.ant-input-search) {
  width: 230px;
}
.case-filters {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  margin: 12px 0;
}
.case-filters :deep(.ant-select) {
  width: 125px;
}
.management-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-top: 16px;
}
.selection-bar {
  background: var(--ms-primary-soft);
  padding: 4px 12px;
  margin-bottom: 8px;
}
.review-case-table :deep(.ant-space-item > .ant-btn-link) {
  padding-left: 4px;
  padding-right: 4px;
}
.case-pagination {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}
.mind-limit {
  color: var(--ms-text-secondary);
}
@media (max-width: 900px) {
  .review-cases {
    grid-template-columns: 1fr;
  }
  .case-modules {
    border-right: 0;
    border-bottom: 1px solid var(--ms-border);
    padding-right: 0;
  }
  .case-modules :deep(.ant-tree) {
    max-height: 180px;
    min-height: 0;
  }
  .case-list {
    padding-left: 0;
  }
  .review-case-table :deep(.ant-space-item > .ant-btn-link) {
    padding-left: 4px;
    padding-right: 4px;
  }
  .case-pagination {
    overflow: auto;
  }
  .case-toolbar :deep(.ant-space) {
    flex-wrap: wrap;
  }
  .case-toolbar :deep(.ant-input-search) {
    width: 200px;
  }
}
</style>
