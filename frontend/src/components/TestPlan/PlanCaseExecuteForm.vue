<template>
  <a-form layout="vertical"
    ><a-form-item label="执行结果" required
      ><a-radio-group
        :value="result"
        :disabled="disabled"
        @change="changeResult"
        ><a-radio
          v-for="option in functionalResults"
          :key="option.value"
          :value="option.value"
          >{{ option.label }}</a-radio
        ></a-radio-group
      ></a-form-item
    >
    <a-form-item label="执行描述"
      ><CaseRichText
        :model-value="description"
        :disabled="disabled"
        label="执行描述"
        @update:model-value="
          (value) => emit('update:description', value)
        " /></a-form-item
    ><slot
  /></a-form>
</template>
<script setup lang="ts">
import CaseRichText from "@/components/TestCase/CaseRichText.vue";
import { functionalResults } from "./functionalExecution";
defineProps<{ result: string; description: string; disabled?: boolean }>();
const emit = defineEmits<{
  "update:result": [value: string];
  "update:description": [value: string];
}>();
function changeResult(event: { target: { value: string } }) {
  emit("update:result", event.target.value);
}
</script>
