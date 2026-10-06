import { describe, it, expect } from "vitest";
import { planMinderActions } from "../planMinderActions";
import type { PlanMinderNode } from "../planMinderTree";
const node = (
  kind: PlanMinderNode["kind"],
  category: PlanMinderNode["category"] = "api",
): PlanMinderNode => ({ id: kind, name: kind, kind, category, count: 0 });
describe("MS规划节点菜单权限与继承", () => {
  it("分类根禁止关联和删除，功能分类只新增测试集", () => {
    expect(planMinderActions(node("category"), true, false)).toEqual([
      "add",
      "mode",
      "configure",
    ]);
    expect(
      planMinderActions(node("category", "functional"), true, false),
    ).toEqual(["add"]);
  });
  it("测试集继承时隐藏执行方式，功能集保留关联与配置", () => {
    expect(planMinderActions(node("collection"), true, true)).toEqual([
      "add",
      "associate",
      "configure",
      "delete",
    ]);
    expect(planMinderActions(node("collection"), true, false)).toContain(
      "mode",
    );
    expect(
      planMinderActions(node("collection", "functional"), true, false),
    ).toEqual(["add", "associate", "configure", "delete"]);
  });
  it("只读只能查看自动化配置，标签没有浮动操作", () => {
    expect(planMinderActions(node("collection"), false, false)).toEqual([
      "configure",
    ]);
    expect(
      planMinderActions(node("category", "functional"), false, false),
    ).toEqual([]);
    for (const kind of ["count", "environment", "resource"] as const)
      expect(planMinderActions(node(kind), true, false)).toEqual([]);
    expect(planMinderActions(node("root"), true, false)).toEqual(["mode"]);
    expect(planMinderActions(node("root"), false, false)).toEqual([]);
  });
});
