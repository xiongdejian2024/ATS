import { beforeEach, describe, it, expect, vi } from "vitest";
const mocks = vi.hoisted(() => ({
  get: vi.fn(),
  update: vi.fn(),
  modules: vi.fn(),
  confirm: vi.fn(),
  templates: vi.fn(),
  project: { id: "p", name: "Project" },
  user: { id: "u" },
}));
vi.mock("@/api/testCase", () => ({
  testCaseApi: {
    getTestCases: mocks.get,
    updateTestCase: mocks.update,
    getFilterFields: vi.fn().mockResolvedValue([]),
  },
}));
vi.mock("@/api/project", () => ({ projectApi: { getModules: mocks.modules } }));
vi.mock("@/api/caseFeatures", () => ({
  saveCaseBlob: vi.fn(),
  caseFeaturesApi: new Proxy(
    {},
    {
      get: (_, key) =>
        key === "templates"
          ? mocks.templates
          : key === "recycle"
            ? vi.fn().mockResolvedValue({ total: 0 })
            : vi.fn().mockResolvedValue([]),
    },
  ),
}));
vi.mock("@/api/caseGovernance", () => ({
  caseGovernanceApi: new Proxy(
    {},
    {
      get: (_, key) =>
        vi
          .fn()
          .mockResolvedValue(
            key === "reviewers" ? [] : { count: 0, permissions: {} },
          ),
    },
  ),
}));
vi.mock("@/stores/project", () => ({
  useProjectStore: () => ({
    projects: [mocks.project],
    currentProject: mocks.project,
    fetchProjects: vi.fn(),
    setCurrentProject: vi.fn(),
  }),
}));
vi.mock("@/stores/user", () => ({
  useUserStore: () => ({ user: mocks.user }),
}));
vi.mock("@vueuse/core", () => ({
  useWindowSize: () => ({ width: { value: 1200 } }),
}));
vi.mock("vue-router", () => ({
  useRoute: () => ({ path: "/test-cases", query: {}, params: {} }),
  useRouter: () => ({ push: vi.fn(), replace: vi.fn() }),
  onBeforeRouteLeave: vi.fn(),
  onBeforeRouteUpdate: vi.fn(),
}));
vi.mock("ant-design-vue", () => ({
  message: { warning: vi.fn(), success: vi.fn(), error: vi.fn() },
  Modal: { confirm: mocks.confirm },
  Input: { render: () => null },
}));
vi.mock("@/components/TestCase/CaseMindMap.vue", () => ({
  default: { render: () => null },
}));
vi.mock("@/components/TestCase/TestCaseDetail.vue", () => ({
  default: { render: () => null },
}));
vi.mock("@/components/TestCase/TestCaseFilter.vue", () => ({
  default: { render: () => null },
}));
vi.mock("@/components/TestCase/ImportCasesModal.vue", () => ({
  default: { render: () => null },
}));
vi.mock("@/components/TestCase/CaseGovernancePanel.vue", () => ({
  default: { render: () => null },
}));
vi.mock("@/components/TestCase/CaseRecycleBin.vue", () => ({
  default: { render: () => null },
}));
vi.mock("@/components/TestCase/CaseTemplateManager.vue", () => ({
  default: { render: () => null },
}));
vi.mock("@/components/TestCase/CaseExportDialog.vue", () => ({
  default: { render: () => null },
}));
import TestCases from "./TestCases.vue";
import { componentHost, flushComponent as flush } from "@/test/componentHost";
const row = (action: string) => ({
  id: "c",
  name: "Case",
  updatedAt: "2026-10-08T10:00:00Z",
  steps: [{ step: 1, action, expected: "saved expected" }],
});
beforeEach(() => {
  vi.clearAllMocks();
  vi.stubGlobal("window", {
    innerWidth: 1200,
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
  });
  vi.stubGlobal("localStorage", {
    getItem: vi.fn().mockReturnValue(null),
    setItem: vi.fn(),
  });
  mocks.get.mockResolvedValue({ items: [row("old")], total: 1 });
  mocks.modules.mockResolvedValue({ modules: [], totalCaseCount: 1 });
  mocks.templates.mockResolvedValue([]);
  mocks.update.mockResolvedValue(row("PUT"));
});
describe("脑图保存确认与父层权威读取", () => {
  it("自定义字段异步加载前保存基础显示，加载后恢复原列宽和可见性", async () => {
    const storage = new Map<string, string>();
    const key = "ats:table-display:u:p:test-cases";
    storage.set(
      key,
      JSON.stringify({
        columns: [{ key: "customFields.model", visible: true, width: 280 }],
        pageSize: 20,
      }),
    );
    vi.stubGlobal("localStorage", {
      getItem: (key: string) => storage.get(key) || null,
      setItem: (key: string, value: string) => storage.set(key, value),
    });
    let finish!: (templates: any[]) => void;
    mocks.templates.mockReturnValue(new Promise((r) => (finish = r)));
    const { state: s, stop } = componentHost(TestCases, {});
    await flush();
    expect(s.columns.some((c: any) => c.key === "customFields.model")).toBe(
      false,
    );
    expect(s.persistTableDisplay({ ...s.tableDisplay, pageSize: 30 })).toBe(
      true,
    );
    expect(JSON.parse(storage.get(key)!).columns).toContainEqual({
      key: "customFields.model",
      visible: true,
      width: 280,
    });
    finish([
      {
        id: "template",
        name: "Template",
        fields: [{ key: "model", name: "车型", type: "text", options: [] }],
      },
    ]);
    await flush();
    expect(
      s.columns.find((c: any) => c.key === "customFields.model"),
    ).toMatchObject({
      width: 280,
      dataIndex: ["customFields", "model"],
      sorter: false,
    });
    expect(s.pagination.pageSize).toBe(30);
    stop();
  });
  it("成功的同秒后读返回新GET，失败后读返回PUT并保留列表", async () => {
    const { state: s, stop } = componentHost(TestCases, {});
    await flush();
    mocks.get.mockResolvedValue({ items: [row("new GET")], total: 1 });
    const saved = await s.saveMindNode("c", { expectedResult: "change" });
    expect(saved.steps[0].action).toBe("new GET");
    mocks.update.mockResolvedValue(row("next PUT"));
    mocks.get.mockRejectedValue(new Error("synthetic failed refresh"));
    const confirmed = await s.saveMindNode("c", {
      expectedResult: "second change",
    });
    expect(confirmed.steps[0].action).toBe("next PUT");
    expect(s.testCases[0].steps[0].action).toBe("new GET");
    stop();
  });
  it("保存期间同步拦截重复请求", async () => {
    let finish!: (value: any) => void;
    const { state: s, stop } = componentHost(TestCases, {});
    await flush();
    mocks.update.mockReturnValue(new Promise((r) => (finish = r)));
    const pending = s.saveMindNode("c", { name: "saved" });
    expect(await s.saveMindNode("c", { name: "duplicate" })).toBe(false);
    expect(mocks.update).toHaveBeenCalledTimes(1);
    finish(row("saved"));
    await pending;
    stop();
  });
});
