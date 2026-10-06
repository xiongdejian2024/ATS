<template>
  <div
    role="toolbar"
    :aria-label="`已选中${count}个测试集的批量操作`"
    class="minder-batch-menu"
    @pointerdown.stop
  >
    <a-tooltip title="删除">
      <button
        type="button"
        aria-label="删除选中的测试集"
        :disabled="disabled"
        @click="emit('delete')"
      >
        <DeleteOutlined />
      </button>
    </a-tooltip>
  </div>
</template>
<script setup lang="ts">
import { DeleteOutlined } from "@ant-design/icons-vue";
defineProps<{ count: number; disabled: boolean }>();
const emit = defineEmits<{ delete: [] }>();
</script>
<style scoped>
.minder-batch-menu {
  position: absolute;
  bottom: 32px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 35;
  padding: 4px 8px;
  border-radius: 4px;
  background: white;
  box-shadow: 0 4px 10px -1px #64646626;
}
button {
  border: 0;
  border-radius: 4px;
  width: 24px;
  height: 24px;
  display: flex;
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
</style>
