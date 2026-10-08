<template>
  <section
    ref="host"
    class="functional-minder"
    aria-label="功能用例执行脑图"
    tabindex="0"
    @keydown="shortcut"
  >
    <div class="minder-toolbar" role="toolbar">
      <a-space wrap>
        <a-button @click="resetView">重置视图</a-button>
        <a-button @click="collapseAll">收起全部</a-button>
        <a-button :type="hand ? 'primary' : 'default'" @click="hand = !hand"
          >手形</a-button
        >
        <a-select
          v-model:value="mode"
          :options="minderModes"
          style="width: 140px"
        />
        <a-button
          aria-label="缩小脑图"
          @click="zoom = Math.max(0.5, zoom - 0.1)"
          >−</a-button
        >
        <span>{{ Math.round(zoom * 100) }}%</span>
        <a-button aria-label="放大脑图" @click="zoom = Math.min(2, zoom + 0.1)"
          >+</a-button
        >
        <a-button @click="toggle">{{
          isFullscreen ? "退出全屏" : "全屏"
        }}</a-button>
        <a-button
          :loading="loading"
          :disabled="saving || uploading"
          @click="refreshSafely"
          >刷新</a-button
        >
      </a-space>
      <span class="shortcut-hint">选择用例后：S 通过 / E 失败 / B 阻塞</span>
    </div>
    <nav class="minder-breadcrumb" aria-label="脑图目录路径">
      <template v-for="(item, index) in folderPath" :key="item.id">
        <span v-if="index" aria-hidden="true"> / </span>
        <a-button
          type="link"
          size="small"
          :disabled="item.id === folder || saving || uploading"
          @click="emit('navigate', item.id)"
          >{{ item.name }}</a-button
        >
      </template>
    </nav>
    <FunctionalMinderOperations
      ref="operations"
      :plan-id="plan.id"
      :selection="operationScope"
      :show-menu="selected.size > 1"
      :can-execute="listing.canExecute"
      :can-modify="canEdit"
      :before-action="prepareOperation"
      @changed="operationsChanged"
    />
    <a-space v-if="selected.size > 1" class="multi-selection"
      ><span>已选择 {{ selected.size }} 个节点</span>
      <a-button
        v-if="listing.canExecute"
        size="small"
        type="primary"
        :loading="previewLoading"
        :disabled="!operationScope || saving || uploading"
        @click="openSelection()"
        >批量执行</a-button
      ><a-button
        size="small"
        :disabled="saving || uploading || formOpen"
        @click="clearSelection"
        >取消选择</a-button
      ></a-space
    >
    <a-alert v-if="error" type="error" :message="error" show-icon />
    <a-alert
      v-if="layoutFailed"
      type="error"
      message="脑图布局失败，请刷新重试"
    />
    <div class="minder-layout">
      <div class="canvas-host">
        <a-spin :spinning="loading">
          <div
            ref="viewport"
            class="minder-viewport"
            tabindex="0"
            @pointerdown="startMarquee"
          >
            <div
              v-if="marqueeStyle"
              class="minder-marquee"
              :style="marqueeStyle"
            />
            <div
              class="minder-sizing"
              :style="{
                width: `${(geometry?.width || 800) * zoom + 80}px`,
                height: `${(geometry?.height || 400) * zoom + 80}px`,
              }"
            >
              <div
                ref="stage"
                class="minder-stage"
                :style="{
                  transform: `scale(${zoom})`,
                  opacity: geometry ? 1 : 0,
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
                    />
                  </g>
                </svg>
                <FunctionalMinderBranch
                  :node="tree"
                  :geometry="geometry"
                  :selected="selected"
                  :collapsed="collapsed"
                  @toggle="toggleNode"
                  @select="selectNode"
                >
                  <template #menu="{ node }">
                    <div
                      v-if="['root', 'folder', 'case'].includes(node.kind)"
                      class="node-menu"
                    >
                      <a-button
                        v-if="listing.canExecute && !isRecycled(node)"
                        size="small"
                        :disabled="saving || uploading || previewLoading"
                        @click="openForm(node)"
                        >执行</a-button
                      >
                      <a-button
                        v-if="node.kind === 'folder'"
                        size="small"
                        :disabled="saving || uploading"
                        @click="emit('navigate', node.folderId!)"
                        >进入目录</a-button
                      >
                      <a-dropdown
                        v-if="listing.canExecute && !isRecycled(node)"
                        :trigger="['click']"
                        ><a-button size="small" :disabled="operations?.isOpen"
                          >缺陷 ▾</a-button
                        ><template #overlay
                          ><a-menu @click="operations?.defectAction($event)"
                            ><a-menu-item key="create">新建缺陷</a-menu-item
                            ><a-menu-item key="associate"
                              >关联缺陷</a-menu-item
                            ></a-menu
                          ></template
                        ></a-dropdown
                      >
                      <a-dropdown v-if="canEdit" :trigger="['click']"
                        ><a-button size="small" :disabled="operations?.isOpen"
                          >更多 ▾</a-button
                        ><template #overlay
                          ><a-menu @click="operations?.operation($event)"
                            ><a-menu-item key="assign">更改执行人</a-menu-item
                            ><a-menu-item key="unlink"
                              >取消关联</a-menu-item
                            ></a-menu
                          ></template
                        ></a-dropdown
                      >
                      <a-button
                        v-if="node.kind === 'case'"
                        size="small"
                        @click="emitOpen(node)"
                        >详情</a-button
                      >
                    </div>
                  </template>
                </FunctionalMinderBranch>
              </div>
            </div>
          </div>
        </a-spin>
        <PlanningMinderNavigator
          :zoom="zoom"
          :hand="hand"
          :preview="preview"
          :geometry="geometry"
          :visible="visibleBox"
          :shortcuts="executionShortcuts"
          @zoom="changeZoom"
          @hand="hand = $event"
          @preview="preview = $event"
          @camera="locateRoot"
          @locate="locatePoint"
        />
      </div>
      <aside v-if="selectedRow" class="minder-sidebar">
        <a-space
          ><strong>{{ selectedRow.caseCode }} {{ selectedRow.name }}</strong
          ><a-button type="text" aria-label="关闭用例侧栏" @click="closeSidebar"
            >×</a-button
          ></a-space
        >
        <a-alert v-if="detailFailed" type="error" message="用例详情加载失败"
          ><template #action><a @click="loadDetail">重试</a></template></a-alert
        >
        <a-spin :spinning="detailLoading">
          <a-tabs v-model:active-key="sideTab">
            <a-tab-pane key="basic" tab="基本信息">
              <a-descriptions :column="1"
                ><a-descriptions-item label="优先级">{{
                  selectedRow.priority
                }}</a-descriptions-item
                ><a-descriptions-item label="测试集">{{
                  selectedRow.collectionName
                }}</a-descriptions-item
                ><a-descriptions-item label="模块">{{
                  selectedRow.moduleName
                }}</a-descriptions-item
                ><a-descriptions-item label="执行人">{{
                  selectedRow.executorName || "—"
                }}</a-descriptions-item></a-descriptions
              >
            </a-tab-pane>
            <a-tab-pane key="attachment" tab="附件">
              <CaseAttachments
                v-if="detail?.canReadCase && !selectedRow.recycled"
                :key="selectedRow.id"
                :project-id="selectedRow.projectId"
                :association-key="selectedRow.id"
                read-only
              />
              <a-empty v-else description="当前无主用例附件访问权限" />
            </a-tab-pane>
            <a-tab-pane key="defect" tab="缺陷"
              ><PlanDefects
                ref="defectPanel"
                :key="selectedRow.id"
                :plan-id="plan.id"
                :association-key="selectedRow.id"
                :editable="canEdit && !selectedRow.recycled"
            /></a-tab-pane>
            <a-tab-pane key="history" :tab="`执行历史 (${detail?.total || 0})`">
              <a-empty
                v-if="detail && !detail.history.length"
                description="暂无独立执行记录"
              />
              <article
                v-for="record in detail?.history || []"
                :key="record.id"
                class="history-record"
              >
                <a-tag>{{
                  functionalResultLabels[record.result] || record.result
                }}</a-tag
                ><span
                  >{{ record.executorName }}
                  {{ formatTime(record.createdAt) }}</span
                >
                <p>
                  执行时用例：{{ record.caseSnapshot.caseCode }}
                  {{ record.caseSnapshot.name }}
                </p>
                <CaseRichText
                  :model-value="record.description"
                  readonly
                  label="执行描述"
                />
                <p v-for="step in record.stepResults" :key="step.index">
                  步骤 {{ step.index + 1 }}：{{
                    functionalResultLabels[step.result]
                  }}
                  {{ step.actual }}
                </p>
              </article>
              <a-pagination
                v-if="(detail?.total || 0) > 10"
                v-model:current="historyPage"
                :page-size="10"
                :total="detail?.total"
                @change="loadDetail"
              />
            </a-tab-pane>
          </a-tabs>
        </a-spin>
      </aside>
    </div>
    <a-modal
      :open="formOpen"
      :title="`执行 ${previewCount} 条功能用例`"
      width="min(680px,calc(100vw - 32px))"
      :footer="null"
      :closable="!saving && !uploading"
      :mask-closable="false"
      destroy-on-close
      @cancel="closeForm"
    >
      <a-alert
        type="info"
        show-icon
        message="按当前筛选和所选目录的完整范围回填，每个计划关联实例独立保存。"
      />
      <PlanCaseExecutionSubmit
        v-if="formOpen"
        v-model:result="result"
        v-model:description="description"
        :plan-id="plan.id"
        :disabled="saving || previewLoading"
        v-model:uploading="uploading"
        v-model:dialog-dirty="dialogDirty"
        :on-submit="submitRange"
        default-active
        @image-uploaded="(plan, media) => mediaDraft.track(plan, media.id)"
        @discard-images="mediaDraft.cleanup()"
      >
        <a-button :disabled="saving || uploading" @click="closeForm"
          >取消</a-button
        >
      </PlanCaseExecutionSubmit>
    </a-modal>
    <a-modal
      :open="stepOpen"
      title="执行结果"
      width="min(800px,100vw)"
      :footer="null"
      :closable="!saving && !uploading"
      :mask-closable="false"
      destroy-on-close
      @cancel="closeSteps"
    >
      <a-alert
        v-if="!detail?.canExecute"
        type="info"
        message="当前用例仅可查看"
      />
      <div
        v-for="(step, index) in stepOpen ? detail?.entry?.steps || [] : []"
        :key="index"
        class="execution-step"
      >
        <h4>步骤 {{ index + 1 }}</h4>
        <CaseRichText :model-value="step.action" readonly label="步骤描述" />
        <CaseRichText :model-value="step.expected" readonly label="预期结果" />
        <a-select
          v-model:value="steps[index].result"
          :disabled="saving || !detail?.canExecute"
          :options="[
            { value: 'pending', label: '未执行' },
            ...functionalResults,
          ]"
          style="width: 150px"
          :aria-label="`步骤 ${index + 1} 执行结果`"
          @change="deriveResult"
        />
        <a-textarea
          v-model:value="steps[index].actual"
          :disabled="saving || !detail?.canExecute"
          :maxlength="10000"
          :placeholder="`步骤 ${index + 1} 实际结果`"
        />
      </div>
      <PlanCaseExecutionSubmit
        v-if="detail?.canExecute"
        v-model:result="result"
        v-model:description="description"
        :plan-id="plan.id"
        :disabled="saving"
        v-model:uploading="uploading"
        v-model:dialog-dirty="dialogDirty"
        :on-submit="submitSteps"
        default-active
        @image-uploaded="(plan, media) => mediaDraft.track(plan, media.id)"
        @discard-images="mediaDraft.cleanup()"
      />
    </a-modal>
  </section>
</template>
<script setup lang="ts">
import {
  computed,
  ref,
  shallowRef,
  watch,
  onBeforeUnmount,
  nextTick,
} from "vue";
import { onBeforeRouteLeave, onBeforeRouteUpdate } from "vue-router";
import { useFullscreen, useElementSize, useScroll } from "@vueuse/core";
import { message, Modal } from "ant-design-vue";
import dayjs from "dayjs";
import type { TestPlan } from "@/types";
import {
  planCaseWorkspaceApi,
  functionalMinderApi,
  type PlanCaseListing,
  type PlanCaseEntry,
  type PlanCaseExecutionDetail,
  type PlanCaseExecutionRecord,
  type FunctionalMinderSelection,
  type CaseFolder,
} from "@/api/planCaseWorkspace";
import { planCaseMediaApi } from "@/api/planCaseMedia";
import CaseRichText from "@/components/TestCase/CaseRichText.vue";
import CaseAttachments from "@/components/TestCase/CaseAttachments.vue";
import FunctionalMinderOperations from "./FunctionalMinderOperations.vue";
import {
  functionalMinderScope,
  prepareFunctionalMinderPreview,
  functionalExecutionDraftChanged,
} from "./functionalMinderScope";
import { useMinderMarquee } from "./useMinderMarquee";
import PlanDefects from "./PlanDefects.vue";
import PlanCaseExecutionSubmit from "./PlanCaseExecutionSubmit.vue";
import FunctionalMinderBranch from "./FunctionalMinderBranch.vue";
import PlanningMinderNavigator from "./PlanningMinderNavigator.vue";
import {
  buildFunctionalMinder,
  functionalFolderPath,
  functionalCameraScroll,
  flattenFunctionalMinder,
  type FunctionalMinderNode,
  type FunctionalMinderPage,
} from "./functionalMinder";
import {
  functionalResults,
  functionalResultLabels,
} from "./functionalExecution";
import { useMinderLayout } from "./useMinderLayout";
import { useMinderPan } from "./useMinderPan";
import { minderModes, type MinderMode } from "./planMinderView";
import { ExecutionMediaDraft } from "./executionMediaDraft";
const props = defineProps<{
  plan: TestPlan;
  listing: PlanCaseListing;
  treeType: "COLLECTION" | "MODULE";
  folder: string;
  condition: FunctionalMinderSelection["condition"];
  canEdit: boolean;
}>();
const emit = defineEmits<{
  changed: [];
  open: [row: PlanCaseEntry];
  navigate: [folder: string];
}>();
const host = ref<HTMLElement>(),
  stage = ref<HTMLElement>(),
  viewport = ref<HTMLElement>();
const { isFullscreen, toggle } = useFullscreen(host);
const mode = ref<MinderMode>("right"),
  hand = ref(false),
  preview = ref(false),
  zoom = ref(1);
const { width: viewportWidth, height: viewportHeight } =
  useElementSize(viewport);
const { x: scrollLeft, y: scrollTop } = useScroll(viewport);
const visibleBox = computed(() => ({
  x: (scrollLeft.value - 40) / zoom.value,
  y: (scrollTop.value - 40) / zoom.value,
  width: viewportWidth.value / zoom.value,
  height: viewportHeight.value / zoom.value,
}));
const executionShortcuts: [string, string][] = [
  ["通过", "S"],
  ["失败", "E"],
  ["阻塞", "B"],
  ["多选节点", "Ctrl / Command + 单击"],
  ["框选", "空白区域拖动"],
];
useMinderPan(viewport, hand);
const pages = shallowRef(new Map<string, FunctionalMinderPage>()),
  histories = shallowRef(new Map<string, PlanCaseExecutionRecord>()),
  collapsed = shallowRef<ReadonlySet<string>>(new Set()),
  selected = shallowRef<ReadonlySet<string>>(new Set());
const loading = ref(false),
  error = ref(""),
  detailLoading = ref(false),
  detailFailed = ref(false),
  detail = ref<PlanCaseExecutionDetail>(),
  historyPage = ref(1),
  sideTab = ref("history");
const formOpen = ref(false),
  stepOpen = ref(false),
  scope = ref<FunctionalMinderSelection>(),
  previewCount = ref(0),
  previewLoading = ref(false),
  result = ref("passed"),
  description = ref(""),
  saving = ref(false),
  uploading = ref(false),
  dialogDirty = ref(false),
  steps = ref<{ index: number; result: string; actual: string }[]>([]);
const mediaDraft = new ExecutionMediaDraft(planCaseMediaApi.cleanup);
let contextSequence = 0,
  detailSequence = 0,
  operationSequence = 0,
  previewSequence = 0,
  pendingRequest: { body: string; id: string } | undefined,
  disposed = false;
const folders = computed(() => {
  const values: CaseFolder[] = [
    ...(props.treeType === "COLLECTION"
      ? props.listing.collections
      : props.listing.modules),
  ];
  const id = props.treeType === "COLLECTION" ? "default" : "unassigned";
  if (!values.some((folder) => folder.nodeType === "PROJECT"))
    values.push({
      id,
      name: props.treeType === "COLLECTION" ? "默认测试集" : "未分配模块",
      count: props.listing.counts[id],
    });
  return values;
});
const folderPath = computed(() =>
  functionalFolderPath(folders.value, props.folder),
);
const text = (value: string) =>
  new DOMParser().parseFromString(value, "text/html").body.textContent || "";
const tree = computed(() => {
  const root = buildFunctionalMinder(
    folders.value,
    pages.value,
    props.folder,
    props.folder === "all"
      ? "功能用例"
      : folders.value.find((f) => f.id === props.folder)?.name || "功能用例",
    text,
    histories.value,
  );
  root.count = props.listing.total;
  return root;
});
const {
  geometry,
  failed: layoutFailed,
  refresh: refreshLayout,
} = useMinderLayout(stage, tree, collapsed, mode, ref<string>());
const rows = computed(
  () =>
    new Map(
      [...pages.value.values()].flatMap((page) =>
        page.items.map((row) => [row.id, row] as const),
      ),
    ),
);
const selectedRow = computed(() =>
  selected.value.size === 1
    ? rows.value.get(
        [...selected.value][0].split(
          /:(?:step|action|expected|actual|text|precondition|description):/,
        )[0],
      )
    : undefined,
);
let initialSteps = "[]",
  initialResult = "passed";
const dirty = computed(() =>
  functionalExecutionDraftChanged({
    description: description.value,
    dialogDirty: dialogDirty.value,
    steps: JSON.stringify(steps.value),
    initialSteps,
    result: result.value,
    initialResult,
  }),
);
const formatTime = (value: string) =>
  dayjs(value).format("YYYY-MM-DD HH:mm:ss");
function isRecycled(node: FunctionalMinderNode) {
  return node.entryId ? !!rows.value.get(node.entryId)?.recycled : false;
}
function resetView() {
  zoom.value = 1;
  if (viewport.value) {
    viewport.value.scrollLeft = 0;
    viewport.value.scrollTop = 0;
  }
}
function locatePoint(point: { x: number; y: number }) {
  viewport.value?.scrollTo({
    left: functionalCameraScroll(point.x, zoom.value, viewportWidth.value),
    top: functionalCameraScroll(point.y, zoom.value, viewportHeight.value),
  });
}
function locateRoot() {
  const root = geometry.value?.nodes["minder-root"];
  if (root)
    locatePoint({ x: root.x + root.width / 2, y: root.y + root.height / 2 });
}
async function changeZoom(value: number) {
  const next = Math.min(2, Math.max(0.5, value));
  const point = {
    x: (scrollLeft.value + viewportWidth.value / 2 - 40) / zoom.value,
    y: (scrollTop.value + viewportHeight.value / 2 - 40) / zoom.value,
  };
  zoom.value = next;
  await nextTick();
  locatePoint(point);
}
async function refreshSafely() {
  if (!(await confirmDiscard())) return;
  await clearDraft();
  await refresh();
}
function collapseAll() {
  collapsed.value = new Set(
    flattenFunctionalMinder(tree.value)
      .filter((n) => n.kind === "folder" || n.kind === "case")
      .map((n) => n.id),
  );
}
async function loadFolder(id: string, append = false) {
  const current = contextSequence,
    planId = props.plan.id,
    previous = pages.value.get(id),
    page = append ? (previous?.page || 0) + 1 : 1;
  loading.value = true;
  error.value = "";
  try {
    const data = await planCaseWorkspaceApi.list(planId, {
      ...props.condition,
      filters: props.condition?.filters
        ? JSON.stringify(props.condition.filters)
        : undefined,
      tree_type: props.treeType,
      category: "functional",
      folder: id,
      include_descendants: false,
      view: "minder-page",
      page,
      size: 100,
    });
    if (disposed || current !== contextSequence) return;
    pages.value = new Map(pages.value).set(id, {
      items: append ? [...(previous?.items || []), ...data.items] : data.items,
      total: data.total,
      page,
    });
    collapsed.value = new Set([
      ...collapsed.value,
      ...data.items
        .filter(
          (row) =>
            !rows.value.has(row.id) ||
            !previous?.items.some((item) => item.id === row.id),
        )
        .map((row) => row.id),
    ]);
    console.info("功能脑图目录分页已加载", {
      folder: id,
      page,
      count: data.items.length,
      total: data.total,
    });
  } catch (cause) {
    console.error("加载功能脑图目录失败", cause);
    if (current === contextSequence)
      error.value = "脑图目录加载失败，请刷新重试";
  } finally {
    if (current === contextSequence) loading.value = false;
  }
}
async function refresh() {
  for (const id of [...pages.value.keys()]) await loadFolder(id);
  if (selectedRow.value) await loadDetail();
  await refreshLayout();
}
async function toggleNode(node: FunctionalMinderNode) {
  if (collapsed.value.has(node.id)) {
    if (
      node.kind === "folder" &&
      !pages.value.has(node.folderId!) &&
      folders.value.find((folder) => folder.id === node.folderId)?.nodeType !==
        "PROJECT"
    )
      await loadFolder(node.folderId!);
    collapsed.value = new Set(
      [...collapsed.value].filter((id) => id !== node.id),
    );
  } else collapsed.value = new Set([...collapsed.value, node.id]);
}
const operations = ref<InstanceType<typeof FunctionalMinderOperations>>();
const defectPanel = ref<InstanceType<typeof PlanDefects>>();
const operationScope = computed(() =>
  functionalMinderScope(
    flattenFunctionalMinder(tree.value).filter((node) =>
      selected.value.has(node.id),
    ),
    props.condition,
    props.treeType,
    props.folder,
  ),
);
async function prepareOperation() {
  if (!(await confirmExecutionDiscard())) return false;
  await clearDraft();
  return true;
}
async function operationsChanged() {
  selected.value = new Set();
  detail.value = undefined;
  await refresh();
  emit("changed");
}
const { start: startMarquee, style: marqueeStyle } = useMinderMarquee(
  viewport,
  () =>
    !hand.value &&
    !dirty.value &&
    !saving.value &&
    !uploading.value &&
    !formOpen.value &&
    !stepOpen.value &&
    !operations.value?.isOpen,
  (ids) => {
    selected.value = new Set(
      flattenFunctionalMinder(tree.value)
        .filter(
          (node) =>
            ids.includes(node.id) &&
            ["root", "folder", "case"].includes(node.kind),
        )
        .map((node) => node.id),
    );
  },
);
async function confirmDiscard() {
  if (
    !((await operations.value?.beforeClose()) ?? true) ||
    !((await defectPanel.value?.beforeClose()) ?? true)
  )
    return false;
  return confirmExecutionDiscard();
}
async function confirmExecutionDiscard() {
  if (saving.value || uploading.value) {
    message.warning("请等待执行提交或图片上传完成");
    return false;
  }
  if (!dirty.value) return true;
  return new Promise<boolean>((resolve) =>
    Modal.confirm({
      title: "放弃未提交的执行结果？",
      content: "当前执行描述和步骤结果尚未提交。",
      okText: "放弃",
      cancelText: "继续编辑",
      onOk: () => resolve(true),
      onCancel: () => resolve(false),
    }),
  );
}
async function clearDraft(preservePreview = false) {
  if (!preservePreview) previewSequence++;
  operationSequence++;
  scope.value = undefined;
  previewLoading.value = false;
  formOpen.value = false;
  stepOpen.value = false;
  description.value = "";
  result.value = "passed";
  steps.value = [];
  initialSteps = "[]";
  initialResult = "passed";
  dialogDirty.value = false;
  pendingRequest = undefined;
  await mediaDraft.cleanup();
}
async function selectNode(node: FunctionalMinderNode, event: MouseEvent) {
  if (node.kind === "more") {
    await loadFolder(node.folderId!, true);
    return;
  }
  if (!(await confirmDiscard())) return;
  await clearDraft();
  const next = new Set(event.ctrlKey || event.metaKey ? selected.value : []);
  if (next.has(node.id)) next.delete(node.id);
  else next.add(node.id);
  selected.value = next;
  await nextTick();
  const surface = viewport.value;
  const label = surface?.querySelector<HTMLElement>(
    `.minder-branch[data-node-id="${CSS.escape(node.id)}"] > .branch-label`,
  );
  if (surface && label && next.size === 1) {
    const bounds = surface.getBoundingClientRect();
    const box =
      label.querySelector<HTMLElement>(".node-menu")?.getBoundingClientRect() ||
      label.getBoundingClientRect();
    if (box.right > bounds.right - 16)
      surface.scrollLeft += box.right - bounds.right + 16;
    if (box.left < bounds.left + 16)
      surface.scrollLeft -= bounds.left + 16 - box.left;
    if (box.bottom > bounds.bottom - 16)
      surface.scrollTop += box.bottom - bounds.bottom + 16;
  }
  if (next.size === 1 && node.entryId) {
    historyPage.value = 1;
    await loadDetail();
    if (
      !selected.value.has(node.id) ||
      selected.value.size !== 1 ||
      detail.value?.entry?.id !== node.entryId ||
      detailFailed.value ||
      detailLoading.value
    )
      return;
    if (node.stepIndex !== undefined && detail.value?.entry) {
      const current = detail.value.history.find(
        (record) => record.id === detail.value?.entry?.executionId,
      );
      const unchanged =
        JSON.stringify(
          current?.caseSnapshot.steps?.map((s) => ({
            action: s.action,
            expected: s.expected,
          })),
        ) ===
        JSON.stringify(
          detail.value.entry.steps.map((s) => ({
            action: s.action,
            expected: s.expected,
          })),
        );
      steps.value = detail.value.entry.steps.map((_, index) => ({
        index,
        result: unchanged
          ? current?.stepResults.find((s) => s.index === index)?.result ||
            "pending"
          : "pending",
        actual: unchanged
          ? current?.stepResults.find((s) => s.index === index)?.actual || ""
          : "",
      }));
      initialSteps = JSON.stringify(steps.value);
      result.value =
        detail.value.entry.result === "pending"
          ? "passed"
          : detail.value.entry.result;
      initialResult = result.value;
      stepOpen.value = true;
    }
  }
}
watch(
  () => selectedRow.value?.id,
  () => {
    detailSequence++;
    detail.value = undefined;
    detailFailed.value = false;
    detailLoading.value = false;
  },
  { flush: "sync" },
);
async function loadDetail() {
  const row = selectedRow.value;
  if (!row) return;
  const current = ++detailSequence;
  detailLoading.value = true;
  detailFailed.value = false;
  try {
    const response = await planCaseWorkspaceApi.execution(props.plan.id, {
      source: row.source,
      associationId: row.associationId,
      caseId: row.caseId,
      page: historyPage.value,
      size: 10,
    });
    if (disposed || current !== detailSequence) return;
    detail.value = response;
    const latest = response.history.find(
      (record) => record.id === response.entry?.executionId,
    );
    if (latest) histories.value = new Map(histories.value).set(row.id, latest);
  } catch (cause) {
    console.error("加载脑图执行详情失败", cause);
    if (current === detailSequence) detailFailed.value = true;
  } finally {
    if (current === detailSequence) detailLoading.value = false;
  }
}
function scopeFor(node: FunctionalMinderNode): FunctionalMinderSelection {
  return functionalMinderScope(
    [node],
    props.condition,
    props.treeType,
    props.folder,
  )!;
}
async function openForm(node: FunctionalMinderNode) {
  await openSelection(scopeFor(node));
}
async function openSelection(selection = operationScope.value) {
  if (!selection || previewLoading.value || saving.value || uploading.value)
    return;
  const intent = ++previewSequence;
  const context = contextSequence;
  const planId = props.plan.id;
  const isCurrent = () =>
    !disposed &&
    intent === previewSequence &&
    context === contextSequence &&
    planId === props.plan.id;
  previewLoading.value = true;
  try {
    const prepared = await prepareFunctionalMinderPreview(selection, planId, {
      isCurrent,
      confirm: confirmDiscard,
      cleanup: () => clearDraft(true),
      preview: (id, frozen) => {
        previewLoading.value = true;
        return functionalMinderApi.preview(id, frozen);
      },
    });
    if (!prepared || !isCurrent()) return;
    previewCount.value = prepared.preview.count;
    if (!prepared.preview.canExecute) {
      message.warning("当前范围没有可执行的功能用例或计划正在执行");
      return;
    }
    scope.value = prepared.selection;
    formOpen.value = true;
  } catch (cause) {
    console.error("预览脑图执行范围失败", cause);
    if (isCurrent()) message.error("执行范围加载失败，请重试");
  } finally {
    if (isCurrent()) previewLoading.value = false;
  }
}
function requestId(body: unknown) {
  const encoded = JSON.stringify(body);
  if (!pendingRequest || pendingRequest.body !== encoded)
    pendingRequest = { body: encoded, id: crypto.randomUUID() };
  return pendingRequest.id;
}
async function saved() {
  await clearDraft();
  await refresh();
  emit("changed");
  message.success("执行结果已回填");
}
async function submitRange() {
  if (!scope.value || saving.value || uploading.value) return false;
  const body = {
    ...scope.value,
    result: result.value,
    description: description.value,
  };
  saving.value = true;
  try {
    await functionalMinderApi.execute(props.plan.id, {
      ...body,
      requestId: requestId(body),
    });
    await saved();
    return true;
  } catch (cause) {
    console.error("提交脑图范围执行失败，保留结果供重试", cause);
    message.error("执行回填失败，已保留输入，请重试");
    return false;
  } finally {
    saving.value = false;
  }
}
function deriveResult() {
  result.value = steps.value.some((s) => s.result === "failed")
    ? "failed"
    : steps.value.some((s) => s.result === "blocked")
      ? "blocked"
      : steps.value.every((s) => s.result === "passed")
        ? "passed"
        : "pending";
}
async function submitSteps() {
  const row = detail.value?.entry;
  if (!row || saving.value || uploading.value) return false;
  const body = {
    selections: [{ source: row.source, id: row.associationId }],
    result: result.value,
    description: description.value,
    stepResults: steps.value,
  };
  saving.value = true;
  try {
    await planCaseWorkspaceApi.execute(props.plan.id, {
      ...body,
      requestId: requestId(body),
    });
    await saved();
    return true;
  } catch (cause) {
    console.error("提交脑图步骤执行失败，保留结果供重试", cause);
    message.error("步骤回填失败，已保留输入，请重试");
    return false;
  } finally {
    saving.value = false;
  }
}
async function closeForm() {
  if (await confirmDiscard()) await clearDraft();
}
async function closeSteps() {
  if (await confirmDiscard()) await clearDraft();
}
async function emitOpen(node: FunctionalMinderNode) {
  if (!(await confirmDiscard())) return;
  await clearDraft();
  const row = rows.value.get(node.entryId || "");
  if (row) emit("open", row);
}
function shortcut(event: KeyboardEvent) {
  if (
    event.ctrlKey ||
    event.metaKey ||
    event.altKey ||
    event.shiftKey ||
    event.repeat ||
    (event.target as HTMLElement)?.closest(
      "input,textarea,select,[contenteditable=true],.ant-select",
    ) ||
    operations.value?.isOpen ||
    formOpen.value ||
    stepOpen.value ||
    saving.value ||
    uploading.value ||
    selected.value.size !== 1
  )
    return;
  const node = flattenFunctionalMinder(tree.value).find(
    (n) => n.id === [...selected.value][0],
  );
  const value = (
    { s: "passed", e: "failed", b: "blocked" } as Record<string, string>
  )[event.key.toLowerCase()];
  if (
    !value ||
    node?.kind !== "case" ||
    !props.listing.canExecute ||
    isRecycled(node)
  )
    return;
  event.preventDefault();
  scope.value = scopeFor(node);
  result.value = value;
  description.value = "";
  void submitRange();
}
const context = computed(() =>
  JSON.stringify({
    plan: props.plan.id,
    tree: props.treeType,
    folder: props.folder,
    condition: props.condition,
  }),
);
watch(
  context,
  async () => {
    contextSequence++;
    detailSequence++;
    operationSequence++;
    pages.value = new Map();
    histories.value = new Map();
    selected.value = new Set();
    detail.value = undefined;
    error.value = "";
    collapsed.value = new Set(folders.value.map((f) => `folder:${f.id}`));
    await clearDraft();
    if (props.folder !== "all") await loadFolder(props.folder);
    else {
      const id = props.treeType === "COLLECTION" ? "default" : "unassigned";
      if (folders.value.some((folder) => folder.id === id))
        await loadFolder(id);
      collapsed.value = new Set(
        [...collapsed.value].filter((n) => n !== `folder:${id}`),
      );
    }
    await nextTick();
    resetView();
  },
  { immediate: true },
);
async function clearSelection() {
  if (!(await confirmDiscard())) return;
  await clearDraft();
  selected.value = new Set();
}
async function closeSidebar() {
  if (await confirmDiscard()) {
    await clearDraft();
    selected.value = new Set();
  }
}
async function beforeClose() {
  if (!(await confirmDiscard())) return false;
  await clearDraft();
  return true;
}
defineExpose({ beforeClose, refresh });
onBeforeRouteLeave(confirmDiscard);
onBeforeRouteUpdate(async () => await confirmDiscard());
onBeforeUnmount(() => {
  disposed = true;
  contextSequence++;
  detailSequence++;
  operationSequence++;
  void mediaDraft.cleanup();
});
</script>
<style scoped>
.functional-minder {
  background: #fff;
  border: 1px solid #e5e6eb;
  min-width: 0;
}
.functional-minder:fullscreen {
  height: 100vh;
  padding: 12px;
  overflow: auto;
}
.minder-toolbar {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  padding: 10px;
  flex-wrap: wrap;
  border-bottom: 1px solid #e5e6eb;
}
.shortcut-hint {
  font-size: 12px;
  color: #86909c;
}
.minder-layout {
  display: flex;
  min-width: 0;
  height: 650px;
}
.canvas-host {
  position: relative;
  flex: 1;
  min-width: 0;
  height: 100%;
}
.canvas-host :deep(.ant-spin-container),
.canvas-host :deep(.ant-spin-nested-loading) {
  height: 100%;
}
.minder-viewport {
  height: 100%;
  overflow: auto;
  background: #f7f8fa;
}
.minder-sizing {
  position: relative;
}
.minder-stage {
  position: absolute;
  left: 40px;
  top: 40px;
  transform-origin: 0 0;
}
.minder-connections {
  position: absolute;
  pointer-events: none;
}
.minder-connections path {
  stroke: #c9cdd4;
  fill: none;
  stroke-width: 1.5;
}
.node-menu {
  position: absolute;
  left: 0;
  top: 100%;
  display: flex;
  gap: 4px;
  background: #fff;
  padding: 4px;
  border: 1px solid #e5e6eb;
  z-index: 5;
  transform: translateY(4px);
}
.execute-popup {
  width: min(416px, calc(100vw - 56px));
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.minder-sidebar {
  width: 400px;
  flex-shrink: 0;
  max-width: 45%;
  padding: 12px;
  border-left: 1px solid #e5e6eb;
  overflow: auto;
  overflow-wrap: anywhere;
}
.history-record {
  border-bottom: 1px solid #e5e6eb;
  padding: 12px 0;
}
.execution-step {
  padding: 12px 0;
  border-bottom: 1px solid #e5e6eb;
}
.execution-step .ant-input {
  margin: 8px 0;
}
@media (max-width: 768px) {
  .minder-layout {
    height: 600px;
    flex-direction: column;
  }
  .minder-sidebar {
    width: 100%;
    max-width: 100%;
    height: 260px;
    flex-shrink: 0;
    border-left: 0;
    border-top: 1px solid #e5e6eb;
  }
  .minder-viewport {
    min-height: 300px;
  }
  .shortcut-hint {
    display: none;
  }
}
.minder-marquee {
  position: absolute;
  pointer-events: none;
  z-index: 20;
  border: 1px solid #811fa3;
  background: #811fa318;
}
.multi-selection {
  margin: 8px;
  display: flex;
  flex-wrap: wrap;
}
.minder-breadcrumb {
  padding: 4px 8px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
}
.minder-breadcrumb :deep(.ant-btn) {
  max-width: 240px;
  white-space: normal;
  height: auto;
}
</style>
