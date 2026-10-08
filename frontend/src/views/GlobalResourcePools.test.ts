import { it, expect, vi, beforeEach } from "vitest";
import { reactive } from "vue";
const m = vi.hoisted(() => ({
  list: vi.fn(),
  nodes: vi.fn(),
  save: vi.fn(),
  enabled: vi.fn(),
  remove: vi.fn(),
  confirm: vi.fn(),
  success: vi.fn(),
}));
const user = reactive({ user: { id: "u" } }),
  project = reactive({
    currentProject: { id: "p" },
    projects: [{ id: "p", name: "P" }],
  }),
  route = reactive({ query: {} });
vi.mock("@/stores/user", () => ({ useUserStore: () => user }));
vi.mock("@/stores/project", () => ({ useProjectStore: () => project }));
vi.mock("@/api/globalResourcePools", () => ({ globalResourcePoolsApi: m }));
vi.mock("ant-design-vue", () => ({
  Modal: { confirm: m.confirm },
  message: { success: m.success, error: vi.fn() },
}));
vi.mock("vue-router", () => ({
  useRoute: () => route,
  onBeforeRouteLeave: vi.fn(),
  onBeforeRouteUpdate: vi.fn(),
}));
import Page from "./GlobalResourcePools.vue";
import { componentHost, flushComponent as flush } from "@/test/componentHost";
const node = (id: string) => ({
  id,
  name: id,
  enabled: true,
  online: true,
  capacity: 1,
});
const row = {
  id: "pool",
  name: "Pool",
  description: "",
  type: "Node",
  enabled: true,
  applications: ["api"],
  allProjects: false,
  projectIds: ["p"],
  environmentIds: ["selected"],
  nodes: [node("selected")],
  revision: 3,
  capacity: { configured: 1, online: 1, running: 0, available: 1 },
};
const data = () => ({ items: [row], total: 1, canEdit: true, canDelete: true });
const deferred = () => {
  let finish!: (x: any) => void;
  const promise = new Promise<any>((r) => (finish = r));
  return { promise, finish };
};
beforeEach(() => {
  vi.resetAllMocks();
  user.user = { id: "u" };
  project.currentProject = { id: "p" };
  route.query = {};
  m.list.mockResolvedValue(data());
  m.nodes.mockResolvedValue({ items: [node("other")], total: 1 });
  m.save.mockResolvedValue({ id: "pool", revision: 4 });
  m.remove.mockResolvedValue({});
  m.enabled.mockResolvedValue({});
  vi.stubGlobal("window", {
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
  });
});
it("preserves selected nodes and displays disabled cached entries without secrets", async () => {
  const h = componentHost(Page, {});
  await flush();
  await h.state.openEditor({
    ...row,
    nodes: [{ ...node("selected"), enabled: false }],
  });
  await flush();
  expect(h.state.nodeOptions).toContainEqual({
    value: "selected",
    label: "selected（已停用）",
    disabled: false,
  });
  expect(h.state.draft.environmentIds).toEqual(["selected"]);
  expect(h.state.nodeLoading).false;
  h.stop();
});
it("pages candidates with a bounded cache retaining selections", async () => {
  m.nodes
    .mockResolvedValueOnce({
      items: Array.from({ length: 50 }, (_, i) => node("a" + i)),
      total: 100,
    })
    .mockResolvedValueOnce({
      items: Array.from({ length: 50 }, (_, i) => node("b" + i)),
      total: 100,
    });
  const h = componentHost(Page, {});
  await flush();
  await h.state.openEditor(row);
  await flush();
  await h.state.loadNodes(true);
  expect(m.nodes.mock.calls[1][0]).toEqual({
    page: 2,
    size: 50,
    search: undefined,
  });
  expect(Object.keys(h.state.nodeCache)).toHaveLength(51);
  expect(h.state.nodeCache.selected).toBeDefined();
  expect(h.state.nodeMore).false;
  h.stop();
});
it("candidate errors retain selected ids and readable labels", async () => {
  m.nodes.mockRejectedValueOnce(Error("offline"));
  const h = componentHost(Page, {});
  await flush();
  await h.state.openEditor(row);
  await flush();
  expect(h.state.nodeError).not.toBe("");
  expect(h.state.draft.environmentIds).toEqual(["selected"]);
  expect(h.state.nodeOptions[0].label).toBe("selected");
  expect(h.state.nodeLoading).false;
  h.stop();
});
it("failed save retains revision and permits explicit retry", async () => {
  const h = componentHost(Page, {});
  await flush();
  await h.state.openEditor(row);
  await flush();
  h.state.draft.name = "New";
  m.save.mockRejectedValueOnce(Error("409"));
  await h.state.save();
  expect(h.state.editorOpen).true;
  expect(h.state.draft.expectedRevision).toBe(3);
  expect(h.state.draft.name).toBe("New");
  expect(h.state.busy).false;
  expect(h.state.editorError).not.toBe("");
  h.stop();
});
it("new creation retries preserve request id and duplicate saves are blocked", async () => {
  const h = componentHost(Page, {});
  await flush();
  await h.state.openEditor();
  await flush();
  Object.assign(h.state.draft, {
    name: "New",
    projectIds: ["p"],
    environmentIds: ["other"],
  });
  const key = h.state.draft.requestId;
  expect(key.length).toBeGreaterThan(0);
  m.save.mockRejectedValueOnce(Error("lost"));
  await h.state.save();
  const wait = deferred();
  m.save.mockReturnValueOnce(wait.promise);
  const pending = h.state.save();
  await h.state.save();
  expect(m.save).toHaveBeenCalledTimes(2);
  expect(m.save.mock.calls.map((c) => c[0].requestId)).toEqual([key, key]);
  wait.finish({ id: "new", revision: 1 });
  await pending;
  expect(h.state.editorOpen).false;
  h.stop();
});
it("acknowledgement saves submitted baseline while preserving later draft", async () => {
  const h = componentHost(Page, {});
  await flush();
  await h.state.openEditor(row);
  await flush();
  h.state.draft.name = "Submitted";
  const wait = deferred();
  m.save.mockReturnValueOnce(wait.promise);
  const pending = h.state.save();
  h.state.draft.name = "Later";
  wait.finish({ id: "pool", revision: 4 });
  await pending;
  expect(m.save.mock.calls[0][0].name).toBe("Submitted");
  expect(h.state.draft.name).toBe("Later");
  expect(h.state.editorOpen).true;
  expect(h.state.dirty).true;
  expect(h.state.draft.expectedRevision).toBe(4);
  h.stop();
});
it.each(["project", "actor", "unmount"])(
  "late save after %s cannot acknowledge or notify another scope",
  async (kind) => {
    const h = componentHost(Page, {});
    await flush();
    await h.state.openEditor(row);
    await flush();
    const wait = deferred();
    m.save.mockReturnValueOnce(wait.promise);
    const pending = h.state.save();
    if (kind === "project") project.currentProject = { id: "q" };
    else if (kind === "actor") user.user = { id: "v" };
    else h.stop();
    wait.finish({ id: "late", revision: 999 });
    await pending;
    expect(m.success).not.toHaveBeenCalled();
    expect(h.state.editingId).not.toBe("late");
    if (kind !== "unmount") h.stop();
  },
);
it("late catalog and candidates cannot restore a previous project", async () => {
  const old = deferred();
  m.list.mockReturnValueOnce(old.promise);
  const h = componentHost(Page, {});
  project.currentProject = { id: "q" };
  await flush();
  old.finish({ ...data(), items: [{ ...row, id: "old" }] });
  await flush();
  expect(h.state.items[0].id).toBe("pool");
  const nodes = deferred();
  m.nodes.mockReturnValueOnce(nodes.promise);
  await h.state.openEditor(row);
  project.currentProject = { id: "p" };
  nodes.finish({ items: [node("old")], total: 1 });
  await flush();
  expect(h.state.nodeOptions).not.toContainEqual(
    expect.objectContaining({ value: "old" }),
  );
  expect(h.state.editorOpen).false;
  h.stop();
});
it("readonly catalog allows viewing without exposing node directory or writes", async () => {
  m.list.mockResolvedValueOnce({ ...data(), canEdit: false, canDelete: false });
  const h = componentHost(Page, {});
  await flush();
  await h.state.openEditor(row);
  await h.state.save();
  await h.state.toggle(row);
  h.state.remove(row);
  expect(m.nodes).not.toHaveBeenCalled();
  expect(m.save).not.toHaveBeenCalled();
  expect(m.enabled).not.toHaveBeenCalled();
  expect(m.confirm).not.toHaveBeenCalled();
  h.stop();
});
it("late delete confirmation after project ABA cannot delete", async () => {
  const h = componentHost(Page, {});
  await flush();
  h.state.remove(row);
  const callback = m.confirm.mock.calls[0][0].onOk;
  project.currentProject = { id: "q" };
  project.currentProject = { id: "p" };
  await flush();
  await callback();
  expect(m.remove).not.toHaveBeenCalled();
  h.stop();
});
it("discard confirmation detects edits made while prompt was open", async () => {
  const h = componentHost(Page, {});
  await flush();
  await h.state.openEditor(row);
  await flush();
  h.state.draft.name = "Changed";
  const pending = h.state.beforeClose();
  h.state.draft.description = "Later";
  m.confirm.mock.calls[0][0].onOk();
  expect(await pending).false;
  expect(h.state.editorOpen).true;
  h.stop();
});
it("all-project scope clears previous restricted ids", async () => {
  const h = componentHost(Page, {});
  await flush();
  await h.state.openEditor(row);
  await flush();
  h.state.setAllProjects(true);
  expect(h.state.draft.projectIds).toEqual([]);
  await h.state.save();
  expect(m.save.mock.calls[0][0].allProjects).true;
  expect(m.save.mock.calls[0][0].projectIds).toEqual([]);
  h.stop();
});
it("can remove selected disabled nodes and cannot select them again", async () => {
  const h = componentHost(Page, {});
  await flush();
  await h.state.openEditor({
    ...row,
    nodes: [{ ...node("selected"), enabled: false }],
  });
  await flush();
  h.state.selectNodes(["other"]);
  expect(h.state.draft.environmentIds).toEqual(["other"]);
  h.state.selectNodes(["other", "selected"]);
  expect(h.state.draft.environmentIds).toEqual(["other"]);
  expect(h.state.nodeError).not.toBe("");
  h.stop();
});
it("limits selected ids immediately and prunes deselected cache", async () => {
  const h = componentHost(Page, {});
  await flush();
  await h.state.openEditor(row);
  await flush();
  for (let page = 1; page <= 2; page++) {
    m.nodes.mockResolvedValueOnce({
      items: Array.from({ length: 50 }, (_, i) =>
        node("n" + ((page - 1) * 50 + i)),
      ),
      total: 150,
    });
    await h.state.loadNodes(page === 2);
    h.state.selectNodes([
      ...h.state.draft.environmentIds.filter((x: string) => x !== "selected"),
      ...h.state.nodeItems.map((n: any) => n.id),
    ]);
  }
  expect(h.state.draft.environmentIds).toHaveLength(100);
  h.state.selectNodes([...h.state.draft.environmentIds, "overflow"]);
  expect(h.state.draft.environmentIds).toHaveLength(100);
  expect(h.state.nodeError).not.toBe("");
  expect(Object.keys(h.state.nodeCache)).toHaveLength(100);
  h.state.selectNodes([]);
  expect(h.state.nodeOptions).toHaveLength(50);
  h.stop();
});

it("actor ABA old save ACK never releases a new pending operation", async () => {
  const h = componentHost(Page, {});
  await flush();
  const s = h.state;
  await s.openEditor(row);
  await flush();
  let finish!: (r: any) => void;
  m.save.mockReturnValueOnce(new Promise((r) => (finish = r)));
  s.draft.name = "Old";
  const old = s.save();
  user.user = { id: "v" };
  user.user = { id: "u" };
  await flush();
  await s.openEditor(row);
  await flush();
  let done!: (r: any) => void;
  m.save.mockReturnValueOnce(new Promise((r) => (done = r)));
  s.draft.name = "New";
  const fresh = s.save();
  finish({ id: "g", revision: 4 });
  await old;
  expect(s.busy).true;
  done({ id: "g", revision: 5 });
  await fresh;
  h.stop();
});

it("old deletion confirm after unmount refuses mutation", async () => {
  const h = componentHost(Page, {});
  await flush();
  h.state.remove(row);
  const c = m.confirm.mock.calls[0][0];
  h.stop();
  await c.onOk();
  expect(m.remove).not.toHaveBeenCalled();
});
