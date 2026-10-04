
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_wiper_mode_abc.py
@Author      : hui.zhao@jiduauto.com
@Time        : 2023/11/9 11:30
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
@allure.story("雨刮维修")
class TestWiperCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["WiperService_client"])
        sleep(2)
        self.soa.start_get_wiper_switch_sts()

    def before_each_func(self, ecu):
        # 读取ccp  方便后面进行恢复
        err_code, recv_data_list = self.sd_tester.send_request_and_recv_response([0x22, 0xF1, 0x06],recv=[0x62, 0xF1, 0x06])
        self.ccp_original_value = recv_data_list[3:1556 + 3]
        self.sd_tester.write_ccp({503:0x02})
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        self.soa.empty_all()
        self.bus_comm.set_vehspd_gear(vehspd=0.0) 
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.Off)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.soa.hmi_set_wiper_mode(WiperPos.Front, WiperMode.Off)
        sleep(1)
        self.bus_comm.ipdu.rx_flag_reset_all()
        sleep(1)
        
        
    def after_each_func(self, ecu):
        self.bus_comm.set("cem_lin1","WmmCem_Lin1Fr01","WiprMotErrSafe",1)
        self.sd_tester.write_ccp_value(self.ccp_original_value)

    def after_class(self, ecu):
        self.soa.stop_get_wiper_switch_sts()
        try:
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
    
    def check_AcsyMod_and_DrvgMod(self,AcsyMod_value:int,DrvgMod_value:int):
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrAcsyModSafe",AcsyMod_value)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrDrvgModSafe",DrvgMod_value)

    def check_WiprMotFrntLvrCmdNotSafe(self,LvrInSnglStrokePos:int,LvrInIntlPosn:int,LvrInLoSpdPosn:int,LvrInHiSpdPosn:int):
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInSnglStrokePos",LvrInSnglStrokePos)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInIntlPosn",LvrInIntlPosn)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",LvrInLoSpdPosn)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInHiSpdPosnSafe",LvrInHiSpdPosn)

    @pytest.mark.smoke
    def test_caseid_1990557(self):
        """
        功率等级:ElPowerLevel=1_driving&normal 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x10, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=2)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=2)

    @pytest.mark.sanity
    def test_caseid_1990556(self):
        """
        功率等级:ElPowerLevel=1_driving&dyno 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x10, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=2)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=2)

    @pytest.mark.full
    def test_caseid_1990555(self):
        """
        功率等级:ElPowerLevel=1_driving&crash 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x10, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.CRASH)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=2)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=2)

    @pytest.mark.full
    def test_caseid_1990554(self):
        """
        功率等级:ElPowerLevel=1_driving&Transport 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x10, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=2)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=2)

    @pytest.mark.full
    def test_caseid_1990553(self):
        """
        功率等级:ElPowerLevel=1_driving&factory 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x10, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.FACTORY)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=2)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=2)

    @pytest.mark.smoke
    def test_caseid_1990552(self):
        """
        功率等级:ElPowerLevel=1_active&normal 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x10, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=2)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=2)

    @pytest.mark.sanity
    def test_caseid_1990551(self):
        """
        功率等级:ElPowerLevel=1_active&dyno 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x10, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=2)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=2)

    @pytest.mark.full
    def test_caseid_1990550(self):
        """
        功率等级:ElPowerLevel=1_active&crash 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x10, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.CRASH)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=2)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=2)

    @pytest.mark.full
    def test_caseid_1990549(self):
        """
        功率等级:ElPowerLevel=1_active&Transport 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x10, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=2)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=2)

    @pytest.mark.full
    def test_caseid_1990548(self):
        """
        功率等级:ElPowerLevel=1_active&factory 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x10, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.FACTORY)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=2)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=2)

    @pytest.mark.smoke
    def test_caseid_1990547(self):
        """
        功率等级:ElPowerLevel=1_convience&normal 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x10, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=2)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=2)

    @pytest.mark.sanity
    def test_caseid_1990546(self):
        """
        功率等级:ElPowerLevel=1_covience&dyno 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x10, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=2)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=2)

    @pytest.mark.full
    def test_caseid_1990545(self):
        """
        功率等级:ElPowerLevel=1_convience&crash 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x10, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.CRASH)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=2)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=2)

    @pytest.mark.full
    def test_caseid_1990544(self):
        """
        功率等级:ElPowerLevel=1_convience&Transport 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x10, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=2)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=2)

    @pytest.mark.full
    def test_caseid_1990543(self):
        """
        功率等级:ElPowerLevel=1_convience&factory 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x10, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.FACTORY)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=2)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=2)

    @pytest.mark.smoke
    def test_caseid_1990542(self):
        """
        功率等级:ElPowerLevel=1_inactive&normal 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x10, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=2)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1.5)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=2)

    @pytest.mark.sanity
    def test_caseid_1990541(self):
        """
        功率等级:ElPowerLevel=1_inactive&dyno 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x10, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=2)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=2)

    @pytest.mark.full
    def test_caseid_1990540(self):
        """
        功率等级:ElPowerLevel=1_inactive&crash 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x10, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.CRASH)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=2)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=2)

    @pytest.mark.full
    def test_caseid_1990539(self):
        """
        功率等级:ElPowerLevel=1_inactive&Transport 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x10, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=2)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=2)

    @pytest.mark.full
    def test_caseid_1990538(self):
        """
        功率等级:ElPowerLevel=1_inactive&factory 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x10, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.FACTORY)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=2)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=2)

    @pytest.mark.smoke
    def test_caseid_1990537(self):
        """
        功率等级:ElPowerLevel=1_abandoned&normal 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x10, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=2)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=2)

    @pytest.mark.sanity
    def test_caseid_1990536(self):
        """
        功率等级:ElPowerLevel=1_abandoned&dyno 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x10, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=2)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=2)

    @pytest.mark.full
    def test_caseid_1990535(self):
        """
        功率等级:ElPowerLevel=1_abandoned&crash 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x10, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.CRASH)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=2)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=2)

    @pytest.mark.full
    def test_caseid_1990534(self):
        """
        功率等级:ElPowerLevel=1_abandoned&Transport 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x10, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=2)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=2)

    @pytest.mark.full
    def test_caseid_1990533(self):
        """
        功率等级:ElPowerLevel=1_abandoned&factory 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x10, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.FACTORY)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=2)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=2)

    @pytest.mark.smoke
    def test_caseid_1990532(self):
        """
        功率等级:ElPowerLevel !=1_abandoned&normal 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x00, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=1)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=1)
    
    @pytest.mark.sanity
    def test_caseid_1990531(self):
        """
        功率等级:ElPowerLevel !=1_abandoned&dyno 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x00, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=1)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=1)

    @pytest.mark.full
    def test_caseid_1990530(self):
        """
        功率等级:ElPowerLevel !=1_abandoned&crash 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x00, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.CRASH)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=1)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=1)

    @pytest.mark.full
    def test_caseid_1990529(self):
        """
        功率等级:ElPowerLevel !=1_abandoned&Transport 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x00, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=1)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=1)

    @pytest.mark.full
    def test_caseid_1990528(self):
        """
        功率等级:ElPowerLevel !=1_abandoned&factory 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x00, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.FACTORY)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=1)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=1)

    @pytest.mark.smoke
    def test_caseid_1990527(self):
        """
        功率等级:ElPowerLevel !=1_driving&normal 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x00, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=2)

    @pytest.mark.sanity
    def test_caseid_1990526(self):
        """
        功率等级:ElPowerLevel !=1_driving&dyno 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x00, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=2)

    @pytest.mark.full
    def test_caseid_1990525(self):
        """
        功率等级:ElPowerLevel !=1_driving&crash 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x00, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.CRASH)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=1)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=1)

    @pytest.mark.full
    def test_caseid_1990524(self):
        """
        功率等级:ElPowerLevel !=1_driving&Transport 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x00, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=1)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=1)

    @pytest.mark.full
    def test_caseid_1990523(self):
        """
        功率等级:ElPowerLevel !=1_driving&factory 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x00, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.FACTORY)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=1)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=1)

    @pytest.mark.smoke
    def test_caseid_1990522(self):
        """
        功率等级:ElPowerLevel !=1_active&normal 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x00, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=2)

    @pytest.mark.sanity
    def test_caseid_1990521(self):
        """
        功率等级:ElPowerLevel !=1_active&dyno 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x00, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=2)

    @pytest.mark.full
    def test_caseid_1990520(self):
        """
        功率等级:ElPowerLevel !=1_active&crash 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x00, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.CRASH)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=1)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=1)

    @pytest.mark.full
    def test_caseid_1990519(self):
        """
        功率等级:ElPowerLevel !=1_active&Transport 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x00, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=1)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=1)

    @pytest.mark.full
    def test_caseid_1990518(self):
        """
        功率等级:ElPowerLevel !=1_active&factory 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x00, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.FACTORY)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=1)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=1)

    @pytest.mark.smoke
    def test_caseid_1990517(self):
        """
        功率等级:ElPowerLevel !=1_convience&normal 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x00, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=1)

    @pytest.mark.sanity
    def test_caseid_1990516(self):
        """
        功率等级:ElPowerLevel !=1_convience&dyno 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x00, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=1)

    @pytest.mark.full
    def test_caseid_1990515(self):
        """
        功率等级:ElPowerLevel !=1_convience&crash 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x00, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.CRASH)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=1)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=1)

    @pytest.mark.full
    def test_caseid_1990514(self):
        """
        功率等级:ElPowerLevel !=1_convience&Transport 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x00, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=1)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=1)

    @pytest.mark.full
    def test_caseid_1990513(self):
        """
        功率等级:ElPowerLevel !=1_convience&factory 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x00, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.FACTORY)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=1)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=1)

    @pytest.mark.smoke
    def test_caseid_1990512(self):
        """
        功率等级:ElPowerLevel !=1_inactive&normal 雨刮维修激活小于10s，雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x00, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        sleep(8)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=1)

    @pytest.mark.smoke
    def test_caseid_1990511(self):
        """
        功率等级:ElPowerLevel !=1_inactive&normal 雨刮维修退出，雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x00, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=1)

    @pytest.mark.sanity
    def test_caseid_1990510(self):
        """
        功率等级:ElPowerLevel !=1_inactive&dyno 雨刮维修激活小于10s，雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x00, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        sleep(8)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=1)

    @pytest.mark.sanity
    def test_caseid_1990509(self):
        """
        功率等级:ElPowerLevel !=1_inactive&dyno 雨刮维修退出，雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x00, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=1)

    @pytest.mark.smoke
    def test_caseid_1990508(self):
        """
        功率等级:ElPowerLevel !=1_inactive&normal 雨刮维修激活超过10s，车速大于7km/h，雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x00, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        sleep(11)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=1)

    @pytest.mark.smoke
    def test_caseid_1990507(self):
        """
        功率等级:ElPowerLevel !=1_inactive&normal 雨刮维修退出，车速大于7km/h，雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x00, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=1)

    @pytest.mark.smoke
    def test_caseid_1990506(self):
        """
        功率等级:ElPowerLevel !=1_inactive&normal 雨刮维修激活超过10s，车速小于7km/h，雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x00, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        sleep(10.5)   
        self.bus_comm.set_vehspd_gear(vehspd=1.0)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrAcsyModSafe",1)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrDrvgModSafe",1)

    @pytest.mark.sanity
    def test_caseid_1990504(self):
        """
        功率等级:ElPowerLevel !=1_inactive&dyno 雨刮维修激活超过10s，车速大于7km/h，雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x00, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        sleep(11)   
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=1)

    @pytest.mark.sanity
    def test_caseid_1990503(self):
        """
        功率等级:ElPowerLevel !=1_inactive&dyno雨刮维修激活超过10s，车速小于7km/h，雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x00, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=1.0)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        sleep(10.5)   
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=1)

    @pytest.mark.sanity
    def test_caseid_1990502(self):
        """
        功率等级:ElPowerLevel !=1_inactive&dyno 雨刮维修退出，车速大于7km/h，雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x00, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=1)

    @pytest.mark.full
    def test_caseid_1990501(self):
        """
        功率等级:ElPowerLevel !=1_inactive&crash 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x00, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.CRASH)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=1)
        self.bus_comm.set_vehspd_gear(vehspd=1.0)
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=1)

    @pytest.mark.full
    def test_caseid_1990500(self):
        """
        功率等级:ElPowerLevel !=1_inactive&Transport 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x00, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=1)
        self.bus_comm.set_vehspd_gear(vehspd=1.0)
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=1)

    @pytest.mark.full
    def test_caseid_1990499(self):
        """
        功率等级:ElPowerLevel !=1_inactive&factory 雨刷电机模式AcsyMode,DrvgMode信号值变化
        """
        self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0X9E,0x03, 0x00, 0X00],recv=[0x6F,0x42,0x9E,0x03])
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.FACTORY)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=2,DrvgMod_value=1)
        self.bus_comm.set_vehspd_gear(vehspd=1.0)
        sleep(1)
        self.check_AcsyMod_and_DrvgMod(AcsyMod_value=1,DrvgMod_value=1)

    @pytest.mark.smoke
    def test_caseid_1990498(self):
        """
        convience&normal 雨刮模式为off,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.sanity
    def test_caseid_1990497(self):
        """
        convience&dyno 雨刮模式为off,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
  
    @pytest.mark.full
    def test_caseid_1990496(self):
        """
        convience&crash 雨刮模式为off,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990495(self):
        """
        convience&factory雨刮模式为off,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990494(self):
        """
        convience&transport雨刮模式为off,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.smoke
    def test_caseid_1990493(self):
        """
       driving&normal 雨刮模式为off,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.sanity
    def test_caseid_1990492(self):
        """
        driving&dyno 雨刮模式为off,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
  
    @pytest.mark.full
    def test_caseid_1990491(self):
        """
        driving&crash 雨刮模式为off,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990490(self):
        """
        driving&factory雨刮模式为off,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990489(self):
        """
        driving&transport雨刮模式为off,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.smoke
    def test_caseid_1990488(self):
        """
       active&normal 雨刮模式为off,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.sanity
    def test_caseid_1990487(self):
        """
        active&dyno 雨刮模式为off,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
  
    @pytest.mark.full
    def test_caseid_1990486(self):
        """
        active&crash 雨刮模式为off,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990485(self):
        """
        active&factory雨刮模式为off,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990484(self):
        """
        active&transport雨刮模式为off,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.smoke
    def test_caseid_1990483(self):
        """
       Inactive&normal 雨刮模式为off,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.sanity
    def test_caseid_1990482(self):
        """
        Inactive&dyno 雨刮模式为off,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
  
    @pytest.mark.full
    def test_caseid_1990481(self):
        """
        Inactive&crash 雨刮模式为off,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990480(self):
        """
        Inactive&factory雨刮模式为off,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990479(self):
        """
        Inactive&transport雨刮模式为off,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.smoke
    def test_caseid_1990478(self):
        """
       abandoned&normal 雨刮模式为off,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.sanity
    def test_caseid_1990477(self):
        """
        abandoned&dyno 雨刮模式为off,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
  
    @pytest.mark.full
    def test_caseid_1990476(self):
        """
        abandoned&crash 雨刮模式为off,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990475(self):
        """
        abandoned&factory雨刮模式为off,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990474(self):
        """
        abandoned&transport雨刮模式为off,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.smoke
    def test_caseid_1990458(self):
        """
        convience&normal 雨刮模式为单刮,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=1,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.sanity
    def test_caseid_1990457(self):
        """
        convience&dyno 雨刮模式为单刮,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=1,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
  
    @pytest.mark.full
    def test_caseid_1990456(self):
        """
        convience&crash 雨刮模式为单刮,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=1,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990455(self):
        """
        convience&factory雨刮模式为单刮,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=1,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990454(self):
        """
        convience&transport雨刮模式为单刮,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=1,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.smoke
    def test_caseid_1990463(self):
        """
       driving&normal 雨刮模式为单刮,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=1,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.sanity
    def test_caseid_1990462(self):
        """
        driving&dyno 雨刮模式为单刮,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=1,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
  
    @pytest.mark.full
    def test_caseid_1990461(self):
        """
        driving&crash 雨刮模式为单刮,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=1,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990460(self):
        """
        driving&factory雨刮模式为单刮,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=1,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990459(self):
        """
        driving&transport雨刮模式为单刮,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=1,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.smoke
    def test_caseid_1990468(self):
        """
       active&normal 雨刮模式为单刮,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=1,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.sanity
    def test_caseid_1990467(self):
        """
        active&dyno 雨刮模式为单刮,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=1,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
  
    @pytest.mark.full
    def test_caseid_1990466(self):
        """
        active&crash 雨刮模式为单刮,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=1,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990465(self):
        """
        active&factory雨刮模式为单刮,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=1,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990464(self):
        """
        active&transport雨刮模式为单刮,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=1,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.smoke
    def test_caseid_1990473(self):
        """
       Inactive&normal 雨刮模式为单刮,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=1,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.sanity
    def test_caseid_1990472(self):
        """
        Inactive&dyno 雨刮模式为单刮,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=1,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
  
    @pytest.mark.full
    def test_caseid_1990471(self):
        """
        Inactive&crash 雨刮模式为单刮,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=1,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990470(self):
        """
        Inactive&factory雨刮模式为单刮,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=1,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990469(self):
        """
        Inactive&transport雨刮模式为单刮,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=1,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.smoke
    def test_caseid_1990453(self):
        """
       abandoned&normal 雨刮模式为单刮,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=1,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.sanity
    def test_caseid_1990452(self):
        """
        abandoned&dyno 雨刮模式为单刮,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=1,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
  
    @pytest.mark.full
    def test_caseid_1990451(self):
        """
        abandoned&crash 雨刮模式为单刮,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=1,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990450(self):
        """
        abandoned&factory雨刮模式为单刮,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=1,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990449(self):
        """
        abandoned&transport雨刮模式为单刮,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=1,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.smoke
    def test_caseid_1990438(self):
        """
        convience&normal 雨刮模式为1档IntLow,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.sanity
    def test_caseid_1990437(self):
        """
        convience&dyno 雨刮模式为1档IntLow,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
  
    @pytest.mark.full
    def test_caseid_1990436(self):
        """
        convience&crash 雨刮模式为1档IntLow,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990435(self):
        """
        convience&factory雨刮模式为1档IntLow,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990434(self):
        """
        convience&transport雨刮模式为1档IntLow,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.smoke
    def test_caseid_1990443(self):
        """
       driving&normal 雨刮模式为1档IntLow,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.sanity
    def test_caseid_1990442(self):
        """
        driving&dyno 雨刮模式为1档IntLow,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
  
    @pytest.mark.full
    def test_caseid_1990441(self):
        """
        driving&crash 雨刮模式为1档IntLow,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.full
    def test_caseid_1990440(self):
        """
        driving&factory雨刮模式为1档IntLow,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.full
    def test_caseid_1990439(self):
        """
        driving&transport雨刮模式为1档IntLow,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)



    @pytest.mark.smoke
    def test_caseid_1990448(self):
        """
       active&normal 雨刮模式为1档IntLow,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.sanity
    def test_caseid_1990447(self):
        """
        active&dyno 雨刮模式为1档IntLow,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
  
    @pytest.mark.full
    def test_caseid_1990446(self):
        """
        active&crash 雨刮模式为1档IntLow,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990445(self):
        """
        active&factory雨刮模式为1档IntLow,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990444(self):
        """
        active&transport雨刮模式为1档IntLow,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.smoke
    def test_caseid_1990433(self):
        """
       Inactive&normal 雨刮模式为1档IntLow,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.sanity
    def test_caseid_1990432(self):
        """
        Inactive&dyno 雨刮模式为1档IntLow,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
  
    @pytest.mark.full
    def test_caseid_1990431(self):
        """
        Inactive&crash 雨刮模式为1档IntLow,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990430(self):
        """
        Inactive&factory雨刮模式为1档IntLow,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990429(self):
        """
        Inactive&transport雨刮模式为1档IntLow,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.smoke
    def test_caseid_1990428(self):
        """
       abandoned&normal 雨刮模式为1档IntLow,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.sanity
    def test_caseid_1990427(self):
        """
        abandoned&dyno 雨刮模式为1档IntLow,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
  
    @pytest.mark.full
    def test_caseid_1990426(self):
        """
        abandoned&crash 雨刮模式为1档IntLow,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990425(self):
        """
        abandoned&factory雨刮模式为1档IntLow,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990424(self):
        """
        abandoned&transport雨刮模式为1档IntLow,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.smoke
    def test_caseid_1990403(self):
        """
        convience&normal 雨刮模式为2档IntHigh,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.sanity
    def test_caseid_1990402(self):
        """
        convience&dyno 雨刮模式为2档IntHigh,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
  
    @pytest.mark.full
    def test_caseid_1990401(self):
        """
        convience&crash 雨刮模式为2档IntHigh,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990400(self):
        """
        convience&factory雨刮模式为2档IntHigh,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990399(self):
        """
        convience&transport雨刮模式为2档IntHigh,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.smoke
    def test_caseid_1990408(self):
        """
       driving&normal 雨刮模式为2档IntHigh,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.sanity
    def test_caseid_1990407(self):
        """
        driving&dyno 雨刮模式为2档IntHigh,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
  
    @pytest.mark.full
    def test_caseid_1990406(self):
        """
        driving&crash 雨刮模式为2档IntHigh,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990405(self):
        """
        driving&factory雨刮模式为2档IntHigh,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990404(self):
        """
        driving&transport雨刮模式为2档IntHigh,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.smoke
    def test_caseid_1990413(self):
        """
       active&normal 雨刮模式为2档IntHigh,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.sanity
    def test_caseid_1990412(self):
        """
        active&dyno 雨刮模式为2档IntHigh,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
  
    @pytest.mark.full
    def test_caseid_1990411(self):
        """
        active&crash 雨刮模式为2档IntHigh,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990410(self):
        """
        active&factory雨刮模式为2档IntHigh,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990409(self):
        """
        active&transport雨刮模式为2档IntHigh,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.smoke
    def test_caseid_1990423(self):
        """
       Inactive&normal 雨刮模式为2档IntHigh,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.sanity
    def test_caseid_1990422(self):
        """
        Inactive&dyno 雨刮模式为2档IntHigh,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
  
    @pytest.mark.full
    def test_caseid_1990421(self):
        """
        Inactive&crash 雨刮模式为2档IntHigh,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990420(self):
        """
        Inactive&factory雨刮模式为2档IntHigh,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990419(self):
        """
        Inactive&transport雨刮模式为2档IntHigh,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.smoke
    def test_caseid_1990418(self):
        """
       abandoned&normal 雨刮模式为2档IntHigh,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.sanity
    def test_caseid_1990417(self):
        """
        abandoned&dyno 雨刮模式为2档IntHigh,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
  
    @pytest.mark.full
    def test_caseid_1990416(self):
        """
        abandoned&crash 雨刮模式为2档IntHigh,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990415(self):
        """
        abandoned&factory雨刮模式为2档IntHigh,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990414(self):
        """
        abandoned&transport雨刮模式为2档IntHigh,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=1,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.smoke
    def test_caseid_1990388(self):
        """
        convience&normal 雨刮模式为3档Low,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=2,LvrInHiSpdPosn=1)

    @pytest.mark.sanity
    def test_caseid_1990387(self):
        """
        convience&dyno 雨刮模式为3档Low,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=2,LvrInHiSpdPosn=1)
  
    @pytest.mark.full
    def test_caseid_1990386(self):
        """
        convience&crash 雨刮模式为3档Low,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=2,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.full
    def test_caseid_1990385(self):
        """
        convience&factory雨刮模式为3档Low,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=2,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.full
    def test_caseid_1990384(self):
        """
        convience&transport雨刮模式为3档Low,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=2,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)



    @pytest.mark.smoke
    def test_caseid_1990393(self):
        """
       driving&normal 雨刮模式为3档Low,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=2,LvrInHiSpdPosn=1)

    @pytest.mark.sanity
    def test_caseid_1990392(self):
        """
        driving&dyno 雨刮模式为3档Low,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=2,LvrInHiSpdPosn=1)
  
    @pytest.mark.full
    def test_caseid_1990391(self):
        """
        driving&crash 雨刮模式为3档Low,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=2,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990390(self):
        """
        driving&factory雨刮模式为3档Low,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=2,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990389(self):
        """
        driving&transport雨刮模式为3档Low,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=2,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.smoke
    def test_caseid_1990398(self):
        """
       active&normal 雨刮模式为3档Low,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=2,LvrInHiSpdPosn=1)

    @pytest.mark.sanity
    def test_caseid_1990397(self):
        """
        active&dyno 雨刮模式为3档Low,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=2,LvrInHiSpdPosn=1)
  
    @pytest.mark.full
    def test_caseid_1990396(self):
        """
        active&crash 雨刮模式为3档Low,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=2,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990395(self):
        """
        active&factory雨刮模式为3档Low,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=2,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990394(self):
        """
        active&transport雨刮模式为3档Low,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=2,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.smoke
    def test_caseid_1990383(self):
        """
       Inactive&normal 雨刮模式为3档Low,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=2,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.sanity
    def test_caseid_1990382(self):
        """
        Inactive&dyno 雨刮模式为3档Low,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=2,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
  
    @pytest.mark.full
    def test_caseid_1990381(self):
        """
        Inactive&crash 雨刮模式为3档Low,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=2,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990380(self):
        """
        Inactive&factory雨刮模式为3档Low,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=2,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990379(self):
        """
        Inactive&transport雨刮模式为3档Low,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=2,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.smoke
    def test_caseid_1990378(self):
        """
       abandoned&normal 雨刮模式为3档Low,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=2,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.sanity
    def test_caseid_1990377(self):
        """
        abandoned&dyno 雨刮模式为3档Low,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=2,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
  
    @pytest.mark.full
    def test_caseid_1990376(self):
        """
        abandoned&crash 雨刮模式为3档Low,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=2,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990375(self):
        """
        abandoned&factory雨刮模式为3档Low,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=2,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990374(self):
        """
        abandoned&transport雨刮模式为3档Low,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=2,LvrInHiSpdPosn=1)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.smoke
    def test_caseid_1990353(self):
        """
        convience&normal 雨刮模式为4档High,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=2)

    @pytest.mark.sanity
    def test_caseid_1990352(self):
        """
        convience&dyno 雨刮模式为4档High,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=2)
  
    @pytest.mark.full
    def test_caseid_1990351(self):
        """
        convience&crash 雨刮模式为4档High,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=2)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990350(self):
        """
        convience&factory雨刮模式为4档High,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=2)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990349(self):
        """
        convience&transport雨刮模式为4档High,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=2)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.smoke
    def test_caseid_1990358(self):
        """
       driving&normal 雨刮模式为4档High,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=2)

    @pytest.mark.sanity
    def test_caseid_1990357(self):
        """
        driving&dyno 雨刮模式为4档High,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=2)
  
    @pytest.mark.full
    def test_caseid_1990356(self):
        """
        driving&crash 雨刮模式为4档High,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=2)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990355(self):
        """
        driving&factory雨刮模式为4档High,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=2)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990354(self):
        """
        driving&transport雨刮模式为4档High,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=2)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.smoke
    def test_caseid_1990363(self):
        """
       active&normal 雨刮模式为4档High,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=2)

    @pytest.mark.sanity
    def test_caseid_1990362(self):
        """
        active&dyno 雨刮模式为4档High,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=2)
  
    @pytest.mark.full
    def test_caseid_1990361(self):
        """
        active&crash 雨刮模式为4档High,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=2)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990360(self):
        """
        active&factory雨刮模式为4档High,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=2)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990359(self):
        """
        active&transport雨刮模式为4档High,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=2)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.smoke
    def test_caseid_1990373(self):
        """
       Inactive&normal 雨刮模式为4档High,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=2)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.sanity
    def test_caseid_1990372(self):
        """
        Inactive&dyno 雨刮模式为4档High,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=2)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
  
    @pytest.mark.full
    def test_caseid_1990371(self):
        """
        Inactive&crash 雨刮模式为4档High,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=2)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990370(self):
        """
        Inactive&factory雨刮模式为4档High,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=2)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990369(self):
        """
        Inactive&transport雨刮模式为4档High,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=2)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.smoke
    def test_caseid_1990368(self):
        """
       abandoned&normal 雨刮模式为4档High,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=2)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.sanity
    def test_caseid_1990367(self):
        """
        abandoned&dyno 雨刮模式为4档High,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=2)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
  
    @pytest.mark.full
    def test_caseid_1990366(self):
        """
        abandoned&crash 雨刮模式为4档High,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=2)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990365(self):
        """
        abandoned&factory雨刮模式为4档High,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=2)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.full
    def test_caseid_1990364(self):
        """
        abandoned&transport雨刮模式为4档High,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=2)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.smoke
    def test_caseid_1990338(self):
        """
        convience&normal 雨刮模式为auto档,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.sanity
    def test_caseid_1990337(self):
        """
        convience&dyno 雨刮模式为auto档,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

  
    @pytest.mark.full
    def test_caseid_1990336(self):
        """
        convience&crash 雨刮模式为auto档,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.full
    def test_caseid_1990335(self):
        """
        convience&factory雨刮模式为auto档,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.full
    def test_caseid_1990334(self):
        """
        convience&transport雨刮模式为auto档,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)



    @pytest.mark.smoke
    def test_caseid_1990343(self):
        """
       driving&normal 雨刮模式为auto档,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.sanity
    def test_caseid_1990342(self):
        """
        driving&dyno 雨刮模式为auto档,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

  
    @pytest.mark.full
    def test_caseid_1990341(self):
        """
        driving&crash 雨刮模式为auto档,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.full
    def test_caseid_1990340(self):
        """
        driving&factory雨刮模式为auto档,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.full
    def test_caseid_1990339(self):
        """
        driving&transport雨刮模式为auto档,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)



    @pytest.mark.smoke
    def test_caseid_1990348(self):
        """
       active&normal 雨刮模式为auto档,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.sanity
    def test_caseid_1990347(self):
        """
        active&dyno 雨刮模式为auto档,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

  
    @pytest.mark.full
    def test_caseid_1990346(self):
        """
        active&crash 雨刮模式为auto档,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.full
    def test_caseid_1990345(self):
        """
        active&factory雨刮模式为auto档,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.full
    def test_caseid_1990344(self):
        """
        active&transport雨刮模式为auto档,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)



    @pytest.mark.smoke
    def test_caseid_1990333(self):
        """
       Inactive&normal 雨刮模式为auto档,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.sanity
    def test_caseid_1990332(self):
        """
        Inactive&dyno 雨刮模式为auto档,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

  
    @pytest.mark.full
    def test_caseid_1990331(self):
        """
        Inactive&crash 雨刮模式为auto档,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.full
    def test_caseid_1990330(self):
        """
        Inactive&factory雨刮模式为auto档,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.full
    def test_caseid_1990329(self):
        """
        Inactive&transport雨刮模式为auto档,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.smoke
    def test_caseid_1990328(self):
        """
       abandoned&normal 雨刮模式为auto档,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.sanity
    def test_caseid_1990327(self):
        """
        abandoned&dyno 雨刮模式为auto档,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

  
    @pytest.mark.full
    def test_caseid_1990326(self):
        """
        abandoned&crash 雨刮模式为auto档,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.CRASH)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.full
    def test_caseid_1990325(self):
        """
        abandoned&factory雨刮模式为auto档,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.FACTORY)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)


    @pytest.mark.full
    def test_caseid_1990324(self):
        """
        abandoned&transport雨刮模式为auto档,检查WiprMotFrntLvrCmdNotSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    @pytest.mark.sanity
    def test_caseid_1990315(self):
        """
        convience&normal 雨刮模式为off,雨传感器关闭，雨刮洗涤关闭，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.Off)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)
      
    @pytest.mark.sanity
    def test_caseid_1990314(self):
        """
        convience&normal 雨刮模式为off,雨传感器激活，雨刮洗涤关闭，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",0)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)

    @pytest.mark.sanity
    def test_caseid_1990313(self):
        """
        driving&normal 雨刮模式为off,雨传感器关闭，雨刮洗涤关闭，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.Off)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)
      
    @pytest.mark.sanity
    def test_caseid_1990312(self):
        """
        driving&normal 雨刮模式为off,雨传感器激活，雨刮洗涤关闭，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",0)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)

    @pytest.mark.sanity
    def test_caseid_1990311(self):
        """
        active&normal 雨刮模式为off,雨传感器关闭，雨刮洗涤关闭，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.Off)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)
      
    @pytest.mark.sanity
    def test_caseid_1990310(self):
        """
        active&normal 雨刮模式为off,雨传感器激活，雨刮洗涤关闭，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",0)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)

    @pytest.mark.sanity
    def test_caseid_1990309(self):
        """
        Inactive&normal 雨刮模式为off,雨传感器关闭，雨刮洗涤关闭，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.Off)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)
      
    @pytest.mark.full
    def test_caseid_1990308(self):
        """
        反向用例，Inactive&normal 雨刮模式为off,雨传感器无法激活，雨刮洗涤关闭，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",0)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)

    @pytest.mark.sanity
    def test_caseid_1990307(self):
        """
        abandoned&normal 雨刮模式为off,雨传感器关闭，雨刮洗涤关闭，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.Off)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)
      
    @pytest.mark.full
    def test_caseid_1990306(self):
        """
        反向用例_abandoned&normal 雨刮模式为off,雨传感器无法激活，雨刮洗涤关闭，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",0)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)
    
    @pytest.mark.sanity
    def test_caseid_1990305(self):
        """
        convience&normal 雨传感器激活，雨传感器模式为direct模式，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",1)

    @pytest.mark.sanity
    def test_caseid_1990304(self):
        """
        convience&normal 雨刮模式为1档IntLow，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",1)

    @pytest.mark.sanity
    def test_caseid_1990303(self):
        """
        driving&normal 雨传感器激活，雨传感器模式为direct模式，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",1)

    @pytest.mark.sanity
    def test_caseid_1990302(self):
        """
        driving&normal 雨刮模式为1档IntLow，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",1)

    @pytest.mark.sanity
    def test_caseid_1990301(self):
        """
        active&normal 雨传感器激活，雨传感器模式为direct模式，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",1)

    @pytest.mark.sanity
    def test_caseid_1990300(self):
        """
        active&normal 雨刮模式为1档IntLow，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",1)

    @pytest.mark.full
    def test_caseid_1990299(self):
        """
        反向用例_Inactive&normal 雨传感器激活，雨传感器模式为direct模式，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)

    @pytest.mark.sanity
    def test_caseid_1990298(self):
        """
        Inactive&normal 雨刮模式为1档IntLow，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",1)

    @pytest.mark.full
    def test_caseid_1990297(self):
        """
        反向用例_abondoned&normal 雨传感器激活，雨传感器模式为direct模式，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)

    @pytest.mark.sanity
    def test_caseid_1990296(self):
        """
        abondoned&normal 雨刮模式为1档IntLow，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",1)

    @pytest.mark.full
    def test_caseid_1990295(self):
        """
        反向用例Inactive&normal 雨传感器无法激活，雨传感器模式为intervalt模式，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",2)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)

    @pytest.mark.sanity
    def test_caseid_1990294(self):
        """
        Inactive&normal 雨刮模式为2档IntHigh，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",2)

    @pytest.mark.full
    def test_caseid_1990293(self):
        """
        反向用例_abondoned&normal 雨传感器无法激活，雨传感器模式为interval模式，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",2)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)

    @pytest.mark.sanity
    def test_caseid_1990292(self):
        """
        abondoned&normal 雨刮模式为2档IntHigh，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",2)

    
    @pytest.mark.sanity
    def test_caseid_1990291(self):
        """
        driving&normal 雨传感器激活，雨传感器模式为interval模式，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",2)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",2)

    @pytest.mark.sanity
    def test_caseid_1990290(self):
        """
        driving&normal 雨刮模式为2档IntHigh，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",2)
    
    @pytest.mark.sanity
    def test_caseid_1990289(self):
        """
        active&normal 雨传感器激活，雨传感器模式为interval模式，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",2)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",2)

    @pytest.mark.sanity
    def test_caseid_1990288(self):
        """
        active&normal 雨刮模式为2档IntHigh，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",2)

    @pytest.mark.sanity
    def test_caseid_1990287(self):
        """
        convience&normal 雨传感器激活，雨传感器模式为interval模式，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",2)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",2)

    @pytest.mark.sanity
    def test_caseid_1990286(self):
        """
        convience&normal 雨刮模式为2档IntHigh，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",2)

    @pytest.mark.sanity
    def test_caseid_1990285(self):
        """
        convience&normal 雨传感器激活，雨传感器模式为continuous模式，擦拭速度为40~45 rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",2)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",3)

    @pytest.mark.sanity
    def test_caseid_1990284(self):
        """
        convience&normal 雨刮模式为3档Low，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",3)

    @pytest.mark.sanity
    def test_caseid_1990283(self):
        """
        driving&normal 雨传感器激活，雨传感器模式为continuous模式，擦拭速度为40~45 rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",2)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",3)

    @pytest.mark.sanity
    def test_caseid_1990282(self):
        """
        driving&normal 雨刮模式为3档Low，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",3)

    @pytest.mark.sanity
    def test_caseid_1990281(self):
        """
        active&normal 雨传感器激活，雨传感器模式为continuous模式，擦拭速度为40~45 rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",2)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",3)

    @pytest.mark.sanity
    def test_caseid_1990280(self):
        """
        active&normal 雨刮模式为3档Low，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",3)

    @pytest.mark.full
    def test_caseid_1990279(self):
        """
        反向用例_abandoned&normal 雨传感器无法激活，雨传感器模式为continuous模式，擦拭速度为40~45 rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",2)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)

    @pytest.mark.sanity
    def test_caseid_1990278(self):
        """
        abandoned&normal 雨刮模式为3档Low，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",3)

    @pytest.mark.full
    def test_caseid_1990277(self):
        """
        反向用例_inactive&normal 雨传感器激活，雨传感器模式为continuous模式，擦拭速度为40~45 rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",2)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)

    @pytest.mark.sanity
    def test_caseid_1990276(self):
        """
        abandoned&normal 雨刮模式为3档Low，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",3)

    @pytest.mark.full
    def test_caseid_1990275(self):
        """
        反向用例_abandoned&normal 雨传感器无法激活，雨传感器模式为continuous模式，擦拭速度为46~50rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",3)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",4)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)

    @pytest.mark.full
    def test_caseid_1990274(self):
        """
        反向用例_Inactive&normal 雨传感器无法激活，雨传感器模式为continuous模式，擦拭速度为46~50rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",3)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",4)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)

    @pytest.mark.sanity
    def test_caseid_1990273(self):
        """
        active&normal 雨传感器激活，雨传感器模式为continuous模式，擦拭速度为46~50rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",3)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",4)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",4)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",4)

    @pytest.mark.sanity
    def test_caseid_1990272(self):
        """
        driving&normal 雨传感器激活，雨传感器模式为continuous模式，擦拭速度为46~50rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",3)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",4)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",4)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",4)

    @pytest.mark.sanity
    def test_caseid_1990271(self):
        """
        convience&normal 雨传感器激活，雨传感器模式为continuous模式，擦拭速度为46~50rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",3)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",4)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",4)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",4)

    @pytest.mark.sanity
    def test_caseid_1990270(self):
        """
        driving&normal 雨传感器激活，雨传感器模式为continuous模式，擦拭速度为51~55rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",5)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",5)

    @pytest.mark.sanity
    def test_caseid_1990269(self):
        """
        active&normal 雨传感器激活，雨传感器模式为continuous模式，擦拭速度为51~55rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",5)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",5)

    @pytest.mark.sanity
    def test_caseid_1990268(self):
        """
        convience&normal 雨传感器激活，雨传感器模式为continuous模式，擦拭速度为51~55rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",5)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",5)

    @pytest.mark.full
    def test_caseid_1990267(self):
        """
        反向用例_inactive&normal 雨传感器无法激活，雨传感器模式为continuous模式，擦拭速度为51~55rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",5)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)

    @pytest.mark.full
    def test_caseid_1990266(self):
        """
        反向用例_abandoned&normal 雨传感器无法激活，雨传感器模式为continuous模式，擦拭速度为51~55rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",5)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)

    @pytest.mark.full
    def test_caseid_1990265(self):
        """
        反向用例_Inactive&normal 雨传感器无法激活，雨传感器模式为continuous模式，擦拭速度为56~60rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",6)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",7)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)

    @pytest.mark.full
    def test_caseid_1990264(self):
        """
        反向用例_abandoned&normal 雨传感器激活，雨传感器模式为continuous模式，擦拭速度为56~60rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",6)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",7)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)

    @pytest.mark.sanity
    def test_caseid_1990263(self):
        """
        driving&normal 雨传感器激活，雨传感器模式为continuous模式，擦拭速度为56~60rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",6)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",6)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",7)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",6)

    @pytest.mark.sanity
    def test_caseid_1990262(self):
        """
        active&normal 雨传感器激活，雨传感器模式为continuous模式，擦拭速度为56~60rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",6)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",6)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",7)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",6)

    @pytest.mark.sanity
    def test_caseid_1990261(self):
        """
        convience&normal 雨传感器激活，雨传感器模式为continuous模式，擦拭速度为56~60rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",6)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",6)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",7)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",6)

    @pytest.mark.sanity
    def test_caseid_1990260(self):
        """
        driving&normal 雨刮电机故障,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set("cem_lin1","WmmCem_Lin1Fr01","WiprMotErrSafe",2)
        self.bus_comm.check("backbonefr","CemBackBoneFr18",'WiprSysFailrDetdSafe',2)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",7)

    @pytest.mark.sanity
    def test_caseid_1990259(self):
        """
        convience&normal 雨刮电机故障,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set("cem_lin1","WmmCem_Lin1Fr01","WiprMotErrSafe",2)
        self.bus_comm.check("backbonefr","CemBackBoneFr18",'WiprSysFailrDetdSafe',2)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",7)

    @pytest.mark.sanity
    def test_caseid_1990258(self):
        """
        active&normal 雨刮电机故障,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set("cem_lin1","WmmCem_Lin1Fr01","WiprMotErrSafe",2)
        self.bus_comm.check("backbonefr","CemBackBoneFr18",'WiprSysFailrDetdSafe',2)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",7)

    @pytest.mark.sanity
    def test_caseid_1990257(self):
        """
        inactive&normal 雨刮电机故障,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set("cem_lin1","WmmCem_Lin1Fr01","WiprMotErrSafe",2)
        self.bus_comm.check("backbonefr","CemBackBoneFr18",'WiprSysFailrDetdSafe',2)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",7)

    @pytest.mark.sanity
    def test_caseid_1990256(self):
        """
        abandoned&normal 雨刮电机故障,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set("cem_lin1","WmmCem_Lin1Fr01","WiprMotErrSafe",2)
        self.bus_comm.check("backbonefr","CemBackBoneFr18",'WiprSysFailrDetdSafe',2)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",7)

    @pytest.mark.sanity
    def test_caseid_1990585(self):
        """
        convience&dyno 雨刮模式为off,雨传感器关闭，雨刮洗涤关闭，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.Off)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)
      
    @pytest.mark.sanity
    def test_caseid_1990586(self):
        """
        convience&dyno 雨刮模式为off,雨传感器激活，雨刮洗涤关闭，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",0)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)

    @pytest.mark.sanity
    def test_caseid_1990587(self):
        """
        driving&dyno 雨刮模式为off,雨传感器关闭，雨刮洗涤关闭，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.Off)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)
      
    @pytest.mark.sanity
    def test_caseid_1990588(self):
        """
        driving&dyno 雨刮模式为off,雨传感器激活，雨刮洗涤关闭，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",0)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)

    @pytest.mark.sanity
    def test_caseid_1990589(self):
        """
        active&dyno 雨刮模式为off,雨传感器关闭，雨刮洗涤关闭，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.Off)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)
      
    @pytest.mark.sanity
    def test_caseid_1990590(self):
        """
        active&dyno 雨刮模式为off,雨传感器激活，雨刮洗涤关闭，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",0)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)

    @pytest.mark.sanity
    def test_caseid_1990591(self):
        """
        Inactive&dyno 雨刮模式为off,雨传感器关闭，雨刮洗涤关闭，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.Off)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)
      
    @pytest.mark.full
    def test_caseid_1990592(self):
        """
        反向用例，Inactive&dyno 雨刮模式为off,雨传感器无法激活，雨刮洗涤关闭，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",0)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)

    @pytest.mark.sanity
    def test_caseid_1990593(self):
        """
        abandoned&dyno 雨刮模式为off,雨传感器关闭，雨刮洗涤关闭，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.Off)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)
      
    @pytest.mark.full
    def test_caseid_1990594(self):
        """
        反向用例_abandoned&dyno 雨刮模式为off,雨传感器无法激活，雨刮洗涤关闭，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",0)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)
    
    @pytest.mark.sanity
    def test_caseid_1990595(self):
        """
        convience&dyno 雨传感器激活，雨传感器模式为direct模式，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",1)

    @pytest.mark.sanity
    def test_caseid_1990596(self):
        """
        convience&dyno 雨刮模式为1档IntLow，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",1)

    @pytest.mark.sanity
    def test_caseid_1990597(self):
        """
        driving&dyno 雨传感器激活，雨传感器模式为direct模式，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",1)

    @pytest.mark.sanity
    def test_caseid_1990598(self):
        """
        driving&dyno 雨刮模式为1档IntLow，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",1)

    @pytest.mark.sanity
    def test_caseid_1990599(self):
        """
        active&dyno 雨传感器激活，雨传感器模式为direct模式，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",1)

    @pytest.mark.sanity
    def test_caseid_1990600(self):
        """
        active&dyno 雨刮模式为1档IntLow，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",1)

    @pytest.mark.full
    def test_caseid_1990601(self):
        """
        反向用例_Inactive&dyno 雨传感器激活，雨传感器模式为direct模式，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)

    @pytest.mark.sanity
    def test_caseid_1990602(self):
        """
        Inactive&dyno 雨刮模式为1档IntLow，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",1)

    @pytest.mark.full
    def test_caseid_1990603(self):
        """
        反向用例_abondoned&dyno 雨传感器激活，雨传感器模式为direct模式，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)

    @pytest.mark.sanity
    def test_caseid_1990604(self):
        """
        abondoned&dyno 雨刮模式为1档IntLow，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",1)

    @pytest.mark.full
    def test_caseid_1990605(self):
        """
        反向用例Inactive&dyno 雨传感器无法激活，雨传感器模式为intervalt模式，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",2)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)

    @pytest.mark.sanity
    def test_caseid_1990606(self):
        """
        Inactive&dyno 雨刮模式为2档IntHigh，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",2)

    @pytest.mark.full
    def test_caseid_1990607(self):
        """
        反向用例_abondoned&dyno 雨传感器无法激活，雨传感器模式为interval模式，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",2)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)

    @pytest.mark.sanity
    def test_caseid_1990608(self):
        """
        abondoned&dyno 雨刮模式为2档IntHigh，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",2)

    
    @pytest.mark.sanity
    def test_caseid_1990609(self):
        """
        driving&dyno 雨传感器激活，雨传感器模式为interval模式，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",2)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",2)

    @pytest.mark.sanity
    def test_caseid_1990610(self):
        """
        driving&dyno 雨刮模式为2档IntHigh，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",2)
    
    @pytest.mark.sanity
    def test_caseid_1990611(self):
        """
        active&dyno 雨传感器激活，雨传感器模式为interval模式，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",2)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",2)

    @pytest.mark.sanity
    def test_caseid_1990612(self):
        """
        active&dyno 雨刮模式为2档IntHigh，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",2)

    @pytest.mark.sanity
    def test_caseid_1990613(self):
        """
        convience&dyno 雨传感器激活，雨传感器模式为interval模式，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",2)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",2)

    @pytest.mark.sanity
    def test_caseid_1990614(self):
        """
        convience&dyno 雨刮模式为2档IntHigh，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",2)

    @pytest.mark.sanity
    def test_caseid_1990615(self):
        """
        convience&dyno 雨传感器激活，雨传感器模式为continuous模式，擦拭速度为40~45 rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",2)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",3)

    @pytest.mark.sanity
    def test_caseid_1990616(self):
        """
        convience&dyno 雨刮模式为3档Low，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",3)

    @pytest.mark.sanity
    def test_caseid_1990617(self):
        """
        driving&dyno 雨传感器激活，雨传感器模式为continuous模式，擦拭速度为40~45 rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",2)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",3)

    @pytest.mark.sanity
    def test_caseid_1990618(self):
        """
        driving&dyno 雨刮模式为3档Low，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",3)

    @pytest.mark.sanity
    def test_caseid_1990619(self):
        """
        active&dyno 雨传感器激活，雨传感器模式为continuous模式，擦拭速度为40~45 rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",2)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",3)

    @pytest.mark.sanity
    def test_caseid_1990620(self):
        """
        active&dyno 雨刮模式为3档Low，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",3)

    @pytest.mark.full
    def test_caseid_1990621(self):
        """
        反向用例_abandoned&dyno 雨传感器无法激活，雨传感器模式为continuous模式，擦拭速度为40~45 rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",2)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)

    @pytest.mark.sanity
    def test_caseid_1990622(self):
        """
        abandoned&dyno 雨刮模式为3档Low，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",3)

    @pytest.mark.full
    def test_caseid_1990623(self):
        """
        反向用例_inactive&dyno 雨传感器激活，雨传感器模式为continuous模式，擦拭速度为40~45 rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",2)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)

    @pytest.mark.sanity
    def test_caseid_1990624(self):
        """
        abandoned&dyno 雨刮模式为3档Low，检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",3)

    @pytest.mark.full
    def test_caseid_1990625(self):
        """
        反向用例_abandoned&dyno 雨传感器无法激活，雨传感器模式为continuous模式，擦拭速度为46~50rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",3)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",4)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)

    @pytest.mark.full
    def test_caseid_1990626(self):
        """
        反向用例_Inactive&dyno 雨传感器无法激活，雨传感器模式为continuous模式，擦拭速度为46~50rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",3)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",4)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)

    @pytest.mark.sanity
    def test_caseid_1990627(self):
        """
        active&dyno 雨传感器激活，雨传感器模式为continuous模式，擦拭速度为46~50rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",3)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",4)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",4)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",4)

    @pytest.mark.sanity
    def test_caseid_1990628(self):
        """
        driving&dyno 雨传感器激活，雨传感器模式为continuous模式，擦拭速度为46~50rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",3)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",4)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",4)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",4)

    @pytest.mark.sanity
    def test_caseid_1990629(self):
        """
        convience&dyno 雨传感器激活，雨传感器模式为continuous模式，擦拭速度为46~50rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",3)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",4)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",4)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",4)

    @pytest.mark.sanity
    def test_caseid_1990630(self):
        """
        driving&dyno 雨传感器激活，雨传感器模式为continuous模式，擦拭速度为51~55rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",5)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",5)

    @pytest.mark.sanity
    def test_caseid_1990631(self):
        """
        active&dyno 雨传感器激活，雨传感器模式为continuous模式，擦拭速度为51~55rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",5)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",5)

    @pytest.mark.sanity
    def test_caseid_1990632(self):
        """
        convience&dyno 雨传感器激活，雨传感器模式为continuous模式，擦拭速度为51~55rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",5)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",5)

    @pytest.mark.full
    def test_caseid_1990633(self):
        """
        反向用例_inactive&dyno 雨传感器无法激活，雨传感器模式为continuous模式，擦拭速度为51~55rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",5)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)

    @pytest.mark.full
    def test_caseid_1990634(self):
        """
        反向用例_abandoned&dyno 雨传感器无法激活，雨传感器模式为continuous模式，擦拭速度为51~55rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",5)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)

    @pytest.mark.full
    def test_caseid_1990635(self):
        """
        反向用例_Inactive&dyno 雨传感器无法激活，雨传感器模式为continuous模式，擦拭速度为56~60rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",6)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",7)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)

    @pytest.mark.full
    def test_caseid_1990636(self):
        """
        反向用例_abandoned&dyno 雨传感器激活，雨传感器模式为continuous模式，擦拭速度为56~60rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",6)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",7)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",0)

    @pytest.mark.sanity
    def test_caseid_1990637(self):
        """
        driving&dyno 雨传感器激活，雨传感器模式为continuous模式，擦拭速度为56~60rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",6)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",6)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",7)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",6)

    @pytest.mark.sanity
    def test_caseid_1990638(self):
        """
        active&dyno 雨传感器激活，雨传感器模式为continuous模式，擦拭速度为56~60rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",6)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",6)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",7)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",6)

    @pytest.mark.sanity
    def test_caseid_1990639(self):
        """
        convience&dyno 雨传感器激活，雨传感器模式为continuous模式，擦拭速度为56~60rpm,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","WipgAutFrntMod",3)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",6)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",6)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","AutWinWipgCmd",7)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",6)

    @pytest.mark.sanity
    def test_caseid_1990640(self):
        """
        driving&dyno 雨刮电机故障,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.bus_comm.set("cem_lin1","WmmCem_Lin1Fr01","WiprMotErrSafe",2)
        self.bus_comm.check("backbonefr","CemBackBoneFr18",'WiprSysFailrDetdSafe',2)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",7)

    @pytest.mark.sanity
    def test_caseid_1990641(self):
        """
        convience&dyno 雨刮电机故障,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set("cem_lin1","WmmCem_Lin1Fr01","WiprMotErrSafe",2)
        self.bus_comm.check("backbonefr","CemBackBoneFr18",'WiprSysFailrDetdSafe',2)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",7)

    @pytest.mark.sanity
    def test_caseid_1990642(self):
        """
        active&dyno 雨刮电机故障,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.bus_comm.set("cem_lin1","WmmCem_Lin1Fr01","WiprMotErrSafe",2)
        self.bus_comm.check("backbonefr","CemBackBoneFr18",'WiprSysFailrDetdSafe',2)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",7)

    @pytest.mark.sanity
    def test_caseid_1990643(self):
        """
        inactive&dyno 雨刮电机故障,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set("cem_lin1","WmmCem_Lin1Fr01","WiprMotErrSafe",2)
        self.bus_comm.check("backbonefr","CemBackBoneFr18",'WiprSysFailrDetdSafe',2)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",7)

    @pytest.mark.sanity
    def test_caseid_1990644(self):
        """
        abandoned&dyno 雨刮电机故障,检查WipgInfoWipgSpdInfo
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set("cem_lin1","WmmCem_Lin1Fr01","WiprMotErrSafe",2)
        self.bus_comm.check("backbonefr","CemBackBoneFr18",'WiprSysFailrDetdSafe',2)
        self.bus_comm.check("backbonefr","CemBackBoneFr07","WipgInfoWipgSpdInfo",7)

    @pytest.mark.full
    def test_caseid_1990773(self):
        """
        反向用例，ccp 503 != 02 ,雨刮灵敏度设置
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.sd_tester.write_ccp({503:0x01})
        for i in [WiperMode.Off,WiperMode.SingleWipe,WiperMode.IntLow,WiperMode.IntHigh,WiperMode.Low,WiperMode.High,WiperMode.Auto,WiperMode.Error]:
            logger.info(f"当前雨刮模式为 {i}")
            self.soa.hmi_set_wiper_mode(WiperPos.Front,i)
            self.bus_comm.check("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 6)

    @pytest.mark.full
    def test_caseid_1987075(self):
        """
        设置雨刮模式off档到1档到自动档_触发雨传感器灵敏度信号值变化
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.sd_tester.write_ccp({503:0x02})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.check("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 6)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.check("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 3)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 5)

    @pytest.mark.full
    def test_caseid_1987074(self):
        """
        设置雨刮模式_单刮到1档到auto档_触发雨传感器灵敏度信号值变化
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.sd_tester.write_ccp({503:0x02})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.bus_comm.check("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 6)
        sleep(0.5)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.check("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 3)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 5)

    @pytest.mark.full
    def test_caseid_1987073(self):
        """
        设置雨刮模式_1档到auto档到off档_触发雨传感器灵敏度信号值变化
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.sd_tester.write_ccp({503:0x02})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.check("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 3)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 5)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.check("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 6)

    @pytest.mark.smoke
    def test_caseid_1987072(self):
        """
        设置雨刮模式_触发雨传感器灵敏度信号值变化
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.sd_tester.write_ccp({503:0x02})
        for i in [WiperMode.Off,WiperMode.SingleWipe,WiperMode.IntLow,WiperMode.IntHigh,WiperMode.Low,WiperMode.High,WiperMode.Auto,WiperMode.Error]:
            sleep(0.5)
            if i == WiperMode.IntLow:
                self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
                self.bus_comm.check("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 3)
            elif i == WiperMode.Auto:
                self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
                self.bus_comm.check("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 5)
            else:
                self.soa.hmi_set_wiper_mode(WiperPos.Front,i)
                self.bus_comm.check("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 6)

    @pytest.mark.full
    def test_caseid_1987071(self):
        """
        设置雨刮模式_2档到auto档到off档_触发雨传感器灵敏度信号值变化
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.sd_tester.write_ccp({503:0x02})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.check("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 6)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 5)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.check("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 6)


    @pytest.mark.full
    def test_caseid_1987070(self):
        """
        设置雨刮模式_3档到auto档到off档_触发雨传感器灵敏度信号值变化
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.sd_tester.write_ccp({503:0x02})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.check("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 6)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 5)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.check("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 6)

    @pytest.mark.full
    def test_caseid_1987070(self):
        """
        设置雨刮模式_4档到auto档到error_触发雨传感器灵敏度信号值变化
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.sd_tester.write_ccp({503:0x02})
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.bus_comm.check("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 6)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 5)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Error)
        self.bus_comm.check("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 6)