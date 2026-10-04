<template>
  <div class="custom-fields">
    <a-form-item
      v-for="field in fields"
      :key="field.key"
      :label="field.name"
      :required="field.required"
    >
      <template v-if="readonly"
        ><span>{{ display(modelValue[field.key]) }}</span></template
      >
      <a-textarea
        v-else-if="field.type === 'textarea'"
        :value="modelValue[field.key] as string"
        :rows="3"
        @update:value="set(field.key, $event)"
      />
      <a-input-number
        v-else-if="field.type === 'number'"
        :value="modelValue[field.key] as number"
        style="width: 100%"
        @update:value="set(field.key, $event)"
      />
      <a-switch
        v-else-if="field.type === 'boolean'"
        :checked="modelValue[field.key] as boolean"
        @update:checked="set(field.key, $event)"
      />
      <a-date-picker
        v-else-if="field.type === 'date'"
        :value="modelValue[field.key] as string"
        value-format="YYYY-MM-DD"
        style="width: 100%"
        @update:value="set(field.key, $event)"
      />
      <a-select
        v-else-if="field.type === 'select' || field.type === 'multiselect'"
        :mode="field.type === 'multiselect' ? 'multiple' : undefined"
        :value="modelValue[field.key] as any"
        :options="field.options.map((value) => ({ value, label: value }))"
        allow-clear
        @update:value="set(field.key, $event)"
      />
      <a-input
        v-else
        :value="modelValue[field.key] as string"
        :maxlength="10000"
        @update:value="set(field.key, $event)"
      />
    </a-form-item>
  </div>
</template>
<script setup lang="ts">
import type { CaseCustomField } from "@/api/caseFeatures";
const props = defineProps<{
  fields: CaseCustomField[];
  modelValue: Record<string, unknown>;
  readonly?: boolean;
}>();
const emit = defineEmits<{
  "update:modelValue": [value: Record<string, unknown>];
}>();
function set(key: string, value: unknown) {
  emit("update:modelValue", { ...props.modelValue, [key]: value ?? null });
}
function display(value: unknown) {
  return value === null || value === undefined
    ? "未填写"
    : typeof value === "boolean"
      ? value
        ? "是"
        : "否"
      : Array.isArray(value)
        ? value.join("、")
        : String(value);
}
</script>
