import { reactive } from "vue";
import { beforeEach, describe, it, expect, vi } from "vitest";
const mocks = vi.hoisted(() => ({
  summary: vi.fn(),
  share: vi.fn(),
  revoke: vi.fn(),
  pdf: vi.fn(),
  confirm: vi.fn(),
  warning: vi.fn(),
  push: vi.fn(),
  leave: vi.fn(),
  update: vi.fn(),
  success: vi.fn(),
}));
vi.mock("@/api/planGroup", () => ({ planGroupApi: mocks }));
vi.mock("ant-design-vue", () => ({
  message: { warning: mocks.warning, error: vi.fn(), success: mocks.success },
  Modal: { confirm: mocks.confirm },
}));
vi.mock("vue-router", () => ({
  useRouter: () => ({
    push: mocks.push,
    resolve: (route: any) => ({ href: "/reports/" + route.params.runId }),
  }),
  onBeforeRouteLeave: mocks.leave,
  onBeforeRouteUpdate: mocks.update,
}));
const user = reactive({ user: { id: "user" } });
vi.mock("@/stores/user", () => ({ useUserStore: () => user }));
import PlanGroupReport from "./PlanGroupReport.vue";
import { componentHost, flushComponent as flush } from "@/test/componentHost";
const run = (id = "run", notes = "saved") => ({
  id,
  summary: { notes },
  report: { total: 0, counts: {}, cases: [] },
  children: [],
});
beforeEach(() => {
  vi.clearAllMocks();
  user.user = { id: "user" };
  vi.stubGlobal("window", {
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
  });
  vi.stubGlobal("location", { origin: "https://synthetic.invalid" });
  mocks.confirm.mockImplementation((options) => options.onCancel());
  mocks.summary.mockResolvedValue({});
  mocks.share.mockResolvedValue({ id: "share", path: "/s/synthetic" });
  mocks.revoke.mockResolvedValue({});
});
describe("计划组报告总结的操作与草稿隔离", () => {
  it("复制链接也阻止重复，切身份范围后忽略迟到提示", async () => {
    let finish!: () => void;
    const writeText = vi
      .fn()
      .mockReturnValue(new Promise<void>((r) => (finish = r)));
    vi.stubGlobal("navigator", { clipboard: { writeText } });
    const {
      state: s,
      props,
      stop,
    } = componentHost(PlanGroupReport, { run: run(), projectId: "old" });
    s.shareLink = "https://synthetic.invalid/s";
    const pending = s.copyShare();
    await s.copyShare();
    expect(writeText).toHaveBeenCalledTimes(1);
    props.projectId = "new";
    await flush();
    finish();
    await pending;
    expect(mocks.success).not.toHaveBeenCalled();
    expect(s.busy).toBe(false);
    stop();
  });
  it("刷新/成员跳转/路由离开取消保留总结，服务端重读不覆盖未保存输入", async () => {
    const refresh = vi.fn(),
      {
        state: s,
        props,
        stop,
      } = componentHost(PlanGroupReport, {
        run: run(),
        projectId: "p",
        onRefresh: refresh,
      });
    s.summary.notes = "draft";
    props.run = run("run", "server refresh");
    await flush();
    expect(s.summary.notes).toBe("draft");
    await s.refresh();
    await s.openChild("child");
    expect(await mocks.leave.mock.calls[0][0]()).toBe(false);
    expect(refresh).not.toHaveBeenCalled();
    expect(mocks.push).not.toHaveBeenCalled();
    expect(s.dirty).toBe(true);
    mocks.confirm.mockImplementation((options) => options.onOk());
    await s.refresh();
    expect(refresh).toHaveBeenCalledTimes(1);
    expect(s.summary.notes).toBe("server refresh");
    expect(s.dirty).toBe(false);
    stop();
  });
  it("保存只确认提交快照，待保存/分享状态阻止重复操作和离开", async () => {
    let finish!: () => void;
    mocks.summary.mockReturnValueOnce(new Promise<void>((r) => (finish = r)));
    const { state: s, stop } = componentHost(PlanGroupReport, {
      run: run(),
      projectId: "p",
    });
    s.summary.notes = "submitted";
    const pending = s.save();
    s.summary.notes = "later edit";
    await s.save();
    await s.share();
    expect(mocks.summary).toHaveBeenCalledTimes(1);
    expect(mocks.summary.mock.calls[0][1].notes).toBe("submitted");
    expect(mocks.share).not.toHaveBeenCalled();
    expect(await s.beforeClose()).toBe(false);
    finish();
    await pending;
    expect(s.summary.notes).toBe("later edit");
    expect(s.dirty).toBe(true);
    mocks.confirm.mockImplementation((options) => options.onOk());
    await s.beforeClose();
    expect(s.summary.notes).toBe("submitted");
    expect(s.dirty).toBe(false);
    stop();
  });
  it("保存失败保留草稿，分享与撤销成功也不确认总结", async () => {
    mocks.summary.mockRejectedValueOnce(new Error("synthetic"));
    const { state: s, stop } = componentHost(PlanGroupReport, {
      run: run(),
      projectId: "p",
    });
    s.summary.notes = "unsaved";
    await s.save();
    expect(s.dirty).toBe(true);
    await s.share();
    expect(s.shareId).toBe("share");
    await s.revoke();
    expect(s.dirty).toBe(true);
    expect(await s.beforeClose()).toBe(false);
    stop();
  });
  it("切批次后旧分享结果不恢复链接，也不解锁新批次待保存", async () => {
    let oldFinish!: (v: any) => void, newFinish!: () => void;
    mocks.share.mockReturnValueOnce(new Promise((r) => (oldFinish = r)));
    mocks.summary.mockReturnValueOnce(
      new Promise<void>((r) => (newFinish = r)),
    );
    const {
      state: s,
      props,
      stop,
    } = componentHost(PlanGroupReport, { run: run(), projectId: "old" });
    const old = s.share();
    props.projectId = "new";
    props.run = run("new");
    await flush();
    s.summary.notes = "new draft";
    const latest = s.save();
    oldFinish({ id: "old-share", path: "/s/old" });
    await old;
    expect(s.shareLink).toBe("");
    expect(s.busy).toBe(true);
    expect(mocks.summary.mock.calls[0][0]).toBe("new");
    newFinish();
    await latest;
    expect(s.busy).toBe(false);
    stop();
  });
  it("原生刷新保护总结草稿和待操作，确认离开后移除保护", async () => {
    const { state: s, stop } = componentHost(PlanGroupReport, {
      run: run(),
      projectId: "p",
    });
    const event = { preventDefault: vi.fn(), returnValue: undefined };
    s.summary.notes = "draft";
    s.beforeUnload(event);
    expect(event.preventDefault).toHaveBeenCalledTimes(1);
    mocks.confirm.mockImplementation((options) => options.onOk());
    await s.beforeClose();
    s.beforeUnload(event);
    expect(event.preventDefault).toHaveBeenCalledTimes(1);
    stop();
    expect(window.removeEventListener).toHaveBeenCalled();
  });
});

for (const n of [1, 2, 3, 4, 5, 6])
  it(`child navigation confirmation tail rejects fresh actor n${n}`, async () => {
    const h = componentHost(PlanGroupReport, { run: run(), projectId: "p" }),
      s = h.state,
      actors: string[] = [];
    mocks.push.mockImplementation(() => {
      actors.push(user.user.id);
      return Promise.resolve();
    });
    s.detailCards = {
      beforeClose: () =>
        Promise.resolve().then(() => {
          const step = (left: number): void =>
            queueMicrotask(() =>
              left > 1 ? step(left - 1) : (user.user = { id: "other" }),
            );
          step(n);
          return true;
        }),
    };
    try {
      await s.openChild("child");
      await flush();
      expect(actors).not.toContain("other");
    } finally {
      h.stop();
    }
  });
it("card drafts block explicit refresh and child navigation", async () => {
  const refresh = vi.fn(),
    h = componentHost(PlanGroupReport, {
      run: run(),
      projectId: "p",
      onRefresh: refresh,
    }),
    s = h.state;
  s.detailCards = { beforeClose: vi.fn().mockResolvedValue(false) };
  await s.refresh();
  await s.openChild("child");
  expect(refresh).not.toHaveBeenCalled();
  expect(mocks.push).not.toHaveBeenCalled();
  h.stop();
});
