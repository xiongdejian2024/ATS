import { apiClient } from "@/utils/api";

export interface CaseVersion {
  id: string;
  caseId: string;
  version: number;
  snapshot: Record<string, any>;
  reason: string;
  createdBy: string;
  createdAt: string;
}
export interface ReviewItem {
  id: string;
  caseId: string;
  version: number;
  snapshot: Record<string, any>;
  status: string;
  outdated: boolean;
  reviewerIds?: string[];
  decisions: {
    reviewerId: string;
    decision: string;
    comment: string;
    updatedAt: string;
  }[];
}
export interface CaseReview {
  lifecycle: string;
  caseCount: number;
  passCount: number;
  unPassCount: number;
  reReviewedCount: number;
  underReviewedCount: number;
  unReviewCount: number;
  reviewedCount: number;
  progress: number;
  passRate: number;
  id: string;
  name: string;
  number?: number | null;
  moduleId?: string | null;
  tags?: string[];
  archived?: boolean;
  status: string;
  policy: string;
  reviewerIds: string[];
  createdBy: string;
  mode?: "single" | "multiple";
  description?: string;
  startTime?: string | null;
  endTime?: string | null;
  startDate?: string | null;
  endDate?: string | null;
  followed?: boolean;
  history?: Record<string, any>[];
  associatedCaseIds?: string[];
  items: ReviewItem[];
  comments: {
    id: string;
    authorId: string;
    content: string;
    createdAt: string;
  }[];
}
export interface CaseSavedView {
  id: string;
  name: string;
  filters: Record<string, any>;
}
const base = (project: string) => `/projects/${project}/case-governance`;
export const caseGovernanceApi = {
  versions: (p: string, c: string) =>
    apiClient.get<CaseVersion[]>(`${base(p)}/cases/${c}/versions`),
  compare: (p: string, c: string, before: number, after: number) =>
    apiClient.get<{ changes: { field: string; before: any; after: any }[] }>(
      `${base(p)}/cases/${c}/compare`,
      { params: { before, after } },
    ),
  restore: (
    p: string,
    c: string,
    v: string,
    expectedVersion: number,
    reason: string,
  ) =>
    apiClient.post(`${base(p)}/cases/${c}/versions/${v}/restore`, {
      expectedVersion,
      reason,
    }),
  reviewers: (p: string) =>
    apiClient.get<{ id: string; name: string }[]>(`${base(p)}/reviewers`),
  reviews: (p: string, params?: Record<string, string>) =>
    apiClient.get<CaseReview[]>(`${base(p)}/reviews`, { params }),
  review: (p: string, id: string) =>
    apiClient.get<CaseReview>(`${base(p)}/reviews/${id}`),
  createReview: (p: string, body: Record<string, unknown>) =>
    apiClient.post<CaseReview>(`${base(p)}/reviews`, body),
  updateReview: (p: string, id: string, body: Record<string, unknown>) =>
    apiClient.put<CaseReview>(`${base(p)}/reviews/${id}`, body),
  copyReview: (p: string, id: string, body?: Record<string, unknown>) =>
    apiClient.post<CaseReview>(`${base(p)}/reviews/${id}/copy`, body),
  resubmit: (p: string, id: string, caseIds?: string[]) =>
    apiClient.post<CaseReview>(`${base(p)}/reviews/${id}/resubmit`, {
      caseIds,
    }),
  batchVote: (
    p: string,
    id: string,
    itemIds: string[],
    decision: string,
    comment: string,
  ) =>
    apiClient.post<CaseReview>(`${base(p)}/reviews/${id}/batch-decision`, {
      itemIds,
      decision,
      comment,
    }),
  reviewFollowState: (p: string, id: string) =>
    apiClient.get<{ followed: boolean; count: number }>(
      `${base(p)}/reviews/${id}/follow`,
    ),
  followReview: (p: string, id: string, enabled: boolean) =>
    enabled
      ? apiClient.post(`${base(p)}/reviews/${id}/follow`)
      : apiClient.delete(`${base(p)}/reviews/${id}/follow`),
  vote: (
    p: string,
    review: string,
    item: string,
    decision: string,
    comment: string,
  ) =>
    apiClient.post<CaseReview>(
      `${base(p)}/reviews/${review}/items/${item}/decision`,
      { decision, comment },
    ),
  comment: (p: string, review: string, content: string) =>
    apiClient.post<CaseReview>(`${base(p)}/reviews/${review}/comments`, {
      content,
    }),
  cancel: (p: string, review: string) =>
    apiClient.post<CaseReview>(`${base(p)}/reviews/${review}/cancel`),
  views: (p: string) => apiClient.get<CaseSavedView[]>(`${base(p)}/views`),
  saveView: (p: string, name: string, filters: Record<string, any>) =>
    apiClient.post<CaseSavedView>(`${base(p)}/views`, { name, filters }),
  renameView: (p: string, id: string, name: string) =>
    apiClient.put<CaseSavedView>(`${base(p)}/views/${id}`, { name }),
  deleteView: (p: string, id: string) =>
    apiClient.delete(`${base(p)}/views/${id}`),
  batch: (p: string, body: Record<string, any>) =>
    apiClient.post<{ updated: number }>(`${base(p)}/batch`, body),
  copy: (p: string, caseIds: string[], moduleId: string | null) =>
    apiClient.post<{ caseIds: string[] }>(`${base(p)}/batch-copy`, {
      caseIds,
      moduleId,
    }),
};
