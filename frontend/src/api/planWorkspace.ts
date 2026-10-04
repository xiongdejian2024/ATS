import { apiClient } from '@/utils/api'
export interface PlanModule { id: string; name: string; parentId?: string; position: number }
export interface PlanMetadata { moduleId?: string; tags: string[]; archived: boolean; followed: boolean }
const base = '/plan-orchestration'
export const planWorkspaceApi = {
  modules: (projectId: string): Promise<PlanModule[]> => apiClient.get(`${base}/projects/${projectId}/modules`),
  createModule: (projectId: string, data: Partial<PlanModule>) => apiClient.post(`${base}/projects/${projectId}/modules`, data),
  updateModule: (id: string, data: Partial<PlanModule>) => apiClient.put(`${base}/modules/${id}`, data),
  deleteModule: (id: string) => apiClient.delete(`${base}/modules/${id}`),
  metadata: (id: string): Promise<PlanMetadata> => apiClient.get(`${base}/plans/${id}/workspace`),
  saveMetadata: (id: string, data: Partial<PlanMetadata>) => apiClient.put(`${base}/plans/${id}/workspace`, data),
  follow: (id: string, followed: boolean) => apiClient.put(`${base}/plans/${id}/follow`, { followed }),
  batch: (projectId: string, planIds: string[], changes: Record<string, unknown>) => apiClient.post(`${base}/projects/${projectId}/plans/batch`, { planIds, changes })
}
