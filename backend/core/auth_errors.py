"""Fail closed when reporting authentication errors: never format their exceptions."""
from uuid import uuid4

from fastapi.responses import JSONResponse

from config import settings
from core.logger import logger


_AUTH_ERRORS = {
    400: ("AUTH_INVALID_REQUEST", "认证请求数据无效"),
    401: ("AUTH_UNAUTHORIZED", "认证失败"),
    403: ("AUTH_FORBIDDEN", "认证请求被拒绝"),
    404: ("AUTH_NOT_FOUND", "认证接口不存在"),
    405: ("AUTH_METHOD_NOT_ALLOWED", "认证请求方法不支持"),
    422: ("AUTH_INVALID_REQUEST", "认证请求数据无效"),
    429: ("AUTH_RATE_LIMITED", "认证请求过于频繁"),
    500: ("AUTH_INTERNAL_ERROR", "认证服务暂时不可用"),
}


def is_auth_path(path: str) -> bool:
    prefix = settings.API_V1_STR.rstrip("/") + "/auth"
    return path == prefix or path.startswith(prefix + "/")


def is_credential_path(path: str) -> bool:
    # User creation stores password_hash; database errors can include SQL params.
    # Cover this entire namespace, including any later password update route.
    users = settings.API_V1_STR.rstrip("/") + "/users"
    return is_auth_path(path) or path == users or path.startswith(users + "/")


def safe_error_response(status_code: int, *, auth: bool = True) -> JSONResponse:
    """Use a fresh server ID and an allowlist, never caller or exception text."""
    if auth:
        if status_code not in _AUTH_ERRORS:
            status_code = 500
        code, message = _AUTH_ERRORS[status_code]
    else:
        errors = {
            400: ("REQUEST_INVALID", "请求数据无效"),
            401: ("REQUEST_UNAUTHORIZED", "认证失败"),
            403: ("REQUEST_FORBIDDEN", "请求被拒绝"),
            404: ("REQUEST_NOT_FOUND", "请求的资源不存在"),
            405: ("REQUEST_METHOD_NOT_ALLOWED", "请求方法不支持"),
            422: ("REQUEST_VALIDATION_ERROR", "请求数据验证失败"),
            429: ("REQUEST_RATE_LIMITED", "请求过于频繁"),
            500: ("INTERNAL_ERROR", "服务器内部错误"),
        }
        if status_code not in errors:
            status_code = 500
        code, message = errors[status_code]
    request_id = uuid4().hex
    # diagnose=False still includes exception text. Do not attach an exception at all.
    logger.opt(exception=None).log(
        "ERROR" if status_code >= 500 else "WARNING",
        "Request rejected: code={} request_id={}", code, request_id,
    )
    headers = {"X-Request-ID": request_id}
    if status_code == 401:
        headers["WWW-Authenticate"] = "Bearer"
    return JSONResponse(
        status_code=status_code,
        headers=headers,
        content={
            "status": "error", "code": code, "message": message,
            "detail": message, "errors": [], "request_id": request_id,
        },
    )


class CredentialErrorBoundaryMiddleware:
    """Consume credential-path failures before the server can rethrow/log them."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or not is_credential_path(scope.get("path", "")):
            await self.app(scope, receive, send)
            return
        response_started = False
        response_complete = False

        async def track_response(message):
            nonlocal response_started, response_complete
            if message["type"] == "http.response.start":
                response_started = True
            elif message["type"] == "http.response.body" and not message.get("more_body", False):
                response_complete = True
            await send(message)

        try:
            await self.app(scope, receive, track_response)
        except Exception:
            response = safe_error_response(500, auth=is_auth_path(scope.get("path", "")))
            if not response_started:
                await response(scope, receive, send)
            elif not response_complete:
                # A late dependency/stream failure cannot replace sent headers;
                # terminate the body without propagating credential-bearing traces.
                await send({"type": "http.response.body", "body": b""})
