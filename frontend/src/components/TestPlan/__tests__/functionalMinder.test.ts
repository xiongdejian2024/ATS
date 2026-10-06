import { describe, it, expect } from "vitest";
import {
  buildFunctionalMinder,
  flattenFunctionalMinder,
  functionalCaseNode,
} from "../functionalMinder";
import type {
  PlanCaseEntry,
  PlanCaseExecutionRecord,
} from "@/api/planCaseWorkspace";
const row = (id: string, extra: Partial<PlanCaseEntry> = {}) =>
  ({
    id,
    caseId: "same",
    name: "中文用例😀",
    steps: [{ action: "动作", expected: "预期" }],
    result: "pending",
    ...extra,
  }) as PlanCaseEntry;
const text = (value: string) => value;
describe("功能脑图关联身份与步骤快照", () => {
  it("重复主用例保留实例身份，首屏存在更多节点而不伪造全量", () => {
    const root = buildFunctionalMinder(
      [],
      new Map([
        [
          "all",
          {
            items: [row("node:a:same"), row("node:b:same")],
            total: 101,
            page: 1,
          },
        ],
      ]),
      "all",
      "用例",
      text,
    );
    expect(root.count).toBe(101);
    expect(
      root.children?.filter((n) => n.kind === "case").map((n) => n.id),
    ).toEqual(["node:a:same", "node:b:same"]);
    expect(root.children?.find((n) => n.kind === "more")?.count).toBe(99);
  });
  it("指定目录显示其子目录，不混入其他目录", () => {
    const root = buildFunctionalMinder(
      [
        { id: "a", name: "父", count: 1 },
        { id: "b", name: "子", parentId: "a", count: 1 },
        { id: "c", name: "其他", count: 1 },
      ],
      new Map(),
      "a",
      "父",
      text,
    );
    expect(root.children?.map((n) => n.folderId)).toEqual(["b"]);
  });
  it("旧主用例步骤快照不套用到修改后的当前步骤", () => {
    const history = {
      id: "h",
      caseSnapshot: {
        steps: [{ step: 1, action: "旧动作", expected: "旧预期" }],
      },
      stepResults: [{ index: 0, result: "failed", actual: "旧实际" }],
    } as PlanCaseExecutionRecord;
    const node = functionalCaseNode(
      row("one", { executionId: "h" }),
      history,
      text,
    );
    expect(
      flattenFunctionalMinder(node).find((n) => n.kind === "actual")?.name,
    ).toBe("未填写");
    const current = functionalCaseNode(
      row("one", {
        executionId: "h",
        steps: [{ step: 1, action: "旧动作", expected: "旧预期" }],
      }),
      history,
      text,
    );
    expect(
      flattenFunctionalMinder(current).find((n) => n.kind === "actual")?.name,
    ).toBe("旧实际");
  });
  it("文本用例不产生虚构步骤；循环目录不会无限递归", () => {
    const node = functionalCaseNode(
      row("text", {
        caseEditType: "TEXT",
        textDescription: "文本",
        expectedResult: "文本预期",
      }),
      undefined,
      text,
    );
    expect(flattenFunctionalMinder(node).some((n) => n.kind === "step")).toBe(
      false,
    );
    const root = buildFunctionalMinder(
      [
        { id: "a", name: "甲", parentId: "b", count: 0 },
        { id: "b", name: "乙", parentId: "a", count: 0 },
      ],
      new Map(),
      "all",
      "用例",
      text,
    );
    expect(flattenFunctionalMinder(root)).toHaveLength(3);
  });
});
