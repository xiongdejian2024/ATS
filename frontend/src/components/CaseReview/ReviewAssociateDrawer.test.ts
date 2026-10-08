import { beforeEach, afterEach, it, expect, vi } from "vitest";
const mocks = vi.hoisted(() => ({
  candidates: vi.fn(),
  select: vi.fn(),
  user: { id: "u" },
}));
vi.mock("@/api/reviewWorkspace", () => ({
  reviewWorkspaceApi: {
    candidates: mocks.candidates,
    selectCandidates: mocks.select,
  },
}));
vi.mock("@/api/caseGovernance", () => ({
  caseGovernanceApi: {
    reviewers: vi.fn().mockResolvedValue([]),
    selectionMembership: vi.fn().mockResolvedValue({ caseIds: [] }),
  },
}));
vi.mock("@/stores/user", () => ({
  useUserStore: () => ({ user: mocks.user }),
}));
vi.mock("ant-design-vue", () => ({
  message: { success: vi.fn(), error: vi.fn() },
}));
vi.mock("./ReviewCandidateFilters.vue", () => ({
  default: { render: () => null },
}));
vi.mock("@/components/Table/TableDisplaySettings.vue", () => ({
  default: { render: () => null },
}));
import Drawer from "./ReviewAssociateDrawer.vue";
import { componentHost, flushComponent as flush } from "@/test/componentHost";
const result = (id: string) => ({
  items: [{ id, name: id }],
  total: 1,
  modules: [],
});
beforeEach(() => {
  vi.clearAllMocks();
  vi.stubGlobal("localStorage", {
    getItem: vi.fn().mockReturnValue(null),
    setItem: vi.fn(),
  });
  mocks.candidates.mockResolvedValue(result("initial"));
  mocks.select.mockResolvedValue({ caseIds: ["found"] });
});
afterEach(() => { vi.unstubAllGlobals(); });
it("advanced paged read and select-all carry identical conditions while selection stays explicit", async () => {
  const host = componentHost(Drawer, {
    open: true,
    projectId: "p",
    defaultReviewers: [],
    excluded: ["existing"],
    availableReviewers: [],
  });
  await flush();
  const s = host.state,
    conditions = [{ field: "customFields.zero", operator: "equals", value: 0 }];
  s.search = "old search";
  s.folder = "old folder";
  s.applyFilters(conditions, "or", "v");
  await flush();
  expect(JSON.parse(mocks.candidates.mock.calls.at(-1)![1].filters)).toEqual({
    conditions,
    logic: "or",
  });
  s.selected = new Set(["selected"]);
  await s.selectAll();
  expect(mocks.select.mock.calls[0][1]).toMatchObject({
    filters: { conditions, logic: "or" },
    mine: false,
    excludeIds: ["existing", "selected"],
  });
  expect([...s.selected]).toEqual(["selected", "found"]);
  host.stop();
});
it("late project reads/selections and save failures preserve only the current draft", async () => {
  const host = componentHost(Drawer, {
    open: true,
    projectId: "p",
    defaultReviewers: [],
    excluded: [],
    availableReviewers: [],
  });
  await flush();
  const s = host.state;
  let finish!: (value: any) => void;
  mocks.candidates.mockReturnValueOnce(new Promise((r) => (finish = r)));
  void s.load();
  await flush();
  host.props.projectId = "q";
  await flush();
  finish(result("stale"));
  await flush();
  expect(s.data.items[0].id).toBe("initial");
  let picked!: (value: any) => void;
  mocks.select.mockReturnValueOnce(new Promise((r) => (picked = r)));
  void s.selectAll();
  await flush();
  host.props.projectId = "r";
  await flush();
  picked({ caseIds: ["old-project"] });
  await flush();
  expect([...s.selected]).toEqual([]);
  s.selected = new Set(["retry"]);
  s.reviewers = ["reviewer"];
  host.props.saveSelection = vi
    .fn()
    .mockRejectedValue(new Error("synthetic failure"));
  await flush();
  await s.confirm();
  expect([...s.selected]).toEqual(["retry"]);
  expect(s.saveError).toContain("关联失败");
  host.stop();
});
it("closing and submission await child draft guards and failed settings do not switch page", async () => {
  const closed = vi.fn(),
    save = vi.fn().mockResolvedValue(undefined);
  const host = componentHost(Drawer, {
    open: true,
    projectId: "p",
    defaultReviewers: [],
    excluded: [],
    availableReviewers: [],
    "onUpdate:open": closed,
    saveSelection: save,
  });
  await flush();
  const s = host.state;
  s.filterEditor = { beforeClose: vi.fn().mockResolvedValue(false) };
  await s.close();
  expect(closed).not.toHaveBeenCalled();
  s.selected = new Set(["case"]);
  s.reviewers = ["reviewer"];
  await s.confirm();
  expect(save).not.toHaveBeenCalled();
  vi.mocked(localStorage.setItem).mockImplementationOnce(() => {
    throw Error("quota");
  });
  s.tableChange({ current: 2, pageSize: 30 });
  expect(s.page).toBe(1);
  expect(s.size).toBe(20);
  expect(s.settingsError).toContain("保留");
  s.filterEditor = { beforeClose: vi.fn().mockResolvedValue(true) };
  await s.confirm();
  expect(save).toHaveBeenCalledTimes(1);
  expect(closed).toHaveBeenCalledWith(false);
  host.stop();
});
