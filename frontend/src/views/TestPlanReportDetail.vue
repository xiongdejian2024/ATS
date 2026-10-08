<template>
  <section class="report-detail">
    <header class="report-heading">
      <a-button @click="back"><ArrowLeftOutlined /> 返回报告列表</a-button>
      <h2>{{ detail?.name || "计划报告" }}</h2>
    </header>
    <a-alert v-if="!projectId" message="请选择项目" type="info" />
    <a-spin v-else :spinning="loading">
      <a-result
        v-if="failed"
        status="error"
        title="报告不可用"
        sub-title="请检查当前项目、报告链接及访问权限。"
        ><template #extra
          ><a-button @click="load">重试</a-button></template
        ></a-result
      >
      <template v-else-if="detail">
        <p class="report-meta">
          {{ detail.kind === "GROUP" ? "集成报告" : "普通报告" }} ·
          {{
            detail.kind === "GROUP"
              ? detail.payload.groupName
              : detail.payload.planName
          }}
          · {{ dayjs(detail.payload.startedAt).format("YYYY-MM-DD HH:mm:ss") }}
        </p>
        <PlanRunReport
          v-if="detail.kind === 'PLAN'"
          :key="`${projectId}:${runId}`"
          :run-id="runId"
          :project-id="projectId"
          :association-id="
            typeof route.query.associationId === 'string'
              ? route.query.associationId
              : undefined
          "
        />
        <PlanGroupReport
          v-else
          ref="groupReport"
          :key="`${projectId}:${runId}`"
          :run="detail.payload"
          :project-id="projectId"
          @refresh="load"
        />
      </template>
    </a-spin>
  </section>
</template>
<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ArrowLeftOutlined } from "@ant-design/icons-vue";
import dayjs from "dayjs";
import { useProjectStore } from "@/stores/project";
import { useUserStore } from "@/stores/user";
import { planReportsApi, type ReportDetail } from "@/api/planReports";
import PlanRunReport from "@/components/TestPlan/PlanRunReport.vue";
import PlanGroupReport from "@/components/TestPlan/PlanGroupReport.vue";
const route = useRoute(),
  router = useRouter(),
  projectStore = useProjectStore(),
  user = useUserStore();
const projectId = computed(() =>
  typeof route.query.projectId === "string"
    ? route.query.projectId
    : projectStore.currentProject?.id,
);
const runId = computed(() => String(route.params.runId || "")),
  kind = computed(() => (route.query.kind === "GROUP" ? "GROUP" : "PLAN"));
const detail = ref<ReportDetail>(),
  loading = ref(false),
  failed = ref(false);
const groupReport = ref<{ beforeClose: () => Promise<boolean> }>();
const loadedIdentity = ref("");
let sequence = 0;
async function load() {
  const current = ++sequence,
    project = projectId.value,
    run = runId.value,
    reportKind = kind.value,
    actor = user.user?.id;
  const identity = JSON.stringify([project, reportKind, run, actor]);
  if (
    groupReport.value &&
    identity === loadedIdentity.value &&
    !(await groupReport.value.beforeClose())
  )
    return;
  if (
    current !== sequence ||
    project !== projectId.value ||
    run !== runId.value ||
    actor !== user.user?.id
  )
    return;
  detail.value = undefined;
  failed.value = false;
  if (!project) {
    loading.value = false;
    return;
  }
  loading.value = true;
  try {
    const result = await planReportsApi.detail(project, reportKind, run);
    if (current === sequence && actor === user.user?.id) {
      detail.value = result;
      loadedIdentity.value = identity;
    }
  } catch (error) {
    console.error("加载独立计划报告失败", error);
    if (current === sequence) failed.value = true;
  } finally {
    if (current === sequence) loading.value = false;
  }
}
const back = () =>
  router.push({
    name: "TestPlanReports",
    query: { projectId: projectId.value },
  });
watch(() => [projectId.value, runId.value, kind.value, user.user?.id], load, {
  immediate: true,
});
</script>
<style scoped>
.report-detail {
  background: white;
  padding: 16px;
  min-height: 100%;
  min-width: 0;
}
.report-heading {
  display: flex;
  gap: 16px;
  align-items: center;
  flex-wrap: wrap;
  margin-bottom: 12px;
}
.report-heading h2 {
  font-size: 18px;
  margin: 0;
  overflow-wrap: anywhere;
}
.report-meta {
  color: var(--ms-text-secondary);
  font-size: 12px;
}
@media (max-width: 768px) {
  .report-detail {
    padding: 12px;
  }
}
</style>
