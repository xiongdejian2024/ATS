import { it, expect, vi, afterEach } from "vitest";
import { effectScope, nextTick, ref, type EffectScope } from "vue";
import { usePlanNativeSelection } from "../planNativeSelection";
import {
  planCaseWorkspaceApi,
  type NativeWorkspaceCondition,
  type NativeWorkspacePreview,
} from "@/api/planCaseWorkspace";
vi.mock("@/api/planCaseWorkspace", () => ({
  planCaseWorkspaceApi: { previewNativeSelection: vi.fn() },
}));
const scopes: EffectScope[] = [];
const result = (count = 25): NativeWorkspacePreview => ({
  count,
  eligibleCount: 25,
  excludedCount: 0,
  canModify: true,
});
const flush = async () => {
  await nextTick();
  await Promise.resolve();
  await nextTick();
};
function setup() {
  const plan = ref("plan"),
    category = ref<"api" | "scenario">("api"),
    query = ref<NativeWorkspaceCondition>({ folder: "all", protocols: "HTTP" }),
    ids = ref(["node:a:case", "node:b:case"]);
  const scope = effectScope();
  scopes.push(scope);
  vi.mocked(planCaseWorkspaceApi.previewNativeSelection).mockResolvedValue(
    result(),
  );
  const s = scope.run(() =>
    usePlanNativeSelection(plan, category, query, ids),
  )!;
  return { s, plan, category, query, ids, scope };
}
afterEach(() => {
  scopes.splice(0).forEach((scope) => scope.stop());
  vi.resetAllMocks();
});
it("显式选择跨页保留，取消本页只影响本页，重复主用例按实例区分", async () => {
  const { s, ids } = setup();
  s.current();
  await flush();
  ids.value = ["node:c:case", "node:d:case"];
  s.keysChanged(["node:c:case"]);
  await flush();
  expect(s.request.value?.selectIds).toEqual([
    "node:a:case",
    "node:b:case",
    "node:c:case",
  ]);
  ids.value = ["node:a:case", "node:b:case"];
  s.keysChanged(["node:b:case"]);
  await flush();
  expect(s.request.value?.selectIds).toEqual(["node:c:case", "node:b:case"]);
  expect(s.request.value?.condition).toBeUndefined();
});
it("所有页提交完整条件，跨页排除及恢复不丢其他页排除", async () => {
  const { s, ids } = setup();
  s.all();
  s.keysChanged(["node:b:case"]);
  await flush();
  ids.value = ["node:c:case", "node:d:case"];
  s.keysChanged(["node:c:case"]);
  await flush();
  expect(s.request.value).toEqual({
    category: "api",
    selectAll: true,
    excludeIds: ["node:a:case", "node:d:case"],
    condition: { folder: "all", protocols: "HTTP" },
  });
  ids.value = ["node:a:case", "node:b:case"];
  s.togglePage();
  await flush();
  expect(s.excluded.value).toEqual(["node:d:case"]);
  s.togglePage();
  await flush();
  expect(s.selectAll.value).toBe(true);
  expect(new Set(s.excluded.value)).toEqual(
    new Set(["node:a:case", "node:b:case", "node:d:case"]),
  );
  s.current();
  await flush();
  expect(s.selectAll.value).toBe(false);
  expect(s.selected.value).toEqual(ids.value);
});
it("范围变化清空选择，分页数据变化保留；分类和计划变化清空", async () => {
  const { s, ids, query, category, plan } = setup();
  s.all();
  await flush();
  ids.value = ["node:c:case"];
  await flush();
  expect(s.selectAll.value).toBe(true);
  query.value = { folder: "default" };
  expect(s.hasSelection.value).toBe(false);
  s.current();
  await flush();
  category.value = "scenario";
  expect(s.hasSelection.value).toBe(false);
  s.current();
  await flush();
  plan.value = "another";
  expect(s.hasSelection.value).toBe(false);
});
it("核对失败保留选择和排除，禁止提交，重试恢复服务端实际数量", async () => {
  const { s } = setup();
  vi.mocked(planCaseWorkspaceApi.previewNativeSelection).mockRejectedValueOnce(
    new Error("隔离网络失败"),
  );
  s.all();
  s.keysChanged(["node:b:case"]);
  await flush();
  expect(s.error.value).toBeTruthy();
  expect(s.ready.value).toBe(false);
  expect(s.excluded.value).toEqual(["node:a:case"]);
  vi.mocked(planCaseWorkspaceApi.previewNativeSelection).mockResolvedValueOnce({
    ...result(23),
    excludedCount: 1,
  });
  await s.preview();
  expect(s.summary.value?.count).toBe(23);
  expect(s.ready.value).toBe(true);
});
it("旧范围异步响应及卸载后的响应不能回填，保存期间不允许选择变更", async () => {
  const { s, scope } = setup();
  let finish!: (v: NativeWorkspacePreview) => void;
  vi.mocked(planCaseWorkspaceApi.previewNativeSelection).mockReturnValueOnce(
    new Promise((resolve) => (finish = resolve)),
  );
  s.all();
  await flush();
  s.clear();
  finish(result(999));
  await flush();
  expect(s.summary.value).toBeUndefined();
  s.current();
  await flush();
  s.working.value = true;
  s.all();
  s.keysChanged([]);
  s.current();
  expect(s.selectAll.value).toBe(false);
  expect(s.selected.value.length).toBe(2);
  s.working.value = false;
  vi.mocked(planCaseWorkspaceApi.previewNativeSelection).mockReturnValueOnce(
    new Promise((resolve) => (finish = resolve)),
  );
  s.all();
  await flush();
  scope.stop();
  finish(result(999));
  await flush();
  expect(s.summary.value).toBeUndefined();
});

it("执行权限与编辑权限独立，归档及保存中禁用执行", async () => {
  const { s } = setup();
  vi.mocked(planCaseWorkspaceApi.previewNativeSelection).mockResolvedValue({
    ...result(),
    canModify: false,
    canExecute: true,
  });
  s.current();
  await flush();
  expect(s.ready.value).toBe(false);
  expect(s.executeReady.value).toBe(true);
  s.working.value = true;
  expect(s.executeReady.value).toBe(false);
  s.working.value = false;
  vi.mocked(planCaseWorkspaceApi.previewNativeSelection).mockResolvedValue({
    ...result(),
    canModify: false,
    canExecute: false,
  });
  await s.preview();
  expect(s.executeReady.value).toBe(false);
});
