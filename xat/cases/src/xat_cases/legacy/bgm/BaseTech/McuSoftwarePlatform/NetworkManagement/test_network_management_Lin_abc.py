#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_steerwheel_ctrl.py
@Author      : hui.zhao@jiduauto.com
@Time        : 2023/11/21 11:30
@Description: BGM车控车方向盘功能
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


@allure.feature("网络管理")
@allure.story("LIN唤醒测试")
class TestNetworkManagementLin(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["SeatService_client","KeyService_client","WindowAppService_client","CentralLockService_client", "GloveBoxService_client"])
        sleep(2)
        self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x4})
        self.bus_comm.set_Hv_sys_relay_sts(HvSysRelaySts.Close)

    def before_each_func(self, ecu):
        pass

    def after_each_func(self, ecu):
        self.bus_comm.ipdu.reset_check_results()
        sleep(5)

    def after_class(self, ecu):
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        try:
            self.mix.network_recover_bgm()
            sleep(20)
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
        
    @allure.title("LIN1_Active_WshngCycActv唤醒_108199")
    @pytest.mark.smoke
    def test_lin_networkmanagement_lin1_caseid_108199(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        sleep(30)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN1,sts=BusSendSts.Sleep)
        self.mix.rain_auto_windows()
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN1,sts=BusSendSts.Awakeup) 

    @allure.title("LIN1_usgmod_Inactive to Convenience_108206")
    @pytest.mark.smoke
    def test_lin_networkmanagement_lin1_caseid_108206(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN1,sts=BusSendSts.Sleep)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE)
        self.mix.check_lin_wakeup_time("cem_lin1","CemCem_Lin1Fr01", "IntrMirrCmdDrvrSide",1,timeout=12)
    
    @allure.title("LIN1 inactive触发雨天自动关窗唤醒_108209")
    @pytest.mark.smoke
    def test_lin_networkmanagement_lin1_caseid_108209(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        sleep(30)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN1,sts=BusSendSts.Sleep)
        self.mix.rain_auto_windows()
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN1,sts=BusSendSts.Awakeup) 

    @allure.title("LIN1_休眠后_Abandoned_雨刮检测唤醒_109712")
    @pytest.mark.smoke
    def test_lin_networkmanagement_lin1_caseid_109712(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        sleep(30)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN1,sts=BusSendSts.Sleep)
        self.mix.rain_auto_windows()
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN1,sts=BusSendSts.Awakeup) 
    
    @allure.title("LIN1_BGM唤醒电平_Lin1Schedule01唤醒_108210")
    @pytest.mark.smoke
    def test_lin_networkmanagement_lin1_caseid_108210(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN1,sts=BusSendSts.Sleep)
        t0 = time.time()
        self.bus_comm.lin_send_pwm(lin_bus=LinChannel.LIN1)
        t1 = time.time()
        self.bus_comm.check_lin_bus_awakeup_result(lin_bus=LinChannel.LIN1,trig_start = t0, trig_stop = t1)

    @allure.title("LIN1_休眠后_Inactive_车速唤醒_109665")
    @pytest.mark.smoke
    def test_lin_networkmanagement_lin1_caseid_109665(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN1,sts=BusSendSts.Sleep)
        with allure.step("设置车速>7km/h"):
            self.bus_comm.set_vehspd_and_qf(1792,VehSpdQf(2))
            self.bus_comm.get_vehicle_speed()
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN1,sts=BusSendSts.Awakeup)
        with allure.step("设置车速 = 0km/h"):
            self.bus_comm.set_vehspd_and_qf(0,VehSpdQf(2))
            self.bus_comm.get_vehicle_speed()
        sleep(10)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN1,sts=BusSendSts.Sleep)

    @allure.title("LIN1_休眠后_Abandoned_车速唤醒_109713")
    @pytest.mark.smoke
    def test_lin_networkmanagement_lin1_caseid_109713(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN1,sts=BusSendSts.Sleep)
        with allure.step("设置车速>7km/h"):
            self.bus_comm.set_vehspd_and_qf(1792,VehSpdQf(2))
            self.bus_comm.get_vehicle_speed()
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN1,sts=BusSendSts.Awakeup)
        with allure.step("设置车速 = 0km/h"):
            self.bus_comm.set_vehspd_and_qf(0,VehSpdQf(2))
            self.bus_comm.get_vehicle_speed()
        sleep(10)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN1,sts=BusSendSts.Sleep)

    @allure.title("LIN4_休眠后_Abandoned_车速唤醒_109683")
    @pytest.mark.smoke
    def test_lin_networkmanagement_lin1_caseid_109683(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN4,sts=BusSendSts.Sleep)
        with allure.step("设置车速>7km/h"):
            self.bus_comm.set_vehspd_and_qf(1792,VehSpdQf(2))
            self.bus_comm.get_vehicle_speed()
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN4,sts=BusSendSts.Awakeup)
        with allure.step("设置车速 = 0km/h"):
            self.bus_comm.set_vehspd_and_qf(0,VehSpdQf(2))
            self.bus_comm.get_vehicle_speed()
        sleep(10)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN4,sts=BusSendSts.Sleep)
 
    @allure.title("LIN1_usgmod_Driving to Abandoned_109667")
    @pytest.mark.smoke
    def test_lin_networkmanagement_lin1_caseid_109667(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN1,sts=BusSendSts.Awakeup)
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN1,sts=BusSendSts.Sleep)

    @allure.title("LIN1_诊断激活_Lin1PartNrSerlNrSchedule_109675")
    @pytest.mark.smoke
    def test_lin_networkmanagement_lin1_caseid_109675(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN1,sts=BusSendSts.Sleep)
        self.sd_tester.send_data([0x22, 0xF1, 0xBB])
        #TODO 等新增检查调度表接口后再check
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN1,sts=BusSendSts.Awakeup)

    @allure.title("LIN2_BGM唤醒电平_Lin2Schedule01唤醒_1983477")
    @pytest.mark.smoke
    def test_lin_networkmanagement_lin2_caseid_1983477(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN2,sts=BusSendSts.Sleep)
        t0 = time.time()
        self.bus_comm.lin_send_pwm(lin_bus=LinChannel.LIN2)
        t1 = time.time()
        self.bus_comm.check_lin_bus_awakeup_result(lin_bus=LinChannel.LIN2,trig_start = t0, trig_stop = t1)

    @allure.title("LIN3_BGM唤醒_Lin3SnsrCmdAndSts唤醒_109657")
    @pytest.mark.smoke
    def test_lin_networkmanagement_lin3_caseid_109657(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN3,sts=BusSendSts.Sleep)
        t0 = time.time()
        self.bus_comm.lin_send_pwm(lin_bus=LinChannel.LIN3)
        t1 = time.time()
        self.bus_comm.check_lin_bus_awakeup_result(lin_bus=LinChannel.LIN3,trig_start = t0, trig_stop = t1)

    @allure.title("LIN4_BGM唤醒电平_Lin4Schedule01唤醒_1983478")
    @pytest.mark.smoke
    def test_lin_networkmanagement_lin4_caseid_1983478(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN4,sts=BusSendSts.Sleep)
        t0 = time.time()
        self.bus_comm.lin_send_pwm(lin_bus=LinChannel.LIN4)
        t1 = time.time()
        self.bus_comm.check_lin_bus_awakeup_result(lin_bus=LinChannel.LIN4,trig_start = t0, trig_stop = t1)   

    @allure.title("LIN5_BGM唤醒电平_Lin5Schedule01唤醒_1983479")
    @pytest.mark.smoke
    def test_lin_networkmanagement_lin5_caseid_1983479(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN5,sts=BusSendSts.Sleep)
        t0 = time.time()
        self.bus_comm.lin_send_pwm(lin_bus=LinChannel.LIN5)
        t1 = time.time()
        self.bus_comm.check_lin_bus_awakeup_result(lin_bus=LinChannel.LIN5,trig_start = t0, trig_stop = t1)

    # @pytest.mark.smoke
    # @pytest.mark.V_1_3
    # def test_lin_networkmanagement_caseid_1983480(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
    #     sleep(15)
    #     self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN6,sts=BusSendSts.Sleep)
    #     t0 = time.time()
    #     self.bus_comm.lin_send_pwm(lin_bus=LinChannel.LIN6)
    #     t1 = time.time()
    #     self.bus_comm.check_lin_bus_awakeup_result(lin_bus=LinChannel.LIN6,trig_start = t0, trig_stop = t1)

    @allure.title("LIN1 inactive 切换abonedone 唤醒_1960054")
    @pytest.mark.smoke
    def test_lin_networkmanagement_lin1_caseid_1960054(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN1,sts=BusSendSts.Sleep)
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.mix.check_lin_wakeup_time("cem_lin1","CemCem_Lin1Fr01","IntrMirrCmdDrvrSide",1,timeout=3)
    
    @allure.title("LIN1 abonedone 切换inactive 唤醒_1960053")
    @pytest.mark.smoke
    def test_lin_networkmanagement_lin1_caseid_1960053(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN1,sts=BusSendSts.Sleep)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.mix.check_lin_wakeup_time("cem_lin1","CemCem_Lin1Fr01","IntrMirrCmdDrvrSide",1,timeout=7.5)   
    
    @allure.title("LIN1 abonedone 切换CONVENIENCE唤醒_1985166")
    @pytest.mark.smoke
    def test_lin_networkmanagement_lin1_caseid_1985166(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN1,sts=BusSendSts.Sleep)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE)
        self.mix.check_lin_wakeup_time("cem_lin1","CemCem_Lin1Fr01", "IntrMirrCmdDrvrSide",1,timeout=12)

    @allure.title("LIN1 abonedone 切换ACTIVE唤醒_109658")
    @pytest.mark.smoke
    def test_lin_networkmanagement_lin1_caseid_109658(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN1,sts=BusSendSts.Sleep)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE)
        self.mix.check_lin_wakeup_time("cem_lin1","CemCem_Lin1Fr01", "IntrMirrCmdDrvrSide",1,timeout=12)

    @allure.title("LIN1 abonedone 切换DRIVING唤醒_1985167")
    @pytest.mark.smoke
    def test_lin_networkmanagement_lin1_caseid_1985167(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN1,sts=BusSendSts.Sleep)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING)
        self.mix.check_lin_wakeup_time("cem_lin1","CemCem_Lin1Fr01", "IntrMirrCmdDrvrSide",1,timeout=12)
    
    @allure.title("LIN1 inactive 切换ACTIVE唤醒_1985168")
    @pytest.mark.smoke
    def test_lin_networkmanagement_lin1_caseid_1985168(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN1,sts=BusSendSts.Sleep)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE)
        self.mix.check_lin_wakeup_time("cem_lin1","CemCem_Lin1Fr01", "IntrMirrCmdDrvrSide",1,timeout=12)

    @allure.title("LIN1 inactive 切换DRIVING唤醒_109677")
    @pytest.mark.smoke
    def test_lin_networkmanagement_lin1_caseid_109677(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN1,sts=BusSendSts.Sleep)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING)
        self.mix.check_lin_wakeup_time("cem_lin1","CemCem_Lin1Fr01", "IntrMirrCmdDrvrSide",1,timeout=12)

    @allure.title("LIN2 Abandoned 切换Inactive唤醒_109684")
    @pytest.mark.smoke
    def test_lin_networkmanagement_lin2_caseid_109684(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN2,sts=BusSendSts.Sleep)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.mix.check_lin_wakeup_time("cem_lin2","CemCem_Lin2Fr07","AIInteractionLampLeftY1",0,timeout=12)

    @allure.title("LIN2 Abandoned 切换CONVENIENCE唤醒_109661")
    @pytest.mark.smoke
    def test_lin_networkmanagement_lin2_caseid_109661(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN2,sts=BusSendSts.Sleep)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE)
        self.mix.check_lin_wakeup_time("cem_lin2","CemCem_Lin2Fr07","AIInteractionLampLeftY1",0,timeout=12)

    # @pytest.mark.smoke
    # def test_lin_networkmanagement_Lin2_abonedone_caseid_109672(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
    #     sleep(15)
    #     self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN2,sts=BusSendSts.Sleep)
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE)
    #     self.mix.check_lin_wakeup_time("cem_lin2","CemCem_Lin2Fr07","AIInteractionLampLeftY1",0,timeout=12)

    @allure.title("LIN2 Abandoned 切换DRIVING唤醒_109662")
    @pytest.mark.smoke
    def test_lin_networkmanagement_lin2_caseid_109662(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN2,sts=BusSendSts.Sleep)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING)
        self.mix.check_lin_wakeup_time("cem_lin2","CemCem_Lin2Fr07","AIInteractionLampLeftY1",0,timeout=12)
        self.bus_comm.set_vehspd(100)

    @allure.title("LIN3 Abandoned 切换Inactive唤醒_109682")
    @pytest.mark.smoke
    def test_lin_networkmanagement_Lin3_abonedone2inactive_caseid_109682(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN3,sts=BusSendSts.Sleep)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.mix.check_lin_wakeup_time("cem_lin3","CemCem_Lin3Fr05","IntrLiGen2RoofDimSpeed",'any',timeout=12)

    @allure.title("LIN3 not Abandoned 保持唤醒_109676")
    @pytest.mark.smoke
    def test_lin_networkmanagement_lin3_inactive_caseid_109676(self):
        with allure.step("set UM: Inactive, LIN3 Awakeup"):
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
            sleep(5)
            self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN3,sts=BusSendSts.Awakeup)
        with allure.step("change UM: CONVENIENCE, LIN3 Awakeup"):
            self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE)
            sleep(5)
            self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN3,sts=BusSendSts.Awakeup)
        with allure.step("change UM: ACTIVE, LIN3 Awakeup"):
            self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE)
            sleep(5)
            self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN3,sts=BusSendSts.Awakeup)
        with allure.step("change UM: DRIVING, LIN3 Awakeup"):
            self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING)
            sleep(5)
            self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN3,sts=BusSendSts.Awakeup)

    @allure.title("LIN3 Abandoned 切换CONVENIENCE唤醒_109668")
    @pytest.mark.smoke
    def test_lin_networkmanagement_Lin3_abonedone2convenience_caseid_109668(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN3,sts=BusSendSts.Sleep)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE)
        self.mix.check_lin_wakeup_time("cem_lin3","CemCem_Lin3Fr05","IntrLiGen2RoofDimSpeed",'any',timeout=12)

    @allure.title("LIN3 Abandoned 切换ACTIVE唤醒_109680")
    @pytest.mark.smoke
    def test_lin_networkmanagement_Lin3_abonedone2active_caseid_109680(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN3,sts=BusSendSts.Sleep)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE)
        self.mix.check_lin_wakeup_time("cem_lin3","CemCem_Lin3Fr05","IntrLiGen2RoofDimSpeed",'any',timeout=12)

    @allure.title("LIN3 Abandoned 切换DRIVING唤醒")
    @pytest.mark.smoke
    def test_lin_networkmanagement_Lin3_abonedone2driving_caseid_109673(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN3,sts=BusSendSts.Sleep)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING)
        self.mix.check_lin_wakeup_time("cem_lin3","CemCem_Lin3Fr05","IntrLiGen2RoofDimSpeed",'any',timeout=12) 

    @allure.title("LIN4 Abandoned 切换Inactive唤醒")
    @pytest.mark.smoke
    def test_lin_networkmanagement_Lin4_abonedone2inactive_caseid_109656(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN4,sts=BusSendSts.Sleep)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.mix.check_lin_wakeup_time("cem_lin4","CemCem_Lin4Fr02","DisAdjMov",0,timeout=12)

    @allure.title("LIN4 Abandoned 切换CONVENIENCE唤醒_109670")
    @pytest.mark.smoke
    def test_lin_networkmanagement_Lin4_abonedone2convenience_caseid_109670(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN4,sts=BusSendSts.Sleep)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE)
        self.mix.check_lin_wakeup_time("cem_lin4","CemCem_Lin4Fr02","DisAdjMov",0,timeout=12)

    @allure.title("LIN4 Abandoned 切换active唤醒_109669")
    @pytest.mark.smoke
    def test_lin_networkmanagement_Lin4_abonedone2active_caseid_109669(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN4,sts=BusSendSts.Sleep)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE)
        self.mix.check_lin_wakeup_time("cem_lin4","CemCem_Lin4Fr02","DisAdjMov",0,timeout=12)


    @allure.title("LIN4 Abandoned 切换DRIVING唤醒")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109669?projectId=46',name='Can_Lin Pdu Case Example 109656',)
    @pytest.mark.smoke
    @pytest.mark.full
    def test_lin_networkmanagement_Lin4_abonedone2driving_caseid_116037(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN4,sts=BusSendSts.Sleep)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING)
        self.mix.check_lin_wakeup_time("cem_lin4","CemCem_Lin4Fr02","DisAdjMov",0,timeout=12)
    
    @allure.title("LIN5 Abandoned 切换Convenience 休眠_109647 ")
    @pytest.mark.smoke
    def test_lin_networkmanagement_lin5_caseid_109647(self):
        self.io.bgm_diag_line_down()
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN5,sts=BusSendSts.Sleep)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.mix.check_lin_wakeup_time("cem_lin5","CemCem_Lin5Fr01","OrdinaryAmbientLightFrontLeftBlue",0,timeout=12)
        self.io.bgm_diag_line_up()


    # @allure.title("LIN6_usgmod_Abandon to Inactive_108625")
    # @pytest.mark.smoke
    # def test_lin_networkmanagement_Lin6_abonedone2incative_caseid_108625(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
    #     sleep(15)
    #     self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
    #     sleep(15)
    #     self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN6,sts=BusSendSts.Awakeup)


    # @allure.title("LIN6_usgmod_abandoned to Convenience_108624")
    # @pytest.mark.smoke
    # def test_lin_networkmanagement_Lin6_abonedone2convenience_caseid_108624(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
    #     sleep(15)
    #     self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
    #     sleep(15)
    #     self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN6,sts=BusSendSts.Awakeup)


    # @allure.title("LIN6 Abandoned 切换Inactive及以上 唤醒")
    # @allure.testcase(
    #     'https://jama.jiduauto.com/perspective.req#/testCases/109669?projectId=46',name='Can_Lin Pdu Case Example 108625',)
    # @pytest.mark.smoke
    # @pytest.mark.V_1_3
    # def test_lin_networkmanagement_Lin6_abonedone2active_caseid_109831(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
    #     sleep(15)
    #     self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN6,sts=BusSendSts.Sleep)
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE)
    #     self.mix.check_lin_wakeup_time("cem_lin4","CemCem_Lin4Fr02","DisAdjMov",0,timeout=12)


    # @allure.title("LIN6 Abandoned 切换Inactive及以上 唤醒")
    # @allure.testcase(
    #     'https://jama.jiduauto.com/perspective.req#/testCases/109669?projectId=46',name='Can_Lin Pdu Case Example 108625',)
    # @pytest.mark.smoke
    # @pytest.mark.V_1_3
    # def test_lin_networkmanagement_Lin6_abonedone2driving_caseid_116031(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
    #     sleep(15)
    #     self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN6,sts=BusSendSts.Sleep)
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING)
    #     self.mix.check_lin_wakeup_time("cem_lin4","CemCem_Lin4Fr02","DisAdjMov",0,timeout=12)   

    @allure.title("LIN6_usgmod_abandoned to Active_109831")
    @pytest.mark.smoke
    def test_lin_networkmanagement_lin6_caseid_109831(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN6,sts=BusSendSts.Awakeup)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN6,sts=BusSendSts.Awakeup)

    @allure.title("LIN6_usgmod_abandoned to Driving_116031")
    @pytest.mark.smoke
    def test_lin_networkmanagement_lin6_caseid_116031(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN6,sts=BusSendSts.Awakeup)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN6,sts=BusSendSts.Awakeup)

    @pytest.mark.smoke
    @pytest.mark.V_1_4
    def test_lin_networkmanagement_caseid_1983481(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN6,sts=BusSendSts.Awakeup)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN6,sts=BusSendSts.Awakeup)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN6,sts=BusSendSts.Awakeup)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN6,sts=BusSendSts.Awakeup)
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.mix.network_sleep()
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN6,sts=BusSendSts.Sleep)
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        sleep(20)

    @allure.title("LIN2_休眠后_Abandoned_OnBdChrgrHndlSts1-opened_1989735")
    @pytest.mark.smoke
    def test_lin_networkmanagement_caseid_1989735(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN2,sts=BusSendSts.Sleep)
        self.bus_comm.set("propulsioncan", "CddObcPropFr01", "OnBdChrgrHndlSts1", 2,)
        self.bus_comm.set("propulsioncan", "CddObcPropFr01", "OnBdChrgrHndlSts1", 0,)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN2,sts=BusSendSts.Awakeup)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN2,sts=BusSendSts.Sleep)
        self.bus_comm.set("propulsioncan", "CddObcPropFr01", "OnBdChrgrHndlSts1", 2,)
        sleep(1)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN2,sts=BusSendSts.Awakeup)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN2,sts=BusSendSts.Sleep)


    @allure.title("LIN2_休眠后_Abandoned_DCChrgnHndlSts-opened_109679")
    @pytest.mark.smoke
    def test_lin_networkmanagement_caseid_109679(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.set("backbonefr", "VddmBackBoneFr29", "DCChrgnHndlSts", 0,)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN2,sts=BusSendSts.Sleep)
        with allure.step("set DCChrgnHndlSts from 0 to 2, lin2 Awakeup"):
            logger.info("---------------->set DCChrgnHndlSts = 2")
            self.bus_comm.set("backbonefr", "VddmBackBoneFr29", "DCChrgnHndlSts", 2,)
            self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN2,sts=BusSendSts.Awakeup)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN2,sts=BusSendSts.Sleep)
        with allure.step("set DCChrgnHndlSts any to 0, lin2 Awakeup"):
            logger.info("---------------->set DCChrgnHndlSts = 0")
            self.bus_comm.set("backbonefr", "VddmBackBoneFr29", "DCChrgnHndlSts", 0,)
        sleep(1)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN2,sts=BusSendSts.Awakeup)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN2,sts=BusSendSts.Sleep)

    @allure.title("LIN2 charge lid j3-26_1995969")
    @pytest.mark.smoke
    def test_caseid_1995969(self):
        self.io.charge_lid_close()
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN2,sts=BusSendSts.Sleep)
        self.io.charge_lid_open()
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN2,sts=BusSendSts.Awakeup)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN2,sts=BusSendSts.Sleep)
        self.io.charge_lid_close()
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN2,sts=BusSendSts.Awakeup)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN2,sts=BusSendSts.Sleep)
