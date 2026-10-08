import { ref, onScopeDispose } from 'vue'
import { testSuiteApi, type SuiteDeliveryState } from '@/api/testSuite'

export function useSuiteDelivery(api = testSuiteApi) {
  const delivery = ref<SuiteDeliveryState | null>(null)
  const confirmed = ref(false), reason = ref(''), busy = ref(false), error = ref('')
  let generation = 0, selection: { suiteId: string; executionId: string } | null = null
  let timer: ReturnType<typeof setTimeout> | undefined
  function invalidate() { ++generation; clearTimeout(timer); timer = undefined }
  async function load(version: number) {
    if (!selection) return
    const target = selection
    try {
      const result = await api.getDeliveryState(target.suiteId, target.executionId)
      if (version !== generation || busy.value) return
      if (result.deliveryState !== delivery.value?.deliveryState) { confirmed.value = false; reason.value = '' }
      delivery.value = result; error.value = ''
      if (result.status === 'running' || result.status === 'pending') timer = setTimeout(() => void load(version), 5000)
    } catch (failure) {
      if (version === generation) { delivery.value = null; error.value = '加载执行核对状态失败'; confirmed.value = false; console.error(error.value, failure) }
    }
  }
  function open(suiteId: string, executionId: string) {
    invalidate(); selection = suiteId && executionId ? { suiteId, executionId } : null
    delivery.value = null; confirmed.value = false; reason.value = ''; busy.value = false; error.value = ''
    if (selection) void load(generation)
  }
  async function resolve() {
    if (busy.value || !selection || !confirmed.value || !reason.value.trim() || !delivery.value?.canResolve) return false
    invalidate()
    const version = generation, target = selection
    busy.value = true; error.value = ''
    try {
      const result = await api.resolveDelivery(target.suiteId, target.executionId, reason.value.trim())
      if (version !== generation) return false
      delivery.value = result; confirmed.value = false; reason.value = ''; error.value = ''
      return true
    } catch (failure) {
      if (version === generation) { error.value = '核对未完成，请刷新状态后重试'; confirmed.value = false; console.error(error.value, failure) }
      return false
    } finally { if (version === generation) busy.value = false }
  }
  function refresh() {
    if (busy.value) return
    invalidate(); confirmed.value = false; reason.value = ''
    if (selection && !busy.value) void load(generation)
  }
  onScopeDispose(() => { invalidate(); selection = null })
  return { delivery, confirmed, reason, busy, error, open, resolve, refresh }
}
