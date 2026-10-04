from typing import Dict, Type, Any, List
from xat_ecu.core.interfaces import IHardwareAdapter
import logging

logger = logging.getLogger(__name__)

class AdapterRegistry:
    """
    硬件适配器注册表，用于自动发现和管理适配器。
    Hardware adapter registry for auto-discovering and managing adapters.
    """
    _adapters: Dict[str, Type[IHardwareAdapter]] = {}

    @classmethod
    def register(cls, name: str):
        """
        注册适配器的装饰器。
        Decorator to register an adapter.
        """
        def decorator(adapter_cls: Type[IHardwareAdapter]):
            if name in cls._adapters:
                logger.warning(f"Adapter '{name}' is already registered. Overwriting.")
            cls._adapters[name] = adapter_cls
            return adapter_cls
        return decorator

    @classmethod
    def get_adapter_class(cls, name: str) -> Type[IHardwareAdapter]:
        """
        获取已注册的适配器类。
        Get a registered adapter class.
        """
        if name not in cls._adapters:
            raise ValueError(f"Adapter '{name}' not found. Available adapters: {list(cls._adapters.keys())}")
        return cls._adapters[name]

    @classmethod
    def get_available_adapters(cls) -> List[str]:
        """
        获取所有可用适配器的名称。
        Get names of all available adapters.
        """
        return list(cls._adapters.keys())
