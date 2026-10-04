"""
HAL Base Adapter - 硬件适配器基类

提供通用的日志记录、连接状态追踪、错误处理包装和上下文管理器支持。
所有具体硬件适配器（SocketCAN、Tosun、PCAN 等）都应继承此类。
"""

import logging
from typing import Any, Dict, Optional

from xat_ecu.core.interfaces import IHardwareAdapter
from xat_ecu.core.errors import HardwareError

logger = logging.getLogger(__name__)


class BaseHardwareAdapter(IHardwareAdapter):
    """
    硬件适配器的基类，提供通用的日志记录、状态追踪和上下文管理功能。

    子类需要实现 _do_connect, _do_disconnect, _do_send, _do_receive 四个模板方法。
    """

    def __init__(self, **kwargs: Any):
        self._config: Dict[str, Any] = kwargs
        self._connected: bool = False
        self._name: str = self.__class__.__name__
        self._log_path: Optional[str] = None

    # ============================================================
    # IHardwareAdapter 接口实现
    # ============================================================

    def connect(self, config: Dict[str, Any]) -> None:
        """连接硬件设备"""
        logger.info("连接硬件适配器：%s", self._name)
        self._config.update(config)
        try:
            self._do_connect(config)
            self._connected = True
            logger.info("硬件适配器已连接：%s", self._name)
        except Exception as e:
            logger.exception("硬件适配器连接失败：%s", self._name)
            raise HardwareError(f"Failed to connect {self._name}: {e}") from e

    def disconnect(self) -> None:
        """断开硬件连接并释放资源"""
        logger.info("断开硬件适配器：%s", self._name)
        try:
            self._do_disconnect()
        except Exception as e:
            logger.exception("硬件适配器断开失败：%s", self._name)
            raise HardwareError(f"断开适配器失败：{self._name}") from e
        finally:
            self._connected = False
            logger.info("硬件适配器连接状态已清理：%s", self._name)

    def send(self, data: bytes, **kwargs: Any) -> None:
        """发送数据到硬件"""
        if not self._connected:
            raise HardwareError(
                f"[{self._name}] Cannot send: adapter is not connected."
            )
        self._do_send(data, **kwargs)

    def receive(self, timeout: float = 1.0) -> Optional[bytes]:
        """从硬件接收数据"""
        if not self._connected:
            raise HardwareError(
                f"[{self._name}] Cannot receive: adapter is not connected."
            )
        return self._do_receive(timeout)

    @property
    def is_connected(self) -> bool:
        """当前是否已连接"""
        return self._connected

    # ============================================================
    # 模板方法 - 子类必须实现
    # ============================================================

    def _do_connect(self, config: Dict[str, Any]) -> None:
        """子类实现：执行实际的硬件连接逻辑"""
        raise NotImplementedError

    def _do_disconnect(self) -> None:
        """子类实现：执行实际的硬件断开逻辑"""
        raise NotImplementedError

    def _do_send(self, data: bytes, **kwargs: Any) -> None:
        """子类实现：执行实际的数据发送逻辑"""
        raise NotImplementedError

    def _do_receive(self, timeout: float) -> Optional[bytes]:
        """子类实现：执行实际的数据接收逻辑"""
        raise NotImplementedError

    # ============================================================
    # Context Manager
    # ============================================================

    def __enter__(self) -> "BaseHardwareAdapter":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.disconnect()
