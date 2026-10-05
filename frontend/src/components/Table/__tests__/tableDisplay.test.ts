import { describe, it, expect, vi } from "vitest";
import {
  normalizeDisplay,
  readDisplay,
  displayStorageKey,
} from "../tableDisplay";
const definitions = [
  { key: "id", title: "ID", required: true },
  { key: "name", title: "名称", required: true },
  { key: "tags", title: "标签" },
  { key: "project", title: "所属项目", defaultVisible: false },
];
describe("表格偏好的版本与隔离", () => {
  it("旧配置保留用户顺序和隐藏状态，补新字段，删除废弃和重复字段，必选列不能隐藏或拖走", () => {
    const state = normalizeDisplay(
      {
        columns: [
          { key: "project", visible: true },
          { key: "id", visible: false },
          { key: "tags", visible: false },
          { key: "tags", visible: true },
          { key: "废弃字段", visible: true },
        ],
        pageSize: 50,
        includeDescendants: false,
      },
      [...definitions, { key: "new", title: "新列" }],
    );
    expect(state.columns).toEqual([
      { key: "id", visible: true },
      { key: "name", visible: true },
      { key: "project", visible: true },
      { key: "tags", visible: false },
      { key: "new", visible: true },
    ]);
    expect(state.pageSize).toBe(50);
    expect(state.includeDescendants).toBe(false);
  });
  it("畸形存储内容、非法每页数量和非布尔开关不会进入表格", () => {
    const state = normalizeDisplay(
      {
        columns: [null, 1, { key: "tags", visible: "false" }],
        pageSize: -1,
        includeDescendants: "false",
      },
      definitions,
    );
    expect(state).toEqual(normalizeDisplay(undefined, definitions));
    expect(
      state.columns.find((column) => column.key === "project")?.visible,
    ).toBe(false);
  });
  it("读取损坏JSON或存储访问异常记录完整错误并回退，不执行保存的字符串", () => {
    const log = vi.spyOn(console, "error").mockImplementation(() => {});
    try {
      expect(
        readDisplay({ getItem: () => "损坏JSON" }, "k", definitions),
      ).toEqual(normalizeDisplay(undefined, definitions));
      const error = new Error("浏览器拒绝访问存储");
      readDisplay(
        {
          getItem: () => {
            throw error;
          },
        },
        "k",
        definitions,
      );
      expect(log).toHaveBeenLastCalledWith(
        "读取表格显示配置失败，使用默认显示",
        error,
      );
    } finally {
      log.mockRestore();
    }
  });
  it("用户、项目和表格分别隔离，编号中的分隔符不会造成键碰撞", () => {
    expect(
      new Set([
        displayStorageKey("甲", "项目", "功能"),
        displayStorageKey("乙", "项目", "功能"),
        displayStorageKey("甲", "另项目", "功能"),
        displayStorageKey("甲", "项目", "场景"),
        displayStorageKey("甲:项目", "另项目", "功能"),
        displayStorageKey("甲", "项目:另项目", "功能"),
      ]).size,
    ).toBe(6);
  });
});
