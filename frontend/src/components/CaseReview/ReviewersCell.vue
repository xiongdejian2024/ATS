<template>
  <div class="reviewers-cell">
    <template v-if="editing">
      <a-select
        v-model:value="draft"
        mode="multiple"
        :options="options"
        :max-tag-count="1"
        :disabled="saving || disabled"
        show-search
        option-filter-prop="label"
        placeholder="选择评审人"
        :aria-label="`选择${name}评审人`"
        @dropdown-visible-change="(visible: boolean) => !visible && save()"
        @blur="save"
        @keydown.esc="cancel"
      />
      <a-alert v-if="error" :message="error" type="error" :show-icon="false" />
    </template>
    <a-tooltip v-else :title="names.join('、')">
      <a-button
        v-if="editable"
        class="reviewer-tags"
        type="text"
        :disabled="disabled"
        :aria-label="`修改${name}评审人`"
        @click="start"
      >
        <span>{{ names[0] || "-" }}</span
        ><a-tag v-if="names.length > 1">+{{ names.length - 1 }}</a-tag
        ><EditOutlined />
      </a-button>
      <span v-else
        >{{ names[0] || "-"
        }}<a-tag v-if="names.length > 1" class="extra-people"
          >+{{ names.length - 1 }}</a-tag
        ></span
      >
    </a-tooltip>
  </div>
</template>
<script setup lang="ts">
import { computed, ref } from "vue";
import { EditOutlined } from "@ant-design/icons-vue";
const props = defineProps<{
  reviewerIds: string[];
  members: { id: string; name: string }[];
  name: string;
  editable: boolean;
  disabled: boolean;
  saveReviewers: (identifiers: string[]) => Promise<void>;
}>();
const editing = ref(false),
  saving = ref(false),
  draft = ref<string[]>([]),
  error = ref("");
const names = computed(() =>
  props.reviewerIds.map(
    (id) => props.members.find((m) => m.id === id)?.name || id,
  ),
);
const options = computed(() =>
  props.members.map((m) => ({ value: m.id, label: m.name })),
);
function start() {
  draft.value = [...props.reviewerIds];
  error.value = "";
  editing.value = true;
}
function cancel() {
  if (!saving.value) editing.value = false;
}
async function save() {
  if (!editing.value || saving.value || props.disabled) return;
  if (!draft.value.length) {
    error.value = "至少选择一位评审人";
    return;
  }
  if (
    JSON.stringify([...draft.value].sort()) ===
    JSON.stringify([...props.reviewerIds].sort())
  ) {
    editing.value = false;
    return;
  }
  saving.value = true;
  error.value = "";
  try {
    await props.saveReviewers([...draft.value]);
    editing.value = false;
  } catch (err) {
    console.error("保存行内评审人失败", err);
    error.value = "保存失败，请重新选择或收起后重试";
  } finally {
    saving.value = false;
  }
}
</script>
<style scoped>
.reviewers-cell {
  min-width: 0;
}
.reviewers-cell :deep(.ant-select) {
  width: 100%;
}
.reviewer-tags {
  display: flex;
  align-items: center;
  gap: 4px;
  width: 100%;
  padding: 0;
}
.reviewer-tags > span:first-child {
  overflow: hidden;
  text-overflow: ellipsis;
}
.reviewer-tags :deep(.ant-tag) {
  margin: 0;
  flex-shrink: 0;
}
.extra-people {
  margin-left: 4px;
}
.reviewers-cell :deep(.ant-alert) {
  padding: 4px;
  font-size: 12px;
  white-space: normal;
}
</style>
