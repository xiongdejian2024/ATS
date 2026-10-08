import { apiClient } from "@/utils/api";
import type { CaseCustomField } from "./caseFeatures";
import type { LibraryFile } from "./fileLibrary";
export interface DefectCapabilities {
  canRead: boolean;
  canCreate: boolean;
  canUpdate: boolean;
  canDelete: boolean;
}
export interface DefectTemplate {
  id: string;
  name: string;
  fields: CaseCustomField[];
  defaults: { status?: string; description?: string; externalRef?: string };
  isDefault: boolean;
  revision: number;
}
export interface Defect {
  id: string;
  projectId: string;
  title: string;
  description: string;
  descriptionFormat: "plain" | "rich";
  status: "open" | "in_progress" | "resolved" | "closed";
  externalRef: string | null;
  templateId: string | null;
  customFields: Record<string, unknown>;
  archived: boolean;
  revision: number;
  createdAt: string;
  updatedAt: string;
  createdBy: string;
  updatedBy: string;
}
export interface DefectDetail extends Defect, DefectCapabilities {
  files: LibraryFile[];
}
export interface DefectInput {
  title: string;
  description: string;
  descriptionFormat: "plain" | "rich";
  status: Defect["status"];
  externalRef: string | null;
  templateId: string | null;
  customFields: Record<string, unknown>;
  fileIds: string[];
  expectedRevision: number;
  requestId?: string;
}
export interface DefectComment {
  id: string;
  authorId: string;
  content: string;
  createdAt: string;
  files: LibraryFile[];
  canDelete: boolean;
}
export interface DefectEvent {
  id: string;
  actorId: string;
  action: string;
  revision: number;
  detail: {
    snapshot: Defect;
    commentId?: string;
    content?: string;
    fileIds: string[];
  };
  createdAt: string;
  files: LibraryFile[];
}
export interface Page<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
}
const base = (p: string) => `/projects/${p}/defects`;
export const defectsApi = {
  list: (
    p: string,
    params: {
      page: number;
      size: number;
      search?: string;
      status?: string;
      archived: boolean;
    },
  ) => apiClient.get<Page<Defect> & DefectCapabilities>(base(p), { params }),
  detail: (p: string, id: string) =>
    apiClient.get<DefectDetail>(`${base(p)}/${id}`),
  save: (p: string, body: DefectInput, id?: string) =>
    id
      ? apiClient.put<{ id: string; revision: number }>(
          `${base(p)}/${id}`,
          body,
        )
      : apiClient.post<{ id: string; revision: number }>(base(p), body),
  archive: (
    p: string,
    id: string,
    archived: boolean,
    expectedRevision: number,
  ) =>
    apiClient.put<{ id: string; revision: number }>(
      `${base(p)}/${id}/archive`,
      { archived, expectedRevision },
    ),
  templates: (p: string) =>
    apiClient.get<{ items: DefectTemplate[] } & DefectCapabilities>(
      `${base(p)}/templates`,
    ),
  saveTemplate: (
    p: string,
    body: Omit<DefectTemplate, "id" | "revision"> & {
      expectedRevision: number;
    },
    id?: string,
  ) =>
    id
      ? apiClient.put<DefectTemplate>(`${base(p)}/templates/${id}`, body)
      : apiClient.post<DefectTemplate>(`${base(p)}/templates`, body),
  removeTemplate: (p: string, id: string, expectedRevision: number) =>
    apiClient.delete(`${base(p)}/templates/${id}`, {
      data: { expectedRevision },
    }),
  comments: (p: string, id: string, page: number) =>
    apiClient.get<Page<DefectComment>>(`${base(p)}/${id}/comments`, {
      params: { page },
    }),
  comment: (
    p: string,
    id: string,
    body: {
      content: string;
      fileIds: string[];
      expectedRevision: number;
      requestId: string;
    },
  ) =>
    apiClient.post<{ id: string; revision: number }>(
      `${base(p)}/${id}/comments`,
      body,
    ),
  removeComment: (
    p: string,
    id: string,
    cid: string,
    expectedRevision: number,
  ) =>
    apiClient.delete<{ id: string; revision: number }>(
      `${base(p)}/${id}/comments/${cid}`,
      { data: { expectedRevision } },
    ),
  history: (p: string, id: string, page: number) =>
    apiClient.get<Page<DefectEvent>>(`${base(p)}/${id}/history`, {
      params: { page },
    }),
};
