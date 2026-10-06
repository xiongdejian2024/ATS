import { apiClient } from "@/utils/api";
import type { PlanNode } from "./planTree";
import type {
  PlanCaseEntry,
  PlanAssociation,
  CandidateSelection,
  CandidateSelectionPreview,
} from "./planCaseWorkspace";
import type { ExecutionCatalog, ExecutionConfig } from "./planExecutionConfig";
import type { PlanPolicy } from "./planOrchestration";
export type MinderCategory = PlanNode["category"];
export interface MinderWorkspace {
  fingerprint: string;
  policy: PlanPolicy;
  nodes: PlanNode[];
  entries: Record<MinderCategory, PlanCaseEntry[]>;
  executionCatalog: ExecutionCatalog;
  usesTree: boolean;
}
export interface MinderSave {
  expectedFingerprint: string;
  executionMode?: "serial" | "parallel";
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
  associations?: PlanAssociation[];
}
const base = (id: string) => `/plan-orchestration/plans/${id}/minder-workspace`;
export const planMinderApi = {
  load: (id: string): Promise<MinderWorkspace> => apiClient.get(base(id)),
  save: (id: string, data: MinderSave): Promise<MinderWorkspace> =>
    apiClient.put(base(id), data),
  previewCandidates: (
    id: string,
    draft: MinderSave,
    selection: CandidateSelection,
  ): Promise<CandidateSelectionPreview> =>
    apiClient.post(base(id) + "/candidates/selection", { draft, selection }),
};
