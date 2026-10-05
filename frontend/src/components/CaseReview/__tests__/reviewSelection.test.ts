import { describe, it, expect } from "vitest";
import { pageExclusions, selectedPageIds } from "../reviewSelection";

describe("全部筛选范围的跨页排除项", () => {
  it("在当前页取消和重新勾选，不丢失其他页的排除项", () => {
    const initial = ["other-page", "a"];
    const next = pageExclusions(initial, ["a", "b", "c"], ["a", "c"]);
    expect(next).toEqual(["other-page", "b"]);
    expect(initial).toEqual(["other-page", "a"]);
    expect(selectedPageIds(["a", "b", "c"], next)).toEqual(["a", "c"]);
  });
  it("取消当前页和重新选中当前页，保留其他页的选择模式", () => {
    const excluded = pageExclusions(["old-page"], ["a", "b"], []);
    expect(excluded).toEqual(["old-page", "a", "b"]);
    expect(pageExclusions(excluded, ["a", "b"], ["a", "b"])).toEqual([
      "old-page",
    ]);
  });
  it("重复选择与排除均幂等，不将其他页ID加入当前页", () => {
    const excluded = pageExclusions(["b"], ["a", "b"], ["a", "foreign"]);
    expect(pageExclusions(excluded, ["a", "b"], ["a", "foreign"])).toEqual([
      "b",
    ]);
    expect(selectedPageIds(["a", "b"], ["b", "foreign"])).toEqual(["a"]);
  });
});
