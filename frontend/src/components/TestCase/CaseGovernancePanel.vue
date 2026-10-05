<template>
  <a-select
    :value="selectedView"
    :disabled="busy || filterSaving"
    class="case-view-select"
    aria-label="用例视图"
    option-label-prop="label"
    :dropdown-match-select-width="280"
    style="width: 145px"
    @change="selectView"
  >
    <a-select-opt-group label="系统视图">
      <a-select-option value="system:all" label="全部用例"
        >全部用例</a-select-option
      >
      <a-select-option value="system:my" label="我创建的"
        >我创建的</a-select-option
      >
      <a-select-option value="system:followed" label="我关注的"
        >我关注的</a-select-option
      >
    </a-select-opt-group>
    <a-select-opt-group label="我的视图">
      <a-select-option
        v-for="v in views"
        :key="v.id"
        :value="v.id"
        :label="v.name"
      >
        <span class="view-option-name">{{ v.name }}</span>
        <span class="view-option-actions" @mousedown.stop.prevent>
          <a-button
            type="text"
            size="small"
            :aria-label="`重命名视图 ${v.name}`"
            @click.stop="renameView(v)"
            ><EditOutlined
          /></a-button>
          <a-button
            type="text"
            size="small"
            :aria-label="`删除视图 ${v.name}`"
            @click.stop="confirmDeleteView(v)"
            ><DeleteOutlined
          /></a-button>
        </span>
      </a-select-option>
    </a-select-opt-group>
    <a-select-option
      value="action:create"
      label="新建视图"
      :disabled="views.length >= 10"
      ><PlusOutlined /> 新建视图</a-select-option
    >
  </a-select>

  <a-modal
    v-model:open="saveVisible"
    :title="editingViewId ? '重命名视图' : '新建视图'"
    :confirm-loading="busy"
    :cancel-button-props="{ disabled: busy }"
    :closable="!busy"
    :keyboard="!busy"
    :mask-closable="!busy"
    @ok="saveView"
  >
    <a-input v-model:value="viewName" placeholder="视图名称" :maxlength="255" />
  </a-modal>
  <a-modal
    v-model:open="batchVisible"
    title="批量更新所选用例"
    :confirm-loading="busy"
    :cancel-button-props="{ disabled: busy }"
    :closable="!busy"
    :keyboard="!busy"
    :mask-closable="!busy"
    @ok="batchUpdate"
  >
    <a-alert
      message="未填写的字段保持原值；每个修改后的用例会保留版本。"
      type="info"
      show-icon
    />
    <a-form :disabled="busy" layout="vertical" style="margin-top: 16px">
      <a-form-item label="优先级"
        ><a-select
          v-model:value="batchPriority"
          allow-clear
          :options="
            ['P0', 'P1', 'P2', 'P3'].map((v) => ({ label: v, value: v }))
          "
      /></a-form-item>
      <a-form-item label="替换标签"
        ><a-select
          v-model:value="batchTags"
          mode="tags"
          :disabled="clearTags"
        /><a-checkbox v-model:checked="clearTags"
          >清空标签</a-checkbox
        ></a-form-item
      >
      <a-form-item label="是否自动化"
        ><a-select
          v-model:value="batchAutomated"
          allow-clear
          :options="[
            { label: '是', value: 'yes' },
            { label: '否', value: 'no' },
          ]"
      /></a-form-item>
    </a-form>
  </a-modal>
  <a-modal
    v-model:open="issueVisible"
    title="批量关联需求 / 缺陷"
    :confirm-loading="busy"
    :cancel-button-props="{ disabled: busy }"
    :closable="!busy"
    :keyboard="!busy"
    :mask-closable="!busy"
    @ok="linkIssues"
    ><a-select
      :disabled="busy"
      v-model:value="issueId"
      show-search
      option-filter-prop="label"
      style="width: 100%"
      :options="issues.map((i) => ({ label: i.title, value: i.id }))"
      placeholder="选择当前项目需求或缺陷" /><a-alert
      style="margin-top: 16px"
      message="重复关联保持幂等；本次关联作为一个事务提交，失败保留选择范围。"
      type="info"
  /></a-modal>
  <a-modal
    v-model:open="organizeVisible"
    :title="organizeMode === 'move' ? '批量移动到模块' : '批量复制到模块'"
    :confirm-loading="busy"
    :cancel-button-props="{ disabled: busy }"
    :closable="!busy"
    :keyboard="!busy"
    :mask-closable="!busy"
    @ok="organize"
  >
    <a-form :disabled="busy" layout="vertical"
      ><a-form-item label="目标模块"
        ><a-select
          v-model:value="targetModule"
          :options="[
            { label: '未规划', value: '__unassigned__' },
            ...modules.map((m) => ({ label: m.name, value: m.id })),
          ]" /></a-form-item
    ></a-form>
    <a-alert
      :message="`操作仅限当前项目，影响所选 ${operationSelection?.count ?? selectedIds.length} 条用例。`"
      type="info"
      show-icon
    />
  </a-modal>

  <a-drawer
    v-model:open="versionsVisible"
    title="用例版本与比较"
    width="min(900px, 96vw)"
  >
    <a-spin :spinning="busy">
      <a-empty
        v-if="!versions.length"
        description="这条历史用例尚无版本；下次编辑或提交评审时会保存原始版本。"
      />
      <template v-else>
        <a-space wrap>
          <a-select
            v-model:value="beforeVersion"
            placeholder="旧版本"
            style="width: 130px"
            :options="versionOptions"
          />
          <a-select
            v-model:value="afterVersion"
            placeholder="新版本"
            style="width: 130px"
            :options="versionOptions"
          />
          <a-button @click="compare">比较版本</a-button>
        </a-space>
        <a-alert
          v-if="compared && !changes.length"
          message="两个版本内容相同"
          type="info"
          style="margin-top: 16px"
        />
        <a-table
          v-if="changes.length"
          :columns="diffColumns"
          :data-source="changes"
          :pagination="false"
          row-key="field"
          style="margin-top: 16px"
          :scroll="{ x: 600 }"
        >
          <template #bodyCell="{ column, record }">
            <pre v-if="column.key !== 'field'" class="snapshot-text">{{
              display(record[column.key])
            }}</pre>
            <span v-else>{{ fieldName(record.field) }}</span></template
          >
        </a-table>
        <a-list :data-source="versions" style="margin-top: 16px">
          <template #renderItem="{ item }"
            ><a-list-item
              ><a-list-item-meta
                :title="`v${item.version} · ${item.snapshot.name}`"
                :description="`${item.reason} · ${item.createdAt}`"
              />
              <template #actions
                ><a-button type="link" @click="previewVersion = item"
                  >查看快照</a-button
                ><a-button
                  v-if="item.id !== versions[0].id"
                  type="link"
                  @click="
                    restoreTarget = item;
                    restoreReason = '';
                    restoreVisible = true;
                  "
                  >恢复此版本</a-button
                ></template
              >
            </a-list-item></template
          >
        </a-list>
        <a-card
          v-if="previewVersion"
          :title="`版本 v${previewVersion.version} 快照`"
        >
          <pre class="snapshot-text">{{
            display(previewVersion.snapshot)
          }}</pre>
        </a-card>
      </template>
    </a-spin>
  </a-drawer>
  <a-modal
    v-model:open="restoreVisible"
    title="恢复历史版本"
    :confirm-loading="busy"
    :cancel-button-props="{ disabled: busy }"
    :closable="!busy"
    :keyboard="!busy"
    :mask-closable="!busy"
    @ok="restore"
  >
    <a-alert
      type="warning"
      show-icon
      message="恢复将创建一个新版本；当前及历史内容都会保留。若有人同时修改，操作会被拒绝。"
    />
    <a-textarea
      v-model:value="restoreReason"
      placeholder="请填写恢复原因"
      :maxlength="500"
      style="margin-top: 16px"
    />
  </a-modal>
</template>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { cloneDeep } from "lodash-es";
import type { ViewSaveMode } from "./advancedFilter";
import { message, Modal } from "ant-design-vue";
import {
  EditOutlined,
  DeleteOutlined,
  PlusOutlined,
} from "@ant-design/icons-vue";
import { saveReviewSelection } from "./caseSelection";
import { useRouter } from "vue-router";
import { projectApi } from "@/api/project";
import { caseFeaturesApi, type CaseIssue } from "@/api/caseFeatures";
import {
  caseGovernanceApi as api,
  type CaseVersion,
  type CaseSavedView,
  type CaseSelection,
} from "@/api/caseGovernance";
const props = defineProps<{
  projectId: string;
  selectedIds: string[];
  filters: Record<string, any>;
  systemView: string;
  filterSaving?: boolean;
  selection?: CaseSelection;
  selectedCount?: number;
  selectionReady?: boolean;
  afterSelectionChange?: () => Promise<void>;
}>();
const emit = defineEmits<{
  (e: "changed"): void;
  (e: "busy-change", value: boolean): void;
  (e: "apply-view", filters: Record<string, any>): void;
  (e: "system-view", value: string): void;
  (e: "new-view"): void;
}>();
const router = useRouter();
const busy = ref(false);
watch(busy, (value) => emit("busy-change", value), { flush: "sync" });
const operationSelection = ref<{
  projectId: string;
  body: CaseSelection;
  count: number;
}>();
function captureSelection() {
  if (busy.value || props.selectionReady === false) return false;
  const body = props.selection || { caseIds: props.selectedIds };
  operationSelection.value = {
    projectId: props.projectId,
    body: cloneDeep(body),
    count: props.selectedCount ?? props.selectedIds.length,
  };
  return true;
}
async function selectionChanged(projectId: string) {
  if (projectId !== props.projectId) {
    message.info("操作已保存到原项目");
    return;
  }
  if (props.afterSelectionChange) await props.afterSelectionChange();
  else emit("changed");
}
const clearTags = ref(false),
  issueVisible = ref(false),
  issueId = ref<string>(),
  issues = ref<CaseIssue[]>([]);
const views = ref<CaseSavedView[]>([]),
  viewId = ref<string>(),
  viewName = ref(""),
  saveVisible = ref(false);
const editingViewId = ref<string>();
const selectedView = computed(
  () => viewId.value || `system:${props.systemView}`,
);
const batchVisible = ref(false),
  batchPriority = ref<string>(),
  batchTags = ref<string[]>([]),
  batchAutomated = ref<string>();
const organizeVisible = ref(false),
  organizeMode = ref<"move" | "copy">("move"),
  targetModule = ref("__unassigned__"),
  modules = ref<{ id: string; name: string }[]>([]);
const versionsVisible = ref(false),
  versions = ref<CaseVersion[]>([]),
  activeCaseId = ref(""),
  beforeVersion = ref<number>(),
  afterVersion = ref<number>();
const previewVersion = ref<CaseVersion>(),
  restoreTarget = ref<CaseVersion>(),
  restoreVisible = ref(false),
  restoreReason = ref("");
const compared = ref(false),
  changes = ref<{ field: string; before: any; after: any }[]>([]);
const versionOptions = computed(() =>
  versions.value.map((v) => ({ label: `v${v.version}`, value: v.version })),
);
const diffColumns = [
  { title: "字段", dataIndex: "field", key: "field" },
  { title: "旧内容", key: "before" },
  { title: "新内容", key: "after" },
];
const fieldName = (v: string) =>
  ({
    case_code: "用例编号",
    name: "名称",
    type: "用例类型",
    priority: "优先级",
    level: "用例等级",
    steps: "步骤",
    precondition: "前置条件",
    tags: "标签",
    is_automated: "是否自动化",
    module_id: "模块",
    module_path: "模块路径",
    executor_id: "执行人",
    requirement_ref: "需求关联",
  })[v] || v;
const display = (value: any) =>
  typeof value === "string" ? value : JSON.stringify(value, null, 2);
async function run(work: () => Promise<void>) {
  if (busy.value) return;
  busy.value = true;
  try {
    await work();
  } catch (error: any) {
    console.error("用例治理操作失败", error);
    message.error(error.response?.data?.detail || "操作失败，请重试");
  } finally {
    busy.value = false;
  }
}
let viewLoadSequence = 0;
watch(
  () => props.projectId,
  async (p) => {
    const sequence = ++viewLoadSequence;
    views.value = [];
    viewId.value = undefined;
    versionsVisible.value = false;
    saveVisible.value = false;
    if (!busy.value) {
      batchVisible.value = false;
      issueVisible.value = false;
      organizeVisible.value = false;
      operationSelection.value = undefined;
    }
    if (!p) return;
    try {
      const rows = await api.views(p);
      if (sequence === viewLoadSequence && p === props.projectId)
        views.value = rows;
    } catch (error) {
      console.error("加载个人视图失败", error);
      if (sequence === viewLoadSequence)
        message.error("加载个人视图失败，请刷新重试");
    }
  },
  { immediate: true },
);
const activeView = computed(() =>
  views.value.find((v) => v.id === viewId.value),
);
const viewNames = computed(() => [
  "全部用例",
  "全部数据",
  "我创建的",
  "我关注的",
  ...views.value.map((v) => v.name),
]);
const cannotAdd = computed(() => views.value.length >= 10);
async function persistFilterView(
  name: string,
  filters: Record<string, any>,
  mode: ViewSaveMode,
) {
  if (busy.value) throw new Error("已有操作正在执行，请稍后重试");
  const project = props.projectId,
    selected = viewId.value,
    payload = cloneDeep(filters);
  if (mode === "update" && !selected) throw new Error("没有可更新的个人视图");
  busy.value = true;
  try {
    const view =
      mode === "update"
        ? await api.updateView(project, selected!, name, payload)
        : await api.saveView(project, name, payload);
    if (project !== props.projectId || selected !== viewId.value)
      throw new Error("视图已保存到原项目，请返回原项目查看");
    if (mode === "update")
      views.value = views.value.map((v) => (v.id === view.id ? view : v));
    else {
      views.value.unshift(view);
      if (mode === "create") viewId.value = view.id;
    }
    message.success(
      mode === "update" ? "视图条件已保存" : "个人筛选视图已保存",
    );
  } finally {
    busy.value = false;
  }
}
function selectView(id: string) {
  if (busy.value || props.filterSaving) return;
  if (id === "action:create") {
    emit("new-view");
    return;
  }
  if (id.startsWith("system:")) {
    viewId.value = undefined;
    emit("system-view", id.slice(7));
    return;
  }
  const view = views.value.find((v) => v.id === id);
  if (view) {
    viewId.value = id;
    emit("apply-view", JSON.parse(JSON.stringify(view.filters)));
  }
}
function renameView(view: CaseSavedView) {
  editingViewId.value = view.id;
  viewName.value = view.name;
  saveVisible.value = true;
}
function confirmDeleteView(view: CaseSavedView) {
  Modal.confirm({
    title: "删除视图",
    content: `确定删除视图“${view.name}”？`,
    onOk: () =>
      run(async () => {
        await api.deleteView(props.projectId, view.id);
        views.value = views.value.filter((v) => v.id !== view.id);
        if (viewId.value === view.id) {
          viewId.value = undefined;
          emit("system-view", "all");
        }
        message.success("视图已删除");
      }),
  });
}
async function saveView() {
  if (!viewName.value.trim()) return message.warning("请填写视图名称");
  if (
    views.value.some(
      (v) => v.id !== editingViewId.value && v.name === viewName.value.trim(),
    )
  )
    return message.warning("视图名称已存在");
  await run(async () => {
    if (editingViewId.value) {
      const view = await api.renameView(
        props.projectId,
        editingViewId.value,
        viewName.value.trim(),
      );
      views.value = views.value.map((v) => (v.id === view.id ? view : v));
      message.success("视图已重命名");
    } else {
      const view = await api.saveView(
        props.projectId,
        viewName.value.trim(),
        props.filters,
      );
      views.value.unshift(view);
      viewId.value = view.id;
      message.success("个人筛选视图已保存");
    }
    saveVisible.value = false;
    editingViewId.value = undefined;
    viewName.value = "";
  });
}
async function batchUpdate() {
  const context = operationSelection.value;
  if (!context) return;
  const changes: Record<string, unknown> = {};
  if (batchPriority.value) changes.priority = batchPriority.value;
  if (clearTags.value) changes.tags = [];
  else if (batchTags.value.length) changes.tags = [...batchTags.value];
  if (batchAutomated.value)
    changes.isAutomated = batchAutomated.value === "yes";
  if (!Object.keys(changes).length)
    return message.warning("请选择需要修改的属性");
  await run(async () => {
    const result = await api.batch(context.projectId, {
      ...context.body,
      ...changes,
    });
    batchVisible.value = false;
    await selectionChanged(context.projectId);
    message.success(`已更新 ${result.updated} 条用例`);
  });
}
async function openIssueLinks() {
  if (!captureSelection()) return;
  const context = operationSelection.value!;
  await run(async () => {
    const rows = await caseFeaturesApi.issues(context.projectId);
    if (context.projectId !== props.projectId) return;
    issues.value = rows;
    issueId.value = undefined;
    issueVisible.value = true;
  });
}
async function linkIssues() {
  const context = operationSelection.value;
  if (!context || !issueId.value) return message.warning("请选择需求或缺陷");
  const selectedIssue = issueId.value;
  await run(async () => {
    const result = await api.linkSelection(
      context.projectId,
      context.body,
      selectedIssue,
    );
    issueVisible.value = false;
    await selectionChanged(context.projectId);
    message.success(`已关联 ${result.linked} 条用例`);
  });
}
async function openOrganize(mode: "move" | "copy") {
  if (!captureSelection()) return;
  const context = operationSelection.value!;
  organizeMode.value = mode;
  await run(async () => {
    const data = await projectApi.getModules(context.projectId);
    if (context.projectId !== props.projectId) return;
    modules.value = data.modules || data;
    targetModule.value = "__unassigned__";
    organizeVisible.value = true;
  });
}
async function organize() {
  const context = operationSelection.value;
  if (!context) return;
  const moduleId =
    targetModule.value === "__unassigned__" ? null : targetModule.value;
  const mode = organizeMode.value;
  await run(async () => {
    if (mode === "move")
      await api.batch(context.projectId, { ...context.body, moduleId });
    else await api.copySelection(context.projectId, context.body, moduleId);
    organizeVisible.value = false;
    await selectionChanged(context.projectId);
    message.success(mode === "move" ? "所选用例已移动" : "所选用例已复制");
  });
}
async function openCreateReview() {
  if (!captureSelection()) return;
  const context = operationSelection.value!;
  try {
    const key = context.body.selectAll
      ? saveReviewSelection(context.projectId, context.body)
      : undefined;
    await router.push({
      name: "CaseReviewEditor",
      query: {
        projectId: context.projectId,
        create: "1",
        ...(key
          ? { selectionKey: key }
          : { caseIds: (context.body.caseIds || []).join(",") }),
      },
    });
  } catch (exception) {
    console.error("保存或打开评审范围失败", exception);
    message.error("无法打开评审，请重试");
  }
}
async function openVersions(caseId: string) {
  activeCaseId.value = caseId;
  compared.value = false;
  changes.value = [];
  previewVersion.value = undefined;
  await run(async () => {
    versions.value = await api.versions(props.projectId, caseId);
    afterVersion.value = versions.value[0]?.version;
    beforeVersion.value = versions.value[1]?.version ?? afterVersion.value;
    versionsVisible.value = true;
  });
}
async function compare() {
  if (!beforeVersion.value || !afterVersion.value) return;
  await run(async () => {
    changes.value = (
      await api.compare(
        props.projectId,
        activeCaseId.value,
        beforeVersion.value!,
        afterVersion.value!,
      )
    ).changes;
    compared.value = true;
  });
}
async function restore() {
  if (!restoreReason.value.trim() || !restoreTarget.value)
    return message.warning("请填写恢复原因");
  await run(async () => {
    await api.restore(
      props.projectId,
      activeCaseId.value,
      restoreTarget.value!.id,
      versions.value[0].version,
      restoreReason.value.trim(),
    );
    versions.value = await api.versions(props.projectId, activeCaseId.value);
    afterVersion.value = versions.value[0]?.version;
    changes.value = [];
    compared.value = false;
    restoreVisible.value = false;
    emit("changed");
    message.success("已恢复并创建新版本");
  });
}
defineExpose({
  activeView,
  viewNames,
  cannotAdd,
  persistFilterView,
  resetViewSelection: () => {
    viewId.value = undefined;
  },
  openVersions,
  openOrganize,
  openIssueLinks,
  openCreateReview,
  openBatch: () => {
    if (captureSelection()) {
      batchPriority.value = undefined;
      batchTags.value = [];
      clearTags.value = false;
      batchAutomated.value = undefined;
      batchVisible.value = true;
    }
  },
});
</script>

<style scoped>
.view-option-name {
  display: inline-block;
  max-width: 95px;
  overflow: hidden;
  text-overflow: ellipsis;
  vertical-align: middle;
}
.view-option-actions {
  float: right;
}
.view-option-actions :deep(.ant-btn) {
  padding: 0;
  width: 22px;
  height: 22px;
}
.snapshot-text {
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  max-width: 100%;
  max-height: 360px;
  overflow: auto;
  font-size: 12px;
  margin: 0;
}
</style>
