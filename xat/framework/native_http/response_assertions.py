"""响应断言适配器：按官方条件语义评估，表达式交成熟库解析。"""

import json
import logging
import math
from decimal import Decimal
import operator
import regex
import elementpath
from lxml import etree
from jsonpath_ng.ext import parse
from jsonpath_ng.jsonpath import Slice, Descendants, Union, Fields, Index
from jsonpath_ng.ext.filter import Filter
from .result_details import assertion_detail
from .variable_assertions import compare_variable

logger = logging.getLogger("XAT响应断言")
COMPARISONS = {
    "EQUALS": operator.eq,
    "NOT_EQUALS": operator.ne,
    "GT": operator.gt,
    "GT_OR_EQUALS": operator.ge,
    "LT": operator.lt,
    "LT_OR_EQUALS": operator.le,
}


def match(pattern, text, *, full=False):
    method = regex.fullmatch if full else regex.search
    return method(pattern, text, timeout=0.2) is not None


def text_value(value):
    if isinstance(value, str):
        return value
    if isinstance(value, float):
        result = format(Decimal(str(value)), "f")
        return result if "." in result else result + ".0"
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False)


def same_json(actual, expected):
    if type(actual) is not type(expected):
        return False
    if isinstance(actual, list):
        return len(actual) == len(expected) and all(
            same_json(a, b) for a, b in zip(actual, expected)
        )
    if isinstance(actual, dict):
        return actual.keys() == expected.keys() and all(
            same_json(actual[k], expected[k]) for k in actual
        )
    return actual == expected


def compare(actual, condition, expected):
    text = text_value(actual)
    if condition in {"EQUALS", "NOT_EQUALS"}:
        # 官方字符串按原输入比较，其他JSON类型以JSON值比较。
        other = expected if isinstance(actual, str) else json.loads(expected)
        equal = same_json(actual, other)
        return equal if condition == "EQUALS" else not equal
    if condition in {"GT", "GT_OR_EQUALS", "LT", "LT_OR_EQUALS"}:
        number = r"[+-]?[0-9]+(?:\.[0-9]{1,10})?"
        if not match(number, text, full=True) or not match(number, expected, full=True):
            raise ValueError("数值条件需要整数或最多10位小数")
        return COMPARISONS[condition](float(text), float(expected))
    if condition.startswith("LENGTH_"):
        if actual is None:
            return False
        # 官方比较Java字符串长度，不把数组项数当作长度；非BMP字符占两位。
        length = len(text.encode("utf-16-le", errors="surrogatepass")) // 2
        if not match(r"[+-]?\d+", expected, full=True):
            raise ValueError("长度条件的匹配值需要整数")
        return COMPARISONS[condition.removeprefix("LENGTH_")](length, int(expected))
    if condition == "CONTAINS":
        return expected in text
    if condition == "NOT_CONTAINS":
        return expected not in text
    if condition == "EMPTY":
        return actual is None or not text.strip()
    if condition == "NOT_EMPTY":
        return actual is not None and bool(text.strip())
    if condition == "START_WITH":
        return actual is not None and text.startswith(expected)
    if condition == "END_WITH":
        return actual is not None and text.endswith(expected)
    if condition == "REGEX":
        return match(expected, text, full=True)
    raise ValueError("不支持的响应匹配条件")


def indefinite(node):
    if isinstance(node, (Slice, Descendants, Union, Filter)):
        return True
    if isinstance(node, Fields) and (len(node.fields) > 1 or "*" in node.fields):
        return True
    if isinstance(node, Index) and len(node.indices) > 1:
        return True
    return any(
        indefinite(child)
        for name in ("left", "right", "child")
        if (child := getattr(node, name, None)) is not None
    )


def json_value(expression, response):
    path = parse(expression)
    values = [result.value for result in path.find(response.json())]
    if indefinite(path):
        return values
    if not values:
        raise ValueError("JSONPath没有找到目标")
    return values[0]


def status_check(condition, expected, actual):
    patterns = {
        "EQUALS": "^" + expected + "$",
        "NOT_EQUALS": "^(?!" + expected + "$).*$",
        "CONTAINS": ".*" + expected + ".*",
        "NOT_CONTAINS": "(?s)^((?!" + expected + ").)*$",
    }
    return match(patterns[condition], str(actual))


def header_check(rule, response):
    headers = "\r\n".join(
        name.decode("latin-1") + ": " + value.decode("latin-1")
        for name, value in response.headers.raw
    )
    ending = (
        ".*" + rule.expectedValue
        if rule.condition in {"CONTAINS", "NOT_CONTAINS"}
        else r"\s*(?:" + rule.expectedValue + r"[\r\n]|" + rule.expectedValue + "$)"
    )
    found = match(
        r"((?:[\r\n]" + rule.header + "|^" + rule.header + "):" + ending + ")", headers
    )
    return not found if rule.condition.startswith("NOT_") else found


def xpath_select(expression, content, response_format):
    parser = (
        etree.HTMLParser(no_network=True)
        if response_format == "HTML"
        else etree.XMLParser(resolve_entities=False, no_network=True, load_dtd=False)
    )
    root = etree.fromstring(content, parser)
    if root is None:
        raise ValueError("响应不是有效文档")
    if root.getroottree().docinfo.doctype and response_format == "XML":
        raise ValueError("响应XML不能声明外部资源或实体")
    selector = elementpath.Selector(
        expression,
        parser=(
            elementpath.XPath1Parser
            if response_format == "HTML"
            else elementpath.XPath2Parser
        ),
    )
    if any(
        token.symbol
        in {
            "doc",
            "doc-available",
            "collection",
            "unparsed-text",
            "unparsed-text-available",
        }
        for token in selector.root_token.iter()
    ):
        raise ValueError("响应XPath只读取当前响应文档")
    # XPath断言验证表达式是否命中，布尔/数字结果使用其有效布尔值。
    return selector.select(root)


def xpath_value(expression, response, response_format):
    value = xpath_select(expression, response.content, response_format)
    if isinstance(value, float) and math.isnan(value):
        return False
    return bool(value)


def evaluate(groups, response, elapsed_ms, detail_sink=None, variables=None):
    results = []
    variables = variables if variables is not None else {}

    def record(
        group,
        index,
        condition,
        callback,
        *,
        value=None,
        expected="",
        name="",
        expression="",
        predicate=None,
        presence=None,
    ):
        row = dict(
            groupId=group.id,
            rowIndex=index,
            assertionType=group.assertionType,
            source=group.assertionType,
            operator=condition,
            passed=False,
        )
        actual, present = "", False
        try:
            if value is not None:
                actual = value()
                present = bool(presence()) if presence else True
            row["passed"] = bool(predicate(actual) if predicate else callback())
            row["description"] = "断言通过" if row["passed"] else "断言未通过"
        except Exception as exception:
            logger.exception(
                "响应断言评估失败：分类=%s，行=%s", group.assertionType, index
            )
            row["description"] = "断言评估失败：" + type(exception).__name__
        results.append(row)
        if detail_sink is not None:
            detail_sink.append(
                assertion_detail(
                    row,
                    actual=text_value(actual),
                    expected=expected,
                    name=name or group.name,
                    expression=expression,
                    present=present,
                )
            )

    for group in groups:
        if not group.enable:
            continue
        kind = group.assertionType
        if kind == "VARIABLE":
            for index, rule in enumerate(group.variableAssertionItems):
                if rule.enable and rule.condition != "UNCHECK":
                    record(
                        group, index, rule.condition, None,
                        value=lambda: variables.get(rule.variableName),
                        presence=lambda: rule.variableName in variables,
                        predicate=lambda actual: compare_variable(actual, rule.condition, rule.expectedValue),
                        expected=rule.expectedValue,
                        name=rule.variableName,
                        expression=rule.variableName,
                    )
        elif kind == "RESPONSE_CODE":
            if group.condition != "UNCHECK":
                record(
                    group,
                    0,
                    group.condition,
                    lambda: status_check(
                        group.condition, group.expectedValue, response.status_code
                    ),
                    value=lambda: response.status_code,
                    expected=group.expectedValue,
                )
        elif kind == "RESPONSE_TIME":
            record(
                group,
                0,
                "LT_OR_EQUALS",
                lambda: elapsed_ms <= group.expectedValue,
                value=lambda: elapsed_ms,
                expected=str(group.expectedValue),
            )
        elif kind == "RESPONSE_HEADER":
            for index, rule in enumerate(group.assertions):
                if rule.enable and rule.expectedValue.strip():
                    record(
                        group,
                        index,
                        rule.condition,
                        lambda: header_check(rule, response),
                        value=lambda: "\r\n".join(
                            v.decode("latin-1")
                            for k, v in response.headers.raw
                            if match("^(?:" + rule.header + ")$", k.decode("latin-1"))
                        ),
                        expected=rule.expectedValue,
                        name=rule.header,
                        presence=lambda: any(
                            match("^(?:" + rule.header + ")$", k.decode("latin-1"))
                            for k, _ in response.headers.raw
                        ),
                    )
        else:
            section = {
                "JSON_PATH": group.jsonPathAssertion,
                "XPATH": group.xpathAssertion,
                "REGEX": group.regexAssertion,
            }[group.assertionBodyType]
            for index, rule in enumerate(section.assertions):
                if not rule.enable:
                    continue
                if group.assertionBodyType == "JSON_PATH":
                    if rule.condition != "UNCHECK":
                        record(
                            group,
                            index,
                            rule.condition,
                            None,
                            value=lambda: json_value(rule.expression, response),
                            predicate=lambda actual: compare(
                                actual, rule.condition, rule.expectedValue
                            ),
                            expected=rule.expectedValue,
                            name=rule.expression,
                            expression=rule.expression,
                        )
                elif group.assertionBodyType == "XPATH":
                    record(
                        group,
                        index,
                        "XPATH",
                        lambda: xpath_value(
                            rule.expression,
                            response,
                            group.xpathAssertion.responseFormat,
                        ),
                        value=lambda: response.text,
                        name=rule.expression,
                        expression=rule.expression,
                    )
                else:
                    record(
                        group,
                        index,
                        "REGEX",
                        lambda: match(rule.expression, response.text),
                        value=lambda: response.text,
                        name=rule.expression,
                        expression=rule.expression,
                    )
    return results
