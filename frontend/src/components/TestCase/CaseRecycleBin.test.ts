import { beforeEach, describe, it, expect, vi } from "vitest";
const mocks = vi.hoisted(() => ({
  recycle: vi.fn(),
  restore: vi.fn(),
  purge: vi.fn(),
  templates: vi.fn(),
  fields: vi.fn(),
  reviewers: vi.fn(),
  modules: vi.fn(),
  error: vi.fn(),
  warning: vi.fn(),
  account: { user: { id: "user" } },
}));
vi.mock("@/api/caseFeatures", () => ({ caseFeaturesApi: mocks }));
vi.mock("@/api/testCase", () => ({
  testCaseApi: { getFilterFields: mocks.fields },
}));
vi.mock("@/api/caseGovernance", () => ({
  caseGovernanceApi: { reviewers: mocks.reviewers },
}));
vi.mock("@/api/project", () => ({ projectApi: { getModules: mocks.modules } }));
vi.mock("@/stores/user", async () => {
  const { reactive } = await import("vue");
  return { useUserStore: () => reactive(mocks.account) };
});
vi.mock("ant-design-vue", () => ({
  Drawer: "aside",
  Modal: { confirm: vi.fn() },
  message: { error: mocks.error, warning: mocks.warning, success: vi.fn() },
}));
vi.mock("vue-router", () => ({
  onBeforeRouteLeave: vi.fn(),
  onBeforeRouteUpdate: vi.fn(),
}));
import CaseRecycleBin from "./CaseRecycleBin.vue";
import { componentHost, flushComponent as flush } from "@/test/componentHost";
beforeEach(() => {
  vi.clearAllMocks();
  vi.stubGlobal("localStorage", { getItem: vi.fn(), setItem: vi.fn() });
  vi.stubGlobal("window", {
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
  });
  mocks.recycle.mockResolvedValue({ items: [], total: 0 });
  mocks.fields.mockResolvedValue([
    { fieldKey: "name", fieldLabel: "名称", fieldType: "text" },
  ]);
  mocks.templates.mockResolvedValue([
    { fields: [{ key: "platform", name: "平台", type: "text", options: [] }] },
  ]);
  mocks.reviewers.mockResolvedValue([]);
  mocks.modules.mockResolvedValue({
    modules: [
      { id: "parent", name: "父" },
      { id: "child", name: "子", parentId: "parent" },
    ],
  });
});
describe("回收站高级筛选、列和请求隔离", () => {
  it("同tick修改列后切项目/用户不覆盖目标范围的已保存设置", async () => {
    mocks.account.user.id = "user";
    const saved = new Map([
      [
        "ats.recycle.columns.v1.user.new",
        JSON.stringify(["caseCode", "deletedAt"]),
      ],
      [
        "ats.recycle.columns.v1.other.new",
        JSON.stringify(["name", "deletedAt"]),
      ],
    ]);
    vi.stubGlobal("localStorage", {
      getItem: (key: string) => saved.get(key) || null,
      setItem: (key: string, value: string) => saved.set(key, value),
    });
    const {
      state: s,
      props,
      stop,
    } = componentHost(CaseRecycleBin, { open: true, projectId: "old" });
    await flush();
    s.columnKeys = ["name", "priority"];
    props.projectId = "new";
    await flush();
    expect(s.columnKeys).toEqual(["caseCode", "deletedAt"]);
    expect(JSON.parse(saved.get("ats.recycle.columns.v1.user.new")!)).toEqual([
      "caseCode",
      "deletedAt",
    ]);
    expect(JSON.parse(saved.get("ats.recycle.columns.v1.user.old")!)).toEqual([
      "name",
      "priority",
    ]);
    s.columnKeys = ["priority"];
    s.user.user.id = "other";
    await flush();
    expect(s.columnKeys).toEqual(["name", "deletedAt"]);
    expect(JSON.parse(saved.get("ats.recycle.columns.v1.other.new")!)).toEqual([
      "name",
      "deletedAt",
    ]);
    stop();
    mocks.account.user.id = "user";
  });
  it("显示实际模块层级与自定义列，高级条件和排序传入回收站范围", async () => {
    const { state: s, stop } = componentHost(CaseRecycleBin, {
      open: true,
      projectId: "p",
    });
    await flush();
    expect(s.moduleTree[1].children[0].key).toBe("child");
    expect(s.filterFields.map((f: any) => f.key)).toContain("deletedAt");
    s.columnKeys = ["name", "customFields.platform"];
    expect(s.columns[1].dataIndex).toEqual(["customFields", "platform"]);
    s.applyFilters(
      [{ field: "name", operator: "contains", value: "回收" }],
      "or",
    );
    await flush();
    expect(JSON.parse(mocks.recycle.mock.calls.at(-1)![1].filters)).toEqual({
      conditions: [{ field: "name", operator: "contains", value: "回收" }],
      logic: "or",
    });
    s.tableChange({ current: 2 }, {}, { columnKey: "name", order: "ascend" });
    await flush();
    expect(mocks.recycle.mock.calls.at(-1)![1]).toMatchObject({
      page: 2,
      sort_by: "name",
      sort_order: "asc",
    });
    stop();
  });
  it("单项操作冻结项目和身份，迟到响应不污染新项目或解锁新项目的待写入", async () => {
    let oldFinish!: (v: any) => void, newFinish!: (v: any) => void;
    mocks.restore
      .mockReturnValueOnce(new Promise((r) => (oldFinish = r)))
      .mockReturnValueOnce(new Promise((r) => (newFinish = r)));
    const changed = vi.fn(),
      {
        state: s,
        props,
        stop,
      } = componentHost(CaseRecycleBin, {
        open: true,
        projectId: "old",
        onChanged: changed,
      });
    await flush();
    const old = s.restore("a");
    await s.purge("a");
    expect(mocks.purge).not.toHaveBeenCalled();
    props.projectId = "new";
    await flush();
    const latest = s.restore("b");
    oldFinish({});
    await old;
    expect(changed).not.toHaveBeenCalled();
    expect(s.mutating).toBe(true);
    expect(mocks.restore.mock.calls).toEqual([
      ["old", "a"],
      ["new", "b"],
    ]);
    newFinish({});
    await latest;
    expect(changed).toHaveBeenCalledTimes(1);
    stop();
  });
  it("部分批量失败保留失败选择，切项目清空筛选/显示并忽略旧读取", async () => {
    mocks.restore
      .mockResolvedValueOnce({})
      .mockRejectedValueOnce(new Error("synthetic"));
    const {
      state: s,
      props,
      stop,
    } = componentHost(CaseRecycleBin, { open: true, projectId: "old" });
    await flush();
    s.selectedIds = ["a", "b"];
    await s.batch("restore");
    expect(s.selectedIds).toEqual(["b"]);
    expect(mocks.warning).toHaveBeenCalled();
    let finish!: (v: any) => void;
    mocks.recycle.mockReturnValueOnce(new Promise((r) => (finish = r)));
    s.conditions = [{ field: "name", operator: "contains", value: "old" }];
    const pending = s.load();
    props.projectId = "new";
    await flush();
    finish({ items: [{ id: "old" }], total: 1 });
    await pending;
    expect(s.rows).toEqual([]);
    expect(s.conditions).toEqual([]);
    expect(s.selectedIds).toEqual([]);
    stop();
  });
});
