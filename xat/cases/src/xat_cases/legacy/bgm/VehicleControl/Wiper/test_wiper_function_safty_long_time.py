#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_wiper_function_safty.py
@Author      : hui.zhao@jiduauto.com
@Time        : 2024/1/18 11:30
@Description: BGM车控车设雨刮DTC功能
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

@allure.feature("BGM车控车设/雨刮功能")
@allure.story("功能安全")
class TestWiperFuncSafe(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["WiperService_client"])

    def before_each_func(self, ecu):   
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        # 读取ccp  方便后面进行恢复
        err_code, recv_data_list = self.sd_tester.send_request_and_recv_response([0x22, 0xF1, 0x06],recv=[0x62, 0xF1, 0x06])
        self.ccp_original_value = recv_data_list[3:1556 + 3]
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        

    def after_each_func(self, ecu):
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.sd_tester.write_ccp_value(self.ccp_original_value)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        try:
            self.sd_tester.clear_all_dtc_and_check(TA.BGM_MCU, SESSION.EMPTY, UnLock.L0, '54')
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    def after_class(self, ecu):
        pass


    def wiper_to_WMM_signal(self,LvrInSnglStrokePos:int,LvrInIntlPosn:int,LvrInLoSpdPosnSafe:int,LvrInHiSpdPosnSafe:int):
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInSnglStrokePos",LvrInSnglStrokePos)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInIntlPosn",LvrInIntlPosn)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",LvrInLoSpdPosnSafe)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInHiSpdPosnSafe",LvrInHiSpdPosnSafe)
    

    @pytest.mark.longtime
    @pytest.mark.smoke
    def test_caseid_1989291(self):
        """
        drivng&nomal wiper CEM Limp Home,雨刮模式为关闭档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        sleep(1)
        self.wiper_to_WMM_signal(0,0,1,1)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.longtime
    @pytest.mark.smoke
    def test_caseid_1989292(self):
        """
        drivng&nomal wiper CEM Limp Home,雨刮模式为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(1)
        self.wiper_to_WMM_signal(0,1,1,1)
        sleep(260)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.longtime
    @pytest.mark.smoke
    def test_caseid_1989293(self):
        """
        drivng&nomal wiper CEM Limp Home,雨刮模式为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(1)
        self.wiper_to_WMM_signal(0,1,1,1)
        sleep(260)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.longtime
    @pytest.mark.smoke
    def test_caseid_1989294(self):
        """
        drivng&nomal wiper CEM Limp Home,雨刮模式为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(1)
        self.wiper_to_WMM_signal(0,0,2,1)
        sleep(260)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.longtime
    @pytest.mark.smoke
    def test_caseid_1989295(self):
        """
        drivng&nomal wiper CEM Limp Home,雨刮模式为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(1)
        self.wiper_to_WMM_signal(0,0,1,2)
        sleep(260)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.longtime
    @pytest.mark.smoke
    def test_caseid_1989296(self):
        """
        active&nomal wiper CEM Limp Home,雨刮模式为关闭档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        sleep(1)
        self.wiper_to_WMM_signal(0,0,1,1)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.longtime
    @pytest.mark.smoke
    def test_caseid_1989297(self):
        """
       active&nomal wiper CEM Limp Home,雨刮模式为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(1)
        self.wiper_to_WMM_signal(0,0,1,2)
        sleep(260)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)  

    @pytest.mark.longtime
    @pytest.mark.smoke
    def test_caseid_1989298(self):
        """
        active&nomal wiper CEM Limp Home,雨刮模式为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(1)
        self.wiper_to_WMM_signal(0,0,2,1)
        sleep(260)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.longtime
    @pytest.mark.smoke
    def test_caseid_1989299(self):
        """
        active&nomal wiper CEM Limp Home,雨刮模式为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(1)
        self.wiper_to_WMM_signal(0,1,1,1)
        sleep(260)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
    
    @pytest.mark.longtime
    @pytest.mark.smoke
    def test_caseid_1989300(self):
        """
        active&nomal wiper CEM Limp Home,雨刮模式为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(1)
        self.wiper_to_WMM_signal(0,1,1,1)
        sleep(260)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.longtime
    @pytest.mark.sanity
    def test_caseid_1989301(self):
        """
        convience&nomal 车速大于7km/h wiper CEM Limp Home,雨刮模式为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(1)
        self.wiper_to_WMM_signal(0,1,1,1)
        sleep(260)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.longtime
    @pytest.mark.sanity
    def test_caseid_1989302(self):
        """
        convience&nomal 车速大于7km/h wiper CEM Limp Home,雨刮模式为关闭档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        sleep(1)
        self.wiper_to_WMM_signal(0,0,1,1)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.longtime
    @pytest.mark.sanity
    def test_caseid_1989303(self):
        """
       convience&nomal 车速大于7km/h wiper CEM Limp Home,雨刮模式为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(1)
        self.wiper_to_WMM_signal(0,0,1,2)
        sleep(260)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.longtime
    @pytest.mark.sanity
    def test_caseid_1989304(self):
        """
        convience&nomal 车速大于7km/h wiper CEM Limp Home,雨刮模式为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(1)
        self.wiper_to_WMM_signal(0,1,1,1)
        sleep(260)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.longtime
    @pytest.mark.sanity
    def test_caseid_1989305(self):
        """
        convience&nomal 车速大于7km/h wiper CEM Limp Home,雨刮模式为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(1)
        self.wiper_to_WMM_signal(0,0,2,1)
        sleep(260)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.longtime
    @pytest.mark.sanity
    def test_caseid_1989308(self):
        """
        inactive&nomal 车速大于7km/h wiper CEM Limp Home,雨刮模式为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(1)
        self.wiper_to_WMM_signal(0,1,1,1)
        sleep(260)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.longtime
    @pytest.mark.sanity
    def test_caseid_1989309(self):
        """
       inactive&nomal 车速大于7km/h wiper CEM Limp Home,雨刮模式为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(1)
        self.wiper_to_WMM_signal(0,0,1,2)
        sleep(260)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.longtime
    @pytest.mark.sanity
    def test_caseid_1989310(self):
        """
        inactive&nomal 车速大于7km/h wiper CEM Limp Home,雨刮模式为关闭档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        sleep(1)
        self.wiper_to_WMM_signal(0,0,1,1)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.longtime
    @pytest.mark.sanity
    def test_caseid_1989311(self):
        """
        inactive&nomal 车速大于7km/h wiper CEM Limp Home,雨刮模式为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(1)
        self.wiper_to_WMM_signal(0,0,2,1)
        sleep(260)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.longtime
    @pytest.mark.sanity
    def test_caseid_1989312(self):
        """
        inactive&nomal 车速大于7km/h wiper CEM Limp Home,雨刮模式为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(1)
        self.wiper_to_WMM_signal(0,1,1,1)
        sleep(260)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.longtime
    @pytest.mark.full
    def test_caseid_1989313(self):
        """
       abondoned&nomal 车速大于7km/h wiper CEM Limp Home,雨刮模式为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(1)
        self.wiper_to_WMM_signal(0,0,1,2)
        sleep(260)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.longtime
    @pytest.mark.full
    def test_caseid_1989314(self):
        """
        abondoned&nomal 车速大于7km/h wiper CEM Limp Home,雨刮模式为关闭档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        sleep(1)
        self.wiper_to_WMM_signal(0,0,1,1)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.longtime
    @pytest.mark.full
    def test_caseid_1989315(self):
        """
        abondoned&nomal 车速大于7km/h wiper CEM Limp Home,雨刮模式为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(1)
        self.wiper_to_WMM_signal(0,0,2,1)
        sleep(260)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.longtime
    @pytest.mark.full
    def test_caseid_1989316(self):
        """
        abondoned&nomal 车速大于7km/h wiper CEM Limp Home,雨刮模式为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(1)
        self.wiper_to_WMM_signal(0,1,1,1)
        sleep(260)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.longtime
    @pytest.mark.full
    def test_caseid_1989317(self):
        """
        abondoned&nomal 车速大于7km/h wiper CEM Limp Home,雨刮模式为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(1)
        self.wiper_to_WMM_signal(0,1,1,1)
        sleep(260)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)