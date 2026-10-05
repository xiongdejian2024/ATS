<template>
  <div class="review-result-form">
    <a-radio-group
      v-model:value="decision"
      :disabled="locked"
      @change="changeDecision"
    >
      <a-radio value="approved">通过</a-radio>
      <a-radio value="rejected">不通过</a-radio>
      <a-radio value="suggestion"
        ><a-tooltip title="建议不改变已有有效通过或不通过结论"
          >建议</a-tooltip
        ></a-radio
      >
    </a-radio-group>
    <template v-if="inlineReason">
      <p class="reason-label">
        评审理由<span v-if="decision !== 'approved'">（必填）</span>
      </p>
      <CaseRichText v-model="reason" :disabled="locked" label="批量评审理由" />
    </template>
    <a-button
      v-else
      class="reason-button"
      size="small"
      :disabled="locked"
      @click="reasonOpen = true"
      >＋ 评审理由</a-button
    >
    <p v-if="reason.length > 10000" class="reason-error">
      评审理由不能超过10000字符
    </p>
    <a-alert v-if="error" :message="error" type="error" show-icon />
    <a-button
      class="submit-button"
      type="primary"
      :loading="saving"
      :disabled="submitDisabled"
      @click="submit"
      >提交评审</a-button
    >
    <a-modal
      v-model:open="reasonOpen"
      title="评审理由"
      :width="680"
      :closable="!saving"
      :mask-closable="!saving"
      :keyboard="!saving"
      :cancel-button-props="{ disabled: saving }"
      :ok-button-props="{ disabled: submitDisabled }"
      :confirm-loading="saving"
      ok-text="提交评审"
      destroy-on-close
      @ok="submit"
    >
      <CaseRichText v-model="reason" :disabled="locked" label="评审理由" />
      <p v-if="decision !== 'approved'" class="reason-label">
        不通过或建议必须填写评审理由
      </p>
      <p v-if="reason.length > 10000" class="reason-error">
        评审理由不能超过10000字符
      </p>
      <a-alert v-if="error" :message="error" type="error" show-icon />
    </a-modal>
  </div>
</template>
<script setup lang="ts">
import { computed, ref } from "vue";
import CaseRichText from "@/components/TestCase/CaseRichText.vue";
export type ReviewDecision = "approved" | "rejected" | "suggestion";
const props = defineProps<{
  disabled?: boolean;
  inlineReason?: boolean;
  submitResult: (decision: ReviewDecision, reason: string) => Promise<void>;
}>();
const decision = ref<ReviewDecision>("approved"),
  reason = ref(""),
  reasonOpen = ref(false),
  saving = ref(false),
  error = ref("");
const locked = computed(() => !!props.disabled || saving.value);
function hasReason(value: string) {
  if (!/<\/?[a-z][\s\S]*>/i.test(value))
    return !!value.replace(/[\u200b\ufeff]/g, "").trim();
  const doc = new DOMParser().parseFromString(value, "text/html");
  doc
    .querySelectorAll("script, style, template")
    .forEach((node) => node.remove());
  return (
    !!doc.body.textContent?.replace(/[\u200b\ufeff]/g, "").trim() ||
    [...doc.querySelectorAll("img")].some(
      (image) => !!image.getAttribute("src")?.trim(),
    )
  );
}
const submitDisabled = computed(
  () =>
    locked.value ||
    reason.value.length > 10000 ||
    (decision.value !== "approved" && !hasReason(reason.value)),
);
function changeDecision() {
  error.value = "";
  if (!props.inlineReason && decision.value !== "approved")
    reasonOpen.value = true;
}
async function submit() {
  if (submitDisabled.value) return;
  saving.value = true;
  error.value = "";
  try {
    await props.submitResult(decision.value, reason.value.trim());
    reasonOpen.value = false;
    reason.value = "";
    decision.value = "approved";
  } catch (failure) {
    console.error("提交评审结论失败，理由草稿保留", failure);
    error.value = "提交评审失败，请保留理由并重试";
  } finally {
    saving.value = false;
  }
}
</script>
<style scoped>
.review-result-form {
  margin-top: 16px;
}
.reason-button {
  display: block;
  margin-top: 8px;
}
.submit-button {
  margin-top: 12px;
}
.reason-label {
  margin: 12px 0 8px;
  color: var(--ms-text-secondary);
}
.reason-error {
  margin: 8px 0;
  color: #f53f3f;
}
.review-result-form :deep(.ant-alert) {
  margin-top: 12px;
}
</style>
