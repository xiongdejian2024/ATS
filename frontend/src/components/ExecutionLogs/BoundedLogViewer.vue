<template>
  <div class="bounded-log-viewer" :style="{ height }">
    <div class="log-tools">
      <span>显示最近{{ lines.length }}行（最多2000行）</span>
      <span v-if="records.some(r => r.truncated)">前段已省略，完整日志保留在服务器</span>
      <a-switch v-model:checked="follow" size="small" aria-label="跟随最新日志" />
      <span>跟随最新</span>
      <a-button size="small" @click="toLatest">跳到最新</a-button>
    </div>
    <div v-bind="containerProps" class="log-window" @wheel="pauseFollow" @touchstart="pauseFollow" @pointerdown="pauseFollow" @keydown="pauseFollow" tabindex="0" aria-label="实时执行日志">
      <div v-bind="wrapperProps">
        <div v-for="item in list" :key="item.index" class="virtual-log-line">
          <span class="line-time">{{ item.data.timestamp }}</span>
          <span>{{ item.data.text || ' ' }}</span>
        </div>
      </div>
      <div v-if="!lines.length" class="log-empty">暂无日志</div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { computed, nextTick, ref, watch } from 'vue';
import { useVirtualList } from '@vueuse/core';
import type { LogRecord } from './boundedLogs';
const props = withDefaults(defineProps<{ records: LogRecord[]; height?: string }>(), { height: 'min(60vh, 600px)' });
const follow = ref(true);
const lines = computed(() => props.records.flatMap(record => record.message.split('\n').map(text => ({ text, timestamp: record.timestamp.slice(11, 23) }))));
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
.line-time { color:#8b949e; margin-right:12px; }
.log-empty { padding:20px; }
</style>
