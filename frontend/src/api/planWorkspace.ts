import type {
  FilterCondition,
  FilterLogic,
} from "@/components/TestCase/advancedFilter";
export interface WorkspaceViewFilters {
  filterConditions: FilterCondition[];
  filterLogic: FilterLogic;
}
export interface WorkspaceSavedView {
  id: string;
  name: string;
  filters: WorkspaceViewFilters;
}
export interface WorkspaceViewApi {
  listing: (projectId: string) => Promise<WorkspaceSavedView[]>;
  save: (
    projectId: string,
    name: string,
    filters: WorkspaceViewFilters,
  ) => Promise<WorkspaceSavedView>;
  update: (
    projectId: string,
    id: string,
    name: string,
    filters?: WorkspaceViewFilters,
  ) => Promise<WorkspaceSavedView>;
  remove: (projectId: string, id: string) => Promise<unknown>;
}
import { apiClient } from "@/utils/api";
export interface PlanModule {
  id: string;
  name: string;
  parentId?: string;
  position: number;
}
export interface PlanMetadata {
  moduleId?: string;
  tags: string[];
  archived: boolean;
  followed: boolean;
}
const base = "/plan-orchestration";
export const planWorkspaceApi = {
  members: (projectId: string): Promise<{ id: string; name: string }[]> =>
    apiClient.get(`${base}/projects/${projectId}/members`),
  modules: (projectId: string): Promise<PlanModule[]> =>
    apiClient.get(`${base}/projects/${projectId}/modules`),
  createModule: (projectId: string, data: Partial<PlanModule>) =>
    apiClient.post(`${base}/projects/${projectId}/modules`, data),
  updateModule: (id: string, data: Partial<PlanModule>) =>
    apiClient.put(`${base}/modules/${id}`, data),
  deleteModule: (id: string) => apiClient.delete(`${base}/modules/${id}`),
  metadata: (id: string): Promise<PlanMetadata> =>
    apiClient.get(`${base}/plans/${id}/workspace`),
  saveMetadata: (id: string, data: Partial<PlanMetadata>) =>
    apiClient.put(`${base}/plans/${id}/workspace`, data),
  follow: (id: string, followed: boolean) =>
    apiClient.put(`${base}/plans/${id}/follow`, { followed }),
  batch: (
    projectId: string,
    planIds: string[],
    changes: Record<string, unknown>,
  ) =>
    apiClient.post(`${base}/projects/${projectId}/plans/batch`, {
      planIds,
      changes,
    }),
};

export const planIndexViewApi: WorkspaceViewApi = {
  listing: (projectId) =>
    apiClient.get(`${base}/projects/${projectId}/index-views`),
  save: (projectId, name, filters) =>
    apiClient.post(`${base}/projects/${projectId}/index-views`, {
      name,
      filters,
    }),
  update: (projectId, id, name, filters) =>
    apiClient.put(`${base}/projects/${projectId}/index-views/${id}`, {
      name,
      ...(filters === undefined ? {} : { filters }),
    }),
  remove: (projectId, id) =>
    apiClient.delete(`${base}/projects/${projectId}/index-views/${id}`),
};
