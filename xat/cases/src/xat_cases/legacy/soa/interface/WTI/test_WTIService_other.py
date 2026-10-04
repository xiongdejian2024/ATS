"""
@File         :test_WTIService_other.py
@Time         :2023/10/26 17:20:31
@Author       :peipei.yang_ext@jiduauto.com
@Description  :
"""
import os
import sys

from xat_ecu.legacy.sdk.sdk_tools import check_pdu, get_pdu_value_and_time
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_cases.legacy.soa.case_helper.common_lib import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_cases.legacy.soa.case_helper.test_base import *
from xat_cases.legacy.soa.case_helper.utils import *
from xat_ecu.legacy.interface.bgm.bgm_env.change_bgm_env import *


@allure.feature("SOA服务接口")
@allure.story("WTI通知/WTIService_other")
@pytest.mark.ypp
class TestWTIService(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([("WTIService", "client")])
        self.partner.method_default_timeout = 0.1
        self.ipdu.send_pdu('chassiscan1', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.ipdu.send_pdu('chassiscan2', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.ipdu.send_pdu('propulsioncan', 0x516, [0x16, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.dk.stop_listen_dk_bgm_response()
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.sd_tester.tester_present()
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'EntityKeyWhiteListVers', self.dk.last_sync_time_entity)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'BLESlotKeyWhiteListVers', self.dk.last_sync_time_ble)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr29, 'DCChrgnHndlSts', 'OnBdChrgrHndlSts_ConnectedWithPower') # lin唤醒
        self.ipdu.set(self.ipdu.connectivitycanfd.TcamConnectivityFr12, 'RemHvStrtActvReq', 'OnOffNoReq_On')
        self.ipdu.set(self.ipdu.connectivitycanfd.TcamConnectivityFr12, 'RemDCChrgLidTelmReq', 'OnOffNoReq_On')
        self.dk.set_pass_seat_notpresent()
        self.dk.set_secle_seat_notpresent()
        self.dk.set_secmid_seat_notpresent()
        self.dk.set_secri_seat_notpresent()
        self.dk.reset_bncm_digital_keyinfo()
        # self.io.init_bgm_HW()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.sd_tester.stop_tester_present()
        super().after_each_func(ecu, start=False)

    def ck_no_specific_event_and_GetWarningMsgList(self, hint, info, timeout=1):
        """校验无指定warningMsgList事件，并请求WarningMsgList获取结果"""
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": str(info)}]})

    def ck_WarningMsgList_and_GetWarningMsgList(self, hint, info, timeout=3):
        """校验指定warningMsgList事件，并请求WarningMsgList获取结果"""
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint, "info": str(info)}]}, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": str(info)}]})

    def ck_no_specific_event_and_GetTelltaleList(self, hint, state, timeout=1):
        """校验无指定warningMsgList事件，并请求WarningMsgList获取结果"""
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "TelltaleList", hint, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                              {"out": [{"name": hint, "state": str(state)}]})

    def ck_TelltaleList_and_GetTelltaleList(self, hint, state, timeout=3):
        """校验指定TelltaleList事件，并请求TelltaleList获取结果"""
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList",
                                  {"list": [{"name": hint, "state": str(state)}]}, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                              {"out": [{"name": hint, "state": str(state)}]})

    @allure.title("获取充电口盖异常提示&通知充电口盖异常提示")  # 183没有lin2
    @pytest.mark.full
    def test_caseid_107680(self):
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcOverTrvlFb', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcOverTrvlFb', 1)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {'list': [{'name': 'Charge Lid Abnormal', 'info': "1"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{'name': 'Charge Lid Abnormal', 'info': "1"}]})
        sleep(1)
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcOverTrvlFb', 0)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {'list': [{'name': 'Charge Lid Abnormal', 'info': "0"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{'name': 'Charge Lid Abnormal', 'info': "0"}]})

    @allure.title("获取行人保护系统故障信息&通知行人保护系统故障信息")
    @pytest.mark.smoke
    def test_caseid_108521(self):
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'PedProtnMsgReqForFlt', 0)
        self.partner.empty_all(0.5)
        hint = "Pedestrian System Failure"
        for usage_mode in [0, 1, 2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            for forflt in [2, 1, 2, 3, 2, 0]:
                sleep(0.2)
                logger.info(f"打印信号{forflt}")
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'PedProtnMsgReqForFlt', forflt)
                if forflt == 2:
                    self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1, timeout=2)  # 两秒后结果拿到
                else:
                    self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0, timeout=2)

    @allure.title("获取行人保护系统激活信息&通知行人保护系统激活信息")
    @pytest.mark.full
    def test_caseid_108578(self):
        hint = "Pedestrian System Enabled"
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'PedProtnMsgReqForImpct', 0)
        for usage_mode in [0, 1, 2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'PedProtnMsgReqForImpct', 1)
            self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'PedProtnMsgReqForImpct', 0)
            self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)

    @allure.title("3D车模显示电动尾翼位置（Msg3DModelShowsTailPosition)")  # 183没有lin6
    @pytest.mark.sanity
    def test_caseid_108099(self):
        self.ipdu.set(self.ipdu.cem_lin6.AwmCem_Lin6Fr01, 'ActvReSplrPosn', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.cem_lin6.AwmCem_Lin6Fr01, 'ActvReSplrPosn', 1)
        sleep(0.1)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": "3D Model Shows Tail Position", "info": "1"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": "3D Model Shows Tail Position", "info": "1"}]})
        self.ipdu.set(self.ipdu.cem_lin6.AwmCem_Lin6Fr01, 'ActvReSplrPosn', 4)
        sleep(0.1)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": "3D Model Shows Tail Position", "info": "4"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": "3D Model Shows Tail Position", "info": "4"}]})
        self.ipdu.set(self.ipdu.cem_lin6.AwmCem_Lin6Fr01, 'ActvReSplrPosn', 0)
        sleep(0.1)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": "3D Model Shows Tail Position", "info": "0"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": "3D Model Shows Tail Position", "info": "0"}]})

    @allure.title("获取触摸换挡器&通知触摸换挡器_故障产生到恢复")
    @pytest.mark.sanity
    def test_caseid_107718(self):
        self.ipdu.set(self.ipdu.propulsioncan.EgsmPropFr01, 'GearLvrIllmnSts', 0)
        self.partner.empty_all(0.5)
        for usage_mode in [0, 1, 2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            self.ipdu.set(self.ipdu.propulsioncan.EgsmPropFr01, 'GearLvrIllmnSts', 1)
            sleep(1.3)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                      {"list": [{"name": "Touch Shift Activated", "info": '1'}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                  {"out": [{"name": "Touch Shift Activated", "info": '1'}]})
            self.ipdu.set(self.ipdu.propulsioncan.EgsmPropFr01, 'GearLvrIllmnSts', 0)
            sleep(1)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                      {"list": [{"name": "Touch Shift Activated", "info": '0'}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                  {"out": [{"name": "Touch Shift Activated", "info": '0'}]})

    @allure.title("获取安全气囊故障信息&通知安全气囊故障信息_切换到11") 
    @pytest.mark.sanity
    def test_caseid_1983454(self):
        hint = "Airbag Failure"
        for usage_mode in [1, 2, 0]:
            logger.info(f"打印模式{usage_mode}")
            self.sd_tester.change_usage_mode(usage_mode)
            self.sd_tester.change_usage_mode(11)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysMsgReq', 2)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                  {"out": [{"name": hint, "info": '0'}]})
            sleep(8)
            self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysMsgReq', 0)
            self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysMsgReq', 2)
            self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysMsgReq', 0)
            self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)

    @allure.title("获取安全气囊故障信息&通知安全气囊故障信息_切换到13")  
    @pytest.mark.smoke
    def test_caseid_1983455(self):
        hint = "Airbag Failure"
        for usage_mode in [1, 2, 0]:
            logger.info(f"打印模式{usage_mode}")
            self.sd_tester.change_usage_mode(usage_mode)
            self.sd_tester.change_usage_mode(13)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysMsgReq', 2)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                  {"out": [{"name": hint, "info": '0'}]})
            sleep(8)
            self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysMsgReq', 0)
            self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysMsgReq', 2)
            self.ck_WarningMsgList_and_GetWarningMsgList(hint, 1)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysMsgReq', 0)
            self.ck_WarningMsgList_and_GetWarningMsgList(hint, 0)

    @allure.title("获取安全气囊故障信息&通知安全气囊故障信息_未出现跳变")
    @pytest.mark.full
    def test_caseid_1984540(self):
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysMsgReq', 0)
        self.sd_tester.change_usage_mode(11)
        sleep(8)
        hint = "Airbag Failure"
        self.sd_tester.change_usage_mode(11)
        sleep(0.5)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysMsgReq', 2)
        self.partner.ck_wti_warning_and_resp(hint, 1)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysMsgReq', 0)
        self.partner.ck_wti_warning_and_resp(hint, 0)

    @allure.title("获取安全气囊故障信息&通知安全气囊故障信息_定时器停止后切换mode开启新的计时器")
    @pytest.mark.full
    def test_caseid_1987888(self):
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysMsgReq', 2)
        self.sd_tester.change_usage_mode(11)
        sleep(3)
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysMsgReq', 2)
        sleep(9)
        hint = "Airbag Failure"
        sleep(0.5)
        self.sd_tester.change_usage_mode(13)
        self.partner.ck_wti_coming_warning_and_resp(hint, 1, timeout=8, deviation=0.3)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysMsgReq', 0)
        self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=0.8)
        
######################################################################################################################################################## 
        
@allure.feature("SOA服务接口")
@allure.story("WTI通知/WTIService_other")
class TestWTIServiceMockMcu(TestBase): 

    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass([WTI_SERVICE_CLIENT, 
                                     CHARGELID_SERVICE_CLIENT,
                                     HIGHVOLTAGE_SERVICE_CLIENT])
        self.partner.wait_for_service_reconnect(CHARGELID_SERVICE_CLIENT) 
        self.partner.wait_for_service_reconnect(WTI_SERVICE_CLIENT) 
        sleep(5)

    def after_class(self, ecu):
        try:
            self.partner.stop_operators()
        except Exception as e:
            logger.error(f"{str(e)}")
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr09, 'ChrgLidRearSts', 2) # Status.sts 充电口盖当前状态 参数值：0=open 2=close 7=na
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetStatus", {}, {"out": 2}, timeout=3)
        self.partner.empty_all(1)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def set_usage_mode(self, mode):
        """通过模拟mcu cdd打包总线数据来输入usage mode给到S2S"""
        logger.info(f"设置usage mode: {mode}")
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', mode)
    
    def ck_no_specific_event_and_GetWarningMsgList(self, hint, info, timeout=1):
        """校验无指定warningMsgList事件,并请求WarningMsgList获取结果"""
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": str(info)}]})

    def ck_WarningMsgList_and_GetWarningMsgList(self, hint, info, timeout=3):
        """校验指定warningMsgList事件,并请求WarningMsgList获取结果"""
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint, "info": str(info)}]}, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": str(info)}]})
    
    def ck_no_specific_event_and_GetTelltaleList(self, hint, state, timeout=1):
        """校验无指定warningMsgList事件,并请求WarningMsgList获取结果"""
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "TelltaleList", hint, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                              {"out": [{"name": hint, "state": str(state)}]})

    def ck_TelltaleList_and_GetTelltaleList(self, hint, state, timeout=3):
        """校验指定TelltaleList事件,并请求TelltaleList获取结果"""
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList",
                                  {"list": [{"name": hint, "state": str(state)}]}, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                              {"out": [{"name": hint, "state": str(state)}]})
    
    @allure.title("安全气囊报警灯(TelltaleAirbag_flag2=0&RestrntSysLampReq=2|3&&&usagemode=2|11|13,模式不满足恢复）")
    @pytest.mark.full
    def test_caseid_1943272(self):
        hint = "Airbag"
        self.set_usage_mode(0)
        for usage_mode in [2, 11, 13]:
            self.set_usage_mode(usage_mode)
            logger.info(f"打印{usage_mode}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 0)
            sleep(0.3)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 2)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 3)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            sleep(8)#flag1==0
            self.ck_TelltaleList_and_GetTelltaleList(hint, 1)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 2)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 2)
            self.set_usage_mode(0)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 0)
            self.set_usage_mode(1)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
    
    @allure.title("安全气囊报警灯(TelltaleAirbag_flag2=1(信号丢失)--模式不满足恢复）")
    @pytest.mark.full
    def test_caseid_1979660(self):
        hint = "Airbag"
        self.set_usage_mode(0)
        for usage_mode in [2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 0)
            sleep(0.3)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 2)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 3)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            sleep(8)  # flag1==0
            self.ipdu.pause_bus_send("backbonefr")
            sleep(1.7)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 1)
            self.ipdu.resume_bus_send("backbonefr")
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 3)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                                  {"out": [{"name": "Airbag", "state": "1"}]})
            self.set_usage_mode(0)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 0)
            self.set_usage_mode(1)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                                  {"out": [{"name": "Airbag", "state": "0"}]})
    
    @allure.title("安全气囊报警灯(TelltaleAirbag_flag2==0&&信号！==2|3恢复)")
    @pytest.mark.full
    def test_caseid_1979664(self):
        hint = "Airbag"
        self.set_usage_mode(0)
        for usage_mode in [2, 11, 13]:
            self.set_usage_mode(usage_mode)
            logger.info(f"打印{usage_mode}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 0)
            sleep(0.3)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 3)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 2)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            sleep(8)  # flag1==0
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 3)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 1)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 2)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 2)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 0)  # 信号不为:2/3情况下恢复
            self.ck_TelltaleList_and_GetTelltaleList(hint, 0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 1)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                                  {"out": [{"name": "Airbag", "state": "0"}]})
    
    @allure.title("安全气囊报警灯(TelltaleAirbag_flag2=0&RestrntSysLampReq=2|3&&&usagemode=2|11|13--flag1==1恢复)")
    @pytest.mark.full
    def test_caseid_1979665(self):
        hint = "Airbag"
        self.set_usage_mode(0)
        for usage_mode in [2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 0)
            sleep(0.3)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 2)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 3)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            sleep(8)  # flag1==0
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 3)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 1)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 2)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 2)
            self.set_usage_mode(0) # flag1=1(RlyPwrDistbnCmd1WdIgnRlyExtCmd信号需要usagemode满足2/11/13即可置1)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 0)
            self.set_usage_mode(1)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                                  {"out": [{"name": "Airbag", "state": "0"}]})
    
    @allure.title("安全气囊报警灯TelltaleAirbag_第二种情况故障产生条件:2&&&3  恢复条件:3(lag1=1)")
    @pytest.mark.full
    def test_caseid_1979666(self):
        hint = "Airbag"
        self.set_usage_mode(0)
        for usage_mode in [2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 0)
            sleep(0.3)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 2)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 3)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
            sleep(8)
            self.ipdu.pause_bus_send("backbonefr")
            sleep(1.7)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                                  {"out": [{"name": "Airbag", "state": "1"}]})
            self.ipdu.resume_bus_send("backbonefr")
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 3)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                                  {"out": [{"name": "Airbag", "state": "1"}]})
            self.set_usage_mode(0)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 0)
    
    @allure.title("安全气囊报警灯TelltaleAirbag_Warning pending(flag1==1)--Normal(模式不满足)不报警)V1.3")
    @pytest.mark.full
    def test_caseid_1979668(self):
        hint = "Airbag"
        self.set_usage_mode(0)
        for usage_mode in [2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 0)
            sleep(0.3)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 2)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 3)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.set_usage_mode(0)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.set_usage_mode(1)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
    
    @allure.title("安全气囊报警灯TelltaleAirbag_Warning pending(flag1==1)--flag2==0&&RestrntSysLampReq!2|3__不报警)V1.3")
    @pytest.mark.full
    def test_caseid_1979675(self):
        hint = "Airbag"
        self.set_usage_mode(0)
        for usage_mode in [2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 0)
            sleep(0.3)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 3)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
            sleep(8)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 1)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 0)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 1)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                                  {"out": [{"name": "Airbag", "state": "0"}]})
    
    @allure.title("安全气囊报警灯TelltaleAirbag_Warning pending(flag1==1)--flag2==0&&RestrntSysLampReq!2|3__不报警)V1.3")
    @pytest.mark.full
    def test_caseid_1979685(self):
        hint = "Airbag"
        self.set_usage_mode(0)
        for usage_mode in [2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 0)
            sleep(0.3)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 3)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.ipdu.pause_bus_send("backbonefr")
            self.partner.ck_wti_coming_telltale_and_resp(hint, "1", timeout=7, deviation=0.5)
            self.ipdu.resume_bus_send("backbonefr")
            self.set_usage_mode(0)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 0)
            self.set_usage_mode(1)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                                  {"out": [{"name": "Airbag", "state": "0"}]})
    
    @allure.title( "安全气囊报警灯TelltaleAirbag_Warning pending(flag1==1)--flag2==0&&RestrntSysLampReq!2|3__不报警)V1.3")
    @pytest.mark.full
    def test_caseid_1979693(self):
        hint = "Airbag"
        self.set_usage_mode(0)
        for usage_mode in [2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 0)
            sleep(0.3)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 3)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
            sleep(8)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 1)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 2)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 2)
            self.ipdu.pause_bus_send("backbonefr")
            sleep(1.7)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 1)
            self.ipdu.resume_bus_send("backbonefr")
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 0)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 1)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                                  {"out": [{"name": "Airbag", "state": "0"}]})

    @allure.title("安全气囊报警灯TelltaleAirbag_flag2=0&2|11|13(故障待确认)--信号变化为0|1--再变成3(故障确认)--模式不满足(恢复)V1.3")
    @pytest.mark.full
    def test_caseid_1979695(self):
        hint = "Airbag"
        self.set_usage_mode(0)
        for usage_mode in [2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 0)
            sleep(0.3)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 2)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 3)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 0)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 3)
            sleep(8)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 1)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 1)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.set_usage_mode(0)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 0)
            self.set_usage_mode(1)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                                    {"out": [{"name": "Airbag", "state": "0"}]})
    
    @allure.title("安全气囊报警灯_flag!=1--1")
    @pytest.mark.full
    def test_caseid_1981506(self):
        hint = "Airbag"
        self.set_usage_mode(0)
        for usage_mode in [2, 11, 13]:
            self.set_usage_mode(usage_mode)
            logger.info(f"打印{usage_mode}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 0)
            sleep(0.3)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 3)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
            self.partner.ck_coming_event_and_resp(WTI_SERVICE_CLIENT, "TelltaleList", 
                                                  {"list": [{'name': 'Airbag', 'state': '1'}]}, timeout=8, deviation=0.5)
            self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT, resume_all_bus=False)
            sleep(5)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                        {"out": [{"name": "Airbag", "state": "0"}]}, timeout=10)
            logger.info(f"usage_mode:{usage_mode}, restart bgm success")
            self.ipdu.resume_all_bus_send()
            sleep(0.3)
            self.partner.ck_coming_event_and_resp(WTI_SERVICE_CLIENT, "TelltaleList", 
                                                  {"list": [{'name': 'Airbag', 'state': '1'}]}, timeout=8, deviation=1)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 0)
            sleep(0.2)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 0)

    @allure.title("获取充电口盖状态&通知充电口盖状态")
    @pytest.mark.sanity
    def test_caseid_107713(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr09, 'ChrgLidRearSts', 0)
        for usage_mode in [0, 1, 2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.partner.empty_all(0.5)
            for sts in [1, 2, 0]:
                logger.info(f"打印信号{sts}")
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr09, 'ChrgLidRearSts', sts)
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                          {'list': [{'name': 'Charge Lid Status', 'info': sts}]})
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                      {"out": [{'name': 'Charge Lid Status', 'info': sts}]})

    @allure.title("获取充电口盖信息&通知充电口盖信息")
    @pytest.mark.smoke
    def test_caseid_107669(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'ChrgLidRearFltSts', 0)
        for usage_mode in [0, 1, 2, 11, 13]:
            self.set_usage_mode(usage_mode)
            logger.info(f"打印模式{usage_mode}")
            self.partner.empty_all(0.5)
            for sts in [1, 0]:
                logger.info(f"打印信号{sts}")
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'ChrgLidRearFltSts', sts)
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                          {'list': [{'name': 'Charge Lid', 'info': sts}]})
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                      {"out": [{'name': 'Charge Lid', 'info': sts}]})

    @allure.title("获取启动相关信息&通知启动相关信息")  # pass
    @pytest.mark.sanity
    def test_caseid_1983356(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'StrtMsgToDrvr', 0)
        for usage_mode in [0, 1, 2, 11, 13]:
            self.set_usage_mode(usage_mode)
            logger.info(f"打印模式{usage_mode}")
            self.partner.empty_all(0.5)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'StrtMsgToDrvr', 1)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                      {"list": [{"name": "Starting", "info": '1'}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                  {"out": [{"name": "Starting", "info": '1'}]})
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'StrtMsgToDrvr', 7)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                      {"list": [{"name": "Starting", "info": '7'}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                  {"out": [{"name": "Starting", "info": '7'}]})
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'StrtMsgToDrvr', 10)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                      {"list": [{"name": "Starting", "info": 'A'}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                  {"out": [{"name": "Starting", "info": 'A'}]})
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'StrtMsgToDrvr', 0)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                      {"list": [{"name": "Starting", "info": '0'}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                  {"out": [{"name": "Starting", "info": '0'}]})

    @allure.title("获取车辆工作相关信息提醒&通知车辆工作相关信息提醒")
    @pytest.mark.sanity
    def test_caseid_108576(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr63, 'StrtInProgs', 0)
        self.partner.empty_all(0.5)
        for sts in [2, 0, 2, 1, 2, 3]:
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr63, 'StrtInProgs', sts)
            sleep(0.5)
            logger.info(f"打印信号{sts}")
            if sts == 2:
                self.partner.ck_s2s_event("WTIService_client", "WarningMsgList",
                                          {"list": [{"name": "Vehicle Working", "info": sts}]})
                self.partner.send_request_and_ck_resp("WTIService_client", "GetWarningMsgList", {},
                                                      {"out": [{"name": "Vehicle Working", "info": sts}]})
            else:
                self.partner.ck_s2s_event("WTIService_client", "WarningMsgList",
                                          {"list": [{"name": "Vehicle Working", "info": "0"}]})
                self.partner.send_request_and_ck_resp("WTIService_client", "GetWarningMsgList", {},
                                                      {"out": [{"name": "Vehicle Working", "info": "0"}]})

    @allure.title(" 获取未驻车提醒信息&通知未驻车提醒信息")
    @pytest.mark.sanity
    def test_caseid_1983357(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'VehNotParkInfoWarn', 0)
        self.partner.empty_all(0.5)
        for sts in [1, 2, 0]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'VehNotParkInfoWarn', sts)
            sleep(0.5)
            logger.info(f"打印信号{sts}")
            self.partner.ck_s2s_event("WTIService_client", "WarningMsgList",
                                      {"list": [{"name": "Not Parked", "info": sts}]})
            self.partner.send_request_and_ck_resp("WTIService_client", "GetWarningMsgList", {},
                                                  {"out": [{"name": "Not Parked", "info": sts}]})

    @allure.title("获取方向盘加热故障&通知方向盘加热故障") 
    @pytest.mark.sanity
    def test_caseid_108554(self):
        self.ipdu.set(self.ipdu.connectivitycanfd.VgmConnFr03, 'SteerWhlHeatgAvlSts', 0)
        self.partner.empty_all(0.5)
        for sts in [5, 1, 5, 2, 5, 3, 5, 4, 5, 6, 5, 7]:
            logger.info(f"打印信号{sts}")
            self.ipdu.set(self.ipdu.connectivitycanfd.VgmConnFr03, 'SteerWhlHeatgAvlSts', sts)
            sleep(0.2)
            if sts == 5:
                self.partner.ck_s2s_event("WTIService_client", "WarningMsgList",
                                          {"list": [{"name": "Steer Wheel Heat Warning", "info": "5"}]})
                self.partner.send_request_and_ck_resp("WTIService_client", "GetWarningMsgList", {},
                                                      {"out": [{"name": "Steer Wheel Heat Warning", "info": "5"}]})
            else:
                self.partner.ck_s2s_event("WTIService_client", "WarningMsgList",
                                          {"list": [{"name": "Steer Wheel Heat Warning", "info": "0"}]})
                self.partner.send_request_and_ck_resp("WTIService_client", "GetWarningMsgList", {},
                                                      {"out": [{"name": "Steer Wheel Heat Warning", "info": "0"}]})

    def set_ChargeLidCloseFailed(self, req=random.choice(list(range(100))), sts=random.choice([0, 7]), pos=random.choice(list(range(11, 101))), warnsts=[0, 0], info=0):
        '''充电口盖关闭失败'''
        Status={0:1, 2:2, 7:0}
        self.ipdu.set(self.ipdu.cem_lin2.CemCem_Lin2Fr06, 'ChrgLidManvgDCorAcDcReq2', req) # 500ms后会回101
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr09, 'ChrgLidRearSts', Status[sts]) # Status.sts 充电口盖当前状态 参数值：0=open 2=close 7=na
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcActPosn2', pos) # ChargeLidPos.pos 充电口盖位置百分比 0-100，255
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcBlkFb', warnsts[0]) # ChargeLidWarnSts.warnsts=[1]
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcOverTrvlFb', warnsts[1]) # ChargeLidWarnSts.warnsts=[2]
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0)   
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0) # pluggerStatus=0, isConnect=0
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"isConnect": False}}, timeout=3) # 充电枪未连接
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": "ChargeLidCloseFailed", "info": str(info)}]})
        self.partner.empty_all()

    @allure.title("充电口盖关闭失败_Normal&Pending_进入Pending后计时器超时_触发ChargeLidWarnSts.warnsts=[1]后无告警") 
    @pytest.mark.full
    def test_caseid_1988802(self): # ChrgLidManvgDCorAcDcReq2:|EventChargeLidStatus|EventChargeLidWarnStsCallback|updateMsg name:ChargeLidCloseFailed,info|EventChargeLidPosCallback,pos|mChargeLidSmSts,change from|ChargingInfo,isConnected
        hint = "ChargeLidCloseFailed" # mChargeLidSmSts,change from ==> 0=normal,1=pending,2=warning
        self.set_ChargeLidCloseFailed()
        self.ipdu.set(self.ipdu.cem_lin2.CemCem_Lin2Fr06, 'ChrgLidManvgDCorAcDcReq2', 100) # 500ms后会回101, 进入Pending
        sleep(3) # Timer=2.5s，超时
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcBlkFb', 1) # 超时后触发异常，无失败告警
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetWarnStatus", {}, {"out": [1]}, timeout=1)
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)

    @allure.title("充电口盖关闭失败_Normal&Pending_进入Pending后计时内满足Status.sts=2_触发ChargeLidWarnSts.warnsts=[1]后无告警") 
    @pytest.mark.full
    def test_caseid_1988803(self):
        hint = "ChargeLidCloseFailed"
        self.set_ChargeLidCloseFailed()
        self.ipdu.set(self.ipdu.cem_lin2.CemCem_Lin2Fr06, 'ChrgLidManvgDCorAcDcReq2', 100) # 500ms后会回101, 进入Pending
        sleep(1.5) 
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr09, 'ChrgLidRearSts', 2) # Status.sts 
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetStatus", {}, {"out": 2}, timeout=0.5)
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcBlkFb', 1) 
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetWarnStatus", {}, {"out": [1]}, timeout=1)
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)        

    @allure.title("充电口盖关闭失败_Normal&Pending_进入Pending后计时内满足ChargeLidPos.pos=[0,10]_触发ChargeLidWarnSts.warnsts=[1,2]后无告警") 
    @pytest.mark.sanity
    def test_caseid_1988804(self):
        hint = "ChargeLidCloseFailed"
        self.set_ChargeLidCloseFailed()
        self.ipdu.set(self.ipdu.cem_lin2.CemCem_Lin2Fr06, 'ChrgLidManvgDCorAcDcReq2', 100) # 500ms后会回101, 进入Pending
        sleep(1) 
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcActPosn2', random.choice(list(range(11)))) # ChargeLidPos.pos
        sleep(0.5) 
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcBlkFb', 1) 
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcOverTrvlFb', 1) 
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetWarnStatus", {}, {"out": [1, 2]}, timeout=1)
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)       

    @allure.title("充电口盖关闭失败_Normal&Pending_进入Pending后计时内满足ChargeLidPos.pos=255_触发ChargeLidWarnSts.warnsts=[1]后无告警") 
    @pytest.mark.full
    def test_caseid_1988805(self):
        hint = "ChargeLidCloseFailed"
        self.set_ChargeLidCloseFailed()
        self.ipdu.set(self.ipdu.cem_lin2.CemCem_Lin2Fr06, 'ChrgLidManvgDCorAcDcReq2', 100) # 500ms后会回101, 进入Pending
        sleep(1) 
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcActPosn2', 101) # ChargeLidPos.pos=255
        sleep(0.5) 
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcBlkFb', 1) 
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetWarnStatus", {}, {"out": [1]}, timeout=1)
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)       
        
    @allure.title("充电口盖关闭失败_Normal&Pending_进入Pending后计时内满足ChargingInfo.info.isConnect=True_触发ChargeLidWarnSts.warnsts=[1]后无告警") 
    @pytest.mark.sanity
    def test_caseid_1989020(self):
        hint = "ChargeLidCloseFailed"
        self.set_ChargeLidCloseFailed()
        self.ipdu.set(self.ipdu.cem_lin2.CemCem_Lin2Fr06, 'ChrgLidManvgDCorAcDcReq2', 100) # 500ms后会回101, 进入Pending
        sleep(0.1) 
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 1) # isConnect 从0跳1
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"isConnect": True}})
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcBlkFb', 1) 
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetWarnStatus", {}, {"out": [1]}, timeout=1)
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)   
        
    @allure.title("充电口盖关闭失败_Normal_先满足ChargingInfo.info.isConnect=True_再使得ChrgLidManvgDCorAcDcReq2=100_触发ChargeLidWarnSts.warnsts=[1]后无告警") 
    @pytest.mark.sanity
    def test_caseid_1989021(self):
        hint = "ChargeLidCloseFailed"
        self.set_ChargeLidCloseFailed()
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 1) # isConnect 从0跳1
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"isConnect": True}})
        self.ipdu.set(self.ipdu.cem_lin2.CemCem_Lin2Fr06, 'ChrgLidManvgDCorAcDcReq2', 100) # 500ms后会回101, 进入Pending
        sleep(0.3)         
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcBlkFb', 1) 
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetWarnStatus", {}, {"out": [1]}, timeout=1)
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)   

    @allure.title("充电口盖关闭失败_Normal_先满足ChrgLidManvgDCorAcDcReq2=100_再使得ChargingInfo.info.isConnect从True变为False_触发ChargeLidWarnSts.warnsts=[1]后无告警") 
    @pytest.mark.full
    def test_caseid_1989126(self):
        hint = "ChargeLidCloseFailed"
        self.set_ChargeLidCloseFailed()
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 1) # isConnect 从0跳1
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"isConnect": True}})
        self.ipdu.set(self.ipdu.cem_lin2.CemCem_Lin2Fr06, 'ChrgLidManvgDCorAcDcReq2', 100) # 500ms后会回101, 进入Pending
        sleep(0.3)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0) # isConnect 从0跳1
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"isConnect": False}})         
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcBlkFb', 1) 
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetWarnStatus", {}, {"out": [1]}, timeout=1)
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)   
    
    @allure.title("充电口盖关闭失败_Normal_先满足ChargeLidPos.pos的退出条件_再使得ChrgLidManvgDCorAcDcReq2=100_触发ChargeLidWarnSts.warnsts=[1,2]后无告警") 
    @pytest.mark.smoke
    def test_caseid_1988806(self):
        hint = "ChargeLidCloseFailed"       
        self.set_ChargeLidCloseFailed(pos=101)
        self.ipdu.set(self.ipdu.cem_lin2.CemCem_Lin2Fr06, 'ChrgLidManvgDCorAcDcReq2', 100)
        sleep(0.3) 
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcBlkFb', 1) 
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcOverTrvlFb', 1) 
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetWarnStatus", {}, {"out": [1, 2]}, timeout=1)
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)   

    @allure.title("充电口盖关闭失败_Pending&Warning_先满足触发条件_再使得ChrgLidManvgDCorAcDcReq2=100_无告警") 
    @pytest.mark.sanity
    def test_caseid_1988807(self): 
        hint = "ChargeLidCloseFailed"       
        self.set_ChargeLidCloseFailed(warnsts=[1, 0]) # # ChargeLidWarnSts.warnsts=[1]
        self.ipdu.set(self.ipdu.cem_lin2.CemCem_Lin2Fr06, 'ChrgLidManvgDCorAcDcReq2', 100) # 进入Pending后，才监听ChargeLidWarnSts.warnsts
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)   
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcOverTrvlFb', 1) # ChargeLidWarnSts.warnsts=[1，2]
        self.partner.ck_wti_warning_and_resp(hint, 1)   

    @allure.title("充电口盖关闭失败_Pending_ChrgLidManvgDCorAcDcReq2=100后2.5s内再变为其他值_满足触发条件后告警") 
    @pytest.mark.full
    def test_caseid_1988808(self): # 实车无该场景
        hint = "ChargeLidCloseFailed"       
        self.set_ChargeLidCloseFailed()
        self.ipdu.set(self.ipdu.cem_lin2.CemCem_Lin2Fr06, 'ChrgLidManvgDCorAcDcReq2', 100) # 此时进入pending
        sleep(1.5) 
        self.ipdu.set(self.ipdu.cem_lin2.CemCem_Lin2Fr06, 'ChrgLidManvgDCorAcDcReq2', 0) # 不是退出条件
        sleep(0.2) 
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcBlkFb', 1)
        self.partner.ck_wti_warning_and_resp(hint, 1)

    @allure.title("充电口盖关闭失败_Pending_2.5s内多次触发ChrgLidManvgDCorAcDcReq2=100_从第一次满足时开启计时") 
    @pytest.mark.full
    def test_caseid_1988809(self): # 实车无该场景
        hint = "ChargeLidCloseFailed"       
        self.set_ChargeLidCloseFailed(warnsts=[1, 0])
        for req2 in [100, 0, 50, 100, 6]:
            self.ipdu.set(self.ipdu.cem_lin2.CemCem_Lin2Fr06, 'ChrgLidManvgDCorAcDcReq2', req2) # 第一次100时进入pending
            sleep(0.4)  
        sleep(0.6)
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcOverTrvlFb', 1)# 【Timer超时，所以无告警】
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0, timeout=2)             

    @allure.title("充电口盖关闭失败_Pending&Warning_进入Pending后计时器未超时_触发ChargeLidWarnSts.warnsts=[2]/[0]后无告警") 
    @pytest.mark.full
    def test_caseid_1988810(self):
        hint = "ChargeLidCloseFailed"       
        self.set_ChargeLidCloseFailed()
        self.ipdu.set(self.ipdu.cem_lin2.CemCem_Lin2Fr06, 'ChrgLidManvgDCorAcDcReq2', 100)
        sleep(0.3) 
        for sig, warnsts in {1:2, 0:0}.items():
            self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcOverTrvlFb', sig) 
            self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetWarnStatus", {}, {"out": [warnsts]}, timeout=1)
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)   

    @allure.title("充电口盖关闭失败_Pending&Warning_进入Pending后计时器未超时_触发ChargeLidWarnSts.warnsts=[1]/[1,2]后告警") 
    @pytest.mark.sanity
    def test_caseid_1988811(self): # ChrgLidManvgDCorAcDcReq2:|EventChargeLidStatus|EventChargeLidWarnStsCallback|updateMsg name:ChargeLidCloseFailed,info|EventChargeLidPosCallback,pos|mChargeLidSmSts,change from
        hint = "ChargeLidCloseFailed"       
        self.set_ChargeLidCloseFailed()
        for sig, warnsts in {0:[1], 1:[1, 2]}.items():
            self.ipdu.set(self.ipdu.cem_lin2.CemCem_Lin2Fr06, 'ChrgLidManvgDCorAcDcReq2', 100)
            sleep(1.5) # 500ms后会回101
            self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcOverTrvlFb', sig) 
            sleep(0.1)
            self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcBlkFb', 1) 
            self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetWarnStatus", {}, {"out": warnsts}, timeout=1)
            if sig == 0:
                self.partner.ck_wti_warning_and_resp(hint, 1)
            else:
                self.partner.ck_wti_no_warning_and_ck_resp(hint, 1, timeout=2)   

    @allure.title("充电口盖关闭失败_Warning_进入Warning后不满足ChargeLidWarnSts.warnsts中包含1_保持告警") 
    @pytest.mark.sanity
    def test_caseid_1988812(self):
        hint = "ChargeLidCloseFailed"       
        self.set_ChargeLidCloseFailed()
        self.ipdu.set(self.ipdu.cem_lin2.CemCem_Lin2Fr06, 'ChrgLidManvgDCorAcDcReq2', 100)
        sleep(1.5)
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcBlkFb', 1) # ChargeLidWarnSts.warnsts=[1]
        self.partner.ck_wti_warning_and_resp(hint, 1)
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcBlkFb', 0) # ChargeLidWarnSts.warnsts=[0]
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 1)   

    @allure.title("充电口盖关闭失败_Warning_进入Warning后不满足ChrgLidManvgDCorAcDcReq2=100_保持告警") 
    @pytest.mark.full
    def test_caseid_1988813(self):
        hint = "ChargeLidCloseFailed"       
        self.set_ChargeLidCloseFailed()
        self.ipdu.set(self.ipdu.cem_lin2.CemCem_Lin2Fr06, 'ChrgLidManvgDCorAcDcReq2', 100)
        sleep(1.5)
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcBlkFb', 1) # ChargeLidWarnSts.warnsts=[1]
        self.partner.ck_wti_warning_and_resp(hint, 1)
        self.ipdu.set(self.ipdu.cem_lin2.CemCem_Lin2Fr06, 'ChrgLidManvgDCorAcDcReq2', random.choice(list(range(100))))
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 1)   

    @allure.title("充电口盖关闭失败_Warning&Normal_进入Warning后满足Status.sts=2_退出告警") 
    @pytest.mark.smoke
    def test_caseid_1988815(self):
        hint = "ChargeLidCloseFailed"       
        self.set_ChargeLidCloseFailed()
        self.ipdu.set(self.ipdu.cem_lin2.CemCem_Lin2Fr06, 'ChrgLidManvgDCorAcDcReq2', 100)
        sleep(1.5)
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcBlkFb', 1)
        self.partner.ck_wti_warning_and_resp(hint, 1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr09, 'ChrgLidRearSts', 2) # Status.sts=2
        self.partner.ck_wti_warning_and_resp(hint, 0)
        
    @allure.title("充电口盖关闭失败_Warning&Normal_进入Warning后满足ChargeLidPos.pos=[0,10]_退出告警") 
    @pytest.mark.full
    def test_caseid_1988817(self):
        hint = "ChargeLidCloseFailed"       
        self.set_ChargeLidCloseFailed()
        self.ipdu.set(self.ipdu.cem_lin2.CemCem_Lin2Fr06, 'ChrgLidManvgDCorAcDcReq2', 100)
        sleep(1.5)
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcBlkFb', 1)
        self.partner.ck_wti_warning_and_resp(hint, 1)
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcActPosn2', random.choice(list(range(11)))) # ChargeLidPos.pos
        self.partner.ck_wti_warning_and_resp(hint, 0)
    
    @allure.title("充电口盖关闭失败_Warning&Normal_进入Warning后满足ChargeLidPos.pos=255_退出告警") 
    @pytest.mark.full
    def test_caseid_1988818(self):
        hint = "ChargeLidCloseFailed"       
        self.set_ChargeLidCloseFailed()
        self.ipdu.set(self.ipdu.cem_lin2.CemCem_Lin2Fr06, 'ChrgLidManvgDCorAcDcReq2', 100)
        sleep(2)
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcBlkFb', 1)
        self.partner.ck_wti_warning_and_resp(hint, 1)
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcActPosn2', random.choice([101, 255])) # ChargeLidPos.pos
        self.partner.ck_wti_warning_and_resp(hint, 0)

    @allure.title("充电口盖关闭失败_Warning&Normal_进入Warning后满足ChargingInfo.info.isConnect=True_退出告警") 
    @pytest.mark.smoke
    def test_caseid_1989022(self):
        hint = "ChargeLidCloseFailed"       
        self.set_ChargeLidCloseFailed()
        self.ipdu.set(self.ipdu.cem_lin2.CemCem_Lin2Fr06, 'ChrgLidManvgDCorAcDcReq2', 100)
        sleep(2)
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcBlkFb', 1)
        self.partner.ck_wti_warning_and_resp(hint, 1)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 1) 
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"isConnect": True}})
        self.partner.ck_wti_warning_and_resp(hint, 0)
        
    @allure.title("充电口盖关闭失败_重启场景_Warning后重启") 
    @pytest.mark.full
    def test_caseid_1988820(self):
        hint = "ChargeLidCloseFailed"       
        self.set_ChargeLidCloseFailed()
        self.ipdu.set(self.ipdu.cem_lin2.CemCem_Lin2Fr06, 'ChrgLidManvgDCorAcDcReq2', 100)
        sleep(2)
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcBlkFb', 1)
        self.partner.ck_wti_warning_and_resp(hint, 1)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT, resume_all_bus=False)
        sleep(5)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": "ChargeLidCloseFailed", "info": '0'}]}, timeout=3)
        self.ipdu.resume_all_bus_send()
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": "ChargeLidCloseFailed", "info": '0'}]}, timeout=3)

@allure.feature("SOA服务接口")
@allure.story("WTI通知/WTIService_other")
@pytest.mark.ypp
@pytest.mark.mock_tcp
class TestWTIServiceMockTcp(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu, tcp_down_mcu_ip="172.16.5.21",udp_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass([WTI_SERVICE_CLIENT])
        self.partner.wait_for_service_reconnect(WTI_SERVICE_CLIENT)
    
    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
    
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.partner.empty_all()
    
    def set_usage_mode(self, mode):
        """通过模拟mcu cdd打包总线数据来输入usage mode给到S2S"""
        logger.info(f"设置usage mode: {mode}")
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', mode)
    
    def ck_lvRelaySts_and_getLVRelaySts(self, ck_dict,timeout=1):
        """校验指定lvRelaySts事件，并请求getLVRelaySts"""
        self.partner.ck_s2s_event(VEHICLEMODESERVICE_CLIENT, "lvRelaySts", {"sts": ck_dict})
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "getLVRelaySts", {}, {"out": ck_dict})
    
    @allure.title("尾翼报警信息(MsgCarTailWarning)")
    @pytest.mark.smoke
    def test_caseid_107493(self):
        for usage_mode in [2, 11, 13]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', usage_mode) 
            logger.info(f"打印模式{usage_mode}")
            self.partner.empty_all(0.5)
            for NotAvlEve in [3, 4, 5, 6, 7, 0]:
                logger.info(f"打印信号{NotAvlEve}")
                self.bgm_eth_inter.set_signal("ActvReSplrStsNotAvlEve", NotAvlEve, send_pdu_immediately=True)
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                            {'list': [{'name': 'Car Tail Failure', 'info': NotAvlEve}]})
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                        {"out": [{'name': 'Car Tail Failure', 'info': NotAvlEve}]}) 
    

@allure.feature("SOA服务接口")
@allure.story("WTI通知/WTIService")
@pytest.mark.yang
class TestWTILampReqService(TestBase):

    def before_class(self, ecu):
        super().before_class(self, ecu)
        write_s2s_json({})
        change_bgm_config(bgm_inter_enable=True, s2s_path=s2s_path, nucapp=self.nucapp)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([("InterCommService", "client", "BGM_InterCommService", ),
                                     ("WTIService", "client")])
        # self.sd_tester.tester_present()
        # 放在before case

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        try:
            self.partner.stop_operators()
        except Exception as e :
            pass
        finally:
            recover_bgm_config()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()
        if ecu.get("testresult") == "Pass":
            try:
                os.system(f'rm {self.pcap_path}')
            except Exception as e:
                logger.info(e)
        super().after_each_func(ecu, start=False)
    
    def ck_no_specific_event_and_GetTelltaleList(self, hint, state, timeout=1):
        """校验无指定warningMsgList事件,并请求WarningMsgList获取结果"""
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "TelltaleList", hint, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                              {"out": [{"name": hint, "state": str(state)}]})

    def ck_TelltaleList_and_GetTelltaleList(self, hint, state, timeout=3):
        """校验指定TelltaleList事件，并请求TelltaleList获取结果"""
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList",
                                  {"list": [{"name": hint, "state": str(state)}]}, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                              {"out": [{"name": hint, "state": str(state)}]})

    @allure.title("安全气囊报警灯(TelltaleAirbag_flag2=1(信号丢失)--信号RestrntSysLampReq!==2|3恢复)")
    @pytest.mark.full
    def test_caseid_1979658(self):
        hint = "Airbag"
        self.partner.send_method_request(INTERCOMM_SERVICE_CLIENT, 'SetDiagnosticConnectStatus',
                                         {"connectActive": 0, 'connectStatus': 0})  # flag1==1
        self.sd_tester.change_usage_mode(0)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 0)
        for usage_mode in [2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            logger.info(f"打印{usage_mode}")
            self.ipdu.pause_bus_send("backbonefr")
            sleep(1.7)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.partner.send_method_request(INTERCOMM_SERVICE_CLIENT, 'SetDiagnosticConnectStatus',
                                                {"connectActive": 1, 'connectStatus': 1})#flag1==1
            sleep(8)#flag1==0
            self.ck_TelltaleList_and_GetTelltaleList(hint, 1)
            self.ipdu.resume_bus_send("backbonefr")
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 0)
            self.ck_TelltaleList_and_GetTelltaleList(hint, 0)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 1)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                                  {"out": [{"name": "Airbag", "state": "0"}]})

    @allure.title("安全气囊报警灯TelltaleAirbag_Warning pending(flag1==1)--flag2==0&&RestrntSysLampReq!2|3__不报警)V1.3")
    @pytest.mark.full
    def test_caseid_1979669(self):
        hint = "Airbag"
        self.sd_tester.change_usage_mode(0)  # 先设置UsageMode为:1
        for usage_mode in [2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 2)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 3)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            sleep(8)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 0)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 1)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)

    @allure.title("安全气囊报警灯TelltaleAirbag_flag2=1(信号丢失)--Normal(模式不满足)不报警)V1.3")
    @pytest.mark.full
    def test_caseid_1979670(self):
        hint = "Airbag"
        self.sd_tester.change_usage_mode(0)  # 先设置UsageMode为:1
        for usage_mode in [2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            self.ipdu.pause_bus_send("backbonefr")
            sleep(1.7)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.sd_tester.change_usage_mode(0)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.sd_tester.change_usage_mode(1)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.ipdu.resume_bus_send("backbonefr")

    @allure.title("安全气囊报警灯TelltaleAirbag_Warning pending(flag1==1)--flag2==0&&RestrntSysLampReq!2|3__不报警)V1.3")
    @pytest.mark.full
    def test_caseid_1979671(self):
        hint = "Airbag"
        self.sd_tester.change_usage_mode(0)  # 先设置UsageMode为:1
        for usage_mode in [2, 11, 13]:
            self.sd_tester.change_usage_mode(usage_mode)
            self.ipdu.pause_bus_send("backbonefr")
            sleep(1.7)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.ipdu.resume_bus_send("backbonefr")
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 0)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 1)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)

    @allure.title("安全气囊报警灯TelltaleAirbag_flag2=0&2|11|13(故障待确认)--信号变化为0|1--再变成3(故障确认)--模式不满足(恢复)V1.3")
    @pytest.mark.full
    def test_caseid_1979696(self):
        hint = "Airbag"
        self.partner.send_method_request(INTERCOMM_SERVICE_CLIENT, 'SetDiagnosticConnectStatus',
                                         {"connectActive": 0, 'connectStatus': 0})  # flag1==0
        self.sd_tester.change_usage_mode(0)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 0)
        for usage_mode in [2]:
            self.sd_tester.change_usage_mode(usage_mode)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 2)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 3)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr02, 'RestrntSysLampReq', 0)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.partner.send_method_request(INTERCOMM_SERVICE_CLIENT, 'SetDiagnosticConnectStatus',
                                             {"connectActive": 1, 'connectStatus': 1})  # flag1==0
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
            self.ipdu.pause_bus_send("backbonefr")
            self.partner.ck_wti_coming_telltale_and_resp(hint, "1", timeout=5, deviation=0.5)
            self.sd_tester.change_usage_mode(0)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.sd_tester.change_usage_mode(1)
            self.partner.ck_no_event(WTI_SERVICE_CLIENT, hint)
            self.ipdu.resume_bus_send("backbonefr")                            
        
    
    