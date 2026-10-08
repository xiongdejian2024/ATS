import { reactive, ref } from 'vue'

export interface Submission { requestId: string; busy: boolean; uncertain: boolean }
const STORAGE_KEY = 'ats.script-job-submissions.v1'
/** Bounded retry identities only. Scripts, output and credentials never enter storage. */
export function createSubmissionStore(storage?: Pick<Storage, 'getItem' | 'setItem'>) {
  const entries = reactive(new Map<string, Submission>())
  const persistent = ref(!!storage)
  try {
    const raw = storage?.getItem(STORAGE_KEY)
    if (raw && raw.length <= 65536) {
      const rows: unknown = JSON.parse(raw)
      if (Array.isArray(rows)) for (const row of rows.slice(0, 64)) {
        if (Array.isArray(row) && row.length === 2 && typeof row[0] === 'string' && row[0].length <= 512 && typeof row[1] === 'string' && row[1].length <= 128)
          entries.set(row[0], { requestId: row[1], busy: false, uncertain: true })
      }
    }
  } catch { persistent.value = false }
  function save() {
    try { storage?.setItem(STORAGE_KEY, JSON.stringify([...entries].map(([key, value]) => [key, value.requestId]))) }
    catch { persistent.value = false }
  }
  return { entries, persistent, save }
}
function browserStorage() { try { return globalThis.sessionStorage } catch { return undefined } }
export const scriptJobSubmissions = createSubmissionStore(browserStorage())
