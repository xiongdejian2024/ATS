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
import { ref } from "vue";
import { Modal } from "ant-design-vue";
import NativeCaseConfig from "./NativeCaseConfig.vue";
defineProps<{
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
function close() {
  if (saving.value) return;
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
      dirty.value = false;
      emit("update:open", false);
    },
  });
}
</script>
