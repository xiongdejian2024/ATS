#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_sun_sensor.py
@Author      : daidi.liang@jiduauto.com
@Time        : 2024/07/09 11:30
@Description: BGM车控车/设雨量光传感器
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

@allure.feature("BGM车控车设")
@allure.story("雨量光传感器")
class TestWiperFuncSafe(TestABCBase):
    def before_class(self, ecu):
        self.sd_tester.write_ccp({353:0x02,352:0x80})
    
    def before_each_func(self, ecu):   
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        # 读取ccp  方便后面进行恢复
        err_code, recv_data_list = self.sd_tester.send_request_and_recv_response([0x22, 0xF1, 0x06],recv=[0x62, 0xF1, 0x06])
        self.ccp_original_value = recv_data_list[3:1556 + 3]
       
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

    def dtc_test_before(self,read_dtc:list,recv_dtc:list):
        #DTC前置条件
        self.mix.set_dtc_precontion()
        #清除历史故障
        self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        sleep(2)
        self.sd_tester.send_request_and_recv_response(read_dtc,recv=recv_dtc)
        
    def set_sunSensor_value(self,set_value:float,check_value:float,sun_sensor_type:str,reverse_case=None):
        if sun_sensor_type == "left" and reverse_case == None:
            self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr03","SolarSnsrLeValue",set_value)
            self.bus_comm.check("bodycan","CemBodyFr04","LeSolarData",check_value)
            
        elif sun_sensor_type == "right" and reverse_case == None:
            self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr03","SolarSnsrRiValue",set_value)
            self.bus_comm.check("bodycan","CemBodyFr04","RiSolarData",check_value)

        else:
            if sun_sensor_type == "left":
                self.bus_comm.check("bodycan","CemBodyFr04","LeSolarData",0.0)
            else:
                self.bus_comm.check("bodycan","CemBodyFr04","RiSolarData",0.0)

    def check_sun_sensor_error_value(self,assert_value=None):
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr03","SolarSnsrLeValue",10.0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr03","SolarSnsrRiValue",10.0)
        if assert_value:
            self.bus_comm.check("bodycan","CemBodyFr04","LeSolarData",10.0)
            self.bus_comm.check("bodycan","CemBodyFr04","RiSolarData",10.0)

    def set_humidity(self):
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr02","CmptFrntWindDewT",10.0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr02","CmptFrntWindT",10.0)
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr02","RelHumSnsrRelHum",10.0)

    def check_humidity(self):
        self.bus_comm.check("bodycan","CemBodyFr60","CmptmtRelHum",10.0)
        self.bus_comm.check("bodycan","CemBodyFr60","CmptmtFrntWindT",10.0)
        self.bus_comm.check("bodycan","CemBodyFr60","CmptmtFrntWindDewT",10.0)

    @pytest.mark.full
    def test_caseid_1989429(self):
        """
        阳光传感器组件故障组件内部故障 （DTC 90BE96)
        """
        self.dtc_test_before([0x19, 0x04,0x90,0xBE,0x96,0x20],[0x59, 0x04,0x90,0xBE,0x96,0x00])
        self.mix.generate_dtc_fault(dtc_fault=DTCFault.SolarSnsrErr,last_time=1)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.SolarSnsrErr, dtc_sts=DTCSts.CurrentFailed, fault_sts=True)
        self.bus_comm.check("bodycan","CemBodyFr04","SolarSnsrVluQf",0)
        self.mix.remove_dtc_fault(dtc_fault=DTCFault.SolarSnsrErr,last_time=1)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.SolarSnsrErr, dtc_sts=DTCSts.FullWithHistory, fault_sts=True)
        self.bus_comm.check("bodycan","CemBodyFr04","SolarSnsrVluQf",1)
        
    @pytest.mark.full
    def test_caseid_1989420(self):
        """
        RLSM相对湿度传感器故障 （DTC 970149)
        """
        self.dtc_test_before([0x19, 0x04,0x97,0x01,0x49,0x20],[0x59, 0x04,0x97,0x01,0x49,0x00])
        self.mix.generate_dtc_fault(dtc_fault=DTCFault.RelHumSnsrErr,last_time=2)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.RelHumSnsrErr, dtc_sts=DTCSts.CurrentFailed, fault_sts=True)
        self.bus_comm.check("bodycan","CEMBodyFr13","RelHumSnsrQf",0)
        self.mix.remove_dtc_fault(dtc_fault=DTCFault.RelHumSnsrErr,last_time=2)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.RelHumSnsrErr, dtc_sts=DTCSts.FullWithHistory, fault_sts=True)
        self.bus_comm.check("bodycan","CEMBodyFr13","RelHumSnsrQf",1)
        
    @pytest.mark.smoke
    def test_caseid_1989422(self):
        """
        CEM将收到的左太阳传感器值传递给CCM
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        for i in [0.0,5.0,1275.0]:
            logger.info(f"当前传递的值为：{i}")
            self.set_sunSensor_value(set_value=i,check_value=i,sun_sensor_type="left")
        else:
            self.set_sunSensor_value(set_value=2.0,check_value=0.0,sun_sensor_type="left")
            
        
    @pytest.mark.smoke
    def test_caseid_1989423(self):
        """
        CEM将收到的右太阳传感器值传递给CCM
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        for i in [0.0,5.0,1275.0]:
            logger.info(f"当前传递的值为：{i}")
            self.set_sunSensor_value(set_value=i,check_value=i,sun_sensor_type="right")
        else:
            self.set_sunSensor_value(set_value=2.0,check_value=0.0,sun_sensor_type="right")
        
    @pytest.mark.smoke
    def test_caseid_1989426(self):
        """
        CEM将相对湿度传递给CCM
        """
        self.sd_tester.write_ccp({353:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        for i in [0.0,2.0,100.0]:
            logger.info(f"当前传递的值为：{i}")
            self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr02","RelHumSnsrRelHum",i)
            self.bus_comm.check("bodycan","CemBodyFr60","CmptmtRelHum",i)
        else:
            self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr02","RelHumSnsrRelHum",0.05)
            self.bus_comm.check("bodycan","CemBodyFr60","CmptmtRelHum",0)
            
            
    @pytest.mark.smoke
    def test_caseid_1989427(self):
        """
        CEM将前挡风玻璃露水湿度传递给CCM
        """
        self.sd_tester.write_ccp({353:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        for i in [0.0,10.0,164.7]:
            logger.info(f"当前传递的值为：{i}")
            self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr02","CmptFrntWindDewT",i)
            self.bus_comm.check("bodycan","CemBodyFr60","CmptmtFrntWindDewT",i)
        else:
            self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr02","CmptFrntWindDewT",0.05)
            self.bus_comm.check("bodycan","CemBodyFr60","CmptmtFrntWindDewT",0.0)
            
    @pytest.mark.smoke
    def test_caseid_1989428(self):
        """
        CEM将前挡风玻璃温度值传递给CCM
        """
        self.sd_tester.write_ccp({353:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        for i in [0.0,10.0,164.7]:
            logger.info(f"当前传递的值为：{i}")
            self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr02","CmptFrntWindT",i)
            self.bus_comm.check("bodycan","CemBodyFr60","CmptmtFrntWindT",i)
        else:
            self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr02","CmptFrntWindT",0.05)
            self.bus_comm.check("bodycan","CemBodyFr60","CmptmtFrntWindT",0.0)

    @pytest.mark.sanity
    def test_caseid_1989417(self):
        """
        检查阳光传感器发生故障时，SolarSnsrLeValue和SolarSnsrLeValue应发送最后一个值，故障恢复发送实际值
        """
        self.check_sun_sensor_error_value()
        self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr03","SolarSnsrLeValue",10.0)
        self.dtc_test_before([0x19, 0x04,0x90,0xBE,0x96,0x20],[0x59, 0x04,0x90,0xBE,0x96,0x00])
        self.mix.generate_dtc_fault(dtc_fault=DTCFault.SolarSnsrErr,last_time=1)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.SolarSnsrErr, dtc_sts=DTCSts.CurrentFailed, fault_sts=True)
        self.bus_comm.check("bodycan","CemBodyFr04","LeSolarData",10.0)
        self.check_sun_sensor_error_value(assert_value=True)
        self.mix.remove_dtc_fault(dtc_fault=DTCFault.SolarSnsrErr,last_time=1)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.SolarSnsrErr, dtc_sts=DTCSts.FullWithHistory, fault_sts=True)
        self.check_sun_sensor_error_value(assert_value=True)
        self.bus_comm.check("bodycan","CemBodyFr04","LeSolarData",10.0)

    @pytest.mark.sanity
    def test_caseid_1989430(self):
        """
        检测到相对湿度传感器故障时，CmptmtRelHum、CmptmtFrntWindDewT、CmptmtFrntWindT 发送最后一个值,故障消失恢复实际值
        """
        self.sd_tester.write_ccp({353:0x02})
        self.set_humidity()
        self.dtc_test_before([0x19, 0x04,0x97,0x01,0x49,0x20],[0x59, 0x04,0x97,0x01,0x49,0x00])
        self.mix.generate_dtc_fault(dtc_fault=DTCFault.RelHumSnsrErr,last_time=2)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.RelHumSnsrErr, dtc_sts=DTCSts.CurrentFailed, fault_sts=True)
        self.check_humidity()
        self.mix.remove_dtc_fault(dtc_fault=DTCFault.RelHumSnsrErr,last_time=2)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.RelHumSnsrErr, dtc_sts=DTCSts.FullWithHistory, fault_sts=True)
        self.check_humidity()

   