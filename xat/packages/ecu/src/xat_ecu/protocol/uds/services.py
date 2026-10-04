"""
UDS Protocol Services Registry
"""

from abc import abstractmethod
import logging

logger = logging.getLogger(__name__)


class ProtocolMeta(type):
    """
    Metaclass for UDS protocol services registry.
    """
    REGISTRY = {}

    def __init__(cls, *args, **kwargs):
        cls._instance = None
        super(ProtocolMeta, cls).__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ProtocolMeta, cls).__call__(*args, **kwargs)
        return cls._instance

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        if name != "ProtocolParser":
            cls.REGISTRY[name] = new_cls
        return new_cls

    @classmethod
    def get_registry(cls):
        return cls.REGISTRY

    @classmethod
    def uninstall_registry(cls, name: str):
        if name in cls.REGISTRY:
            return cls.REGISTRY.pop(name)
        return None


class ProtocolParser(metaclass=ProtocolMeta):
    """
    Base class for protocol parsers/builders.
    """
    
    def __init__(self):
        self._objects = {}

    @classmethod
    @abstractmethod
    def protocol_build(cls, data: dict):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def protocol_parse(cls, data, frame_obj=None):
        raise NotImplementedError


class UdsServiceRegistry:
    @classmethod
    def get_service(cls, name):
        return ProtocolMeta.get_registry().get(name)

# Here we could define the base services or we can let them be defined dynamically.
# For simplicity and clear architecture, we will define placeholders for standard services.

class UdsServiceSid10(ProtocolParser):
    @classmethod
    def protocol_build(cls, data: dict):
        pass
        
    @classmethod
    def protocol_parse(cls, data, frame_obj=None):
        pass

class UdsServiceSid11(ProtocolParser):
    @classmethod
    def protocol_build(cls, data: dict):
        pass
        
    @classmethod
    def protocol_parse(cls, data, frame_obj=None):
        pass

# Add other service stubs as needed: 0x14, 0x19, 0x22, 0x27, 0x2E, 0x2F, 0x31, 0x34, 0x36, 0x37, 0x3E, 0x85
