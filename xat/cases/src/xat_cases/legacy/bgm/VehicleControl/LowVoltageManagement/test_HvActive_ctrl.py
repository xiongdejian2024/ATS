#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_relaycontrol_ctrl.py
@Time         :2023/07/24 17:20:31
@Author       :hui.zhao@jiduauto.com
@Description  :
"""
import allure
import pytest
import time
from time import sleep
from xat_ecu.legacy.sdk.digital_key.digital_key_const import *
from xat_ecu.legacy.common.data_type_handing import logger
from xat_cases.legacy.bgm.case_helper.test_base import TestBase
from xat_ecu.legacy.sdk.digital_key.digital_key_class import DigitalKey
from xat_ecu.legacy.soa_partner.src.base_partner import S2sBaseClass
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_cases.legacy.bgm.case_helper.environment_check import partner_process_check
from xat_cases.legacy.bgm.VehicleControl.case_helper.common_lib_bgm import *
from xat_cases.legacy.bgm.VehicleControl.case_helper.parse_excel_bgm import *
from xat_ecu.legacy.interface.nuc_app import *

HIGHVOLTAGE_SERVICE_CLIENT = "HighVoltageService_client"

def set_bgm_diag_active_line(status):
    if status == "conntected":
        cmd_set = f"usbrelay 1_3=1"
    elif status == "disconntected":
        cmd_set = f"usbrelay 1_3=0"

    exec_shell(cmd_set)
    sleep(2)

    cmd_get = f"usbrelay"
    exec_result = exec_shell(cmd_get)
    # logger.info(exec_result)

    if status == "conntected":
        if exec_result["output"].find("1_3=1") != -1:
            logger.info("BGM诊断激活线连接成功")
            return True
        else:
            return False

    elif status == "disconntected":
        if exec_result["output"].find("1_3=0") != -1:
            logger.info("BGM诊断激活线断开成功")
            return True
        else:
            return False

@allure.feature("车身网关测试/整车控制")
@allure.story("Relay Control")
class TestRelayContolCtrl(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.sd_tester = Sd_Tester(**self.tc_config)
        self.nucapp.bgm_diag_line_up()
        self.ipdu.start_all_time_control()
        self.busapp.start_all_cyclic_msg()

        self.sd_tester.update_serverdoipid(0x1002)
        sleep(0.5)
        self.sd_tester.diagnostic_client_sim_start()
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.sd_tester.tester_present()
        sleep(0.5)
        

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        sleep(0.1)

    def after_each_func(self, ecu):
        self.sd_tester.change_car_mode(0)
        sleep(0.1)
        self.sd_tester.change_usage_mode(0)
        sleep(0.1)
        self.ipdu.reset_check_results()
        sleep(0.1)
        logger.info("诊断激活线连接")
        set_bgm_diag_active_line("conntected")
        # sleep(1)
        super().after_each_func(ecu)

    def after_class(self, ecu):
        try:
            self.sd_tester.change_usage_mode(1)
            self.sd_tester.change_car_mode(0)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
        self.ipdu.time_control_stop()  # 停止数据模拟(数据库周期性报文和调度表)
        self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动,总线开始收发报文
        sleep(0.5)
        self.sd_tester.stop_tester_present()
        self.nucapp.bgm_diag_line_down()
        sleep(0.5)
        self.sd_tester.diagnostic_client_sim_close()
        sleep(0.5)
        logger.info("诊断激活线连接")
        set_bgm_diag_active_line("conntected")
        sleep(0.5)
        super().after_class(self, ecu)
    

    def trigger_low_voltage_req(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为Inactive
            self.sd_tester.change_usage_mode(1)
            sleep(1)
            # 诊断激活线连接
            logger.info("诊断激活线连接")
            set_bgm_diag_active_line("conntected")
            sleep(1)
            # 仿真BattUarw=5V
            logger.info("仿真LIN6数据")
            self.ipdu.send_pdu("cem_lin6", 0x06, [0x0, 0x7c, 0x00, 0xff, 0xff, 0xff, 0xff])
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'CnvnAllwd',1)

        with allure.step(f"Step:等待1分钟"):
            logger.info("等待1分钟")
            sleep(10)

        with allure.step(f"检测是否CnvnReq=1"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 1, 1
            )

        with allure.step(f"检测当前ChrgnUReq=14.4"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',14.4,
            )
        sleep(2)

    @allure.title("智能补电_低压补电Inactive_触发")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109474?projectId=46'
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_109474(self):
        self.trigger_low_voltage_req()
        # with allure.step(f"Step:设置初始条件"):
        #     # UsageMode 设置为Inactive
        #     self.sd_tester.change_usage_mode(1)
        #     sleep(1)
        #     # 诊断激活线连接
        #     logger.info("诊断激活线连接")
        #     set_bgm_diag_active_line("conntected")
        #     sleep(1)
        #     # 仿真BattUarw=5V
        #     logger.info("仿真LIN6数据")
        #     self.ipdu.send_pdu("cem_lin6", 0x06, [0x0, 0x7c, 0x00, 0xff, 0xff, 0xff, 0xff])
        #     self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'CnvnAllwd',1)

        # with allure.step(f"Step:等待1分钟"):
        #     logger.info("等待1分钟")
        #     sleep(10)

        # with allure.step(f"检测是否CnvnReq=1"):
        #     self.ipdu.check(
        #         self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 1, 1
        #     )
        # with allure.step(f"检测当前ChrgnUReq=14.4"):
        #     self.ipdu.check(
        #         self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',14.4,
        #     )
        # sleep(5)
    
    @allure.title("智能补电_低压补电Inactive_停止")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109443?projectId=46'
    )   
    @pytest.mark.smoke
    def test_HvActive_caseid_109443(self):
        
        with allure.step(f"Step:执行第一个case"):
            # UsageMode 设置为Inactive
            self.trigger_low_voltage_req()
            
        with allure.step(f"Step:执行发送LIN6停止补电"):
            self.ipdu.send_pdu("cem_lin6", 0x06, [0x0, 0x7c, 0xc8, 0xff, 0xff, 0xff, 0xff])
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'CnvnAllwd',0)
        
        with allure.step(f"Step:等待1分钟"):
            logger.info("等待1分钟")
            sleep(10)

        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0, 1
            )
        with allure.step(f"检测当前ChrgnUReq=13.5"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',13.5,
            )
        sleep(5)

    @allure.title("智能补电_低压补电abonedone_停止")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/119277?projectId=46'
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_119277(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为Inactive
            self.sd_tester.change_usage_mode(1)
            sleep(1)
            # 诊断激活线连接
            logger.info("诊断激活线连接")
            set_bgm_diag_active_line("conntected")

        with allure.step(f"Step:usgmod由01inactive切换为00abonedone"):
            self.sd_tester.change_usage_mode(0)
            sleep(10)

        with allure.step(f"Step:诊断激活线断开"):
            logger.info("诊断激活线断开")
            set_bgm_diag_active_line("disconntected")

        with allure.step(f"Step:等待1分钟"):
            logger.info("等待1分钟")
            sleep(10)

        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0, 1
            )
        with allure.step(f"检测当前ChrgnUReq=13.5"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',13.5,
            )
        sleep(5)
    
    @allure.title("智能补电_DcDcActvd_触发")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109441?projectId=46'
    )
    @pytest.mark.full
    @pytest.mark.v110only
    def test_HvActive_caseid_109441_109481(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为Inactive
            self.sd_tester.change_usage_mode(1)
            sleep(1)
            # 诊断激活线连接
            logger.info("诊断激活线连接")    
        with allure.step(f"Step:执行发送LIN6停止补电"):
            self.ipdu.send_pdu("cem_lin6", 0x06, [0x0, 0x7c, 0xc8, 0xff, 0xff, 0xff, 0xff]) 
        with allure.step(f"Step:等待1分钟"):
            logger.info("等待1分钟")
            sleep(10)
        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0, 1
            )
        with allure.step(f"检测当前ChrgnUReq=13.5"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',13.5,
            )
        with allure.step(f"Step:仿真DcDcactvd 为1 "):
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'DcDcActvd',1)
            sleep(10)   
        with allure.step(f"检测当前ChrgnUReq=14.4"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',14.4,
            )  
        sleep(5)

    @allure.title("智能补电_DcDcActvd_停止")
    @pytest.mark.smoke
    def test_HvActive_caseid_109442(self): 
        #with allure.step(f"Step:设置初始条件"):
            #self.test_HvActive_caseid_0000004()
        with allure.step(f"Step:仿真DcDcactvd 为0 "):
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'DcDcActvd',0)
            sleep(10)   
        with allure.step(f"检测当前ChrgnUReq=13.5"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',13.5,
            )  
        sleep(5)

    @allure.title("智能补电_DcDcActvd_触发")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109441?projectId=46'
    )
    @pytest.mark.full
    def test_HvActive_caseid_109441(self):
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为Inactive
            self.sd_tester.change_usage_mode(1)
            sleep(1)
            # 诊断激活线连接
            logger.info("诊断激活线连接")    
        with allure.step(f"Step:执行发送LIN6停止补电"):
            self.ipdu.send_pdu("cem_lin6", 0x06, [0x0, 0x7c, 0xc8, 0xff, 0xff, 0xff, 0xff]) 
        with allure.step(f"Step:等待1分钟"):
            logger.info("等待1分钟")
            sleep(10)
        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0, 1
            )
        with allure.step(f"检测当前ChrgnUReq=13.5"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',13.5,
            )
        with allure.step(f"Step:仿真DcDcactvd 为1 "):
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'DcDcActvd',1)
            sleep(10)   
        with allure.step(f"检测当前ChrgnUReq=14.4"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',14.4,
            )  
        sleep(5)
    
    @allure.title("智能补电_低压_Convenience")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/118488?projectId=46'
    )
    @pytest.mark.full
    def test_HvActive_caseid_118488(self): 
        with allure.step(f"Step:设置初始条件"):
            self.trigger_low_voltage_req()
            sleep(5)
        with allure.step(f"Step:usgmod由01inactive切换为02Convenience"):    
            # UsageMode 设置为02Convenience
            self.sd_tester.change_usage_mode(1)
            sleep(5)
            self.sd_tester.change_usage_mode(2)
            sleep(1)
        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0, 1
            )  
        with allure.step(f"检测当前ChrgnUReq=13.5"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',13.5,
            )  
        sleep(5)

    
    @allure.title("智能补电_低压_Active")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/118487?projectId=46'
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_118487(self): 
        with allure.step(f"Step:设置初始条件"):
            self.trigger_low_voltage_req()
            
            sleep(1)
        with allure.step(f"Step:usgmod由01inactive切换为0b Active"):    
            # UsageMode 设置为0b Active
            self.sd_tester.change_usage_mode(1)
            sleep(5)
            self.sd_tester.change_usage_mode(11)
            sleep(1)
        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0, 1
            )  
        with allure.step(f"检测当前ChrgnUReq=13.5"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',13.5,
            )  
        sleep(5)
    
    @allure.title("智能补电_低压_Driving")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/118489?projectId=46'
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_118489(self): 
        with allure.step(f"Step:设置初始条件"):
            self.trigger_low_voltage_req()
            sleep(1)
        with allure.step(f"Step:usgmod由01inactive切换为0D Driving"):    
            # UsageMode 设置为0D Driving
            self.sd_tester.change_usage_mode(1)
            sleep(5)
            self.sd_tester.change_usage_mode(13)
            sleep(1)
        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0, 1
            )  
        with allure.step(f"检测当前ChrgnUReq=13.5"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',13.5,
            )  
        sleep(5)


    @allure.title("智能补电_低压_CnvnAllwd_Ok保持")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/118489?projectId=46'
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_118490(self): 
        with allure.step(f"Step:设置初始条件"):
            self.trigger_low_voltage_req()
            sleep(1)
        with allure.step(f"Step:usgmod由01inactive切换为0D Driving"):    
            # UsageMode 设置为0D Driving
            self.sd_tester.change_usage_mode(1)
            sleep(5)
            self.sd_tester.change_usage_mode(13)
            sleep(1)
        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0, 1
            )  
        with allure.step(f"检测当前ChrgnUReq=13.5"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',13.5,
            ) 
        with allure.step(f"Step:usgmod由0D Driving切换为01inactive"):    
            # UsageMode 设置为01inactive
            self.sd_tester.change_usage_mode(1)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'CnvnAllwd',1)   
            result = self.ipdu.check_event(self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq',1, 0,timeout=30)
            logger.info("result {}".format(result))
            if result == 0:
                assert True
            else:
                assert False
        sleep(5)    

    @allure.title("智能补电_低压_CnvnAllwd_NotOk保持")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/118489?projectId=46'
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_118491(self): 
        with allure.step(f"Step:设置初始条件"):
            self.trigger_low_voltage_req()
            sleep(1)
        with allure.step(f"Step:usgmod由01inactive切换为0D Driving"):    
            # UsageMode 设置为0D Driving
            self.sd_tester.change_usage_mode(1)
            sleep(5)
            self.sd_tester.change_usage_mode(13)
            sleep(1)
        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0, 1
            )  
        with allure.step(f"检测当前ChrgnUReq=13.5"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',13.5,
            ) 
        with allure.step(f"Step:usgmod由0D Driving切换为01inactive"):    
            # UsageMode 设置为01inactive
            self.sd_tester.change_usage_mode(1)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'CnvnAllwd',0)   
            result = self.ipdu.check_event(self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq',0, 1,timeout=30)
            logger.info("result {}".format(result))
            if result == 5:
                assert True
            else:
                assert False
        sleep(5)

    @allure.title("智能补电_系统故障_Inactive")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109485?projectId=46'
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_109485(self): 
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为01 Inactive
            self.sd_tester.change_usage_mode(1)
            self.ipdu.resume_bus_send("cem_lin6")
            sleep(1)
        with allure.step(f"Step:执行发送LIN6停止补电"):
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'CnvnAllwd',0)
            self.ipdu.send_pdu("cem_lin6", 0x06, [0x0, 0x7c, 0xc8, 0xff, 0xff, 0xff, 0xff])
            sleep(15)

        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0, 
            )
        with allure.step(f"检测当前ChrgnUReq=13.5"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',13.5,
            )
        with allure.step(f"Step:断开Lin6通讯 触发系统故障"):
            self.ipdu.pause_bus_send("cem_lin6")
            sleep(15)

        with allure.step(f"检测是否CnvnReq=1"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 1, 
            )
        with allure.step(f"检测当前ChrgnUReq=13.5"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',13.5,
            )
        with allure.step(f"Step:恢复Lin6通讯"):
            self.ipdu.resume_bus_send("cem_lin6")
            sleep(1)
        sleep(5)
    
    @allure.title("智能补电_系统故障_abonedone")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109484?projectId=46'
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_109484(self): 
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为01 Inactive
            self.sd_tester.change_usage_mode(1)
            sleep(1)
            # 断开Lin6通讯 触发系统故障
            self.ipdu.pause_bus_send("cem_lin6")
            sleep(12)

        with allure.step(f"检测是否CnvnReq=1"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 1, 
            )
        with allure.step(f"检测当前ChrgnUReq=13.5"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',13.5,
            )
        
        with allure.step(f"Step:usgmod由01inactive切换为00 abonedone"):    
            # UsageMode 设置为00 abonedone
            self.sd_tester.change_usage_mode(0)
            sleep(11)
            

        with allure.step(f"检测是否CnvnReq=1"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 1, 
            )
        with allure.step(f"检测当前ChrgnUReq=13.5"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',13.5,
            )
        with allure.step(f"Step:恢复Lin6通讯"):
            self.ipdu.resume_bus_send("cem_lin6")
            sleep(1)    

        sleep(5)

    @allure.title("智能补电_系统故障_Convenience")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/118822?projectId=46'
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_118822(self): 
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为01 Inactive
            self.sd_tester.change_usage_mode(1)
            sleep(1)
            # 断开Lin6通讯 触发系统故障
            self.ipdu.pause_bus_send("cem_lin6")
            sleep(12)
        with allure.step(f"检测是否CnvnReq=1"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 1, 
            )
        with allure.step(f"检测当前ChrgnUReq=13.5"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',13.5,
            )       
        with allure.step(f"Step:usgmod由01inactive切换为02 Convenience"):    
            # UsageMode 设置为02 Convenience
            self.sd_tester.change_usage_mode(2)
            sleep(5)    
        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0, 
            )
        with allure.step(f"检测当前ChrgnUReq=13.5"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',13.5,
            )
        with allure.step(f"Step:恢复Lin6通讯"):
            self.ipdu.resume_bus_send("cem_lin6")
            sleep(1)       
        sleep(5)

    @allure.title("智能补电_系统故障_Active")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/118823?projectId=46'
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_118823(self): 
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为01 Inactive
            self.sd_tester.change_usage_mode(1)
            sleep(1)
            # 断开Lin6通讯 触发系统故障
            self.ipdu.pause_bus_send("cem_lin6")
            sleep(12)
        with allure.step(f"检测是否CnvnReq=1"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 1, 
            )
        with allure.step(f"检测当前ChrgnUReq=13.5"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',13.5,
            )    
        with allure.step(f"Step:usgmod由01inactive切换为0B Active"):    
            # UsageMode 设置为0B Active
            self.sd_tester.change_usage_mode(11)
            sleep(5)    
        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0, 
            )
        with allure.step(f"检测当前ChrgnUReq=13.5"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',13.5,
            )
        with allure.step(f"Step:恢复Lin6通讯"):
            self.ipdu.resume_bus_send("cem_lin6")
            sleep(1)
        sleep(5)

    @allure.title("智能补电_系统故障_Driving")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/118824?projectId=46'
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_118824(self): 
        with allure.step(f"Step:设置初始条件"):
            # UsageMode 设置为01 Inactive
            self.sd_tester.change_usage_mode(1)
            sleep(1)
            # 断开Lin6通讯 触发系统故障
            self.ipdu.pause_bus_send("cem_lin6")
            sleep(12)
        with allure.step(f"检测是否CnvnReq=1"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 1, 
            )
        with allure.step(f"检测当前ChrgnUReq=13.5"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',13.5,
            )    
        with allure.step(f"Step:usgmod由01inactive切换为0D Driving"):    
            # UsageMode 设置为0D Driving
            self.sd_tester.change_usage_mode(13)
            sleep(5)    
        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0, 
            )
        with allure.step(f"检测当前ChrgnUReq=13.5"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',13.5,
            )
        with allure.step(f"Step:恢复Lin6通讯"):
            self.ipdu.resume_bus_send("cem_lin6")
            sleep(1)

    @allure.title("智能补电_Convenience_Notreqd")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/118730?projectId=46'
    )
    @pytest.mark.full
    def test_HvActive_caseid_118730(self): 
        with allure.step(f"Step:设置Convenience"):
            # UsageMode 设置为02 Convenience
            self.sd_tester.change_usage_mode(2)
            sleep(1)
        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0, 
            )
            sleep(5)
    
    @allure.title("智能补电_Active_Notreqd")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/118735?projectId=46'
    )
    @pytest.mark.full
    def test_HvActive_caseid_118735(self): 
        with allure.step(f"Step:设置Active"):
            # UsageMode 设置为0B Active
            self.sd_tester.change_usage_mode(11)
            sleep(1)
        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0, 
            )
            sleep(5)

    @allure.title("智能补电_Driving_Notreqd")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/118736?projectId=46'
    )
    @pytest.mark.full
    def test_HvActive_caseid_118736(self): 
        with allure.step(f"Step:设置Driving"):
            # UsageMode 设置为0D Driving
            self.sd_tester.change_usage_mode(13)
            sleep(1)
        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0, 
            )
            sleep(5)

    @allure.title("智能补电_超时补电_触发")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109642?projectId=46'
    )
    @pytest.mark.debug_01
    def test_HvActive_caseid_109642(self): 
        with allure.step(f"Step:设置inactive"):
            # UsageMode 设置为01 inactive
            self.sd_tester.change_usage_mode(1)
            sleep(1)
        with allure.step(f"Step:设置BattURaw"):
            # LIN6信号 设置为11.8 BattURaw
            self.ipdu.send_pdu("cem_lin6", 0x06, [0xE8, 0x7F, 0x88, 0xff, 0xff, 0xff, 0xff])
            sleep(0.5)
            self.ipdu.send_pdu("cem_lin6", 0x04, [0x00, 0x60, 0xA8, 0x0B, 0x00, 0xff, 0xA1])
            sleep(0.5)
            self.ipdu.send_pdu("cem_lin6", 0x02, [0x20, 0x80, 0x00, 0x00, 0x00, 0x80, 0x00,0XF0])
            sleep(0.5)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr06,'DispHvBattLvlOfChrg',600)
            sleep(0.5)
        with allure.step(f"Step:仿真CnvnAllwd 为1 "):
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'CnvnAllwd',1)
            sleep(0.5)   
        with allure.step(f"Step:执行操作确保BGM进入睡眠状态"):
            logger.info("诊断激活线断开")
            # set_bgm_diag_active_line("disconntected")
            self.io.brake_up()
            sleep(1)
            self.sd_tester.stop_tester_present()
            self.sd_tester.diagnostic_client_sim_close()
             #四门两盖关闭
            self.dk.set_door_opener_sts(0, 0, 0, 0, 0)  # 设置bodycan上五个电动门均关闭
            # self.io.init_bgm_HW()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
            sleep(1)
            self.ipdu.pause_all_bus_send()  # 停止数据模拟(数据库周期性报文和调度表)
            sleep(1)
            self.ipdu.send_pdu("cem_lin6", 0x06, [0xE8, 0x7F, 0x88, 0xff, 0xff, 0xff, 0xff])
            sleep(700)
        with allure.step(f"Step:检测唤醒源"):
            self.ipdu.resume_all_bus_send()
            sleep(0.5)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'CnvnAllwd',1)
            sleep(0.5)
        with allure.step(f"检测是否CnvnReq=1"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq',1, 
            )   
        with allure.step(f"检测是否TiLVBattChrgn=10"):
            self.ipdu.check(
                self.ipdu.connectivitycanfd.BgmConnectivityFr06, 'TiLVBattChrgn', 10, 
            )
            sleep(5)
        
        self.sd_tester.update_serverdoipid(0x1002)
        sleep(0.5)
        self.sd_tester.diagnostic_client_sim_start()
        sleep(2)
        self.sd_tester.tester_present()
        sleep(0.5)

    @allure.title("智能补电_超时补电_停止")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109491?projectId=46'
    )
    @pytest.mark.debug_01
    def test_HvActive_caseid_109493(self): 
        with allure.step(f"Step:设置inactive"):
            # UsageMode 设置为01 inactive
            self.sd_tester.change_usage_mode(1)
            sleep(1)
        with allure.step(f"Step:设置BattURaw"):
            # LIN6信号 设置为11.8 BattURaw
            self.ipdu.send_pdu("cem_lin6", 0x06, [0xE8, 0x7F, 0xC8, 0xff, 0xff, 0xff, 0xff])
            sleep(1)
        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0, 
            )
            sleep(480)

        with allure.step(f"检测是否CnvnReq=1"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq',1, 
            )   
        with allure.step(f"检测是否TiLVBattChrgn=10"):
            self.ipdu.check(
                self.ipdu.connectivitycanfd.BgmConnectivityFr06, 'TiLVBattChrgn', 10, 
            )
            sleep(5)
        
    @allure.title("智能补电_低压故障_LVPwrSplyErrSts=5")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109440?projectId=46'
    )
    @pytest.mark.full
    def test_HvActive_caseid_109440(self): 
        with allure.step(f"Step:设置BattURaw"):
            # LIN6信号 设置为11.8 BattURaw
            self.sd_tester.change_usage_mode(1)
            self.ipdu.send_pdu("cem_lin6", 0x06, [0xE8, 0x7F, 0xC8, 0xff, 0xff, 0xff, 0xff])
            sleep(1)
            self.ipdu.resume_bus_send("cem_lin6")
        with allure.step(f"Step:仿真DcDcactvd 为1 避免低压报06"):
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'DcDcActvd',1)
            sleep(1) 
            self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattSnsrHwFltRaw', 1)
            sleep(10)
            self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattSnsrHwFltRaw', 1)
            sleep(10)
        with allure.step(f"Step:设置Driving"):
            # UsageMode 设置为13 Driving
            self.sd_tester.change_usage_mode(13)
            sleep(5)
        with allure.step(f"检测是否LVPwrSplyErrSts=5"): 
            sleep(1)  
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'LVPwrSplyErrSts', 5)
        
        with allure.step(f"Step:恢复Lin6通讯"):
            self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattSnsrHwFltRaw', 0)  
            sleep(1)

    # @allure.title("智能补电_低压故障_LVPwrSplyErrSts=6")
    # @allure.testcase(
    #     'https://jama.jiduauto.com/perspective.req#/testCases/109440?projectId=46'
    # )
    # @pytest.mark.smoke
    # def test_HvActive_caseid_109442(self): 
    #     with allure.step(f"Step:设置BattURaw"):
    #         # LIN6信号 设置为11.8 BattURaw
    #         self.ipdu.send_pdu("cem_lin6", 0x06, [0xE8, 0x7F, 0xC8, 0xff, 0xff, 0xff, 0xff])
    #         sleep(1)
    #         self.ipdu.resume_bus_send("cem_lin6")
    #     with allure.step(f"Step:仿真DcDcactvd 为1 避免低压报06"):
    #         self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'DcDcActvd',0)
    #         sleep(1) 
    #         self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattSnsrHwFltRaw', 1)
    #         sleep(10)
    #         self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattSnsrHwFltRaw', 1)
    #         sleep(10)
    #     with allure.step(f"Step:设置Driving"):
    #         # UsageMode 设置为13 Driving
    #         self.sd_tester.change_usage_mode(13)
    #         sleep(5)
    #     with allure.step(f"检测是否LVPwrSplyErrSts=6"): 
    #         sleep(1)  
    #         self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'LVPwrSplyErrSts', 6)
        
    #     with allure.step(f"Step:恢复Lin6通讯"):
    #         self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattSnsrHwFltRaw', 0)  
    #         sleep(1)

    @allure.title("智能补电_低压故障_ULoWarn = ULoPrmnt")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109440?projectId=46'
    )
    @pytest.mark.full
    def test_HvActive_caseid_109441(self): 
        with allure.step(f"Step:设置Driving"):
            # UsageMode 设置为13 Driving
            self.sd_tester.change_usage_mode(13)
            sleep(1)
        with allure.step(f"Step:设置BattURaw"):
            # LIN6信号 设置为11.8 BattURaw
            self.ipdu.send_pdu("cem_lin6", 0x06, [0xE8, 0x7F, 0xC8, 0xff, 0xff, 0xff, 0xff])
            sleep(1)
            self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr01, 'BattSftySigSysSaftyBattI', 0)
            sleep(1)
            self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr01, 'BattSftySigSysSaftyBattU', 11)
            sleep(1)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00,'EngSt1WdStsEngSt1WdSts',5)
            sleep(65)
        
        with allure.step(f"检测是否ULoWarnULoWarn=2"): 
            sleep(1)  
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn', 2)

    @allure.title("智能补电_系统故障_CnvnAllwd=OK切NOK")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/118538?projectId=46'
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_118538(self): 
        with allure.step(f"Step:设置inactive"):
            # UsageMode 设置为01 inactive
            self.sd_tester.change_usage_mode(1)
            sleep(1)
        with allure.step(f"Step:设置BattURaw"):
            # LIN6信号 设置为11.8 BattURaw
            self.ipdu.send_pdu("cem_lin6", 0x06, [0xE8, 0x7F, 0xC8, 0xff, 0xff, 0xff, 0xff])
            sleep(1)
            self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattSnsrHwFltRaw', 1)
            self.ipdu.pause_bus_send("cem_lin6")
            sleep(15)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'CnvnAllwd',1)
            sleep(1)
        with allure.step(f"检测是否CnvnReq=1"):
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 1,)  
        with allure.step(f"检测当前ChrgnUReq=13.5"):
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',13.5,)  
        with allure.step(f"Step:设置CnvnAllwd ok切Nok"):
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'CnvnAllwd',0)
            sleep(1)
        with allure.step(f"检测是否CnvnReq=1"):
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 1,)
            sleep(1)
        with allure.step(f"Step:恢复Lin6通讯"):
            self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattSnsrHwFltRaw', 0)
            self.ipdu.resume_bus_send("cem_lin6")
            sleep(1)
   
    @allure.title("智能补电_低压故障_CnvnAllwd=OK切NOK")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/118492?projectId=46'
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_118492(self): 
        with allure.step(f"Step:设置inactive"):
            # UsageMode 设置为01 inactive
            self.sd_tester.change_usage_mode(1)
            sleep(1)
        with allure.step(f"Step:设置BattURaw"):
            # LIN6信号 设置为5v BattURaw
            self.ipdu.send_pdu("cem_lin6", 0x06, [0xE8, 0x7F, 0x00, 0xff, 0xff, 0xff, 0xff])
            sleep(1)
            self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattSnsrHwFltRaw', 0)
            sleep(10)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'CnvnAllwd',1)
            sleep(1)
        with allure.step(f"检测是否CnvnReq=1"):
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 1,)  
        with allure.step(f"检测当前ChrgnUReq=14.4"):
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',14.4,)  
        with allure.step(f"Step:设置CnvnAllwd ok切Nok"):
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'CnvnAllwd',0)
            sleep(1)
        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0,10)  

    @allure.title("智能补电_低压故障_CnvnAllwd=OK切NOK")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/118492?projectId=46'
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_118493(self): 
        with allure.step(f"Step:设置inactive"):
            # UsageMode 设置为01 inactive
            self.sd_tester.change_usage_mode(1)
            sleep(1)
        with allure.step(f"Step:设置BattURaw"):
            # LIN6信号 设置为5v BattURaw
            self.ipdu.send_pdu("cem_lin6", 0x06, [0xE8, 0x7F, 0x00, 0xff, 0xff, 0xff, 0xff])
            sleep(1)
            self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattSnsrHwFltRaw', 0)
            sleep(10)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'CnvnAllwd',1)
            sleep(1)
        with allure.step(f"检测是否CnvnReq=1"):
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 1,)  
        with allure.step(f"检测当前ChrgnUReq=14.4"):
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',14.4,)  
        with allure.step(f"Step:设置CnvnAllwd ok切Nok"):
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'CnvnAllwd',0)
            sleep(3)
        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0,4)  
    
    @allure.title("智能补电_系统故障_多次触发")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109490?projectId=46'
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_109488(self): 
        with allure.step(f"Step:设置inactive"):
            # UsageMode 设置为01 inactive
            self.sd_tester.change_usage_mode(1)
            sleep(1)
        with allure.step(f"Step:设置BattURaw"):
            # LIN6信号 设置为5v BattURaw
            self.ipdu.send_pdu("cem_lin6", 0x06, [0xE8, 0x7F, 0xc8, 0xff, 0xff, 0xff, 0xff])
            sleep(1)
            self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattSnsrHwFltRaw', 1)
            sleep(20)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'CnvnAllwd',0)
            sleep(1)
        with allure.step(f"检测是否CnvnReq=1"):
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 1,)    
        with allure.step(f"Step:设置CnvnAllwd ok切Nok"):
            self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattSnsrHwFltRaw', 0)
            sleep(20)
        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0,4)
        with allure.step(f"Step:设置CnvnAllwd ok切Nok"):
            self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattSnsrHwFltRaw', 1)
            sleep(20)
        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 1,4)   


    @allure.title("智能补电_低压故障_多次触发")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109490?projectId=46'
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_109490_110410(self): 
        with allure.step(f"Step:设置inactive"):
            # UsageMode 设置为01 inactive
            self.sd_tester.change_usage_mode(1)
            sleep(1)
        with allure.step(f"Step:设置BattURaw"):
            # LIN6信号 设置为5v BattURaw
            self.ipdu.send_pdu("cem_lin6", 0x06, [0xE8, 0x7F, 0x00, 0xff, 0xff, 0xff, 0xff])
            sleep(1)
            self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattSnsrHwFltRaw', 0)
            sleep(10)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'CnvnAllwd',1)
            sleep(1)
        with allure.step(f"检测是否CnvnReq=1"):
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 1,)  
        with allure.step(f"检测当前ChrgnUReq=14.4"):
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',14.4,)  
        with allure.step(f"Step:设置CnvnAllwd ok切Nok"):
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'CnvnAllwd',0)
            sleep(3)
        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0,4)


    @allure.title("智能补电_服务补电_触发")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109491?projectId=46'
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_109491(self): 
        with allure.step(f"Step:设置inactive"):
            # UsageMode 设置为01 inactive
            self.sd_tester.change_usage_mode(1)
            sleep(1)
        with allure.step(f"Step:设置BattURaw停止补电"):
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'CnvnAllwd',0)
            self.ipdu.send_pdu("cem_lin6", 0x06, [0x0, 0x7c, 0xc8, 0xff, 0xff, 0xff, 0xff])
            self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattSnsrHwFltRaw', 0)
            sleep(3)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'CnvnAllwd',1)
            sleep(3)
        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0, 
            )
        with allure.step(f"检测当前ChrgnUReq=13.5"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',13.5,
            )
        with allure.step(f"高压服务请求"):
            self.partner = S2sBaseClass([("HighVoltageService", "client")])
            self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetOutput", {"on": True})
            sleep(3)
        with allure.step(f"检测是否CnvnReq=1"):
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 1,) 
            sleep(10) 
        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0,)    
        with allure.step(f"停止服务请求"):
            self.partner.stop_operators() 
    
    @allure.title("智能补电_补电_Convenience")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/118488?projectId=46'
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_118488(self): 
        with allure.step(f"Step:设置初始条件"):
            self.trigger_low_voltage_req()
            sleep(5)
        with allure.step(f"Step:usgmod由01inactive切换为02Convenience"):    
            # UsageMode 设置为02Convenience
            self.sd_tester.change_usage_mode(1)
            sleep(5)
            self.sd_tester.change_usage_mode(2)
            sleep(1)
        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0, 1
            )  
        with allure.step(f"检测当前ChrgnUReq=13.5"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',13.5,
            )  
        sleep(5)
    
    @allure.title("智能补电_IPM_触发")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109491?projectId=46'
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_1919302(self): 
        with allure.step(f"Step:设置inactive"):
            # UsageMode 设置为01 inactive
            self.sd_tester.change_usage_mode(1)
            sleep(1)
        with allure.step(f"Step:设置BattURaw停止补电"):
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'CnvnAllwd',0)
            self.ipdu.send_pdu("cem_lin6", 0x06, [0x0, 0x7c, 0xc8, 0xff, 0xff, 0xff, 0xff])
            self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattSnsrHwFltRaw', 0)
            sleep(3)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'CnvnAllwd',1)
            sleep(3)
        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0, 
            )
        with allure.step(f"检测当前ChrgnUReq=13.5"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',13.5,
            )
        with allure.step(f"IPM触发请求补电"):
            self.sd_tester.change_usage_mode(0)
            self.ipdu.set(self.ipdu.bodycan.IpmBodyFr01, 'IPMLoUWakeUpReq', 1)
        with allure.step(f"检测是否CnvnReq=1"):
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 1,) 
        #    self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,'VehModMngtGlbSafe1UsgModSts_0_CEMBackBoneSignalIpdu02', 1,)
            self.ipdu.set(self.ipdu.bodycan.IpmBodyFr01, 'IPMLoUWakeUpReq', 0)
            sleep(10) 

    @allure.title("智能补电_IPM_Convenience触发")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109491?projectId=46'
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_1919304(self): 
        with allure.step(f"Step:设置inactive"):
            # UsageMode 设置为01 inactive
            self.sd_tester.change_usage_mode(1)
            sleep(1)
        with allure.step(f"Step:设置BattURaw停止补电"):
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'CnvnAllwd',0)
            self.ipdu.send_pdu("cem_lin6", 0x06, [0x0, 0x7c, 0xc8, 0xff, 0xff, 0xff, 0xff])
            self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattSnsrHwFltRaw', 0)
            sleep(3)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'CnvnAllwd',1)
            sleep(3)
        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0, 
            )
        with allure.step(f"检测当前ChrgnUReq=13.5"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',13.5,
            )
        with allure.step(f"IPM触发请求补电"):
            self.sd_tester.change_usage_mode(0)
            self.ipdu.set(self.ipdu.bodycan.IpmBodyFr01, 'IPMLoUWakeUpReq', 1)
        with allure.step(f"检测是否CnvnReq=1"):
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 1,) 
        #    self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,'VehModMngtGlbSafe1UsgModSts_0_CEMBackBoneSignalIpdu02', 1,)
            sleep(10)  
        with allure.step(f"usgmod 切换到Convenience"):
            self.sd_tester.change_usage_mode(2)
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0,)
            self.ipdu.set(self.ipdu.bodycan.IpmBodyFr01, 'IPMLoUWakeUpReq', 0)

    @allure.title("智能补电_IPM_Active触发")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109491?projectId=46'
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_1919305(self): 
        with allure.step(f"Step:设置inactive"):
            # UsageMode 设置为01 inactive
            self.sd_tester.change_usage_mode(1)
            sleep(1)
        with allure.step(f"Step:设置BattURaw停止补电"):
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'CnvnAllwd',0)
            self.ipdu.send_pdu("cem_lin6", 0x06, [0x0, 0x7c, 0xc8, 0xff, 0xff, 0xff, 0xff])
            self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattSnsrHwFltRaw', 0)
            sleep(3)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'CnvnAllwd',1)
            sleep(3)
        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0, 
            )
        with allure.step(f"检测当前ChrgnUReq=13.5"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',13.5,
            )
        with allure.step(f"IPM触发请求补电"):
            self.sd_tester.change_usage_mode(0)
            self.ipdu.set(self.ipdu.bodycan.IpmBodyFr01, 'IPMLoUWakeUpReq', 1)
        with allure.step(f"检测是否CnvnReq=1"):
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 1,) 
        #    self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,'VehModMngtGlbSafe1UsgModSts_0_CEMBackBoneSignalIpdu02', 1,)
            sleep(10)  
        with allure.step(f"usgmod 切换到Active"):
            self.sd_tester.change_usage_mode(11)
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0,)
            self.ipdu.set(self.ipdu.bodycan.IpmBodyFr01, 'IPMLoUWakeUpReq', 0)

    @allure.title("智能补电_IPM_Driving触发")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109491?projectId=46'
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_1919306(self): 
        with allure.step(f"Step:设置inactive"):
            # UsageMode 设置为01 inactive
            self.sd_tester.change_usage_mode(1)
            sleep(1)
        with allure.step(f"Step:设置BattURaw停止补电"):
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'CnvnAllwd',0)
            self.ipdu.send_pdu("cem_lin6", 0x06, [0x0, 0x7c, 0xc8, 0xff, 0xff, 0xff, 0xff])
            self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattSnsrHwFltRaw', 0)
            sleep(3)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'CnvnAllwd',1)
            sleep(3)
        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0, 
            )
        with allure.step(f"检测当前ChrgnUReq=13.5"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',13.5,
            )
        with allure.step(f"IPM触发请求补电"):
            self.sd_tester.change_usage_mode(0)
            self.ipdu.set(self.ipdu.bodycan.IpmBodyFr01, 'IPMLoUWakeUpReq', 1)
        with allure.step(f"检测是否CnvnReq=1"):
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 1,) 
        #    self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,'VehModMngtGlbSafe1UsgModSts_0_CEMBackBoneSignalIpdu02', 1,)
            sleep(10)  
        with allure.step(f"usgmod 切换到Driving"):
            self.sd_tester.change_usage_mode(13)
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0,)
            self.ipdu.set(self.ipdu.bodycan.IpmBodyFr01, 'IPMLoUWakeUpReq', 0)

    @allure.title("智能补电_低压_多次触发")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109491?projectId=46'
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_1919308(self): 
        with allure.step(f"Step:设置inactive"):
            # UsageMode 设置为01 inactive
            self.sd_tester.change_usage_mode(1)
            sleep(1)
        with allure.step(f"Step:设置BattURaw停止补电"):
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'CnvnAllwd',0)
            self.ipdu.send_pdu("cem_lin6", 0x06, [0x0, 0x7c, 0xc8, 0xff, 0xff, 0xff, 0xff])
            self.ipdu.set(self.ipdu.cem_lin6.BmsCem_Lin6Fr03, 'BattSnsrHwFltRaw', 0)
            sleep(3)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'CnvnAllwd',1)
            sleep(3)
        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0, 
            )
        with allure.step(f"检测当前ChrgnUReq=13.5"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr06,'ChrgnUReq',13.5,
            )
        with allure.step(f"IPM触发请求补电"):
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'CnvnAllwd',1)
            self.ipdu.send_pdu("cem_lin6", 0x06, [0x0, 0x7c, 0x00, 0xff, 0xff, 0xff, 0xff])
            sleep(5)
        with allure.step(f"检测是否CnvnReq=1"):
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 1,) 
        with allure.step(f"usgmod 切换到Driving"): 
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr08,'CnvnAllwd',0)   
            result = self.ipdu.check_event(self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq',0, 1,timeout=30)
            logger.info("result {}".format(result))
            if result == 5:
                assert True
            else:
                assert False

    @allure.title("智能补电_超时补电_360分钟")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109411?projectId=46'
    )
    @pytest.mark.debug_01
    def test_HvActive_caseid_109411(self): 
        with allure.step(f"Step:设置inactive"):
            # UsageMode 设置为01 inactive
            self.sd_tester.change_usage_mode(1)
            sleep(1)
        with allure.step(f"Step:设置BattURaw"):
            # LIN6信号 设置为11.8 BattURaw
            self.ipdu.send_pdu("cem_lin6", 0x06, [0xE8, 0x7F, 0x88, 0xff, 0xff, 0xff, 0xff])
            sleep(1)
            self.ipdu.send_pdu("cem_lin6", 0x04, [0x00, 0x60, 0xA8, 0x0B, 0x00, 0xff, 0xA1])
            sleep(0.5)
            self.ipdu.send_pdu("cem_lin6", 0x02, [0x20, 0x80, 0x00, 0x00, 0x00, 0x80, 0x00,0XF0])
            sleep(0.5)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr06,'DispHvBattLvlOfChrg',600)
            sleep(0.5)

        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0, 
            )
            sleep(0.5)
            
        with allure.step(f"检测是否TiLVBattChrgn=10"):

            self.ipdu.check(
                self.ipdu.connectivitycanfd.BgmConnectivityFr06, 'TiLVBattChrgn', 10, 
            )
            sleep(5)
        with allure.step(f"检测是否TiLVBattChrgn=10"):
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr06,'DispHvBattLvlOfChrg',0)
            sleep(0.5)
        
        with allure.step(f"检测是否TiLVBattChrgn=360"):
            self.ipdu.check(
                self.ipdu.connectivitycanfd.BgmConnectivityFr06, 'TiLVBattChrgn', 360, 
            )
            sleep(5)

    @allure.title("智能补电_超时补电_10分钟")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/109477?projectId=46'
    )
    @pytest.mark.full 
    def test_HvActive_caseid_109477(self): 
        with allure.step(f"Step:设置inactive"):
            # UsageMode 设置为01 inactive
            self.sd_tester.change_usage_mode(1)
            sleep(1)
        with allure.step(f"Step:设置BattURaw"):
            # LIN6信号 设置为11.8 BattURaw
            self.ipdu.send_pdu("cem_lin6", 0x06, [0xE8, 0x7F, 0x88, 0xff, 0xff, 0xff, 0xff])
            sleep(2)
            self.ipdu.send_pdu("cem_lin6", 0x04, [0x00, 0x60, 0xA8, 0x0B, 0x00, 0xff, 0xA1])
            sleep(0.5)
            self.ipdu.send_pdu("cem_lin6", 0x02, [0x20, 0x80, 0x00, 0x00, 0x00, 0x80, 0x00,0XF0])
            sleep(0.5)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr06,'DispHvBattLvlOfChrg',600)
            sleep(0.5)
        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0, 
            )
            sleep(5)
        with allure.step(f"Step:重启BGM"):
            # LIN6信号 设置为11.8 BattURaw
            self.sd_tester.stop_tester_present()
            self.sd_tester.diagnostic_client_sim_close()

            self.io.set_do_level("BGM_P",True)
            sleep(1)
            self.io.set_do_level("BGM_P",False)
            sleep(20)
            
        with allure.step(f"检测是否TiLVBattChrgn=10"):
            self.ipdu.check(
                self.ipdu.connectivitycanfd.BgmConnectivityFr06, 'TiLVBattChrgn', 10, 
            )
            sleep(5)

        self.sd_tester.update_serverdoipid(0x1002)
        sleep(0.5)
        self.sd_tester.diagnostic_client_sim_start()
        sleep(2)
        self.sd_tester.tester_present()
        sleep(0.5)

    @allure.title("智能补电_上电默认值_360分钟")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1919278?projectId=46'
    )
    @pytest.mark.full 
    def test_HvActive_caseid_1919278(self): 
        with allure.step(f"Step:设置inactive"):
            # UsageMode 设置为01 inactive
            self.sd_tester.change_usage_mode(1)
            sleep(1)
        with allure.step(f"Step:设置BattURaw"):
            # LIN6信号 设置为11.8 BattURaw
            self.ipdu.send_pdu("cem_lin6", 0x06, [0xE8, 0x7F, 0x00, 0xff, 0xff, 0xff, 0xff])
            sleep(0.5)
        with allure.step(f"Step:重启BGM"):
            # LIN6信号 设置为11.8 BattURaw
            self.sd_tester.stop_tester_present()
            self.sd_tester.diagnostic_client_sim_close()

            self.io.set_do_level("BGM_P",True)
            sleep(1)
            self.io.set_do_level("BGM_P",False)
            sleep(20)
            self.sd_tester.update_serverdoipid(0x1002)
            sleep(0.5)
            self.sd_tester.diagnostic_client_sim_start()
            sleep(2)
            self.sd_tester.tester_present()
            sleep(0.5)
            self.ipdu.send_pdu("cem_lin6", 0x06, [0xE8, 0x7F, 0x00, 0xff, 0xff, 0xff, 0xff])
            sleep(0.5)
        with allure.step(f"检测是否TiLVBattChrgn=360"):
            self.ipdu.check(
                self.ipdu.connectivitycanfd.BgmConnectivityFr06, 'TiLVBattChrgn', 20160, 
            )
            sleep(5)
    
    @allure.title("智能补电_RTC时间计算_持续增加")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1919286?projectId=46'
    )
    @pytest.mark.full 
    def test_HvActive_caseid_1919286(self): 
        with allure.step(f"Step:设置inactive"):
            # UsageMode 设置为01 inactive
            self.sd_tester.change_usage_mode(0)
            sleep(1)
            self.sd_tester.change_usage_mode(1)
            sleep(1)
        with allure.step(f"Step:设置BattURaw"):
            # LIN6信号 设置为12.7 BattURaw
            self.ipdu.send_pdu("cem_lin6", 0x06, [0xE8, 0x7F, 0x9A, 0xff, 0xff, 0xff, 0xff])
            sleep(0.5)
            self.ipdu.send_pdu("cem_lin6", 0x04, [0x00, 0x60, 0xA8, 0x0B, 0x00, 0xff, 0xA1])
            sleep(0.5)
            self.ipdu.send_pdu("cem_lin6", 0x02, [0x20, 0x80, 0x00, 0x00, 0x00, 0x80, 0x00,0XF0])
            sleep(0.5)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr06,'DispHvBattLvlOfChrg',600)
            sleep(0.5)
        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0, 
            )
            sleep(5)
        with allure.step(f"检测是否TiLVBattChrgn=154"):
            self.ipdu.check(
                self.ipdu.connectivitycanfd.BgmConnectivityFr06, 'TiLVBattChrgn', 154, 
            )
            sleep(5)
        with allure.step(f"补电1分钟 检测是否TiLVBattChrgn=154"):
            self.ipdu.send_pdu("cem_lin6", 0x02, [0x00, 0x99, 0x00, 0x00, 0x00, 0x80, 0x00,0XF0])
            sleep(10)
            self.ipdu.check(
                self.ipdu.connectivitycanfd.BgmConnectivityFr06, 'TiLVBattChrgn', 164, 
            )
    
    @allure.title("智能补电_RTC时间计算_持续减少")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1919285?projectId=46'
    )
    @pytest.mark.full 
    def test_HvActive_caseid_1919285(self): 
        with allure.step(f"Step:设置inactive"):
            # UsageMode 设置为01 inactive
            self.sd_tester.change_usage_mode(0)
            sleep(1)
            self.sd_tester.change_usage_mode(1)
            sleep(1)
        with allure.step(f"Step:设置BattURaw"):
            # LIN6信号 设置为12.7 BattURaw
            self.ipdu.send_pdu("cem_lin6", 0x06, [0xE8, 0x7F, 0x9A, 0xff, 0xff, 0xff, 0xff])
            sleep(3)
            self.ipdu.send_pdu("cem_lin6", 0x04, [0x00, 0x60, 0xA8, 0x0B, 0x00, 0xff, 0xA1])
            sleep(0.5)
            self.ipdu.send_pdu("cem_lin6", 0x02, [0x20, 0x80, 0x00, 0x00, 0x00, 0x80, 0x00,0XF0])
            sleep(0.5)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr06,'DispHvBattLvlOfChrg',600)
            sleep(0.5)
        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0, 
            )
            sleep(5)
        with allure.step(f"检测是否TiLVBattChrgn=154"):
            self.ipdu.check(
                self.ipdu.connectivitycanfd.BgmConnectivityFr06, 'TiLVBattChrgn', 154, 
            )
            sleep(5)
        with allure.step(f"补电1分钟 检测是否TiLVBattChrgn=143"):
            self.ipdu.send_pdu("cem_lin6", 0x02, [0x00, 0x67, 0x00, 0x00, 0x00, 0x80, 0x00,0XF0])
            sleep(10)
            self.ipdu.check(
                self.ipdu.connectivitycanfd.BgmConnectivityFr06, 'TiLVBattChrgn', 143, 
            )    ### 监测TiLVBattChrgn', 18    2分钟

        ###self.ipdu.send_pdu("cem_lin6", 0x02, [0x20, 0x80, 0x00, 0x00, 0x00, 0x80, 0x00,0XF0])发送3帧
        ####self.ipdu.check(
        #        self.ipdu.connectivitycanfd.BgmConnectivityFr06, 'TiLVBattChrgn', 143, 
        #    ) 希望TiLVBattChrgn', 18 还是18不变化


    @allure.title("智能补电_RTC时间计算_持续减少")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1919285?projectId=46'
    )
    @pytest.mark.full 
    def test_HvActive_caseid_1919285(self): 
        with allure.step(f"Step:设置inactive"):
            # UsageMode 设置为01 inactive
            self.sd_tester.change_usage_mode(0)
            sleep(1)
            self.sd_tester.change_usage_mode(1)
            sleep(1)
        with allure.step(f"Step:设置BattURaw"):
            # LIN6信号 设置为12.7 BattURaw
            self.ipdu.send_pdu("cem_lin6", 0x06, [0xE8, 0x7F, 0x9A, 0xff, 0xff, 0xff, 0xff])
            sleep(3)
            self.ipdu.send_pdu("cem_lin6", 0x04, [0x00, 0x60, 0xA8, 0x0B, 0x00, 0xff, 0xA1])
            sleep(0.5)
            self.ipdu.send_pdu("cem_lin6", 0x02, [0x20, 0x80, 0x00, 0x00, 0x00, 0x80, 0x00,0XF0])
            sleep(0.5)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr06,'DispHvBattLvlOfChrg',600)
            sleep(0.5)
        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0, 
            )
            sleep(5)
        with allure.step(f"检测是否TiLVBattChrgn=154"):
            self.ipdu.check(
                self.ipdu.connectivitycanfd.BgmConnectivityFr06, 'TiLVBattChrgn', 154, 
            )
            sleep(5)
        with allure.step(f"补电1分钟 检测是否TiLVBattChrgn=143"):
            self.ipdu.send_pdu("cem_lin6", 0x02, [0x00, 0x67, 0x00, 0x00, 0x00, 0x80, 0x00,0XF0])
            sleep(10)
            self.ipdu.check(
                self.ipdu.connectivitycanfd.BgmConnectivityFr06, 'TiLVBattChrgn', 143, 
            )

    @allure.title("智能补电_RTC时间计算_查表10分钟")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1919285?projectId=46'
    )
    @pytest.mark.full 
    def test_HvActive_caseid_1919279(self): 
        with allure.step(f"Step:设置inactive"):
            # UsageMode 设置为01 inactive
            self.sd_tester.change_usage_mode(0)
            sleep(1)
            self.sd_tester.change_usage_mode(1)
            sleep(1)
        with allure.step(f"Step:设置BattURaw"):
            # LIN6信号 设置为12.7 BattURaw
            self.ipdu.send_pdu("cem_lin6", 0x06, [0xE8, 0x7F, 0x9A, 0xff, 0xff, 0xff, 0xff])
            sleep(3)
        with allure.step(f"Step:重启BGM"):
            self.sd_tester.stop_tester_present()
            self.sd_tester.diagnostic_client_sim_close()
            self.io.set_do_level("BGM_P",True)
            sleep(1)
            self.io.set_do_level("BGM_P",False)
            sleep(20)
            
            self.sd_tester.update_serverdoipid(0x1002)
            sleep(0.5)
            self.sd_tester.diagnostic_client_sim_start()
            sleep(2)
            self.sd_tester.tester_present()
            sleep(0.5)

        with allure.step(f"检测是否TiLVBattChrgn=154"):
            self.ipdu.check(
                self.ipdu.connectivitycanfd.BgmConnectivityFr06, 'TiLVBattChrgn', 154, 
            )
            sleep(5)

    @allure.title("智能补电_RTC时间计算_持续减少")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1919285?projectId=46'
    )
    @pytest.mark.full 
    def test_HvActive_caseid_2345678(self): 
        with allure.step(f"Step:设置inactive"):
            # UsageMode 设置为01 inactive
            self.sd_tester.change_usage_mode(0)
            sleep(1)
            self.sd_tester.change_usage_mode(1)
            sleep(1)
        with allure.step(f"Step:设置BattURaw"):
            # LIN6信号 设置为12.7 BattURaw
            self.ipdu.send_pdu("cem_lin6", 0x06, [0xE8, 0x7F, 0x9A, 0xff, 0xff, 0xff, 0xff])
            sleep(3)
            self.ipdu.send_pdu("cem_lin6", 0x04, [0x00, 0x60, 0xA8, 0x0B, 0x00, 0xff, 0xA1])
            sleep(0.5)
            self.ipdu.send_pdu("cem_lin6", 0x02, [0x20, 0x80, 0x00, 0x00, 0x00, 0x80, 0x00,0XF0])
            sleep(0.5)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr06,'DispHvBattLvlOfChrg',600)
            sleep(0.5)
        with allure.step(f"检测是否CnvnReq=0"):
            self.ipdu.check(
                self.ipdu.backbonefr.CemBackBoneFr03, 'CnvnReq', 0, 
            )
            sleep(5)
        with allure.step(f"检测是否TiLVBattChrgn=154"):
            self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr06, 'TiLVBattChrgn', 90)
            sleep(5)
        with allure.step(f"补电1分钟 检测是否TiLVBattChrgn=143"):
            self.ipdu.send_pdu("cem_lin6", 0x02, [0x00, 0x67, 0x00, 0x00, 0x00, 0x80, 0x00,0XF0])
            sleep(10)

        running_time = 0
        while True:
            expectedvalue = self.ipdu.get_recent_signal_raw_value(self.ipdu.connectivitycanfd.BgmConnectivityFr06, 'TiLVBattChrgn')
            logger.info(f"获取补电时间分钟:{expectedvalue}")
            if int(expectedvalue) == 18:
                self.ipdu.send_pdu("cem_lin6", 0x02, [0x00, 0x85, 0x00, 0x00, 0x00, 0x80, 0x00,0XF0])
                sleep(5)
                expectedvalue = self.ipdu.get_recent_signal_raw_value(self.ipdu.connectivitycanfd.BgmConnectivityFr06, 'TiLVBattChrgn')
                logger.info(f"获取实际的补电时间:{expectedvalue}")
                self.ipdu.send_pdu("cem_lin6", 0x02, [0x20, 0x80, 0x00, 0x00, 0x00, 0x80, 0x00,0XF0])
                sleep(0.1)
                self.ipdu.send_pdu("cem_lin6", 0x02, [0x00, 0x85, 0x00, 0x00, 0x00, 0x80, 0x00,0XF0])
                sleep(5)
                expectedvalue = self.ipdu.get_recent_signal_raw_value(self.ipdu.connectivitycanfd.BgmConnectivityFr06, 'TiLVBattChrgn')
                logger.info(f"获取实际补电时间分钟:{expectedvalue}")
                assert int(expectedvalue) == 20
                break
            else:
                if running_time > 10*60:
                    break
                else:
                    sleep(0.02)
                    running_time = running_time + 0.02
                    logger.info("还没有获取到TiLVBattChrgn = 18，继续")
    
    