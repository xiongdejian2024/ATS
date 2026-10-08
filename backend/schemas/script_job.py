"""Small, bounded user script contract. Agent validates independently."""
import json
from pathlib import PurePosixPath, PureWindowsPath
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, StrictBool, model_validator


class ScriptJobConfig(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    name: str = Field(min_length=1, max_length=255)
    environment_id: str = Field(alias="environmentId", min_length=1, max_length=36)
    mode: Literal["shell", "python", "command"]
    script: str = Field(default="", max_length=65536)
    command: str = Field(default="", max_length=4096)
    args: list[str] = Field(default_factory=list, max_length=128)
    work_dir: str = Field(default="", alias="workDir", max_length=500)
    timeout_seconds: float = Field(default=3600, alias="timeoutSeconds", ge=1, le=86400, strict=True, allow_inf_nan=False)

    @model_validator(mode="after")
    def bounded(self):
        self.name = self.name.strip()
        if not self.name or (self.mode == "command" and (not self.command.strip() or self.script)):
            raise ValueError("命令模式需要可执行文件，且不能同时填写脚本")
        if self.mode != "command" and (not self.script.strip() or self.command):
            raise ValueError("脚本模式需要脚本内容，且不能同时填写命令")
        values = [self.script, self.command, self.work_dir, *self.args]
        if any("\x00" in value for value in values) or any(len(arg) > 8192 for arg in self.args):
            raise ValueError("脚本参数包含无效字符或超出长度上限")
        if len(json.dumps(values, ensure_ascii=False).encode()) > 128 * 1024 or len(self.script.encode()) > 65536:
            raise ValueError("脚本或参数过大")
        for path in (PurePosixPath(self.work_dir), PureWindowsPath(self.work_dir)):
            if path.is_absolute() or path.drive or ".." in path.parts:
                raise ValueError("工作目录必须为工作空间内的相对路径")
        return self


class ScriptJobCreate(ScriptJobConfig):
    project_id: str = Field(alias="projectId", min_length=1, max_length=36)


class ResolveScriptJob(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    confirmed_stopped: StrictBool = Field(alias="confirmedStopped")
    reason: str = Field(default="", max_length=1000)
