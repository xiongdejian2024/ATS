import { beforeEach, describe, expect, it, vi } from "vitest";
const mocks = vi.hoisted(() => ({
  get: vi.fn(),
  post: vi.fn(),
  put: vi.fn(),
  delete: vi.fn(),
  rawGet: vi.fn(),
}));
vi.mock("@/utils/api", () => ({
  apiClient: {
    get: mocks.get,
    post: mocks.post,
    put: mocks.put,
    delete: mocks.delete,
    getInstance: () => ({ get: mocks.rawGet }),
  },
}));
import { testCaseApi } from "@/api/testCase";
import { caseFeaturesApi } from "@/api/caseFeatures";
import { caseGovernanceApi } from "@/api/caseGovernance";
beforeEach(() => { vi.clearAllMocks(); });
describe("用例前端实际接口契约", () => {
  it("组合OR筛选、排序、个人范围与选中编号全部传递", async () => {
    const filters = {
      conditions: [
        { field: "name", operator: "contains", value: "中文" },
        { field: "priority", operator: "equals", value: "P0" },
      ],
      logic: "or",
    };
    await testCaseApi.getTestCases("project", {
      filters,
      sortBy: "name",
      sortOrder: "asc",
      mine: true,
      followed: false,
      caseIds: "a,b",
    });
    expect(mocks.get).toHaveBeenCalledWith("/test-cases", {
      params: {
        project_id: "project",
        filters: JSON.stringify(filters),
        sort_by: "name",
        sort_order: "asc",
        mine: true,
        followed: false,
        case_ids: "a,b",
      },
    });
  });
  it("附件使用multipart而不是默认JSON；下载保留Blob", async () => {
    const file = new Blob(["附件内容"], { type: "text/plain" }) as File;
    await caseFeaturesApi.upload("p", "c", file);
    const [path, body, config] = mocks.post.mock.calls[0];
    expect(path).toBe("/projects/p/case-features/cases/c/attachments");
    expect(body).toBeInstanceOf(FormData);
    expect(config.headers["Content-Type"]).toBe("multipart/form-data");
    mocks.rawGet.mockResolvedValue({ data: file });
    expect(await caseFeaturesApi.download("p", "a")).toBe(file);
  });
  it("预校验强制validate_only不写入用例", async () => {
    await testCaseApi.validateImport("p", new Blob(["x"]) as File);
    expect(mocks.post.mock.calls[0][0]).toBe(
      "/projects/p/cases/import?validate_only=true",
    );
  });
  it("XMind与选定ID、组合筛选使用相同导出接口", async () => {
    mocks.rawGet.mockResolvedValue({ data: new Blob(["x"]) });
    await testCaseApi.exportCases("p", {
      format: "xmind",
      caseIds: "a,b",
      filters: { logic: "and", conditions: [] },
    });
    const path = mocks.rawGet.mock.calls[0][0];
    const query = new URL(path, "http://localhost").searchParams;
    expect(query.get("format")).toBe("xmind");
    expect(query.get("case_ids")).toBe("a,b");
    expect(JSON.parse(query.get("filters")!)).toEqual({
      logic: "and",
      conditions: [],
    });
  });
  it("复制使用真实治理接口，剥离原用例ID并保留目标模块", async () => {
    mocks.get
      .mockResolvedValueOnce({ id: "c", moduleId: "module" })
      .mockResolvedValueOnce({ id: "new" });
    mocks.post.mockResolvedValueOnce({ caseIds: ["new"] });
    await testCaseApi.copyCase("p", "c");
    expect(mocks.post).toHaveBeenCalledWith(
      "/projects/p/case-governance/batch-copy",
      { caseIds: ["c"], moduleId: "module" },
    );
    expect(mocks.get).toHaveBeenLastCalledWith("/test-cases/new", {
      params: { project_id: "p" },
    });
  });
  it("评审新模式及建议不降级为旧any策略", async () => {
    await caseGovernanceApi.createReview("p", {
      name: "评审",
      mode: "single",
      caseIds: ["c"],
      reviewerIds: ["u"],
      itemReviewers: { c: ["u"] },
      startDate: "2026-10-01",
      endDate: "2026-10-02",
    });
    expect(mocks.post.mock.calls[0][1]).not.toHaveProperty("policy");
    await caseGovernanceApi.vote("p", "r", "i", "suggestion", "补充边界");
    expect(mocks.post).toHaveBeenLastCalledWith(
      "/projects/p/case-governance/reviews/r/items/i/decision",
      { decision: "suggestion", comment: "补充边界" },
    );
  });
  it("附件/回收站恢复/彻底删除均携带项目范围", async () => {
    await caseFeaturesApi.restore("p", "c");
    await caseFeaturesApi.purge("p", "c");
    expect(mocks.post).toHaveBeenCalledWith(
      "/projects/p/case-features/cases/c/restore",
    );
    expect(mocks.delete).toHaveBeenCalledWith(
      "/projects/p/case-features/cases/c/purge",
    );
  });
});
