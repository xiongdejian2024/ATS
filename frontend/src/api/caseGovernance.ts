import { apiClient } from '@/utils/api'

export interface CaseVersion {
  id: string; caseId: string; version: number; snapshot: Record<string, any>
  reason: string; createdBy: string; createdAt: string
}
export interface ReviewItem {
  id: string; caseId: string; version: number; snapshot: Record<string, any>; status: string; outdated: boolean
  decisions: { reviewerId: string; decision: string; comment: string; updatedAt: string }[]
}
export interface CaseReview {
  id: string; name: string; status: string; policy: string; reviewerIds: string[]; createdBy: string
  items: ReviewItem[]; comments: { id: string; authorId: string; content: string; createdAt: string }[]
}
export interface CaseSavedView { id: string; name: string; filters: Record<string, any> }
const base = (project: string) => `/projects/${project}/case-governance`
export const caseGovernanceApi = {
  versions: (p: string, c: string) => apiClient.get<CaseVersion[]>(`${base(p)}/cases/${c}/versions`),
  compare: (p: string, c: string, before: number, after: number) => apiClient.get<{ changes: { field: string; before: any; after: any }[] }>(`${base(p)}/cases/${c}/compare`, { params: { before, after } }),
  restore: (p: string, c: string, v: string, expectedVersion: number, reason: string) => apiClient.post(`${base(p)}/cases/${c}/versions/${v}/restore`, { expectedVersion, reason }),
  reviewers: (p: string) => apiClient.get<{ id: string; name: string }[]>(`${base(p)}/reviewers`),
  reviews: (p: string) => apiClient.get<CaseReview[]>(`${base(p)}/reviews`),
  createReview: (p: string, body: { name: string; caseIds: string[]; reviewerIds: string[]; policy: string }) => apiClient.post<CaseReview>(`${base(p)}/reviews`, body),
  vote: (p: string, review: string, item: string, decision: string, comment: string) => apiClient.post<CaseReview>(`${base(p)}/reviews/${review}/items/${item}/decision`, { decision, comment }),
  comment: (p: string, review: string, content: string) => apiClient.post<CaseReview>(`${base(p)}/reviews/${review}/comments`, { content }),
  cancel: (p: string, review: string) => apiClient.post<CaseReview>(`${base(p)}/reviews/${review}/cancel`),
  views: (p: string) => apiClient.get<CaseSavedView[]>(`${base(p)}/views`),
  saveView: (p: string, name: string, filters: Record<string, any>) => apiClient.post<CaseSavedView>(`${base(p)}/views`, { name, filters }),
  deleteView: (p: string, id: string) => apiClient.delete(`${base(p)}/views/${id}`),
  batch: (p: string, body: Record<string, any>) => apiClient.post<{ updated: number }>(`${base(p)}/batch`, body),
  copy: (p: string, caseIds: string[], moduleId: string | null) => apiClient.post<{ caseIds: string[] }>(`${base(p)}/batch-copy`, {caseIds, moduleId}),
}
