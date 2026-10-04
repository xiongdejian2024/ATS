"""AI 输入严格校验；模型输出始终先进入草稿。"""
from typing import Literal
from urllib.parse import urlsplit
import ipaddress
from pydantic import BaseModel, Field, field_validator, ConfigDict


class ModelConfiguration(BaseModel):
    base_url: str = Field(min_length=8, max_length=500)
    model: str = Field(min_length=1, max_length=200)
    api_key: str | None = Field(default=None, max_length=4096)
    clear_api_key: bool = False
    timeout_seconds: int = Field(default=60, ge=5, le=180)
    enabled: bool = True

    @field_validator("base_url")
    @classmethod
    def valid_url(cls, value):
        url = urlsplit(value)
        if url.scheme not in {"https", "http"} or not url.hostname or url.username or url.password or url.query or url.fragment:
            raise ValueError("请输入不含凭证或查询参数的 HTTP(S) API 地址")
        try:
            host = ipaddress.ip_address(url.hostname)
        except ValueError:
            host = None
        if host and (host.is_link_local or host.is_multicast or host.is_unspecified):
            raise ValueError("此地址不能用于模型服务")
        return value.rstrip("/")


class ChatRequest(BaseModel):
    project_id: str
    conversation_id: str | None = None
    message: str = Field(min_length=1, max_length=16000)


class GenerateRequest(BaseModel):
    project_id: str
    requirement: str = Field(min_length=5, max_length=24000)
    count: int = Field(default=5, ge=1, le=20)
    case_type: Literal["functional", "interface", "ui", "performance", "security"] = "functional"


class DraftStep(BaseModel):
    action: str = Field(min_length=1, max_length=4000)
    expected: str = Field(min_length=1, max_length=4000)


class DraftContent(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name: str = Field(min_length=1, max_length=500)
    type: Literal["functional", "interface", "ui", "performance", "security"] = "functional"
    priority: Literal["P0", "P1", "P2", "P3"] = "P2"
    precondition: str = Field(default="", max_length=4000)
    requirement_ref: str = Field(default="", max_length=255)
    steps: list[DraftStep] = Field(min_length=1, max_length=50)
    tags: list[str] = Field(default_factory=list, max_length=20)

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, value):
        if any(len(tag) > 100 for tag in value):
            raise ValueError("标签长度不能超过 100 字")
        return value


class DraftUpdate(BaseModel):
    revision: int = Field(ge=1)
    content: DraftContent


class DraftDecision(BaseModel):
    revision: int = Field(ge=1)
