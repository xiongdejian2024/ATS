import type { PlanCaseEntry } from "@/api/planCaseWorkspace";
export const functionalResults = [
  { value: "passed", label: "通过" },
  { value: "failed", label: "失败" },
  { value: "blocked", label: "阻塞" },
];
export const functionalResultLabels: Record<string, string> = {
  pending: "未执行",
  passed: "通过",
  failed: "失败",
  blocked: "阻塞",
  error: "错误",
  skipped: "跳过",
  cancelled: "已取消",
};
export function nextFunctionalEntry(
  items: PlanCaseEntry[],
  currentId: string,
): PlanCaseEntry | undefined {
  const index = items.findIndex((item) => item.id === currentId);
  return items.slice(index + 1).find((item) => !item.recycled && !item.grouped);
}

/** 执行详情与返回列表共用范围，深链接参数只接受合法分页和排序。 */
export function functionalListingState(query: Record<string, unknown>) {
  const value = (key: string) =>
    typeof query[key] === "string" ? (query[key] as string) : "";
  const integer = (key: string, fallback: number, max: number) => {
    const number = Number(value(key));
    return Number.isInteger(number) && number > 0 && number <= max
      ? number
      : fallback;
  };
  return {
    search: value("caseSearch"),
    priority: ["P0", "P1", "P2", "P3"].includes(value("casePriority"))
      ? value("casePriority")
      : undefined,
    result: value("caseResult") || undefined,
    executor: value("caseExecutor") || undefined,
    tag: value("caseTag"),
    page: integer("casePage", 1, 1000000),
    size: integer("caseSize", 20, 100),
    sort: [
      "caseCode",
      "name",
      "priority",
      "createdAt",
      "updatedAt",
      "result",
    ].includes(value("caseSort"))
      ? value("caseSort")
      : "createdAt",
    direction: value("caseDirection") === "asc" ? "asc" : "desc",
    advanced: value("caseAdvanced") === "1",
    filters:
      typeof query.caseFilters === "string"
        ? query.caseFilters || undefined
        : query.caseFilters == null
          ? undefined
          : JSON.stringify(query.caseFilters),
    viewId: value("caseViewId") || undefined,
    includeDescendants: value("caseIncludeDescendants") !== "0",
  };
}
