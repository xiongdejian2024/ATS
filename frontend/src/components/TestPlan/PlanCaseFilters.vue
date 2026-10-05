<template>
  <a-space wrap>
    <a-select
      :value="viewId || 'system:all'"
      :disabled="busy || saving || viewLoading"
      :aria-label="
        mode === 'association' ? '计划关联用例视图' : '计划功能用例视图'
      "
      option-label-prop="label"
      :dropdown-match-select-width="280"
      style="width: 145px"
      @change="selectView"
    >
      <a-select-opt-group label="系统视图">
        <a-select-option value="system:all" label="全部数据"
          >全部数据</a-select-option
        >
        <a-select-option value="system:my" label="我创建的"
          >我创建的</a-select-option
        >
      </a-select-opt-group>
      <a-select-opt-group label="我的视图">
        <a-select-option
          v-for="v in views"
          :key="v.id"
          :value="v.id"
          :label="v.name"
        >
          <span class="view-name">{{ v.name }}</span>
          <span class="view-actions" @mousedown.stop.prevent>
            <a-button
              type="text"
              size="small"
              :aria-label="`重命名视图 ${v.name}`"
              @click.stop="rename(v)"
              ><EditOutlined
            /></a-button>
            <a-button
              type="text"
              size="small"
              :aria-label="`删除视图 ${v.name}`"
              @click.stop="remove(v)"
              ><DeleteOutlined
            /></a-button>
          </span>
        </a-select-option>
      </a-select-opt-group>
      <a-select-option
        value="action:create"
        label="新建视图"
        :disabled="views.length >= 10 || !!viewError"
        ><PlusOutlined /> 新建视图</a-select-option
      >
    </a-select>
    <a-button
      :disabled="busy || saving"
      :type="conditions?.length || activeView ? 'primary' : 'default'"
      @click="open(false)"
      >高级筛选</a-button
    >
    <a-button
      v-if="conditions !== undefined"
      type="link"
      :disabled="busy || saving"
      @click="emit('apply', undefined, 'and')"
      >重置筛选</a-button
    >
    <a-button
      v-if="viewError"
      danger
      :loading="viewLoading"
      aria-label="重试加载计划个人视图"
      @click="loadViews"
      >视图加载失败，重试</a-button
    >
  </a-space>
  <TestCaseFilter
    :key="planId"
    v-model:visible="visible"
    :available-fields="fields"
    :initial-fields="
      mode === 'association'
        ? ['id', 'name', 'moduleId']
        : ['id', 'name', 'moduleId', 'collectionId']
    "
    :module-tree-data="moduleTree"
    :conditions="conditions"
    :logic="logic"
    :view="activeView"
    :view-names="viewNames"
    :new-view="newView"
    :system-view="viewId === 'system:my' ? 'my' : 'all'"
    :metadata-error="metadataError || viewError"
    :metadata-loading="metadataLoading || viewLoading"
    :cannot-add="views.length >= 10 || !!viewError"
    :save-view="saveView"
    @apply="apply"
    @saving="
      (value) => {
        saving = value;
        emit('saving', value);
      }
    "
    @retry-fields="retryMetadata"
  />
  <a-modal
    v-model:open="renameOpen"
    title="重命名视图"
    :confirm-loading="saving"
    :closable="!saving"
    :keyboard="!saving"
    :mask-closable="!saving"
    :cancel-button-props="{ disabled: saving }"
    @ok="saveName"
  >
    <a-input
      v-model:value="renameName"
      placeholder="视图名称"
      :maxlength="255"
      :disabled="saving"
    />
    <a-alert v-if="renameError" :message="renameError" type="error" show-icon />
  </a-modal>
</template>
<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { Modal, message } from "ant-design-vue";
import {
  EditOutlined,
  DeleteOutlined,
  PlusOutlined,
} from "@ant-design/icons-vue";
import { cloneDeep } from "lodash-es";
import {
  planCaseWorkspaceApi as api,
  type CaseFolder,
  type PlanCaseSavedView,
} from "@/api/planCaseWorkspace";
import { caseFeaturesApi, type CaseTemplate } from "@/api/caseFeatures";
import { caseGovernanceApi } from "@/api/caseGovernance";
import TestCaseFilter from "@/components/TestCase/TestCaseFilter.vue";
import {
  type FilterCondition,
  type FilterLogic,
  type ViewSaveMode,
} from "@/components/TestCase/advancedFilter";
import { caseFolderTree } from "./planCaseFolders";
import { planCandidateFilterFields } from "./planCandidateFilterFields";
import { planCaseFilterFields } from "./planCaseFilterFields";
const props = withDefaults(
  defineProps<{
    mode?: import("@/api/planCaseWorkspace").PlanFilterMode;
    category?: "functional" | "api" | "scenario";
    plans?: { id: string; name: string }[];
    planId: string;
    projectId: string;
    projectName: string;
    collections: CaseFolder[];
    modules: CaseFolder[];
    conditions?: FilterCondition[];
    logic: FilterLogic;
    viewId?: string;
    busy: boolean;
  }>(),
  { mode: "workspace", category: "functional", plans: () => [] },
);
const emit = defineEmits<{
  apply: [
    conditions: FilterCondition[] | undefined,
    logic: FilterLogic,
    viewId?: string,
  ];
  saving: [value: boolean];
}>();
const visible = ref(false),
  newView = ref(false),
  saving = ref(false),
  views = ref<PlanCaseSavedView[]>([]),
  viewLoading = ref(false),
  viewError = ref(""),
  metadataLoading = ref(false),
  metadataError = ref(""),
  templates = ref<CaseTemplate[]>([]),
  members = ref<{ id: string; name: string }[]>([]);
const activeView = computed(() =>
  views.value.find((v) => v.id === props.viewId),
);
const viewNames = computed(() => [
  "全部数据",
  "我创建的",
  ...views.value.map((v) => v.name),
]);
const fields = computed(() =>
  props.mode === "association"
    ? planCandidateFilterFields(
        { id: props.projectId, name: props.projectName },
        props.plans,
        templates.value,
        members.value,
        props.category,
      )
    : planCaseFilterFields(
        { id: props.projectId, name: props.projectName },
        props.collections,
        templates.value,
        members.value,
      ),
);
const moduleTree = computed(() => {
  const mark = (nodes: ReturnType<typeof caseFolderTree>): any[] =>
    nodes.map((n) => ({
      ...n,
      nodeType: "module",
      children: mark(n.children || []),
    }));
  return [
    { key: "__unassigned__", title: "未分配模块", nodeType: "module" },
    ...mark(caseFolderTree(props.modules, "")),
  ];
});
let viewSequence = 0,
  metadataSequence = 0;
async function loadViews() {
  const plan = props.planId,
    sequence = ++viewSequence;
  viewLoading.value = true;
  try {
    const rows = await api.views(plan, props.category, props.mode);
    if (sequence !== viewSequence || plan !== props.planId) return;
    views.value = rows;
    viewError.value = "";
  } catch (error) {
    console.error("加载计划个人视图失败", error);
    if (sequence === viewSequence && plan === props.planId)
      viewError.value = "个人视图加载失败，请重试";
  } finally {
    if (sequence === viewSequence) viewLoading.value = false;
  }
}
async function loadMetadata() {
  const project = props.projectId,
    sequence = ++metadataSequence;
  metadataLoading.value = true;
  const results = await Promise.allSettled([
    caseFeaturesApi.templates(project),
    caseGovernanceApi.reviewers(project),
  ]);
  if (sequence !== metadataSequence || project !== props.projectId) return;
  const errors: string[] = [];
  if (results[0].status === "fulfilled") templates.value = results[0].value;
  else {
    errors.push("自定义字段");
    console.error("加载计划自定义筛选字段失败", results[0].reason);
  }
  if (results[1].status === "fulfilled") members.value = results[1].value;
  else {
    errors.push("项目成员");
    console.error("加载计划筛选成员失败", results[1].reason);
  }
  metadataError.value = errors.length
    ? `${errors.join("、")}加载失败，请重试；已加载字段和草稿保留`
    : "";
  metadataLoading.value = false;
}
function retryMetadata() {
  void loadMetadata();
  void loadViews();
}
function open(create: boolean) {
  savedViewId = undefined;
  newView.value = create;
  visible.value = true;
}
let savedViewId: string | undefined;
function apply(conditions: FilterCondition[], logic: FilterLogic) {
  emit(
    "apply",
    conditions.length ||
      activeView.value ||
      savedViewId ||
      props.viewId === "system:my"
      ? conditions
      : undefined,
    logic,
    savedViewId || (newView.value ? undefined : props.viewId),
  );
}
function selectView(value: string) {
  if (value === "action:create") return open(true);
  if (value === "system:all") return emit("apply", undefined, "and");
  if (value === "system:my") return emit("apply", [], "and", value);
  const view = views.value.find((v) => v.id === value);
  if (view)
    emit(
      "apply",
      cloneDeep(view.filters.filterConditions || []),
      view.filters.filterLogic || "and",
      view.id,
    );
}
async function saveView(
  name: string,
  conditions: FilterCondition[],
  logic: FilterLogic,
  mode: ViewSaveMode,
) {
  const plan = props.planId,
    context = `${props.category}:${props.mode}`,
    selected = props.viewId;
  const filters = { filterConditions: conditions, filterLogic: logic };
  const row =
    mode === "update" && activeView.value
      ? await api.updateView(
          plan,
          activeView.value.id,
          name,
          filters,
          props.category,
          props.mode,
        )
      : await api.saveView(plan, name, filters, props.category, props.mode);
  if (
    plan !== props.planId ||
    context !== `${props.category}:${props.mode}` ||
    selected !== props.viewId
  )
    throw new Error("计划或视图已切换，请重新打开筛选");
  views.value = [row, ...views.value.filter((v) => v.id !== row.id)];
  newView.value = false;
  savedViewId = row.id;
  emit("apply", cloneDeep(conditions), logic, row.id);
}
const renameOpen = ref(false),
  renameName = ref(""),
  renameId = ref(""),
  renameError = ref("");
function rename(view: PlanCaseSavedView) {
  renameId.value = view.id;
  renameName.value = view.name;
  renameError.value = "";
  renameOpen.value = true;
}
async function saveName() {
  const name = renameName.value.trim(),
    plan = props.planId,
    category = props.category,
    mode = props.mode;
  if (
    !name ||
    viewNames.value.some(
      (n) =>
        n === name &&
        views.value.find((v) => v.name === n)?.id !== renameId.value,
    )
  ) {
    renameError.value = "请输入不重复的视图名称";
    return;
  }
  saving.value = true;
  emit("saving", true);
  try {
    const row = await api.updateView(
      plan,
      renameId.value,
      name,
      undefined,
      category,
      mode,
    );
    if (
      plan !== props.planId ||
      category !== props.category ||
      mode !== props.mode
    )
      return;
    views.value = views.value.map((v) => (v.id === row.id ? row : v));
    renameOpen.value = false;
  } catch (error) {
    console.error("重命名计划视图失败", error);
    renameError.value = "保存失败，草稿保留，请重试";
  } finally {
    saving.value = false;
    emit("saving", false);
  }
}
function remove(view: PlanCaseSavedView) {
  const plan = props.planId,
    category = props.category,
    mode = props.mode;
  const confirmation = Modal.confirm({
    title: `删除视图“${view.name}”？`,
    content: "删除后不可恢复。",
    onOk: async () => {
      saving.value = true;
      emit("saving", true);
      confirmation.update({ cancelButtonProps: { disabled: true } });
      try {
        if (
          plan !== props.planId ||
          category !== props.category ||
          mode !== props.mode
        )
          throw new Error("计划或分类已切换");
        await api.deleteView(plan, view.id, category, mode);
        if (
          plan !== props.planId ||
          category !== props.category ||
          mode !== props.mode
        )
          return;
        views.value = views.value.filter((v) => v.id !== view.id);
        if (props.viewId === view.id) emit("apply", undefined, "and");
        message.success("个人视图已删除");
      } catch (error) {
        console.error("删除计划视图失败", error);
        message.error("删除失败，请重试");
        throw error;
      } finally {
        confirmation.update({ cancelButtonProps: { disabled: false } });
        saving.value = false;
        emit("saving", false);
      }
    },
  });
}
watch(
  () => [props.planId, props.projectId, props.category, props.mode],
  () => {
    ++viewSequence;
    ++metadataSequence;
    visible.value = false;
    renameOpen.value = false;
    views.value = [];
    templates.value = [];
    members.value = [];
    viewError.value = "";
    metadataError.value = "";
    void loadViews();
    void loadMetadata();
  },
  { immediate: true },
);
</script>
<style scoped>
.view-name {
  display: inline-block;
  max-width: 170px;
  overflow: hidden;
  text-overflow: ellipsis;
  vertical-align: middle;
}
.view-actions {
  float: right;
}
</style>
