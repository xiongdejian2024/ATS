<template>
  <MinderPopupAnchor
    v-if="actions.length"
    class="node-float-menu"
    role="toolbar"
    :aria-label="`${node.name}节点菜单`"
    :zoom="zoom"
    @pointerdown.stop
  >
    <a-tooltip v-for="action in actions" :key="action" :title="labels[action]">
      <button
        type="button"
        :aria-label="labels[action]"
        :disabled="disabled"
        :class="{
          'mode-button': action === 'mode',
          parallel: node.executionMode === 'parallel',
        }"
        @click.stop="emit('action', action)"
      >
        <FolderAddOutlined v-if="action === 'add'" />
        <PlusOutlined v-else-if="action === 'associate'" />
        <SettingOutlined v-else-if="action === 'configure'" />
        <DeleteOutlined v-else-if="action === 'delete'" />
        <span v-else>{{
          node.executionMode === "parallel" ? "并" : "串"
        }}</span>
      </button>
    </a-tooltip>
  </MinderPopupAnchor>
</template>
<script setup lang="ts">
import MinderPopupAnchor from "./MinderPopupAnchor.vue";
import {
  FolderAddOutlined,
  PlusOutlined,
  SettingOutlined,
  DeleteOutlined,
} from "@ant-design/icons-vue";
import type { PlanMinderNode } from "./planMinderTree";
import type { MinderAction } from "./planMinderActions";
defineProps<{
  node: PlanMinderNode;
  actions: MinderAction[];
  disabled: boolean;
  zoom: number;
}>();
const emit = defineEmits<{ action: [action: MinderAction] }>();
const labels: Record<MinderAction, string> = {
  add: "添加测试集",
  associate: "关联用例",
  mode: "切换执行方式",
  configure: "配置",
  delete: "删除测试集",
};
</script>
<style scoped>
.node-float-menu {
  display: flex;
  gap: 8px;
  padding: 4px 8px;
  white-space: nowrap;
}
button {
  border: 0;
  border-radius: 4px;
  width: 24px;
  height: 24px;
  display: inline-flex;
  justify-content: center;
  align-items: center;
  background: transparent;
  color: #555;
  cursor: pointer;
}
button:hover {
  background: var(--ms-primary-soft);
  color: var(--primary-color);
}
button:disabled {
  cursor: wait;
  opacity: 0.5;
}
.mode-button {
  border-radius: 50%;
  background: #edf3ff;
  color: #165dff;
  font-size: 12px;
}
.mode-button.parallel {
  background: #e8ffea;
  color: #00a870;
}
</style>
