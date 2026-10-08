import { computed, ref } from 'vue'
// A successful action acknowledges only fields that it actually persisted.
export function useDraftBaseline(read: () => Record<string, unknown>) {
  const baseline = ref<Record<string, string>>({})
  const snapshot = () => Object.fromEntries(Object.entries(read()).map(([key, value]) => [key, JSON.stringify(value)]))
  const dirty = computed(() => { const current = snapshot(); return Object.keys(current).some(key => current[key] !== baseline.value[key]) })
  function acknowledge(keys?: string[]) { const current = snapshot(); baseline.value = keys ? { ...baseline.value, ...Object.fromEntries(keys.map(key => [key, current[key]])) } : current }
  return { dirty, acknowledge }
}
