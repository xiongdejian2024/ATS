import type { TestCase } from "@/types";
import { apiClient } from "@/utils/api";
export interface PlanCaseEntry {
  nativeState?: string | null;
  protocol?: string | null;
  path?: string | null;
  environmentName?: string | null;
  environmentLabel?: string | null;
  stepTotal?: number | null;
  nativeResult?: string;
  nativeExecutorId?: string | null;
  nativeExecutorName?: string;
  nativeExecutionEnvironmentName?: string | null;
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
  steps: { step?: number; action: string; expected: string }[];
  caseEditType?: string;
  textDescription?: string;
  expectedResult?: string;
  description?: string;
}
export interface CaseFolder {
  category?: "functional" | "api" | "scenario";
  nodeType?: "PROJECT" | "DEFAULT";
  projectId?: string;
  id: string;
  name: string;
  parentId?: string;
  count: number;
}
export interface PlanCaseListing {
  nativeOptions?: import("./nativeCase").NativeFilterCatalog;
  items: PlanCaseEntry[];
  total: number;
  selectableTotal?: number;
  page: number;
  size: number;
  collections: CaseFolder[];
  modules: CaseFolder[];
  counts: { all: number; default: number; unassigned: number };
  usesTree: boolean;
  canExecute: boolean;
  projects?: { id: string; name: string }[];
}
export type PlanCandidateRow = Pick<TestCase, "id" | "name"> &
  Partial<TestCase> & {
    moduleName: string;
    alreadyLinked: boolean;
    method?: string | null;
    caseTotal?: number;
    createdByName?: string | null;
  };
export interface PlanAssociateListing {
  basicOptions?: {
    protocols: string[];
    creators: { value: string; text: string }[];
  };
  syncCollections: { api: CaseFolder[]; scenario: CaseFolder[] };
  projectId: string;
  projectName: string;
  plans: { id: string; name: string }[];
  items: PlanCandidateRow[];
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
  protocols?: string[];
  methods?: string[];
  createdBy?: string[];
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
  resourceType?: "CASE" | "API";
  definitionIds?: string[];
  syncCase?: boolean;
  apiCaseCollectionId?: string;
  apiScenarioCollectionId?: string;
  projectId?: string;
  category: "functional" | "api" | "scenario";
  selectAll?: boolean;
  caseIds?: string[];
  excludeIds?: string[];
  condition?: CandidateCondition;
  moduleMaps?: Record<string, CandidateModuleSelection>;
}
export interface CandidateSelectionPreview {
  selectedDefinitionCount?: number;
  sync?: Record<
    "api" | "scenario",
    { count: number; compatibleSuiteIds: string[] }
  >;
  moduleCounts?: Record<string, { total: number; selected: number }>;
  eligibleCount?: number;
  count: number;
  excludedCount: number;
  automatedCount: number;
  requiresSuiteCount?: number;
  usesTree: boolean;
  compatibleSuiteIds: string[];
  canAssociate: boolean;
}
export interface PlanAssociation extends CandidateSelection {
  collectionId?: string | null;
  suiteId?: string | null;
  syncApiSuiteId?: string | null;
  syncScenarioSuiteId?: string | null;
}
export interface NativeWorkspaceCondition {
  tree_type?: "COLLECTION" | "MODULE";
  folder?: string;
  search?: string;
  include_descendants?: boolean;
  protocols?: string;
  priority?: string;
  result?: string;
  filters?: CandidateCondition["filters"];
  mine?: boolean;
}
export interface NativeWorkspaceSelection {
  category: "api" | "scenario";
  selectAll?: boolean;
  selectIds?: string[];
  excludeIds?: string[];
  condition?: NativeWorkspaceCondition;
}
export interface NativeWorkspacePreview {
  count: number;
  eligibleCount: number;
  excludedCount: number;
  canModify: boolean;
  canExecute?: boolean;
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
    resourceType: "CASE" | "API" = "CASE",
  ) =>
    apiClient.get<PlanCaseSavedView[]>(viewBase(id, mode), {
      params: {
        category,
        ...(mode === "association"
          ? { projectId, ...(resourceType === "API" ? { resourceType } : {}) }
          : {}),
      },
    }),
  saveView: (
    id: string,
    name: string,
    filters: PlanCaseSavedView["filters"],
    category = "functional",
    mode: PlanFilterMode = "workspace",
    projectId?: string,
    resourceType: "CASE" | "API" = "CASE",
  ) =>
    apiClient.post<PlanCaseSavedView>(
      viewBase(id, mode),
      { name, filters },
      {
        params: {
          category,
          ...(mode === "association"
            ? { projectId, ...(resourceType === "API" ? { resourceType } : {}) }
            : {}),
        },
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
    resourceType: "CASE" | "API" = "CASE",
  ) =>
    apiClient.put<PlanCaseSavedView>(
      viewBase(id, mode) + "/" + view,
      {
        name,
        ...(filters === undefined ? {} : { filters }),
      },
      {
        params: {
          category,
          ...(mode === "association"
            ? { projectId, ...(resourceType === "API" ? { resourceType } : {}) }
            : {}),
        },
      },
    ),
  deleteView: (
    id: string,
    view: string,
    category = "functional",
    mode: PlanFilterMode = "workspace",
    projectId?: string,
    resourceType: "CASE" | "API" = "CASE",
  ) =>
    apiClient.delete(viewBase(id, mode) + "/" + view, {
      params: {
        category,
        ...(mode === "association"
          ? { projectId, ...(resourceType === "API" ? { resourceType } : {}) }
          : {}),
      },
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
  previewNativeSelection: (id: string, data: NativeWorkspaceSelection) =>
    apiClient.post<NativeWorkspacePreview>(base(id) + "/selection", data),
  runNativeRange: (
    id: string,
    data: NativeWorkspaceSelection & { requestId: string },
  ) =>
    apiClient.post<import("./planOrchestration").PlanRun>(
      base(id) + "/run-range",
      data,
    ),
  nativeBatch: (
    id: string,
    data: NativeWorkspaceSelection & {
      action: "move" | "unlink";
      collectionId?: string | null;
    },
  ) => apiClient.post<{ updated: number }>(base(id) + "/batch-range", data),
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
  associate: (id: string, data: PlanAssociation) =>
    apiClient.post(base(id) + "/associate", data),
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
  canReadCase: boolean;
  canEditCase: boolean;
  entry?: PlanCaseEntry;
  detached: boolean;
  canExecute: boolean;
  history: PlanCaseExecutionRecord[];
  total: number;
  page: number;
  size: number;
}

export interface FunctionalMinderSelection {
  category?: "functional";
  selectAll?: boolean;
  selectIds?: string[];
  excludeIds?: string[];
  condition?: {
    tree_type?: "COLLECTION" | "MODULE";
    folder?: string;
    folderIds?: string[];
    entryIds?: string[];
    include_descendants?: boolean;
    search?: string;
    priority?: string;
    result?: string;
    executor?: string;
    tag?: string;
    filters?: {
      conditions: import("@/components/TestCase/advancedFilter").FilterCondition[];
      logic: "and" | "or";
    };
    mine?: boolean;
  };
}
export const functionalMinderApi = {
  preview: (id: string, data: FunctionalMinderSelection) =>
    apiClient.post<{
      count: number;
      eligibleCount: number;
      excludedCount: number;
      canExecute: boolean;
    }>(base(id) + "/minder-preview", data),
  execute: (
    id: string,
    data: FunctionalMinderSelection & {
      requestId: string;
      result: string;
      description: string;
    },
  ) =>
    apiClient.post<{ updated: number; replayed: boolean }>(
      base(id) + "/minder-execute",
      data,
    ),
};
export const functionalMinderBatch = (
  id: string,
  data: FunctionalMinderSelection & {
    action: "assign" | "unlink";
    assignedTo?: string | null;
  },
) => apiClient.post<{ updated: number }>(base(id) + "/minder-batch", data);

export const functionalMinderBatchPreview = (
  id: string,
  data: FunctionalMinderSelection & { action: "assign" | "unlink" },
) =>
  apiClient.post<{ count: number; canModify: boolean }>(
    base(id) + "/minder-batch/preview",
    data,
  );
