import { beforeEach, it, expect, vi } from "vitest";
import { reactive } from "vue";
const mocks = vi.hoisted(() => ({
  list: vi.fn(),
  save: vi.fn(),
  update: vi.fn(),
  remove: vi.fn(),
  confirm: vi.fn(),
}));
const user = reactive({ user: { id: "u" } });
vi.mock("@/stores/user", () => ({ useUserStore: () => user }));
vi.mock("ant-design-vue", () => ({
  Modal: { confirm: mocks.confirm },
  message: { success: vi.fn(), error: vi.fn() },
}));
vi.mock("@/components/TestCase/TestCaseFilter.vue", () => ({
  default: { render: () => null },
}));
import Filters from "./WorkspaceAdvancedFilters.vue";
import { componentHost, flushComponent as flush } from "@/test/componentHost";
const view = {
  id: "v",
  name: "View",
  filters: {
    filterConditions: [
      { field: "ownerId", operator: "equals", value: "CURRENT_USER" },
    ],
    filterLogic: "and",
  },
};
const props = () => ({
  projectId: "p",
  namespace: "plan-index",
  label: "计划视图",
  modules: [],
  logic: "and",
  busy: false,
  api: {
    listing: mocks.list,
    save: mocks.save,
    update: mocks.update,
    remove: mocks.remove,
  },
  loadFields: vi
    .fn()
    .mockResolvedValue([{ key: "name", label: "名称", type: "text" }]),
});
beforeEach(() => {
  vi.clearAllMocks();
  user.user = { id: "u" };
  mocks.list.mockResolvedValue([view]);
  mocks.save.mockResolvedValue({ ...view, id: "new" });
  mocks.update.mockResolvedValue({ ...view, name: "Renamed" });
});
it("personal save preserves only explicit visible conditions and invalidates older GET acknowledgements", async () => {
  const h = componentHost(Filters, props());
  await flush();
  let finish!: (v: any) => void;
  mocks.list.mockReturnValueOnce(new Promise((r) => (finish = r)));
  const old = h.state.loadViews();
  await flush();
  const rows = [
    { field: "ownerId", operator: "equals", value: "CURRENT_USER" },
  ];
  await h.state.saveView("New", rows, "or", "create");
  finish([]);
  await old;
  expect(mocks.save).toHaveBeenCalledWith("p", "New", {
    filterConditions: rows,
    filterLogic: "or",
  });
  expect(h.state.views.map((v: any) => v.id)).toContain("new");
  expect(h.state.viewLoading).toBe(false);
  h.stop();
});
it.each(["project", "actor", "namespace"])(
  "old private write ACKs cannot populate a %s scope after ABA",
  async (dimension) => {
    const h = componentHost(Filters, props());
    await flush();
    let finish!: (v: any) => void;
    mocks.save.mockReturnValueOnce(new Promise((r) => (finish = r)));
    const saved = h.state.saveView("Old", [], "and", "create");
    const rejected = expect(saved).rejects.toThrow("切换");
    await flush();
    if (dimension === "project") h.props.projectId = "q";
    else if (dimension === "namespace") h.props.namespace = "reports";
    else user.user = { id: "v" };
    await flush();
    if (dimension === "project") h.props.projectId = "p";
    else if (dimension === "namespace") h.props.namespace = "plan-index";
    else user.user = { id: "u" };
    await flush();
    finish({ ...view, id: "stale" });
    await rejected;
    expect(h.state.views.map((v: any) => v.id)).not.toContain("stale");
    h.stop();
  },
);
it("failed rename preserves its draft and old unmounted delete confirmation cannot make requests", async () => {
  const h = componentHost(Filters, props());
  await flush();
  h.state.rename(view);
  h.state.renameName = "Draft";
  mocks.update.mockRejectedValueOnce(new Error("offline"));
  await h.state.saveName();
  expect(h.state.renameName).toBe("Draft");
  expect(h.state.renameOpen).toBe(true);
  expect(h.state.renameError).toContain("草稿保留");
  h.state.renameOpen = false;
  h.state.remove(view);
  const confirm = mocks.confirm.mock.calls[0][0];
  h.stop();
  await expect(confirm.onOk()).rejects.toThrow();
  expect(mocks.remove).not.toHaveBeenCalled();
});
it("draft cancellation preserves editor contents and blocks view application", async () => {
  const h = componentHost(Filters, props());
  await flush();
  h.state.visible = true;
  h.state.filterEditor = { beforeClose: vi.fn().mockResolvedValue(false) };
  await h.state.selectView("system:all");
  expect(h.state.visible).toBe(true);
  h.state.filterEditor = { beforeClose: vi.fn().mockResolvedValue(true) };
  expect(await h.state.beforeClose()).toBe(true);
  h.stop();
});
