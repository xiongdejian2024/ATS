import type { FunctionalMinderSelection } from "@/api/planCaseWorkspace";
import type { FunctionalMinderNode } from "./functionalMinder";
/** 选择目录使用服务端范围；已加载用例不能代表整目录。 */
export function functionalMinderScope(
  nodes: FunctionalMinderNode[],
  condition: FunctionalMinderSelection["condition"],
  treeType: "COLLECTION" | "MODULE",
  folder = "all",
): FunctionalMinderSelection | undefined {
  if (
    !nodes.length ||
    nodes.some((node) => !["root", "folder", "case"].includes(node.kind))
  )
    return;
  const base = { ...condition, tree_type: treeType, include_descendants: true };
  if (nodes.some((node) => node.kind === "root"))
    return { selectAll: true, condition: { ...base, folder } };
  const folderIds = [
    ...new Set(
      nodes
        .filter((node) => node.kind === "folder")
        .map((node) => node.folderId!),
    ),
  ];
  const entryIds = [
    ...new Set(
      nodes.filter((node) => node.kind === "case").map((node) => node.entryId!),
    ),
  ];
  if (!folderIds.length) return { selectIds: entryIds };
  return {
    selectAll: true,
    condition: { ...base, folder: "all", folderIds, entryIds },
  };
}
