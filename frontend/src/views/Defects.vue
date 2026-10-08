<template>
  <section class="defects-page">
    <header>
      <h2>缺陷</h2>
      <a-space wrap
        ><a-button
          v-if="capabilities.canCreate"
          type="primary"
          @click="openDetail()"
          >新建缺陷</a-button
        ><a-button v-if="capabilities.canUpdate" @click="openTemplates"
          >缺陷模板</a-button
        ><a-button :loading="loading" @click="reload">刷新</a-button></a-space
      >
    </header>
    <a-space wrap class="filters"
      ><a-input-search
        v-model:value="search"
        :maxlength="255"
        placeholder="搜索缺陷标题"
        allow-clear
        @search="applyFilters"
      /><a-select
        v-model:value="status"
        :options="[{ value: '', label: '全部状态' }, ...statusOptions]"
        style="width: 140px"
      /><a-checkbox v-model:checked="archived">已归档</a-checkbox
      ><a-button @click="applyFilters">查询</a-button></a-space
    ><a-alert v-if="error" type="error" :message="error" />
    <a-table
      :columns="columns"
      :data-source="items"
      row-key="id"
      :loading="loading"
      :pagination="false"
      :scroll="{ x: 840 }"
      ><template #bodyCell="{ column, record }"
        ><a v-if="column.key === 'title'" @click="openDetail(record.id)">{{
          record.title
        }}</a
        ><a-tag v-else-if="column.key === 'status'">{{
          statusLabels[record.status] || record.status
        }}</a-tag
        ><span v-else-if="column.key === 'updatedAt'">{{
          new Date(record.updatedAt).toLocaleString("zh-CN")
        }}</span
        ><span v-else-if="column.key === 'revision'">{{ record.revision }}</span
        ><a-tag v-else-if="column.key === 'archived'">{{
          record.archived ? "已归档" : "有效"
        }}</a-tag></template
      ></a-table
    ><a-pagination
      :current="page"
      :total="total"
      :page-size="20"
      :show-size-changer="false"
      @change="paginate"
    />
    <DefectDetailDrawer
      v-if="drawerOpen"
      :key="editorKey"
      ref="drawer"
      :open="drawerOpen"
      :project-id="projectId"
      :defect-id="selectedId || undefined"
      :initial-capabilities="capabilities"
      @update:open="drawerOpen = $event"
      @changed="changed"
    />
    <DefectTemplateManager
      v-if="templatesOpen"
      ref="templateManager"
      :project-id="projectId"
      @closed="templatesOpen = false"
    />
  </section>
</template>
<script setup lang="ts">
import { computed, ref, reactive, watch, nextTick, onBeforeUnmount } from "vue";
import { useRoute, onBeforeRouteLeave, onBeforeRouteUpdate } from "vue-router";
import { useProjectStore } from "@/stores/project";
import { useUserStore } from "@/stores/user";
import {
  defectsApi as api,
  type Defect,
  type DefectCapabilities,
} from "@/api/defects";
import DefectDetailDrawer from "@/components/TestCase/DefectDetailDrawer.vue";
import DefectTemplateManager from "@/components/TestCase/DefectTemplateManager.vue";
const user = useUserStore(),
  project = useProjectStore(),
  route = useRoute();
const projectId = computed(() =>
  typeof route.query.projectId === "string"
    ? route.query.projectId
    : project.currentProject?.id || "",
);
const items = ref<Defect[]>([]),
  total = ref(0),
  page = ref(1),
  search = ref(""),
  status = ref(""),
  archived = ref(false),
  loading = ref(false),
  error = ref("");
const applied = reactive({ search: "", status: "", archived: false }),
  capabilities = reactive<DefectCapabilities>({
    canRead: false,
    canCreate: false,
    canUpdate: false,
    canDelete: false,
  });
const drawerOpen = ref(false),
  selectedId = ref(""),
  editorKey = ref(0),
  drawer = ref<InstanceType<typeof DefectDetailDrawer>>(),
  templatesOpen = ref(false),
  templateManager = ref<InstanceType<typeof DefectTemplateManager>>();
let epoch = 0,
  sequence = 0,
  live = true;
const current = (mine: number) => live && mine === epoch;
const statusLabels: Record<string, string> = {
  open: "待处理",
  in_progress: "处理中",
  resolved: "已解决",
  closed: "已关闭",
};
const statusOptions = Object.entries(statusLabels).map(([value, label]) => ({
  value,
  label,
}));
const columns = [
  { title: "标题", key: "title" },
  { title: "状态", key: "status" },
  { title: "版本", key: "revision" },
  { title: "归档", key: "archived" },
  { title: "更新时间", key: "updatedAt" },
];
async function load() {
  const mine = epoch,
    ticket = ++sequence,
    p = projectId.value;
  if (!p) {
    items.value = [];
    total.value = 0;
    error.value = "请先选择项目";
    return;
  }
  loading.value = true;
  error.value = "";
  try {
    const data = await api.list(p, {
      page: page.value,
      size: 20,
      search: applied.search || undefined,
      status: applied.status || undefined,
      archived: applied.archived,
    });
    if (!current(mine) || ticket !== sequence) return;
    items.value = data.items;
    total.value = data.total;
    for (const key of [
      "canRead",
      "canCreate",
      "canUpdate",
      "canDelete",
    ] as const)
      capabilities[key] = data[key];
  } catch (failure) {
    if (current(mine) && ticket === sequence) {
      items.value = [];
      total.value = 0;
      Object.assign(capabilities, {
        canRead: false,
        canCreate: false,
        canUpdate: false,
        canDelete: false,
      });
      error.value = "读取失败或没有独立缺陷权限，请核对项目后重试";
    }
  } finally {
    if (current(mine) && ticket === sequence) loading.value = false;
  }
}
async function beforeClose() {
  const mine = epoch;
  if (!current(mine)) return false;
  if (!((await drawer.value?.beforeClose()) ?? true) || !current(mine))
    return false;
  if (!((await templateManager.value?.beforeClose()) ?? true) || !current(mine))
    return false;
  return true;
}
async function openDetail(identifier = "") {
  const mine = epoch;
  if (!identifier && !capabilities.canCreate) return;
  if (!(await beforeClose()) || !current(mine)) return;
  await nextTick();
  if (!current(mine)) return;
  templatesOpen.value = false;
  selectedId.value = identifier;
  ++editorKey.value;
  drawerOpen.value = true;
}
async function openTemplates() {
  const mine = epoch;
  if (!capabilities.canUpdate || !(await beforeClose()) || !current(mine))
    return;
  drawerOpen.value = false;
  await nextTick();
  if (current(mine)) templatesOpen.value = true;
}
async function applyFilters() {
  const mine = epoch;
  if (!(await beforeClose()) || !current(mine)) return;
  Object.assign(applied, {
    search: search.value,
    status: status.value,
    archived: archived.value,
  });
  page.value = 1;
  await load();
}
async function paginate(value: number) {
  const mine = epoch;
  if (!(await beforeClose()) || !current(mine)) return;
  page.value = value;
  await load();
}
async function reload() {
  const mine = epoch;
  if (!(await beforeClose()) || !current(mine)) return;
  await load();
}
async function changed() {
  await load();
}
watch(
  () => [projectId.value, user.user?.id],
  () => {
    ++epoch;
    ++sequence;
    loading.value = false;
    drawerOpen.value = false;
    templatesOpen.value = false;
    selectedId.value = "";
    items.value = [];
    total.value = 0;
    page.value = 1;
    search.value = status.value = "";
    archived.value = false;
    Object.assign(applied, { search: "", status: "", archived: false });
    Object.assign(capabilities, {
      canRead: false,
      canCreate: false,
      canUpdate: false,
      canDelete: false,
    });
    void load();
    const identifier = route.query.defectId;
    if (typeof identifier === "string" && identifier)
      void openDetail(identifier);
  },
  { immediate: true, flush: "sync" },
);
watch(
  () => route.query.defectId,
  (identifier) => {
    if (typeof identifier === "string" && identifier)
      void openDetail(identifier);
  },
);
onBeforeUnmount(() => {
  live = false;
  ++epoch;
  ++sequence;
});
onBeforeRouteLeave(beforeClose);
onBeforeRouteUpdate(beforeClose);
</script>
<style scoped>
.defects-page {
  padding: 20px;
  background: #fff;
  border: 1px solid #e8edf5;
  border-radius: 8px;
}
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}
h2 {
  color: #1677ff;
  margin: 0;
}
.filters {
  margin: 16px 0;
}
.ant-pagination {
  margin-top: 16px;
}
@media (max-width: 640px) {
  .defects-page {
    padding: 12px;
  }
}
</style>
