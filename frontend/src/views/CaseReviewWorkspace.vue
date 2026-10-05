<template>
  <section class="review-page">
    <a-alert v-if="!projectId" message="请选择项目" type="info" />
    <template v-else>
      <div class="review-layout">
        <main v-if="active" class="review-workspace">
          <ReviewDetailHeader
            :review="active"
            :disabled="associateSaving || resultSaving || busy"
            @back="router.push({ name: 'CaseReviews', query: { projectId } })"
          >
            <template #actions>
              <a-button
                v-if="
                  canManage &&
                  !active.archived &&
                  !['cancelled', 'superseded'].includes(active.status)
                "
                :disabled="associateSaving || resultSaving || busy"
                @click="associateOpen = true"
                >关联用例</a-button
              >
              <a-button
                v-if="canManage && !active.archived"
                :disabled="associateSaving || resultSaving || busy"
                @click="openEditor(active)"
                >编辑</a-button
              >
              <a-button
                v-if="canManage"
                :disabled="associateSaving || resultSaving || busy"
                @click="copyReview"
                >复制</a-button
              >
              <a-button
                :disabled="associateSaving || resultSaving || busy"
                @click="follow"
                >{{ followed ? "取消关注" : "关注" }}</a-button
              >
              <a-dropdown :trigger="['click']">
                <a-button :disabled="associateSaving || resultSaving || busy"
                  >更多 <DownOutlined
                /></a-button>
                <template #overlay
                  ><a-menu @click="moreAction">
                    <a-menu-item key="refresh">刷新</a-menu-item>
                    <a-menu-item
                      v-if="canManage && !active.archived"
                      key="resubmit"
                      >重新提审</a-menu-item
                    >
                    <a-menu-item
                      v-if="
                        canManage &&
                        !active.archived &&
                        active.status === 'pending'
                      "
                      key="cancel"
                      danger
                      >取消评审</a-menu-item
                    >
                    <a-menu-divider v-if="canDelete" />
                    <a-menu-item v-if="canDelete" key="delete" danger
                      >删除</a-menu-item
                    >
                  </a-menu></template
                >
              </a-dropdown>
            </template>
          </ReviewDetailHeader>
          <a-space wrap style="margin: 16px 0"
            ><a-radio-group v-model:value="layout"
              ><a-radio-button value="list">列表</a-radio-button
              ><a-radio-button value="mind">脑图</a-radio-button></a-radio-group
            ><a-checkbox v-model:checked="autoNext">评审后自动下一条</a-checkbox
            ><a-button
              :disabled="
                !selectedItems.length || resultSaving || associateSaving
              "
              @click="batchVisible = true"
              >批量评审（{{ selectedItems.length }}）</a-button
            ></a-space
          >
          <CaseMindMap
            v-if="layout === 'mind'"
            :cases="mindCases"
            readonly
            @select="selectCase"
          />
          <a-table
            v-else
            :columns="itemColumns"
            :data-source="active.items"
            row-key="id"
            :pagination="{ pageSize: 20 }"
            :row-selection="{
              selectedRowKeys: selectedItems,
              getCheckboxProps: (item: ReviewItem) => ({
                disabled: !canVote(item),
              }),
              onChange: (keys: any) => (selectedItems = keys),
            }"
            :scroll="{ x: 650 }"
          >
            <template #bodyCell="{ column, record }"
              ><a
                v-if="column.key === 'name'"
                @click="activeItemId = record.id"
                >{{ record.snapshot.name }}</a
              ><span v-else-if="column.key === 'reviewers'">{{
                (record.reviewerIds || active.reviewerIds)
                  .map(memberName)
                  .join("、")
              }}</span
              ><a-tag
                v-else-if="column.key === 'status'"
                :color="statusColor(record.status)"
                >{{ statusName(record.status)
                }}{{ record.outdated ? " · 内容已变化" : "" }}</a-tag
              ><a-button
                v-else-if="column.key === 'actions'"
                @click="activeItemId = record.id"
                >评审</a-button
              ></template
            >
          </a-table>
          <a-card
            v-if="activeItem"
            class="item-card"
            :title="`${activeItem.snapshot.name} · v${activeItem.version}`"
          >
            <template #extra
              ><a-space
                ><a-button @click="previousItem">上一条</a-button
                ><a-button @click="nextItem">下一条</a-button
                ><a-button
                  v-if="canManage && !active.archived"
                  :disabled="associateSaving || resultSaving"
                  @click="
                    editCaseId = activeItem.caseId;
                    caseEditorVisible = true;
                  "
                  >编辑用例</a-button
                ></a-space
              ></template
            >
            <a-alert
              v-if="activeItem.outdated"
              message="当前用例与本次评审快照不同；请确认后重新提审以审阅最新内容。"
              type="warning"
              show-icon
            />
            <p class="text">
              <strong>前置条件：</strong
              >{{ activeItem.snapshot.precondition || "无" }}
            </p>
            <a-table
              :columns="stepColumns"
              :data-source="activeItem.snapshot.steps || []"
              :pagination="false"
              size="small"
              ><template #bodyCell="{ column, record }"
                ><span class="text">{{
                  record[column.dataIndex]
                }}</span></template
              ></a-table
            >
            <a-list :data-source="activeItem.decisions"
              ><template #renderItem="{ item }"
                ><a-list-item
                  >{{ memberName(item.reviewerId) }} ·
                  {{ statusName(item.decision) }} · {{ item.updatedAt }}
                  <CaseRichText
                    v-if="item.comment"
                    :model-value="item.comment"
                    readonly
                    class="decision-reason"
                  /> </a-list-item></template
            ></a-list>
            <template v-if="canVote(activeItem)">
              <ReviewResultForm
                :key="`${active.id}:${activeItem.id}`"
                :disabled="associateSaving"
                :submit-result="vote"
              /> </template
            ><a-alert
              v-else
              message="当前账号未被指定为本条用例的评审人，或评审已取消。"
              type="info"
            />
          </a-card>
          <a-tabs
            ><a-tab-pane key="discussion" tab="评审讨论"
              ><a-list :data-source="active.comments"
                ><template #renderItem="{ item }"
                  ><a-list-item
                    ><span class="text"
                      >{{ memberName(item.authorId) }}：{{ item.content }}</span
                    ></a-list-item
                  ></template
                ></a-list
              ><a-textarea
                v-if="!active.archived"
                v-model:value="discussion"
                :rows="2"
                placeholder="整单讨论意见"
              /><a-button
                v-if="!active.archived"
                style="margin-top: 12px"
                :loading="busy"
                @click="comment"
                >发表评论</a-button
              ></a-tab-pane
            ><a-tab-pane key="history" tab="历史记录"
              ><a-empty
                v-if="!active.history?.length"
                description="暂无历史记录" /><a-timeline v-else
                ><a-timeline-item v-for="(entry, i) in active.history" :key="i">
                  <pre class="text">{{
                    entry.action === "评审结论"
                      ? `${entry.createdAt || ""} · ${memberName(entry.actorId || "")} · ${statusName(entry.detail?.decision || "")}`
                      : historyText(entry)
                  }}</pre>
                  <CaseRichText
                    v-if="entry.action === '评审结论' && entry.detail?.comment"
                    :model-value="entry.detail.comment"
                    readonly
                  /> </a-timeline-item></a-timeline></a-tab-pane
          ></a-tabs>
        </main>
        <a-empty
          v-else
          class="empty-workspace"
          description="选择评审单或新建评审"
        />
      </div>
    </template>
    <ReviewAssociateDrawer
      v-if="active"
      :open="associateOpen"
      :project-id="projectId"
      :excluded="active.items.map((item) => item.caseId)"
      :default-reviewers="active.reviewerIds"
      :members="members"
      :save-selection="associateCases"
      @update:open="associateOpen = $event"
    />
    <a-modal
      v-model:open="batchVisible"
      title="批量评审"
      :width="680"
      :footer="null"
      :closable="!resultSaving"
      :mask-closable="!resultSaving"
      :keyboard="!resultSaving"
      destroy-on-close
    >
      <a-alert
        message="只允许提交你有评审权限的条目；包含无权限条目时整批拒绝。"
        type="info"
      />
      <ReviewResultForm
        v-if="batchVisible"
        inline-reason
        :disabled="associateSaving || resultSaving"
        :submit-result="batchVote"
      />
    </a-modal>
    <a-modal
      v-model:open="deleteVisible"
      title="删除评审"
      :closable="!busy"
      :mask-closable="!busy"
      :keyboard="!busy"
      :cancel-button-props="{ disabled: busy }"
      :confirm-loading="busy"
      :ok-button-props="{ danger: true, disabled: deleteName !== active?.name }"
      @ok="deleteReview"
    >
      <a-alert
        type="warning"
        message="删除评审会同时删除其关联及评审记录，请输入完整评审名称确认。"
      />
      <p>{{ active?.name }}</p>
      <a-input
        v-model:value="deleteName"
        placeholder="请输入评审名称"
        :disabled="busy"
      />
    </a-modal>
    <a-drawer
      v-model:open="caseEditorVisible"
      title="编辑用例"
      width="min(1000px, 96vw)"
      destroy-on-close
      ><TestCaseEdit
        v-if="caseEditorVisible"
        :case-id="editCaseId"
        :project-id="projectId"
        @cancel="caseEditorVisible = false"
        @save="
          caseEditorVisible = false;
          load();
        "
    /></a-drawer>
  </section>
</template>
<script setup lang="ts">
import { ref, computed, watch, onMounted } from "vue";
import {
  useRoute,
  useRouter,
  onBeforeRouteLeave,
  onBeforeRouteUpdate,
} from "vue-router";
import { message, Modal } from "ant-design-vue";
import { DownOutlined } from "@ant-design/icons-vue";
import ReviewDetailHeader from "@/components/CaseReview/ReviewDetailHeader.vue";
import {
  caseGovernanceApi as api,
  type CaseReview,
  type ReviewItem,
} from "@/api/caseGovernance";
import { useProjectStore } from "@/stores/project";
import { useUserStore } from "@/stores/user";
import type { TestCase } from "@/types";
import { reviewWorkspaceApi } from "@/api/reviewWorkspace";
import CaseMindMap from "@/components/TestCase/CaseMindMap.vue";
import ReviewAssociateDrawer from "@/components/CaseReview/ReviewAssociateDrawer.vue";
import CaseRichText from "@/components/TestCase/CaseRichText.vue";
import ReviewResultForm, {
  type ReviewDecision,
} from "@/components/CaseReview/ReviewResultForm.vue";
import TestCaseEdit from "@/components/TestCase/TestCaseEdit.vue";
const route = useRoute(),
  router = useRouter(),
  projectStore = useProjectStore(),
  user = useUserStore();
const projectId = ref(""),
  busy = ref(false),
  reviews = ref<CaseReview[]>([]),
  members = ref<{ id: string; name: string }[]>([]);
const activeId = ref<string>(),
  activeItemId = ref<string>(),
  selectedItems = ref<string[]>([]),
  layout = ref("list"),
  autoNext = ref(true),
  discussion = ref(""),
  followed = ref(false);
const batchVisible = ref(false),
  caseEditorVisible = ref(false),
  editCaseId = ref("");
const deleteVisible = ref(false),
  deleteName = ref("");
const canManage = ref(false),
  canDelete = ref(false),
  associateOpen = ref(false),
  associateSaving = ref(false),
  resultSaving = ref(false);
const active = computed(() =>
    reviews.value.find((r) => r.id === activeId.value),
  ),
  activeItem = computed(() =>
    active.value?.items.find((i) => i.id === activeItemId.value),
  );
const mindCases = computed(
  () =>
    (active.value?.items.map((i) => ({
      ...i.snapshot,
      id: i.caseId,
      caseCode: i.snapshot.case_code,
      moduleId: i.snapshot.module_id,
      status:
        i.status === "approved"
          ? "passed"
          : i.status === "rejected"
            ? "failed"
            : "not_executed",
    })) as Partial<TestCase>[]) || [],
);
const itemColumns = [
  { title: "用例", key: "name" },
  { title: "评审人", key: "reviewers" },
  { title: "状态", key: "status" },
  { title: "操作", key: "actions", width: 90 },
];
const stepColumns = [
  { title: "序号", dataIndex: "step", width: 65 },
  { title: "操作", dataIndex: "action" },
  { title: "预期结果", dataIndex: "expected" },
];
const statusName = (s: string) =>
  ({
    pending: "待评审",
    approved: "通过",
    rejected: "不通过",
    suggestion: "建议",
    cancelled: "已取消",
    superseded: "已重新提审",
  })[s] || s;
const statusColor = (s: string) =>
  ({ approved: "green", rejected: "red", cancelled: "default" })[s] || "blue";
const memberName = (id: string) =>
  members.value.find((m) => m.id === id)?.name || id;
const canVote = (item: ReviewItem) =>
  !!active.value &&
  !active.value.archived &&
  !["cancelled", "superseded"].includes(active.value.status) &&
  (item.reviewerIds || active.value?.reviewerIds || []).includes(
    String(user.user?.id),
  );
function historyText(entry: Record<string, any>) {
  const details = entry.detail || {};
  return `${entry.createdAt || ""} · ${memberName(entry.actorId || "")} · ${entry.action || ""}\n${details.decision ? `${statusName(details.decision)}：${details.comment || ""}` : JSON.stringify(details, null, 2)}`;
}
async function run(task: () => Promise<void>) {
  if (associateSaving.value || resultSaving.value)
    return void message.info("正在保存评审，请稍候");
  busy.value = true;
  try {
    await task();
  } catch (error) {
    console.error("评审操作失败", error);
  } finally {
    busy.value = false;
  }
}
let loadSequence = 0;
async function load() {
  const p = projectId.value,
    id = String(route.query.reviewId || activeId.value || ""),
    sequence = ++loadSequence;
  if (!p || !id) return;
  busy.value = true;
  try {
    const review = await api.review(p, id);
    if (sequence !== loadSequence || p !== projectId.value) return;
    reviews.value = [review];
    activeId.value = review.id;
    if (!review.items.some((i) => i.id === activeItemId.value))
      activeItemId.value = review.items[0]?.id;
  } catch (error) {
    console.error("加载评审详情失败", error);
  } finally {
    if (sequence === loadSequence) busy.value = false;
  }
}
async function loadOptions() {
  const p = projectId.value;
  const result = await Promise.all([
    api.reviewers(p),
    reviewWorkspaceApi.list(p, { size: 1 }),
  ]);
  if (p === projectId.value) {
    members.value = result[0];
    canManage.value = result[1].permissions.update;
    canDelete.value = result[1].permissions.delete;
  }
}
async function selectReview(id: string) {
  activeId.value = id;
  activeItemId.value = active.value?.items[0]?.id;
  selectedItems.value = [];
  await router.replace({ query: { projectId: projectId.value, reviewId: id } });
}
async function associateCases(data: {
  caseIds: string[];
  reviewerIds: string[];
}) {
  const p = projectId.value,
    id = activeId.value;
  if (
    !id ||
    !canManage.value ||
    active.value?.archived ||
    associateSaving.value ||
    resultSaving.value
  )
    throw new Error("当前评审不能追加关联");
  associateSaving.value = true;
  try {
    const record = await reviewWorkspaceApi.associate(p, id, data);
    if (p !== projectId.value || id !== activeId.value)
      throw new Error("项目或评审已切换，请重新打开详情");
    replace(record);
    if (!activeItemId.value) activeItemId.value = record.items[0]?.id;
    console.info("已向评审追加用例，已有结论与人员保留", {
      projectId: p,
      reviewId: id,
      count: data.caseIds.length,
    });
    message.success("用例已关联");
  } finally {
    associateSaving.value = false;
  }
}
function canLeaveAssociation() {
  if (
    associateSaving.value ||
    resultSaving.value ||
    (deleteVisible.value && busy.value)
  ) {
    message.info("正在保存评审，请稍候");
    return false;
  }
  return true;
}
onBeforeRouteLeave(canLeaveAssociation);
onBeforeRouteUpdate(canLeaveAssociation);
async function openEditor(review?: CaseReview) {
  if (!canManage.value) return;
  await router.push({
    name: "CaseReviewEditor",
    query: {
      projectId: projectId.value,
      ...(review ? { reviewId: review.id, returnTo: "detail" } : {}),
    },
  });
}
function replace(review: CaseReview) {
  const index = reviews.value.findIndex((r) => r.id === review.id);
  if (index < 0) reviews.value.unshift(review);
  else reviews.value[index] = review;
}
function nextItem() {
  const items = active.value?.items || [];
  const index = items.findIndex((i) => i.id === activeItemId.value);
  activeItemId.value = items[(index + 1) % items.length]?.id;
}
function previousItem() {
  const items = active.value?.items || [];
  const index = items.findIndex((i) => i.id === activeItemId.value);
  activeItemId.value = items[(index - 1 + items.length) % items.length]?.id;
}
function selectCase(c: Partial<TestCase>) {
  activeItemId.value = active.value?.items.find((i) => i.caseId === c.id)?.id;
}
async function saveResult(
  decision: ReviewDecision,
  reason: string,
  batch = false,
) {
  const p = projectId.value,
    review = active.value,
    item = activeItem.value;
  if (
    !review ||
    (!batch && (!item || !canVote(item))) ||
    resultSaving.value ||
    associateSaving.value
  )
    throw new Error("当前评审不能提交结论");
  const identifiers = [...selectedItems.value];
  if (batch && !identifiers.length) throw new Error("请先选择评审用例");
  resultSaving.value = true;
  try {
    const record = batch
      ? await api.batchVote(p, review.id, identifiers, decision, reason)
      : await api.vote(p, review.id, item!.id, decision, reason);
    if (p !== projectId.value || review.id !== activeId.value)
      throw new Error("项目或评审已切换，请重新加载详情");
    replace(record);
    if (batch) {
      batchVisible.value = false;
      selectedItems.value = [];
    } else if (autoNext.value && item!.id === activeItemId.value) nextItem();
    console.info("评审结论已保存", {
      projectId: p,
      reviewId: review.id,
      decision,
      count: batch ? identifiers.length : 1,
    });
    message.success(batch ? "批量评审已保存" : "评审结论已记录");
  } finally {
    resultSaving.value = false;
  }
}
async function vote(decision: ReviewDecision, reason: string) {
  await saveResult(decision, reason);
}
async function batchVote(decision: ReviewDecision, reason: string) {
  await saveResult(decision, reason, true);
}
async function comment() {
  if (!active.value || !discussion.value.trim()) return;
  await run(async () => {
    replace(
      await api.comment(
        projectId.value,
        active.value!.id,
        discussion.value.trim(),
      ),
    );
    discussion.value = "";
  });
}
async function follow() {
  if (active.value)
    await run(async () => {
      await api.followReview(
        projectId.value,
        active.value!.id,
        !followed.value,
      );
      followed.value = !followed.value;
    });
}
async function moreAction({ key }: { key: string | number }) {
  if (key === "refresh") await load();
  if (key === "resubmit") await resubmit();
  if (key === "cancel")
    Modal.confirm({
      title: "取消整张评审单？",
      okText: "确认",
      cancelText: "取消",
      onOk: cancel,
    });
  if (key === "delete" && canDelete.value) {
    deleteName.value = "";
    deleteVisible.value = true;
  }
}
async function deleteReview() {
  const review = active.value,
    p = projectId.value;
  if (!review || !canDelete.value || deleteName.value !== review.name) return;
  await run(async () => {
    await reviewWorkspaceApi.delete(p, review.id, deleteName.value);
    console.info("评审已删除", { projectId: p, reviewId: review.id });
    deleteVisible.value = false;
    message.success("评审已删除");
    await router.replace({ name: "CaseReviews", query: { projectId: p } });
  });
}
async function cancel() {
  if (active.value)
    await run(async () =>
      replace(await api.cancel(projectId.value, active.value!.id)),
    );
}
async function copyReview() {
  if (active.value && canManage.value)
    await router.push({
      name: "CaseReviewEditor",
      query: { projectId: projectId.value, copyFrom: active.value.id },
    });
}
async function resubmit() {
  if (active.value)
    await run(async () => {
      const result = await api.resubmit(
        projectId.value,
        active.value!.id,
        selectedItems.value.length
          ? active
              .value!.items.filter((i) => selectedItems.value.includes(i.id))
              .map((i) => i.caseId)
          : undefined,
      );
      replace(result);
      await selectReview(result.id);
      message.success("已按当前用例内容重新提审");
    });
}
let followSequence = 0;
watch(activeId, async (id) => {
  const p = projectId.value,
    sequence = ++followSequence;
  followed.value = false;
  if (id)
    try {
      const result = await api.reviewFollowState(p, id);
      if (
        p === projectId.value &&
        id === activeId.value &&
        sequence === followSequence
      )
        followed.value = result.followed;
    } catch (error) {
      console.error("加载评审关注失败", error);
    }
});
watch(
  () => projectStore.currentProject?.id,
  (id) => {
    if (id && id !== projectId.value) projectId.value = id;
  },
);
watch(projectId, async (id) => {
  ++loadSequence;
  canManage.value = false;
  canDelete.value = false;
  deleteVisible.value = false;
  deleteName.value = "";
  associateOpen.value = false;
  activeId.value = undefined;
  reviews.value = [];
  selectedItems.value = [];
  const p = projectStore.projects.find((p) => p.id === id);
  if (p) projectStore.setCurrentProject(p);
  await load();
  await run(loadOptions);
});
onMounted(async () => {
  if (!projectStore.projects.length) await projectStore.fetchProjects();
  projectId.value = String(
    route.query.projectId ||
      projectStore.currentProject?.id ||
      projectStore.projects[0]?.id ||
      "",
  );
  await load();
  if (typeof route.query.reviewId === "string")
    await selectReview(route.query.reviewId);
  if (route.query.create === "1")
    await router.replace({ name: "CaseReviewEditor", query: route.query });
  if (route.query.edit === "1" && active.value) await openEditor(active.value);
});
</script>
<style scoped>
.review-page {
  padding: 24px;
  max-width: 1800px;
  margin: auto;
}
.review-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 20px;
}
.review-workspace {
  min-width: 0;
}
.decision-reason {
  width: 100%;
  margin-top: 8px;
}
.item-card :deep(.ant-list-item) {
  flex-wrap: wrap;
}

.stats b {
  font-size: 20px;
  padding-left: 6px;
}
.item-card {
  margin: 16px 0;
}
.text {
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  max-height: 350px;
  overflow: auto;
}
.empty-workspace {
  align-self: center;
}
@media (max-width: 900px) {
  .review-page {
    padding: 12px;
  }
  .review-header {
    align-items: flex-start;
    flex-direction: column;
  }
  .review-layout {
    grid-template-columns: 1fr;
  }
  .review-list {
    max-height: 240px;
  }
}
</style>
