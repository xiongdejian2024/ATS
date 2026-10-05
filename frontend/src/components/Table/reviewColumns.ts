import type { DisplayColumn } from "./tableDisplay";
export const reviewColumns = [
  { key: "number", title: "ID", width: 100, required: true, sorter: true },
  { key: "name", title: "评审名称", width: 200, required: true, sorter: true },
  { key: "caseCount", title: "用例数量", width: 100 },
  { key: "lifecycle", title: "评审状态", width: 150 },
  { key: "passRate", title: "通过率", width: 200 },
  { key: "mode", title: "模式", width: 100 },
  { key: "reviewers", title: "评审人", width: 150 },
  { key: "creator", title: "创建人", width: 120 },
  { key: "moduleName", title: "所属模块", width: 120 },
  { key: "tags", title: "标签", width: 170 },
  { key: "description", title: "描述", width: 150 },
  { key: "period", title: "周期", width: 350 },
  { key: "createdAt", title: "创建时间", width: 180, sorter: true },
];
export const reviewDefinitions: DisplayColumn[] = reviewColumns;
export const reviewStates = [
  { value: "prepared", label: "未开始" },
  { value: "underway", label: "进行中" },
  { value: "completed", label: "已完成" },
  { value: "archived", label: "已归档" },
  { value: "cancelled", label: "已取消" },
  { value: "superseded", label: "已重新提审" },
];
export function reviewStateName(value: string) {
  return reviewStates.find((s) => s.value === value)?.label || value;
}
