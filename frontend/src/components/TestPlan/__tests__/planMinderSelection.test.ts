import { describe, it, expect } from "vitest";
import { minderDeletionTargets, intersects } from "../planMinderSelection";
import type { PlanMinderNode } from "../planMinderTree";
import type { PlanNode } from "@/api/planTree";
const point = (id: string, category = "api", parentId: string | null = null) =>
  ({ id, nodeType: "point", category, parentId }) as PlanNode;
const collection = (
  nodeId?: string,
  category: PlanMinderNode["category"] = "api",
): PlanMinderNode => ({
  id: nodeId || `default:${category}`,
  nodeId,
  category,
  name: "测试集",
  kind: "collection",
  count: 1,
});
describe("脑图多选删除范围", () => {
  it("默认集与跨分类实体集可一起删除，重复选择去重", () => {
    const points = [point("a"), point("b", "scenario")];
    expect(
      minderDeletionTargets(
        [
          collection(),
          collection("a"),
          collection("a"),
          collection("b", "scenario"),
        ],
        points,
        true,
      ),
    ).toEqual([
      { nodeId: undefined, category: "api" },
      { nodeId: "a", category: "api" },
      { nodeId: "b", category: "scenario" },
    ]);
  });
  it("父子同时选择只删除父根，仍接受合法旧跨分类子集", () => {
    const points = [
      point("p", "functional"),
      point("c", "api", "p"),
      point("leaf", "api", "c"),
    ];
    expect(
      minderDeletionTargets(
        [collection("leaf"), collection("p", "functional"), collection("c")],
        points,
        true,
      ),
    ).toEqual([{ nodeId: "p", category: "functional" }]);
  });
  it("混入标签或分类、只读、丢失节点与旧公共集投影均整批禁用", () => {
    for (const kind of [
      "root",
      "category",
      "count",
      "environment",
      "resource",
    ] as const)
      expect(
        minderDeletionTargets(
          [collection(), { ...collection(), id: kind, kind }],
          [],
          true,
        ),
      ).toBeUndefined();
    expect(minderDeletionTargets([collection()], [], false)).toBeUndefined();
    expect(
      minderDeletionTargets([collection("missing")], [], true),
    ).toBeUndefined();
    expect(
      minderDeletionTargets(
        [collection("old")],
        [point("old", "functional")],
        true,
      ),
    ).toBeUndefined();
    expect(minderDeletionTargets([], [], true)).toBeUndefined();
  });
  it("框选按实际可见缩放盒的相交面积判定，不要求完全包住节点", () => {
    const region = { left: 20, top: 20, right: 60, bottom: 60 };
    expect(
      intersects(region, { left: 50, top: 50, right: 100, bottom: 90 }),
    ).toBe(true);
    expect(
      intersects(region, { left: 60, top: 20, right: 80, bottom: 40 }),
    ).toBe(false);
    expect(intersects(region, { left: 0, top: 0, right: 10, bottom: 10 })).toBe(
      false,
    );
  });
});
