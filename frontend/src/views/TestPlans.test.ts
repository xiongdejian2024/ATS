import { it, expect, vi, beforeEach } from "vitest";
import { reactive } from "vue";
const mocks = vi.hoisted(() => ({
  get: vi.fn(),
  groups: vi.fn(),
  clone: vi.fn(),
  remove: vi.fn(),
  save: vi.fn(),
  replace: vi.fn(),
  push: vi.fn(),
  confirm: vi.fn(),
  guard: vi.fn(),
  updateGuard: vi.fn(),
  success: vi.fn(),
}));
const project = reactive({
  currentProject: { id: "p" },
  projects: [{ id: "p", name: "P" }],
  fetchProjects: vi.fn(),
  setCurrentProject: vi.fn(),
});
const user = reactive({ user: { id: "u" } });
const route = reactive({ query: {} as Record<string, string> });
vi.mock("@/stores/project", () => ({ useProjectStore: () => project }));
vi.mock("@/stores/user", () => ({ useUserStore: () => user }));
vi.mock("@/api/testPlan", () => ({ testPlanApi: { getTestPlans: mocks.get } }));
vi.mock("@/api/planOrchestration", () => ({
  planOrchestrationApi: {
    groups: mocks.groups,
    cloneGroup: mocks.clone,
    deleteGroup: mocks.remove,
    createGroup: mocks.save,
  },
}));
vi.mock("@/api/planWorkspace", () => ({
  planWorkspaceApi: {
    modules: vi.fn().mockResolvedValue([]),
    members: vi.fn().mockResolvedValue([]),
  },
  planIndexViewApi: {},
}));
vi.mock("@/api/caseGovernance", () => ({
  caseGovernanceApi: { reviewers: vi.fn().mockResolvedValue([]) },
}));
vi.mock("vue-router", () => ({
  useRoute: () => route,
  useRouter: () => ({ replace: mocks.replace, push: mocks.push }),
  onBeforeRouteLeave: mocks.guard,
  onBeforeRouteUpdate: mocks.updateGuard,
}));
vi.mock("ant-design-vue", () => ({
  Modal: { confirm: mocks.confirm },
  message: { success: mocks.success, error: vi.fn(), warning: vi.fn() },
}));
vi.mock("@/components/TestPlan/TestPlanEdit.vue", () => ({
  default: { render: () => null },
}));
vi.mock("@/components/TestPlan/PlanWorkspaceToolbar.vue", () => ({
  default: { render: () => null },
}));
vi.mock("@/components/TestPlan/PlanGroupExecution.vue", () => ({
  default: { render: () => null },
}));
vi.mock("@/components/TestPlan/PlanNavigator.vue", () => ({
  default: { render: () => null },
}));
vi.mock("@/components/Table/WorkspaceAdvancedFilters.vue", () => ({
  default: { render: () => null },
}));
import Plans from "./TestPlans.vue";
import { componentHost, flushComponent as flush } from "@/test/componentHost";
const groups = [
  { id: "old", name: "Old", planCount: 1 },
  { id: "clicked", name: "Clicked", planCount: 0 },
];
beforeEach(() => {
  vi.clearAllMocks();
  project.currentProject = { id: "p" };
  user.user = { id: "u" };
  route.query = {};
  mocks.get.mockResolvedValue({
    items: [{ id: "current", name: "Current" }],
    total: 1,
  });
  mocks.groups.mockResolvedValue(groups);
  mocks.clone.mockResolvedValue({ id: "copied", name: "Copy" });
  mocks.remove.mockResolvedValue(undefined);
  mocks.save.mockResolvedValue({ id: "saved" });
});
it("advanced filters clear hidden basic conditions and group/module scopes", async () => {
  const h = componentHost(Plans, {});
  await flush();
  const s = h.state;
  s.searchValue = "hidden";
  s.statusFilter = "running";
  s.groupFilter = "old";
  s.workspaceFilter = {
    module_id: "mod",
    followed: true,
    archived: true,
    tag: "hidden",
  };
  const conditions = [
    { field: "ownerId", operator: "equals", value: "CURRENT_USER" },
  ];
  s.applyAdvanced(conditions, "or", "personal");
  await flush();
  expect(s.planQuery).toEqual({
    filters: JSON.stringify({ conditions, logic: "or" }),
    module_id: undefined,
    group_id: undefined,
    include_descendants: true,
  });
  h.stop();
});
it("canceling the advanced draft blocks navigation, group copy, edit and delete", async () => {
  const h = componentHost(Plans, {});
  await flush();
  const s = h.state;
  s.groupFilter = "old";
  s.advancedEditor = { beforeClose: vi.fn().mockResolvedValue(false) };
  for (const action of ["copy", "edit", "delete"])
    await s.groupAction(action, "clicked");
  await s.viewPlanDetail("plan");
  expect(await mocks.guard.mock.calls[0][0]()).toBe(false);
  expect(await mocks.updateGuard.mock.calls[0][0]()).toBe(false);
  expect(mocks.clone).not.toHaveBeenCalled();
  expect(mocks.remove).not.toHaveBeenCalled();
  expect(mocks.confirm).not.toHaveBeenCalled();
  expect(s.groupModal).toBe(false);
  expect(mocks.push).not.toHaveBeenCalled();
  h.stop();
});
it("deleting a clicked group freezes that identity even if selection changes", async () => {
  const h = componentHost(Plans, {});
  await flush();
  const s = h.state;
  await s.groupAction("delete", "clicked");
  s.groupFilter = "old";
  await mocks.confirm.mock.calls[0][0].onOk();
  expect(mocks.remove).toHaveBeenCalledWith("clicked");
  expect(s.groupFilter).toBe("old");
  h.stop();
});
it("an old confirmation cannot delete after project returns to the same identity", async () => {
  const h = componentHost(Plans, {});
  await flush();
  const s = h.state;
  await s.groupAction("delete", "clicked");
  const confirm = mocks.confirm.mock.calls[0][0];
  project.currentProject = { id: "q" };
  await flush();
  project.currentProject = { id: "p" };
  await flush();
  await expect(confirm.onOk()).rejects.toThrow();
  expect(mocks.remove).not.toHaveBeenCalled();
  h.stop();
});
it.each(["project", "actor"])(
  "a %s ABA does not accept old group-write ACK or release the new pending operation",
  async (dimension) => {
    const h = componentHost(Plans, {});
    await flush();
    const s = h.state;
    let finish!: (v: any) => void;
    mocks.save.mockReturnValueOnce(new Promise((r) => (finish = r)));
    s.groupForm = {
      name: "old",
      description: "",
      tags: [],
      archived: false,
      moduleId: null,
    };
    const old = s.saveGroup();
    await flush();
    if (dimension === "project") project.currentProject = { id: "q" };
    else user.user = { id: "v" };
    await flush();
    if (dimension === "project") project.currentProject = { id: "p" };
    else user.user = { id: "u" };
    await flush();
    let finishNew!: (v: any) => void;
    mocks.save.mockReturnValueOnce(new Promise((r) => (finishNew = r)));
    s.groupForm = {
      name: "fresh",
      description: "",
      tags: [],
      archived: false,
      moduleId: null,
    };
    s.groupModal = true;
    const current = s.saveGroup();
    await flush();
    finish({ id: "old" });
    await old;
    await flush();
    expect(s.groupSaving).toBe(true);
    expect(s.groupModal).toBe(true);
    expect(s.groupForm.name).toBe("fresh");
    expect(mocks.success).not.toHaveBeenCalled();
    finishNew({ id: "fresh" });
    await current;
    expect(s.groupSaving).toBe(false);
    h.stop();
  },
);
it("project/user changes discard old list ACKs and reset private filter identities", async () => {
  const h = componentHost(Plans, {});
  await flush();
  const s = h.state;
  let finish!: (v: any) => void;
  mocks.get.mockReturnValueOnce(new Promise((r) => (finish = r)));
  const old = s.loadPlans();
  await flush();
  user.user = { id: "v" };
  await flush();
  finish({ items: [{ id: "stale" }], total: 1 });
  await old;
  expect(s.plans[0].id).toBe("current");
  s.applyAdvanced([], "and", "private");
  await flush();
  project.currentProject = { id: "q" };
  await flush();
  expect(s.advancedViewId).toBeUndefined();
  expect(s.advancedConditions).toBeUndefined();
  h.stop();
});

it("a group-write acknowledgement keeps any newer unsubmitted group draft visible", async () => {
  const h = componentHost(Plans, {});
  await flush();
  const s = h.state;
  s.groupModal = true;
  s.groupForm = {
    name: "Old",
    description: "",
    tags: [],
    archived: false,
    moduleId: null,
  };
  let finish!: (v: any) => void;
  mocks.save.mockReturnValueOnce(new Promise((r) => (finish = r)));
  const old = s.saveGroup();
  await flush();
  s.groupForm.name = "New";
  finish({ id: "old" });
  await old;
  expect(s.groupModal).toBe(true);
  expect(s.groupForm.name).toBe("New");
  expect(s.groupSaving).toBe(false);
  h.stop();
});

it("a completed copy cannot unlock a new group save begun during its navigation", async () => {
  const h = componentHost(Plans, {});
  await flush();
  const s = h.state;
  let finishNav!: () => void, finishSave!: (v: any) => void;
  mocks.replace.mockReturnValueOnce(new Promise<void>((r) => (finishNav = r)));
  const copying = s.cloneGroup("old");
  await flush();
  expect(s.groupSaving).toBe(false);
  mocks.save.mockReturnValueOnce(new Promise((r) => (finishSave = r)));
  s.groupForm.name = "New";
  const saving = s.saveGroup();
  await flush();
  finishNav();
  await copying;
  expect(s.groupSaving).toBe(true);
  finishSave({});
  await saving;
  h.stop();
});

it.each([1, 2, 3, 4, 5])(
  "group deletion closing tail with %s microtasks cannot send under a different actor",
  async (n) => {
    const h = componentHost(Plans, {});
    await flush();
    const s = h.state;
    await s.groupAction("delete", "clicked");
    const confirmation = mocks.confirm.mock.calls[0][0],
      actors: string[] = [];
    mocks.remove.mockImplementation(() => {
      actors.push(user.user.id);
      return Promise.resolve();
    });
    s.advancedEditor = {
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
