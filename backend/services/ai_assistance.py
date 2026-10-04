"""OpenAI 兼容模型协议适配；不执行模型生成的代码。"""
import base64
import asyncio
import hashlib
import ipaddress
import json
import re
import socket
import uuid
import httpx
from cryptography.fernet import Fernet, InvalidToken
from fastapi import HTTPException
from loguru import logger
from config import settings
from models.ai_assistance import AIModelConfig, AIConversation, AICaseDraft
from schemas.ai_assistance import DraftContent


def cipher():
    secret = getattr(settings, "AI_ENCRYPTION_KEY", "") or settings.JWT_SECRET_KEY
    return Fernet(base64.urlsafe_b64encode(hashlib.sha256(secret.encode()).digest()))


def encrypt_key(value):
    return cipher().encrypt(value.encode()).decode() if value else None


def decrypt_key(value):
    if not value:
        return None
    try:
        return cipher().decrypt(value.encode()).decode()
    except InvalidToken as exc:
        logger.exception("模型密钥解密失败，请重新配置密钥")
        raise HTTPException(503, "模型密钥无法解密，请在模型设置中重新填写") from exc


def get_config(db, user):
    personal = db.query(AIModelConfig).filter_by(owner_key=user.id).first()
    config = personal or db.query(AIModelConfig).filter_by(owner_key="system").first()
    if not config or not config.enabled:
        raise HTTPException(409, "尚未启用模型服务，请先完成模型设置")
    return config


def config_view(config):
    if not config:
        return None
    return {"base_url": config.base_url, "model": config.model,
            "has_api_key": bool(config.api_key_encrypted), "enabled": config.enabled,
            "timeout_seconds": config.timeout_seconds,
            "scope": "system" if config.owner_key == "system" else "personal"}


async def resolve_model_endpoint(base_url):
    """校验解析地址并固定本次连接IP，保留本地模型以及原域名TLS验证。"""
    original = httpx.URL(base_url + "/chat/completions")
    addresses = await asyncio.wait_for(asyncio.get_running_loop().getaddrinfo(
        original.host, original.port or (443 if original.scheme == "https" else 80),
        type=socket.SOCK_STREAM,
    ), timeout=5)
    parsed = []
    for record in addresses:
        address = ipaddress.ip_address(record[4][0])
        effective = address.ipv4_mapped if isinstance(address, ipaddress.IPv6Address) and address.ipv4_mapped else address
        if effective.is_link_local or effective.is_multicast or effective.is_unspecified:
            raise HTTPException(400, "模型地址解析到了不允许访问的网络地址")
        parsed.append(address)
    if not parsed:
        raise HTTPException(502, "模型地址没有可用的解析结果")
    # IPv4优先兼容只监听127.0.0.1的本地模型。URL固定IP避免第二次DNS解析改变目的地。
    parsed.sort(key=lambda address: address.version)
    return original.copy_with(host=str(parsed[0])), original.netloc.decode("ascii"), original.host


async def complete(config, messages):
    key = decrypt_key(config.api_key_encrypted)
    headers = {"Authorization": "Bearer " + key} if key else {}
    logger.info("请求模型服务：模型={}，消息数={}", config.model, len(messages))
    try:
        endpoint, host, hostname = await resolve_model_endpoint(config.base_url)
        headers["Host"] = host
        async with httpx.AsyncClient(timeout=config.timeout_seconds, follow_redirects=False, trust_env=False) as client:
            response = await client.post(endpoint, headers=headers, extensions={"sni_hostname": hostname},
                                         json={"model": config.model, "messages": messages, "stream": False})
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            if not isinstance(content, str) or not content.strip():
                raise ValueError("模型未返回文本")
            if len(content) > 120000:
                raise ValueError("模型输出超过限制")
            return content
    except (httpx.TimeoutException, asyncio.TimeoutError) as exc:
        logger.exception("模型服务响应超时")
        raise HTTPException(504, "模型服务响应超时，请稍后重试") from exc
    except (httpx.HTTPError, OSError, ValueError, KeyError, IndexError, TypeError) as exc:
        logger.exception("模型服务调用失败，未保存生成结果")
        raise HTTPException(502, "模型服务调用失败，请检查地址、模型名称和凭证；详情见服务日志") from exc


def owned_conversation(db, user, identifier):
    row = db.query(AIConversation).filter_by(id=identifier, user_id=user.id).first()
    if not row:
        raise HTTPException(404, "会话不存在")
    return row


def draft_view(row):
    return {"id": row.id, "project_id": row.project_id, "batch_id": row.batch_id,
            "content": row.content, "status": row.status, "revision": row.revision,
            "imported_case_id": row.imported_case_id, "created_at": row.created_at.isoformat()}


async def generate_drafts(db, user, request):
    config = get_config(db, user)
    schema = {"cases": [{"name": "用例名称", "type": request.case_type, "priority": "P2",
                        "precondition": "前置条件", "requirement_ref": "需求编号",
                        "steps": [{"action": "操作", "expected": "预期结果"}], "tags": []}]}
    instruction = ("你是测试设计助手。根据用户明确提供的需求生成中文测试用例草稿，覆盖正常、边界、异常场景。"
                   "不得假设测试已经执行，不生成设备执行命令。仅返回 JSON，无 Markdown。结构示例："
                   + json.dumps(schema, ensure_ascii=False)
                   + f"。严格生成 {request.count} 条，用例类型 {request.case_type}。")
    content = await complete(config, [{"role": "system", "content": instruction},
                                      {"role": "user", "content": request.requirement}])
    try:
        raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", content.strip())
        cases = json.loads(raw)["cases"]
        if not isinstance(cases, list) or len(cases) != request.count:
            raise ValueError("模型返回数量不符")
        parsed = [DraftContent.model_validate(case).model_dump() for case in cases]
        if any(case["type"] != request.case_type for case in parsed):
            raise ValueError("用例类型不符")
    except (ValueError, KeyError, TypeError) as exc:
        logger.exception("模型用例结构校验失败，不生成伪造草稿")
        raise HTTPException(502, "模型返回的用例格式不正确，请调整需求后重试") from exc
    batch = str(uuid.uuid4())
    rows = [AICaseDraft(user_id=user.id, project_id=request.project_id, batch_id=batch,
                        content=case, source_prompt=request.requirement) for case in parsed]
    db.add_all(rows)
    db.commit()
    logger.info("AI 草稿已生成：项目={}，批次={}，数量={}", request.project_id, batch, len(rows))
    return [draft_view(row) for row in rows]
