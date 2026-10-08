<template>
  <div class="bounded-log-viewer" :style="{ height }">
    <div class="log-tools">
      <span>窗口内 {{ rawLineCount }} 行，展示 {{ lines.length }} 行（最多2000行 / 512 KiB）</span>
      <span v-if="records.some(r => r.truncated)">前段已省略，可从服务器历史/下载查看已接收的完整日志</span>
      <a-switch v-model:checked="follow" size="small" aria-label="跟随最新日志" />
      <span>跟随最新</span>
      <a-switch v-model:checked="fold" size="small" aria-label="折叠连续重复日志" /><span>折叠重复行</span>
      <a-button size="small" @click="toLatest">跳到最新</a-button>
    </div>
    <div v-bind="containerProps" class="log-window" @wheel="pauseFollow" @touchstart="pauseFollow" @pointerdown="pauseFollow" @keydown="pauseFollow" tabindex="0" aria-label="实时执行日志">
      <div v-bind="wrapperProps">
        <div v-for="item in list" :key="item.index" class="virtual-log-line">
          <span class="line-time">{{ item.data.timestamp }}</span>
          <span>{{ item.data.text || ' ' }}</span>
          <span v-if="item.data.count > 1" class="repeat-count"> ×{{ item.data.count }}（至 {{ item.data.lastTimestamp }}）</span>
        </div>
      </div>
      <div v-if="!lines.length" class="log-empty">暂无日志</div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { computed, nextTick, ref, watch } from 'vue';
import { useVirtualList } from '@vueuse/core';
import { displayLogLines } from './logPresentation';
import type { LogRecord } from './boundedLogs';
const props = withDefaults(defineProps<{ records: LogRecord[]; height?: string }>(), { height: 'min(60vh, 600px)' });
const follow = ref(true);
const fold = ref(true);
const rawLineCount = computed(() => props.records.reduce((sum, record) => sum + record.message.split('\n').length, 0));
const lines = computed(() => displayLogLines(props.records, fold.value));
const { list, containerProps, wrapperProps, scrollTo } = useVirtualList(lines, { itemHeight: 24, overscan: 15 });
function pauseFollow() { follow.value = false; }
function toLatest() { follow.value = true; scrollTo(Math.max(0, lines.value.length - 1)); }
watch([lines, follow], async () => { await nextTick(); if (follow.value) scrollTo(Math.max(0, lines.value.length - 1)); }, { immediate: true });
</script>
<style scoped>
.bounded-log-viewer { flex:1; display:flex; flex-direction:column; min-height:0; }
.log-tools { flex-shrink:0; display:flex; flex-wrap:wrap; align-items:center; gap:8px; padding:8px 0; color:#86909c; }
.log-window { flex:1; min-height:0; overflow:auto; background:#171b22; color:#e6edf3; font-family:monospace; }
.virtual-log-line { height:24px; line-height:24px; white-space:pre; min-width:max-content; padding:0 8px; }
.repeat-count { color:#93c5fd; margin-left:8px; }
.line-time { color:#8b949e; margin-right:12px; }
.log-empty { padding:20px; }
</style>
