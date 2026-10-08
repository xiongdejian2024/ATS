import { beforeEach, describe, expect, it, vi } from "vitest";
const mocks = vi.hoisted(() => ({
  confirm: vi.fn(),
  error: vi.fn(),
  warning: vi.fn(),
  info: vi.fn(),
}));
vi.mock("ant-design-vue", () => ({
  message: mocks,
  Modal: { confirm: mocks.confirm },
}));
vi.mock("echarts/core", () => ({ use: vi.fn() }));
vi.mock("echarts/charts", () => ({ TreeChart: {} }));
vi.mock("echarts/components", () => ({ TooltipComponent: {} }));
vi.mock("echarts/renderers", () => ({ CanvasRenderer: {} }));
vi.mock("vue-echarts", () => ({ default: { render: () => null } }));
vi.mock("./CaseRichText.vue", () => ({ default: { render: () => null } }));
import CaseMindMap from "./CaseMindMap.vue";
import { componentHost, flushComponent as flush } from "@/test/componentHost";
const cases = [
  {
    id: "a",
    name: "Alpha",
    moduleId: "m",
    caseEditType: "TEXT",
    textDescription: "<p>Saved</p>",
    expectedResult: "<p>OK</p>",
    steps: [],
  },
  { id: "b", name: "Beta", moduleId: "m", steps: [] },
];
const node = (id = "a", kind = "textDescription") => ({
  data: { id: `case:${id}:${kind}`, caseId: id, kind, name: kind },
});
beforeEach(() => {
  vi.clearAllMocks();
  vi.stubGlobal("window", {
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
  });
  mocks.confirm.mockImplementation((o) => o.onCancel?.());
});
describe("脑图持久化与草稿边界", () => {
  it("保存中的新GET比PUT确认更新时，后续编辑采用GET的新记录", async () => {
    const original = {
      id: "s",
      name: "Step",
      updatedAt: "2026-10-08T10:00:00Z",
      steps: [{ step: 1, action: "old", expected: "old expected" }],
    };
    let finish!: (result: any) => void;
    const persistEdit = vi
      .fn()
      .mockImplementationOnce(() => new Promise((r) => (finish = r)))
      .mockResolvedValue(true);
    const {
      state: s,
      props,
      stop,
    } = componentHost(CaseMindMap, { cases: [original], persistEdit });
    await s.selectNode({
      data: {
        id: "expected",
        kind: "expected",
        caseId: "s",
        stepIndex: 0,
        name: "expected",
      },
    });
    s.editText = "my expected";
    const pending = s.save();
    props.cases = [
      {
        ...original,
        updatedAt: "2026-10-08T10:02:00Z",
        steps: [{ step: 1, action: "newer server", expected: "my expected" }],
      },
    ];
    await flush();
    finish({
      ...original,
      updatedAt: "2026-10-08T10:01:00Z",
      steps: [{ step: 1, action: "old", expected: "my expected" }],
    });
    await pending;
    s.editText = "next expected";
    await s.save();
    expect(persistEdit.mock.calls[1][1].steps[0].action).toBe("newer server");
    stop();
  });
  it("后续成功重读采用服务端新步骤，保留待编辑字段直到确认", async () => {
    const original = {
      id: "s",
      name: "Step",
      steps: [{ step: 1, action: "old action", expected: "old expected" }],
    };
    const persistEdit = vi.fn().mockResolvedValue(true);
    const {
      state: s,
      props,
      stop,
    } = componentHost(CaseMindMap, { cases: [original], persistEdit });
    const stepNode = (kind: string) => ({
      data: { id: kind, kind, caseId: "s", stepIndex: 0, name: kind },
    });
    await s.selectNode(stepNode("action"));
    s.editText = "my save";
    await s.save();
    await s.selectNode(stepNode("expected"));
    s.editText = "my expected draft";
    props.cases = [
      {
        ...original,
        steps: [{ step: 1, action: "new server", expected: "server expected" }],
      },
    ];
    await flush();
    expect(s.editText).toBe("my expected draft");
    expect(s.savedText).toBe("server expected");
    await s.save();
    expect(persistEdit.mock.calls[1][1].steps).toEqual([
      { step: 1, action: "new server", expected: "my expected draft" },
    ]);
    stop();
  });
  it("保存已确认但列表重读失败时，连续编辑、增减步骤使用确认快照", async () => {
    const original = {
      id: "s",
      name: "Step",
      moduleId: "m",
      steps: [{ step: 1, action: "old action", expected: "old expected" }],
    };
    const persistEdit = vi.fn().mockResolvedValue(true);
    const { state: s, stop } = componentHost(CaseMindMap, {
      cases: [original],
      persistEdit,
    });
    const stepNode = (kind: string) => ({
      data: { id: kind, kind, caseId: "s", stepIndex: 0, name: kind },
    });
    await s.selectNode(stepNode("action"));
    s.editText = "new action";
    await s.save();
    await s.selectNode(stepNode("expected"));
    s.editText = "new expected";
    await s.save();
    expect(persistEdit.mock.calls[1][1].steps).toEqual([
      { step: 1, action: "new action", expected: "new expected" },
    ]);
    await s.addStep();
    await s.addStep();
    expect(persistEdit.mock.calls[3][1].steps).toHaveLength(3);
    await s.removeStep();
    await s.selectNode({
      data: { id: "s", kind: "case", caseId: "s", name: "Step" },
    });
    expect(s.selectedCase.steps).toHaveLength(2);
    expect(original.steps).toHaveLength(1);
    stop();
  });
  it("节点切换、关闭和原生离开取消保留 TEXT 富文本", async () => {
    const { state: s, stop } = componentHost(CaseMindMap, {
      cases,
      scopeKey: "p:user",
    });
    await s.selectNode(node());
    s.editText = "<p>Draft</p>";
    await s.selectNode(node("b", "case"));
    await s.closeEditor();
    expect(s.selected.caseId).toBe("a");
    expect(s.editText).toBe("<p>Draft</p>");
    const event = { preventDefault: vi.fn(), returnValue: undefined };
    s.beforeUnload(event);
    expect(event.preventDefault).toHaveBeenCalled();
    mocks.confirm.mockImplementation((o) => o.onOk());
    await s.selectNode(node("b", "case"));
    expect(s.selected.caseId).toBe("b");
    stop();
  });
  it("保存失败保留草稿；成功只确认提交快照并同步阻止重复", async () => {
    let finish!: (ok: boolean) => void;
    const persistEdit = vi
      .fn()
      .mockResolvedValueOnce(false)
      .mockImplementationOnce(() => new Promise<boolean>((r) => (finish = r)));
    const { state: s, stop } = componentHost(CaseMindMap, {
      cases,
      scopeKey: "p:user",
      persistEdit,
    });
    await s.selectNode(node());
    s.editText = "<p>Draft</p>";
    await s.save();
    expect(s.dirty).toBe(true);
    const pending = s.save();
    s.editText = "<p>Later</p>";
    await s.save();
    expect(persistEdit).toHaveBeenCalledTimes(2);
    expect(await s.beforeClose()).toBe(false);
    finish(true);
    await pending;
    expect(s.editText).toBe("<p>Later</p>");
    expect(s.dirty).toBe(true);
    mocks.confirm.mockImplementation((o) => o.onOk());
    await s.beforeClose();
    expect(s.editText).toBe("<p>Draft</p>");
    stop();
  });
  it("换项目清除剪贴板和草稿，旧保存响应不污染新范围", async () => {
    let finish!: (ok: boolean) => void;
    const persistEdit = vi.fn(() => new Promise<boolean>((r) => (finish = r)));
    const {
      state: s,
      props,
      stop,
    } = componentHost(CaseMindMap, { cases, scopeKey: "old", persistEdit });
    await s.selectNode(node());
    s.copy();
    s.editText = "old draft";
    const pending = s.save();
    props.scopeKey = "new";
    await flush();
    expect(s.clipboard).toBeUndefined();
    expect(s.selected).toBeUndefined();
    await s.selectNode(node("b", "case"));
    finish(true);
    await pending;
    expect(s.editText).toBe("Beta");
    expect(s.dirty).toBe(false);
    stop();
  });
  it("剪切保留原身份，失败可以重试，复制到未规划清除原模块", async () => {
    const persistMove = vi
        .fn()
        .mockResolvedValueOnce(false)
        .mockResolvedValueOnce(true),
      persistCreate = vi.fn().mockResolvedValue(true);
    const { state: s, stop } = componentHost(CaseMindMap, {
      cases,
      modules: [
        { id: "m", name: "M" },
        { id: "target", name: "Target" },
      ],
      persistMove,
      persistCreate,
    });
    await s.selectNode(node("a", "case"));
    await s.cut();
    await s.selectNode({
      data: {
        id: "module:target",
        kind: "module",
        moduleId: "target",
        name: "Target",
      },
    });
    await s.paste();
    expect(s.clipboard).toEqual({ kind: "case", id: "a" });
    await s.paste();
    expect(persistMove).toHaveBeenLastCalledWith("case", "a", "target");
    expect(s.clipboard).toBeUndefined();
    await s.selectNode(node("a", "case"));
    s.copy();
    await s.selectNode({
      data: { id: "unassigned", kind: "module", name: "未规划" },
    });
    await s.paste();
    const draft = persistCreate.mock.calls[0][1];
    expect(draft).not.toHaveProperty("id");
    expect(draft.moduleId).toBeUndefined();
    expect(draft.textDescription).toBe("<p>Saved</p>");
    stop();
  });
  it("新增模块失败保留名称；删除确认期间冻结选择，旧范围确认不会删除", async () => {
    const persistCreateModule = vi
        .fn()
        .mockResolvedValueOnce(false)
        .mockResolvedValueOnce(true),
      persistDelete = vi.fn();
    const {
      state: s,
      props,
      stop,
    } = componentHost(CaseMindMap, {
      cases,
      modules: [{ id: "m", name: "M", parentId: "root" }],
      scopeKey: "old",
      persistCreateModule,
      persistDelete,
    });
    await s.selectNode({
      data: { id: "module:m", kind: "module", moduleId: "m", name: "M" },
    });
    await s.newModule(false);
    s.moduleName = "Sibling";
    await s.saveNewModule();
    expect(s.moduleName).toBe("Sibling");
    expect(persistCreateModule).toHaveBeenLastCalledWith("root", "Sibling");
    await s.saveNewModule();
    expect(s.moduleDraft).toBeUndefined();
    let confirmation: any;
    mocks.confirm.mockImplementation((o) => (confirmation = o));
    await s.deleteNode();
    expect(s.busy).toBe(true);
    await s.selectNode(node());
    expect(s.selected.moduleId).toBe("m");
    props.scopeKey = "new";
    await flush();
    await confirmation.onOk();
    expect(persistDelete).not.toHaveBeenCalled();
    stop();
  });
  it("快捷键不拦截富文本编辑器自身的复制、剪切和删除", async () => {
    const persistDelete = vi.fn();
    const { state: s, stop } = componentHost(CaseMindMap, {
      cases,
      persistDelete,
    });
    await s.selectNode(node());
    for (const key of ["c", "x", "v", "Delete"]) {
      const e = {
        target: { tagName: "DIV", isContentEditable: true },
        ctrlKey: true,
        key,
        preventDefault: vi.fn(),
      };
      s.keyboard(e);
      expect(e.preventDefault).not.toHaveBeenCalled();
    }
    expect(s.clipboard).toBeUndefined();
    expect(persistDelete).not.toHaveBeenCalled();
    stop();
  });
});
