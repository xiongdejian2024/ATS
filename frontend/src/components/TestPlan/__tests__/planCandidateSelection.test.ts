import { describe, it, expect, vi, afterEach } from "vitest";
import { effectScope, nextTick, ref, type EffectScope } from "vue";
import { usePlanCandidateSelection } from "../planCandidateSelection";
import {
  planCaseWorkspaceApi,
  type CandidateCondition,
  type CandidateSelectionPreview,
  type CandidateSelection,
} from "@/api/planCaseWorkspace";

vi.mock("@/api/planCaseWorkspace", () => ({
  planCaseWorkspaceApi: { previewCandidates: vi.fn() },
}));
const scopes: EffectScope[] = [];
it("接口显式选择与范围排除保持资源身份，切换用例模式清理旧响应", async () => {
  const extras = ref<Pick<CandidateSelection, "resourceType">>({
    resourceType: "API",
  });
  const scope = effectScope();
  scopes.push(scope);
  const selection = scope.run(() =>
    usePlanCandidateSelection(
      ref("plan"),
      ref("api"),
      ref({}),
      ref(["definition"]),
      undefined,
      ref("source"),
      extras,
    ),
  )!;
  vi.mocked(planCaseWorkspaceApi.previewCandidates).mockResolvedValue({
    ...response(2),
    selectedDefinitionCount: 1,
  });
  selection.keysChanged(["definition"]);
  await flush();
  expect(selection.request.value).toEqual({
    category: "api",
    projectId: "source",
    resourceType: "API",
    definitionIds: ["definition"],
  });
  expect(selection.summary.value?.count).toBe(2);
  let finish!: (value: CandidateSelectionPreview) => void;
  vi.mocked(planCaseWorkspaceApi.previewCandidates).mockReturnValueOnce(
    new Promise((resolve) => (finish = resolve)),
  );
  selection.all();
  await flush();
  extras.value = { resourceType: "CASE" };
  await flush();
  finish({ ...response(999), selectedDefinitionCount: 999 });
  await flush();
  expect(selection.request.value).toBeUndefined();
  expect(selection.summary.value).toBeUndefined();
  selection.restore({ category: "api", caseIds: ["case"] });
  await flush();
  expect(selection.request.value?.caseIds).toEqual(["case"]);
  expect(selection.request.value?.definitionIds).toBeUndefined();
});
it("同步目标变化保留原选择和排除，旧同步预览不能覆盖新目标", async () => {
  const extras = ref<
    Pick<
      CandidateSelection,
      "syncCase" | "apiCaseCollectionId" | "apiScenarioCollectionId"
    >
  >({});
  const scope = effectScope();
  scopes.push(scope);
  const s = scope.run(() =>
    usePlanCandidateSelection(
      ref("plan"),
      ref("functional"),
      ref({}),
      ref(["one", "two"]),
      undefined,
      ref("source"),
      extras,
    ),
  )!;
  vi.mocked(planCaseWorkspaceApi.previewCandidates).mockResolvedValue(
    response(1),
  );
  s.all();
  s.keysChanged(["one"]);
  await flush();
  let finish!: (value: CandidateSelectionPreview) => void;
  vi.mocked(planCaseWorkspaceApi.previewCandidates).mockReturnValueOnce(
    new Promise((resolve) => (finish = resolve)),
  );
  extras.value = { syncCase: true, apiCaseCollectionId: "default" };
  await flush();
  expect(s.loading.value).toBe(true);
  const latest = {
    ...response(1),
    sync: {
      api: { count: 2, compatibleSuiteIds: ["api-suite"] },
      scenario: { count: 1, compatibleSuiteIds: ["scene-suite"] },
    },
  };
  vi.mocked(planCaseWorkspaceApi.previewCandidates).mockResolvedValueOnce(
    latest,
  );
  extras.value = {
    syncCase: true,
    apiCaseCollectionId: "api-target",
    apiScenarioCollectionId: "scenario-target",
  };
  await flush();
  finish({
    ...response(999),
    sync: {
      api: { count: 999, compatibleSuiteIds: [] },
      scenario: { count: 0, compatibleSuiteIds: [] },
    },
  });
  await flush();
  expect(s.request.value).toMatchObject({
    projectId: "source",
    selectAll: true,
    excludeIds: ["two"],
    apiCaseCollectionId: "api-target",
    apiScenarioCollectionId: "scenario-target",
  });
  expect(s.summary.value?.sync).toEqual(latest.sync);
  extras.value = {};
  await flush();
  expect(s.request.value?.syncCase).toBeUndefined();
  expect(s.request.value?.excludeIds).toEqual(["two"]);
});
const response = (count = 23): CandidateSelectionPreview => ({
  count,
  excludedCount: 0,
  automatedCount: 0,
  usesTree: false,
  compatibleSuiteIds: [],
  canAssociate: true,
});
const flush = async () => {
  await nextTick();
  await Promise.resolve();
  await nextTick();
};
function setup() {
  const plan = ref("plan"),
    category = ref<CandidateSelection["category"]>("functional"),
    query = ref<CandidateCondition>({ search: "范围", folder: "all" }),
    ids = ref(["one", "two"]);
  const scope = effectScope();
  scopes.push(scope);
  const selection = scope.run(() =>
    usePlanCandidateSelection(plan, category, query, ids),
  )!;
  vi.mocked(planCaseWorkspaceApi.previewCandidates).mockResolvedValue(
    response(),
  );
  return { plan, category, query, ids, selection };
}
afterEach(() => {
  scopes.splice(0).forEach((scope) => scope.stop());
  vi.resetAllMocks();
});

describe("计划关联筛选范围选择", () => {
  it("全选只提交条件，跨页排除保留，当前页勾选恢复不改其他页", async () => {
    const { selection: s, ids } = setup();
    s.all();
    await flush();
    expect(s.request.value).toEqual({
      category: "functional",
      selectAll: true,
      excludeIds: [],
      condition: { search: "范围", folder: "all" },
    });
    expect(s.pageSelected.value).toEqual(["one", "two"]);
    s.keysChanged(["two"]);
    await flush();
    ids.value = ["three", "four"];
    s.keysChanged(["three"]);
    await flush();
    expect(s.excluded.value).toEqual(["one", "four"]);
    ids.value = ["one", "two"];
    expect(s.pageSelected.value).toEqual(["two"]);
    s.togglePage();
    await flush();
    expect(s.excluded.value).toEqual(["four"]);
    expect(s.request.value?.caseIds).toBeUndefined();
    s.togglePage();
    await flush();
    expect(new Set(s.excluded.value)).toEqual(new Set(["one", "two", "four"]));
  });

  it("全选当前页切回逐条模式；逐条跨页选择与筛选保留；范围变化清全选", async () => {
    const { selection: s, query, ids, category } = setup();
    s.current();
    await flush();
    ids.value = ["three"];
    s.current();
    await flush();
    expect(s.selected.value).toEqual(["one", "two", "three"]);
    query.value = { search: "另外" };
    expect(s.selected.value).toHaveLength(3);
    s.all();
    await flush();
    s.current();
    await flush();
    expect(s.request.value).toEqual({
      category: "functional",
      caseIds: ["three"],
    });
    s.all();
    await flush();
    query.value = {
      filters: {
        conditions: [{ field: "apiChange", operator: "equals", value: false }],
        logic: "and",
      },
    };
    expect(s.request.value).toBeUndefined();
    s.keysChanged(["three"]);
    await flush();
    category.value = "api";
    expect(s.request.value).toBeUndefined();
  });

  it("预览失败保留条件与排除，重试成功后才能关联；写入期间不改选择", async () => {
    const { selection: s } = setup();
    vi.mocked(planCaseWorkspaceApi.previewCandidates).mockRejectedValueOnce(
      new Error("模拟范围预览断网"),
    );
    s.all();
    await flush();
    expect(s.error.value).toBe("选择范围核对失败，请重试");
    expect(s.ready.value).toBe(false);
    expect(s.request.value?.selectAll).toBe(true);
    s.keysChanged(["two"]);
    await flush();
    expect(s.excluded.value).toEqual(["one"]);
    expect(s.ready.value).toBe(true);
    s.working.value = true;
    s.keysChanged([]);
    s.all();
    s.current();
    s.togglePage();
    expect(s.excluded.value).toEqual(["one"]);
    expect(s.ready.value).toBe(false);
    s.working.value = false;
    vi.mocked(planCaseWorkspaceApi.previewCandidates).mockResolvedValueOnce({
      ...response(0),
      canAssociate: false,
    });
    await s.preview();
    expect(s.ready.value).toBe(false);
    expect(s.request.value?.excludeIds).toEqual(["one"]);
  });

  it("旧预览和旧项目响应不能覆盖新范围，重新读取真实自动化测试套", async () => {
    const { selection: s, plan } = setup();
    let resolveOld!: (value: CandidateSelectionPreview) => void;
    vi.mocked(planCaseWorkspaceApi.previewCandidates).mockReturnValueOnce(
      new Promise((resolve) => {
        resolveOld = resolve;
      }),
    );
    s.all();
    await flush();
    expect(s.loading.value).toBe(true);
    s.keysChanged(["two"]);
    await flush();
    expect(s.summary.value?.count).toBe(23);
    resolveOld(response(999));
    await flush();
    expect(s.summary.value?.count).toBe(23);
    vi.mocked(planCaseWorkspaceApi.previewCandidates).mockResolvedValueOnce({
      ...response(21),
      automatedCount: 2,
      usesTree: true,
      compatibleSuiteIds: ["suite-a"],
    });
    await s.preview();
    expect(s.summary.value?.compatibleSuiteIds).toEqual(["suite-a"]);
    expect(s.summary.value?.automatedCount).toBe(2);
    plan.value = "another-plan";
    expect(s.summary.value).toBeUndefined();
    expect(s.hasSelection.value).toBe(false);
  });
});

it("来源项目切换立即清除范围与排除，旧预览不得覆盖新项目", async () => {
  const project = ref<string | undefined>("source-one");
  const scope = effectScope();
  scopes.push(scope);
  const s = scope.run(() =>
    usePlanCandidateSelection(
      ref("plan"),
      ref("functional"),
      ref({}),
      ref(["one"]),
      undefined,
      project,
    ),
  )!;
  let finish!: (value: CandidateSelectionPreview) => void;
  vi.mocked(planCaseWorkspaceApi.previewCandidates).mockImplementationOnce(
    () =>
      new Promise((resolve) => {
        finish = resolve;
      }),
  );
  s.all();
  await flush();
  expect(s.request.value?.projectId).toBe("source-one");
  s.keysChanged([]);
  await flush();
  project.value = "source-two";
  expect(s.request.value).toBeUndefined();
  expect(s.excluded.value).toEqual([]);
  finish(response(999));
  await flush();
  expect(s.summary.value).toBeUndefined();
  vi.mocked(planCaseWorkspaceApi.previewCandidates).mockResolvedValue(
    response(1),
  );
  s.current();
  await flush();
  expect(s.request.value).toEqual({
    projectId: "source-two",
    category: "functional",
    caseIds: ["one"],
  });
  expect(s.summary.value?.count).toBe(1);
});
