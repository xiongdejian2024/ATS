import {
  effectiveConditions,
  type FilterCondition,
  type FilterLogic,
} from "./advancedFilter";

export interface CaseSearchScope {
  personalView: boolean;
  systemView: string;
  conditions: FilterCondition[];
  logic: FilterLogic;
  search: string;
  moduleKeys: string[];
  moduleIds: string[];
  priority?: string;
  status?: string;
  reviewStatus?: string;
  automated?: boolean;
}

export function isAdvancedCaseSearch(
  scope: Pick<CaseSearchScope, "personalView" | "systemView" | "conditions">,
) {
  return (
    scope.personalView ||
    scope.systemView !== "all" ||
    effectiveConditions(scope.conditions).length > 0
  );
}

// 列表与导出共享业务范围。分页、排序、选中编号由调用方单独附加。
export function caseSearchParams(scope: CaseSearchScope): Record<string, any> {
  const params: Record<string, any> = {
    mine: !scope.personalView && scope.systemView === "my",
    followed: !scope.personalView && scope.systemView === "followed",
  };
  if (isAdvancedCaseSearch(scope)) {
    const conditions = effectiveConditions(scope.conditions);
    if (conditions.length) params.filters = { conditions, logic: scope.logic };
    return params;
  }
  if (scope.search) params.search = scope.search;
  if (scope.moduleKeys.includes("unplanned")) params.moduleId = "null";
  else if (!scope.moduleKeys.includes("all") && scope.moduleIds.length)
    params.moduleIds = [...new Set(scope.moduleIds)].join(",");
  if (scope.priority) params.priority = scope.priority;
  if (scope.status) params.status = scope.status;
  if (scope.reviewStatus) params.review_status = scope.reviewStatus;
  if (scope.automated !== undefined) params.is_automated = scope.automated;
  return params;
}
