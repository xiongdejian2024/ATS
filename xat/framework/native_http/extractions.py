"""响应提取与一次执行内的变量传递；不读取文件、数据库或外部XML资源。"""

import html
import logging
import random
import re
from urllib.parse import urlsplit, urlunsplit
import regex
from lxml import etree
from jsonpath_ng.ext import parse
from .models import FrozenRequest
from .parameters import path_parameters
from .response_assertions import text_value, xpath_select
from .result_details import text

logger = logging.getLogger("XAT参数提取")
VARIABLE = re.compile(r"\$\{([^{}]+)\}")
VALUE_LIMIT = 1024 * 1024
MATCH_LIMIT = 1000


def scope_text(rule, response):
    scope = rule.extractScope
    if scope == "BODY":
        return response.text
    if scope == "UNESCAPED_BODY":
        return html.unescape(response.text)
    if scope == "BODY_AS_DOCUMENT":
        # 文本化文档使用已有lxml；二进制文档的Tika适配另行接入。
        if (
            "html" not in response.headers.get("content-type", "").lower()
            and "xml" not in response.headers.get("content-type", "").lower()
        ):
            raise ValueError("Body as a Document当前仅支持HTML/XML响应")
        root = etree.fromstring(response.content, etree.HTMLParser(no_network=True))
        if root is None:
            raise ValueError("响应不是有效文档")
        return "".join(root.itertext())
    if scope == "URL":
        return str(response.request.url)
    if scope in {"REQUEST_HEADERS", "RESPONSE_HEADERS"}:
        headers = (
            response.request.headers if scope == "REQUEST_HEADERS" else response.headers
        )
        # JMeter以LF结束每一行；请求头排除Cookie，响应头包含状态行。
        prefix = (
            f"{response.http_version} {response.status_code} {response.reason_phrase}\n"
            if scope == "RESPONSE_HEADERS" else ""
        )
        return prefix + "".join(
            k.decode("latin-1") + ": " + v.decode("latin-1") + "\n"
            for k, v in headers.raw
            if scope != "REQUEST_HEADERS" or k.lower() != b"cookie"
        )
    if scope == "RESPONSE_CODE":
        return str(response.status_code)
    return response.reason_phrase


def matches(rule, response):
    if len(response.content) > VALUE_LIMIT:
        raise ValueError("提取响应超过1MiB")
    if rule.extractType == "JSON_PATH":
        values = [m.value for m in parse(rule.expression).find(response.json())]
        result = ["" if v is None else text_value(v) for v in values]
    elif rule.extractType == "X_PATH":
        value = xpath_select(rule.expression, response.content, rule.responseFormat)
        result = [
            "".join(v.itertext()) if isinstance(v, etree._Element) else text_value(v)
            for v in (value if isinstance(value, list) else [value])
        ]
    else:
        result = []
        for match in regex.finditer(
            rule.expression, scope_text(rule, response), timeout=0.2
        ):
            if len(result) >= MATCH_LIMIT:
                raise ValueError("提取匹配数量超过1000")
            result.append(match)
    if len(result) > MATCH_LIMIT:
        raise ValueError("提取匹配数量超过1000")
    return result


def sample_values(rule, found):
    if rule.extractType != "REGEX":
        return found
    index = 1 if rule.expressionMatchingRule == "GROUP" else 0
    return [match.group(index) or "" for match in found]


def bind(rule, found, variables):
    """保留JMeter派生变量名及各模式的空结果行为；缺失变量仍为模板文本。"""
    name, kind, mode = rule.variableName, rule.extractType, rule.resultMatchingRule
    values = sample_values(rule, found)
    try:
        previous = min(MATCH_LIMIT, max(0, int(variables.get(name + "_matchNr", "0"))))
    except ValueError:
        logger.exception("提取旧匹配计数不是整数，按零条清理")
        previous = 0
    indexed = re.compile(re.escape(name) + r"_(\d+)(?:_g\d*)?$")
    for key in list(variables):
        marker = indexed.fullmatch(key)
        if marker and 1 <= int(marker.group(1)) <= previous:
            variables.pop(key)
    variables.pop(name + "_matchNr", None)
    for k in list(variables):
        if re.fullmatch(re.escape(name + "_g") + r"\d*", k):
            variables.pop(k)
    if kind != "REGEX":
        variables[name] = (
            "" if kind == "X_PATH" or not values else variables.get(name, "")
        )
    selected = []
    if values:
        if mode == "ALL":
            selected = list(range(len(values)))
        elif mode == "RANDOM":
            selected = [random.randrange(len(values))]
        elif kind == "JSON_PATH" and len(values) == 1:
            # 官方JMeter单值JSON结果分支忽略指定序号。
            selected = [0]
        elif rule.resultMatchingRuleNum <= len(values):
            selected = [rule.resultMatchingRuleNum - 1]
    if mode == "ALL":
        for i, value in enumerate(values, 1):
            variables[f"{name}_{i}"] = value
        variables[name + "_matchNr"] = str(len(values))
        if kind == "JSON_PATH":
            variables[name + "_ALL"] = ",".join(values)
        elif kind == "X_PATH" and values:
            variables[name] = values[0]
    elif selected:
        variables[name] = values[selected[0]]
    elif kind != "REGEX":
        variables[name] = ""
    if kind == "JSON_PATH" and (mode != "RANDOM" or not values):
        variables[name + "_matchNr"] = str(len(values))
    if kind == "X_PATH":
        # XPath处理器的编号变量是选中的结果，不是未选中的全部响应节点。
        picked = values if mode == "ALL" else [values[i] for i in selected]
        variables[name + "_matchNr"] = str(len(picked))
        for i, value in enumerate(picked, 1):
            variables[f"{name}_{i}"] = value
    if kind == "REGEX":
        for i in selected:
            prefix = f"{name}_{i + 1}" if mode == "ALL" else name
            match = found[i]
            variables[prefix + "_g"] = str(len(match.groups()))
            for n in range(len(match.groups()) + 1):
                variables[f"{prefix}_g{n}"] = match.group(n) or ""
    if (
        len(variables) > 10000
        or sum(len(k.encode()) + len(v.encode()) for k, v in variables.items())
        > 8 * VALUE_LIMIT
        or any(len(v.encode()) > VALUE_LIMIT for v in variables.values())
    ):
        raise ValueError("提取变量超过执行容量")
    return (
        [variables[f"{name}_{i + 1}"] for i in selected]
        if mode == "ALL"
        else [variables[name]] if selected else []
    )


class RecordedBindings(dict):
    """Track equal-value writes and deleted extraction aliases, not value diffs."""
    def __init__(self, source):
        super().__init__(source)
        self.touched = set()

    def __setitem__(self, key, value):
        self.touched.add(key)
        super().__setitem__(key, value)

    def pop(self, key, *default):
        self.touched.add(key)
        return super().pop(key, *default)


def evaluate(config, response, variables, temporary=None):
    results = []
    for processor in config.processors:
        if not processor.enable:
            continue
        for rule in processor.extractors:
            if not rule.enable:
                continue
            row = dict(
                name=rule.variableName,
                type=rule.variableType,
                expression=rule.expression,
                processorId=processor.id,
                extractorId=rule.id,
                matched=False,
                matchCount=0,
                value="",
                truncated=False,
                message="未匹配到结果",
            )
            try:
                rule = type(rule).model_validate(
                    {
                        **rule.model_dump(),
                        "expression": render_value(rule.expression, variables),
                    }
                )
                found = matches(rule, response)
                next_variables = RecordedBindings(variables)
                picked = bind(rule, found, next_variables)
                if temporary is not None:
                    for key in next_variables.touched:
                        if key in next_variables:
                            temporary[key] = next_variables[key]
                        else:
                            temporary.pop(key, None)
                variables.clear()
                variables.update(next_variables)
                row.update(
                    matched=bool(picked),
                    matchCount=len(found),
                    message="提取成功" if picked else "未匹配到指定结果",
                )
                row["value"], row["truncated"] = text(",".join(picked))
            except Exception as exception:
                logger.exception(
                    "后置提取失败：处理器=%s，提取行=%s", processor.id, rule.id
                )
                row["message"] = "提取失败：" + type(exception).__name__
            results.append(row)
    return results


def render_value(value, variables, depth=0, keys=False, budget=None):
    if budget is None:
        budget = [0]
    if depth > 100:
        raise ValueError("变量模板嵌套过深")
    if isinstance(value, str):
        result = VARIABLE.sub(lambda m: variables.get(m.group(1), m.group(0)), value)
        if len(result.encode()) > VALUE_LIMIT:
            raise ValueError("变量展开结果超过1MiB")
        budget[0] += len(result.encode())
        if budget[0] > 8 * VALUE_LIMIT:
            raise ValueError("变量展开总量超过8MiB")
        return result
    if isinstance(value, list):
        return [render_value(v, variables, depth + 1, keys, budget) for v in value]
    if isinstance(value, dict):
        result = {}
        for key, item in value.items():
            name = render_value(key, variables, budget=budget) if keys else key
            if name in result:
                raise ValueError("变量展开后的参数名称重复")
            result[name] = render_value(item, variables, depth + 1, keys, budget)
        return result
    return value


def resolve_request(request, variables):
    budget = [0]
    data = request.model_dump()
    for field in (
        "url",
        "headers",
        "query",
        "body",
        "authConfig",
        "assertions",
        "responseAssertions",
    ):
        data[field] = render_value(
            data[field],
            variables,
            keys=field in {"headers", "query", "body"},
            budget=budget,
        )
    for field in (
        "headerParams",
        "queryParams",
        "restParams",
        "formParams",
        "multipartParams",
    ):
        for row in data.get(field) or []:
            if row["enable"]:
                row["key"] = render_value(row["key"], variables, budget=budget)
                row["value"] = render_value(row["value"], variables, budget=budget)
                # 文件ID/哈希/元数据及路径均不做模板替换。
    parsed = urlsplit(data["url"])
    pending = [
        row
        for row in (request.restParams or [])
        if row.enable and "{" + row.key + "}" in parsed.path
    ]
    if pending:
        from .models import RequestParam

        rows = [
            RequestParam.model_validate(row)
            for row in data["restParams"]
            if row["enable"]
        ]
        data["url"] = urlunsplit(
            parsed._replace(path=path_parameters(parsed.path, rows))
        )
    return FrozenRequest.model_validate(data)
