import type {
  ExecutionCatalog,
  ExecutionConfig,
} from "@/api/planExecutionConfig";
import type { PlanMinderNode } from "./planMinderTree";
export const executionPoolOptions = (
  catalog: ExecutionCatalog,
  category?: string,
) => [
  { value: "DEFAULT", label: "默认资源池" },
  ...catalog.pools.map((item) => ({ value: item.id, label: item.name })),
  ...(catalog.globalPools || [])
    .filter(
      (item) =>
        !category || item.applications.includes(category as "api" | "scenario"),
    )
    .map((item) => ({
      value: `GLOBAL:${item.id}`,
      label: `独立池：${item.name}`,
    })),
];
export const executionEnvironmentOptions = (catalog: ExecutionCatalog) => [
  { value: "NONE", label: "默认环境" },
  ...(catalog.requestEnvironmentGroups || []).map((item) => ({
    value: `GROUP:${item.id}`,
    label: `环境组：${item.name}`,
  })),
  ...catalog.requestEnvironments.map((item) => ({
    value: item.id,
    label: item.name,
  })),
];
export function planMinderTag(
  node: PlanMinderNode | undefined,
  catalog: ExecutionCatalog | undefined,
  editable: boolean,
) {
  if (
    !editable ||
    !node ||
    !catalog ||
    !node.configurationScope ||
    !["environment", "resource"].includes(node.kind)
  )
    return undefined;
  const entry = catalog.configurations[node.configurationScope];
  if (!entry || entry.config.extended) return undefined;
  const field: keyof Pick<
    ExecutionConfig,
    "requestEnvironmentId" | "testResourcePoolId"
  > =
    node.kind === "environment" ? "requestEnvironmentId" : "testResourcePoolId";
  return {
    scope: node.configurationScope,
    field,
    value:
      node.kind === "environment"
        ? executionEnvironmentValue(entry.effectiveConfig)
        : executionPoolValue(entry.effectiveConfig),
    config: entry.effectiveConfig,
    label: node.kind === "environment" ? "接口请求环境选择" : "资源池选择",
    options:
      node.kind === "environment"
        ? executionEnvironmentOptions(catalog)
        : executionPoolOptions(catalog, node.category),
  };
}

export function executionEnvironmentValue(config: ExecutionConfig) {
  return config.requestEnvironmentGroupId &&
    config.requestEnvironmentGroupId !== "NONE"
    ? `GROUP:${config.requestEnvironmentGroupId}`
    : config.requestEnvironmentId;
}
export function selectExecutionEnvironment(
  config: ExecutionConfig,
  value: string,
): ExecutionConfig {
  return value.startsWith("GROUP:")
    ? {
        ...config,
        requestEnvironmentId: "NONE",
        requestEnvironmentGroupId: value.slice(6),
      }
    : {
        ...config,
        requestEnvironmentId: value,
        requestEnvironmentGroupId: "NONE",
      };
}

export function executionPoolValue(config: ExecutionConfig) {
  return config.testResourcePoolScope === "global"
    ? `GLOBAL:${config.testResourcePoolId}`
    : config.testResourcePoolId;
}
export function selectExecutionPool(
  config: ExecutionConfig,
  value: string,
): ExecutionConfig {
  return value.startsWith("GLOBAL:")
    ? {
        ...config,
        testResourcePoolScope: "global",
        testResourcePoolId: value.slice(7),
      }
    : {
        ...config,
        testResourcePoolScope: "project",
        testResourcePoolId: value,
      };
}
