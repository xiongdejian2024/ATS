#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_WTIService_Tpms.py
@Time         :2023/04/08 17:20:31
@Author       :jiabin.zhu@jiduauto.com
@Description  :
"""
import random
import allure
import pytest
from time import sleep
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_cases.legacy.soa.interface.VehicleControl.test_TyreService import MockMcuCddTyre


@allure.feature("SOA服务接口")
@allure.story("WTI通知/WTIService_Tpms")
@pytest.mark.wjj
class TestTpmsWTIService(TestBase):

    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21")
        self.mockmcu = MockMcuCddTyre(self.ipdu)
        self.partner = S2sBaseClass([WTI_SERVICE_CLIENT])
        self.partner.wait_for_service_reconnect(WTI_SERVICE_CLIENT)

    def after_class(self, ecu):
        try:
            self.partner.stop_operators()
        except Exception as e:
            logger.error(f"{str(e)}")
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        for i in range(4):
            self.mockmcu.set_temperature(i, 25)
            self.mockmcu.set_pressure(i, 260.0)
            self.mockmcu.set_PWarnFlg(i, 0)
            self.mockmcu.set_TWarnFlg(i, 0)
            self.mockmcu.set_FastLoseWarnFlg(i, 0)
            self.mockmcu.set_MsgOldFlg(i, 0)
            self.mockmcu.set_SysWarnFlg(i, 0)
            self.mockmcu.set_BattLoSt(i, 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecLeBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecMidBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecRiBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'DispMsgByVehHld', 0)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0)
        self.partner.empty_all(0.5)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def set_usage_mode(self, mode):
        """通过模拟mcu cdd打包总线数据来输入usage mode给到S2S"""
        logger.info(f"设置usage mode: {mode}")
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', mode)

    def ck_warningmsg(self, hint, last_info, new_info):
        """
        校验WTI提示信息
        @param hint: WTI提示信息
        @param last_info: 老的WTI提示信息状态
        @param new_info: 新的WTI提示信息状态
        """
        if last_info != new_info:
            self.partner.ck_wti_warning_and_resp(hint, new_info,timeout=3)
        else:
            self.partner.ck_wti_no_warning_and_ck_resp(hint, new_info)
            
    def ck_noWarningMsgList_and_GetWarningMsgList(self, name1, info1, name2, info2):
        """
        校验WTI提示信息无event
        """
        self.partner.ck_no_event(WTI_SERVICE_CLIENT, "WarningMsgList")
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": name1, "info": info1},{"name": name2, "info": info2}]})  
        
    def ck_WarningMsgList_and_TwoGetWarningMsgList(self, name1, info1, name2, info2):
        """
        校验WTI提示信息Get中获取校验两个值
        """
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": name1, "info": info1}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": name1, "info": info1},{"name": name2, "info": info2}]})       
    

    @allure.title("左前轮胎胎压低一级警告信息(MsgTireFLPressureLowLevel1)_告警产生恢复")
    @pytest.mark.smoke
    def test_caseid_109017(self):
        hint = "Front Left Tire Pressure Low Level 1"
        last_info = 0
        for usage_mode in [0, 1, 2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.partner.empty_all(0.5)
            for PWarnFlag in [1, 2, 3, 0] + [random.randint(0, 3) for _ in range(5)]:
                self.mockmcu.set_PWarnFlg(0, PWarnFlag)
                new_info = 1 if PWarnFlag == 1 else 0
                self.ck_warningmsg(hint, last_info, new_info)
                last_info = new_info

    @allure.title("左前轮胎胎压警告信息优先级_设二级设一级取消一级取消二级")
    @pytest.mark.full
    def test_caseid_1984981(self):
        hint1 = "Front Left Tire Pressure Low Level 1"
        hint2 = "Front Left Tire Pressure Low Level 2"
        self.mockmcu.set_pressure(0, 100)
        self.ck_WarningMsgList_and_TwoGetWarningMsgList(hint2, 1, hint1, 0)
        self.mockmcu.set_PWarnFlg(0, 1)
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint2, "info": 1},{"name": hint1, "info": 0}]})
        self.mockmcu.set_PWarnFlg(0, 0)
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint2, "info": 1},{"name": hint1, "info": 0}]})
        self.mockmcu.set_pressure(0, 140)
        self.ck_WarningMsgList_and_TwoGetWarningMsgList(hint2, 0, hint1, 0)
        
    @allure.title("左前轮胎胎压警告信息优先级_设二级设一级取消二级")
    @pytest.mark.full
    def test_caseid_1984977(self):
        hint1 = "Front Left Tire Pressure Low Level 1"
        hint2 = "Front Left Tire Pressure Low Level 2"
        self.mockmcu.set_pressure(0, 100)
        self.ck_WarningMsgList_and_TwoGetWarningMsgList(hint2, 1, hint1, 0)
        self.mockmcu.set_PWarnFlg(0, 1)
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint2, "info": 1},{"name": hint1, "info": 0}]})
        self.mockmcu.set_pressure(0, 140)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint2, "info": 0},{"name": hint1, "info": 1}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint2, "info": 0},{"name": hint1, "info": 1}]}) 
        
    @allure.title("左前轮胎胎压警告信息优先级_设一级设二级取消一级取消二级")
    @pytest.mark.full
    def test_caseid_1984969(self):
        hint1 = "Front Left Tire Pressure Low Level 1"
        hint2 = "Front Left Tire Pressure Low Level 2"
        self.mockmcu.set_PWarnFlg(0, 1)
        self.ck_WarningMsgList_and_TwoGetWarningMsgList(hint1, 1, hint2, 0)
        self.mockmcu.set_pressure(0, 100)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint1, "info": 0},{"name": hint2, "info": 1}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint1, "info": '0'},{"name": hint2, "info": '1'}]})
        self.mockmcu.set_PWarnFlg(0, 0)
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint2, "info": 1},{"name": hint1, "info": 0}]})
        self.mockmcu.set_pressure(0, 140)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint2, "info": 0}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint2, "info": '0'},{"name": hint1, "info": '0'}]})
        
    @allure.title("左前轮胎胎压低一级警告信息(MsgTireFLPressureLowLevel1)_BGM重启后上报")
    @pytest.mark.full
    def test_caseid_109007(self):
        hint = "Front Left Tire Pressure Low Level 1"
        self.set_usage_mode(2)
        self.mockmcu.set_PWarnFlg(0, 1)
        self.partner.ck_wti_warning_and_resp(hint, 1)
        self.partner.ck_wti_telltale_and_resp("Tire Pressure", 1)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
        # todo： 待yuhui优化partner，注册回调函数直接设置要发默认值，之后就可以check warning，timeout设5s，防止下面SSIG没拿到数据
        # 重启后WTIService重连上，但WTIService还没有和VMM连上，或者还没有从SSIG拿到总线信号，所以不会立即上报
        # 另外可能WTI启动后已经发了event，但是partner还没连上，就获取不到event
        sleep(10)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": '1'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                              {"out": [{"name": "Tire Pressure", "state": '1'}]})
        
    @allure.title("左前后轮胎胎压警告信息优先级_告警产生恢复")
    @pytest.mark.full
    def test_caseid_1984935(self):
        hint1 = "Front Left Tire Pressure Low Level 1"
        hint2 = "Front Left Tire Pressure Low Level 2"
        for usage_mode in [0, 1, 2, 11, 13]:
            logger.info({f'usgmode现在是{usage_mode}'})
            self.set_usage_mode(usage_mode)
            self.mockmcu.set_PWarnFlg(0, 1)
            if usage_mode != 0:
                self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint2)
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint2, "info": 1},{"name": hint1, "info": 0}]})
            else:
                self.ck_WarningMsgList_and_TwoGetWarningMsgList(hint1, '1', hint2, '0')
            self.mockmcu.set_pressure(0, 89)
            if usage_mode != 0:
               self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint2)
               self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint2, "info": 1},{"name": hint1, "info": 0}]})
            else:
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint1, "info": '0'},{"name": hint2, "info": '1'}]})
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint1, "info": '0'},{"name": hint2, "info": '1'}]}) 

    @allure.title("左前轮胎胎压警告信息优先级_BGM重启后上报")
    @pytest.mark.full
    def test_caseid_1984961(self):
        hint1 = "Front Left Tire Pressure Low Level 1"
        hint2 = "Front Left Tire Pressure Low Level 2"
        self.mockmcu.set_PWarnFlg(0, 1)
        self.ck_WarningMsgList_and_TwoGetWarningMsgList(hint1, 1, hint2, 0)
        self.mockmcu.set_pressure(0, 100)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint1, "info": '0'},{"name": hint2, "info": '1'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint1, "info": '0'},{"name": hint2, "info": '1'}]})
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
        sleep(10)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint1, "info": '0'},{"name": hint2, "info": '1'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint1, "info": '0'},{"name": hint2, "info": '1'}]})
        
    @allure.title("右前轮胎胎压低一级警告信息(MsgTireFRPressureLowLevel1)_告警产生恢复")
    @pytest.mark.full
    def test_caseid_109012(self):
        hint = "Front Right Tire Pressure Low Level 1"
        last_info = 0
        for usage_mode in [0, 1, 2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.partner.empty_all(0.5)
            for PWarnFlag in [1, 2, 3, 0] + [random.randint(0, 3) for _ in range(5)]:
                self.mockmcu.set_PWarnFlg(1, PWarnFlag)
                new_info = 1 if PWarnFlag == 1 else 0
                self.ck_warningmsg(hint, last_info, new_info)
                last_info = new_info
                
    @allure.title("右前轮胎胎压警告信息优先级_设二级设一级取消一级取消二级")
    @pytest.mark.full
    def test_caseid_1984980(self):
        hint1 = "Front Right Tire Pressure Low Level 1"
        hint2 = "Front Right Tire Pressure Low Level 2"
        self.mockmcu.set_pressure(1, 100)
        self.ck_WarningMsgList_and_TwoGetWarningMsgList(hint2, 1, hint1, 0)
        self.mockmcu.set_PWarnFlg(1, 1)
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint2, "info": 1},{"name": hint1, "info": 0}]})
        self.mockmcu.set_PWarnFlg(1, 0)
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint2, "info": 1},{"name": hint1, "info": 0}]})
        self.mockmcu.set_pressure(1, 140)
        self.ck_WarningMsgList_and_TwoGetWarningMsgList(hint2, 0, hint1, 0)
        
    @allure.title("右前轮胎胎压警告信息优先级_设二级设一级取消二级")
    @pytest.mark.full
    def test_caseid_1984976(self):
        hint1 = "Front Right Tire Pressure Low Level 1"
        hint2 = "Front Right Tire Pressure Low Level 2"
        self.mockmcu.set_pressure(1, 100)
        self.ck_WarningMsgList_and_TwoGetWarningMsgList(hint2, 1, hint1, 0)
        self.mockmcu.set_PWarnFlg(1, 1)
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint2, "info": 1},{"name": hint1, "info": 0}]})
        self.mockmcu.set_pressure(1, 140)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint2, "info": 0},{"name": hint1, "info": 1}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint2, "info": 0},{"name": hint1, "info": 1}]}) 
        
    @allure.title("右前轮胎胎压警告信息优先级_设一级设二级取消一级取消二级")
    @pytest.mark.full
    def test_caseid_1984971(self):
        hint1 = "Front Right Tire Pressure Low Level 1"
        hint2 = "Front Right Tire Pressure Low Level 2"
        self.mockmcu.set_PWarnFlg(1, 1)
        self.ck_WarningMsgList_and_TwoGetWarningMsgList(hint1, 1, hint2, 0)
        self.mockmcu.set_pressure(1, 100)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint1, "info": 0},{"name": hint2, "info": 1}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint1, "info": '0'},{"name": hint2, "info": '1'}]})
        self.mockmcu.set_PWarnFlg(1, 0)
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint2, "info": 1},{"name": hint1, "info": 0}]})
        self.mockmcu.set_pressure(1, 140)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint2, "info": 0}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint2, "info": '0'},{"name": hint1, "info": '0'}]}) 

    @allure.title("右前轮胎胎压低一级警告信息(MsgTireFRPressureLowLevel1)_BGM重启后上报")
    @pytest.mark.full
    def test_caseid_108985(self):
        hint = "Front Right Tire Pressure Low Level 1"
        self.mockmcu.set_PWarnFlg(1, 1)
        self.set_usage_mode(13)
        self.partner.ck_wti_warning_and_resp(hint, 1)
        self.partner.ck_wti_telltale_and_resp("Tire Pressure", 1)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
        sleep(10)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": '1'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                              {"out": [{"name": "Tire Pressure", "state": '1'}]})
        
    @allure.title("右前后轮胎胎压警告信息优先级_告警产生恢复")
    @pytest.mark.full
    def test_caseid_1984945(self):
        hint1 = "Front Right Tire Pressure Low Level 1"
        hint2 = "Front Right Tire Pressure Low Level 2"
        for usage_mode in [0, 1, 2, 11, 13]:
            logger.info({f'usgmode现在是{usage_mode}'})
            self.set_usage_mode(usage_mode)
            self.mockmcu.set_PWarnFlg(1, 1)
            if usage_mode != 0:
                self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint2)
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint2, "info": 1},{"name": hint1, "info": 0}]})
            else:
                self.ck_WarningMsgList_and_TwoGetWarningMsgList(hint1, '1', hint2, '0')
            self.mockmcu.set_pressure(1, 89)
            if usage_mode != 0:
               self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint2)
               self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint2, "info": 1},{"name": hint1, "info": 0}]})
            else:
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint1, "info": '0'},{"name": hint2, "info": '1'}]})
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint1, "info": '0'},{"name": hint2, "info": '1'}]}) 
        
    @allure.title("右前轮胎胎压警告信息优先级_BGM重启后上报")
    @pytest.mark.full
    def test_caseid_1984962(self):
        hint1 = "Front Right Tire Pressure Low Level 1"
        hint2 = "Front Right Tire Pressure Low Level 2"
        self.mockmcu.set_PWarnFlg(1, 1)
        self.ck_WarningMsgList_and_TwoGetWarningMsgList(hint1, 1, hint2, 0)
        self.mockmcu.set_pressure(1, 100)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint1, "info": 0},{"name": hint2, "info": 1}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint1, "info": '0'},{"name": hint2, "info": '1'}]})
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
        sleep(10)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint1, "info": "0"},{"name": hint2, "info": "1"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint1, "info": '0'},{"name": hint2, "info": '1'}]})

    @allure.title("左后轮胎胎压低一级警告信息(MsgTireRLPressureLowLevel1)_告警产生恢复")
    @pytest.mark.full
    def test_caseid_1959661(self):
        hint = "Rear Left Tire Pressure Low Level 1"
        last_info = 0
        for usage_mode in [0, 1, 2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.partner.empty_all(0.5)
            for PWarnFlag in [1, 2, 3, 0] + [random.randint(0, 3) for _ in range(5)]:
                self.mockmcu.set_PWarnFlg(2, PWarnFlag)
                new_info = 1 if PWarnFlag == 1 else 0
                self.ck_warningmsg(hint, last_info, new_info)
                last_info = new_info
                
    @allure.title("左后轮胎胎压警告信息优先级_设二级设一级取消一级取消二级")
    @pytest.mark.full
    def test_caseid_1984979(self):
        hint1 = "Rear Left Tire Pressure Low Level 1"
        hint2 = "Rear Left Tire Pressure Low Level 2"
        self.mockmcu.set_pressure(2, 100)
        self.ck_WarningMsgList_and_TwoGetWarningMsgList(hint2, 1, hint1, 0)
        self.mockmcu.set_PWarnFlg(2, 1)
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint2, "info": 1},{"name": hint1, "info": 0}]})
        self.mockmcu.set_PWarnFlg(2, 0)
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint2, "info": 1},{"name": hint1, "info": 0}]})
        self.mockmcu.set_pressure(2, 140)
        self.ck_WarningMsgList_and_TwoGetWarningMsgList(hint2, 0, hint1, 0)
        
    @allure.title("左后轮胎胎压警告信息优先级_设二级设一级取消二级")
    @pytest.mark.full
    def test_caseid_1984975(self):
        hint1 = "Rear Left Tire Pressure Low Level 1"
        hint2 = "Rear Left Tire Pressure Low Level 2"
        self.mockmcu.set_pressure(2, 100)
        self.ck_WarningMsgList_and_TwoGetWarningMsgList(hint2, 1, hint1, 0)
        self.mockmcu.set_PWarnFlg(2, 1)
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint2, "info": 1},{"name": hint1, "info": 0}]})
        self.mockmcu.set_pressure(2, 140)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint2, "info": 0},{"name": hint1, "info": 1}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint2, "info": 0},{"name": hint1, "info": 1}]})   
        
    @allure.title("左后轮胎胎压警告信息优先级_设一级设二级取消一级取消二级")
    @pytest.mark.full
    def test_caseid_1984972(self):
        hint1 = "Rear Left Tire Pressure Low Level 1"
        hint2 = "Rear Left Tire Pressure Low Level 2"
        self.mockmcu.set_PWarnFlg(2, 1)
        self.ck_WarningMsgList_and_TwoGetWarningMsgList(hint1, 1, hint2, 0)
        self.mockmcu.set_pressure(2, 100)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint1, "info": 0},{"name": hint2, "info": 1}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint1, "info": '0'},{"name": hint2, "info": '1'}]})
        self.mockmcu.set_PWarnFlg(2, 0)
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint2, "info": 1},{"name": hint1, "info": 0}]})
        self.mockmcu.set_pressure(2, 140)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint2, "info": 0}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint2, "info": '0'},{"name": hint1, "info": '0'}]})   

    @allure.title("左后轮胎胎压低一级警告信息(MsgTireRLPressureLowLevel1)_BGM重启后上报")
    @pytest.mark.sanity
    def test_caseid_109004(self):
        hint = "Rear Left Tire Pressure Low Level 1"
        self.set_usage_mode(2)
        self.mockmcu.set_PWarnFlg(2, 1)
        self.partner.ck_wti_warning_and_resp(hint, 1)
        self.partner.ck_wti_telltale_and_resp("Tire Pressure", 1)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
        sleep(10)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": '1'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                              {"out": [{"name": "Tire Pressure", "state": '1'}]})
        
    @allure.title("左后后轮胎胎压警告信息优先级_告警产生恢复")
    @pytest.mark.full
    def test_caseid_1984946(self):
        hint1 = "Rear Left Tire Pressure Low Level 1"
        hint2 = "Rear Left Tire Pressure Low Level 2"
        for usage_mode in [0, 1, 2, 11, 13]:
            logger.info({f'usgmode现在是{usage_mode}'})
            self.set_usage_mode(usage_mode)
            self.mockmcu.set_PWarnFlg(2, 1)
            if usage_mode != 0:
                self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint2)
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint2, "info": 1},{"name": hint1, "info": 0}]})
            else:
                self.ck_WarningMsgList_and_TwoGetWarningMsgList(hint1, '1', hint2, '0')
            self.mockmcu.set_pressure(2, 89)
            if usage_mode != 0:
               self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint2)
               self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint2, "info": 1},{"name": hint1, "info": 0}]})
            else:
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint1, "info": '0'},{"name": hint2, "info": '1'}]})
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint1, "info": '0'},{"name": hint2, "info": '1'}]}) 
        
    @allure.title("左后轮胎胎压警告信息优先级_BGM重启后上报")
    @pytest.mark.full
    def test_caseid_1984963(self):
        hint1 = "Rear Left Tire Pressure Low Level 1"
        hint2 = "Rear Left Tire Pressure Low Level 2"
        self.mockmcu.set_PWarnFlg(2, 1)
        self.ck_WarningMsgList_and_TwoGetWarningMsgList(hint1, '1', hint2, '0')
        self.mockmcu.set_pressure(2, 100)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint1, "info": '0'},{"name": hint2, "info": '1'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint1, "info": '0'},{"name": hint2, "info": '1'}]})
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
        sleep(5)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint1, "info": '0'},{"name": hint2, "info": '1'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint1, "info": '0'},{"name": hint2, "info": '1'}]})

    @allure.title("右后轮胎胎压低一级警告信息(MsgTireRRPressureLowLevel1)_告警产生恢复")
    @pytest.mark.full
    def test_caseid_109011(self):
        hint = "Rear Right Tire Pressure Low Level 1"
        last_info = 0
        for usage_mode in [0, 1, 2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.partner.empty_all(0.5)
            for PWarnFlag in [1, 2, 3, 0] + [random.randint(0, 3) for _ in range(5)]:
                self.mockmcu.set_PWarnFlg(3, PWarnFlag)
                new_info = 1 if PWarnFlag == 1 else 0
                self.ck_warningmsg(hint, last_info, new_info)
                last_info = new_info

    @allure.title("右后轮胎胎压警告信息优先级_设二级设一级取消一级取消二级")
    @pytest.mark.full
    def test_caseid_1984978(self):
        hint1 = "Rear Right Tire Pressure Low Level 1"
        hint2 = "Rear Right Tire Pressure Low Level 2"
        self.mockmcu.set_pressure(3, 100)
        self.ck_WarningMsgList_and_TwoGetWarningMsgList(hint2, 1, hint1, 0)
        self.mockmcu.set_PWarnFlg(3, 1)
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint2, "info": 1},{"name": hint1, "info": 0}]})
        self.mockmcu.set_PWarnFlg(3, 0)
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint2, "info": 1},{"name": hint1, "info": 0}]})
        self.mockmcu.set_pressure(3, 140)
        self.ck_WarningMsgList_and_TwoGetWarningMsgList(hint2, 0, hint1, 0)  
        
    @allure.title("右后轮胎胎压警告信息优先级_设二级设一级取消二级")
    @pytest.mark.full
    def test_caseid_1984974(self):
        hint1 = "Rear Right Tire Pressure Low Level 1"
        hint2 = "Rear Right Tire Pressure Low Level 2"
        self.mockmcu.set_pressure(3, 100)
        self.ck_WarningMsgList_and_TwoGetWarningMsgList(hint2, 1, hint1, 0)
        self.mockmcu.set_PWarnFlg(3, 1)
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint2, "info": 1},{"name": hint1, "info": 0}]})
        self.mockmcu.set_pressure(3, 140)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint2, "info": 0},{"name": hint1, "info": 1}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint2, "info": 0},{"name": hint1, "info": 1}]})
        
    @allure.title("右后轮胎胎压警告信息优先级_设一级设二级取消一级取消二级")
    @pytest.mark.full
    def test_caseid_1984973(self):
        hint1 = "Rear Right Tire Pressure Low Level 1"
        hint2 = "Rear Right Tire Pressure Low Level 2"
        self.mockmcu.set_PWarnFlg(3, 1)
        self.ck_WarningMsgList_and_TwoGetWarningMsgList(hint1, 1, hint2, 0)
        self.mockmcu.set_pressure(3, 100)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint1, "info": 0},{"name": hint2, "info": 1}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint1, "info": '0'},{"name": hint2, "info": '1'}]})
        self.mockmcu.set_PWarnFlg(3, 0)
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint2, "info": 1},{"name": hint1, "info": 0}]})
        self.mockmcu.set_pressure(3, 140)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint2, "info": 0}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint2, "info": '0'},{"name": hint1, "info": '0'}]})
        
    @allure.title("右后轮胎胎压警告信息优先级_告警产生恢复")
    @pytest.mark.full
    def test_caseid_1984959(self):
        hint1 = "Rear Right Tire Pressure Low Level 1"
        hint2 = "Rear Right Tire Pressure Low Level 2"
        for usage_mode in [0, 1, 2, 11, 13]:
            logger.info({f'usgmode现在是{usage_mode}'})
            self.set_usage_mode(usage_mode)
            self.mockmcu.set_PWarnFlg(3, 1)
            if usage_mode != 0:
                self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint2)
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint2, "info": 1},{"name": hint1, "info": 0}]})
            else:
                self.ck_WarningMsgList_and_TwoGetWarningMsgList(hint1, '1', hint2, '0')
            self.mockmcu.set_pressure(3, 89)
            if usage_mode != 0:
               self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", hint2)
               self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint2, "info": 1},{"name": hint1, "info": 0}]})
            else:
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint1, "info": '0'},{"name": hint2, "info": '1'}]})
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint1, "info": '0'},{"name": hint2, "info": '1'}]})   
        
    @allure.title("右后轮胎胎压低一级警告信息(MsgTireRRPressureLowLevel1)_BGM重启后上报")
    @pytest.mark.sanity
    def test_caseid_108995(self):
        hint = "Rear Right Tire Pressure Low Level 1"
        self.set_usage_mode(2)
        self.mockmcu.set_PWarnFlg(3, 1)
        self.partner.ck_wti_warning_and_resp(hint, 1)
        self.partner.ck_wti_telltale_and_resp("Tire Pressure", 1)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
        sleep(10)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": '1'}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {},
                                              {"out": [{"name": "Tire Pressure", "state": '1'}]})
        
    @allure.title("右后轮胎胎压警告信息优先级_BGM重启后上报")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1984960(self):
        hint1 = "Rear Right Tire Pressure Low Level 1"
        hint2 = "Rear Right Tire Pressure Low Level 2"
        self.mockmcu.set_PWarnFlg(3, 1)
        self.ck_WarningMsgList_and_TwoGetWarningMsgList(hint1, 1, hint2, 0)
        self.mockmcu.set_pressure(3, 100)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint1, "info": "0"},{"name": hint2, "info": "1"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint1, "info": '0'},{"name": hint2, "info": '1'}]})
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
        sleep(5)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint1, "info": "0"},{"name": hint2, "info": "1"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint1, "info": '0'},{"name": hint2, "info": '1'}]})
        
    @allure.title("左前轮胎胎压低二级警告信息(MsgTireFLPressureLowLevel2)_告警产生恢复")
    @pytest.mark.full
    def test_caseid_109002(self):
        hint = "Front Left Tire Pressure Low Level 2"
        for usage_mode in [0, 1, 2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.partner.empty_all(0.5)
            self.mockmcu.set_pressure(0, 138)
            self.partner.ck_wti_warning_and_resp(hint, 1)
            self.mockmcu.set_pressure(0, 140)
            self.partner.ck_wti_warning_and_resp(hint, 0)

    @allure.title("左前轮胎胎压低二级警告信息(MsgTireFLPressureLowLevel2)_BGM重启后上报")
    @pytest.mark.full
    def test_caseid_108996(self):
        hint = "Front Left Tire Pressure Low Level 2"
        self.mockmcu.set_pressure(0, 138)
        self.partner.ck_wti_warning_and_resp(hint, 1)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
        sleep(10)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": '1'}]})

    @allure.title("右前轮胎胎压低二级警告信息(MsgTireFRPressureLowLevel2)_告警产生恢复")
    @pytest.mark.smoke
    def test_caseid_109003(self):
        hint = "Front Right Tire Pressure Low Level 2"
        for usage_mode in [0, 1, 2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.partner.empty_all(0.5)
            self.mockmcu.set_pressure(1, 138)
            self.partner.ck_wti_warning_and_resp(hint, 1)
            self.mockmcu.set_pressure(1, 140)
            self.partner.ck_wti_warning_and_resp(hint, 0)

    @allure.title("右前轮胎胎压低二级警告信息(MsgTireFRPressureLowLevel2)_BGM重启后上报")
    @pytest.mark.sanity
    def test_caseid_108990(self):
        hint = "Front Right Tire Pressure Low Level 2"
        self.mockmcu.set_pressure(1, 138)
        self.partner.ck_wti_warning_and_resp(hint, 1)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
        sleep(10)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": '1'}]})

    @allure.title("左后轮胎胎压低二级警告信息(MsgTireRLPressureLowLevel2)_告警产生恢复")
    @pytest.mark.full
    def test_caseid_108992(self):
        hint = "Rear Left Tire Pressure Low Level 2"
        for usage_mode in [0, 1, 2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.partner.empty_all(0.5)
            self.mockmcu.set_pressure(2, 138)
            self.partner.ck_wti_warning_and_resp(hint, 1)
            self.mockmcu.set_pressure(2, 140)
            self.partner.ck_wti_warning_and_resp(hint, 0)

    @allure.title("左后轮胎胎压低二级警告信息(MsgTireRLPressureLowLevel2)_BGM重启后上报")
    @pytest.mark.sanity
    def test_caseid_109009(self):
        hint = "Rear Left Tire Pressure Low Level 2"
        self.mockmcu.set_pressure(2, 138)
        self.partner.ck_wti_warning_and_resp(hint, 1)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
        sleep(10)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": '1'}]},timeout=5)

    @allure.title("右后轮胎胎压低二级警告信息(MsgTireRRPressureLowLevel2)_告警产生恢复")
    @pytest.mark.full
    def test_caseid_108987(self):
        hint = "Rear Right Tire Pressure Low Level 2"
        for usage_mode in [0, 1, 2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.partner.empty_all(0.5)
            self.mockmcu.set_pressure(3, 138)
            self.partner.ck_wti_warning_and_resp(hint, 1)
            self.mockmcu.set_pressure(3, 140)
            self.partner.ck_wti_warning_and_resp(hint, 0)

    @allure.title("右后轮胎胎压低二级警告信息(MsgTireRRPressureLowLevel2)_BGM重启后上报")
    @pytest.mark.full
    def test_caseid_109005(self):
        hint = "Rear Right Tire Pressure Low Level 2"
        self.mockmcu.set_pressure(3, 138)
        self.partner.ck_wti_warning_and_resp(hint, 1)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
        sleep(10)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": '1'}]})

    @allure.title("左前轮胎温度高警告信息(MsgTireFLTempHigh)_告警产生恢复")
    @pytest.mark.full
    def test_caseid_109001(self):
        hint = "Front Left Tire Temperature High"
        last_info = 0
        for usage_mode in [0, 1, 2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.partner.empty_all(0.5)
            for TWarnFlag in [1, 0]:
                self.mockmcu.set_TWarnFlg(0, TWarnFlag)
                new_info = 1 if TWarnFlag == 1 else 0
                self.ck_warningmsg(hint, last_info, new_info)
                last_info = new_info

    @allure.title("右前轮胎温度高警告信息(MsgTireFRTempHigh)_告警产生恢复")
    @pytest.mark.full
    def test_caseid_108986(self):
        hint = "Front Right Tire Temperature High"
        last_info = 0
        for usage_mode in [0, 1, 2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.partner.empty_all(0.5)
            for TWarnFlag in [1, 0]:
                self.mockmcu.set_TWarnFlg(1, TWarnFlag)
                new_info = 1 if TWarnFlag == 1 else 0
                self.ck_warningmsg(hint, last_info, new_info)
                last_info = new_info

    @allure.title("左后轮胎温度高警告信息(MsgTireFLTempHigh)_告警产生恢复")
    @pytest.mark.full
    def test_caseid_108980(self):
        hint = "Rear Left Tire Temperature High"
        last_info = 0
        for usage_mode in [0, 1, 2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.partner.empty_all(0.5)
            for TWarnFlag in [1, 0]:
                self.mockmcu.set_TWarnFlg(2, TWarnFlag)
                new_info = 1 if TWarnFlag == 1 else 0
                self.ck_warningmsg(hint, last_info, new_info)
                last_info = new_info

    @allure.title("右后轮胎温度高警告信息(MsgTireFRTempHigh)_告警产生恢复")
    @pytest.mark.smoke
    def test_caseid_109008(self):
        hint = "Rear Right Tire Temperature High"
        last_info = 0
        for usage_mode in [0, 1, 2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.partner.empty_all(0.5)
            for TWarnFlag in [1, 0]:
                self.mockmcu.set_TWarnFlg(3, TWarnFlag)
                new_info = 1 if TWarnFlag == 1 else 0
                self.ck_warningmsg(hint, last_info, new_info)
                last_info = new_info

    @allure.title("左前轮胎温度高警告信息(MsgTireFLTempHigh)_BGM重启后上报")
    @pytest.mark.sanity
    def test_caseid_108991(self):
        hint = "Front Left Tire Temperature High"
        self.mockmcu.set_TWarnFlg(0, 1)
        self.partner.ck_wti_warning_and_resp(hint, 1)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
        sleep(10)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": '1'}]})

    @allure.title("右前轮胎温度高警告信息(MsgTireFRTempHigh)_BGM重启后上报")
    @pytest.mark.full
    def test_caseid_108999(self):
        hint = "Front Right Tire Temperature High"
        self.mockmcu.set_TWarnFlg(1, 1)
        self.partner.ck_wti_warning_and_resp(hint, 1)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
        sleep(10)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": '1'}]})

    @allure.title("左后轮胎温度高警告信息(MsgTireFLTempHigh)_BGM重启后上报")
    @pytest.mark.sanity
    def test_caseid_109000(self):
        hint = "Rear Left Tire Temperature High"
        self.mockmcu.set_TWarnFlg(2, 1)
        self.partner.ck_wti_warning_and_resp(hint, 1)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
        sleep(10)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": '1'}]})

    @allure.title("右后轮胎温度高警告信息(MsgTireFRTempHigh)_BGM重启后上报")
    @pytest.mark.full
    def test_caseid_108998(self):
        hint = "Rear Right Tire Temperature High"
        self.mockmcu.set_TWarnFlg(3, 1)
        self.partner.ck_wti_warning_and_resp(hint, 1)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
        sleep(10)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": '1'}]})

    @allure.title("左前轮胎传感器低电量警告信息(MsgTireFLSensorBattLow)_告警产生恢复")
    @pytest.mark.full
    def test_caseid_108982(self):
        hint = "Front Left Tire Sensor Batt Low"
        last_info = 0
        for usage_mode in [0, 1, 2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.partner.empty_all(0.5)
            for BattLoSt in [1, 0]:
                self.mockmcu.set_BattLoSt(0, BattLoSt)
                new_info = 1 if BattLoSt == 1 else 0
                self.ck_warningmsg(hint, last_info, new_info)
                last_info = new_info

    @allure.title("右前轮胎传感器低电量警告信息(MsgTireFRSensorBattLow)_告警产生恢复")
    @pytest.mark.sanity
    def test_caseid_108984(self):
        hint = "Front Right Tire Sensor Batt Low"
        last_info = 0
        for usage_mode in [0, 1, 2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.partner.empty_all(0.5)
            for BattLoSt in [1, 0]:
                self.mockmcu.set_BattLoSt(1, BattLoSt)
                new_info = 1 if BattLoSt == 1 else 0
                self.ck_warningmsg(hint, last_info, new_info)
                last_info = new_info

    @allure.title("左后轮胎传感器低电量警告信息(MsgTireRLSensorBattLow)_告警产生恢复")
    @pytest.mark.smoke
    def test_caseid_108988(self):
        hint = "Rear Left Tire Sensor Batt Low"
        last_info = 0
        for usage_mode in [0, 1, 2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.partner.empty_all(0.5)
            for BattLoSt in [1, 0]:
                self.mockmcu.set_BattLoSt(2, BattLoSt)
                new_info = 1 if BattLoSt == 1 else 0
                self.ck_warningmsg(hint, last_info, new_info)
                last_info = new_info

    @allure.title("右后轮胎传感器低电量警告信息(MsgTireRRSensorBattLow)_告警产生恢复")
    @pytest.mark.full
    def test_caseid_108994(self):
        hint = "Rear Right Tire Sensor Batt Low"
        last_info = 0
        for usage_mode in [0, 1, 2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.partner.empty_all(0.5)
            for BattLoSt in [1, 0]:
                self.mockmcu.set_BattLoSt(3, BattLoSt)
                new_info = 1 if BattLoSt == 1 else 0
                self.ck_warningmsg(hint, last_info, new_info)
                last_info = new_info

    @allure.title("左前轮胎快速漏气警告信息(MsgTireFLPressureFastLost)_告警产生恢复")
    @pytest.mark.sanity
    def test_caseid_108983(self):
        hint = "Front Left Tire Pressure Fast Lost"
        last_info = 0
        for usage_mode in [0, 1, 2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.partner.empty_all(0.5)
            for FastLoseWarnFlg in [1, 0]:
                self.mockmcu.set_FastLoseWarnFlg(0, FastLoseWarnFlg)
                new_info = 1 if FastLoseWarnFlg == 1 else 0
                self.ck_warningmsg(hint, last_info, new_info)
                last_info = new_info

    @allure.title("右前轮胎快速漏气警告信息(MsgTireFRPressureFastLost)_告警产生恢复")
    @pytest.mark.full
    def test_caseid_108993(self):
        hint = "Front Right Tire Pressure Fast Lost"
        last_info = 0
        for usage_mode in [0, 1, 2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.partner.empty_all(0.5)
            for FastLoseWarnFlg in [1, 0]:
                self.mockmcu.set_FastLoseWarnFlg(1, FastLoseWarnFlg)
                new_info = 1 if FastLoseWarnFlg == 1 else 0
                self.ck_warningmsg(hint, last_info, new_info)
                last_info = new_info

    @allure.title("左后轮胎快速漏气警告信息(MsgTireRLPressureFastLost)_告警产生恢复")
    @pytest.mark.full
    def test_caseid_108981(self):
        hint = "Rear Left Tire Pressure Fast Lost"
        last_info = 0
        for usage_mode in [0, 1, 2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.partner.empty_all(0.5)
            for FastLoseWarnFlg in [1, 0]:
                self.mockmcu.set_FastLoseWarnFlg(2, FastLoseWarnFlg)
                new_info = 1 if FastLoseWarnFlg == 1 else 0
                self.ck_warningmsg(hint, last_info, new_info)
                last_info = new_info

    @allure.title("右后轮胎快速漏气警告信息(MsgTireRRPressureFastLost)_告警产生恢复")
    @pytest.mark.smoke
    def test_caseid_108989(self):
        hint = "Rear Right Tire Pressure Fast Lost"
        last_info = 0
        for usage_mode in [0, 1, 2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.partner.empty_all(0.5)
            for FastLoseWarnFlg in [1, 0]:
                self.mockmcu.set_FastLoseWarnFlg(3, FastLoseWarnFlg)
                new_info = 1 if FastLoseWarnFlg == 1 else 0
                self.ck_warningmsg(hint, last_info, new_info)
                last_info = new_info

    @allure.title("左前胎压监测系统故障信息(MsgTirePressureSysFailureFL)_告警产生恢复")
    @pytest.mark.full
    def test_caseid_109015(self):
        hint = "Left Front Tire System Failure"
        last_info = 0
        for usage_mode in [0, 1, 2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.partner.empty_all(0.5)
            for SysWarnFlg in [1, 0]:
                self.mockmcu.set_SysWarnFlg(0, SysWarnFlg)
                new_info = 1 if SysWarnFlg == 1 else 0
                self.ck_warningmsg(hint, last_info, new_info)
                last_info = new_info

    @allure.title("右前胎压监测系统故障信息(MsgTirePressureSysFailureFR)_告警产生恢复")
    @pytest.mark.sanity
    def test_caseid_109013(self):
        hint = "Right Front Tire System Failure"
        last_info = 0
        for usage_mode in [0, 1, 2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.partner.empty_all(0.5)
            for SysWarnFlg in [1, 0]:
                self.mockmcu.set_SysWarnFlg(1, SysWarnFlg)
                new_info = 1 if SysWarnFlg == 1 else 0
                self.ck_warningmsg(hint, last_info, new_info)
                last_info = new_info

    @allure.title("左后胎压监测系统故障信息(MsgTirePressureSysFailureRL)_告警产生恢复")
    @pytest.mark.smoke
    def test_caseid_109014(self):
        hint = "Rear Left Tire System Failure"
        last_info = 0
        for usage_mode in [0, 1, 2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.partner.empty_all(0.5)
            for SysWarnFlg in [1, 0]:
                self.mockmcu.set_SysWarnFlg(2, SysWarnFlg)
                new_info = 1 if SysWarnFlg == 1 else 0
                self.ck_warningmsg(hint, last_info, new_info)
                last_info = new_info

    @allure.title("右后胎压监测系统故障信息(MsgTirePressureSysFailureRR)_告警产生恢复")
    @pytest.mark.full
    def test_caseid_109010(self):
        hint = "Rear Right Tire System Failure"
        last_info = 0
        for usage_mode in [0, 1, 2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.partner.empty_all(0.5)
            for SysWarnFlg in [1, 0]:
                self.mockmcu.set_SysWarnFlg(3, SysWarnFlg)
                new_info = 1 if SysWarnFlg == 1 else 0
                self.ck_warningmsg(hint, last_info, new_info)
                last_info = new_info

    @allure.title("胎压系统故障_车速丢失_告警产生恢复")
    @pytest.mark.full
    def test_caseid_108997(self):
        hint1 = "Left Front Tire System Failure"
        hint2 = "Right Front Tire System Failure"
        hint3 = "Rear Left Tire System Failure"
        hint4 = "Rear Right Tire System Failure"
        hint_map = {0: hint1, 1: hint2, 2: hint3, 3: hint4}
        for tyre_id in range(4):
            self.mockmcu.set_SysWarnFlg(tyre_id, 1)
            res = [{"name": hint_map[tyre_id], "info": '1'}]
            self.partner.ck_wti_warning_and_resp(hint_map[tyre_id], 1)

        for tyre_id in range(4):
            self.mockmcu.set_SysWarnFlg(tyre_id, 0)
            self.partner.ck_wti_warning_and_resp(hint_map[tyre_id], 0)

    @allure.title("左前轮胎胎压高警告信息(MsgTireFLPressureHigh)_告警产生恢复")
    @pytest.mark.full
    def test_caseid_1960010(self):
        hint = "Front Left Tire Pressure High"
        last_info = 0
        for usage_mode in [0, 1, 2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.partner.empty_all(0.5)
            for PWarnFlg in [2, 1, 2, 0, 2, 3]:
                self.mockmcu.set_PWarnFlg(0, PWarnFlg)
                new_info = 1 if PWarnFlg == 2 else 0
                self.ck_warningmsg(hint, last_info, new_info)
                last_info = new_info

    @allure.title("右前轮胎胎压高警告信息(MsgTireFRPressureHigh)_告警产生恢复")
    @pytest.mark.sanity
    def test_caseid_1960011(self):
        hint = "Front Right Tire Pressure High"
        last_info = 0
        for usage_mode in [0, 1, 2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.partner.empty_all(0.5)
            for PWarnFlg in [2, 1, 2, 0, 2, 3]:
                self.mockmcu.set_PWarnFlg(1, PWarnFlg)
                new_info = 1 if PWarnFlg == 2 else 0
                self.ck_warningmsg(hint, last_info, new_info)
                last_info = new_info

    @allure.title("左后轮胎胎压高警告信息(MsgTireRLPressureHigh)_告警产生恢复")
    @pytest.mark.smoke
    def test_caseid_1960012(self):
        hint = "Rear Left Tire Pressure High"
        last_info = 0
        for usage_mode in [0, 1, 2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.partner.empty_all(0.5)
            for PWarnFlg in [2, 1, 2, 0, 2, 3]:
                self.mockmcu.set_PWarnFlg(2, PWarnFlg)
                new_info = 1 if PWarnFlg == 2 else 0
                self.ck_warningmsg(hint, last_info, new_info)
                last_info = new_info

    @allure.title("右后轮胎胎压高警告信息(MsgTireRRPressureHigh)_告警产生恢复")
    @pytest.mark.sanity
    def test_caseid_1960013(self):
        hint = "Rear Right Tire Pressure High"
        last_info = 0
        for usage_mode in [0, 1, 2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.partner.empty_all(0.5)
            for PWarnFlg in [2, 1, 2, 0, 2, 3]:
                self.mockmcu.set_PWarnFlg(3, PWarnFlg)
                new_info = 1 if PWarnFlg == 2 else 0
                self.ck_warningmsg(hint, last_info, new_info)
                last_info = new_info

    @allure.title("胎压报警灯(TelltaleTirePressure)_usagemode在2,11,13时胎压传感器低压报警（常亮）_产生恢复")
    @pytest.mark.sanity
    def test_caseid_108978(self):
        for usage_mode in [2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.partner.empty_all(0.5)
            for tyre_id in range(4):
                self.mockmcu.set_PWarnFlg(tyre_id, 1)
                self.partner.ck_wti_telltale_and_resp("Tire Pressure", 1)
                self.mockmcu.set_PWarnFlg(tyre_id, 0)
                self.partner.ck_wti_telltale_and_resp("Tire Pressure", 0)

    @allure.title("胎压报警灯(TelltaleTirePressure)_usagemode在2,11,13时胎压传感器系统故障报警（闪灯）_产生恢复")
    @pytest.mark.full
    def test_caseid_1960015(self):
        for usage_mode in [2, 11, 13]:
            self.set_usage_mode(usage_mode)
            self.partner.empty_all(0.5)
            for tyre_id in range(4):
                self.mockmcu.set_SysWarnFlg(tyre_id, 1)
                self.partner.ck_wti_telltale_and_resp("Tire Pressure", 2)
                self.mockmcu.set_SysWarnFlg(tyre_id, 0)
                self.partner.ck_wti_telltale_and_resp("Tire Pressure", 0)

    @allure.title("胎压报警灯(TelltaleTirePressure)_usagemode在0,1时不会触发报警灯常亮")
    @pytest.mark.sanity
    def test_caseid_1960016(self):
        for usage_mode in [0, 1]:
            self.set_usage_mode(usage_mode)
            self.partner.empty_all(0.5)
            for tyre_id in range(4):
                self.mockmcu.set_PWarnFlg(tyre_id, 1)
            self.partner.ck_wti_no_telltale_and_ck_resp("Tire Pressure", 0)
        self.set_usage_mode(2)
        self.partner.ck_wti_telltale_and_resp("Tire Pressure", 1)

    @allure.title("胎压报警灯(TelltaleTirePressure)_usagemode在0,1时不会触发报警灯闪灯")
    @pytest.mark.full
    def test_caseid_1960017(self):
        for usage_mode in [0, 1]:
            self.set_usage_mode(usage_mode)
            self.partner.empty_all(0.5)
            for tyre_id in range(4):
                self.mockmcu.set_SysWarnFlg(tyre_id, 1)
            self.partner.ck_wti_no_telltale_and_ck_resp("Tire Pressure", 0)
        self.set_usage_mode(2)
        self.partner.ck_wti_telltale_and_resp("Tire Pressure", 2)

    @allure.title("胎压报警灯(TelltaleTirePressure)_常亮和闪灯切换0->1->2->1->0")
    @pytest.mark.smoke
    def test_caseid_108979(self):
        self.set_usage_mode(0xD)
        self.mockmcu.set_PWarnFlg(0, 1)
        self.mockmcu.set_PWarnFlg(1, 1)
        self.partner.ck_wti_telltale_and_resp("Tire Pressure", "1")

        self.mockmcu.set_SysWarnFlg(0, 1)
        self.partner.ck_wti_telltale_and_resp("Tire Pressure", "2")

        self.mockmcu.set_PWarnFlg(1, 0)
        self.partner.ck_wti_no_telltale_and_ck_resp("Tire Pressure", 2)

        self.mockmcu.set_SysWarnFlg(0, 0)
        self.partner.ck_wti_telltale_and_resp("Tire Pressure", "1")

        self.mockmcu.set_PWarnFlg(0, 0)
        self.partner.ck_wti_telltale_and_resp("Tire Pressure", "0")

    @allure.title("胎压报警灯(TelltaleTirePressure)_常亮和闪灯切换0->2->1->0")
    @pytest.mark.full
    def test_caseid_108977(self):
        self.set_usage_mode(0xD)
        self.mockmcu.set_SysWarnFlg(0, 1)
        self.partner.ck_wti_telltale_and_resp("Tire Pressure", "2")

        self.mockmcu.set_PWarnFlg(0, 1)
        sleep(1)
        self.partner.ck_wti_no_telltale_and_ck_resp("Tire Pressure", 2)

        self.mockmcu.set_SysWarnFlg(0, 0)
        self.partner.ck_wti_telltale_and_resp("Tire Pressure", "1")

        self.mockmcu.set_PWarnFlg(0, 0)
        self.partner.ck_wti_telltale_and_resp("Tire Pressure", "0")

    @allure.title("胎压报警灯(TelltaleTirePressure)_非低压或系统故障不会点亮报警灯")
    @pytest.mark.full
    def test_caseid_108976(self):
        self.set_usage_mode(0xD)
        for i in range(4):
            self.mockmcu.set_PWarnFlg(i, 2)
            sleep(0.5)
            self.mockmcu.set_PWarnFlg(i, 3)
            self.mockmcu.set_BattLoSt(i, 1)
            self.mockmcu.set_TWarnFlg(i, 1)
            self.mockmcu.set_FastLoseWarnFlg(i, 1)
            self.mockmcu.set_MsgOldFlg(i, 1)
        self.partner.ck_wti_no_telltale_and_ck_resp("Tire Pressure", "0")
