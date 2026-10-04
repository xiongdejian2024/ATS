"""按需加载原公共接口，公共类型与追踪器不提前加载设备和私有平台。"""
from importlib import import_module

_COMMON = ['CommonIo', 'CommonTsp', 'CommonSsh', 'CommonDiagMock', 'CommonSoa', 'CommonSerial', 'CommonSdTest', 'CommonBusComm', 'CommonLogManagement', 'CommonAdb', 'CommonMockMcu', 'CommonMockMpu']
_ABSTRACT = ['AbcAdb', 'AbcBusComm', 'AbcDiagMock', 'AbcTsp', 'AbcSsh', 'AbcIo', 'AbcSerial', 'AbcMix', 'AbcMockMpuMock', 'AbcSdTest', 'AbcLogManagement', 'AbcSoa', 'AbcMockMcu']
__all__ = _COMMON + _ABSTRACT


def __getattr__(name):
    if name not in __all__:
        raise AttributeError(name)
    module = 'interface' if name in _COMMON else 'abc_interface'
    return getattr(import_module('xat_ecu.api.' + module), name)
