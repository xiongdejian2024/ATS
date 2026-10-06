<template>
  <div class="binary-body">
    <a-form-item label="描述"
      ><a-textarea
        :value="data.description"
        :maxlength="255"
        :disabled="disabled"
        :rows="3"
        aria-label="binary请求体描述"
        @change="describe($event.target.value)"
    /></a-form-item>
    <NativeRequestFilePicker
      :model-value="data.file ? [data.file] : []"
      :project-id="projectId"
      :disabled="disabled"
      @update:model-value="select"
    />
    <a-alert v-if="error" :message="error" type="error" />
  </div>
</template>
<script setup lang="ts">
import { ref, watch } from "vue";
import NativeRequestFilePicker from "./NativeRequestFilePicker.vue";
import type { FileReference } from "@/api/nativeRequestFiles";
const props = defineProps<{
  modelValue: string;
  projectId: string;
  disabled?: boolean;
}>();
const emit = defineEmits<{ "update:modelValue": [value: string] }>();
const data = ref<{ file: FileReference | null; description: string }>({
    file: null,
    description: "",
  }),
  error = ref("");
watch(
  () => props.modelValue,
  (raw) => {
    try {
      const value = JSON.parse(raw);
      if (!value || typeof value !== "object" || Array.isArray(value))
        throw new Error("binary正文须为对象");
      data.value = {
        file: value.file ?? null,
        description: value.description ?? "",
      };
      error.value = "";
    } catch (exception) {
      console.error("加载binary正文失败", exception);
      error.value = "binary正文配置无效";
    }
  },
  { immediate: true },
);
function select(files: FileReference[]) {
  if (!props.disabled)
    emit(
      "update:modelValue",
      JSON.stringify({ ...data.value, file: files[0] ?? null }),
    );
}
function describe(value: string) {
  if (!props.disabled)
    emit(
      "update:modelValue",
      JSON.stringify({ ...data.value, description: value }),
    );
}
</script>
<style scoped>
.binary-body {
  margin-top: 16px;
}
.binary-body :deep(.ant-form-item) {
  margin-bottom: 16px;
}
</style>
