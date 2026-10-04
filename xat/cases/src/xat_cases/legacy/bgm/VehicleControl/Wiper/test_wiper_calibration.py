"""
@File        : test_wiper_calibration.py
@Author      : xue.li01@jiduauto.com
@Time        : 2024/04/28 11:30
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
@allure.story("雨刮标定")
class TestWiperCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["WiperService_client"])
        sleep(2)
        self.soa.start_get_wiper_switch_sts()
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        
        
    def before_each_func(self, ecu):
        self.soa.empty_all()
        err_code, recv_data_list = self.sd_tester.send_request_and_recv_response([0x22, 0xF1, 0x06],recv=[0x62, 0xF1, 0x06])
        self.ccp_original_value = recv_data_list[3:1556 + 3]
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.Off)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.soa.hmi_set_wiper_mode(WiperPos.Front, WiperMode.Off)
        sleep(1)

    def after_each_func(self, ecu):
        sleep(1)
        self.sd_tester.write_ccp_value(self.ccp_original_value)
        
    def after_class(self, ecu):
        self.soa.stop_get_wiper_switch_sts()
        try:
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    def set_pre_condition_for_maintain_service(self, wash_func_sts: isOn, maintain_pos: isOn, wiper_mode: WiperMode,
                                               usage_mode: Union[UsageMode, None] = None,
                                               car_mode: Union[CarMode, None] = None, ccp: dict = {},time_wait = 1):
        self.mix.set_common_precontion(usage_mode=usage_mode, car_mode=car_mode, ccp=ccp)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, wash_func_sts)
        self.soa.hmi_set_wiper_maintaince_pos(maintain_pos)
        self.soa.hmi_set_wiper_mode(WiperPos.Front, wiper_mode)
        sleep(time_wait) 
        
    def check_calibration_signal(self,type,WindCorrnValFrnt_value,WindCorrnValAmb_calue,defalt_flag=None):
        if type == "mars":
            self.bus_comm.check_singal("cem_lin1","CemCem_Lin1Fr03", "WindCorrnValFrnt", WindCorrnValFrnt_value)
            self.bus_comm.check_singal("cem_lin1","CemCem_Lin1Fr03", "WindCorrnValAmb", WindCorrnValAmb_calue) 
        elif type == "venus":
            self.bus_comm.check_singal("cem_lin1","CemCem_Lin1Fr03", "WindCorrnValFrnt", WindCorrnValFrnt_value)
            self.bus_comm.check_singal("cem_lin1","CemCem_Lin1Fr03", "WindCorrnValAmb", WindCorrnValAmb_calue) 
        elif type == "default":
            if defalt_flag == True:
                ccp = "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"
                self.sd_tester.write_ccp_value(ccp)
            self.bus_comm.check_singal("cem_lin1","CemCem_Lin1Fr03", "WindCorrnValFrnt", WindCorrnValFrnt_value)
            self.bus_comm.check_singal("cem_lin1","CemCem_Lin1Fr03", "WindCorrnValAmb", WindCorrnValAmb_calue) 
        else:
            prompt_info = "---------->指定传入的 type 参数有问题"
            with allure.step(prompt_info):
                logger.info(prompt_info)
        self.bus_comm.check_singal("cem_lin1","CemCem_Lin1Fr03","WindCorrnValHud",0)

    @pytest.mark.smoke
    def test_caseid_1986455(self):
        """
        当车辆配置CCP#950==0x2(Venus)，验证(WindCorrnValFrnt、WindCorrnValAmb）显示的信号值是否正确
        """
        self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL,
                                                    ccp={950: 0x2}, wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off) 
        self.check_calibration_signal("venus",78,31)
        
    @pytest.mark.smoke
    def test_caseid_1986454(self):
        """
        当车辆配置设为CCP#950==0x1(Mars1)，验证(WindCorrnValFrnt、WindCorrnValAmb）显示的信号值是否正确
        """
        self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL,
                                                    ccp={950: 0x1}, wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off) 
        self.check_calibration_signal("mars",75,30)
        
    @pytest.mark.smoke
    def test_caseid_1986449(self):
        """
        当车辆配置设为默认（Default），验证(WindCorrnValFrnt、WindCorrnValAmb）显示的信号值是否正确
        """
        self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL,
                                                    ccp={950: 0x0}, wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off) 
        self.check_calibration_signal("default",75,45,defalt_flag=True)
        
    
    @pytest.mark.sanity
    def test_caseid_1986457(self):
        """
        台架用例_当车辆配置设为默认（Default），ccp值改为CCP#950==0x2(Venus)
        """
        self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL,
                                                    ccp={950: 0x0}, wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off) 
        self.check_calibration_signal("default",75,45)
        self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL,
                                                    ccp={950: 0x02}, wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off) 
        self.sd_tester.write_ccp({950:0x02})
        self.check_calibration_signal("venus",78,31)
        
    @pytest.mark.sanity
    def test_caseid_1986456(self):
        """
        台架用例_当车辆配置设为默认（Default），ccp值改为CCP#950==0x1(Mars1)
        """
        self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL,
                                                    ccp={950: 0x00}, wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off) 
        self.check_calibration_signal("default",75,45)
        self.sd_tester.write_ccp({950:0x01})
        self.check_calibration_signal("mars",75,30)
         
        
    
    @pytest.mark.sanity
    def test_caseid_1989473(self):
        """
        检查雨刮为off档时，雨感器灵敏度校正
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.check("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 6)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr03","RainSnsrSnvtyForUsrSnvty6",13)

    @pytest.mark.sanity
    def test_caseid_1989474(self):
        """
        检查雨刮为单刮时，雨感器灵敏度校正
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.bus_comm.check_singal("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 6)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr03","RainSnsrSnvtyForUsrSnvty6",13)

    @pytest.mark.sanity
    def test_caseid_1989475(self):
        """
        检查雨刮为1档时，雨感器灵敏度校正
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.check_singal("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 3)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr03","RainSnsrSnvtyForUsrSnvty3",8)

    @pytest.mark.sanity
    def test_caseid_1989476(self):
        """
        检查雨刮为2档时，雨感器灵敏度校正
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.check_singal("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 6)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr03","RainSnsrSnvtyForUsrSnvty6",13)

    @pytest.mark.sanity
    def test_caseid_1989477(self):
        """
        检查雨刮为3档时，雨感器灵敏度校正
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.check_singal("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 6)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr03","RainSnsrSnvtyForUsrSnvty6",13)

    @pytest.mark.sanity
    def test_caseid_1989478(self):
        """
        检查雨刮为4档时，雨感器灵敏度校正
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.bus_comm.check_singal("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 6)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr03","RainSnsrSnvtyForUsrSnvty6",13)

    @pytest.mark.sanity
    def test_caseid_1989479(self):
        """
        检查雨刮为自动档时，雨感器灵敏度校正
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check_singal("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr03","RainSnsrSnvtyForUsrSnvty5",12)
    
    @pytest.mark.sanity
    def test_caseid_1989759(self):
        """
        检查雨刮故障时，雨感器灵敏度校正
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Error)
        self.bus_comm.check_singal("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 6)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr03","RainSnsrSnvtyForUsrSnvty6",13)
