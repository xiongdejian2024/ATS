import { apiClient } from '@/utils/api'

export interface PlanGroup { id: string; name: string; description?: string; planCount: number; moduleId?: string | null; tags?: string[]; archived?: boolean }
export interface PlanPolicy {
  groupId: string | null; executionMode: 'serial' | 'parallel'; stopOnFailure: boolean
  passThreshold: number; suiteOrder: string[]
}
export interface RunCase {
  caseId: string; caseName: string; suiteName: string; executionId: string | null
  result: string; notes?: string; duration?: string
}
export interface PlanRun {
  id: string; planId: string; planName: string; status: string; notes?: string
  createdAt: string; startedAt: string; completedAt?: string
  configSnapshot: PlanPolicy
  reportDeleted?: boolean
  report: { total: number; passRate: number; passThreshold: number; outcome: string
    counts: Record<string, number>; cases: RunCase[]
    items: { suiteId: string; suiteName: string; status: string; executionId: string }[] }
}
export const planOrchestrationApi = {
  groups: (projectId: string, archived=false): Promise<PlanGroup[]> => apiClient.get(`/plan-orchestration/projects/${projectId}/groups`, {params:{archived}}),
  cloneGroup: (id: string): Promise<PlanGroup> => apiClient.post(`/plan-orchestration/groups/${id}/clone`),
  createGroup: (projectId: string, data: { name: string; description?: string; tags?: string[]; archived?: boolean; moduleId?: string|null }): Promise<PlanGroup> => apiClient.post(`/plan-orchestration/projects/${projectId}/groups`, data),
  updateGroup: (id: string, data: { name: string; description?: string; tags?: string[]; archived?: boolean; moduleId?: string|null }): Promise<PlanGroup> => apiClient.put(`/plan-orchestration/groups/${id}`, data),
  deleteGroup: (id: string) => apiClient.delete(`/plan-orchestration/groups/${id}`),
  settings: (planId: string): Promise<PlanPolicy> => apiClient.get(`/plan-orchestration/plans/${planId}/settings`),
  saveSettings: (planId: string, policy: PlanPolicy): Promise<PlanPolicy> => apiClient.put(`/plan-orchestration/plans/${planId}/settings`, policy),
  run: (id: string): Promise<PlanRun> => apiClient.get(`/plan-orchestration/runs/${id}`),
  resolve: (id: string): Promise<PlanRun> => apiClient.post(`/plan-orchestration/runs/${id}/resolve`, { agentStopped: true }),
  cancel: (id: string): Promise<PlanRun> => apiClient.post(`/plan-orchestration/runs/${id}/cancel`),
  manualResult: (id: string, caseId: string, result: string, notes: string): Promise<PlanRun> => apiClient.put(`/plan-orchestration/runs/${id}/cases/${caseId}/result`, { result, notes })
}
