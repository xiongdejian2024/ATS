import type { PlanNode, NodeConfig } from "@/api/planTree";
import type { PlanCaseEntry } from "@/api/planCaseWorkspace";
import { nodeHierarchy } from "./planCategoryTree";
export type PlanCategory = "functional" | "api" | "scenario";
export interface PlanMinderNode {
  id: string;
  name: string;
  kind:
    | "root"
    | "category"
    | "collection"
    | "count"
    | "environment"
    | "resource";
  category?: PlanCategory;
  nodeId?: string;
  count: number;
  executionMode?: "serial" | "parallel";
  children?: PlanMinderNode[];
}
export const planCategoryNames: Record<PlanCategory, string> = {
  functional: "功能用例",
  api: "API 用例",
  scenario: "API 场景",
};
/** 分类展示真实关联实例；旧直接关联和混合分类的公共测试点均保留。 */
export function buildPlanMinder(
  name: string,
  nodes: PlanNode[],
  entries: Record<PlanCategory, PlanCaseEntry[]>,
  options: {
    environmentNames?: Record<string, string>;
    defaultEnvironmentId?: string | null;
  } = {},
): PlanMinderNode {
  function configurationNodes(
    category: PlanCategory,
    nodeId: string | undefined,
    effective: NodeConfig,
    count: number,
  ): PlanMinderNode[] {
    if (category === "functional") return [];
    const environmentName = effective.environmentId
      ? options.environmentNames?.[effective.environmentId] || "已指定环境"
      : "默认环境";
    const pool = effective.resourcePool || [];
    const poolName = pool.length
      ? pool
          .map((id) => options.environmentNames?.[id] || "已指定节点")
          .join("、")
      : "默认资源池";
    return [
      {
        id: `environment:${category}:${nodeId || "default"}`,
        name: `环境：${environmentName}`,
        kind: "environment",
        category,
        nodeId,
        count,
      },
      {
        id: `resource:${category}:${nodeId || "default"}`,
        name: `资源池：${poolName}`,
        kind: "resource",
        category,
        nodeId,
        count,
      },
    ];
  }
  const points = nodes.filter((node) => node.nodeType === "point"),
    byId = new Map(points.map((node) => [node.id, node]));
  const categories = (Object.keys(planCategoryNames) as PlanCategory[]).map(
    (category) => {
      const items = entries[category],
        visible = new Set<string>();
      function showParent(id?: string | null) {
        const seen = new Set<string>();
        while (id && byId.has(id) && !seen.has(id)) {
          seen.add(id);
          visible.add(id);
          id = byId.get(id)?.parentId;
        }
      }
      for (const point of points)
        if (point.category === category) showParent(point.id);
      for (const item of items) showParent(item.collectionId);
      const hierarchy = nodeHierarchy(
        points.filter((point) => visible.has(point.id)),
      );
      function collection(
        point: ReturnType<typeof nodeHierarchy>[number],
      ): PlanMinderNode {
        const children = (point.children || []).map(collection);
        const count =
          items.filter((item) => item.collectionId === point.id).length +
          children.reduce((sum, node) => sum + node.count, 0);
        return {
          id: `${category}:${point.id}`,
          nodeId: point.id,
          name: point.name,
          kind: "collection",
          category,
          count,
          executionMode: point.effectiveConfig?.executionMode || undefined,
          children: [
            {
              id: `count:${category}:${point.id}`,
              nodeId: point.id,
              name: `${count} 条用例`,
              kind: "count",
              category,
              count,
            },
            ...configurationNodes(
              category,
              point.id,
              point.effectiveConfig || point.config || {},
              count,
            ),
            ...children,
          ],
        };
      }
      const collections = hierarchy.map(collection),
        unassigned = items.filter(
          (item) => !item.collectionId || !byId.has(item.collectionId),
        ).length;
      if (unassigned)
        collections.unshift({
          id: `default:${category}`,
          name: "默认测试集",
          kind: "collection",
          category,
          count: unassigned,
          children: [
            ...configurationNodes(
              category,
              undefined,
              {
                environmentId: options.defaultEnvironmentId,
              },
              unassigned,
            ),
            {
              id: `count:default:${category}`,
              name: `${unassigned} 条用例`,
              kind: "count",
              category,
              count: unassigned,
            },
          ],
        });
      return {
        id: `category:${category}`,
        name: `${planCategoryNames[category]} (${items.length})`,
        kind: "category" as const,
        category,
        count: items.length,
        children: collections,
      };
    },
  );
  return {
    id: "root",
    name,
    kind: "root",
    count: categories.reduce((sum, node) => sum + node.count, 0),
    children: categories,
  };
}

/** 折叠仅改变展示，不改变关联数量或原始节点，展开后可恢复完整树。 */
export function presentPlanMinder(
  node: PlanMinderNode,
  collapsed: ReadonlySet<string>,
): PlanMinderNode {
  return {
    ...node,
    name:
      collapsed.has(node.id) && node.children?.length
        ? `${node.name} [+]`
        : node.name,
    children: collapsed.has(node.id)
      ? undefined
      : node.children?.map((child) => presentPlanMinder(child, collapsed)),
  };
}
