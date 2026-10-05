import { describe, it, expect } from "vitest";
import {
  caseSearchParams,
  isAdvancedCaseSearch,
  type CaseSearchScope,
} from "./caseSearchScope";
const scope: CaseSearchScope = {
  personalView: false,
  systemView: "all",
  conditions: [],
  logic: "and",
  search: "旧关键字",
  moduleKeys: ["父模块"],
  moduleIds: ["父模块", "子模块", "子模块"],
  priority: "P0",
  status: "passed",
  reviewStatus: "approved",
  automated: false,
};
describe("用例列表和导出的检索范围", () => {
  it("基础检索保留模块、列筛选和否自动化，重复模块去重", () => {
    expect(caseSearchParams(scope)).toEqual({
      mine: false,
      followed: false,
      search: "旧关键字",
      moduleIds: "父模块,子模块",
      priority: "P0",
      status: "passed",
      review_status: "approved",
      is_automated: false,
    });
    expect(
      caseSearchParams({ ...scope, moduleKeys: ["unplanned"] }).moduleId,
    ).toBe("null");
  });
  it("高级OR只使用显式条件，忽略隐藏的关键词、模块和列筛选", () => {
    const conditions = [
      { field: "tags", operator: "count_gt", value: 0 },
      { field: "isAutomated", operator: "equals", value: false },
    ];
    const advanced = { ...scope, conditions, logic: "or" as const };
    expect(caseSearchParams(advanced)).toEqual({
      mine: false,
      followed: false,
      filters: { conditions, logic: "or" },
    });
    expect(isAdvancedCaseSearch(advanced)).toBe(true);
  });
  it("我创建的与关注视图始终使用项目范围，零条件个人视图也是高级模式", () => {
    expect(caseSearchParams({ ...scope, systemView: "my" })).toEqual({
      mine: true,
      followed: false,
    });
    expect(caseSearchParams({ ...scope, systemView: "followed" })).toEqual({
      mine: false,
      followed: true,
    });
    expect(caseSearchParams({ ...scope, personalView: true })).toEqual({
      mine: false,
      followed: false,
    });
    expect(isAdvancedCaseSearch({ ...scope, personalView: true })).toBe(true);
    expect(
      caseSearchParams({ ...scope, personalView: true, systemView: "my" }),
    ).toEqual({ mine: false, followed: false });
  });
  it("未填写的系统默认行仍保持基础模式，空值运算和显式模块条件可跨左侧模块检索", () => {
    expect(
      isAdvancedCaseSearch({
        ...scope,
        conditions: [{ field: "name", operator: "contains", value: "" }],
      }),
    ).toBe(false);
    const conditions = [
      { field: "moduleId", operator: "belongs_to", value: ["另一模块"] },
      { field: "precondition", operator: "is_empty" },
    ];
    expect(caseSearchParams({ ...scope, conditions })).toEqual({
      mine: false,
      followed: false,
      filters: { conditions, logic: "and" },
    });
  });
});
