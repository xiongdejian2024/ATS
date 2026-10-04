"""
Core Events - 事件总线

提供发布/订阅机制，用于模块间松耦合通信。
替代原有的直接方法调用和回调链。
"""

import threading
import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
from enum import Enum, auto


class EventType(Enum):
    """预定义的事件类型"""
    # 连接事件
    HARDWARE_CONNECTED = auto()
    HARDWARE_DISCONNECTED = auto()
    TRANSPORT_OPENED = auto()
    TRANSPORT_CLOSED = auto()

    # 诊断事件
    DIAG_REQUEST_SENT = auto()
    DIAG_RESPONSE_RECEIVED = auto()
    DIAG_SESSION_CHANGED = auto()
    DIAG_SECURITY_UNLOCKED = auto()

    # 总线事件
    BUS_MESSAGE_SENT = auto()
    BUS_MESSAGE_RECEIVED = auto()
    BUS_ERROR = auto()
    CYCLIC_MSG_STARTED = auto()
    CYCLIC_MSG_STOPPED = auto()

    # 刷写事件
    FLASH_STARTED = auto()
    FLASH_PROGRESS = auto()
    FLASH_COMPLETED = auto()
    FLASH_FAILED = auto()

    # 信号事件
    SIGNAL_VALUE_CHANGED = auto()

    # 通用
    CUSTOM = auto()


@dataclass
class Event:
    """事件数据"""
    event_type: EventType
    source: str = ""               # 事件来源模块
    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = 0.0


class EventBus:
    """
    事件总线 - 线程安全的发布/订阅机制

    Usage:
        bus = EventBus()

        # 订阅事件
        def on_message(event: Event):
            print(f"Received: {event.data}")

        bus.subscribe(EventType.BUS_MESSAGE_RECEIVED, on_message)

        # 发布事件
        bus.publish(Event(
            event_type=EventType.BUS_MESSAGE_RECEIVED,
            data={"msg_id": 0x123, "data": b"\\x01\\x02"}
        ))
    """

    _instance: Optional["EventBus"] = None
    _lock = threading.Lock()

    def __new__(cls) -> "EventBus":
        """单例模式 - 全局唯一的事件总线"""
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._subscribers: Dict[
                    EventType, List[Callable[[Event], None]]
                ] = {}
                cls._instance._sub_lock = threading.Lock()
        return cls._instance

    def subscribe(self, event_type: EventType,
                  callback: Callable[[Event], None]) -> None:
        """
        订阅事件

        Args:
            event_type: 要监听的事件类型
            callback: 事件处理回调函数
        """
        with self._sub_lock:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            if callback not in self._subscribers[event_type]:
                self._subscribers[event_type].append(callback)

    def unsubscribe(self, event_type: EventType,
                    callback: Callable[[Event], None]) -> None:
        """
        取消订阅

        Args:
            event_type: 事件类型
            callback: 要移除的回调函数
        """
        with self._sub_lock:
            if event_type in self._subscribers:
                try:
                    self._subscribers[event_type].remove(callback)
                except ValueError:
                    pass

    def publish(self, event: Event) -> None:
        """
        发布事件 - 同步通知所有订阅者

        Args:
            event: 要发布的事件
        """
        import time
        if event.timestamp == 0.0:
            event.timestamp = time.time()

        with self._sub_lock:
            callbacks = list(self._subscribers.get(event.event_type, []))

        for callback in callbacks:
            try:
                callback(event)
            except Exception:
                # 订阅者异常不应影响事件总线
                logging.getLogger(__name__).exception("XAT ECU 事件订阅者执行失败：%s", event.event_type)

    def clear(self) -> None:
        """清除所有订阅"""
        with self._sub_lock:
            self._subscribers.clear()

    @classmethod
    def reset(cls) -> None:
        """重置单例（仅用于测试）"""
        with cls._lock:
            if cls._instance is not None:
                cls._instance.clear()
            cls._instance = None
