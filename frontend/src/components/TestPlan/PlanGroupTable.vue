<template>
  <a-card
    v-if="groups.length"
    size="small"
    class="group-table"
    title="计划组（展开查看符合当前筛选的成员）"
  >
    <a-table
      :data-source="groups"
      :columns="groupColumns"
      row-key="id"
      size="small"
      :pagination="{ pageSize: 20, showSizeChanger: false }"
      :expanded-row-keys="expanded"
      @expand="expand"
    >
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'name'"
          ><a-button
            type="link"
            :disabled="busy"
            @click="emit('select', record.id)"
            >{{ record.name }}</a-button
          ><a-tag v-if="record.archived">已归档</a-tag></template
        >
        <template v-else-if="column.key === 'planCount'"
          >{{ record.planCount || 0 }} 个成员</template
        >
      </template>
      <template #expandedRowRender="{ record }">
        <a-alert
          v-if="state[record.id]?.error"
          type="error"
          message="成员加载失败，请重试"
          ><template #action
            ><a-button
              :disabled="busy"
              @click="load(record.id, state[record.id]?.page || 1)"
              >重试</a-button
            ></template
          ></a-alert
        >
        <a-table
          :data-source="state[record.id]?.items || []"
          :columns="memberColumns"
          row-key="id"
          size="small"
          :loading="state[record.id]?.loading"
          :pagination="false"
        >
          <template #bodyCell="{ column, record: plan }">
            <template v-if="column.key === 'name'"
              ><a-button
                type="link"
                :disabled="busy"
                @click="emit('open', plan.id)"
                >{{ plan.name }}</a-button
              ></template
            >
            <template v-else-if="column.key === 'progress'"
              >{{ plan.executedCases || 0 }}/{{
                plan.totalCases || 0
              }}</template
            >
          </template>
        </a-table>
        <a-pagination
          :current="state[record.id]?.page || 1"
          :page-size="20"
          :total="state[record.id]?.total || 0"
          :disabled="busy || state[record.id]?.loading"
          :show-total="(total: number) => `符合筛选的成员 ${total} 个`"
          @change="(page: number) => load(record.id, page)"
        />
      </template>
    </a-table>
  </a-card>
</template>
<script setup lang="ts">
import { ref, watch, onBeforeUnmount } from "vue";
import type { TestPlan } from "@/types";
import type { PlanGroup } from "@/api/planOrchestration";
import { testPlanApi } from "@/api/testPlan";
const props = defineProps<{
  projectId: string;
  scopeKey: string;
  revision: number;
  groups: PlanGroup[];
  query: NonNullable<Parameters<typeof testPlanApi.getTestPlans>[1]>;
  busy: boolean;
}>();
const emit = defineEmits<{ open: [id: string]; select: [id: string] }>();
const groupColumns = [
  { key: "name", title: "计划组", dataIndex: "name" },
  { key: "planCount", title: "全部成员", dataIndex: "planCount", width: 140 },
];
const memberColumns = [
  { key: "planNumber", title: "编号", dataIndex: "planNumber", width: 140 },
  { key: "name", title: "计划", dataIndex: "name" },
  { key: "progress", title: "已执行/全部用例", width: 170 },
];
const expanded = ref<string[]>([]);
const state = ref<
  Record<
    string,
    {
      items: TestPlan[];
      total: number;
      page: number;
      loading: boolean;
      error: boolean;
      sequence: number;
    }
  >
>({});
let epoch = 0,
  live = true,
  sequence = 0;
watch(
  () => [
    JSON.stringify([
      props.projectId,
      props.scopeKey,
      props.query,
      props.revision,
    ]),
    props.groups,
  ],
  () => {
    ++epoch;
    expanded.value = [];
    state.value = {};
  },
  { immediate: true, flush: "sync" },
);
onBeforeUnmount(() => {
  live = false;
  ++epoch;
});
async function load(id: string, page: number) {
  if (
    !live ||
    props.busy ||
    !props.projectId ||
    !props.groups.some((group) => group.id === id)
  )
    return;
  const scope = epoch,
    request = ++sequence;
  const previous = state.value[id];
  state.value[id] = {
    items: previous?.items || [],
    total: previous?.total || 0,
    page: previous?.page || 1,
    loading: true,
    error: false,
    sequence: request,
  };
  const current = () =>
    live && epoch === scope && state.value[id]?.sequence === request;
  try {
    const result = await testPlanApi.getTestPlans(props.projectId, {
      ...props.query,
      group_id: id,
      page,
      size: 20,
    });
    if (!current()) return;
    state.value[id] = {
      items: result.items || [],
      total: result.total || 0,
      page,
      loading: false,
      error: false,
      sequence: request,
    };
  } catch (error) {
    console.error("加载计划组成员失败", error);
    if (current()) state.value[id].error = true;
  } finally {
    if (current()) state.value[id].loading = false;
  }
}
function expand(open: boolean, group: PlanGroup) {
  if (props.busy) return;
  expanded.value = open
    ? [...new Set([...expanded.value, group.id])].slice(-10)
    : expanded.value.filter((id) => id !== group.id);
  const keep = new Set(expanded.value);
  state.value = Object.fromEntries(
    Object.entries(state.value).filter(([id]) => keep.has(id)),
  );
  if (open && !state.value[group.id]) void load(group.id, 1);
}
</script>
<style scoped>
.group-table {
  margin-bottom: 12px;
}
</style>
