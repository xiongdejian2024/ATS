<template>
  <section class="case-editor-page">
    <a-spin v-if="loading" spinning />
    <a-alert
      v-else-if="loadError"
      :message="loadError"
      type="error"
      show-icon
    />
    <TestCaseEdit
      v-else-if="projectId"
      ref="editorRef"
      :key="editorKey"
      :project-id="projectId"
      :case-id="caseId"
      :default-module-id="defaultModuleId"
      :initial-draft="draft"
      allow-continue
      @dirty="dirty = $event"
      @save="saved"
      @cancel="returnToList"
    />
    <a-empty v-else description="请先选择项目" />
  </section>
</template>
<script setup lang="ts">
import { computed, ref, watch, onMounted, onUnmounted } from "vue";
import {
  useRoute,
  useRouter,
  onBeforeRouteLeave,
  onBeforeRouteUpdate,
} from "vue-router";
import { Modal } from "ant-design-vue";
import { useProjectStore } from "@/stores/project";
import { useUserStore } from "@/stores/user";
import { testCaseApi } from "@/api/testCase";
import { copyCaseDraft } from "@/components/TestCase/caseMindMap";
import TestCaseEdit from "@/components/TestCase/TestCaseEdit.vue";
import type { TestCase } from "@/types";
const route = useRoute(),
  router = useRouter(),
  projects = useProjectStore(),
  user = useUserStore();
const projectId = computed(() =>
  typeof route.query.projectId === "string"
    ? route.query.projectId
    : projects.currentProject?.id || "",
);
const caseId = computed(() =>
  typeof route.params.caseId === "string" ? route.params.caseId : "",
);
const defaultModuleId = computed(() =>
  typeof route.query.moduleId === "string" ? route.query.moduleId : "",
);
const draft = ref<Partial<TestCase>>(),
  loading = ref(false),
  loadError = ref(""),
  dirty = ref(false),
  editorKey = ref(0);
const editorRef = ref<InstanceType<typeof TestCaseEdit>>()
let sequence = 0;
watch(
  () => [projectId.value, caseId.value, route.query.copyFrom],
  async () => {
    const current = ++sequence,
      p = projectId.value,
      source = route.query.copyFrom;
    loading.value = true;
    loadError.value = "";
    draft.value = undefined;
    dirty.value = false;
    try {
      if (p && typeof source === "string") {
        const record = await testCaseApi.getTestCase(p, source);
        if (current !== sequence) return;
        draft.value = copyCaseDraft(record);
        console.info("独立页面已加载复制草稿，等待确认创建", {
          sourceId: source,
          projectId: p,
        });
      }
      if (current === sequence) editorKey.value++;
    } catch (error) {
      console.error("加载用例编辑页面失败", error);
      if (current === sequence)
        loadError.value = "加载用例失败，请返回列表重试";
    } finally {
      if (current === sequence) loading.value = false;
    }
  },
  { immediate: true },
);
function canLeave() {
  if (!dirty.value) return true;
  return new Promise<boolean>((resolve) =>
    Modal.confirm({
      title: "内容尚未保存",
      content: "离开后将丢失未保存的修改，是否继续？",
      okText: "离开",
      cancelText: "继续编辑",
      onOk: () => resolve(true),
      onCancel: () => resolve(false),
    }),
  );
}
onBeforeRouteLeave(canLeave);
onBeforeRouteUpdate(canLeave);
function returnToList() {
  return router.push({
    path: "/test-cases",
    query: { projectId: projectId.value },
  });
}
async function saved(record: TestCase, continueCreation = false) {
  dirty.value = false;
  if (continueCreation) {
    await router.replace({
      path: "/test-cases/create",
      query: {
        projectId: projectId.value,
        moduleId: record.moduleId || undefined,
      },
    });
    draft.value = undefined;
    editorKey.value++;
    console.info("用例保存成功，继续新建", {
      caseId: record.id,
      projectId: projectId.value,
    });
    return;
  }
  if (
    caseId.value ||
    localStorage.getItem(`caseCreateSuccessHidden:${user.user?.id}`) === "true"
  )
    await returnToList();
  else
    await router.push({
      path: `/test-cases/${record.id}/created`,
      query: { projectId: projectId.value },
    });
}
function unload(event: BeforeUnloadEvent) {
  if (dirty.value) {
    event.preventDefault();
    event.returnValue = "";
  }
}
function shortcut(event: KeyboardEvent) {
  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "s") {
    event.preventDefault();void editorRef.value?.save()
  }
}
onMounted(() => {window.addEventListener("beforeunload",unload);window.addEventListener("keydown",shortcut)})
onUnmounted(() => {window.removeEventListener("beforeunload",unload);window.removeEventListener("keydown",shortcut)})
</script>
<style scoped>
.case-editor-page {
  height: 100%;
  min-height: 0;
  background: #fff;
}
.case-editor-page :deep(.test-case-edit) {
  height: 100%;
}
</style>
