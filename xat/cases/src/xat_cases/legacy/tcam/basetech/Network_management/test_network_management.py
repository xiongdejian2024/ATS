#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename     : test_network_management.py
@time         : 2024/09/02
@author       : junxing.pang@jiduauto.com
'''


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

bgm_log_goto_sleep = ""
bgm_log_awakeup = ""

@allure.feature("软件平台/网络管理")
class TestCertificate(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.bus_comm.set_SOC_display_value(800)
        self.soa.update(["CallService_client"])
        sleep(2)
        global ip
        ip = self.tc_config.get('gateway_ip')


    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_up()
        sleep(3)
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_FLDOOR_SW)
        sleep(5)
        
    def after_class(self, ecu):
        super().after_class(self, ecu) 
        self.io.bgm_diag_line_up()
        with allure.step("初始化环境"):
            self.mix.init_boot_per()

    @pytest.mark.smoke
    @allure.title("TCAM_wakeup_by_ConnectivityCAN:NM报文唤醒测试")
    def test_caseid_1986735(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_CONNCANFD)
        msg = self.bus_comm.recv_pdu("connectivitycanfd", 0x509, timeout=2)
        logger.info(f"检查唤醒时connectivitycanfd上报文的结果是{msg}")
        assert msg[-1][1] == 64 #查看509报文第一个字节是否是被动唤醒

    @pytest.mark.full
    @allure.title("PNC27_SOS置位测试")
    def test_caseid_1986727(self):    
        self.soa.trigger_call_sos_notcheck_funsts_by_soa_partner(ReqSrc=eCallReqSource.kCDC)    
        sleep(4)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x509, TCAMPNC.PNC27, NMSts.valid) #check pnc置位
        sleep(5)
        self.soa.hang_up_call_sos_not_check_funsts(ReqSrc=eCallReqSource.kCDC)

    @pytest.mark.full
    @allure.title("PNC30_IP发送远程解闭锁PNC置位测试")
    def test_caseid_1986726(self): 
        self.bus_comm.resume_bus_send('connectivitycanfd')
        self.tsp.rvc_lock_control(1)  
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x509, TCAMPNC.PNC30, NMSts.valid,timeout=30) #check pnc置位
        
    @pytest.mark.smoke
    @allure.title("TCAM_wakeup_by_IP发送远控指令")
    def test_caseid_1986729(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.mix.network_sleep() 
        self.tsp.rvc_lock_control(1)   
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_CONNCANFD)

    @pytest.mark.sanity
    @allure.title("PNC27_ecall置位及释放测试")
    def test_caseid_1986713(self):    
        self.soa.trigger_call_sos_notcheck_funsts_by_soa_partner(ReqSrc=eCallReqSource.kCDC)    
        sleep(4)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x509, TCAMPNC.PNC27, NMSts.valid) #check pnc置位
        sleep(5)
        self.soa.hang_up_call_sos_not_check_funsts(ReqSrc=eCallReqSource.kCDC)
        msg = self.bus_comm.check_bus_recv_message("connectivitycanfd")  
        logger.info(f"检查休眠时connectivitycanfd上报文的结果是{msg}")

    @pytest.mark.full
    @allure.title("TCAM_Sleep休眠测试")
    def test_caseid_1986728(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.mix.network_sleep()    
        msg = self.bus_comm.check_bus_recv_message("connectivitycanfd")  
        logger.info(f"检查休眠时connectivitycanfd上报文的结果是{msg}")
        assert msg == None, f"休眠检查失败"   
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_CONNCANFD)

    @pytest.mark.sanity
    @allure.title("第一帧NM报文发出时间测试")
    def test_caseid_1986717(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_CONNCANFD)
        msg = self.bus_comm.recv_pdu("connectivitycanfd", 0x509, timeout=0.2)
        logger.info(f"检查唤醒时connectivitycanfd上报文的结果是{msg}")
        assert msg != None 

    @pytest.mark.smoke
    @allure.title("应用报文不会唤醒TCAM")
    def test_caseid_1986718(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.mix.network_sleep()
        self.bus_comm.send_pdu("connectivitycanfd", 0x164, "00 00 00 00 00 00 00 00", 0.5)
        time.sleep(5)
        self.bus_comm.stop_send_pdu("connectivitycanfd", 0x164)
        logger.info(f"校验应用报文不会唤醒TCAM") 
        msg = self.bus_comm.check_bus_recv_message("connectivitycanfd")  
        assert msg == None, f"应用报文异常唤醒TCAM" 

    @pytest.mark.smoke
    @allure.title("BGM_wake_sleep_by_BodyExposedCAN")
    def test_caseid_101352(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYEXPCANCANFD)
        msg = self.bus_comm.recv_pdu("connectivitycanfd", 0x509, timeout=2)
        logger.info(f"检查唤醒时connectivitycanfd上报文的结果是{msg}")
        assert msg[-1][1] == 64 #查看509报文第一个字节是否是被动唤醒  

    @pytest.mark.smoke
    @allure.title("BGM_wake_sleep_by_ChassisCAN1")
    def test_caseid_101351(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_CLASSICCAN1)
        msg = self.bus_comm.recv_pdu("connectivitycanfd", 0x509, timeout=2)
        logger.info(f"检查唤醒时connectivitycanfd上报文的结果是{msg}")
        assert msg[-1][1] == 64 #查看509报文第一个字节是否是被动唤醒  

    @pytest.mark.full
    @allure.title("BGM_wake_sleep_by_ChassisCAN2")
    def test_caseid_101353(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_CLASSICCAN2)
        msg = self.bus_comm.recv_pdu("connectivitycanfd", 0x509, timeout=2)
        logger.info(f"检查唤醒时connectivitycanfd上报文的结果是{msg}")
        assert msg[-1][1] == 64 #查看509报文第一个字节是否是被动唤醒               

    @pytest.mark.full
    @allure.title("BGM_wake_sleep_by_DiagnosticCAN")
    def test_caseid_101348(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_DIAGCAN)
        msg = self.bus_comm.recv_pdu("connectivitycanfd", 0x509, timeout=2)
        logger.info(f"检查唤醒时connectivitycanfd上报文的结果是{msg}")
        assert msg[-1][1] == 64 #查看509报文第一个字节是否是被动唤醒  

    @pytest.mark.full
    @allure.title("BGM_wake_sleep_by_InfoCAN")
    def test_caseid_101354(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_INFOCAN)
        msg = self.bus_comm.recv_pdu("connectivitycanfd", 0x509, timeout=2)
        logger.info(f"检查唤醒时connectivitycanfd上报文的结果是{msg}")
        assert msg[-1][1] == 64 #查看509报文第一个字节是否是被动唤醒    

    @pytest.mark.full
    @allure.title("BGM_wake_sleep_by_PassiveSafetyCAN")
    def test_caseid_101350(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_PASSIVESAFETYCAN)
        msg = self.bus_comm.recv_pdu("connectivitycanfd", 0x509, timeout=2)
        logger.info(f"检查唤醒时connectivitycanfd上报文的结果是{msg}")
        assert msg[-1][1] == 64 #查看509报文第一个字节是否是被动唤醒  

    @pytest.mark.full
    @allure.title("BGM_wake_sleep_by_PropulsionCAN")
    def test_caseid_101349(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_PROPULSIONCAN)
        msg = self.bus_comm.recv_pdu("connectivitycanfd", 0x509, timeout=2)
        logger.info(f"检查唤醒时connectivitycanfd上报文的结果是{msg}")
        assert msg[-1][1] == 64 #查看509报文第一个字节是否是被动唤醒  

    @pytest.mark.full
    @allure.title("BGM_wake_sleep_by_SmartALMCAN1")
    def test_caseid_101347(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_ALM1)
        msg = self.bus_comm.recv_pdu("connectivitycanfd", 0x509, timeout=2)
        logger.info(f"检查唤醒时connectivitycanfd上报文的结果是{msg}")
        assert msg[-1][1] == 64 #查看509报文第一个字节是否是被动唤醒

    @pytest.mark.full
    @allure.title("BGM_wake_sleep_by_ConnectivityCAN")
    def test_caseid_101346(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_CONNCANFD)
        msg = self.bus_comm.recv_pdu("connectivitycanfd", 0x509, timeout=2)
        logger.info(f"检查唤醒时connectivitycanfd上报文的结果是{msg}")
        assert msg[-1][1] == 64 #查看509报文第一个字节是否是被动唤醒   

    @pytest.mark.smoke
    @allure.title("TCAM_wake_sleep_by_hardline")
    def test_caseid_101355(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.mix.network_sleep()
        logger.info("接通BGM诊断激活线")
        self.io.bgm_diag_line_up()
        msg = self.bus_comm.recv_pdu("connectivitycanfd", 0x509, timeout=2)
        logger.info(f"检查唤醒时connectivitycanfd上报文的结果是{msg}")
        assert msg[-1][1] == 64,f"BGM接通诊断激活线，TCAM唤醒失败"#查看509报文第一个字节是否是被动唤醒     

     