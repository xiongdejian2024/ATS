<template>
  <a-form layout="vertical" :class="{ 'compact-execute-form': compact }"
    ><a-form-item :label="compact ? undefined : '执行结果'" :required="!compact"
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
    <a-form-item :label="compact ? undefined : '执行描述'">
      <div
        class="execution-description"
        @click="descriptionClick"
        @dblclick="descriptionDoubleClick"
      >
        <a-textarea
          v-if="compact && !active"
          :value="description"
          :disabled="disabled || uploading"
          placeholder="双击可全屏输入"
          aria-label="执行描述"
          :maxlength="1000"
          :auto-size="{ minRows: 1 }"
          @update:value="(value: string) => emit('update:description', value)"
        />
        <CaseRichText
          v-else
          ref="richText"
          :model-value="description"
          :disabled="disabled || uploading"
          label="执行描述"
          :upload-image="planId ? uploadImage : undefined"
          @uploading="imageUploading"
          @update:model-value="
            (value: string) => emit('update:description', value)
          "
        /></div></a-form-item
    ><slot
  /></a-form>
</template>
<script setup lang="ts">
import CaseRichText from "@/components/TestCase/CaseRichText.vue";
import { functionalResults } from "./functionalExecution";
import { ref } from "vue";
const props = defineProps<{
  result: string;
  description: string;
  disabled?: boolean;
  planId?: string;
  uploading?: boolean;
  compact?: boolean;
  active?: boolean;
}>();
const emit = defineEmits<{
  "update:result": [value: string];
  "update:description": [value: string];
  "update:uploading": [value: boolean];
  activate: [];
  expand: [];
  imageUploaded: [
    planId: string,
    media: import("@/api/planCaseMedia").PlanCaseMedia,
  ];
}>();
const richText = ref<InstanceType<typeof CaseRichText>>();
function isDescription(event: MouseEvent) {
  const target = event.target as Element;
  return (
    !props.disabled &&
    !props.uploading &&
    !!target.closest('textarea, [role="textbox"]') &&
    !target.closest("button, .rich-text-image")
  );
}
function descriptionClick(event: MouseEvent) {
  if (props.compact && isDescription(event)) emit("activate");
}
function descriptionDoubleClick(event: MouseEvent) {
  if (props.compact && isDescription(event)) emit("expand");
}
defineExpose({ focus: () => richText.value?.focus() });
import { planCaseMediaApi } from "@/api/planCaseMedia";
async function uploadImage(file: File) {
  const planId = props.planId!;
  const image = await planCaseMediaApi.upload(planId, file);
  emit("imageUploaded", planId, image);
  return image;
}
function imageUploading(value: boolean) {
  emit("update:uploading", value);
}
function changeResult(event: { target: { value: string } }) {
  emit("update:result", event.target.value);
}
</script>
<style scoped>
.compact-execute-form :deep(.ant-form-item) {
  margin-bottom: 8px;
}
.compact-execute-form :deep(.tiptap) {
  min-height: 58px;
  height: 58px;
  overflow-y: auto;
}
</style>
