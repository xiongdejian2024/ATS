<template>
  <a-form layout="vertical"
    ><a-form-item label="执行结果" required
      ><a-radio-group
        :value="result"
        :disabled="disabled || uploading"
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
        :disabled="disabled || uploading"
        label="执行描述"
        :upload-image="planId ? uploadImage : undefined"
        @uploading="imageUploading"
        @update:model-value="
          (value) => emit('update:description', value)
        " /></a-form-item
    ><slot
  /></a-form>
</template>
<script setup lang="ts">
import CaseRichText from "@/components/TestCase/CaseRichText.vue";
import { functionalResults } from "./functionalExecution";
const props = defineProps<{
  result: string;
  description: string;
  disabled?: boolean;
  planId?: string;
  uploading?: boolean;
}>();
const emit = defineEmits<{
  "update:result": [value: string];
  "update:description": [value: string];
  "update:uploading": [value: boolean];
}>();
import { planCaseMediaApi } from "@/api/planCaseMedia";
async function uploadImage(file: File) {
  return planCaseMediaApi.upload(props.planId!, file);
}
function imageUploading(value: boolean) {
  emit("update:uploading", value);
}
function changeResult(event: { target: { value: string } }) {
  emit("update:result", event.target.value);
}
</script>
