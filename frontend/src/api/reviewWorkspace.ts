import type { CaseReview, ReviewItem } from "./caseGovernance";
import type { CaseIssue, CaseFile, CaseCustomField } from "./caseFeatures";
import type { TestCase } from "@/types";
import type { CaseFolder } from "./planCaseWorkspace";
import { apiClient } from "@/utils/api";
import type { PlanCaseSavedView } from "./planCaseWorkspace";
import type {
  FilterCondition,
  FilterLogic,
} from "@/components/TestCase/advancedFilter";
type ReviewViewFilters = {
  filterConditions: FilterCondition[];
  filterLogic: FilterLogic;
};
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
  myStatus: string;
  recycled: boolean;
  canVote: boolean;
  canReReview: boolean;
}
export interface ReviewCaseListing {
  items: ReviewCaseEntry[];
  total: number;
  page: number;
  size: number;
  modules: CaseFolder[];
  counts: { all: number; unassigned: number };
}
export interface ReviewReading {
  review: CaseReview;
  item: ReviewCaseEntry;
  history: Record<string, any>[];
  createdAt: string | null;
  customFields: CaseCustomField[];
  requirements: CaseIssue[];
  attachments: CaseFile[];
}
export interface ReviewItemSelection {
  itemIds?: string[];
  selectAll?: boolean;
  excludeIds?: string[];
  condition?: {
    search?: string;
    folder?: string;
    includeDescendants?: boolean;
    priority?: string;
    state?: string;
    states?: string[];
    reviewerId?: string;
    creatorId?: string;
    onlyMine?: boolean;
  };
}
export interface ReviewSelectionSummary {
  count: number;
  excludedCount: number;
  canVote: boolean;
  canReReview: boolean;
  loading?: boolean;
}
const base = (project: string) =>
  `/projects/${project}/case-governance/review-workspace`;
export const reviewWorkspaceApi = {
  candidateViews: (p: string) =>
    apiClient.get<PlanCaseSavedView[]>(`${base(p)}/candidate-views`),
  saveCandidateView: (p: string, name: string, filters: ReviewViewFilters) =>
    apiClient.post<PlanCaseSavedView>(`${base(p)}/candidate-views`, {
      name,
      filters,
    }),
  updateCandidateView: (
    p: string,
    id: string,
    name: string,
    filters?: ReviewViewFilters,
  ) =>
    apiClient.put<PlanCaseSavedView>(`${base(p)}/candidate-views/${id}`, {
      name,
      ...(filters === undefined ? {} : { filters }),
    }),
  deleteCandidateView: (p: string, id: string) =>
    apiClient.delete(`${base(p)}/candidate-views/${id}`),
  selection: (p: string, id: string, body: ReviewItemSelection) =>
    apiClient.post<ReviewSelectionSummary>(
      `${base(p)}/${id}/item-selection`,
      body,
    ),
  selectionCaseIds: (p: string, id: string, body: ReviewItemSelection) =>
    apiClient.post<{ caseIds: string[] }>(
      `${base(p)}/${id}/selection-case-ids`,
      body,
    ),
  batchVote: (
    p: string,
    id: string,
    body: ReviewItemSelection & {
      decision: string;
      comment: string;
      fileIds?: string[];
    },
  ) => apiClient.post<CaseReview>(`${base(p)}/${id}/batch-decision`, body),
  reading: (p: string, id: string, item: string) =>
    apiClient.get<ReviewReading>(`${base(p)}/${id}/items/${item}/reading`),
  reReview: (
    p: string,
    id: string,
    body: ReviewItemSelection & { comment: string },
  ) => apiClient.post<CaseReview>(`${base(p)}/${id}/re-review`, body),
  changeItemReviewers: (
    p: string,
    id: string,
    body: ReviewItemSelection & { reviewerIds: string[]; append: boolean },
  ) => apiClient.post<CaseReview>(`${base(p)}/${id}/item-reviewers`, body),
  disassociate: (p: string, id: string, body: ReviewItemSelection) =>
    apiClient.post<CaseReview>(`${base(p)}/${id}/disassociate`, body),
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
