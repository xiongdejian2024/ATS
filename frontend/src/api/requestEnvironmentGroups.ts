import { apiClient } from "@/utils/api";
export interface EnvironmentMapping {
  projectId: string;
  environmentId: string;
}
export interface EnvironmentGroup {
  id: string;
  name: string;
  description: string;
  revision: number;
  mappings: EnvironmentMapping[];
}
export interface GroupInput {
  name: string;
  description: string;
  expectedRevision: number;
  requestId?: string;
  mappings: EnvironmentMapping[];
}
export interface GroupCatalog {
  items: EnvironmentGroup[];
  total: number;
  page: number;
  size: number;
  canEdit: boolean;
  canDelete: boolean;
}
const base = (project: string) =>
  `/projects/${project}/request-environment-groups`;
export const requestEnvironmentGroupsApi = {
  list: (
    project: string,
    params: { page: number; size: number; search?: string },
  ): Promise<GroupCatalog> => apiClient.get(base(project), { params }),
  sources: (project: string): Promise<{ id: string; name: string }[]> =>
    apiClient.get(`${base(project)}/source-environments`),
  save: (
    project: string,
    input: GroupInput,
    id?: string,
  ): Promise<{ id: string; revision: number }> =>
    id
      ? apiClient.put(`${base(project)}/${id}`, input)
      : apiClient.post(base(project), input),
  remove: (project: string, id: string, revision: number) =>
    apiClient.delete(`${base(project)}/${id}`, {
      data: { expectedRevision: revision },
    }),
};
