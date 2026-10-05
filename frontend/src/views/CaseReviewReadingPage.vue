<template>
  <section ref="pageElement" class="reading-page">
    <header class="reading-header">
      <a-button aria-label="返回评审详情" :disabled="locked" @click="back"
        ><ArrowLeftOutlined
      /></a-button>
      <strong :title="review?.name">{{ review?.name || "用例审阅" }}</strong>
      <a-tag>{{ review?.mode === "single" ? "单人" : "多人" }}</a-tag>
      <a-space v-if="review?.mode !== 'single'" class="mine-status"
        ><a-switch
          v-model:checked="mineStatus"
          :disabled="locked"
          size="small"
        />我的评审结果</a-space
      >
      <a-button
        class="fullscreen-button"
        aria-label="切换全屏"
        @click="toggleFullscreen"
        ><FullscreenOutlined
      /></a-button>
    </header>
    <a-result
      v-if="contextError"
      status="error"
      title="审阅页面加载失败"
      sub-title="请检查项目、评审和用例访问权限。"
      ><template #extra
        ><a-button @click="initialize">重试</a-button></template
      ></a-result
    >
    <a-spin v-else :spinning="contextLoading">
      <div class="reading-body">
        <aside class="reading-sidebar">
          <div class="sidebar-search">
            <a-input-search
              v-model:value="keyword"
              placeholder="通过 ID/名称/标签搜索"
              allow-clear
              :disabled="locked"
              @search="filterList"
            /><a-select
              v-model:value="selectedStates"
              mode="multiple"
              placeholder="评审结果"
              :disabled="locked || mineStatus"
              :options="reviewStates"
              allow-clear
              @change="filterList"
            />
          </div>
          <a-alert v-if="listError" type="error" message="用例列表加载失败"
            ><template #action><a @click="loadList">重试</a></template></a-alert
          >
          <a-spin :spinning="listLoading"
            ><div class="reading-list">
              <button
                v-for="row in list?.items || []"
                :key="row.id"
                class="reading-case"
                :class="{ active: row.id === itemId }"
                :disabled="locked"
                @click="choose(row.id)"
              >
                <span class="case-first-line"
                  ><span>{{ row.caseCode }}</span
                  ><a-tag
                    :color="
                      reviewStateColor(
                        mineStatus ? row.myStatus : row.reviewState,
                      )
                    "
                    >{{
                      reviewStateName(
                        mineStatus ? row.myStatus : row.reviewState,
                      )
                    }}</a-tag
                  ></span
                ><span class="case-name" :title="row.name">{{ row.name }}</span>
              </button>
              <a-empty
                v-if="list && !list.items.length"
                description="暂无用例"
              /></div
          ></a-spin>
          <a-pagination
            v-model:current="page"
            :total="list?.total || 0"
            :page-size="size"
            simple
            :disabled="locked"
            @change="pageChanged"
          />
        </aside>
        <main class="reading-main">
          <a-result v-if="detailError" status="error" title="用例详情加载失败"
            ><template #extra
              ><a-button @click="loadReading(itemId)">重试</a-button></template
            ></a-result
          >
          <a-spin v-else :spinning="detailLoading">
            <template v-if="record">
              <div class="reading-content">
                <div class="case-summary">
                  <div class="summary-title">
                    <a :title="record.item.snapshot.name" @click="openMainCase"
                      >【{{ record.item.caseCode }}】{{
                        record.item.snapshot.name
                      }}</a
                    ><a-button
                      v-if="canEdit"
                      size="small"
                      :disabled="locked"
                      @click="editOpen = true"
                      >编辑</a-button
                    >
                  </div>
                  <div class="summary-metadata">
                    <span><FolderOutlined /> {{ record.item.moduleName }}</span
                    ><span class="meta-label">用例等级</span
                    ><a-tag>{{ record.item.snapshot.priority }}</a-tag
                    ><span class="meta-label">评审结果</span
                    ><a-popover v-if="review?.mode !== 'single'" trigger="click"
                      ><template #content
                        ><div
                          v-for="id in record.item.reviewerIds"
                          :key="id"
                          class="reviewer-status"
                        >
                          {{ memberName(id) }}
                          <a-tag :color="reviewStateColor(personState(id))">{{
                            reviewStateName(personState(id))
                          }}</a-tag>
                        </div></template
                      ><a-tag :color="reviewStateColor(displayState)"
                        >{{ reviewStateName(displayState) }}
                        <DownOutlined /></a-tag></a-popover
                    ><a-tag v-else :color="reviewStateColor(displayState)">{{
                      reviewStateName(displayState)
                    }}</a-tag>
                  </div>
                </div>
                <a-alert
                  v-if="record.item.outdated"
                  type="warning"
                  show-icon
                  message="当前用例与本次评审快照不同；请确认后重新提审以审阅最新内容。"
                />
                <a-alert
                  v-if="record.item.recycled"
                  type="info"
                  message="主用例已回收，保留评审快照与历史供查阅。"
                />
                <a-tabs v-model:active-key="tab">
                  <a-tab-pane key="basic" tab="基本信息"
                    ><a-descriptions
                      :column="1"
                      :label-style="{ width: '90px' }"
                      ><a-descriptions-item label="所属模块">{{
                        record.item.moduleName
                      }}</a-descriptions-item
                      ><a-descriptions-item
                        v-for="field in record.customFields"
                        :key="field.key"
                        :label="field.name"
                        >{{ fieldValue(field.key) }}</a-descriptions-item
                      ><a-descriptions-item label="创建人">{{
                        record.item.creator || "—"
                      }}</a-descriptions-item
                      ><a-descriptions-item label="创建时间">{{
                        formatTime(record.createdAt)
                      }}</a-descriptions-item></a-descriptions
                    ></a-tab-pane
                  >
                  <a-tab-pane key="detail" tab="详情"
                    ><ReviewSnapshotContent :snapshot="record.item.snapshot" />
                    <h4>附件</h4>
                    <a-list
                      v-if="record.attachments.length"
                      :data-source="record.attachments"
                      ><template #renderItem="{ item }"
                        ><a-list-item
                          ><a
                            :aria-label="`下载 ${item.fileName}`"
                            @click="download(item)"
                            >{{ item.fileName }}</a
                          ><span
                            >{{ item.fileSize || 0 }} 字节</span
                          ></a-list-item
                        ></template
                      ></a-list
                    ><a-empty v-else description="暂无附件"
                  /></a-tab-pane>
                  <a-tab-pane
                    key="requirements"
                    :tab="`需求${record.requirements.length ? `（${record.requirements.length}）` : ''}`"
                    ><div class="requirement-toolbar">
                      <span>当前用例关联的需求</span
                      ><a-input-search
                        v-model:value="requirementKeyword"
                        placeholder="通过 ID/名称搜索"
                        allow-clear
                      />
                    </div>
                    <a-table
                      :columns="requirementColumns"
                      :data-source="visibleRequirements"
                      row-key="id"
                      :pagination="false"
                      :scroll="{ x: 480 }"
                  /></a-tab-pane>
                  <a-tab-pane key="history" tab="评审历史"
                    ><div
                      class="history-item"
                      v-for="event in [...record.history].reverse()"
                      :key="event.id"
                    >
                      <a-avatar><UserOutlined /></a-avatar>
                      <div class="history-content">
                        <div class="history-heading">
                          <strong>{{
                            event.detail?.automatic
                              ? "系统"
                              : memberName(event.actorId)
                          }}</strong
                          ><a-tag
                            :color="
                              reviewStateColor(
                                event.detail?.decision || 're_review',
                              )
                            "
                            >{{
                              event.action === "重新提审"
                                ? event.detail?.automatic
                                  ? "自动重新提审"
                                  : "重新提审"
                                : event.detail?.decision === "suggestion"
                                  ? "建议"
                                  : reviewStateName(event.detail?.decision)
                            }}</a-tag
                          ><a-tag v-if="event.abandoned">已作废</a-tag>
                        </div>
                        <CaseRichText
                          v-if="event.detail?.comment"
                          :model-value="event.detail.comment"
                          readonly
                        /><small>{{ formatTime(event.createdAt) }}</small>
                      </div>
                    </div>
                    <a-empty
                      v-if="!record.history.length"
                      description="暂无评审历史"
                  /></a-tab-pane>
                </a-tabs>
              </div>
              <footer class="reading-footer">
                <div class="footer-heading">
                  <strong>开始评审</strong
                  ><a-space
                    ><a-switch
                      v-model:checked="autoNext"
                      size="small"
                      :disabled="locked" /><span>评审后自动下一条</span
                    ><a-tooltip
                      title="提交后按当前列表顺序跳到下一条；筛选结果变化时继续处理下一条，最后一条保留当前详情。"
                      ><QuestionCircleOutlined /></a-tooltip
                  ></a-space>
                </div>
                <ReviewResultForm
                  v-if="record.item.canVote"
                  :key="`${reviewId}:${itemId}`"
                  :disabled="locked || detailLoading || listLoading"
                  :submit-result="submitVote"
                />
                <a-alert
                  v-else
                  type="info"
                  :message="
                    review?.archived
                      ? '评审已归档，当前内容仅供查阅'
                      : '当前账号未被指定为本条用例的评审人，或评审已关闭'
                  "
                />
              </footer> </template
            ><a-empty v-else-if="!detailLoading" description="请选择用例" />
          </a-spin>
        </main>
      </div>
    </a-spin>
    <a-drawer
      :open="editOpen"
      title="更新用例"
      width="min(1200px, 96vw)"
      :closable="!editorSaving"
      :mask-closable="!editorSaving"
      :keyboard="!editorSaving"
      destroy-on-close
      @close="closeEditor"
      ><TestCaseEdit
        v-if="editOpen && record"
        ref="editor"
        :case-id="record.item.caseId"
        :project-id="projectId"
        @cancel="closeEditor"
        @save="edited"
    /></a-drawer>
  </section>
</template>
<script setup lang="ts">
import { computed, ref, watch, onBeforeUnmount } from "vue";
import {
  useRoute,
  useRouter,
  onBeforeRouteLeave,
  onBeforeRouteUpdate,
} from "vue-router";
import { useFullscreen } from "@vueuse/core";
import { message } from "ant-design-vue";
import {
  ArrowLeftOutlined,
  DownOutlined,
  FolderOutlined,
  FullscreenOutlined,
  QuestionCircleOutlined,
  UserOutlined,
} from "@ant-design/icons-vue";
import dayjs from "dayjs";
import {
  reviewWorkspaceApi,
  type ReviewReading,
  type ReviewCaseListing,
} from "@/api/reviewWorkspace";
import { caseGovernanceApi, type CaseReview } from "@/api/caseGovernance";
import {
  caseFeaturesApi,
  saveCaseBlob,
  type CaseFile,
} from "@/api/caseFeatures";
import CaseRichText from "@/components/TestCase/CaseRichText.vue";
import ReviewResultForm, {
  type ReviewDecision,
} from "@/components/CaseReview/ReviewResultForm.vue";
import ReviewSnapshotContent from "@/components/CaseReview/ReviewSnapshotContent.vue";
import TestCaseEdit from "@/components/TestCase/TestCaseEdit.vue";
import {
  readingScope,
  afterReviewTarget,
  reviewStates,
  reviewStateName,
  reviewStateColor,
} from "@/components/CaseReview/reviewReading";
const route = useRoute(),
  router = useRouter();
const projectId = computed(() => String(route.query.projectId || "")),
  reviewId = computed(() => String(route.query.reviewId || ""));
const scope = ref(readingScope(route.query.scope)),
  page = ref(scope.value.page),
  size = ref(scope.value.size),
  keyword = ref(scope.value.search || ""),
  selectedStates = ref<string[]>(
    scope.value.states || (scope.value.state ? [scope.value.state] : []),
  );
const itemId = ref(""),
  record = ref<ReviewReading>(),
  review = ref<CaseReview>(),
  list = ref<ReviewCaseListing>(),
  members = ref<{ id: string; name: string }[]>([]),
  canManage = ref(false);
const contextLoading = ref(false),
  contextError = ref(false),
  listLoading = ref(false),
  listError = ref(false),
  detailLoading = ref(false),
  detailError = ref(false),
  saving = ref(false),
  autoNext = ref(false),
  mineStatus = ref(false),
  tab = ref("detail"),
  requirementKeyword = ref(""),
  editOpen = ref(false);
const editor = ref<InstanceType<typeof TestCaseEdit>>(),
  editorSaving = computed(() => !!editor.value?.isSaving()),
  locked = computed(() => saving.value || editorSaving.value),
  canEdit = computed(
    () =>
      canManage.value &&
      !review.value?.archived &&
      !["cancelled", "superseded"].includes(review.value?.status || "") &&
      !record.value?.item.recycled,
  );
const pageElement = ref<HTMLElement>(),
  { toggle: toggleFullscreen } = useFullscreen(pageElement);
const displayState = computed(() =>
  mineStatus.value
    ? record.value?.item.myStatus || "un_review"
    : record.value?.item.reviewState || "un_review",
);
const visibleRequirements = computed(
  () =>
    record.value?.requirements.filter((r) =>
      (r.id + " " + r.title)
        .toLowerCase()
        .includes(requirementKeyword.value.toLowerCase()),
    ) || [],
);
const requirementColumns = [
  { title: "ID", dataIndex: "id", width: 160 },
  { title: "需求名称", dataIndex: "title" },
  { title: "状态", dataIndex: "status", width: 100 },
];
const memberName = (id: string) =>
  members.value.find((m) => m.id === id)?.name || id;
const formatTime = (value: string | null) =>
  value ? dayjs(value).format("YYYY-MM-DD HH:mm:ss") : "—";
function fieldValue(key: string) {
  const value = record.value?.item.snapshot.custom_fields?.[key];
  return Array.isArray(value)
    ? value.join("、")
    : typeof value === "boolean"
      ? value
        ? "是"
        : "否"
      : (value ?? "—");
}
function personState(id: string) {
  const events =
      record.value?.history.filter(
        (e) => e.actorId === id && !e.abandoned && !e.detail?.automatic,
      ) || [],
    event = events[events.length - 1];
  return event?.action === "重新提审"
    ? "re_review"
    : (
        {
          approved: "approved",
          rejected: "rejected",
          suggestion: "under_review",
        } as Record<string, string>
      )[event?.detail?.decision] || "un_review";
}
let contextSequence = 0,
  listSequence = 0,
  detailSequence = 0;
async function loadList(): Promise<ReviewCaseListing | undefined> {
  const seq = ++listSequence,
    p = projectId.value,
    r = reviewId.value;
  listLoading.value = true;
  listError.value = false;
  try {
    const data = await reviewWorkspaceApi.items(p, r, {
      ...scope.value,
      page: page.value,
      size: size.value,
      search: keyword.value,
      state: undefined,
      states: selectedStates.value.join(","),
    });
    if (seq !== listSequence || p !== projectId.value || r !== reviewId.value)
      return;
    if (page.value > 1 && (page.value - 1) * size.value >= data.total) {
      page.value = Math.max(1, Math.ceil(data.total / size.value));
      return await loadList();
    }
    list.value = data;
    return data;
  } catch (error) {
    console.error("加载独立审阅列表失败", error);
    if (seq === listSequence) {
      listError.value = true;
      list.value = undefined;
    }
  } finally {
    if (seq === listSequence) listLoading.value = false;
  }
}
async function loadReading(id: string) {
  const seq = ++detailSequence,
    p = projectId.value,
    r = reviewId.value;
  itemId.value = id;
  record.value = undefined;
  detailError.value = false;
  detailLoading.value = true;
  try {
    const data = await reviewWorkspaceApi.reading(p, r, id);
    if (
      seq === detailSequence &&
      p === projectId.value &&
      r === reviewId.value
    ) {
      record.value = data;
      review.value = data.review;
    }
  } catch (error) {
    console.error("加载独立审阅详情失败", error);
    if (seq === detailSequence) detailError.value = true;
  } finally {
    if (seq === detailSequence) detailLoading.value = false;
  }
}
let navigationTarget = "";
async function choose(id: string, internal = false) {
  if ((locked.value && !internal) || !id) return;
  navigationTarget = id;
  try {
    await router.replace({
      name: "CaseReviewReading",
      query: {
        ...route.query,
        itemId: id,
        scope: JSON.stringify({
          ...scope.value,
          page: page.value,
          size: size.value,
          search: keyword.value,
          state: undefined,
          states: selectedStates.value,
        }),
      },
    });
  } finally {
    navigationTarget = "";
  }
  await loadReading(id);
}
async function initialize() {
  const seq = ++contextSequence,
    p = projectId.value,
    r = reviewId.value;
  ++listSequence;
  ++detailSequence;
  record.value = undefined;
  list.value = undefined;
  review.value = undefined;
  contextError.value = false;
  contextLoading.value = true;
  itemId.value = "";
  canManage.value = false;
  members.value = [];
  editOpen.value = false;
  scope.value = readingScope(route.query.scope);
  page.value = scope.value.page;
  size.value = scope.value.size;
  keyword.value = scope.value.search || "";
  selectedStates.value =
    scope.value.states || (scope.value.state ? [scope.value.state] : []);
  try {
    if (!p || !r) throw new Error("缺少项目或评审标识");
    const [header, people, permissions] = await Promise.all([
      reviewWorkspaceApi.detail(p, r),
      caseGovernanceApi.reviewers(p),
      reviewWorkspaceApi.list(p, { size: 1 }),
    ]);
    if (seq !== contextSequence) return;
    review.value = header;
    members.value = people;
    canManage.value = permissions.permissions.update;
    const loaded = await loadList();
    if (seq !== contextSequence) return;
    const id =
      typeof route.query.itemId === "string"
        ? route.query.itemId
        : loaded?.items[0]?.id;
    if (id) await loadReading(id);
  } catch (error) {
    console.error("加载独立审阅上下文失败", error);
    if (seq === contextSequence) contextError.value = true;
  } finally {
    if (seq === contextSequence) contextLoading.value = false;
  }
}
async function filterList() {
  if (locked.value) return;
  page.value = 1;
  await loadList();
  if (list.value && !list.value.items.some((i) => i.id === itemId.value)) {
    if (list.value.items[0]) await choose(list.value.items[0].id);
    else {
      ++detailSequence;
      record.value = undefined;
      itemId.value = "";
    }
  }
}
async function pageChanged() {
  if (locked.value) return;
  await loadList();
  if (list.value?.items[0]) await choose(list.value.items[0].id);
}
async function submitVote(decision: ReviewDecision, reason: string) {
  if (locked.value || !record.value?.item.canVote)
    throw new Error("当前用例不能提交评审");
  const previous = (list.value?.items || []).map((i) => i.id),
    id = itemId.value,
    p = projectId.value,
    r = reviewId.value;
  saving.value = true;
  try {
    try {
      await caseGovernanceApi.vote(p, r, id, decision, reason);
    } catch (error) {
      console.error("独立审阅结论保存失败", error);
      throw error;
    }
    console.info("独立审阅结论已保存", {
      projectId: p,
      reviewId: r,
      itemId: id,
      decision,
    });
    message.success("评审结论已记录");
    await loadList();
    if (listError.value) {
      await loadReading(id);
      return;
    }
    const current = (list.value?.items || []).map((i) => i.id);
    let target: string | undefined = afterReviewTarget(
      previous,
      id,
      current,
      autoNext.value,
    );
    if (
      autoNext.value &&
      target === id &&
      current.at(-1) === id &&
      page.value * size.value < (list.value?.total || 0)
    ) {
      page.value++;
      await loadList();
      if (!listError.value) target = list.value?.items[0]?.id;
    }
    if (target) await choose(target, true);
    else {
      record.value = undefined;
      itemId.value = "";
    }
  } finally {
    saving.value = false;
  }
}

function closeEditor() {
  if (!editorSaving.value) editOpen.value = false;
}
async function edited() {
  editOpen.value = false;
  await loadList();
  await loadReading(itemId.value);
}
async function download(file: CaseFile) {
  try {
    saveCaseBlob(
      await caseFeaturesApi.download(projectId.value, file.id),
      file.fileName,
    );
  } catch (error) {
    console.error("下载审阅用例附件失败", error);
    message.error("附件下载失败，请重试");
  }
}
function openMainCase() {
  if (record.value)
    window.open(
      router.resolve({
        name: "TestCases",
        query: { projectId: projectId.value, caseId: record.value.item.caseId },
      }).href,
      "_blank",
      "noopener",
    );
}
function back() {
  router.push({
    name: "CaseReviewWorkspace",
    query: {
      projectId: projectId.value,
      reviewId: reviewId.value,
      scope: JSON.stringify({
        ...scope.value,
        page: page.value,
        size: size.value,
        search: keyword.value,
        state:
          selectedStates.value.length === 1
            ? selectedStates.value[0]
            : undefined,
      }),
    },
  });
}
function canLeave(to: any) {
  if (
    navigationTarget &&
    to.name === "CaseReviewReading" &&
    to.query.projectId === projectId.value &&
    to.query.reviewId === reviewId.value &&
    to.query.itemId === navigationTarget
  )
    return true;
  if (locked.value) {
    message.info("正在保存，请稍候");
    return false;
  }
  return true;
}
onBeforeRouteLeave(canLeave);
onBeforeRouteUpdate(canLeave);
watch(mineStatus, () => {
  page.value = 1;
  void loadList();
});
watch(() => [projectId.value, reviewId.value], initialize, { immediate: true });
watch(
  () => route.query.itemId,
  (id) => {
    if (
      !navigationTarget &&
      !contextLoading.value &&
      typeof id === "string" &&
      id !== itemId.value
    )
      void loadReading(id);
  },
);
onBeforeUnmount(() => {
  ++contextSequence;
  ++listSequence;
  ++detailSequence;
});
</script>
<style scoped>
.reading-page {
  background: #fff;
  border: 1px solid var(--ms-border);
  border-radius: 4px;
  height: calc(100vh - 112px);
  display: flex;
  flex-direction: column;
  min-height: 600px;
  overflow: hidden;
}
.reading-page:fullscreen {
  height: 100vh;
  min-height: 0;
}
.reading-header {
  height: 56px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border-bottom: 1px solid var(--ms-border);
}
.reading-header strong {
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-weight: 500;
}
.fullscreen-button {
  margin-left: auto;
}
.reading-page > :deep(.ant-spin-nested-loading) {
  flex: 1;
  min-height: 0;
}
.reading-page > :deep(.ant-spin-nested-loading > .ant-spin-container) {
  height: 100%;
}
.reading-body {
  height: 100%;
  display: flex;
  min-height: 0;
}
.reading-sidebar {
  width: 356px;
  flex-shrink: 0;
  border-right: 1px solid var(--ms-border);
  padding: 16px 16px 16px 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.sidebar-search {
  display: flex;
  gap: 8px;
}
.sidebar-search > :deep(.ant-select) {
  width: 112px;
  flex-shrink: 0;
}
.sidebar-search > :deep(.ant-input-group-wrapper) {
  min-width: 0;
}
.reading-sidebar > :deep(.ant-spin-nested-loading) {
  flex: 1;
  min-height: 0;
}
.reading-sidebar > :deep(.ant-spin-nested-loading > .ant-spin-container) {
  height: 100%;
}
.reading-list {
  height: 100%;
  background: var(--ms-page-bg);
  padding: 16px;
  border-radius: 4px;
  overflow-y: auto;
}
.reading-case {
  width: 100%;
  text-align: left;
  background: white;
  border: 1px solid transparent;
  border-radius: 4px;
  padding: 16px;
  cursor: pointer;
  display: block;
}
.reading-case + .reading-case {
  margin-top: 8px;
}
.reading-case.active {
  border-color: var(--primary-color);
  background: var(--ms-primary-soft);
}
.reading-case:disabled {
  cursor: wait;
}
.case-first-line {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}
.case-name {
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.reading-main {
  flex: 1;
  min-width: 0;
  min-height: 0;
  display: flex;
  flex-direction: column;
}
.reading-main > :deep(.ant-spin-nested-loading) {
  height: 100%;
  min-height: 0;
  flex: 1;
}
.reading-main > :deep(.ant-spin-nested-loading > .ant-spin-container) {
  height: 100%;
  display: flex;
  flex-direction: column;
  min-height: 0;
}
.reading-content {
  flex: 1;
  min-height: 0;
  overflow: auto;
  padding: 16px;
}
.case-summary {
  background: var(--ms-page-bg);
  border-radius: 4px;
  padding: 16px;
}
.summary-title {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 12px;
}
.summary-title > a {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-weight: 500;
}
.summary-metadata {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  align-items: center;
}
.meta-label {
  color: var(--ms-text-secondary);
}
.requirement-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}
.requirement-toolbar > :deep(.ant-input-group-wrapper) {
  width: 300px;
  max-width: 60%;
}
.reading-footer {
  padding: 16px;
  box-shadow: 0 -1px 4px rgb(31 35 41 / 10%);
  flex-shrink: 0;
}
.footer-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}
.reading-footer:deep(.review-result-form) {
  margin-top: 12px;
}
.history-item {
  display: flex;
  gap: 12px;
  padding: 16px 0;
  border-bottom: 1px solid var(--ms-border);
}
.history-content {
  flex: 1;
  min-width: 0;
}
.history-heading {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}
.history-heading strong {
  flex: 1;
}
.history-content small {
  color: var(--ms-text-secondary);
  display: block;
  margin-top: 8px;
}
.reviewer-status {
  padding: 4px 0;
}
@media (max-width: 1100px) {
  .reading-sidebar {
    width: 280px;
    padding: 16px;
  }
  .sidebar-search {
    flex-wrap: wrap;
  }
  .sidebar-search > :deep(.ant-select) {
    width: 100%;
  }
  .mine-status {
    font-size: 12px;
  }
}
@media (max-width: 700px) {
  .reading-page {
    height: auto;
    min-height: 0;
    overflow: visible;
  }
  .reading-header {
    padding: 12px;
    flex-wrap: wrap;
    height: auto;
  }
  .reading-header strong {
    max-width: 150px;
  }
  .reading-body {
    display: block;
  }
  .reading-sidebar {
    width: 100%;
    border-right: 0;
    border-bottom: 1px solid var(--ms-border);
  }
  .reading-sidebar > :deep(.ant-spin-nested-loading) {
    height: 220px;
    flex: auto;
  }
  .reading-content {
    overflow: visible;
  }
  .footer-heading {
    flex-wrap: wrap;
  }
  .reading-main {
    min-height: 400px;
  }
  .sidebar-search {
    flex-wrap: nowrap;
  }
  .sidebar-search > :deep(.ant-select) {
    width: 130px;
  }
  .reading-list {
    height: 220px;
  }
}
</style>
