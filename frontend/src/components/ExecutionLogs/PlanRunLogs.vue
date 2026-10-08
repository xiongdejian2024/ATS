<template>
  <a-button size="small" :loading="loading" @click="refresh">刷新日志</a-button>
  <RawLogDownload :target="{ endpoint: `${path}/export`, filename: `plan-${planId}-run-${runId}` }" />
  <a-alert v-if="error" :message="error" type="error" show-icon />
  <a-spin :spinning="loading"><BoundedLogViewer :records="records" /></a-spin>
</template>
<script setup lang="ts">
import { computed, onBeforeUnmount, ref, watch } from 'vue'
import { apiClient } from '@/utils/api'
import { normalizeLogs, type LogRecord } from './boundedLogs'
import BoundedLogViewer from './BoundedLogViewer.vue'
import RawLogDownload from './RawLogDownload.vue'
const props = defineProps<{ planId: string; runId: string }>()
const path = computed(() => `/test-plans/${props.planId}/executions/${props.runId}/logs`)
const records = ref<LogRecord[]>([]), loading = ref(false), error = ref('')
let request: AbortController | null = null, generation = 0
function stop() { generation++; request?.abort(); request = null }
async function refresh() {
  stop(); const current = generation
  request = new AbortController(); loading.value = true; error.value = ''
  try {
    const data = await apiClient.get(path.value, { params: { tailChars: 32768 }, signal: request.signal })
    if (current === generation) {
      records.value = normalizeLogs(data.items)
      if (data.total > data.items.length && records.value.length) records.value[0].truncated = true
    }
  } catch (reason) {
    if (current === generation) error.value = '加载日志失败，请重试。'
  } finally { if (current === generation) loading.value = false }
}
watch(path, () => { records.value = []; void refresh() }, { immediate: true })
onBeforeUnmount(stop)
</script>
