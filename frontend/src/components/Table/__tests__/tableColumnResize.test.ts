import { afterEach, describe, expect, it, vi } from "vitest";
import { effectScope, ref } from "vue";
import { normalizeDisplay, resizableColumn } from "../tableDisplay";
import { useTableColumnResize } from "../useTableColumnResize";

const definitions = [
  { key: "id", title: "ID", required: true },
  { key: "name", title: "名称" },
  { key: "tags", title: "标签" },
];
afterEach(() => { vi.useRealTimers(); });
describe("列宽持久化与上下文隔离", () => {
  it("旧配置保持默认宽，非法宽度不会进入表格，必选列和标签遵循最小宽度", () => {
    for (const width of [undefined, "200", NaN, Infinity, -1, 0]) {
      const next = normalizeDisplay(
        { columns: [{ key: "id", visible: false, width }] },
        definitions,
      );
      expect(next.columns[0]).toEqual({ key: "id", visible: true });
      expect(
        resizableColumn({ key: "id", width: 100 }, next.columns[0]).width,
      ).toBe(100);
    }
    const next = normalizeDisplay(
      {
        columns: [
          { key: "tags", visible: false, width: 100 },
          { key: "id", visible: true, width: 20 },
        ],
      },
      definitions,
    );
    expect(next.columns.find((c) => c.key === "id")?.width).toBe(80);
    expect(next.columns.find((c) => c.key === "tags")).toEqual({
      key: "tags",
      visible: false,
      width: 216,
    });
    expect(
      normalizeDisplay(
        JSON.parse(JSON.stringify({ ...next, pageSize: 50 })),
        definitions,
      ),
    ).toEqual({ ...next, pageSize: 50 });
  });
  it("连续拖动合并多个字段与最新显隐设置，离开页面保存最后宽度", () => {
    vi.useFakeTimers();
    const scope = effectScope(),
      display = ref(normalizeDisplay(undefined, definitions)),
      key = ref("项目甲");
    const persist = vi.fn((next) => {
      display.value = normalizeDisplay(next, definitions);
      return true;
    });
    const resize = scope.run(() =>
      useTableColumnResize(display, key, persist),
    )!;
    resize(120, { key: "id" });
    resize(240, { key: "name" });
    resize(320, { key: "tags" });
    display.value.columns[1].visible = false;
    vi.advanceTimersByTime(200);
    expect(display.value.columns).toEqual([
      { key: "id", visible: true, width: 120 },
      { key: "name", visible: false, width: 240 },
      { key: "tags", visible: true, width: 320 },
    ]);
    resize(260, { key: "name" });
    resize(280, { key: "name" });
    scope.stop();
    expect(display.value.columns[1].width).toBe(280);
  });
  it("切换项目立即取消旧列宽，保存失败不修改已保存状态，未知列及非法事件不写存储", () => {
    vi.useFakeTimers();
    const scope = effectScope(),
      display = ref(normalizeDisplay(undefined, definitions)),
      key = ref("项目甲");
    const persist = vi.fn((next) => {
      display.value = next;
      return true;
    });
    const resize = scope.run(() =>
      useTableColumnResize(display, key, persist),
    )!;
    resize(120, { key: "id" });
    resize(260, { key: "name" });
    key.value = "项目乙";
    display.value = normalizeDisplay(undefined, definitions);
    vi.advanceTimersByTime(300);
    expect(persist).toHaveBeenCalledTimes(1);
    expect(display.value).toEqual(normalizeDisplay(undefined, definitions));
    persist.mockImplementation(() => false);
    resize(260, { key: "name" });
    expect(display.value.columns[1].width).toBeUndefined();
    resize(Infinity, { key: "id" });
    resize(-1, { key: "id" });
    resize(200, { key: "操作选择列" });
    scope.stop();
    expect(persist).toHaveBeenCalledTimes(2);
  });
});
