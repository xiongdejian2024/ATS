import re
from nidaqmx.system import Device, System
from nidaqmx.constants import ProductCategory
from jidutest_io.constant import NiDeviceType


"""
  Validator for IO cli input
"""
def is_valid_ipv4_address(addr: str) -> bool:
    pattern='^((25[0-5]|2[0-4]\d|[10]?\d?\d)\.){3}(25[0-5]|2[0-4]\d|[10]?\d?\d)$'
    if re.search(pattern, addr):
        return True
    return False


def is_valid_io_device(device: str or Device) -> bool:
    if isinstance(device, str):
        try:
            device = Device(device)
        except:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/driver/jidutest_io/utils/io_device.py")
            return False
        
    if not isinstance(device, Device):
        return False
    
    system = System()
    if device in system.devices:
        return True
    return False


def is_valid_io_channel(channel: str) -> bool:
    device_name = channel.split("/")[0]
    if not is_valid_io_device(device_name):
        return False
    
    device_type = get_device_type(device_name)
    device = Device(device_name)
    if device_type is NiDeviceType.cModule_AI:
        return channel in device.ai_physical_chans.channel_names
    if device_type is NiDeviceType.cModule_AO:
        return channel in device.ao_physical_chans.channel_names
    if device_type is NiDeviceType.cModule_CI:
        return channel in device.ci_physical_chans.channel_names
    if device_type is NiDeviceType.cModule_CO:
        return channel in device.co_physical_chans.channel_names
    if device_type is NiDeviceType.cModule_DI:
        return channel in device.di_lines.channel_names
    if device_type is NiDeviceType.cModule_DO:
        return channel in device.do_lines.channel_names
    return False


"""
  Tool functions for IO
"""
def get_device_type(device: str or Device) -> NiDeviceType:
    if not is_valid_io_device(device):
        return None
    
    if isinstance(device, str):
        device = Device(device)
        
    if device.product_category is ProductCategory.COMPACT_DAQ_CHASSIS:
        return NiDeviceType.cDAQ
    
    if device.product_category is ProductCategory.C_SERIES_MODULE:
        if device.ai_physical_chans.channel_names:
            return NiDeviceType.cModule_AI
        if device.ao_physical_chans.channel_names:
            return NiDeviceType.cModule_AO
        if device.ci_physical_chans.channel_names:
            return NiDeviceType.cModule_CU
        if device.co_physical_chans.channel_names:
            return NiDeviceType.cModule_CO
        if device.di_ports.channel_names:
            return NiDeviceType.cModule_DI
        if device.do_ports.channel_names:
            return NiDeviceType.cModule_DO

    return None


def get_channel_type(channel: str) -> NiDeviceType:
    if not is_valid_io_channel(channel):
        return None
    
    device = channel.split("/")[0]
    return get_device_type(device)


def get_str(lst: list) -> str:
    rtn = ""
    for i,v in enumerate(lst):
        rtn = rtn + v + "\t"
        if (i+1)%4==0:
            rtn += "\n"
    return rtn
