import { apiClient } from "@/utils/api";
export interface PoolNode {
  id: string;
  name: string;
  enabled: boolean;
  online: boolean;
  capacity: number;
}
export interface ResourcePool {
  id: string;
  name: string;
  description: string;
  type: "Node";
  enabled: boolean;
  applications: ("api" | "scenario")[];
  allProjects: boolean;
  projectIds: string[];
  environmentIds: string[];
  nodes: PoolNode[];
  revision: number;
  capacity: {
    configured: number;
    online: number;
    running: number;
    available: number;
  };
}
export interface PoolInput {
  name: string;
  description: string;
  type: "Node";
  enabled: boolean;
  applications: ("api" | "scenario")[];
  allProjects: boolean;
  projectIds: string[];
  environmentIds: string[];
  expectedRevision: number;
  requestId?: string;
}
export interface PoolCatalog {
  items: ResourcePool[];
  total: number;
  page: number;
  size: number;
  canEdit: boolean;
  canDelete: boolean;
}
const base = "/resource-pools";
export const globalResourcePoolsApi = {
  list: (params: {
    projectId?: string;
    page: number;
    size: number;
    search?: string;
  }): Promise<PoolCatalog> => apiClient.get(base, { params }),
  nodes: (params: {
    page: number;
    size: number;
    search?: string;
  }): Promise<{
    items: PoolNode[];
    total: number;
    page: number;
    size: number;
  }> => apiClient.get(base + "/nodes", { params }),
  save: (
    body: PoolInput,
    id?: string,
  ): Promise<{ id: string; revision: number }> =>
    id ? apiClient.put(base + "/" + id, body) : apiClient.post(base, body),
  enabled: (id: string, enabled: boolean, expectedRevision: number) =>
    apiClient.put(base + "/" + id + "/enabled", { enabled, expectedRevision }),
  remove: (id: string, expectedRevision: number) =>
    apiClient.delete(base + "/" + id, { data: { expectedRevision } }),
};
