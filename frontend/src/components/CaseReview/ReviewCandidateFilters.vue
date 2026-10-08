<template>
  <a-space wrap>
    <a-select
      :value="viewId || 'system:all'"
      :disabled="busy || saving || viewLoading"
      aria-label="评审关联用例视图"
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
      @click="selectView('system:all')"
      >重置筛选</a-button
    >
    <a-button
      v-if="viewError"
      danger
      :loading="viewLoading"
      aria-label="重试加载评审关联个人视图"
      @click="loadViews"
      >视图加载失败，重试</a-button
    >
  </a-space>
  <TestCaseFilter
    ref="filterEditor"
    guard-closing
    :key="identity"
    v-model:visible="visible"
    :available-fields="fields"
    :initial-fields="['id', 'name', 'moduleId']"
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
    :open="renameOpen"
    title="重命名视图"
    :confirm-loading="saving"
    :closable="!saving"
    :keyboard="!saving"
    :mask-closable="!saving"
    :cancel-button-props="{ disabled: saving }"
    @ok="saveName"
    @cancel="beforeClose"
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
import { computed, ref, watch, onBeforeUnmount } from "vue";
import { Modal, message } from "ant-design-vue";
import {
  EditOutlined,
  DeleteOutlined,
  PlusOutlined,
} from "@ant-design/icons-vue";
import { cloneDeep } from "lodash-es";
import type { CaseFolder } from "@/api/planCaseWorkspace";
import type { ReviewCandidateSavedView } from "@/api/reviewWorkspace";
import { reviewWorkspaceApi as api } from "@/api/reviewWorkspace";
import { caseFeaturesApi, type CaseTemplate } from "@/api/caseFeatures";
import { useUserStore } from "@/stores/user";
import { caseGovernanceApi } from "@/api/caseGovernance";
import TestCaseFilter from "@/components/TestCase/TestCaseFilter.vue";
import {
  type FilterCondition,
  type FilterLogic,
  type ViewSaveMode,
} from "@/components/TestCase/advancedFilter";
import { caseFolderTree } from "@/components/TestPlan/planCaseFolders";
import { planCandidateFilterFields } from "@/components/TestPlan/planCandidateFilterFields";
const props = defineProps<{
  projectId: string;
  modules: CaseFolder[];
  conditions?: FilterCondition[];
  logic: FilterLogic;
  viewId?: string;
  mine?: boolean;
  busy: boolean;
}>();
let live = true;
onBeforeUnmount(() => {
  live = false;
  ++viewSequence;
  ++metadataSequence;
});
const user = useUserStore();
const identity = computed(() =>
  JSON.stringify([props.projectId, user.user?.id]),
);
const emit = defineEmits<{
  apply: [
    conditions: FilterCondition[] | undefined,
    logic: FilterLogic,
    viewId?: string,
    mine?: boolean,
  ];
  saving: [value: boolean];
}>();
const visible = ref(false),
  newView = ref(false),
  saving = ref(false),
  views = ref<ReviewCandidateSavedView[]>([]),
  viewLoading = ref(false),
  viewError = ref(""),
  metadataLoading = ref(false),
  metadataError = ref(""),
  templates = ref<CaseTemplate[]>([]),
  members = ref<{ id: string; name: string }[]>([]);
const filterEditor = ref<{ beforeClose: () => Promise<boolean> }>();
const activeView = computed(() =>
  views.value.find((v) => v.id === props.viewId),
);
const viewNames = computed(() => [
  "全部数据",
  "我创建的",
  ...views.value.map((v) => v.name),
]);
const fields = computed(() =>
  planCandidateFilterFields(
    { id: props.projectId, name: "当前项目" },
    [],
    templates.value,
    members.value,
    "functional",
  ).filter((field) => field.key !== "planIds"),
);
const moduleTree = computed(() => {
  const mark = (nodes: ReturnType<typeof caseFolderTree>): any[] =>
    nodes.map((n) => ({
      ...n,
      nodeType: "module",
      selectable: n.nodeType !== "PROJECT",
      children: mark(n.children || []),
    }));
  return [
    { key: "__unassigned__", title: "未分配模块", nodeType: "module" },
    ...mark(
      caseFolderTree(
        props.modules.filter((m) => m.nodeType !== "DEFAULT"),
        "",
      ),
    ),
  ];
});
let viewSequence = 0,
  metadataSequence = 0;
function acknowledgeViews() {
  ++viewSequence;
  viewLoading.value = false;
  viewError.value = "";
}
async function loadViews() {
  const scope = identity.value,
    sequence = ++viewSequence;
  viewLoading.value = true;
  try {
    const rows = await api.candidateViews(props.projectId);
    if (!live || sequence !== viewSequence || scope !== identity.value) return;
    views.value = rows;
    viewError.value = "";
  } catch (error) {
    console.error("加载评审关联个人视图失败", error);
    if (live && sequence === viewSequence && scope === identity.value)
      viewError.value = "个人视图加载失败，请重试";
  } finally {
    if (live && sequence === viewSequence && scope === identity.value)
      viewLoading.value = false;
  }
}
async function loadMetadata() {
  const scope = identity.value,
    sequence = ++metadataSequence;
  metadataLoading.value = true;
  const results = await Promise.allSettled([
    caseFeaturesApi.templates(props.projectId),
    caseGovernanceApi.reviewers(props.projectId),
  ]);
  if (!live || sequence !== metadataSequence || scope !== identity.value)
    return;
  const errors: string[] = [];
  if (results[0].status === "fulfilled") templates.value = results[0].value;
  else {
    errors.push("自定义字段");
    console.error("加载关联模板失败", results[0].reason);
  }
  if (results[1].status === "fulfilled") members.value = results[1].value;
  else {
    errors.push("项目成员");
    console.error("加载关联成员失败", results[1].reason);
  }
  metadataError.value = errors.length
    ? `${errors.join("、")}加载失败，请重试；草稿保留`
    : "";
  metadataLoading.value = false;
}
function retryMetadata() {
  void loadMetadata();
  void loadViews();
}
async function open(create: boolean) {
  if (props.busy || saving.value || !(await beforeClose())) return;
  void loadMetadata();
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
      props.mine ||
      props.viewId === "system:my"
      ? conditions
      : undefined,
    logic,
    savedViewId || (newView.value ? undefined : props.viewId),
    props.mine || props.viewId === "system:my",
  );
}
async function selectView(value: string) {
  if (!live || props.busy || saving.value) return;
  if (value === "action:create") return open(true);
  if (!(await beforeClose())) return;
  if (value === "system:all") return emit("apply", undefined, "and");
  if (value === "system:my") return emit("apply", [], "and", value);
  const view = views.value.find((v) => v.id === value);
  if (view)
    emit(
      "apply",
      cloneDeep(view.filters.filterConditions || []),
      view.filters.filterLogic || "and",
      view.id,
      view.filters.mine === true,
    );
}
async function saveView(
  name: string,
  conditions: FilterCondition[],
  logic: FilterLogic,
  mode: ViewSaveMode,
) {
  if (!live || props.busy) throw new Error("项目已切换或操作进行中");
  const scope = identity.value,
    selected = props.viewId;
  const filters = {
    filterConditions: cloneDeep(conditions),
    filterLogic: logic,
    ...(props.mine || props.viewId === "system:my" ? { mine: true } : {}),
  };
  const row =
    mode === "update" && activeView.value
      ? await api.updateCandidateView(
          props.projectId,
          activeView.value.id,
          name,
          filters,
        )
      : await api.saveCandidateView(props.projectId, name, filters);
  if (!live || scope !== identity.value || selected !== props.viewId)
    throw new Error("项目或视图已切换");
  acknowledgeViews();
  views.value = [row, ...views.value.filter((v) => v.id !== row.id)];
  newView.value = false;
  savedViewId = row.id;
  emit("apply", cloneDeep(conditions), logic, row.id, filters.mine === true);
}
const renameOpen = ref(false),
  renameName = ref(""),
  renameId = ref(""),
  renameError = ref("");
function rename(view: ReviewCandidateSavedView) {
  if (!live || saving.value || props.busy || visible.value) return;
  renameId.value = view.id;
  renameName.value = view.name;
  renameError.value = "";
  renameOpen.value = true;
}
async function saveName() {
  if (!live || saving.value || props.busy) return;
  const name = renameName.value.trim(),
    scope = identity.value,
    id = renameId.value;
  if (
    !name ||
    views.value.some((v) => v.name === name && v.id !== id) ||
    ["全部数据", "我创建的"].includes(name)
  ) {
    renameError.value = "请输入不重复的视图名称";
    return;
  }
  saving.value = true;
  emit("saving", true);
  try {
    const row = await api.updateCandidateView(props.projectId, id, name);
    if (!live || scope !== identity.value) return;
    acknowledgeViews();
    views.value = views.value.map((v) => (v.id === row.id ? row : v));
    renameOpen.value = false;
  } catch (error) {
    console.error("重命名个人视图失败", error);
    if (live && scope === identity.value)
      renameError.value = "保存失败，草稿保留，请重试";
  } finally {
    if (live && scope === identity.value) {
      saving.value = false;
      emit("saving", false);
    }
  }
}
function remove(view: ReviewCandidateSavedView) {
  if (!live || saving.value || props.busy || visible.value) return;
  const scope = identity.value,
    project = props.projectId;
  const confirmation = Modal.confirm({
    title: `删除视图“${view.name}”？`,
    content: "删除后不可恢复。",
    onOk: async () => {
      if (!live || scope !== identity.value || saving.value || props.busy)
        throw new Error("项目已切换或操作进行中");
      saving.value = true;
      emit("saving", true);
      confirmation.update({ cancelButtonProps: { disabled: true } });
      try {
        await api.deleteCandidateView(project, view.id);
        if (!live || scope !== identity.value) return;
        acknowledgeViews();
        views.value = views.value.filter((v) => v.id !== view.id);
        if (props.viewId === view.id) emit("apply", undefined, "and");
        message.success("个人视图已删除");
      } catch (error) {
        console.error("删除个人视图失败", error);
        if (live && scope === identity.value) message.error("删除失败，请重试");
        throw error;
      } finally {
        confirmation.update({ cancelButtonProps: { disabled: false } });
        if (live && scope === identity.value) {
          saving.value = false;
          emit("saving", false);
        }
      }
    },
  });
}
let closing = false;
async function beforeClose() {
  if (!live || saving.value || closing) return false;
  const scope = identity.value;
  closing = true;
  try {
    if (
      renameOpen.value &&
      renameName.value !==
        views.value.find((v) => v.id === renameId.value)?.name
    ) {
      const accepted = await new Promise<boolean>((resolve) =>
        Modal.confirm({
          title: "放弃视图名称草稿？",
          onOk: () => resolve(true),
          onCancel: () => resolve(false),
        }),
      );
      if (!live || !accepted || scope !== identity.value) return false;
    }
    if (
      visible.value &&
      filterEditor.value &&
      !(await filterEditor.value.beforeClose())
    )
      return false;
    if (!live || scope !== identity.value || saving.value) return false;
    visible.value = false;
    renameOpen.value = false;
    return true;
  } finally {
    closing = false;
  }
}
defineExpose({ beforeClose });
watch(
  identity,
  () => {
    ++viewSequence;
    ++metadataSequence;
    visible.value = false;
    renameOpen.value = false;
    saving.value = false;
    views.value = [];
    templates.value = [];
    members.value = [];
    viewError.value = "";
    metadataError.value = "";
    savedViewId = undefined;
    emit("saving", false);
    void loadViews();
    void loadMetadata();
  },
  { immediate: true, flush: "sync" },
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
