import { describe, it, expect, vi } from "vitest";
import {
  blankParam,
  readParams,
  filledParams,
  validParams,
  batchParams,
  paramCount,
} from "../nativeRequestParams";
describe("请求参数表数据与旧配置兼容", () => {
  it("保留旧键值、空值、Unicode及新的启停/顺序/描述", () => {
    expect(
      readParams('{"中文":"","second":"a:b"}').map((r) => [r.key, r.value]),
    ).toEqual([
      ["中文", ""],
      ["second", "a:b"],
    ]);
    const rows = [
      { ...blankParam(), key: "off", enable: false, description: "保留说明" },
      { ...blankParam(), key: "on", value: "实际值" },
    ];
    expect(readParams(JSON.stringify(rows))).toEqual(rows);
    expect(paramCount(JSON.stringify(rows))).toBe(1);
    expect(filledParams([...rows, blankParam()])).toEqual(rows);
  });
  it("启用名称重复、非法长度、半填写参数拒绝，禁用重复项保留", () => {
    expect(() =>
      validParams(
        [
          { ...blankParam(), key: "X" },
          { ...blankParam(), key: "x" },
        ],
        true,
      ),
    ).toThrow("重复");
    expect(
      validParams([
        { ...blankParam(), key: "x" },
        { ...blankParam(), key: "x", enable: false },
      ]),
    ).toHaveLength(2);
    expect(() => validParams([{ ...blankParam(), value: "未命名" }])).toThrow(
      "名称",
    );
    expect(() =>
      validParams([{ ...blankParam(), key: "q", lengthRange: [3, 2] }]),
    ).toThrow("长度");
    expect(() => readParams('{"q":1}')).toThrow("字符串");
  });
  it("批量文本保留值中的冒号，错误不产生半成品", () => {
    expect(
      batchParams("X-One: one\nX-Url: https://example.test/a:b", true).map(
        (r) => r.value,
      ),
    ).toEqual(["one", "https://example.test/a:b"]);
    expect(() => batchParams("合法:值\n错误行")).toThrow("格式");
    const log = vi.spyOn(console, "error").mockImplementation(() => {});
    expect(paramCount("{invalid")).toBe(0);
    expect(log).toHaveBeenCalledWith("请求参数徽标计算失败", expect.any(Error));
    log.mockRestore();
  });
});
