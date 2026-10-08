<template>
  <div class="execution-log-page">
    <a-page-header
      :title="`执行日志 - ${suiteName || '未知测试套'}`"
      @back="handleBack"
    >
      <template #extra>
        <a-space>
          <a-button @click="clearLogs" size="small">清空</a-button>
          <a-button @click="refreshLogs" size="small">
            <template #icon><ReloadOutlined /></template>
            刷新
          </a-button>
        </a-space>
      </template>
    </a-page-header>

    <div class="log-container">
      <a-alert v-if="logStatus" :type="logStatus.type" :message="logStatus.message" show-icon class="log-status" />
      <a-spin :spinning="loading" class="log-spin">
        <BoundedLogViewer :records="suiteLogs" height="100%" />
      </a-spin>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onUnmounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { message } from 'ant-design-vue';
import { ReloadOutlined } from '@ant-design/icons-vue';
import { testSuiteApi } from '@/api/testSuite';
import BoundedLogViewer from '@/components/ExecutionLogs/BoundedLogViewer.vue'
import { useSuiteLogStream } from '@/components/ExecutionLogs/useSuiteLogStream'

const route = useRoute()
const router = useRouter()
const suiteName = ref('')
const logStream = useSuiteLogStream()
const { records: suiteLogs, loading, status: logStatus, clear: clearLogs, refresh: refreshLogs } = logStream
let suiteRequest = 0
const handleBack = () => router.back()
const queryString = (value: unknown) => typeof value === 'string' ? value : undefined

// Query-only navigation can reuse this component; isolate every selection and request.
watch(() => [route.query.suiteId, route.query.logId, route.query.executionId, route.query.isRunning], () => {
  const request = ++suiteRequest
  const suiteId = queryString(route.query.suiteId)
  suiteName.value = ''
  if (!suiteId) {
    logStream.close()
    message.error('缺少测试套ID')
    router.back()
    return
  }
  logStream.open({ suiteId, logId: queryString(route.query.logId),
    executionId: queryString(route.query.executionId), live: route.query.isRunning === 'true' })
  void testSuiteApi.getTestSuite(suiteId).then(suite => {
    if (request === suiteRequest) suiteName.value = suite.name
  }).catch(error => {
    if (request === suiteRequest) console.error('加载测试套失败:', error)
  })
}, { immediate: true })

onUnmounted(() => { suiteRequest++ })
</script>

<style scoped>
.log-status { flex-shrink: 0; margin-bottom: 8px; }
.execution-log-page {
  /* 使用calc计算高度：100vh - layout-header(64px) - layout-content上下padding(48px) */
  height: calc(100vh - 64px - 48px);
  display: flex;
  flex-direction: column;
  background: #f5f5f5;
  overflow: hidden; /* 防止页面整体滚动 */
}

/* a-page-header 通常高度约为 64px，但我们需要让它自适应 */
.execution-log-page :deep(.ant-page-header) {
  flex-shrink: 0; /* 防止header被压缩 */
  border-bottom: 1px solid #f0f0f0;
}

.log-container {
  min-height: 0;
  flex: 1;
  padding: 16px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

.log-container :deep(.ant-spin-nested-loading) {
  min-height: 0;
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.log-container :deep(.ant-spin-container) {
  min-height: 0;
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.log-content {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  background: #1e1e1e;
  color: #d4d4d4;
  padding: 12px;
  font-family: 'Courier New', 'Monaco', 'Menlo', monospace;
  font-size: 13px;
  line-height: 1.6;
  border-radius: 4px;
  /* 确保滚动条可见 */
  scrollbar-width: thin;
  scrollbar-color: #555 #1e1e1e;
}

/* Webkit浏览器滚动条样式 */
.log-content::-webkit-scrollbar {
  width: 8px;
}

.log-content::-webkit-scrollbar-track {
  background: #1e1e1e;
  border-radius: 4px;
}

.log-content::-webkit-scrollbar-thumb {
  background: #555;
  border-radius: 4px;
}

.log-content::-webkit-scrollbar-thumb:hover {
  background: #777;
}

.log-entry {
  margin-bottom: 16px;
  border-bottom: 1px solid #2d2d2d;
  padding-bottom: 12px;
}

.log-entry:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.log-header {
  margin-bottom: 8px;
}

.log-time {
  color: #858585;
  font-size: 12px;
}

.log-message {
  white-space: pre-wrap;
  word-break: break-all;
  font-family: 'Courier New', 'Monaco', 'Menlo', monospace;
}

.log-line {
  margin-bottom: 2px;
  line-height: 1.6;
}

.log-empty-line {
  display: block;
  height: 1.6em;
}

.log-empty {
  text-align: center;
  color: #858585;
  padding: 40px;
}
</style>

