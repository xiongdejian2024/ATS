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

import { functionalMinderScope } from "../functionalMinderScope";
describe("脑图批量节点范围", () => {
  const a = {
    id: "a",
    kind: "folder",
    folderId: "a",
    name: "父",
    count: 101,
  } as const;
  const b = {
    id: "b",
    kind: "case",
    entryId: "node:b:same",
    name: "同名实例",
    count: 1,
  } as const;
  it("目录与实例使用服务端并集，不以已加载节点数量替代全目录", () => {
    expect(functionalMinderScope([a, b], { search: "中文" }, "MODULE")).toEqual(
      {
        selectAll: true,
        condition: {
          search: "中文",
          tree_type: "MODULE",
          include_descendants: true,
          folder: "all",
          folderIds: ["a"],
          entryIds: ["node:b:same"],
        },
      },
    );
  });
  it("目录根保留当前目录范围，纯实例去重且内容节点不能批量修改", () => {
    expect(
      functionalMinderScope(
        [{ id: "root", kind: "root", name: "子目录", count: 101 }],
        {},
        "COLLECTION",
        "child",
      )?.condition?.folder,
    ).toBe("child");
    expect(functionalMinderScope([b, b], {}, "MODULE")).toEqual({
      selectIds: ["node:b:same"],
    });
    expect(
      functionalMinderScope([{ ...b, kind: "actual" }], {}, "MODULE"),
    ).toBeUndefined();
  });
});

import {
  functionalFolderPath,
  functionalCameraScroll,
} from "../functionalMinder";
describe("功能脑图目录导航与实例标识", () => {
  it("保留每个实例自己的编号、等级及缺陷计数", () => {
    const a = functionalCaseNode(
      row("a", { caseCode: "F-1", priority: "P0", bugCount: 2 }),
      undefined,
      text,
    );
    const b = functionalCaseNode(
      row("b", { caseCode: "F-1", priority: "P2", bugCount: 0 }),
      undefined,
      text,
    );
    expect([a.caseCode, a.priority, a.bugCount]).toEqual(["F-1", "P0", 2]);
    expect([b.caseCode, b.priority, b.bugCount]).toEqual(["F-1", "P2", 0]);
  });
  it("目录路径支持任意祖先返回，并排除其他分支", () => {
    const folders = [
      { id: "p", name: "父", count: 5 },
      { id: "c", name: "子", parentId: "p", count: 2 },
      { id: "other", name: "其他", count: 0 },
    ];
    expect(functionalFolderPath(folders, "c").map((x) => x.id)).toEqual([
      "all",
      "p",
      "c",
    ]);
    expect(functionalFolderPath(folders, "p").map((x) => x.id)).toEqual([
      "all",
      "p",
    ]);
    expect(functionalFolderPath(folders, "all")).toEqual([
      { id: "all", name: "功能用例" },
    ]);
  });
  it("删除或循环目录不会产生无效链接或无限循环", () => {
    expect(functionalFolderPath([], "missing").map((x) => x.id)).toEqual([
      "all",
    ]);
    const values = functionalFolderPath(
      [
        { id: "a", name: "甲", parentId: "b", count: 0 },
        { id: "b", name: "乙", parentId: "a", count: 0 },
      ],
      "a",
    );
    expect(values.map((x) => x.id)).toEqual(["all", "b", "a"]);
  });
  it("缩略图定位与画布40px边距和实际视口一致", () => {
    expect(functionalCameraScroll(200, 1, 200)).toBe(140);
    expect(functionalCameraScroll(200, 2, 200)).toBe(340);
    expect(functionalCameraScroll(0, 0.5, 600)).toBe(0);
  });
});
