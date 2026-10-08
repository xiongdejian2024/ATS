import type { WorkspaceViewApi } from "./planWorkspace";
import { apiClient } from "@/utils/api";
import type { ReportRun } from "./planCollaboration";
import type { GroupRun } from "./planGroup";

export type ReportKind = "PLAN" | "GROUP";
export interface PlanReportEntry {
  id: string;
  kind: ReportKind;
  sourceId: string;
  name: string;
  planName: string;
  status: string;
  resultStatus: string;
  passRate: number | null;
  triggerMode: "manual" | "cron";
  executorId: string;
  createUserName: string;
  createTime: string;
  completedAt?: string;
}
export type ReportDetail =
  | { kind: "PLAN"; name: string; payload: ReportRun }
  | { kind: "GROUP"; name: string; payload: GroupRun };
const base = (projectId: string) =>
  `/plan-orchestration/projects/${projectId}/reports`;
export const planReportsApi = {
  list: (projectId: string, params: Record<string, unknown>) =>
    apiClient.get<{
      items: PlanReportEntry[];
      total: number;
      canRename: boolean;
      canDelete: boolean;
    }>(base(projectId), { params }),
  detail: (projectId: string, kind: ReportKind, id: string) =>
    apiClient.get<ReportDetail>(`${base(projectId)}/${kind}/${id}`),
  rename: (projectId: string, row: PlanReportEntry, name: string) =>
    apiClient.put<{ name: string }>(
      `${base(projectId)}/${row.kind}/${row.id}/name`,
      { name },
    ),
  remove: (projectId: string, row: PlanReportEntry) =>
    apiClient.delete(`${base(projectId)}/${row.kind}/${row.id}`),
  batchRemove: (
    projectId: string,
    reports: { kind: ReportKind; id: string }[],
  ) => apiClient.post(`${base(projectId)}/batch-delete`, { reports }),
};
export const reportResultOptions = [
  { value: "passed", label: "成功" },
  { value: "failed", label: "失败" },
  { value: "cancelled", label: "已取消" },
  { value: "queued", label: "排队中" },
  { value: "running", label: "执行中" },
  { value: "cancelling", label: "取消中" },
  { value: "needs_confirmation", label: "待核对" },
  { value: "group_waiting", label: "等待前序计划" },
  { value: "skipped", label: "跳过" },
];
export const reportResultLabel = (value: string) =>
  reportResultOptions.find((item) => item.value === value)?.label ||
  { completed: "已完成" }[value] ||
  value;
export const reportResultColor = (value: string) =>
  ({
    passed: "success",
    failed: "error",
    running: "processing",
    queued: "processing",
    needs_confirmation: "warning",
  })[value] || "default";

export const reportIndexViewApi: WorkspaceViewApi = {
  listing: (projectId) => apiClient.get(`${base(projectId)}/views`),
  save: (projectId, name, filters) =>
    apiClient.post(`${base(projectId)}/views`, { name, filters }),
  update: (projectId, id, name, filters) =>
    apiClient.put(`${base(projectId)}/views/${id}`, {
      name,
      ...(filters === undefined ? {} : { filters }),
    }),
  remove: (projectId, id) => apiClient.delete(`${base(projectId)}/views/${id}`),
};
