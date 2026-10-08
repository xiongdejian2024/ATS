<template>
  <a-modal :open="open" title="选择计划关联实例" width="min(900px,100vw)" :ok-button-props="{ disabled: !selected.length || failed || loading }" @ok="confirm" @cancel="emit('cancel')">
    <a-alert type="info" message="重复主用例按计划实例分别选择；只操作本次勾选范围" />
    <a-input-search v-model:value="search" placeholder="搜索编号 / 名称" allow-clear @search="page=1;load()" />
    <a-alert v-if="failed" type="error" message="实例加载失败，请刷新重试" />
    <a-table :data-source="items" row-key="id" :columns="columns" :pagination="false" :loading="loading" :scroll="{ x: 650 }" size="small"
      :row-selection="{ selectedRowKeys: selected, preserveSelectedRowKeys: true, onChange: choose, getCheckboxProps: (row: PlanCaseEntry) => ({ disabled: row.recycled || row.grouped }) }" />
    <a-pagination v-model:current="page" :page-size="20" :total="total" @change="load" />
    <p>已选择 {{ selected.length }} 个实例（每次最多500个）</p>
  </a-modal>
</template>
<script setup lang="ts">
import { ref, watch, onBeforeUnmount } from 'vue'
import { message } from 'ant-design-vue'
import type { Key } from 'ant-design-vue/es/_util/type'
import { planCaseWorkspaceApi, type PlanCaseEntry } from '@/api/planCaseWorkspace'
const props = defineProps<{ planId: string; open: boolean }>()
const emit = defineEmits<{ confirm: [string[]]; cancel: [] }>()
const items = ref<PlanCaseEntry[]>([]), selected = ref<string[]>([]), search = ref(''), page = ref(1), total = ref(0), loading = ref(false), failed = ref(false)
const columns = [{ title: '编号', dataIndex: 'caseCode', width: 140 }, { title: '用例', dataIndex: 'name', width: 220 }, { title: '测试集', dataIndex: 'collectionName', width: 160 }, { title: '实例身份', dataIndex: 'id', width: 320 }]
let generation = 0
function choose(keys: Key[]) {
  if (keys.length > 500) { message.warning('每次最多选择500个实例，请缩小范围'); return }
  selected.value = keys.map(String)
}
async function load() {
  const current = ++generation, target = props.planId
  loading.value = true; failed.value = false
  try {
    const response = await planCaseWorkspaceApi.list(target, { category: 'functional', page: page.value, size: 20, search: search.value })
    if (current !== generation || !props.open) return
    items.value = response.items; total.value = response.total
  } catch (error) { if (current === generation) { failed.value = true; items.value = []; console.error('加载计划实例失败', error) } }
  finally { if (current === generation) loading.value = false }
}
function confirm() { if (selected.value.length && !loading.value && !failed.value) emit('confirm', [...selected.value]) }
watch(() => [props.planId, props.open], () => {
  ++generation; selected.value = []; items.value = []; search.value = ''; page.value = 1; total.value = 0; failed.value = false; loading.value = false
  if (props.open) void load()
}, { immediate: true })
onBeforeUnmount(() => { ++generation })
</script>
