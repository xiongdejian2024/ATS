<template>
  <PlanCaseExecuteForm
    ref="inlineForm"
    :result="result"
    :description="description"
    :plan-id="planId"
    :disabled="disabled || expanded"
    :uploading="uploading"
    compact
    :active="active"
    @update:result="(value) => emit('update:result', value)"
    @update:description="(value) => emit('update:description', value)"
    @update:uploading="(value) => emit('update:uploading', value)"
    @activate="activate"
    @expand="expand"
  />
  <a-space wrap
    ><a-button
      type="primary"
      :loading="disabled"
      :disabled="uploading || expanded"
      @click="submit"
      >提交结果</a-button
    ><slot
  /></a-space>
  <a-modal
    v-model:open="expanded"
    title="开始执行"
    width="min(800px,100vw)"
    destroy-on-close
    :confirm-loading="disabled"
    :closable="!disabled && !uploading"
    :mask-closable="!disabled && !uploading"
    :ok-button-props="{ disabled: uploading }"
    :cancel-button-props="{ disabled: disabled || uploading }"
    ok-text="提交结果"
    @ok="submit"
    @cancel="cancel"
  >
    <PlanCaseExecuteForm
      ref="dialogForm"
      v-model:result="dialogResult"
      v-model:description="dialogDescription"
      :plan-id="planId"
      :disabled="disabled"
      :uploading="uploading"
      @update:uploading="(value) => emit('update:uploading', value)"
    />
  </a-modal>
</template>
<script setup lang="ts">
import { ref, nextTick, onBeforeUnmount, watch } from "vue";
import PlanCaseExecuteForm from "./PlanCaseExecuteForm.vue";
const props = defineProps<{
  result: string;
  description: string;
  planId: string;
  disabled: boolean;
  uploading: boolean;
  onSubmit: () => Promise<boolean>;
  dialogDirty?: boolean;
}>();
const emit = defineEmits<{
  "update:result": [value: string];
  "update:description": [value: string];
  "update:uploading": [value: boolean];
  "update:dialogDirty": [value: boolean];
}>();
const active = ref(!!props.description),
  expanded = ref(false),
  dialogResult = ref("passed"),
  dialogDescription = ref(""),
  inlineForm = ref<InstanceType<typeof PlanCaseExecuteForm>>(),
  dialogForm = ref<InstanceType<typeof PlanCaseExecuteForm>>();
let clickTimer: ReturnType<typeof setTimeout> | undefined;
function clearClick() {
  if (clickTimer) clearTimeout(clickTimer);
  clickTimer = undefined;
}
function activate() {
  if (active.value || props.disabled || props.uploading) return;
  clearClick();
  clickTimer = setTimeout(async () => {
    active.value = true;
    clickTimer = undefined;
    await nextTick();
    inlineForm.value?.focus();
  }, 200);
}
async function expand() {
  if (props.disabled || props.uploading) return;
  clearClick();
  dialogResult.value = props.result;
  dialogDescription.value = props.description;
  expanded.value = true;
  await nextTick();
  dialogForm.value?.focus();
}
function cancel(event: MouseEvent | KeyboardEvent) {
  if (props.disabled || props.uploading) return;
  const maskClose = Boolean(
    (event.target as Element | undefined)?.classList?.contains(
      "ant-modal-wrap",
    ),
  );
  // 官方遮罩关闭保留弹窗内容；取消、关闭与 Escape 重置执行表单，步骤保持原样。
  emit("update:result", maskClose ? dialogResult.value : "passed");
  emit("update:description", maskClose ? dialogDescription.value : "");
  expanded.value = false;
  active.value = maskClose && !!dialogDescription.value;
}
async function submit() {
  if (props.disabled || props.uploading) return;
  clearClick();
  const wasExpanded = expanded.value,
    previous = { result: props.result, description: props.description };
  if (wasExpanded) {
    emit("update:result", dialogResult.value);
    emit("update:description", dialogDescription.value);
    await nextTick();
  }
  if (await props.onSubmit()) {
    expanded.value = false;
    active.value = false;
  } else if (wasExpanded) {
    emit("update:result", previous.result);
    emit("update:description", previous.description);
  }
}
watch(
  [
    expanded,
    dialogResult,
    dialogDescription,
    () => props.result,
    () => props.description,
  ],
  () =>
    emit(
      "update:dialogDirty",
      expanded.value &&
        (dialogResult.value !== props.result ||
          dialogDescription.value !== props.description),
    ),
);
onBeforeUnmount(() => {
  clearClick();
  emit("update:dialogDirty", false);
});
</script>
