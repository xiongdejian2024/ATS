import type { TestCase } from "@/types";

export interface MindModule {
  id: string;
  name: string;
  parentId?: string | null;
  parent_id?: string | null;
}
export interface CaseMindNode {
  id: string;
  name: string;
  kind:
    | "root"
    | "module"
    | "case"
    | "precondition"
    | "step"
    | "action"
    | "expected"
    | "textDescription"
    | "expectedResult";
  caseId?: string;
  moduleId?: string;
  stepIndex?: number;
  children?: CaseMindNode[];
  itemStyle?: { color: string };
  collapsed?: boolean;
}

/** 用例内容节点与数据库字段保持一一对应，展示标识不能作为复制后的数据库 ID。 */
export function buildCaseMindMap(
  cases: Partial<TestCase>[],
  modules: MindModule[] = [],
): CaseMindNode {
  const root: CaseMindNode = {
    id: "root",
    name: "测试用例",
    kind: "root",
    children: [],
  };
  const nodes = new Map(
    modules.map((m) => [
      m.id,
      {
        id: `module:${m.id}`,
        moduleId: m.id,
        name: m.name,
        kind: "module",
        children: [],
      } as CaseMindNode,
    ]),
  );
  for (const m of modules) {
    const parentId = m.parentId || m.parent_id;
    // 畸形模块数据也不能造成循环图。
    const visited = new Set([m.id]);
    let ancestor = parentId;
    let cyclic = false;
    while (ancestor) {
      if (visited.has(ancestor)) {
        cyclic = true;
        break;
      }
      visited.add(ancestor);
      const parent = modules.find((p) => p.id === ancestor);
      ancestor = parent?.parentId || parent?.parent_id;
    }
    const parent = !cyclic && parentId ? nodes.get(parentId) : undefined;
    (parent || root).children!.push(nodes.get(m.id)!);
  }
  const unassigned: CaseMindNode = {
    id: "unassigned",
    name: "未规划",
    kind: "module",
    children: [],
  };
  for (const c of cases) {
    if (!c.id) continue;
    const prefix = `case:${c.id}`;
    const children: CaseMindNode[] = [
      {
        id: `${prefix}:precondition`,
        name: `前置条件：${c.precondition || "未填写"}`,
        kind: "precondition",
        caseId: c.id,
      },
    ];
    if (c.caseEditType === "TEXT") {
      for (const [kind, label] of [
        ["textDescription", "描述"],
        ["expectedResult", "预期结果"],
      ] as const) {
        children.push({
          id: `${prefix}:${kind}`,
          name: `${label}：${mindText(c[kind] || "未填写")}`,
          kind,
          caseId: c.id,
        });
      }
    } else
      (c.steps || []).forEach((s, i) =>
        children.push({
          id: `${prefix}:step:${i}`,
          name: `步骤 ${i + 1}`,
          kind: "step",
          caseId: c.id,
          stepIndex: i,
          children: [
            {
              id: `${prefix}:action:${i}`,
              name: `操作：${s.action || "未填写"}`,
              kind: "action",
              caseId: c.id,
              stepIndex: i,
            },
            {
              id: `${prefix}:expected:${i}`,
              name: `预期：${s.expected || "未填写"}`,
              kind: "expected",
              caseId: c.id,
              stepIndex: i,
            },
          ],
        }),
      );
    const color =
      c.status === "passed"
        ? "#389e0d"
        : c.status === "failed"
          ? "#cf1322"
          : "#1677ff";
    (nodes.get(c.moduleId || "") || unassigned).children!.push({
      id: prefix,
      name: `${c.caseCode ? `${c.caseCode} · ` : ""}${c.name || "未命名"}`,
      kind: "case",
      caseId: c.id,
      moduleId: c.moduleId || undefined,
      children,
      itemStyle: { color },
    });
  }
  if (unassigned.children!.length) root.children!.push(unassigned);
  return root;
}

/** 图上只展示文本，编辑及复制仍保留原富文本，不改写 HTML 或身份。 */
export function mindText(value: string): string {
  return value
    .replace(/<[^>]*>/g, " ")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, 500);
}

export function mindNodeValue(
  node: CaseMindNode,
  testCase?: Partial<TestCase>,
): string {
  if (node.kind === "module") return node.name;
  if (!testCase) return "";
  if (node.kind === "case") return testCase.name || "";
  if (["precondition", "textDescription", "expectedResult"].includes(node.kind))
    return String(
      testCase[
        node.kind as "precondition" | "textDescription" | "expectedResult"
      ] || "",
    );
  const step = testCase.steps?.[node.stepIndex ?? -1];
  return (node.kind === "expected" ? step?.expected : step?.action) || "";
}

export function mindNodePatch(
  node: CaseMindNode,
  testCase: Partial<TestCase>,
  value: string,
): Partial<TestCase> | undefined {
  if (node.kind === "case")
    return value.trim() ? { name: value.trim() } : undefined;
  if (["precondition", "textDescription", "expectedResult"].includes(node.kind))
    return { [node.kind]: value };
  const index = node.stepIndex;
  if (
    index === undefined ||
    index < 0 ||
    !Number.isInteger(index) ||
    !testCase.steps?.[index] ||
    testCase.caseEditType === "TEXT"
  )
    return undefined;
  const steps = testCase.steps.map((step) => ({ ...step }));
  steps[index] = {
    ...steps[index],
    [node.kind === "expected" ? "expected" : "action"]: value,
  };
  return { steps };
}

/** 只复制可编辑内容，剥离用例/步骤身份、审计字段和执行结果。 */
export function copyCaseDraft(
  c: Partial<TestCase>,
  moduleId?: string,
): Partial<TestCase> {
  return {
    templateId: c.templateId,
    customFields: JSON.parse(JSON.stringify(c.customFields || {})),
    name: `${(c.name || "用例").slice(0, 251)}（副本）`,
    type: c.type || "functional",
    priority: c.priority || "P2",
    moduleId: moduleId || c.moduleId || undefined,
    precondition: c.precondition || "",
    caseEditType: c.caseEditType || "STEP",
    textDescription: c.textDescription || "",
    expectedResult: c.expectedResult || "",
    description: c.description || "",
    executorId: c.executorId,
    requirementRef: c.requirementRef || "",
    tags: [...(c.tags || [])],
    isAutomated: c.isAutomated || false,
    steps: (c.steps || []).map((s, i) => ({
      step: i + 1,
      action: s.action,
      expected: s.expected,
    })),
  };
}
