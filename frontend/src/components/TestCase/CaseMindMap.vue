<template>
  <section
    class="case-mind-map"
    tabindex="0"
    aria-label="测试用例脑图"
    @keydown="keyboard"
  >
    <a-space wrap class="mind-toolbar">
      <a-tag>模块 → 用例 → 前置条件 / 步骤 / TEXT 描述及预期</a-tag>
      <a-button @click="fit">重置视图</a-button>
      <template v-if="!readonly">
        <a-button :disabled="busy" @click="createCase">新增用例</a-button>
        <a-button :disabled="busy" @click="newModule(false)"
          >新增同级模块</a-button
        >
        <a-button :disabled="busy" @click="newModule(true)"
          >新增子模块</a-button
        >
        <a-button
          :disabled="
            busy || !selectedCase || selectedCase.caseEditType === 'TEXT'
          "
          @click="addStep"
          >添加步骤</a-button
        >
        <a-button :disabled="!selectedCase" @click="copy">复制内容</a-button>
        <a-button
          :disabled="busy || (!selectedCase && !selected?.moduleId)"
          @click="cut"
          >剪切节点</a-button
        >
        <a-button :disabled="busy || !clipboard" @click="paste">{{
          clipboard?.kind === "copy" ? "粘贴为新用例" : "粘贴到此模块"
        }}</a-button>
        <a-button
          :disabled="busy || (!selectedCase && !selected?.moduleId)"
          danger
          @click="deleteNode"
          >删除节点</a-button
        >
      </template>
      <span class="mind-hint"
        >滚轮缩放 · 拖动平移 · 点击节点查看{{
          readonly ? "" : " / 编辑（Ctrl/Cmd+C、X、V，Delete）"
        }}</span
      >
    </a-space>
    <v-chart
      ref="chart"
      class="mind-chart"
      :option="option"
      autoresize
      @click="selectNode"
    />
    <a-card
      v-if="selected"
      class="mind-editor"
      :title="selected.kind === 'module' ? '模块' : '选中节点'"
      size="small"
    >
      <template #extra
        ><a-button type="text" :disabled="busy" @click="closeEditor"
          >关闭</a-button
        ></template
      >
      <p class="node-title">{{ selected.name }}</p>
      <template v-if="selectedCase">
        <a-space wrap style="margin-bottom: 12px"
          ><a-button :disabled="busy" @click="openDetail">查看用例详情</a-button
          ><a-tag v-if="readonly">{{ selectedCase.priority }}</a-tag
          ><a-select
            v-else
            :value="selectedCase.priority || 'P2'"
            :disabled="busy"
            aria-label="用例优先级"
            style="width: 85px"
            @change="savePriority"
            ><a-select-option
              v-for="level in ['P0', 'P1', 'P2', 'P3']"
              :key="level"
              :value="level"
              >{{ level }}</a-select-option
            ></a-select
          ></a-space
        >
        <template v-if="!readonly">
          <a-form layout="vertical">
            <a-form-item :label="fieldLabel"
              ><CaseRichText
                v-if="isTextNode"
                v-model="editText"
                :disabled="busy"
                :label="fieldLabel" />
              <a-textarea
                v-else
                v-model:value="editText"
                :disabled="busy"
                :rows="3"
                :maxlength="selected.kind === 'case' ? 200 : 10000"
            /></a-form-item>
            <a-space
              ><a-button type="primary" :loading="busy" @click="save"
                >保存节点</a-button
              ><a-popconfirm
                v-if="selected.stepIndex !== undefined"
                title="删除这个步骤及对应预期？"
                @confirm="removeStep"
                ><a-button danger :disabled="busy"
                  >删除步骤</a-button
                ></a-popconfirm
              ></a-space
            >
          </a-form>
        </template>
        <CaseRichText
          v-else-if="isTextNode"
          :model-value="editText"
          readonly
          :label="fieldLabel"
        />
        <p v-else class="node-content">{{ editText }}</p>
      </template>
      <template v-else-if="selected.kind === 'module' && !readonly">
        <a-space direction="vertical" style="width: 100%"
          ><a-input
            v-model:value="editText"
            :disabled="busy"
            placeholder="模块名称"
            :maxlength="100"
          /><a-button
            v-if="selected.moduleId"
            :loading="busy"
            @click="saveModule"
            >保存模块名</a-button
          ><a-button :disabled="busy" @click="createCase"
            >在此模块新建用例</a-button
          ></a-space
        >
      </template>
    </a-card>
    <a-modal
      :open="moduleDraft !== undefined"
      title="新增模块"
      :confirm-loading="busy"
      :closable="!busy"
      :mask-closable="false"
      :keyboard="!busy"
      @ok="saveNewModule"
      @cancel="cancelNewModule"
    >
      <a-input
        v-model:value="moduleName"
        :disabled="busy"
        :maxlength="100"
        aria-label="新增模块名称"
        placeholder="请输入模块名称"
      />
    </a-modal>
  </section>
</template>
<script setup lang="ts">
import { computed, ref, reactive, watch, onBeforeUnmount } from "vue";
import { use } from "echarts/core";
import { TreeChart } from "echarts/charts";
import { TooltipComponent } from "echarts/components";
import { CanvasRenderer } from "echarts/renderers";
import VChart from "vue-echarts";
import { message, Modal } from "ant-design-vue";
import CaseRichText from "./CaseRichText.vue";
import type { TestCase } from "@/types";
import {
  buildCaseMindMap,
  copyCaseDraft,
  mindNodeValue,
  mindNodePatch,
  type MindModule,
  type CaseMindNode,
} from "./caseMindMap";
use([TreeChart, TooltipComponent, CanvasRenderer]);
const props = withDefaults(
  defineProps<{
    cases: Partial<TestCase>[];
    modules?: MindModule[];
    readonly?: boolean;
    saving?: boolean;
    selectedCaseId?: string;
    scopeKey?: string;
    persistEdit?: (
      id: string,
      patch: Partial<TestCase>,
    ) => Promise<boolean | Partial<TestCase>>;
    persistRename?: (id: string, name: string) => Promise<boolean>;
    persistCreate?: (
      moduleId: string | undefined,
      draft: Partial<TestCase>,
    ) => Promise<boolean>;
    persistCreateModule?: (
      parentId: string | null,
      name: string,
    ) => Promise<boolean>;
    persistMove?: (
      kind: "case" | "module",
      id: string,
      parentId: string | null,
    ) => Promise<boolean>;
    persistDelete?: (kind: "case" | "module", id: string) => Promise<boolean>;
  }>(),
  { modules: () => [], readonly: false, saving: false },
);
const emit = defineEmits<{
  select: [testCase: Partial<TestCase>];
  edit: [caseId: string, patch: Partial<TestCase>];
  create: [moduleId?: string, draft?: Partial<TestCase>];
  renameModule: [moduleId: string, name: string];
}>();
const chart = ref<InstanceType<typeof VChart>>();
const selected = ref<CaseMindNode>();
const editText = ref("");
const clipboard = ref<
  | { kind: "copy"; draft: Partial<TestCase> }
  | { kind: "case" | "module"; id: string }
>();
const moduleDraft = ref<{ parentId: string | null }>();
const moduleName = ref("");
const selectedSource = ref<Partial<TestCase>>();
const acknowledgedCases = reactive(new Map<string, Partial<TestCase>>());
function sourceCase(id?: string) {
  const current = props.cases.find((c) => c.id === id),
    saved = id ? acknowledgedCases.get(id) : undefined;
  if (
    saved?.updatedAt &&
    current?.updatedAt &&
    Date.parse(current.updatedAt) > Date.parse(saved.updatedAt)
  )
    return current;
  return saved || current;
}
function acknowledgeCase(
  c: Partial<TestCase>,
  patch: Partial<TestCase>,
  result?: boolean | Partial<TestCase>,
) {
  const updated = {
    ...c,
    ...patch,
    ...(typeof result === "object" ? result : {}),
  };
  if (c.id) acknowledgedCases.set(c.id, updated);
  selectedSource.value = updated;
}
const savedText = ref("");
const working = ref(false);
const confirming = ref(false);
let generation = 0;
let disposed = false;
const busy = computed(() => working.value || confirming.value || props.saving);
const dirty = computed(
  () =>
    !props.readonly &&
    (editText.value !== savedText.value || moduleDraft.value !== undefined),
);
const selectedCase = computed(() =>
  props.readonly
    ? props.cases.find((c) => c.id === selected.value?.caseId)
    : sourceCase(selected.value?.caseId) || selectedSource.value,
);
const isTextNode = computed(() =>
  ["textDescription", "expectedResult"].includes(selected.value?.kind || ""),
);
const fieldLabel = computed(
  () =>
    ({
      case: "用例名称",
      precondition: "前置条件",
      action: "操作步骤",
      expected: "预期结果",
      textDescription: "TEXT 描述",
      expectedResult: "TEXT 预期结果",
      step: "操作步骤",
      module: "模块名称",
      root: "名称",
    })[selected.value?.kind || "root"],
);
const option = computed(() => ({
  tooltip: {
    trigger: "item",
    renderMode: "richText",
    formatter: (p: any) => p.data.name,
  },
  series: [
    {
      type: "tree",
      data: [buildCaseMindMap(props.cases, props.modules)],
      top: 35,
      left: 150,
      bottom: 35,
      right: 190,
      orient: "LR",
      roam: true,
      expandAndCollapse: false,
      initialTreeDepth: -1,
      symbolSize: 9,
      label: {
        position: "left",
        align: "right",
        fontSize: 12,
        width: 120,
        overflow: "truncate",
        backgroundColor: "#f4f7fb",
        padding: [5, 8],
        borderRadius: 4,
      },
      lineStyle: { curveness: 0.5, color: "#c3d2e7" },
      leaves: { label: { position: "right", align: "left", width: 160 } },
      emphasis: { focus: "descendant" },
      animationDuration: 180,
    },
  ],
}));
async function beforeClose(): Promise<boolean> {
  if (busy.value) return false;
  if (!dirty.value) return true;
  const requestGeneration = generation;
  confirming.value = true;
  return new Promise((resolve) =>
    Modal.confirm({
      title: "放弃未保存的节点内容？",
      content: "取消会保留当前编辑，保存后可以切换节点或离开脑图。",
      onCancel: () => {
        if (requestGeneration === generation) confirming.value = false;
        resolve(false);
      },
      onOk: () => {
        if (requestGeneration === generation) confirming.value = false;
        if (requestGeneration !== generation || busy.value || disposed) {
          resolve(false);
          return;
        }
        editText.value = savedText.value;
        moduleDraft.value = undefined;
        moduleName.value = "";
        resolve(true);
      },
    }),
  );
}
async function selectNode(event: any) {
  const requestGeneration = generation;
  if (!(await beforeClose())) return;
  if (requestGeneration !== generation || disposed || busy.value) return;
  selected.value = event.data;
  const c = sourceCase(event.data.caseId);
  selectedSource.value = c ? JSON.parse(JSON.stringify(c)) : undefined;
  editText.value = savedText.value = mindNodeValue(event.data, c);
  if (c && props.readonly) emit("select", c);
}
async function operation(
  action: () => Promise<boolean | Partial<TestCase>>,
  acknowledged?: (result: boolean | Partial<TestCase>) => void,
) {
  if (busy.value || props.readonly) return false;
  const requestGeneration = generation;
  working.value = true;
  try {
    const ok = await action();
    if (disposed || requestGeneration !== generation) return false;
    if (ok) acknowledged?.(ok);
    return Boolean(ok);
  } catch {
    if (!disposed && requestGeneration === generation)
      message.error("操作失败，编辑内容已保留");
    return false;
  } finally {
    if (!disposed && requestGeneration === generation) working.value = false;
  }
}
async function save() {
  const c = selectedCase.value;
  const n = selected.value;
  if (!c?.id || !n) return;
  const submitted = editText.value;
  const patch = mindNodePatch(n, c, submitted);
  if (!patch)
    return message.warning("节点已变化或用例名称为空，请重新选择节点");
  if (!props.persistEdit) {
    emit("edit", c.id, patch);
    return;
  }
  await operation(
    () => props.persistEdit!(c.id!, patch),
    (result) => {
      acknowledgeCase(c, patch, result);
      const persisted = sourceCase(c.id) || selectedSource.value;
      savedText.value = mindNodeValue(n, persisted);
      if (editText.value === submitted) editText.value = savedText.value;
    },
  );
}
async function saveModule() {
  const id = selected.value?.moduleId,
    submitted = editText.value.trim();
  if (!id || !submitted) return;
  if (!props.persistRename) {
    emit("renameModule", id, submitted);
    return;
  }
  await operation(
    () => props.persistRename!(id, submitted),
    () => {
      savedText.value = submitted;
      editText.value = submitted;
    },
  );
}
async function savePriority(value: string) {
  const c = selectedCase.value;
  if (!c?.id || !["P0", "P1", "P2", "P3"].includes(value) || !props.persistEdit)
    return;
  const patch = { priority: value as TestCase["priority"] };
  await operation(
    () => props.persistEdit!(c.id!, patch),
    (result) => acknowledgeCase(c, patch, result),
  );
}
async function addStep() {
  const requestGeneration = generation;
  if (!(await beforeClose())) return;
  if (requestGeneration !== generation || disposed) return;
  const c = selectedCase.value;
  if (c?.id && c.caseEditType !== "TEXT") {
    const patch = {
      steps: [
        ...(c.steps || []),
        { step: (c.steps || []).length + 1, action: "新步骤", expected: "" },
      ],
    };
    if (props.persistEdit)
      await operation(
        () => props.persistEdit!(c.id!, patch),
        (result) => acknowledgeCase(c, patch, result),
      );
    else emit("edit", c.id, patch);
  }
}
async function removeStep() {
  const requestGeneration = generation;
  if (!(await beforeClose())) return;
  if (requestGeneration !== generation || disposed) return;
  const c = selectedCase.value;
  if (
    c?.id &&
    selected.value?.stepIndex !== undefined &&
    c.caseEditType !== "TEXT"
  ) {
    const patch = {
      steps: (c.steps || [])
        .filter((_, i) => i !== selected.value?.stepIndex)
        .map((s, i) => ({ ...s, step: i + 1 })),
    };
    if (props.persistEdit)
      await operation(
        () => props.persistEdit!(c.id!, patch),
        (result) => {
          selected.value = undefined;
          selectedSource.value = undefined;
          editText.value = savedText.value = "";
          if (c.id)
            acknowledgedCases.set(c.id, {
              ...c,
              ...patch,
              ...(typeof result === "object" ? result : {}),
            });
        },
      );
    else emit("edit", c.id, patch);
  }
}
function copy() {
  if (busy.value) return;
  if (selectedCase.value) {
    clipboard.value = {
      kind: "copy",
      draft: copyCaseDraft(selectedCase.value),
    };
    message.info("已复制用例内容，可粘贴为新用例");
  }
}
async function paste() {
  const requestGeneration = generation;
  if (!(await beforeClose())) return;
  if (requestGeneration !== generation || disposed) return;
  if (clipboard.value) {
    const source = clipboard.value;
    const moduleId =
      selected.value?.moduleId || selectedCase.value?.moduleId || undefined;
    if (source.kind !== "copy") {
      const exists =
        source.kind === "module"
          ? props.modules.some((m) => m.id === source.id)
          : props.cases.some((c) => c.id === source.id);
      if (!exists)
        return message.warning("原节点不在当前范围中，请重新选择并剪切");
      if (source.kind === "module" && source.id === moduleId)
        return message.warning("模块不能移动到自身内");
      if (props.persistMove)
        await operation(
          () => props.persistMove!(source.kind, source.id, moduleId || null),
          () => {
            clipboard.value = undefined;
            selected.value = undefined;
            selectedSource.value = undefined;
            editText.value = savedText.value = "";
          },
        );
      return;
    }
    const draft = {
      ...JSON.parse(JSON.stringify(source.draft)),
      moduleId,
    };
    if (props.persistCreate)
      await operation(() => props.persistCreate!(moduleId, draft));
    else emit("create", moduleId, draft);
  }
}
async function cut() {
  const requestGeneration = generation;
  if (!(await beforeClose()) || requestGeneration !== generation) return;
  const c = selectedCase.value,
    m = selected.value?.moduleId;
  if (c?.id) clipboard.value = { kind: "case", id: c.id };
  else if (m) clipboard.value = { kind: "module", id: m };
  if (clipboard.value) message.info("已剪切，选择目标模块后粘贴将移动原节点");
}
async function newModule(child: boolean) {
  const requestGeneration = generation;
  if (!(await beforeClose()) || requestGeneration !== generation) return;
  const id = selected.value?.moduleId || selectedCase.value?.moduleId;
  const module = props.modules.find((m) => m.id === id);
  moduleDraft.value = {
    parentId: child
      ? id || null
      : module?.parentId || module?.parent_id || null,
  };
  moduleName.value = "";
}
async function saveNewModule() {
  if (
    !moduleDraft.value ||
    !moduleName.value.trim() ||
    !props.persistCreateModule
  )
    return;
  const name = moduleName.value.trim(),
    parent = moduleDraft.value.parentId;
  await operation(
    () => props.persistCreateModule!(parent, name),
    () => {
      moduleDraft.value = undefined;
      moduleName.value = "";
    },
  );
}
async function cancelNewModule() {
  if (await beforeClose()) {
    moduleDraft.value = undefined;
    moduleName.value = "";
  }
}
async function deleteNode() {
  const requestGeneration = generation;
  if (!(await beforeClose()) || requestGeneration !== generation) return;
  const c = selectedCase.value,
    id = c?.id || selected.value?.moduleId;
  if (!id || !props.persistDelete) return;
  const kind = c?.id ? "case" : "module";
  confirming.value = true;
  Modal.confirm({
    title: kind === "case" ? "将此用例移入回收站？" : "删除此模块？",
    content:
      kind === "case"
        ? "用例可以从回收站恢复。"
        : "此模块中的用例会保留并移到未规划，子模块会提升到上一级。",
    onCancel: () => {
      if (requestGeneration === generation) confirming.value = false;
    },
    onOk: async () => {
      if (requestGeneration === generation) confirming.value = false;
      if (requestGeneration !== generation || disposed || busy.value) return;
      await operation(
        () => props.persistDelete!(kind, id),
        () => {
          selected.value = undefined;
          selectedSource.value = undefined;
          editText.value = savedText.value = "";
        },
      );
    },
  });
}
async function createCase() {
  const requestGeneration = generation;
  if ((await beforeClose()) && requestGeneration === generation)
    emit(
      "create",
      selected.value?.moduleId || selectedCase.value?.moduleId || undefined,
    );
}
async function openDetail() {
  const requestGeneration = generation;
  if (
    selectedCase.value &&
    (await beforeClose()) &&
    requestGeneration === generation
  )
    emit("select", selectedCase.value);
}
async function closeEditor() {
  const requestGeneration = generation;
  if ((await beforeClose()) && requestGeneration === generation) {
    selected.value = undefined;
    selectedSource.value = undefined;
  }
}
function keyboard(event: KeyboardEvent) {
  if (
    props.readonly ||
    busy.value ||
    ["INPUT", "TEXTAREA", "SELECT"].includes(
      (event.target as HTMLElement).tagName,
    ) ||
    (event.target as HTMLElement).isContentEditable
  )
    return;
  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "c") {
    event.preventDefault();
    copy();
  }
  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "v") {
    event.preventDefault();
    paste();
  }
  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "x") {
    event.preventDefault();
    void cut();
  }
  if (event.key === "Delete") {
    event.preventDefault();
    void deleteNode();
  }
  if (event.key === "Enter") {
    event.preventDefault();
    void openDetail();
  }
  if (event.key === "Escape") {
    event.preventDefault();
    void closeEditor();
  }
}
function fit() {
  chart.value?.clear();
  chart.value?.setOption(option.value);
}
watch(
  () => props.cases,
  (rows, previous) => {
    const visible = new Set(rows.map((c) => c.id));
    for (const id of acknowledgedCases.keys())
      if (!visible.has(id) && id !== selected.value?.caseId)
        acknowledgedCases.delete(id);
    for (const row of rows)
      if (row.id && previous?.find((c) => c.id === row.id) !== row)
        acknowledgedCases.delete(row.id);
    const row = rows.find((c) => c.id === selected.value?.caseId);
    if (props.readonly && !row && selected.value?.caseId) {
      selected.value = undefined;
      selectedSource.value = undefined;
      editText.value = savedText.value = "";
      return;
    }
    if (!row || !selected.value || working.value || confirming.value) return;
    const hadDraft = dirty.value;
    selectedSource.value = JSON.parse(JSON.stringify(row));
    savedText.value = mindNodeValue(selected.value, row);
    if (!hadDraft) editText.value = savedText.value;
  },
);
watch(
  () => props.selectedCaseId,
  (id) => {
    if (id) {
      const c = props.cases.find((x) => x.id === id);
      if (c)
        selectNode({
          data: {
            id: `case:${id}`,
            name: c.name || "",
            kind: "case",
            caseId: id,
          },
        });
    }
  },
);
watch(
  () => props.scopeKey,
  () => {
    generation++;
    working.value = false;
    confirming.value = false;
    selected.value = undefined;
    selectedSource.value = undefined;
    acknowledgedCases.clear();
    clipboard.value = undefined;
    moduleDraft.value = undefined;
    moduleName.value = "";
    editText.value = savedText.value = "";
  },
  { flush: "sync" },
);
function beforeUnload(event: BeforeUnloadEvent) {
  if (dirty.value || busy.value) {
    event.preventDefault();
    event.returnValue = "";
  }
}
window.addEventListener("beforeunload", beforeUnload);
onBeforeUnmount(() => {
  disposed = true;
  generation++;
  window.removeEventListener("beforeunload", beforeUnload);
});
defineExpose({ beforeClose });
</script>
<style scoped>
.case-mind-map {
  position: relative;
  overflow: auto;
  background: #fff;
  border: 1px solid #e4e9f0;
  border-radius: 10px;
  outline: none;
}
.case-mind-map:focus {
  border-color: #91caff;
}
.mind-toolbar {
  padding: 12px;
  border-bottom: 1px solid #edf0f5;
}
.mind-chart {
  height: clamp(360px, calc(100vh - 360px), 650px);
  min-width: 800px;
  width: 100%;
}
.mind-hint {
  font-size: 12px;
  color: #667085;
}
.mind-editor {
  position: absolute;
  right: 14px;
  top: 100px;
  width: 320px;
  max-width: 90%;
  max-height: 520px;
  overflow: auto;
  box-shadow: 0 8px 24px #163c6418;
}
.node-title,
.node-content {
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}
.node-title {
  color: #667085;
  font-size: 12px;
}
@media (max-width: 700px) {
  .mind-chart {
    height: 500px;
  }
  .mind-editor {
    position: relative;
    inset: auto;
    width: auto;
    margin: 12px;
  }
}
</style>
