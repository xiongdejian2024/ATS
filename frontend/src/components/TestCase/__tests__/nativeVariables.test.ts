import { describe, expect, it, vi } from "vitest";
import { effectScope, reactive } from "vue";
import { readNativeVariables } from "../nativeVariables";
import { useNativeExecutionDraft } from "../nativeExecutionDraft";
describe("初始变量", () => {
  it("保留字面空格、空值和停用行，拒绝重复及容量溢出", () => {
    expect(
      readNativeVariables(
        '[{"name":"a","value":"  "},{"name":"b","value":"","enable":false}]',
      ).map((r) => r.value),
    ).toEqual(["  ", ""]);
    for (const value of [
      [{ name: "a" }, { name: "a", enable: false }],
      [{ name: "${x}" }],
      [{ name: "a", enable: 1 }],
      Array.from({ length: 101 }, (_, i) => ({ name: String(i) })),
      [
        { name: "a", value: "中".repeat(20000) },
        { name: "b", value: "中".repeat(20000) },
      ],
    ])
      expect(() => readNativeVariables(JSON.stringify(value))).toThrow();
  });
  it.each(["api", "scenario"])(
    "%s 保存/reopen初值，非法草稿不覆盖已保存JSON",
    (category) => {
      const key = category === "api" ? "request" : "scenario";
      const props = reactive({
        modelValue: JSON.stringify({
          [key]:
            category === "api"
              ? {}
              : { steps: [{ apiCaseId: "api", enabled: true }] },
        }),
        category,
        apiCases: [{ id: "api", name: "api" }],
      });
      const scope = effectScope(),
        errors: string[] = [],
        drafts: string[] = [];
      const spy = vi.spyOn(console, "error").mockImplementation(() => {});
      try {
        const state = scope.run(() =>
          useNativeExecutionDraft(props, {
            update: (v) => (props.modelValue = v),
            error: (v) => errors.push(v),
            draft: (v) => drafts.push(v),
          }),
        )!;
        state.initialVariables.value = '[{"name":"a","value":"  "}]';
        const saved = props.modelValue;
        expect(JSON.parse(saved)[key].initialVariables[0].value).toBe("  ");
        state.initialVariables.value = '[{"name":""}]';
        expect(props.modelValue).toBe(saved);
        expect(errors.at(-1)).toBeTruthy();
        expect(drafts.at(-1)).toContain('\\"name\\"');
        props.modelValue = "{}";
        props.modelValue = saved;
        expect(readNativeVariables(state.initialVariables.value)[0].value).toBe(
          "  ",
        );
      } finally {
        scope.stop();
        spy.mockRestore();
      }
    },
  );
});
