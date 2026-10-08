<template>
  <section class="pools-page">
    <header>
      <h2>独立资源池</h2>
      <a-space
        ><a-input
          v-model:value="search"
          placeholder="搜索资源池"
          :maxlength="255"
          @press-enter="searchPools"
        /><a-button :disabled="busy" @click="searchPools">搜索</a-button
        ><a-button
          v-if="canEdit"
          type="primary"
          :disabled="busy"
          @click="openEditor()"
          >新建资源池</a-button
        ></a-space
      >
    </header>
    <p class="hint">
      复用现有 Agent
      节点，资源池与接口请求环境分别配置。容量为当前记录，实际派发仍按节点共享槽位控制。
    </p>
    <a-alert v-if="error" :message="error" type="error" show-icon
      ><template #action
        ><a-button @click="load">重试</a-button></template
      ></a-alert
    >
    <a-table
      :loading="loading"
      :data-source="items"
      :columns="columns"
      row-key="id"
      :pagination="false"
      :scroll="{ x: 950 }"
    >
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'enabled'"
          ><a-tag :color="record.enabled ? 'blue' : 'default'">{{
            record.enabled ? "启用" : "停用"
          }}</a-tag></template
        >
        <template v-else-if="column.key === 'scope'"
          >{{
            record.allProjects
              ? "全部项目"
              : canEdit
                ? `${record.projectIds.length} 个项目`
                : "当前项目可用"
          }}
          /
          {{
            record.applications
              .map((v: string) => (v === "api" ? "API" : "场景"))
              .join("、")
          }}</template
        >
        <template v-else-if="column.key === 'capacity'"
          >在线 {{ record.capacity.online }} / 配置
          {{ record.capacity.configured }}；运行
          {{ record.capacity.running }}，可用
          {{ record.capacity.available }}</template
        >
        <a-space v-else-if="column.key === 'actions'"
          ><a-button type="link" :disabled="busy" @click="openEditor(record)">{{
            canEdit ? "编辑" : "查看"
          }}</a-button
          ><a-button
            v-if="canEdit"
            type="link"
            :disabled="busy"
            @click="toggle(record)"
            >{{ record.enabled ? "停用" : "启用" }}</a-button
          ><a-button
            v-if="canDelete"
            danger
            type="link"
            :disabled="busy"
            @click="remove(record)"
            >删除</a-button
          ></a-space
        >
      </template>
    </a-table>
    <a-pagination
      :current="page"
      :page-size="20"
      :total="total"
      :show-size-changer="false"
      @change="changePage"
    />
  </section>
  <a-drawer
    :open="editorOpen"
    :title="editingId ? (canEdit ? '编辑资源池' : '查看资源池') : '新建资源池'"
    width="min(720px,100vw)"
    :closable="!busy"
    :mask-closable="!busy"
    :keyboard="!busy"
    @close="beforeClose"
  >
    <a-alert v-if="editorError" :message="editorError" type="error" show-icon />
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
      <a-form-item label="类型">现有 Agent 节点（Node）</a-form-item>
      <a-form-item label="启用"
        ><a-switch v-model:checked="draft.enabled" :disabled="busy || !canEdit"
      /></a-form-item>
      <a-form-item label="适用执行"
        ><a-checkbox-group
          v-model:value="draft.applications"
          :options="[
            { label: 'API', value: 'api' },
            { label: '场景', value: 'scenario' },
          ]"
          :disabled="busy || !canEdit"
      /></a-form-item>
      <a-form-item label="适用项目"
        ><a-switch
          :checked="draft.allProjects"
          :disabled="busy || !canEdit"
          @change="setAllProjects"
        />
        全部项目
        <a-select
          v-if="canEdit && !draft.allProjects"
          v-model:value="draft.projectIds"
          mode="multiple"
          :options="projectOptions"
          :max-tag-count="5"
          placeholder="选择项目"
          :disabled="busy"
        />
        <p v-else-if="!draft.allProjects" class="hint">
          该资源池按项目开放；当前项目可用。
        </p>
      </a-form-item>
      <a-form-item label="Agent 节点">
        <a-select
          :value="draft.environmentIds"
          mode="multiple"
          :options="nodeOptions"
          :max-tag-count="5"
          :disabled="busy || !canEdit"
          :loading="nodeLoading"
          :filter-option="false"
          show-search
          @search="searchNodes"
          @change="selectNodes"
        />
        <a-space v-if="canEdit"
          ><a-button :disabled="busy || nodeLoading" @click="loadNodes(false)"
            >刷新候选</a-button
          ><a-button
            v-if="nodeMore"
            :disabled="busy || nodeLoading"
            @click="loadNodes(true)"
            >更多候选</a-button
          ><span>已选择 {{ draft.environmentIds.length }} / 100</span></a-space
        >
        <a-alert v-if="nodeError" :message="nodeError" type="error" />
      </a-form-item>
      <p class="hint">
        停用或修改适用范围只影响新批次，已创建批次继续使用冻结的节点成员；被执行配置引用的池不能删除。
      </p>
      <a-space
        ><a-button
          v-if="canEdit"
          type="primary"
          :loading="busy"
          :disabled="busy || nodeLoading"
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
import { useUserStore } from "@/stores/user";
import { useProjectStore } from "@/stores/project";
import { createRequestId } from "@/utils/requestId";
import {
  globalResourcePoolsApi as api,
  type ResourcePool,
  type PoolInput,
  type PoolNode,
} from "@/api/globalResourcePools";
const user = useUserStore(),
  project = useProjectStore(),
  route = useRoute();
const projectId = computed(() =>
  typeof route.query.projectId === "string"
    ? route.query.projectId
    : project.currentProject?.id || "",
);
const items = ref<ResourcePool[]>([]),
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
const draft = reactive<PoolInput>({
  name: "",
  description: "",
  type: "Node",
  enabled: true,
  applications: ["api", "scenario"],
  allProjects: false,
  projectIds: [],
  environmentIds: [],
  expectedRevision: 0,
  requestId: "",
});
const nodeLoading = ref(false),
  nodeError = ref(""),
  nodeSearch = ref(""),
  nodePage = ref(1),
  nodeTotal = ref(0),
  nodeItems = ref<PoolNode[]>([]),
  nodeCache = reactive<Record<string, PoolNode>>({});
let epoch = 0,
  sequence = 0,
  nodeSequence = 0,
  live = true,
  closing = false,
  nodeTimer: ReturnType<typeof setTimeout> | undefined;
const current = (mine: number) => live && mine === epoch;
const navigationCurrent = (mine: number) => current(mine) && !busy.value;
const body = (): PoolInput => ({
  ...draft,
  applications: [...draft.applications],
  projectIds: [...draft.projectIds],
  environmentIds: [...draft.environmentIds],
});
const dirty = computed(
  () => editorOpen.value && saved.value !== JSON.stringify(body()),
);
const nodeMore = computed(() => nodePage.value * 50 < nodeTotal.value);
const projectOptions = computed(() => {
  const options = project.projects.map((p) => ({ value: p.id, label: p.name }));
  for (const id of draft.projectIds)
    if (!options.some((p) => p.value === id))
      options.push({ value: id, label: `已记录项目 ${id}` });
  return options;
});
const nodeOptions = computed(() => {
  const unique = new Set([
    ...draft.environmentIds,
    ...nodeItems.value.map((n) => n.id),
  ]);
  return [...unique].map((id) => ({
    value: id,
    label: nodeCache[id]
      ? nodeCache[id].name + (nodeCache[id].enabled ? "" : "（已停用）")
      : `已记录节点 ${id}`,
    disabled:
      !!nodeCache[id] &&
      !nodeCache[id].enabled &&
      !draft.environmentIds.includes(id),
  }));
});
const columns = [
  { title: "名称", dataIndex: "name" },
  { title: "状态", key: "enabled" },
  { title: "适用范围", key: "scope" },
  { title: "节点容量", key: "capacity" },
  { title: "操作", key: "actions" },
];
function resetNodes() {
  ++nodeSequence;
  clearTimeout(nodeTimer);
  nodeTimer = undefined;
  nodeItems.value = [];
  nodeSearch.value = "";
  nodePage.value = 1;
  nodeTotal.value = 0;
  nodeError.value = "";
  nodeLoading.value = false;
  for (const key of Object.keys(nodeCache)) delete nodeCache[key];
}
function selectNodes(values: string[]) {
  if (!editorOpen.value || !canEdit.value || busy.value) return;
  const ids = [...new Set(values)];
  if (ids.length > 100) {
    nodeError.value = "最多选择100个节点，请先移除其他节点";
    return;
  }
  const selected = new Set(draft.environmentIds);
  if (
    ids.some(
      (id) => !selected.has(id) && (!nodeCache[id] || !nodeCache[id].enabled),
    )
  ) {
    nodeError.value = "停用节点不能重新选入";
    return;
  }
  draft.environmentIds = ids;
  const keep = new Set([...ids, ...nodeItems.value.map((n) => n.id)]);
  for (const key of Object.keys(nodeCache))
    if (!keep.has(key)) delete nodeCache[key];
  nodeError.value = "";
}
async function load() {
  const mine = epoch,
    ticket = ++sequence;
  loading.value = true;
  error.value = "";
  try {
    const data = await api.list({
      projectId: projectId.value || undefined,
      page: page.value,
      size: 20,
      search: appliedSearch.value || undefined,
    });
    if (!current(mine) || ticket !== sequence) return;
    items.value = data.items;
    total.value = data.total;
    canEdit.value = data.canEdit;
    canDelete.value = data.canDelete;
  } catch (exception) {
    if (current(mine) && ticket === sequence) {
      console.error("读取资源池失败", exception);
      error.value = "读取失败，请选择有权限的项目或重试";
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
    editingId.value = "";
    saved.value = "";
    resetNodes();
    void load();
  },
  { immediate: true, flush: "sync" },
);
async function loadNodes(more = false) {
  if (!editorOpen.value || !canEdit.value || busy.value) return;
  const mine = epoch,
    ticket = ++nodeSequence,
    target = more ? nodePage.value + 1 : 1;
  nodeLoading.value = true;
  nodeError.value = "";
  try {
    const data = await api.nodes({
      page: target,
      size: 50,
      search: nodeSearch.value || undefined,
    });
    if (!current(mine) || ticket !== nodeSequence || !editorOpen.value) return;
    nodeItems.value = data.items;
    nodePage.value = target;
    nodeTotal.value = data.total;
    const keep = new Set([
      ...draft.environmentIds,
      ...data.items.map((n) => n.id),
    ]);
    for (const key of Object.keys(nodeCache))
      if (!keep.has(key)) delete nodeCache[key];
    for (const item of data.items) nodeCache[item.id] = item;
  } catch (exception) {
    if (current(mine) && ticket === nodeSequence && editorOpen.value) {
      console.error("读取候选节点失败", exception);
      nodeError.value = "读取失败，已选择的节点保留；可重试";
    }
  } finally {
    if (current(mine) && ticket === nodeSequence) nodeLoading.value = false;
  }
}
function searchNodes(value: string) {
  nodeSearch.value = value.slice(0, 255);
  ++nodeSequence;
  clearTimeout(nodeTimer);
  const mine = epoch;
  nodeTimer = setTimeout(() => {
    if (current(mine) && editorOpen.value) void loadNodes(false);
  }, 250);
}
function setAllProjects(value: boolean) {
  if (busy.value || !canEdit.value) return;
  draft.allProjects = value;
  if (value) draft.projectIds = [];
}
async function openEditor(record?: ResourcePool) {
  const mine = epoch;
  if (
    !(await beforeClose()) ||
    !navigationCurrent(mine) ||
    (!record && !canEdit.value)
  )
    return;
  resetNodes();
  editingId.value = record?.id || "";
  Object.assign(draft, {
    name: record?.name || "",
    description: record?.description || "",
    type: "Node",
    enabled: record?.enabled ?? true,
    applications: [...(record?.applications || ["api", "scenario"])],
    allProjects: record?.allProjects || false,
    projectIds: [...(record?.projectIds || [])],
    environmentIds: [...(record?.environmentIds || [])],
    expectedRevision: record?.revision || 0,
    requestId: createRequestId(),
  });
  for (const node of record?.nodes || []) nodeCache[node.id] = node;
  editorError.value = "";
  editorOpen.value = true;
  saved.value = JSON.stringify(body());
  if (canEdit.value) void loadNodes(false);
}
async function beforeClose() {
  if (!live || busy.value || closing) return false;
  if (!editorOpen.value) return true;
  if (!dirty.value) {
    editorOpen.value = false;
    resetNodes();
    return true;
  }
  const mine = epoch,
    submitted = JSON.stringify(body());
  closing = true;
  try {
    return await new Promise<boolean>((resolve) =>
      Modal.confirm({
        title: "放弃未保存的资源池？",
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
          resetNodes();
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
  if (busy.value || closing || !canEdit.value || nodeLoading.value) return;
  const mine = epoch,
    id = editingId.value,
    input = body();
  if (
    !input.name.trim() ||
    !input.applications.length ||
    !input.environmentIds.length ||
    input.environmentIds.length > 100 ||
    (!input.allProjects && !input.projectIds.length) ||
    input.projectIds.length > 100
  ) {
    editorError.value = "请填写名称、适用范围和1至100个节点";
    return;
  }
  busy.value = true;
  editorError.value = "";
  try {
    const result = await api.save(input, id || undefined);
    if (!current(mine)) return;
    editingId.value = result.id;
    draft.expectedRevision = result.revision;
    saved.value = JSON.stringify({
      ...input,
      expectedRevision: result.revision,
    });
    if (JSON.stringify(body()) === saved.value) {
      editorOpen.value = false;
      resetNodes();
    }
    message.success("资源池已保存");
    ++sequence;
    await load();
  } catch (exception) {
    if (current(mine)) {
      console.error("保存资源池失败", exception);
      editorError.value =
        "保存失败或版本冲突，草稿已保留；请核对当前版本后重试";
    }
  } finally {
    if (current(mine)) busy.value = false;
  }
}
async function toggle(record: ResourcePool) {
  if (busy.value || closing || !canEdit.value) return;
  const mine = epoch,
    id = record.id,
    revision = record.revision,
    enabled = !record.enabled;
  if (!(await beforeClose()) || !navigationCurrent(mine) || !canEdit.value)
    return;
  busy.value = true;
  try {
    await api.enabled(id, enabled, revision);
    if (!current(mine)) return;
    ++sequence;
    await load();
    if (current(mine))
      message.success(enabled ? "资源池已启用" : "资源池已停用");
  } catch (exception) {
    if (current(mine)) {
      console.error("资源池启停失败", exception);
      message.error("修改失败或版本冲突，请刷新后核对");
    }
  } finally {
    if (current(mine)) busy.value = false;
  }
}
function remove(record: ResourcePool) {
  if (busy.value || closing || !canDelete.value) return;
  const mine = epoch,
    id = record.id,
    revision = record.revision;
  Modal.confirm({
    title: `删除资源池“${record.name}”？`,
    content: "被执行配置引用的资源池会拒绝删除；冻结批次保持原成员。",
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
        await api.remove(id, revision);
        if (!current(mine)) return;
        if (items.value.length === 1 && page.value > 1) --page.value;
        ++sequence;
        await load();
        if (current(mine)) message.success("资源池已删除");
      } catch (exception) {
        if (current(mine)) {
          console.error("删除资源池失败", exception);
          message.error("删除失败或仍被引用，请核对后重试");
        }
      } finally {
        if (current(mine)) busy.value = false;
      }
    },
  });
}
async function searchPools() {
  const mine = epoch;
  if (!(await beforeClose()) || !navigationCurrent(mine)) return;
  page.value = 1;
  appliedSearch.value = search.value;
  await load();
}
async function changePage(value: number) {
  const mine = epoch;
  if (!(await beforeClose()) || !navigationCurrent(mine)) return;
  page.value = value;
  await load();
}
function beforeUnload(event: BeforeUnloadEvent) {
  if (dirty.value || busy.value) {
    event.preventDefault();
    event.returnValue = "";
  }
}
onMounted(() => window.addEventListener("beforeunload", beforeUnload));
onBeforeUnmount(() => {
  live = false;
  ++epoch;
  ++sequence;
  resetNodes();
  window.removeEventListener("beforeunload", beforeUnload);
});
onBeforeRouteLeave(beforeClose);
onBeforeRouteUpdate(beforeClose);
</script>
<style scoped>
.pools-page {
  padding: 20px;
  background: #fff;
  border: 1px solid #e8edf5;
  border-radius: 8px;
}
header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}
h2 {
  margin: 0;
  color: #1677ff;
}
.hint {
  color: #667085;
  font-size: 12px;
  line-height: 1.7;
}
.ant-pagination {
  margin-top: 16px;
}
.ant-select {
  width: 100%;
}
@media (max-width: 640px) {
  .pools-page {
    padding: 12px;
  }
  header :deep(.ant-space) {
    flex-wrap: wrap;
    width: 100%;
  }
}
</style>
