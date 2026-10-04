import { describe, expect, it } from "vitest";
import { buildCaseMindMap, copyCaseDraft } from "../caseMindMap";
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
});
