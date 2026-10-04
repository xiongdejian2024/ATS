import { apiClient } from "@/utils/api";
import type { TestCase } from "@/types";
export interface NodeConfig {
  executionMode?: "serial" | "parallel" | null;
  environmentId?: string | null;
  resourcePool?: string[] | null;
}
export interface PlanNode {
  id: string;
  planId: string;
  parentId?: string | null;
  name: string;
  nodeType: "point" | "case" | "suite";
  category: "functional" | "api" | "scenario";
  caseId?: string | null;
  suiteId?: string | null;
  assignedTo?: string | null;
  linkedFunctionalId?: string | null;
  position: number;
  config: NodeConfig;
  effectiveConfig: NodeConfig;
  case?: TestCase;
}
const base = "/plan-orchestration";
export const planTreeApi = {
  list: (id: string): Promise<PlanNode[]> =>
    apiClient.get(`${base}/plans/${id}/nodes`),
  create: (id: string, data: Partial<PlanNode>): Promise<PlanNode> =>
    apiClient.post(`${base}/plans/${id}/nodes`, data),
  update: (id: string, data: Partial<PlanNode>): Promise<PlanNode> =>
    apiClient.put(`${base}/nodes/${id}`, data),
  remove: (id: string) => apiClient.delete(`${base}/nodes/${id}`),
  assign: (id: string, nodeIds: string[], assignedTo?: string) =>
    apiClient.post(`${base}/plans/${id}/nodes/assign`, {
      nodeIds,
      assignedTo: assignedTo || null,
    }),
  executors: (id: string): Promise<{ id: string; name: string }[]> =>
    apiClient.get(`${base}/plans/${id}/executors`),
};
