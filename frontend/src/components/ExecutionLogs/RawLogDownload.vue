<template>
  <div class="raw-log-download">
    <a-space wrap>
      <a-button v-if="picker" size="small" :loading="busy" @click="download.saveFull(picker)">保存完整原始日志</a-button>
      <a-button size="small" :loading="busy" :disabled="complete" @click="download.nextPart()">
        {{ complete ? '所有分段已下载' : parts ? `下载下一分段 (${parts + 1})` : '分段下载原始日志' }}
      </a-button>
      <a-button v-if="busy" size="small" @click="restart">取消下载</a-button>
      <a-button v-else-if="parts || error" size="small" @click="restart">重新开始</a-button>
      <span v-if="parts">已处理 {{ parts }} 段{{ complete ? '，快照完整' : '，尚未完成' }}</span>
    </a-space>
    <div class="download-hint">{{ picker ? '完整保存逐段写入文件；也可逐次下载分段。' : '此浏览器需要逐次下载分段。' }}每段最多 256 KiB，按编号拼接可恢复完整快照。范围固定为开始时已接收的日志，保留空格、换行和重复内容。</div>
    <a-alert v-if="error" :message="error" type="error" show-icon />
  </div>
</template>
<script setup lang="ts">
import { watch } from 'vue'
import { useRawLogDownload, type RawLogTarget, type LogFilePicker } from './useRawLogDownload'
const props = defineProps<{ target: RawLogTarget | null }>()
const picker = (window as Window & { showSaveFilePicker?: LogFilePicker }).showSaveFilePicker?.bind(window)
const download = useRawLogDownload()
const { busy, complete, parts, error } = download
const restart = () => download.open(props.target)
watch(() => [props.target?.endpoint, props.target?.filename, props.target?.executionId, props.target?.logId], restart, { immediate: true })
</script>
<style scoped>
.raw-log-download { margin: 8px 0; }
.download-hint { color: #86909c; font-size: 12px; margin-top: 5px; }
</style>
