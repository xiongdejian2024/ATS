import { onScopeDispose, ref, shallowRef } from 'vue'
import { scriptJobsApi, type ScriptJob, type ScriptJobRun, type ScriptNode } from '@/api/scriptJobs'
import { isActiveRun, isUnknownRun, scriptJobError } from './scriptJobState'
import { createRequestId } from '@/utils/requestId'
import { scriptJobSubmissions } from './scriptJobSubmissions'

export function useScriptJobs(api = scriptJobsApi, requestStore = scriptJobSubmissions, ownerId = '') {
  const requests = requestStore.entries
  const projectId = ref(''), jobs = shallowRef<ScriptJob[]>([]), nodes = shallowRef<ScriptNode[]>([])
  const page = ref(1), total = ref(0), loading = ref(false), error = ref(''), nodeError = ref('')
  const job = shallowRef<ScriptJob | null>(null), runs = shallowRef<ScriptJobRun[]>([]), run = shallowRef<ScriptJobRun | null>(null)
  const historyPage = ref(1), historyTotal = ref(0), historyLoading = ref(false), historyError = ref(''), runError = ref(''), actionError = ref('')
  const actionBusy = ref(false)
  let scope = 0, selection = 0, runSelection = 0, listRequest = 0, historyRequest = 0, runRequest = 0
  let disposed = false, timer: ReturnType<typeof setTimeout> | undefined
  const reads = new Set<AbortController>()
  const activeReads = new Map<string, AbortController>()
  const key = (id: string) => JSON.stringify([ownerId, projectId.value, id])
  const submission = (id: string) => requests.get(key(id))
  function reader(kind: string) { activeReads.get(kind)?.abort(); const request = new AbortController(); activeReads.set(kind, request); reads.add(request); return request }
  function closeRun() { activeReads.get('run')?.abort(); runSelection++; runRequest++; run.value = null; runError.value = ''; actionError.value = ''; actionBusy.value = false }
  function closeJob() { activeReads.get('job')?.abort(); activeReads.get('history')?.abort(); selection++; historyRequest++; closeRun(); job.value = null; runs.value = []; historyTotal.value = 0; historyPage.value = 1; historyLoading.value = false; historyError.value = '' }
  function setProject(id: string) {
    scope++; listRequest++; reads.forEach(request => request.abort()); reads.clear(); closeJob()
    projectId.value = id; page.value = 1; total.value = 0; jobs.value = []; nodes.value = []; error.value = ''; nodeError.value = ''; loading.value = false
    if (id) void refresh()
  }
  async function refresh() {
    if (!projectId.value || disposed) return
    const currentScope = scope, requestId = ++listRequest, request = reader('list'), id = projectId.value
    loading.value = true; error.value = ''; nodeError.value = ''
    const [list, options] = await Promise.allSettled([api.list(id, page.value, request.signal), api.nodes(id, request.signal)])
    reads.delete(request)
    if (disposed || currentScope !== scope || requestId !== listRequest) return
    if (list.status === 'fulfilled') { jobs.value = list.value.items; total.value = list.value.total }
    else error.value = scriptJobError(list.reason)
    if (options.status === 'fulfilled') nodes.value = options.value.items
    else { nodes.value = []; nodeError.value = scriptJobError(options.reason) }
    loading.value = false
  }
  async function refreshHistory() {
    if (!job.value || disposed) return
    const currentScope = scope, currentSelection = selection, requestId = ++historyRequest, request = reader('history'), id = job.value.id
    historyLoading.value = true; historyError.value = ''
    try {
      const response = await api.history(id, historyPage.value, request.signal)
      if (disposed || currentScope !== scope || currentSelection !== selection || requestId !== historyRequest) return
      runs.value = response.items; historyTotal.value = response.total
    } catch (reason) {
      if (!disposed && currentScope === scope && currentSelection === selection && requestId === historyRequest) historyError.value = scriptJobError(reason)
    } finally {
      reads.delete(request)
      if (!disposed && currentScope === scope && currentSelection === selection && requestId === historyRequest) historyLoading.value = false
    }
  }
  async function selectJob(id: string) {
    closeJob()
    if (!id || !projectId.value || disposed) return
    const currentScope = scope, currentSelection = selection, request = reader('job')
    historyLoading.value = true
    try {
      const response = await api.get(id, request.signal)
      if (disposed || currentScope !== scope || currentSelection !== selection) return
      if (response.projectId !== projectId.value) throw new Error('此作业不属于当前项目。')
      job.value = response
      await refreshHistory()
    } catch (reason) {
      if (!disposed && currentScope === scope && currentSelection === selection) historyError.value = scriptJobError(reason)
    } finally {
      reads.delete(request)
      if (!disposed && currentScope === scope && currentSelection === selection) historyLoading.value = false
    }
  }
  async function selectRun(id: string) {
    closeRun()
    if (!id || !job.value || disposed) return
    const currentScope = scope, currentSelection = selection, currentRun = runSelection, requestId = ++runRequest, request = reader('run'), jobId = job.value.id
    try {
      const response = await api.getRun(jobId, id, request.signal)
      if (!disposed && currentScope === scope && currentSelection === selection && currentRun === runSelection && requestId === runRequest) run.value = response
    } catch (reason) {
      if (!disposed && currentScope === scope && currentSelection === selection && currentRun === runSelection && requestId === runRequest) runError.value = scriptJobError(reason)
    } finally { reads.delete(request) }
  }
  async function refreshRun() {
    if (!run.value || disposed) return
    const selected = run.value, currentScope = scope, currentSelection = selection, currentRun = runSelection, requestId = ++runRequest, request = reader('run')
    try {
      const response = await api.getRun(selected.jobId, selected.executionId, request.signal)
      if (!disposed && currentScope === scope && currentSelection === selection && currentRun === runSelection && requestId === runRequest) { run.value = response; runError.value = '' }
    } catch (reason) {
      if (!disposed && currentScope === scope && currentSelection === selection && currentRun === runSelection && requestId === runRequest) runError.value = scriptJobError(reason)
    } finally { reads.delete(request) }
  }
  async function submit(selected: ScriptJob): Promise<ScriptJobRun | undefined> {
    const submissionKey = JSON.stringify([ownerId, selected.projectId, selected.id])
    if (disposed || selected.projectId !== projectId.value || requests.get(submissionKey)?.busy) return
    if (!requests.has(submissionKey) && requests.size >= 64) { error.value = '尚有较多提交待核对，请先确认已有提交结果。'; return }
    const pending = requests.get(submissionKey) || { requestId: createRequestId(), busy: false, uncertain: false }
    requests.set(submissionKey, { ...pending, busy: true })
    requestStore.save()
    const currentScope = scope, currentSelection = selection, currentRun = runSelection
    error.value = ''
    try {
      const response = await api.run(selected.id, pending.requestId)
      requests.delete(submissionKey)
      requestStore.save()
      if (disposed || currentScope !== scope || currentSelection !== selection || currentRun !== runSelection) return
      return response
    } catch (reason) {
      requests.set(submissionKey, { ...pending, busy: false, uncertain: true })
      requestStore.save()
      if (!disposed && currentScope === scope) error.value = `${scriptJobError(reason)} 提交结果尚未确认。再次点击会使用同一个请求编号核对，不会自动重跑。`
    }
  }
  async function act(kind: 'cancel' | 'resolve', confirmedStopped = false, reason = '') {
    if (!run.value || actionBusy.value || disposed) return
    const selected = run.value
    if (kind === 'resolve' ? !confirmedStopped || !isUnknownRun(selected) : !isActiveRun(selected) || selected.cancelRequested) return
    const currentScope = scope, currentSelection = selection, currentRun = runSelection
    runRequest++ // An older poll cannot overwrite the action result.
    actionBusy.value = true; actionError.value = ''
    try {
      const response = kind === 'cancel' ? await api.cancel(selected.jobId, selected.executionId) : await api.resolve(selected.jobId, selected.executionId, reason)
      if (disposed || currentScope !== scope || currentSelection !== selection || currentRun !== runSelection) return
      runRequest++; run.value = response
      void refreshHistory()
    } catch (failure) {
      if (!disposed && currentScope === scope && currentSelection === selection && currentRun === runSelection) actionError.value = `${scriptJobError(failure)} 请刷新核对当前执行状态。`
    } finally {
      if (!disposed && currentScope === scope && currentSelection === selection && currentRun === runSelection) actionBusy.value = false
    }
  }
  async function poll() {
    if (disposed) return
    if (typeof document === 'undefined' || document.visibilityState !== 'hidden') {
      await Promise.all([job.value ? refreshHistory() : undefined, run.value && isActiveRun(run.value) && !actionBusy.value ? refreshRun() : undefined])
    }
    if (!disposed) timer = setTimeout(poll, 3000)
  }
  timer = setTimeout(poll, 3000)
  onScopeDispose(() => { disposed = true; scope++; closeJob(); if (timer) clearTimeout(timer); reads.forEach(request => request.abort()); reads.clear() })
  return { projectId, jobs, nodes, page, total, loading, error, nodeError, job, runs, run, historyPage, historyTotal, historyLoading, historyError, runError, actionError, actionBusy,
    setProject, refresh, selectJob, closeJob, selectRun, closeRun, refreshRun, refreshHistory, submit, submission, act, persistentRequests: requestStore.persistent }
}
