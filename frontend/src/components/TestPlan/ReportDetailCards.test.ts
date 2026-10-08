import { beforeEach, afterEach, it, expect, vi } from "vitest";
import { reactive } from "vue";
const mocks = vi.hoisted(() => ({
  read: vi.fn(),
  write: vi.fn(),
  confirm: vi.fn(),
  leave: vi.fn(),
  update: vi.fn(),
}));
const user = reactive({ user: { id: "first" } });
vi.mock("@/stores/user", () => ({ useUserStore: () => user }));
vi.mock("ant-design-vue", () => ({
  Modal: { confirm: mocks.confirm },
  message: { success: vi.fn(), warning: vi.fn() },
}));
vi.mock("vue-router", () => ({
  onBeforeRouteLeave: mocks.leave,
  onBeforeRouteUpdate: mocks.update,
}));
vi.mock("vue-draggable-plus", () => ({ VueDraggable: { render: () => null } }));
import Cards from "./ReportDetailCards.vue";
import { normalizeReportCards, reportCardsKey } from "./reportCardPreferences";
import { componentHost, flushComponent as flush } from "@/test/componentHost";
const initial = () => ({
  projectId: "project",
  runId: "run",
  kind: "PLAN",
  status: "running",
  report: { total: 2, passRate: 50, counts: { passed: 1, pending: 1 } },
});
beforeEach(() => {
  vi.clearAllMocks();
  user.user = { id: "first" };
  mocks.read.mockReturnValue(null);
  mocks.confirm.mockImplementation((o) => o.onCancel());
  vi.stubGlobal("localStorage", { getItem: mocks.read, setItem: mocks.write });
  vi.stubGlobal("window", {
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
  });
});
afterEach(() => {
  vi.unstubAllGlobals();
});
it("normalizes untrusted settings, preserves known order and locks overview", () => {
  const normalized = normalizeReportCards([
    { key: "defects", visible: false },
    { key: "defects", visible: true },
    { key: "overview", visible: false },
    { key: "unknown", visible: true },
    { key: "configuration", visible: "yes" },
  ]);
  expect(normalized[0]).toEqual({ key: "overview", visible: true });
  expect(normalized[1]).toEqual({ key: "defects", visible: false });
  expect(normalized).toHaveLength(5);
  expect(reportCardsKey("a:b", "p/q", "PLAN")).not.toBe(
    reportCardsKey("a", "b:p/q", "PLAN"),
  );
});
it("storage failure preserves order/visibility draft; unchanged closing and cancel remain usable", async () => {
  const h = componentHost(Cards, initial()),
    s = h.state;
  s.openSettings();
  s.draft.reverse();
  s.draft[0].visible = false;
  mocks.write.mockImplementationOnce(() => {
    throw Error("synthetic quota");
  });
  s.saveSettings();
  expect(s.settingsOpen).toBe(true);
  expect(s.settingsError).toContain("草稿");
  expect(s.draft[0].visible).toBe(false);
  expect(await s.beforeClose()).toBe(false);
  expect(s.settingsOpen).toBe(true);
  s.discardSettings();
  s.openSettings();
  expect(s.dirty).toBe(false);
  expect(await s.beforeClose()).toBe(true);
  expect(mocks.write).toHaveBeenCalledTimes(1);
  s.openSettings();
  s.draft[0].visible = false;
  s.saveSettings();
  expect(s.settingsOpen).toBe(false);
  expect(
    JSON.parse(mocks.write.mock.calls[1][1]).find(
      (c: any) => c.key === "analysis",
    ).visible,
  ).toBe(false);
  h.stop();
});
it("project/actor/kind isolate settings and old ABA/unmount confirmations cannot discard a fresh draft", async () => {
  const h = componentHost(Cards, initial()),
    s = h.state;
  mocks.confirm.mockImplementation(() => {});
  s.openSettings();
  s.draft[0].visible = false;
  const pending = s.beforeClose(),
    old = mocks.confirm.mock.calls[0][0];
  h.props.projectId = "other";
  h.props.projectId = "project";
  user.user = { id: "second" };
  h.props.kind = "GROUP";
  await flush();
  s.openSettings();
  s.draft[1].visible = false;
  old.onOk();
  expect(await pending).toBe(false);
  expect(s.settingsOpen).toBe(true);
  expect(s.draft[1].visible).toBe(false);
  expect(mocks.read).toHaveBeenLastCalledWith(
    reportCardsKey("second", "project", "GROUP"),
  );
  const newer = s.beforeClose(),
    confirmation = mocks.confirm.mock.calls[1][0];
  h.stop();
  confirmation.onOk();
  expect(await newer).toBe(false);
  expect(mocks.write).not.toHaveBeenCalled();
});
it("confirmation cannot discard newer settings and execution analysis uses actual counts", async () => {
  const h = componentHost(Cards, initial()),
    s = h.state;
  s.openSettings();
  s.draft[0].visible = false;
  mocks.confirm.mockImplementation(() => {});
  const pending = s.beforeClose(),
    confirmation = mocks.confirm.mock.calls[0][0];
  s.draft[1].visible = false;
  confirmation.onOk();
  expect(await pending).toBe(false);
  expect(s.dirty).toBe(true);
  expect(s.resultCounts).toEqual([
    { state: "passed", count: 1 },
    { state: "pending", count: 1 },
  ]);
  expect(s.settled).toBe(false);
  h.props.status = "completed";
  await flush();
  expect(s.settled).toBe(true);
  h.stop();
});
