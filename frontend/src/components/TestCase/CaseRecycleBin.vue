<template>
  <component :is="embedded ? 'section' : Drawer" v-if="open" class="case-recycle-bin"
    v-bind="embedded ? {} : { open, title: '用例回收站', width: 'min(1000px, 96vw)' }"
    @close="emit('update:open', false)">
    <header v-if="embedded" class="recycle-header"><h3>回收站（{{ total }}）</h3><a-button @click="emit('close')">返回用例</a-button></header>
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
    <a-space v-if="selectedIds.length" class="recycle-batch" wrap>
      <span>已选择 {{ selectedIds.length }} 条</span>
      <a-button :loading="mutating" @click="batch('restore')">恢复</a-button>
      <a-popconfirm :title="`彻底删除所选 ${selectedIds.length} 条用例？不可撤销。`" @confirm="batch('purge')"><a-button danger :disabled="mutating">彻底删除</a-button></a-popconfirm>
      <a-button type="text" @click="selectedIds=[]">清空</a-button>
    </a-space>
    <a-table
      :columns="columns"
      :data-source="rows"
      :loading="busy"
      row-key="id"
      :scroll="{ x: 650 }"
      :row-selection="{ selectedRowKeys: selectedIds, onChange: (ids: any[]) => selectedIds = ids.map(String) }"
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
            ><a-button :disabled="mutating" @click="restore(record.id)">恢复</a-button
            ><a-popconfirm
              :title="`彻底删除 ${record.name}？不可撤销。`"
              @confirm="purge(record.id)"
              ><a-button danger :disabled="mutating">彻底删除</a-button></a-popconfirm
            ></a-space
          ></template
        ></template
      >
    </a-table>
  </component>
</template>
<script setup lang="ts">
import { ref, watch } from "vue";
import dayjs from "dayjs";
import { Drawer, message } from "ant-design-vue";
import { caseFeaturesApi as api } from "@/api/caseFeatures";
import type { TestCase } from "@/types";
const props = defineProps<{ projectId: string; open: boolean; embedded?: boolean }>(),
  emit = defineEmits<{ "update:open": [value: boolean]; changed: []; total: [value: number]; close: [] }>();
const selectedIds = ref<string[]>([]), mutating = ref(false);
const rows = ref<TestCase[]>([]),
  total = ref(0),
  page = ref(1),
  search = ref(""),
  busy = ref(false);
const columns = [
  { title: "编号", dataIndex: "caseCode" },
  { title: "名称", dataIndex: "name" },
  { title: "删除时间", dataIndex: "deletedAt", customRender: ({ text }: { text?: string }) => text ? dayjs(text).format("YYYY-MM-DD HH:mm:ss") : "-" },
  { title: "操作", key: "actions" },
];
let loadSequence = 0;
async function load() {
  if (!props.open || !props.projectId) return;
  const sequence = ++loadSequence;
  const projectId = props.projectId;
  busy.value = true;
  try {
    const data = await api.recycle(projectId, {
      page: page.value,
      size: 20,
      search: search.value,
    });
    if (sequence !== loadSequence || projectId !== props.projectId) return;
    rows.value = data.items;
    total.value = data.total;
    emit("total", data.total);
  } catch (error) {
    console.error("加载回收站失败", error);
  } finally {
    if (sequence === loadSequence) busy.value = false;
  }
}
async function batch(action: 'restore' | 'purge') {
  if (mutating.value || !selectedIds.value.length) return;
  mutating.value = true;
  const ids = [...selectedIds.value];
  const projectId = props.projectId;
  try {
    const results = await Promise.allSettled(ids.map(id => api[action](projectId, id)));
    const failed = results.filter(result => result.status === 'rejected');
    for (const result of failed) if (result.status === 'rejected') console.error(`批量${action === 'restore' ? '恢复' : '彻底删除'}用例失败`, result.reason);
    const count = results.length - failed.length;
    if (projectId !== props.projectId) return;
    selectedIds.value = ids.filter((_, i) => results[i].status === 'rejected');
    if (failed.length) message.warning(`成功 ${count} 条，失败 ${failed.length} 条${action === 'purge' ? '；有历史引用的用例无法彻底删除' : '，请重试或检查权限'}`);
    else message.success(`已${action === 'restore' ? '恢复' : '彻底删除'} ${count} 条用例`);
    console.info('回收站批量操作已结束', { action, projectId: props.projectId, success: count, failed: failed.length });
    if (count) emit('changed');
    await load();
  } catch (error) {
    console.error('执行回收站批量操作失败', error);
    message.error('批量操作失败，请重试');
  } finally { mutating.value = false; }
}
async function restore(id: string) {
  try {
    await api.restore(props.projectId, id);
    selectedIds.value = selectedIds.value.filter(value => value !== id);
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
    selectedIds.value = selectedIds.value.filter(value => value !== id);
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
    selectedIds.value = [];
    load();
  },
  { immediate: true },
);
</script>

<style scoped>
.case-recycle-bin { background:#fff; }
.recycle-header { display:flex; align-items:center; justify-content:space-between; margin-bottom:16px; }
.recycle-header h3 { font-size:14px; font-weight:500; }
.recycle-batch { margin-bottom:12px; }
</style>
