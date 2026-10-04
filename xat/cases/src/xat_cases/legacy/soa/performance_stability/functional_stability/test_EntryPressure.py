import allure
import pytest
import copy
import uuid
from time import sleep
from random import randint
from xat_ecu.legacy.common.data_type_handing import logger, DataTypeHanding
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_cases.legacy.bgm.case_helper.environment_check import partner_process_check
from xat_ecu.legacy.sdk.digital_key.RVCTSPMessage_pb2 import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.sdk.sdk_tools import *

KEY_MATCH_INFO = {1: [2, 3, 4, 5, 6, 8, 0xA, 0xB],
                  2: [2, 3, 4, 5, 6, 0xA, 0xB],
                  3: [3, 6, 0xA],
                  4: [4, 6, 0xB],
                  6: [8],
                  7: [8],
                  8: [8]
                  }


@allure.feature("性能稳定性")
@allure.story("业务稳定性/启动场景压测--进入系统")
@pytest.mark.soa
class TestEntryPressure(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        partner_process_check()
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([("EntryService", "client"),
                                     ("CentralLockService", "client"),
                                     ("ChassisService", "client"),
                                     ("KeyService", "client"),
                                     ("AVPService", "server"),
                                     ("RPAAPAService", "server"),
                                     ("HornService", "client"),
                                     ("DoorService", "client"),
                                     ("PedalService", "client"),
                                     ("CTDService", "client"),
                                     ])
        self.io.hood_door1_close()
        self.io.hood_door2_close()

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.dk.stop_listen_dk_bgm_response()
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.ipdu.rx_flag_reset_all()
        self.ipdu.reset_check_results()
        self.sd_tester.change_car_mode(0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')        
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.sd_tester.write_multi_ccp({94: 0x80, 98: 0x2, 97: 0x2, 10: 0x2, 481: 0x4, 578: 0x4, 142: 0x83})
        self.partner.send_method_request("KeyService_client", "SetConfigInfo", {"infos": [{"key": 5, "value": 0}]})
        self.dk.set_pass_seat_notpresent()
        self.dk.set_secle_seat_notpresent()
        self.dk.set_secmid_seat_notpresent()
        self.dk.set_secri_seat_notpresent()
        self.dk.reset_bncm_digital_keyinfo()
        self.sd_tester.change_car_mode(0)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.io.init_bgm_HW()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        self.partner.empty_all()
        self.dk.empty_dk_data_queue()

    def after_each_func(self, ecu):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 'NoYes1_No')
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        if ecu.get("testresult") != "Pass":
            logger.info("case失败，需等待10s让环境恢复")
            sleep(10)
        else:
            sleep(3)  # 避免防玩
        super().after_each_func(ecu, start=False)
    
    def ck_EntrySystemAudioLightInfo(self, audio, light, timeout=2.0):
        """校验进入系统声光提醒信息"""
        self.partner.ck_s2s_event(ENTRY_SERVICE_CLIENT, "EntrySystemAudioLightInfo", {"info": {"audio": audio, "light": light}}, timeout)
        self.partner.ck_s2s_event(ENTRY_SERVICE_CLIENT, "EntrySystemAudioLightInfo", {"info": {"audio": 0, "light": 0}}, timeout)
        self.partner.send_request_and_ck_resp(ENTRY_SERVICE_CLIENT, "GetEntrySystemAudioLightInfo", {}, {"out": {"audio": 0, "light": 0}})
 
    def ck_NotifyLockWarning(self, lock=None, Reminder=None, ck_horn=True, timeout=2.0):
        """校验进入系统的报警信息"""
        if ck_horn:
            self.partner.ck_s2s_event("HornService_client", "Status", {"sts": 0}, timeout=0.4)  # todo: 之后切换io输出校验
            self.partner.ck_s2s_event("HornService_client", "Status", {"sts": 1}, timeout=0.2)
        else:
            self.partner.ck_no_event("HornService_client", "Status")
        if lock is None and Reminder is None:
            self.partner.ck_no_event(ENTRY_SERVICE_CLIENT, "NotifyLockWarning")
        else:
            self.partner.ck_s2s_event(ENTRY_SERVICE_CLIENT, "NotifyLockWarning", {"warnnings": {"lock": lock, "reminder": Reminder}}, timeout)
            if lock != 0 or Reminder != 0:
            # 通知完成后将提示请求置为IDLE     
                self.partner.ck_s2s_event(ENTRY_SERVICE_CLIENT, "NotifyLockWarning", {"warnnings": {"lock": 0, "reminder": 0}})
                self.partner.send_request_and_ck_resp(ENTRY_SERVICE_CLIENT, "GetLockWarning", {}, {"out": {"lock": 0, "reminder": 0}})    
    
    Times=50
    @allure.title("BGM重启后踩刹车_触发关主驾门")
    @pytest.mark.full
    @pytest.mark.restart
    @pytest.mark.repeat(Times)
    def test_caseid_1984237(self):        
        self.dk.set_cenlock_sts(1)
        # 当usgMod=0/1/2时， VehModMngtGlbSafe1EgyLvlElecMai =0 ；usgMod=11/13,不判断
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 8) # SWSR：507156
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)  # 制动踏板位置
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)  # 制动踏板踩下无故障
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1) 
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorOpenerDrvrSts', 2) # sts
        self.partner.empty_all(5)
        self.ipdu.pause_all_bus_send()
        self.bgm_power_off_and_on() # 无需等待服务连接
        self.ipdu.resume_all_bus_send() # 待MCU起来    
        # self.partner.empty_all(3)
        # logger.info(f"打印当前时间1")
        # 检测到刹车状态变更的event事件后，才会触发踩刹车自动关门
        # self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        # BrakePedalStatus  #上电后接口中有1s等待时间，性能指标为7s内功能可用
        # self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalStatus", {"status": {"value": 1, "validity": 0}})
        self.dk.ck_door_opener_cmd(1, 2, timeout=7.1)
        self.dk.ck_door_opener_cmd(2, 0) 