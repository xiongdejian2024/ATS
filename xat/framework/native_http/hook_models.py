"""References at save time; only the controller may freeze executable script data."""
import json
from pathlib import PurePosixPath, PureWindowsPath
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, model_validator


class Model(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True, hide_input_in_errors=True)


class ScriptHook(Model):
    type: Literal['script'] = 'script'
    id: str = Field(min_length=1, max_length=36)
    name: str = Field(default='脚本钩子', max_length=255)
    enable: StrictBool = True
    jobId: str = Field(min_length=1, max_length=36)
    expectedRevision: StrictInt | None = Field(default=None, ge=1)


class HookConfig(Model):
    name: str = Field(min_length=1, max_length=255)
    environmentId: str = Field(min_length=1, max_length=36)
    mode: Literal['python', 'shell', 'command']
    script: str = Field(default='', max_length=65536)
    command: str = Field(default='', max_length=4096)
    args: list[str] = Field(default_factory=list, max_length=128)
    workDir: str = Field(default='', max_length=500)
    timeoutSeconds: float = Field(default=3600, ge=1, le=86400, allow_inf_nan=False)

    @model_validator(mode='after')
    def bounded(self):
        if ((self.mode == 'command' and (not self.command.strip() or self.script))
                or (self.mode != 'command' and (not self.script.strip() or self.command))):
            raise ValueError('脚本模式与内容不一致')
        values=[self.script,self.command,self.workDir,*self.args]
        if (any('\x00' in v for v in values) or any(len(v)>8192 for v in self.args)
                or len(self.script.encode())>65536 or len(json.dumps(values,ensure_ascii=False).encode())>128*1024):
            raise ValueError('脚本配置超过容量')
        for path in (PurePosixPath(self.workDir),PureWindowsPath(self.workDir)):
            if path.is_absolute() or path.drive or '..' in path.parts:
                raise ValueError('工作目录必须位于执行工作空间')
        return self


class FrozenScriptHook(ScriptHook):
    projectId: str = Field(min_length=1, max_length=36)
    revision: StrictInt = Field(ge=1)
    config: HookConfig
