<template>
  <div class="minder-header" role="toolbar" aria-label="脑图视图操作">
    <a-dropdown :trigger="['click']"
      ><button
        type="button"
        aria-label="选择脑图布局"
        :title="minderModes.find((item) => item.value === mode)?.label"
      >
        <PlanningMinderLayoutIcon :mode="mode" /></button
      ><template #overlay
        ><a-menu
          class="minder-layout-menu"
          :selected-keys="[mode]"
          @click="chooseMode"
          ><a-menu-item
            v-for="item in minderModes"
            :key="item.value"
            :aria-label="item.label"
            :title="item.label"
            :data-layout="item.value"
            ><PlanningMinderLayoutIcon
              :mode="item.value" /></a-menu-item></a-menu></template
    ></a-dropdown>
    <span class="separator" />
    <button
      type="button"
      :aria-label="fullscreen ? '退出脑图全屏' : '脑图全屏'"
      :title="fullscreen ? '退出全屏' : '全屏'"
      @click="emit('fullscreen')"
    >
      <FullscreenExitOutlined v-if="fullscreen" /><FullscreenOutlined v-else />
    </button>
    <button
      v-if="canEdit"
      type="button"
      class="save-view"
      aria-label="保存脑图规划"
      title="保存 (Ctrl/⌘ + S)"
      :disabled="disabled"
      @click="emit('save')"
    >
      保存 ({{ commandKey }} + S)
    </button>
  </div>
</template>
<script setup lang="ts">
import {
  FullscreenOutlined,
  FullscreenExitOutlined,
} from "@ant-design/icons-vue";
import PlanningMinderLayoutIcon from "./PlanningMinderLayoutIcon.vue";
const commandKey = /Mac|iPhone|iPad/.test(navigator.platform) ? "⌘" : "Ctrl";
import { minderModes, type MinderMode } from "./planMinderView";
defineProps<{
  mode: MinderMode;
  fullscreen: boolean;
  canEdit: boolean;
  disabled: boolean;
}>();
function chooseMode(item: { key: string | number }) {
  emit("mode", item.key as MinderMode);
}
const emit = defineEmits<{
  mode: [value: MinderMode];
  fullscreen: [];
  save: [];
}>();
</script>
<style scoped>
.minder-header {
  position: absolute;
  top: 16px;
  right: 4px;
  z-index: 45;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 8px;
  background: white;
  border-radius: 4px;
  box-shadow: 0 2px 8px #0002;
}
button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  width: 24px;
  height: 24px;
  background: white;
  border: 0;
  border-radius: 3px;
  cursor: pointer;
  font-size: 16px;
  color: #4e5969;
}
button:disabled {
  cursor: default;
  color: #c9cdd4;
}
.separator {
  height: 16px;
  border-left: 1px solid #e5e6eb;
}
.save-view {
  width: auto;
  padding: 2px 8px;
  font-size: 12px;
  border: 1px solid #e5e6eb;
}
</style>
