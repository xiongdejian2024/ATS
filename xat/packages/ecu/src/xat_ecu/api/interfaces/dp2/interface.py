from __future__ import annotations
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :interface.py
@Time         :2024/10/25 17:11
@Author       :dejian.xiong@jiduauto.com
@Description  :每个对象接口的启动部分
"""

import time
from xat_ecu.api.call_tracker import BaseABCMeta
from xat_ecu.api.interfaces.dp2 import *


class CommonAdb(metaclass=BaseABCMeta):
    pass


class CommonBusComm(metaclass=BaseABCMeta):
    def __init__(self, cls_path, **cfg):
        from xat_ecu.legacy.sdk.bus_app import BusApp
        from xat_ecu.legacy.sdk.digital_key.digital_key_class import DigitalKey
        from xat_ecu.legacy.sdk.i_signal_i_pdu import ISignalIPdu
        self.cfg = cfg
        self.dut_ecu = self.cfg.get('dut_ecu')
        self.running_env = self.cfg.get('running_env', "HIL")
        self.ipdu = ISignalIPdu(cls_path=cls_path, dut_ecu=self.dut_ecu)
        self.bus_app = BusApp(self.ipdu, **self.cfg)
        self.dk = DigitalKey(self.ipdu, self.bus_app, None, self.cfg, auto_start=False)

    def start_all_cyclic_msg(self):
        if self.running_env == "SIL":
            self.ipdu.start_all_time_control(isrealbus=False)
        else:
            self.ipdu.start_all_time_control()
            self.bus_app.start_all_cyclic_msg()
        return

    def stop_all_cyclic_msgs(self):
        self.ipdu.time_control_stop()
        self.ipdu.recv_pdu_thread_all_stop()
        self.bus_app.stop_all_cyclic_msgs()
        return

    def start_dk(self):
        self.dk.start_dk()

    def stop_dk(self):
        self.dk.stop_dk()


class CommonDiagMock(metaclass=BaseABCMeta):
    # 需要在buscomm之后运行
    def __init__(self, **cfg):
        from xat_ecu.legacy.sdk.ecu_simulator_app import Ecu_Sim_App
        self.cfg = cfg
        self.dmock = Ecu_Sim_App(**self.cfg)

    def all_start(self):
        """
        全部 诊断server 启动 （包括doip和非doip）
        :returns:
        :raises keyError:
        """
        self.dmock.all_start()

    def all_close(self):
        """
        全部 诊断server 停止 （包括doip和非doip）
        :returns:
        :raises keyError:
        """
        self.dmock.all_close()

    def doip_sim_start(self):
        """
        doip 诊断server 启动
        :returns:
        :raises keyError:
        """
        self.dmock.doip_sim_start()

    def doip_sim_close(self):
        """
        doip 诊断server 停止
        :returns:
        :raises keyError:
        """
        self.dmock.doip_sim_close()

    def all_ecu_start(self):
        """
        非 doip 诊断server 启动
        :returns:
        :raises keyError:
        """
        self.dmock.all_ecu_start()

    def all_ecu_close(self):
        """
        非 doip 诊断server 停止
        :returns:
        :raises keyError:
        """
        self.dmock.all_ecu_close()


class CommonIo(metaclass=BaseABCMeta):
    def __init__(self, tc_config: dict):
        from xat_ecu.legacy.sdk.driver.jidutest_io.io.io_system import IOSystem
        from xat_ecu.legacy.interface.nuc_app import NucApp
        self.nuc_app = NucApp(tb_cfg=tc_config)
        self.io = IOSystem(io_config=tc_config, auto_start=False)

    def start_io(self):
        self.io.start_io()

    def stop_io(self):
        self.io.close()


class CommonLogManagement(metaclass=BaseABCMeta):
    def __init__(self):
        from xat_ecu.legacy.common.logmanagment.logmanager import Logmagment
        self.log_manage = Logmagment()

    def start_record_log(self, case_name: str):
        self.log_manage.start_record_log(case_name)

    def stop_record_log(self):
        return self.log_manage.stop_record_log()

    def start_record_soa_partner_log(self):
        self.log_manage.start_record_soa_partner_log()

    def stop_record_soa_partner_log(self):
        return self.log_manage.stop_record_soa_partner_log()


class CommonMock(metaclass=BaseABCMeta):

    def __init__(self, **kwargs):
        from xat_ecu.legacy.sdk.Internal_ETH.tools.mock_udp_tcp_server_dp2 import MockTcp
        from xat_ecu.legacy.sdk.Internal_ETH.tools.mock_udp_tcp_server_dp2 import MockUdp
        self.cfg = kwargs.get("cfg")
        self.channel_dict = kwargs.get("channel_dict")
        self.veh_type = kwargs.get("veh_type")
        self.bl_ver = kwargs.get("bl_ver")
        self.tcp = MockTcp(channel_dict=self.channel_dict, veh_type=self.veh_type, bl_ver=self.bl_ver)
        self.udp = MockUdp(channel_dict=self.channel_dict, veh_type=self.veh_type, bl_ver=self.bl_ver)
        # self.diag = Ecu_Sim_App(**self.cfg)


class CommonSdTest(metaclass=BaseABCMeta):
    def __init__(self, **cfg):
        from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
        self.sd_tester = Sd_Tester(**cfg)

    def start_sd_tester(self):
        self.sd_tester.diagnostic_client_sim_start()
        time.sleep(0.5)
        self.sd_tester.tester_present()
        time.sleep(0.5)
        self.sd_tester.update_serverdoipid(0x1002)

    def stop_sd_tester(self):
        self.sd_tester.stop_tester_present()
        time.sleep(0.5)
        self.sd_tester.diagnostic_client_sim_close()
        time.sleep(0.5)


class CommonSerial(metaclass=BaseABCMeta):
    def __init__(self, *args, **kwargs):
        from xat_ecu.legacy.driver.serial_client import BaseSerial
        self.serial = BaseSerial(*args, baudrate=921600, auto_start=False, is_check_login=False, timeout=0.1, **kwargs)

    def start_serial(self):
        return self.serial.start_serial()

    def stop_serial(self):
        return self.serial.close()


class CommonSoa(metaclass=BaseABCMeta):
    def __init__(self):
        from xat_ecu.legacy.soa_partner.src.base_partner import S2sBaseClass
        self.soa_partner = S2sBaseClass(auto_start=False)

    def stop_soa(self):
        return self.soa_partner.stop_operators()


class CommonSsh(metaclass=BaseABCMeta):
    def __init__(self, domain):
        from xat_ecu.legacy.interface.cd_soc.cd_soc_ssh import CD_SOC_SSH
        self.device_dict = {}
        self.domain = domain.upper()
        if self.domain == DeviceName.CCU_CD.value:
            self.cd_soc = CD_SOC_SSH()
            self.device_dict[DeviceName.CCU_CD] = self.cd_soc
        elif self.domain == DeviceName.CCU_CD_LCU.value:
            pass
        elif self.domain == DeviceName.CCU_CD_AD.value:
            pass
        elif self.domain == DeviceName.CCU_CD_AD_LCU.value:
            pass
        elif self.domain == DeviceName.LCU_L.value:
            pass
        elif self.domain == DeviceName.LCU_R.value:
            pass
        logger.debug(f"self.device_dict:{self.device_dict}")


class CommonTsp(metaclass=BaseABCMeta):
    def __init__(self, **cfg):
        self.cfg = cfg
        self.vid = self.cfg.get('vid')
        self.vin = self.cfg.get('vin')
        self.tel = self.cfg.get('tel')

# 保留显式模块属性访问；普通导入不初始化设备或私有服务。
_DEFERRED_IMPORTS = {'BaseSerial': ('xat_ecu.legacy.driver.serial_client', 'BaseSerial'), 'Sd_Tester': ('xat_ecu.legacy.ecu_sim.sd_tester', 'Sd_Tester'), 'CD_SOC_SSH': ('xat_ecu.legacy.interface.cd_soc.cd_soc_ssh', 'CD_SOC_SSH'), 'NucApp': ('xat_ecu.legacy.interface.nuc_app', 'NucApp'), 'MockUdp': ('xat_ecu.legacy.sdk.Internal_ETH.tools.mock_udp_tcp_server_dp2', 'MockUdp'), 'MockTcp': ('xat_ecu.legacy.sdk.Internal_ETH.tools.mock_udp_tcp_server_dp2', 'MockTcp'), 'BusApp': ('xat_ecu.legacy.sdk.bus_app', 'BusApp'), 'DigitalKey': ('xat_ecu.legacy.sdk.digital_key.digital_key_class', 'DigitalKey'), 'IOSystem': ('xat_ecu.legacy.sdk.driver.jidutest_io.io.io_system', 'IOSystem'), 'Ecu_Sim_App': ('xat_ecu.legacy.sdk.ecu_simulator_app', 'Ecu_Sim_App'), 'ISignalIPdu': ('xat_ecu.legacy.sdk.i_signal_i_pdu', 'ISignalIPdu'), 'S2sBaseClass': ('xat_ecu.legacy.soa_partner.src.base_partner', 'S2sBaseClass')}

def __getattr__(name):
    if name not in _DEFERRED_IMPORTS:
        raise AttributeError(name)
    from importlib import import_module
    module, attribute = _DEFERRED_IMPORTS[name]
    value = getattr(import_module(module), attribute)
    globals()[name] = value
    return value

_DEFERRED_IMPORTS["Logmagment"] = ("xat_ecu.legacy.common.logmanagment.logmanager", "Logmagment")
