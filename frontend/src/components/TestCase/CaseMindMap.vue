<template>
  <section
    class="case-mind-map"
    tabindex="0"
    aria-label="测试用例脑图"
    @keydown="keyboard"
  >
    <a-space wrap class="mind-toolbar">
      <a-tag>模块 → 用例 → 前置条件 / 步骤 → 操作 / 预期</a-tag>
      <a-button @click="fit">重置视图</a-button>
      <template v-if="!readonly">
        <a-button @click="emit('create', selected?.moduleId)"
          >新增用例</a-button
        >
        <a-button :disabled="!selectedCase" @click="addStep">添加步骤</a-button>
        <a-button :disabled="!selectedCase" @click="copy">复制内容</a-button>
        <a-button :disabled="!clipboard" @click="paste">粘贴为新用例</a-button>
      </template>
      <span class="mind-hint"
        >滚轮缩放 · 拖动平移 · 点击节点查看{{
          readonly ? "" : " / 编辑（Ctrl/Cmd+C、V）"
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
        ><a-button type="text" @click="selected = undefined"
          >关闭</a-button
        ></template
      >
      <p class="node-title">{{ selected.name }}</p>
      <template v-if="selectedCase">
        <a-space wrap style="margin-bottom: 12px"
          ><a-button @click="emit('select', selectedCase)"
            >查看用例详情</a-button
          ><a-tag>{{ selectedCase.priority }}</a-tag></a-space
        >
        <template v-if="!readonly">
          <a-form layout="vertical">
            <a-form-item :label="fieldLabel"
              ><a-textarea
                v-model:value="editText"
                :rows="3"
                :maxlength="selected.kind === 'case' ? 200 : 10000"
            /></a-form-item>
            <a-space
              ><a-button type="primary" :loading="saving" @click="save"
                >保存节点</a-button
              ><a-popconfirm
                v-if="selected.stepIndex !== undefined"
                title="删除这个步骤及对应预期？"
                @confirm="removeStep"
                ><a-button danger>删除步骤</a-button></a-popconfirm
              ></a-space
            >
          </a-form>
        </template>
        <p v-else class="node-content">{{ editText }}</p>
      </template>
      <template v-else-if="selected.kind === 'module' && !readonly">
        <a-space direction="vertical" style="width: 100%"
          ><a-input v-model:value="editText" placeholder="模块名称" /><a-button
            v-if="selected.moduleId"
            :loading="saving"
            @click="emit('renameModule', selected.moduleId!, editText)"
            >保存模块名</a-button
          ><a-button @click="emit('create', selected.moduleId)"
            >在此模块新建用例</a-button
          ></a-space
        >
      </template>
    </a-card>
  </section>
</template>
<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { use } from "echarts/core";
import { TreeChart } from "echarts/charts";
import { TooltipComponent } from "echarts/components";
import { CanvasRenderer } from "echarts/renderers";
import VChart from "vue-echarts";
import { message } from "ant-design-vue";
import type { TestCase } from "@/types";
import {
  buildCaseMindMap,
  copyCaseDraft,
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
const clipboard = ref<Partial<TestCase>>();
const selectedCase = computed(() =>
  props.cases.find((c) => c.id === selected.value?.caseId),
);
const fieldLabel = computed(
  () =>
    ({
      case: "用例名称",
      precondition: "前置条件",
      action: "操作步骤",
      expected: "预期结果",
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
      left: 70,
      bottom: 35,
      right: 240,
      orient: "LR",
      roam: true,
      expandAndCollapse: false,
      initialTreeDepth: -1,
      symbolSize: 9,
      label: {
        position: "right",
        fontSize: 12,
        width: 160,
        overflow: "truncate",
        backgroundColor: "#f4f7fb",
        padding: [5, 8],
        borderRadius: 4,
      },
      lineStyle: { curveness: 0.5, color: "#c3d2e7" },
      emphasis: { focus: "descendant" },
      animationDuration: 180,
    },
  ],
}));
function selectNode(event: any) {
  selected.value = event.data;
  const c = props.cases.find((row) => row.id === event.data.caseId);
  const n = event.data;
  editText.value =
    n.kind === "module"
      ? n.name
      : n.kind === "case"
        ? c?.name || ""
        : n.kind === "precondition"
          ? c?.precondition || ""
          : n.kind === "expected"
            ? c?.steps?.[n.stepIndex!]?.expected || ""
            : c?.steps?.[n.stepIndex!]?.action || "";
  if (c && props.readonly) emit("select", c);
}
function save() {
  const c = selectedCase.value;
  const n = selected.value;
  if (!c?.id || !n) return;
  if (n.kind === "case") {
    if (!editText.value.trim()) return message.warning("请填写用例名称");
    emit("edit", c.id, { name: editText.value.trim() });
  } else if (n.kind === "precondition")
    emit("edit", c.id, { precondition: editText.value });
  else if (n.stepIndex !== undefined) {
    const steps = (c.steps || []).map((s) => ({ ...s }));
    steps[n.stepIndex] = {
      ...steps[n.stepIndex],
      [n.kind === "expected" ? "expected" : "action"]: editText.value,
    };
    emit("edit", c.id, { steps });
  }
}
function addStep() {
  const c = selectedCase.value;
  if (c?.id)
    emit("edit", c.id, {
      steps: [
        ...(c.steps || []),
        { step: (c.steps || []).length + 1, action: "新步骤", expected: "" },
      ],
    });
}
function removeStep() {
  const c = selectedCase.value;
  if (c?.id) {
    emit("edit", c.id, {
      steps: (c.steps || [])
        .filter((_, i) => i !== selected.value?.stepIndex)
        .map((s, i) => ({ ...s, step: i + 1 })),
    });
    selected.value = undefined;
  }
}
function copy() {
  if (selectedCase.value) {
    clipboard.value = copyCaseDraft(selectedCase.value);
    message.info("已复制用例内容，可粘贴为新用例");
  }
}
function paste() {
  if (clipboard.value)
    emit("create", selected.value?.moduleId, {
      ...clipboard.value,
      moduleId: selected.value?.moduleId || clipboard.value.moduleId,
    });
}
function keyboard(event: KeyboardEvent) {
  if (
    props.readonly ||
    ["INPUT", "TEXTAREA"].includes((event.target as HTMLElement).tagName)
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
  if (event.key === "Escape") selected.value = undefined;
}
function fit() {
  chart.value?.clear();
  chart.value?.setOption(option.value);
}
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
</script>
<style scoped>
.case-mind-map {
  position: relative;
  min-height: 600px;
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
  height: 650px;
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
