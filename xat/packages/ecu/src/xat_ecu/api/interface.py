from __future__ import annotations
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :interface.py
@Time         :2024/10/21 14:05
@Author       :dejian.xiong@jiduauto.com
@Description  :每个对象接口的启动部分
"""
import base64
import time
from functools import partial

from xat_ecu.legacy.common.data_type_handing import DataTypeHanding
from xat_ecu.legacy.common.logger import logger
from xat_ecu.api.call_tracker import BaseABCMeta
from xat_ecu.api.constants.common import DeviceName, VSP_PUBLIC_ACCOUNT


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
        # self.dk = DigitalKey(self.ipdu, self.bus_app, None, self.cfg, auto_start=False)
        self.dk = DigitalKey(self.ipdu, self.bus_app, None, self.cfg)
        self.ccp_raw_value = "A3018006FD030201A302090304020102848B06010004050203000002048F800C01010301020182020102160107010101000301020285820202010203026E74030101010101010103010202020201020102010101010102020103010201800203028001800001008180110103040101010102010302810202010101010104010101010101010203010103020201830201010201012902010402038002810381040114010A80010101020102020382050205010102020180040102010101020203010101030202030402040201010103020A010101010201010180810A0102040107070A0A07070A0A00000400010201020101010180030301020000000202020102020402010102000000010300010300018101000000000000000000000000000001010101000000000000000100010100000201000080000000008403010300000000020100000000000000000002018001020101010101020103020180018002020201010102050380010601030110010003030100000000000300000000000000000000000000000000000000000002000000000001010301000000000200000000000000000000000000000000000000000000000000010201010000000002040302010101020202048501020101020302030101020201010101010202020401020101010101030200000280020202010102010202020103010302020101010101010101000101010201010502020204080808080302010402010202010101020101010301010100000000000001020301020117030101010202020101030104020401010101010203030505020001010201010101010101020101020101010101010101020102020101020101010101000106000000020100010101040401000102000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002020205080802010102000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002020202020102020101020202020202020201020201020102020202010202020201010201010202010102010202010201010101020101010102010101010102010101000101010101020202010101010201010101010102020102020101020101010001010101010101020101010101020101010101010101010101010101010101010101010202020201010101020200000101010101010101010101010101010101010202000101010101010202020101010100000000000000000000000000000000000000000000000000000000000000000000010102020202020201020202010202020101010101010202020201010002020202020102020201020001C862"
        self.mock_ccp_flag = False
        self.block_bytes = {}  # RVS 蓝牙数据上报存储对象  {'10102':[Bytes]}
        self.lin_schedule_data = None

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


class CommonMockMcu(metaclass=BaseABCMeta):

    def __init__(self, ipdu=None, **kwargs):
        from xat_ecu.legacy.sdk.Internal_ETH.tools.bgm_eth_internal_mock_mcu import BgmEthInternalMockMcu
        self.bgm_eth_internal = BgmEthInternalMockMcu(ipdu, **kwargs)
        self.ccp = DataTypeHanding.hexstr_to_inlist(
            "A3018006FD030101A302090304020102858B06010004050203000001048C800C0101010102010202010216010701010100030102028089020301010302736E03010101010101010302020202020A010103820201010102020103010201800202020201800000008182118003010103020102020302800102010102010104010101010101010203010103020101830201020201012902010402038002820103040128030A800104010201020203820402810101020101130301010101010205020101000302020304020202010101020001010101010101010180030A0101040607070A0A07070A0A00000400000201010101010280030301020000000202020102020200010102000000010300000100008100000000000000000000000000000080000000000000000000000100010100000200000080000000008403010100000000020100000000000000000002018001020101010101020103020180018002020101010101050380020601030110000002030100000000000000000000000000000000000000000000000000000002000000000001010301000000000200000000000000000000000000000000000000000000000000010201000000000085040102020201020202040301020201028004030101020201030101010202020101020101010101030000000180020201010202010202020102010302020101010101010101000103010201010502020204010101010301010402010201010101020101010101010100000000000001020301010109030101010202020101030104010401010101010201030105020001010101010101010101010101010101010101010101010202010101010102010101010201000001010401000000010100000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001030202080100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001010201020102020101020101010101010201010201010101010202010201010101020202020202010202010202010201010101020101010102010101000102010101000101010101020202010101020201010101010102020102010101010101010001010101010101020101010101020101010101010101010101010101010101010101020201020101010101010100000101010101010101020101010101010101010202000101010101010202020101010100000000000000000000000000000000000000000000000000000000000000000000020202020202020101010101010101020101010101010202020202010002020101020102020201020001")

    def start_mock(self):
        self.bgm_eth_internal.env_pre_process()

    def stop_mock(self):
        self.bgm_eth_internal.env_post_process()


class CommonMockMpu(metaclass=BaseABCMeta):
    def __init__(self):
        self.pm_socket = None
        self.s2s_socket = None
        self.mcu_log_socke = None
        self.mcu_log_socket = None
        self.udp_socket = None


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
        self.lastHandleUid = 0
        self.LastHandleType = 0
        self.APAFunctionStatus = 0
        self.apaFunctionFailReason = 0

    def stop_soa(self):
        return self.soa_partner.stop_operators()


class CommonSsh(metaclass=BaseABCMeta):
    def __init__(self, domain):
        from xat_ecu.legacy.interface.acu.acu_ssh import ACU_SSH
        from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH
        from xat_ecu.legacy.interface.cdc.cdca_adb import CDCA_ADB
        from xat_ecu.legacy.interface.cdc.cdcq_ssh import CDCQ_SSH
        from xat_ecu.legacy.interface.tcam.tcam_ssh import TCAM_SSH
        self.device_dict = {}
        self.domain = domain
        if domain == "single_tcam":
            self.tcam_ssh = TCAM_SSH()
            self.device_dict[DeviceName.TCAM.value] = self.tcam_ssh
        elif domain == "single_bgm":
            self.bgm_ssh = BGM_SSH()
            self.device_dict[DeviceName.BGM.value] = self.bgm_ssh
        elif domain == "two_domain":
            self.bgm_ssh = BGM_SSH()
            self.tcam_ssh = TCAM_SSH(connect_type='obd')
            self.device_dict[DeviceName.BGM.value] = self.bgm_ssh
            self.device_dict[DeviceName.TCAM.value] = self.tcam_ssh
        elif domain == "four_domain":
            self.bgm_ssh = BGM_SSH()
            self.tcam_ssh = TCAM_SSH(connect_type='obd')
            self.acu_ssh = ACU_SSH()
            self.cdcq_ssh = CDCQ_SSH()
            self.device_dict = {
                DeviceName.BGM.value: self.bgm_ssh,
                DeviceName.TCAM.value: self.tcam_ssh,
                DeviceName.ACU.value: self.acu_ssh,
                DeviceName.CDCQ.value: self.cdcq_ssh,
            }
        self.cdca_adb = CDCA_ADB()


class CommonTsp(metaclass=BaseABCMeta):
    def __init__(self, **cfg):
        from xat_ecu.legacy.interface.rvs.rvs_lib import ES_client
        from groot2 import FotaPortalTaskManager
        from xat_ecu.legacy.tsp.rvs_client import RvsClient
        from groot2 import VspApi
        self.cfg = cfg
        self.vid = self.cfg.get('vid')
        self.vin = self.cfg.get('vin')
        self.tel = self.cfg.get('tel')
        logger.info("Get bench config: vid {0}, tel {1}".format(self.vid, self.tel))
        self.rvs_obj = partial(RvsClient, vid=self.vid)  # 偏函数，调用的时候需要加括号才可以使用，例如self.rvs_client()
        self.log_platform_obj = ES_client()
        self.ota_obj = partial(
            FotaPortalTaskManager,
            x_jidu_color="vehicle-future-sl",
            user_name=base64.b64decode(VSP_PUBLIC_ACCOUNT.Name).decode('utf-8'),
            password=base64.b64decode(VSP_PUBLIC_ACCOUNT.Password).decode(
                'utf-8'))  # 偏函数，调用的时候需要加括号才可以使用，例如self.ota(task_id)
        self.api = VspApi(env_name="staging")
        self.token_url = __import__("os").environ.get('XAT_CREDENTIAL_____INTERFACE_PY_TOKEN_URL', "")
        self.pb_url = 'https://api.jidustaging.com/api/rvc/test/jsonToPB'
        self.cmd_url = 'https://apistaging.jiduapp.cn/api/rvc/client/sendRealTimeCmd'
        self.Ready_url = 'http://api.jidustaging.com/api/rvc/client/opQuickReady'
        self.gb32960_dirct_url = "http://10.80.51.28:8887/gb32960Receiverer/queryList"
        self.gb32960_forward_url = "https://platform-vehicle.jidustaging.com/api/remote-monitor-gb/cms/v1/timelyData"
        self.Subscribe_task_url = "https://api.jidustaging.com/api/rvc/client/opSubscribeSuperTask"
        # self.cybertron_url = "http://10.80.192.141:8080"
        self.log_search_list = []
        self.token = None

# 保留显式模块属性访问；普通导入不初始化设备或私有服务。
_DEFERRED_IMPORTS = {'FotaPortalTaskManager': ('groot2', 'FotaPortalTaskManager'), 'VspApi': ('groot2', 'VspApi'), 'BaseSerial': ('xat_ecu.legacy.driver.serial_client', 'BaseSerial'), 'Sd_Tester': ('xat_ecu.legacy.ecu_sim.sd_tester', 'Sd_Tester'), 'ACU_SSH': ('xat_ecu.legacy.interface.acu.acu_ssh', 'ACU_SSH'), 'BGM_SSH': ('xat_ecu.legacy.interface.bgm.bgm_ssh', 'BGM_SSH'), 'CDCA_ADB': ('xat_ecu.legacy.interface.cdc.cdca_adb', 'CDCA_ADB'), 'CDCQ_SSH': ('xat_ecu.legacy.interface.cdc.cdcq_ssh', 'CDCQ_SSH'), 'NucApp': ('xat_ecu.legacy.interface.nuc_app', 'NucApp'), 'ES_client': ('xat_ecu.legacy.interface.rvs.rvs_lib', 'ES_client'), 'TCAM_SSH': ('xat_ecu.legacy.interface.tcam.tcam_ssh', 'TCAM_SSH'), 'BgmEthInternalMockMcu': ('xat_ecu.legacy.sdk.Internal_ETH.tools.bgm_eth_internal_mock_mcu', 'BgmEthInternalMockMcu'), 'BusApp': ('xat_ecu.legacy.sdk.bus_app', 'BusApp'), 'DigitalKey': ('xat_ecu.legacy.sdk.digital_key.digital_key_class', 'DigitalKey'), 'IOSystem': ('xat_ecu.legacy.sdk.driver.jidutest_io.io.io_system', 'IOSystem'), 'Ecu_Sim_App': ('xat_ecu.legacy.sdk.ecu_simulator_app', 'Ecu_Sim_App'), 'ISignalIPdu': ('xat_ecu.legacy.sdk.i_signal_i_pdu', 'ISignalIPdu'), 'S2sBaseClass': ('xat_ecu.legacy.soa_partner.src.base_partner', 'S2sBaseClass'), 'RvsClient': ('xat_ecu.legacy.tsp.rvs_client', 'RvsClient')}

def __getattr__(name):
    if name not in _DEFERRED_IMPORTS:
        raise AttributeError(name)
    from importlib import import_module
    module, attribute = _DEFERRED_IMPORTS[name]
    value = getattr(import_module(module), attribute)
    globals()[name] = value
    return value

_DEFERRED_IMPORTS["Logmagment"] = ("xat_ecu.legacy.common.logmanagment.logmanager", "Logmagment")
