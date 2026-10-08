"""Bounded literal declarations; expansion uses the existing ${name} renderer."""

import json
from pydantic import BaseModel, ConfigDict, Field, StrictBool, field_validator


class InitialVariable(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, hide_input_in_errors=True)
    name: str = Field(min_length=1, max_length=255)
    value: str = Field(default="", max_length=20000)
    enable: StrictBool = True
    description: str = Field(default="", max_length=1000)

    @field_validator("name")
    @classmethod
    def valid_name(cls, value):
        if not value.strip() or any(c in value for c in "${}\r\n\x00"):
            raise ValueError("变量名称须为非空文本，不能包含模板或控制字符")
        return value


def validate_variables(rows):
    if len(rows) > 100 or len({r.name for r in rows}) != len(rows):
        raise ValueError("变量最多100项，名称不能重复")
    if (
        len(json.dumps([r.model_dump() for r in rows], ensure_ascii=False).encode())
        > 65536
    ):
        raise ValueError("变量声明总量不能超过64KiB")
    return rows


def values(rows):
    return {r.name: r.value for r in rows if r.enable}


def wire_case(case):
    """Old strict Agents must receive no newly added empty fields."""
    data = case.model_dump()
    for field in ('initialVariables','globalPreProcessors','globalPostProcessors'):
        if not data[field]: data.pop(field)
    for request in data["requests"]:
        for field in ("initialVariables", "environmentVariables", "preProcessors", "postProcessors", "globalPreProcessors", "globalPostProcessors"):
            if not request[field]:
                request.pop(field)
        if not request.get("reportPhases"):
            request.pop("reportPhases", None)
        if not (request.get("mockResponse") or {}).get("enable"):
            request.pop("mockResponse", None)
    return data
