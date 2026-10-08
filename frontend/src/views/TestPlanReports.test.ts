import { it, expect, vi, beforeEach, afterEach } from "vitest";
import { reactive } from "vue";
const mocks = vi.hoisted(() => ({
  list: vi.fn(),
  rename: vi.fn(),
  remove: vi.fn(),
  push: vi.fn(),
  resolve: vi.fn(),
  confirm: vi.fn(),
  guard: vi.fn(),
  updateGuard: vi.fn(),
  success: vi.fn(),
  write: vi.fn(),
  read: vi.fn(),
}));
const project = reactive({ currentProject: { id: "p" } }),
  user = reactive({ user: { id: "u" } }),
  route = reactive({ query: {} as Record<string, string> });
vi.mock("@/stores/project", () => ({ useProjectStore: () => project }));
vi.mock("@/stores/user", () => ({ useUserStore: () => user }));
vi.mock("vue-router", () => ({
  useRoute: () => route,
  useRouter: () => ({ push: mocks.push, resolve: mocks.resolve }),
  onBeforeRouteLeave: mocks.guard,
  onBeforeRouteUpdate: mocks.updateGuard,
}));
vi.mock("ant-design-vue", () => ({
  message: { success: mocks.success, error: vi.fn(), warning: vi.fn() },
  Modal: { confirm: mocks.confirm },
}));
vi.mock("@/api/planReports", () => ({
  planReportsApi: {
    list: mocks.list,
    rename: mocks.rename,
    batchRemove: mocks.remove,
  },
  reportIndexViewApi: {},
  reportResultOptions: [],
  reportResultLabel: (s: string) => s,
  reportResultColor: () => "",
}));
vi.mock("@/api/planWorkspace", () => ({
  planWorkspaceApi: { members: vi.fn().mockResolvedValue([]) },
}));
vi.mock("@/components/Table/WorkspaceAdvancedFilters.vue", () => ({
  default: { render: () => null },
}));
vi.mock("@/components/Table/TableDisplaySettings.vue", () => ({
  default: { render: () => null },
}));
vi.mock("@/api/planCollaboration", () => ({ downloadPlanFile: vi.fn() }));
vi.mock("@/api/planGroup", () => ({ planGroupApi: { pdf: vi.fn() } }));
import Reports from "./TestPlanReports.vue";
import { componentHost, flushComponent as flush } from "@/test/componentHost";
const row = {
  id: "r",
  kind: "PLAN",
  sourceId: "plan",
  name: "Report",
  planName: "Plan",
  status: "completed",
  resultStatus: "passed",
  passRate: 100,
  triggerMode: "manual",
  executorId: "u",
  createUserName: "User",
  createTime: "2026-10-08",
};
const listing = (name = "Report") => ({
  items: [{ ...row, name }],
  total: 1,
  canRename: true,
  canDelete: true,
});
beforeEach(() => {
  vi.clearAllMocks();
  mocks.write.mockReset();
  project.currentProject = { id: "p" };
  user.user = { id: "u" };
  route.query = {};
  mocks.list.mockResolvedValue(listing());
  mocks.rename.mockResolvedValue({ name: "Saved" });
  mocks.remove.mockResolvedValue({ deleted: 1 });
  mocks.resolve.mockReturnValue({ href: "/report" });
  mocks.confirm.mockReturnValue({ update: vi.fn() });
  mocks.read.mockReturnValue(null);
  vi.stubGlobal("localStorage", { getItem: mocks.read, setItem: mocks.write });
});
afterEach(() => {
  vi.unstubAllGlobals();
});
it("applied advanced views clear hidden basics and type navigation remains an additional visible constraint", async () => {
  const h = componentHost(Reports, {});
  await flush();
  const s = h.state;
  s.search = "hidden";
  s.filters.operator = "hidden";
  s.filters.result_status = "failed";
  const conditions = [
    { field: "executorId", operator: "equals", value: "CURRENT_USER" },
  ];
  s.applyAdvanced(conditions, "or", "personal");
  await flush();
  expect(s.query).toEqual({
    filters: JSON.stringify({ conditions, logic: "or" }),
    kind: undefined,
  });
  expect(s.search).toBe("");
  expect(s.filters).toEqual({});
  await s.changeType("GROUP");
  await flush();
  expect(s.query.kind).toBe("GROUP");
  expect(s.advancedConditions).toEqual(conditions);
  expect(s.advancedViewId).toBeUndefined();
  h.stop();
});
it("cancelled filter/name drafts block type, report, paging and route transitions", async () => {
  const h = componentHost(Reports, {});
  await flush();
  const s = h.state;
  s.filterEditor = { beforeClose: vi.fn().mockResolvedValue(false) };
  await s.changeType("GROUP");
  await s.openReport(row);
  await s.tableChange({ current: 2, pageSize: 20 }, {}, {});
  expect(s.showType).toBe("ALL");
  expect(s.page).toBe(1);
  expect(mocks.push).not.toHaveBeenCalled();
  expect(await mocks.guard.mock.calls[0][0]()).toBe(false);
  expect(await mocks.updateGuard.mock.calls[0][0]()).toBe(false);
  s.filterEditor = { beforeClose: vi.fn().mockResolvedValue(true) };
  await s.beginRename(row);
  s.editName = "Draft";
  const close = s.openReport(row);
  await flush();
  mocks.confirm.mock.calls.at(-1)![0].onCancel();
  await close;
  expect(s.editing).toBe("PLAN:r");
  expect(s.editName).toBe("Draft");
  expect(mocks.push).not.toHaveBeenCalled();
  h.stop();
});
it("storage failures retain column draft and page, with a discard path back to unchanged settings", async () => {
  const h = componentHost(Reports, {});
  await flush();
  const s = h.state;
  s.settingsVisible = true;
  const old = JSON.parse(JSON.stringify(s.display.columns));
  const changed = old.map((c: any) =>
    c.key === "passRate" ? { ...c, visible: false, width: 299 } : c,
  );
  mocks.write.mockImplementationOnce(() => {
    throw new Error("full");
  });
  s.saveColumns(changed);
  expect(s.settingsVisible).toBe(true);
  expect(s.settingsError).not.toBe("");
  expect(s.display.columns).toEqual(old);
  mocks.write.mockImplementationOnce(() => {
    throw new Error("full");
  });
  await s.tableChange({ current: 2, pageSize: 100 }, {}, {});
  expect(s.page).toBe(1);
  s.saveColumns(old);
  expect(s.settingsVisible).toBe(false);
  expect(s.settingsError).toBe("");
  h.stop();
});
it("columns, widths and legacy hundred-row pages persist only in their actor/project namespace", async () => {
  const stored = {
    columns: [
      { key: "passRate", visible: false, width: 244 },
      { key: "name", visible: true, width: 344 },
    ],
    pageSize: 100,
  };
  mocks.read.mockImplementation((key: string) =>
    key.includes(":u:") ? JSON.stringify(stored) : null,
  );
  const h = componentHost(Reports, {});
  await flush();
  const s = h.state;
  expect(s.size).toBe(100);
  expect(s.columns.some((c: any) => c.key === "passRate")).toBe(false);
  expect(s.columns.find((c: any) => c.key === "name").width).toBe(344);
  user.user = { id: "v" };
  await flush();
  expect(s.size).toBe(20);
  expect(s.columns.some((c: any) => c.key === "passRate")).toBe(true);
  expect(s.displayKey).toContain(":v:");
  h.stop();
});
it.each(["project", "actor"])(
  "old %s write ACK cannot close a new rename or release its pending lock",
  async (dimension) => {
    const h = componentHost(Reports, {});
    await flush();
    const s = h.state;
    await s.beginRename(row);
    s.editName = "Old";
    let finish!: (v: any) => void;
    mocks.rename.mockReturnValueOnce(new Promise((r) => (finish = r)));
    const old = s.rename(row);
    await flush();
    if (dimension === "project") project.currentProject = { id: "q" };
    else user.user = { id: "v" };
    await flush();
    if (dimension === "project") project.currentProject = { id: "p" };
    else user.user = { id: "u" };
    await flush();
    await s.beginRename(row);
    s.editName = "New";
    let finishNew!: (v: any) => void;
    mocks.rename.mockReturnValueOnce(new Promise((r) => (finishNew = r)));
    const current = s.rename(row);
    await flush();
    finish({ name: "Old" });
    await old;
    expect(s.busy).toBe(true);
    expect(s.editing).toBe("PLAN:r");
    expect(s.editName).toBe("New");
    expect(mocks.success).not.toHaveBeenCalled();
    finishNew({ name: "New" });
    await current;
    expect(s.busy).toBe(false);
    h.stop();
  },
);
it("old deletion confirmation and list ACK cannot act after a returning project scope", async () => {
  const h = componentHost(Reports, {});
  await flush();
  const s = h.state;
  s.deleteOne(row);
  const confirm = mocks.confirm.mock.calls[0][0];
  let finish!: (v: any) => void;
  mocks.list.mockReturnValueOnce(new Promise((r) => (finish = r)));
  const old = s.load();
  await flush();
  project.currentProject = { id: "q" };
  await flush();
  project.currentProject = { id: "p" };
  await flush();
  finish(listing("Stale"));
  await old;
  expect(s.items[0].name).toBe("Report");
  await expect(confirm.onOk()).rejects.toThrow();
  expect(mocks.remove).not.toHaveBeenCalled();
  h.stop();
});
it("an ACK preserves a newer report-name draft and does not refresh it out of its current row", async () => {
  const h = componentHost(Reports, {});
  await flush();
  const s = h.state;
  await s.beginRename(row);
  s.editName = "Old";
  let finish!: (v: any) => void;
  mocks.rename.mockReturnValueOnce(new Promise((r) => (finish = r)));
  const old = s.rename(row);
  await flush();
  s.editName = "New";
  finish({ name: "Old" });
  await old;
  expect(s.editing).toBe("PLAN:r");
  expect(s.editName).toBe("New");
  expect(s.items[0].name).toBe("Old");
  expect(s.editBaseline).toBe("Old");
  h.stop();
});

it("paging and sorting do not depend on storage when the page size is unchanged", async () => {
  const h = componentHost(Reports, {});
  await flush();
  const s = h.state;
  mocks.write.mockImplementation(() => {
    throw new Error("disabled");
  });
  await s.tableChange(
    { current: 2, pageSize: 20 },
    {},
    { columnKey: "passRate", order: "ascend" },
  );
  await flush();
  expect(s.page).toBe(2);
  expect(s.sort).toBe("pass_rate");
  expect(s.direction).toBe("asc");
  expect(mocks.write).not.toHaveBeenCalled();
  await s.tableChange({ current: 3, pageSize: 100 }, {}, {});
  expect(s.page).toBe(2);
  expect(s.size).toBe(20);
  h.stop();
});

it.each([1, 2, 3, 4, 5])(
  "delete closing-decision tail with %s microtasks never sends under another actor",
  async (n) => {
    const h = componentHost(Reports, {});
    await flush();
    const s = h.state;
    s.deleteOne(row);
    const confirmation = mocks.confirm.mock.calls[0][0],
      actors: string[] = [];
    mocks.remove.mockImplementation(() => {
      actors.push(user.user.id);
      return Promise.resolve({ deleted: 1 });
    });
    s.filterEditor = {
      beforeClose: vi.fn(() =>
        Promise.resolve().then(() => {
          const step = (left: number): void =>
            queueMicrotask(() =>
              left > 1 ? step(left - 1) : (user.user = { id: "new" }),
            );
          step(n);
          return true;
        }),
      ),
    };
    try {
      await confirmation.onOk();
    } catch {}
    await flush();
    expect(actors.every((id) => id === "u")).toBe(true);
    h.stop();
  },
);
