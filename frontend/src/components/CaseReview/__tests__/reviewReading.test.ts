import { describe, it, expect } from "vitest";
import {
  afterReviewTarget,
  readingScope,
  selectedReviewStates,
} from "../reviewReading";
describe("独立审阅列表上下文和自动下一条", () => {
  it("保留合法跨页、搜索、目录、人员及多结果，不信任其他项目标识", () => {
    expect(
      readingScope(
        JSON.stringify({
          page: 2,
          size: 20,
          sort: "caseCode",
          order: "asc",
          folder: "模块",
          search: "中文",
          reviewerId: "用户",
          states: ["approved", "re_review", "fake"],
          projectId: "other",
          view: "mind",
        }),
      ),
    ).toEqual({
      page: 2,
      size: 20,
      sort: "caseCode",
      order: "asc",
      folder: "模块",
      search: "中文",
      reviewerId: "用户",
      states: ["approved", "re_review"],
      view: "list",
    });
  });
  it("非法分页和排序使用默认值", () => {
    expect(
      readingScope({ page: 0, size: 999, sort: "sql", order: "drop" }),
    ).toEqual({
      page: 1,
      size: 10,
      sort: "createdAt",
      order: "desc",
      folder: "all",
      view: "list",
    });
  });
  it("旧单结果地址升级为多结果，往返保留两个结果并去重", () => {
    expect(selectedReviewStates(readingScope({ state: "rejected" }))).toEqual([
      "rejected",
    ]);
    const scope = readingScope(
      JSON.stringify({
        states: ["approved", "re_review", "approved", "fake"],
        state: "rejected",
      }),
    );
    expect(selectedReviewStates(scope)).toEqual(["approved", "re_review"]);
  });
  it("显式清空多结果不能从原地址复活旧单结果", () => {
    expect(
      selectedReviewStates(readingScope({ state: "approved", states: [] })),
    ).toEqual([]);
    expect(selectedReviewStates(readingScope({ state: "fake" }))).toEqual([]);
  });
  it("自动下一条按刷新后列表移动，最后一条保持当前", () => {
    expect(afterReviewTarget(["a", "b", "c"], "b", ["a", "b", "c"], true)).toBe(
      "c",
    );
    expect(afterReviewTarget(["a", "b"], "b", ["a", "b"], true)).toBe("b");
  });
  it("提交条目被筛选移除后选同位置，末尾回到第一条，全部移除返回空", () => {
    expect(afterReviewTarget(["a", "b", "c"], "b", ["a", "c"], true)).toBe("c");
    expect(afterReviewTarget(["a", "b"], "b", ["a"], true)).toBe("a");
    expect(afterReviewTarget(["a"], "a", [], true)).toBeUndefined();
  });
  it("关闭自动下一条仍保持当前详情，空范围清空", () => {
    expect(afterReviewTarget(["a", "b"], "a", ["b"], false)).toBe("a");
    expect(afterReviewTarget(["a"], "a", [], false)).toBeUndefined();
  });
});
