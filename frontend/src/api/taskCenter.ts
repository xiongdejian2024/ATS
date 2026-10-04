import { apiClient } from '@/utils/api'

export interface TaskSchedule {
  id: string; projectId: string; name: string; targetType: 'suite' | 'plan' | 'group'; targetId: string
  cronExpression: string | null; timezone: string; enabled: boolean
  nextRunAt: string | null; lastRunAt: string | null; createdAt: string
}
export interface ScheduleRun {
  id: string; scheduleId: string; triggerType: string; status: string
  executionId: string | null; planRunId: string | null; errorMessage: string | null
  groupRunId?: string | null
  scheduledFor: string; createdAt: string; completedAt: string | null
}
export interface ScheduleForm {
  projectId: string; name: string; targetType: 'suite' | 'plan' | 'group'; targetId: string
  cronExpression?: string | null; timezone: string
}
export interface TargetOption { id: string; name: string; planId?: string }
export const taskCenterApi = {
  list: (projectId: string) => apiClient.get<{ items: TaskSchedule[]; total: number }>('/task-center', { params: { projectId } }),
  targets: (projectId: string) => apiClient.get<{ plans: TargetOption[]; suites: TargetOption[]; groups: TargetOption[] }>('/task-center/targets', { params: { projectId } }),
  create: (data: ScheduleForm) => apiClient.post<TaskSchedule>('/task-center', data),
  update: (id: string, data: { name: string; cronExpression: string | null; timezone: string }) => apiClient.put<TaskSchedule>(`/task-center/${id}`, data),
  enable: (id: string, enabled: boolean) => apiClient.post<TaskSchedule>(`/task-center/${id}/enabled`, { enabled }),
  run: (id: string, requestId: string) => apiClient.post<ScheduleRun>(`/task-center/${id}/run`, { requestId }),
  history: (id: string, page = 1) => apiClient.get<{ items: ScheduleRun[]; total: number }>(`/task-center/${id}/runs`, { params: { page, size: 20 } }),
  cancel: (id: string, runId: string) => apiClient.post<ScheduleRun>(`/task-center/${id}/runs/${runId}/cancel`),
  resolve: (id: string, runId: string) => apiClient.post<ScheduleRun>(`/task-center/${id}/runs/${runId}/resolve`),
}
