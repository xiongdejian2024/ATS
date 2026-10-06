import type { PlanMinderNode } from "./planMinderTree";
export type MinderAction =
  | "add"
  | "associate"
  | "mode"
  | "configure"
  | "delete";
/** MS规划的分类、测试集及只读节点菜单；继承配置不能独立切换执行方式。 */
export function planMinderActions(
  node: PlanMinderNode,
  editable: boolean,
  inherited: boolean,
): MinderAction[] {
  if (node.kind === "root") return editable ? ["mode"] : [];
  if (node.kind !== "category" && node.kind !== "collection") return [];
  if (!editable) return node.category !== "functional" ? ["configure"] : [];
  const actions: MinderAction[] = ["add"];
  if (node.kind === "collection") actions.push("associate");
  if (
    node.category !== "functional" &&
    !(node.kind === "collection" && inherited)
  )
    actions.push("mode");
  if (node.kind === "collection" || node.category !== "functional")
    actions.push("configure");
  if (node.kind === "collection") actions.push("delete");
  return actions;
}
