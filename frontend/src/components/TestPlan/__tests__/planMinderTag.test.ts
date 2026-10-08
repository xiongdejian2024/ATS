import { describe, it, expect } from "vitest";
import {
  planMinderTag,
  executionEnvironmentOptions,
  executionPoolOptions,
  executionPoolValue,
  selectExecutionPool,
} from "../planMinderTag";
import type {
  ExecutionCatalog,
  ExecutionConfig,
} from "@/api/planExecutionConfig";
import type { PlanMinderNode } from "../planMinderTree";
const config: ExecutionConfig = {
  extended: false,
  executionMode: "parallel",
  testResourcePoolId: "pool",
  requestEnvironmentId: "target",
  stopOnFailure: false,
  retryOnFailure: true,
  retryTimes: 3,
  retryInterval: 200,
};
const catalog: ExecutionCatalog = {
  configurations: {
    "root:api": {
      scope: "root:api",
      revision: 2,
      config,
      effectiveConfig: config,
    },
    "node:api:a": {
      scope: "node:api:a",
      revision: 0,
      config: { ...config, extended: true },
      effectiveConfig: { ...config, extended: true },
    },
  },
  pools: [
    { id: "pool", name: "独立执行池", environmentIds: ["agent"], revision: 1 },
  ],
  requestEnvironments: [{ id: "target", name: "独立请求目标" }],
  resources: [],
};
const node = (
  kind: PlanMinderNode["kind"],
  scope = "root:api",
): PlanMinderNode => ({
  id: kind,
  kind,
  name: kind,
  category: "api",
  count: 1,
  configurationScope: scope,
});
describe("脑图环境和资源池标签真实作用域", () => {
  it("请求环境与执行池使用各自目录，包含官方默认选项", () => {
    expect(executionEnvironmentOptions(catalog)).toEqual([
      { value: "NONE", label: "默认环境" },
      { value: "target", label: "独立请求目标" },
    ]);
    expect(executionPoolOptions(catalog)).toEqual([
      { value: "DEFAULT", label: "默认资源池" },
      { value: "pool", label: "独立执行池" },
    ]);
    const environment = planMinderTag(node("environment"), catalog, true)!;
    expect(environment.field).toBe("requestEnvironmentId");
    expect(environment.value).toBe("target");
    expect(environment.scope).toBe("root:api");
    expect(planMinderTag(node("resource"), catalog, true)!.value).toBe("pool");
    expect(environment.config.retryTimes).toBe(3);
  });
  it("继承节点、只读用户、计数和不存在作用域不允许标签写入", () => {
    expect(
      planMinderTag(node("resource", "node:api:a"), catalog, true),
    ).toBeUndefined();
    expect(planMinderTag(node("environment"), catalog, false)).toBeUndefined();
    expect(planMinderTag(node("count"), catalog, true)).toBeUndefined();
    expect(
      planMinderTag(node("resource", "missing"), catalog, true),
    ).toBeUndefined();
  });
  it("关闭继承后的默认或实体集按自身作用域切换，不修改根或其他字段", () => {
    const local = structuredClone(catalog);
    local.configurations["node:api:a"].config.extended = false;
    const result = planMinderTag(node("resource", "node:api:a"), local, true)!;
    expect(result.scope).toBe("node:api:a");
    expect(result.field).toBe("testResourcePoolId");
    expect(catalog.configurations["node:api:a"].config.extended).toBe(true);
  });
});

it("independent pool ids do not collide with project pools and category choices are exact", () => {
  const both = {
    ...catalog,
    globalPools: [
      {
        id: "pool",
        name: "Global API",
        applications: ["api"] as ("api" | "scenario")[],
      },
      {
        id: "scene",
        name: "Global scene",
        applications: ["scenario"] as ("api" | "scenario")[],
      },
    ],
  };
  expect(executionPoolOptions(both, "api")).toEqual([
    { value: "DEFAULT", label: "默认资源池" },
    { value: "pool", label: "独立执行池" },
    { value: "GLOBAL:pool", label: "独立池：Global API" },
  ]);
  expect(executionPoolOptions(both, "scenario")).toContainEqual({
    value: "GLOBAL:scene",
    label: "独立池：Global scene",
  });
  const global = selectExecutionPool(config, "GLOBAL:pool");
  expect(global.testResourcePoolScope).toBe("global");
  expect(global.testResourcePoolId).toBe("pool");
  expect(executionPoolValue(global)).toBe("GLOBAL:pool");
  const project = selectExecutionPool(global, "pool");
  expect(project.testResourcePoolScope).toBe("project");
  expect(executionPoolValue(project)).toBe("pool");
  expect(selectExecutionPool(global, "DEFAULT").testResourcePoolScope).toBe(
    "project",
  );
  expect(global.retryTimes).toBe(3);
  expect(config.testResourcePoolScope).undefined;
});
