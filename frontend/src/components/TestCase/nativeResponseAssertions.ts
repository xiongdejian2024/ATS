/** 官方响应与变量断言；未知类型不转换为通过项，旧断言独立保留。 */
export const responseKinds = [
  { value: "RESPONSE_CODE", label: "状态码" },
  { value: "RESPONSE_HEADER", label: "响应头" },
  { value: "RESPONSE_BODY", label: "响应体" },
  { value: "RESPONSE_TIME", label: "响应时间" },
  { value: "VARIABLE", label: "变量断言" },
] as const;
export type Kind = (typeof responseKinds)[number]["value"];
export type RuleMode = "HEADER" | "JSON_PATH" | "XPATH" | "REGEX" | "VARIABLE";
export const conditions = [
  ["UNCHECK", "不校验"],
  ["EQUALS", "等于"],
  ["NOT_EQUALS", "不等于"],
  ["GT", "大于"],
  ["GT_OR_EQUALS", "大于等于"],
  ["LT", "小于"],
  ["LT_OR_EQUALS", "小于等于"],
  ["CONTAINS", "包含"],
  ["NOT_CONTAINS", "不包含"],
  ["START_WITH", "以...开始"],
  ["END_WITH", "以...结束"],
  ["EMPTY", "为空"],
  ["NOT_EMPTY", "不为空"],
  ["REGEX", "正则匹配"],
  ["LENGTH_GT", "长度大于"],
  ["LENGTH_GT_OR_EQUALS", "长度大于等于"],
  ["LENGTH_LT", "长度小于"],
  ["LENGTH_LT_OR_EQUALS", "长度小于等于"],
  ["LENGTH_EQUALS", "长度等于"],
].map(([value, label]) => ({ value, label }));
export const matchConditions = [
  "CONTAINS",
  "NOT_CONTAINS",
  "EQUALS",
  "NOT_EQUALS",
];
export const codeConditions = matchConditions
  .concat("UNCHECK")
  .map((value) => conditions.find((c) => c.value === value)!);
export const headerNames = [
  "Content-Type",
  "Content-Length",
  "Content-Control",
  "Content-Disposition",
  "Content-Encoding",
  "Location",
  "Set-Cookie",
  "Access-Control-Allow-Origin",
  "Expires",
  "Last-Modified",
].map((value) => ({ value }));
export interface AssertionRule {
  variableName?: string;
  header?: string;
  expression?: string;
  condition?: string;
  expectedValue?: string;
  enable: boolean;
}
export interface ResponseGroup {
  id: string;
  name: string;
  assertionType: Kind;
  enable: boolean;
  condition?: string;
  expectedValue?: string | number | null;
  assertions?: AssertionRule[];
  variableAssertionItems?: AssertionRule[];
  assertionBodyType?: "JSON_PATH" | "XPATH" | "REGEX";
  jsonPathAssertion?: { assertions: AssertionRule[] };
  xpathAssertion?: {
    responseFormat: "XML" | "HTML";
    assertions: AssertionRule[];
  };
  regexAssertion?: { assertions: AssertionRule[] };
}
export function blankRule(mode: RuleMode): AssertionRule {
  if (mode === "VARIABLE")
    return {
      variableName: "",
      condition: "EQUALS",
      expectedValue: "",
      enable: true,
    };
  return mode === "HEADER"
    ? { header: "", condition: "EQUALS", expectedValue: "", enable: true }
    : mode === "JSON_PATH"
      ? { expression: "", condition: "EQUALS", expectedValue: "", enable: true }
      : { expression: "", enable: true };
}
export function rules(rows: AssertionRule[], mode: RuleMode) {
  const key =
    mode === "VARIABLE"
      ? "variableName"
      : mode === "HEADER"
        ? "header"
        : "expression";
  const filled = rows.filter((r) => r[key] || r.expectedValue);
  if (filled.length > 100) throw new Error("每类响应断言最多100行");
  for (const row of filled) {
    if (
      typeof row[key] !== "string" ||
      !row[key]?.trim() ||
      row[key]!.length > 255
    )
      throw new Error("请填写有效的变量名、响应头名称或表达式");
    if (typeof row.enable !== "boolean") throw new Error("断言启用状态无效");
    if (mode === "VARIABLE" && /[\r\n\0]/.test(row.variableName!))
      throw new Error("变量断言名称不能包含控制字符");
    if (
      mode === "VARIABLE" &&
      Object.keys(row).some(
        (k) =>
          !["variableName", "condition", "expectedValue", "enable"].includes(k),
      )
    )
      throw new Error("变量断言包含未知字段");
    if (mode === "HEADER" || mode === "JSON_PATH" || mode === "VARIABLE") {
      const allowed =
        mode === "HEADER" ? matchConditions : conditions.map((c) => c.value);
      if (
        !allowed.includes(row.condition || "") ||
        typeof row.expectedValue !== "string" ||
        row.expectedValue.length > 20000
      )
        throw new Error("响应断言的匹配条件或匹配值无效");
    }
  }
  return filled;
}
export function newResponseGroup(kind: Kind): ResponseGroup {
  const common = {
    id: crypto.randomUUID(),
    name: responseKinds.find((x) => x.value === kind)!.label,
    assertionType: kind,
    enable: true,
  };
  if (kind === "RESPONSE_CODE")
    return { ...common, condition: "EQUALS", expectedValue: "200" };
  if (kind === "RESPONSE_TIME") return { ...common, expectedValue: 200 };
  if (kind === "VARIABLE") return { ...common, variableAssertionItems: [] };
  if (kind === "RESPONSE_HEADER") return { ...common, assertions: [] };
  return {
    ...common,
    assertionBodyType: "JSON_PATH",
    jsonPathAssertion: { assertions: [] },
    xpathAssertion: { responseFormat: "XML", assertions: [] },
    regexAssertion: { assertions: [] },
  };
}
export function readResponseAssertions(raw: string): ResponseGroup[] {
  const data = JSON.parse(raw);
  if (!Array.isArray(data) || data.length > responseKinds.length)
    throw new Error("响应与变量断言须为五类列表");
  const types = new Set<string>(),
    ids = new Set<string>();
  for (const group of data) {
    if (
      !group ||
      !responseKinds.some((k) => k.value === group.assertionType) ||
      typeof group.id !== "string" ||
      !group.id ||
      group.id.length > 36 ||
      typeof group.name !== "string" ||
      !group.name ||
      group.name.length > 255 ||
      typeof group.enable !== "boolean" ||
      types.has(group.assertionType) ||
      ids.has(group.id)
    )
      throw new Error("响应断言分类、ID或启用状态无效");
    types.add(group.assertionType);
    ids.add(group.id);
    if (group.assertionType === "RESPONSE_CODE") {
      if (
        !codeConditions.some((c) => c.value === group.condition) ||
        typeof group.expectedValue !== "string" ||
        group.expectedValue.length > 20000
      )
        throw new Error("状态码匹配条件或值无效");
    } else if (group.assertionType === "RESPONSE_TIME") {
      if (
        !Number.isInteger(group.expectedValue) ||
        group.expectedValue < 0 ||
        group.expectedValue > 2147483647
      )
        throw new Error("响应时间须为非负整数毫秒");
    } else if (group.assertionType === "VARIABLE") {
      if (!Array.isArray(group.variableAssertionItems))
        throw new Error("变量断言行无效");
      if (
        Object.keys(group).some(
          (k) =>
            ![
              "id",
              "name",
              "enable",
              "assertionType",
              "variableAssertionItems",
            ].includes(k),
        )
      )
        throw new Error("变量断言分组包含未知字段");
      group.variableAssertionItems = rules(
        group.variableAssertionItems,
        "VARIABLE",
      );
    } else if (group.assertionType === "RESPONSE_HEADER") {
      if (!Array.isArray(group.assertions)) throw new Error("响应头断言行无效");
      group.assertions = rules(group.assertions, "HEADER");
    } else {
      if (
        !["JSON_PATH", "XPATH", "REGEX"].includes(group.assertionBodyType) ||
        !["XML", "HTML"].includes(group.xpathAssertion?.responseFormat)
      )
        throw new Error("响应体断言方式或格式无效");
      for (const [key, mode] of [
        ["jsonPathAssertion", "JSON_PATH"],
        ["xpathAssertion", "XPATH"],
        ["regexAssertion", "REGEX"],
      ] as const) {
        if (!Array.isArray(group[key]?.assertions))
          throw new Error("响应体断言行无效");
        group[key].assertions = rules(group[key].assertions, mode);
      }
    }
  }
  return data;
}
