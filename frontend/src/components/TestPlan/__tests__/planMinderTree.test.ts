import { describe, it, expect } from "vitest";
import { buildPlanMinder, presentPlanMinder } from "../planMinderTree";
import type { PlanCaseEntry } from "@/api/planCaseWorkspace";
import type { PlanNode } from "@/api/planTree";
import type {
  ExecutionConfig,
  ExecutionCatalog,
} from "@/api/planExecutionConfig";
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

describe("脑图环境与资源池真实配置", () => {
  it("分类根、默认测试集及实体测试集的请求环境与资源池不会混成执行节点", () => {
    const config: ExecutionConfig = {
      extended: false,
      executionMode: "parallel",
      testResourcePoolId: "pool",
      requestEnvironmentId: "target",
      stopOnFailure: false,
      retryOnFailure: true,
      retryTimes: 2,
      retryInterval: 100,
    };
    const catalog: ExecutionCatalog = {
      configurations: Object.fromEntries(
        ["root:api", "default:api", "node:api:api"].map((scope) => [
          scope,
          { scope, revision: 1, config, effectiveConfig: config },
        ]),
      ),
      pools: [
        {
          id: "pool",
          name: "自建执行池",
          environmentIds: ["agent"],
          revision: 1,
        },
      ],
      requestEnvironments: [{ id: "target", name: "请求目标环境" }],
      resources: [{ id: "agent", name: "执行Agent", enabled: true }],
    };
    const api = {
      ...point("api"),
      category: "api",
      effectiveConfig: { environmentId: "agent" },
    } as PlanNode;
    const tree = buildPlanMinder(
      "计划",
      [api],
      { functional: [], api: [entry(), entry("api")], scenario: [] },
      { executionCatalog: catalog, environmentNames: { agent: "执行Agent" } },
    );
    const category = tree.children![1];
    expect(category.executionMode).toBe("parallel");
    expect(category.children!.slice(0, 2).map((node) => node.name)).toEqual([
      "环境：请求目标环境",
      "资源池：自建执行池",
    ]);
    expect(category.children![2].executionMode).toBe("parallel");
    expect(category.children![3].executionMode).toBe("parallel");
    const ids: string[] = [];
    function walk(node: typeof tree) {
      ids.push(node.id);
      node.children?.forEach(walk);
    }
    walk(tree);
    expect(new Set(ids).size).toBe(ids.length);
    expect(category.children![0].configurationScope).toBe("root:api");
    expect(category.children![2].children![0].configurationScope).toBe(
      "default:api",
    );
    expect(JSON.stringify(category)).not.toContain("执行Agent");
    expect(category.count).toBe(2);
  });
  it("API测试集显示生效环境和执行方式，功能测试集没有配置叶子", () => {
    const api = {
      ...point("api"),
      category: "api",
      config: { environmentId: "own" },
      effectiveConfig: { environmentId: "actual", executionMode: "parallel" },
    } as PlanNode;
    const tree = buildPlanMinder(
      "计划",
      [point("functional"), api],
      { functional: [], api: [], scenario: [] },
      { environmentNames: { actual: "继承软件环境" } },
    );
    const collection = tree.children![1].children![0];
    expect(collection.executionMode).toBe("parallel");
    expect(collection.children!.map((child) => child.name)).toEqual([
      "0 条用例",
      "环境：继承软件环境",
      "资源池：默认资源池",
    ]);
    expect(
      tree.children![0].children![0].children!.map((child) => child.kind),
    ).toEqual(["count"]);
    expect(tree.count).toBe(0);
  });
  it("场景资源池以实际节点名称展示，未知节点使用可读文案且不泄露内部标识", () => {
    const scenario = {
      ...point("scenario"),
      category: "scenario",
      effectiveConfig: { resourcePool: ["first", "unknown-internal-id"] },
    } as PlanNode;
    const tree = buildPlanMinder(
      "计划",
      [scenario],
      { functional: [], api: [], scenario: [entry("scenario")] },
      { environmentNames: { first: "软件节点一" } },
    );
    const resource = tree.children![2].children![0].children!.find(
      (child) => child.kind === "resource",
    )!;
    expect(resource.name).toBe("资源池：软件节点一、已指定节点");
    expect(resource.nodeId).toBe("scenario");
    expect(resource.count).toBe(1);
    expect(tree.children![2].count).toBe(1);
  });
});
