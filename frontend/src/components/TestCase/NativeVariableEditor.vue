<template>
  <div class="native-variables">
    <p>使用 ${变量名} 引用。值保留空格和空字符串；停用行不参与执行。</p>
    <div v-for="(row, index) in rows" :key="index" class="variable-row">
      <a-checkbox
        :checked="row.enable"
        :disabled="disabled"
        aria-label="启用变量"
        @change="change(index, 'enable', $event.target.checked)"
      />
      <a-input
        :value="row.name"
        :disabled="disabled"
        :maxlength="255"
        placeholder="变量名"
        aria-label="变量名称"
        @update:value="change(index, 'name', $event)"
      />
      <a-input
        :value="row.value"
        :disabled="disabled"
        :maxlength="20000"
        placeholder="变量值"
        aria-label="变量值"
        @update:value="change(index, 'value', $event)"
      />
      <a-input
        :value="row.description"
        :disabled="disabled"
        :maxlength="1000"
        placeholder="说明"
        aria-label="变量说明"
        @update:value="change(index, 'description', $event)"
      />
      <a-button danger :disabled="disabled" @click="remove(index)"
        >移除</a-button
      >
    </div>
    <a-button :disabled="disabled || rows.length >= 100" @click="add"
      >添加变量</a-button
    >
    <a-alert v-if="error" :message="error" type="error" show-icon />
  </div>
</template>
<script setup lang="ts">
import { ref, watch } from "vue";
import { readNativeVariables, type NativeVariable } from "./nativeVariables";
const props = defineProps<{ modelValue: string; disabled?: boolean }>();
const emit = defineEmits<{ "update:modelValue": [value: string] }>();
const rows = ref<NativeVariable[]>([]),
  error = ref("");
let output = "";
watch(
  () => props.modelValue,
  (raw) => {
    if (raw === output) return;
    output = raw;
    try {
      rows.value = readNativeVariables(raw);
      error.value = "";
    } catch {
      rows.value = [];
      error.value = "变量配置无效，请通过高级配置修正";
    }
  },
  { immediate: true, flush: "sync" },
);
function publish() {
  output = JSON.stringify(rows.value);
  try {
    readNativeVariables(output);
    error.value = "";
  } catch (failure) {
    error.value = failure instanceof Error ? failure.message : "变量配置无效";
  }
  emit("update:modelValue", output);
}
function change<K extends keyof NativeVariable>(
  index: number,
  field: K,
  value: NativeVariable[K],
) {
  if (props.disabled || !rows.value[index]) return;
  rows.value[index][field] = value;
  publish();
}
function add() {
  if (props.disabled || rows.value.length >= 100) return;
  rows.value.push({ name: "", value: "", enable: true, description: "" });
  publish();
}
function remove(index: number) {
  if (props.disabled) return;
  rows.value.splice(index, 1);
  publish();
}
</script>
<style scoped>
.variable-row {
  display: grid;
  grid-template-columns:
    auto minmax(100px, 1fr) minmax(100px, 2fr) minmax(100px, 1fr)
    auto;
  gap: 8px;
  margin-bottom: 8px;
}
@media (max-width: 600px) {
  .variable-row {
    grid-template-columns: auto 1fr;
  }
}
</style>
