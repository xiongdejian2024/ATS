<template>
  <section class="review-page">
    <a-alert v-if="!projectId" message="请选择项目" type="info" />
    <template v-else>
      <div class="review-layout">
        <main v-if="active" class="review-workspace">
          <ReviewDetailHeader
            :review="active"
            :disabled="
              associateSaving || resultSaving || managementSaving || busy
            "
            @back="router.push({ name: 'CaseReviews', query: { projectId } })"
          >
            <template #actions>
              <a-button
                v-if="
                  canManage &&
                  !active.archived &&
                  !['cancelled', 'superseded'].includes(active.status)
                "
                :disabled="
                  associateSaving || resultSaving || managementSaving || busy
                "
                @click="associateOpen = true"
                >关联用例</a-button
              >
              <a-button
                v-if="canManage && !active.archived"
                :disabled="
                  associateSaving || resultSaving || managementSaving || busy
                "
                @click="openEditor(active)"
                >编辑</a-button
              >
              <a-button
                v-if="canManage"
                :disabled="
                  associateSaving || resultSaving || managementSaving || busy
                "
                @click="copyReview"
                >复制</a-button
              >
              <a-button
                :disabled="
                  associateSaving || resultSaving || managementSaving || busy
                "
                @click="follow"
                >{{ followed ? "取消关注" : "关注" }}</a-button
              >
              <a-dropdown :trigger="['click']">
                <a-button
                  :disabled="
                    associateSaving || resultSaving || managementSaving || busy
                  "
                  >更多 <DownOutlined
                /></a-button>
                <template #overlay
                  ><a-menu @click="moreAction">
                    <a-menu-item key="refresh">刷新</a-menu-item>
                    <a-menu-item
                      v-if="canManage && !active.archived"
                      key="resubmit"
                      >新建后续评审</a-menu-item
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
          <ReviewCaseTable
            ref="caseTable"
            :key="`${projectId}:${active.id}`"
            :project-id="projectId"
            :initial-scope="route.query.scope"
            :review-id="active.id"
            :members="members"
            :can-manage="
              canManage &&
              !active.archived &&
              !['cancelled', 'superseded'].includes(active.status)
            "
            @saving="managementSaving = $event"
            @changed="load"
            @selection-summary="selectionSummary = $event"
            :revision="tableRevision"
            :disabled="
              resultSaving || associateSaving || managementSaving || busy
            "
            v-model:selected="selectedItems"
            @select="openReading"
          >
            <template #actions>
              <a-button
                :disabled="
                  !selectionSummary.count ||
                  selectionSummary.loading ||
                  !caseTable?.canReviewSelection() ||
                  resultSaving ||
                  associateSaving ||
                  managementSaving ||
                  busy
                "
                @click="batchVisible = true"
                >批量评审（{{ selectionSummary.count }}）</a-button
              >
            </template>
          </ReviewCaseTable>
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
      :excluded="active.associatedCaseIds || []"
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
} from "@/api/caseGovernance";
import { useProjectStore } from "@/stores/project";
import {
  reviewWorkspaceApi,
  type ReviewSelectionSummary,
} from "@/api/reviewWorkspace";
import ReviewCaseTable from "@/components/CaseReview/ReviewCaseTable.vue";
import ReviewAssociateDrawer from "@/components/CaseReview/ReviewAssociateDrawer.vue";
import ReviewResultForm, {
  type ReviewDecision,
} from "@/components/CaseReview/ReviewResultForm.vue";
const route = useRoute(),
  router = useRouter(),
  projectStore = useProjectStore();
const projectId = ref(""),
  busy = ref(false),
  reviews = ref<CaseReview[]>([]),
  members = ref<{ id: string; name: string }[]>([]);
const activeId = ref<string>(),
  selectedItems = ref<string[]>([]),
  followed = ref(false);
const batchVisible = ref(false);
const selectionSummary = ref<ReviewSelectionSummary>({
  count: 0,
  excludedCount: 0,
  canVote: false,
  canReReview: false,
});
const deleteVisible = ref(false),
  deleteName = ref("");
const canManage = ref(false),
  canDelete = ref(false),
  associateOpen = ref(false),
  associateSaving = ref(false),
  resultSaving = ref(false),
  managementSaving = ref(false);
const active = computed(() =>
  reviews.value.find((r) => r.id === activeId.value),
);
const caseTable = ref<InstanceType<typeof ReviewCaseTable>>(),
  tableRevision = ref(0);
function openReading(id: string) {
  if (
    !activeId.value ||
    resultSaving.value ||
    managementSaving.value ||
    associateSaving.value
  )
    return;
  router.push({
    name: "CaseReviewReading",
    query: {
      projectId: projectId.value,
      reviewId: activeId.value,
      itemId: id,
      scope: JSON.stringify(caseTable.value?.readingScope() || {}),
    },
  });
}
async function run(task: () => Promise<void>) {
  if (associateSaving.value || resultSaving.value || managementSaving.value)
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
    const review = await reviewWorkspaceApi.detail(p, id);
    if (sequence !== loadSequence || p !== projectId.value) return;
    reviews.value = [review];
    activeId.value = review.id;
    ++tableRevision.value;
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
  selectedItems.value = [];
  await router.replace({
    query: { ...route.query, projectId: projectId.value, reviewId: id },
  });
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
    managementSaving.value ||
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
function replace(review: CaseReview, refresh = true) {
  const compact = { ...review, items: [] };
  const index = reviews.value.findIndex((r) => r.id === review.id);
  if (index < 0) reviews.value.unshift(compact);
  else reviews.value[index] = compact;
  if (refresh) ++tableRevision.value;
}
async function batchVote(decision: ReviewDecision, reason: string) {
  const p = projectId.value,
    review = active.value;
  if (
    !review ||
    resultSaving.value ||
    associateSaving.value ||
    managementSaving.value ||
    !selectionSummary.value.count ||
    selectionSummary.value.loading
  )
    throw new Error("当前评审不能批量提交结论");
  const selection = caseTable.value?.selectionRequest(),
    count = selectionSummary.value.count;
  if (!selection) throw new Error("选择范围不存在，请重新选择");
  resultSaving.value = true;
  try {
    const record = await reviewWorkspaceApi.batchVote(p, review.id, {
      ...selection,
      decision,
      comment: reason,
    });
    if (p !== projectId.value || review.id !== activeId.value)
      throw new Error("项目或评审已切换，请重新加载详情");
    replace(record, false);
    caseTable.value?.clearSelection();
    await caseTable.value?.refresh();
    batchVisible.value = false;
    selectedItems.value = [];
    console.info("批量评审结论已保存", {
      projectId: p,
      reviewId: review.id,
      decision,
      count,
    });
    message.success("批量评审已保存");
  } finally {
    resultSaving.value = false;
  }
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
        selectionSummary.value.count
          ? await caseTable.value?.selectedCaseIds()
          : undefined,
      );
      replace(result);
      await selectReview(result.id);
      message.success("已按当前内容创建后续评审");
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
    if (id && id !== projectId.value) {
      if (!canLeaveAssociation()) {
        const previous = projectStore.projects.find(
          (p) => p.id === projectId.value,
        );
        if (previous) projectStore.setCurrentProject(previous);
        return;
      }
      projectId.value = id;
    }
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
