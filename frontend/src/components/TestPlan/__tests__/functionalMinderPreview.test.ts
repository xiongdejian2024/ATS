import { describe, it, expect, vi } from "vitest";
import { prepareFunctionalMinderPreview } from "../functionalMinderScope";
function deferred<T>() {
  let resolve!: (value: T) => void;
  const promise = new Promise<T>((done) => {
    resolve = done;
  });
  return { promise, resolve };
}
describe("脑图执行预览的异步上下文保护", () => {
  it("清理旧图片期间切计划，不把旧范围发送给新计划", async () => {
    let current = true;
    const gate = deferred<void>();
    const cleanup = vi.fn(() => gate.promise),
      preview = vi.fn(async () => ({ count: 2 }));
    const promise = prepareFunctionalMinderPreview(
      { selectAll: true, condition: { search: "旧条件" } },
      "old-plan",
      {
        isCurrent: () => current,
        confirm: async () => true,
        cleanup,
        preview,
      },
    );
    await Promise.resolve();
    expect(cleanup).toHaveBeenCalledOnce();
    current = false;
    gate.resolve();
    expect(await promise).toBeUndefined();
    expect(preview).not.toHaveBeenCalled();
  });
  it("确认期间切目录，不清理新页面或发出预览", async () => {
    let current = true;
    const gate = deferred<boolean>();
    const cleanup = vi.fn(async () => {}),
      preview = vi.fn(async () => ({ count: 1 }));
    const promise = prepareFunctionalMinderPreview(
      { selectIds: ["one"] },
      "plan",
      {
        isCurrent: () => current,
        confirm: () => gate.promise,
        cleanup,
        preview,
      },
    );
    current = false;
    gate.resolve(true);
    expect(await promise).toBeUndefined();
    expect(cleanup).not.toHaveBeenCalled();
    expect(preview).not.toHaveBeenCalled();
  });
  it("请求途中取消选择，不重新打开陈旧表单", async () => {
    let current = true;
    const gate = deferred<{ count: number }>();
    const preview = vi.fn(() => gate.promise);
    const promise = prepareFunctionalMinderPreview(
      { selectIds: ["one"] },
      "plan",
      {
        isCurrent: () => current,
        confirm: async () => true,
        cleanup: async () => {},
        preview,
      },
    );
    await Promise.resolve();
    await Promise.resolve();
    expect(preview).toHaveBeenCalledWith("plan", { selectIds: ["one"] });
    current = false;
    gate.resolve({ count: 1 });
    expect(await promise).toBeUndefined();
  });
  it("冻结原计划和完整筛选范围，嵌套草稿修改不改变请求", async () => {
    const gate = deferred<boolean>(),
      selection = {
        selectAll: true,
        condition: { folderIds: ["parent"], search: "before" },
      };
    const preview = vi.fn(async () => ({ count: 102, canExecute: true }));
    const promise = prepareFunctionalMinderPreview(selection, "plan-a", {
      isCurrent: () => true,
      confirm: () => gate.promise,
      cleanup: async () => {},
      preview,
    });
    selection.condition.search = "after";
    selection.condition.folderIds.push("other");
    gate.resolve(true);
    const result = await promise;
    expect(preview).toHaveBeenCalledWith("plan-a", {
      selectAll: true,
      condition: { folderIds: ["parent"], search: "before" },
    });
    expect(result?.preview.count).toBe(102);
    expect(result?.selection).not.toBe(selection);
  });
  it("拒绝丢弃草稿与初始无效请求不产生副作用", async () => {
    const cleanup = vi.fn(async () => {}),
      preview = vi.fn(async () => ({ count: 1 })),
      confirm = vi.fn(async () => false);
    expect(
      await prepareFunctionalMinderPreview({ selectIds: ["one"] }, "plan", {
        isCurrent: () => true,
        confirm,
        cleanup,
        preview,
      }),
    ).toBeUndefined();
    expect(cleanup).not.toHaveBeenCalled();
    expect(preview).not.toHaveBeenCalled();
    confirm.mockClear();
    await prepareFunctionalMinderPreview({ selectIds: ["one"] }, "plan", {
      isCurrent: () => false,
      confirm,
      cleanup,
      preview,
    });
    expect(confirm).not.toHaveBeenCalled();
  });
});

import { functionalExecutionDraftChanged } from "../functionalMinderScope";
describe("执行结果草稿离开保护", () => {
  const empty = {
    description: "",
    dialogDirty: false,
    steps: "[]",
    initialSteps: "[]",
    result: "passed",
    initialResult: "passed",
  };
  it("只改变结果也必须提示；改回原结果恢复干净", () => {
    expect(functionalExecutionDraftChanged(empty)).toBe(false);
    expect(
      functionalExecutionDraftChanged({ ...empty, result: "failed" }),
    ).toBe(true);
    expect(
      functionalExecutionDraftChanged({ ...empty, result: "blocked" }),
    ).toBe(true);
  });
  it("载入已有失败结果不误报修改；描述、步骤或子弹窗仍受保护", () => {
    expect(
      functionalExecutionDraftChanged({
        ...empty,
        result: "failed",
        initialResult: "failed",
      }),
    ).toBe(false);
    expect(
      functionalExecutionDraftChanged({ ...empty, description: "新描述" }),
    ).toBe(true);
    expect(
      functionalExecutionDraftChanged({
        ...empty,
        steps: '[{"result":"failed"}]',
      }),
    ).toBe(true);
    expect(
      functionalExecutionDraftChanged({ ...empty, dialogDirty: true }),
    ).toBe(true);
  });
});
