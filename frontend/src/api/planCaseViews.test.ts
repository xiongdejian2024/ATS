import { it, expect, vi } from "vitest";
vi.mock("@/utils/api", () => ({
  apiClient: { get: vi.fn(), post: vi.fn(), put: vi.fn(), delete: vi.fn() },
}));
import { apiClient } from "@/utils/api";
import { planCaseWorkspaceApi as api } from "./planCaseWorkspace";

it("视图读写按工作区/关联入口及分类携带相同隔离参数", async () => {
  await api.views("计划", "api", "association");
  expect(apiClient.get).toHaveBeenLastCalledWith(
    "/plan-orchestration/plans/计划/case-workspace/candidates/views",
    { params: { category: "api" } },
  );
  await api.saveView("计划", "视图", {}, "scenario", "association");
  expect(apiClient.post).toHaveBeenLastCalledWith(
    "/plan-orchestration/plans/计划/case-workspace/candidates/views",
    { name: "视图", filters: {} },
    { params: { category: "scenario" } },
  );
  await api.updateView(
    "计划",
    "视图ID",
    "改名",
    undefined,
    "api",
    "association",
  );
  expect(apiClient.put).toHaveBeenLastCalledWith(
    "/plan-orchestration/plans/计划/case-workspace/candidates/views/视图ID",
    { name: "改名" },
    { params: { category: "api" } },
  );
  await api.deleteView("计划", "视图ID", "api", "association");
  expect(apiClient.delete).toHaveBeenLastCalledWith(
    "/plan-orchestration/plans/计划/case-workspace/candidates/views/视图ID",
    { params: { category: "api" } },
  );
  await api.views("计划");
  expect(apiClient.get).toHaveBeenLastCalledWith(
    "/plan-orchestration/plans/计划/case-workspace/views",
    { params: { category: "functional" } },
  );
});
