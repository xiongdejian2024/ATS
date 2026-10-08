import { beforeEach, describe, it, expect, vi } from "vitest";
const mocks = vi.hoisted(() => ({
  post: vi.fn(),
  confirm: vi.fn(),
  warning: vi.fn(),
  leave: vi.fn(),
  update: vi.fn(),
}));
vi.mock("@/utils/api", () => ({
  apiClient: { getInstance: () => ({ post: mocks.post }) },
}));
vi.mock("@/api/testCase", () => ({
  testCaseApi: { getCaseTemplate: vi.fn() },
}));
vi.mock("@/api/caseFeatures", () => ({ saveCaseBlob: vi.fn() }));
vi.mock("@/stores/user", () => ({
  useUserStore: () => ({ user: { id: "user" } }),
}));
vi.mock("ant-design-vue", () => ({
  message: { warning: mocks.warning, error: vi.fn() },
  Modal: { confirm: mocks.confirm },
}));
vi.mock("vue-router", () => ({
  onBeforeRouteLeave: mocks.leave,
  onBeforeRouteUpdate: mocks.update,
}));
import ImportCasesModal from "./ImportCasesModal.vue";
import { componentHost, flushComponent as flush } from "@/test/componentHost";
const valid = {
  data: {
    status: "success",
    data: { total: 2, validated: 2, errors: 0, preview: { to_create: 2 } },
  },
};
beforeEach(() => {
  vi.clearAllMocks();
  vi.stubGlobal("window", {
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
  });
  mocks.post.mockResolvedValue(valid);
});
describe("导入用例确认向导", () => {
  it("选文件与校验都不写入；必须经过确认页且重复点击只发起一次写入", async () => {
    const success = vi.fn(),
      { state: s, stop } = componentHost(ImportCasesModal, {
        visible: true,
        projectId: "p",
        onSuccess: success,
      });
    s.selectFile(new File(["data"], "cases.xmind"));
    expect(mocks.post).not.toHaveBeenCalled();
    await s.validate();
    expect(mocks.post.mock.calls[0][2].params).toEqual({
      validate_only: true,
      overwrite: false,
    });
    expect(s.step).toBe(1);
    await s.submit();
    expect(mocks.post).toHaveBeenCalledTimes(1);
    let finish!: (value: any) => void;
    mocks.post.mockReturnValueOnce(new Promise((r) => (finish = r)));
    s.step = 2;
    const write = s.submit();
    await s.submit();
    expect(mocks.post).toHaveBeenCalledTimes(2);
    expect(mocks.post.mock.calls[1][2].params.validate_only).toBe(false);
    expect(await s.beforeClose()).toBe(false);
    finish(valid);
    await write;
    expect(success).toHaveBeenCalledTimes(1);
    stop();
  });
  it("校验失败保留文件但禁止确认；改覆盖选项必须重新校验", async () => {
    mocks.post.mockRejectedValueOnce(new Error("synthetic"));
    const { state: s, stop } = componentHost(ImportCasesModal, {
      visible: true,
      projectId: "p",
    });
    s.selectFile(new File(["data"], "cases.csv"));
    await s.validate();
    expect(s.file.name).toBe("cases.csv");
    expect(s.validated).toBe(false);
    s.step = 2;
    await s.submit();
    expect(mocks.post).toHaveBeenCalledTimes(1);
    await s.validate();
    expect(s.validated).toBe(true);
    s.back();
    s.overwrite = true;
    await flush();
    expect(s.validated).toBe(false);
    expect(s.step).toBe(0);
    stop();
  });
  it("切项目取消旧校验结果，迟到响应不能使新项目可导入", async () => {
    let finish!: (value: any) => void;
    mocks.post.mockReturnValueOnce(new Promise((r) => (finish = r)));
    const closed = vi.fn(),
      {
        state: s,
        props,
        stop,
      } = componentHost(ImportCasesModal, {
        visible: true,
        projectId: "old",
        "onUpdate:visible": closed,
      });
    s.selectFile(new File(["data"], "cases.csv"));
    const pending = s.validate();
    props.projectId = "new";
    await flush();
    finish(valid);
    await pending;
    expect(mocks.post.mock.calls[0][0]).toBe("/projects/old/cases/import");
    expect(s.file).toBeUndefined();
    expect(s.validated).toBe(false);
    expect(closed).toHaveBeenCalledWith(false);
    stop();
  });
  it("取消离开保留草稿，确认离开清除校验并关闭同页面弹窗", async () => {
    const closed = vi.fn(),
      { state: s, stop } = componentHost(ImportCasesModal, {
        visible: true,
        projectId: "p",
        "onUpdate:visible": closed,
      });
    s.selectFile(new File(["data"], "cases.csv"));
    await s.validate();
    const first = s.beforeClose();
    mocks.confirm.mock.calls[0][0].onCancel();
    expect(await first).toBe(false);
    expect(s.validated).toBe(true);
    const second = mocks.update.mock.calls[0][0]();
    mocks.confirm.mock.calls[1][0].onOk();
    expect(await second).toBe(true);
    expect(s.file).toBeUndefined();
    expect(s.validated).toBe(false);
    expect(closed).toHaveBeenCalledWith(false);
    stop();
  });
});
