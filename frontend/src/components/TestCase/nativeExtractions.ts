/** MS临时提取器协议；未接入的环境参数明确校验失败。 */
export const extractModes = [
  { value: "JSON_PATH", label: "JSONPath" },
  { value: "X_PATH", label: "XPath" },
  { value: "REGEX", label: "正则" },
];
export const extractScopes = [
  "BODY",
  "UNESCAPED_BODY",
  "BODY_AS_DOCUMENT",
  "URL",
  "REQUEST_HEADERS",
  "RESPONSE_HEADERS",
  "RESPONSE_CODE",
  "RESPONSE_MESSAGE",
].map((value, index) => ({
  value,
  label: [
    "Body",
    "Body (unescaped)",
    "Body as a Document",
    "URL",
    "Request Headers",
    "Response Headers",
    "Response Code",
    "Response Message",
  ][index],
}));
export interface Extractor {
  id: string;
  enable: boolean;
  variableName: string;
  variableType: "TEMPORARY";
  description: string;
  extractType: "JSON_PATH" | "X_PATH" | "REGEX";
  expression: string;
  extractScope: string;
  expressionMatchingRule: "EXPRESSION" | "GROUP";
  resultMatchingRule: "RANDOM" | "SPECIFIC" | "ALL";
  resultMatchingRuleNum: number;
  responseFormat: "XML" | "HTML";
}
export interface ExtractProcessor {
  id: string;
  name: string;
  enable: boolean;
  processorType: "EXTRACT";
  extractors: Extractor[];
}
export const clone = <T>(value: T): T => JSON.parse(JSON.stringify(value));
export const newExtractor = (): Extractor => ({
  id: crypto.randomUUID(),
  enable: true,
  variableName: "",
  variableType: "TEMPORARY",
  description: "",
  extractType: "JSON_PATH",
  expression: "",
  extractScope: "BODY",
  expressionMatchingRule: "EXPRESSION",
  resultMatchingRule: "RANDOM",
  resultMatchingRuleNum: 1,
  responseFormat: "XML",
});
export const newProcessor = (): ExtractProcessor => ({
  id: crypto.randomUUID(),
  name: "参数提取",
  enable: true,
  processorType: "EXTRACT",
  extractors: [],
});
export function readProcessors(raw: string): ExtractProcessor[] {
  const parsed = JSON.parse(raw);
  const config =
    parsed && typeof parsed === "object" && !Array.isArray(parsed)
      ? { processors: [], ...parsed }
      : parsed;
  if (
    !config ||
    typeof config !== "object" ||
    Array.isArray(config) ||
    Object.keys(config).some((k) => k !== "processors") ||
    !Array.isArray(config.processors) ||
    config.processors.length > 100
  )
    throw new Error("后置条件配置无效");
  const seen = new Set<string>();
  let total = 0;
  return config.processors.map((supplied: ExtractProcessor) => {
    const p = { ...newProcessor(), ...supplied, id: supplied?.id };
    if (
      !p ||
      typeof p.id !== "string" ||
      !p.id ||
      p.id.length > 36 ||
      seen.has(p.id) ||
      typeof p.enable !== "boolean" ||
      p.processorType !== "EXTRACT" ||
      typeof p.name !== "string" ||
      !p.name.trim() ||
      p.name.length > 255 ||
      !Array.isArray(p.extractors) ||
      Object.keys(p).some(
        (k) =>
          !["id", "name", "enable", "processorType", "extractors"].includes(k),
      )
    )
      throw new Error("后置条件标识、类型或名称无效");
    seen.add(p.id);
    total += p.extractors.length;
    if (total > 200) throw new Error("每个请求最多200个提取参数");
    const ids = new Set<string>(),
      names = new Set<string>();
    p.extractors = p.extractors.map((r: Extractor) => ({
      ...newExtractor(),
      ...r,
      id: r?.id,
    }));
    const fields = Object.keys(newExtractor());
    for (const r of p.extractors) {
      if (
        !r ||
        typeof r.id !== "string" ||
        !r.id ||
        r.id.length > 36 ||
        ids.has(r.id) ||
        typeof r.enable !== "boolean" ||
        r.variableType !== "TEMPORARY" ||
        typeof r.variableName !== "string" ||
        !r.variableName.trim() ||
        r.variableName.length > 100 ||
        /[${}\r\n\0]/.test(r.variableName) ||
        typeof r.description !== "string" ||
        r.description.length > 1000 ||
        typeof r.expression !== "string" ||
        !r.expression.trim() ||
        r.expression.length > 200 ||
        !extractModes.some((m) => m.value === r.extractType) ||
        !extractScopes.some((s) => s.value === r.extractScope) ||
        !["EXPRESSION", "GROUP"].includes(r.expressionMatchingRule) ||
        !["RANDOM", "SPECIFIC", "ALL"].includes(r.resultMatchingRule) ||
        !Number.isInteger(r.resultMatchingRuleNum) ||
        r.resultMatchingRuleNum < 1 ||
        r.resultMatchingRuleNum > 2147483647 ||
        !["XML", "HTML"].includes(r.responseFormat) ||
        Object.keys(r).some((k) => !fields.includes(k))
      )
        throw new Error("变量名、表达式或提取高级设置无效；当前支持临时参数");
      ids.add(r.id);
      if (r.enable && names.has(r.variableName))
        throw new Error("同一提取器中的启用变量名不能重复");
      if (r.enable) names.add(r.variableName);
    }
    return clone(p);
  });
}
export interface PathNode {
  title: string;
  key: string;
  children?: PathNode[];
}
export function jsonPaths(raw: string): PathNode[] {
  let count = 0;
  function node(value: unknown, path: string, depth: number): PathNode {
    if (++count > 1000 || depth > 100)
      throw new Error("响应节点超过路径选择范围");
    const entries =
      value && typeof value === "object" ? Object.entries(value) : [];
    const children = entries.map(([k, v]) =>
      node(
        v,
        path + (Array.isArray(value) ? `[${k}]` : `[${JSON.stringify(k)}]`),
        depth + 1,
      ),
    );
    return {
      title: path + (children.length ? "" : ` : ${JSON.stringify(value)}`),
      key: path,
      ...(children.length ? { children } : {}),
    };
  }
  return [node(JSON.parse(raw), "$", 0)];
}
export function xmlPaths(raw: string, format: "XML" | "HTML"): PathNode[] {
  if (/<!DOCTYPE|<!ENTITY/i.test(raw) && format === "XML")
    throw new Error("XML不能声明外部资源或实体");
  const doc = new DOMParser().parseFromString(
    raw,
    format === "XML" ? "application/xml" : "text/html",
  );
  if (doc.querySelector("parsererror")) throw new Error("响应不是有效XML");
  let count = 0;
  function node(el: Element, path: string, depth: number): PathNode {
    if (++count > 1000 || depth > 100)
      throw new Error("响应节点超过路径选择范围");
    const children = Array.from(el.children).map((child) => {
      const siblings = Array.from(el.children).filter(
        (s) => s.localName === child.localName,
      );
      return node(
        child,
        path +
          `/*[local-name()='${child.localName}'][${siblings.indexOf(child) + 1}]`,
        depth + 1,
      );
    });
    return { title: path, key: path, ...(children.length ? { children } : {}) };
  }
  return [
    node(
      doc.documentElement,
      `/*[local-name()='${doc.documentElement.localName}'][1]`,
      0,
    ),
  ];
}
