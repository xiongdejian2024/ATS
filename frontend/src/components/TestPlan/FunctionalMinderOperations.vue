<template>
  <a-space
    v-if="showMenu !== false && selection && (canExecute || canModify)"
    class="minder-operations"
    role="toolbar"
  >
    <a-dropdown v-if="canExecute" :trigger="['click']"
      ><a-button size="small" :disabled="busy">缺陷 ▾</a-button
      ><template #overlay
        ><a-menu @click="defectAction"
          ><a-menu-item key="create">新建缺陷</a-menu-item
          ><a-menu-item key="associate">关联缺陷</a-menu-item></a-menu
        ></template
      ></a-dropdown
    >
    <a-dropdown v-if="canModify" :trigger="['click']"
      ><a-button size="small" :disabled="busy">更多 ▾</a-button
      ><template #overlay
        ><a-menu @click="operation"
          ><a-menu-item key="assign">更改执行人</a-menu-item
          ><a-menu-item key="unlink">取消关联</a-menu-item></a-menu
        ></template
      ></a-dropdown
    >
  </a-space>
  <PlanDefectBindingEditor
    v-if="selection"
    ref="editor"
    :plan-id="planId"
    :selection="selection"
    :before-open="beforeAction"
    @changed="emit('changed')"
  />
  <a-modal
    :open="assignOpen"
    title="更改执行人"
    :confirm-loading="busy"
    :mask-closable="false"
    @ok="assign"
    @cancel="assignOpen = false"
    ><a-alert
      :message="`已选择 ${count} 个计划关联实例`"
      type="info" /><a-select
      v-model:value="assignedTo"
      allow-clear
      placeholder="未分配"
      :options="executors.map((item) => ({ value: item.id, label: item.name }))"
      style="width: 100%; margin-top: 16px"
  /></a-modal>
</template>
<script setup lang="ts">
import { ref, computed } from "vue";
import { Modal, message } from "ant-design-vue";
import {
  functionalMinderBatchPreview,
  functionalMinderBatch,
  type FunctionalMinderSelection,
} from "@/api/planCaseWorkspace";
import { planTreeApi } from "@/api/planTree";
import PlanDefectBindingEditor from "./PlanDefectBindingEditor.vue";
const props = defineProps<{
  planId: string;
  selection?: FunctionalMinderSelection;
  canExecute: boolean;
  canModify: boolean;
  showMenu?: boolean;
  beforeAction: () => Promise<boolean>;
}>();
const emit = defineEmits<{ changed: [] }>();
const editor = ref<InstanceType<typeof PlanDefectBindingEditor>>(),
  busy = ref(false),
  assignOpen = ref(false),
  unlinkOpen = ref(false),
  count = ref(0),
  assignedTo = ref<string>(),
  executors = ref<{ id: string; name: string }[]>([]);
const isOpen = computed(
  () =>
    busy.value ||
    assignOpen.value ||
    unlinkOpen.value ||
    !!editor.value?.isOpen,
);
async function beforeClose() {
  if (unlinkOpen.value) {
    message.warning("请先完成或关闭取消关联确认");
    return false;
  }
  if (busy.value) {
    message.warning("请等待批量操作完成");
    return false;
  }
  if (assignOpen.value)
    return new Promise<boolean>((resolve) =>
      Modal.confirm({
        title: "放弃执行人修改？",
        okText: "放弃",
        cancelText: "继续编辑",
        onOk: () => {
          assignOpen.value = false;
          resolve(true);
        },
        onCancel: () => resolve(false),
      }),
    );
  return (await editor.value?.beforeClose()) ?? true;
}
async function defectAction({ key }: { key: string | number }) {
  await editor.value?.open(key === "create" ? "create" : "associate");
}
async function operation({ key }: { key: string | number }) {
  if (!props.selection || !(await props.beforeAction())) return;
  busy.value = true;
  try {
    const result = await functionalMinderBatchPreview(props.planId, {
      ...props.selection,
      action: key === "assign" ? "assign" : "unlink",
    });
    if (!result.canModify) {
      message.warning("当前范围为空、计划已归档或没有修改权限");
      return;
    }
    count.value = result.count;
    if (key === "assign") {
      executors.value = await planTreeApi.executors(props.planId);
      assignedTo.value = undefined;
      assignOpen.value = true;
    } else {
      unlinkOpen.value = true;
      Modal.confirm({
        title: `取消 ${count.value} 个用例关联？`,
        content: "缺陷身份快照与执行历史保留。",
        okText: "取消关联",
        cancelText: "保留",
        onOk: async () => {
          await submit("unlink");
          unlinkOpen.value = false;
        },
        onCancel: () => {
          unlinkOpen.value = false;
        },
      });
    }
  } catch (error) {
    console.error("预览脑图批量管理范围失败", error);
    message.error("操作范围加载失败");
  } finally {
    busy.value = false;
  }
}
async function assign() {
  await submit("assign");
}
async function submit(action: "assign" | "unlink") {
  if (!props.selection || busy.value) return;
  busy.value = true;
  try {
    const result = await functionalMinderBatch(props.planId, {
      ...props.selection,
      action,
      ...(action === "assign" ? { assignedTo: assignedTo.value || null } : {}),
    });
    assignOpen.value = false;
    message.success(`已更新 ${result.updated} 个关联实例`);
    emit("changed");
  } catch (error) {
    console.error("提交脑图批量管理失败", error);
    message.error("操作失败，请刷新核对范围及权限");
  } finally {
    busy.value = false;
  }
}
defineExpose({ beforeClose, isOpen, defectAction, operation });
</script>
