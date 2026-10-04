<template>
  <section class="planning-minder" aria-label="测试规划脑图" tabindex="0">
    <a-alert
      message="通过测试集组织用例；执行批次保留创建时的用例和配置。"
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
        ><a-button @click="fit">重置视图</a-button
        ><a-button :loading="loading" @click="load">刷新</a-button
        ><a-button @click="openAdvanced">用例和场景配置</a-button></a-space
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
          <v-chart
            ref="chart"
            :option="option"
            class="plan-chart"
            :style="{ minWidth: `${chartWidth}px` }"
            autoresize
            @click="selectNode"
          />
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
              v-if="selectedPoint"
              layout="vertical"
              class="point-form"
              :disabled="!canEdit"
            >
              <a-form-item label="测试集名称" required
                ><a-input v-model:value="pointForm.name" :maxlength="255"
              /></a-form-item>
              <template v-if="selected.category !== 'functional'">
                <a-form-item label="继承上级配置"
                  ><a-switch
                    v-model:checked="pointForm.inherit"
                    :disabled="!canEdit"
                    @change="changeInheritance"
                /></a-form-item>
                <a-alert
                  v-if="selectedPoint.category !== selected.category"
                  message="此节点是多个分类共用的父测试集，配置会影响其下级测试集。"
                  type="info"
                  show-icon
                />
                <a-form-item label="执行方式"
                  ><a-select
                    :value="
                      pointForm.inherit
                        ? selectedPoint.effectiveConfig.executionMode
                        : pointForm.executionMode
                    "
                    :disabled="!canEdit || pointForm.inherit"
                    @change="changeExecutionMode"
                    allow-clear
                    placeholder="继承计划/父测试集配置"
                    :options="[
                      { value: 'serial', label: '串行' },
                      { value: 'parallel', label: '并行' },
                    ]"
                /></a-form-item>
                <a-form-item label="环境"
                  ><a-select
                    ref="environmentSelect"
                    :value="
                      pointForm.inherit
                        ? selectedPoint.effectiveConfig.environmentId
                        : pointForm.environmentId
                    "
                    :disabled="!canEdit || pointForm.inherit"
                    allow-clear
                    placeholder="继承计划/父测试集环境"
                    :options="
                      environments.map((item) => ({
                        value: item.id,
                        label: item.name,
                      }))
                    "
                    @change="changeEnvironment"
                /></a-form-item>
                <a-form-item label="资源池"
                  ><a-select
                    ref="resourceSelect"
                    :value="
                      pointForm.inherit
                        ? selectedPoint.effectiveConfig.resourcePool
                        : pointForm.resourcePool
                    "
                    :disabled="!canEdit || pointForm.inherit"
                    mode="multiple"
                    placeholder="继承父配置"
                    :options="
                      environments.map((item) => ({
                        value: item.id,
                        label: item.name,
                      }))
                    "
                    @change="changeResourcePool"
                /></a-form-item>
              </template>
              <a-space v-if="canEdit" wrap
                ><a-button type="primary" :loading="saving" @click="savePoint"
                  >保存</a-button
                ><a-button :disabled="saving" @click="resetPoint"
                  >取消修改</a-button
                ><a-button danger :disabled="saving" @click="removePoint"
                  >删除测试集</a-button
                ></a-space
              >
            </a-form>
          </template>
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
import {
  useRouter,
  useRoute,
  onBeforeRouteLeave,
  onBeforeRouteUpdate,
} from "vue-router";
import { message, Modal } from "ant-design-vue";
import { use } from "echarts/core";
import { TreeChart } from "echarts/charts";
import { TooltipComponent } from "echarts/components";
import { CanvasRenderer } from "echarts/renderers";
import VChart from "vue-echarts";
import type { TestPlan, Environment } from "@/types";
import { environmentApi } from "@/api/environment";
import { planTreeApi, type PlanNode } from "@/api/planTree";
import {
  planCaseWorkspaceApi,
  type PlanCaseEntry,
} from "@/api/planCaseWorkspace";
import {
  buildPlanMinder,
  presentPlanMinder,
  planCategoryNames,
  type PlanCategory,
  type PlanMinderNode,
} from "./planMinderTree";
import PlanCaseAssociateDrawer from "./PlanCaseAssociateDrawer.vue";
import PlanTreeWorkspace from "./PlanTreeWorkspace.vue";
use([TreeChart, TooltipComponent, CanvasRenderer]);
const props = defineProps<{ plan: TestPlan; canEdit: boolean }>(),
  emit = defineEmits<{ changed: []; configurePlan: [] }>(),
  router = useRouter(),
  route = useRoute();
const nodes = ref<PlanNode[]>([]),
  entries = ref<Record<PlanCategory, PlanCaseEntry[]>>({
    functional: [],
    api: [],
    scenario: [],
  }),
  environments = ref<Environment[]>([]),
  usesTree = ref(false),
  loading = ref(false),
  failed = ref(false),
  saving = ref(false),
  selected = ref<PlanMinderNode>(),
  chart = ref<InstanceType<typeof VChart>>(),
  viewport = ref<HTMLElement>(),
  collapsed = ref(new Set<string>());
const tree = computed(() =>
  buildPlanMinder(props.plan.name, nodes.value, entries.value, {
    environmentNames: Object.fromEntries(
      environments.value.map((item) => [item.id, item.name]),
    ),
    defaultEnvironmentId: props.plan.environmentId,
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
  return node.nodeId
    ? `${node.category}:${node.nodeId}`
    : `default:${node.category}`;
});
const selectedPoint = computed(() =>
  selected.value?.nodeId
    ? nodes.value.find((node) => node.id === selected.value?.nodeId)
    : undefined,
);
const pointForm = reactive({
  name: "",
  inherit: true,
  executionMode: undefined as "serial" | "parallel" | undefined,
  environmentId: undefined as string | undefined,
  resourcePool: [] as string[],
});
function resetPoint() {
  const node = selectedPoint.value;
  pointForm.name = node?.name || "";
  pointForm.inherit = !hasOwnConfiguration(node);
  pointForm.executionMode = node?.config.executionMode || undefined;
  pointForm.environmentId = node?.config.environmentId || undefined;
  pointForm.resourcePool = [...(node?.config.resourcePool || [])];
}
function hasOwnConfiguration(node?: PlanNode) {
  return !!(
    node?.config.executionMode ||
    node?.config.environmentId ||
    node?.config.resourcePool?.length
  );
}
function changeExecutionMode(value: unknown) {
  pointForm.executionMode =
    value === "serial" || value === "parallel" ? value : undefined;
}
function changeEnvironment(value: unknown) {
  pointForm.environmentId = typeof value === "string" ? value : undefined;
  pointForm.resourcePool = [];
}
function changeResourcePool(value: unknown) {
  pointForm.resourcePool = Array.isArray(value)
    ? value.filter((item): item is string => typeof item === "string")
    : [];
  pointForm.environmentId = undefined;
}
function changeInheritance(inherit: boolean) {
  if (inherit) {
    pointForm.executionMode = undefined;
    pointForm.environmentId = undefined;
    pointForm.resourcePool = [];
  } else {
    const effective = selectedPoint.value?.effectiveConfig;
    pointForm.executionMode = effective?.executionMode || "serial";
    pointForm.environmentId = effective?.environmentId || undefined;
    pointForm.resourcePool = [...(effective?.resourcePool || [])];
  }
}
const environmentSelect = ref<{ focus: () => void }>(),
  resourceSelect = ref<{ focus: () => void }>();
const dirty = computed(() => {
  const node = selectedPoint.value;
  if (!node) return false;
  return (
    pointForm.name !== node.name ||
    pointForm.inherit === hasOwnConfiguration(node) ||
    (!pointForm.inherit &&
      (pointForm.executionMode !== (node.config.executionMode || undefined) ||
        pointForm.environmentId !== (node.config.environmentId || undefined) ||
        JSON.stringify(pointForm.resourcePool) !==
          JSON.stringify(node.config.resourcePool || [])))
  );
});
const presentedTree = computed(() =>
  presentPlanMinder(tree.value, collapsed.value),
);
const chartWidth = computed(() => {
  function depth(node: PlanMinderNode): number {
    return 1 + Math.max(0, ...(node.children || []).map(depth));
  }
  return Math.max(950, 400 + (depth(presentedTree.value) - 1) * 210);
});
function allowNavigation() {
  if (!dirty.value) return true;
  message.warning("请先保存或取消当前测试集的修改");
  return false;
}
onBeforeRouteLeave(allowNavigation);
onBeforeRouteUpdate(allowNavigation);
const option = computed(() => ({
  tooltip: {
    trigger: "item",
    renderMode: "richText",
    formatter: (item: any) => item.data.name,
  },
  series: [
    {
      type: "tree",
      data: [presentedTree.value],
      orient: "LR",
      roam: true,
      expandAndCollapse: false,
      initialTreeDepth: -1,
      top: 40,
      bottom: 40,
      left: 180,
      right: 220,
      symbolSize: 9,
      label: {
        formatter: (item: any) =>
          `${item.data.executionMode ? (item.data.executionMode === "parallel" ? "并行 · " : "串行 · ") : ""}${item.data.name}`,
        position: "left",
        align: "right",
        fontSize: 12,
        width: 150,
        overflow: "truncate",
        backgroundColor: "#f7f8fa",
        padding: [7, 10],
        borderRadius: 3,
      },
      leaves: { label: { position: "right", align: "left", width: 110 } },
      lineStyle: { color: "#c5b1d0", curveness: 0.4 },
      itemStyle: { color: "#811fa3" },
      emphasis: { focus: "descendant" },
      animationDuration: 180,
    },
  ],
}));
let sequence = 0;
async function load() {
  if (dirty.value) {
    message.warning("请先保存或取消当前测试集的修改");
    return;
  }
  const request = ++sequence;
  loading.value = true;
  failed.value = false;
  try {
    const [points, functional, api, scenario] = await Promise.all([
      planTreeApi.list(props.plan.id),
      ...(["functional", "api", "scenario"] as PlanCategory[]).map((category) =>
        planCaseWorkspaceApi.list(props.plan.id, {
          category,
          view: "mind",
          tree_type: "COLLECTION",
          folder: "all",
          page: 1,
          size: 100,
        }),
      ),
    ]);
    if (request === sequence) {
      nodes.value = points;
      entries.value = {
        functional: functional.items,
        api: api.items,
        scenario: scenario.items,
      };
      usesTree.value = functional.usesTree;
      const activeId = selected.value?.id || "root";
      selected.value =
        flatNodes.value.find((node) => node.id === activeId) || tree.value;
      resetPoint();
    }
  } catch (error) {
    console.error("加载测试规划脑图失败", error);
    if (request === sequence) {
      nodes.value = [];
      entries.value = { functional: [], api: [], scenario: [] };
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
    message.warning("请先保存或取消当前测试集的修改");
    return;
  }
  selected.value = flatNodes.value.find((node) => node.id === id);
  resetPoint();
}
function selectNode(event: unknown) {
  if (!event || typeof event !== "object" || !("data" in event)) return;
  const data = event.data;
  if (!data || typeof data !== "object" || !("id" in data)) return;
  const node = flatNodes.value.find((item) => item.id === data.id);
  if (!node) return;
  selectById(node.id);
  if (dirty.value) return;
  viewport.value?.focus({ preventScroll: true });
  if (node.kind === "count" && props.canEdit && !dirty.value)
    associateOpen.value = true;
  if (["environment", "resource"].includes(node.kind) && props.canEdit) {
    void nextTick(() =>
      (node.kind === "environment"
        ? environmentSelect.value
        : resourceSelect.value
      )?.focus(),
    );
  }
}

const canAdd = computed(
  () =>
    selected.value?.kind === "category" ||
    (selected.value?.kind === "collection" && !!selected.value.nodeId),
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
      (event.key === "Enter" && node.kind === "collection" && node.nodeId)
    ) {
      event.preventDefault();
      openCreate();
    } else if (
      event.key === "Backspace" &&
      node.kind === "collection" &&
      node.nodeId
    ) {
      event.preventDefault();
      removePoint();
    }
  }
}

function fit() {
  chart.value?.clear();
  chart.value?.setOption(option.value);
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
  if (dirty.value) {
    message.warning("请先保存或取消当前测试集的修改");
    return;
  }
  associateOpen.value = true;
}
function openAdvanced() {
  if (dirty.value) {
    message.warning("请先保存或取消当前测试集的修改");
    return;
  }
  advancedOpen.value = true;
}
function openCreate() {
  if (!props.canEdit || !canAdd.value) return;
  if (dirty.value) {
    message.warning("请先保存或取消当前测试集的修改");
    return;
  }
  newName.value = "默认测试集";
  createOpen.value = true;
}
async function createPoint() {
  if (!props.canEdit) return;
  if (!newName.value.trim()) {
    message.warning("请填写测试集名称");
    return;
  }
  saving.value = true;
  try {
    const parent = selectedPoint.value?.parentId;
    const row = await planTreeApi.create(props.plan.id, {
      name: newName.value.trim(),
      nodeType: "point",
      category: selected.value?.category || "functional",
      parentId: parent || null,
      position:
        Math.max(
          -1,
          ...nodes.value
            .filter((node) => (node.parentId || null) === (parent || null))
            .map((node) => node.position),
        ) + 1,
      config: {},
    });
    createOpen.value = false;
    selected.value = {
      id: `${row.category}:${row.id}`,
      name: row.name,
      nodeId: row.id,
      kind: "collection",
      category: row.category,
      count: 0,
    };
    await changed();
    message.success("测试集已添加");
  } catch (error) {
    console.error("添加测试集失败", error);
    message.error("添加失败，请检查名称和分类");
  } finally {
    saving.value = false;
  }
}
async function savePoint() {
  const node = selectedPoint.value;
  if (!props.canEdit || !node) return;
  if (!pointForm.name.trim()) {
    message.warning("请填写测试集名称");
    return;
  }
  saving.value = true;
  try {
    const updated = await planTreeApi.update(node.id, {
      name: pointForm.name.trim(),
      config:
        selected.value?.category === "functional"
          ? node.config
          : pointForm.inherit
            ? {}
            : {
                ...node.config,
                executionMode: pointForm.executionMode || null,
                environmentId: pointForm.environmentId || null,
                resourcePool: pointForm.resourcePool,
              },
    });
    nodes.value = nodes.value.map((item) =>
      item.id === node.id ? updated : item,
    );
    resetPoint();
    await changed();
    message.success("测试集配置已保存");
  } catch (error) {
    console.error("保存测试集脑图配置失败", error);
    message.error("保存失败，请核对配置");
  } finally {
    saving.value = false;
  }
}
async function changed() {
  await load();
  emit("changed");
}
function removePoint() {
  const node = selectedPoint.value;
  if (!props.canEdit || !node) return;
  Modal.confirm({
    title: "删除此测试集及子测试集？",
    content: usesTree.value
      ? "其中的用例关联会取消，原用例和历史执行记录保留。"
      : "其中的用例移至默认测试集，原用例和历史执行记录保留。",
    okType: "danger",
    async onOk() {
      try {
        await planTreeApi.remove(node.id);
        selected.value = undefined;
        await changed();
        message.success("测试集已删除");
      } catch (error) {
        console.error("删除脑图测试集失败", error);
        message.error("删除失败");
        throw error;
      }
    },
  });
}
watch(
  () => props.plan.id,
  () => {
    sequence++;
    collapsed.value = new Set();
    selected.value = undefined;
    createOpen.value = false;
    associateOpen.value = false;
    advancedOpen.value = false;
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
.plan-chart {
  height: clamp(420px, calc(100vh - 320px), 700px);
  min-width: 950px;
  width: 100%;
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
