import { beforeEach, describe, it, expect, vi } from "vitest";
const mocks = vi.hoisted(() => ({
  detail: vi.fn(),
  confirm: vi.fn(),
  route: { query: { projectId: "p", kind: "GROUP" }, params: { runId: "run" } },
  account: { user: { id: "user" } },
}));
vi.mock("@/api/planReports", async () => ({
  ...(await vi.importActual<any>("@/api/planReports")),
  planReportsApi: { detail: mocks.detail },
}));
vi.mock("@/api/planGroup", () => ({ planGroupApi: {} }));
vi.mock("ant-design-vue", () => ({
  message: { warning: vi.fn(), error: vi.fn(), success: vi.fn() },
  Modal: { confirm: mocks.confirm },
}));
vi.mock("vue-router", async () => {
  const { reactive } = await import("vue");
  return {
    useRoute: () => reactive(mocks.route),
    useRouter: () => ({
      push: vi.fn(),
      resolve: () => ({ href: "/synthetic" }),
    }),
    onBeforeRouteLeave: vi.fn(),
    onBeforeRouteUpdate: vi.fn(),
  };
});
vi.mock("@/stores/project", () => ({
  useProjectStore: () => ({ currentProject: { id: "p" } }),
}));
vi.mock("@/stores/user", async () => {
  const { reactive } = await import("vue");
  return { useUserStore: () => reactive(mocks.account) };
});
vi.mock("@/components/TestPlan/PlanRunReport.vue", () => ({
  default: { render: () => null },
}));
import TestPlanReportDetail from "./TestPlanReportDetail.vue";
import { componentHost, flushComponent as flush } from "@/test/componentHost";
const report = (id = "run") => ({
  kind: "GROUP",
  name: "synthetic",
  payload: {
    id,
    summary: { notes: "saved" },
    report: { total: 0, counts: {}, cases: [] },
    children: [],
  },
});
beforeEach(() => {
  vi.clearAllMocks();
  mocks.account.user.id = "user";
  mocks.route.query.projectId = "p";
  mocks.route.params.runId = "run";
  vi.stubGlobal("window", {
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
  });
  mocks.confirm.mockImplementation((options) => options.onCancel());
  mocks.detail.mockResolvedValue(report());
});
describe("独立报告页面在清除组件之前保护计划组总结", () => {
  it("父页面直接刷新先调用子组件关闭契约，取消时保留数据且不再读取", async () => {
    const { state: s, stop } = componentHost(TestPlanReportDetail, {});
    await flush();
    const child = { beforeClose: vi.fn().mockResolvedValue(false) };
    s.groupReport = child;
    await s.load();
    expect(s.detail.payload.id).toBe("run");
    expect(s.groupReport.beforeClose).toBe(child.beforeClose);
    expect(child.beforeClose).toHaveBeenCalledTimes(1);
    expect(mocks.detail).toHaveBeenCalledTimes(1);
    stop();
  });
  it("身份切换即清除旧内容，旧身份的迟到响应不能覆盖新身份报告", async () => {
    let finish!: (v: any) => void;
    mocks.detail.mockReturnValueOnce(new Promise((r) => (finish = r)));
    const { state: s, stop } = componentHost(TestPlanReportDetail, {});
    s.user.user.id = "new-user";
    await flush();
    expect(mocks.detail).toHaveBeenCalledTimes(2);
    expect(s.detail.name).toBe("synthetic");
    finish({ ...report(), name: "old secret" });
    await flush();
    expect(s.detail.name).toBe("synthetic");
    stop();
  });
  it("已显示旧身份报告的草稿契约不会阻止身份切换清除数据", async () => {
    const { state: s, stop } = componentHost(TestPlanReportDetail, {});
    await flush();
    const guard = vi.fn().mockResolvedValue(false);
    s.groupReport = { beforeClose: guard };
    let finish!: (v: any) => void;
    mocks.detail.mockReturnValueOnce(new Promise((r) => (finish = r)));
    s.user.user.id = "other";
    await flush();
    expect(s.detail).toBeUndefined();
    expect(guard).not.toHaveBeenCalled();
    finish(report());
    await flush();
    expect(s.detail.name).toBe("synthetic");
    stop();
  });
});
