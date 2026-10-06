<template>
  <div
    ref="menu"
    v-if="actions.length"
    class="node-float-menu"
    role="toolbar"
    :aria-label="`${node.name}节点菜单`"
    :style="{
      transform: `scale(${1 / zoom}) translateX(${shift}px)`,
      transformOrigin: 'top left',
    }"
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
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from "vue";
import { useEventListener, useResizeObserver } from "@vueuse/core";
import {
  FolderAddOutlined,
  PlusOutlined,
  SettingOutlined,
  DeleteOutlined,
} from "@ant-design/icons-vue";
import type { PlanMinderNode } from "./planMinderTree";
import type { MinderAction } from "./planMinderActions";
const props = defineProps<{
  node: PlanMinderNode;
  actions: MinderAction[];
  disabled: boolean;
  zoom: number;
}>();
const menu = ref<HTMLElement>(),
  viewport = ref<HTMLElement>(),
  shift = ref(0);
function positionMenu() {
  if (!menu.value || !viewport.value) return;
  const box = menu.value.getBoundingClientRect(),
    bounds = viewport.value.getBoundingClientRect();
  const anchor = box.left - shift.value;
  shift.value = Math.max(
    bounds.left + 8 - anchor,
    Math.min(0, bounds.right - 8 - anchor - box.width),
  );
}
onMounted(() => {
  viewport.value =
    menu.value?.closest<HTMLElement>(".minder-viewport") || undefined;
  positionMenu();
});
useEventListener(viewport, "scroll", positionMenu);
useResizeObserver(viewport, positionMenu);
watch(
  () => [props.zoom, props.node],
  () => void nextTick(positionMenu),
  { flush: "post" },
);
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
  position: absolute;
  left: 0;
  top: calc(100% + 6px);
  z-index: 30;
  display: flex;
  gap: 8px;
  padding: 4px 8px;
  background: white;
  border-radius: 4px;
  box-shadow: 0 4px 10px -1px #64646626;
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
  background: #f5eafa;
  color: #811fa3;
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
