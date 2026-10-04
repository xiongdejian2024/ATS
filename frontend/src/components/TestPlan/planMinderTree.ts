import type { PlanNode } from "@/api/planTree";
import type { PlanCaseEntry } from "@/api/planCaseWorkspace";
import { nodeHierarchy } from "./planCategoryTree";
export type PlanCategory = "functional" | "api" | "scenario";
export interface PlanMinderNode {
  id: string;
  name: string;
  kind: "root" | "category" | "collection" | "count";
  category?: PlanCategory;
  nodeId?: string;
  count: number;
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
): PlanMinderNode {
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
          children: [
            {
              id: `count:${category}:${point.id}`,
              nodeId: point.id,
              name: `${count} 条用例`,
              kind: "count",
              category,
              count,
            },
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
