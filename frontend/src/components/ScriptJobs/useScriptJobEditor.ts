import { computed, onScopeDispose, ref, watch } from 'vue'
import { scriptJobsApi, type ScriptJob, type ScriptNode, type ScriptJobConfig } from '@/api/scriptJobs'
import { emptyScriptJob, nodeLabel, scriptJobError, validateScriptJob } from './scriptJobState'

export interface ScriptEditorSource { open: boolean; projectId: string; job: ScriptJob | null; nodes: ScriptNode[] }
export function useScriptJobEditor(source: ScriptEditorSource, events: { close(): void; saved(job: ScriptJob): void }, api = scriptJobsApi) {
  const form = ref<ScriptJobConfig>(emptyScriptJob('')), saving = ref(false), error = ref('')
  let generation = 0
  const selectedNode = computed(() => source.nodes.find(node => node.id === form.value.environmentId))
  const nodeOptions = computed(() => source.nodes.map(node => ({ value: node.id, label: nodeLabel(node) })))
  watch(() => [source.open, source.projectId, source.job?.id], () => {
    generation++; saving.value = false; error.value = ''
    form.value = source.job ? { ...source.job, args: [...source.job.args] } : emptyScriptJob(source.projectId)
  }, { immediate: true, flush: 'sync' })
  function close() { generation++; events.close() }
  async function save() {
    if (!source.open || saving.value) return
    const value = form.value
    const config: ScriptJobConfig = { projectId: source.projectId, name: value.name.trim(), environmentId: value.environmentId, mode: value.mode,
      script: value.mode === 'command' ? '' : value.script, command: value.mode === 'command' ? value.command.trim() : '', args: [...value.args],
      workDir: value.workDir.trim(), timeoutSeconds: value.timeoutSeconds }
    error.value = validateScriptJob(config)
    if (!selectedNode.value) error.value ||= '节点不可用或无访问权限，请重新选择节点。'
    if (error.value) return
    const current = generation, jobId = source.job?.id
    saving.value = true
    try {
      const { projectId: _projectId, ...update } = config
      const saved = jobId ? await api.update(jobId, update) : await api.create(config)
      if (current === generation) events.saved(saved)
    } catch (reason) { if (current === generation) error.value = scriptJobError(reason) }
    finally { if (current === generation) saving.value = false }
  }
  onScopeDispose(() => { generation++ })
  return { form, saving, error, selectedNode, nodeOptions, close, save }
}
