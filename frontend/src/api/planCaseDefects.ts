import { apiClient } from "@/utils/api";
import type { CaseIssue } from "./caseFeatures";
import type { FunctionalMinderSelection } from "./planCaseWorkspace";
const base = (id: string) =>
  `/plan-orchestration/plans/${id}/case-workspace/defects`;
export type PlanInstanceDefect = CaseIssue & {
  linkId: string;
  associationKey: string;
  caseName: string;
  linkedAt: string;
};
export interface DefectPage<T = CaseIssue> {
  items: T[];
  total: number;
  page: number;
  size: number;
}
export interface DefectCapabilities {
  canAssociate: boolean;
  canCreate: boolean;
}
export const planCaseDefectsApi = {
  list: (id: string, params: Record<string, unknown>) =>
    apiClient.get<
      DefectPage<PlanInstanceDefect> &
        DefectCapabilities & { detached: boolean }
    >(base(id), { params }),
  candidates: (id: string, params: Record<string, unknown>) =>
    apiClient.get<DefectPage>(base(id) + "/candidates", { params }),
  preview: (id: string, scope: FunctionalMinderSelection) =>
    apiClient.post<DefectCapabilities & { count: number }>(
      base(id) + "/preview",
      scope,
    ),
  create: (
    id: string,
    data: FunctionalMinderSelection & {
      title: string;
      description: string;
      requestId: string;
    },
  ) => apiClient.post<{ updated: number }>(base(id), data),
  associate: (
    id: string,
    data: FunctionalMinderSelection & { issueIds: string[] },
  ) => apiClient.post<{ updated: number }>(base(id) + "/associate", data),
  unlink: (id: string, linkId: string) =>
    apiClient.delete(base(id) + "/" + linkId),
};
export const defectStatusLabels: Record<string, string> = {
  open: "待处理",
  in_progress: "处理中",
  resolved: "已解决",
  closed: "已关闭",
};
