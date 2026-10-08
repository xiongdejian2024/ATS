<template>
  <MinderPopupAnchor
    ref="anchor"
    :zoom="zoom"
    class="minder-tag-dropdown"
    role="listbox"
    :aria-label="label"
    @pointerdown.stop
    @keydown.esc.stop.prevent="emit('close')"
  >
    <button
      v-for="option in options"
      :key="option.value"
      type="button"
      role="option"
      :aria-selected="value === option.value"
      :title="option.label"
      :data-value="option.value"
      :disabled="disabled"
      @click.stop="emit('select', option.value)"
    >
      {{ option.label }}
    </button>
  </MinderPopupAnchor>
</template>
<script setup lang="ts">
import { computed, ref } from "vue";
import { onClickOutside } from "@vueuse/core";
import MinderPopupAnchor from "./MinderPopupAnchor.vue";
const props = defineProps<{
  zoom: number;
  label: string;
  value: string;
  options: { value: string; label: string }[];
  disabled: boolean;
}>();
const emit = defineEmits<{ select: [value: string]; close: [] }>();
const anchor = ref<InstanceType<typeof MinderPopupAnchor>>();
onClickOutside(
  computed(() => anchor.value?.element),
  () => {
    if (!props.disabled) emit("close");
  },
  { ignore: [computed(() => anchor.value?.element?.parentElement)] },
);
</script>
<style scoped>
.minder-tag-dropdown {
  width: 200px;
  max-height: 350px;
  overflow-y: auto;
  padding: 4px;
}
button {
  display: block;
  width: 100%;
  padding: 8px 12px;
  border: 0;
  border-radius: 3px;
  text-align: left;
  font-size: 12px;
  color: #333;
  background: white;
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
  cursor: pointer;
}
button:hover,
button[aria-selected="true"] {
  color: var(--primary-color);
  background: var(--ms-primary-soft);
}
button:disabled {
  cursor: wait;
  opacity: 0.5;
}
</style>
