import { apiClient } from '@/utils/api'
import type { LogRecord } from '@/components/ExecutionLogs/boundedLogs'

export type ScriptMode = 'shell' | 'python' | 'command'
export interface ScriptJobConfig {
  projectId: string
  name: string
  environmentId: string
  mode: ScriptMode
  script: string
  command: string
  args: string[]
  workDir: string
  timeoutSeconds: number
}
export interface ScriptJob extends ScriptJobConfig { id: string; revision: number; createdAt: string; updatedAt: string }
export interface ScriptNode { id: string; name: string; isOnline: boolean; supportsScriptJobs: boolean; owned: boolean; osType?: string }
export interface ScriptJobRun {
  executionId: string
  jobId: string
  projectId: string
  environmentId: string
  executorId: string
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled'
  deliveryState: 'queued' | 'dispatching' | 'sent' | 'running' | 'unknown' | 'terminal'
  cancelRequested: boolean
  result: null | 'success' | 'failed' | 'timeout' | 'error' | 'cancelled' | 'unknown'
  exitCode: number | null
  durationSeconds: number | null
  errorMessage: string | null
  configSnapshot: Omit<ScriptJobConfig, 'projectId'> & { revision?: number }
  createdAt: string
  startedAt: string | null
  completedAt: string | null
  closedBy: string | null
  closedAt: string | null
  logDelivery: Record<string, unknown> | null
}
export interface ScriptPage<T> { items: T[]; total: number; page: number; size: number }
export interface ScriptLogPage { items: LogRecord[]; total: number; skip: number; limit: number }
const jobPath = (jobId: string) => `/script-jobs/${encodeURIComponent(jobId)}`
export const scriptRunPath = (jobId: string, executionId: string) => `${jobPath(jobId)}/runs/${encodeURIComponent(executionId)}`
export const scriptJobsApi = {
  list: (projectId: string, page = 1, signal?: AbortSignal): Promise<ScriptPage<ScriptJob>> => apiClient.get('/script-jobs', { params: { projectId, page, size: 20 }, signal }),
  nodes: (projectId: string, signal?: AbortSignal): Promise<{ items: ScriptNode[] }> => apiClient.get('/script-jobs/nodes', { params: { projectId }, signal }),
  get: (jobId: string, signal?: AbortSignal): Promise<ScriptJob> => apiClient.get(jobPath(jobId), { signal }),
  create: (config: ScriptJobConfig): Promise<ScriptJob> => apiClient.post('/script-jobs', config),
  update: (jobId: string, config: Omit<ScriptJobConfig, 'projectId'>): Promise<ScriptJob> => apiClient.put(jobPath(jobId), config),
  run: (jobId: string, requestId: string): Promise<ScriptJobRun> => apiClient.post(`${jobPath(jobId)}/runs`, { requestId }),
  history: (jobId: string, page = 1, signal?: AbortSignal): Promise<ScriptPage<ScriptJobRun>> => apiClient.get(`${jobPath(jobId)}/runs`, { params: { page, size: 20 }, signal }),
  getRun: (jobId: string, executionId: string, signal?: AbortSignal): Promise<ScriptJobRun> => apiClient.get(scriptRunPath(jobId, executionId), { signal }),
  cancel: (jobId: string, executionId: string): Promise<ScriptJobRun> => apiClient.post(`${scriptRunPath(jobId, executionId)}/cancel`, {}),
  resolve: (jobId: string, executionId: string, reason: string): Promise<ScriptJobRun> => apiClient.post(`${scriptRunPath(jobId, executionId)}/resolve`, { confirmedStopped: true, reason }),
  logs: (jobId: string, executionId: string, signal?: AbortSignal): Promise<ScriptLogPage> => apiClient.get(`${scriptRunPath(jobId, executionId)}/logs`, { params: { skip: 0, limit: 20 }, signal }),
}
