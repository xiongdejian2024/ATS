<template>
  <section class="case-detail">
    <a-spin :spinning="loading">
      <a-page-header
        :title="item?.name || '用例详情'"
        :sub-title="item?.caseCode"
      >
        <template #extra
          ><a-space
            ><a-button @click="share">复制链接</a-button
            ><a-button type="primary" @click="emit('edit')"
              >编辑用例</a-button
            ></a-space
          ></template
        >
      </a-page-header>
      <template v-if="item">
        <a-descriptions bordered :column="2" size="small">
          <a-descriptions-item label="优先级">{{
            item.priority
          }}</a-descriptions-item
          ><a-descriptions-item label="类型">{{
            typeNames[item.type] || item.type
          }}</a-descriptions-item>
          <a-descriptions-item label="执行结果">{{
            statusNames[item.status] || item.status
          }}</a-descriptions-item
          ><a-descriptions-item label="自动化">{{
            item.isAutomated ? "是" : "否"
          }}</a-descriptions-item>
          <a-descriptions-item label="需求">{{
            item.requirementRef || "未填写"
          }}</a-descriptions-item
          ><a-descriptions-item label="标签"
            ><a-tag v-for="tag in item.tags" :key="tag">{{
              tag
            }}</a-tag></a-descriptions-item
          >
        </a-descriptions>
        <a-tabs v-model:active-key="activeTab">
          <a-tab-pane key="content" tab="用例内容"
            ><a-card title="前置条件" size="small"
              ><p class="text">{{ item.precondition || "无" }}</p></a-card
            ><a-table
              :columns="stepColumns"
              :data-source="item.steps || []"
              :pagination="false"
              size="small"
              ><template #bodyCell="{ column, record }"
                ><p class="text">{{ record[column.dataIndex] }}</p></template
              ></a-table
            ></a-tab-pane
          >
          <a-tab-pane key="links" tab="关联管理"
            ><CaseLinks
              :project-id="projectId"
              :case-id="caseId"
              @navigate="emit('navigate', $event)"
              @changed="loadChanges"
          /></a-tab-pane>
          <a-tab-pane key="discussion" tab="关注与讨论"
            ><CaseDiscussion
              :project-id="projectId"
              :case-id="caseId"
              @changed="loadChanges"
          /></a-tab-pane>
          <a-tab-pane v-if="template" key="fields" tab="自定义字段"
            ><a-form layout="vertical"
              ><CaseCustomFields
                :fields="template.fields"
                :model-value="(item as any).customFields || {}"
                readonly /></a-form
          ></a-tab-pane>
          <a-tab-pane key="attachments" tab="附件"
            ><CaseAttachments :project-id="projectId" :case-id="caseId"
          /></a-tab-pane>
          <a-tab-pane key="usage" tab="关联计划与评审"
            ><h4>测试计划</h4>
            <a-list :data-source="usage.plans"
              ><template #renderItem="{ item: plan }"
                ><a-list-item
                  ><router-link
                    :to="{
                      path: '/test-plans',
                      query: { projectId, planId: plan.id },
                    }"
                    >{{ plan.name }}</router-link
                  ></a-list-item
                ></template
              ></a-list
            >
            <h4>用例评审</h4>
            <a-list :data-source="usage.reviews"
              ><template #renderItem="{ item: review }"
                ><a-list-item
                  ><router-link
                    :to="{
                      path: '/case-reviews',
                      query: { projectId, reviewId: review.id },
                    }"
                    >{{ review.name }}</router-link
                  ></a-list-item
                ></template
              ></a-list
            ></a-tab-pane
          >
          <a-tab-pane key="changes" tab="变更记录"
            ><a-empty
              v-if="!changes.length"
              description="暂无变更记录"
            /><a-timeline v-else
              ><a-timeline-item v-for="change in changes" :key="change.id"
                ><strong>{{
                  actionNames[change.action] || change.action
                }}</strong>
                · {{ change.createdAt }}
                <pre class="text">{{
                  JSON.stringify(change.detail, null, 2)
                }}</pre>
              </a-timeline-item></a-timeline
            ></a-tab-pane
          >
        </a-tabs>
      </template>
    </a-spin>
  </section>
</template>
<script setup lang="ts">
import { ref, watch } from "vue";
import { message } from "ant-design-vue";
import type { TestCase } from "@/types";
import { testCaseApi } from "@/api/testCase";
import {
  caseFeaturesApi,
  type CaseChange,
  type CaseTemplate,
} from "@/api/caseFeatures";
import CaseAttachments from "./CaseAttachments.vue";
import CaseLinks from "./CaseLinks.vue";
import CaseDiscussion from "./CaseDiscussion.vue";
import CaseCustomFields from "./CaseCustomFields.vue";
const props = defineProps<{
  caseId: string;
  projectId: string;
  readOnly?: boolean;
}>();
const emit = defineEmits<{
  edit: [];
  delete: [];
  copy: [];
  execute: [];
  navigate: [caseId: string];
}>();
const template = ref<CaseTemplate>();
const usage = ref<{
  plans: { id: string; name: string }[];
  reviews: { id: string; name: string }[];
}>({ plans: [], reviews: [] });
const loading = ref(false),
  item = ref<TestCase>(),
  changes = ref<CaseChange[]>([]),
  activeTab = ref("content");
const typeNames: Record<string, string> = {
  functional: "功能测试",
  interface: "接口测试",
  ui: "UI测试",
  performance: "性能测试",
  security: "安全测试",
};
const statusNames: Record<string, string> = {
  not_executed: "未执行",
  passed: "通过",
  failed: "失败",
  blocked: "阻塞",
  skipped: "跳过",
};
const actionNames: Record<string, string> = {
  created: "创建用例",
  updated: "更新用例",
  deleted: "移入回收站",
  restored: "恢复用例",
  attachment_uploaded: "上传附件",
  attachment_deleted: "删除附件",
};
const stepColumns = [
  { title: "步骤", dataIndex: "step", width: 65 },
  { title: "操作", dataIndex: "action" },
  { title: "预期结果", dataIndex: "expected" },
];
async function load() {
  if (!props.caseId) return;
  loading.value = true;
  try {
    item.value = await testCaseApi.getTestCase(props.projectId, props.caseId);
    await loadChanges();
    usage.value = await caseFeaturesApi.usage(props.projectId, props.caseId);
    template.value = (await caseFeaturesApi.templates(props.projectId)).find(
      (t) => t.id === (item.value as any).templateId,
    );
  } catch (error) {
    console.error("加载用例详情失败", error);
  } finally {
    loading.value = false;
  }
}
async function loadChanges() {
  try {
    changes.value = await caseFeaturesApi.changes(
      props.projectId,
      props.caseId,
    );
  } catch (error) {
    console.error("加载变更记录失败", error);
  }
}
async function share() {
  try {
    const url = new URL("/test-cases", location.origin);
    url.searchParams.set("projectId", props.projectId);
    url.searchParams.set("caseId", props.caseId);
    await navigator.clipboard.writeText(url.toString());
    message.success("用例链接已复制，访问者仍需项目权限");
  } catch (error) {
    console.error("复制用例链接失败", error);
    message.error("浏览器未允许复制，请使用地址栏链接");
  }
}
watch(
  () => [props.projectId, props.caseId],
  () => {
    activeTab.value = "content";
    load();
  },
  { immediate: true },
);
</script>
<style scoped>
.case-detail {
  padding: 16px;
}
.text {
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  margin: 8px 0;
  max-height: 400px;
  overflow: auto;
}
.case-detail :deep(.ant-page-header) {
  padding: 0 0 18px;
}
</style>
