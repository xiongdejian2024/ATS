<template>
  <a-drawer
    :open="open"
    title="用例回收站"
    width="min(1000px, 96vw)"
    @close="emit('update:open', false)"
  >
    <a-alert
      message="恢复后重新进入用例库。彻底删除无法撤销；有执行历史的用例会被系统阻止删除。"
      type="info"
      show-icon
    />
    <a-input-search
      v-model:value="search"
      placeholder="搜索编号或名称"
      style="margin: 16px 0"
      @search="
        page = 1;
        load();
      "
    />
    <a-table
      :columns="columns"
      :data-source="rows"
      :loading="busy"
      row-key="id"
      :pagination="{ current: page, pageSize: 20, total }"
      @change="
        (p: any) => {
          page = p.current;
          load();
        }
      "
    >
      <template #bodyCell="{ column, record }"
        ><template v-if="column.key === 'actions'"
          ><a-space
            ><a-button @click="restore(record.id)">恢复</a-button
            ><a-popconfirm
              :title="`彻底删除 ${record.name}？不可撤销。`"
              @confirm="purge(record.id)"
              ><a-button danger>彻底删除</a-button></a-popconfirm
            ></a-space
          ></template
        ></template
      >
    </a-table>
  </a-drawer>
</template>
<script setup lang="ts">
import { ref, watch } from "vue";
import { message } from "ant-design-vue";
import { caseFeaturesApi as api } from "@/api/caseFeatures";
import type { TestCase } from "@/types";
const props = defineProps<{ projectId: string; open: boolean }>(),
  emit = defineEmits<{ "update:open": [value: boolean]; changed: [] }>();
const rows = ref<TestCase[]>([]),
  total = ref(0),
  page = ref(1),
  search = ref(""),
  busy = ref(false);
const columns = [
  { title: "编号", dataIndex: "caseCode" },
  { title: "名称", dataIndex: "name" },
  { title: "删除时间", dataIndex: "deletedAt" },
  { title: "操作", key: "actions" },
];
async function load() {
  if (!props.open || !props.projectId) return;
  busy.value = true;
  try {
    const data = await api.recycle(props.projectId, {
      page: page.value,
      size: 20,
      search: search.value,
    });
    rows.value = data.items;
    total.value = data.total;
  } catch (error) {
    console.error("加载回收站失败", error);
  } finally {
    busy.value = false;
  }
}
async function restore(id: string) {
  try {
    await api.restore(props.projectId, id);
    message.success("用例已恢复");
    emit("changed");
    await load();
  } catch (error) {
    console.error("恢复用例失败", error);
  }
}
async function purge(id: string) {
  try {
    await api.purge(props.projectId, id);
    message.success("用例已彻底删除");
    emit("changed");
    await load();
  } catch (error) {
    console.error("彻底删除用例失败", error);
  }
}
watch(
  () => [props.projectId, props.open],
  () => {
    page.value = 1;
    load();
  },
  { immediate: true },
);
</script>
