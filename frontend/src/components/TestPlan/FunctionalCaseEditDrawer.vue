<template>
  <a-drawer
    :open="open"
    title="更新用例"
    width="min(1200px, 100vw)"
    :closable="!saving"
    :mask-closable="!saving"
    :keyboard="!saving"
    destroy-on-close
    @close="confirmClose"
    @after-open-change="afterOpenChange"
  >
    <TestCaseEdit
      v-if="open"
      ref="editor"
      :key="`${projectId}:${caseId}`"
      :project-id="projectId"
      :case-id="caseId"
      embedded
      @dirty="dirty = $event"
      @save="saved"
      @cancel="confirmClose"
    />
    <template #footer>
      <a-space
        ><a-button :disabled="saving" @click="confirmClose">取消</a-button>
        <a-button
          type="primary"
          :loading="saving"
          :disabled="!editor?.canSave()"
          @click="editor?.save()"
          >更新</a-button
        >
      </a-space>
    </template>
  </a-drawer>
</template>
<script setup lang="ts">
import { computed, onBeforeUnmount, ref, watch } from "vue";
import { Modal } from "ant-design-vue";
import TestCaseEdit from "@/components/TestCase/TestCaseEdit.vue";
const props = defineProps<{
  open: boolean;
  projectId: string;
  caseId: string;
}>();
const emit = defineEmits<{
  (e: "update:open", value: boolean): void;
  (e: "dirty", value: boolean): void;
  (e: "busy", value: boolean): void;
}>();
const editor = ref<InstanceType<typeof TestCaseEdit>>();
const saving = computed(() => !!editor.value?.isSaving());
const dirty = ref(false);
watch(saving, (value) => emit("busy", value));
watch(dirty, (value) => emit("dirty", value));
watch(
  () => props.open,
  (value) => {
    if (!value) dirty.value = false;
  },
);
let closing: Promise<boolean> | undefined;
function close() {
  dirty.value = false;
  emit("dirty", false);
  emit("update:open", false);
}
async function confirmClose(): Promise<boolean> {
  if (saving.value) return false;
  if (!dirty.value) {
    close();
    return true;
  }
  if (closing) return closing;
  closing = new Promise((resolve) =>
    Modal.confirm({
      title: "编辑内容尚未保存",
      content: "关闭会丢弃本次主用例修改。",
      okText: "丢弃修改",
      cancelText: "继续编辑",
      onOk() {
        close();
        resolve(true);
      },
      onCancel() {
        resolve(false);
      },
    }),
  );
  try {
    return await closing;
  } finally {
    closing = undefined;
  }
}
function saved() {
  console.info("计划执行页主用例已更新", {
    caseId: props.caseId,
    projectId: props.projectId,
  });
  close();
}
function afterOpenChange(open: boolean) {
  if (!open) {
    emit("busy", false);
  }
}
onBeforeUnmount(() => {
  emit("busy", false);
  emit("dirty", false);
});
defineExpose({ confirmClose });
</script>
<style scoped>
:deep(.test-case-edit) {
  height: auto;
}
:deep(.edit-scroll-content) {
  padding: 0;
}
@media (max-width: 768px) {
  :deep(.steps-table-wrapper) {
    overflow-x: auto;
  }
  :deep(.steps-table-header),
  :deep(.steps-list) {
    min-width: 620px;
  }
}
</style>
