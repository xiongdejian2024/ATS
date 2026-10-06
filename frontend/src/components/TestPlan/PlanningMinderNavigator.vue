<template>
  <div class="minder-navigator">
    <div class="minder-navigation" role="toolbar" aria-label="脑图导航器">
      <a-slider
        class="navigation-slider"
        :value="Math.max(0, zoom * 100 - 50)"
        :min="0"
        :max="150"
        :step="1"
        :marks="{ 50: '' }"
        :tip-formatter="zoomLabel"
        aria-label-for-handle="脑图缩放比例"
        @change="setZoom"
      />
      <button
        type="button"
        aria-label="拖动画布"
        title="拖动画布"
        :aria-pressed="hand"
        @click="emit('hand', !hand)"
      >
        <DragOutlined />
      </button>
      <button
        type="button"
        aria-label="切换缩略图"
        title="缩略图"
        :aria-pressed="preview"
        @click="emit('preview', !preview)"
      >
        <PlanningMinderNavigationIcon kind="preview" />
      </button>
      <button
        type="button"
        aria-label="定位根节点"
        title="定位根节点"
        @click="emit('camera')"
      >
        <AimOutlined />
      </button>
      <a-popover trigger="hover" placement="rightBottom">
        <template #content
          ><div class="shortcut-help">
            <h4>快捷键</h4>
            <div class="shortcut-list">
              <div v-for="shortcut in shortcuts" :key="shortcut[0]">
                <span>{{ shortcut[0] }}</span
                ><kbd>{{ shortcut[1] }}</kbd>
              </div>
            </div>
          </div></template
        >
        <button
          type="button"
          aria-label="脑图快捷键帮助"
          title="快捷键"
          @click="emit('camera')"
        >
          <PlanningMinderNavigationIcon kind="keyboard" />
        </button>
      </a-popover>
    </div>
    <svg
      v-if="preview && geometry"
      ref="minimap"
      class="minder-preview"
      role="img"
      aria-label="脑图缩略图，点击或拖动定位画布"
      :viewBox="`9.5 9.5 ${geometry.width - 19} ${geometry.height - 19}`"
      @pointerdown="start"
      @pointermove="move"
      @pointerup="stop"
      @pointercancel="stop"
      @lostpointercapture="stop"
    >
      <g :transform="`translate(${geometry.offset.x} ${geometry.offset.y})`">
        <path
          v-for="(path, index) in geometry.paths"
          :key="index"
          :d="path"
          fill="none"
          stroke="#811fa3"
          stroke-width="1"
        />
      </g>
      <rect
        v-for="(box, id) in geometry.nodes"
        :key="id"
        :x="box.x"
        :y="box.y"
        :width="box.width"
        :height="box.height"
        rx="3"
        fill="#811fa3"
      />
      <rect
        :x="visible.x"
        :y="visible.y"
        :width="visible.width"
        :height="visible.height"
        fill="#ff000010"
        stroke="#f53f3f"
        stroke-width="1"
        vector-effect="non-scaling-stroke"
      />
    </svg>
  </div>
</template>
<script setup lang="ts">
import { ref } from "vue";
import PlanningMinderNavigationIcon from "./PlanningMinderNavigationIcon.vue";
import { DragOutlined, AimOutlined } from "@ant-design/icons-vue";
import type { MinderBox, MinderGeometry } from "./planMinderView";
defineProps<{
  zoom: number;
  hand: boolean;
  preview: boolean;
  geometry?: MinderGeometry;
  visible: MinderBox;
}>();
const emit = defineEmits<{
  zoom: [value: number];
  hand: [value: boolean];
  preview: [value: boolean];
  camera: [];
  locate: [point: { x: number; y: number }];
}>();
function zoomLabel(value: number | undefined) {
  return `${(value || 0) + 50}%`;
}
function setZoom(value: number | number[]) {
  if (typeof value === "number") emit("zoom", (value + 50) / 100);
}
const shortcuts = [
  ["展开/收起节点", "/"],
  ["添加同级测试集", "Enter"],
  ["添加子测试集", "Tab"],
  ["删除测试集", "Backspace"],
  ["文本编辑", "Space"],
];
const minimap = ref<SVGSVGElement>();
let pointer: number | undefined;
function locate(event: PointerEvent) {
  const element = minimap.value,
    matrix = element?.getScreenCTM();
  if (!element || !matrix) return;
  const point = new DOMPoint(event.clientX, event.clientY).matrixTransform(
    matrix.inverse(),
  );
  emit("locate", { x: point.x, y: point.y });
}
function start(event: PointerEvent) {
  if (event.button !== 0 || !minimap.value) return;
  pointer = event.pointerId;
  minimap.value.setPointerCapture(pointer);
  locate(event);
  event.preventDefault();
}
function move(event: PointerEvent) {
  if (event.pointerId === pointer) locate(event);
}
function stop() {
  if (pointer !== undefined && minimap.value?.hasPointerCapture(pointer))
    minimap.value.releasePointerCapture(pointer);
  pointer = undefined;
}
</script>
<style scoped>
.minder-navigator {
  position: absolute;
  left: 6px;
  bottom: 6px;
  z-index: 45;
}
.minder-navigation {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 8px;
  border-radius: 4px;
  background: white;
  box-shadow: 0 2px 8px #0002;
}
.navigation-slider {
  width: 100px;
  margin: 6px 0 6px 8px;
}
.minder-navigation button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  width: 24px;
  height: 24px;
  border: 0;
  border-radius: 3px;
  background: white;
  color: #86909c;
  cursor: pointer;
  font-size: 16px;
}
.minder-navigation button[aria-pressed="true"] {
  background: #f5eafa;
  color: #811fa3;
}
.minder-preview {
  position: absolute;
  left: 45px;
  bottom: 36px;
  z-index: 44;
  box-sizing: border-box;
  width: 240px;
  height: 160px;
  padding: 8px;
  background: white;
  border-radius: 4px;
  box-shadow: 0 2px 8px #0002;
  cursor: crosshair;
  touch-action: none;
}
.shortcut-help {
  padding: 4px;
}
.shortcut-help h4 {
  margin: 0 0 4px;
  font-size: 14px;
  font-weight: 500;
}
.shortcut-list {
  display: grid;
  grid-template-columns: repeat(2, 190px);
  gap: 8px 12px;
}
.shortcut-list > div {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 4px 8px;
  font-size: 12px;
  border-radius: 4px;
  background: #f7f8fa;
}
kbd {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 22px;
  height: 22px;
  padding: 2px 4px;
  border: 1px solid #e5e6eb;
  border-radius: 4px;
  color: #86909c;
  font-size: 12px;
}
@media (max-width: 768px) {
  .shortcut-list {
    grid-template-columns: 190px;
  }
}
</style>
