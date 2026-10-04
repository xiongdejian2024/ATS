import { describe, it, expect } from "vitest";
import { mergeCaseSelection } from "../planCaseSelection";
describe("关联用例跨页选择", () => {
  it("跨页、模块筛选和返回后保留完整选择，取消单条不影响其他页", () => {
    const first = { id: "first", isAutomated: false },
      second = { id: "second", isAutomated: true };
    let selected = mergeCaseSelection(new Map(), ["first"], [first]);
    selected = mergeCaseSelection(selected, ["first", "second"], [second]);
    expect(Array.from(selected.values())).toEqual([first, second]);
    selected = mergeCaseSelection(selected, ["second"], [first]);
    expect(Array.from(selected.values())).toEqual([second]);
  });
  it("未知键不伪造完整记录，刷新页面替换所选记录内容且不修改旧快照", () => {
    const old = new Map([["one", { id: "one", name: "旧内容" }]]);
    const selected = mergeCaseSelection(
      old,
      ["one", "missing"],
      [{ id: "one", name: "新内容" }],
    );
    expect(Array.from(selected.values())).toEqual([
      { id: "one", name: "新内容" },
    ]);
    expect(old.get("one")?.name).toBe("旧内容");
  });
});
