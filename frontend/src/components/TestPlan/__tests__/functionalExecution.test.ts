import { describe, expect, it } from "vitest";
import {
  nextFunctionalEntry,
  functionalListingState,
} from "../functionalExecution";
import type { PlanCaseEntry } from "@/api/planCaseWorkspace";
const row = (id: string, extra: Partial<PlanCaseEntry> = {}) =>
  ({ id, recycled: false, grouped: false, ...extra }) as PlanCaseEntry;
describe("功能用例提交后自动切换", () => {
  it("跳过回收和测试套成员，保持当前筛选顺序", () => {
    const items = [
      row("当前"),
      row("已回收", { recycled: true }),
      row("套成员", { grouped: true }),
      row("下一条"),
    ];
    expect(nextFunctionalEntry(items, "当前")?.id).toBe("下一条");
    expect(nextFunctionalEntry(items, "下一条")).toBeUndefined();
  });
  it("当前结果已从筛选中移除时，从剩余范围首条继续", () => {
    expect(
      nextFunctionalEntry(
        [row("回收", { recycled: true }), row("剩余")],
        "已通过的当前",
      )?.id,
    ).toBe("剩余");
    expect(nextFunctionalEntry([], "当前")).toBeUndefined();
  });
});

it("执行深链接保留筛选分页，非法分页排序回退安全默认值", () => {
  expect(
    functionalListingState({
      caseSearch: "诊断",
      casePage: "2",
      caseSize: "50",
      caseSort: "name",
      caseDirection: "asc",
      casePriority: "P1",
    }),
  ).toMatchObject({
    search: "诊断",
    page: 2,
    size: 50,
    sort: "name",
    direction: "asc",
    priority: "P1",
  });
  expect(
    functionalListingState({
      casePage: "NaN",
      caseSize: "10000",
      caseSort: "无效",
      caseDirection: "无效",
      caseSearch: ["重复参数"],
    }),
  ).toMatchObject({
    search: "",
    page: 1,
    size: 20,
    sort: "createdAt",
    direction: "desc",
  });
});
