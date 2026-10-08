"""Bounded native extensions; saved configuration never starts a server."""
import json
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, model_validator


class MockResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, hide_input_in_errors=True)
    enable: StrictBool = False
    statusCode: StrictInt = Field(default=200, ge=200, le=599)
    headers: dict[str, str] = Field(default_factory=dict)
    body: str = Field(default="", max_length=131072)
    delayMs: StrictInt = Field(default=0, ge=0, le=3000)

    @model_validator(mode="after")
    def bounded_response(self):
        if (len(self.headers) > 100 or any(not k or len(k) > 255 or len(v) > 20000 or '\r' in k + v or '\n' in k + v for k, v in self.headers.items())
                or len(json.dumps(self.model_dump(), ensure_ascii=False).encode()) > 256 * 1024):
            raise ValueError("Mock响应头或正文超过限制")
        return self
