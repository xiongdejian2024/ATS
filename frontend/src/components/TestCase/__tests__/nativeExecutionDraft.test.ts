import { afterEach, describe, expect, it, vi } from "vitest";
import { effectScope, reactive } from "vue";
import { useNativeExecutionDraft } from "../nativeExecutionDraft";
let scope: ReturnType<typeof effectScope>;
afterEach(() => {
  scope?.stop();
  vi.restoreAllMocks();
});
function setup(category = "api", parameters: Record<string, unknown> = {}) {
  const props = reactive({
    modelValue: JSON.stringify(parameters),
    category,
    apiCases: [{ id: "api", name: "实际接口" }],
  });
  const errors: string[] = [],
    drafts: string[] = [];
  scope = effectScope();
  const state = scope.run(() =>
    useNativeExecutionDraft(props, {
      update: (value) => (props.modelValue = value),
      error: (value) => errors.push(value),
      draft: (value) => drafts.push(value),
    }),
  )!;
  return { props, state, errors, drafts };
}
describe("原生执行草稿与实际配置范围", () => {
  it("HTTP请求启用、正文类型及查询参数保留其他配置，关闭执行移除标记", () => {
    const { props, state } = setup("api", { preserved: { key: "原内容" } });
    state.toggle(true);
    state.method.value = "POST";
    state.bodyType.value = "text";
    state.body.value = "中文正文";
    state.query.value = '{"q":"中文"}';
    const result = JSON.parse(props.modelValue);
    expect(result.preserved).toEqual({ key: "原内容" });
    expect(result.request).toMatchObject({
      method: "POST",
      bodyType: "text",
      body: "中文正文",
      query: { q: "中文" },
    });
    state.toggle(false);
    expect(JSON.parse(props.modelValue)).toEqual({
      preserved: { key: "原内容" },
    });
  });
  it("无效JSON保留草稿与上一次有效值，错误进入离开保护，修复后同步配置", () => {
    vi.spyOn(console, "error").mockImplementation(() => {});
    const { props, state, errors, drafts } = setup();
    state.toggle(true);
    const valid = props.modelValue;
    state.headers.value = "{未完成";
    expect(props.modelValue).toBe(valid);
    expect(state.headers.value).toBe("{未完成");
    expect(errors.at(-1)).toBeTruthy();
    expect(drafts.at(-1)).toContain("未完成");
    state.headers.value = '{"X-Test":"value"}';
    expect(errors.at(-1)).toBe("");
    expect(JSON.parse(props.modelValue).request.headers).toEqual({
      "X-Test": "value",
    });
  });
  it("场景必须选择并启用真实API步骤，重复引用与重排不会合并实例", () => {
    vi.spyOn(console, "error").mockImplementation(() => {});
    const { props, state, errors } = setup("scenario");
    state.toggle(true);
    expect(errors.at(-1)).toBeTruthy();
    state.steps.value = [
      { apiCaseId: "api", enabled: true },
      { apiCaseId: "api", enabled: false },
      { apiCaseId: "other", enabled: true },
    ];
    state.move(2, -1);
    state.stop.value = false;
    expect(JSON.parse(props.modelValue).scenario).toEqual({
      steps: [
        { apiCaseId: "api", enabled: true },
        { apiCaseId: "other", enabled: true },
        { apiCaseId: "api", enabled: false },
      ],
      stopOnFailure: false,
    });
    state.steps.value.forEach((step) => (step.enabled = false));
    expect(errors.at(-1)).toBeTruthy();
  });
});
