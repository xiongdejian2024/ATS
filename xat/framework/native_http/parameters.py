"""参数表与旧键值兼容；URL编码及认证交由标准库、httpx处理。"""

from urllib.parse import quote, quote_plus
import httpx


def enabled(rows):
    return [row for row in (rows or []) if row.enable]


def path_parameters(path, rows):
    for row in enabled(rows):
        placeholder = "{" + row.key + "}"
        if placeholder not in path:
            raise ValueError("REST参数名称不在请求路径中")
        path = path.replace(
            placeholder, quote(row.value, safe="") if row.encode else row.value
        )
    return path


def request_url(request):
    url = httpx.URL(request.url)
    if request.queryParams is None:
        return url.copy_merge_params(request.query)
    rows = enabled(request.queryParams)
    keys = {row.key for row in rows}
    # 先按名称替换URL原查询；参数排序及显式空值保持。
    original = httpx.QueryParams(url.query)
    for key in keys:
        original = original.remove(key)
    parts = [str(original)] if original else []
    for row in rows:
        # 关闭编码保留已编码值及查询分隔符；非ASCII和空格仍需合法URI表示。
        value = (
            quote_plus(row.value)
            if row.encode
            else quote(row.value, safe="!$&'()*+,-./:;=?@_~%")
        )
        parts.append(quote_plus(row.key) + "=" + value)
    return url.copy_with(query="&".join(parts).encode("utf-8"))


def arguments(request):
    result = dict(
        headers=(
            request.headers
            if request.headerParams is None
            else {row.key: row.value for row in enabled(request.headerParams)}
        ),
        timeout=request.timeoutMs / 1000,
        follow_redirects=request.followRedirects,
    )
    if request.connectTimeoutMs is not None or request.responseTimeoutMs is not None:
        connect = (
            request.timeoutMs
            if request.connectTimeoutMs is None
            else request.connectTimeoutMs
        )
        response = (
            request.timeoutMs
            if request.responseTimeoutMs is None
            else request.responseTimeoutMs
        )
        result["timeout"] = httpx.Timeout(
            None,
            connect=connect / 1000 if connect else None,
            read=response / 1000 if response else None,
            write=response / 1000 if response else None,
            pool=connect / 1000 if connect else None,
        )
    auth = request.authConfig
    if auth and auth.authType != "NONE":
        credentials = auth.basicAuth if auth.authType == "BASIC" else auth.digestAuth
        auth_class = httpx.BasicAuth if auth.authType == "BASIC" else httpx.DigestAuth
        result["auth"] = auth_class(credentials.userName, credentials.password)
    if request.bodyType == "form" and request.formParams is not None:
        result["data"] = {row.key: row.value for row in enabled(request.formParams)}
    return result
