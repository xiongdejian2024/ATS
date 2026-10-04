"""
Core Plugin - 插件注册与发现机制

支持通过装饰器或显式调用注册插件，实现第三方服务的可插拔集成。
替代原有在 bus_app.py 中直接 import BosApi/YouZiClient 的强耦合方式。
"""

import importlib
import logging
import threading
from typing import Any, Callable, Dict, Optional, Type, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


class PluginRegistry:
    """
    插件注册表 - 全局单例

    支持按类型注册和获取插件实例。第三方集成（飞书、Jira、BOS 等）
    通过插件方式注入，核心 SDK 不直接依赖它们。

    Usage:
        # 注册插件
        PluginRegistry.register("storage", BosStoragePlugin())
        PluginRegistry.register("notifier", FeishuPlugin(webhook="..."))

        # 使用插件（安全获取，不存在时返回 None）
        storage = PluginRegistry.get("storage")
        if storage:
            storage.upload("report.html", "/path/to/report.html")
    """

    _plugins: Dict[str, Any] = {}
    _factories: Dict[str, Callable[..., Any]] = {}
    _lock = threading.RLock()

    @classmethod
    def register(cls, plugin_type: str, plugin_instance: Any) -> None:
        """
        注册插件实例

        Args:
            plugin_type: 插件类型标识 (如 "storage", "notifier", "test_manager")
            plugin_instance: 插件实例
        """
        with cls._lock:
            cls._plugins[plugin_type] = plugin_instance
            logger.info(f"Plugin registered: {plugin_type} -> "
                       f"{type(plugin_instance).__name__}")

    @classmethod
    def register_factory(cls, plugin_type: str,
                         factory: Callable[..., Any]) -> None:
        """
        注册插件工厂（延迟实例化）

        Args:
            plugin_type: 插件类型标识
            factory: 创建插件实例的工厂函数
        """
        with cls._lock:
            cls._factories[plugin_type] = factory
            logger.info(f"Plugin factory registered: {plugin_type}")

    @classmethod
    def get(cls, plugin_type: str, default: Any = None) -> Any:
        """
        获取插件实例

        如果插件未直接注册但有工厂，则通过工厂创建并缓存。

        Args:
            plugin_type: 插件类型标识
            default: 未找到时的默认值

        Returns:
            插件实例或 default
        """
        with cls._lock:
            if plugin_type in cls._plugins:
                return cls._plugins[plugin_type]

            if plugin_type in cls._factories:
                try:
                    instance = cls._factories[plugin_type]()
                    cls._plugins[plugin_type] = instance
                    logger.info(
                        f"Plugin lazy-created: {plugin_type} -> "
                        f"{type(instance).__name__}"
                    )
                    return instance
                except Exception:
                    logger.exception("创建 ECU 库插件失败：%s", plugin_type)
                    raise

        return default

    @classmethod
    def get_required(cls, plugin_type: str) -> Any:
        """
        获取必需的插件，不存在时抛出异常

        Args:
            plugin_type: 插件类型标识

        Raises:
            PluginNotFoundError: 插件未注册
        """
        from xat_ecu.core.errors import PluginNotFoundError

        result = cls.get(plugin_type)
        if result is None:
            raise PluginNotFoundError(
                f"Required plugin '{plugin_type}' is not registered. "
                f"Available plugins: {list(cls._plugins.keys())}"
            )
        return result

    @classmethod
    def has(cls, plugin_type: str) -> bool:
        """检查插件是否已注册"""
        with cls._lock:
            return (plugin_type in cls._plugins or
                    plugin_type in cls._factories)

    @classmethod
    def unregister(cls, plugin_type: str) -> Optional[Any]:
        """
        注销插件

        Args:
            plugin_type: 插件类型标识

        Returns:
            被注销的插件实例或 None
        """
        with cls._lock:
            cls._factories.pop(plugin_type, None)
            return cls._plugins.pop(plugin_type, None)

    @classmethod
    def list_plugins(cls) -> Dict[str, str]:
        """列出所有已注册的插件"""
        with cls._lock:
            result = {}
            for name, instance in cls._plugins.items():
                result[name] = type(instance).__name__
            for name in cls._factories:
                if name not in result:
                    result[name] = "(factory, not yet created)"
            return result

    @classmethod
    def clear(cls) -> None:
        """清除所有注册（仅用于测试）"""
        with cls._lock:
            cls._plugins.clear()
            cls._factories.clear()

    @classmethod
    def load_plugin_module(cls, module_path: str) -> None:
        """
        从 Python 模块路径动态加载插件

        插件模块应在导入时自动调用 PluginRegistry.register()。

        Args:
            module_path: 模块路径 (如 "xat_ecu.plugins.jidu")
        """
        try:
            importlib.import_module(module_path)
            logger.info(f"Plugin module loaded: {module_path}")
        except ImportError:
            logger.exception("加载 ECU 库插件模块失败：%s", module_path)
            raise


def plugin(plugin_type: str) -> Callable[[Type[T]], Type[T]]:
    """
    插件注册装饰器

    在类定义时自动注册到 PluginRegistry。

    Usage:
        @plugin("storage")
        class BosStoragePlugin:
            def upload(self, name, path):
                ...
    """
    def decorator(cls: Type[T]) -> Type[T]:
        PluginRegistry.register_factory(plugin_type, cls)
        return cls
    return decorator
