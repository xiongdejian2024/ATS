<template>
  <section class="planning-minder" aria-label="测试规划脑图" tabindex="0">
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
          @click="zoom = Math.max(0.25, zoom - 0.1)"
          >−</a-button
        >
        <span class="zoom-value">{{ Math.round(zoom * 100) }}%</span>
        <a-button aria-label="放大脑图" @click="zoom = Math.min(2, zoom + 0.1)"
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
      ><div class="minder-layout">
        <div
          ref="viewport"
          class="minder-viewport"
          tabindex="0"
          aria-label="脑图画布，按斜线展开收起，Tab 添加分类下测试集，Enter 添加同级测试集，Backspace 删除"
          @keydown="handleShortcut"
        >
          <div
            class="minder-sizing"
            :style="{
              width: `${stageWidth * zoom}px`,
              height: `${stageHeight * zoom}px`,
            }"
          >
            <div
              ref="stage"
              class="minder-stage"
              :style="{ transform: `scale(${zoom})` }"
            >
              <PlanningMinderBranch
                v-if="!failed"
                :node="tree"
                :points="nodes"
                :selected-id="selected?.id"
                :collapsed="collapsed"
                :can-edit="canEdit && !saving && !dirty"
                @select="selectCanvasNode"
                @toggle="toggleById"
                @reorder="reorderPoints"
              />
            </div>
          </div>
        </div>
        <aside v-if="selected" class="node-configuration">
          <h3>{{ selected.name }}</h3>
          <p>关联用例 {{ selected.count }} 条</p>
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
              ><a-button v-if="canEdit" @click="openAssociation"
                >关联用例</a-button
              ><a-button :disabled="!selected.count" @click="viewCases"
                >查看用例</a-button
              ></a-space
            >
            <a-form
              v-if="canRename"
              layout="vertical"
              class="point-form"
              :disabled="!canEdit"
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
              :disabled="!canEdit"
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
      v-model:open="createOpen"
      title="添加测试集"
      :confirm-loading="saving"
      @ok="createPoint"
      ><a-form layout="vertical"
        ><a-form-item label="分类">{{
          planCategoryNames[selected?.category || "functional"]
        }}</a-form-item
        ><a-form-item label="名称" required
          ><a-input
            v-model:value="newName"
            :maxlength="255" /></a-form-item></a-form
    ></a-modal>
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
import { useElementSize } from "@vueuse/core";
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
import { PlanMinderDraft } from "./planMinderDraft";
import PlanningMinderBranch from "./PlanningMinderBranch.vue";
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
const { width: stageWidth, height: stageHeight } = useElementSize(stage);
const tree = computed(() =>
  buildPlanMinder(props.plan.name, nodes.value, entries.value, {
    environmentNames: Object.fromEntries(
      environments.value.map((item) => [item.id, item.name]),
    ),
    defaultEnvironmentId: props.plan.environmentId,
    executionCatalog: executionCatalog.value,
  }),
);
const flatNodes = computed(() => {
  const result: PlanMinderNode[] = [];
  function walk(node: PlanMinderNode) {
    result.push(node);
    node.children?.forEach(walk);
  }
  walk(tree.value);
  return result;
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
const hasChanges = computed(() => dirty.value || draft.dirty);
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
  if (dirty.value) {
    message.warning("请先保存或取消当前节点的修改");
    return;
  }
  selected.value = flatNodes.value.find((node) => node.id === id);
  resetPoint();
}
function selectCanvasNode(id: string) {
  if (dirty.value) {
    message.warning("请先保存或取消当前节点的修改");
    return;
  }
  selectById(id);
  const node = selected.value;
  viewport.value?.focus({ preventScroll: true });
  if (node?.kind === "count" && props.canEdit) openAssociation();
  if (node && ["environment", "resource"].includes(node.kind) && props.canEdit)
    void nextTick(() =>
      executionEditor.value?.focus(node.kind as "environment" | "resource"),
    );
}
function toggleById(id: string) {
  const next = new Set(collapsed.value);
  next.has(id) ? next.delete(id) : next.add(id);
  collapsed.value = next;
}
function reorderPoints(parent: PlanMinderNode, ordered: PlanMinderNode[]) {
  if (!props.canEdit || dirty.value || saving.value || !parent.category) return;
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
    createOpen.value ||
    associateOpen.value ||
    advancedOpen.value
  )
    return;
  if (
    (event.target as HTMLElement)?.closest(
      "input, textarea, select, button, [contenteditable=true]",
    )
  )
    return;
  if (event.key === "/" && node.children?.length) {
    event.preventDefault();
    toggleSelected();
  } else if (props.canEdit) {
    if (
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

function fit() {
  zoom.value = 1;
  viewport.value?.scrollTo({ top: 0, left: 0, behavior: "smooth" });
}
function fitCanvas() {
  const element = viewport.value;
  if (!element || !stageWidth.value || !stageHeight.value) return;
  zoom.value = Math.max(
    0.25,
    Math.min(
      1,
      (element.clientWidth - 80) / stageWidth.value,
      (element.clientHeight - 80) / stageHeight.value,
    ),
  );
  element.scrollTo({ top: 0, left: 0 });
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
const createOpen = ref(false),
  associateOpen = ref(false),
  advancedOpen = ref(false),
  newName = ref("");
function openAssociation() {
  if (!props.canEdit) return;
  if (hasChanges.value) {
    message.warning("请先保存测试规划，再关联用例");
    return;
  }
  associateOpen.value = true;
}
function openAdvanced() {
  if (hasChanges.value) {
    message.warning("请先保存或取消当前节点的修改");
    return;
  }
  advancedOpen.value = true;
}
function openCreate() {
  if (!props.canEdit || !canAdd.value) return;
  if (dirty.value) {
    message.warning("请先保存或取消当前节点的修改");
    return;
  }
  newName.value = "默认测试集";
  createOpen.value = true;
}
function createPoint() {
  if (!props.canEdit || !selected.value?.category) return;
  try {
    const point = draft.add(
      selected.value.category,
      newName.value,
      selectedPoint.value?.id ||
        (selected.value.kind === "collection" ? "default" : undefined),
    );
    createOpen.value = false;
    selected.value = flatNodes.value.find(
      (n) => n.nodeId === point.id && n.category === point.category,
    );
    resetPoint();
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
  const id = selected.value?.id;
  draft.load(result);
  selected.value = flatNodes.value.find((n) => n.id === id) || tree.value;
  resetPoint();
}
async function savePoint() {
  if (!props.canEdit || saving.value || !hasChanges.value) return;
  saving.value = true;
  try {
    let node = selectedPoint.value;
    const scope = selectedScope.value;
    if (dirty.value) {
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
async function changed() {
  await load();
  emit("changed");
}
function removePoint() {
  const node = selected.value;
  if (
    !props.canEdit ||
    !canRename.value ||
    !node?.category ||
    dirty.value ||
    saving.value
  ) {
    if (dirty.value) message.warning("请先保存或取消当前节点的修改");
    return;
  }
  Modal.confirm({
    title: "删除此测试集及子测试集？",
    content: "保存规划后取消其中的用例关联，原用例和历史执行记录保留。",
    okType: "danger",
    onOk() {
      if (node.nodeId) draft.remove(node.nodeId);
      else draft.removeDefault(node.category!);
      selected.value = flatNodes.value.find(
        (n) => n.id === `category:${node.category}`,
      );
      resetPoint();
      console.info("测试集删除已暂存", {
        计划: props.plan.id,
        分类: node.category,
      });
      message.success("删除已加入草稿，请保存规划");
    },
  });
}
watch(
  () => props.plan.id,
  () => {
    sequence++;
    draft.clear();
    zoom.value = 1;
    collapsed.value = new Set();
    selected.value = undefined;
    createOpen.value = false;
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
  display: flex;
  min-width: 0;
  border: 1px solid var(--ms-border);
}
.minder-viewport {
  min-width: 0;
  flex: 1;
  overflow: auto;
}
.minder-viewport {
  padding: 40px;
  height: clamp(420px, calc(100vh - 320px), 700px);
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
