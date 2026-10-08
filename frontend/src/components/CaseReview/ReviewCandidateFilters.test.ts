import { beforeEach, afterEach, it, expect, vi } from "vitest";
const mocks = vi.hoisted(() => ({
  views: vi.fn(),
  save: vi.fn(),
  update: vi.fn(),
  remove: vi.fn(),
  confirm: vi.fn(),
}));
vi.mock("@/api/reviewWorkspace", () => ({
  reviewWorkspaceApi: {
    candidateViews: mocks.views,
    saveCandidateView: mocks.save,
    updateCandidateView: mocks.update,
    deleteCandidateView: mocks.remove,
  },
}));
vi.mock("@/api/caseFeatures", () => ({
  caseFeaturesApi: { templates: vi.fn().mockResolvedValue([]) },
}));
vi.mock("@/api/caseGovernance", () => ({
  caseGovernanceApi: { reviewers: vi.fn().mockResolvedValue([]) },
}));
vi.mock("@/stores/user", () => ({
  useUserStore: () => ({ user: { id: "u" } }),
}));
vi.mock("ant-design-vue", () => ({
  Modal: { confirm: mocks.confirm },
  message: { success: vi.fn(), error: vi.fn() },
}));
vi.mock("@/components/TestCase/TestCaseFilter.vue", () => ({
  default: { render: () => null },
}));
import Filters from "./ReviewCandidateFilters.vue";
import { componentHost, flushComponent as flush } from "@/test/componentHost";
const view = {
  id: "v",
  name: "View",
  filters: {
    filterConditions: [{ field: "name", operator: "contains", value: "base" }],
    filterLogic: "and",
  },
};
beforeEach(() => {
  vi.clearAllMocks();
  mocks.views.mockResolvedValue([view]);
  mocks.save.mockResolvedValue({ ...view, id: "new" });
  mocks.remove.mockResolvedValue(undefined);
});
afterEach(() => {
  vi.unstubAllGlobals();
});
it("unmounted delete confirmations cannot issue requests to the former project", async () => {
  const host = componentHost(Filters, {
    projectId: "p",
    modules: [],
    logic: "and",
    busy: false,
  });
  await flush();
  const s = host.state;
  mocks.confirm.mockReturnValue({ update: vi.fn() });
  s.remove(view);
  const confirmation = mocks.confirm.mock.calls[0][0];
  host.stop();
  await expect(confirmation.onOk()).rejects.toThrow();
  expect(mocks.remove).not.toHaveBeenCalled();
});
it("a pre-write list response cannot replace an acknowledged new personal view", async () => {
  let finish!: (rows: any[]) => void;
  mocks.views.mockReturnValueOnce(new Promise((resolve) => (finish = resolve)));
  const host = componentHost(Filters, {
    projectId: "p",
    modules: [],
    logic: "and",
    busy: false,
  });
  await flush();
  const s = host.state;
  await s.saveView("New", [], "and", "create");
  finish([]);
  await flush();
  expect(s.views.map((v: any) => v.id)).toEqual(["new"]);
  expect(s.viewLoading).toBe(false);
  host.stop();
});
it("reset and project changes cannot silently discard filter drafts or apply late saved views", async () => {
  const applied = vi.fn(),
    host = componentHost(Filters, {
      projectId: "p",
      modules: [],
      logic: "and",
      busy: false,
      viewId: "v",
      onApply: applied,
    });
  await flush();
  const s = host.state;
  s.visible = true;
  s.filterEditor = { beforeClose: vi.fn().mockResolvedValue(false) };
  await s.selectView("system:all");
  expect(applied).not.toHaveBeenCalled();
  expect(s.visible).toBe(true);
  let finish!: (v: any) => void;
  mocks.save.mockReturnValueOnce(new Promise((r) => (finish = r)));
  const write = s.saveView("New", [], "and", "create");
  await flush();
  host.props.projectId = "q";
  await flush();
  finish({ ...view, id: "late" });
  await expect(write).rejects.toThrow();
  expect(applied).not.toHaveBeenCalled();
  expect(s.views.some((v: any) => v.id === "late")).toBe(false);
  host.stop();
});
it("failed rename preserves draft and failed delete preserves the selected view", async () => {
  const host = componentHost(Filters, {
    projectId: "p",
    modules: [],
    logic: "and",
    busy: false,
    viewId: "v",
  });
  await flush();
  const s = host.state;
  s.rename(view);
  s.renameName = "Edited";
  mocks.update.mockRejectedValueOnce(Error("synthetic rename failure"));
  await s.saveName();
  expect(s.renameOpen).toBe(true);
  expect(s.renameName).toBe("Edited");
  expect(s.renameError).toContain("草稿");
  mocks.confirm.mockReturnValue({ update: vi.fn() });
  mocks.remove.mockRejectedValueOnce(Error("synthetic delete failure"));
  s.remove(view);
  await expect(mocks.confirm.mock.calls[0][0].onOk()).rejects.toThrow();
  expect(s.views.map((v: any) => v.id)).toContain("v");
  expect(s.saving).toBe(false);
  host.stop();
});
