import type { CaseReview, ReviewItem } from "./caseGovernance";
import type { TestCase } from "@/types";
import type { CaseFolder } from "./planCaseWorkspace";
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
  startTime: string | null;
  endTime: string | null;
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
export interface ReviewCandidates {
  items: (TestCase & { moduleName: string })[];
  total: number;
  page: number;
  size: number;
  modules: CaseFolder[];
  counts: { all: number; unassigned: number };
}
export interface ReviewCaseEntry extends ReviewItem {
  name: string;
  caseCode: string;
  priority: string;
  moduleId: string | null;
  moduleName: string;
  createdBy: string | null;
  creator: string;
  reviewState: string;
  recycled: boolean;
  canVote: boolean;
}
export interface ReviewCaseListing {
  items: ReviewCaseEntry[];
  total: number;
  page: number;
  size: number;
  modules: CaseFolder[];
  counts: { all: number; unassigned: number };
}
const base = (project: string) =>
  `/projects/${project}/case-governance/review-workspace`;
export const reviewWorkspaceApi = {
  changeItemReviewers: (
    p: string,
    id: string,
    body: { itemIds: string[]; reviewerIds: string[]; append: boolean },
  ) => apiClient.post<CaseReview>(`${base(p)}/${id}/item-reviewers`, body),
  disassociate: (p: string, id: string, itemIds: string[]) =>
    apiClient.post<CaseReview>(`${base(p)}/${id}/disassociate`, { itemIds }),
  detail: (p: string, id: string) =>
    apiClient.get<CaseReview>(`${base(p)}/${id}/detail`),
  items: (p: string, id: string, params: Record<string, unknown>) =>
    apiClient.get<ReviewCaseListing>(`${base(p)}/${id}/items`, { params }),
  item: (p: string, id: string, item: string) =>
    apiClient.get<ReviewCaseEntry>(`${base(p)}/${id}/items/${item}`),
  associate: (
    p: string,
    id: string,
    body: { caseIds: string[]; reviewerIds: string[] },
  ) =>
    apiClient.post<import("./caseGovernance").CaseReview>(
      `${base(p)}/${id}/associate`,
      body,
    ),
  updateHeader: (p: string, id: string, body: Record<string, unknown>) =>
    apiClient.put<import("./caseGovernance").CaseReview>(
      `${base(p)}/${id}/header`,
      body,
    ),
  candidates: (p: string, params: Record<string, unknown>) =>
    apiClient.get<ReviewCandidates>(`${base(p)}/candidates`, { params }),
  selectCandidates: (p: string, body: Record<string, unknown>) =>
    apiClient.post<{ caseIds: string[]; total: number }>(
      `${base(p)}/candidate-selection`,
      body,
    ),
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
