import { apiClient } from "@/utils/api";
export interface ReviewModule {
  id: string;
  name: string;
  parentId: string | null;
  position: number;
  count: number;
}
export interface ReviewSummary {
  id: string;
  number: number | null;
  name: string;
  caseCount: number;
  passedCount: number;
  passRate: number;
  lifecycle: string;
  mode: string;
  reviewerIds: string[];
  reviewers: string[];
  createdBy: string;
  creator: string;
  moduleId: string | null;
  moduleName: string;
  modulePath: string;
  tags: string[];
  description: string;
  startDate: string | null;
  endDate: string | null;
  createdAt: string;
  archived: boolean;
}
export interface ReviewList {
  items: ReviewSummary[];
  total: number;
  page: number;
  size: number;
  modules: ReviewModule[];
  defaultCount: number;
  allCount: number;
  permissions: { update: boolean; delete: boolean };
}
const base = (project: string) =>
  `/projects/${project}/case-governance/review-workspace`;
export const reviewWorkspaceApi = {
  list: (p: string, params: Record<string, unknown>) =>
    apiClient.get<ReviewList>(base(p), { params }),
  saveModule: (
    p: string,
    body: { name: string; parentId: string | null; position: number },
    id?: string,
  ) =>
    id
      ? apiClient.put<ReviewModule>(`${base(p)}/modules/${id}`, body)
      : apiClient.post<ReviewModule>(`${base(p)}/modules`, body),
  deleteModule: (p: string, id: string, name: string) =>
    apiClient.post(`${base(p)}/modules/${id}/delete`, { name }),
  move: (p: string, reviewIds: string[], moduleId: string | null) =>
    apiClient.post(`${base(p)}/move`, { reviewIds, moduleId }),
  delete: (p: string, id: string, name: string) =>
    apiClient.post(`${base(p)}/${id}/delete`, { name }),
  archive: (p: string, id: string) =>
    apiClient.post(`${base(p)}/${id}/archive`),
};
