<template>
  <a-drawer
    :open="open"
    title="关联用例"
    width="min(1200px,100vw)"
    destroy-on-close
    @close="close"
    :mask-closable="!locked"
    :closable="!locked"
  >
    <a-radio-group :disabled="locked" value="functional" class="category"
      ><a-radio-button value="functional"
        >功能用例</a-radio-button
      ></a-radio-group
    >
    <a-alert
      v-if="saveError"
      class="save-error"
      type="error"
      :message="saveError"
      show-icon
    />
    <div class="associate-layout">
      <aside>
        <a-input
          :disabled="locked"
          v-model:value="moduleSearch"
          placeholder="搜索模块"
          allow-clear
        />
        <div class="folder-all">
          <a-button :disabled="locked" type="text" @click="selectFolder('all')"
            >全部用例 ({{ data?.counts.all || 0 }})</a-button
          ><a-button
            :disabled="locked"
            aria-label="展开或收起关联模块"
            type="text"
            @click="
              expanded = expanded.length
                ? []
                : (data?.modules || []).map((m) => m.id)
            "
            ><FolderOpenOutlined
          /></a-button>
        </div>
        <a-tree
          :disabled="locked"
          :tree-data="moduleTree"
          :selected-keys="[folder]"
          :expanded-keys="expanded"
          block-node
          @expand="(keys: (string | number)[]) => (expanded = keys.map(String))"
          @select="
            (keys: (string | number)[]) =>
              selectFolder(String(keys[0] || 'all'))
          "
          ><template #title="node"
            ><span>{{ node.name }}</span
            ><span class="module-count">{{ node.count }}</span></template
          ></a-tree
        >
        <a-button
          :disabled="locked"
          type="text"
          @click="selectFolder('unassigned')"
          >未分配模块 ({{ data?.counts.unassigned || 0 }})</a-button
        >
      </aside>
      <main>
        <div class="search-toolbar">
          <a-input-search
            :disabled="locked"
            v-model:value="search"
            placeholder="通过 ID / 名称搜索"
            :maxlength="255"
            allow-clear
            @search="resetPage"
          /><a-select
            :disabled="locked"
            v-model:value="priority"
            placeholder="等级"
            allow-clear
            :options="
              ['P0', 'P1', 'P2', 'P3'].map((value) => ({ value, label: value }))
            "
            @change="resetPage"
          /><a-button :disabled="locked" :loading="loading" @click="load"
            >刷新</a-button
          >
        </div>
        <a-alert
          v-if="failed"
          type="error"
          message="关联用例列表加载失败，请重试"
          show-icon
        />
        <div class="selection-toolbar">
          <span>已选择 {{ selected.size }} 个用例</span
          ><a-button
            type="link"
            :loading="selecting"
            :disabled="locked || loading || failed || !data?.total"
            @click="selectAll"
            >全选筛选结果</a-button
          ><a-button
            type="link"
            :disabled="!selected.size || locked"
            @click="selected.clear()"
            >清空选择</a-button
          >
        </div>
        <a-table
          :columns="columns"
          :data-source="data?.items || []"
          :loading="loading"
          row-key="id"
          :row-selection="rowSelection"
          :pagination="pagination"
          :scroll="{ x: 800, y: 400 }"
          @change="tableChange"
          ><template #bodyCell="{ column, record }"
            ><template v-if="column.key === 'name'"
              >{{ record.name
              }}<a-tag v-if="excluded.includes(record.id)">{{
                saveSelection ? "已关联" : "已选择"
              }}</a-tag></template
            ><a-tag v-else-if="column.key === 'priority'">{{
              record.priority
            }}</a-tag
            ><a-space v-else-if="column.key === 'tags'" wrap
              ><a-tag v-for="tag in record.tags" :key="tag">{{
                tag
              }}</a-tag></a-space
            ></template
          ></a-table
        >
      </main>
    </div>
    <template #footer
      ><div class="associate-footer">
        <a-form layout="inline"
          ><a-form-item label="评审人" required
            ><a-select
              :disabled="locked"
              v-model:value="reviewers"
              mode="multiple"
              show-search
              option-filter-prop="label"
              :options="members.map((m) => ({ value: m.id, label: m.name }))"
              placeholder="请选择评审人"
              :max-tag-count="2"
              style="width: 290px" /></a-form-item></a-form
        ><a-space
          ><a-button :disabled="locked" @click="close">取消</a-button
          ><a-button
            type="primary"
            :loading="saving"
            :disabled="
              !selected.size || !reviewers.length || failed || loading || locked
            "
            @click="confirm"
            >关联 ({{ selected.size }})</a-button
          ></a-space
        >
      </div></template
    >
  </a-drawer>
</template>
<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { message } from "ant-design-vue";
import { FolderOpenOutlined } from "@ant-design/icons-vue";
import {
  reviewWorkspaceApi,
  type ReviewCandidates,
} from "@/api/reviewWorkspace";
import { caseFolderTree } from "@/components/TestPlan/planCaseFolders";
const props = defineProps<{
  open: boolean;
  projectId: string;
  excluded: string[];
  defaultReviewers: string[];
  members: { id: string; name: string }[];
  saveSelection?: (data: {
    caseIds: string[];
    reviewerIds: string[];
  }) => Promise<void>;
}>();
const emit = defineEmits<{
  "update:open": [boolean];
  confirm: [{ caseIds: string[]; reviewerIds: string[] }];
}>();
const data = ref<ReviewCandidates>(),
  loading = ref(false),
  failed = ref(false),
  selecting = ref(false),
  saving = ref(false),
  saveError = ref(""),
  search = ref(""),
  priority = ref<string>(),
  folder = ref("all"),
  moduleSearch = ref(""),
  expanded = ref<string[]>([]),
  page = ref(1),
  size = ref(20),
  selected = ref(new Set<string>()),
  reviewers = ref<string[]>([]);
const locked = computed(() => selecting.value || saving.value);
const moduleTree = computed(() =>
  caseFolderTree(data.value?.modules || [], moduleSearch.value),
);
const pagination = computed(() => ({
  current: page.value,
  pageSize: size.value,
  total: data.value?.total || 0,
  showSizeChanger: true,
  showTotal: (total: number) => `共 ${total} 条`,
}));
const columns = [
  { title: "ID", dataIndex: "caseCode", width: 130 },
  { title: "名称", key: "name", width: 240 },
  { title: "等级", key: "priority", width: 70 },
  { title: "标签", key: "tags", width: 160 },
  { title: "所属模块", dataIndex: "moduleName", width: 200 },
];
const rowSelection = computed(() => ({
  selectedRowKeys: [...selected.value],
  preserveSelectedRowKeys: true,
  getCheckboxProps: (row: { id: string }) => ({
    disabled: props.excluded.includes(row.id) || locked.value,
  }),
  onChange: (keys: (string | number)[]) => {
    if (keys.length + props.excluded.length > 10000)
      return void message.warning("一个评审最多关联10000个用例");
    selected.value = new Set(keys.map(String));
  },
}));
let sequence = 0;
async function load() {
  if (!props.open || !props.projectId) return;
  const current = ++sequence,
    p = props.projectId;
  loading.value = true;
  failed.value = false;
  try {
    const result = await reviewWorkspaceApi.candidates(p, {
      search: search.value,
      priority: priority.value,
      folder: folder.value,
      page: page.value,
      size: size.value,
    });
    if (current === sequence && p === props.projectId && props.open)
      data.value = result;
  } catch (error) {
    console.error("加载评审关联候选失败", error);
    if (current === sequence) {
      data.value = undefined;
      failed.value = true;
    }
  } finally {
    if (current === sequence) loading.value = false;
  }
}
function resetPage() {
  page.value = 1;
  void load();
}
function selectFolder(id: string) {
  folder.value = id;
  resetPage();
}
function tableChange(p: { current: number; pageSize: number }) {
  page.value = p.current;
  size.value = p.pageSize;
  void load();
}
async function selectAll() {
  const p = props.projectId,
    current = sequence;
  selecting.value = true;
  try {
    const result = await reviewWorkspaceApi.selectCandidates(p, {
      search: search.value,
      folder: folder.value,
      priority: priority.value,
      excludeIds: [...new Set([...props.excluded, ...selected.value])],
    });
    if (p !== props.projectId || !props.open || current !== sequence) return;
    selected.value = new Set([...selected.value, ...result.caseIds]);
    console.info("评审草稿已全选筛选结果", {
      projectId: p,
      count: result.total,
    });
  } catch (error) {
    console.error("评审关联全选失败", error);
  } finally {
    selecting.value = false;
  }
}
function close() {
  if (locked.value) return;
  emit("update:open", false);
}
async function confirm() {
  if (!reviewers.value.length || !selected.value.size || locked.value) return;
  const data = {
    caseIds: [...selected.value],
    reviewerIds: [...reviewers.value],
  };
  saving.value = true;
  saveError.value = "";
  try {
    if (props.saveSelection) await props.saveSelection(data);
    else emit("confirm", data);
    emit("update:open", false);
    console.info(
      props.saveSelection ? "评审关联已保存" : "关联选择已加入评审草稿",
      { projectId: props.projectId, count: data.caseIds.length },
    );
  } catch (error) {
    console.error("保存评审关联失败，保留当前选择", error);
    saveError.value = "关联失败，请根据提示修正后重试，或刷新列表重新选择";
  } finally {
    saving.value = false;
  }
}
watch(
  () => [props.open, props.projectId],
  () => {
    ++sequence;
    data.value = undefined;
    selected.value = new Set();
    reviewers.value = [...props.defaultReviewers];
    search.value = "";
    priority.value = undefined;
    folder.value = "all";
    moduleSearch.value = "";
    expanded.value = [];
    page.value = 1;
    loading.value = false;
    failed.value = false;
    saveError.value = "";
    void load();
  },
  { immediate: true },
);
</script>
<style scoped>
.save-error {
  margin-bottom: 16px;
}
.category {
  margin-bottom: 20px;
}
.associate-layout {
  display: flex;
  gap: 24px;
}
.associate-layout aside {
  width: 240px;
  flex: none;
  border-right: 1px solid #e5e6eb;
  padding-right: 16px;
}
.associate-layout main {
  flex: 1;
  min-width: 0;
}
.folder-all,
.selection-toolbar,
.associate-footer {
  display: flex;
  align-items: center;
  gap: 8px;
}
.folder-all,
.associate-footer {
  justify-content: space-between;
}
.module-count {
  float: right;
  color: #86909c;
}
.search-toolbar {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}
.search-toolbar .ant-input-search {
  flex: 1;
}
.search-toolbar .ant-select {
  width: 100px;
}
.selection-toolbar {
  margin-bottom: 8px;
}
.associate-footer {
  flex-wrap: wrap;
  gap: 16px;
}
@media (max-width: 700px) {
  .associate-layout {
    display: block;
  }
  .associate-layout aside {
    width: 100%;
    max-height: 180px;
    overflow: auto;
    border-right: 0;
    margin-bottom: 16px;
  }
  .search-toolbar {
    flex-wrap: wrap;
  }
  .associate-footer :deep(.ant-select) {
    max-width: 75vw;
  }
}
</style>
