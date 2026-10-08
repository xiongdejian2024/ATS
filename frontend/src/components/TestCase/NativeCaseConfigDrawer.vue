<template>
  <a-drawer
    :open="open"
    title="用例配置"
    width="min(800px,100vw)"
    destroy-on-close
    :closable="!saving"
    :keyboard="!saving"
    :mask-closable="!saving"
    @close="close"
    ><NativeCaseConfig
      ref="configRef"
      v-if="open"
      :project-id="projectId"
      :case-id="caseId"
      :category="category"
      @saving="
        (v) => {
          saving = v;
          emit('saving', v);
        }
      "
      @saved="emit('saved')"
      @dirty="dirty = $event"
  /></a-drawer>
</template>
<script setup lang="ts">
import { ref, watch, onBeforeUnmount } from "vue";
import { useUserStore } from "@/stores/user";
import { Modal } from "ant-design-vue";
import NativeCaseConfig from "./NativeCaseConfig.vue";
const props = defineProps<{
  open: boolean;
  projectId: string;
  caseId: string;
  category: string;
}>();
const emit = defineEmits<{
  "update:open": [value: boolean];
  saving: [value: boolean];
  saved: [];
}>();
const saving = ref(false),
  dirty = ref(false);
const configRef = ref<{ canLeave(): boolean | Promise<boolean> }>();
const user = useUserStore();
let epoch = 0,
  live = true;
watch(
  () => [props.projectId, props.caseId, props.open, user.user?.id],
  () => {
    epoch++;
    saving.value = false;
    dirty.value = false;
  },
  { flush: "sync" },
);
onBeforeUnmount(() => {
  live = false;
  epoch++;
});
async function close() {
  if (saving.value) return;
  const context = epoch;
  if (configRef.value) {
    const allowed = await configRef.value.canLeave();
    if (allowed && live && context === epoch && !saving.value)
      emit("update:open", false);
    return;
  }
  if (!dirty.value) {
    emit("update:open", false);
    return;
  }
  Modal.confirm({
    title: "配置尚未保存",
    content: "关闭后将丢失编辑草稿，是否继续？",
    okText: "关闭",
    cancelText: "继续编辑",
    onOk: () => {
      if (!live || context !== epoch || saving.value) return;
      dirty.value = false;
      emit("update:open", false);
    },
  });
}
</script>
