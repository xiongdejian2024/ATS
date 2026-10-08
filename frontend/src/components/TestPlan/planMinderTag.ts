import type {
  ExecutionCatalog,
  ExecutionConfig,
} from "@/api/planExecutionConfig";
import type { PlanMinderNode } from "./planMinderTree";
export const executionPoolOptions = (catalog: ExecutionCatalog) => [
  { value: "DEFAULT", label: "默认资源池" },
  ...catalog.pools.map((item) => ({ value: item.id, label: item.name })),
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
        : entry.effectiveConfig[field],
    config: entry.effectiveConfig,
    label: node.kind === "environment" ? "接口请求环境选择" : "资源池选择",
    options:
      node.kind === "environment"
        ? executionEnvironmentOptions(catalog)
        : executionPoolOptions(catalog),
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
