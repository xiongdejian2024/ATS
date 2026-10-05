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
  projectId: string;
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
  nodeType?: "PROJECT" | "DEFAULT";
  projectId?: string;
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
  projects?: { id: string; name: string }[];
}
export interface PlanAssociateListing {
  projectId: string;
  projectName: string;
  plans: { id: string; name: string }[];
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
export interface CandidateCondition {
  search?: string;
  folder?: string;
  priority?: string;
  filters?: {
    conditions: import("@/components/TestCase/advancedFilter").FilterCondition[];
    logic: "and" | "or";
  };
  mine?: boolean;
}
export interface CandidateModuleSelection {
  selectAll: boolean;
  selectIds: string[];
  excludeIds: string[];
}
export interface CandidateSelection {
  projectId?: string;
  category: "functional" | "api" | "scenario";
  selectAll?: boolean;
  caseIds?: string[];
  excludeIds?: string[];
  condition?: CandidateCondition;
  moduleMaps?: Record<string, CandidateModuleSelection>;
}
export interface CandidateSelectionPreview {
  moduleCounts?: Record<string, { total: number; selected: number }>;
  eligibleCount?: number;
  count: number;
  excludedCount: number;
  automatedCount: number;
  usesTree: boolean;
  compatibleSuiteIds: string[];
  canAssociate: boolean;
}
const base = (id: string) => `/plan-orchestration/plans/${id}/case-workspace`;
export type PlanFilterMode = "workspace" | "association";
const viewBase = (id: string, mode: PlanFilterMode) =>
  base(id) + (mode === "association" ? "/candidates/views" : "/views");
export interface PlanCaseSavedView {
  id: string;
  name: string;
  filters: {
    filterConditions?: import("@/components/TestCase/advancedFilter").FilterCondition[];
    filterLogic?: "and" | "or";
  };
}
export const planCaseWorkspaceApi = {
  list: (id: string, params: Record<string, unknown>) =>
    apiClient.get<PlanCaseListing>(base(id), { params }),
  views: (
    id: string,
    category = "functional",
    mode: PlanFilterMode = "workspace",
    projectId?: string,
  ) =>
    apiClient.get<PlanCaseSavedView[]>(viewBase(id, mode), {
      params: { category, ...(mode === "association" ? { projectId } : {}) },
    }),
  saveView: (
    id: string,
    name: string,
    filters: PlanCaseSavedView["filters"],
    category = "functional",
    mode: PlanFilterMode = "workspace",
    projectId?: string,
  ) =>
    apiClient.post<PlanCaseSavedView>(
      viewBase(id, mode),
      { name, filters },
      {
        params: { category, ...(mode === "association" ? { projectId } : {}) },
      },
    ),
  updateView: (
    id: string,
    view: string,
    name: string,
    filters?: PlanCaseSavedView["filters"],
    category = "functional",
    mode: PlanFilterMode = "workspace",
    projectId?: string,
  ) =>
    apiClient.put<PlanCaseSavedView>(
      viewBase(id, mode) + "/" + view,
      {
        name,
        ...(filters === undefined ? {} : { filters }),
      },
      {
        params: { category, ...(mode === "association" ? { projectId } : {}) },
      },
    ),
  deleteView: (
    id: string,
    view: string,
    category = "functional",
    mode: PlanFilterMode = "workspace",
    projectId?: string,
  ) =>
    apiClient.delete(viewBase(id, mode) + "/" + view, {
      params: { category, ...(mode === "association" ? { projectId } : {}) },
    }),
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
  candidateProjects: (id: string) =>
    apiClient.get<{ id: string; name: string }[]>(
      base(id) + "/candidates/projects",
    ),
  candidates: (id: string, params: Record<string, unknown>) =>
    apiClient.get<PlanAssociateListing>(base(id) + "/candidates", { params }),
  previewCandidates: (id: string, data: CandidateSelection) =>
    apiClient.post<CandidateSelectionPreview>(
      base(id) + "/candidates/selection",
      data,
    ),
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
    data: CandidateSelection & {
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
