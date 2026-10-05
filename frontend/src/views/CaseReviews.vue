<template>
  <section class="review-index">
    <a-alert v-if="!projectId" type="info" message="请选择项目" />
    <template v-else>
      <aside class="module-panel">
        <a-input
          v-model:value="moduleSearch"
          placeholder="请输入模块名称"
          allow-clear
        />
        <div class="module-heading">
          <a-button type="text" @click="selectModule('all')"
            >全部评审 <span class="count">({{ data.allCount }})</span></a-button
          >
          <a-space
            ><a-button
              type="text"
              aria-label="展开或折叠模块"
              @click="toggleExpand"
              ><DownOutlined
            /></a-button>
            <a-button
              v-if="data.permissions.update"
              type="text"
              aria-label="新建评审模块"
              @click="openModule()"
              ><PlusOutlined /></a-button
          ></a-space>
        </div>
        <a-tree
          :tree-data="tree"
          :selected-keys="[selectedModule]"
          v-model:expanded-keys="expanded"
          :draggable="data.permissions.update"
          block-node
          @select="(keys: any[]) => selectModule(String(keys[0] || 'all'))"
          @drop="dropModule"
        >
          <template #title="node">
            <div class="module-node">
              <span :title="node.title"
                ><FolderOutlined /> {{ node.title }}
                <span class="count">({{ node.count }})</span></span
              >
              <a-dropdown
                v-if="
                  node.key !== 'default' &&
                  (data.permissions.update || data.permissions.delete)
                "
                :trigger="['click']"
              >
                <a-button
                  type="text"
                  size="small"
                  :aria-label="`操作模块${node.title}`"
                  @click.stop
                  ><MoreOutlined
                /></a-button>
                <template #overlay
                  ><a-menu>
                    <a-menu-item
                      v-if="data.permissions.update"
                      @click="openModule(undefined, node.key)"
                      >添加子模块</a-menu-item
                    >
                    <a-menu-item
                      v-if="data.permissions.update"
                      @click="openModule(node.key)"
                      >重命名</a-menu-item
                    >
                    <a-menu-item
                      v-if="data.permissions.delete"
                      danger
                      @click="confirmModuleDelete(node.key)"
                      >删除</a-menu-item
                    >
                  </a-menu></template
                >
              </a-dropdown>
            </div>
          </template>
        </a-tree>
      </aside>
      <main class="review-table-panel">
        <div class="toolbar">
          <a-radio-group
            v-model:value="scope"
            button-style="solid"
            @change="reload"
          >
            <a-radio-button value="all">全部</a-radio-button
            ><a-radio-button value="reviewByMe">我评审的</a-radio-button
            ><a-radio-button value="createByMe">我创建的</a-radio-button>
          </a-radio-group>
          <a-space wrap
            ><a-input-search
              v-model:value="search"
              placeholder="通过 ID/名称/标签搜索"
              allow-clear
              @search="reload"
            />
            <a-button aria-label="刷新评审列表" @click="load"
              ><ReloadOutlined
            /></a-button>
            <a-button aria-label="表格设置" @click="settingsVisible = true"
              ><SettingOutlined
            /></a-button>
            <a-button
              v-if="data.permissions.update"
              type="primary"
              @click="openWorkspace(undefined, 'create')"
              >创建评审</a-button
            >
          </a-space>
        </div>
        <a-space class="column-filters" wrap>
          <a-select
            v-model:value="lifecycle"
            allow-clear
            placeholder="评审状态"
            :options="reviewStates"
            @change="reload"
          />
          <a-select
            v-model:value="mode"
            allow-clear
            placeholder="模式"
            :options="[
              { label: '单人', value: 'single' },
              { label: '多人', value: 'multiple' },
            ]"
            @change="reload"
          />
          <a-select
            v-model:value="reviewerId"
            allow-clear
            show-search
            :filter-option="filterMember"
            placeholder="评审人"
            :options="memberOptions"
            @change="reload"
          />
          <a-select
            v-model:value="creatorId"
            allow-clear
            show-search
            :filter-option="filterMember"
            placeholder="创建人"
            :options="memberOptions"
            @change="reload"
          />
          <a-button v-if="hasFilters" type="link" @click="clearFilters"
            >清空筛选</a-button
          >
        </a-space>
        <a-alert v-if="loadError" type="error" :message="loadError" show-icon />
        <div v-if="selected.length" class="batch-toolbar">
          <span>已选择 {{ selected.length }} 条</span>
          <a-button
            v-if="data.permissions.update"
            @click="
              moveTarget = undefined;
              moveVisible = true;
            "
            >移动到</a-button
          ><a-button type="link" @click="selected = []">取消选择</a-button>
        </div>
        <a-table
          :columns="columns"
          :data-source="data.items"
          row-key="id"
          :loading="busy"
          :pagination="pagination"
          :scroll="{ x: tableWidth }"
          :row-selection="
            data.permissions.update
              ? {
                  selectedRowKeys: selected,
                  onChange: (keys: any[]) => (selected = keys.map(String)),
                  getCheckboxProps: (record: ReviewSummary) => ({
                    disabled: record.archived,
                  }),
                }
              : undefined
          "
          @change="tableChange"
        >
          <template #headerCell="{ column }"
            ><a-tooltip
              v-if="column.key === 'passRate'"
              title="通过的用例数 / 总用例数 × 100%"
              >通过率 <QuestionCircleOutlined /></a-tooltip
            ><span v-else>{{ column.title }}</span></template
          >
          <template #bodyCell="{ column, record }">
            <a
              v-if="column.key === 'number'"
              :title="record.id"
              @click="openWorkspace(record.id)"
              >{{ record.number ?? record.id.slice(0, 8) }}</a
            >
            <a
              v-else-if="column.key === 'name'"
              @click="openWorkspace(record.id)"
              >{{ record.name }}</a
            >
            <a-tag
              v-else-if="column.key === 'lifecycle'"
              :color="stateColor(record.lifecycle)"
              >{{ reviewStateName(record.lifecycle) }}</a-tag
            >
            <div v-else-if="column.key === 'passRate'" class="pass-rate">
              <a-progress
                :percent="record.passRate"
                :show-info="false"
                size="small"
              /><span>{{ record.passRate }}%</span>
            </div>
            <a-tag
              v-else-if="column.key === 'mode'"
              :color="record.mode === 'single' ? 'green' : 'blue'"
              >{{ record.mode === "single" ? "单人" : "多人" }}</a-tag
            >
            <a-tooltip
              v-else-if="column.key === 'reviewers'"
              :title="record.reviewers.join('、')"
              ><span>{{ record.reviewers.join("、") }}</span></a-tooltip
            >
            <a-tooltip
              v-else-if="column.key === 'moduleName'"
              :title="record.modulePath"
              ><span>{{ record.moduleName }}</span></a-tooltip
            >
            <template v-else-if="column.key === 'tags'"
              ><a-tag v-for="tag in record.tags" :key="tag">{{
                tag
              }}</a-tag></template
            >
            <span v-else-if="column.key === 'period'">{{
              record.startDate && record.endDate
                ? `${record.startDate} ～ ${record.endDate}`
                : "-"
            }}</span>
            <span v-else-if="column.key === 'createdAt'">{{
              formatDate(record.createdAt)
            }}</span>
            <a-space v-else-if="column.key === 'actions'" :size="4">
              <a-button
                v-if="data.permissions.update && !record.archived"
                type="link"
                size="small"
                @click="openWorkspace(record.id, 'edit')"
                >编辑</a-button
              >
              <a-dropdown v-if="data.permissions.delete" :trigger="['click']"
                ><a-button
                  type="text"
                  size="small"
                  :aria-label="`更多操作${record.name}`"
                  ><MoreOutlined
                /></a-button>
                <template #overlay
                  ><a-menu
                    ><a-menu-item
                      v-if="record.lifecycle === 'completed'"
                      @click="confirmArchive(record)"
                      >归档</a-menu-item
                    ><a-menu-item danger @click="confirmDelete(record)"
                      >删除</a-menu-item
                    ></a-menu
                  ></template
                >
              </a-dropdown>
            </a-space>
          </template>
          <template #emptyText
            ><div class="empty">
              暂无评审数据
              <a-button
                v-if="data.permissions.update"
                type="link"
                @click="openWorkspace(undefined, 'create')"
                >创建评审</a-button
              >
            </div></template
          >
        </a-table>
      </main>
    </template>
    <TableDisplaySettings
      :open="settingsVisible"
      :definitions="reviewDefinitions"
      :columns="display.columns"
      :page-size="display.pageSize"
      :include-descendants="display.includeDescendants"
      :error="settingsError"
      @close="saveColumns"
      @page-size-change="saveSize"
      @descendants-change="saveDescendants"
    />
    <a-modal
      v-model:open="moduleVisible"
      :title="editingModule ? '重命名模块' : '新建模块'"
      :confirm-loading="mutating"
      :mask-closable="false"
      @ok="saveModule"
    >
      <a-form layout="vertical"
        ><a-form-item label="模块名称" required
          ><a-input
            v-model:value="moduleName"
            :maxlength="100"
            placeholder="请输入模块名称"
            @press-enter="saveModule" /></a-form-item
      ></a-form>
    </a-modal>
    <a-modal
      v-model:open="deleteVisible"
      :title="deletingModule ? '删除模块' : '删除评审'"
      :confirm-loading="mutating"
      :mask-closable="false"
      :ok-button-props="{
        danger: true,
        disabled: deleteName !== deleteExpected,
      }"
      @ok="performDelete"
    >
      <a-alert
        type="warning"
        show-icon
        :message="
          deletingModule
            ? '删除模块及其下所有资源，包含子模块中的评审。用例和历史版本保留。'
            : '删除评审及其结论、评论和关注记录。用例和历史版本保留。'
        "
      />
      <p>请输入“{{ deleteExpected }}”确认删除</p>
      <a-input v-model:value="deleteName" placeholder="请输入名称确认" />
    </a-modal>
    <a-modal
      v-model:open="moveVisible"
      :title="`移动评审（已选 ${selected.length} 条）`"
      :confirm-loading="mutating"
      :mask-closable="false"
      :ok-button-props="{ disabled: moveTarget === undefined }"
      @ok="moveReviews"
    >
      <a-tree-select
        v-model:value="moveTarget"
        :tree-data="moveTree"
        tree-default-expand-all
        placeholder="请选择目标模块"
        style="width: 100%"
      />
    </a-modal>
  </section>
</template>
<script setup lang="ts">
import { computed, ref, watch, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { message, Modal } from "ant-design-vue";
import {
  FolderOutlined,
  PlusOutlined,
  MoreOutlined,
  DownOutlined,
  ReloadOutlined,
  SettingOutlined,
  QuestionCircleOutlined,
} from "@ant-design/icons-vue";
import dayjs from "dayjs";
import { useWindowSize } from "@vueuse/core";
import { useProjectStore } from "@/stores/project";
import { useUserStore } from "@/stores/user";
import { caseGovernanceApi } from "@/api/caseGovernance";
import {
  reviewWorkspaceApi as api,
  type ReviewSummary,
  type ReviewList,
} from "@/api/reviewWorkspace";
import TableDisplaySettings from "@/components/Table/TableDisplaySettings.vue";
import {
  displayStorageKey,
  readDisplay,
  normalizeDisplay,
  type ColumnVisibility,
} from "@/components/Table/tableDisplay";
import {
  reviewColumns,
  reviewDefinitions,
  reviewStates,
  reviewStateName,
} from "@/components/Table/reviewColumns";
const route = useRoute(),
  router = useRouter(),
  projects = useProjectStore(),
  user = useUserStore();
const projectId = computed(() => projects.currentProject?.id || "");
const emptyData = (): ReviewList => ({
  items: [],
  total: 0,
  page: 1,
  size: 20,
  modules: [],
  defaultCount: 0,
  allCount: 0,
  permissions: { update: false, delete: false },
});
const data = ref(emptyData()),
  busy = ref(false),
  loadError = ref(""),
  mutating = ref(false);
const scope = ref("all"),
  search = ref(""),
  moduleSearch = ref(""),
  selectedModule = ref("all"),
  expanded = ref<string[]>([]),
  selected = ref<string[]>([]),
  page = ref(1);
const lifecycle = ref<string>(),
  mode = ref<string>(),
  reviewerId = ref<string>(),
  creatorId = ref<string>();
const sort = ref("createdAt"),
  order = ref("desc");
const members = ref<{ id: string; name: string }[]>([]);
const memberOptions = computed(() =>
  members.value.map((m) => ({ label: m.name, value: m.id })),
);
const filterMember = (input: string, option: any) =>
  String(option.label).toLowerCase().includes(input.toLowerCase());
const display = ref(normalizeDisplay(undefined, reviewDefinitions)),
  settingsVisible = ref(false),
  settingsError = ref("");
const displayKey = computed(() =>
  displayStorageKey(
    String(user.user?.id || ""),
    projectId.value,
    "review-list",
  ),
);
const { width: viewportWidth } = useWindowSize();
const columns = computed(() => [
  ...display.value.columns
    .filter((c) => c.visible)
    .map((c) => ({
      ...reviewColumns.find((d) => d.key === c.key)!,
      dataIndex: c.key,
      ellipsis: true,
    })),
  {
    key: "actions",
    title: "操作",
    width: 110,
    fixed: viewportWidth.value >= 700 ? "right" : undefined,
  },
]);
const tableWidth = computed(() =>
  columns.value.reduce((n, c) => n + (c.width || 100), 0),
);
const pagination = computed(() => ({
  current: page.value,
  pageSize: display.value.pageSize,
  total: data.value.total,
  showSizeChanger: false,
  showTotal: (n: number) => `共 ${n} 条`,
}));
const hasFilters = computed(() =>
  Boolean(
    search.value ||
    lifecycle.value ||
    mode.value ||
    reviewerId.value ||
    creatorId.value,
  ),
);
interface Node {
  key: string;
  value: string;
  title: string;
  count: number;
  children: Node[];
}
function buildTree(filtered: boolean): Node[] {
  const nodes = new Map(
    data.value.modules.map((m) => [
      m.id,
      {
        key: m.id,
        value: m.id,
        title: m.name,
        count: m.count,
        children: [] as Node[],
      },
    ]),
  );
  const roots: Node[] = [];
  data.value.modules.forEach((m) => {
    const node = nodes.get(m.id)!;
    if (m.parentId && nodes.has(m.parentId))
      nodes.get(m.parentId)!.children.push(node);
    else roots.push(node);
  });
  roots.unshift({
    key: "default",
    value: "default",
    title: "默认模块",
    count: data.value.defaultCount,
    children: [],
  });
  function filter(nodes: Node[]): Node[] {
    return nodes.flatMap((n) => {
      const children = filter(n.children);
      return n.title.includes(moduleSearch.value) || children.length
        ? [{ ...n, children }]
        : [];
    });
  }
  return filtered && moduleSearch.value ? filter(roots) : roots;
}
const tree = computed(() => buildTree(true)),
  moveTree = computed(() => buildTree(false));
const stateColor = (s: string) =>
  ({
    prepared: "default",
    underway: "blue",
    completed: "green",
    archived: "default",
    cancelled: "default",
    superseded: "default",
  })[s] || "default";
const formatDate = (date: string) => dayjs(date).format("YYYY-MM-DD HH:mm:ss");
let loadSequence = 0;
async function load() {
  const p = projectId.value,
    sequence = ++loadSequence;
  if (!p) return;
  busy.value = true;
  loadError.value = "";
  try {
    const result = await api.list(p, {
      page: page.value,
      size: display.value.pageSize,
      scope: scope.value,
      search: search.value,
      moduleId:
        selectedModule.value === "all" ? undefined : selectedModule.value,
      includeDescendants: display.value.includeDescendants,
      lifecycle: lifecycle.value,
      mode: mode.value,
      reviewerId: reviewerId.value,
      creatorId: creatorId.value,
      sort: sort.value,
      order: order.value,
    });
    if (sequence !== loadSequence || p !== projectId.value) return;
    data.value = result;
    if (
      page.value > 1 &&
      !result.items.length &&
      result.total < (page.value - 1) * display.value.pageSize + 1
    ) {
      page.value = Math.max(
        1,
        Math.ceil(result.total / display.value.pageSize),
      );
      await load();
    }
    selected.value = selected.value.filter((id) =>
      result.items.some((r) => r.id === id && !r.archived),
    );
  } catch (error) {
    console.error("加载评审首页失败", error);
    if (sequence === loadSequence && p === projectId.value) {
      data.value.items = [];
      loadError.value = "评审列表加载失败，请刷新重试";
    }
  } finally {
    if (sequence === loadSequence) busy.value = false;
  }
}
function reload() {
  page.value = 1;
  selected.value = [];
  void load();
}
function selectModule(key: string) {
  selectedModule.value = key;
  reload();
}
function toggleExpand() {
  expanded.value = expanded.value.length
    ? []
    : data.value.modules.map((m) => m.id);
}
function clearFilters() {
  search.value = "";
  lifecycle.value = mode.value = reviewerId.value = creatorId.value = undefined;
  reload();
}
function tableChange(p: any, _filters: any, s: any) {
  page.value = p.current || 1;
  if (s?.order) {
    sort.value = s.columnKey;
    order.value = s.order === "ascend" ? "asc" : "desc";
  } else {
    sort.value = "createdAt";
    order.value = "desc";
  }
  selected.value = [];
  void load();
}
function persist(next: typeof display.value) {
  try {
    localStorage.setItem(displayKey.value, JSON.stringify(next));
    display.value = next;
    settingsError.value = "";
    return true;
  } catch (error) {
    console.error("保存评审表格设置失败", error);
    settingsError.value = "无法保存表格设置，请释放浏览器存储空间后重试";
    return false;
  }
}
function saveColumns(columns: ColumnVisibility[]) {
  if (persist({ ...display.value, columns })) settingsVisible.value = false;
}
function saveSize(size: number) {
  if (persist({ ...display.value, pageSize: size })) reload();
}
function saveDescendants(value: boolean) {
  if (persist({ ...display.value, includeDescendants: value })) reload();
}
function openWorkspace(id?: string, action?: string) {
  void router.push({
    name: "CaseReviewWorkspace",
    query: {
      projectId: projectId.value,
      ...(id ? { reviewId: id } : {}),
      ...(action === "create"
        ? {
            create: "1",
            ...(typeof route.query.caseIds === "string"
              ? { caseIds: route.query.caseIds }
              : {}),
            moduleId:
              selectedModule.value === "all" ? "default" : selectedModule.value,
          }
        : {}),
      ...(action === "edit" ? { edit: "1" } : {}),
    },
  });
}
async function mutation(
  operation: (p: string) => Promise<unknown>,
  success: string,
) {
  if (mutating.value) return;
  const p = projectId.value;
  mutating.value = true;
  try {
    await operation(p);
    if (p === projectId.value) {
      message.success(success);
      await load();
    }
    return true;
  } catch (error) {
    console.error("评审首页操作失败", error);
    return false;
  } finally {
    mutating.value = false;
  }
}
const moduleVisible = ref(false),
  editingModule = ref<string>(),
  moduleName = ref(""),
  moduleParent = ref<string | null>(null),
  modulePosition = ref(0);
function openModule(id?: string, parent?: string) {
  const row = data.value.modules.find((m) => m.id === id);
  editingModule.value = id;
  moduleName.value = row?.name || "";
  moduleParent.value = row?.parentId || parent || null;
  modulePosition.value =
    row?.position ??
    data.value.modules.filter((m) => m.parentId === (parent || null)).length;
  moduleVisible.value = true;
}
async function saveModule() {
  if (!moduleName.value.trim()) return message.warning("请输入模块名称");
  if (
    await mutation(
      (p) =>
        api.saveModule(
          p,
          {
            name: moduleName.value.trim(),
            parentId: moduleParent.value,
            position: modulePosition.value,
          },
          editingModule.value,
        ),
      "模块已保存",
    )
  )
    moduleVisible.value = false;
}
async function dropModule(info: any) {
  const source = data.value.modules.find(
      (m) => m.id === String(info.dragNode.key),
    ),
    target = data.value.modules.find((m) => m.id === String(info.node.key));
  if (!source || !target)
    return message.warning("默认模块不能拖动或添加子模块");
  const parent = info.dropToGap ? target.parentId : target.id;
  const siblings = data.value.modules.filter(
    (m) => m.parentId === parent && m.id !== source.id,
  );
  const index = info.dropToGap
    ? siblings.findIndex((m) => m.id === target.id) +
      (info.dropPosition > Number(String(info.node.pos).split("-").at(-1))
        ? 1
        : 0)
    : siblings.length;
  await mutation(
    (p) =>
      api.saveModule(
        p,
        { name: source.name, parentId: parent, position: Math.max(0, index) },
        source.id,
      ),
    "模块已移动",
  );
}
const deleteVisible = ref(false),
  deletingModule = ref(false),
  deleteId = ref(""),
  deleteExpected = ref(""),
  deleteName = ref("");
function confirmDelete(row: ReviewSummary) {
  deletingModule.value = false;
  deleteId.value = row.id;
  deleteExpected.value = row.name;
  deleteName.value = "";
  deleteVisible.value = true;
}
function confirmModuleDelete(id: string) {
  const row = data.value.modules.find((m) => m.id === id);
  if (!row) return;
  deletingModule.value = true;
  deleteId.value = id;
  deleteExpected.value = row.name;
  deleteName.value = "";
  deleteVisible.value = true;
}
async function performDelete() {
  if (deleteName.value !== deleteExpected.value) return;
  if (
    await mutation(
      (p) =>
        deletingModule.value
          ? api.deleteModule(p, deleteId.value, deleteName.value)
          : api.delete(p, deleteId.value, deleteName.value),
      "删除成功",
    )
  ) {
    deleteVisible.value = false;
    if (
      deletingModule.value &&
      !data.value.modules.some((m) => m.id === selectedModule.value)
    ) {
      selectedModule.value = "all";
      reload();
    }
  }
}
function confirmArchive(row: ReviewSummary) {
  const p = projectId.value;
  Modal.confirm({
    title: "归档评审",
    content:
      "归档后不在默认列表展示，可通过已归档筛选查看。归档后的评审内容不能修改。",
    async onOk() {
      if (p !== projectId.value) throw new Error("项目已切换，请重新操作");
      if (!(await mutation((id) => api.archive(id, row.id), "评审已归档")))
        throw new Error("归档未成功");
    },
  });
}
const moveVisible = ref(false),
  moveTarget = ref<string>();
async function moveReviews() {
  if (moveTarget.value === undefined) return;
  if (
    await mutation(
      (p) =>
        api.move(
          p,
          selected.value,
          moveTarget.value === "default" ? null : moveTarget.value!,
        ),
      "评审已移动",
    )
  ) {
    moveVisible.value = false;
    selected.value = [];
  }
}
watch(
  projectId,
  async (p) => {
    ++loadSequence;
    busy.value = false;
    data.value = emptyData();
    members.value = [];
    scope.value = "all";
    search.value = moduleSearch.value = "";
    selectedModule.value = "all";
    selected.value = [];
    page.value = 1;
    lifecycle.value =
      mode.value =
      reviewerId.value =
      creatorId.value =
        undefined;
    expanded.value = [];
    moduleVisible.value =
      deleteVisible.value =
      moveVisible.value =
      settingsVisible.value =
        false;
    display.value = readDisplay(
      localStorage,
      displayKey.value,
      reviewDefinitions,
    );
    settingsError.value = "";
    await load();
    if (p && p === projectId.value) {
      try {
        const result = await caseGovernanceApi.reviewers(p);
        if (p === projectId.value) members.value = result;
      } catch (error) {
        console.error("加载评审成员失败", error);
      }
    }
  },
  { immediate: true },
);
onMounted(async () => {
  if (!projects.projects.length) await projects.fetchProjects();
  const query =
    typeof route.query.projectId === "string"
      ? route.query.projectId
      : undefined;
  const project =
    projects.projects.find((p) => p.id === query) ||
    projects.currentProject ||
    projects.projects[0];
  if (project && project.id !== projectId.value)
    projects.setCurrentProject(project);
  if (route.query.create === "1" || route.query.reviewId)
    openWorkspace(
      typeof route.query.reviewId === "string"
        ? route.query.reviewId
        : undefined,
      route.query.create === "1" ? "create" : undefined,
    );
});
</script>
<style scoped>
.review-index {
  display: grid;
  grid-template-columns: 300px minmax(0, 1fr);
  min-height: calc(100vh - 130px);
  background: #fff;
  margin: 16px;
  border: 1px solid #eef0f4;
  border-radius: 4px;
  min-width: 0;
}
.module-panel {
  padding: 16px;
  border-right: 1px solid #eef0f4;
  min-width: 0;
}
.module-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 12px 0;
}
.module-node {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 4px;
  min-width: 0;
}
.module-node > span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.count {
  color: #86909c;
}
.review-table-panel {
  padding: 16px;
  min-width: 0;
}
.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}
.toolbar :deep(.ant-input-search) {
  width: 260px;
}
.column-filters {
  margin-bottom: 16px;
}
.column-filters :deep(.ant-select) {
  width: 140px;
}
.batch-toolbar {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 8px 12px;
  margin-bottom: 12px;
  background: #f2f7ff;
}
.pass-rate {
  display: flex;
  align-items: center;
  gap: 8px;
}
.pass-rate :deep(.ant-progress) {
  width: 100px;
  margin: 0;
}
.empty {
  padding: 30px;
}
.review-table-panel :deep(.ant-table-wrapper) {
  max-width: 100%;
}
@media (max-width: 900px) {
  .review-index {
    grid-template-columns: 220px minmax(0, 1fr);
  }
}
@media (max-width: 700px) {
  .review-index {
    grid-template-columns: minmax(0, 1fr);
    margin: 8px;
  }
  .module-panel {
    border-right: 0;
    border-bottom: 1px solid #eef0f4;
    max-height: 260px;
    overflow: auto;
  }
  .toolbar :deep(.ant-input-search) {
    width: 220px;
  }
  .review-table-panel {
    padding: 12px;
  }
  .toolbar :deep(.ant-space) {
    max-width: 100%;
  }
  .column-filters :deep(.ant-select) {
    width: 140px;
  }
}
</style>
