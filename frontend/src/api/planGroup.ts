import { apiClient } from '@/utils/api'
import type { PlanRun } from '@/api/planOrchestration'

export interface GroupPolicy { executionMode: 'serial' | 'parallel'; stopOnFailure: boolean; passThreshold: number; planOrder: string[]; members?: {id:string;name:string}[] }
export interface GroupRun { id: string; groupId: string; projectId: string; groupName: string; status: string; startedAt: string; completedAt?: string; configSnapshot: GroupPolicy; summary: { conclusion?: string; risk?: string; notes?: string }; report: PlanRun['report']; children: PlanRun[] }
export const planGroupApi = {
  settings: (id: string) => apiClient.get<GroupPolicy>(`/plan-groups/${id}/settings`),
  save: (id: string, data: GroupPolicy) => apiClient.put<GroupPolicy>(`/plan-groups/${id}/settings`, data),
  execute: (id: string, requestId: string) => apiClient.post<GroupRun>(`/plan-groups/${id}/runs`, { requestId }),
  history: (id: string, page = 1) => apiClient.get<{ items: GroupRun[]; total: number }>(`/plan-groups/${id}/runs`, { params: { page } }),
  run: (id: string) => apiClient.get<GroupRun>(`/plan-groups/runs/${id}`),
  cancel: (id: string) => apiClient.post<GroupRun>(`/plan-groups/runs/${id}/cancel`),
  summary: (id: string, data: GroupRun['summary']) => apiClient.put<GroupRun>(`/plan-groups/runs/${id}/summary`, data),
  share: (id: string, expiresHours: number) => apiClient.post<{ id: string; path: string; expiresAt: string }>(`/plan-groups/runs/${id}/share`, { expiresHours }),
  revoke: (id: string, shareId: string) => apiClient.delete(`/plan-groups/runs/${id}/shares/${shareId}`),
  pdf: async (id: string) => (await apiClient.getInstance().get(`/plan-groups/runs/${id}/pdf`, { responseType: 'blob', timeout: 60000 })).data as Blob,
}
