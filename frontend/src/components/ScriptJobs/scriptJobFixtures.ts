import type { ScriptJob, ScriptJobRun, ScriptNode } from '@/api/scriptJobs'
export const fixtureJob = (id = 'job-a', projectId = 'project-a'): ScriptJob => ({ id, projectId, name: id, environmentId: 'node-old', mode: 'shell', script: 'echo hello', command: '', args: [], workDir: '', timeoutSeconds: 60, revision: 1, createdAt: '2026-10-08T01:00:00Z', updatedAt: '2026-10-08T01:00:00Z' })
export const fixtureRun = (executionId = 'run-a', extra: Partial<ScriptJobRun> = {}): ScriptJobRun => ({ executionId, jobId: 'job-a', projectId: 'project-a', environmentId: 'node-old', executorId: 'user-a', status: 'running', deliveryState: 'running', cancelRequested: false, result: null, exitCode: null, durationSeconds: null, errorMessage: null, configSnapshot: fixtureJob(), createdAt: '2026-10-08T01:00:00Z', startedAt: null, completedAt: null, closedAt: null, closedBy: null, logDelivery: null, ...extra })
export const fixtureNode = (extra: Partial<ScriptNode> = {}): ScriptNode => ({ id: 'node-old', name: 'build-node', isOnline: true, supportsScriptJobs: true, owned: true, ...extra })
export function deferred<T>() {
  let resolve!: (value: T) => void, reject!: (reason: unknown) => void
  const promise = new Promise<T>((yes, no) => { resolve = yes; reject = no })
  return { promise, resolve, reject }
}
