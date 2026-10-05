<template>
  <section class="review-detail-header">
    <div class="header-row">
      <div class="header-title">
        <a-button
          type="text"
          aria-label="返回评审列表"
          :disabled="disabled"
          @click="$emit('back')"
          ><ArrowLeftOutlined
        /></a-button>
        <span class="review-name" :title="review.name">{{ review.name }}</span>
        <span class="mode-badge"
          ><TeamOutlined />
          {{ review.mode === "single" ? "单人" : "多人" }}</span
        >
        <a-tag :color="stateColor">{{
          reviewStateName(review.lifecycle)
        }}</a-tag>
      </div>
      <a-space wrap class="header-actions"><slot name="actions" /></a-space>
    </div>
    <div class="review-progress">
      <div class="progress-labels">
        <span
          >已评审用例
          <b>{{
            prepared ? "-" : `${review.reviewedCount}/${review.caseCount}`
          }}</b></span
        >
        <span
          >通过率 <b>{{ prepared ? "-" : `${review.passRate}%` }}</b></span
        >
      </div>
      <a-popover :trigger="['hover', 'focus', 'click']" placement="bottomLeft">
        <template #content>
          <table class="progress-popover">
            <tr>
              <td>评审进度</td>
              <td>
                {{ progressText }} ({{ review.reviewedCount }}/{{
                  review.caseCount
                }})
              </td>
            </tr>
            <tr v-for="row in counts" :key="row.key">
              <td><i :style="{ background: row.color }" />{{ row.label }}</td>
              <td>{{ row.count }}</td>
            </tr>
          </table>
        </template>
        <div
          class="progress-line"
          tabindex="0"
          role="progressbar"
          aria-label="评审进度"
          :aria-valuenow="review.progress"
          :aria-valuemin="0"
          :aria-valuemax="100"
          :aria-valuetext="`${progressText}，${review.reviewedCount}/${review.caseCount}`"
        >
          <span
            v-for="row in counts"
            :key="row.key"
            :style="{
              width: `${review.caseCount ? (row.count / review.caseCount) * 100 : 0}%`,
              background: row.color,
            }"
          />
        </div>
      </a-popover>
    </div>
  </section>
</template>
<script setup lang="ts">
import { computed } from "vue";
import { ArrowLeftOutlined, TeamOutlined } from "@ant-design/icons-vue";
import type { CaseReview } from "@/api/caseGovernance";
import { reviewStateName } from "@/components/Table/reviewColumns";
const props = defineProps<{ review: CaseReview; disabled?: boolean }>();
defineEmits<{ (e: "back"): void }>();
const prepared = computed(() => props.review.lifecycle === "prepared");
const stateColor = computed(
  () =>
    ({
      prepared: "default",
      underway: "blue",
      completed: "green",
      archived: "default",
      cancelled: "default",
      superseded: "default",
    })[props.review.lifecycle] || "default",
);
const progressText = computed(() =>
  props.review.caseCount ? `${props.review.progress.toFixed(2)}%` : "0%",
);
const counts = computed(() => [
  {
    key: "pass",
    label: "通过",
    count: props.review.passCount,
    color: "#00b42a",
  },
  {
    key: "fail",
    label: "不通过",
    count: props.review.unPassCount,
    color: "#f53f3f",
  },
  {
    key: "rereview",
    label: "重新提审",
    count: props.review.reReviewedCount,
    color: "#ff7d00",
  },
  {
    key: "reviewing",
    label: "评审中",
    count: props.review.underReviewedCount,
    color: "#165dff",
  },
  {
    key: "unreviewed",
    label: "未评审",
    count: props.review.unReviewCount,
    color: "#c9cdd4",
  },
]);
</script>
<style scoped>
.review-detail-header {
  background: white;
  border: 1px solid var(--ms-border, #e5e6eb);
  border-radius: 4px 4px 0 0;
  padding: 16px 24px;
}
.header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}
.header-title {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
}
.review-name {
  max-width: 300px;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  font-weight: 500;
}
.mode-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  white-space: nowrap;
  border: 1px solid var(--primary-color);
  border-radius: 0 999px 999px 0;
  padding: 2px 8px;
  color: var(--primary-color);
  font-size: 12px;
  line-height: 16px;
}
.header-title :deep(.ant-tag) {
  margin: 0 16px;
  white-space: nowrap;
}
.header-actions {
  flex-shrink: 0;
}
.review-progress {
  margin-top: 16px;
  width: min(476px, 100%);
}
.progress-labels {
  display: flex;
  gap: 24px;
  margin-bottom: 4px;
  color: #86909c;
  font-size: 14px;
}
.progress-labels b {
  color: #1d2129;
  font-weight: 400;
  margin-left: 8px;
}
.progress-line {
  height: 8px;
  border-radius: 4px;
  overflow: hidden;
  background: #c9cdd4;
  display: flex;
  cursor: pointer;
}
.progress-line:focus-visible {
  outline: 2px solid var(--primary-color);
  outline-offset: 2px;
}
.progress-popover td {
  padding: 4px 8px 4px 0;
  color: #86909c;
}
.progress-popover td:last-child {
  color: #1d2129;
  font-weight: 500;
}
.progress-popover i {
  display: inline-block;
  width: 6px;
  height: 6px;
  margin-right: 4px;
  border-radius: 50%;
}
@media (max-width: 1100px) {
  .header-row {
    flex-wrap: wrap;
  }
}
@media (max-width: 600px) {
  .review-detail-header {
    padding: 16px;
  }
  .header-title {
    flex-wrap: wrap;
    width: 100%;
  }
  .review-name {
    max-width: calc(100% - 48px);
  }
  .header-title :deep(.ant-tag) {
    margin: 0 8px;
  }
  .header-actions {
    width: 100%;
  }
  .progress-labels {
    flex-wrap: wrap;
    gap: 8px 24px;
  }
}
</style>
