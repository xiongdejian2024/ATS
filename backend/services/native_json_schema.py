"""官方 MS 预览与自动生成语义，独立于执行正文与响应断言。"""

import json
import random
import warnings
from decimal import Decimal, ROUND_HALF_UP, localcontext
from hypothesis import strategies as st
from hypothesis.errors import NonInteractiveExampleWarning
from core.logger import logger
from framework.native_http.schema_models import JsonSchemaItem, validate_schema_budget

_rng = random.SystemRandom()


def _text(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _random_string(length):
    return "".join(chr(_rng.randint(ord("0"), ord("z"))) for _ in range(length))


def _string(node):
    if node.example.strip():
        return node.example
    low = (
        node.minLength
        if node.minLength is not None
        else (1 if node.maxLength else 0) if node.maxLength is not None else 8
    )
    high = (
        node.maxLength
        if node.maxLength is not None
        else node.minLength + 10 if node.minLength is not None else 8
    )
    if node.enumValues:
        value = _rng.choice(node.enumValues)
        return value[:high] if node.maxLength is not None else value
    if node.pattern and node.pattern.strip():
        try:
            # 成熟库负责正则生成，MS 的正则优先于默认值及长度；仅限制资源规模。
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", NonInteractiveExampleWarning)
                return (
                    st.from_regex(node.pattern, fullmatch=True)
                    .filter(lambda s: len(s) <= 20000)
                    .example()
                )
        except Exception:
            logger.exception("Schema 正则生成失败，按MS行为保留正则文本")
            return node.pattern
    value = _text(node.defaultValue)
    if value.strip():
        if node.maxLength is not None:
            value = value[:high]
        return value + _random_string(max(0, low - len(value)))
    return _random_string(_rng.randint(low, high))


def _number(node, preview):
    value = node.example
    if value.startswith(("@", "${")):
        raise ValueError("数字Schema示例中的Mock或变量表达式尚未支持，请填写数字或留空")
    if not preview and not value.strip():
        if node.enumValues:
            value = _rng.choice(node.enumValues)
        elif _text(node.defaultValue).strip():
            value = _text(node.defaultValue)
        elif node.type == "integer":
            low = int(node.minimum) if node.minimum is not None else -(2**31)
            high = int(node.maximum) if node.maximum is not None else 2**31 - 1
            return low if low == high else _rng.randrange(low, high)
        else:
            low = (
                Decimal(str(node.minimum))
                if node.minimum is not None
                else Decimal("1.4E-45")
            )
            high = (
                Decimal(str(node.maximum))
                if node.maximum is not None
                else Decimal("3.4028235E38")
            )
            with localcontext() as ctx:
                ctx.prec = 350
                return float(
                    (low + Decimal(str(_rng.random())) * (high - low)).quantize(
                        Decimal("0.01"), rounding=ROUND_HALF_UP
                    )
                )
    if not value.strip():
        return 0
    try:
        # MS INTEGER 的无效示例回退0，NUMBER回退0；不擅自校验示例是否符合范围。
        return int(value) if node.type == "integer" else float(Decimal(value))
    except (ValueError, ArithmeticError):
        logger.exception("Schema 数字示例转换失败，按MS行为回退零")
        return 0


def convert_schema(schema: JsonSchemaItem, *, preview: bool):
    validate_schema_budget(schema)

    def generate(node):
        # 官方 JsonSchemaBuilder 不依据 enable/required 过滤属性，两者为编辑元数据。
        if node.type == "object":
            return {
                key: generate(child) for key, child in (node.properties or {}).items()
            }
        if node.type == "array":
            items = node.items or []
            if preview:
                return [generate(child) for child in items]
            count = min(
                len(items), node.maxItems if node.maxItems is not None else len(items)
            )
            return [generate(child) for child in items[:count]] + [
                _random_string(8) for _ in range(max(0, (node.minItems or 0) - count))
            ]
        if node.type == "string":
            return (
                (node.example if node.example.strip() else "string")
                if preview
                else _string(node)
            )
        if node.type in {"integer", "number"}:
            return _number(node, preview)
        if node.type == "boolean":
            if node.example.startswith(("@", "${")):
                raise ValueError("布尔Schema示例中的Mock或变量表达式尚未支持")
            return node.example == "true"
        return None

    value = json.dumps(generate(schema), ensure_ascii=False, indent=2, allow_nan=False)
    if len(value.encode()) > 1024 * 1024:
        raise ValueError("生成正文超过1MiB，请减少属性数量或长度")
    logger.info(
        "Schema {}完成，生成正文{}字节",
        "预览" if preview else "自动生成",
        len(value.encode()),
    )
    return value
