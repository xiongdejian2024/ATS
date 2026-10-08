<template>
  <div class="test-plans-container">
    <PlanNavigator
      :project-id="projectId"
      :modules="groupModules"
      :groups="planGroups"
      :plans="navigationPlans"
      :selected-key="navigationKey"
      @select="selectNavigation"
      @create-plan="createPlan"
      @create-group="openGroup()"
      @module-action="moduleAction"
      @group-action="groupAction"
    />
    <section class="plan-workspace">
      <header class="plan-workspace-header">
        <strong
          >{{ navigationTitle }} <span>({{ pagination.total }})</span></strong
        ><a-space
          ><a-input-search
            v-if="advancedConditions === undefined"
            v-model:value="searchValue"
            placeholder="搜索计划名称或编号"
            style="width: 187px"
            allow-clear
            @search="handleSearch"
            @change="handleSearchChange" /><a-button
            v-if="advancedConditions === undefined"
            @click="filtersOpen = !filtersOpen"
            >筛选</a-button
          ><a-button aria-label="刷新计划" @click="refreshPlans"
            ><ReloadOutlined /></a-button
        ></a-space>
      </header>
      <WorkspaceAdvancedFilters
        v-if="projectId"
        ref="advancedEditor"
        :key="scopeIdentity"
        :project-id="projectId"
        namespace="plan-index"
        label="测试计划首页视图"
        :modules="groupModules.map((m) => ({ ...m, count: 0 }))"
        :api="planIndexViewApi"
        :load-fields="loadAdvancedFields"
        :conditions="advancedConditions"
        :logic="advancedLogic"
        :view-id="advancedViewId"
        :busy="groupSaving"
        @apply="applyAdvanced"
        @saving="filterSaving = $event"
      />
      <PlanWorkspaceToolbar
        ref="workspaceToolbar"
        :key="scopeIdentity"
        compact
        :project-id="projectId || ''"
        :selected-ids="selectedPlanIds"
        :groups="planGroups"
        @filter="applyWorkspaceFilter"
        @saved="
          selectedPlanIds = [];
          loadPlans();
        "
      />
      <div v-if="selectedGroup" class="selected-group-tools">
        <PlanGroupExecution
          :group-id="selectedGroup.id"
          :group-name="selectedGroup.name"
          :project-id="projectId || ''"
          :run-id="
            typeof route.query.groupRunId === 'string'
              ? route.query.groupRunId
              : undefined
          "
        />
      </div>
      <a-card
        v-if="filtersOpen && advancedConditions === undefined"
        class="filter-card"
        size="small"
      >
        <a-space wrap style="margin-bottom: 12px"
          ><a-checkbox
            v-model:checked="archivedGroups"
            @change="
              groupFilter = undefined;
              loadPlans();
            "
            >已归档计划组</a-checkbox
          ><a-button
            @click="
              groupFilter = '__ungrouped__';
              workspaceFilter.module_id = undefined;
              handleFilterChange();
            "
            >未分组计划</a-button
          ></a-space
        >
        <a-row :gutter="16" align="middle">
          <a-col :span="6">
            <a-input-search
              v-model:value="searchValue"
              placeholder="搜索计划名称或编号"
              @search="handleSearch"
              @change="handleSearchChange"
            />
          </a-col>
          <a-col :span="4">
            <a-select
              v-model:value="statusFilter"
              placeholder="状态筛选"
              style="width: 100%"
              allow-clear
              @change="handleFilterChange"
            >
              <a-select-option value="not_started">未开始</a-select-option>
              <a-select-option value="running">进行中</a-select-option>
              <a-select-option value="completed">已完成</a-select-option>
              <a-select-option value="paused">已暂停</a-select-option>
              <a-select-option value="overdue">已逾期</a-select-option>
            </a-select>
          </a-col>
          <a-col :span="4">
            <a-select
              v-model:value="typeFilter"
              placeholder="类型筛选"
              style="width: 100%"
              allow-clear
              @change="handleFilterChange"
            >
              <a-select-option value="manual">手动测试</a-select-option>
              <a-select-option value="automated">自动化测试</a-select-option>
              <a-select-option value="mixed">混合测试</a-select-option>
            </a-select>
          </a-col>
          <a-col :span="6">
            <a-range-picker
              v-model:value="dateRange"
              style="width: 100%"
              @change="handleDateFilterChange"
            />
          </a-col>
          <a-col :span="4">
            <a-space>
              <a-button @click="resetFilters">重置</a-button>
              <a-button type="primary" @click="exportPlans">
                <template #icon><DownloadOutlined /></template>
                导出本页
              </a-button>
            </a-space>
          </a-col>
        </a-row>
      </a-card>
      <div class="plan-list-content">
        <PlanGroupTable
          v-if="projectId"
          :key="scopeIdentity"
          :project-id="projectId"
          :scope-key="scopeIdentity"
          :revision="groupRevision"
          :groups="tableGroups"
          :query="planQuery"
          :busy="groupSaving || filterSaving"
          @select="(id) => selectNavigation(`group:${id}`)"
          @open="viewPlanDetail"
        />
        <!-- 计划列表 -->
        <a-card class="plans-card">
          <a-table
            :columns="columns"
            :data-source="plans"
            :loading="loading"
            :pagination="false"
            row-key="id"
            :row-selection="{
              selectedRowKeys: selectedPlanIds,
              onChange: (keys: any[]) => (selectedPlanIds = keys.map(String)),
            }"
            :scroll="{ x: 1200, y: 'calc(100vh - 330px)' }"
            @change="handleTableChange"
            size="middle"
          >
            <template #bodyCell="{ column, record }">
              <template v-if="column.key === 'name'">
                <div class="plan-name-link">
                  <div class="plan-icon">
                    <ExperimentOutlined />
                  </div>
                  <div class="plan-info">
                    <router-link
                      class="plan-name"
                      :to="{
                        name: 'TestPlanDetailPage',
                        params: { planId: record.id },
                        query: { projectId },
                      }"
                      >{{ record.name }}</router-link
                    >
                    <a-button
                      type="text"
                      size="small"
                      @click.stop="toggleFollow(record)"
                      >{{ record.followed ? "★" : "☆" }}</a-button
                    >
                    <a-tag v-for="tag in record.tags || []" :key="tag">{{
                      tag
                    }}</a-tag>
                    <a-tag v-if="record.archived">已归档</a-tag>
                    <div class="plan-subtitle">
                      {{ record.planNumber }}
                    </div>
                  </div>
                </div>
              </template>

              <template v-else-if="column.key === 'status'">
                <a-tag
                  :color="getStatusColor(record.status)"
                  class="status-tag"
                >
                  <template #icon>
                    <ClockCircleOutlined
                      v-if="record.status === 'not_started'"
                    />
                    <PlayCircleOutlined
                      v-else-if="record.status === 'running'"
                    />
                    <CheckCircleOutlined
                      v-else-if="record.status === 'completed'"
                    />
                    <PauseCircleOutlined
                      v-else-if="record.status === 'paused'"
                    />
                  </template>
                  {{ getStatusLabel(record.status) }}
                </a-tag>
              </template>

              <template v-else-if="column.key === 'planType'">
                <a-tag :color="getTypeColor(record.planType)" class="type-tag">
                  {{ getTypeLabel(record.planType) }}
                </a-tag>
              </template>

              <template v-else-if="column.key === 'progress'">
                <div
                  class="progress-wrapper"
                  @click="viewPlanDetail(record.id)"
                >
                  <div class="progress-content">
                    <div class="multi-status-progress">
                      <div
                        v-for="segment in getProgressSegments(record)"
                        :key="segment.status"
                        class="progress-segment"
                        :class="`segment-${segment.status}`"
                        :style="{ width: `${segment.percent}%` }"
                        :title="`${segment.label}: ${segment.count}`"
                      ></div>
                    </div>
                    <span class="progress-percent"
                      >{{ getProgressPercent(record) }}%</span
                    >
                  </div>
                  <div class="progress-text">
                    {{ record.executedCases || 0 }}/{{ record.totalCases || 0 }}
                  </div>
                </div>
              </template>

              <template v-else-if="column.key === 'startDate'">
                <div class="date-range-single">
                  <span v-if="record.startDate">{{
                    formatDate(record.startDate)
                  }}</span>
                  <span v-if="record.startDate && record.endDate"> 至 </span>
                  <span v-if="record.endDate">{{
                    formatDate(record.endDate)
                  }}</span>
                  <span v-if="!record.startDate && !record.endDate">-</span>
                </div>
              </template>

              <template v-else-if="column.key === 'createdAt'">
                <div>{{ formatDateTime(record.createdAt) }}</div>
              </template>

              <template v-else-if="column.key === 'actions'">
                <a-space>
                  <a-button
                    type="link"
                    size="small"
                    @click="viewPlanDetail(record.id)"
                  >
                    查看
                  </a-button>
                  <a-button
                    type="link"
                    size="small"
                    @click="editPlan(record.id)"
                    v-if="canEditPlan(record)"
                  >
                    编辑
                  </a-button>
                  <a-dropdown>
                    <a-button type="link" size="small"> 更多 </a-button>
                    <template #overlay>
                      <a-menu @click="handleActionMenuEvent($event, record)">
                        <a-menu-item key="workspace">用例与测试套</a-menu-item>
                        <a-menu-item
                          key="execute"
                          v-if="canExecutePlan(record)"
                        >
                          执行
                        </a-menu-item>
                        <a-menu-item key="pause" v-if="canPausePlan(record)">
                          停止执行
                        </a-menu-item>
                        <a-menu-item key="resume" v-if="canResumePlan(record)">
                          重新执行
                        </a-menu-item>
                        <a-menu-item
                          key="complete"
                          v-if="canCompletePlan(record)"
                        >
                          完成
                        </a-menu-item>
                        <a-menu-divider />
                        <a-menu-item key="clone">复制</a-menu-item>
                        <a-menu-item
                          key="delete"
                          danger
                          v-if="canDeletePlan(record)"
                        >
                          删除
                        </a-menu-item>
                      </a-menu>
                    </template>
                  </a-dropdown>
                </a-space>
              </template>
            </template>
          </a-table>
        </a-card>

        <!-- 固定底部分页器 -->
        <div class="fixed-footer">
          <a-pagination
            v-model:current="pagination.current"
            v-model:page-size="pagination.pageSize"
            :total="pagination.total"
            :show-size-changer="true"
            :show-quick-jumper="true"
            :show-total="paginationTotal"
            @change="handlePaginationChange"
            @show-size-change="handlePaginationChange"
          />
        </div>
      </div>
    </section>

    <a-modal
      :open="groupModal"
      :closable="!groupSaving"
      :keyboard="!groupSaving"
      :mask-closable="!groupSaving"
      :cancel-button-props="{ disabled: groupSaving }"
      @cancel="closeGroup"
      :title="groupId ? '编辑计划组' : '新建计划组'"
      @ok="saveGroup"
      :confirm-loading="groupSaving"
    >
      <a-form layout="vertical"
        ><a-form-item label="计划组名称" required
          ><a-input
            :disabled="groupSaving"
            v-model:value="groupForm.name"
            :maxlength="100" /></a-form-item
        ><a-form-item label="说明"
          ><a-textarea
            :disabled="groupSaving"
            v-model:value="groupForm.description"
            :rows="3" /></a-form-item
        ><a-form-item label="计划模块"
          ><a-select
            :disabled="groupSaving"
            v-model:value="groupForm.moduleId"
            allow-clear
            :options="
              groupModules.map((m) => ({ value: m.id, label: m.name }))
            " /></a-form-item
        ><a-form-item label="标签"
          ><a-select
            :disabled="groupSaving"
            v-model:value="groupForm.tags"
            mode="tags" /></a-form-item
        ><a-form-item label="归档"
          ><a-switch
            :disabled="groupSaving"
            v-model:checked="groupForm.archived" /></a-form-item
      ></a-form>
    </a-modal>

    <!-- 计划编辑对话框 -->
    <a-modal
      v-model:visible="editModalVisible"
      :title="isEditMode ? '编辑测试计划' : '新建测试计划'"
      width="800px"
      :footer="null"
      @cancel="closeEditModal"
    >
      <TestPlanEdit
        v-if="editModalVisible"
        :plan-id="editingPlanId || undefined"
        :project-id="projectId || ''"
        @save="handlePlanSaved"
        @cancel="closeEditModal"
      />
    </a-modal>

    <!-- 执行确认对话框 -->
    <a-modal
      v-model:visible="executeModalVisible"
      title="执行测试计划"
      @ok="confirmExecutePlan"
      @cancel="executeModalVisible = false"
      :confirm-loading="executing"
    >
      <a-form layout="vertical">
        <a-alert
          message="按本计划已保存的执行配置创建新批次。自动化用例使用各测试套绑定的 Agent 节点；手工用例在批次报告中回填。"
          type="info"
          show-icon
          style="margin-bottom: 16px"
        />
        <a-form-item label="执行说明">
          <a-textarea
            v-model:value="executeForm.notes"
            placeholder="请输入执行说明（可选）"
            :rows="3"
          />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, onBeforeUnmount } from "vue";
import {
  useRouter,
  useRoute,
  onBeforeRouteLeave,
  onBeforeRouteUpdate,
} from "vue-router";
import { message, Modal } from "ant-design-vue";
import {
  ReloadOutlined,
  DownloadOutlined,
  ExperimentOutlined,
  PlayCircleOutlined,
  PauseCircleOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
} from "@ant-design/icons-vue";
import type { Dayjs } from "dayjs";
import type { TestPlan, Environment, Project, CaseStatusCounts } from "@/types";
import { testPlanApi } from "@/api/testPlan";
import { planOrchestrationApi, type PlanGroup } from "@/api/planOrchestration";
import { useProjectStore } from "@/stores/project";
import TestPlanEdit from "@/components/TestPlan/TestPlanEdit.vue";
import PlanWorkspaceToolbar from "@/components/TestPlan/PlanWorkspaceToolbar.vue";
import PlanGroupExecution from "@/components/TestPlan/PlanGroupExecution.vue";
import PlanNavigator from "@/components/TestPlan/PlanNavigator.vue";
import {
  planWorkspaceApi,
  planIndexViewApi,
  type PlanModule,
} from "@/api/planWorkspace";
import WorkspaceAdvancedFilters from "@/components/Table/WorkspaceAdvancedFilters.vue";
import PlanGroupTable from "@/components/TestPlan/PlanGroupTable.vue";
import { planIndexFilterFields } from "@/components/TestPlan/planIndexFilterFields";
import type {
  FilterCondition,
  FilterLogic,
} from "@/components/TestCase/advancedFilter";
import { useUserStore } from "@/stores/user";

const router = useRouter();
const route = useRoute();
const projectStore = useProjectStore();

// 项目选择
const projects = computed<Project[]>(() => projectStore.projects);
const projectId = computed<string | undefined>(() => {
  if (typeof route.query.projectId === "string") return route.query.projectId;
  if (projectStore.currentProject) return projectStore.currentProject.id;
  return projects.value[0]?.id;
});

const userStore = useUserStore();
const scopeIdentity = computed(() =>
  JSON.stringify([projectId.value, userStore.user?.id]),
);
let scopeEpoch = 0,
  live = true;
const scopeSnapshot = () => JSON.stringify([scopeEpoch, scopeIdentity.value]);
const advancedEditor = ref<{ beforeClose: () => Promise<boolean> }>();
const advancedConditions = ref<FilterCondition[]>();
const advancedLogic = ref<FilterLogic>("and");
const advancedViewId = ref<string>();
const filterSaving = ref(false);
async function loadAdvancedFields(id: string) {
  const [members, active, archived] = await Promise.all([
    planWorkspaceApi.members(id),
    planOrchestrationApi.groups(id),
    planOrchestrationApi.groups(id, true),
  ]);
  return planIndexFilterFields(members, [...active, ...archived]);
}
let closing = false;
const navigationCurrent = (scope: string) =>
  live &&
  scope === scopeSnapshot() &&
  !filterSaving.value &&
  !groupSaving.value;
async function beforeNavigation() {
  const scope = scopeSnapshot(),
    draft = JSON.stringify([
      groupModal.value,
      groupForm.value,
      groupBaseline.value,
    ]);
  if (!navigationCurrent(scope) || closing) return false;
  closing = true;
  try {
    if (
      !((await advancedEditor.value?.beforeClose()) ?? true) ||
      !navigationCurrent(scope) ||
      draft !==
        JSON.stringify([groupModal.value, groupForm.value, groupBaseline.value])
    )
      return false;
    if (
      groupModal.value &&
      JSON.stringify(groupForm.value) !== groupBaseline.value
    ) {
      const accepted = await new Promise<boolean>((resolve) =>
        Modal.confirm({
          title: "放弃计划组草稿？",
          onOk: () => resolve(true),
          onCancel: () => resolve(false),
        }),
      );
      if (
        !accepted ||
        !navigationCurrent(scope) ||
        draft !==
          JSON.stringify([
            groupModal.value,
            groupForm.value,
            groupBaseline.value,
          ])
      )
        return false;
      groupModal.value = false;
    }
    return navigationCurrent(scope);
  } finally {
    if (live && scope === scopeSnapshot()) closing = false;
  }
}
onBeforeRouteLeave(beforeNavigation);
onBeforeRouteUpdate(beforeNavigation);
onBeforeUnmount(() => {
  live = false;
  ++scopeEpoch;
  ++planLoadSequence;
});
function applyAdvanced(
  conditions: FilterCondition[] | undefined,
  logic: FilterLogic,
  viewId?: string,
) {
  if (!live || groupSaving.value) return;
  advancedConditions.value = conditions;
  advancedLogic.value = logic;
  advancedViewId.value = viewId;
  searchValue.value = "";
  statusFilter.value = undefined;
  typeFilter.value = undefined;
  dateRange.value = null;
  workspaceFilter.value = { followed: false, archived: false };
  groupFilter.value = undefined;
  filtersOpen.value = false;
  selectedPlanIds.value = [];
  pagination.value.current = 1;
  void loadPlans();
}

// 响应式数据
const loading = ref(false);
const plans = ref<TestPlan[]>([]);
const selectedPlanIds = ref<string[]>([]);
const workspaceFilter = ref<{
  module_id?: string;
  followed: boolean;
  archived: boolean;
  tag?: string;
}>({
  module_id:
    typeof route.query.moduleId === "string" ? route.query.moduleId : undefined,
  followed: false,
  archived: false,
});
async function applyWorkspaceFilter(value: typeof workspaceFilter.value) {
  const scope = scopeSnapshot();
  if (!(await beforeNavigation()) || !navigationCurrent(scope)) return;
  advancedConditions.value = undefined;
  advancedViewId.value = undefined;
  advancedLogic.value = "and";
  workspaceFilter.value = {
    ...value,
    module_id: workspaceFilter.value.module_id,
  };
  pagination.value.current = 1;
  void loadPlans();
}
async function toggleFollow(plan: TestPlan & { followed?: boolean }) {
  try {
    await planWorkspaceApi.follow(plan.id, !plan.followed);
    await loadPlans();
  } catch (error) {
    console.error("关注计划失败", error);
    message.error("关注失败");
  }
}

const selectedPlan = ref<TestPlan | null>(null);
const environments = ref<Environment[]>([]);

// 筛选条件
const searchValue = ref("");
const statusFilter = ref<string>();
const typeFilter = ref<string>();
const dateRange = ref<[Dayjs, Dayjs] | null>(null);

// 模态框状态
const editModalVisible = ref(false);
const executeModalVisible = ref(false);
const isEditMode = ref(false);
const editingPlanId = ref<string | null>(null);
const executing = ref(false);

// 执行表单
const executeForm = ref({
  environmentId: "",
  notes: "",
});

// 分页配置
const pagination = ref({
  current: 1,
  pageSize: 20,
  total: 0,
  showSizeChanger: true,
  showQuickJumper: true,
  showTotal: (total: number, range: [number, number]) =>
    `第 ${range[0]}-${range[1]} 条，共 ${total} 条`,
});

// 表格列配置
const columns = [
  {
    title: "计划信息",
    key: "name",
    dataIndex: "name",
    width: 200,
    align: "left" as const,
  },
  {
    title: "状态",
    key: "status",
    dataIndex: "status",
    width: 100,
    align: "center" as const,
  },
  {
    title: "类型",
    key: "planType",
    dataIndex: "planType",
    width: 100,
    align: "center" as const,
  },
  {
    title: "执行进度",
    key: "progress",
    width: 150,
    align: "center" as const,
  },
  {
    title: "时间范围",
    key: "startDate",
    width: 180,
    align: "left" as const,
  },
  {
    title: "创建时间",
    key: "createdAt",
    dataIndex: "createdAt",
    width: 180,
    align: "left" as const,
  },
  {
    title: "操作",
    key: "actions",
    width: 150,
    align: "center" as const,
    fixed: "right" as const,
  },
];

const groupFilter = ref<string | undefined>(
  typeof route.query.groupId === "string" ? route.query.groupId : undefined,
);
const archivedGroups = ref(false);
const groupModules = ref<PlanModule[]>([]);
const navigationPlans = ref<TestPlan[]>([]);
const workspaceToolbar = ref<InstanceType<typeof PlanWorkspaceToolbar>>();
const filtersOpen = ref(false);
const planGroups = ref<PlanGroup[]>([]);
const selectedGroup = computed(() =>
  planGroups.value.find((g) => g.id === groupFilter.value),
);
const groupModal = ref(false);
const groupSaving = ref(false);
const groupRevision = ref(0);
let groupOperation = 0;
const groupBaseline = ref("");
const groupId = ref("");
const groupForm = ref({
  name: "",
  description: "",
  tags: [] as string[],
  archived: false,
  moduleId: null as string | null,
});
async function openGroup(group?: PlanGroup) {
  const scope = scopeSnapshot();
  if (!(await beforeNavigation()) || !navigationCurrent(scope)) return;
  groupId.value = group?.id || "";
  groupForm.value = {
    name: group?.name || "",
    description: group?.description || "",
    tags: [...(group?.tags || [])],
    archived: group?.archived || false,
    moduleId: group?.moduleId || workspaceFilter.value.module_id || null,
  };
  groupBaseline.value = JSON.stringify(groupForm.value);
  groupModal.value = true;
}
async function closeGroup() {
  const scope = scopeSnapshot();
  if ((await beforeNavigation()) && navigationCurrent(scope))
    groupModal.value = false;
}
async function saveGroup() {
  if (!live || !projectId.value || groupSaving.value || filterSaving.value)
    return;
  if (!groupForm.value.name.trim()) {
    message.warning("请输入计划组名称");
    return;
  }
  const scope = scopeSnapshot(),
    operation = ++groupOperation,
    id = groupId.value,
    project = projectId.value,
    body = { ...groupForm.value, tags: [...groupForm.value.tags] };
  groupSaving.value = true;
  try {
    if (id) await planOrchestrationApi.updateGroup(id, body);
    else await planOrchestrationApi.createGroup(project, body);
    if (!live || scope !== scopeSnapshot() || operation !== groupOperation)
      return;
    groupBaseline.value = JSON.stringify(body);
    if (JSON.stringify(groupForm.value) === groupBaseline.value) {
      groupModal.value = false;
      message.success("计划组已保存");
    } else message.warning("已保存提交的版本；新草稿保留，请继续保存");
    await loadPlans();
  } catch (error) {
    console.error("保存计划组失败", error);
    if (live && scope === scopeSnapshot() && operation === groupOperation)
      message.error("保存计划组失败");
  } finally {
    if (live && scope === scopeSnapshot() && operation === groupOperation)
      groupSaving.value = false;
  }
}
async function cloneGroup(id = selectedGroup.value?.id) {
  if (!live || !id || groupSaving.value || filterSaving.value) return false;
  const scope = scopeSnapshot(),
    operation = ++groupOperation;
  groupSaving.value = true;
  try {
    const group = await planOrchestrationApi.cloneGroup(id);
    if (!live || scope !== scopeSnapshot() || operation !== groupOperation)
      return false;
    groupSaving.value = false;
    if (
      (await selectNavigation(`group:${group.id}`)) &&
      live &&
      scope === scopeSnapshot() &&
      operation === groupOperation
    )
      message.success("计划组与成员计划已完整复制");
    return true;
  } catch (error) {
    console.error("复制计划组失败", error);
    if (live && scope === scopeSnapshot() && operation === groupOperation)
      message.error("复制计划组失败");
    return false;
  } finally {
    if (live && scope === scopeSnapshot() && operation === groupOperation)
      groupSaving.value = false;
  }
}
async function deleteGroup(id = selectedGroup.value?.id) {
  if (!live || !id || groupSaving.value || filterSaving.value) return false;
  const scope = scopeSnapshot(),
    operation = ++groupOperation;
  groupSaving.value = true;
  try {
    await planOrchestrationApi.deleteGroup(id);
    if (!live || scope !== scopeSnapshot() || operation !== groupOperation)
      return false;
    if (groupFilter.value === id) groupFilter.value = undefined;
    await loadPlans();
    if (!live || scope !== scopeSnapshot() || operation !== groupOperation)
      return false;
    message.success("分组已删除，计划已保留");
    return true;
  } catch (error) {
    console.error("删除计划组失败", error);
    if (live && scope === scopeSnapshot() && operation === groupOperation)
      message.error("删除失败");
    throw error;
  } finally {
    if (live && scope === scopeSnapshot() && operation === groupOperation)
      groupSaving.value = false;
  }
}

// 每次刷新加载完整导航范围，列表保留分页；序号防止旧项目响应覆盖当前页面。
let planLoadSequence = 0;
async function navigationRows(id: string) {
  const scope = scopeSnapshot(),
    archived = workspaceFilter.value.archived;
  const first = await testPlanApi.getTestPlans(id, {
    page: 1,
    size: 100,
    archived,
  });
  if (!live || scope !== scopeSnapshot()) return [];
  const normalize = (items: TestPlan[]) =>
    items.map((p) => ({
      ...p,
      groupId: (p as any).executionPolicy?.groupId || null,
    }));
  const rows = normalize(first.items || []);
  for (let page = 2; rows.length < first.total; page++) {
    const next = await testPlanApi.getTestPlans(id, {
      page,
      size: 100,
      archived,
    });
    if (!live || scope !== scopeSnapshot()) return [];
    if (!next.items?.length) break;
    rows.push(...normalize(next.items));
  }
  return rows;
}
const loadPlans = async () => {
  const id = projectId.value,
    sequence = ++planLoadSequence,
    scope = scopeSnapshot();
  if (!id) {
    plans.value = [];
    navigationPlans.value = [];
    groupModules.value = [];
    planGroups.value = [];
    pagination.value.total = 0;
    return;
  }
  loading.value = true;
  try {
    const params = {
      ...planQuery.value,
      page: pagination.value.current,
      size: pagination.value.pageSize,
    };
    const [response, groups, modules, allPlans] = await Promise.all([
      testPlanApi.getTestPlans(id, params),
      planOrchestrationApi.groups(id, archivedGroups.value),
      planWorkspaceApi.modules(id),
      navigationRows(id),
    ]);
    if (
      !live ||
      scope !== scopeSnapshot() ||
      sequence !== planLoadSequence ||
      id !== projectId.value
    )
      return;
    plans.value = response.items || [];
    pagination.value.total = response.total || 0;
    planGroups.value = groups;
    groupModules.value = modules;
    navigationPlans.value = allPlans;
    ++groupRevision.value;
    console.info("测试计划列表与导航已加载", {
      projectId: id,
      total: response.total,
      navigationCount: allPlans.length,
    });
  } catch (error) {
    console.error("加载测试计划列表与导航失败", error);
    if (live && scope === scopeSnapshot() && sequence === planLoadSequence)
      message.error("加载测试计划失败");
  } finally {
    if (live && scope === scopeSnapshot() && sequence === planLoadSequence)
      loading.value = false;
  }
};
const planQuery = computed(() => ({
  ...(advancedConditions.value === undefined
    ? {
        ...workspaceFilter.value,
        search: searchValue.value || undefined,
        status: statusFilter.value || undefined,
        type: typeFilter.value || undefined,
        startDate: dateRange.value?.[0]?.format("YYYY-MM-DD"),
        endDate: dateRange.value?.[1]?.format("YYYY-MM-DD"),
      }
    : {
        filters: JSON.stringify({
          conditions: advancedConditions.value,
          logic: advancedLogic.value,
        }),
      }),
  module_id: workspaceFilter.value.module_id,
  include_descendants: true,
  group_id: groupFilter.value || undefined,
}));
const tableGroups = computed(() => {
  if (groupFilter.value === "__ungrouped__") return [];
  if (groupFilter.value)
    return planGroups.value.filter((g) => g.id === groupFilter.value);
  const module = workspaceFilter.value.module_id;
  if (!module) return planGroups.value;
  const ids = new Set([module]);
  let count = 0;
  while (count !== ids.size) {
    count = ids.size;
    for (const m of groupModules.value)
      if (m.parentId && ids.has(m.parentId)) ids.add(m.id);
  }
  return planGroups.value.filter((g) =>
    module === "__ungrouped__"
      ? !g.moduleId
      : g.moduleId && ids.has(g.moduleId),
  );
});
const navigationKey = computed(() =>
  groupFilter.value
    ? `group:${groupFilter.value}`
    : workspaceFilter.value.module_id
      ? `module:${workspaceFilter.value.module_id}`
      : "all",
);
const navigationTitle = computed(() =>
  groupFilter.value === "__ungrouped__"
    ? "未分组计划"
    : selectedGroup.value?.name ||
      groupModules.value.find((m) => m.id === workspaceFilter.value.module_id)
        ?.name ||
      "全部测试计划",
);
async function selectNavigation(key: string) {
  const scope = scopeSnapshot();
  if (!(await beforeNavigation()) || !navigationCurrent(scope)) return false;
  if (key.startsWith("plan:")) {
    return await viewPlanDetail(key.slice(5));
  }
  groupFilter.value = key.startsWith("group:") ? key.slice(6) : undefined;
  workspaceFilter.value.module_id = key.startsWith("module:")
    ? key.slice(7)
    : undefined;
  pagination.value.current = 1;
  selectedPlanIds.value = [];
  await router.replace({
    query: {
      projectId: projectId.value,
      groupId: groupFilter.value,
      moduleId: workspaceFilter.value.module_id,
    },
  });
  if (!live || scope !== scopeSnapshot()) return false;
  await loadPlans();
  return live && scope === scopeSnapshot();
}
async function moduleAction(action: string, id?: string) {
  const scope = scopeSnapshot();
  if (!(await beforeNavigation()) || !navigationCurrent(scope)) return;
  if (action === "create") workspaceToolbar.value?.editModule(undefined, id);
  else if (action === "edit")
    workspaceToolbar.value?.editModule(
      groupModules.value.find((m) => m.id === id),
    );
  else if (id)
    Modal.confirm({
      title: "删除模块？",
      content: "模块内计划将保留。请先处理子模块。",
      okText: "删除",
      cancelText: "取消",
      onOk: async () => {
        if (
          !live ||
          scope !== scopeSnapshot() ||
          !(await beforeNavigation()) ||
          !navigationCurrent(scope)
        )
          throw new Error("项目已切换或操作进行中");
        await workspaceToolbar.value?.removeModule(id);
        if (live && scope === scopeSnapshot()) await selectNavigation("all");
      },
    });
}
async function groupAction(action: string, id: string) {
  const scope = scopeSnapshot();
  if (
    !(await selectNavigation(`group:${id}`)) ||
    !live ||
    scope !== scopeSnapshot()
  )
    return;
  if (action === "edit")
    await openGroup(planGroups.value.find((g) => g.id === id));
  else if (action === "copy") await cloneGroup(id);
  else
    Modal.confirm({
      title: "删除计划组？",
      content: "组内计划将保留并移至未分组。",
      okText: "删除",
      cancelText: "取消",
      onOk: async () => {
        if (
          !live ||
          scope !== scopeSnapshot() ||
          !(await beforeNavigation()) ||
          !navigationCurrent(scope)
        )
          throw new Error("项目已切换或操作进行中");
        await deleteGroup(id);
      },
    });
}

const loadEnvironments = async () => {
  try {
    // 这里应该调用环境API
    environments.value = [];
  } catch (error) {
    console.error("Failed to load environments:", error);
  }
};

const handleSearch = () => {
  pagination.value.current = 1;
  loadPlans();
};

const handleSearchChange = () => {
  // 搜索防抖
  clearTimeout((handleSearchChange as any).timer);
  (handleSearchChange as any).timer = setTimeout(() => {
    handleSearch();
  }, 500);
};

const handleFilterChange = () => {
  pagination.value.current = 1;
  loadPlans();
};

const handleDateFilterChange = () => {
  pagination.value.current = 1;
  loadPlans();
};

const resetFilters = () => {
  searchValue.value = "";
  groupFilter.value = undefined;
  statusFilter.value = undefined;
  typeFilter.value = undefined;
  dateRange.value = null;
  pagination.value.current = 1;
  loadPlans();
};

const handleTableChange = (paginationConfig: any) => {
  pagination.value.current = paginationConfig.current;
  pagination.value.pageSize = paginationConfig.pageSize;
  loadPlans();
};

const handlePaginationChange = (page: number, pageSize: number) => {
  pagination.value.current = page;
  pagination.value.pageSize = pageSize;
  loadPlans();
};

const createPlan = () => {
  isEditMode.value = false;
  editingPlanId.value = null;
  editModalVisible.value = true;
};

const editPlan = (planId: string) => {
  isEditMode.value = true;
  editingPlanId.value = planId;
  editModalVisible.value = true;
};

const viewPlanDetail = async (planId: string) => {
  const scope = scopeSnapshot();
  if (!(await beforeNavigation()) || !navigationCurrent(scope)) return false;
  await router.push({
    name: "TestPlanDetailPage",
    params: { planId },
    query: {
      projectId: projectId.value,
      ...(route.query.runId ? { runId: route.query.runId } : {}),
    },
  });
  return true;
};

const viewPlanExecution = (plan: TestPlan) => {
  // 获取项目名称
  const project = projects.value.find((p) => p.id === plan.projectId);
  const projectName = project?.name || "default";

  // 构建URL：/test-plans/{projectName}/{planName}?planId={planId}
  const encodedProjectName = encodeURIComponent(projectName);
  const encodedPlanName = encodeURIComponent(plan.name);
  router.push({
    path: `/test-plans/${encodedProjectName}/${encodedPlanName}`,
    query: {
      planId: plan.id,
    },
  });
};

const closeEditModal = () => {
  editModalVisible.value = false;
  isEditMode.value = false;
  editingPlanId.value = null;
};

const handlePlanSaved = () => {
  closeEditModal();
  // 重置到第一页并刷新列表，确保新创建的计划能显示
  pagination.value.current = 1;
  loadPlans();
};

const handleActionClick = (action: string, plan: TestPlan) => {
  switch (action) {
    case "workspace":
      viewPlanExecution(plan);
      break;
    case "execute":
      executePlan(plan);
      break;
    case "pause":
      pausePlan(plan);
      break;
    case "resume":
      resumePlan(plan);
      break;
    case "complete":
      completePlan(plan);
      break;
    case "clone":
      clonePlan(plan);
      break;
    case "delete":
      deletePlan(plan);
      break;
  }
};

const executePlan = (plan: TestPlan) => {
  executeForm.value = {
    environmentId: "",
    notes: "",
  };
  executeModalVisible.value = true;
  selectedPlan.value = plan;
};

const confirmExecutePlan = async () => {
  executing.value = true;
  try {
    // 执行计划（如果是手动测试，environmentId 可以为空）
    await testPlanApi.executePlan(
      selectedPlan.value!.id,
      executeForm.value.environmentId || undefined,
      executeForm.value.notes,
    );
    message.success("计划执行启动成功");
    executeModalVisible.value = false;
    loadPlans();
  } catch (error) {
    console.error("Failed to execute plan:", error);
    message.error("计划执行失败");
  } finally {
    executing.value = false;
  }
};

const pausePlan = async (plan: TestPlan) => {
  try {
    await testPlanApi.stopPlanExecution(plan.id);
    message.success("已请求停止计划执行");
    loadPlans();
  } catch (error) {
    message.error("暂停计划失败");
  }
};

const resumePlan = async (plan: TestPlan) => {
  try {
    await testPlanApi.resumePlan(plan.id);
    message.success("已创建新的执行批次");
    loadPlans();
  } catch (error) {
    message.error("恢复计划失败");
  }
};

const completePlan = async (plan: TestPlan) => {
  try {
    await testPlanApi.completePlan(plan.id);
    message.success("计划已完成");
    loadPlans();
  } catch (error) {
    message.error("完成计划失败");
  }
};

const clonePlan = async (plan: TestPlan) => {
  try {
    if (!projectId.value) {
      message.warning("请先选择项目");
      return;
    }
    await testPlanApi.clonePlan(projectId.value, plan.id);
    message.success("计划复制成功");
    loadPlans();
  } catch (error) {
    message.error("复制计划失败");
  }
};

const deletePlan = async (plan: TestPlan) => {
  // 这里应该显示确认对话框
  try {
    await testPlanApi.deletePlan(plan.id);
    message.success("计划删除成功");
    loadPlans();
  } catch (error) {
    message.error("删除计划失败");
  }
};

const refreshPlans = () => {
  loadPlans();
};

const exportPlans = () => {
  const blob = new Blob([JSON.stringify(plans.value, null, 2)], {
    type: "application/json",
  });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `ATS-测试计划-第${pagination.value.current}页.json`;
  link.click();
  URL.revokeObjectURL(url);
};

// 权限检查方法
const canEditPlan = (plan: TestPlan) => {
  return plan.status === "not_started" || plan.status === "paused";
};

const canExecutePlan = (plan: TestPlan) => {
  return plan.status === "not_started" || plan.status === "paused";
};

const canPausePlan = (plan: TestPlan) => {
  return plan.status === "running";
};

const canResumePlan = (plan: TestPlan) => {
  return plan.status === "paused";
};

const canCompletePlan = (plan: TestPlan) => {
  return plan.status === "running";
};

const canDeletePlan = (plan: TestPlan) => {
  return plan.status === "not_started" || plan.status === "completed";
};

// 辅助方法
const getStatusColor = (status: string) => {
  const colorMap: Record<string, string> = {
    not_started: "default",
    running: "blue",
    completed: "green",
    paused: "orange",
    overdue: "red",
  };
  return colorMap[status] || "default";
};

const getStatusLabel = (status: string) => {
  const labelMap: Record<string, string> = {
    not_started: "未开始",
    running: "进行中",
    completed: "已完成",
    paused: "已暂停",
    overdue: "已逾期",
  };
  return labelMap[status] || status;
};

const getTypeColor = (type: string) => {
  const colorMap: Record<string, string> = {
    manual: "blue",
    automated: "green",
    mixed: "#722ed1",
  };
  return colorMap[type] || "default";
};

const getTypeLabel = (type: string) => {
  const labelMap: Record<string, string> = {
    manual: "手动测试",
    automated: "自动化测试",
    mixed: "混合测试",
  };
  return labelMap[type] || type;
};

const getProgressPercent = (plan: TestPlan) => {
  const total = plan.totalCases || 0;
  const executed = plan.executedCases || 0;
  return total > 0 ? Math.round((executed / total) * 100) : 0;
};

// 获取分段进度条数据
const getProgressSegments = (plan: TestPlan) => {
  const total = plan.totalCases || 0;
  if (total === 0) {
    return [];
  }

  const statusCounts = plan.caseStatusCounts || {
    pending: 0,
    pass: 0,
    fail: 0,
    broken: 0,
    error: 0,
    skip: 0,
  };

  // 定义状态顺序和标签
  const statusOrder: Array<{
    status: keyof CaseStatusCounts;
    label: string;
    color: string;
  }> = [
    { status: "pass", label: "通过", color: "#52c41a" },
    { status: "fail", label: "失败", color: "#ff4d4f" },
    { status: "broken", label: "阻塞", color: "#faad14" },
    { status: "error", label: "错误", color: "#ff4d4f" },
    { status: "skip", label: "跳过", color: "#bfbfbf" },
    { status: "pending", label: "待执行", color: "#d9d9d9" },
  ];

  const segments: Array<{
    status: string;
    label: string;
    percent: number;
    count: number;
    color: string;
  }> = [];

  statusOrder.forEach(({ status, label, color }) => {
    const count = statusCounts[status] || 0;
    if (count > 0) {
      segments.push({
        status,
        label,
        percent: Math.round((count / total) * 100),
        count,
        color,
      });
    }
  });

  return segments;
};

const formatDate = (date: string) => {
  if (!date) return "-";
  const d = new Date(date);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${year}/${month}/${day}`;
};

const formatDateTime = (dateStr: string) => {
  if (!dateStr) return "-";
  // 如果是 ISO 格式，直接返回（如 2025-12-25T14:39:26）
  if (dateStr.includes("T")) {
    return dateStr.replace("T", " ").substring(0, 19);
  }
  // 否则格式化
  const d = new Date(dateStr);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  const hours = String(d.getHours()).padStart(2, "0");
  const minutes = String(d.getMinutes()).padStart(2, "0");
  const seconds = String(d.getSeconds()).padStart(2, "0");
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
};

// 生命周期
onMounted(async () => {
  // 确保项目列表已加载
  if (projects.value.length === 0) {
    await projectStore.fetchProjects();
  }
  // 如果没有当前项目，设置第一个项目为当前项目
  if (!projectStore.currentProject && projects.value.length > 0) {
    const linked = projects.value.find(
      (project) => project.id === route.query.projectId,
    );
    projectStore.setCurrentProject(linked || projects.value[0]);
  }
  loadPlans();
  loadEnvironments();
  if (typeof route.query.planId === "string")
    await viewPlanDetail(route.query.planId);
});

watch(
  () => [route.query.groupId, route.query.moduleId],
  ([group, module]) => {
    const g = typeof group === "string" ? group : undefined,
      m = typeof module === "string" ? module : undefined;
    if (g !== groupFilter.value || m !== workspaceFilter.value.module_id) {
      groupFilter.value = g;
      workspaceFilter.value.module_id = m;
      pagination.value.current = 1;
      void loadPlans();
    }
  },
);
watch(
  () => route.query.planId,
  (value) => {
    if (typeof value === "string") void viewPlanDetail(value);
  },
);

// 项目/用户每次切换都产生新代次，返回原项目也不接收旧读写 ACK。
watch(
  scopeIdentity,
  () => {
    ++scopeEpoch;
    closing = false;
    ++groupOperation;
    ++planLoadSequence;
    groupFilter.value =
      typeof route.query.groupId === "string" ? route.query.groupId : undefined;
    workspaceFilter.value = {
      module_id:
        typeof route.query.moduleId === "string"
          ? route.query.moduleId
          : undefined,
      followed: false,
      archived: false,
    };
    searchValue.value = "";
    statusFilter.value = undefined;
    typeFilter.value = undefined;
    dateRange.value = null;
    advancedConditions.value = undefined;
    advancedLogic.value = "and";
    advancedViewId.value = undefined;
    filterSaving.value = false;
    navigationPlans.value = [];
    groupModules.value = [];
    planGroups.value = [];
    plans.value = [];
    pagination.value.total = 0;
    pagination.value.current = 1;
    selectedPlanIds.value = [];
    groupModal.value = false;
    groupBaseline.value = "";
    groupSaving.value = false;
    editModalVisible.value = false;
    executeModalVisible.value = false;
    loading.value = false;
    if (projectId.value) {
      void loadPlans();
      void loadEnvironments();
    }
  },
  { flush: "sync" },
);

// 暴露方法
defineExpose({
  refreshPlans,
});
const paginationTotal = (total: number) => `共 ${total} 条`;
const handleActionMenuEvent = (
  info: { key: string | number },
  record: TestPlan,
) => handleActionClick(String(info.key), record);
</script>

<style scoped>
.plan-workspace {
  flex: 1;
  min-width: 0;
  min-height: 0;
  display: flex;
  flex-direction: column;
  background: #fff;
  padding: 16px;
}
.plan-workspace-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}
.plan-workspace-header strong span {
  font-weight: 400;
  color: #86909c;
}
.plan-list-content {
  flex: 1;
  min-height: 0;
  overflow: auto;
}
.plan-workspace :deep(.plans-card) {
  border: 0;
}
.plan-workspace :deep(.plans-card > .ant-card-body) {
  padding: 0;
}
.plan-workspace .fixed-footer {
  margin-bottom: 0;
  padding: 12px 0;
}
.selected-group-tools {
  padding: 8px 0;
}
.plan-workspace :deep(.workspace-toolbar) {
  padding: 12px 0;
}
.plan-workspace .filter-card {
  margin-bottom: 12px;
}
@media (max-width: 768px) {
  .test-plans-container {
    flex-direction: column !important;
  }
  .plan-workspace {
    padding: 12px;
  }
  .plan-workspace-header .ant-space {
    flex-wrap: wrap;
  }
  .plan-workspace :deep(.ant-table-cell-fix-right) {
    position: static !important;
  }
}

.plan-groups {
  margin-bottom: 12px;
}
.test-plans-container {
  height: 100%;
  display: flex;
  flex-direction: row;
  background: #f5f5f5;
  overflow: hidden;
}

/* 固定顶部工具栏和筛选区域 */
.fixed-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: #f5f5f5;
  border-bottom: 1px solid #f0f0f0;
  flex-shrink: 0;
}

.content-wrapper {
  padding: 16px;
}

.filter-card {
  margin-bottom: 0;
}

/* 可滚动内容区域 */
.scrollable-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.plans-card {
  margin: 0;
}

/* 固定底部分页器和批量操作栏 */
.fixed-footer {
  position: sticky;
  bottom: 0;
  z-index: 100;
  background: #fff;
  border-top: 1px solid #f0f0f0;
  padding: 12px 16px;
  margin-bottom: 20px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  flex-shrink: 0;
}

.plan-name-link {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  text-decoration: none;
}

.plan-name-disabled {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: not-allowed;
}

.plan-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: #e6f7ff;
  color: #1890ff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  transition: all 0.3s;
  flex-shrink: 0;
}

.plan-name-link:hover .plan-icon {
  background: #1890ff;
  color: #fff;
  transform: scale(1.1);
  box-shadow: 0 2px 8px rgba(24, 144, 255, 0.3);
}

.plan-icon.icon-disabled {
  background: #f5f5f5;
  color: #d9d9d9;
}

.plan-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-width: 0;
}

.plan-name {
  font-weight: 500;
  font-size: 14px;
  color: #1890ff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.plan-name-disabled .plan-name {
  color: #8c8c8c;
}

.plan-subtitle {
  font-size: 12px;
  color: #8c8c8c;
  margin-top: 2px;
}

.status-tag {
  border-radius: 12px;
  min-width: 80px;
  text-align: center;
}

.type-tag {
  border-radius: 4px;
}

.progress-wrapper {
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.progress-wrapper:hover {
  background-color: #f5f5f5;
}

.progress-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.multi-status-progress {
  display: flex;
  flex: 1;
  height: 8px;
  border-radius: 4px;
  overflow: hidden;
  background-color: #f0f0f0;
}

.progress-percent {
  font-size: 12px;
  color: #262626;
  font-weight: 500;
  white-space: nowrap;
  min-width: 40px;
  text-align: right;
}

.progress-segment {
  height: 100%;
  transition: width 0.3s ease;
  min-width: 0;
}

.progress-segment.segment-pass {
  background-color: #52c41a;
}

.progress-segment.segment-fail {
  background-color: #ff4d4f;
}

.progress-segment.segment-broken {
  background-color: #faad14;
}

.progress-segment.segment-error {
  background-color: #ff4d4f;
}

.progress-segment.segment-skip {
  background-color: #bfbfbf;
}

.progress-segment.segment-pending {
  background-color: #d9d9d9;
}

.progress-text {
  font-size: 12px;
  color: #8c8c8c;
  text-align: center;
  margin-top: 4px;
}

.date-range {
  font-size: 12px;
  color: #8c8c8c;
}

/* 表格对齐样式 */
.plans-card :deep(.ant-table) {
  table-layout: fixed;
}

/* 修复表格固定列重叠问题 - 增强版 */
.plans-card :deep(.ant-table-cell-fix-right) {
  background: #fff !important;
  z-index: 10 !important; /* 提高层级 */
}

/* 表头固定列背景色需要与表头一致 */
.plans-card :deep(.ant-table-thead > tr > th.ant-table-cell-fix-right) {
  background: #fafafa !important; /* 默认表头背景 */
  z-index: 20 !important; /* 表头层级更高 */
}

/* Hover 状态下的背景色 */
.plans-card :deep(.ant-table-tbody > tr:hover > td.ant-table-cell-fix-right) {
  background: #fafafa !important;
}

/* 兼容可能存在的其他固定列类名 */
.plans-card :deep(.ant-table-fix-right),
.plans-card :deep(.ant-table-fixed-right) {
  background: #fff !important;
}

.plans-card :deep(.ant-table-thead > tr > th) {
  white-space: nowrap;
  padding: 12px 16px;
}

.plans-card :deep(.ant-table-tbody > tr > td) {
  white-space: nowrap;
  padding: 12px 16px;
  vertical-align: middle;
}

/* 确保计划信息列左对齐 */
.plans-card :deep(.ant-table-thead > tr > th:first-child),
.plans-card :deep(.ant-table-tbody > tr > td:first-child) {
  text-align: left;
}

.plans-card :deep(.ant-table-tbody > tr > td:first-child .plan-name-link) {
  text-align: left;
  display: block;
}

.plans-card :deep(.ant-table-tbody > tr > td:first-child .plan-subtitle) {
  text-align: left;
}

/* 时间范围列左对齐 */
.plans-card :deep(.ant-table-thead > tr > th:nth-child(5)),
.plans-card :deep(.ant-table-tbody > tr > td:nth-child(5)) {
  text-align: left;
}

.date-range-single {
  white-space: nowrap;
}

.plans-card :deep(.ant-table-tbody > tr > td:nth-child(5) .date-range) {
  text-align: left;
}

/* 创建时间列左对齐 */
.plans-card :deep(.ant-table-thead > tr > th:nth-child(6)),
.plans-card :deep(.ant-table-tbody > tr > td:nth-child(6)) {
  text-align: left;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .content-wrapper {
    padding: 16px;
  }

  .plans-grid {
    gap: 16px;
  }
}

@media (max-width: 992px) {
  .content-wrapper {
    padding: 12px;
  }

  .plans-grid {
    gap: 12px;
  }

  .plan-card {
    padding: 16px;
  }
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 8px;
  }

  .filter-card {
    margin-bottom: 12px;
  }

  .filter-card :deep(.ant-row) {
    gap: 8px;
  }

  .filter-card :deep(.ant-col) {
    margin-bottom: 8px;
  }

  .filter-card :deep(.ant-input-search),
  .filter-card :deep(.ant-select),
  .filter-card :deep(.ant-picker) {
    width: 100% !important;
  }

  .plans-grid {
    gap: 8px;
  }

  .plan-card {
    padding: 12px;
  }

  .plan-header {
    margin-bottom: 12px;
  }

  .plan-header h3 {
    font-size: 16px;
  }

  .plan-stats {
    gap: 12px;
  }

  .plan-stat {
    padding: 8px;
  }

  .plan-actions {
    gap: 8px;
  }
}

@media (max-width: 576px) {
  .content-wrapper {
    padding: 6px;
  }

  .page-header {
    margin-bottom: 12px;
    padding: 12px;
  }

  .page-header h2 {
    font-size: 18px;
  }

  .plan-card {
    padding: 10px;
  }

  .plan-header {
    margin-bottom: 10px;
  }

  .plan-header h3 {
    font-size: 14px;
    margin-bottom: 4px;
  }

  .plan-description {
    font-size: 12px;
    margin-bottom: 8px;
  }

  .plan-stats {
    gap: 8px;
    margin-bottom: 8px;
  }

  .plan-stat {
    padding: 6px;
    font-size: 12px;
  }

  .plan-actions {
    flex-direction: column;
    gap: 6px;
  }

  .plan-actions .ant-btn {
    width: 100%;
  }

  .filter-card :deep(.ant-row) {
    flex-direction: column;
    gap: 6px;
  }

  .filter-card :deep(.ant-col) {
    margin-bottom: 6px;
  }

  .pagination {
    margin-top: 16px;
    text-align: center;
  }
}
</style>
