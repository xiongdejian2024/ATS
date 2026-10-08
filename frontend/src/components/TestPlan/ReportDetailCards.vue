<template>
  <div class="report-cards">
    <div class="card-tools">
      <a-button size="small" @click="openSettings">卡片设置</a-button>
    </div>
    <a-card
      v-for="card in visibleCards"
      :key="card.key"
      :title="title(card.key)"
      size="small"
    >
      <a-row v-if="card.key === 'overview'" :gutter="16">
        <a-col :xs="12" :md="6"
          ><a-statistic title="执行项" :value="report.total"
        /></a-col>
        <a-col :xs="12" :md="6"
          ><a-statistic title="通过" :value="report.counts.passed || 0"
        /></a-col>
        <a-col :xs="12" :md="6"
          ><a-statistic
            title="失败 / 错误"
            :value="(report.counts.failed || 0) + (report.counts.error || 0)"
        /></a-col>
        <a-col :xs="12" :md="6"
          ><a-statistic
            :title="settled ? '通过率' : '当前通过率'"
            :value="report.passRate"
            suffix="%"
        /></a-col>
      </a-row>
      <template v-else-if="card.key === 'analysis'">
        <a-space wrap
          ><a-tag v-for="row in resultCounts" :key="row.state"
            >{{ stateLabel(row.state) }}：{{ row.count }}</a-tag
          ></a-space
        >
        <a-empty v-if="!resultCounts.length" description="尚无执行项" />
      </template>
      <template v-else-if="card.key === 'testSets'">
        <a-table
          :data-source="details?.testSets || []"
          :columns="setColumns"
          row-key="key"
          size="small"
          :pagination="{ pageSize: 20, showSizeChanger: false }"
          :scroll="{ x: 900 }"
        >
          <template #bodyCell="{ column, record }">
            <span v-if="column.key === 'testSet'">{{
              setName(record.testSet)
            }}</span>
            <span v-else-if="column.key === 'category'">{{
              categoryLabel(record.category)
            }}</span>
            <span v-else-if="column.key === 'passed'">{{
              record.counts.passed || 0
            }}</span>
            <span v-else-if="column.key === 'failed'">{{
              (record.counts.failed || 0) + (record.counts.error || 0)
            }}</span>
            <span v-else-if="column.key === 'rate'"
              >{{ record.passRate }}%</span
            >
          </template>
        </a-table>
      </template>
      <template v-else-if="card.key === 'defects'">
        <p class="hint">
          按本批次步骤保存的缺陷记录统计；展开查看各实例当时的标题和状态。
        </p>
        <a-table
          :data-source="details?.defects || []"
          :columns="defectColumns"
          row-key="id"
          size="small"
          :pagination="{ pageSize: 20, showSizeChanger: false }"
          :scroll="{ x: 600 }"
        >
          <template #expandedRowRender="{ record }">
            <a-table
              :data-source="record.occurrences"
              :columns="occurrenceColumns"
              row-key="key"
              size="small"
              :pagination="{ pageSize: 20, showSizeChanger: false }"
              :scroll="{ x: 1100 }"
            >
              <template #bodyCell="{ column, record: location }"
                ><span v-if="column.key === 'testSet'">{{
                  setName(location.testSet)
                }}</span
                ><span v-else-if="column.key === 'step'">{{
                  Number.isInteger(location.stepIndex)
                    ? location.stepIndex + 1
                    : "未记录"
                }}</span></template
              >
            </a-table>
          </template>
        </a-table>
      </template>
      <template v-else-if="card.key === 'configuration'">
        <p class="hint">
          显示批次创建时保存的执行配置；未记录的字段显示“未记录”。
        </p>
        <a-descriptions
          v-for="policy in details?.configuration.policies || []"
          :key="policy.key"
          :title="policy.planName"
          size="small"
          bordered
          :column="{ xs: 1, sm: 2, md: 3 }"
          class="policy"
        >
          <a-descriptions-item label="执行模式">{{
            mode(policy.executionMode)
          }}</a-descriptions-item
          ><a-descriptions-item label="失败停止">{{
            booleanLabel(policy.stopOnFailure)
          }}</a-descriptions-item
          ><a-descriptions-item label="通过阈值">{{
            policy.passThreshold === undefined
              ? "未记录"
              : `${policy.passThreshold}%`
          }}</a-descriptions-item>
        </a-descriptions>
        <a-table
          :data-source="details?.configuration.items || []"
          :columns="configColumns"
          row-key="id"
          size="small"
          :pagination="{ pageSize: 20, showSizeChanger: false }"
          :scroll="{ x: 1000 }"
        >
          <template #bodyCell="{ column, record }"
            ><span v-if="column.key === 'testSet'">{{
              setName(record.testSet)
            }}</span></template
          >
          <template #expandedRowRender="{ record }">
            <a-descriptions
              size="small"
              bordered
              :column="{ xs: 1, sm: 2, md: 3 }"
            >
              <a-descriptions-item label="执行模式">{{
                mode(record.executionConfig.executionMode)
              }}</a-descriptions-item
              ><a-descriptions-item label="继承上级">{{
                booleanLabel(record.executionConfig.extended)
              }}</a-descriptions-item
              ><a-descriptions-item label="失败停止">{{
                booleanLabel(record.executionConfig.stopOnFailure)
              }}</a-descriptions-item>
              <a-descriptions-item label="失败重试">{{
                booleanLabel(record.executionConfig.retryOnFailure)
              }}</a-descriptions-item
              ><a-descriptions-item label="重试次数">{{
                record.executionConfig.retryTimes ?? "未记录"
              }}</a-descriptions-item
              ><a-descriptions-item label="重试间隔（毫秒）">{{
                record.executionConfig.retryInterval ?? "未记录"
              }}</a-descriptions-item>
              <a-descriptions-item label="请求环境">{{
                record.executionConfig.requestEnvironmentId === "NONE"
                  ? "无"
                  : record.executionConfig.requestEnvironmentId || "未记录"
              }}</a-descriptions-item
              ><a-descriptions-item label="资源池">{{
                record.executionConfig.testResourcePoolId === "DEFAULT"
                  ? "默认资源池"
                  : record.executionConfig.testResourcePoolId || "未记录"
              }}</a-descriptions-item
              ><a-descriptions-item label="冻结节点范围">{{
                record.resourcePool.length
                  ? record.resourcePool.join("、")
                  : "未记录"
              }}</a-descriptions-item>
            </a-descriptions>
          </template>
        </a-table>
        <a-empty v-if="!details" description="此报告未提供冻结配置" />
      </template>
    </a-card>
  </div>
  <a-drawer
    :open="settingsOpen"
    title="报告卡片设置"
    width="min(480px,100vw)"
    @close="beforeClose"
  >
    <a-alert
      v-if="settingsError"
      type="error"
      :message="settingsError"
      show-icon
    />
    <div class="setting-row">
      <span>执行概况</span><a-switch checked disabled />
    </div>
    <VueDraggable v-model="draft" handle=".sort-handle" :animation="150">
      <div v-for="card in draft" :key="card.key" class="setting-row">
        <span
          ><HolderOutlined
            class="sort-handle"
            :aria-label="`拖动${title(card.key)}`"
          />
          {{ title(card.key) }}</span
        ><a-switch
          v-model:checked="card.visible"
          :aria-label="`显示${title(card.key)}`"
        />
      </div>
    </VueDraggable>
    <a-space class="settings-actions"
      ><a-button type="primary" @click="saveSettings">保存</a-button
      ><a-button @click="restoreDefaults">默认设置</a-button
      ><a-button @click="discardSettings">取消</a-button></a-space
    >
  </a-drawer>
</template>
<script setup lang="ts">
import { ref, computed, watch, onMounted, onBeforeUnmount } from "vue";
import { onBeforeRouteLeave, onBeforeRouteUpdate } from "vue-router";
import { Modal, message } from "ant-design-vue";
import { VueDraggable } from "vue-draggable-plus";
import { HolderOutlined } from "@ant-design/icons-vue";
import { useUserStore } from "@/stores/user";
import type { ReportDetails, FrozenTestSet } from "@/api/reportDetails";
import {
  reportCards,
  readReportCards,
  reportCardsKey,
  normalizeReportCards,
  type ReportCardPreference,
} from "./reportCardPreferences";
const props = defineProps<{
  projectId: string;
  kind: "PLAN" | "GROUP";
  runId: string;
  status: string;
  report: { total: number; counts: Record<string, number>; passRate: number };
  details?: ReportDetails;
}>();
const user = useUserStore(),
  cards = ref<ReportCardPreference[]>(normalizeReportCards(undefined)),
  draft = ref<ReportCardPreference[]>([]),
  settingsOpen = ref(false),
  settingsError = ref("");
const storageKey = computed(() =>
  reportCardsKey(user.user?.id || "", props.projectId, props.kind),
);
let generation = 0,
  live = true,
  closing = false;
watch(
  () =>
    JSON.stringify([props.projectId, props.kind, props.runId, user.user?.id]),
  () => {
    ++generation;
    closing = false;
    settingsOpen.value = false;
    settingsError.value = "";
    draft.value = [];
    try {
      cards.value =
        user.user?.id && props.projectId
          ? readReportCards(localStorage, storageKey.value)
          : normalizeReportCards(undefined);
    } catch (error) {
      console.error("读取报告卡片配置失败", error);
      cards.value = normalizeReportCards(undefined);
    }
  },
  { immediate: true, flush: "sync" },
);
const title = (key: string) =>
  reportCards.find((c) => c.key === key)?.title || key;
const visibleCards = computed(() => cards.value.filter((c) => c.visible));
const settled = computed(() =>
  ["completed", "failed", "cancelled", "skipped"].includes(props.status),
);
const resultCounts = computed(() =>
  Object.entries(props.report.counts)
    .filter(([, count]) => count > 0)
    .map(([state, count]) => ({ state, count })),
);
const stateLabel = (value: string) =>
  (
    ({
      passed: "通过",
      failed: "失败",
      error: "错误",
      fake_error: "误报",
      blocked: "阻塞",
      pending: "未执行",
      skipped: "跳过",
      cancelled: "取消",
    }) as Record<string, string>
  )[value] || value;
const categoryLabel = (value: string) =>
  (
    ({ functional: "功能", api: "API", scenario: "场景" }) as Record<
      string,
      string
    >
  )[value] || value;
const setName = (set: FrozenTestSet) =>
  set.path?.length ? set.path.map((p) => p.name).join(" / ") : set.name;
const mode = (value?: string) =>
  value === "serial" ? "串行" : value === "parallel" ? "并行" : "未记录";
const booleanLabel = (value?: boolean) =>
  value === true ? "是" : value === false ? "否" : "未记录";
const setColumns = [
  { title: "计划", dataIndex: "planName" },
  { title: "测试集", key: "testSet" },
  { title: "分类", key: "category" },
  { title: "执行项", dataIndex: "total" },
  { title: "通过", key: "passed" },
  { title: "失败 / 错误", key: "failed" },
  { title: "通过率", key: "rate" },
  { title: "关联缺陷", dataIndex: "defectCount" },
];
const defectColumns = [
  { title: "缺陷编号", dataIndex: "id" },
  { title: "首次记录标题", dataIndex: "title" },
  { title: "关联位置数", dataIndex: "occurrenceCount" },
];
const occurrenceColumns = [
  { title: "计划", dataIndex: "planName" },
  { title: "测试集", key: "testSet" },
  { title: "用例", dataIndex: "caseName" },
  { title: "关联实例", dataIndex: "associationId" },
  { title: "步骤", key: "step" },
  { title: "当时标题", dataIndex: "title" },
  { title: "当时状态", dataIndex: "status" },
];
const configColumns = [
  { title: "计划", dataIndex: "planName" },
  { title: "测试集", key: "testSet" },
  { title: "测试套", dataIndex: "suiteName" },
  { title: "冻结执行节点", dataIndex: "environmentId" },
  { title: "执行编号", dataIndex: "executionId" },
];
const dirty = computed(
  () =>
    JSON.stringify(normalizeReportCards(draft.value)) !==
    JSON.stringify(cards.value),
);
function openSettings() {
  if (
    closing ||
    settingsOpen.value ||
    !live ||
    !user.user?.id ||
    !props.projectId
  )
    return;
  draft.value = cards.value
    .filter((c) => c.key !== "overview")
    .map((c) => ({ ...c }));
  settingsError.value = "";
  settingsOpen.value = true;
}
function restoreDefaults() {
  draft.value = normalizeReportCards(undefined).filter(
    (c) => c.key !== "overview",
  );
  settingsError.value = "";
}
function discardSettings() {
  if (closing) return;
  settingsOpen.value = false;
  settingsError.value = "";
  draft.value = [];
}
function saveSettings() {
  if (
    closing ||
    !settingsOpen.value ||
    !live ||
    !user.user?.id ||
    !props.projectId
  )
    return;
  const value = normalizeReportCards(draft.value);
  try {
    if (JSON.stringify(value) !== JSON.stringify(cards.value))
      localStorage.setItem(storageKey.value, JSON.stringify(value));
    cards.value = value;
    settingsOpen.value = false;
    settingsError.value = "";
    message.success("报告卡片设置已保存");
  } catch (error) {
    console.error("保存报告卡片设置失败", error);
    settingsError.value = "保存失败，草稿已保留；请重试或取消。";
  }
}
async function beforeClose() {
  if (closing) return false;
  if (!settingsOpen.value) return true;
  if (!dirty.value) {
    discardSettings();
    return true;
  }
  const mine = generation,
    submitted = JSON.stringify(draft.value);
  closing = true;
  try {
    return await new Promise<boolean>((resolve) =>
      Modal.confirm({
        title: "放弃未保存的报告卡片设置？",
        okText: "丢弃草稿",
        cancelText: "继续编辑",
        onOk() {
          if (
            !live ||
            mine !== generation ||
            submitted !== JSON.stringify(draft.value)
          ) {
            resolve(false);
            return;
          }
          settingsOpen.value = false;
          settingsError.value = "";
          draft.value = [];
          resolve(true);
        },
        onCancel() {
          resolve(false);
        },
      }),
    );
  } finally {
    if (mine === generation) closing = false;
  }
}
onBeforeRouteLeave(beforeClose);
onBeforeRouteUpdate(beforeClose);
function beforeUnload(event: BeforeUnloadEvent) {
  if (settingsOpen.value && dirty.value) {
    event.preventDefault();
    event.returnValue = "";
  }
}
onMounted(() => window.addEventListener("beforeunload", beforeUnload));
onBeforeUnmount(() => {
  live = false;
  ++generation;
  window.removeEventListener("beforeunload", beforeUnload);
});
defineExpose({ beforeClose });
</script>
<style scoped>
.report-cards {
  margin: 16px 0;
  min-width: 0;
}
.card-tools {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 8px;
}
.report-cards :deep(.ant-card) {
  margin-bottom: 12px;
}
.hint {
  color: var(--ms-text-secondary);
  font-size: 12px;
}
.policy {
  margin-bottom: 12px;
}
.setting-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 18px 0;
  gap: 12px;
}
.sort-handle {
  cursor: grab;
}
.settings-actions {
  margin-top: 18px;
}
.report-cards :deep(.ant-descriptions-item-content) {
  overflow-wrap: anywhere;
}
</style>
