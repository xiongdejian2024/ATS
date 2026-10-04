"""原抽象接口公开名称按需加载，不初始化设备。"""
from importlib import import_module
from xat_ecu.api.constants.common import *

_CLASSES = {'AbcAdb': 'adb', 'AbcBusComm': 'buscomm', 'AbcDiagMock': 'diagmock', 'AbcIo': 'ioNew', 'AbcLogManagement': 'logmanagment', 'AbcMix': 'mix', 'AbcMockMcu': 'mockmcu', 'AbcMockMpuMock': 'mockmpu', 'AbcSdTest': 'sdtest', 'AbcSerial': 'serial', 'AbcSoa': 'soa', 'AbcSsh': 'ssh', 'AbcTsp': 'tsp'}

def __getattr__(name):
    if name in _CLASSES:
        return getattr(import_module("xat_ecu.api.abc_interface." + _CLASSES[name]), name)
    helper = import_module("xat_ecu.api.common.common")
    try:
        return getattr(helper, name)
    except AttributeError:
        raise AttributeError(name) from None

__all__ = list(_CLASSES) + ['get_signal_times_interval', 'check_all_value_is', 'check_signal_value_exist', 'calculate_signal_times_and_duration', 'check_signal_num', 'parse_excel_to_signal_routing_csv', 'read_signal_routing_info', 'log_and_allure_step', 'crc8', 'get_current_time_delayed_timestamp', 'dealwithDID', 'transferDTCtoBytes', 'retry_on_failure', 'set_bench_vlan9_ip', 'start_process', 'stop_process', 'data_field_to_dict', 'check_gb_data_extremumData', 'get_signals_info_and_send_with_time', 'get_skip_ecu_list', 'next_occurrence_timestamp', 'get_timestamp_after_minutes'] + [name for name in globals() if not name.startswith("_") and name not in {"import_module"}]
