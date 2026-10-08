import { it, expect, vi, beforeEach } from "vitest";
import { reactive } from "vue";
const m = vi.hoisted(() => ({
  list: vi.fn(),
  sources: vi.fn(),
  save: vi.fn(),
  remove: vi.fn(),
  confirm: vi.fn(),
  success: vi.fn(),
}));
const user = reactive({ user: { id: "u" } }),
  project = reactive({
    currentProject: { id: "p" },
    projects: [
      { id: "p", name: "P" },
      { id: "q", name: "Q" },
    ],
  }),
  route = reactive({ query: {} });
vi.mock("@/stores/user", () => ({ useUserStore: () => user }));
vi.mock("@/stores/project", () => ({ useProjectStore: () => project }));
vi.mock("@/api/requestEnvironmentGroups", () => ({
  requestEnvironmentGroupsApi: m,
}));
vi.mock("ant-design-vue", () => ({
  Modal: { confirm: m.confirm },
  message: { success: m.success, error: vi.fn() },
}));
vi.mock("vue-router", () => ({
  useRoute: () => route,
  onBeforeRouteLeave: vi.fn(),
  onBeforeRouteUpdate: vi.fn(),
}));
import Page from "@/views/RequestEnvironmentGroups.vue";
import { componentHost, flushComponent as flush } from "@/test/componentHost";
const row = {
  id: "g",
  name: "G",
  description: "D",
  revision: 3,
  mappings: [{ projectId: "p", environmentId: "e" }],
};
const data = () => ({ items: [row], total: 1, canEdit: true, canDelete: true });
beforeEach(() => {
  vi.resetAllMocks();
  user.user = { id: "u" };
  project.currentProject = { id: "p" };
  route.query = {};
  m.list.mockResolvedValue(data());
  m.sources.mockResolvedValue([{ id: "e", name: "E" }]);
  m.save.mockResolvedValue({ id: "g", revision: 4 });
  m.remove.mockResolvedValue({});
  vi.stubGlobal("window", {
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
  });
});
it("source initial read releases loading and preserves choices", async () => {
  const h = componentHost(Page, {});
  await flush();
  const s = h.state;
  await s.openEditor(row);
  await flush();
  const key = s.draft.mappings[0].key;
  const state = s.sourceState[key];
  h.stop();
  expect(state.loading).false;
  expect(state.options[0].id).toBe("e");
});
it("late source read cannot restore previous project options", async () => {
  const h = componentHost(Page, {});
  await flush();
  const s = h.state;
  await s.openEditor();
  s.addMapping();
  let finish!: (v: any) => void;
  m.sources
    .mockReturnValueOnce(new Promise((r) => (finish = r)))
    .mockResolvedValueOnce([{ id: "qenv", name: "QEnv" }]);
  const key = s.draft.mappings[0].key;
  const old = s.selectProject(key, "p");
  await s.selectProject(key, "q");
  finish([{ id: "penv", name: "PEnv" }]);
  await old;
  await flush();
  const state = s.sourceState[key];
  h.stop();
  expect(state.loading).false;
  expect(state.options.map((x: any) => x.id)).toEqual(["qenv"]);
});
it("version failure preserves editable original revision and draft", async () => {
  const h = componentHost(Page, {});
  await flush();
  const s = h.state;
  await s.openEditor(row);
  await flush();
  s.draft.name = "New";
  m.save.mockRejectedValueOnce(Error("409"));
  await s.save();
  expect(s.editorOpen).true;
  expect(s.draft.expectedRevision).toBe(3);
  expect(s.draft.name).toBe("New");
  expect(s.busy).false;
  h.stop();
});
it("deleted-group refresh completion does not notify after actor switches", async () => {
  const h = componentHost(Page, {});
  await flush();
  const s = h.state;
  s.remove(row);
  const c = m.confirm.mock.calls[0][0];
  let finish!: (v: any) => void;
  m.list
    .mockReturnValueOnce(new Promise((r) => (finish = r)))
    .mockResolvedValue(data());
  const pending = c.onOk();
  await flush();
  user.user = { id: "new" };
  await flush();
  finish(data());
  await pending;
  h.stop();
  expect(m.success).not.toHaveBeenCalled();
});

import {
  selectExecutionEnvironment,
  executionEnvironmentValue,
  executionEnvironmentOptions,
} from "@/components/TestPlan/planMinderTag";
it("environment group selection keeps legacy environment and group fields mutually exclusive", () => {
  const config: any = {
    requestEnvironmentId: "old",
    requestEnvironmentGroupId: "NONE",
    executionMode: "parallel",
    retryTimes: 3,
  };
  const grouped = selectExecutionEnvironment(config, "GROUP:g");
  expect(grouped.requestEnvironmentId).toBe("NONE");
  expect(grouped.requestEnvironmentGroupId).toBe("g");
  expect(executionEnvironmentValue(grouped)).toBe("GROUP:g");
  expect(config.requestEnvironmentId).toBe("old");
  const single = selectExecutionEnvironment(grouped, "new");
  expect(single.requestEnvironmentId).toBe("new");
  expect(single.requestEnvironmentGroupId).toBe("NONE");
  expect(single.retryTimes).toBe(3);
  expect(executionEnvironmentValue(single)).toBe("new");
  expect(
    selectExecutionEnvironment(grouped, "NONE").requestEnvironmentGroupId,
  ).toBe("NONE");
  expect(
    executionEnvironmentOptions({
      requestEnvironments: [{ id: "e", name: "E" }],
    } as any),
  ).toEqual([
    { value: "NONE", label: "默认环境" },
    { value: "e", label: "E" },
  ]);
});
it("old ABA deletion confirmation cannot submit under current actor", async () => {
  const h = componentHost(Page, {});
  await flush();
  const s = h.state;
  s.remove(row);
  const c = m.confirm.mock.calls[0][0];
  user.user = { id: "other" };
  user.user = { id: "u" };
  await flush();
  await c.onOk();
  h.stop();
  expect(m.remove).not.toHaveBeenCalled();
});
it("unmounted old deletion confirmation cannot submit", async () => {
  const h = componentHost(Page, {});
  await flush();
  const s = h.state;
  s.remove(row);
  const c = m.confirm.mock.calls[0][0];
  h.stop();
  await c.onOk();
  expect(m.remove).not.toHaveBeenCalled();
});

it("readonly catalog cannot create, edit mappings, save or delete", async () => {
  m.list.mockResolvedValue({ ...data(), canEdit: false, canDelete: false });
  const h = componentHost(Page, {});
  await flush();
  const s = h.state;
  await s.openEditor();
  expect(s.editorOpen).false;
  await s.openEditor(row);
  await flush();
  expect(s.editorOpen).true;
  s.addMapping();
  s.removeMapping(s.draft.mappings[0].key);
  await s.save();
  s.remove(row);
  expect(s.draft.mappings).toHaveLength(1);
  expect(m.save).not.toHaveBeenCalled();
  expect(m.remove).not.toHaveBeenCalled();
  h.stop();
});
it("unreadable source preserves recorded mapping and changing source clears old choices", async () => {
  const h = componentHost(Page, {});
  await flush();
  const s = h.state;
  await s.openEditor(row);
  await flush();
  const key = s.draft.mappings[0].key;
  m.sources.mockRejectedValueOnce(Error("403"));
  await s.loadSource(key);
  expect(s.draft.mappings[0].environmentId).toBe("e");
  expect(s.sourceOptions(s.draft.mappings[0]).some((o: any) => o.value === "e"))
    .true;
  m.sources.mockRejectedValueOnce(Error("403"));
  await s.selectProject(key, "q");
  expect(s.draft.mappings[0].environmentId).toBe("");
  expect(s.sourceOptions(s.draft.mappings[0])).toEqual([]);
  h.stop();
});
it("removed mapping cannot receive a late directory response", async () => {
  const h = componentHost(Page, {});
  await flush();
  const s = h.state;
  await s.openEditor(row);
  await flush();
  const key = s.draft.mappings[0].key;
  let finish!: (v: any) => void;
  m.sources.mockReturnValueOnce(new Promise((r) => (finish = r)));
  const pending = s.loadSource(key);
  s.removeMapping(key);
  finish([{ id: "late", name: "late" }]);
  await pending;
  expect(s.sourceState[key]).toBeUndefined();
  expect(s.draft.mappings).toHaveLength(0);
  h.stop();
});
it("save captures submitted values, blocks duplicates and preserves newer draft on acknowledgement", async () => {
  const h = componentHost(Page, {});
  await flush();
  const s = h.state;
  await s.openEditor(row);
  await flush();
  s.draft.name = "submitted";
  let finish!: (v: any) => void;
  m.save.mockReturnValueOnce(new Promise((r) => (finish = r)));
  const pending = s.save();
  await flush();
  expect(s.busy).true;
  expect(await s.beforeClose()).false;
  await s.save();
  expect(m.save).toHaveBeenCalledTimes(1);
  expect(m.save.mock.calls[0][1].name).toBe("submitted");
  s.draft.name = "newer";
  finish({ id: "g", revision: 4 });
  await pending;
  expect(s.editorOpen).true;
  expect(s.dirty).true;
  expect(s.draft.name).toBe("newer");
  expect(s.draft.expectedRevision).toBe(4);
  expect(s.busy).false;
  h.stop();
});
it("failed creation retries the same request ID and retains all draft values", async () => {
  const h = componentHost(Page, {});
  await flush();
  const s = h.state;
  await s.openEditor();
  s.draft.name = "new";
  s.addMapping();
  const key = s.draft.mappings[0].key;
  await s.selectProject(key, "p");
  s.draft.mappings[0].environmentId = "e";
  m.save.mockRejectedValueOnce(Error("response lost"));
  await s.save();
  const first = m.save.mock.calls[0][1];
  expect(first.requestId.length).toBeLessThanOrEqual(36);
  expect(s.editorOpen).true;
  expect(s.draft.name).toBe("new");
  await s.save();
  expect(m.save.mock.calls[1][1].requestId).toBe(first.requestId);
  expect(m.save.mock.calls[1][2]).toBeUndefined();
  h.stop();
});
it("actor ABA invalidates pending save acknowledgements and success messages", async () => {
  const h = componentHost(Page, {});
  await flush();
  const s = h.state;
  await s.openEditor(row);
  await flush();
  s.draft.name = "submitted";
  let finish!: (v: any) => void;
  m.save.mockReturnValueOnce(new Promise((r) => (finish = r)));
  const pending = s.save();
  user.user = { id: "other" };
  user.user = { id: "u" };
  await flush();
  finish({ id: "g", revision: 4 });
  await pending;
  expect(s.editorOpen).false;
  expect(m.success).not.toHaveBeenCalled();
  expect(s.busy).false;
  h.stop();
});
it("discard confirmation cannot close a draft edited after confirmation opened", async () => {
  const h = componentHost(Page, {});
  await flush();
  const s = h.state;
  await s.openEditor(row);
  await flush();
  s.draft.name = "before";
  const pending = s.beforeClose();
  const confirm = m.confirm.mock.calls[0][0];
  s.draft.name = "after";
  confirm.onOk();
  expect(await pending).false;
  expect(s.editorOpen).true;
  expect(s.draft.name).toBe("after");
  const again = s.beforeClose();
  m.confirm.mock.calls[1][0].onCancel();
  expect(await again).false;
  h.stop();
});
