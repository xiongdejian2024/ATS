<template>
  <section class="case-created-page">
    <a-result
      status="success"
      title="用例创建成功"
      :sub-title="record ? `【${record.caseCode}】${record.name}` : ''"
    >
      <template #extra
        ><a-space wrap
          ><a-button type="primary" @click="go('/test-cases/create')"
            >继续新建</a-button
          ><a-button @click="go('/test-cases', { caseId })">查看详情</a-button
          ><a-button @click="go(`/test-cases/${caseId}/edit`)"
            >编辑用例</a-button
          ><a-button @click="go('/test-cases')">返回列表</a-button></a-space
        ></template
      >
    </a-result>
    <a-checkbox v-model:checked="skipNext" @change="savePreference"
      >下次不再提示</a-checkbox
    >
  </section>
</template>
<script setup lang="ts">
import { computed, ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useUserStore } from "@/stores/user";
import { useProjectStore } from "@/stores/project";
import { testCaseApi } from "@/api/testCase";
import type { TestCase } from "@/types";
const route = useRoute(),
  router = useRouter(),
  user = useUserStore(),
  projects = useProjectStore();
const caseId = computed(() => String(route.params.caseId || ""));
const projectId = computed(() =>
  typeof route.query.projectId === "string"
    ? route.query.projectId
    : projects.currentProject?.id || "",
);
const record = ref<TestCase>(),
  skipNext = ref(false);
function go(path: string, query: Record<string, string> = {}) {
  void router.push({ path, query: { projectId: projectId.value, ...query } });
}
function savePreference() {
  try {
    localStorage.setItem(
      `caseCreateSuccessHidden:${user.user?.id}`,
      String(skipNext.value),
    );
  } catch (error) {
    console.error("保存创建成功页提示设置失败", error);
  }
}
onMounted(async () => {
  try {
    record.value = await testCaseApi.getTestCase(projectId.value, caseId.value);
  } catch (error) {
    console.error("加载新建用例摘要失败", error);
  }
});
</script>
<style scoped>
.case-created-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #fff;
  height: 100%;
  padding: 32px 16px;
}
</style>
