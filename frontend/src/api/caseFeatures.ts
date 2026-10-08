import { apiClient } from "@/utils/api";
import type { TestCase } from "@/types";
export interface CaseFile {
  id: string;
  caseId: string;
  fileName: string;
  fileSize: number;
  fileType: string;
  uploadedBy: string;
  uploadTime: string;
}
export interface CaseChange {
  id: string;
  actorId: string;
  action: string;
  detail: Record<string, unknown>;
  createdAt: string;
}
export interface CaseCustomField {
  key: string;
  name: string;
  type:
    | "text"
    | "textarea"
    | "number"
    | "boolean"
    | "date"
    | "select"
    | "multiselect";
  required: boolean;
  options: string[];
  default: unknown;
}
export interface CaseTemplate {
  id: string;
  name: string;
  fields: CaseCustomField[];
  defaults: Record<string, any>;
  isDefault: boolean;
}
export interface CaseIssue {
  id: string;
  projectId?: string;
  linkId?: string;
  kind: "requirement" | "defect";
  title: string;
  description: string;
  status: string;
  externalRef?: string;
}
export interface CaseRelation {
  id: string;
  targetCaseId: string;
  name: string;
  caseCode: string;
  deleted: boolean;
  kind: string;
}
export interface CaseAutomation {
  id: string;
  category: string;
  targetCaseId?: string;
  suiteId?: string;
  externalRef?: string;
}
export interface CaseComment {
  canDelete?: boolean;
  files?: import("./fileLibrary").LibraryFile[];
  id: string;
  authorId: string;
  content: string;
  createdAt: string;
}
const base = (p: string) => `/projects/${p}/case-features`;
export const caseFeaturesApi = {
  settings: (p: string) => apiClient.get<{autoResubmit:boolean}>(`${base(p)}/settings`),
  saveSettings: (p: string, autoResubmit: boolean) => apiClient.put(`${base(p)}/settings`, {autoResubmit}),
  usage: (p: string, c: string) =>
    apiClient.get<{
      plans: { id: string; name: string; status: string }[];
      reviews: { id: string; name: string; status: string }[];
    }>(`${base(p)}/cases/${c}/usage`),
  templates: (p: string) =>
    apiClient.get<CaseTemplate[]>(`${base(p)}/templates`),
  saveTemplate: (p: string, body: Omit<CaseTemplate, "id">, id?: string) =>
    id
      ? apiClient.put<CaseTemplate>(`${base(p)}/templates/${id}`, body)
      : apiClient.post<CaseTemplate>(`${base(p)}/templates`, body),
  deleteTemplate: (p: string, id: string) =>
    apiClient.delete(`${base(p)}/templates/${id}`),
  issues: (p: string, params?: Record<string, string>) =>
    apiClient.get<CaseIssue[]>(`${base(p)}/issues`, { params }),
  saveIssue: (
    p: string,
    body: Omit<CaseIssue, "id" | "linkId">,
    id?: string,
  ) =>
    id
      ? apiClient.put<CaseIssue>(`${base(p)}/issues/${id}`, body)
      : apiClient.post<CaseIssue>(`${base(p)}/issues`, body),
  deleteIssue: (p: string, id: string) =>
    apiClient.delete(`${base(p)}/issues/${id}`),
  linkedIssues: (p: string, c: string) =>
    apiClient.get<CaseIssue[]>(`${base(p)}/cases/${c}/issues`),
  linkIssue: (p: string, c: string, issueId: string) =>
    apiClient.post(`${base(p)}/cases/${c}/issues`, { issueId }),
  unlinkIssue: (p: string, c: string, id: string) =>
    apiClient.delete(`${base(p)}/cases/${c}/issues/${id}`),
  relations: (p: string, c: string) =>
    apiClient.get<CaseRelation[]>(`${base(p)}/cases/${c}/relations`),
  relate: (p: string, c: string, targetCaseId: string, kind: string) =>
    apiClient.post(`${base(p)}/cases/${c}/relations`, { targetCaseId, kind }),
  unrelate: (p: string, c: string, id: string) =>
    apiClient.delete(`${base(p)}/cases/${c}/relations/${id}`),
  automationTargets: (p: string) =>
    apiClient.get<{
      cases: { id: string; name: string; type: string }[];
      suites: { id: string; name: string }[];
    }>(`${base(p)}/automation-targets`),
  automation: (p: string, c: string) =>
    apiClient.get<CaseAutomation[]>(`${base(p)}/cases/${c}/automation`),
  linkAutomation: (p: string, c: string, body: Omit<CaseAutomation, "id">) =>
    apiClient.post(`${base(p)}/cases/${c}/automation`, body),
  unlinkAutomation: (p: string, c: string, id: string) =>
    apiClient.delete(`${base(p)}/cases/${c}/automation/${id}`),
  followState: (p: string, c: string) =>
    apiClient.get<{ followed: boolean; count: number }>(
      `${base(p)}/cases/${c}/follow`,
    ),
  follow: (p: string, c: string, enabled: boolean) =>
    enabled
      ? apiClient.post(`${base(p)}/cases/${c}/follow`)
      : apiClient.delete(`${base(p)}/cases/${c}/follow`),
  comments: (p: string, c: string) =>
    apiClient.get<CaseComment[]>(`${base(p)}/cases/${c}/comments`),
  comment: (p: string, c: string, content: string, fileIds: string[] = []) =>
    apiClient.post<CaseComment>(`${base(p)}/cases/${c}/comments`, { content, fileIds }),
  deleteComment: (p: string, c: string, id: string) =>
    apiClient.delete(`${base(p)}/cases/${c}/comments/${id}`),
  attachments: (p: string, c: string) =>
    apiClient.get<CaseFile[]>(`${base(p)}/cases/${c}/attachments`),
  upload: (p: string, c: string, file: File) => {
    const data = new FormData();
    data.append("file", file);
    return apiClient.post<CaseFile>(`${base(p)}/cases/${c}/attachments`, data, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
  download: async (p: string, id: string) =>
    (
      await apiClient
        .getInstance()
        .get<Blob>(`${base(p)}/attachments/${id}/download`, {
          responseType: "blob",
        })
    ).data,
  deleteAttachment: (p: string, id: string) =>
    apiClient.delete(`${base(p)}/attachments/${id}`),
  recycle: (
    p: string,
    params: { page: number; size: number; search?: string; filters?: string; sort_by?: string; sort_order?: string },
  ) =>
    apiClient.get<{ items: TestCase[]; total: number }>(
      `${base(p)}/recycle-bin`,
      { params },
    ),
  restore: (p: string, id: string) =>
    apiClient.post<TestCase>(`${base(p)}/cases/${id}/restore`),
  purge: (p: string, id: string) =>
    apiClient.delete(`${base(p)}/cases/${id}/purge`),
  changes: (p: string, id: string) =>
    apiClient.get<CaseChange[]>(`${base(p)}/cases/${id}/changes`),
};
export function saveCaseBlob(blob: Blob, name: string) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = name;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
