import { describe, expect, it } from "vitest";
import {
  buildCaseMindMap,
  copyCaseDraft,
  mindNodeValue,
  mindNodePatch,
} from "../caseMindMap";
describe("用例脑图内容映射", () => {
  it("保留完整步骤/预期并放在对应模块内", () => {
    const root = buildCaseMindMap(
      [
        {
          id: "c",
          name: "登录",
          moduleId: "m",
          precondition: "未登录",
          steps: [{ step: 1, action: "输入", expected: "成功" }],
        },
      ],
      [{ id: "m", name: "账户" }],
    );
    const node = root.children![0].children![0];
    expect(node.kind).toBe("case");
    expect(node.children![1].children!.map((n) => n.kind)).toEqual([
      "action",
      "expected",
    ]);
    expect(node.children![0].name).toContain("未登录");
  });
  it("复制内容不携带数据库标识及执行结果", () => {
    const draft = copyCaseDraft({
      id: "原id",
      caseCode: "原编号",
      templateId: "模板",
      customFields: { model: "车型" },
      name: "登录",
      status: "passed",
      steps: [
        { id: "步骤id", step: 1, action: "输入", expected: "成功" },
      ] as any,
    });
    expect(draft).not.toHaveProperty("id");
    expect(draft).not.toHaveProperty("caseCode");
    expect(draft).not.toHaveProperty("status");
    expect(draft.steps![0]).not.toHaveProperty("id");
    expect(draft.templateId).toBe("模板");
    expect(draft.customFields).toEqual({ model: "车型" });
  });
  it("最长用例名复制仍满足255字符限制并保留副本标记", () => {
    const source = "测".repeat(255);
    const copy = copyCaseDraft({ name: source });
    expect(copy.name).toHaveLength(255);
    expect(copy.name).toContain("（副本）");
    expect(source).toHaveLength(255);
  });
  it("循环模块数据仍可序列化", () => {
    expect(() =>
      JSON.stringify(
        buildCaseMindMap(
          [],
          [
            { id: "a", name: "甲", parentId: "b" },
            { id: "b", name: "乙", parentId: "a" },
          ],
        ),
      ),
    ).not.toThrow();
  });
  it("TEXT 内容节点保留字段和富文本，不显示历史隐藏步骤", () => {
    const row = {
      id: "t",
      name: "文本",
      caseEditType: "TEXT" as const,
      textDescription: "<p>描述</p>",
      expectedResult: "<p>预期</p>",
      steps: [{ step: 1, action: "旧隐藏步骤", expected: "旧预期" }],
    };
    const node = buildCaseMindMap([row]).children![0].children![0];
    expect(node.children!.map((n) => n.kind)).toEqual([
      "precondition",
      "textDescription",
      "expectedResult",
    ]);
    const description = node.children![1];
    expect(description.name).toContain("描述");
    expect(description.name).not.toContain("<p>");
    expect(mindNodeValue(description, row)).toBe("<p>描述</p>");
    expect(mindNodePatch(description, row, "<p>新描述</p>")).toEqual({
      textDescription: "<p>新描述</p>",
    });
    expect(copyCaseDraft(row).steps).toEqual(row.steps);
    expect(copyCaseDraft(row).textDescription).toBe(row.textDescription);
  });
  it("步骤索引失效时不造出新步骤，编辑只修改目标字段", () => {
    const row = { steps: [{ step: 1, action: "原操作", expected: "原预期" }] };
    expect(
      mindNodePatch(
        { id: "x", name: "x", kind: "expected", stepIndex: 8 },
        row,
        "新预期",
      ),
    ).toBeUndefined();
    expect(
      mindNodePatch(
        { id: "x", name: "x", kind: "expected", stepIndex: 0 },
        row,
        "新预期",
      ),
    ).toEqual({ steps: [{ step: 1, action: "原操作", expected: "新预期" }] });
    expect(row.steps[0].expected).toBe("原预期");
  });
});
