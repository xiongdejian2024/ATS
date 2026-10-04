"""库资源定位与配置凭证解析，不依赖框架、用例或旧工程。"""
import os
import re
from pathlib import Path

LIBRARY_ROOT = Path(__file__).resolve().parent
LEGACY_ROOT = LIBRARY_ROOT / 'legacy'


def resolve_environment(value):
    if isinstance(value, dict):
        return {key: resolve_environment(item) for key, item in value.items()}
    if isinstance(value, list):
        return [resolve_environment(item) for item in value]
    if isinstance(value, str):
        def lookup(match):
            name = match.group(1)
            if name not in os.environ:
                raise ValueError('缺少配置凭证环境变量：' + name)
            return os.environ[name]
        return re.sub(r'\$\{(XAT_CREDENTIAL_[A-Z0-9_]+)\}', lookup, value)
    return value
