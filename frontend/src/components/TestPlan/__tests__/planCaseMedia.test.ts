import { describe, expect, it } from "vitest";
import { privateImagePath } from "@/api/planCaseMedia";

describe("私有图片登录凭据的路由边界", () => {
  const path =
    "/api/v1/plan-orchestration/plans/plan-1/execution-media/01234567-89ab-cdef-0123-456789abcdef/preview";
  it("规范私有路由移除API前缀，保持原计划和图片编号", () => {
    expect(privateImagePath(path)).toBe(path.slice("/api/v1".length));
  });
  it("外域、协议相对地址、目录穿越及伪装查询不能获得登录凭据", () => {
    for (const source of [
      "https://example.test" + path,
      "//example.test" + path,
      path + "?redirect=other",
      path.replace("plan-1", ".."),
      path.replace("/preview", "/download"),
      path.replace("01234567-89ab-cdef-0123-456789abcdef", "other"),
      "data:image/png;base64,x",
    ]) {
      expect(privateImagePath(source)).toBeUndefined();
    }
  });
});
