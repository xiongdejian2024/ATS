<template>
  <section class="review-editor-page">
    <header>
      <h2>{{ isEdit ? "编辑评审" : "创建评审" }}</h2>
    </header>
    <main>
      <a-spin v-if="loading" spinning /><a-alert
        v-else-if="loadError"
        :message="loadError"
        type="error"
        show-icon
      /><a-empty v-else-if="!projectId" description="请先选择项目" />
      <a-form
        v-else
        ref="formRef"
        :model="form"
        layout="vertical"
        class="review-form"
        :disabled="saving || !canManage"
      >
        <a-form-item
          name="name"
          label="评审名称"
          :rules="[
            { required: true, whitespace: true, message: '评审名称不能为空' },
          ]"
          required
          ><a-input
            v-model:value="form.name"
            placeholder="请输入评审名称"
            :maxlength="255"
        /></a-form-item>
        <a-form-item label="描述"
          ><a-textarea
            v-model:value="form.description"
            placeholder="请输入描述"
            :maxlength="1000"
            :rows="3"
            show-count
        /></a-form-item>
        <a-form-item label="所属模块"
          ><a-tree-select
            v-model:value="form.moduleId"
            show-search
            tree-node-filter-prop="title"
            :tree-data="moduleTree"
            placeholder="请选择所属模块"
            class="narrow"
        /></a-form-item>
        <a-form-item v-if="!isEdit" label="评审模式"
          ><a-radio-group v-model:value="form.mode"
            ><a-radio value="single"
              >单人
              <a-tooltip title="最后一次评审结果，为最终评审结果"
                ><QuestionCircleOutlined /></a-tooltip></a-radio
            ><a-radio value="multiple"
              >多人
              <a-tooltip title="所有评审人评审通过则通过"
                ><QuestionCircleOutlined /></a-tooltip></a-radio></a-radio-group
        ></a-form-item>
        <a-form-item
          name="reviewerIds"
          label="默认评审人"
          :rules="[
            {
              required: true,
              type: 'array',
              min: 1,
              message: '默认评审人不能为空',
            },
          ]"
          required
          ><a-select
            v-model:value="form.reviewerIds"
            mode="multiple"
            show-search
            option-filter-prop="label"
            :options="members.map((m) => ({ label: m.name, value: m.id }))"
            placeholder="请选择评审人"
            allow-clear
          /><span class="help"
            >新添加的用例，评审人为默认评审人</span
          ></a-form-item
        >
        <a-form-item label="标签"
          ><a-select
            v-model:value="form.tags"
            mode="tags"
            :max-tag-count="10"
            :token-separators="[',']"
            placeholder="请输入标签"
        /></a-form-item>
        <a-form-item label="评审周期"
          ><a-range-picker
            v-model:value="form.cycle"
            :show-time="{
              defaultValue: [
                dayjs('00:00:00', 'HH:mm:ss'),
                dayjs('00:00:00', 'HH:mm:ss'),
              ],
            }"
            value-format="YYYY-MM-DD HH:mm:ss"
            format="YYYY-MM-DD HH:mm:ss"
            :placeholder="['开始时间', '结束时间']"
            separator="至"
            class="narrow"
        /></a-form-item>
        <a-form-item v-if="!isEdit"
          ><template #label
            ><span>选择需要评审的用例</span
            ><a-divider v-if="!isCopy" type="vertical" /><a-button
              v-if="!isCopy"
              type="link"
              :disabled="!caseIds.length && !rangeSelection"
              @click="clearCases"
              >清空已选用例</a-button
            ></template
          >
          <div class="selected-cases">
            已选 {{ selectedCount }} 个用例
            <a-alert
              v-if="rangeError"
              :message="rangeError"
              type="error"
              show-icon
              ><template #action
                ><a-button :loading="rangeLoading" @click="loadRange"
                  >重试核对范围</a-button
                ></template
              ></a-alert
            ><a-divider v-if="!isCopy" type="vertical" /><a-button
              v-if="!isCopy"
              type="link"
              @click="associateOpen = true"
              >关联用例</a-button
            >
          </div></a-form-item
        >
      </a-form>
    </main>
    <footer>
      <a-button :disabled="saving" @click="cancel">取消</a-button
      ><template v-if="canManage && !loading && !loadError"
        ><a-button
          v-if="isEdit"
          type="primary"
          :loading="saving"
          @click="save(false)"
          >更新</a-button
        ><template v-else
          ><a-button
            :disabled="rangeLoading || !!rangeError"
            :loading="saving"
            @click="save(false)"
            >保存</a-button
          ><a-button
            type="primary"
            :disabled="saving || rangeLoading || !!rangeError"
            @click="save(true)"
            >评审</a-button
          ></template
        ></template
      >
    </footer>
    <ReviewAssociateDrawer
      :open="associateOpen"
      :project-id="projectId"
      :excluded="caseIds"
      :selection-scope="rangeSelection"
      :default-reviewers="form.reviewerIds"
      :members="members"
      @update:open="associateOpen = $event"
      @confirm="associate"
    />
  </section>
</template>
<script setup lang="ts">
import { ref, reactive, computed, watch, onMounted, onUnmounted } from "vue";
import {
  useRoute,
  useRouter,
  onBeforeRouteLeave,
  onBeforeRouteUpdate,
} from "vue-router";
import { Modal, message } from "ant-design-vue";
import type { FormInstance } from "ant-design-vue";
import { QuestionCircleOutlined } from "@ant-design/icons-vue";
import dayjs from "dayjs";
import customParseFormat from "dayjs/plugin/customParseFormat";
import utc from "dayjs/plugin/utc";
import "dayjs/locale/zh-cn";
import { readReviewSelection } from "@/components/TestCase/caseSelection";
import {
  caseGovernanceApi,
  type CaseSelection,
  type CaseReview,
} from "@/api/caseGovernance";
import { reviewWorkspaceApi, type ReviewModule } from "@/api/reviewWorkspace";
import { useProjectStore } from "@/stores/project";
import ReviewAssociateDrawer from "@/components/CaseReview/ReviewAssociateDrawer.vue";
import { caseFolderTree } from "@/components/TestPlan/planCaseFolders";
dayjs.extend(customParseFormat);
dayjs.extend(utc);
dayjs.locale("zh-cn");
const route = useRoute(),
  router = useRouter(),
  projects = useProjectStore();
const projectId = computed(() =>
  typeof route.query.projectId === "string"
    ? route.query.projectId
    : projects.currentProject?.id || "",
);
const reviewId = computed(() =>
  typeof route.query.reviewId === "string" ? route.query.reviewId : "",
);
const copyFrom = computed(() =>
  typeof route.query.copyFrom === "string" ? route.query.copyFrom : "",
);
const isEdit = computed(() => !!reviewId.value),
  isCopy = computed(() => !!copyFrom.value);
const loading = ref(false),
  saving = ref(false),
  loadError = ref(""),
  canManage = ref(false),
  associateOpen = ref(false),
  members = ref<{ id: string; name: string }[]>([]),
  modules = ref<ReviewModule[]>([]),
  caseIds = ref<string[]>([]),
  itemReviewers = ref<Record<string, string[]>>({}),
  source = ref<CaseReview>(),
  baseline = ref(""),
  initialCycle = ref<string[]>([]),
  formRef = ref<FormInstance>();
const form = reactive({
  name: "",
  description: "",
  moduleId: "default",
  mode: "single" as "single" | "multiple",
  reviewerIds: [] as string[],
  tags: [] as string[],
  cycle: [] as string[],
});
const rangeSelection = ref<CaseSelection>(),
  rangeCount = ref<number>(),
  rangeError = ref(""),
  rangeLoading = ref(false);
const selectedCount = computed(() =>
  rangeSelection.value ? (rangeCount.value ?? "待核对") : caseIds.value.length,
);
let rangeSequence = 0;
function selectionWithExtras(): CaseSelection {
  return {
    ...rangeSelection.value!,
    includeIds: [
      ...new Set([
        ...(rangeSelection.value?.includeIds || []),
        ...caseIds.value,
      ]),
    ],
  };
}
async function loadRange() {
  const current = ++rangeSequence,
    p = projectId.value;
  rangeCount.value = undefined;
  rangeError.value = "";
  if (!rangeSelection.value) {
    rangeLoading.value = false;
    return;
  }
  rangeLoading.value = true;
  try {
    const result = await caseGovernanceApi.previewSelection(
      p,
      selectionWithExtras(),
    );
    if (current !== rangeSequence || p !== projectId.value) return;
    rangeCount.value = result.count;
  } catch (exception: any) {
    console.error("核对评审草稿选择范围失败，保留草稿", exception);
    if (current === rangeSequence)
      rangeError.value =
        exception.response?.data?.detail || "选择范围核对失败，请重试";
  } finally {
    if (current === rangeSequence) rangeLoading.value = false;
  }
}
const moduleTree = computed(() => [
  { title: "默认模块", value: "default", key: "default" },
  ...caseFolderTree(
    modules.value.map((row) => ({
      ...row,
      parentId: row.parentId || undefined,
    })),
  ).map(withValue),
]);
function withValue(node: any): any {
  return { ...node, value: node.key, children: node.children?.map(withValue) };
}
const signature = () =>
  JSON.stringify({
    form,
    caseIds: caseIds.value,
    selection: rangeSelection.value,
    itemReviewers: itemReviewers.value,
  });
const dirty = computed(
  () => !!baseline.value && baseline.value !== signature(),
);
let sequence = 0;
watch(
  () => [
    projectId.value,
    reviewId.value,
    copyFrom.value,
    route.query.caseIds,
    route.query.selectionKey,
    route.query.moduleId,
  ],
  async () => {
    const current = ++sequence,
      p = projectId.value;
    loading.value = true;
    loadError.value = "";
    canManage.value = false;
    baseline.value = "";
    source.value = undefined;
    associateOpen.value = false;
    members.value = [];
    modules.value = [];
    caseIds.value = [];
    rangeSelection.value = undefined;
    rangeCount.value = undefined;
    rangeError.value = "";
    ++rangeSequence;
    rangeLoading.value = false;
    itemReviewers.value = {};
    Object.assign(form, {
      name: "",
      description: "",
      moduleId: "default",
      mode: "single",
      reviewerIds: [],
      tags: [],
      cycle: [],
    });
    try {
      if (!p) return;
      const [listing, people, record] = await Promise.all([
        reviewWorkspaceApi.list(p, { size: 1 }),
        caseGovernanceApi.reviewers(p),
        reviewId.value || copyFrom.value
          ? caseGovernanceApi.review(p, reviewId.value || copyFrom.value)
          : Promise.resolve(undefined),
      ]);
      if (current !== sequence || p !== projectId.value) return;
      canManage.value = listing.permissions.update;
      members.value = people;
      modules.value = listing.modules;
      if (!canManage.value) {
        loadError.value = "当前账号没有评审编辑权限";
        return;
      }
      if (
        isEdit.value &&
        record &&
        (record.archived || ["cancelled", "superseded"].includes(record.status))
      ) {
        loadError.value = "评审已归档或关闭，不能编辑基本信息";
        canManage.value = false;
        return;
      }
      source.value = record;
      Object.assign(form, {
        name: record
          ? isCopy.value
            ? `${record.name.slice(0, 251)}（副本）`
            : record.name
          : "",
        description: record?.description || "",
        moduleId:
          record?.moduleId ||
          (typeof route.query.moduleId === "string"
            ? route.query.moduleId
            : "default"),
        mode: record?.mode || "single",
        reviewerIds: [...(record?.reviewerIds || [])],
        tags: [...(record?.tags || [])],
        cycle:
          record?.startTime && record.endTime
            ? [
                dayjs(record.startTime)
                  .utcOffset(480)
                  .format("YYYY-MM-DD HH:mm:ss"),
                dayjs(record.endTime)
                  .utcOffset(480)
                  .format("YYYY-MM-DD HH:mm:ss"),
              ]
            : [],
      });
      initialCycle.value = [...form.cycle];
      caseIds.value = record
        ? record.items.map((i) => i.caseId)
        : typeof route.query.caseIds === "string"
          ? [...new Set(route.query.caseIds.split(",").filter(Boolean))]
          : [];
      itemReviewers.value = record
        ? Object.fromEntries(
            record.items.map((i) => [
              i.caseId,
              [...(i.reviewerIds || record.reviewerIds)],
            ]),
          )
        : {};
      if (!record && typeof route.query.selectionKey === "string") {
        rangeSelection.value = readReviewSelection(p, route.query.selectionKey);
        await loadRange();
        if (current !== sequence || p !== projectId.value) return;
      }
      baseline.value = signature();
      console.info("独立评审编辑页面已加载", {
        projectId: p,
        reviewId: record?.id,
        copyDraft: isCopy.value,
      });
    } catch (error) {
      console.error("加载独立评审编辑页面失败", error);
      if (current === sequence)
        loadError.value = "加载评审失败，请返回列表重试";
    } finally {
      if (current === sequence) loading.value = false;
    }
  },
  { immediate: true },
);
async function associate(data: { caseIds: string[]; reviewerIds: string[] }) {
  caseIds.value = [...new Set([...caseIds.value, ...data.caseIds])];
  for (const id of data.caseIds)
    itemReviewers.value[id] = [...data.reviewerIds];
  await loadRange();
}
function clearCases() {
  rangeSelection.value = undefined;
  rangeCount.value = undefined;
  rangeError.value = "";
  ++rangeSequence;
  rangeLoading.value = false;
  caseIds.value = [];
  itemReviewers.value = {};
  console.info("已清空评审草稿关联用例", { projectId: projectId.value });
}
function period() {
  if (form.cycle?.length !== 2) return { startTime: null, endTime: null };
  if (
    source.value &&
    JSON.stringify(form.cycle) === JSON.stringify(initialCycle.value)
  )
    return { startTime: source.value.startTime, endTime: source.value.endTime };
  return {
    startTime: form.cycle[0].replace(" ", "T") + "+08:00",
    endTime: form.cycle[1].replace(" ", "T") + "+08:00",
  };
}
async function save(openReview: boolean) {
  if (
    saving.value ||
    loading.value ||
    !canManage.value ||
    rangeLoading.value ||
    rangeError.value
  )
    return;
  try {
    await formRef.value?.validate();
  } catch (error) {
    console.info("评审表单校验未通过", error);
    return;
  }
  const p = projectId.value,
    current = sequence;
  const header = {
    name: form.name.trim(),
    description: form.description,
    moduleId: form.moduleId === "default" ? null : form.moduleId,
    mode: form.mode,
    reviewerIds: [...form.reviewerIds],
    tags: [...form.tags],
    ...period(),
  };
  saving.value = true;
  try {
    const record = isEdit.value
      ? await reviewWorkspaceApi.updateHeader(p, reviewId.value, header)
      : isCopy.value
        ? await caseGovernanceApi.copyReview(p, copyFrom.value, header)
        : await caseGovernanceApi.createReview(p, {
            ...header,
            caseIds: [...caseIds.value],
            ...(rangeSelection.value
              ? { selection: rangeSelection.value }
              : {}),
            itemReviewers: itemReviewers.value,
          });
    if (p !== projectId.value || current !== sequence) return;
    baseline.value = signature();
    if (typeof route.query.selectionKey === "string")
      sessionStorage.removeItem(route.query.selectionKey);
    console.info("评审已保存", {
      projectId: p,
      reviewId: record.id,
      edit: isEdit.value,
      copy: isCopy.value,
    });
    message.success(isEdit.value ? "评审已更新" : "评审已创建");
    saving.value = false;
    const detail =
      openReview || (isEdit.value && route.query.returnTo === "detail");
    await router.push({
      name: detail ? "CaseReviewWorkspace" : "CaseReviews",
      query: { projectId: p, ...(detail ? { reviewId: record.id } : {}) },
    });
  } catch (error) {
    console.error("保存独立评审失败", error);
  } finally {
    saving.value = false;
  }
}
function canLeave() {
  if (saving.value) {
    message.info("正在保存评审，请稍候");
    return false;
  }
  if (!dirty.value) return true;
  return new Promise<boolean>((resolve) =>
    Modal.confirm({
      title: "内容尚未保存",
      content: "离开后将丢失未保存的修改，是否继续？",
      okText: "离开",
      cancelText: "继续编辑",
      onOk: () => resolve(true),
      onCancel: () => resolve(false),
    }),
  );
}
onBeforeRouteLeave(canLeave);
onBeforeRouteUpdate(canLeave);
function cancel() {
  return router.push({
    name:
      isEdit.value && route.query.returnTo === "detail"
        ? "CaseReviewWorkspace"
        : "CaseReviews",
    query: {
      projectId: projectId.value,
      ...(isEdit.value && route.query.returnTo === "detail"
        ? { reviewId: reviewId.value }
        : {}),
    },
  });
}
function unload(event: BeforeUnloadEvent) {
  if (dirty.value) {
    event.preventDefault();
    event.returnValue = "";
  }
}
function shortcut(event: KeyboardEvent) {
  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "s") {
    event.preventDefault();
    void save(false);
  }
}
onMounted(() => {
  window.addEventListener("beforeunload", unload);
  window.addEventListener("keydown", shortcut);
});
onUnmounted(() => {
  ++sequence;
  ++rangeSequence;
  window.removeEventListener("beforeunload", unload);
  window.removeEventListener("keydown", shortcut);
});
</script>
<style scoped>
.review-editor-page {
  height: 100%;
  min-height: 0;
  background: white;
  display: flex;
  flex-direction: column;
}
.review-editor-page header {
  padding: 24px 24px 0;
}
.review-editor-page h2 {
  font-size: 16px;
  font-weight: 500;
  margin: 0;
}
.review-editor-page main {
  flex: 1;
  min-height: 0;
  overflow: auto;
  padding: 24px;
}
.review-form {
  width: 732px;
  max-width: 100%;
}
.narrow {
  width: 436px;
  max-width: 100%;
}
.help {
  display: block;
  color: #86909c;
  margin-top: 8px;
}
.selected-cases {
  background: #f7f8fa;
  padding: 12px;
}
.review-editor-page footer {
  border-top: 1px solid #e5e6eb;
  display: flex;
  justify-content: flex-end;
  gap: 16px;
  padding: 16px 24px;
}
.review-form :deep(.ant-form-item-label) {
  padding-bottom: 8px;
}
.review-form :deep(.anticon-question-circle) {
  color: #86909c;
}
</style>
