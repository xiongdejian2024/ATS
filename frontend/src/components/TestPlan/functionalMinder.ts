import type {
  CaseFolder,
  PlanCaseEntry,
  PlanCaseExecutionRecord,
} from "@/api/planCaseWorkspace";
import { functionalResultLabels } from "./functionalExecution";
export type FunctionalMinderKind =
  | "root"
  | "folder"
  | "case"
  | "precondition"
  | "step"
  | "action"
  | "expected"
  | "actual"
  | "text"
  | "description"
  | "more";
export interface FunctionalMinderNode {
  id: string;
  name: string;
  kind: FunctionalMinderKind;
  count: number;
  folderId?: string;
  entryId?: string;
  stepIndex?: number;
  result?: string;
  caseCode?: string;
  priority?: string;
  bugCount?: number;
  children?: FunctionalMinderNode[];
}
export interface FunctionalMinderPage {
  items: PlanCaseEntry[];
  total: number;
  page: number;
}
export function functionalCaseNode(
  row: PlanCaseEntry,
  history: PlanCaseExecutionRecord | undefined,
  text: (value: string) => string,
): FunctionalMinderNode {
  const node: FunctionalMinderNode = {
    id: row.id,
    name: row.name,
    kind: "case",
    entryId: row.id,
    count: 1,
    result: row.result,
    caseCode: row.caseCode,
    priority: row.priority,
    bugCount: row.bugCount,
    children: [],
  };
  const child = (
    kind: FunctionalMinderKind,
    name: string,
    stepIndex?: number,
  ): FunctionalMinderNode => ({
    id: `${row.id}:${kind}:${stepIndex ?? ""}`,
    name: text(name) || "未填写",
    kind,
    count: 0,
    entryId: row.id,
    stepIndex,
  });
  const current = history?.id === row.executionId ? history : undefined;
  node.children!.push(child("precondition", row.precondition || ""));
  if (row.caseEditType === "TEXT") {
    node.children!.push(
      child("text", row.textDescription || ""),
      child("expected", row.expectedResult || ""),
    );
  } else {
    const unchanged =
      current &&
      JSON.stringify(
        current.caseSnapshot.steps?.map((s) => ({
          action: s.action,
          expected: s.expected,
        })),
      ) ===
        JSON.stringify(
          row.steps?.map((s) => ({ action: s.action, expected: s.expected })),
        );
    (row.steps || []).forEach((step, index) => {
      const recorded = unchanged
        ? current?.stepResults.find((r) => r.index === index)
        : undefined;
      const actual = child("actual", recorded?.actual || "", index);
      const expected = child("expected", step.expected, index);
      expected.children = [actual];
      const action = child("action", step.action, index);
      action.children = [expected];
      node.children!.push({
        ...child("step", `步骤 ${index + 1}`, index),
        result: recorded?.result,
        children: [action],
      });
    });
  }
  node.children!.push(child("description", row.description || ""));
  if (current?.description)
    node.children!.push(child("actual", current.description));
  return node;
}
/** 关联实例ID始终作为用例节点身份；主用例重复关联不会共享结果。 */
export function buildFunctionalMinder(
  folders: CaseFolder[],
  pages: ReadonlyMap<string, FunctionalMinderPage>,
  rootFolder: string,
  rootName: string,
  text: (value: string) => string,
  history: ReadonlyMap<string, PlanCaseExecutionRecord> = new Map(),
): FunctionalMinderNode {
  const root: FunctionalMinderNode = {
    id: "minder-root",
    kind: "root",
    name: rootName,
    count: 0,
    folderId: rootFolder,
    children: [],
  };
  const nodes = new Map(
    folders.map((f) => [
      f.id,
      {
        id: `folder:${f.id}`,
        kind: "folder",
        name: f.name,
        count: f.count,
        folderId: f.id,
        children: [],
      } as FunctionalMinderNode,
    ]),
  );
  const byId = new Map(folders.map((f) => [f.id, f]));
  if (rootFolder === "all" || nodes.has(rootFolder)) {
    for (const f of folders) {
      const seen = new Set([f.id]);
      let parent = f.parentId;
      let cycle = false;
      while (parent && byId.has(parent)) {
        if (seen.has(parent)) {
          cycle = true;
          break;
        }
        seen.add(parent);
        parent = byId.get(parent)?.parentId;
      }
      if (f.id === rootFolder) continue;
      if (rootFolder !== "all" && !seen.has(rootFolder)) continue;
      (cycle || f.parentId === rootFolder
        ? root
        : nodes.get(f.parentId || "") || root
      ).children!.push(nodes.get(f.id)!);
    }
  }
  const targetFor = (id: string) => (id === rootFolder ? root : nodes.get(id));
  for (const [id, page] of pages) {
    const target = targetFor(id);
    if (!target) continue;
    target.count = page.total;
    target.children!.push(
      ...page.items.map((row) =>
        functionalCaseNode(row, history.get(row.id), text),
      ),
    );
    if (page.items.length < page.total)
      target.children!.push({
        id: `more:${id}`,
        kind: "more",
        name: "更多用例",
        count: page.total - page.items.length,
        folderId: id,
      });
  }
  return root;
}
export function flattenFunctionalMinder(
  root: FunctionalMinderNode,
): FunctionalMinderNode[] {
  const nodes: FunctionalMinderNode[] = [];
  const visit = (n: FunctionalMinderNode) => {
    nodes.push(n);
    n.children?.forEach(visit);
  };
  visit(root);
  return nodes;
}
export const functionalMinderTags: Record<FunctionalMinderKind, string> = {
  root: "",
  folder: "",
  case: "",
  precondition: "前置条件",
  step: "步骤描述",
  action: "步骤描述",
  expected: "预期结果",
  actual: "实际结果",
  text: "文本描述",
  description: "备注",
  more: "",
};
export const resultLabel = (node: FunctionalMinderNode) =>
  node.result ? functionalResultLabels[node.result] || node.result : "";

/** Directory breadcrumbs never invent a parent or recurse through corrupt cycles. */
export function functionalFolderPath(folders: CaseFolder[], current: string) {
  const root = { id: "all", name: "功能用例" };
  if (current === "all") return [root];
  const byId = new Map(folders.map((folder) => [folder.id, folder]));
  const path: { id: string; name: string }[] = [];
  const seen = new Set<string>();
  let id: string | undefined = current;
  while (id && byId.has(id) && !seen.has(id)) {
    seen.add(id);
    const item: CaseFolder = byId.get(id)!;
    path.unshift({ id: item.id, name: item.name });
    id = item.parentId;
  }
  return [root, ...path];
}
export function functionalCameraScroll(
  center: number,
  zoom: number,
  viewport: number,
) {
  return Math.max(0, 40 + center * zoom - viewport / 2);
}
