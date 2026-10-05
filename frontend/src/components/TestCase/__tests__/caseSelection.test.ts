import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { effectScope, nextTick, ref } from "vue";
const mocks = vi.hoisted(() => ({ preview: vi.fn() }));
vi.mock("@/api/caseGovernance", () => ({
  caseGovernanceApi: { previewSelection: mocks.preview },
}));
import {
  useCaseSelection,
  readReviewSelection,
  saveReviewSelection,
} from "../caseSelection";
let scope: ReturnType<typeof effectScope>;
function setup() {
  scope = effectScope();
  const project = ref("p"),
    query = ref<Record<string, unknown>>({ search: "范围" }),
    ids = ref<string[]>([]),
    page = ref(["a", "b"]);
  const state = scope.run(() => useCaseSelection(project, query, ids, page))!;
  return { project, query, ids, page, state };
}
beforeEach(() => {
  mocks.preview
    .mockReset()
    .mockResolvedValue({ count: 23, permissions: { update: true } });
});
afterEach(() => {
  scope?.stop();
  vi.restoreAllMocks();
});
const settle = async () => {
  await nextTick();
  await nextTick();
};
describe("主用例跨页范围选择", () => {
  it("翻页和表头只改变当前页排除，返回后保留其他页；当前页菜单退出范围", async () => {
    const { state, page, ids } = setup();
    state.all();
    await settle();
    expect(state.count.value).toBe(23);
    state.keysChanged(["b"]);
    await settle();
    page.value = ["c", "d"];
    state.keysChanged(["d"]);
    await settle();
    expect(state.request.value).toEqual({
      selectAll: true,
      condition: { search: "范围" },
      excludeIds: ["a", "c"],
    });
    page.value = ["a", "b"];
    expect(state.pageSelected.value).toEqual(["b"]);
    state.keysChanged(["a", "b"]);
    expect(state.excluded.value).toEqual(["c"]);
    state.current();
    await settle();
    expect(state.request.value).toEqual({ caseIds: ["a", "b"] });
    expect(ids.value).toEqual(["a", "b"]);
  });
  it("核对失败保留范围但禁用写入，重试成功再开放；零范围不可操作", async () => {
    const { state } = setup();
    vi.spyOn(console, "error").mockImplementation(() => {});
    mocks.preview.mockRejectedValueOnce(new Error("注入断网"));
    state.all();
    await settle();
    expect(state.error.value).toContain("失败");
    expect(state.count.value).toBeUndefined();
    expect(state.ready.value).toBe(false);
    expect(state.request.value?.condition).toEqual({ search: "范围" });
    await state.preview();
    expect(state.ready.value).toBe(true);
    mocks.preview.mockResolvedValueOnce({
      count: 0,
      permissions: { update: true },
    });
    await state.preview();
    expect(state.ready.value).toBe(false);
  });
  it("旧请求乱序返回和项目切换不能恢复旧数量或排除", async () => {
    const { state, project } = setup();
    let complete!: (value: any) => void;
    mocks.preview.mockReturnValueOnce(
      new Promise((resolve) => (complete = resolve)),
    );
    state.all();
    await nextTick();
    state.keysChanged(["b"]);
    await settle();
    expect(state.count.value).toBe(23);
    complete({ count: 999, permissions: { delete: true } });
    await settle();
    expect(state.count.value).toBe(23);
    expect(state.excluded.value).toEqual(["a"]);
    project.value = "other";
    await settle();
    expect(state.request.value).toBeUndefined();
    expect(state.count.value).toBeUndefined();
  });
  it("保存期间忽略勾选和选择菜单，筛选改变清空而分页保留", async () => {
    const { state, page, query } = setup();
    state.all();
    await settle();
    state.working.value = true;
    state.keysChanged([]);
    state.current();
    expect(state.selectAll.value).toBe(true);
    expect(state.excluded.value).toEqual([]);
    page.value = ["x"];
    expect(state.hasSelection.value).toBe(true);
    query.value = { search: "新范围" };
    expect(state.request.value).toBeUndefined();
    expect(state.working.value).toBe(true);
  });
  it("评审草稿范围可恢复，跨项目与过期键拒绝，不共享可变对象", () => {
    const entries = new Map<string, string>();
    const storage = {
      setItem: (key: string, value: string) => {
        entries.set(key, value);
      },
      getItem: (key: string) => entries.get(key) ?? null,
      removeItem: (key: string) => {
        entries.delete(key);
      },
      clear: () => entries.clear(),
      key: (index: number) => [...entries.keys()][index] ?? null,
      length: 0,
    } as Storage;
    const key = saveReviewSelection(
      "p",
      { selectAll: true, condition: { mine: true }, excludeIds: ["a"] },
      storage,
    );
    const body = readReviewSelection("p", key, storage);
    body.excludeIds!.push("b");
    expect(readReviewSelection("p", key, storage).excludeIds).toEqual(["a"]);
    expect(() => readReviewSelection("other", key, storage)).toThrow(
      "当前项目",
    );
    expect(() =>
      readReviewSelection("p", "ats-case-selection:missing", storage),
    ).toThrow("过期");
    expect(() => readReviewSelection("p", "untrusted", storage)).toThrow(
      "无效",
    );
  });
});
