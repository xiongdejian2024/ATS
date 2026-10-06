"""请求文件只引用不可变内容，冻结契约不接受节点本地路径。"""

from pydantic import BaseModel, ConfigDict, Field, StrictInt, field_validator


class Model(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, hide_input_in_errors=True)


class FileReference(Model):
    fileId: str = Field(pattern=r"^[a-zA-Z0-9_-]{1,36}$")
    fileAlias: str = Field(default="", max_length=255)

    @field_validator("fileAlias")
    @classmethod
    def valid_alias(cls, value):
        if any(c in value for c in "\x00\r\n/\\"):
            raise ValueError("文件别名不能包含路径或控制字符")
        return value


class BinaryBody(Model):
    file: FileReference | None = None
    description: str = Field(default="", max_length=255)


class FrozenFile(Model):
    fileId: str = Field(pattern=r"^[a-zA-Z0-9_-]{1,36}$")
    fileName: str = Field(min_length=1, max_length=255)
    contentType: str = Field(min_length=1, max_length=255)
    byteLength: StrictInt = Field(ge=0)
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")

    @field_validator("fileName", "contentType")
    @classmethod
    def valid_header(cls, value):
        if any(c in value for c in "\x00\r\n"):
            raise ValueError("文件元数据不能包含控制字符")
        return value
