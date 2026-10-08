import {
  normalizeDisplay,
  pageSizes,
  type DisplayColumn,
} from "./tableDisplay";
export const reportPageSizes = [...pageSizes, 100];
export const reportColumnDefinitions: DisplayColumn[] = [
  { key: "name", title: "报告名称", required: true },
  { key: "kind", title: "报告类型" },
  { key: "planName", title: "所属计划" },
  { key: "resultStatus", title: "结果" },
  { key: "passRate", title: "通过率" },
  { key: "triggerMode", title: "触发方式" },
  { key: "createUserName", title: "操作人" },
  { key: "createTime", title: "操作时间" },
  { key: "operation", title: "操作" },
];
export function normalizeReportDisplay(value: unknown) {
  const result = normalizeDisplay(value, reportColumnDefinitions);
  if (
    value &&
    typeof value === "object" &&
    (value as { pageSize?: number }).pageSize === 100
  )
    result.pageSize = 100;
  return result;
}
export function readReportDisplay(
  storage: Pick<Storage, "getItem">,
  key: string,
) {
  try {
    return normalizeReportDisplay(JSON.parse(storage.getItem(key) || "null"));
  } catch (error) {
    console.error("读取报告显示配置失败，使用默认显示", error);
    return normalizeReportDisplay(undefined);
  }
}
export const reportColumnCatalog = [
  { title: "报告名称", dataIndex: "name", key: "name", width: 200 },
  { title: "报告类型", key: "kind", width: 150 },
  {
    title: "所属计划",
    dataIndex: "planName",
    key: "planName",
    width: 200,
    ellipsis: true,
  },
  { title: "结果", key: "resultStatus", width: 150, sorter: true },
  { title: "通过率", key: "passRate", width: 200, sorter: true },
  { title: "触发方式", key: "triggerMode", width: 150 },
  {
    title: "操作人",
    dataIndex: "createUserName",
    key: "createUserName",
    width: 300,
    ellipsis: true,
  },
  {
    title: "操作时间",
    key: "createTime",
    width: 180,
    sorter: true,
    defaultSortOrder: "descend" as const,
  },
  { title: "操作", key: "operation", width: 130, fixed: "right" as const },
];
