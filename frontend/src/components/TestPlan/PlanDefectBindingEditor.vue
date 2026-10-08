<template>
  <a-drawer
    :open="visible"
    :title="mode === 'create' ? '新建缺陷' : '关联缺陷'"
    width="min(800px,100vw)"
    destroy-on-close
    :mask-closable="false"
    @close="close"
  >
    <a-spin :spinning="loading">
      <a-alert
        :message="`已选择 ${count} 个计划关联实例`"
        type="info"
        class="scope-hint"
      />
      <a-form v-if="mode === 'create'" layout="vertical">
        <a-form-item label="缺陷标题" required
          ><a-input v-model:value="title" :maxlength="300" :disabled="saving"
        /></a-form-item>
        <a-form-item label="描述"
          ><a-textarea
            v-model:value="description"
            :maxlength="20000"
            :rows="8"
            :disabled="saving"
        /></a-form-item>
      </a-form>
      <template v-else>
        <a-input-search
          v-model:value="search"
          placeholder="搜索缺陷标题"
          allow-clear
          :disabled="saving"
          @search="searchCandidates"
        />
        <a-alert v-if="failed" message="缺陷加载失败，请重试" type="error" />
        <a-table
          :data-source="items"
          row-key="id"
          :columns="columns"
          :pagination="false"
          :loading="candidateLoading"
          :row-selection="{
            selectedRowKeys: selected,
            preserveSelectedRowKeys: true,
            onChange: choose,
            getCheckboxProps: () => ({ disabled: saving }),
          }"
          size="small"
        >
          <template #bodyCell="{ column, record }"
            ><a-tag v-if="column.key === 'status'">{{
              defectStatusLabels[record.status] || record.status
            }}</a-tag></template
          >
        </a-table>
        <a-pagination
          v-model:current="page"
          :total="total"
          :page-size="10"
          :disabled="saving"
          @change="loadCandidates"
        />
        <p>已选择 {{ selected.length }} 个缺陷（每批最多100个）</p>
      </template>
    </a-spin>
    <template #footer
      ><a-space
        ><a-button :disabled="saving" @click="close">取消</a-button
        ><a-button
          type="primary"
          :loading="saving"
          :disabled="
            loading ||
            !allowed ||
            (mode === 'associate' && (!selected.length || failed))
          "
          @click="save"
          >{{ mode === "create" ? "创建并关联" : "关联" }}</a-button
        ></a-space
      ></template
    >
  </a-drawer>
</template>
<script setup lang="ts">
import {onMounted as mountUnload, onBeforeUnmount as unmountUnload} from "vue";
import { computed, ref, watch, onBeforeUnmount } from "vue";
import { Modal, message } from "ant-design-vue";
import type { Key } from "ant-design-vue/es/_util/type";
import { planCaseDefectsApi, defectStatusLabels } from "@/api/planCaseDefects";
import type { CaseIssue } from "@/api/caseFeatures";
import type { FunctionalMinderSelection } from "@/api/planCaseWorkspace";
const props = defineProps<{
  planId: string;
  selection: FunctionalMinderSelection;
  beforeOpen?: () => Promise<boolean>;
}>();
const emit = defineEmits<{ changed: [] }>();
const visible = ref(false),
  mode = ref<"create" | "associate">("associate"),
  loading = ref(false),
  saving = ref(false),
  allowed = ref(false),
  count = ref(0);
const title = ref(""),
  description = ref(""),
  search = ref(""),
  page = ref(1),
  total = ref(0),
  items = ref<CaseIssue[]>([]),
  selected = ref<string[]>([]),
  candidateLoading = ref(false),
  failed = ref(false);
const columns = [
  { title: "缺陷标题", dataIndex: "title" },
  { title: "状态", key: "status", width: 100 },
];
const dirty = computed(
  () => !!(title.value || description.value || selected.value.length),
);
let sequence = 0,
  candidatesSequence = 0,
  pending: { body: string; id: string } | undefined;
function beforeUnload(event: BeforeUnloadEvent) { if (visible.value && (dirty.value || saving.value)) { event.preventDefault(); event.returnValue = ""; } }
mountUnload(() => window.addEventListener("beforeunload", beforeUnload));
unmountUnload(() => window.removeEventListener("beforeunload", beforeUnload));
async function beforeClose() {
  if (saving.value || loading.value) {
    message.warning("请等待缺陷操作完成");
    return false;
  }
  if (!visible.value || !dirty.value) return true;
  return new Promise<boolean>((resolve) =>
    Modal.confirm({
      title: "放弃未提交的缺陷操作？",
      okText: "放弃",
      cancelText: "继续编辑",
      onOk: () => {
        visible.value = false;
        title.value = description.value = "";
        selected.value = [];
        resolve(true);
      },
      onCancel: () => resolve(false),
    }),
  );
}
async function close() {
  if (await beforeClose()) {
    visible.value = false;
    sequence++;
    candidatesSequence++;
  }
}
async function open(next: "create" | "associate") {
  if (
    !(await beforeClose()) ||
    (props.beforeOpen && !(await props.beforeOpen()))
  )
    return;
  title.value = description.value = search.value = "";
  selected.value = [];
  page.value = 1;
  pending = undefined;
  mode.value = next;
  allowed.value = false;
  loading.value = true;
  const current = ++sequence;
  try {
    const result = await planCaseDefectsApi.preview(
      props.planId,
      props.selection,
    );
    if (current !== sequence) return;
    count.value = result.count;
    allowed.value = next === "create" ? result.canCreate : result.canAssociate;
    if (!allowed.value) {
      message.warning("当前范围为空、计划已归档或没有相应权限");
      return;
    }
    visible.value = true;
    if (next === "associate") await loadCandidates();
  } catch (error) {
    console.error("预览计划缺陷范围失败", error);
    message.error("缺陷范围加载失败");
  } finally {
    if (current === sequence) loading.value = false;
  }
}
function choose(keys: Key[]) {
  if (keys.length > 100) {
    message.warning("每批最多选择100个缺陷");
    return;
  }
  selected.value = keys.map(String);
}
async function searchCandidates() {
  page.value = 1;
  await loadCandidates();
}
async function loadCandidates() {
  const current = ++candidatesSequence;
  candidateLoading.value = true;
  failed.value = false;
  try {
    const result = await planCaseDefectsApi.candidates(props.planId, {
      page: page.value,
      size: 10,
      search: search.value,
    });
    if (current === candidatesSequence) {
      items.value = result.items;
      total.value = result.total;
    }
  } catch (error) {
    console.error("加载待关联缺陷失败", error);
    if (current === candidatesSequence) {
      failed.value = true;
      items.value = [];
    }
  } finally {
    if (current === candidatesSequence) candidateLoading.value = false;
  }
}
async function save() {
  if (saving.value) return;
  if (mode.value === "create" && !title.value.trim()) {
    message.warning("请填写缺陷标题");
    return;
  }
  const current = sequence;
  saving.value = true;
  try {
    const body = {
      ...props.selection,
      title: title.value.trim(),
      description: description.value,
    };
    if (!pending || pending.body !== JSON.stringify(body))
      pending = { body: JSON.stringify(body), id: crypto.randomUUID() };
    const result =
      mode.value === "create"
        ? await planCaseDefectsApi.create(props.planId, {
            ...body,
            requestId: pending.id,
          })
        : await planCaseDefectsApi.associate(props.planId, {
            ...props.selection,
            issueIds: selected.value,
          });
    if (current !== sequence) return;
    visible.value = false;
    title.value = description.value = "";
    selected.value = [];
    pending = undefined;
    console.info("计划实例缺陷操作完成", {
      mode: mode.value,
      updated: result.updated,
    });
    message.success(
      `已${mode.value === "create" ? "创建并关联" : "关联"}缺陷，更新 ${result.updated} 条关系`,
    );
    emit("changed");
  } catch (error) {
    console.error("提交计划实例缺陷失败", error);
    message.error("提交失败，保留内容可重试；请核对范围及权限");
  } finally {
    if (current === sequence) saving.value = false;
  }
}
watch(
  () => props.planId,
  () => {
    sequence++;
    candidatesSequence++;
    visible.value = false;
    allowed.value = false;
  },
);
onBeforeUnmount(() => {
  sequence++;
  candidatesSequence++;
});
defineExpose({
  open,
  beforeClose,
  isOpen: computed(() => visible.value || loading.value),
});
</script>
<style scoped>
.scope-hint {
  margin-bottom: 16px;
}
.ant-table-wrapper,
.ant-pagination {
  margin-top: 16px;
}
</style>
