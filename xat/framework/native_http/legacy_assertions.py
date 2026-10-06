"""旧键值断言保持原有类型比较和JSON路径语义。"""

import logging
import httpx
from .models import Assertion
from .result_details import assertion_detail
import json

logger = logging.getLogger("XAT原生HTTP")


def equal(actual, expected):
    """JSON数值按数值比较，布尔值不会被Python当作0/1。"""
    if isinstance(actual, bool) or isinstance(expected, bool):
        return type(actual) is type(expected) and actual == expected
    if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
        return actual == expected
    if type(actual) is not type(expected):
        return False
    if isinstance(actual, list):
        return len(actual) == len(expected) and all(
            equal(a, b) for a, b in zip(actual, expected)
        )
    if isinstance(actual, dict):
        return actual.keys() == expected.keys() and all(
            equal(actual[k], expected[k]) for k in actual
        )
    return actual == expected


def check(assertion: Assertion, response: httpx.Response, detail_sink=None):
    present = True
    if assertion.source == "status":
        actual = response.status_code
    elif assertion.source == "text":
        actual = response.text
    elif assertion.source == "header":
        present = bool(assertion.name and assertion.name in response.headers)
        actual = response.headers.get(assertion.name or "")
    else:
        try:
            actual = response.json()
            for segment in assertion.path:
                if (
                    isinstance(segment, int)
                    and isinstance(actual, list)
                    and 0 <= segment < len(actual)
                ):
                    actual = actual[segment]
                elif (
                    isinstance(segment, str)
                    and isinstance(actual, dict)
                    and segment in actual
                ):
                    actual = actual[segment]
                else:
                    present = False
                    actual = None
                    break
        except ValueError:
            logger.exception("响应JSON解析失败，JSON断言未通过")
            row = dict(
                source=assertion.source,
                operator=assertion.operator,
                passed=False,
                description="响应不是有效JSON",
            )
            capture(assertion, row, None, False, detail_sink)
            return row
    op, expected = assertion.operator, assertion.expected
    if op == "exists":
        success = present
    elif op == "not_exists":
        success = not present
    elif not present:
        success = False
    elif op == "equals":
        success = equal(actual, expected)
    elif op == "not_equals":
        success = not equal(actual, expected)
    else:
        success = (
            (
                isinstance(actual, str)
                and isinstance(expected, str)
                and expected in actual
            )
            or (isinstance(actual, list) and any(equal(v, expected) for v in actual))
            or (
                isinstance(actual, dict)
                and isinstance(expected, str)
                and expected in actual
            )
        )
    # 不把完整响应、头部或用户凭据写入执行日志。
    row = dict(
        source=assertion.source,
        operator=op,
        passed=success,
        description="断言通过" if success else "断言未通过",
    )

    capture(assertion, row, actual, present, detail_sink)
    return row


def capture(assertion, row, actual, present, detail_sink):
    if detail_sink is None:
        return
    name = assertion.name or (
        ".".join(map(str, assertion.path)) if assertion.path else assertion.source
    )
    serialize = lambda value: (
        value
        if isinstance(value, str)
        else json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    )
    detail_sink.append(
        assertion_detail(
            row,
            actual=serialize(actual),
            expected=serialize(assertion.expected),
            name=name,
            expression=name,
            present=present,
        )
    )
