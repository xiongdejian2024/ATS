import { afterEach, describe, expect, it, vi } from "vitest";
import { effectScope, ref, computed, nextTick, type EffectScope } from "vue";
import { usePlanCandidateSelection } from "../planCandidateSelection";
import { moduleDescendants } from "../planCandidateModules";
import {
  planCaseWorkspaceApi,
  type CandidateCondition,
  type CaseFolder,
} from "@/api/planCaseWorkspace";
vi.mock("@/api/planCaseWorkspace", () => ({
  planCaseWorkspaceApi: { previewCandidates: vi.fn() },
}));
const scopes: EffectScope[] = [];
const flush = async () => {
  await nextTick();
  await Promise.resolve();
  await nextTick();
};
function setup() {
  const enabled = ref(true),
    query = ref<CandidateCondition>({ folder: "all", search: "范围" });
  const modules = ref<CaseFolder[]>([
    { id: "parent", name: "父", count: 24 },
    { id: "child", parentId: "parent", name: "子", count: 23 },
    { id: "sibling", name: "另", count: 1 },
  ]);
  const rows = ref<{ id: string; moduleId?: string | null }[]>([
    { id: "one", moduleId: "child" },
    { id: "two", moduleId: "child" },
  ]);
  const scope = effectScope();
  scopes.push(scope);
  const s = scope.run(() =>
    usePlanCandidateSelection(
      ref("plan"),
      ref("functional"),
      query,
      computed(() => rows.value.map((row) => row.id)),
      { enabled, modules, rows },
    ),
  )!;
  vi.mocked(planCaseWorkspaceApi.previewCandidates).mockResolvedValue({
    count: 24,
    excludedCount: 0,
    automatedCount: 0,
    usesTree: false,
    canAssociate: true,
    compatibleSuiteIds: [],
    eligibleCount: 26,
    moduleCounts: {
      parent: { total: 1, selected: 1 },
      child: { total: 23, selected: 22 },
      sibling: { total: 1, selected: 1 },
      unassigned: { total: 1, selected: 0 },
    },
  });
  return { s, rows, modules, query, enabled };
}
afterEach(() => {
  scopes.splice(0).forEach((scope) => scope.stop());
  vi.resetAllMocks();
});
describe("计划关联多模块联动", () => {
  it("父子组合跨页排除，切换目录保留范围，半选与逐条回显", async () => {
    const { s, query, rows } = setup();
    s.checkModule("parent", true);
    s.checkModule("sibling", true);
    await flush();
    expect(Object.keys(s.request.value!.moduleMaps!)).toEqual([
      "parent",
      "child",
      "sibling",
    ]);
    expect(s.request.value?.caseIds).toBeUndefined();
    s.keysChanged(["two"]);
    await flush();
    rows.value = [
      { id: "three", moduleId: "child" },
      { id: "four", moduleId: "child" },
    ];
    s.keysChanged(["three"]);
    await flush();
    expect(s.request.value!.moduleMaps!.child.excludeIds).toEqual([
      "one",
      "four",
    ]);
    query.value = { ...query.value, folder: "sibling" };
    rows.value = [{ id: "other", moduleId: "sibling" }];
    await flush();
    expect(s.pageSelected.value).toEqual(["other"]);
    expect(s.request.value!.condition!.folder).toBe("all");
    expect(s.request.value!.moduleMaps!.child.excludeIds).toEqual([
      "one",
      "four",
    ]);
    expect(s.modules!.halfChecked("parent")).toBe(true);
    expect(s.modules!.checked("sibling")).toBe(true);
    expect(s.modules!.treeChecked.value.halfChecked).toContain("child");
  });
  it("全部模块取消子模块保留其他和未分配，重新勾选清除该模块排除", async () => {
    const { s, rows } = setup();
    s.checkModule("all", true);
    await flush();
    s.keysChanged(["two"]);
    await flush();
    s.checkModule("parent", false);
    await flush();
    expect(s.pageSelected.value).toEqual([]);
    expect(s.request.value!.moduleMaps!.all.selectAll).toBe(true);
    expect(s.request.value!.moduleMaps!.child.selectAll).toBe(false);
    rows.value = [{ id: "free", moduleId: null }];
    expect(s.pageSelected.value).toEqual(["free"]);
    s.checkModule("child", true);
    await flush();
    expect(s.request.value!.moduleMaps!.child.excludeIds).toEqual([]);
    s.checkModule("all", false);
    await flush();
    expect(s.request.value).toBeUndefined();
  });
  it("逐条跨页保留；当前页替换当前模块范围并保留其他模块", async () => {
    const { s, query, rows } = setup();
    s.keysChanged(["one"]);
    await flush();
    expect(s.request.value!.moduleMaps!.child.selectIds).toEqual(["one"]);
    rows.value = [{ id: "three", moduleId: "child" }];
    s.keysChanged(["three"]);
    await flush();
    expect(s.request.value!.moduleMaps!.child.selectIds).toEqual([
      "one",
      "three",
    ]);
    s.checkModule("sibling", true);
    query.value = { ...query.value, folder: "child" };
    s.current();
    await flush();
    expect(s.request.value!.moduleMaps!.child.selectIds).toEqual(["three"]);
    expect(s.request.value!.moduleMaps!.sibling.selectAll).toBe(true);
    s.keysChanged([]);
    await flush();
    expect(s.request.value!.moduleMaps!.child).toBeUndefined();
    expect(s.hasSelection.value).toBe(true);
  });
  it("断网保留重试，保存锁定，搜索和高级模式切换清除组合", async () => {
    const { s, query, enabled } = setup();
    vi.mocked(planCaseWorkspaceApi.previewCandidates).mockRejectedValueOnce(
      new Error("模拟多模块预览断网"),
    );
    s.checkModule("parent", true);
    await flush();
    expect(s.ready.value).toBe(false);
    expect(s.request.value!.moduleMaps!.child.selectAll).toBe(true);
    await s.preview();
    expect(s.ready.value).toBe(true);
    s.working.value = true;
    s.checkModule("all", false);
    s.all();
    s.current();
    s.keysChanged([]);
    expect(s.request.value!.moduleMaps!.child.selectAll).toBe(true);
    s.working.value = false;
    query.value = { search: "新的条件", folder: "child" };
    await flush();
    expect(s.request.value).toBeUndefined();
    s.checkModule("parent", true);
    await flush();
    enabled.value = false;
    expect(s.request.value).toBeUndefined();
  });
  it("循环目录安全展开且使用完整目录不受搜索隐藏影响", () => {
    const rows = [
      { id: "a", parentId: "b", name: "甲", count: 0 },
      { id: "b", parentId: "a", name: "乙", count: 0 },
      { id: "c", parentId: "a", name: "丙", count: 0 },
    ];
    expect(moduleDescendants(rows, "a")).toEqual(["a", "b", "c"]);
    expect(moduleDescendants(rows, "all")).toEqual([
      "unassigned",
      "a",
      "b",
      "c",
    ]);
  });
});
