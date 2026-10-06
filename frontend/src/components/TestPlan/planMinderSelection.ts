import type { PlanNode } from "@/api/planTree";
import type { PlanMinderNode, PlanCategory } from "./planMinderTree";

export interface MinderDeletionTarget {
  nodeId?: string;
  category: PlanCategory;
}
export interface MinderSelectionBox {
  left: number;
  top: number;
  right: number;
  bottom: number;
}
export function intersects(a: MinderSelectionBox, b: MinderSelectionBox) {
  return (
    Math.max(a.left, b.left) < Math.min(a.right, b.right) &&
    Math.max(a.top, b.top) < Math.min(a.bottom, b.bottom)
  );
}
/** 与MS一致，混入分类或标签时整个批量删除不可用；旧公共集投影只在原分类删除。 */
export function minderDeletionTargets(
  selected: PlanMinderNode[],
  points: PlanNode[],
  editable: boolean,
): MinderDeletionTarget[] | undefined {
  if (!editable || !selected.length) return undefined;
  const byId = new Map(points.map((point) => [point.id, point]));
  if (
    selected.some(
      (node) =>
        node.kind !== "collection" ||
        !node.category ||
        (node.nodeId && byId.get(node.nodeId)?.category !== node.category),
    )
  )
    return undefined;
  const selectedPoints = new Set(selected.map((node) => node.nodeId));
  const targets = new Map<string, MinderDeletionTarget>();
  for (const node of selected) {
    let parent = node.nodeId && byId.get(node.nodeId)?.parentId;
    const seen = new Set<string>();
    let covered = false;
    while (parent) {
      if (seen.has(parent)) return undefined;
      seen.add(parent);
      if (selectedPoints.has(parent)) covered = true;
      parent = byId.get(parent)?.parentId;
    }
    if (!covered)
      targets.set(node.nodeId || `default:${node.category}`, {
        nodeId: node.nodeId,
        category: node.category!,
      });
  }
  return [...targets.values()];
}
