<template>
  <a-space :size="4" class="selection-header">
    <a-checkbox
      aria-label="选择用例"
      :checked="count > 0 && ((all && !excludedCount) || count === total)"
      :indeterminate="
        count > 0 && !((all && !excludedCount) || count === total)
      "
      :disabled="disabled"
      @change="$emit('togglePage')"
    />
    <a-dropdown :trigger="['click']" :disabled="disabled">
      <a-button
        type="text"
        size="small"
        aria-label="选择范围"
        :disabled="disabled"
        ><DownOutlined
      /></a-button>
      <template #overlay
        ><a-menu @click="choose">
          <a-menu-item key="current">全选当前页</a-menu-item>
          <a-menu-item v-if="all" key="clear">取消全选所有页</a-menu-item>
          <a-menu-item v-else key="all">全选所有页</a-menu-item>
        </a-menu></template
      >
    </a-dropdown>
  </a-space>
</template>
<script setup lang="ts">
import { DownOutlined } from "@ant-design/icons-vue";
defineProps<{
  count: number;
  total: number;
  all: boolean;
  excludedCount: number;
  disabled: boolean;
}>();
const emit = defineEmits<{ togglePage: []; current: []; all: []; clear: [] }>();
function choose({ key }: { key: string | number }) {
  if (key === "current") emit("current");
  else if (key === "all") emit("all");
  else emit("clear");
}
</script>
<style scoped>
.selection-header {
  white-space: nowrap;
}
.selection-header :deep(.ant-btn) {
  width: 16px;
  min-width: 16px;
  padding: 0;
}
</style>
