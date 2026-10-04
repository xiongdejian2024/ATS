#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_wiper_RLSM.py
@Author      : daidi.liang@jiduauto.com
@Time        : 2024/07/04 11:30
@Description: BGM车控车设外后视镜功能
"""

import os
import sys
import pytest
import allure
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.api.constants.common import *


@allure.feature("BGM车控车设/雨刮功能")
@allure.story("RLSM")
class TestWiperCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["WiperService_client"])
        sleep(2)
        self.soa.start_get_wiper_switch_sts()
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)

    def before_each_func(self, ecu):
        self.soa.empty_all()
        # 读取ccp  方便后面进行恢复
        err_code, recv_data_list = self.sd_tester.send_request_and_recv_response([0x22, 0xF1, 0x06],recv=[0x62, 0xF1, 0x06])
        self.ccp_original_value = recv_data_list[3:1556 + 3]
        self.bus_comm.set_vehspd(0.0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)

    def after_each_func(self, ecu):
        sleep(1)
        self.sd_tester.write_ccp_value(self.ccp_original_value)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)

    def after_class(self, ecu):
        self.soa.stop_get_wiper_switch_sts()
        try:
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
    
    def wiper_position_msg(self,set_signal_name,check_signal_name,ccp="true"):
        for i in range(2):
            logger.info(f"当前信号值为：{i}")
            self.bus_comm.set("cem_lin1","WmmCem_Lin1Fr01",set_signal_name,i)
            if ccp != "true":
                self.bus_comm.check("cem_lin1","CemCem_Lin1Fr06",check_signal_name,0)
            else:
                self.bus_comm.check("cem_lin1","CemCem_Lin1Fr06",check_signal_name,i)
        self.bus_comm.set("cem_lin1","WmmCem_Lin1Fr01",set_signal_name,0)
        
    def wiper_change_mode(self,wiper_mode,RainSenAct_sig_value,HMI_sig_value):
        self.soa.hmi_set_wiper_mode(WiperPos.Front,wiper_mode)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",RainSenAct_sig_value)
        self.bus_comm.check("backbonefr","CemBackBoneFr08","RainSnsrStsToHMI",HMI_sig_value)
        
    def wiper_maintain_isOn(self):
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.bus_comm.check("backbonefr","CemBackBoneFr08","RainSnsrStsToHMI",0)

    @pytest.mark.smoke
    def test_caseid_1991393(self):
        """
        雨刮状态发送给RLSM，检查雨刮器在挡风玻璃的位置信息
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.sd_tester.write_ccp({401:0x02,503:0x02})
        self.wiper_position_msg("WiprInWipgArFromWMM","WiprInWipgAr")
        self.wiper_position_msg("WiprInPrkgPosnLoFromWMM","WiprInPrkgPosnLo")

    
    @pytest.mark.smoke
    def test_caseid_1989108(self):
        """
        向RLSM发送洗涤周期信号
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.sd_tester.write_ccp({503:0x02})
        self.wiper_position_msg("WshngCycActvFromWMM","WshngCycActv")

    @pytest.mark.smoke
    def test_caseid_1989109(self):
        """
        发送雨刮激活信号给RLSM
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.sd_tester.write_ccp({503:0x02})
        self.wiper_position_msg("WiprActvFromWMM","WiprActv")

    @pytest.mark.smoke
    def test_caseid_1989123(self):
        """
        driving&Nomal 雨传感器激活,雨刮挡位由自动挡切换为单刮
        """
        self.mix.set_wiper_test_before(UsageMode.DRIVING,CarMode.NORMAL,wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.sd_tester.write_ccp({401:0x02})
        self.wiper_change_mode(WiperMode.Auto,1,1)
        self.wiper_change_mode(WiperMode.SingleWipe,0,0)

    @pytest.mark.smoke
    def test_caseid_1989124(self):
        """
        driving&dyno 雨传感器激活,雨刮挡位由自动挡切换为关闭档
        """
        self.mix.set_wiper_test_before(UsageMode.DRIVING,CarMode.DYNO,wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.sd_tester.write_ccp({401:0x02})
        self.wiper_change_mode(WiperMode.Auto,1,1)
        self.wiper_change_mode(WiperMode.Off,0,0)

    @pytest.mark.smoke
    def test_caseid_1989119(self):
        """
        convience&Nomal 雨传感器激活,雨刮挡位由自动挡切换为1档
        """
        self.mix.set_wiper_test_before(UsageMode.CONVENIENCE,CarMode.NORMAL,wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.sd_tester.write_ccp({401:0x02})
        self.wiper_change_mode(WiperMode.Auto,1,1)
        self.wiper_change_mode(WiperMode.IntLow,0,0)

    @pytest.mark.smoke
    def test_caseid_1989120(self):
        """
        convience&Dyno 雨传感器激活,雨刮挡位由自动挡切换为2档
        """
        self.mix.set_wiper_test_before(UsageMode.CONVENIENCE,CarMode.DYNO,wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.sd_tester.write_ccp({401:0x02})
        self.wiper_change_mode(WiperMode.Auto,1,1)
        self.wiper_change_mode(WiperMode.IntHigh,0,0)

    @pytest.mark.smoke
    def test_caseid_1989121(self):
        """
        active&Nomal 雨传感器激活,雨刮挡位由自动挡切换为3档
        """
        self.mix.set_wiper_test_before(UsageMode.ACTIVE,CarMode.NORMAL,wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.sd_tester.write_ccp({401:0x02})
        self.wiper_change_mode(WiperMode.Auto,1,1)
        self.wiper_change_mode(WiperMode.Low,0,0)

    @pytest.mark.smoke
    def test_caseid_1989122(self):
        """
        active&Dyno 雨传感器激活,雨刮挡位由自动挡切换为4档
        """
        self.mix.set_wiper_test_before(UsageMode.ACTIVE,CarMode.DYNO,wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.sd_tester.write_ccp({401:0x02})
        self.wiper_change_mode(WiperMode.Auto,1,1)
        self.wiper_change_mode(WiperMode.High,0,0)

    @pytest.mark.restart
    @pytest.mark.sanity
    def test_caseid_1989126(self):
        """
        active&Dyno 雨传感器停用,雨刮开启自动挡后，雨刮维修激活
        """
        self.mix.set_wiper_test_before(UsageMode.ACTIVE,CarMode.DYNO,wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.sd_tester.write_ccp({401:0x02})
        self.wiper_change_mode(WiperMode.Auto,1,1)
        sleep(1)
        self.wiper_maintain_isOn()

    @pytest.mark.restart
    @pytest.mark.sanity
    def test_caseid_1989130(self):
        """
        active&Nomal 雨传感器停用，雨刮从自动挡后，雨刮维修激活
        """
        self.mix.set_wiper_test_before(UsageMode.ACTIVE,CarMode.NORMAL,wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.sd_tester.write_ccp({401:0x02})
        self.wiper_change_mode(WiperMode.Auto,1,1)
        sleep(1)
        self.wiper_maintain_isOn()

    @pytest.mark.restart
    @pytest.mark.sanity
    def test_caseid_1989129(self):
        """
        convience&Dyno 雨传感器停用，雨刮从自动挡后，雨刮维修激活
        """
        self.mix.set_wiper_test_before(UsageMode.CONVENIENCE,CarMode.DYNO,wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.sd_tester.write_ccp({401:0x02})
        self.wiper_change_mode(WiperMode.Auto,1,1)
        sleep(1)
        self.wiper_maintain_isOn()
    
    @pytest.mark.restart
    @pytest.mark.sanity
    def test_caseid_1989125(self):
        """
        convience&Nomal 雨传感器停用,雨刮开启自动挡后，雨刮维修激活
        """
        self.mix.set_wiper_test_before(UsageMode.CONVENIENCE,CarMode.NORMAL,wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.sd_tester.write_ccp({401:0x02})
        self.wiper_change_mode(WiperMode.Auto,1,1)
        sleep(1)
        self.wiper_maintain_isOn()

    @pytest.mark.restart
    @pytest.mark.sanity
    def test_caseid_1989127(self):
        """
        driving&dyno 雨传感器停用，雨刮从自动挡后，雨刮维修激活
        """
        self.mix.set_wiper_test_before(UsageMode.DRIVING,CarMode.DYNO,wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.sd_tester.write_ccp({401:0x02})
        self.wiper_change_mode(WiperMode.Auto,1,1)
        sleep(1)
        self.wiper_maintain_isOn()

    @pytest.mark.restart
    @pytest.mark.sanity
    def test_caseid_1989128(self):
        """
        driving&Nomal 雨传感器停用，雨刮从自动挡后，雨刮维修激活
        """
        self.mix.set_wiper_test_before(UsageMode.DRIVING,CarMode.NORMAL,wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.sd_tester.write_ccp({401:0x02})
        self.wiper_change_mode(WiperMode.Auto,1,1)
        sleep(1)
        self.wiper_maintain_isOn()

    @pytest.mark.sanity
    def test_caseid_1989118(self):
        """
        为雨传感器提供环境温度
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.sd_tester.write_ccp({401:0x02})
        self.bus_comm.set("bodycan","DdmBodyFr02","AmbTRawAtDrvrSideAmbTVal",2)
        self.bus_comm.set("bodycan","DdmBodyFr02","AmbTRawAtDrvrSideQly",2)
        self.bus_comm.set("bodycan","PdmBodyFr03","AmbTRawAtPassSideAmbTVal",2)
        self.bus_comm.set("bodycan","PdmBodyFr03","AmbTRawAtPassSideQly",2)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr02","AmbTForVisy",255)
        # self.bus_comm.set("bodycan","DdmBodyFr02","AmbTRawAtDrvrSideAmbTVal",0)
        # self.bus_comm.set("bodycan","DdmBodyFr02","AmbTRawAtDrvrSideQly",3)
        # self.bus_comm.set("bodycan","PdmBodyFr03","AmbTRawAtPassSideAmbTVal",32.9)
        # self.bus_comm.set("bodycan","PdmBodyFr03","AmbTRawAtPassSideQly",3)
        # self.bus_comm.check("cem_lin1","CemCem_Lin1Fr02","AmbTForVisy",255)

    @pytest.mark.full
    def test_caseid_1989110(self):
        """
        发送雨刮激活信号给RLSM
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.sd_tester.write_ccp({503:0x01})
        self.wiper_position_msg("WiprActvFromWMM","WiprActv",ccp="false")
        
    @pytest.mark.full
    def test_caseid_1989115(self):
        """
        反向用例_ccp401!=02,雨刮状态发送给RLSM，检查雨刮器在挡风玻璃的位置信息
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.sd_tester.write_ccp({401:0x01,503:0x02})
        self.wiper_position_msg("WiprInWipgArFromWMM","WiprInWipgAr",ccp="false")
        self.wiper_position_msg("WiprInPrkgPosnLoFromWMM","WiprInPrkgPosnLo",ccp="false")

    @pytest.mark.full
    def test_caseid_1989117(self):
        """
        反向用例_ccp503!=02 & 401!=02 ,雨刮状态发送给RLSM，检查雨刮器在挡风玻璃的位置信息
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.sd_tester.write_ccp({401:0x01,503:0x01})
        self.wiper_position_msg("WiprInWipgArFromWMM","WiprInWipgAr",ccp="false")
        self.wiper_position_msg("WiprInPrkgPosnLoFromWMM","WiprInPrkgPosnLo",ccp="false")
    
    @pytest.mark.full
    def test_caseid_1989107(self):
        """
        反向用例_CCP503!=02 向RLSM发送洗涤周期信号
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.sd_tester.write_ccp({503:0x01})
        self.wiper_position_msg("WshngCycActvFromWMM","WshngCycActv",ccp="false")

    @pytest.mark.full
    def test_caseid_1989116(self):
        """
        反向用例_ccp503!=02,雨刮状态发送给RLSM，检查雨刮器在挡风玻璃的位置信息
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.sd_tester.write_ccp({401:0x02,503:0x01})
        self.wiper_position_msg("WiprInWipgArFromWMM","WiprInWipgAr",ccp="false")
        self.wiper_position_msg("WiprInPrkgPosnLoFromWMM","WiprInPrkgPosnLo",ccp="false")

    @pytest.mark.full
    def test_caseid_1989136(self):
        """
        active&Factory 雨传感器不能被激活,雨刮挡位由自动挡切换为3档
        """
        self.mix.set_wiper_test_before(UsageMode.ACTIVE,CarMode.FACTORY,wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.sd_tester.write_ccp({401:0x02})
        self.wiper_change_mode(WiperMode.Auto,0,0)
        self.wiper_change_mode(WiperMode.Low,0,0)

    @pytest.mark.full
    def test_caseid_1989135(self):
        """
        active&Transport 雨传感器不能被激活,雨刮挡位由自动挡切换为2档
        """
        self.mix.set_wiper_test_before(UsageMode.ACTIVE,CarMode.TRANSPORT,wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.sd_tester.write_ccp({401:0x02})
        self.wiper_change_mode(WiperMode.Auto,0,0)
        self.wiper_change_mode(WiperMode.IntHigh,0,0)

    @pytest.mark.full
    def test_caseid_1989134(self):
        """
        active&Crash 雨传感器不能被激活,雨刮挡位由自动挡切换为单刮
        """
        self.mix.set_wiper_test_before(UsageMode.ACTIVE,CarMode.CRASH,wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.sd_tester.write_ccp({401:0x02})
        self.wiper_change_mode(WiperMode.Auto,0,0)
        self.wiper_change_mode(WiperMode.SingleWipe,0,0)

    @pytest.mark.full
    def test_caseid_1989133(self):
        """
        Convience&factory 雨传感器不能被激活,雨刮挡位由自动挡切换为关闭档
        """
        self.mix.set_wiper_test_before(UsageMode.CONVENIENCE,CarMode.FACTORY,wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.sd_tester.write_ccp({401:0x02})
        self.bus_comm.set_vehspd(3.0)
        self.wiper_change_mode(WiperMode.Auto,0,0)
        self.wiper_change_mode(WiperMode.Off,0,0)

    @pytest.mark.full
    def test_caseid_1989132(self):
        """
        Concience&Transport 雨传感器不能被激活,雨刮挡位由自动挡切换为4档
        """
        self.mix.set_wiper_test_before(UsageMode.CONVENIENCE,CarMode.TRANSPORT,wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.sd_tester.write_ccp({401:0x02})
        self.bus_comm.set_vehspd(3.0)
        self.wiper_change_mode(WiperMode.Auto,0,0)
        self.wiper_change_mode(WiperMode.High,0,0)

    @pytest.mark.full
    def test_caseid_1989131(self):
        """
        Convience&Crash 雨传感器不能被激活,雨刮挡位由自动挡切换为1档
        """
        self.mix.set_wiper_test_before(UsageMode.CONVENIENCE,CarMode.CRASH,wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.sd_tester.write_ccp({401:0x02})
        self.bus_comm.set_vehspd(3.0)
        self.wiper_change_mode(WiperMode.Auto,0,0)
        self.wiper_change_mode(WiperMode.IntLow,0,0)

    @pytest.mark.full
    def test_caseid_1989382(self):
        """
        Driving&Factory 雨传感器停用,雨刮开启自动挡后，雨刮维修激活，雨传感器不能被激活
        """
        self.mix.set_wiper_test_before(UsageMode.DRIVING,CarMode.TRANSPORT,wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.sd_tester.write_ccp({401:0x02})
        self.wiper_change_mode(WiperMode.Auto,0,0)
        self.wiper_maintain_isOn()

    @pytest.mark.full
    def test_caseid_1989383(self):
        """
        abondoned&Dyno 雨传感器停用,雨刮开启自动挡后，雨刮维修激活，雨传感器不能被激活
        """
        self.mix.set_wiper_test_before(UsageMode.ABANDONED,CarMode.DYNO,wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.sd_tester.write_ccp({401:0x02})
        self.wiper_change_mode(WiperMode.Auto,0,0)
        self.wiper_maintain_isOn()

    @pytest.mark.full
    def test_caseid_1989140(self):
        """
        abondoned&Nomal 雨传感器停用，雨刮从自动挡后，雨刮维修激活，雨传感器不能被激活
        """
        self.mix.set_wiper_test_before(UsageMode.ABANDONED,CarMode.NORMAL,wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.sd_tester.write_ccp({401:0x02})
        self.wiper_change_mode(WiperMode.Auto,0,0)
        self.wiper_maintain_isOn()

    @pytest.mark.full
    def test_caseid_1989139(self):
        """
        Driving&Crash 雨传感器停用，雨刮从自动挡后，雨刮维修激活，雨传感器不能被激活
        """
        self.mix.set_wiper_test_before(UsageMode.DRIVING,CarMode.CRASH,wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.sd_tester.write_ccp({401:0x02})
        self.wiper_change_mode(WiperMode.Auto,0,0)
        self.wiper_maintain_isOn()

    @pytest.mark.full
    def test_caseid_1989138(self):
        """
        Inactive&Dyno 雨传感器停用，雨刮从自动挡后，雨刮维修激活，雨传感器不能被激活
        """
        self.mix.set_wiper_test_before(UsageMode.INACTIVE,CarMode.DYNO,wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.sd_tester.write_ccp({401:0x02})
        self.wiper_change_mode(WiperMode.Auto,0,0)
        self.wiper_maintain_isOn()

    @pytest.mark.full
    def test_caseid_1989137(self):
        """
        Inactive&Nomal 雨传感器停用，雨刮从自动挡后，雨刮维修激活，雨传感器不能被激活
        """
        self.mix.set_wiper_test_before(UsageMode.INACTIVE,CarMode.NORMAL,wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.sd_tester.write_ccp({401:0x02})
        self.wiper_change_mode(WiperMode.Auto,0,0)
        self.wiper_maintain_isOn()

    @pytest.mark.full
    def test_caseid_1989143(self):
        """
        convience&Nomal ccp 401!=02 雨传感器不能激活,雨刮挡位由自动挡切换为1档
        """
        self.mix.set_wiper_test_before(UsageMode.CONVENIENCE,CarMode.NORMAL,wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.sd_tester.write_ccp({401:0x01})
        self.wiper_change_mode(WiperMode.Auto,0,0)
        self.wiper_change_mode(WiperMode.IntLow,0,0)

    @pytest.mark.full
    def test_caseid_1989144(self):
        """
        active&Dyno ccp 401!=02 雨传感器不能激活,雨刮挡位由自动挡切换为4档
        """
        self.mix.set_wiper_test_before(UsageMode.ACTIVE,CarMode.DYNO,wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.sd_tester.write_ccp({401:0x01})
        self.wiper_change_mode(WiperMode.Auto,0,0)
        self.wiper_change_mode(WiperMode.High,0,0)

    @pytest.mark.full
    def test_caseid_1989145(self):
        """
        driving&dyno ccp 401!=02雨传感器不能激活,雨刮挡位由自动挡切换为关闭档
        """
        self.mix.set_wiper_test_before(UsageMode.DRIVING,CarMode.DYNO,wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.sd_tester.write_ccp({401:0x01})
        self.wiper_change_mode(WiperMode.Auto,0,0)
        self.wiper_change_mode(WiperMode.Off,0,0)

    @pytest.mark.full
    def test_caseid_1989146(self):
        """
        driving&Nomal ccp 401!=02 雨传感器不能激活,雨刮挡位由自动挡切换为单刮
        """
        self.mix.set_wiper_test_before(UsageMode.DRIVING,CarMode.NORMAL,wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.sd_tester.write_ccp({401:0x01})
        self.wiper_change_mode(WiperMode.Auto,0,0)
        self.wiper_change_mode(WiperMode.SingleWipe,0,0)

    @pytest.mark.full
    def test_caseid_1989147(self):
        """
        convience&Dyno ccp 401!=02 雨传感器不能激活,雨刮挡位由自动挡切换为2档
        """
        self.mix.set_wiper_test_before(UsageMode.CONVENIENCE,CarMode.DYNO,wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.sd_tester.write_ccp({401:0x01})
        self.wiper_change_mode(WiperMode.Auto,0,0)
        self.wiper_change_mode(WiperMode.IntHigh,0,0)

    @pytest.mark.full
    def test_caseid_1989148(self):
        """
        active&Nomal ccp 401!=02 雨传感器不能激活,雨刮挡位由自动挡切换为3档
        """
        self.mix.set_wiper_test_before(UsageMode.ACTIVE,CarMode.NORMAL,wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.sd_tester.write_ccp({401:0x01})
        self.wiper_change_mode(WiperMode.Auto,0,0)
        self.wiper_change_mode(WiperMode.Low,0,0)

    @pytest.mark.full
    def test_caseid_1989164(self):
        """
        driving&Nomal 雨传感器错误&CEM与RSM通讯失败
        """
        self.sd_tester.write_ccp({401:0x02})
        self.mix.set_dtc_precontion()
        self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        self.mix.set_wiper_test_before(UsageMode.DRIVING,CarMode.NORMAL,wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.wiper_change_mode(WiperMode.Auto,1,1)
        self.mix.generate_dtc_fault(dtc_fault=DTCFault.Rainerror,last_time=4)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.Rainerror, dtc_sts=DTCSts.CurrentFailed, fault_sts=True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.bus_comm.check("backbonefr","CemBackBoneFr08","RainSnsrStsToHMI",0)
        self.mix.remove_dtc_fault(dtc_fault=DTCFault.Rainerror,last_time=4)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.Rainerror, dtc_sts=DTCSts.FullWithHistory, fault_sts=True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr08","RainSnsrStsToHMI",1)

  