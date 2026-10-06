import { apiClient } from "@/utils/api";
import type { PlanNode } from "./planTree";
import type { PlanCaseEntry } from "./planCaseWorkspace";
import type { ExecutionCatalog, ExecutionConfig } from "./planExecutionConfig";
export type MinderCategory = PlanNode["category"];
export interface MinderWorkspace {
  fingerprint: string;
  nodes: PlanNode[];
  entries: Record<MinderCategory, PlanCaseEntry[]>;
  executionCatalog: ExecutionCatalog;
  usesTree: boolean;
}
export interface MinderSave {
  expectedFingerprint: string;
  points: {
    id: string;
    name: string;
    category: MinderCategory;
    parentId: string | null;
    position: number;
    materializeDefault?: MinderCategory;
  }[];
  deleteDefaults: MinderCategory[];
  configurations: Record<
    string,
    { config: ExecutionConfig; expectedRevision: number }
  >;
}
const base = (id: string) => `/plan-orchestration/plans/${id}/minder-workspace`;
export const planMinderApi = {
  load: (id: string): Promise<MinderWorkspace> => apiClient.get(base(id)),
  save: (id: string, data: MinderSave): Promise<MinderWorkspace> =>
    apiClient.put(base(id), data),
};
