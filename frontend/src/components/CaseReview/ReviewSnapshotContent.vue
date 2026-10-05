<template>
  <section class="snapshot-content">
    <h4>前置条件</h4>
    <CaseRichText
      v-if="snapshot.precondition"
      :model-value="snapshot.precondition"
      readonly
    />
    <p v-else>无</p>
    <template v-if="snapshot.case_edit_type === 'TEXT'">
      <h4>文本描述</h4>
      <CaseRichText :model-value="snapshot.text_description || ''" readonly />
      <h4>预期结果</h4>
      <CaseRichText :model-value="snapshot.expected_result || ''" readonly />
    </template>
    <template v-else>
      <h4>步骤描述</h4>
      <a-table
        :columns="columns"
        :data-source="snapshot.steps || []"
        :pagination="false"
        size="small"
        :scroll="{ x: 480 }"
      >
        <template #bodyCell="{ column, record }"
          ><span class="step-text">{{
            record[column.dataIndex]
          }}</span></template
        >
      </a-table>
    </template>
    <h4>备注</h4>
    <CaseRichText
      v-if="snapshot.description"
      :model-value="snapshot.description"
      readonly
    />
    <p v-else>无</p>
  </section>
</template>
<script setup lang="ts">
import CaseRichText from "@/components/TestCase/CaseRichText.vue";
defineProps<{ snapshot: Record<string, any> }>();
const columns = [
  { title: "序号", dataIndex: "step", width: 65 },
  { title: "用例步骤", dataIndex: "action" },
  { title: "预期结果", dataIndex: "expected" },
];
</script>
<style scoped>
h4 {
  margin: 16px 0 8px;
  font-weight: 500;
}
.step-text {
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}
</style>
