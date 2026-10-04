"""
Credentials - Providers for handling credentials safely
"""

import os
import base64
from typing import Dict, Any

from xat_ecu.core.interfaces import ICredentialProvider
from xat_ecu.utils.file_utils import load_yaml


class CredentialProvider(ICredentialProvider):
    """基本凭证提供者（支持直接注入）"""
    def __init__(self, credentials: Dict[str, Dict[str, str]] = None):
        self._credentials = credentials or {}

    def get_credential(self, name: str) -> Dict[str, str]:
        if name not in self._credentials:
            raise KeyError(f"Credential '{name}' not found.")
        return self._credentials[name]

    def has_credential(self, name: str) -> bool:
        return name in self._credentials
        
    def add_credential(self, name: str, cred_dict: Dict[str, str]) -> None:
        self._credentials[name] = cred_dict


class EnvCredentialProvider(ICredentialProvider):
    """从环境变量加载凭证"""
    
    def __init__(self, prefix: str = "XAT_CRED_"):
        self.prefix = prefix
        
    def get_credential(self, name: str) -> Dict[str, str]:
        # Expecting env vars like: AUTO_SDK_CRED_BGM_USERNAME, AUTO_SDK_CRED_BGM_PASSWORD
        env_prefix = f"{self.prefix}{name.upper()}_"
        
        cred = {}
        for key, value in os.environ.items():
            if key.startswith(env_prefix):
                cred_key = key[len(env_prefix):].lower()
                cred[cred_key] = value
                
        if not cred:
            raise KeyError(f"Credential '{name}' not found in environment.")
            
        return cred
        
    def has_credential(self, name: str) -> bool:
        env_prefix = f"{self.prefix}{name.upper()}_"
        return any(key.startswith(env_prefix) for key in os.environ)


class YamlCredentialProvider(ICredentialProvider):
    """从 YAML 文件加载凭证"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._credentials = {}
        self._load()
        
    def _load(self):
        if os.path.exists(self.file_path):
            data = load_yaml(self.file_path)
            if isinstance(data, dict) and 'credentials' in data:
                self._credentials = data['credentials']
                
    def get_credential(self, name: str) -> Dict[str, str]:
        if name not in self._credentials:
            raise KeyError(f"Credential '{name}' not found in YAML.")
        return self._credentials[name]
        
    def has_credential(self, name: str) -> bool:
        return name in self._credentials


class LegacyCredentialProvider(ICredentialProvider):
    """向后兼容加载旧的 constants.py 中 Base64 编码的凭证"""
    
    def __init__(self, module_path: str = "xat_ecu.legacy.common.constant"):
        self.module_path = module_path
        self._credentials = {}
        self._load()
        
    def _load(self):
        try:
            import importlib
            module = importlib.import_module(self.module_path)
            
            # Simple heuristic to find constant classes like BGM_CONSTANT
            for attr_name in dir(module):
                if attr_name.endswith("_CONSTANT"):
                    ecu_name = attr_name.split("_")[0].lower()
                    cls = getattr(module, attr_name)
                    
                    cred = {}
                    for prop in dir(cls):
                        if not prop.startswith("_"):
                            val = getattr(cls, prop)
                            if isinstance(val, str) and self._is_base64(val):
                                decoded = base64.b64decode(val).decode('utf-8')
                                key = prop.split("_")[-1].lower()
                                cred[key] = decoded
                                
                    if cred:
                        self._credentials[ecu_name] = cred
                        
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/config/credentials.py")
            import logging
            logging.getLogger(__name__).warning(f"Failed to load legacy credentials: {e}")

    def _is_base64(self, s: str) -> bool:
        # 简单启发式，检查是否可能为 base64
        if len(s) % 4 != 0: return False
        try:
            return base64.b64encode(base64.b64decode(s)).decode('utf-8') == s
        except Exception:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/config/credentials.py")
            return False

    def get_credential(self, name: str) -> Dict[str, str]:
        name_lower = name.lower()
        if name_lower not in self._credentials:
            raise KeyError(f"Legacy credential '{name}' not found.")
        return self._credentials[name_lower]
        
    def has_credential(self, name: str) -> bool:
        return name.lower() in self._credentials
