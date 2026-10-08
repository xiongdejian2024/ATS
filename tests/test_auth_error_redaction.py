"""Exercise real application handlers with distinctive, synthetic credentials only."""
import asyncio
import json
import re
from types import SimpleNamespace

import pytest
from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.testclient import TestClient
from pydantic import BaseModel, model_validator
from sqlalchemy.exc import StatementError

import main
from api.deps import get_current_active_user, get_current_user
from config import settings
from core.logger import logger
from database import get_db

PASSWORD = "Synthetic-Passphrase!NeverEcho-79"
PASSWORD_HASH = "$2b$12$synthetic_hash_marker_not_a_real_password_hash"
TOKEN = "synthetic.header.payload.signature-never-echo"
SECRETS = (PASSWORD, PASSWORD_HASH, TOKEN)


@pytest.fixture
def logs():
    messages = []
    records = []

    def collect(message):
        messages.append(str(message))
        records.append(message.record)

    # Include exceptions and locals, so a logger.exception regression cannot hide
    # behind the production sinks' diagnose=False setting.
    sink = logger.add(collect, format="{message}\n{exception}", diagnose=True, backtrace=True)
    try:
        yield messages, records
    finally:
        logger.remove(sink)


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(main.app, "dependency_overrides", dict(main.app.dependency_overrides))
    monkeypatch.setattr(main.app.router, "routes", list(main.app.router.routes))
    main.app.dependency_overrides[get_current_active_user] = lambda: SimpleNamespace(id="synthetic")
    # Raising on application exceptions is intentional: a sanitized 500 from the
    # outer ServerErrorMiddleware still rethrows and would leak to uvicorn.error.
    with TestClient(main.app, raise_server_exceptions=True) as test_client:
        yield test_client


def assert_safe(response, logs, status=422, code="AUTH_INVALID_REQUEST"):
    assert response.status_code == status
    payload = response.json()
    assert payload["code"] == code
    assert payload["status"] == "error"
    assert payload["errors"] == []
    assert payload["detail"] == payload["message"]
    request_id = payload["request_id"]
    assert re.fullmatch(r"[a-f0-9]{32}", request_id)
    assert response.headers["x-request-id"] == request_id
    messages, records = logs
    all_output = response.text + repr(dict(response.headers)) + "".join(messages)
    for secret in SECRETS:
        assert secret not in all_output
    assert "Traceback" not in all_output
    matching = [record for record in records if request_id in record["message"]]
    assert len(matching) == 1
    assert code in matching[0]["message"]
    assert all(record["exception"] is None for record in records)


@pytest.mark.parametrize("endpoint,payload", [
    ("login", {"password": PASSWORD}),  # missing unrelated field echoes whole body
    ("login", {"username": "synthetic", "password": {"nested": [PASSWORD, PASSWORD_HASH, TOKEN]}}),
    ("login", [{"password": PASSWORD, "password_hash": PASSWORD_HASH, "token": TOKEN}]),
    ("login", PASSWORD),  # root input, with no credential field name
    ("refresh", {"other": {"refresh_token": TOKEN, "password": PASSWORD}}),
    ("refresh", {"refresh_token": [TOKEN, PASSWORD_HASH]}),
])
def test_auth_validation_never_echoes_input(endpoint, payload, client, logs):
    response = client.post(f"/api/v1/auth/{endpoint}", json=payload,
                           headers={"X-Request-ID": PASSWORD})
    assert_safe(response, logs)


@pytest.mark.parametrize("path", ["/api/v1/auth/login", "/api/v1/auth/refresh", "/api/v1/users"])
@pytest.mark.parametrize("body", [
    '{"password":"' + PASSWORD + '","token":"' + TOKEN + '",',
    '{"password":"' + PASSWORD + '"}\n' + PASSWORD_HASH,
])
def test_malformed_json_is_safe_everywhere(path, body, client, logs):
    response = client.post(path, content=body, headers={"Content-Type": "application/json"})
    code = "AUTH_INVALID_REQUEST" if "/auth/" in path else "REQUEST_VALIDATION_ERROR"
    assert_safe(response, logs, code=code)


def test_unparseable_json_http_exception_is_safe(client, logs):
    response = client.post("/api/v1/auth/login", content=b'\xff' + PASSWORD.encode(),
                           headers={"Content-Type": "application/json"})
    assert_safe(response, logs, status=400)


@pytest.mark.parametrize("method,path,payload", [
    ("post", "/api/v1/users", {"password": PASSWORD, "email": "synthetic@example.com"}),
    ("post", "/api/v1/users", {"username": "synthetic", "password": PASSWORD, "email": TOKEN}),
    ("put", "/api/v1/users/not-a-uuid", {"password": PASSWORD, "email": TOKEN}),
])
def test_user_credential_validation_is_safe(method, path, payload, client, logs):
    response = client.request(method, path, json=payload)
    assert_safe(response, logs, code="REQUEST_VALIDATION_ERROR")


def test_malformed_query_does_not_echo_any_credentials(client, logs):
    response = client.get("/api/v1/users", params={"page": PASSWORD, "token": TOKEN,
                                                 "password_hash": PASSWORD_HASH})
    assert_safe(response, logs, code="REQUEST_VALIDATION_ERROR")


class NestedPayload(BaseModel):
    metadata: dict

    @model_validator(mode="after")
    def fail_with_sensitive_context(self):
        raise ValueError(" | ".join(SECRETS))


def test_root_validator_message_and_nested_body_are_not_exposed(client, logs):
    @main.app.post("/redaction-test/nested")
    async def nested(payload: NestedPayload):
        return {"unexpected": True}

    response = client.post("/redaction-test/nested", json={"metadata": {
        "nested": [{"password": PASSWORD, "password_hash": PASSWORD_HASH, "refresh_token": TOKEN}],
    }})
    assert_safe(response, logs, code="REQUEST_VALIDATION_ERROR")


def test_custom_error_location_context_and_message_are_never_formatted(client, logs):
    @main.app.post("/redaction-test/custom")
    async def custom():
        raise RequestValidationError([{
            "type": TOKEN, "loc": ("body", PASSWORD), "msg": PASSWORD_HASH,
            "input": {"root": SECRETS}, "ctx": {"error": ValueError(PASSWORD)},
        }], body={"password": PASSWORD})

    response = client.post("/redaction-test/custom")
    assert_safe(response, logs, code="REQUEST_VALIDATION_ERROR")


@pytest.mark.parametrize("target", ["login", "refresh", "tokens", "profile", "users", "dependency", "teardown"])
def test_internal_failure_cannot_reach_server_traceback(target, client, logs, monkeypatch):
    # Development must be safe too. SQLAlchemy errors include statement parameters.
    monkeypatch.setattr(settings, "ENVIRONMENT", "development")

    def fail(*args, **kwargs):
        raise StatementError("configuration " + TOKEN, "INSERT users (password_hash)",
                             {"password": PASSWORD, "password_hash": PASSWORD_HASH}, ValueError(TOKEN))

    async def async_fail(*args, **kwargs):
        fail()

    endpoint = "/api/v1/auth/login"
    payload = {"username": "synthetic", "password": PASSWORD}
    if target == "login":
        monkeypatch.setattr(main.auth, "authenticate_user", async_fail)
    elif target == "refresh":
        monkeypatch.setattr(main.auth, "verify_token", fail)
        endpoint, payload = "/api/v1/auth/refresh", {"refresh_token": TOKEN}
    elif target == "tokens":
        async def user(*args):
            return SimpleNamespace(password_hash=PASSWORD_HASH)
        monkeypatch.setattr(main.auth, "authenticate_user", user)
        monkeypatch.setattr(main.auth, "create_tokens", async_fail)
    elif target == "profile":
        main.app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(password_hash=PASSWORD_HASH)
        response = client.get("/api/v1/auth/profile", headers={"Authorization": "Bearer " + TOKEN})
        assert_safe(response, logs, status=500, code="AUTH_INTERNAL_ERROR")
        return
    elif target == "users":
        monkeypatch.setattr(main.users, "create_user", async_fail)
        endpoint = "/api/v1/users"
        payload["email"] = "synthetic@example.com"
    elif target == "dependency":
        def broken_open():
            fail()
        main.app.dependency_overrides[get_db] = broken_open
    elif target == "teardown":
        def broken_session():
            try:
                yield object()
            finally:
                fail()
        main.app.dependency_overrides[get_db] = broken_session
        async def rejected(*args):
            raise HTTPException(401, detail="expected failure")
        monkeypatch.setattr(main.auth, "authenticate_user", rejected)
    response = client.post(endpoint, json=payload, headers={"X-Request-ID": PASSWORD})
    code = "INTERNAL_ERROR" if target == "users" else "AUTH_INTERNAL_ERROR"
    assert_safe(response, logs, status=500, code=code)


def test_http_exception_details_and_headers_are_not_reflected(client, logs, monkeypatch):
    async def rejected(*args):
        raise HTTPException(401, detail={"password": PASSWORD, "token": TOKEN},
                            headers={"X-Secret": PASSWORD_HASH, "WWW-Authenticate": TOKEN})

    monkeypatch.setattr(main.auth, "authenticate_user", rejected)
    response = client.post("/api/v1/auth/login", json={"username": "synthetic", "password": PASSWORD})
    assert_safe(response, logs, status=401, code="AUTH_UNAUTHORIZED")
    assert response.headers["www-authenticate"] == "Bearer"
    assert "x-secret" not in response.headers


def test_safe_request_ids_are_unique_and_client_ids_are_ignored(client, logs):
    first = client.post("/api/v1/auth/login", json={"password": PASSWORD},
                        headers={"X-Request-ID": TOKEN})
    second = client.post("/api/v1/auth/login", json={"password": PASSWORD},
                         headers={"X-Request-ID": TOKEN})
    assert_safe(first, logs)
    assert_safe(second, logs)
    assert first.json()["request_id"] != second.json()["request_id"]


def test_global_fallback_itself_is_safe(monkeypatch, logs):
    monkeypatch.setattr(settings, "ENVIRONMENT", "development")
    request = Request({"type": "http", "method": "POST", "path": "/api/v1/auth/login", "headers": []})
    response = asyncio.run(main.global_exception_handler(request, RuntimeError(" ".join(SECRETS))))
    body = json.loads(response.body)
    assert body["code"] == "AUTH_INTERNAL_ERROR"
    combined = response.body.decode() + "".join(logs[0])
    assert all(secret not in combined for secret in SECRETS)
    assert all(record["exception"] is None for record in logs[1])


def test_business_http_error_contract_is_preserved(client):
    @main.app.get("/redaction-test/business")
    async def business():
        raise HTTPException(409, detail={"reason": "business-conflict"}, headers={"X-Business": "kept"})

    response = client.get("/redaction-test/business")
    assert response.status_code == 409
    assert response.json() == {"detail": {"reason": "business-conflict"}}
    assert response.headers["x-business"] == "kept"


def test_successful_login_refresh_and_profile_remain_usable(client, logs):
    from uuid import uuid4
    from core.security import get_password_hash
    from database import SessionLocal
    from models import User

    with SessionLocal() as db:
        db.add(User(id=str(uuid4()), username="synthetic", email="synthetic@example.com",
                    password_hash=get_password_hash(PASSWORD), status=True))
        db.commit()
    response = client.post("/api/v1/auth/login", json={"username": "synthetic", "password": PASSWORD})
    assert response.status_code == 200
    token_data = response.json()["data"]
    refreshed = client.post("/api/v1/auth/refresh", json={"refresh_token": token_data["refresh_token"]})
    assert refreshed.status_code == 200
    access_token = refreshed.json()["data"]["access_token"]
    profile = client.get("/api/v1/auth/profile", headers={"Authorization": "Bearer " + access_token})
    assert profile.status_code == 200
    assert profile.json()["data"]["username"] == "synthetic"
    output = "".join(logs[0])
    assert PASSWORD not in response.text + refreshed.text + profile.text + output
    assert token_data["refresh_token"] not in output
    assert access_token not in output


def test_failure_after_response_start_does_not_escape_to_server(client, logs):
    from fastapi.responses import StreamingResponse

    @main.app.get("/api/v1/auth/redaction-test-late")
    async def late():
        async def body():
            yield b"started"
            raise RuntimeError(" ".join(SECRETS))
        return StreamingResponse(body())

    response = client.get("/api/v1/auth/redaction-test-late")
    # Headers already sent cannot be replaced, but no traceback may escape.
    assert response.status_code == 200
    assert response.text == "started"
    output = response.text + "".join(logs[0])
    assert all(secret not in output for secret in SECRETS)
    assert "AUTH_INTERNAL_ERROR" in output
    assert "Traceback" not in output
    assert all(record["exception"] is None for record in logs[1])
