<template>
  <a-space wrap class="toolbar"
    ><a-button
      v-if="data?.canCreate"
      type="primary"
      @click="editor?.open('create')"
      >新建缺陷</a-button
    ><a-button v-if="data?.canAssociate" @click="editor?.open('associate')"
      >关联缺陷</a-button
    ><a-input-search
      v-model:value="search"
      placeholder="搜索缺陷标题"
      allow-clear
      @search="reload"
    /><a-button :loading="loading" @click="load">刷新</a-button></a-space
  >
  <a-alert v-if="failed" type="error" message="缺陷列表加载失败" />
  <a-alert
    v-if="data?.detached"
    type="info"
    message="用例已取消关联，缺陷身份快照保留；当前仅可查看"
  />
  <a-spin :spinning="loading">
    <a-empty
      v-if="!data?.items.length && !loading"
      description="暂无关联缺陷"
    />
    <article
      v-for="item in data?.items || []"
      :key="item.linkId"
      class="defect-card"
    >
      <div class="defect-card-header">
        <a @click="view = item">{{ item.externalRef || item.id.slice(0, 8) }}</a
        ><a-popconfirm
          v-if="data?.canAssociate"
          title="取消当前实例的缺陷关联？"
          @confirm="unlink(item.linkId)"
          ><a :aria-disabled="saving">取消关联</a></a-popconfirm
        >
      </div>
      <a class="defect-card-title" :title="item.title" @click="view = item">{{
        item.title
      }}</a>
      <a-tag>{{ defectStatusLabels[item.status] || item.status }}</a-tag>
    </article>
  </a-spin>
  <a-pagination
    v-model:current="page"
    :total="data?.total || 0"
    :page-size="10"
    @change="load"
  />
  <PlanDefectBindingEditor
    ref="editor"
    :plan-id="planId"
    :selection="{ selectIds: [associationKey] }"
    @changed="changed"
  />
  <a-drawer
    :open="!!view"
    title="缺陷详情"
    width="min(640px,100vw)"
    @close="view = undefined"
    ><template v-if="view"
      ><h3>{{ view.title }}</h3>
      <a-tag>{{ defectStatusLabels[view.status] || view.status }}</a-tag>
      <p class="description">{{ view.description || "无描述" }}</p>
      <p>关联实例：{{ view.caseName }}</p></template
    ></a-drawer
  >
</template>
<script setup lang="ts">
import { ref, watch, onBeforeUnmount } from "vue";
import { message } from "ant-design-vue";
import { onBeforeRouteLeave, onBeforeRouteUpdate } from "vue-router";
import PlanDefectBindingEditor from "./PlanDefectBindingEditor.vue";
import {
  planCaseDefectsApi,
  defectStatusLabels,
  type PlanInstanceDefect,
  type DefectPage,
  type DefectCapabilities,
} from "@/api/planCaseDefects";
const props = defineProps<{ planId: string; associationKey: string }>();
const emit = defineEmits<{ changed: [] }>();
const editor = ref<InstanceType<typeof PlanDefectBindingEditor>>(),
  data = ref<
    DefectPage<PlanInstanceDefect> & DefectCapabilities & { detached: boolean }
  >(),
  loading = ref(false),
  saving = ref(false),
  failed = ref(false),
  search = ref(""),
  page = ref(1),
  view = ref<PlanInstanceDefect>();
let sequence = 0;
async function load() {
  const current = ++sequence;
  loading.value = true;
  failed.value = false;
  try {
    const result = await planCaseDefectsApi.list(props.planId, {
      associationKey: props.associationKey,
      page: page.value,
      size: 10,
      search: search.value,
    });
    if (current === sequence) data.value = result;
  } catch (error) {
    console.error("加载实例缺陷失败", error);
    if (current === sequence) {
      failed.value = true;
      data.value = undefined;
    }
  } finally {
    if (current === sequence) loading.value = false;
  }
}
async function reload() {
  page.value = 1;
  await load();
}
async function changed() {
  await reload();
  emit("changed");
}
async function unlink(id: string) {
  if (saving.value) return;
  saving.value = true;
  try {
    await planCaseDefectsApi.unlink(props.planId, id);
    await changed();
    message.success("已取消当前实例的缺陷关联");
  } catch (error) {
    console.error("取消实例缺陷关联失败", error);
    message.error("取消关联失败，请刷新核对权限");
  } finally {
    saving.value = false;
  }
}
async function beforeClose() {
  if (saving.value) {
    message.warning("请等待取消关联完成");
    return false;
  }
  return (await editor.value?.beforeClose()) ?? true;
}
onBeforeRouteLeave(beforeClose);
onBeforeRouteUpdate(beforeClose);
watch(
  () => [props.planId, props.associationKey],
  () => {
    data.value = undefined;
    view.value = undefined;
    search.value = "";
    void reload();
  },
  { immediate: true },
);
onBeforeUnmount(() => sequence++);
defineExpose({ beforeClose });
</script>
<style scoped>
.toolbar {
  margin-bottom: 16px;
}
.toolbar :deep(.ant-input-search) {
  width: 220px;
}
.ant-pagination {
  margin-top: 12px;
}
.description {
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}
.defect-card {
  border: 1px solid #e5e6eb;
  border-radius: 4px;
  padding: 8px;
  margin-bottom: 8px;
}
.defect-card-header {
  display: flex;
  justify-content: space-between;
  gap: 8px;
}
.defect-card-title {
  display: block;
  color: #1d2129;
  margin: 6px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
