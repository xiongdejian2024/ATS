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
      <a-spin :spinning="loading" class="log-spin">
        <BoundedLogViewer :records="suiteLogs" height="100%" />
      </a-spin>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { message } from 'ant-design-vue';
import { ReloadOutlined } from '@ant-design/icons-vue';
import { testSuiteApi } from '@/api/testSuite';
import { logWebSocketManager, type LogMessage } from '@/utils/logWebSocket';
import BoundedLogViewer from '@/components/ExecutionLogs/BoundedLogViewer.vue'
import { useBoundedLogs } from '@/components/ExecutionLogs/useBoundedLogs'

const route = useRoute()
const router = useRouter()

const suiteId = ref<string>('')
const suiteName = ref<string>('')
const logId = ref<string | undefined>(undefined)
const executionId = ref<string | undefined>(undefined)
const isRunning = ref<boolean>(false)

const loading = ref(false)
const { records: suiteLogs, append: appendLog, replace: replaceLogs, clear: clearLogBuffer } = useBoundedLogs()
let active = true
let logRequest = 0
const currentLogHandler = ref<((message: LogMessage) => void) | null>(null)

const loadSuiteLogs = async () => {
  if (!suiteId.value) return

  loading.value = true
  const request = ++logRequest
  try {
    const params: any = {
      skip: 0,
      limit: 20
    }

    if (logId.value) {
      params.logId = logId.value
    } else if (executionId.value) {
      params.executionId = executionId.value
    }

    const response = await testSuiteApi.getSuiteLogs(suiteId.value, params)

    if (active && request === logRequest) replaceLogs(response.items || [])
  } catch (error) {
    console.error('加载测试套日志失败:', error)
    message.error('加载日志失败')
  } finally {
    if (request === logRequest) loading.value = false
  }
}

const refreshLogs = () => {
  loadSuiteLogs()
}

const clearLogs = () => {
  logRequest++
  loading.value = false
  clearLogBuffer()
}

const handleBack = () => {
  router.back()
}

// 初始化
onMounted(async () => {
  // 从路由参数获取信息
  suiteId.value = route.query.suiteId as string || ''
  logId.value = route.query.logId as string || undefined
  executionId.value = route.query.executionId as string || undefined
  isRunning.value = route.query.isRunning === 'true'

  if (!suiteId.value) {
    message.error('缺少测试套ID')
    router.back()
    return
  }

  // 加载测试套信息
  try {
    const suite = await testSuiteApi.getTestSuite(suiteId.value)
    suiteName.value = suite.name
  } catch (error) {
    console.error('加载测试套失败:', error)
  }

  if (isRunning.value && active) await connectWebSocket()
  if (active) await loadSuiteLogs()
})

// 连接WebSocket
const connectWebSocket = async () => {
  if (!suiteId.value) return

  // 如果之前有处理器，先移除
  if (currentLogHandler.value) {
    logWebSocketManager.off(currentLogHandler.value)
    currentLogHandler.value = null
  }

  const logHandler = (event: LogMessage) => {
    if (active && event.type === 'test_suite_log' && event.suite_id === suiteId.value && event.data
      && (!executionId.value || event.data.execution_id === executionId.value)
      && (!logId.value || event.data.id === logId.value)) appendLog(event.data)
  }

  logWebSocketManager.on(logHandler)
  currentLogHandler.value = logHandler
  if (!await logWebSocketManager.connect(suiteId.value) && active) message.warning('实时日志连接失败，可刷新查看服务器日志')
}

// 组件卸载时清理
onUnmounted(() => {
  active = false
  logRequest++
  // 断开WebSocket连接
  if (currentLogHandler.value) {
    logWebSocketManager.off(currentLogHandler.value)
    currentLogHandler.value = null
  }
  logWebSocketManager.disconnect()
})
</script>

<style scoped>
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

