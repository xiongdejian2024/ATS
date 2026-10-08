<template>
  <section class="groups-page">
    <header>
      <h2>请求环境组</h2>
      <a-space
        ><a-input
          v-model:value="search"
          placeholder="搜索环境组"
          :maxlength="255"
          @press-enter="searchGroups"
        /><a-button @click="searchGroups" :disabled="busy">搜索</a-button
        ><a-button
          type="primary"
          v-if="canEdit"
          :disabled="busy"
          @click="openEditor()"
          >新建环境组</a-button
        ></a-space
      >
    </header>
    <a-alert v-if="!projectId" type="info" message="请选择项目" />
    <template v-else>
      <a-alert v-if="error" type="error" :message="error" show-icon
        ><template #action
          ><a-button size="small" @click="load">重试</a-button></template
        ></a-alert
      >
      <a-table
        :loading="loading"
        :data-source="items"
        :columns="columns"
        row-key="id"
        :pagination="false"
        :scroll="{ x: 650 }"
      >
        <template #bodyCell="{ column, record }"
          ><span v-if="column.key === 'mappings'"
            >{{ record.mappings.length }} 个来源项目</span
          ><a-space v-else-if="column.key === 'actions'"
            ><a-button type="link" @click="openEditor(record)">{{
              canEdit ? "编辑" : "查看"
            }}</a-button
            ><a-button
              v-if="canDelete"
              danger
              type="link"
              :disabled="busy"
              @click="remove(record)"
              >删除</a-button
            ></a-space
          ></template
        >
      </a-table>
      <a-pagination
        :current="page"
        :page-size="20"
        :total="total"
        :show-size-changer="false"
        @change="changePage"
      />
    </template>
  </section>
  <a-drawer
    :open="editorOpen"
    :title="editingId ? (canEdit ? '编辑环境组' : '查看环境组') : '新建环境组'"
    width="min(720px,100vw)"
    :closable="!busy"
    :mask-closable="!busy"
    :keyboard="!busy"
    @close="beforeClose"
  >
    <a-alert v-if="editorError" type="error" :message="editorError" show-icon />
    <a-form layout="vertical">
      <a-form-item label="名称"
        ><a-input
          v-model:value="draft.name"
          :maxlength="255"
          :disabled="busy || !canEdit"
      /></a-form-item>
      <a-form-item label="描述"
        ><a-textarea
          v-model:value="draft.description"
          :maxlength="10000"
          :rows="3"
          :disabled="busy || !canEdit"
      /></a-form-item>
      <a-form-item label="来源项目与请求环境">
        <div v-for="row in draft.mappings" :key="row.key" class="mapping-row">
          <a-select
            :value="row.projectId || undefined"
            :options="projectOptions"
            placeholder="来源项目"
            :disabled="busy || !canEdit"
            @change="(value: string) => selectProject(row.key, value)"
          />
          <a-select
            v-model:value="row.environmentId"
            :options="sourceOptions(row)"
            placeholder="请求环境"
            :loading="sourceState[row.key]?.loading"
            :disabled="
              busy ||
              !canEdit ||
              !row.projectId ||
              sourceState[row.key]?.loading
            "
          />
          <a-button
            v-if="canEdit"
            danger
            :disabled="busy"
            @click="removeMapping(row.key)"
            >移除</a-button
          >
          <a-alert
            v-if="sourceState[row.key]?.error"
            class="mapping-error"
            :message="sourceState[row.key].error"
            type="error"
            ><template #action
              ><a-button size="small" @click="loadSource(row.key)"
                >重试</a-button
              ></template
            ></a-alert
          >
        </div>
        <a-button
          v-if="canEdit"
          :disabled="busy || draft.mappings.length >= 100"
          @click="addMapping"
          >添加来源项目</a-button
        >
      </a-form-item>
      <p class="hint">
        每个来源项目选择一个该项目的请求环境。执行时按用例来源项目解析并冻结；组中未配置的来源会拒绝执行。
      </p>
      <a-space
        ><a-button
          v-if="canEdit"
          type="primary"
          :loading="busy"
          :disabled="busy || sourceLoading"
          @click="save"
          >保存</a-button
        ><a-button :disabled="busy" @click="beforeClose"
          >关闭</a-button
        ></a-space
      >
    </a-form>
  </a-drawer>
</template>
<script setup lang="ts">
import {
  ref,
  reactive,
  computed,
  watch,
  onMounted,
  onBeforeUnmount,
} from "vue";
import { useRoute, onBeforeRouteLeave, onBeforeRouteUpdate } from "vue-router";
import { Modal, message } from "ant-design-vue";
import { useProjectStore } from "@/stores/project";
import { useUserStore } from "@/stores/user";
import { createRequestId } from "@/utils/requestId";
import {
  requestEnvironmentGroupsApi as api,
  type EnvironmentGroup,
  type GroupInput,
} from "@/api/requestEnvironmentGroups";
const projectStore = useProjectStore(),
  user = useUserStore(),
  route = useRoute();
const projectId = computed(() =>
  typeof route.query.projectId === "string"
    ? route.query.projectId
    : projectStore.currentProject?.id || "",
);
const items = ref<EnvironmentGroup[]>([]),
  total = ref(0),
  page = ref(1),
  search = ref(""),
  appliedSearch = ref(""),
  loading = ref(false),
  busy = ref(false),
  error = ref(""),
  canEdit = ref(false),
  canDelete = ref(false),
  editorOpen = ref(false),
  editorError = ref(""),
  editingId = ref(""),
  saved = ref("");
type MappingRow = { key: string; projectId: string; environmentId: string };
const draft = reactive({
  name: "",
  description: "",
  expectedRevision: 0,
  requestId: "",
  mappings: [] as MappingRow[],
});
const sourceState = reactive<
  Record<
    string,
    {
      loading: boolean;
      sequence: number;
      options: { id: string; name: string }[];
      error: string;
    }
  >
>({});
let epoch = 0,
  live = true,
  closing = false,
  sequence = 0,
  rowSequence = 0;
const current = (mine: number) => live && mine === epoch;
const navigationCurrent = (mine: number) => current(mine) && !busy.value;
const body = (): GroupInput => ({
  name: draft.name,
  description: draft.description,
  expectedRevision: draft.expectedRevision,
  requestId: draft.requestId,
  mappings: draft.mappings.map(({ projectId, environmentId }) => ({
    projectId,
    environmentId,
  })),
});
const dirty = computed(
  () => editorOpen.value && saved.value !== JSON.stringify(body()),
);
const sourceLoading = computed(() =>
  Object.values(sourceState).some((s) => s.loading),
);
const projectOptions = computed(() =>
  projectStore.projects.map((p) => ({ value: p.id, label: p.name })),
);
const columns = [
  { title: "环境组", dataIndex: "name" },
  { title: "描述", dataIndex: "description" },
  { title: "环境映射", key: "mappings" },
  { title: "操作", key: "actions" },
];
function resetSources() {
  for (const key of Object.keys(sourceState)) delete sourceState[key];
}
async function load() {
  const mine = epoch,
    project = projectId.value,
    ticket = ++sequence;
  if (!project) return;
  loading.value = true;
  error.value = "";
  try {
    const result = await api.list(project, {
      page: page.value,
      size: 20,
      search: appliedSearch.value || undefined,
    });
    if (!current(mine) || ticket !== sequence) return;
    items.value = result.items;
    total.value = result.total;
    canEdit.value = result.canEdit;
    canDelete.value = result.canDelete;
  } catch (exception) {
    if (current(mine) && ticket === sequence) {
      console.error("读取请求环境组失败", exception);
      error.value = "读取失败，请检查项目权限或重试";
    }
  } finally {
    if (current(mine) && ticket === sequence) loading.value = false;
  }
}
watch(
  () => JSON.stringify([projectId.value, user.user?.id]),
  () => {
    ++epoch;
    ++sequence;
    closing = false;
    busy.value = false;
    loading.value = false;
    items.value = [];
    total.value = 0;
    page.value = 1;
    search.value = "";
    appliedSearch.value = "";
    canEdit.value = false;
    canDelete.value = false;
    editorOpen.value = false;
    editorError.value = "";
    saved.value = "";
    resetSources();
    void load();
  },
  { immediate: true, flush: "sync" },
);
function addMapping() {
  if (busy.value || !canEdit.value || draft.mappings.length >= 100) return;
  draft.mappings.push({
    key: String(++rowSequence),
    projectId: "",
    environmentId: "",
  });
}
function removeMapping(key: string) {
  if (busy.value || !canEdit.value) return;
  draft.mappings = draft.mappings.filter((r) => r.key !== key);
  delete sourceState[key];
}
function sourceOptions(row: MappingRow) {
  const options = (sourceState[row.key]?.options || []).map((e) => ({
    value: e.id,
    label: e.name,
  }));
  if (row.environmentId && !options.some((e) => e.value === row.environmentId))
    options.push({
      value: row.environmentId,
      label: `已记录环境 ${row.environmentId}`,
    });
  return options;
}
async function loadSource(key: string) {
  const row = draft.mappings.find((r) => r.key === key);
  if (!row?.projectId) return;
  const mine = epoch,
    project = row.projectId;
  if (!sourceState[key])
    sourceState[key] = { loading: false, sequence: 0, options: [], error: "" };
  const entry = sourceState[key];
  const ticket = ++entry.sequence;
  entry.loading = true;
  entry.error = "";
  try {
    const options = await api.sources(project);
    if (
      !current(mine) ||
      sourceState[key] !== entry ||
      ticket !== entry.sequence ||
      draft.mappings.find((r) => r.key === key)?.projectId !== project
    )
      return;
    entry.options = options;
  } catch (exception) {
    if (
      current(mine) &&
      sourceState[key] === entry &&
      ticket === entry.sequence
    ) {
      console.error("读取来源请求环境失败", exception);
      entry.error = "无权读取或读取失败；当前映射已保留";
    }
  } finally {
    if (
      current(mine) &&
      sourceState[key] === entry &&
      ticket === entry.sequence
    )
      entry.loading = false;
  }
}
async function selectProject(key: string, project: string) {
  if (busy.value || !canEdit.value) return;
  const row = draft.mappings.find((r) => r.key === key);
  if (!row || row.projectId === project) return;
  row.projectId = project;
  row.environmentId = "";
  if (sourceState[key]) sourceState[key].options = [];
  await loadSource(key);
}
async function openEditor(record?: EnvironmentGroup) {
  const mine = epoch;
  if (!(await beforeClose()) || !navigationCurrent(mine)) return;
  if (!record && !canEdit.value) return;
  resetSources();
  editingId.value = record?.id || "";
  Object.assign(draft, {
    name: record?.name || "",
    description: record?.description || "",
    expectedRevision: record?.revision || 0,
    requestId: createRequestId(),
    mappings: (record?.mappings || []).map((m) => ({
      ...m,
      key: String(++rowSequence),
    })),
  });
  editorError.value = "";
  editorOpen.value = true;
  saved.value = JSON.stringify(body());
  for (const row of draft.mappings) void loadSource(row.key);
}
async function beforeClose() {
  if (!live || busy.value || closing) return false;
  if (!editorOpen.value) return true;
  if (!dirty.value) {
    editorOpen.value = false;
    resetSources();
    return true;
  }
  const mine = epoch,
    submitted = JSON.stringify(body());
  closing = true;
  try {
    return await new Promise<boolean>((resolve) =>
      Modal.confirm({
        title: "放弃未保存的环境组？",
        okText: "丢弃草稿",
        cancelText: "继续编辑",
        onOk() {
          if (
            !navigationCurrent(mine) ||
            submitted !== JSON.stringify(body())
          ) {
            resolve(false);
            return;
          }
          editorOpen.value = false;
          editorError.value = "";
          resetSources();
          resolve(true);
        },
        onCancel() {
          resolve(false);
        },
      }),
    );
  } finally {
    if (current(mine)) closing = false;
  }
}
async function save() {
  if (busy.value || closing || !canEdit.value || sourceLoading.value) return;
  const mine = epoch,
    project = projectId.value,
    id = editingId.value,
    input = body();
  if (
    !input.name.trim() ||
    !input.mappings.length ||
    input.mappings.some((m) => !m.projectId || !m.environmentId) ||
    new Set(input.mappings.map((m) => m.projectId)).size !==
      input.mappings.length
  ) {
    editorError.value = "名称和映射不能为空，每个来源项目只能选择一次";
    return;
  }
  busy.value = true;
  editorError.value = "";
  try {
    const result = await api.save(project, input, id || undefined);
    if (!current(mine)) return;
    editingId.value = result.id;
    draft.expectedRevision = result.revision;
    saved.value = JSON.stringify({
      ...input,
      expectedRevision: result.revision,
    });
    if (JSON.stringify(body()) === saved.value) editorOpen.value = false;
    message.success("请求环境组已保存");
    ++sequence;
    await load();
  } catch (exception) {
    if (current(mine)) {
      console.error("保存请求环境组失败", exception);
      editorError.value =
        "保存失败或版本冲突，草稿已保留；请核对当前版本后重试";
    }
  } finally {
    if (current(mine)) busy.value = false;
  }
}
function remove(record: EnvironmentGroup) {
  if (busy.value || closing || !canDelete.value) return;
  const mine = epoch,
    project = projectId.value,
    id = record.id,
    revision = record.revision;
  Modal.confirm({
    title: `删除环境组“${record.name}”？`,
    content: "仍被执行配置引用的环境组会拒绝删除。历史批次的冻结请求不会改变。",
    okText: "删除",
    okType: "danger",
    async onOk() {
      if (!navigationCurrent(mine) || !canDelete.value) return;
      if (
        !(await beforeClose()) ||
        !navigationCurrent(mine) ||
        !canDelete.value
      )
        return;
      busy.value = true;
      try {
        await api.remove(project, id, revision);
        if (!current(mine)) return;
        if (items.value.length === 1 && page.value > 1) --page.value;
        ++sequence;
        await load();
        if (current(mine)) message.success("环境组已删除");
      } catch (exception) {
        if (current(mine)) {
          console.error("删除请求环境组失败", exception);
          message.error("删除失败或仍被引用，请核对后重试");
        }
      } finally {
        if (current(mine)) busy.value = false;
      }
    },
  });
}
async function searchGroups() {
  const mine = epoch;
  if (!(await beforeClose()) || !navigationCurrent(mine)) return;
  appliedSearch.value = search.value;
  page.value = 1;
  await load();
}
async function changePage(value: number) {
  const mine = epoch;
  if (!(await beforeClose()) || !navigationCurrent(mine)) return;
  page.value = value;
  await load();
}
onBeforeRouteLeave(beforeClose);
onBeforeRouteUpdate(beforeClose);
function beforeUnload(event: BeforeUnloadEvent) {
  if (busy.value || dirty.value) {
    event.preventDefault();
    event.returnValue = "";
  }
}
onMounted(() => window.addEventListener("beforeunload", beforeUnload));
onBeforeUnmount(() => {
  live = false;
  ++epoch;
  ++sequence;
  window.removeEventListener("beforeunload", beforeUnload);
});
</script>
<style scoped>
.groups-page {
  background: white;
  padding: 16px;
  min-height: 100%;
  min-width: 0;
}
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}
h2 {
  font-size: 18px;
  margin: 0;
}
.mapping-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin: 10px 0;
}
.mapping-row :deep(.ant-select) {
  flex: 1;
  min-width: 180px;
}
.mapping-error {
  width: 100%;
}
.hint {
  font-size: 12px;
  color: var(--ms-text-secondary);
}
.groups-page :deep(.ant-pagination) {
  margin-top: 16px;
  text-align: right;
}
</style>
