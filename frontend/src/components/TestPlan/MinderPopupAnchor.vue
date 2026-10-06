<template>
  <div
    ref="element"
    class="minder-popup-anchor"
    :style="{
      transform: `scale(${1 / zoom}) translateX(${shift}px)`,
      transformOrigin: 'top left',
    }"
  >
    <slot />
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from "vue";
import { useEventListener, useResizeObserver } from "@vueuse/core";
const props = defineProps<{ zoom: number }>();
const element = ref<HTMLElement>(),
  viewport = ref<HTMLElement>(),
  shift = ref(0);
function positionPopup() {
  if (!element.value || !viewport.value) return;
  const box = element.value.getBoundingClientRect(),
    bounds = viewport.value.getBoundingClientRect();
  const anchor = box.left - shift.value;
  shift.value = Math.max(
    bounds.left + 8 - anchor,
    Math.min(0, bounds.right - 8 - anchor - box.width),
  );
}
onMounted(() => {
  viewport.value =
    element.value?.closest<HTMLElement>(".minder-viewport") || undefined;
  positionPopup();
});
useEventListener(viewport, "scroll", positionPopup);
useResizeObserver([viewport, element], positionPopup);
watch(
  () => props.zoom,
  () => void nextTick(positionPopup),
  { flush: "post" },
);
defineExpose({ element });
</script>
<style scoped>
.minder-popup-anchor {
  position: absolute;
  left: 0;
  top: calc(100% + 6px);
  z-index: 30;
  background: white;
  border-radius: 4px;
  box-shadow: 0 4px 10px -1px #64646626;
}
</style>
