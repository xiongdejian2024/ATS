<template>
  <section class="case-detail">
    <a-spin :spinning="loading">
      <template v-if="item">
        <header class="case-detail-header">
          <div class="case-detail-title">
            <span>【{{ item.caseCode }}】</span><span>{{ item.name }}</span>
          </div>
          <a-space :size="4" wrap>
            <a-button @click="emit('edit')"><EditOutlined /> 编辑</a-button>
            <a-button @click="share"><LinkOutlined /> 分享</a-button>
            <a-button :loading="followBusy" @click="toggleFollow"
              ><StarFilled
                v-if="followed"
                style="color: #f7ba1e"
              /><StarOutlined v-else />
              {{ followed ? "取消关注" : "关注" }}</a-button
            >
            <a-dropdown
              ><a-button><MoreOutlined /> 更多</a-button
              ><template #overlay
                ><a-menu
                  ><a-menu-item @click="emit('copy')">复制</a-menu-item
                  ><a-menu-item danger @click="emit('delete')"
                    >删除</a-menu-item
                  ></a-menu
                ></template
              ></a-dropdown
            >
          </a-space>
        </header>
        <a-tabs v-model:active-key="activeTab" class="case-detail-tabs">
          <template #rightExtra
            ><a-button type="text" @click="settingsVisible = true"
              >显示设置</a-button
            ></template
          >
          <a-tab-pane
            v-for="tab in visibleTabs"
            :key="tab.key"
            :tab="tab.label"
          >
            <template v-if="tab.key === 'basicInfo'">
              <a-descriptions :column="2" size="small" bordered>
                <a-descriptions-item label="ID">{{
                  item.caseCode
                }}</a-descriptions-item
                ><a-descriptions-item label="名称">{{
                  item.name
                }}</a-descriptions-item>
                <a-descriptions-item label="等级">{{
                  item.priority
                }}</a-descriptions-item
                ><a-descriptions-item label="类型">{{
                  typeNames[item.type] || item.type
                }}</a-descriptions-item>
                <a-descriptions-item label="执行结果">{{
                  statusNames[item.status] || item.status
                }}</a-descriptions-item
                ><a-descriptions-item label="是否自动化">{{
                  item.isAutomated ? "是" : "否"
                }}</a-descriptions-item>
                <a-descriptions-item label="标签"
                  ><a-tag v-for="tag in item.tags" :key="tag">{{
                    tag
                  }}</a-tag></a-descriptions-item
                ><a-descriptions-item label="需求关联">{{
                  item.requirementRef || "-"
                }}</a-descriptions-item>
                <a-descriptions-item label="创建时间">{{
                  item.createdAt || "-"
                }}</a-descriptions-item
                ><a-descriptions-item label="更新时间">{{
                  item.updatedAt || "-"
                }}</a-descriptions-item>
              </a-descriptions>
              <a-form v-if="template" layout="vertical" class="custom-fields"
                ><CaseCustomFields
                  :fields="template.fields"
                  :model-value="item.customFields || {}"
                  readonly
              /></a-form>
            </template>
            <template v-else-if="tab.key === 'detail'">
              <a-card title="前置条件" size="small"
                ><CaseRichText :model-value="item.precondition || '无'" readonly /></a-card
              >
              <template v-if="item.caseEditType === 'TEXT'">
                <a-card title="文本描述" size="small"><CaseRichText :model-value="item.textDescription || '无'" readonly /></a-card>
                <a-card title="预期结果" size="small"><CaseRichText :model-value="item.expectedResult || '无'" readonly /></a-card>
              </template>
              <a-table
                v-else
                :columns="stepColumns"
                :data-source="item.steps || []"
                :pagination="false"
                size="small"
                ><template #bodyCell="{ column, record }"
                  ><p class="text">{{ record[column.dataIndex] }}</p></template
                ></a-table
              >
              <a-card title="备注" size="small"><CaseRichText :model-value="item.description || '无'" readonly /></a-card>
              <CaseAttachments :project-id="projectId" :case-id="caseId" />
            </template>
            <CaseLinks
              v-else-if="
                ['case', 'requirement', 'defect', 'dependency'].includes(
                  tab.key,
                )
              "
              :project-id="projectId"
              :case-id="caseId"
              :section="
                tab.key as 'case' | 'requirement' | 'defect' | 'dependency'
              "
              @navigate="emit('navigate', $event)"
              @changed="loadChanges"
            />
            <a-list
              v-else-if="tab.key === 'testPlan'"
              :data-source="usage.plans"
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
            <a-list
              v-else-if="tab.key === 'caseReview'"
              :data-source="usage.reviews"
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
            >
            <CaseDiscussion
              v-else-if="tab.key === 'comments'"
              :project-id="projectId"
              :case-id="caseId"
              hide-follow
              @changed="loadChanges"
            />
            <template v-else-if="tab.key === 'changes'"
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
              ></template
            >
          </a-tab-pane>
        </a-tabs>
      </template>
      <a-drawer v-model:open="settingsVisible" title="显示设置" width="320">
        <p>拖动调整页签顺序，基本信息和详情始终显示。</p>
        <VueDraggable
          v-model="tabSettings"
          :animation="150"
          handle=".tab-drag-handle"
          @end="saveTabSettings"
        >
          <div
            v-for="tab in tabSettings"
            :key="tab.key"
            class="tab-setting-row"
          >
            <HolderOutlined class="tab-drag-handle" /><a-checkbox
              v-model:checked="tab.show"
              :disabled="['basicInfo', 'detail'].includes(tab.key)"
              @change="saveTabSettings"
              >{{ tab.label }}</a-checkbox
            >
          </div>
        </VueDraggable>
      </a-drawer>
    </a-spin>
  </section>
</template>
<script setup lang="ts">
import { ref, watch, computed } from "vue";
import { message } from "ant-design-vue";
import {
  EditOutlined,
  LinkOutlined,
  StarFilled,
  StarOutlined,
  MoreOutlined,
  HolderOutlined,
} from "@ant-design/icons-vue";
import { VueDraggable } from "vue-draggable-plus";
import { useUserStore } from "@/stores/user";
import type { TestCase } from "@/types";
import { testCaseApi } from "@/api/testCase";
import {
  caseFeaturesApi,
  type CaseChange,
  type CaseTemplate,
} from "@/api/caseFeatures";
import CaseAttachments from "./CaseAttachments.vue";
import CaseRichText from "./CaseRichText.vue";
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
  activeTab = ref("detail");
const followed = ref(false),
  followBusy = ref(false),
  settingsVisible = ref(false);
const defaultTabs = [
  { key: "basicInfo", label: "基本信息" },
  { key: "detail", label: "详情" },
  { key: "case", label: "用例" },
  { key: "requirement", label: "需求" },
  { key: "defect", label: "缺陷" },
  { key: "dependency", label: "依赖关系" },
  { key: "caseReview", label: "用例评审" },
  { key: "testPlan", label: "测试计划" },
  { key: "comments", label: "评论" },
  { key: "changes", label: "变更历史" },
];
const user = useUserStore();
const settingsKey = () => `caseDetailTabs:${user.user?.id || "local"}`;
const tabSettings = ref(defaultTabs.map((tab) => ({ ...tab, show: true })));
const visibleTabs = computed(() => tabSettings.value.filter((tab) => tab.show));
function loadTabSettings() {
  try {
    const raw = localStorage.getItem(settingsKey());
    if (!raw) return;
    const saved = JSON.parse(raw);
    if (!Array.isArray(saved)) return;
    const seen = new Set<string>();
    const restored = saved.flatMap((entry: any) => {
      const known = defaultTabs.find((tab) => tab.key === entry.key);
      if (!known || seen.has(known.key)) return [];
      seen.add(known.key);
      return [
        {
          ...known,
          show:
            ["basicInfo", "detail"].includes(known.key) || entry.show !== false,
        },
      ];
    });
    tabSettings.value = [
      ...restored,
      ...defaultTabs
        .filter((tab) => !seen.has(tab.key))
        .map((tab) => ({ ...tab, show: true })),
    ];
  } catch (error) {
    console.error("读取用例详情显示设置失败", error);
  }
}
function saveTabSettings() {
  try {
    localStorage.setItem(settingsKey(), JSON.stringify(tabSettings.value));
    if (!visibleTabs.value.some((tab) => tab.key === activeTab.value))
      activeTab.value = "detail";
  } catch (error) {
    console.error("保存用例详情显示设置失败", error);
    message.error("保存显示设置失败");
  }
}
async function toggleFollow() {
  followBusy.value = true;
  try {
    await caseFeaturesApi.follow(
      props.projectId,
      props.caseId,
      !followed.value,
    );
    followed.value = !followed.value;
    await loadChanges();
  } catch (error) {
    console.error("关注用例失败", error);
  } finally {
    followBusy.value = false;
  }
}
loadTabSettings();
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
let loadSequence = 0;
async function load() {
  if (!props.caseId) return;
  const sequence = ++loadSequence,
    projectId = props.projectId,
    caseId = props.caseId;
  loading.value = true;
  item.value = undefined;
  try {
    const [record, state, history, links, templates] = await Promise.all([
      testCaseApi.getTestCase(projectId, caseId),
      caseFeaturesApi.followState(projectId, caseId),
      caseFeaturesApi.changes(projectId, caseId),
      caseFeaturesApi.usage(projectId, caseId),
      caseFeaturesApi.templates(projectId),
    ]);
    if (
      sequence !== loadSequence ||
      projectId !== props.projectId ||
      caseId !== props.caseId
    )
      return;
    item.value = record;
    followed.value = state.followed;
    changes.value = history;
    usage.value = links;
    template.value = templates.find((t) => t.id === record.templateId);
  } catch (error) {
    console.error("加载用例详情失败", error);
  } finally {
    if (sequence === loadSequence) loading.value = false;
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
    activeTab.value = "detail";
    load();
  },
  { immediate: true },
);
</script>
<style scoped>
.case-detail {
  padding: 0;
}
.text {
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  margin: 8px 0;
  max-height: 400px;
  overflow: auto;
}
.case-detail-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}
.case-detail-title {
  display: flex;
  gap: 4px;
  min-width: 0;
  font-weight: 500;
  overflow-wrap: anywhere;
}
.case-detail-tabs :deep(.ant-tabs-nav) {
  margin-bottom: 16px;
}
.tab-setting-row {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 0;
}
.tab-drag-handle {
  cursor: grab;
}
.custom-fields {
  margin-top: 16px;
}
</style>
