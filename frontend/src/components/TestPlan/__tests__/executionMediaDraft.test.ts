import { describe, it, expect, vi } from "vitest";
import { ExecutionMediaDraft } from "../executionMediaDraft";

describe("执行图片草稿生命周期", () => {
  it("按上传时的计划分组，已提交和已删除编号都从待清理列表移除", async () => {
    const remove = vi.fn(async (_plan: string, ids: string[]) => ({
      removed: [],
      retained: ids,
      missing: [],
    }));
    const draft = new ExecutionMediaDraft(remove);
    draft.track("旧计划", "a");
    draft.track("当前计划", "b");
    await draft.cleanup();
    expect(remove.mock.calls).toEqual([
      ["旧计划", ["a"]],
      ["当前计划", ["b"]],
    ]);
    expect(draft.size).toBe(0);
    await draft.cleanup();
    expect(remove).toHaveBeenCalledTimes(2);
  });
  it("清理失败保留编号供重试，记录异常后不阻塞退出编辑", async () => {
    const error = new Error("软件回归模拟清理网络失败"),
      log = vi.spyOn(console, "error").mockImplementation(() => {});
    const remove = vi
      .fn()
      .mockRejectedValueOnce(error)
      .mockResolvedValueOnce({ removed: ["a"], retained: [], missing: [] });
    try {
      const draft = new ExecutionMediaDraft(remove);
      draft.track("p", "a");
      await draft.cleanup();
      expect(draft.size).toBe(1);
      expect(log).toHaveBeenCalledWith(
        "清理未提交执行图片失败，保留待重试编号",
        error,
      );
      await draft.cleanup();
      expect(draft.size).toBe(0);
      expect(remove.mock.calls).toEqual([
        ["p", ["a"]],
        ["p", ["a"]],
      ]);
    } finally {
      log.mockRestore();
    }
  });
  it("等待服务端期间新上传的图片不被旧清理确认吞掉", async () => {
    let finish!: (value: {
      removed: string[];
      retained: string[];
      missing: string[];
    }) => void;
    const remove = vi
      .fn()
      .mockImplementationOnce(
        () =>
          new Promise((resolve) => {
            finish = resolve;
          }),
      )
      .mockResolvedValueOnce({ removed: ["b"], retained: [], missing: [] });
    const draft = new ExecutionMediaDraft(remove);
    draft.track("p", "a");
    const pending = draft.cleanup();
    await Promise.resolve();
    draft.track("p", "b");
    finish({ removed: ["a"], retained: [], missing: [] });
    await pending;
    expect(draft.size).toBe(1);
    await draft.cleanup();
    expect(remove.mock.calls).toEqual([
      ["p", ["a"]],
      ["p", ["b"]],
    ]);
  });
  it("大批草稿按实际接口500个上限拆分，不丢失确认", async () => {
    const remove = vi.fn(async (_plan: string, ids: string[]) => ({
      removed: ids,
      retained: [],
      missing: [],
    }));
    const draft = new ExecutionMediaDraft(remove);
    for (let i = 0; i < 501; i++) draft.track("p", String(i));
    await draft.cleanup();
    expect(remove.mock.calls.map(([, ids]) => ids.length)).toEqual([500, 1]);
    expect(draft.size).toBe(0);
  });
});
