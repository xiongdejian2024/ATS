import { describe, expect, it } from "vitest";
import {
  blankRule,
  newResponseGroup,
  readResponseAssertions,
  rules,
} from "../nativeResponseAssertions";
describe("响应断言的定义及草稿", () => {
  it("四类唯一、排列和停用保持；三正文方式分别保留", () => {
    const time = newResponseGroup("RESPONSE_TIME"),
      body = newResponseGroup("RESPONSE_BODY");
    body.enable = false;
    body.jsonPathAssertion!.assertions = [
      {
        ...blankRule("JSON_PATH"),
        expression: "$.value",
        expectedValue: "true",
      },
    ];
    body.xpathAssertion!.responseFormat = "HTML";
    body.xpathAssertion!.assertions = [
      { ...blankRule("XPATH"), expression: "//p" },
    ];
    body.regexAssertion!.assertions = [
      { ...blankRule("REGEX"), expression: "value" },
    ];
    body.assertionBodyType = "REGEX";
    expect(readResponseAssertions(JSON.stringify([time, body]))).toEqual([
      time,
      body,
    ]);
    expect(() =>
      readResponseAssertions(
        JSON.stringify([time, { ...time, id: "duplicate-type" }]),
      ),
    ).toThrow();
    expect(() =>
      readResponseAssertions(
        JSON.stringify([{ ...time, expectedValue: null }]),
      ),
    ).toThrow();
  });
  it("自动空行不存，半行不替代有效定义；复制允许重复表达式", () => {
    const rule = {
      ...blankRule("JSON_PATH"),
      expression: "$.value",
      expectedValue: "[]",
    };
    expect(
      rules([rule, structuredClone(rule), blankRule("JSON_PATH")], "JSON_PATH"),
    ).toEqual([rule, rule]);
    expect(() =>
      rules(
        [{ ...blankRule("JSON_PATH"), expectedValue: "未命名" }],
        "JSON_PATH",
      ),
    ).toThrow();
    expect(() =>
      rules([{ ...rule, condition: "UNKNOWN" }], "JSON_PATH"),
    ).toThrow();
  });
});
