import { it, expect, vi, beforeEach, afterEach } from "vitest";
import { reactive } from "vue";
const mocks = vi.hoisted(() => ({
  list: vi.fn(),
  push: vi.fn(),
  guard: vi.fn(),
  success: vi.fn(),
  saveModule: vi.fn(),
}));
const project = reactive({
  currentProject: { id: "p", name: "Project" },
  projects: [{ id: "p", name: "Project" }],
  fetchProjects: vi.fn(),
  setCurrentProject: vi.fn(),
});
const user = reactive({ user: { id: "u" } });
vi.mock("@/stores/project", () => ({ useProjectStore: () => project }));
vi.mock("@/stores/user", () => ({ useUserStore: () => user }));
vi.mock("@/api/reviewWorkspace", () => ({
  reviewWorkspaceApi: { list: mocks.list, saveModule: mocks.saveModule },
}));
vi.mock("@/api/caseGovernance", () => ({
  caseGovernanceApi: { reviewers: vi.fn().mockResolvedValue([]) },
}));
vi.mock("@/components/CaseReview/ReviewCandidateFilters.vue", () => ({
  default: { render: () => null },
}));
vi.mock("@/components/Table/TableDisplaySettings.vue", () => ({
  default: { render: () => null },
}));
vi.mock("ant-design-vue", () => ({
  message: { success: mocks.success, warning: vi.fn() },
  Modal: { confirm: vi.fn() },
}));
vi.mock("@vueuse/core", () => ({
  useWindowSize: () => ({ width: { value: 1200 } }),
}));
vi.mock("vue-router", () => ({
  useRoute: () => ({ query: {} }),
  useRouter: () => ({ push: mocks.push }),
  onBeforeRouteLeave: mocks.guard,
}));
import Reviews from "./CaseReviews.vue";
import { componentHost, flushComponent as flush } from "@/test/componentHost";
const result = (name: string) => ({
  items: [{ id: name, name, lifecycle: "prepared", archived: false }],
  total: 1,
  page: 1,
  size: 20,
  modules: [],
  defaultCount: 1,
  allCount: 1,
  permissions: { update: false, delete: false },
});
beforeEach(() => {
  vi.clearAllMocks();
  project.currentProject = { id: "p", name: "Project" };
  user.user = { id: "u" };
  mocks.list.mockResolvedValue(result("current"));
  vi.stubGlobal("localStorage", {
    getItem: vi.fn().mockReturnValue(null),
    setItem: vi.fn(),
  });
});
afterEach(() => {
  vi.unstubAllGlobals();
});
it("actual review-page advanced selection clears hidden basic filters and sends scope independently", async () => {
  const host = componentHost(Reviews, {});
  await flush();
  const s = host.state,
    conditions = [{ field: "tags", operator: "contains", value: "回归" }];
  s.search = "hidden";
  s.lifecycle = "archived";
  s.selectedModule = "old";
  s.applyAdvanced(conditions, "or", "v", false, "reviewByMe");
  await flush();
  const params = mocks.list.mock.calls.at(-1)![1];
  expect(JSON.parse(params.filters)).toEqual({ conditions, logic: "or" });
  expect(params.scope).toBe("reviewByMe");
  expect(params.search).toBe("");
  expect(params.lifecycle).toBeUndefined();
  expect(params.moduleId).toBeUndefined();
  host.stop();
});
it("actor/project changes invalidate old list writes and restore only their scoped table settings", async () => {
  const host = componentHost(Reviews, {});
  await flush();
  const s = host.state;
  let finish!: (data: any) => void;
  mocks.list.mockReturnValueOnce(new Promise((r) => (finish = r)));
  void s.load();
  await flush();
  user.user = { id: "new-user" };
  await flush();
  finish(result("stale-user"));
  await flush();
  expect(s.data.items[0].name).toBe("current");
  s.applyAdvanced([], "and", "private", false, "createByMe");
  await flush();
  project.currentProject = { id: "q", name: "Other" };
  await flush();
  expect(s.conditions).toBeUndefined();
  expect(s.viewId).toBeUndefined();
  expect(s.scope).toBe("all");
  expect(s.displayKey).toContain("new-user");
  expect(s.displayKey).toContain("q");
  host.stop();
});
it("filter draft cancellation blocks system scope changes, detail navigation and route leave", async () => {
  const host = componentHost(Reviews, {});
  await flush();
  const s = host.state;
  s.filterEditor = { beforeClose: vi.fn().mockResolvedValue(false) };
  await s.changeScope("reviewByMe");
  expect(s.scope).toBe("all");
  await s.openWorkspace("r");
  expect(mocks.push).not.toHaveBeenCalled();
  expect(await mocks.guard.mock.calls[0][0]()).toBe(false);
  s.filterEditor = { beforeClose: vi.fn().mockResolvedValue(true) };
  await s.changeScope("createByMe");
  expect(s.scope).toBe("createByMe");
  await s.openWorkspace("r");
  expect(mocks.push).toHaveBeenCalledOnce();
  host.stop();
});
it.each(["project", "actor"])(
  "a %s round trip cannot acknowledge old writes or unlock a new module save",
  async (change) => {
    let oldDone!: (value: any) => void, newDone!: (value: any) => void;
    mocks.saveModule
      .mockReturnValueOnce(new Promise((r) => (oldDone = r)))
      .mockReturnValueOnce(new Promise((r) => (newDone = r)));
    const host = componentHost(Reviews, {});
    await flush();
    const s = host.state;
    s.moduleName = "Old";
    s.moduleVisible = true;
    const old = s.saveModule();
    await flush();
    if (change === "project")
      project.currentProject = { id: "q", name: "Other" };
    else user.user = { id: "v" };
    await flush();
    if (change === "project")
      project.currentProject = { id: "p", name: "Project" };
    else user.user = { id: "u" };
    await flush();
    s.moduleName = "New";
    s.moduleVisible = true;
    const current = s.saveModule();
    await flush();
    expect(s.mutating).toBe(true);
    oldDone({});
    await old;
    await flush();
    expect(s.mutating).toBe(true);
    expect(s.moduleVisible).toBe(true);
    expect(mocks.success).not.toHaveBeenCalled();
    newDone({});
    await current;
    expect(s.mutating).toBe(false);
    expect(s.moduleVisible).toBe(false);
    host.stop();
  },
);
it("route leave rechecks locks after an awaited filter closing decision", async () => {
  const host = componentHost(Reviews, {});
  await flush();
  const s = host.state;
  let finish!: (value: boolean) => void;
  s.filterEditor = {
    beforeClose: vi.fn().mockReturnValue(new Promise((r) => (finish = r))),
  };
  const leaving = mocks.guard.mock.calls[0][0]();
  await flush();
  s.mutating = true;
  finish(true);
  expect(await leaving).toBe(false);
  host.stop();
});
