<template>
  <div>
    <a-space wrap
      ><a-tag :color="reportResultColor(run.report.outcome)">{{
        reportResultLabel(run.report.outcome)
      }}</a-tag
      ><span>批次 {{ run.id }}</span>
      <a-button @click="refresh" :disabled="busy">刷新</a-button
      ><a-button :loading="busy" @click="pdf" :disabled="busy"
        >导出 PDF</a-button
      ><a-button @click="shareOpen = true" :disabled="busy"
        >分享报告</a-button
      ></a-space
    >
    <a-row :gutter="16" class="stats"
      ><a-col :xs="12" :md="6"
        ><a-statistic title="执行项" :value="run.report.total" /></a-col
      ><a-col :xs="12" :md="6"
        ><a-statistic title="通过" :value="run.report.counts.passed" /></a-col
      ><a-col :xs="12" :md="6"
        ><a-statistic
          title="失败 / 错误"
          :value="
            (run.report.counts.failed || 0) + (run.report.counts.error || 0)
          " /></a-col
      ><a-col :xs="12" :md="6"
        ><a-statistic
          title="通过率"
          :value="run.report.passRate"
          suffix="%" /></a-col
    ></a-row>
    <a-tabs>
      <a-tab-pane key="plans" tab="计划结果"
        ><a-table
          :data-source="run.children"
          :columns="planColumns"
          row-key="id"
          size="small"
          :scroll="{ x: 650 }"
        >
          <template #bodyCell="{ column, record }"
            ><a
              v-if="column.key === 'name'"
              :href="childHref(record.id)"
              @click.prevent="openChild(record.id)"
              >{{ record.planName }}</a
            ><a-tag
              v-else-if="column.key === 'result'"
              :color="reportResultColor(record.report.outcome)"
              >{{ reportResultLabel(record.report.outcome) }}</a-tag
            ><span v-else-if="column.key === 'rate'"
              >{{ record.report.passRate }}%</span
            ></template
          >
        </a-table></a-tab-pane
      >
      <a-tab-pane key="cases" tab="用例结果"
        ><a-table
          :data-source="run.report.cases"
          :columns="caseColumns"
          :row-key="caseKey"
          size="small"
          :scroll="{ x: 650 }"
          ><template #bodyCell="{ column, record }"
            ><a-tag v-if="column.key === 'result'">{{
              caseResultLabel(record.result)
            }}</a-tag></template
          ></a-table
        ></a-tab-pane
      >
      <a-tab-pane key="summary" tab="报告总结"
        ><a-form layout="vertical"
          ><a-form-item label="测试结论"
            ><a-textarea
              :disabled="busy"
              v-model:value="summary.conclusion"
              :rows="3"
              :maxlength="10000" /></a-form-item
          ><a-form-item label="风险与遗留问题"
            ><a-textarea
              :disabled="busy"
              v-model:value="summary.risk"
              :rows="3"
              :maxlength="10000" /></a-form-item
          ><a-form-item label="备注"
            ><a-textarea
              :disabled="busy"
              v-model:value="summary.notes"
              :rows="3"
              :maxlength="10000" /></a-form-item
          ><a-button
            type="primary"
            :loading="busy"
            :disabled="busy"
            @click="save"
            >保存总结</a-button
          ></a-form
        ></a-tab-pane
      >
    </a-tabs>
  </div>
  <a-modal
    v-model:open="shareOpen"
    :closable="!busy"
    :mask-closable="!busy"
    :keyboard="!busy"
    title="限时只读报告分享"
    :footer="null"
    ><a-space wrap
      ><span>有效期（小时）</span
      ><a-input-number
        v-model:value="expiresHours"
        :disabled="busy"
        :min="1"
        :max="720"
      /><a-button type="primary" :loading="busy" :disabled="busy" @click="share"
        >创建分享链接</a-button
      ></a-space
    >
    <template v-if="shareLink"
      ><a-input :value="shareLink" readonly style="margin: 16px 0" /><a-space
        ><a-button @click="copyShare" :disabled="busy">复制链接</a-button
        ><a-button danger :loading="busy" :disabled="busy" @click="revoke"
          >撤销此分享</a-button
        ></a-space
      ></template
    >
  </a-modal>
</template>
<script setup lang="ts">
import {
  reactive,
  ref,
  watch,
  computed,
  onMounted,
  onBeforeUnmount,
} from "vue";
import { useRouter, onBeforeRouteLeave, onBeforeRouteUpdate } from "vue-router";
import { message, Modal } from "ant-design-vue";
import { planGroupApi, type GroupRun } from "@/api/planGroup";
import { reportResultLabel, reportResultColor } from "@/api/planReports";
import { useUserStore } from "@/stores/user";
const props = defineProps<{ run: GroupRun; projectId: string }>(),
  emit = defineEmits<{ refresh: [] }>(),
  router = useRouter(),
  user = useUserStore();
const busy = ref(false),
  shareOpen = ref(false),
  expiresHours = ref(24),
  shareLink = ref(""),
  shareId = ref("");
const summary = reactive({ conclusion: "", risk: "", notes: "" }),
  savedSummary = ref("");
const normalized = (value: GroupRun["summary"]) => ({
  conclusion: value.conclusion || "",
  risk: value.risk || "",
  notes: value.notes || "",
});
const dirty = computed(
  () => !!savedSummary.value && JSON.stringify(summary) !== savedSummary.value,
);
let generation = 0;
function reset() {
  ++generation;
  busy.value = false;
  shareOpen.value = false;
  shareLink.value = "";
  shareId.value = "";
  Object.assign(summary, normalized(props.run.summary));
  savedSummary.value = JSON.stringify(summary);
}
watch(
  () => JSON.stringify([props.projectId, props.run.id, user.user?.id]),
  reset,
  {
    immediate: true,
  },
);
watch(
  () => props.run.summary,
  (value) => {
    if (!busy.value) {
      const keepDraft = dirty.value,
        persisted = normalized(value);
      savedSummary.value = JSON.stringify(persisted);
      if (!keepDraft) Object.assign(summary, persisted);
    }
  },
);
const planColumns = [
  { title: "计划名称", key: "name" },
  { title: "结果", key: "result" },
  { title: "通过率", key: "rate" },
];
const caseColumns = [
  { title: "计划名称", dataIndex: "planName" },
  { title: "用例名称", dataIndex: "caseName" },
  { title: "结果", key: "result" },
  { title: "说明", dataIndex: "notes" },
];
const caseKey = (row: any) =>
  `${row.planRunId}:${row.executionId || "manual"}:${row.associationId || row.caseId}`;
const caseLabels: Record<string, string> = {
  passed: "通过",
  failed: "失败",
  pending: "未执行",
  error: "错误",
  skipped: "跳过",
  cancelled: "取消",
};
const caseResultLabel = (value: string) => caseLabels[value] || value;
const childHref = (id: string) =>
  router.resolve({
    name: "TestPlanReportDetail",
    params: { runId: id },
    query: { projectId: props.projectId, kind: "PLAN" },
  }).href;
async function beforeClose() {
  if (busy.value) {
    message.warning("请等待本次报告操作完成");
    return false;
  }
  if (!dirty.value) return true;
  const mine = generation;
  return new Promise<boolean>((resolve) =>
    Modal.confirm({
      title: "放弃未保存的报告总结？",
      okText: "丢弃草稿",
      cancelText: "继续编辑",
      onOk() {
        if (mine !== generation || busy.value) {
          resolve(false);
          return;
        }
        Object.assign(summary, JSON.parse(savedSummary.value));
        resolve(true);
      },
      onCancel() {
        resolve(false);
      },
    }),
  );
}
async function refresh() {
  if (await beforeClose()) emit("refresh");
}
async function openChild(id: string) {
  if (await beforeClose()) await router.push(childHref(id));
}
onBeforeRouteLeave(beforeClose);
onBeforeRouteUpdate(beforeClose);
async function operation(
  task: (runId: string, current: () => boolean) => Promise<void>,
) {
  if (busy.value) return;
  const mine = generation,
    runId = props.run.id,
    project = props.projectId,
    actor = user.user?.id;
  const current = () =>
    mine === generation &&
    runId === props.run.id &&
    project === props.projectId &&
    actor === user.user?.id;
  busy.value = true;
  try {
    await task(runId, current);
  } catch (error) {
    if (current()) message.error("操作失败，草稿保留；请重试");
  } finally {
    if (current()) busy.value = false;
  }
}
async function save() {
  const submitted = { ...summary };
  await operation(async (runId, current) => {
    await planGroupApi.summary(runId, submitted);
    if (!current()) return;
    savedSummary.value = JSON.stringify(submitted);
    message.success("总结已保存");
  });
}
async function pdf() {
  await operation(async (runId, current) => {
    const blob = await planGroupApi.pdf(runId);
    if (!current()) return;
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `ATS-计划组报告-${runId}.pdf`;
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
}
async function share() {
  const expiry = expiresHours.value;
  await operation(async (runId, current) => {
    const result = await planGroupApi.share(runId, expiry);
    if (!current()) return;
    shareLink.value = new URL(result.path, location.origin).href;
    shareId.value = result.id;
  });
}
async function copyShare() {
  const link = shareLink.value;
  if (!link || busy.value) return;
  await operation(async (_runId, current) => {
    await navigator.clipboard.writeText(link);
    if (current()) message.success("链接已复制");
  });
}
async function revoke() {
  const id = shareId.value;
  if (!id) return;
  await operation(async (runId, current) => {
    await planGroupApi.revoke(runId, id);
    if (!current()) return;
    shareLink.value = "";
    shareId.value = "";
    message.success("分享已撤销");
  });
}
function beforeUnload(event: BeforeUnloadEvent) {
  if (busy.value || dirty.value) {
    event.preventDefault();
    event.returnValue = "";
  }
}
onMounted(() => window.addEventListener("beforeunload", beforeUnload));
onBeforeUnmount(() => {
  ++generation;
  window.removeEventListener("beforeunload", beforeUnload);
});
defineExpose({ beforeClose });
</script>
<style scoped>
.stats {
  margin: 20px 0;
}
.stats .ant-col {
  margin-bottom: 12px;
}
</style>
