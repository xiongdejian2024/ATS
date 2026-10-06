<template>
  <span v-if="!supported">-</span>
  <a-input-number
    v-else-if="numeric"
    :value="numericValue"
    :disabled="disabled"
    :min="unsigned ? 0 : undefined"
    :max="field.endsWith('Items') ? 200 : unsigned ? 20000 : undefined"
    :precision="record.type === 'integer' || unsigned ? 0 : undefined"
    :aria-label="label"
    @change="set($event ?? undefined)"
  />
  <a-select
    v-else-if="field === 'defaultValue' && record.type === 'boolean'"
    :value="record.defaultValue === '' ? undefined : record.defaultValue"
    :options="[
      { value: true, label: 'true' },
      { value: false, label: 'false' },
    ]"
    allow-clear
    :disabled="disabled"
    :aria-label="label"
    @change="set($event ?? '')"
  />
  <a-select
    v-else-if="field === 'format'"
    :value="record.format"
    :options="formats.map((value) => ({ value, label: value }))"
    allow-clear
    :disabled="disabled"
    :aria-label="label"
    @change="set($event)"
  />
  <a-textarea
    v-else-if="field === 'enumValues'"
    :value="record.enumValues"
    :rows="compact ? 1 : 4"
    placeholder="每行一个枚举值"
    :disabled="disabled"
    :aria-label="label"
    @change="set($event.target.value)"
  />
  <a-input
    v-else
    :value="textValue"
    :maxlength="field === 'pattern' ? 512 : 20000"
    :disabled="disabled"
    :aria-label="label"
    @change="set($event.target.value)"
  />
</template>
<script setup lang="ts">
import { computed } from "vue";
import type { SchemaRow } from "./nativeJsonSchema";
const props = defineProps<{
  record: SchemaRow;
  field: string;
  label: string;
  disabled?: boolean;
  compact?: boolean;
}>();
const emit = defineEmits<{ change: [] }>();
const textValue = computed(() => (props.record as any)[props.field]);
const formats = [
  "date",
  "date-time",
  "email",
  "hostname",
  "ipv4",
  "ipv6",
  "url",
];
const supported = computed(() => {
  if (props.field === "description") return true;
  if (["minLength", "maxLength", "pattern", "format"].includes(props.field))
    return props.record.type === "string";
  if (["minimum", "maximum"].includes(props.field))
    return ["number", "integer"].includes(props.record.type);
  if (["minItems", "maxItems"].includes(props.field))
    return props.record.type === "array";
  if (props.field === "enumValues")
    return ["string", "number", "integer"].includes(props.record.type);
  return !["object", "array", "null"].includes(props.record.type);
});
const unsigned = computed(() =>
  ["minLength", "maxLength", "minItems", "maxItems"].includes(props.field),
);
const numeric = computed(
  () =>
    unsigned.value ||
    ["minimum", "maximum"].includes(props.field) ||
    (props.field === "defaultValue" &&
      ["number", "integer"].includes(props.record.type)),
);
const numericValue = computed(() => {
  const value = (props.record as any)[props.field];
  return value === "" ? undefined : value;
});
function set(value: unknown) {
  (props.record as any)[props.field] = value;
  emit("change");
}
</script>
<style scoped>
.ant-select,
.ant-input-number {
  width: 100%;
  min-width: 90px;
}
</style>
