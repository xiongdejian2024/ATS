<template>
  <a-spin :spinning="busy">
    <a-tabs v-model:active-key="tab" :class="{ 'section-only': section }">
      <a-tab-pane
        v-if="!section || section === 'requirement' || section === 'defect'"
        key="issues"
        tab="需求与缺陷"
      >
        <a-space v-if="!readOnly" wrap
          ><a-select
            v-model:value="issueId"
            show-search
            option-filter-prop="label"
            :placeholder="
              section === 'defect'
                ? '关联已有缺陷'
                : section === 'requirement'
                  ? '关联已有需求'
                  : '关联已有需求或缺陷'
            "
            style="width: 320px; max-width: 100%"
            :options="
              visibleIssues
                .filter((i) => !linkedIssues.some((l) => l.id === i.id))
                .map((i) => ({
                  label: `${i.kind === 'defect' ? '缺陷' : '需求'} · ${i.title}`,
                  value: i.id,
                }))
            "
          /><a-button :disabled="!issueId" @click="linkIssue">关联</a-button
          ><a-button @click="openIssue()">{{
            section === "defect"
              ? "新建缺陷"
              : section === "requirement"
                ? "新建需求"
                : "新建需求 / 缺陷"
          }}</a-button></a-space
        >
        <a-list :data-source="visibleLinkedIssues"
          ><template #renderItem="{ item }"
            ><a-list-item
              ><a-list-item-meta
                :title="`${item.kind === 'defect' ? '缺陷' : '需求'} · ${item.title}`"
                :description="`${issueStatuses[item.status] || item.status} · ${item.externalRef || item.description || ''}`"
              /><template v-if="!readOnly" #actions
                ><a-button type="link" @click="openIssue(item)">编辑</a-button
                ><a-popconfirm
                  title="取消这条关联？"
                  @confirm="removeIssue(item.linkId)"
                  ><a-button type="link" danger
                    >取消关联</a-button
                  ></a-popconfirm
                ></template
              ></a-list-item
            ></template
          ></a-list
        >
      </a-tab-pane>
      <a-tab-pane
        v-if="!section || section === 'dependency'"
        key="relations"
        tab="前后置与相关用例"
      >
        <a-alert
          message="这里记录用例之间的关系，不会自动改变执行顺序。执行顺序请在计划或测试任务中配置。"
          type="info"
          show-icon
          style="margin-bottom: 12px"
        />
        <a-space v-if="!readOnly" wrap
          ><a-select
            v-model:value="relationKind"
            :options="visibleRelationKinds"
            style="width: 140px"
          /><a-select
            v-model:value="targetCaseId"
            show-search
            :filter-option="false"
            @search="searchCases"
            placeholder="搜索目标用例"
            style="width: 300px"
            :options="
              caseOptions
                .filter((c) => c.id !== caseId)
                .map((c) => ({ label: c.name, value: c.id }))
            "
          /><a-button :disabled="!targetCaseId" @click="relate"
            >添加关系</a-button
          ></a-space
        >
        <a-list :data-source="visibleRelations"
          ><template #renderItem="{ item }"
            ><a-list-item
              ><a-list-item-meta
                :title="`${relationKinds.find((k) => k.value === item.kind)?.label || item.kind} · ${item.name}`"
                :description="item.deleted ? '用例已移入回收站' : item.caseCode"
              /><template v-if="!readOnly" #actions
                ><a-button
                  type="link"
                  @click="emit('navigate', item.targetCaseId)"
                  :disabled="item.deleted"
                  >查看</a-button
                ><a-popconfirm
                  title="删除此用例关系？"
                  @confirm="unrelate(item.id)"
                  ><a-button danger type="link"
                    >删除关系</a-button
                  ></a-popconfirm
                ></template
              ></a-list-item
            ></template
          ></a-list
        >
      </a-tab-pane>
      <a-tab-pane
        v-if="!section || section === 'case'"
        key="automation"
        tab="自动化关联"
      >
        <a-alert
          message="可关联已有自动化用例、ATS 执行模板或外部引用。建立关联不会启动执行。"
          type="info"
          show-icon
          style="margin-bottom: 12px"
        />
        <a-form v-if="!readOnly" layout="vertical"
          ><a-row :gutter="12"
            ><a-col :span="8"
              ><a-form-item label="自动化类型"
                ><a-select
                  v-model:value="automationCategory"
                  :options="automationKinds" /></a-form-item></a-col
            ><a-col :span="16"
              ><a-form-item label="关联目标"
                ><a-radio-group v-model:value="automationMode"
                  ><a-radio-button value="case">自动化用例</a-radio-button
                  ><a-radio-button value="suite">执行模板</a-radio-button
                  ><a-radio-button value="external"
                    >外部引用</a-radio-button
                  ></a-radio-group
                ></a-form-item
              ></a-col
            ></a-row
          >
          <a-space style="width: 100%" wrap
            ><a-select
              v-if="automationMode !== 'external'"
              v-model:value="automationTargetId"
              style="width: 320px"
              show-search
              option-filter-prop="label"
              :options="
                (automationMode === 'case' ? targets.cases : targets.suites)
                  .filter((t) => t.id !== caseId)
                  .map((t) => ({ label: t.name, value: t.id }))
              "
              placeholder="选择关联目标"
            /><a-input
              v-else
              v-model:value="externalRef"
              style="width: 320px"
              placeholder="外部用例编号或链接"
            /><a-button @click="addAutomation">关联</a-button></a-space
          ></a-form
        >
        <a-list :data-source="automations"
          ><template #renderItem="{ item }"
            ><a-list-item
              ><a-list-item-meta
                :title="
                  automationKinds.find((k) => k.value === item.category)?.label
                "
                :description="automationName(item)"
              /><template v-if="!readOnly" #actions
                ><a-popconfirm
                  title="删除此自动化关联？"
                  @confirm="removeAutomation(item.id)"
                  ><a-button type="link" danger
                    >取消关联</a-button
                  ></a-popconfirm
                ></template
              ></a-list-item
            ></template
          ></a-list
        >
      </a-tab-pane>
    </a-tabs>
    <a-modal
      v-model:open="issueVisible"
      :title="
        (editingIssueId ? '编辑' : '新建并关联') +
        (section === 'defect'
          ? '缺陷'
          : section === 'requirement'
            ? '需求'
            : '需求 / 缺陷')
      "
      :confirm-loading="busy"
      @ok="saveIssue"
    >
      <a-form v-if="!readOnly" layout="vertical"
        ><a-form-item v-if="!section" label="类别"
          ><a-radio-group v-model:value="issueForm.kind"
            ><a-radio value="requirement">需求</a-radio
            ><a-radio value="defect">缺陷</a-radio></a-radio-group
          ></a-form-item
        ><a-form-item label="标题" required
          ><a-input
            v-model:value="issueForm.title"
            :maxlength="300" /></a-form-item
        ><a-form-item label="描述"
          ><a-textarea
            v-model:value="issueForm.description"
            :rows="4" /></a-form-item
        ><a-form-item label="状态"
          ><a-select
            v-model:value="issueForm.status"
            :options="
              Object.entries(issueStatuses).map(([value, label]) => ({
                value,
                label,
              }))
            " /></a-form-item
        ><a-form-item label="外部引用"
          ><a-input v-model:value="issueForm.externalRef" /></a-form-item
      ></a-form>
    </a-modal>
  </a-spin>
</template>
<script setup lang="ts">
import { ref, reactive, watch, computed } from "vue";
import { message } from "ant-design-vue";
import {
  caseFeaturesApi as api,
  type CaseIssue,
  type CaseRelation,
  type CaseAutomation,
} from "@/api/caseFeatures";
import { testCaseApi } from "@/api/testCase";
const props = defineProps<{
    projectId: string;
    readOnly?: boolean;
    caseId: string;
    section?: "requirement" | "defect" | "dependency" | "case";
  }>(),
  emit = defineEmits<{ navigate: [caseId: string]; changed: [] }>();
const busy = ref(false),
  tab = ref(
    props.section === "dependency"
      ? "relations"
      : props.section === "case"
        ? "automation"
        : "issues",
  ),
  issues = ref<CaseIssue[]>([]),
  linkedIssues = ref<CaseIssue[]>([]),
  issueId = ref<string>(),
  issueVisible = ref(false),
  editingIssueId = ref<string>();
const relations = ref<CaseRelation[]>([]),
  targetCaseId = ref<string>(),
  relationKind = ref("precondition"),
  caseOptions = ref<{ id: string; name: string }[]>([]);
const targets = ref<{
    cases: { id: string; name: string }[];
    suites: { id: string; name: string }[];
  }>({ cases: [], suites: [] }),
  automations = ref<CaseAutomation[]>([]),
  automationMode = ref("case"),
  automationCategory = ref("api"),
  automationTargetId = ref<string>(),
  externalRef = ref("");
const issueStatuses: Record<string, string> = {
  open: "待处理",
  in_progress: "进行中",
  resolved: "已解决",
  closed: "已关闭",
};
const relationKinds = [
  { label: "前置用例", value: "precondition" },
  { label: "后置用例", value: "postcondition" },
  { label: "相关用例", value: "related" },
];
const automationKinds = [
  { label: "接口用例", value: "api" },
  { label: "场景用例", value: "scenario" },
  { label: "UI自动化", value: "ui" },
  { label: "脚本", value: "script" },
];
const visibleIssues = computed(() =>
  issues.value.filter(
    (i) =>
      !["requirement", "defect"].includes(props.section || "") ||
      i.kind === props.section,
  ),
);
const visibleLinkedIssues = computed(() =>
  linkedIssues.value.filter(
    (i) =>
      !["requirement", "defect"].includes(props.section || "") ||
      i.kind === props.section,
  ),
);
const visibleRelations = computed(() =>
  relations.value.filter(
    (i) => props.section !== "dependency" || i.kind !== "related",
  ),
);
const visibleRelationKinds = computed(() =>
  relationKinds.filter(
    (i) => props.section !== "dependency" || i.value !== "related",
  ),
);
const issueForm = reactive({
  kind: "requirement" as "requirement" | "defect",
  title: "",
  description: "",
  status: "open",
  externalRef: "",
});
async function load() {
  busy.value = true;
  try {
    const data = await Promise.all([
      api.issues(props.projectId),
      api.linkedIssues(props.projectId, props.caseId),
      api.relations(props.projectId, props.caseId),
      api.automationTargets(props.projectId),
      api.automation(props.projectId, props.caseId),
    ]);
    [
      issues.value,
      linkedIssues.value,
      relations.value,
      targets.value,
      automations.value,
    ] = data;
    await searchCases("");
  } catch (error) {
    console.error("加载用例关联失败", error);
  } finally {
    busy.value = false;
  }
}
async function run(task: () => Promise<unknown>) {
  if (props.readOnly) return;
  busy.value = true;
  try {
    await task();
    await load();
    emit("changed");
  } catch (error) {
    console.error("保存用例关联失败", error);
  } finally {
    busy.value = false;
  }
}
async function searchCases(search: string) {
  try {
    caseOptions.value = (
      await testCaseApi.getTestCases(props.projectId, { search, size: 100 })
    ).items;
  } catch (error) {
    console.error("搜索关联用例失败", error);
  }
}
function openIssue(item?: CaseIssue) {
  editingIssueId.value = item?.id;
  Object.assign(
    issueForm,
    item
      ? {
          kind: item.kind,
          title: item.title,
          description: item.description,
          status: item.status,
          externalRef: item.externalRef || "",
        }
      : {
          kind: props.section === "defect" ? "defect" : "requirement",
          title: "",
          description: "",
          status: "open",
          externalRef: "",
        },
  );
  issueVisible.value = true;
}
async function saveIssue() {
  if (!issueForm.title.trim()) return message.warning("请输入标题");
  await run(async () => {
    const row = await api.saveIssue(
      props.projectId,
      { ...issueForm, title: issueForm.title.trim() },
      editingIssueId.value,
    );
    if (!editingIssueId.value)
      await api.linkIssue(props.projectId, props.caseId, row.id);
    issueVisible.value = false;
    message.success("需求 / 缺陷已保存");
  });
}
async function linkIssue() {
  if (issueId.value)
    await run(async () => {
      await api.linkIssue(props.projectId, props.caseId, issueId.value!);
      issueId.value = undefined;
    });
}
async function removeIssue(id: string) {
  await run(() => api.unlinkIssue(props.projectId, props.caseId, id));
}
async function relate() {
  if (targetCaseId.value)
    await run(async () => {
      await api.relate(
        props.projectId,
        props.caseId,
        targetCaseId.value!,
        relationKind.value,
      );
      targetCaseId.value = undefined;
    });
}
async function unrelate(id: string) {
  await run(() => api.unrelate(props.projectId, props.caseId, id));
}
async function addAutomation() {
  const target =
    automationMode.value === "external"
      ? externalRef.value.trim()
      : automationTargetId.value;
  if (!target) return message.warning("请选择或填写关联目标");
  await run(async () => {
    await api.linkAutomation(props.projectId, props.caseId, {
      category: automationCategory.value,
      ...(automationMode.value === "case"
        ? { targetCaseId: target }
        : automationMode.value === "suite"
          ? { suiteId: target }
          : { externalRef: target }),
    });
    automationTargetId.value = undefined;
    externalRef.value = "";
  });
}
async function removeAutomation(id: string) {
  await run(() => api.unlinkAutomation(props.projectId, props.caseId, id));
}
function automationName(item: CaseAutomation) {
  return (
    item.externalRef ||
    targets.value.cases.find((c) => c.id === item.targetCaseId)?.name ||
    targets.value.suites.find((s) => s.id === item.suiteId)?.name ||
    "目标已移除"
  );
}
watch(automationMode, () => {
  automationTargetId.value = undefined;
  externalRef.value = "";
});
watch(() => [props.projectId, props.caseId], load, { immediate: true });
</script>

<style scoped>
.section-only :deep(.ant-tabs-nav) {
  display: none;
}
</style>
