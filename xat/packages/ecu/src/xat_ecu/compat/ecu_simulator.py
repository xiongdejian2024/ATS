"""按需使用迁入 XAT 的原接口，避免把不兼容的新类当成原接口。"""
from importlib import import_module

_INTERFACES = {
    "ECUInterface": ("xat_ecu.legacy.interface.ecuinterface", "EcuInterFace"),
    "BusApp": ("xat_ecu.legacy.sdk.bus_app", "BusApp"),
    "Diagnostic_Odx_Client_Sim_App": ("xat_ecu.legacy.sdk.diagnostic_odx_client_simulator_app", "Diagnostic_Odx_Client_Sim_App"),
    "Sd_Tester": ("xat_ecu.legacy.ecu_sim.sd_tester", "Sd_Tester"),
}


def __getattr__(name):
    if name not in _INTERFACES:
        raise AttributeError(name)
    module, attribute = _INTERFACES[name]
    return getattr(import_module(module), attribute)
