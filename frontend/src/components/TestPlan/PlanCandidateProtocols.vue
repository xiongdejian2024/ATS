<template>
  <a-popover trigger="click" placement="bottomLeft">
    <template #content>
      <div class="protocol-menu">
        <a-checkbox
          :checked="
            modelValue === undefined || selected.length === options.length
          "
          :indeterminate="
            selected.length > 0 && selected.length < options.length
          "
          :disabled="disabled"
          @change="
            emit('update:modelValue', $event.target.checked ? undefined : [])
          "
          >全部</a-checkbox
        >
        <a-divider />
        <a-checkbox-group
          :value="selected"
          :options="options"
          :disabled="disabled"
          @change="change"
        />
        <span v-if="!options.length" class="protocol-empty"
          >当前项目暂无接口协议</span
        >
      </div>
    </template>
    <a-tooltip title="协议">
      <a-button
        type="text"
        aria-label="筛选关联协议"
        :disabled="disabled"
        :class="{ filtered: modelValue !== undefined }"
        ><ApiOutlined
      /></a-button>
    </a-tooltip>
  </a-popover>
</template>
<script setup lang="ts">
import { computed } from "vue";
import { ApiOutlined } from "@ant-design/icons-vue";
const props = defineProps<{
  modelValue?: string[];
  options: string[];
  disabled: boolean;
}>();
const emit = defineEmits<{
  "update:modelValue": [value: string[] | undefined];
}>();
const selected = computed(() => props.modelValue ?? props.options);
function change(values: (string | number | boolean)[]) {
  const list = values.map(String);
  emit(
    "update:modelValue",
    list.length === props.options.length ? undefined : list,
  );
}
</script>
<style scoped>
.protocol-menu {
  min-width: 140px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.protocol-menu :deep(.ant-checkbox-group) {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.protocol-menu :deep(.ant-divider) {
  margin: 0;
}
.filtered {
  color: var(--ms-primary);
  background: var(--ms-primary-soft);
}
.protocol-empty {
  color: var(--ms-text-secondary);
  font-size: 12px;
}
</style>
