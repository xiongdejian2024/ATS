import { describe, it, expect, vi } from "vitest";
vi.mock("vue-draggable-plus", () => ({ VueDraggable: { render: () => null } }));
import TableDisplaySettings from "./TableDisplaySettings.vue";
import { componentHost, flushComponent as flush } from "@/test/componentHost";

describe("列设置在目录重读时保留草稿", () => {
  it("同次打开中字段消失后恢复保留未保存顺序/宽度/显示；重开清除旧草稿", async () => {
    const base = { key: "id", title: "ID", required: true },
      a = { key: "customFields.a", title: "A" },
      b = { key: "customFields.b", title: "B" };
    const initial = [
      { key: "id", visible: true },
      { key: "customFields.a", visible: true, width: 200 },
      { key: "customFields.b", visible: true, width: 250 },
    ];
    const close = vi.fn();
    const {
      state: s,
      props,
      stop,
    } = componentHost(TableDisplaySettings, {
      open: true,
      definitions: [base, a, b],
      columns: initial,
      pageSize: 20,
      includeDescendants: true,
      onClose: close,
    });
    s.movable = [
      { key: "customFields.b", visible: true, width: 300 },
      { key: "customFields.a", visible: false, width: 400 },
    ];
    props.definitions = [base, b];
    props.columns = [initial[0], initial[2]];
    await flush();
    expect(s.movable).toEqual([
      { key: "customFields.b", visible: true, width: 300 },
    ]);
    s.closeDrawer();
    expect(close.mock.calls[0][0]).toContainEqual({
      key: "customFields.a",
      visible: false,
      width: 400,
    });
    props.definitions = [base, a, b];
    props.columns = initial;
    await flush();
    expect(s.movable).toEqual([
      { key: "customFields.b", visible: true, width: 300 },
      { key: "customFields.a", visible: false, width: 400 },
    ]);
    expect(s.changed).toBe(true);
    props.open = false;
    await flush();
    props.open = true;
    await flush();
    expect(s.movable).toEqual(initial.slice(1));
    expect(s.changed).toBe(false);
    stop();
  });
  it("字段目录变化保留已有拖动/显示草稿，新增字段采用持久化偏好", async () => {
    const definitions = [
      { key: "id", title: "ID", required: true },
      { key: "customFields.a", title: "A", defaultVisible: false },
    ];
    const {
      state: s,
      props,
      stop,
    } = componentHost(TableDisplaySettings, {
      open: true,
      definitions,
      columns: [
        { key: "id", visible: true },
        { key: "customFields.a", visible: true, width: 200 },
      ],
      pageSize: 20,
      includeDescendants: true,
    });
    s.movable[0].visible = false;
    props.columns = [
      { key: "id", visible: true },
      { key: "customFields.a", visible: true, width: 200 },
      { key: "customFields.b", visible: true, width: 300 },
    ];
    props.definitions = [
      ...definitions,
      { key: "customFields.b", title: "B", defaultVisible: false },
    ];
    await flush();
    expect(s.movable).toEqual([
      { key: "customFields.a", visible: false, width: 200 },
      { key: "customFields.b", visible: true, width: 300 },
    ]);
    expect(s.changed).toBe(true);
    s.movable[0].visible = true;
    expect(s.changed).toBe(false);
    stop();
  });
});
