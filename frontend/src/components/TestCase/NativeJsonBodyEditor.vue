<template>
  <div class="json-body-editor">
    <div class="json-mode-toolbar">
      <a-radio-group
        :value="schemaMode"
        option-type="button"
        :options="[
          { value: true, label: 'Schema' },
          { value: false, label: 'Json' },
        ]"
        :disabled="disabled"
        aria-label="JSON正文编辑模式"
        @change="emit('update:schemaMode', $event.target.value)"
      /><a-button
        v-if="!schemaMode && !disabled"
        :loading="generating"
        @click="generate"
        >自动生成</a-button
      >
    </div>
    <NativeJsonSchemaEditor
      v-show="schemaMode"
      :model-value="schema"
      :project-id="projectId"
      :disabled="disabled"
      @update:model-value="emit('update:schema', $event)"
    />
    <a-textarea
      v-show="!schemaMode"
      :value="modelValue"
      :disabled="disabled"
      :rows="12"
      aria-label="HTTP请求体JSON"
      @change="emit('update:modelValue', $event.target.value)"
    />
  </div>
</template>
<script setup lang="ts">
import { ref, onUnmounted } from "vue";
import { message } from "ant-design-vue";
import NativeJsonSchemaEditor from "./NativeJsonSchemaEditor.vue";
import { readJsonSchema } from "./nativeJsonSchema";
import { convertJsonSchema } from "@/api/nativeJsonSchema";
const props = defineProps<{
  modelValue: string;
  schema: string;
  schemaMode: boolean;
  projectId: string;
  disabled?: boolean;
}>();
const emit = defineEmits<{
  "update:modelValue": [value: string];
  "update:schema": [value: string];
  "update:schemaMode": [value: boolean];
}>();
const generating = ref(false);
let active = true;
onUnmounted(() => {
  active = false;
});
async function generate() {
  if (props.disabled || generating.value) return;
  const original = props.schema;
  const originalProject = props.projectId,
    originalBody = props.modelValue;
  generating.value = true;
  try {
    if (!props.projectId) throw new Error("请先选择项目");
    const schema = readJsonSchema(original);
    if (
      !Object.keys(schema.properties || {}).length &&
      !(schema.items || []).length
    ) {
      message.warning("请先设置JSON Schema");
      return;
    }
    const result = await convertJsonSchema(props.projectId, schema, "generate");
    // 生成期间切换用例或修改Schema时不能把旧响应写进新草稿。
    if (
      !active ||
      props.projectId !== originalProject ||
      props.modelValue !== originalBody ||
      props.schema !== original ||
      props.schemaMode ||
      props.disabled
    ) {
      message.warning("Schema已变化，请重新生成");
      return;
    }
    emit("update:modelValue", result.jsonValue);
  } catch (exception) {
    console.error("Schema自动生成失败，保留JSON正文", exception);
    message.error(exception instanceof Error ? exception.message : "生成失败");
  } finally {
    generating.value = false;
  }
}
</script>
<style scoped>
.json-mode-toolbar {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  margin: 16px 0;
}
</style>
