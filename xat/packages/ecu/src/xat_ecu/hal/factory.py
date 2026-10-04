from typing import Any, List
from xat_ecu.core.interfaces import IHardwareAdapter
from xat_ecu.hal.registry import AdapterRegistry

class HardwareFactory:
    """
    硬件适配器工厂，用于创建适配器实例。
    Hardware factory for creating adapter instances.
    """
    @staticmethod
    def create(name: str, **config: Any) -> IHardwareAdapter:
        """
        创建指定名称的硬件适配器实例。
        Create an instance of the specified hardware adapter.
        
        Args:
            name: 适配器名称 (Adapter name)
            **config: 适配器配置参数 (Adapter configuration parameters)
            
        Returns:
            IHardwareAdapter: 适配器实例 (Adapter instance)
        """
        adapter_cls = AdapterRegistry.get_adapter_class(name)
        return adapter_cls(**config)

    @staticmethod
    def list_adapters() -> List[str]:
        """
        列出所有可用的硬件适配器。
        List all available hardware adapters.
        
        Returns:
            List[str]: 适配器名称列表 (List of adapter names)
        """
        return AdapterRegistry.get_available_adapters()
