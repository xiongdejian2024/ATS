import type { TestCase } from "@/types";
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
  projectName: string;
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
  executionId?: string;
  executedBy?: string;
  executedAt?: string;
  precondition?: string;
  steps: { action: string; expected: string }[];
  caseEditType?: string;
  textDescription?: string;
  expectedResult?: string;
  description?: string;
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
  canExecute: boolean;
}
export interface PlanAssociateListing {
  items: (TestCase & { moduleName: string; alreadyLinked: boolean })[];
  total: number;
  page: number;
  size: number;
  modules: CaseFolder[];
  collections: CaseFolder[];
  counts: { all: number; unassigned: number };
  usesTree: boolean;
  suites: { id: string; name: string; caseIds: string[] }[];
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
  candidates: (id: string, params: Record<string, unknown>) =>
    apiClient.get<PlanAssociateListing>(base(id) + "/candidates", { params }),
  execute: (
    id: string,
    data: {
      requestId: string;
      selections: { source: string; id: string }[];
      result: string;
      description?: string;
      stepResults?: { index: number; result: string; actual?: string }[];
    },
  ) => apiClient.post(base(id) + "/execute", data),
  execution: (id: string, params: Record<string, unknown>) =>
    apiClient.get<PlanCaseExecutionDetail>(base(id) + "/execution", { params }),
  associate: (
    id: string,
    data: {
      category?: string;
      caseIds: string[];
      collectionId?: string | null;
      suiteId?: string | null;
    },
  ) => apiClient.post(base(id) + "/associate", data),
};

export interface PlanCaseExecutionRecord {
  id: string;
  result: string;
  description: string;
  executorName: string;
  createdAt: string;
  caseSnapshot: TestCase;
  stepResults: { index: number; result: string; actual: string }[];
}
export interface PlanCaseExecutionDetail {
  entry?: PlanCaseEntry;
  detached: boolean;
  canExecute: boolean;
  history: PlanCaseExecutionRecord[];
  total: number;
  page: number;
  size: number;
}
