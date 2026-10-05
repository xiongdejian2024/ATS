<template>
  <section class="functional-execution">
    <header>
      <a-button @click="back">返回测试计划</a-button>
      <h2>{{ plan?.name || "功能用例执行" }}</h2>
    </header>
    <a-result
      v-if="failed"
      status="error"
      title="用例执行页面不可用"
      sub-title="请检查项目、计划关联和访问权限。"
      ><template #extra
        ><a-button @click="loadContext">重试</a-button></template
      ></a-result
    >
    <a-spin v-else :spinning="loading">
      <div v-if="plan" class="execution-layout">
        <aside class="case-sidebar">
          <h3>
            功能用例 <span>{{ listing?.total || 0 }}</span>
          </h3>
          <a-input-search
            v-model:value="search"
            placeholder="搜索 ID / 用例名称"
            allow-clear
            @search="filterCases"
          />
          <a-select
            v-model:value="resultFilter"
            mode="multiple"
            placeholder="执行结果"
            allow-clear
            :options="resultOptions"
            @change="filterCases"
          />
          <a-alert v-if="listFailed" type="error" message="用例列表加载失败"
            ><template #action><a @click="loadList">重试</a></template></a-alert
          >
          <a-spin :spinning="listLoading"
            ><div class="case-cards">
              <button
                v-for="item in listing?.items || []"
                :key="item.id"
                class="case-card"
                :class="{ active: item.id === selectedKey }"
                @click="selectCase(item)"
              >
                <span>{{ item.caseCode }}</span
                ><strong>{{ item.name }}</strong
                ><a-tag :color="resultColor(item.result)">{{
                  labels[item.result] || item.result
                }}</a-tag
                ><small v-if="item.recycled">已回收</small></button
              ><a-empty
                v-if="listing && !listing.items.length"
                description="当前范围没有用例"
              /></div
          ></a-spin>
          <a-pagination
            v-model:current="page"
            :total="listing?.total || 0"
            :page-size="listSize"
            simple
            @change="loadList"
          />
        </aside>
        <main class="execution-detail">
          <a-spin :spinning="detailLoading">
            <a-result
              v-if="detailFailed"
              status="error"
              title="执行详情加载失败"
              ><template #extra
                ><a-button @click="loadDetail">重试</a-button></template
              ></a-result
            >
            <template v-else-if="detail && currentCase">
              <div class="case-heading">
                <a-tag
                  :color="
                    resultColor(
                      detail.entry?.result ||
                        detail.history[0]?.result ||
                        'pending',
                    )
                  "
                  >{{
                    labels[
                      detail.entry?.result ||
                        detail.history[0]?.result ||
                        "pending"
                    ]
                  }}</a-tag
                ><a @click="openMainCase">{{ currentCase.caseCode }}</a>
                <h3>{{ currentCase.name }}</h3>
              </div>
              <a-alert
                v-if="detail.detached"
                type="info"
                message="原计划关联已移除，保留执行历史供查阅"
              />
              <a-alert
                v-else-if="detail.entry?.recycled"
                type="info"
                message="主用例已回收，当前关联不可执行"
              />
              <a-tabs v-model:active-key="tab">
                <a-tab-pane
                  :disabled="mediaUploading || saving"
                  key="basic"
                  tab="基本信息"
                  ><a-descriptions bordered :column="1"
                    ><a-descriptions-item label="优先级">{{
                      currentCase.priority
                    }}</a-descriptions-item
                    ><a-descriptions-item label="测试集">{{
                      detail.entry?.collectionName || "原关联已移除"
                    }}</a-descriptions-item
                    ><a-descriptions-item label="模块">{{
                      detail.entry?.moduleName || "—"
                    }}</a-descriptions-item
                    ><a-descriptions-item label="执行人">{{
                      detail.entry?.executorName || "—"
                    }}</a-descriptions-item
                    ><a-descriptions-item label="标签"
                      ><a-tag
                        v-for="tag in currentCase.tags || []"
                        :key="tag"
                        >{{ tag }}</a-tag
                      ></a-descriptions-item
                    ></a-descriptions
                  ></a-tab-pane
                >
                <a-tab-pane
                  :disabled="mediaUploading || saving"
                  key="details"
                  tab="用例详情"
                >
                  <h4>前置条件</h4>
                  <CaseRichText
                    :model-value="currentCase.precondition || ''"
                    readonly
                    label="前置条件"
                  />
                  <template v-if="currentCase.caseEditType === 'TEXT'"
                    ><h4>步骤描述</h4>
                    <CaseRichText
                      :model-value="currentCase.textDescription || ''"
                      readonly
                      label="步骤描述" />
                    <h4>预期结果</h4>
                    <CaseRichText
                      :model-value="currentCase.expectedResult || ''"
                      readonly
                      label="预期结果"
                  /></template>
                  <div
                    v-else
                    v-for="(step, index) in currentCase.steps || []"
                    :key="index"
                    class="execution-step"
                  >
                    <h4>步骤 {{ index + 1 }}</h4>
                    <div class="step-content">
                      <CaseRichText
                        :model-value="step.action"
                        readonly
                        label="操作步骤"
                      /><CaseRichText
                        :model-value="step.expected"
                        readonly
                        label="预期结果"
                      />
                    </div>
                    <a-space
                      v-if="detail.canExecute"
                      direction="vertical"
                      class="step-result"
                      ><a-select
                        v-model:value="steps[index].result"
                        :disabled="saving"
                        :options="resultOptions"
                        @change="deriveResult" /><a-textarea
                        v-model:value="steps[index].actual"
                        :disabled="saving"
                        :maxlength="10000"
                        placeholder="实际结果"
                    /></a-space>
                  </div>
                  <h4>备注</h4>
                  <CaseRichText
                    :model-value="currentCase.description || ''"
                    readonly
                    label="用例备注"
                  />
                  <CaseAttachments
                    v-if="!detail.detached && !detail.entry?.recycled"
                    :key="selectedKey"
                    :project-id="projectId"
                    :case-id="caseId"
                    read-only
                  />
                </a-tab-pane>
                <a-tab-pane
                  :disabled="mediaUploading || saving"
                  key="defects"
                  tab="缺陷"
                  ><PlanDefects
                    :key="selectedKey"
                    :plan-id="planId"
                    :case-id="caseId"
                    :editable="
                      !!plan.capabilities?.edit &&
                      !detail.detached &&
                      !detail.entry?.recycled
                    "
                /></a-tab-pane>
                <a-tab-pane
                  :disabled="mediaUploading || saving"
                  key="history"
                  :tab="`执行历史 (${detail.total})`"
                  ><a-empty
                    v-if="!detail.history.length"
                    description="暂无独立执行记录" />
                  <article
                    v-for="record in detail.history"
                    :key="record.id"
                    class="history-record"
                  >
                    <a-space wrap
                      ><a-tag :color="resultColor(record.result)">{{
                        labels[record.result]
                      }}</a-tag
                      ><span>{{ record.executorName }}</span
                      ><time>{{ formatTime(record.createdAt) }}</time></a-space
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
                      步骤 {{ step.index + 1 }}：{{ labels[step.result] }}
                      {{ step.actual }}
                    </p>
                  </article>
                  <a-pagination
                    v-if="detail.total > 10"
                    v-model:current="historyPage"
                    :page-size="10"
                    :total="detail.total"
                    @change="loadDetail(false)"
                /></a-tab-pane>
              </a-tabs>
              <div
                v-if="detail.canExecute && tab === 'details'"
                class="submit-panel"
              >
                <PlanCaseExecutionSubmit
                  v-model:result="result"
                  v-model:description="description"
                  :disabled="saving"
                  :plan-id="planId"
                  v-model:uploading="mediaUploading"
                  v-model:dialog-dirty="dialogDirty"
                  :on-submit="submit"
                  ><a-switch
                    v-model:checked="autoNext"
                    :disabled="saving || mediaUploading"
                  /><span>提交后自动切换下一条</span></PlanCaseExecutionSubmit
                >
              </div>
            </template>
          </a-spin>
        </main>
      </div>
    </a-spin>
  </section>
</template>
<script setup lang="ts">
import { computed, reactive, ref, watch } from "vue";
import dayjs from "dayjs";
import { useEventListener } from "@vueuse/core";
import {
  onBeforeRouteLeave,
  onBeforeRouteUpdate,
  useRoute,
  useRouter,
} from "vue-router";
import { message, Modal } from "ant-design-vue";
import { testPlanApi } from "@/api/testPlan";
import {
  planCaseWorkspaceApi,
  type PlanCaseEntry,
  type PlanCaseListing,
  type PlanCaseExecutionDetail,
} from "@/api/planCaseWorkspace";
import { useProjectStore } from "@/stores/project";
import type { TestPlan } from "@/types";
import CaseAttachments from "@/components/TestCase/CaseAttachments.vue";
import CaseRichText from "@/components/TestCase/CaseRichText.vue";
import PlanCaseExecutionSubmit from "@/components/TestPlan/PlanCaseExecutionSubmit.vue";
import PlanDefects from "@/components/TestPlan/PlanDefects.vue";
import {
  functionalResults,
  functionalResultLabels as labels,
  nextFunctionalEntry,
  functionalListingState,
} from "@/components/TestPlan/functionalExecution";
const route = useRoute(),
  router = useRouter(),
  projects = useProjectStore();
const planId = computed(() => String(route.params.planId || ""));
const projectId = computed(() =>
  String(route.query.projectId || projects.currentProject?.id || ""),
);
const caseId = computed(() => String(route.query.caseId || ""));
const selectedKey = computed(
  () => `${route.query.source}:${route.query.associationId}:${caseId.value}`,
);
const plan = ref<TestPlan>(),
  listing = ref<PlanCaseListing>(),
  detail = ref<PlanCaseExecutionDetail>();
const currentCase = computed(
  () => detail.value?.entry || detail.value?.history[0]?.caseSnapshot,
);
const loading = ref(false),
  failed = ref(false),
  listLoading = ref(false),
  listFailed = ref(false),
  detailLoading = ref(false),
  detailFailed = ref(false),
  saving = ref(false),
  mediaUploading = ref(false),
  dialogDirty = ref(false);
const initialListing = functionalListingState(route.query);
const listSize = initialListing.size;
const search = ref(initialListing.search),
  resultFilter = ref<string[]>(
    (initialListing.result || "").split(",").filter(Boolean),
  ),
  page = ref(initialListing.page),
  historyPage = ref(1),
  tab = ref("details");
const result = ref("passed"),
  description = ref(""),
  autoNext = ref(false);
const steps = reactive<{ index: number; result: string; actual: string }[]>([]);
const resultOptions = [
  { value: "pending", label: "未执行" },
  ...functionalResults,
];
const draft = () =>
  JSON.stringify({
    result: result.value,
    description: description.value,
    steps,
  });
const baseline = ref(""),
  dirty = computed(
    () => dialogDirty.value || (!!baseline.value && draft() !== baseline.value),
  );
let contextSequence = 0,
  listSequence = 0,
  detailSequence = 0,
  retryPayload = "",
  retryId = "";
const formatTime = (value: string) =>
  dayjs(value).format("YYYY-MM-DD HH:mm:ss");
useEventListener(window, "beforeunload", (event) => {
  if (dirty.value || saving.value || mediaUploading.value) {
    event.preventDefault();
    event.returnValue = "";
  }
});
function resultColor(value: string) {
  return (
    { passed: "green", failed: "red", blocked: "orange" } as Record<
      string,
      string
    >
  )[value];
}
function confirmLeave(): Promise<boolean> {
  if (saving.value || mediaUploading.value) return Promise.resolve(false);
  if (!dirty.value) return Promise.resolve(true);
  return new Promise((resolve) =>
    Modal.confirm({
      title: "执行结果尚未提交",
      content: "离开会丢弃当前执行描述和步骤结果。",
      okText: "丢弃并离开",
      cancelText: "继续编辑",
      onOk() {
        baseline.value = "";
        resolve(true);
      },
      onCancel() {
        resolve(false);
      },
    }),
  );
}
onBeforeRouteLeave(confirmLeave);
onBeforeRouteUpdate(async (to, from) => {
  if (
    to.params.planId !== from.params.planId ||
    to.query.projectId !== from.query.projectId ||
    to.query.caseId !== from.query.caseId ||
    to.query.associationId !== from.query.associationId
  )
    return confirmLeave();
  return true;
});
async function loadContext() {
  const request = ++contextSequence;
  ++listSequence;
  ++detailSequence;
  plan.value = undefined;
  listing.value = undefined;
  detail.value = undefined;
  baseline.value = "";
  loading.value = true;
  failed.value = false;
  try {
    const data = await testPlanApi.getTestPlan(planId.value, projectId.value);
    if (request !== contextSequence) return;
    plan.value = data;
    await Promise.all([loadList(), loadDetail()]);
  } catch (error) {
    console.error("加载功能用例执行页面失败", error);
    if (request === contextSequence) failed.value = true;
  } finally {
    if (request === contextSequence) loading.value = false;
  }
}
async function loadList() {
  if (!plan.value) return;
  const request = ++listSequence;
  listLoading.value = true;
  listFailed.value = false;
  try {
    const data = await planCaseWorkspaceApi.list(planId.value, {
      category: "functional",
      page: page.value,
      size: listSize,
      search: search.value,
      result: resultFilter.value?.join(","),
      priority: initialListing.priority,
      executor: initialListing.executor,
      tag: initialListing.tag,
      sort: initialListing.sort,
      direction: initialListing.direction,
      tree_type: route.query.caseTree === "MODULE" ? "MODULE" : "COLLECTION",
      folder: route.query.caseFolder || "all",
    });
    if (request === listSequence) listing.value = data;
  } catch (error) {
    console.error("加载执行页功能用例列表失败", error);
    if (request === listSequence) {
      listing.value = undefined;
      listFailed.value = true;
    }
  } finally {
    if (request === listSequence) listLoading.value = false;
  }
}
async function loadDetail(reset = true) {
  if (!plan.value || !caseId.value) return;
  const request = ++detailSequence;
  detailLoading.value = true;
  detailFailed.value = false;
  detail.value = undefined;
  try {
    const data = await planCaseWorkspaceApi.execution(planId.value, {
      source: route.query.source,
      associationId: route.query.associationId,
      caseId: caseId.value,
      page: historyPage.value,
      size: 10,
    });
    if (request !== detailSequence) return;
    detail.value = data;
    if (reset) {
      result.value = "passed";
      description.value = "";
      steps.splice(
        0,
        steps.length,
        ...(data.entry?.caseEditType === "TEXT"
          ? []
          : (data.entry?.steps || []).map((_, index) => ({
              index,
              result: "pending",
              actual: "",
            }))),
      );
      baseline.value = draft();
      retryPayload = "";
      retryId = "";
    }
  } catch (error) {
    console.error("加载功能用例执行详情失败", error);
    if (request === detailSequence) detailFailed.value = true;
  } finally {
    if (request === detailSequence) detailLoading.value = false;
  }
}
function filterCases() {
  page.value = 1;
  void loadList();
}
function deriveResult() {
  result.value = steps.some((step) => step.result === "failed")
    ? "failed"
    : steps.some((step) => step.result === "blocked")
      ? "blocked"
      : steps.every((step) => step.result === "passed")
        ? "passed"
        : "pending";
}
async function selectCase(item: PlanCaseEntry) {
  await router.push({
    name: "PlanFunctionalExecution",
    params: { planId: planId.value },
    query: {
      ...route.query,
      source: item.source,
      associationId: item.associationId,
      caseId: item.caseId,
      casePage: String(page.value),
    },
  });
}
function back() {
  const { source, associationId, caseId: unused, ...query } = route.query;
  void router.push({
    name: "TestPlanDetailPage",
    params: { planId: planId.value },
    query: { ...query, tab: "featureCase" },
  });
}
function openMainCase() {
  void router.push({
    name: "CaseEdit",
    params: { caseId: caseId.value },
    query: { projectId: projectId.value },
  });
}
async function submit(): Promise<boolean> {
  const entry = detail.value?.entry;
  if (
    !entry ||
    !detail.value?.canExecute ||
    saving.value ||
    mediaUploading.value
  )
    return false;
  if (!functionalResults.some((option) => option.value === result.value)) {
    message.warning("请选择通过、失败或阻塞");
    return false;
  }
  const stepResults = steps.some(
    (step) => step.result !== "pending" || step.actual.trim(),
  )
    ? steps.map((step) => ({ ...step }))
    : [];
  if (
    result.value === "passed" &&
    stepResults.some((step) => step.result !== "passed")
  ) {
    message.warning("提交整体通过时，已填写的步骤须全部通过");
    return false;
  }
  const data = {
    selections: [{ source: entry.source, id: entry.associationId }],
    result: result.value,
    description: description.value,
    stepResults,
  };
  const payload = JSON.stringify(data);
  if (payload !== retryPayload) {
    retryPayload = payload;
    retryId = crypto.randomUUID();
  }
  saving.value = true;
  try {
    await planCaseWorkspaceApi.execute(planId.value, {
      requestId: retryId,
      ...data,
    });
    baseline.value = "";
    historyPage.value = 1;
    await Promise.all([loadList(), loadDetail()]);
    message.success("执行结果已提交");
    if (autoNext.value) {
      let next = nextFunctionalEntry(listing.value?.items || [], entry.id);
      while (
        !next &&
        listing.value &&
        page.value * listSize < listing.value.total
      ) {
        page.value++;
        await loadList();
        next = nextFunctionalEntry(listing.value?.items || [], "");
      }
      saving.value = false;
      if (next) await selectCase(next);
      else message.info("已到当前范围最后一条用例");
    }
    return true;
  } catch (error) {
    console.error("提交功能用例执行结果失败", error);
    message.error("提交失败，请检查活动批次、关联状态及权限");
    return false;
  } finally {
    saving.value = false;
  }
}
watch(
  () => [planId.value, projectId.value],
  () => {
    page.value = functionalListingState(route.query).page;
    historyPage.value = 1;
    void loadContext();
  },
  { immediate: true },
);
watch(selectedKey, () => {
  if (plan.value) {
    historyPage.value = 1;
    void loadDetail();
  }
});
</script>
<style scoped>
.functional-execution {
  background: white;
  min-width: 0;
  padding: 16px;
  min-height: 100%;
}
header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}
header h2 {
  margin: 0;
  font-size: 18px;
  overflow-wrap: anywhere;
}
.execution-layout {
  display: grid;
  grid-template-columns: 318px minmax(0, 1fr);
  gap: 24px;
}
.case-sidebar {
  border-right: 1px solid #e5e6eb;
  padding-right: 16px;
  min-width: 0;
}
.case-sidebar > .ant-select {
  width: 100%;
  margin: 12px 0;
}
.case-sidebar h3 {
  display: flex;
  justify-content: space-between;
}
.case-cards {
  max-height: calc(100vh - 320px);
  min-height: 180px;
  overflow: auto;
  margin-bottom: 16px;
}
.case-card {
  display: flex;
  flex-wrap: wrap;
  text-align: left;
  gap: 8px;
  border: 1px solid #e5e6eb;
  background: white;
  width: 100%;
  padding: 12px;
  margin-bottom: 8px;
  cursor: pointer;
  border-radius: 4px;
}
.case-card strong {
  width: 100%;
  overflow-wrap: anywhere;
}
.case-card.active {
  border-color: #165dff;
  background: #f2f5ff;
}
.execution-detail {
  min-width: 0;
}
.case-heading {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}
.case-heading h3 {
  margin: 0;
  overflow-wrap: anywhere;
}
.execution-step {
  padding: 12px 0;
  border-bottom: 1px solid #e5e6eb;
}
.step-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}
.step-result {
  width: 100%;
  margin-top: 12px;
}
.step-result :deep(.ant-select) {
  width: 150px;
}
.submit-panel {
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid #e5e6eb;
}
.history-record {
  padding: 16px 0;
  border-bottom: 1px solid #e5e6eb;
  overflow-wrap: anywhere;
}
@media (max-width: 900px) {
  .execution-layout {
    grid-template-columns: 1fr;
  }
  .case-sidebar {
    border-right: 0;
    border-bottom: 1px solid #e5e6eb;
    padding: 0 0 16px;
  }
  .case-cards {
    max-height: 250px;
  }
  .step-content {
    grid-template-columns: 1fr;
  }
  .functional-execution {
    padding: 12px;
  }
}
</style>
