import { describe, it, expect } from "vitest";
import { buildPlanMinder, presentPlanMinder } from "../planMinderTree";
import type { PlanCaseEntry } from "@/api/planCaseWorkspace";
import type { PlanNode } from "@/api/planTree";
const entry = (collectionId?: string) => ({ collectionId }) as PlanCaseEntry;
const point = (id: string, parentId?: string) =>
  ({
    id,
    parentId,
    name: id,
    nodeType: "point",
    category: "functional",
    position: 0,
  }) as PlanNode;
describe("测试规划脑图实际关联范围", () => {
  it("父测试集汇总下级数量，同一用例的两个关联仍按两个实例统计", () => {
    const tree = buildPlanMinder(
      "计划",
      [point("parent"), point("child", "parent")],
      {
        functional: [entry("child"), entry("child"), entry()],
        api: [],
        scenario: [],
      },
    );
    expect(tree.count).toBe(3);
    expect(tree.children).toHaveLength(3);
    const functional = tree.children![0];
    expect(functional.children![0].name).toBe("默认测试集");
    expect(functional.children![1].count).toBe(2);
    expect(functional.children![1].children![1].count).toBe(2);
    expect(tree.children![1].name).toBe("API 用例 (0)");
  });
  it("混合分类测试点保留公共父链，分类统计互不混入", () => {
    const tree = buildPlanMinder(
      "计划",
      [point("parent"), point("child", "parent")],
      { functional: [entry()], api: [entry("child")], scenario: [] },
    );
    expect(tree.children![1].children![0].nodeId).toBe("parent");
    expect(tree.children![1].children![0].count).toBe(1);
    expect(tree.children![0].count).toBe(1);
  });
  it("旧数据异常父链不会无限递归或丢失关联数量", () => {
    const tree = buildPlanMinder("计划", [point("a", "b"), point("b", "a")], {
      functional: [entry("a"), entry("b"), entry("missing")],
      api: [],
      scenario: [],
    });
    expect(() => JSON.stringify(tree)).not.toThrow();
    expect(tree.count).toBe(3);
    expect(
      tree.children![0].children!.reduce((sum, node) => sum + node.count, 0),
    ).toBe(3);
  });
});

describe("脑图折叠与数据保留", () => {
  it("隐藏测试集不丢失统计，展开可恢复原关联，且不修改原树", () => {
    const tree = buildPlanMinder(
      "计划",
      [point("parent"), point("child", "parent")],
      { functional: [entry("child"), entry()], api: [], scenario: [] },
    );
    const folded = presentPlanMinder(tree, new Set(["category:functional"]));
    expect(folded.children![0].children).toBeUndefined();
    expect(folded.children![0].count).toBe(2);
    expect(tree.children![0].children).toHaveLength(2);
    expect(presentPlanMinder(tree, new Set())).toEqual(tree);
  });
});
