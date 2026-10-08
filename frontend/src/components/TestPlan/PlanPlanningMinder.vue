<template>
  <section
    class="planning-minder"
    aria-label="测试规划脑图"
    tabindex="0"
    @keydown="handleShortcut"
  >
    <a-alert
      message="通过测试集组织用例；新增、改名、排序和删除在保存规划后生效。"
      type="info"
      show-icon
    />
    <div class="planning-toolbar">
      <a-select
        :value="selectedOption"
        show-search
        option-filter-prop="label"
        placeholder="定位节点"
        :options="nodeOptions"
        @change="selectById"
      /><a-space wrap
        ><a-button @click="expandAll">展开全部</a-button
        ><a-button @click="collapseAll">收起全部</a-button
        ><a-button @click="fit">重置视图</a-button>
        <a-button
          aria-label="缩小脑图"
          @click="changeZoom(Math.max(0.5, zoom - 0.1))"
          >−</a-button
        >
        <span class="zoom-value">{{ Math.round(zoom * 100) }}%</span>
        <a-button
          aria-label="放大脑图"
          @click="changeZoom(Math.min(2, zoom + 0.1))"
          >+</a-button
        >
        <a-button @click="fitCanvas">适应画布</a-button
        ><a-button :loading="loading" @click="load">刷新</a-button
        ><a-button @click="openAdvanced">用例和场景配置</a-button>
        <a-button
          v-if="canEdit"
          type="primary"
          :loading="saving"
          :disabled="!hasChanges || loading || failed"
          @click="savePoint"
          >保存规划</a-button
        >
        <a-button
          v-if="canEdit"
          :disabled="!hasChanges || saving"
          @click="cancelDraft"
          >取消修改</a-button
        ></a-space
      >
    </div>
    <a-alert
      v-if="failed"
      message="测试规划加载失败，请重试"
      type="error"
      show-icon
    />
    <a-spin v-else :spinning="loading"
      ><div
        ref="layoutElement"
        class="minder-layout"
        :class="{
          fullscreen: isFullscreen,
          'config-open': selected && configVisible,
        }"
      >
        <div class="minder-canvas">
          <div
            ref="viewport"
            class="minder-viewport"
            :class="{ 'hand-mode': hand }"
            tabindex="0"
            aria-label="脑图画布，按斜线展开收起，Tab 添加分类下测试集，Enter 添加同级测试集，Ctrl/⌘ 点击多选，空白处拖动框选，Backspace 删除"
            @pointerdown="marquee.start"
          >
            <div
              class="minder-sizing"
              :style="{
                width: `${stageWidth * zoom + viewportWidth}px`,
                height: `${stageHeight * zoom + viewportHeight}px`,
              }"
            >
              <div
                ref="stage"
                class="minder-stage"
                :style="{
                  transform: `scale(${zoom})`,
                  width: geometry ? `${geometry.width}px` : undefined,
                  height: geometry ? `${geometry.height}px` : undefined,
                  left: `${viewportWidth / 2}px`,
                  top: `${viewportHeight / 2}px`,
                }"
              >
                <svg
                  v-if="geometry"
                  class="minder-connections"
                  :width="geometry.width"
                  :height="geometry.height"
                  aria-hidden="true"
                >
                  <g
                    :transform="`translate(${geometry.offset.x} ${geometry.offset.y})`"
                  >
                    <path
                      v-for="(path, index) in geometry.paths"
                      :key="index"
                      :d="path"
                      fill="none"
                      stroke="var(--primary-border)"
                      stroke-width="1"
                    />
                  </g>
                </svg>
                <PlanningMinderBranch
                  v-if="!failed"
                  :node="tree"
                  :geometry="geometry"
                  :points="nodes"
                  :selected-ids="selectedIds"
                  :collapsed="collapsed"
                  :can-edit="
                    canEdit &&
                    !saving &&
                    !dirty &&
                    !editingId &&
                    selectedIds.size <= 1 &&
                    !marquee.active.value &&
                    !hand
                  "
                  :editing-id="editingId"
                  :edit-name="editName"
                  @edit="beginNameEdit"
                  @edit-name="(name) => (editName = name)"
                  @rename="commitNameEdit"
                  @cancel-edit="cancelNameEdit"
                  @select="selectCanvasNode"
                  @toggle="toggleById"
                  @reorder="reorderPoints"
                  @drag-choose="dragPreview.choose"
                  @drag-start="dragPreview.start"
                  @drag-end="dragPreview.end"
                  ><template #menu="{ node }"
                    ><PlanningMinderMenu
                      :node="node"
                      :actions="nodeActions(node)"
                      :disabled="saving || loading"
                      :zoom="zoom"
                      @action="handleNodeAction" />
                    <PlanningMinderTagMenu
                      v-if="tagOpen && tagConfiguration"
                      :zoom="zoom"
                      :label="tagConfiguration.label"
                      :value="tagConfiguration.value"
                      :options="tagConfiguration.options"
                      :disabled="saving || loading"
                      @select="saveTag"
                      @close="tagOpen = false" /></template
                ></PlanningMinderBranch>
              </div>
            </div>
            <div
              v-if="marquee.style.value"
              class="minder-marquee"
              :style="marquee.style.value"
              aria-hidden="true"
            />
          </div>
          <a-alert
            v-if="layoutFailed"
            class="layout-error"
            message="脑图布局加载失败，请刷新重试"
            type="error"
          />
          <PlanningMinderHeader
            :mode="mode"
            :fullscreen="isFullscreen"
            :can-edit="canEdit"
            :disabled="!hasChanges || loading || failed || saving"
            @mode="changeMode"
            @fullscreen="toggleFullscreen"
            @save="savePoint"
          />
          <PlanningMinderNavigator
            :zoom="zoom"
            :hand="hand"
            :preview="viewPreferences?.preview === true"
            :geometry="geometry"
            :visible="visibleBox"
            @zoom="changeZoom"
            @hand="(value) => (hand = value)"
            @preview="
              (value) =>
                (viewPreferences = { ...viewPreferences, preview: value })
            "
            @camera="locateRoot"
            @locate="locatePoint"
          />
        </div>
        <PlanningMinderBatchMenu
          v-if="selectedIds.size > 1 && deletionTargets"
          :count="selectedIds.size"
          :disabled="saving || loading || !!editingId || dirty"
          @delete="removePoint"
        />
        <aside v-if="selected && configVisible" class="node-configuration">
          <h3>{{ selected.name }}</h3>
          <p>关联用例 {{ selected.count }} 条</p>
          <a-alert
            v-if="pendingAssociation"
            type="info"
            show-icon
            :message="`${pendingAssociation.request.resourceType === 'API' ? `已选 ${pendingAssociation.summary.selectedDefinitionCount || 0} 个接口，` : ''}待关联 ${pendingAssociation.summary.count} 条用例${pendingAssociation.summary.sync ? `，同步接口 ${pendingAssociation.summary.sync.api.count} 条、场景 ${pendingAssociation.summary.sync.scenario.count} 条` : ''}，保存规划后生效`"
          />
          <a-button
            v-if="selected.children?.length"
            size="small"
            class="fold-button"
            @click="toggleSelected"
            >{{
              collapsed.has(selected.id) ? "展开当前节点" : "收起当前节点"
            }}</a-button
          >
          <template v-if="selected.kind === 'root'"
            ><a-button v-if="canEdit" @click="emit('configurePlan')"
              >执行配置</a-button
            ></template
          >
          <template v-else>
            <a-space wrap
              ><a-button v-if="canEdit && canAdd" @click="openCreate"
                >添加测试集</a-button
              ><a-button
                v-if="canEdit && selected.kind === 'collection'"
                @click="openAssociation"
                >关联用例</a-button
              ><a-button :disabled="!selected.count" @click="viewCases"
                >查看用例</a-button
              ></a-space
            >
            <a-form
              v-if="canRename"
              layout="vertical"
              class="point-form"
              :disabled="!canEdit || saving || loading"
            >
              <a-form-item label="测试集名称" required
                ><a-input v-model:value="pointForm.name" :maxlength="255"
              /></a-form-item>
            </a-form>
          </template>
          <a-form
            v-if="selectedScope && executionCatalog && executionDraft"
            layout="vertical"
            class="point-form"
          >
            <ExecutionConfiguration
              ref="executionEditor"
              v-model:value="executionDraft"
              :inherited="inheritedConfiguration"
              :root="selectedScope.startsWith('root:')"
              :catalog="executionCatalog"
              :disabled="!canEdit || saving || loading"
              @manage-pool="openPool"
            />
          </a-form>
          <a-space v-if="canEdit && (canRename || selectedScope)" wrap
            ><a-button type="primary" :loading="saving" @click="savePoint"
              >保存</a-button
            ><a-button :disabled="saving" @click="resetPoint">取消修改</a-button
            ><a-button
              v-if="canRename"
              danger
              :disabled="saving"
              @click="removePoint"
              >删除测试集</a-button
            ></a-space
          >
        </aside>
      </div></a-spin
    >
    <a-modal
      v-model:open="poolOpen"
      title="配置资源池"
      :confirm-loading="saving"
      @ok="savePool"
    >
      <a-form layout="vertical"
        ><a-form-item label="资源池"
          ><a-select
            v-model:value="poolSelection"
            :options="[
              { value: 'new', label: '创建资源池' },
              ...(executionCatalog?.pools || []).map((item) => ({
                value: item.id,
                label: item.name,
              })),
            ]"
            @change="resetPool"
        /></a-form-item>
        <a-form-item label="名称" required
          ><a-input v-model:value="poolDraft.name" :maxlength="255"
        /></a-form-item>
        <a-form-item label="执行节点" required
          ><a-select
            v-model:value="poolDraft.environmentIds"
            mode="multiple"
            :options="
              (executionCatalog?.resources || []).map((item) => ({
                value: item.id,
                label: item.name,
                disabled: !item.enabled,
              }))
            "
        /></a-form-item>
      </a-form>
    </a-modal>
    <PlanCaseAssociateDrawer
      v-model:open="associateOpen"
      :plan-id="plan.id"
      :can-edit="canEdit"
      :category="selected?.category"
      :collection-id="selected?.nodeId"
      :minder-draft="associationDraft"
      :initial-association="pendingAssociation?.request"
      @staged="stageAssociation"
      @associated="changed"
    />
    <a-drawer
      v-model:open="advancedOpen"
      title="用例和场景配置"
      width="min(1200px,100vw)"
      destroy-on-close
      ><PlanTreeWorkspace
        v-if="advancedOpen"
        :plan-id="plan.id"
        :project-id="plan.projectId"
        :can-edit="canEdit"
        @changed="changed"
    /></a-drawer>
  </section>
</template>
<script setup lang="ts">
import { computed, ref, reactive, watch, nextTick } from "vue";
import {
  useElementSize,
  useScroll,
  useFullscreen,
  useStorage,
} from "@vueuse/core";
import PlanningMinderHeader from "./PlanningMinderHeader.vue";
import PlanningMinderNavigator from "./PlanningMinderNavigator.vue";
import { useMinderLayout } from "./useMinderLayout";
import { useMinderDragPreview } from "./useMinderDragPreview";
import { useMinderPan } from "./useMinderPan";
import {
  isMinderMode,
  zoomScroll,
  cameraScroll,
  visibleMinderBox,
  type MinderMode,
} from "./planMinderView";
import {
  useRouter,
  useRoute,
  onBeforeRouteLeave,
  onBeforeRouteUpdate,
} from "vue-router";
import { message, Modal } from "ant-design-vue";
import type { TestPlan, Environment } from "@/types";
import { environmentApi } from "@/api/environment";
import { planMinderApi, type MinderWorkspace } from "@/api/planMinder";
import type {
  PlanAssociation,
  CandidateSelectionPreview,
} from "@/api/planCaseWorkspace";
import { PlanMinderDraft } from "./planMinderDraft";
import PlanningMinderBranch from "./PlanningMinderBranch.vue";
import PlanningMinderMenu from "./PlanningMinderMenu.vue";
import PlanningMinderTagMenu from "./PlanningMinderTagMenu.vue";
import PlanningMinderBatchMenu from "./PlanningMinderBatchMenu.vue";
import { minderDeletionTargets } from "./planMinderSelection";
import { useMinderMarquee } from "./useMinderMarquee";
import { planMinderTag } from "./planMinderTag";
import { planMinderActions, type MinderAction } from "./planMinderActions";
import {
  buildPlanMinder,
  planCategoryNames,
  type PlanMinderNode,
} from "./planMinderTree";
import PlanCaseAssociateDrawer from "./PlanCaseAssociateDrawer.vue";
import PlanTreeWorkspace from "./PlanTreeWorkspace.vue";
import ExecutionConfiguration from "./ExecutionConfiguration.vue";
import {
  planExecutionApi,
  type ExecutionConfig,
} from "@/api/planExecutionConfig";

const props = defineProps<{ plan: TestPlan; canEdit: boolean }>(),
  emit = defineEmits<{ changed: []; configurePlan: [] }>(),
  router = useRouter(),
  route = useRoute();
const draft = reactive(new PlanMinderDraft());
const nodes = computed(() => draft.workspace?.nodes || []),
  entries = computed(
    () => draft.workspace?.entries || { functional: [], api: [], scenario: [] },
  ),
  executionCatalog = computed(() => draft.workspace?.executionCatalog),
  environments = ref<Environment[]>([]),
  loading = ref(false),
  failed = ref(false),
  saving = ref(false),
  selected = ref<PlanMinderNode>(),
  viewport = ref<HTMLElement>(),
  collapsed = ref(new Set<string>()),
  stage = ref<HTMLElement>(),
  zoom = ref(1);
const configVisible = ref(false),
  tagOpen = ref(false),
  editingId = ref<string>(),
  editName = ref("");
const layoutElement = ref<HTMLElement>();
const { isFullscreen, toggle: toggleFullscreen } = useFullscreen(layoutElement);
const hand = ref(false);
const viewPreferences = useStorage<{ mode: MinderMode; preview: boolean }>(
  "ats-plan-minder-view",
  { mode: "right", preview: false },
  undefined,
  { onError: (error) => console.error("读取或保存脑图视图偏好失败", error) },
);
const mode = computed(() =>
  isMinderMode(viewPreferences.value?.mode)
    ? viewPreferences.value.mode
    : "right",
);
const { width: viewportWidth, height: viewportHeight } =
  useElementSize(viewport);
const { x: scrollLeft, y: scrollTop } = useScroll(viewport);
const visibleBox = computed(() =>
  visibleMinderBox(
    scrollLeft.value,
    scrollTop.value,
    viewportWidth.value,
    viewportHeight.value,
    zoom.value,
  ),
);
useMinderPan(viewport, hand);
const dragPreview = useMinderDragPreview();
const tree = computed(() =>
  buildPlanMinder(props.plan.name, nodes.value, entries.value, {
    environmentNames: Object.fromEntries(
      environments.value.map((item) => [item.id, item.name]),
    ),
    defaultEnvironmentId: props.plan.environmentId,
    executionCatalog: executionCatalog.value,
    executionMode: draft.workspace?.policy.executionMode,
  }),
);
const { geometry, failed: layoutFailed } = useMinderLayout(
  stage,
  tree,
  collapsed,
  mode,
  editingId,
);
const stageWidth = computed(() => geometry.value?.width || 1),
  stageHeight = computed(() => geometry.value?.height || 1);
let initialPosition = true;
watch(
  () => props.plan.id,
  () => {
    initialPosition = true;
    hand.value = false;
  },
);
watch(geometry, async () => {
  if (initialPosition && !loading.value) {
    initialPosition = false;
    await nextTick();
    locateRoot();
  }
});
const flatNodes = computed(() => {
  const result: PlanMinderNode[] = [];
  function walk(node: PlanMinderNode) {
    result.push(node);
    node.children?.forEach(walk);
  }
  walk(tree.value);
  return result;
});
const selectedIds = ref<ReadonlySet<string>>(new Set());
const selectedNodes = computed(() =>
  flatNodes.value.filter((node) => selectedIds.value.has(node.id)),
);
const deletionTargets = computed(() =>
  minderDeletionTargets(selectedNodes.value, nodes.value, props.canEdit),
);
function canSelectNodes() {
  return !saving.value && !loading.value && !editingId.value && !dirty.value;
}
function setSelection(ids: string[]) {
  if (!canSelectNodes()) return;
  const wanted = new Set(ids);
  selectedIds.value = new Set(
    flatNodes.value.filter((n) => wanted.has(n.id)).map((n) => n.id),
  );
  selected.value = flatNodes.value.find(
    (n) => n.id === [...selectedIds.value].at(-1),
  );
  tagOpen.value = false;
  if (selectedIds.value.size !== 1) configVisible.value = false;
  resetPoint();
}
const marquee = useMinderMarquee(
  viewport,
  () => !hand.value && canSelectNodes(),
  setSelection,
);
watch(
  () => selected.value?.id,
  (id) => {
    if (!id || !selectedIds.value.has(id))
      selectedIds.value = new Set(id ? [id] : []);
  },
);
watch(flatNodes, (current) => {
  const available = new Set(current.map((n) => n.id));
  selectedIds.value = new Set(
    [...selectedIds.value].filter((id) => available.has(id)),
  );
});
const nodeOptions = computed(() =>
  flatNodes.value
    .filter((node) => ["root", "category", "collection"].includes(node.kind))
    .map((node) => ({
      value: node.id,
      label:
        node.kind === "root"
          ? node.name
          : node.kind === "category"
            ? node.name
            : `${planCategoryNames[node.category!]} / ${node.name}`,
    })),
);
const selectedOption = computed(() => {
  const node = selected.value;
  if (!node || ["root", "category", "collection"].includes(node.kind))
    return node?.id;
  if (node.configurationScope?.startsWith("root:"))
    return `category:${node.category}`;
  return node.nodeId
    ? `${node.category}:${node.nodeId}`
    : `default:${node.category}`;
});
const selectedPoint = computed(() =>
  selected.value?.nodeId
    ? nodes.value.find((node) => node.id === selected.value?.nodeId)
    : undefined,
);
const executionDraft = ref<ExecutionConfig>(),
  executionEditor = ref<InstanceType<typeof ExecutionConfiguration>>(),
  baseline = ref("");
const pointForm = reactive({ name: "" });
const selectedScope = computed(() => {
  const node = selected.value;
  if (
    !node?.category ||
    node.category === "functional" ||
    node.kind === "root" ||
    node.kind === "count"
  )
    return undefined;
  return (
    node.configurationScope ||
    (node.kind === "category"
      ? `root:${node.category}`
      : node.nodeId
        ? `node:${node.category}:${node.nodeId}`
        : `default:${node.category}`)
  );
});
const inheritedConfiguration = computed(() => {
  const scope = selectedScope.value,
    category = selected.value?.category;
  if (!scope || !category) return undefined;
  const parent = selectedPoint.value?.parentId;
  return executionCatalog.value?.configurations[
    parent ? `node:${category}:${parent}` : `root:${category}`
  ]?.effectiveConfig;
});
function draftState() {
  return JSON.stringify({
    name: pointForm.name,
    config: selectedScope.value ? executionDraft.value : undefined,
  });
}
function resetPoint() {
  pointForm.name =
    selectedPoint.value?.name ||
    (selected.value?.kind === "collection" ? selected.value.name : "");
  const entry = selectedScope.value
    ? executionCatalog.value?.configurations[selectedScope.value]
    : undefined;
  executionDraft.value = entry
    ? { ...entry.effectiveConfig, extended: entry.config.extended }
    : undefined;
  baseline.value = draftState();
}
const dirty = computed(() => draftState() !== baseline.value);
const hasChanges = computed(
  () => dirty.value || draft.dirty || !!editingId.value,
);
const tagConfiguration = computed(() =>
  planMinderTag(selected.value, executionCatalog.value, props.canEdit),
);
async function saveTag(value: string) {
  const tag = tagConfiguration.value;
  if (!tag || saving.value || loading.value || value === tag.value) return;
  if (dirty.value || editingId.value) {
    message.warning("请先保存或取消当前节点的修改");
    return;
  }
  if (!tag.options.some((option) => option.value === value)) return;
  try {
    const id = selected.value?.id;
    draft.configure(tag.scope, { ...tag.config, [tag.field]: value });
    selected.value = flatNodes.value.find((n) => n.id === id);
    resetPoint();
    console.info("脑图标签选择已进入整体保存", {
      计划: props.plan.id,
      作用域: tag.scope,
      字段: tag.field,
    });
    await savePoint();
  } catch (error) {
    console.error("脑图标签选择失败，草稿保留", error);
    message.error(
      error instanceof Error ? error.message : "标签保存失败，草稿已保留",
    );
  }
}
function nodeActions(node: PlanMinderNode) {
  const inherited = node.configurationScope
    ? executionCatalog.value?.configurations[node.configurationScope]?.config
        .extended
    : node.category
      ? executionCatalog.value?.configurations[
          node.nodeId
            ? `node:${node.category}:${node.nodeId}`
            : `default:${node.category}`
        ]?.config.extended
      : false;
  return planMinderActions(node, props.canEdit, !!inherited).filter(
    (action) => action !== "add" || canAdd.value,
  );
}
function beginNameEdit(id: string) {
  if (!props.canEdit || saving.value || loading.value || editingId.value)
    return;
  const node = flatNodes.value.find((n) => n.id === id);
  if (node?.kind !== "collection") return;
  selectById(id);
  if (selected.value?.id !== id || dirty.value || !canRename.value) return;
  editName.value = node.name;
  editingId.value = id;
}
function cancelNameEdit() {
  editingId.value = undefined;
  editName.value = "";
}
function commitNameEdit(): boolean {
  if (!editingId.value) return true;
  const node = flatNodes.value.find((n) => n.id === editingId.value);
  if (!node?.category || node.kind !== "collection") return false;
  try {
    if (
      editName.value.trim() !== node.name ||
      (node.nodeId && draft.isNew(node.nodeId))
    ) {
      const point = node.nodeId
        ? nodes.value.find((n) => n.id === node.nodeId)
        : draft.materializeDefault(node.category, editName.value);
      if (!point) throw new Error("测试集已不存在，请取消编辑并刷新");
      draft.rename(point.id, editName.value);
      selected.value = flatNodes.value.find(
        (n) => n.nodeId === point.id && n.category === node.category,
      );
      console.info("测试集行内改名已暂存", {
        计划: props.plan.id,
        分类: node.category,
      });
    }
    cancelNameEdit();
    resetPoint();
    return true;
  } catch (error) {
    console.error("测试集行内改名失败，文本保留", error);
    message.error(
      error instanceof Error ? error.message : "改名失败，文本已保留",
    );
    void nextTick(() =>
      viewport.value
        ?.querySelector<HTMLInputElement>(".minder-name-editor")
        ?.focus(),
    );
    return false;
  }
}
function handleNodeAction(action: MinderAction) {
  if (
    !selected.value ||
    !nodeActions(selected.value).includes(action) ||
    saving.value
  )
    return;
  if (action === "add") openCreate();
  else if (action === "associate") openAssociation();
  else if (action === "delete") removePoint();
  else if (action === "configure") {
    if (dirty.value) {
      message.warning("请先保存或取消当前节点的修改");
      return;
    }
    configVisible.value = !configVisible.value;
  } else {
    if (dirty.value) {
      message.warning("请先保存或取消当前节点的修改");
      return;
    }
    const node = selected.value,
      mode = node.executionMode === "parallel" ? "serial" : "parallel";
    if (node.kind === "root") draft.setExecutionMode(mode);
    else if (selectedScope.value && executionDraft.value)
      draft.configure(selectedScope.value, {
        ...executionDraft.value,
        executionMode: mode,
      });
    selected.value = flatNodes.value.find((n) => n.id === node.id);
    resetPoint();
    console.info("脑图执行方式已暂存", {
      计划: props.plan.id,
      节点: node.id,
      方式: mode,
    });
  }
}
const canRename = computed(
  () =>
    selected.value?.kind === "collection" &&
    (!selectedPoint.value ||
      selectedPoint.value.category === selected.value.category),
);
const poolOpen = ref(false),
  poolSelection = ref("new"),
  poolDraft = reactive({ name: "", environmentIds: [] as string[] });
function resetPool() {
  const pool = executionCatalog.value?.pools.find(
    (item) => item.id === poolSelection.value,
  );
  poolDraft.name = pool?.name || "";
  poolDraft.environmentIds = [...(pool?.environmentIds || [])];
}
function openPool() {
  poolSelection.value =
    executionDraft.value?.testResourcePoolId !== "DEFAULT"
      ? executionDraft.value?.testResourcePoolId || "new"
      : "new";
  resetPool();
  poolOpen.value = true;
}
async function savePool() {
  if (!poolDraft.name.trim() || !poolDraft.environmentIds.length) {
    message.warning("请填写资源池名称并选择执行节点");
    return;
  }
  saving.value = true;
  try {
    const pool = executionCatalog.value?.pools.find(
      (item) => item.id === poolSelection.value,
    );
    const catalog = await planExecutionApi.savePool(
      props.plan.id,
      {
        name: poolDraft.name.trim(),
        environmentIds: poolDraft.environmentIds,
        expectedRevision: pool?.revision || 0,
      },
      pool?.id,
    );
    if (draft.workspace) {
      draft.workspace.executionCatalog.pools = catalog.pools;
      draft.workspace.executionCatalog.resources = catalog.resources;
      draft.recalculate();
    }
    poolOpen.value = false;
    message.success("资源池已保存");
  } catch (error) {
    console.error("保存资源池失败", error);
    message.error("保存失败，请检查资源池或刷新版本");
  } finally {
    saving.value = false;
  }
}
function allowNavigation() {
  if (!hasChanges.value && !saving.value) return true;
  message.warning("请先保存或取消测试规划草稿");
  return false;
}
onBeforeRouteLeave(allowNavigation);
onBeforeRouteUpdate(allowNavigation);
let sequence = 0;
async function load() {
  if (hasChanges.value) {
    message.warning("请先保存或取消测试规划草稿");
    return;
  }
  const request = ++sequence;
  loading.value = true;
  failed.value = false;
  try {
    const result = await planMinderApi.load(props.plan.id);
    if (request === sequence) {
      draft.load(result);
      const activeId = selected.value?.id || "root";
      selected.value =
        flatNodes.value.find((node) => node.id === activeId) || tree.value;
      resetPoint();
    }
  } catch (error) {
    console.error("加载测试规划脑图失败", error);
    if (request === sequence) {
      selected.value = undefined;
      failed.value = true;
    }
  } finally {
    if (request === sequence) loading.value = false;
  }
}
async function loadEnvironments() {
  try {
    const all: Environment[] = [];
    let page = 1;
    while (true) {
      const result = await environmentApi.getEnvironments({ page, size: 100 });
      all.push(...result.items);
      if (all.length >= result.total || !result.items.length) break;
      page++;
    }
    environments.value = all;
  } catch (error) {
    console.error("加载测试集环境选项失败", error);
  }
}
function selectById(id: string) {
  if (editingId.value || saving.value || loading.value) return;
  if (dirty.value) {
    message.warning("请先保存或取消当前节点的修改");
    return;
  }
  selected.value = flatNodes.value.find((node) => node.id === id);
  selectedIds.value = new Set(selected.value ? [id] : []);
  tagOpen.value = false;
  if (
    selected.value?.kind === "root" ||
    (selected.value?.kind === "category" &&
      selected.value.category === "functional")
  )
    configVisible.value = false;
  resetPoint();
}
function selectCanvasNode(id: string, event: MouseEvent) {
  if (saving.value || loading.value || editingId.value) return;
  if (dirty.value) {
    message.warning("请先保存或取消当前节点的修改");
    return;
  }
  if (event.ctrlKey || event.metaKey) {
    const ids = new Set(selectedIds.value);
    ids.has(id) ? ids.delete(id) : ids.add(id);
    setSelection([...ids]);
    viewport.value?.focus({ preventScroll: true });
    return;
  }
  selectById(id);
  const node = selected.value;
  viewport.value?.focus({ preventScroll: true });
  if (node?.kind === "count" && props.canEdit) openAssociation();
  if (
    node &&
    ["environment", "resource"].includes(node.kind) &&
    props.canEdit
  ) {
    tagOpen.value = !!tagConfiguration.value;
  }
}
function toggleById(id: string) {
  const next = new Set(collapsed.value);
  next.has(id) ? next.delete(id) : next.add(id);
  collapsed.value = next;
}
function reorderPoints(parent: PlanMinderNode, ordered: PlanMinderNode[]) {
  if (
    !props.canEdit ||
    dirty.value ||
    editingId.value ||
    saving.value ||
    !parent.category
  )
    return;
  try {
    const category = parent.category;
    const ids = ordered
      .filter((n) => n.kind === "collection")
      .map((n) => n.nodeId || draft.materializeDefault(category).id);
    const parentId = parent.kind === "category" ? null : parent.nodeId || null;
    draft.reorder(category, parentId, ids);
    console.info("测试规划同级排序已暂存", {
      计划: props.plan.id,
      分类: category,
      数量: ids.length,
    });
  } catch (error) {
    console.error("暂存测试集排序失败", error);
    message.error(error instanceof Error ? error.message : "排序失败");
  }
}
function cancelDraft() {
  cancelNameEdit();
  draft.reset();
  selected.value =
    flatNodes.value.find((n) => n.id === selected.value?.id) || tree.value;
  resetPoint();
}

const canAdd = computed(
  () =>
    selected.value?.kind === "category" ||
    (selected.value?.kind === "collection" &&
      (!selectedPoint.value || !selectedPoint.value.parentId) &&
      (!selectedPoint.value ||
        selectedPoint.value.category === selected.value.category)),
);
function toggleSelected() {
  const node = selected.value;
  if (!node?.children?.length) return;
  const next = new Set(collapsed.value);
  next.has(node.id) ? next.delete(node.id) : next.add(node.id);
  collapsed.value = next;
}
function expandAll() {
  collapsed.value = new Set();
}
function collapseAll() {
  collapsed.value = new Set(
    tree.value.children
      ?.filter((node) => node.children?.length)
      .map((node) => node.id),
  );
}
function handleShortcut(event: KeyboardEvent) {
  const textTarget = (event.target as HTMLElement)?.closest(
    "input, textarea, select, [contenteditable=true]",
  );
  if (!textTarget && !event.isComposing && !event.repeat && canSelectNodes()) {
    if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "a") {
      event.preventDefault();
      setSelection(flatNodes.value.map((node) => node.id));
      return;
    }
    if (event.key === "Escape") {
      event.preventDefault();
      marquee.cancel();
      setSelection([]);
      return;
    }
  }

  if (
    (event.ctrlKey || event.metaKey) &&
    event.key.toLowerCase() === "s" &&
    !event.isComposing &&
    !event.repeat &&
    !(event.target as HTMLElement)?.closest(
      "input, textarea, [contenteditable=true]",
    )
  ) {
    event.preventDefault();
    void savePoint();
    return;
  }
  if (
    event.isComposing ||
    event.repeat ||
    event.ctrlKey ||
    event.metaKey ||
    event.altKey ||
    event.shiftKey
  )
    return;
  const node = selected.value;
  if (
    !node ||
    saving.value ||
    associateOpen.value ||
    advancedOpen.value ||
    editingId.value
  )
    return;
  if (
    (event.target as HTMLElement)?.closest(
      "input, textarea, select, button, [contenteditable=true]",
    )
  )
    return;
  if (selectedIds.value.size > 1) {
    if (event.key === "Backspace" && deletionTargets.value) {
      event.preventDefault();
      removePoint();
    }
    return;
  }
  if (event.key === "/" && node.children?.length) {
    event.preventDefault();
    toggleSelected();
  } else if (props.canEdit) {
    if (event.code === "Space" && node.kind === "collection") {
      event.preventDefault();
      beginNameEdit(node.id);
    } else if (
      (event.key === "Tab" && node.kind === "category") ||
      (event.key === "Enter" && node.kind === "collection")
    ) {
      event.preventDefault();
      openCreate();
    } else if (event.key === "Backspace" && node.kind === "collection") {
      event.preventDefault();
      removePoint();
    }
  }
}

async function changeZoom(value: number) {
  const element = viewport.value;
  if (!element) return;
  const before = zoom.value,
    left = zoomScroll(element.scrollLeft, before, value),
    top = zoomScroll(element.scrollTop, before, value);
  zoom.value = value;
  await nextTick();
  element.scrollTo({ left, top });
}
function locatePoint(point: { x: number; y: number }) {
  viewport.value?.scrollTo({
    left: cameraScroll(point.x, zoom.value),
    top: cameraScroll(point.y, zoom.value),
  });
}
function locateRoot() {
  const root = geometry.value?.nodes.root;
  if (root)
    locatePoint({ x: root.x + root.width / 2, y: root.y + root.height / 2 });
}
async function changeMode(value: MinderMode) {
  if (value === mode.value) return;
  initialPosition = true;
  viewPreferences.value = { ...viewPreferences.value, mode: value };
  console.info("脑图布局已切换", { 布局: value, 计划: props.plan.id });
}
async function fit() {
  await changeZoom(1);
  locateRoot();
}
async function fitCanvas() {
  const element = viewport.value;
  if (!element || !stageWidth.value || !stageHeight.value) return;
  await changeZoom(
    Math.max(
      0.25,
      Math.min(
        1,
        (element.clientWidth - 80) / stageWidth.value,
        (element.clientHeight - 80) / stageHeight.value,
      ),
    ),
  );
  locatePoint({ x: stageWidth.value / 2, y: stageHeight.value / 2 });
}
function viewCases() {
  const node = selected.value;
  if (!node?.category || !node.count) return;
  const tab = {
    functional: "featureCase",
    api: "apiCase",
    scenario: "apiScenario",
  }[node.category];
  void router.replace({
    query: {
      ...route.query,
      tab,
      caseTree: "COLLECTION",
      caseFolder: node.kind === "category" ? "all" : node.nodeId || "default",
    },
  });
}
const associateOpen = ref(false),
  advancedOpen = ref(false);
const pendingAssociation = computed(() =>
  selected.value?.category
    ? draft.association(selected.value.category, selected.value.nodeId)
    : undefined,
);
const associationDraft = computed(() =>
  selected.value?.category
    ? draft.associationPreview(selected.value.category, selected.value.nodeId)
    : draft.payload,
);
function openAssociation() {
  if (!props.canEdit || saving.value || loading.value) return;
  if (!commitNameEdit()) return;
  try {
    stageCurrentConfiguration();
    draft.validate();
    associateOpen.value = true;
  } catch (error) {
    console.error("打开脑图关联草稿失败，保留当前修改", error);
    message.error(error instanceof Error ? error.message : "请核对测试集配置");
  }
}
function stageAssociation(
  request: PlanAssociation,
  summary: CandidateSelectionPreview,
) {
  try {
    draft.associate(request, summary);
    console.info("脑图用例关联已暂存", {
      计划: props.plan.id,
      分类: request.category,
      数量: summary.count,
    });
    if (!configVisible.value) void savePoint();
    else message.success("关联选择已加入草稿，请保存规划");
  } catch (error) {
    console.error("暂存脑图用例关联失败", error);
    message.error(error instanceof Error ? error.message : "暂存关联失败");
  }
}
function openAdvanced() {
  if (saving.value || loading.value) return;
  if (hasChanges.value) {
    message.warning("请先保存或取消当前节点的修改");
    return;
  }
  advancedOpen.value = true;
}
function openCreate() {
  if (
    !props.canEdit ||
    !canAdd.value ||
    saving.value ||
    loading.value ||
    editingId.value
  )
    return;
  if (dirty.value) {
    message.warning("请先保存或取消当前节点的修改");
    return;
  }
  if (!selected.value?.category) return;
  try {
    const point = draft.insert(
      selected.value.category,
      selectedPoint.value?.id ||
        (selected.value.kind === "collection" ? "default" : undefined),
    );
    selected.value = flatNodes.value.find(
      (n) => n.nodeId === point.id && n.category === point.category,
    );
    resetPoint();
    editingId.value = selected.value?.id;
    editName.value = point.name;
    collapsed.value = new Set(
      [...collapsed.value].filter((id) => id !== `category:${point.category}`),
    );
    console.info("测试集新增草稿已暂存", {
      计划: props.plan.id,
      分类: point.category,
    });
    message.success("测试集已加入草稿，请保存规划");
  } catch (error) {
    console.error("暂存新增测试集失败", error);
    message.error(error instanceof Error ? error.message : "新增失败");
  }
}
function acceptWorkspace(result: MinderWorkspace) {
  tagOpen.value = false;
  const id = selected.value?.id;
  draft.load(result);
  selected.value = flatNodes.value.find((n) => n.id === id) || tree.value;
  resetPoint();
}
async function savePoint() {
  if (!props.canEdit || saving.value || !hasChanges.value) return;
  if (!commitNameEdit()) return;
  saving.value = true;
  try {
    stageCurrentConfiguration();
    draft.validate();
    const result = await planMinderApi.save(props.plan.id, draft.payload);
    acceptWorkspace(result);
    emit("changed");
    message.success("测试规划已保存");
  } catch (error: any) {
    console.error("保存完整测试规划失败", error);
    message.error(
      typeof error.response?.data?.detail === "string"
        ? error.response.data.detail
        : error.isAxiosError
          ? "保存失败，当前规划草稿已保留，请重试"
          : error instanceof Error
            ? error.message
            : "保存失败，当前规划草稿已保留",
    );
  } finally {
    saving.value = false;
  }
}
function stageCurrentConfiguration() {
  if (!dirty.value) return;
  let node = selectedPoint.value;
  const scope = selectedScope.value;
  if (canRename.value && selected.value?.category) {
    if (!node && pointForm.name.trim() !== selected.value.name) {
      node = draft.materializeDefault(
        selected.value.category,
        pointForm.name.trim(),
      );
      selected.value = flatNodes.value.find(
        (n) => n.nodeId === node!.id && n.category === node!.category,
      );
    }
    if (node) draft.rename(node.id, pointForm.name);
  }
  const currentScope =
    node && scope?.startsWith("default:")
      ? `node:${node.category}:${node.id}`
      : scope;
  if (currentScope && executionDraft.value)
    draft.configure(currentScope, executionDraft.value);
  selected.value =
    flatNodes.value.find((n) => n.id === selected.value?.id) || tree.value;
  resetPoint();
}
async function changed() {
  await load();
  emit("changed");
}
function removePoint() {
  const targets = deletionTargets.value;
  if (!targets?.length || !canSelectNodes()) {
    if (dirty.value) message.warning("请先保存或取消当前节点的修改");
    return;
  }
  const count = selectedIds.value.size;
  Modal.confirm({
    title:
      count > 1
        ? `删除选中的${count}个测试集及子测试集？`
        : "删除此测试集及子测试集？",
    content: "保存规划后取消其中的用例关联，原用例和历史执行记录保留。",
    okType: "danger",
    onOk() {
      if (!props.canEdit || !canSelectNodes()) return;
      try {
        draft.removeMany(targets);
        selectedIds.value = new Set();
        selected.value = undefined;
        tagOpen.value = false;
        configVisible.value = false;
        resetPoint();
        console.info("测试集批量删除已暂存", {
          计划: props.plan.id,
          选中数: count,
          删除根数: targets.length,
        });
        message.success("删除已加入草稿，请保存规划");
      } catch (error) {
        console.error("测试集批量删除失败，原草稿保留", error);
        message.error(error instanceof Error ? error.message : "删除失败");
      }
    },
  });
}
watch(
  () => props.plan.id,
  () => {
    sequence++;
    marquee.cancel();
    selectedIds.value = new Set();
    draft.clear();
    zoom.value = 1;
    collapsed.value = new Set();
    selected.value = undefined;
    configVisible.value = false;
    cancelNameEdit();
    tagOpen.value = false;
    associateOpen.value = false;
    advancedOpen.value = false;
    resetPoint();
    void load();
    void loadEnvironments();
  },
  { immediate: true },
);
</script>
<style scoped>
.planning-minder {
  min-width: 0;
  outline: none;
}
.planning-toolbar {
  display: flex;
  gap: 16px;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  margin: 16px 0;
}
.planning-toolbar :deep(.ant-select) {
  width: 240px;
}
.minder-layout {
  position: relative;
  display: flex;
  min-width: 0;
  border: 1px solid var(--ms-border);
}
.minder-canvas {
  flex: 1;
  position: relative;
  min-width: 0;
}
.minder-connections {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: visible;
}
.hand-mode,
.hand-mode :deep(.minder-node) {
  cursor: grab;
  touch-action: none;
  user-select: none;
}
.hand-mode:active {
  cursor: grabbing;
}
.layout-error {
  position: absolute;
  top: 50px;
  left: 16px;
  right: 16px;
  z-index: 50;
}
.fullscreen {
  background: white;
  width: 100vw;
  height: 100vh;
}
.fullscreen .minder-viewport,
.fullscreen .node-configuration {
  height: 100vh;
  max-height: 100vh;
}
.minder-viewport {
  position: relative;
  min-width: 0;
  flex: 1;
  overflow: auto;
}
.minder-viewport {
  padding: 0;
  height: clamp(420px, calc(100vh - 320px), 700px);
}
.minder-marquee {
  position: absolute;
  z-index: 40;
  pointer-events: none;
  border: 1px solid var(--primary-color);
  background: var(--primary-selection-overlay);
}
.minder-sizing {
  position: relative;
}
.minder-stage {
  position: absolute;
  width: max-content;
  transform-origin: 0 0;
}
.zoom-value {
  min-width: 42px;
  text-align: center;
}
.node-configuration {
  width: 320px;
  max-height: clamp(420px, calc(100vh - 320px), 700px);
  overflow-y: auto;
  flex-shrink: 0;
  padding: 16px;
  border-left: 1px solid var(--ms-border);
}
.node-configuration h3 {
  font-size: 15px;
  overflow-wrap: anywhere;
}
.fold-button {
  margin-bottom: 16px;
}
.point-form {
  margin-top: 16px;
}
@media (max-width: 768px) {
  .fullscreen.config-open .minder-viewport {
    height: 65vh;
  }
  .fullscreen.config-open .node-configuration {
    height: 35vh;
    max-height: 35vh;
    overflow-y: auto;
  }
  .minder-layout {
    flex-direction: column;
  }
  .node-configuration {
    width: 100%;
    max-height: none;
    overflow-y: visible;
    border-left: 0;
    border-top: 1px solid var(--ms-border);
  }
  .planning-toolbar :deep(.ant-select) {
    max-width: 100%;
  }
}
</style>
