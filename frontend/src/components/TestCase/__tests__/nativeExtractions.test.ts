import { describe, expect, it, vi } from "vitest";
import {
  clone,
  newExtractor,
  newProcessor,
  readProcessors,
  jsonPaths,
} from "../nativeExtractions";
import { effectScope, reactive } from "vue";
import { useNativeExecutionDraft } from "../nativeExecutionDraft";

function sample() {
  const p = newProcessor();
  p.extractors = [
    {
      ...newExtractor(),
      variableName: "token",
      expression: "$.token",
      resultMatchingRule: "ALL",
    },
  ];
  return p;
}
describe("后置临时提取器协议、草稿与响应路径", () => {
  it("保存顺序、停用、高级设置，克隆产生独立对象", () => {
    const p = sample(),
      q = clone(p);
    q.id = "other";
    q.enable = false;
    q.extractors[0].extractType = "REGEX";
    q.extractors[0].expressionMatchingRule = "GROUP";
    q.extractors[0].extractScope = "RESPONSE_HEADERS";
    const rows = readProcessors(JSON.stringify({ processors: [q, p] }));
    expect(rows.map((r) => r.id)).toEqual(["other", p.id]);
    expect(rows[0].extractors[0]).toMatchObject({
      resultMatchingRule: "ALL",
      expressionMatchingRule: "GROUP",
      extractScope: "RESPONSE_HEADERS",
    });
    expect(p.extractors[0].extractType).toBe("JSON_PATH");
  });
  it("高级配置中的默认省略项按后端协议补全，必填身份不擅自重建", () => {
    const rows = readProcessors(
      JSON.stringify({
        processors: [
          {
            id: "p",
            extractors: [{ id: "r", variableName: "n", expression: "$.v" }],
          },
        ],
      }),
    );
    expect(rows[0]).toMatchObject({
      name: "参数提取",
      processorType: "EXTRACT",
      enable: true,
    });
    expect(rows[0].extractors[0]).toMatchObject({
      variableType: "TEMPORARY",
      resultMatchingRule: "RANDOM",
      responseFormat: "XML",
    });
    expect(() =>
      readProcessors(JSON.stringify({ processors: [{ extractors: [] }] })),
    ).toThrow();
  });
  it("空行、重名、未接入环境参数及非法匹配序号不能保存", () => {
    const p = sample();
    p.extractors.push({ ...p.extractors[0], id: "duplicate" });
    expect(() => readProcessors(JSON.stringify({ processors: [p] }))).toThrow(
      "重复",
    );
    p.extractors[1].enable = false;
    expect(
      readProcessors(JSON.stringify({ processors: [p] }))[0].extractors,
    ).toHaveLength(2);
    for (const bad of [
      { variableName: "" },
      { variableType: "ENVIRONMENT" },
      { resultMatchingRuleNum: 0 },
      { expression: "x".repeat(201) },
      { extractScope: "unknown" },
    ])
      expect(() =>
        readProcessors(
          JSON.stringify({
            processors: [
              { ...p, extractors: [{ ...p.extractors[0], ...bad }] },
            ],
          }),
        ),
      ).toThrow();
  });
  it("JSON路径保留特殊键、数组序号、null和false，不执行响应内容", () => {
    const paths = jsonPaths('{"a.b":[false,null,"<script>"],"quote\\\"":7}');
    expect(paths[0].children?.[0].key).toBe('$["a.b"]');
    expect(paths[0].children?.[0].children?.map((r) => r.key)).toEqual([
      '$["a.b"][0]',
      '$["a.b"][1]',
      '$["a.b"][2]',
    ]);
    expect(paths[0].children?.[1].key).toBe('$["quote\\\""]');
    expect(() => jsonPaths("{")).toThrow();
    expect(() =>
      jsonPaths(JSON.stringify(Array.from({ length: 1001 }, (_, i) => i))),
    ).toThrow("范围");
  });
  it("有效提取配置重开保持；无效新草稿不能覆盖实际正文和已保存配置", () => {
    const log = vi.spyOn(console, "error").mockImplementation(() => {}),
      p = sample(),
      scope = effectScope(),
      errors: string[] = [],
      drafts: string[] = [];
    const props = reactive({
      modelValue: JSON.stringify({
        request: {
          bodyType: "json",
          body: { keep: "原值" },
          postProcessorConfig: { processors: [p] },
        },
      }),
      category: "api",
      apiCases: [],
    });
    const state = scope.run(() =>
      useNativeExecutionDraft(props, {
        update: (value) => (props.modelValue = value),
        error: (value) => errors.push(value),
        draft: (value) => drafts.push(value),
      }),
    )!;
    expect(
      JSON.parse(state.postProcessors.value).processors[0].extractors[0]
        .variableName,
    ).toBe("token");
    const saved = props.modelValue;
    state.postProcessors.value = JSON.stringify({
      processors: [
        { ...p, extractors: [{ ...p.extractors[0], variableName: "" }] },
      ],
    });
    expect(props.modelValue).toBe(saved);
    expect(errors.at(-1)).toBeTruthy();
    expect(drafts.at(-1)).toContain("token");
    state.postProcessors.value = JSON.stringify({ processors: [p] });
    expect(errors.at(-1)).toBe("");
    expect(JSON.parse(props.modelValue).request.body).toEqual({ keep: "原值" });
    props.modelValue = "{}";
    props.modelValue = saved;
    expect(
      JSON.parse(state.postProcessors.value).processors[0].extractors[0]
        .resultMatchingRule,
    ).toBe("ALL");
    scope.stop();
    log.mockRestore();
  });
});
