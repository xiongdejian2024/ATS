<template>
  <section class="review-page">
    <header class="review-header">
      <div>
        <h2>评审详情</h2>
        <p>按锁定版本审阅，记录建议和每次结论变更。</p>
      </div>
      <a-space wrap
        ><a-button
          @click="router.push({ name: 'CaseReviews', query: { projectId } })"
          >返回评审列表</a-button
        ><a-button
          v-if="canManage"
          type="primary"
          :disabled="!projectId"
          @click="openEditor()"
          >新建评审</a-button
        ><a-button @click="load">刷新</a-button></a-space
      >
    </header>
    <a-alert v-if="!projectId" message="请选择项目" type="info" />
    <template v-else>
      <div class="review-layout">
        <main v-if="active" class="review-workspace">
          <a-card :title="active.name">
            <template #extra
              ><a-space wrap
                ><a-button @click="follow">{{
                  followed ? "取消关注" : "关注"
                }}</a-button
                ><a-button v-if="canManage && !active.archived" @click="openEditor(active)">编辑</a-button
                ><a-button v-if="canManage" @click="copyReview">复制</a-button
                ><a-button v-if="canManage && !active.archived" @click="resubmit">重新提审</a-button
                ><a-popconfirm
                  v-if="
                    canManage && !active.archived && active.status === 'pending'
                  "
                  title="取消整张评审单？"
                  @confirm="cancel"
                  ><a-button danger>取消评审</a-button></a-popconfirm
                ></a-space
              ></template
            >
            <p>{{ active.description || "未填写描述" }}</p>
            <a-space wrap
              ><a-tag :color="statusColor(active.status)">{{
                statusName(active.status)
              }}</a-tag
              ><span>{{
                active.mode === "single"
                  ? "单人：最后一次有效结论"
                  : "多人：每位评审人的末次有效结论均通过才通过"
              }}</span
              ><span
                >计划周期：{{ active.startDate || "未设置" }} ～
                {{ active.endDate || "未设置" }}</span
              ></a-space
            >
            <a-alert
              style="margin-top: 12px"
              type="info"
              show-icon
              message="建议不计入通过或不通过结论。允许改投，历史记录保留。计划日期过期后仍可继续评审。"
            />
            <div class="stats">
              <span
                >总数 <b>{{ active.items.length }}</b></span
              ><span
                >通过 <b>{{ count("approved") }}</b></span
              ><span
                >不通过 <b>{{ count("rejected") }}</b></span
              ><span
                >待评审 <b>{{ count("pending") }}</b></span
              ><span
                >内容已变化
                <b>{{ active.items.filter((i) => i.outdated).length }}</b></span
              >
            </div>
          </a-card>
          <a-space wrap style="margin: 16px 0"
            ><a-radio-group v-model:value="layout"
              ><a-radio-button value="list">列表</a-radio-button
              ><a-radio-button value="mind">脑图</a-radio-button></a-radio-group
            ><a-checkbox v-model:checked="autoNext">评审后自动下一条</a-checkbox
            ><a-button
              :disabled="!selectedItems.length"
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
                  {{ statusName(item.decision) }} · {{ item.comment }} ·
                  {{ item.updatedAt }}</a-list-item
                ></template
              ></a-list
            >
            <template v-if="canVote(activeItem)"
              ><a-textarea
                v-model:value="opinion"
                :rows="3"
                placeholder="评审意见（必填）"
                :maxlength="10000"
              /><a-space style="margin-top: 12px"
                ><a-button
                  type="primary"
                  :loading="busy"
                  @click="vote('approved')"
                  >通过 / 改为通过</a-button
                ><a-button danger :loading="busy" @click="vote('rejected')"
                  >不通过 / 改为不通过</a-button
                ><a-button :loading="busy" @click="vote('suggestion')"
                  >仅提建议</a-button
                ></a-space
              ></template
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
                description="暂无历史记录"
              /><a-timeline v-else
                ><a-timeline-item v-for="(entry, i) in active.history" :key="i">
                  <pre class="text">{{ historyText(entry) }}</pre>
                </a-timeline-item></a-timeline
              ></a-tab-pane
            ></a-tabs
          >
        </main>
        <a-empty
          v-else
          class="empty-workspace"
          description="选择评审单或新建评审"
        />
      </div>
    </template>
    <a-modal
      v-model:open="editorVisible"
      :title="editingId ? '编辑评审' : '新建评审'"
      width="min(900px, 96vw)"
      :confirm-loading="busy"
      @ok="saveReview"
    >
      <a-form layout="vertical"
        ><a-form-item label="名称" required
          ><a-input v-model:value="form.name" :maxlength="200" /></a-form-item
        ><a-form-item label="说明"
          ><a-textarea
            v-model:value="form.description"
            :rows="2" /></a-form-item
        ><a-form-item label="评审模式"
          ><a-radio-group v-model:value="form.mode"
            ><a-radio value="single">单人：最后一次有效结论</a-radio
            ><a-radio value="multiple"
              >多人：全部评审人通过</a-radio
            ></a-radio-group
          ></a-form-item
        ><a-row :gutter="12"
          ><a-col :span="12"
            ><a-form-item label="预计开始"
              ><a-date-picker
                v-model:value="form.startDate"
                value-format="YYYY-MM-DD"
                style="width: 100%" /></a-form-item></a-col
          ><a-col :span="12"
            ><a-form-item label="预计结束"
              ><a-date-picker
                v-model:value="form.endDate"
                value-format="YYYY-MM-DD"
                style="width: 100%" /></a-form-item></a-col></a-row
        ><a-form-item label="默认评审人" required
          ><a-select
            v-model:value="form.reviewerIds"
            mode="multiple"
            :options="memberOptions" /></a-form-item
        ><a-form-item label="关联用例" required
          ><a-select
            v-model:value="form.caseIds"
            mode="multiple"
            show-search
            option-filter-prop="label"
            :options="
              cases.map((c) => ({
                label: `${c.caseCode || ''} ${c.name}`,
                value: c.id,
              }))
            "
        /></a-form-item>
        <a-collapse v-if="form.caseIds.length"
          ><a-collapse-panel
            key="members"
            header="逐条指定评审人员（未配置的使用默认人员）"
            ><a-form-item
              v-for="id in form.caseIds"
              :key="id"
              :label="cases.find((c) => c.id === id)?.name || id"
              ><a-select
                v-model:value="form.itemReviewers[id]"
                mode="multiple"
                :options="memberOptions"
                placeholder="默认评审人" /></a-form-item></a-collapse-panel
        ></a-collapse>
      </a-form>
    </a-modal>
    <a-modal
      v-model:open="batchVisible"
      title="批量评审"
      :confirm-loading="busy"
      @ok="batchVote"
      ><a-alert
        message="只允许提交你有评审权限的条目；包含无权限条目时整批拒绝。"
        type="info" /><a-radio-group
        v-model:value="batchDecision"
        style="margin: 16px 0"
        ><a-radio value="approved">通过</a-radio
        ><a-radio value="rejected">不通过</a-radio
        ><a-radio value="suggestion">建议</a-radio></a-radio-group
      ><a-textarea
        v-model:value="batchOpinion"
        placeholder="批量评审意见（必填）"
        :rows="3"
    /></a-modal>
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
import { ref, reactive, computed, watch, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { message } from "ant-design-vue";
import {
  caseGovernanceApi as api,
  type CaseReview,
  type ReviewItem,
} from "@/api/caseGovernance";
import { testCaseApi } from "@/api/testCase";
import { useProjectStore } from "@/stores/project";
import { useUserStore } from "@/stores/user";
import type { TestCase } from "@/types";
import { reviewWorkspaceApi } from "@/api/reviewWorkspace";
import CaseMindMap from "@/components/TestCase/CaseMindMap.vue";
import TestCaseEdit from "@/components/TestCase/TestCaseEdit.vue";
const route = useRoute(),
  router = useRouter(),
  projectStore = useProjectStore(),
  user = useUserStore();
const projectId = ref(""),
  busy = ref(false),
  reviews = ref<CaseReview[]>([]),
  members = ref<{ id: string; name: string }[]>([]),
  cases = ref<TestCase[]>([]);
const activeId = ref<string>(),
  activeItemId = ref<string>(),
  selectedItems = ref<string[]>([]),
  layout = ref("list"),
  autoNext = ref(true),
  opinion = ref(""),
  discussion = ref(""),
  followed = ref(false);
const editorVisible = ref(false),
  editingId = ref<string>(),
  batchVisible = ref(false),
  batchDecision = ref("approved"),
  batchOpinion = ref(""),
  caseEditorVisible = ref(false),
  editCaseId = ref("");
const canManage = ref(false);
const form = reactive({
  moduleId: null as string | null,
  tags: [] as string[],
  name: "",
  description: "",
  mode: "multiple",
  reviewerIds: [] as string[],
  caseIds: [] as string[],
  itemReviewers: {} as Record<string, string[]>,
  startDate: undefined as string | undefined,
  endDate: undefined as string | undefined,
});
const active = computed(() =>
    reviews.value.find((r) => r.id === activeId.value),
  ),
  activeItem = computed(() =>
    active.value?.items.find((i) => i.id === activeItemId.value),
  );
const memberOptions = computed(() =>
  members.value.map((m) => ({ label: m.name, value: m.id })),
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
const count = (s: string) =>
  active.value?.items.filter((i) => i.status === s).length || 0;
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
    testCaseApi.getTestCases(p, { size: 10000 }).then((r) => r.items),
    reviewWorkspaceApi.list(p, { size: 1 }),
  ]);
  if (p === projectId.value) {
    members.value = result[0];
    cases.value = result[1];
    canManage.value = result[2].permissions.update;
  }
}
async function selectReview(id: string) {
  activeId.value = id;
  activeItemId.value = active.value?.items[0]?.id;
  selectedItems.value = [];
  opinion.value = "";
  await router.replace({ query: { projectId: projectId.value, reviewId: id } });
}
async function openEditor(review?: CaseReview) {
  await run(async () => {
    const p = projectId.value;
    await loadOptions();
    if (p !== projectId.value) return;
    if (!canManage.value) return void message.warning("没有评审编辑权限");
    editingId.value = review?.id;
    Object.assign(form, {
      name: review?.name || "",
      moduleId:
        review?.moduleId ||
        (typeof route.query.moduleId === "string" &&
        route.query.moduleId !== "default"
          ? route.query.moduleId
          : null),
      tags: [...(review?.tags || [])],
      description: review?.description || "",
      mode: review?.mode || "multiple",
      reviewerIds: [...(review?.reviewerIds || [String(user.user?.id)])],
      caseIds:
        review?.items.map((i) => i.caseId) ||
        (typeof route.query.caseIds === "string"
          ? route.query.caseIds.split(",")
          : []),
      itemReviewers: Object.fromEntries(
        (review?.items || []).map((i) => [
          i.caseId,
          [...(i.reviewerIds || [])],
        ]),
      ),
      startDate: review?.startDate || undefined,
      endDate: review?.endDate || undefined,
    });
    editorVisible.value = true;
  });
}
async function saveReview() {
  if (!form.name.trim() || !form.caseIds.length || !form.reviewerIds.length)
    return message.warning("请填写名称、用例和评审人员");
  await run(async () => {
    const body = {
      ...form,
      name: form.name.trim(),
      startDate: form.startDate || null,
      endDate: form.endDate || null,
      itemReviewers: Object.fromEntries(
        Object.entries(form.itemReviewers).filter(
          ([id, ids]) => form.caseIds.includes(id) && ids.length,
        ),
      ),
    };
    const result = editingId.value
      ? await api.updateReview(projectId.value, editingId.value, body)
      : await api.createReview(projectId.value, body);
    editorVisible.value = false;
    replace(result);
    await selectReview(result.id);
    message.success("评审已保存");
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
  opinion.value = "";
}
function previousItem() {
  const items = active.value?.items || [];
  const index = items.findIndex((i) => i.id === activeItemId.value);
  activeItemId.value = items[(index - 1 + items.length) % items.length]?.id;
  opinion.value = "";
}
function selectCase(c: Partial<TestCase>) {
  activeItemId.value = active.value?.items.find((i) => i.caseId === c.id)?.id;
}
async function vote(decision: string) {
  if (!active.value || !activeItem.value) return;
  if (!opinion.value.trim()) return message.warning("请填写评审意见");
  await run(async () => {
    replace(
      await api.vote(
        projectId.value,
        active.value!.id,
        activeItem.value!.id,
        decision,
        opinion.value.trim(),
      ),
    );
    opinion.value = "";
    if (autoNext.value) nextItem();
    message.success("评审结论已记录");
  });
}
async function batchVote() {
  if (!active.value || !batchOpinion.value.trim())
    return message.warning("请填写批量意见");
  await run(async () => {
    replace(
      await api.batchVote(
        projectId.value,
        active.value!.id,
        selectedItems.value,
        batchDecision.value,
        batchOpinion.value.trim(),
      ),
    );
    batchVisible.value = false;
    batchOpinion.value = "";
    selectedItems.value = [];
    message.success("批量评审已保存");
  });
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
async function cancel() {
  if (active.value)
    await run(async () =>
      replace(await api.cancel(projectId.value, active.value!.id)),
    );
}
async function copyReview() {
  if (active.value)
    await run(async () => {
      const result = await api.copyReview(projectId.value, active.value!.id);
      replace(result);
      await selectReview(result.id);
      message.success("评审已复制，结论已重置");
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
  editorVisible.value = false;
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
  if (route.query.create === "1") await openEditor();
  if (route.query.edit === "1" && active.value) await openEditor(active.value);
});
</script>
<style scoped>
.review-page {
  padding: 24px;
  max-width: 1800px;
  margin: auto;
}
.review-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}
.review-header h2 {
  margin: 0;
}
.review-header p {
  color: #667085;
  margin: 8px 0;
}
.filters {
  margin: 20px 0;
}
.review-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 20px;
}
.review-workspace {
  min-width: 0;
}
.stats {
  display: flex;
  gap: 24px;
  padding-top: 16px;
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
