import { ref, watch } from 'vue'
import type { ScriptJobRun } from '@/api/scriptJobs'
import { isUnknownRun } from './scriptJobState'

export function useUnknownRunConfirmation(selected: () => ScriptJobRun) {
  const confirmed = ref(false), reason = ref('')
  watch(() => [selected().jobId, selected().executionId, isUnknownRun(selected())], () => {
    confirmed.value = false; reason.value = ''
  }, { immediate: true, flush: 'sync' })
  return { confirmed, reason }
}
