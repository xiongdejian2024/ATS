import { apiClient } from "@/utils/api";
export interface PlanCaseEntry {
  id: string;
  source: "legacy" | "node";
  associationId: string;
  caseId: string;
  name: string;
  caseCode: string;
  priority: string;
  tags: string[];
  collectionId?: string;
  collectionName: string;
  moduleId?: string;
  moduleName: string;
  createdAt: string;
  updatedAt: string;
  createdByName: string;
  assignedTo?: string;
  executorName: string;
  isAutomated: boolean;
  recycled: boolean;
  result: string;
  bugCount: number;
  runId?: string;
  grouped: boolean;
  precondition?: string;
  steps: { action: string; expected: string }[];
  caseEditType?: string;
  textDescription?: string;
  expectedResult?: string;
}
export interface CaseFolder {
  id: string;
  name: string;
  parentId?: string;
  count: number;
}
export interface PlanCaseListing {
  items: PlanCaseEntry[];
  total: number;
  page: number;
  size: number;
  collections: CaseFolder[];
  modules: CaseFolder[];
  counts: { all: number; default: number; unassigned: number };
  usesTree: boolean;
}
const base = (id: string) => `/plan-orchestration/plans/${id}/case-workspace`;
export const planCaseWorkspaceApi = {
  list: (id: string, params: Record<string, unknown>) =>
    apiClient.get<PlanCaseListing>(base(id), { params }),
  batch: (
    id: string,
    data: {
      category?: string;
      action: "assign" | "move" | "unlink";
      selections: { source: string; id: string }[];
      assignedTo?: string | null;
      collectionId?: string | null;
    },
  ) => apiClient.post(base(id) + "/batch", data),
  associate: (
    id: string,
    data: { caseIds: string[]; collectionId?: string; suiteId?: string },
  ) => apiClient.post(base(id) + "/associate", data),
};
