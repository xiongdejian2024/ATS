"""官方Groovy变量断言语义；不执行用户脚本，正则采用已有regex库。"""

import math
import operator
import regex

COMPARISONS = {
    "EQUALS": operator.eq,
    "GT": operator.gt,
    "GT_OR_EQUALS": operator.ge,
    "LT": operator.lt,
    "LT_OR_EQUALS": operator.le,
}
DOUBLE = regex.compile(
    r"[\x00-\x20]*[+-]?(?:NaN|Infinity|"
    r"(?:[0-9]+\.?[0-9]*|\.[0-9]+)(?:[eE][+-]?[0-9]+)?[fFdD]?|"
    r"0[xX](?:[0-9a-fA-F]+\.?[0-9a-fA-F]*|\.[0-9a-fA-F]+)"
    r"[pP][+-]?[0-9]+[fFdD]?)[\x00-\x20]*"
)


def java_double(value):
    """对齐Double.parseDouble语法，再交Python成熟浮点转换处理。"""
    if not isinstance(value, str) or DOUBLE.fullmatch(value, timeout=0.2) is None:
        raise ValueError("变量数值条件需要有效Java浮点值")
    number = value.strip("".join(chr(i) for i in range(33)))
    if number[-1:] in "fFdD":
        number = number[:-1]
    if number.lstrip("+-").lower().startswith("0x"):
        try:
            return float.fromhex(number)
        except OverflowError:
            return -math.inf if number.startswith("-") else math.inf
    return float(number)


def compare_variable(actual, condition, expected):
    if condition == "EQUALS":
        return actual == expected
    if condition == "NOT_EQUALS":
        # Groovy的null.equals(字符串)返回false；未定义变量不等于字符串。
        return actual != expected
    if condition == "REGEX":
        return actual is not None and regex.fullmatch(expected, actual, timeout=0.2) is not None
    if actual is None:
        # 官方EMPTY使用void而非null，缺失变量调用length也会失败。
        raise ValueError("变量未定义，无法评估此匹配条件")
    if condition in {"GT", "GT_OR_EQUALS", "LT", "LT_OR_EQUALS"}:
        return COMPARISONS[condition](java_double(actual), java_double(expected))
    if condition.startswith("LENGTH_"):
        length = len(actual.encode("utf-16-le", errors="surrogatepass")) // 2
        return COMPARISONS[condition.removeprefix("LENGTH_")](length, java_double(expected))
    if condition == "CONTAINS":
        return expected in actual
    if condition == "NOT_CONTAINS":
        return expected not in actual
    if condition == "START_WITH":
        return actual.startswith(expected)
    if condition == "END_WITH":
        return actual.endswith(expected)
    if condition == "EMPTY":
        return actual == ""
    if condition == "NOT_EMPTY":
        return actual != ""
    raise ValueError("不支持的变量匹配条件")
