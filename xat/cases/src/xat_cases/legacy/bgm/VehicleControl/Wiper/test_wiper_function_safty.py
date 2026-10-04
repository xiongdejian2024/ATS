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
        sleep(2)
        self.soa.start_get_wiper_switch_sts()

    def before_each_func(self, ecu):   
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.sd_tester.write_ccp({503:0x02,401:0x02})
        # 读取ccp  方便后面进行恢复
        err_code, recv_data_list = self.sd_tester.send_request_and_recv_response([0x22, 0xF1, 0x06],recv=[0x62, 0xF1, 0x06])
        self.ccp_original_value = recv_data_list[3:1556 + 3]
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.Off)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.soa.hmi_set_wiper_mode(WiperPos.Front, WiperMode.Off)
        sleep(1)


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
        self.soa.stop_get_wiper_switch_sts()
        try:
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    def wiper_disable_and_DIM(self,ActvnOfWshr_value,dim_value,set_wiper_error_value="None",signal_lost=False):
        if not (signal_lost) and set_wiper_error_value != "None":
            self.bus_comm.set('cem_lin1','WmmCem_Lin1Fr01','WiprMotErrSafe',set_wiper_error_value)
        else:
            self.bus_comm.stop_send_pdu('cem_lin1',0x25)
            sleep(2)

        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",ActvnOfWshr_value)
        self.bus_comm.check("backbonefr","CemBackBoneFr18",'WiprSysFailrDetdSafe',dim_value)
        if signal_lost:
            self.bus_comm.resume_send_pdu('cem_lin1',0x25)

    def check_WiprMotFrntLvrCmdNotSafe(self,LvrInSnglStrokePos:int,LvrInIntlPosn:int,LvrInLoSpdPosn:int,LvrInHiSpdPosn:int):
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInSnglStrokePos",LvrInSnglStrokePos)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInIntlPosn",LvrInIntlPosn)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",LvrInLoSpdPosn)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInHiSpdPosnSafe",LvrInHiSpdPosn)
    
    def wiper_test_before(self,wash_func_sts,maintain_pos,wiper_mode):
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, wash_func_sts)
        self.soa.hmi_set_wiper_maintaince_pos(maintain_pos)
        self.soa.hmi_set_wiper_mode(WiperPos.Front, wiper_mode)
        sleep(1)
        
         
    
    @pytest.mark.sanity
    def test_caseid_1988557(self):
        """
        active&Nomal场景下，激活雨刮洗涤，检查雨刮洗涤擦拭状态
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.wiper_test_before(isOn.Off,isOn.Off,WiperMode.Off)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",1)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",2)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",2)

    
    @pytest.mark.sanity
    def test_caseid_1988558(self):
        """
        DRIVING&Nomal场景下，激活雨刮洗涤，检查雨刮洗涤擦拭状态
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.wiper_test_before(isOn.Off,isOn.Off,WiperMode.Off)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",1)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",2)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",2)
        
    @pytest.mark.full
    def test_caseid_1989366(self):
        """
        driving&nomal 无法进行前擦拭时，前清洗器受到抑制
        """
        self.mix.set_dtc_precontion()
        self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        self.mix.generate_dtc_fault(dtc_fault=DTCFault.WiperError,last_time=4)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.WiperError, dtc_sts=DTCSts.CurrentFailed, fault_sts=True)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        self.mix.remove_dtc_fault(dtc_fault=DTCFault.WiperError,last_time=4)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.WiperError, dtc_sts=DTCSts.FullWithHistory, fault_sts=True)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
    

    @pytest.mark.full
    def test_caseid_1989408(self):
        """
        driving&nomal 刮水器低压，无法进行前擦拭时，前清洗器受到抑制
        """
        self.mix.set_dtc_precontion()
        self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        self.mix.generate_dtc_fault(dtc_fault=DTCFault.WiperVoltage,last_time=4)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.WiperVoltage, dtc_sts=DTCSts.CurrentFailed, fault_sts=True)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        self.mix.remove_dtc_fault(dtc_fault=DTCFault.WiperVoltage,last_time=4)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.WiperVoltage, dtc_sts=DTCSts.FullWithHistory, fault_sts=True)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
    

    @pytest.mark.full 
    def test_caseid_1989409(self):
        """
        driving&nomal 刮水器高压，无法进行前擦拭时，前清洗器受到抑制
        """
        self.mix.set_dtc_precontion()
        self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        self.mix.generate_dtc_fault(dtc_fault=DTCFault.WiperOverVoltage,last_time=4)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.WiperOverVoltage, dtc_sts=DTCSts.CurrentFailed, fault_sts=True)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        self.mix.remove_dtc_fault(dtc_fault=DTCFault.WiperOverVoltage,last_time=4)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.WiperOverVoltage, dtc_sts=DTCSts.FullWithHistory, fault_sts=True)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
    

    @pytest.mark.full
    def test_caseid_1989410(self):
        """
        driving&nomal 刮水器过载，无法进行前擦拭时，前清洗器受到抑制
        """
        self.mix.set_dtc_precontion()
        self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        self.mix.generate_dtc_fault(dtc_fault=DTCFault.WiperOverload,last_time=4)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.WiperOverload, dtc_sts=DTCSts.CurrentFailed, fault_sts=True)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        self.mix.remove_dtc_fault(dtc_fault=DTCFault.WiperOverload,last_time=4)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.WiperOverload, dtc_sts=DTCSts.FullWithHistory, fault_sts=True)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)   
        
    @pytest.mark.smoke
    def test_caseid_1981250(self):
        """
        Active&nomal 雨刮电机故障，雨刮洗涤禁用，雨刮故障DIM通知
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.wiper_disable_and_DIM(set_wiper_error_value=2,ActvnOfWshr_value=1,dim_value=2)


    @pytest.mark.smoke
    def test_caseid_1988710(self):
        """
        driving&nomal 雨刮电机故障，雨刮洗涤禁用，雨刮故障DIM通知
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.wiper_disable_and_DIM(set_wiper_error_value=2,ActvnOfWshr_value=1,dim_value=2)

    @pytest.mark.sanity
    def test_caseid_1988711(self):
        """
        CONVENIENCE&nomal 雨刮电机故障，雨刮洗涤禁用，雨刮故障DIM通知
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)  
        self.wiper_disable_and_DIM(set_wiper_error_value=2,ActvnOfWshr_value=1,dim_value=2)

    @pytest.mark.sanity
    def test_caseid_1988712(self):
        """
        ABANDONED&nomal 雨刮电机故障，雨刮洗涤禁用，雨刮故障DIM通知
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)  
        self.wiper_disable_and_DIM(set_wiper_error_value=2,ActvnOfWshr_value=1,dim_value=2)

    @pytest.mark.sanity
    def test_caseid_1988713(self):
        """
        INACTIVE&nomal 雨刮电机故障，雨刮洗涤禁用，雨刮故障DIM通知
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)  
        self.wiper_disable_and_DIM(set_wiper_error_value=2,ActvnOfWshr_value=1,dim_value=2)

    @pytest.mark.full
    def test_caseid_1988714(self):
        """
        CONVENIENCE&nomal 车速小于7km/h,雨刮电机故障，雨刮洗涤禁用，雨刮故障DIM通知
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=1.0)  
        self.wiper_disable_and_DIM(set_wiper_error_value=2,ActvnOfWshr_value=1,dim_value=1)

    @pytest.mark.full
    def test_caseid_1989319(self):
        """
        inactive&nomal 车速小于7km/h,雨刮电机故障，雨刮洗涤禁用，雨刮故障DIM通知
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=1.0)  
        self.wiper_disable_and_DIM(set_wiper_error_value=2,ActvnOfWshr_value=1,dim_value=1)

    @pytest.mark.full
    def test_caseid_1989320(self):
        """
        Abondoned&nomal 车速小于7km/h,雨刮电机故障，雨刮洗涤禁用，雨刮故障DIM通知
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=1.0)  
        self.wiper_disable_and_DIM(set_wiper_error_value=2,ActvnOfWshr_value=1,dim_value=1)

    @pytest.mark.sanity
    def test_caseid_1989355(self):
        """
        雨水传感器故障DIM通知
        """
        self.sd_tester.write_ccp({503:0x02})
        self.mix.set_dtc_precontion()
        self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        self.bus_comm.pause_ecu_send("cem_lin1","WMM")
        sleep(4)
        self.sd_tester.send_request_and_recv_response([0x19, 0x04,0xD3,0x53,0x87,0x20],recv=[0x59, 0x04,0xD3,0x53,0x87,0x27])
        self.bus_comm.check("backbonefr","CemBackBoneFr27","WiprMotErr",1)
        self.bus_comm.resume_all_bus_send()
        sleep(4)
        self.sd_tester.send_request_and_recv_response([0x19, 0x04,0xD3,0x53,0x87,0x20],recv=[0x59, 0x04,0xD3,0x53,0x87,0x26])
        self.bus_comm.check("backbonefr","CemBackBoneFr27","WiprMotErr",0)

    @pytest.mark.full
    def test_caseid_1989357(self):
        """
        反向用例-车辆不带WMM,未收到WMM节点信息，DIM通知
        """
        self.sd_tester.write_ccp({503:0x01})
        self.mix.set_dtc_precontion()
        self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        self.bus_comm.pause_ecu_send("cem_lin1","WMM")
        sleep(4)
        self.sd_tester.send_request_and_recv_response([0x19, 0x04,0xD3,0x53,0x87,0x20],recv=[0x59, 0x04,0xD3,0x53,0x87,0x50])
        self.bus_comm.check("backbonefr","CemBackBoneFr27","WiprMotErr",0)
        self.bus_comm.resume_all_bus_send()
        sleep(4)
        self.sd_tester.send_request_and_recv_response([0x19, 0x04,0xD3,0x53,0x87,0x20],recv=[0x59, 0x04,0xD3,0x53,0x87,0x50])
        self.bus_comm.check("backbonefr","CemBackBoneFr27","WiprMotErr",0)

    @pytest.mark.sanity
    def test_caseid_1989285(self):
        """
        driving&nomal 错误的操作不会导致雨刮失效
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrAcsyModSafe",2 )

    @pytest.mark.sanity
    def test_caseid_1989286(self):
        """
       active&nomal 错误的操作不会导致雨刮失效
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrAcsyModSafe",2 )

    @pytest.mark.sanity
    def test_caseid_1989287(self):
        """
       convience&nomal 车速大于7km/h 错误的操作不会导致雨刮失效
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrAcsyModSafe",2 )

    @pytest.mark.sanity
    def test_caseid_1989288(self):
        """
       inactive&nomal 车速大于7km/h 错误的操作不会导致雨刮失效
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrAcsyModSafe",2 )

    @pytest.mark.sanity
    def test_caseid_1989289(self):
        """
       abonded&nomal 车速大于7km/h 错误的操作不会导致雨刮失效
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrAcsyModSafe",2 )


    @pytest.mark.full
    def test_caseid_1989403(self):
        """
       反向用例_abonded&nomal 车速小于7km/h 错误的操作不会导致雨刮失效
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(10)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrAcsyModSafe",1)

    @pytest.mark.full
    def test_caseid_1989404(self):
        """
       反向用例_inactive&nomal 车速小于7km/h 错误的操作不会导致雨刮失效
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        sleep(10)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrAcsyModSafe",1)

    @pytest.mark.smoke
    def test_caseid_1988603(self):
        """
       Active&Nomal场景下，CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe值为NotVld2）
        """
        self.sd_tester.write_ccp({503:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.wiper_disable_and_DIM(set_wiper_error_value=3,ActvnOfWshr_value=1,dim_value=2)

    @pytest.mark.smoke
    def test_caseid_1988601(self):
        """
       Driving&Nomal场景下，CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe值为NotVld2）
        """
        self.sd_tester.write_ccp({503:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.wiper_disable_and_DIM(set_wiper_error_value=3,ActvnOfWshr_value=1,dim_value=2)
    
    @pytest.mark.smoke
    def test_caseid_1988599(self):
        """
       Driving&Nomal场景下，CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe值为NotVld1）
        """
        self.sd_tester.write_ccp({503:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.wiper_disable_and_DIM(set_wiper_error_value=0,ActvnOfWshr_value=1,dim_value=2)

    @pytest.mark.smoke
    def test_caseid_1988598(self):
        """
       Active&Nomal场景下，CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe值为NotVld1）
        """
        self.sd_tester.write_ccp({503:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.wiper_disable_and_DIM(set_wiper_error_value=0,ActvnOfWshr_value=1,dim_value=2)
    
    @pytest.mark.smoke
    def test_caseid_1988591(self):
        """
       Active&Nomal场景下，CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe信号丢失）
        """
        self.sd_tester.write_ccp({503:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.wiper_disable_and_DIM(set_wiper_error_value=0,ActvnOfWshr_value=1,dim_value=2,signal_lost=True)

    @pytest.mark.smoke
    def test_caseid_1988590(self):
        """
       Driving&Nomal场景下，CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe信号丢失）
        """
        self.sd_tester.write_ccp({503:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.wiper_disable_and_DIM(ActvnOfWshr_value=1,dim_value=2,signal_lost=True)

    @pytest.mark.sanity
    def test_caseid_1988592(self):
        """
       CONVENIENCE&Nomal场景下，CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe信号丢失）
        """
        self.sd_tester.write_ccp({503:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.wiper_disable_and_DIM(ActvnOfWshr_value=1,dim_value=2,signal_lost=True)

    @pytest.mark.sanity
    def test_caseid_1988593(self):
        """
       ABANDONED&Nomal场景下，CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe信号丢失）
        """
        self.sd_tester.write_ccp({503:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.wiper_disable_and_DIM(ActvnOfWshr_value=1,dim_value=2,signal_lost=True)

    @pytest.mark.sanity
    def test_caseid_1988594(self):
        """
       INACTIVE&Nomal场景下，CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe信号丢失）
        """
        self.sd_tester.write_ccp({503:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.wiper_disable_and_DIM(ActvnOfWshr_value=1,dim_value=2,signal_lost=True)

    @pytest.mark.sanity
    def test_caseid_1988596(self):
        """
       CONVENIENCE&Nomal场景下，CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe值为NotVld1）
        """
        self.sd_tester.write_ccp({503:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.wiper_disable_and_DIM(set_wiper_error_value=0,ActvnOfWshr_value=1,dim_value=2)

    @pytest.mark.sanity
    def test_caseid_1988597(self):
        """
       INACTIVE&Nomal场景下，CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe值为NotVld1）
        """
        self.sd_tester.write_ccp({503:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.wiper_disable_and_DIM(set_wiper_error_value=0,ActvnOfWshr_value=1,dim_value=2)

    @pytest.mark.sanity
    def test_caseid_1988600(self):
        """
       ABANDONED&Nomal场景下，CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe值为NotVld1）
        """
        self.sd_tester.write_ccp({503:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.wiper_disable_and_DIM(set_wiper_error_value=0,ActvnOfWshr_value=1,dim_value=2)

    @pytest.mark.sanity
    def test_caseid_1988602(self):
        """
       CONVENIENCE&Nomal场景下，CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe值为NotVld2）
        """
        self.sd_tester.write_ccp({503:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.wiper_disable_and_DIM(set_wiper_error_value=3,ActvnOfWshr_value=1,dim_value=2)

    @pytest.mark.sanity
    def test_caseid_1988604(self):
        """
       INACTIVE&Nomal场景下，CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe值为NotVld2）
        """
        self.sd_tester.write_ccp({503:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.wiper_disable_and_DIM(set_wiper_error_value=3,ActvnOfWshr_value=1,dim_value=2)

    @pytest.mark.sanity
    def test_caseid_1988605(self):
        """
       ABANDONED&Nomal场景下，CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe值为NotVld2）
        """
        self.sd_tester.write_ccp({503:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.wiper_disable_and_DIM(set_wiper_error_value=3,ActvnOfWshr_value=1,dim_value=2)

    

    @pytest.mark.sanity
    def test_caseid_1989340(self):
        """
       CONVENIENCE&Nomal场景下，车速小于7km/h CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe值为NotVld1）
        """
        self.sd_tester.write_ccp({503:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        self.wiper_disable_and_DIM(set_wiper_error_value=0,ActvnOfWshr_value=1,dim_value=1)

    @pytest.mark.sanity
    def test_caseid_1989341(self):
        """
       CONVENIENCE&Nomal场景下，车速小于7km/h CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe信号丢失）
        """
        self.sd_tester.write_ccp({503:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        self.wiper_disable_and_DIM(ActvnOfWshr_value=1,dim_value=1,signal_lost=True)

    @pytest.mark.sanity
    def test_caseid_1989342(self):
        """
       CONVENIENCE&Nomal场景下，车速小于7km/h CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe值为NotVld2）
        """
        self.sd_tester.write_ccp({503:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        self.wiper_disable_and_DIM(set_wiper_error_value=3,ActvnOfWshr_value=1,dim_value=1)

    @pytest.mark.sanity
    def test_caseid_1989343(self):
        """
       Inactive &Nomal场景下，车速小于7km/h CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe信号丢失）
        """
        self.sd_tester.write_ccp({503:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        self.wiper_disable_and_DIM(ActvnOfWshr_value=1,dim_value=1,signal_lost=True)

    @pytest.mark.sanity
    def test_caseid_1989344(self):
        """
       Inactive&Nomal场景下，车速小于7km/h CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe值为NotVld1）
        """
        self.sd_tester.write_ccp({503:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        self.wiper_disable_and_DIM(set_wiper_error_value=0,ActvnOfWshr_value=1,dim_value=1)

    @pytest.mark.sanity
    def test_caseid_1989345(self):
        """
       Inactive &Nomal场景下，车速小于7km/h CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe值为NotVld2）
        """
        self.sd_tester.write_ccp({503:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        self.wiper_disable_and_DIM(set_wiper_error_value=3,ActvnOfWshr_value=1,dim_value=1)

    @pytest.mark.sanity
    def test_caseid_1989346(self):
        """
       Abondened &Nomal场景下，车速小于7km/h CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe信号丢失）
        """
        self.sd_tester.write_ccp({503:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        self.wiper_disable_and_DIM(ActvnOfWshr_value=1,dim_value=1,signal_lost=True)
    
    @pytest.mark.sanity
    def test_caseid_1989347(self):
        """
       Abondened&Nomal场景下，车速小于7km/h CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe值为NotVld1）
        """
        self.sd_tester.write_ccp({503:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        self.wiper_disable_and_DIM(set_wiper_error_value=0,ActvnOfWshr_value=1,dim_value=1)

    @pytest.mark.sanity
    def test_caseid_1989348(self):
        """
       Abondened &Nomal场景下，车速小于7km/h CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe值为NotVld2）
        """
        self.sd_tester.write_ccp({503:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=1.0) 
        self.wiper_disable_and_DIM(set_wiper_error_value=3,ActvnOfWshr_value=1,dim_value=1)

    #-------------------------------------------------------------------------------
    @pytest.mark.full
    def test_caseid_1989339(self):
        """
       反向用例 ccp 503!=02 Driving&Nomal场景下，CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe信号丢失）
        """
        self.sd_tester.write_ccp({503:0x01})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.wiper_disable_and_DIM(ActvnOfWshr_value=1,dim_value=1,signal_lost=True)

    @pytest.mark.full
    def test_caseid_1989338(self):
        """
       反向用例 ccp 503!=02 Driving&Nomal场景下，CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe值为NotVld1）
        """
        self.sd_tester.write_ccp({503:0x01})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.wiper_disable_and_DIM(set_wiper_error_value=0,ActvnOfWshr_value=1,dim_value=1)

    @pytest.mark.full
    def test_caseid_1989337(self):
        """
       反向用例 ccp 503!=02 Driving&Nomal场景下，CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe值为NotVld2）
        """
        self.sd_tester.write_ccp({503:0x01})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.wiper_disable_and_DIM(set_wiper_error_value=3,ActvnOfWshr_value=1,dim_value=1)


    @pytest.mark.full
    def test_caseid_1989336(self):
        """
       反向用例 ccp 503!=02 Active&Nomal场景下，CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe信号丢失）
        """
        self.sd_tester.write_ccp({503:0x01})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.wiper_disable_and_DIM(ActvnOfWshr_value=1,dim_value=1,signal_lost=True)

    @pytest.mark.full
    def test_caseid_1989335(self):
        """
       反向用例 ccp 503!=02 Active&Nomal场景下，CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe值为NotVld2）
        """
        self.sd_tester.write_ccp({503:0x01})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.wiper_disable_and_DIM(set_wiper_error_value=3,ActvnOfWshr_value=1,dim_value=1)

    @pytest.mark.full
    def test_caseid_1989334(self):
        """
       反向用例 ccp 503!=02  Active&Nomal场景下，CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe值为NotVld1）
        """
        self.sd_tester.write_ccp({503:0x01})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.wiper_disable_and_DIM(set_wiper_error_value=0,ActvnOfWshr_value=1,dim_value=1)

    @pytest.mark.full
    def test_caseid_1989333(self):
        """
       反向用例 ccp 503!=02 ABANDONED&Nomal场景下，CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe值为NotVld2）
        """
        self.sd_tester.write_ccp({503:0x01})
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.wiper_disable_and_DIM(set_wiper_error_value=3,ActvnOfWshr_value=1,dim_value=1)
    
    @pytest.mark.full
    def test_caseid_1989332(self):
        """
       反向用例 ccp 503!=02 Active&Nomal场景下，CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe信号丢失）
        """
        self.sd_tester.write_ccp({503:0x01})
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.wiper_disable_and_DIM(ActvnOfWshr_value=1,dim_value=1,signal_lost=True)

    @pytest.mark.full
    def test_caseid_1989331(self):
        """
       反向用例 ccp 503!=02 ABANDONED&Nomal场景下，CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe值为NotVld1）
        """
        self.sd_tester.write_ccp({503:0x01})
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.wiper_disable_and_DIM(set_wiper_error_value=0,ActvnOfWshr_value=1,dim_value=1)

    @pytest.mark.full
    def test_caseid_1989330(self):
        """
       反向用例 ccp 503!=02 INACTIVE&Nomal场景下，CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe值为NotVld1）
        """
        self.sd_tester.write_ccp({503:0x01})
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.wiper_disable_and_DIM(set_wiper_error_value=0,ActvnOfWshr_value=1,dim_value=1)

    @pytest.mark.full
    def test_caseid_1989329(self):
        """
       反向用例 ccp 503!=02 INACTIVE&Nomal场景下，CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe信号丢失）
        """
        self.sd_tester.write_ccp({503:0x01})
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.wiper_disable_and_DIM(ActvnOfWshr_value=1,dim_value=1,signal_lost=True)
    
    @pytest.mark.full
    def test_caseid_1989328(self):
        """
       反向用例 ccp 503!=02 INACTIVE&Nomal场景下，CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe值为NotVld2）
        """
        self.sd_tester.write_ccp({503:0x01})
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.wiper_disable_and_DIM(set_wiper_error_value=3,ActvnOfWshr_value=1,dim_value=1)

    @pytest.mark.full
    def test_caseid_1989324(self):
        """
       反向用例 ccp 503!=02 CONVENIENCE&Nomal场景下，CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe值为NotVld2）
        """
        self.sd_tester.write_ccp({503:0x01})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.wiper_disable_and_DIM(set_wiper_error_value=3,ActvnOfWshr_value=1,dim_value=1)

    @pytest.mark.full
    def test_caseid_1989323(self):
        """
       反向用例 ccp 503!=02 CONVENIENCE&Nomal场景下，CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe信号丢失）
        """
        self.sd_tester.write_ccp({503:0x01})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.wiper_disable_and_DIM(ActvnOfWshr_value=1,dim_value=1,signal_lost=True)

    @pytest.mark.full
    def test_caseid_1989322(self):
        """
       反向用例 ccp 503!=02 CONVENIENCE&Nomal场景下，CEM与WMM通信失败,雨刮洗涤禁用（WiprMotErrSafe值为NotVld1）
        """
        self.sd_tester.write_ccp({503:0x01})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        self.wiper_disable_and_DIM(set_wiper_error_value=0,ActvnOfWshr_value=1,dim_value=1)

    @pytest.mark.smoke
    def test_caseid_1989167(self):
        """
        雨水传感器故障DIM通知
        """
        self.sd_tester.write_ccp({401:0x02})
        self.mix.set_dtc_precontion()
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.mix.generate_dtc_fault(dtc_fault=DTCFault.Rainerror,last_time=5)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.Rainerror, dtc_sts=DTCSts.CurrentFailed, fault_sts=True)
        sleep(0.5)
        self.bus_comm.check("backbonefr","CemBackBoneFr19","RainSnsrActvnErrToHmi",1)
        self.mix.remove_dtc_fault(dtc_fault=DTCFault.Rainerror,last_time=4)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.Rainerror, dtc_sts=DTCSts.FullWithHistory, fault_sts=True)
        self.bus_comm.check("backbonefr","CemBackBoneFr19","RainSnsrActvnErrToHmi",0)
        
    @pytest.mark.sanity
    def test_caseid_1989174(self):
        """
        雨水传感器故障DIM通知，雨刮从自动档切换为关闭档
        """
        self.sd_tester.write_ccp({401:0x02})
        self.mix.set_dtc_precontion()
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.mix.generate_dtc_fault(dtc_fault=DTCFault.Rainerror,last_time=5)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.Rainerror, dtc_sts=DTCSts.CurrentFailed, fault_sts=True)
        self.bus_comm.check("backbonefr","CemBackBoneFr19","RainSnsrActvnErrToHmi",1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        sleep(4)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.Rainerror, dtc_sts=DTCSts.FullWithHistory, fault_sts=True)
        self.bus_comm.check("backbonefr","CemBackBoneFr19","RainSnsrActvnErrToHmi",0)
        
    @pytest.mark.sanity
    def test_caseid_1989173(self):
        """
        雨水传感器故障DIM通知，雨刮从自动档切换为单刮
        """
        self.sd_tester.write_ccp({401:0x02})
        self.mix.set_dtc_precontion()
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.mix.generate_dtc_fault(dtc_fault=DTCFault.Rainerror,last_time=5)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.Rainerror, dtc_sts=DTCSts.CurrentFailed, fault_sts=True)
        self.bus_comm.check("backbonefr","CemBackBoneFr19","RainSnsrActvnErrToHmi",1)
        with allure.step("进入扩展会话"):
            self.sd_tester.send_request_and_recv_response([0x10,0x03],recv=[0x50,0x03])
        with allure.step("通过安全访问L5"):
            self.sd_tester.security_access_level(UnLock.L5)
        self.sd_tester.send_request_and_recv_response([0x2F,0x43,0x28,0x03,0x01],recv=[0x6F, 0x43, 0X28])
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInSnglStrokePos",1)
        self.bus_comm.check("backbonefr","CemBackBoneFr19","RainSnsrActvnErrToHmi",0)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.Rainerror, dtc_sts=DTCSts.FullWithHistory, fault_sts=True)
        self.sd_tester.send_request_and_recv_response([0x2F,0x43,0x28,0x00],recv=[0x6F, 0x43, 0X28])

    @pytest.mark.sanity
    def test_caseid_1989172(self):
        """
        雨水传感器故障DIM通知，雨刮从自动档切换为4档
        """
        self.sd_tester.write_ccp({401:0x02})
        self.mix.set_dtc_precontion()
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.mix.generate_dtc_fault(dtc_fault=DTCFault.Rainerror,last_time=5)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.Rainerror, dtc_sts=DTCSts.CurrentFailed, fault_sts=True)
        self.bus_comm.check("backbonefr","CemBackBoneFr19","RainSnsrActvnErrToHmi",1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(4)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.Rainerror, dtc_sts=DTCSts.FullWithHistory, fault_sts=True)
        self.bus_comm.check("backbonefr","CemBackBoneFr19","RainSnsrActvnErrToHmi",0)
        
 
    @pytest.mark.sanity
    def test_caseid_1989171(self):
        """
        雨水传感器故障DIM通知，雨刮从自动档切换为3档
        """
        self.sd_tester.write_ccp({401:0x02})
        self.mix.set_dtc_precontion()
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.mix.generate_dtc_fault(dtc_fault=DTCFault.Rainerror,last_time=5)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.Rainerror, dtc_sts=DTCSts.CurrentFailed, fault_sts=True)
        self.bus_comm.check("backbonefr","CemBackBoneFr19","RainSnsrActvnErrToHmi",1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(4)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.Rainerror, dtc_sts=DTCSts.FullWithHistory, fault_sts=True)
        self.bus_comm.check("backbonefr","CemBackBoneFr19","RainSnsrActvnErrToHmi",0)
        
  
    @pytest.mark.sanity
    def test_caseid_1989170(self):
        """
        雨水传感器故障DIM通知，雨刮从自动档切换为2档
        """
        self.sd_tester.write_ccp({401:0x02})
        self.mix.set_dtc_precontion()
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.mix.generate_dtc_fault(dtc_fault=DTCFault.Rainerror,last_time=5)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.Rainerror, dtc_sts=DTCSts.CurrentFailed, fault_sts=True)
        self.bus_comm.check("backbonefr","CemBackBoneFr19","RainSnsrActvnErrToHmi",1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(4)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.Rainerror, dtc_sts=DTCSts.FullWithHistory, fault_sts=True)
        self.bus_comm.check("backbonefr","CemBackBoneFr19","RainSnsrActvnErrToHmi",0)
        

    @pytest.mark.sanity
    def test_caseid_1989169(self):
        """
        雨水传感器故障DIM通知，雨刮从自动档切换为1档
        """
        self.sd_tester.write_ccp({401:0x02})
        self.mix.set_dtc_precontion()
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.mix.generate_dtc_fault(dtc_fault=DTCFault.Rainerror,last_time=5)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.Rainerror, dtc_sts=DTCSts.CurrentFailed, fault_sts=True)
        self.bus_comm.check("backbonefr","CemBackBoneFr19","RainSnsrActvnErrToHmi",1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(4)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.Rainerror, dtc_sts=DTCSts.FullWithHistory, fault_sts=True)
        self.bus_comm.check("backbonefr","CemBackBoneFr19","RainSnsrActvnErrToHmi",0)
        

    @pytest.mark.full
    def test_caseid_1989179(self):
        """
        反向用例_ccp 401!=02 雨水传感器故障DIM通知，雨刮从自动档切换为4档
        """
        self.sd_tester.write_ccp({401:0x01})
        self.mix.set_dtc_precontion()
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.mix.generate_dtc_fault(dtc_fault=DTCFault.Rainerror,last_time=5)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.Rainerror, dtc_sts=DTCSts.Trc_dissatisfaction, fault_sts=True)
        self.bus_comm.check("backbonefr","CemBackBoneFr19","RainSnsrActvnErrToHmi",0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.Rainerror, dtc_sts=DTCSts.Trc_dissatisfaction, fault_sts=True)
        self.bus_comm.check("backbonefr","CemBackBoneFr19","RainSnsrActvnErrToHmi",0)
        
 
    @pytest.mark.full
    def test_caseid_1989178(self):
        """
        反向用例_ccp 401!=02 雨水传感器故障DIM通知，雨刮从自动档切换为1档   
        """
        self.sd_tester.write_ccp({401:0x01})
        self.mix.set_dtc_precontion()
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.mix.generate_dtc_fault(dtc_fault=DTCFault.Rainerror,last_time=5)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.Rainerror, dtc_sts=DTCSts.Trc_dissatisfaction, fault_sts=True)
        self.bus_comm.check("backbonefr","CemBackBoneFr19","RainSnsrActvnErrToHmi",0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.Rainerror, dtc_sts=DTCSts.Trc_dissatisfaction, fault_sts=True)
        self.bus_comm.check("backbonefr","CemBackBoneFr19","RainSnsrActvnErrToHmi",0)
        

    @pytest.mark.full
    def test_caseid_1989177(self):
        """
        反向用例_ccp 401!=02 雨水传感器故障DIM通知，雨刮从自动档切换为2档
        """
        self.sd_tester.write_ccp({401:0x01})
        self.mix.set_dtc_precontion()
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.mix.generate_dtc_fault(dtc_fault=DTCFault.Rainerror,last_time=5)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.Rainerror, dtc_sts=DTCSts.Trc_dissatisfaction, fault_sts=True)
        self.bus_comm.check("backbonefr","CemBackBoneFr19","RainSnsrActvnErrToHmi",0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.Rainerror, dtc_sts=DTCSts.Trc_dissatisfaction, fault_sts=True)
        self.bus_comm.check("backbonefr","CemBackBoneFr19","RainSnsrActvnErrToHmi",0)
    

    @pytest.mark.full
    def test_caseid_1989176(self):
        """
        反向用例_ccp 401!=02雨水传感器故障DIM通知，雨刮从自动档切换为关闭档
        """
        self.sd_tester.write_ccp({401:0x01})
        self.mix.set_dtc_precontion()
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.mix.generate_dtc_fault(dtc_fault=DTCFault.Rainerror,last_time=5)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.Rainerror, dtc_sts=DTCSts.Trc_dissatisfaction, fault_sts=True)
        self.bus_comm.check("backbonefr","CemBackBoneFr19","RainSnsrActvnErrToHmi",0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.Rainerror, dtc_sts=DTCSts.Trc_dissatisfaction, fault_sts=True)
        self.bus_comm.check("backbonefr","CemBackBoneFr19","RainSnsrActvnErrToHmi",0)
        

    @pytest.mark.full
    def test_caseid_1989175(self):
        """
        反向用例_ccp 401!=02 雨水传感器故障DIM通知，雨刮从自动档切换为单刮
        """
        self.sd_tester.write_ccp({401:0x01})
        self.mix.set_dtc_precontion()
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.mix.generate_dtc_fault(dtc_fault=DTCFault.Rainerror,last_time=5)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.Rainerror, dtc_sts=DTCSts.Trc_dissatisfaction, fault_sts=True)
        self.bus_comm.check("backbonefr","CemBackBoneFr19","RainSnsrActvnErrToHmi",0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.Rainerror, dtc_sts=DTCSts.Trc_dissatisfaction, fault_sts=True)
        self.bus_comm.check("backbonefr","CemBackBoneFr19","RainSnsrActvnErrToHmi",0)

    @pytest.mark.full
    def test_caseid_1989180(self):
        """
        反向用例_ccp 401!=02 雨水传感器故障DIM通知，雨刮从自动档切换为3档
        """
        self.sd_tester.write_ccp({401:0x01})
        self.mix.set_dtc_precontion()
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.mix.generate_dtc_fault(dtc_fault=DTCFault.Rainerror,last_time=5)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.Rainerror, dtc_sts=DTCSts.Trc_dissatisfaction, fault_sts=True)
        self.bus_comm.check("backbonefr","CemBackBoneFr19","RainSnsrActvnErrToHmi",0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.Rainerror, dtc_sts=DTCSts.Trc_dissatisfaction, fault_sts=True)
        self.bus_comm.check("backbonefr","CemBackBoneFr19","RainSnsrActvnErrToHmi",0)
    
    @pytest.mark.full
    def test_caseid_1989168(self):
        """
        反向用例_ccp 401!=02雨水传感器故障DIM通知
        """
        self.sd_tester.write_ccp({401:0x01})
        self.mix.set_dtc_precontion()
        self.mix.generate_dtc_fault(dtc_fault=DTCFault.Rainerror,last_time=5)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.Rainerror, dtc_sts=DTCSts.Trc_dissatisfaction, fault_sts=True)
        self.bus_comm.check("backbonefr","CemBackBoneFr19","RainSnsrActvnErrToHmi",0)
        self.mix.remove_dtc_fault(dtc_fault=DTCFault.Rainerror,last_time=4)
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.Rainerror, dtc_sts=DTCSts.Trc_dissatisfaction, fault_sts=True)
        self.bus_comm.check("backbonefr","CemBackBoneFr19","RainSnsrActvnErrToHmi",0)
        
    #----------------------------------------------------------------------------------
    @pytest.mark.sanity
    def test_caseid_1988544(self):
        """
        Active&Nomal场景下，雨刮模式为4档（high），检查雨刮电机状态
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.wiper_test_before(isOn.Off,isOn.Off,WiperMode.Off)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInHiSpdPosnSafe",1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInHiSpdPosnSafe",2)
        
    @pytest.mark.sanity
    def test_caseid_1988545(self):
        """
        Driving&Nomal场景下，雨刮模式为4档（high），检查雨刮电机状态
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.wiper_test_before(isOn.Off,isOn.Off,WiperMode.Off)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInHiSpdPosnSafe",1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInHiSpdPosnSafe",2)
        
    @pytest.mark.sanity
    def test_caseid_1988546(self):
        """
        ABANDONED&Nomal场景下，雨刮模式为4档（high），检查雨刮电机状态
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.wiper_test_before(isOn.Off,isOn.Off,WiperMode.Off)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInHiSpdPosnSafe",1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(2)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInHiSpdPosnSafe",2)
    
    @pytest.mark.sanity
    def test_caseid_1988547(self):
        """
        CONVENIENCE&Nomal场景下，雨刮模式为4档（high），检查雨刮电机状态
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.wiper_test_before(isOn.Off,isOn.Off,WiperMode.Off)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInHiSpdPosnSafe",1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(2)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInHiSpdPosnSafe",2)
    
    @pytest.mark.sanity
    def test_caseid_1988548(self):
        """
        INACTIVE&Nomal场景下，雨刮模式为4档（high），检查雨刮电机状态
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.wiper_test_before(isOn.Off,isOn.Off,WiperMode.Off)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInHiSpdPosnSafe",1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(2)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInHiSpdPosnSafe",2)

    @pytest.mark.sanity
    def test_caseid_1988549(self):
        """
        Active&Nomal场景下，雨刮模式为3档（low），检查雨刮电机状态
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.wiper_test_before(isOn.Off,isOn.Off,WiperMode.Off)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",2)
        
    @pytest.mark.sanity
    def test_caseid_1988550(self):
        """
        Driving&Nomal场景下，雨刮模式为3档（low），检查雨刮电机状态
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.wiper_test_before(isOn.Off,isOn.Off,WiperMode.Off)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",2)
        
    @pytest.mark.sanity
    def test_caseid_1988551(self):
        """
        Inactive&Nomal场景下，雨刮模式为3档（low），检查雨刮电机状态
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.wiper_test_before(isOn.Off,isOn.Off,WiperMode.Off)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(2)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",2)
        
    @pytest.mark.sanity
    def test_caseid_1988552(self):
        """
        ABANDONED&Nomal场景下，雨刮模式为3档（low），检查雨刮电机状态
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.wiper_test_before(isOn.Off,isOn.Off,WiperMode.Off)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(2)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",2)
        
    @pytest.mark.sanity
    def test_caseid_1988553(self):
        """
        CONVENIENCE&Nomal场景下，雨刮模式为3档（low），检查雨刮电机状态
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.wiper_test_before(isOn.Off,isOn.Off,WiperMode.Off)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(2)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",2)
        
    @pytest.mark.sanity
    def test_caseid_1988554(self):
        """
        CONVENIENCE&Nomal场景下，激活雨刮洗涤，检查雨刮洗涤擦拭状态
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.wiper_test_before(isOn.Off,isOn.Off,WiperMode.Off)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",1)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",2)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",2)
 
    
    @pytest.mark.sanity
    def test_caseid_1988555(self):
        """
        ABANDONED&Nomal场景下，激活雨刮洗涤，检查雨刮洗涤擦拭状态
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.wiper_test_before(isOn.Off,isOn.Off,WiperMode.Off)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",1)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",1)

    @pytest.mark.sanity
    def test_caseid_1988556(self):
        """
        INACTIVE&Nomal场景下，激活雨刮洗涤，检查雨刮洗涤擦拭状态
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.wiper_test_before(isOn.Off,isOn.Off,WiperMode.Off)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",1)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",1)

        
    @pytest.mark.sanity
    def test_caseid_1989280(self):
        """
        driving模式下，"WiprMotErrSafe"=3，错误的操作不应禁止擦拭
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set("cem_lin1","WmmCem_Lin1Fr01","WiprMotErrSafe",3)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrAcsyModSafe",2)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrDrvgModSafe",2)
        
    @pytest.mark.sanity
    def test_caseid_1989279(self):
        """
        driving模式下，"WiprMotErrSafe"=2，错误的操作不应禁止擦拭
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set("cem_lin1","WmmCem_Lin1Fr01","WiprMotErrSafe",2)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrAcsyModSafe",2)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrDrvgModSafe",2)
        
    @pytest.mark.sanity
    def test_caseid_1989278(self):
        """
        driving模式下，"WiprMotErrSafe"=1，错误的操作不应禁止擦拭
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set("cem_lin1","WmmCem_Lin1Fr01","WiprMotErrSafe",1)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrAcsyModSafe",2)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrDrvgModSafe",2)
        
    @pytest.mark.sanity
    def test_caseid_1989277(self):
        """
        driving模式下，"WiprMotErrSafe"=0，错误的操作不应禁止擦拭
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set("cem_lin1","WmmCem_Lin1Fr01","WiprMotErrSafe",0)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrAcsyModSafe",2)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrDrvgModSafe",2)
        
  
    @pytest.mark.full
    def test_caseid_1988560(self):
        """
        Inactive&Nomal场景下，车速<7km/h,激活雨刮洗涤，检查雨刮洗涤擦拭状态
        """
        self.wiper_test_before(isOn.Off,isOn.Off,WiperMode.Off)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=1.0)
        self.wiper_test_before(isOn.Off,isOn.Off,WiperMode.Off)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",1)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        sleep(2)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",1)
    

    @pytest.mark.full
    def test_caseid_1988561(self):
        """
        ABANDONED&Nomal场景下，车速<7km/h,激活雨刮洗涤，检查雨刮洗涤擦拭状态
        """
        self.wiper_test_before(isOn.Off,isOn.Off,WiperMode.Off)
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=1.0)
        self.wiper_test_before(isOn.Off,isOn.Off,WiperMode.Off)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",1)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.On)
        self.bus_comm.check("bodycan","CemBodyFr71","ActvnOfWshrFrntSafe",1)
        sleep(2)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WshrLvrPosnSafe",1)
        
    @pytest.mark.full
    def test_caseid_1988564(self):
        """
        CONVENIENCE&Nomal场景下，车速小于7km/h,雨刮模式为4档（high），检查雨刮电机状态
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.wiper_test_before(isOn.Off,isOn.Off,WiperMode.Off)
        self.bus_comm.set_vehspd_gear(vehspd=1.0)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",1)
        
    @pytest.mark.full
    def test_caseid_1988566(self):
        """
        CONVENIENCE&Nomal场景下，车速小于7km/h，雨刮模式为3档（low），检查雨刮电机状态
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.wiper_test_before(isOn.Off,isOn.Off,WiperMode.Off)
        self.bus_comm.set_vehspd_gear(vehspd=1.0)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",1)
        
    @pytest.mark.full
    def test_caseid_1989412(self):
        """
        inactive&Nomal场景下，车速小于7km/h，雨刮模式为3档（low），检查雨刮电机状态
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.wiper_test_before(isOn.Off,isOn.Off,WiperMode.Off)
        self.bus_comm.set_vehspd_gear(vehspd=1.0)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",1)
        
    @pytest.mark.full
    def test_caseid_1989411(self):
        """
        inactive&Nomal场景下，车速小于7km/h,雨刮模式为4档（high），检查雨刮电机状态
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.wiper_test_before(isOn.Off,isOn.Off,WiperMode.Off)
        self.bus_comm.set_vehspd_gear(vehspd=1.0)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",1)
        
    @pytest.mark.full
    def test_caseid_1989414(self):
        """
        abondoned&Nomal场景下，车速小于7km/h,雨刮模式为4档（high），检查雨刮电机状态
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.wiper_test_before(isOn.Off,isOn.Off,WiperMode.Off)
        self.bus_comm.set_vehspd_gear(vehspd=1.0)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",1)
        
    @pytest.mark.full
    def test_caseid_1989413(self):
        """
        abondoned&Nomal场景下，车速小于7km/h，雨刮模式为3档（low），检查雨刮电机状态
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.wiper_test_before(isOn.Off,isOn.Off,WiperMode.Off)
        self.bus_comm.set_vehspd_gear(vehspd=1.0)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe",1)


    @pytest.mark.full
    def test_caseid_1981059(self):
        """
        LIN1唤醒BGM-RLSM发送车速信号
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=0.0) 
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","VehSpdForWipg",0)
        self.bus_comm.set_vehspd_gear(vehspd=2.777610) 
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","VehSpdForWipg",10)
        self.bus_comm.set_vehspd_gear(vehspd=72.0) 
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","VehSpdForWipg",255)


    @pytest.mark.sanity
    def test_caseid_1991867(self):
        """
        Inactive&normal 车速大于7km/h，车速QF值无效时，雨刮能正常工作
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=2)
        self.bus_comm.set("backbonefr", "BcmVddmBackBoneFr06", 'VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06', 0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=2)
        self.bus_comm.set_vehspd_gear(vehspd=1.0)
        self.bus_comm.set("backbonefr", "BcmVddmBackBoneFr06", 'VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06', 3)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)
        
    @pytest.mark.sanity
    def test_caseid_1991857(self):
        """
        abandoned&normal 车速大于7km/h，车速QF值无效时，雨刮能正常工作
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=2)
        self.bus_comm.set("backbonefr", "BcmVddmBackBoneFr06", 'VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06', 0)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=2)
        self.bus_comm.set_vehspd_gear(vehspd=1.0)
        self.bus_comm.set("backbonefr", "BcmVddmBackBoneFr06", 'VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06', 3)
        self.check_WiprMotFrntLvrCmdNotSafe(LvrInSnglStrokePos=0,LvrInIntlPosn=0,LvrInLoSpdPosn=1,LvrInHiSpdPosn=1)

    