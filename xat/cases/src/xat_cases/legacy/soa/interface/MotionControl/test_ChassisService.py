#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_ChassisService.py
@Time         :2023/05/23
@Author       :wenyu.liang_ext@jiduauto.com
@Description  :
"""
import allure
import pytest
import time
import random
from time import sleep
from xat_ecu.legacy.common.data_type_handing import logger
from xat_ecu.legacy.interface.nuc_app import get_obd_ip
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.sdk.sdk_tools import *
from xat_cases.legacy.soa.case_helper.utils import *

@allure.feature("SOA服务接口")
@allure.story("运动控制/ChassisService")
@pytest.mark.aqx
class TestChassisService(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.partner = S2sBaseClass([("ChassisService", "client")])
        self.partner.method_default_timeout = 0.1
        self.sd_tester.tester_present()

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.partner.stop_operators()        
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkNotEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set_vehspd(0)
        sleep(1)
        self.sd_tester.change_usage_mode(1)
        self.sd_tester.change_car_mode(0)
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()
        sleep(1)
        super().after_each_func(ecu, start=False)

    def ck_pdu(self,file_path,save_name,data_list1,data_list2):
        self.bgmcli.stop_bgm_tcpdump()
        file_path=self.bgmcli.scp_bgm_log_to_local(bgm_log_name=save_name)
        self.bgmcli.delete_bgm_tcpdump_file(bgm_log_name='*.pcap')
        ret, res_dict = check_pdu(data_list1, file_path) 
        res_dict=get_pdu_value_and_time(data_list2, file_path)
        if ret==False :
             assert False, f"对应信号不存在" 

    def chassis_fault_default(self): # WhlSpdCircumlReLeQf| WhlSpdCircumlFrntRiQf
        '''清空当前chassis模块故障列表'''
        list_WhlSpdCircuml=["WhlSpdCircumlFrntLeQf","WhlSpdCircumlFrntRiQf","WhlSpdCircumlReLeQf","WhlSpdCircumlReRiQf"]
        for i in range(4):
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, f'{list_WhlSpdCircuml[i]}', 3) # 故障列表没有 3-6 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)  # 故障列表没有 1，2 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 4) # 故障列表没有 15  
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'AutHldSoftSwtEnaSts', 0) # 故障列表没有 16  
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetChassisFault", {},{"out": [0]},timeout=3)
        self.partner.empty_all()
            
    def ck_Gear_and_GetGear(self, gear, timeout=3):
        """校验指定Gear事件，并请求GetGear获取结果"""
        self.partner.ck_s2s_event("ChassisService_client", "Gear", {"gear": gear}, timeout)
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetGear", {}, {"out": gear})

    def ck_no_event_and_GetGear(self, gear, timeout=3):
        """校验指定Gear事件，并请求GetGear获取结果"""
        self.partner.ck_no_event("ChassisService_client", "Gear")
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetGear", {}, {"out": gear})       
    
    def ck_brkSysWarnIndicateReqSts_and_getBrkSysWarnIndicateReqSts(self, sts, timeout=3):  
        # 获取&通知制动系统报警指示请求状态  
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "brkSysWarnIndicateReqSts", {"sts": sts})
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnIndicateReqSts", {}, {"out": sts}, timeout)
        
    def ck_no_event_and_getBrkSysWarnIndicateReqSts(self, sts, timeout=3):    
        # 获取&通知制动系统报警指示请求状态
        self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "brkSysWarnIndicateReqSts")
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnIndicateReqSts", {}, {"out": sts}, timeout)
        
    def ck_absWarnIndicateReqSts_and_getABSWarnIndicateReqSts(self, value, timeout=3):
        # 获取&通知ABS报警指示请求状态
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "absWarnIndicateReqSts",{"sts": value}, timeout)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getABSWarnIndicateReqSts", {}, {"out": value})   

    def ck_escWarnIndicateReqSts_and_getESCWarnIndicateReqSts(self, value, timeout=3):
        # 获取&通知ESC报警指示请求状态
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "escWarnIndicateReqSts",{"sts": value}, timeout)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getESCWarnIndicateReqSts", {}, {"out": value})   
            
    def reset_JiduVehicle(self, value, sleeptime):
        '''修改车辆配置 value=1 Mars1, 2 Venus, 3 Other'''
        self.sd_tester.write_single_ccp(950, value) # kCCPJiduVehicleType
        sleep(2)
        self.restart_bgm_and_connect_service(CHASSIS_SERVICE_CLIENT)
        sleep(sleeptime)

    def ck_WheelImpluseCounter_and_GetWheelImpluseCounter(self, wheelId=1, counter=0, isvalid=True, timeout=3):  
        '''单个 车轮旋转脉冲计数状态'''     
        self.partner.ck_s2s_event("ChassisService_client", "WheelImpluseCounter", 
                                  {"wheelsImpluseCounter":[{"wheelId":wheelId, "wheelImpluseCounter":counter, "isvalid":isvalid}]}, timeout=3)  
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetWheelImpluseCounter", {"wheels": [wheelId]}, 
                                            {"out": [{"wheelId": wheelId, "wheelImpluseCounter": counter, "isvalid": isvalid}]}) 
    
    def set_WhlRotToothCntr(self, signal=[0, 0, 0, 0], sleeptime=2):
        '''设置四车轮旋转脉冲计数状态信号'''
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlRotToothCntrFrntLe', signal[0])
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlRotToothCntrFrntRi', signal[1])
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlRotToothCntrReLe', signal[2])
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlRotToothCntrReRi', signal[3])
        sleep(sleeptime)
        
    def ck_All_WheelImpluseCounter_and_GetWheelImpluseCounter(self, counter=0, isvalid=True, timeout=3):  
        '''四个车轮旋转脉冲计数状态'''     
        self.partner.ck_s2s_event("ChassisService_client", "WheelImpluseCounter", 
                                  {"wheelsImpluseCounter":[{"wheelId":1, "wheelImpluseCounter":counter, "isvalid":isvalid}, 
                                                           {"wheelId":2, "wheelImpluseCounter":counter, "isvalid":isvalid},
                                                           {"wheelId":3, "wheelImpluseCounter":counter, "isvalid":isvalid},
                                                           {"wheelId":4, "wheelImpluseCounter":counter, "isvalid":isvalid}]}, timeout=3)  
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetWheelImpluseCounter", {"wheels": [1, 2, 3, 4]}, 
                                            {"out": [{"wheelId":1, "wheelImpluseCounter":counter, "isvalid":isvalid}, 
                                                     {"wheelId":2, "wheelImpluseCounter":counter, "isvalid":isvalid},
                                                     {"wheelId":3, "wheelImpluseCounter":counter, "isvalid":isvalid},
                                                     {"wheelId":4, "wheelImpluseCounter":counter, "isvalid":isvalid}]}) 
                
    def ck_no_event_and_GetWheelImpluseCounter(self, wheelId=1, counter=0, isvalid=0, timeout=3):  
        '''四个车轮旋转脉冲计数状态'''     
        self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "WheelImpluseCounter", timeout=3)
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetWheelImpluseCounter", {"wheels": [wheelId]}, 
                                            {"out": [{"wheelId": wheelId, "wheelImpluseCounter": counter, "isvalid": isvalid}]}) 

    @allure.title("获取&通知左前车轮旋转脉冲计数状态_isvalid=1")
    @pytest.mark.full
    def test_caseid_1981479(self): # WhlRotToothCntrFrntLe|WheelImpluseCounter|WheelImpluse_TimeOut
        for FrntLe in [1, 255, 249, 0]:
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlRotToothCntrFrntLe', FrntLe)
            self.ck_WheelImpluseCounter_and_GetWheelImpluseCounter(wheelId=1, counter=FrntLe, isvalid=True)
            
    @allure.title("获取&通知左后车轮旋转脉冲计数状态_isvalid=1") 
    @pytest.mark.full
    def test_caseid_1981481(self): 
        for FrntRi in [1, 255, 249, 0]:
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlRotToothCntrFrntRi', FrntRi)
            self.ck_WheelImpluseCounter_and_GetWheelImpluseCounter(wheelId=2, counter=FrntRi, isvalid=True)
            
    @allure.title("获取&通知右前车轮旋转脉冲计数状态_isvalid=1") 
    @pytest.mark.full
    def test_caseid_1981480(self): 
        for ReLe in [1, 255, 249, 0]:
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlRotToothCntrReLe', ReLe)
            self.ck_WheelImpluseCounter_and_GetWheelImpluseCounter(wheelId=3, counter=ReLe, isvalid=True)
            
    @allure.title("获取&通知右后车轮旋转脉冲计数状态_isvalid=1")
    @pytest.mark.smoke
    def test_caseid_1981482(self): 
        for ReRi in [1, 255, 249, 0]:
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlRotToothCntrReRi', ReRi)
            self.ck_WheelImpluseCounter_and_GetWheelImpluseCounter(wheelId=4, counter=ReRi, isvalid=True)      

    @allure.title("获取&通知车轮旋转脉冲计数状态_isvalid=0") 
    @pytest.mark.sanity
    def test_caseid_1981484(self): 
        self.set_WhlRotToothCntr([100, 100, 100, 100])
        self.ck_All_WheelImpluseCounter_and_GetWheelImpluseCounter(counter=100, isvalid=True)
        try:
            self.ipdu.set_no_crc(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlRotToothCntrFrntLe')
            sleep(2)
            self.ck_All_WheelImpluseCounter_and_GetWheelImpluseCounter(counter=100, isvalid=False)  
            self.partner.empty_all(2)
            self.set_WhlRotToothCntr()
            self.ck_All_WheelImpluseCounter_and_GetWheelImpluseCounter(counter=0, isvalid=False)
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlRotToothCntrFrntLe')
            assert False, error
        else:
            self.ipdu.restore_crc(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlRotToothCntrFrntLe')
        sleep(2)
        self.ck_All_WheelImpluseCounter_and_GetWheelImpluseCounter(counter=0, isvalid=True)
        
    @allure.title("获取&通知车轮旋转脉冲计数状态_信号丢失") 
    @pytest.mark.full
    def test_caseid_1981485(self): 
        self.set_WhlRotToothCntr([100, 100, 100, 100])
        self.ck_All_WheelImpluseCounter_and_GetWheelImpluseCounter(counter=100, isvalid=True)
        self.ipdu.pause_bus_send("backbonefr")
        self.ck_All_WheelImpluseCounter_and_GetWheelImpluseCounter(counter=100, isvalid=False, timeout=1.5)  
        self.ipdu.resume_bus_send("backbonefr")
        self.ck_All_WheelImpluseCounter_and_GetWheelImpluseCounter(counter=100, isvalid=True)                                      
    
    @allure.title("获取&通知档位状态P档_GearLvrIndcn=0_TrsmParkLockd=0")
    @pytest.mark.full
    def test_caseid_110767(self): 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 2)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.ck_Gear_and_GetGear(0)

    @allure.title("获取&通知档位状态P档_GearLvrIndcn=0_TrsmParkLockd=1")
    @pytest.mark.smoke
    def test_caseid_110678(self): 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 2)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 1)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.ck_Gear_and_GetGear(0)

    @allure.title("获取&通知档位状态P档_GearLvrIndcn=7_TrsmParkLockd=1")
    @pytest.mark.smoke 
    def test_caseid_110631(self):
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 2)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 1)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 7)
        self.ck_Gear_and_GetGear(0)

    @allure.title("获取&通知档位状态R档和D档")
    @pytest.mark.sanity
    def test_caseid_110592(self):
        for usgMod in [11,13]:
            self.sd_tester.change_usage_mode(usgMod)
            for signal1 in [0,1]:                
                self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', signal1)
                self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 3)
                self.ck_Gear_and_GetGear(3)
                self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 1)
                self.ck_Gear_and_GetGear(1)

    @allure.title("获取&通知档位状态N档")
    @pytest.mark.smoke
    def test_caseid_110588(self): #  TrsmParkLockd|GearLvrIndcn|wti current mode|GearEvent
        self.sd_tester.change_usage_mode(1)
        for signal1 in [0,1]:                
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', signal1)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
            self.partner.empty_all(1)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 2)
            self.ck_Gear_and_GetGear(2)

    @allure.title("获取&通知档位状态_lastvalue")
    @pytest.mark.sanity
    def test_caseid_110567(self): 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 2)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 1)
        self.partner.empty_all(1)
        for usgMod in [0,1,2]:
            self.sd_tester.change_usage_mode(usgMod)
            for signal1 in [0,1]:                
                self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', signal1)
                self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 3)
                self.ck_no_event_and_GetGear(2)
                self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 1)
                self.ck_no_event_and_GetGear(2)

    @allure.title("获取&通知档位状态_NA")
    @pytest.mark.full
    def test_caseid_110494(self): 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 7)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 1)
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ck_Gear_and_GetGear(5)     
        
    @allure.title("获取&通知档位状态_信号全部丢失")
    @pytest.mark.full
    def test_caseid_1980529(self): # GearLvrFaultIndcn_TimeOut|TrsmParkLockdTrsmParkLockd_TimeOut|UpdateGearEventDeduplication:gear
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetGear", {}, {"out": 0})
        self.partner.empty_all(2)
        self.ipdu.pause_bus_send("propulsioncan")
        self.ck_Gear_and_GetGear(5, timeout=1.5)   
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_Gear_and_GetGear(0) 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 2)
        self.ck_Gear_and_GetGear(2) 
        
    @allure.title("获取&通知档位状态_GearLvrIndcn信号丢失")
    @pytest.mark.full
    def test_caseid_1980533(self): # GearLvrFaultIndcn_TimeOut|TrsmParkLockdTrsmParkLockd_TimeOut|UpdateGearEventDeduplication:gear
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetGear", {}, {"out": 0}, timeout=3)
        self.partner.empty_all(2)
        self.ipdu.stop_send_pdu('propulsioncan', 0x04B) # 停发GearLvrIndcn
        self.ck_Gear_and_GetGear(5, timeout=1.5)   
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_Gear_and_GetGear(0) 
        
    @allure.title("获取&通知档位状态_TrsmParkLockdTrsmParkLockd信号丢失")
    @pytest.mark.full
    def test_caseid_1980534(self): # GearLvrFaultIndcn_TimeOut|TrsmParkLockdTrsmParkLockd_TimeOut|UpdateGearEventDeduplication:gear
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetGear", {}, {"out": 0}, timeout=3)
        self.partner.empty_all(2)
        self.ipdu.stop_send_pdu('propulsioncan', 0x155) # TrsmParkLockdTrsmParkLockd
        self.ck_Gear_and_GetGear(5, timeout=1.5)   
        self.ipdu.resume_bus_send("propulsioncan")
        self.ck_Gear_and_GetGear(0) 
        
    @allure.title("获取&通知档位状态_信号全部丢失后通过发送信号恢复")
    @pytest.mark.full
    def test_caseid_1980535(self): # GearLvrFaultIndcn_TimeOut|TrsmParkLockdTrsmParkLockd_TimeOut|UpdateGearEventDeduplication:gear
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetGear", {}, {"out": 0}, timeout=3)
        self.partner.empty_all(2)
        self.ipdu.pause_bus_send("propulsioncan")
        self.ck_Gear_and_GetGear(5, timeout=1.5)   
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 2)
        self.ck_Gear_and_GetGear(2) 
        
    @allure.title("获取&通知档位状态_TrsmParkLockdTrsmParkLockd信号E2E校验失败_发送信号后再恢复")
    @pytest.mark.full
    def test_caseid_1980531(self): # TrsmParkLockd_E2E|UpdateGearEvent
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetGear", {}, {"out": 0}, timeout=3)
        self.partner.empty_all(2)
        try:
            self.ipdu.set_no_crc(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd')
            self.ck_Gear_and_GetGear(5) 
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 2)
            sleep(2)
            self.ck_no_event_and_GetGear(5) 
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd')
            assert False, error
        else:
            self.ipdu.restore_crc(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd')        
        self.ck_Gear_and_GetGear(2) 
        
    @allure.title("获取&通知档位状态_TrsmParkLockdTrsmParkLockd信号E2E校验失败后恢复")
    @pytest.mark.full
    def test_caseid_1980530(self): 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetGear", {}, {"out": 0}, timeout=3)
        self.partner.empty_all()
        try:
            self.ipdu.set_no_crc(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd')
            self.ck_Gear_and_GetGear(5) 
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd')
            assert False, error
        else:
            self.ipdu.restore_crc(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd')        
        self.ck_Gear_and_GetGear(0) 

    @allure.title("获取&通知档位状态_UsgMod遍历_信号值遍历")
    @pytest.mark.full
    def test_caseid_1980536(self): # can GearLvrIndcn|can TrsmParkLockdTrsmParkLockd|UpdateGearEvent|lastUM
        self.partner.empty_all(2)
        last_value=self.partner.send_request_and_return_resp("ChassisService_client", "GetGear", {})["out"] 
        for usgmod in [0, 1, 2, 11, 13]:
            self.sd_tester.change_usage_mode(usgmod)
            for gear in range(8):
                self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', gear)
                sleep(0.5)
                for trsmParkLock in range(4):
                    # self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', gear)
                    self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', trsmParkLock)
                    logger.info(f"打印当前返回值1： usgmod={usgmod}, gear={gear}, trsmParkLock={trsmParkLock},last_value={last_value}")
                    sleep(2)
                    if ((trsmParkLock == 0 or trsmParkLock == 1) and gear == 0) or (gear == 7 and trsmParkLock == 1):
                        value=0
                    elif (trsmParkLock == 0 or trsmParkLock == 1)  and gear == 2:
                        value=2
                    elif gear in [1, 3] and usgmod in [11, 13] and (trsmParkLock == 0 or trsmParkLock == 1):
                        value=gear
                    elif gear in [1, 3] and usgmod in [0, 1 ,2] and (trsmParkLock == 0 or trsmParkLock == 1):
                        self.ck_no_event_and_GetGear(value)                            
                    else:
                        value=5
                    logger.info(f"打印当前返回值2： usgmod={usgmod}, gear={gear}, trsmParkLock={trsmParkLock},last_value={last_value}, value={value}")
                    if last_value!=value:
                        self.ck_Gear_and_GetGear(value) 
                    else:
                        self.ck_no_event_and_GetGear(value)
                    last_value=value
                       
    @allure.title("获取&通知超级节能模式状态反馈关闭_信号遍历")
    @pytest.mark.sanity
    def test_caseid_1980397(self): # can DrvModSetFbk|SuperEnergySaveMode|GetSuperEnergySaveMode
        self.ipdu.set(self.ipdu.adcanfd.AcuADCANFDFr06, 'DrvModSetFbk', 0) # len=4
        for i in range(16):
            self.partner.empty_all(2)
            self.ipdu.set(self.ipdu.adcanfd.AcuADCANFDFr06, 'DrvModSetFbk', i) # len=4
            value = 1 if i==9 else 0
            if i in [9, 10]:
                self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "SuperEnergySaveMode", {"mode": value})
            else:
                self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "SuperEnergySaveMode")
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetSuperEnergySaveMode", {}, {"out": value})

    @allure.title("获取&通知HDC功能运行状态_取值遍历")
    @pytest.mark.sanity
    def test_caseid_110766(self): # MsgReqByHillDwnCtrl|hdcWorkSts
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'MsgReqByHillDwnCtrl', 1)
        for i in range(8):
            self.partner.empty_all(1)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'MsgReqByHillDwnCtrl', i)
            value= 4 if i > 4 else i
            if i > 4 :
                self.partner.ck_no_event("ChassisService_client", "hdcWorkSts")
            else:
                self.partner.ck_s2s_event("ChassisService_client", "hdcWorkSts", {"sts": value})
            self.partner.send_request_and_ck_resp("ChassisService_client", "getHdcWorkSts", {}, {"out": value})
            
    @allure.title("获取HDC功能运行状态/获取驻车系统故障状态_服务启动默认值")
    @pytest.mark.full
    @pytest.mark.restart 
    def test_caseid_110756_1980480_1979633_1980489_1980490_1980512_109490_1980527_1980408_1979795_1980558(self):  
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'MsgReqByHillDwnCtrl', 1) # 获取HDC功能运行状态
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkRelsWarnReq', 1) # 获取驻车系统故障状态
        self.sd_tester.change_usage_mode(13) # 获取车辆Ready指示状态
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3) # 获取显示车速状态 车速值有效
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 1.0) # 获取显示车速状态 车速值
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'ActModOfDampr', 6) # 悬架减震阻尼等级状态=6
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr12, 'TqModAct', 0) # 扭矩模式状态
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr09, 'CrpModAct', 1) # 获取蠕行模式状态
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 1) # 获取EPB功能运行状态
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 3) # 获取档位状态
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0) # 获取档位状态
        self.set_DisplayReqSts([3, 1, 3, 3]) # 获取EPB显示请求状态
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 2) # 获取车辆运动状态   
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 1) # 获取转向系统故障状态
        sleep(3)
        self.restart_bgm_and_connect_service("ChassisService_client", resume_all_bus=False)
        self.partner.send_request_and_ck_resp("ChassisService_client", "getBrkRelsWarnReqSts",{}, {"out": False}) # 获取驻车系统故障状态   
        self.partner.send_request_and_ck_resp("ChassisService_client", "getHdcWorkSts", {}, {"out": 0}) # 获取HDC功能运行状态
        self.partner.send_request_and_ck_resp("ChassisService_client", "getVehReadySts", {}, {"out": False}) # 获取车辆Ready指示状态   
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetDisplaySpeed", {}, {"out": {"speed":0,"speedUnit":2,"isvalid":False}})  # 获取显示车速状态 
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetTorqueMode", {}, {"out": 0}) # 获取扭矩模式状态
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetSuspensionLevel", {}, {"out": 0}) # 获取悬架减震阻尼等级状态 
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetCreepMode", {}, {"out": True}) # 获取蠕行模式状态      
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetEPBOperationStatus", {},{"out": 0}) # 获取EPB功能运行状态
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetGear", {}, {"out": 5}) # 获取档位状态
        self.partner.send_request_and_ck_resp("ChassisService_client", "getDisplayReqSts", {}, {"out": {"highPriSts": 0, "lowPriSts": 0}}) # 获取EPB显示请求状态
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetVehicleMotionState", {}, {"out": {"motionState": 0, "isvalid": False}}) # 获取车辆运动状态
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetSteerErrorReqStatus", {}, {"out": 0}) # 获取转向系统故障状态
         
    @allure.title("获取&通知扭矩模式状态_取值遍历")
    @pytest.mark.sanity
    def test_caseid_110279(self): # TqModAct|TorqueMode
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr12, 'TqModAct', 15)
        self.partner.empty_all(2)  
        for i in range(16):
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr12, 'TqModAct', i)
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "TorqueMode", {"mode": i})
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetTorqueMode", {}, {"out": i})
            
    @allure.title("获取&通知扭矩模式状态_信号丢失")
    @pytest.mark.full
    def test_caseid_1982237(self):
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr12, 'TqModAct', 15)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetTorqueMode", {}, {"out": 15}, timeout=3)
        self.partner.empty_all()  
        self.ipdu.pause_bus_send("chassiscan1")
        self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "TorqueMode", timeout=3)
        self.ipdu.resume_bus_send("chassiscan1")
        self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "TorqueMode", timeout=3)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetTorqueMode", {}, {"out": 15})

    @allure.title("设置扭矩模式_取值遍历&下行PDU校验")
    @pytest.mark.smoke
    def test_caseid_110172(self): 
        file_path, save_name = self.bgmcli.start_bgm_tcpdump() 
        for i in range(16):
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetTorqueMode", {"mode": i})
            self.ipdu.check(self.ipdu.chassiscan1.BgmChas1Fr02, 'TqModReq', i)
            sleep(2)
        # 检验TCP报文 # 列表里面为元祖（pdu的id，数据长度，信号起始bit位，信号长度，信号值），可以 是多个元祖
        data_list1 = [(10011, 1, 3, 4, 0),(10011, 1, 3, 4, 15)]
        data_list2 = [(10011, 1, 3, 4)]
        self.ck_pdu(file_path,save_name,data_list1,data_list2)
                
    @allure.title("获取&通知转向系统故障状态_取值遍历")
    @pytest.mark.sanity
    def test_caseid_110719(self):
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 7)
        for i in range(8):
            self.partner.empty_all(2)
            self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', i)
            self.partner.ck_s2s_event("ChassisService_client", "SteerErrorReqStatus", {"state": i})
            self.partner.send_request_and_ck_resp("ChassisService_client", "GetSteerErrorReqStatus", {}, {"out": i})
            
    @allure.title("获取&通知转向系统故障状态_UsgMod=0/1/2_信号丢失")
    @pytest.mark.full
    def test_caseid_1980556(self): 
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 1)
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetSteerErrorReqStatus", {}, {"out": 1}, timeout=3)
        self.partner.empty_all()
        for usgmod in [0, 1, 2]:
            self.sd_tester.change_usage_mode(usgmod) 
            sleep(2)  
            self.ipdu.pause_bus_send("chassiscan1")
            self.partner.ck_no_event("ChassisService_client", "SteerErrorReqStatus", timeout=5.5)
            self.partner.send_request_and_ck_resp("ChassisService_client", "GetSteerErrorReqStatus", {}, {"out": 1})
            self.ipdu.resume_bus_send("chassiscan1")
        
    @allure.title("获取&通知转向系统故障状态_UsgMod=11/13_信号丢失")
    @pytest.mark.full
    def test_caseid_1980557(self): # SteerErrReq_TimeOut|SteerErrorReqStatus
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 7)
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetSteerErrorReqStatus", {}, {"out": 7}, timeout=3)
        self.partner.empty_all()
        for usgmod in [11, 13]:
            self.sd_tester.change_usage_mode(usgmod) 
            sleep(2)  
            self.ipdu.pause_bus_send("chassiscan1")
            self.partner.ck_s2s_event("ChassisService_client", "SteerErrorReqStatus", {"state": 4}, timeout=5.5)
            self.partner.send_request_and_ck_resp("ChassisService_client", "GetSteerErrorReqStatus", {}, {"out": 4})
            self.ipdu.resume_bus_send("chassiscan1")        
            self.partner.ck_s2s_event("ChassisService_client", "SteerErrorReqStatus", {"state": 7})
            self.partner.send_request_and_ck_resp("ChassisService_client", "GetSteerErrorReqStatus", {}, {"out": 7})

    @allure.title("获取&通知车辆Ready指示状态_信号取值遍历")
    @pytest.mark.sanity
    def test_caseid_1980477(self): # fr VehModMngtGlbSafe1UsgModSts|vehicleReadyEvent
        for usgmod in [0, 1, 2, 13, 11]:      
            self.sd_tester.change_usage_mode(usgmod)      
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', usgmod)
            value=True if usgmod==13 else False 
            if usgmod in [13, 11]:
                self.partner.ck_s2s_event("ChassisService_client", "vehicleReady", {"sts": value})
            else:
                self.partner.ck_no_event("ChassisService_client", "vehicleReady")
            self.partner.send_request_and_ck_resp("ChassisService_client", "getVehReadySts", {}, {"out": value})

    @allure.title("设置悬架减震阻尼等级_初始化")
    @pytest.mark.full
    def test_caseid_1985515(self):         
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetSuspensionLevel", {"level": 1})
        self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'ModReqOfDampr', 1, timeout=0.5)
        self.restart_bgm_and_connect_service(CHASSIS_SERVICE_CLIENT)
        sleep(1)
        self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'ModReqOfDampr', 0, timeout=0.5)
        
    @allure.title("设置悬架减震阻尼等级_参数遍历&下行PDU校验")
    @pytest.mark.sanity
    def test_caseid_1985513(self): 
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetSuspensionLevel", {"level": 0})
        sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        for level in range(8):            
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetSuspensionLevel", {"level": level})
            self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'ModReqOfDampr', level, timeout=2)
            sleep(0.5)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array("ModReqOfDampr", [0,1,2,3,4,5,6,7])
        self.bgm_eth_inter.ck_period_time("HVActvForProxy", 0.5)
        self.bgm_eth_inter.start_bgm_tcpdump()
        for level in [8,255]:            
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetSuspensionLevel", {"level": level})
            self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'ModReqOfDampr', 7, timeout=0.5)
            sleep(0.5)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array("ModReqOfDampr", [7,7])
              
    @allure.title("获取&通知悬架减震阻尼等级状态_信号取值遍历")
    @pytest.mark.sanity
    def test_caseid_1980488(self):
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'ActModOfDampr', 6)
        self.partner.empty_all(2)
        for level in range(8):       
            self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'ActModOfDampr', level) # len=3
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "SuspensionLevel", {"level": level})
            self.partner.send_request_and_ck_resp("ChassisService_client", "GetSuspensionLevel", {}, {"out": level})        
        
    @allure.title("获取&通知运动模式有效状态_取值遍历")
    @pytest.mark.sanity
    def test_caseid_110370(self):  
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr18, 'PrpsnModSptBlkd', 6)
        for i in range(7):
            self.partner.empty_all(1)
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr18, 'PrpsnModSptBlkd', i)
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "SportModeAvailableStatus", {"state": i})
            self.partner.send_request_and_ck_resp("ChassisService_client", "GetSportModeAvailableStatus", {}, {"out": i})
            
    @allure.title("获取&通知运动模式有效状态_信号丢失")
    @pytest.mark.full
    def test_caseid_1979655(self):  # PrpsnModSptBlkd|SportModeAvailableStatus|PrpsnModSptBlkd_TimeOut
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr18, 'PrpsnModSptBlkd', 1)
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetSportModeAvailableStatus", {}, {"out": 1}, timeout=3)
        self.partner.empty_all(1)
        self.ipdu.pause_bus_send("chassiscan2")
        sleep(2.5)
        self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "SportModeAvailableStatus") # 保持Last Value
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetSportModeAvailableStatus", {}, {"out": 1})  
        self.ipdu.resume_bus_send("chassiscan2")      
        self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "SportModeAvailableStatus") 
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetSportModeAvailableStatus", {}, {"out": 1})    
 
    @allure.title("获取&通知ABS报警指示请求状态_信号取值遍历")
    @pytest.mark.sanity
    def test_caseid_1980422(self): # fr BrkAndAbsWarnIndcnReqAbsWarnIndcnReq|absWarnIndicateReqSts|getABSWarnIndicateReqSts
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqAbsWarnIndcnReq', 3) # len=2
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getABSWarnIndicateReqSts", {}, {"out": 0}, timeout=3)   
        self.partner.empty_all()
        dict1={0:1, 1:2, 2:3, 3:0}
        for key,value in dict1.items():
            logger.info(f"打印当前返回值： key={key},value={value}")
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqAbsWarnIndcnReq', key)
            self.ck_absWarnIndicateReqSts_and_getABSWarnIndicateReqSts(value)

    @allure.title("获取&通知ABS报警指示请求状态_信号丢失")
    @pytest.mark.full
    def test_caseid_1980423(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqAbsWarnIndcnReq', 1) # len=2
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getABSWarnIndicateReqSts", {}, {"out": 2}, timeout=3)
        self.partner.empty_all()
        self.ipdu.pause_bus_send("backbonefr") 
        self.ck_absWarnIndicateReqSts_and_getABSWarnIndicateReqSts(1, timeout=2.3)      
        self.ipdu.resume_bus_send("backbonefr")
        self.ck_absWarnIndicateReqSts_and_getABSWarnIndicateReqSts(2, timeout=2.3)  

    @allure.title("获取&通知ABS报警指示请求状态_E2E校验失败")
    @pytest.mark.full
    def test_caseid_1980425(self): # fr BrkAndAbsWarnIndcnReqAbsWarnIndcnReq|absWarnIndicateReqSts
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqAbsWarnIndcnReq', 1) # len=2
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getABSWarnIndicateReqSts", {}, {"out": 2}, timeout=3)
        self.partner.empty_all()
        try:
            self.ipdu.set_no_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqAbsWarnIndcnReq')
            self.ck_absWarnIndicateReqSts_and_getABSWarnIndicateReqSts(1)    
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqAbsWarnIndcnReq', 2) 
            self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "absWarnIndicateReqSts")
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqAbsWarnIndcnReq')
            assert False, error
        else:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqAbsWarnIndcnReq')
        self.ck_absWarnIndicateReqSts_and_getABSWarnIndicateReqSts(3)  
                        
    @allure.title("获取&通知ABS报警指示请求状态_UsgMod从0/1/2切至11/13_2s计时器内维持")
    @pytest.mark.sanity
    def test_caseid_1980426(self): # 重复上报 SOA-18864 fr BrkAndAbsWarnIndcnReqAbsWarnIndcnReq|absWarnIndicateReqSts|getABSWarnIndicateReqSts|lastUM
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqAbsWarnIndcnReq', 1) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getABSWarnIndicateReqSts", {}, {"out": 2}, timeout=5)   
        for usgmod1 in [0, 1, 2]:
            for usgmod2 in [11, 13]:
                logger.info(f"打印当前循环值： usgmod1={usgmod1},usgmod2={usgmod2}")
                self.sd_tester.change_usage_mode(usgmod1)
                self.partner.empty_all(2)
                # self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "absWarnIndicateReqSts", timeout=3)
                self.sd_tester.change_usage_mode(usgmod2) 
                self.ck_absWarnIndicateReqSts_and_getABSWarnIndicateReqSts(0, timeout=2)    
                self.ck_absWarnIndicateReqSts_and_getABSWarnIndicateReqSts(2)        

    @allure.title("获取&通知ABS报警指示请求状态_UsgMod从0/1/2切至11/13_2s内下切")
    @pytest.mark.full
    def test_caseid_1980427(self): # # 计时器未取消，2s后会再次报3 SOA-18864
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqAbsWarnIndcnReq', 2) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getABSWarnIndicateReqSts", {}, {"out": 3}, timeout=3)   
        for usgmod1 in [0, 1, 2]:
            for usgmod2 in [11, 13]:
                logger.info(f"打印当前循环值： usgmod1={usgmod1},usgmod2={usgmod2}")
                self.sd_tester.change_usage_mode(usgmod1)
                self.partner.empty_all(2)
                # self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "absWarnIndicateReqSts", timeout=3)
                self.sd_tester.change_usage_mode(usgmod2) 
                self.sd_tester.change_usage_mode(usgmod1)
                # self.ck_absWarnIndicateReqSts_and_getABSWarnIndicateReqSts(0, timeout=2)    
                self.ck_absWarnIndicateReqSts_and_getABSWarnIndicateReqSts(3, timeout=2)   

    @allure.title("获取&通知ESC报警指示请求状态_信号取值遍历")
    @pytest.mark.sanity
    def test_caseid_1980441(self): 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq', 3)
        self.partner.empty_all(2)
        for i in range(4):
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq', i)
            self.ck_escWarnIndicateReqSts_and_getESCWarnIndicateReqSts(i)

    @allure.title("获取&通知ESC报警指示请求状态_信号丢失")
    @pytest.mark.full
    def test_caseid_1980442(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq', 1) # len=2
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getESCWarnIndicateReqSts", {}, {"out": 1}, timeout=3)
        self.ipdu.pause_bus_send("backbonefr") 
        self.ck_escWarnIndicateReqSts_and_getESCWarnIndicateReqSts(0, timeout=2.3)      
        self.ipdu.resume_bus_send("backbonefr")
        self.ck_escWarnIndicateReqSts_and_getESCWarnIndicateReqSts(1)  

    @allure.title("获取&通知ESC报警指示请求状态_E2E校验失败")
    @pytest.mark.full
    def test_caseid_1980443(self): 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq', 2)
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "escWarnIndicateReqSts",{"sts": 2})
        try:
            self.ipdu.set_no_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq')
            self.ck_escWarnIndicateReqSts_and_getESCWarnIndicateReqSts(0)    
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq', 3)
            self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "escWarnIndicateReqSts")
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq')
            assert False, error
        else:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq')
        self.ck_escWarnIndicateReqSts_and_getESCWarnIndicateReqSts(3)    

    @allure.title("获取&通知ESC报警指示请求状态_UsgMod从0/1/2切至11/13_2s计时器内维持")
    @pytest.mark.full
    def test_caseid_1980444(self): # fr EscWarnIndcnReqEscWarnIndcnReq|escWarnIndicateReqSts|getESCWarnIndicateReqSts|lastUM
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq', 2)
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "escWarnIndicateReqSts",{"sts": 2})
        for usgmod1 in [0, 1, 2]:
            for usgmod2 in [11, 13]:
                logger.info(f"打印当前循环值： usgmod1={usgmod1},usgmod2={usgmod2}")
                self.sd_tester.change_usage_mode(usgmod1)
                self.partner.empty_all(2)
                # self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "escWarnIndicateReqSts", timeout=3)
                self.sd_tester.change_usage_mode(usgmod2) 
                self.ck_escWarnIndicateReqSts_and_getESCWarnIndicateReqSts(3, timeout=2)    
                self.ck_escWarnIndicateReqSts_and_getESCWarnIndicateReqSts(2) 

    @allure.title("获取&通知ESC报警指示请求状态_UsgMod从0/1/2切至11/13_2s内下切")
    @pytest.mark.full
    def test_caseid_1980445(self): # 计时器未取消，2s后会再次报3  fr EscWarnIndcnReqEscWarnIndcnReq|escWarnIndicateReqSts|getESCWarnIndicateReqSts|lastUM
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq', 1) 
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "escWarnIndicateReqSts",{"sts": 1})
        self.partner.empty_all(2)
        for usgmod1 in [0, 1, 2]:
            for usgmod2 in [11, 13]:
                logger.info(f"打印当前循环值： usgmod1={usgmod1},usgmod2={usgmod2}")
                self.sd_tester.change_usage_mode(usgmod1)
                self.partner.empty_all(3)
                self.sd_tester.change_usage_mode(usgmod2)    
                self.sd_tester.change_usage_mode(usgmod1)  
                self.ck_escWarnIndicateReqSts_and_getESCWarnIndicateReqSts(1)             

    @allure.title("获取&通知车辆加速度信息_范围内取值")
    @pytest.mark.sanity
    def test_caseid_1980595(self): # can ADataRawSafeA|VehicleAcceleration
        for long in [16353, 0, -16352]:
            for lateral in [16353, 0, -16352]:
                for vertical in [16353, 0, -16352]:
                    self.ipdu.set(self.ipdu.passivesafetycan.SrsPassSafeCANFr04, 'ADataRawSafeALgt', long)
                    self.ipdu.set(self.ipdu.passivesafetycan.SrsPassSafeCANFr04, 'ADataRawSafeALat', lateral)
                    self.ipdu.set(self.ipdu.passivesafetycan.SrsPassSafeCANFr04, 'ADataRawSafeAVert', vertical)
                    value={"longAcceleration": long*0.0085, "lateralAcceleration": lateral*0.0085, "verticalAcceleration": vertical*0.0085}
                    self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, 'VehicleAcceleration', {"info": value})
                    self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, 'GetVehicleAcceleration', {}, {"out": value})
                       
    @allure.title("通知车辆加速度信息_delay50ms")
    @pytest.mark.full
    def test_caseid_1980686(self):    
        self.ipdu.set(self.ipdu.passivesafetycan.SrsPassSafeCANFr04, 'ADataRawSafeALgt', 500) 
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, 'VehicleAcceleration', {"info": {"longAcceleration": 500*0.0085}})
        self.partner.empty_all()
        for long in range(1, 7):
            self.ipdu.set(self.ipdu.passivesafetycan.SrsPassSafeCANFr04, 'ADataRawSafeALgt', long*1000) 
            sleep(0.02)
        event_times=0
        for event in list(self.partner.partner_infos[CHASSIS_SERVICE_CLIENT].event_queue.queue):
            if event['function'] == "UpdateVehicleAccelerationEvent":
                event_times+=1
        assert  event_times<4                     
                    
    @allure.title("获取&通知车辆加速度信息_超范围值")
    @pytest.mark.full
    def test_caseid_1980596(self): # can ADataRawSafeA|VehicleAcceleration
        value=self.partner.send_request_and_return_resp(CHASSIS_SERVICE_CLIENT, 'GetVehicleAcceleration', {})["out"]
        self.partner.empty_all()
        for long in [16360, -16353]:
            for lateral in [16360, -16353]:
                for vertical in [16360, -16353]:
                    self.ipdu.set(self.ipdu.passivesafetycan.SrsPassSafeCANFr04, 'ADataRawSafeALgt', long)
                    self.ipdu.set(self.ipdu.passivesafetycan.SrsPassSafeCANFr04, 'ADataRawSafeALat', lateral)
                    self.ipdu.set(self.ipdu.passivesafetycan.SrsPassSafeCANFr04, 'ADataRawSafeAVert', vertical)
                    self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, 'VehicleAcceleration')
                    self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, 'GetVehicleAcceleration', {}, {"out": value})            

    @allure.title("EPB指示灯请求状态_带功能安全需求参数_信号遍历")
    @pytest.mark.smoke
    def test_caseid_1886137(self): # EpbLampReqEpbLampReq|EpbLampReqSecEpbLampReq|epbIndicatorLightReqStsValidity        
        for epb_lamp in [1,0,2,3]:
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq',epb_lamp)
            sleep(0.5)
            for sec_epb_lamp in [0,1,2,3]:    
                last_value=self.partner.send_request_and_return_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{})["out"]["value"]            
                sleep(0.5)
                self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq',sec_epb_lamp)  
                if epb_lamp==0 and sec_epb_lamp==0:                        
                    value=1
                elif epb_lamp==1 and sec_epb_lamp==1: 
                    value=0
                else:
                    value=2  
                logger.info(f"打印当前返回值EpbLampReq={epb_lamp};EpbLampReqSec={sec_epb_lamp};last_value={last_value};value={value}")
                if last_value==value:
                    self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT,'epbIndicatorLightReqStsValidity')
                else:
                    self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,'epbIndicatorLightReqStsValidity',{'sts':{"value":value,"validity":0}})
                self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{},{"out":{"value":value,"validity":0}}) 
                
    @allure.title("EPB指示灯请求状态_带功能安全需求参数_服务启动默认值")
    @pytest.mark.full
    @pytest.mark.restart 
    def test_caseid_1980462(self):     
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq',0)
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq',0) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{},{"out":{"value":1,"validity":0}}, timeout=3)  
        self.restart_bgm_and_connect_service(CHASSIS_SERVICE_CLIENT, resume_all_bus=False)
        sleep(2)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{},{"out":{"value":0,"validity":0}}) 

    @allure.title("EPB指示灯请求状态_带功能安全需求参数_信号丢失")
    @pytest.mark.full
    def test_caseid_1886138(self): # mEpbLampReqTimeOutFlag|mEpbLampReqSecTimeOutFlag|fr EpbLampReqEpbLampReq|fr EpbLampReqSecEpbLampReq|epbIndicatorLightReqStsValidity
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq',1)
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq',1) 
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq',0)
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq',0) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{},{"out":{"value":1,"validity":0}}, timeout=5)  
        self.partner.empty_all(2)    
        self.ipdu.pause_bus_send("backbonefr")   
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,'epbIndicatorLightReqStsValidity',{'sts':{"value":1,"validity":4}}, timeout=2.5)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{},{"out":{"value":1,"validity":4}}) 
        self.ipdu.resume_bus_send("backbonefr") 
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,'epbIndicatorLightReqStsValidity',{'sts':{"value":1,"validity":0}})
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{},{"out":{"value":1,"validity":0}})

    @allure.title("EPB指示灯请求状态_带功能安全需求参数_EpbLampReq信号丢失")
    @pytest.mark.full
    def test_caseid_1981323(self):  
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq',1)
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq',1) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{},{"out":{"value":0,"validity":0}}, timeout=3)  
        self.partner.empty_all()  
        self.ipdu.stop_send_pdu('backbonefr', 3741504)
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,'epbIndicatorLightReqStsValidity',{'sts':{"value":0,"validity":4}}, timeout=2.5)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{},{"out":{"value":0,"validity":4}}) 
        self.ipdu.resume_bus_send("backbonefr") 
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,'epbIndicatorLightReqStsValidity',{'sts':{"value":0,"validity":0}})
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{},{"out":{"value":0,"validity":0}}) 
            
    @allure.title("EPB指示灯请求状态_带功能安全需求参数_EpbLampReqSec信号丢失")
    @pytest.mark.full
    def test_caseid_1981324(self):  
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq',0)
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq',1) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{},{"out":{"value":2,"validity":0}}, timeout=3)  
        self.partner.empty_all()    
        self.ipdu.stop_send_pdu('backbonefr', 460864)    
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,'epbIndicatorLightReqStsValidity',{'sts':{"value":2,"validity":4}}, timeout=2.5)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{},{"out":{"value":2,"validity":4}}) 
        self.ipdu.resume_bus_send("backbonefr") 
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,'epbIndicatorLightReqStsValidity',{'sts':{"value":2,"validity":0}})
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{},{"out":{"value":2,"validity":0}}) 

    @allure.title("EPB指示灯请求状态_带功能安全需求参数_EpbLampReqSec信号E2E校验失败")
    @pytest.mark.full
    def test_caseid_1886139(self): # mEpbLampReqSecE2EFlag
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq',1)
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq',1) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{},{"out":{"value":0,"validity":0}}, timeout=3) 
        self.partner.empty_all()
        try:
            self.ipdu.set_no_crc(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq')
            sleep(1)
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,'epbIndicatorLightReqStsValidity',{'sts':{"value":0,"validity":7}})
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{},{"out":{"value":0,"validity":7}})             
            self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq',0) 
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,'epbIndicatorLightReqStsValidity',{'sts':{"value":2,"validity":7}})
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{},{"out":{"value":2,"validity":7}}) 
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq')
            assert False, error
        else:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq')
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,'epbIndicatorLightReqStsValidity',{'sts':{"value":2,"validity":0}})
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{},{"out":{"value":2,"validity":0}})   
        
    @allure.title("EPB指示灯请求状态_带功能安全需求参数_EpbLampReq信号E2E校验失败")
    @pytest.mark.full
    def test_caseid_1980461(self): # mEpbLampReqE2EError|mEpbLampReqSecE2EError|epbIndicatorLightReqStsValidity|fr EpbLampReq
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq',2)
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq',0) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{},{"out":{"value":2,"validity":0}}, timeout=3) 
        self.partner.empty_all()
        try:
            self.ipdu.set_no_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq')
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,'epbIndicatorLightReqStsValidity',{'sts':{"value":2,"validity":7}})
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{},{"out":{"value":2,"validity":7}}) 
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq',0)
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,'epbIndicatorLightReqStsValidity',{'sts':{"value":1,"validity":7}})
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{},{"out":{"value":1,"validity":7}}) 
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq')
            assert False, error
        else:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq')
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,'epbIndicatorLightReqStsValidity',{'sts':{"value":1,"validity":0}})
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{},{"out":{"value":1,"validity":0}})   

    @allure.title("EPB显示请求状态_EpbDrvrDisp与EpbDrvrDispSec信号遍历")
    @pytest.mark.full
    def test_caseid_1892809(self):  
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 1)
        self.ipdu.set(self.ipdu.backbonefr.BbmVcuBackBoneFr02, 'EpbDrvrDispSec', 4)
        self.partner.send_request_and_ck_resp("ChassisService_client", "getDisplayReqSts", {}, {"out": {"highPriSts": 2, "lowPriSts": 3}}, timeout=3)
        before_highPriSts, before_lowPriSts=2, 3
        self.partner.empty_all()  
        signal=[3,1,4,15,6,8,14,7,2,13,5,11,9,0,10,12] # 优先级顺序
        value=[1,2,3,4,5,6,7,8,9,10,11,12,13,0,0,0]
        # signal_1 遍历信号EpbDrvrDisp  
        for signal_1 in signal:
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', signal_1)
            # sigbal_2 遍历信号EpbDrvrDispSec
            for signal_2 in signal:
                self.ipdu.set(self.ipdu.backbonefr.BbmVcuBackBoneFr02, 'EpbDrvrDispSec', signal_2)
                sleep(0.5)
                # 信号EpbDrvrDisp与EpbDrvrDispSec状态 相同
                logger.info(f"打印循环值：signal_1={signal_1},signal_2={signal_2}")
                if signal_1==signal_2:
                    highPriSts=value[signal.index(signal_1)] # signal_1在signal的位置 是value中对应的下标索引
                    lowPriSts=0
                    if highPriSts==13:
                        lowPriSts=13
                # 信号EpbDrvrDisp与EpbDrvrDispSec状态 不同
                else:
                    index_1=signal.index(signal_1) # 找到signal_1在signal列表中对应的索引
                    index_2=signal.index(signal_2) # 找到signal_2在signal列表中对应的索引
                    highPriSts=value[min(index_1,index_2)]
                    lowPriSts=value[max(index_1,index_2)]
                logger.info(f"打印上次优先级结果：before_highPriSts={before_highPriSts},before_lowPriSts={before_lowPriSts}")  
                logger.info(f"打印当前优先级结果：highPriSts={highPriSts},lowPriSts={lowPriSts}")    
                # 校验event事件是否上报 & 校验get返回值
                if highPriSts != before_highPriSts or lowPriSts != before_lowPriSts:
                    self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "epbDisplayReqSts", {"sts": {"highPriSts": highPriSts, "lowPriSts": lowPriSts}})
                else:
                    self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "epbDisplayReqSts")
                self.partner.send_request_and_ck_resp("ChassisService_client", "getDisplayReqSts", {}, {"out": {"highPriSts": highPriSts, "lowPriSts": lowPriSts}})
                before_highPriSts=highPriSts
                before_lowPriSts=lowPriSts
                self.partner.empty_all() 

    @allure.title("EPB显示请求状态_EpbLampReq与EpbLampReqSec信号遍历")
    @pytest.mark.smoke
    def test_caseid_1903206(self):
        self.set_DisplayReqSts()
        self.partner.empty_all()
        for epb_lamp in [0,1,2]:
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq',epb_lamp)
            sleep(0.5)
            for sec_epb_lamp in [0,1,2]:
                before_value=self.partner.send_request_and_return_resp("ChassisService_client", "getDisplayReqSts", {})["out"]["highPriSts"]
                self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq',sec_epb_lamp)  
                value = 5 if (epb_lamp==0 and sec_epb_lamp==1) or (epb_lamp==1 and sec_epb_lamp==0) else 0
                if before_value != value:
                    self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "epbDisplayReqSts", {"sts": {"highPriSts": value, "lowPriSts": value}})
                else:
                    self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "epbDisplayReqSts")
                self.partner.send_request_and_ck_resp("ChassisService_client", "getDisplayReqSts", {}, {"out": {"highPriSts": value, "lowPriSts": value}})
                              
    @allure.title("EPB显示请求状态_UsagMoede在Convenience及以上_信号丢失")
    @pytest.mark.full
    def test_caseid_1892808(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 3)
        self.ipdu.set(self.ipdu.backbonefr.BbmVcuBackBoneFr02, 'EpbDrvrDispSec', 1)
        self.partner.send_request_and_ck_resp("ChassisService_client", "getDisplayReqSts", {}, {"out": {"highPriSts": 1, "lowPriSts": 2}}, timeout=2)       
        for usgmod in [0x2, 0xB, 0xD]:
            self.sd_tester.change_usage_mode(usgmod)
            self.partner.empty_all(2)
            self.ipdu.pause_bus_send("backbonefr") 
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "epbDisplayReqSts", {"sts": {"highPriSts": 5, "lowPriSts": 5}}, timeout=2.5)
            self.partner.send_request_and_ck_resp("ChassisService_client", "getDisplayReqSts", {}, {"out": {"highPriSts": 5, "lowPriSts": 5}})
            self.ipdu.resume_bus_send("backbonefr")  
            self.partner.send_request_and_ck_resp("ChassisService_client", "getDisplayReqSts", {}, {"out": {"highPriSts": 1, "lowPriSts": 2}}, timeout=2)       
            
    @allure.title("EPB显示请求状态_UsagMoede在Abandoned/Inactive_信号丢失")
    @pytest.mark.full
    def test_caseid_1903181(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 15)
        self.ipdu.set(self.ipdu.backbonefr.BbmVcuBackBoneFr02, 'EpbDrvrDispSec', 1)
        self.partner.send_request_and_ck_resp("ChassisService_client", "getDisplayReqSts", {}, {"out": {"highPriSts": 2, "lowPriSts": 4}}, timeout=2)  
        for usgmod in [0, 1]:
            self.sd_tester.change_usage_mode(usgmod)
            self.partner.empty_all(2)
            self.ipdu.pause_bus_send("backbonefr") 
            self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "epbDisplayReqSts", timeout=2.5)
            self.partner.send_request_and_ck_resp("ChassisService_client", "getDisplayReqSts", {}, {"out": {"highPriSts": 2, "lowPriSts": 4}}) #last value
            self.ipdu.resume_bus_send("backbonefr")                  
            
    def set_DisplayReqSts(self, signal=[0, 0, 3, 3], sleep_time=2):
        # 设置EPB显示请求状态，默认设0
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', signal[0])
        self.ipdu.set(self.ipdu.backbonefr.BbmVcuBackBoneFr02, 'EpbDrvrDispSec', signal[1])
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq', signal[2])
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq', signal[3])  
        sleep(sleep_time)
                    
    @allure.title("EPB显示请求状态_UsgMod遍历_EpbLampReq信号E2E校验失败")
    @pytest.mark.full
    def test_caseid_1980017(self):  
        # epbDisplayReqStsEvent|fr EpbLampReq|lastUM|fr EpbDrvrDisp|fr BrkSysWarnIndcnReq| EpbLampReq_E2E result|getDisplayReqSts|mEpbLampReqE2EError|mEpbLampReqSecE2EError
        self.set_DisplayReqSts()
        for UsgMod in [0, 1, 2, 11, 13]:
            self.sd_tester.change_usage_mode(UsgMod)
            self.partner.empty_all(2)
            try:
                self.ipdu.set_no_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq') # add into changDataMap E2E GroupId: EpbLampReq_E2E result
                sleep(2)
                logger.info(f"打印当前循环值:UsgMod={UsgMod}") 
                self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "epbDisplayReqSts", {"sts": {"highPriSts": 5, "lowPriSts": 5}})
                self.partner.send_request_and_ck_resp("ChassisService_client", "getDisplayReqSts", {}, {"out": {"highPriSts": 5, "lowPriSts": 5}}, timeout=3)
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq', 3)
                self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "epbDisplayReqSts", timeout=3)
            except Exception as error:
                self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq') 
                assert False, error
            else:
                self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq')   
            self.partner.send_request_and_ck_resp("ChassisService_client", "getDisplayReqSts", {}, {"out": {"highPriSts": 0, "lowPriSts": 0}}, timeout=3)    
        
    @allure.title("EPB显示请求状态_UsgMod上切遍历_EpbLampReqSec信号E2E校验失败")
    @pytest.mark.sanity
    def test_caseid_1980020(self):   # EPBDisplayReqSts,sts|mEpbLampReqSecE2EError|lastUM|getDisplayReqSts
        # epbDisplayReqStsEvent|r EpbLampReq|lastUM|r EpbDrvrDisp|r BrkSysWarnIndcnReq|mEpbLampReqSecE2EError|getDisplayReqSts|lastUM|EPBDisplayReqSts,sts|VehModMngtGlbSafe1UsgModSts
        self.set_DisplayReqSts()
        for UsgMod in [0, 1, 2, 11, 13]:
            self.sd_tester.change_usage_mode(UsgMod)
            self.partner.empty_all(2)
            try:
                self.ipdu.set_no_crc(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq') # add into changDataMap E2E GroupId: EpbLampReq_E2E result
                logger.info(f"打印当前循环值:UsgMod={UsgMod}")
                sleep(2)
                if UsgMod in [0, 1]:
                    self.partner.send_request_and_ck_resp("ChassisService_client", "getDisplayReqSts", {}, {"out": {"highPriSts": 0, "lowPriSts": 0}}, timeout=3)   
                else: 
                    self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "epbDisplayReqSts", {"sts": {"highPriSts": 5, "lowPriSts": 5}})
                    self.partner.send_request_and_ck_resp("ChassisService_client", "getDisplayReqSts", {}, {"out": {"highPriSts": 5, "lowPriSts": 5}}, timeout=3)
            except Exception as error:
                self.ipdu.restore_crc(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq')
                assert False, error
            else:
                self.ipdu.restore_crc(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq')
            sleep(2)
            self.partner.send_request_and_ck_resp("ChassisService_client", "getDisplayReqSts", {}, {"out": {"highPriSts": 0, "lowPriSts": 0}}, timeout=3)    
            sleep(5)    

    @allure.title("EPB显示请求状态_UsgMod从2/11/13下切至1的10s内_EpbLampReqSec信号E2E校验失败")
    @pytest.mark.full
    def test_caseid_1980021(self):   
        self.set_DisplayReqSts()
        for UsgMod1 in [2, 11, 13]:   
            self.sd_tester.change_usage_mode(UsgMod1)
            self.partner.empty_all(2)
            self.sd_tester.change_usage_mode(1) # 下切到1
            try:
                self.ipdu.set_no_crc(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq') 
                sleep(2) 
                self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "epbDisplayReqSts", {"sts": {"highPriSts": 5, "lowPriSts": 5}})
                self.partner.send_request_and_ck_resp("ChassisService_client", "getDisplayReqSts", {}, {"out": {"highPriSts": 5, "lowPriSts": 5}}, timeout=3)
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 3)
                self.ipdu.set(self.ipdu.backbonefr.BbmVcuBackBoneFr02, 'EpbDrvrDispSec', 1)
                sleep(2)
                self.partner.send_request_and_ck_resp("ChassisService_client", "getDisplayReqSts", {}, {"out": {"highPriSts": 1, "lowPriSts": 2}}, timeout=3)    
            except Exception as error:
                self.ipdu.restore_crc(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq') 
                assert False, error
            else:
                self.ipdu.restore_crc(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq') 
            self.partner.send_request_and_ck_resp("ChassisService_client", "getDisplayReqSts", {}, {"out": {"highPriSts": 1, "lowPriSts": 2}}, timeout=3)    
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 0)
            self.ipdu.set(self.ipdu.backbonefr.BbmVcuBackBoneFr02, 'EpbDrvrDispSec', 0)
            self.sd_tester.change_usage_mode(UsgMod1)
            sleep(2)    
            
    @allure.title("EPB显示请求状态_UsgMod从2/11/13下切至1的10s后_EpbLampReqSec信号E2E校验失败")
    @pytest.mark.full
    def test_caseid_1980023(self):   
        self.set_DisplayReqSts()
        for UsgMod1 in [2, 11, 13]:   
            self.sd_tester.change_usage_mode(UsgMod1)
            self.partner.empty_all(2)
            self.sd_tester.change_usage_mode(1) # 下切到1 等待10s
            sleep(10)
            try:
                self.ipdu.set_no_crc(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq') 
                sleep(2) 
                self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "epbDisplayReqSts")
                self.partner.send_request_and_ck_resp("ChassisService_client", "getDisplayReqSts", {}, {"out": {"highPriSts": 0, "lowPriSts": 0}}, timeout=3)
            except Exception as error:
                self.ipdu.restore_crc(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq') 
                assert False, error
            else:
                self.ipdu.restore_crc(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq') 
            sleep(2)       
            
    @allure.title("EPB显示请求状态_UsgMod从2/11/13下切至0_EpbLampReqSec信号E2E校验失败")
    @pytest.mark.full
    def test_caseid_1980024(self):   # epbDisplayReqStsEvent|fr EpbLampReq|lastUM|fr EpbDrvrDisp|fr BrkSysWarnIndcnReq|add into changDataMap E2E GroupId: EpbLampReq_E2E result|getDisplayReqSts
        self.set_DisplayReqSts()
        for UsgMod1 in [2, 11, 13]:   
            self.sd_tester.change_usage_mode(UsgMod1)   
            self.partner.empty_all(2)
            self.sd_tester.change_usage_mode(0) # 下切到0   
            try:
                self.ipdu.set_no_crc(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq') 
                sleep(2)  
                self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "epbDisplayReqSts")
                self.partner.send_request_and_ck_resp("ChassisService_client", "getDisplayReqSts", {}, {"out": {"highPriSts": 0, "lowPriSts": 0}}, timeout=3)
            except Exception as error:
                self.ipdu.restore_crc(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq') 
                assert False, error
            else:
                self.ipdu.restore_crc(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq')  
            sleep(2)
                   
    @allure.title("EPB显示请求状态_UsgMod从0/1切换至2/11/13_debounce确认")
    @pytest.mark.full
    def test_caseid_1980025(self):   
        self.set_DisplayReqSts()
        for UsgMod1 in [0, 1]: 
            for UsgMod2 in [2, 11, 13]:  
                self.sd_tester.change_usage_mode(UsgMod1)  
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 0) 
                self.partner.send_request_and_ck_resp("ChassisService_client", "getDisplayReqSts", {}, {"out": {"highPriSts": 0, "lowPriSts": 0}})    
                self.partner.empty_all()
                self.sd_tester.change_usage_mode(UsgMod2)
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 15) 
                self.partner.send_request_and_ck_resp("ChassisService_client", "getDisplayReqSts", {}, {"out": {"highPriSts": 0, "lowPriSts": 0}})
                self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "epbDisplayReqSts", timeout=0.8)
                self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "epbDisplayReqSts", {"sts": {"highPriSts": 4, "lowPriSts": 0}})
                self.partner.send_request_and_ck_resp("ChassisService_client", "getDisplayReqSts", {}, {"out": {"highPriSts": 4, "lowPriSts": 0}})                      

    def ck_epbDisplayReqSts_and_getDisplayReqSts(self, highPriSts, lowPriSts, timeout=3):
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "epbDisplayReqSts", {"sts": {"highPriSts": highPriSts, "lowPriSts": lowPriSts}}, timeout)
        self.partner.send_request_and_ck_resp("ChassisService_client", "getDisplayReqSts", {}, {"out": {"highPriSts": highPriSts, "lowPriSts": lowPriSts}})
        
    @allure.title("EPB显示请求状态_仲裁")
    @pytest.mark.full
    def test_caseid_1981677(self):   
        self.set_DisplayReqSts(signal=[0, 0, 0, 0])  
        self.partner.send_request_and_ck_resp("ChassisService_client", "getDisplayReqSts", {}, {"out": {"highPriSts": 0, "lowPriSts": 0}}, timeout=3)
        self.set_DisplayReqSts(signal=[0, 0, 0, 1])
        self.ck_epbDisplayReqSts_and_getDisplayReqSts(highPriSts=5, lowPriSts=5)
        self.set_DisplayReqSts(signal=[1, 3, 0, 1])
        self.ck_epbDisplayReqSts_and_getDisplayReqSts(highPriSts=1, lowPriSts=2)
        self.set_DisplayReqSts(signal=[1, 1, 0, 1])  
        self.ck_epbDisplayReqSts_and_getDisplayReqSts(highPriSts=2, lowPriSts=5)
        self.set_DisplayReqSts(signal=[15, 11, 0, 1])  
        self.ck_epbDisplayReqSts_and_getDisplayReqSts(highPriSts=4, lowPriSts=5)
        self.set_DisplayReqSts(signal=[5, 11, 0, 1])  
        self.ck_epbDisplayReqSts_and_getDisplayReqSts(highPriSts=5, lowPriSts=5)
        self.set_DisplayReqSts(signal=[5, 11, 0, 0])  
        self.ck_epbDisplayReqSts_and_getDisplayReqSts(highPriSts=11, lowPriSts=12)    
        
    @allure.title("设置EGSM虚拟挡位显示状态_取值遍历&下行PDU周期校验")
    @pytest.mark.sanity
    def test_caseid_1980825(self):     # V1.3.1 周期80ms
        file_path, save_name = self.bgmcli.start_bgm_tcpdump() 
        dict1={1:0, 2:1, 3:2, 7:7}
        for key,value in dict1.items():
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetEGSMVirtualGearDisp", {"gear": key})
            self.ipdu.check(self.ipdu.propulsioncan.BgmPropulsionFr01, 'GearLvrIndcnInv', value, timeout=0.5)
            sleep(2)
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetEGSMVirtualGearDisp", {"gear": 0})
            sleep(2)       
        # 检验TCP报文 # 列表里面为元祖（pdu的id，数据长度，信号起始bit位，信号长度，信号值），可以 是多个元祖
        data_list1 = [(10014, 1, 2, 3, 0),(10014, 1, 2, 3, 1),(10014, 1, 2, 3, 2),(10014, 1, 2, 3, 7)]
        data_list2 = [(10014, 1, 2, 3)]
        self.ck_pdu(file_path,save_name,data_list1,data_list2)     

    @allure.title("设置EGSM虚拟挡位显示状态_启动默认值")
    @pytest.mark.full
    def test_caseid_1985789(self):  
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetEGSMVirtualGearDisp", {"gear": 7})
        self.ipdu.check(self.ipdu.propulsioncan.BgmPropulsionFr01, 'GearLvrIndcnInv', 7, timeout=0.5)
        sleep(2)
        self.restart_bgm_and_connect_service("ChassisService_client")
        self.ipdu.check(self.ipdu.propulsioncan.BgmPropulsionFr01, 'GearLvrIndcnInv', 0, timeout=7)

    @allure.title("获取&通知EGSM虚拟挡位请求_取值遍历")
    @pytest.mark.sanity
    def test_caseid_109528(self): # DrvrGearShiftReqInv|EGSMVirtualShiftReq     
        self.ipdu.set(self.ipdu.propulsioncan.EgsmPropFr01, 'DrvrGearShiftReqInv', 3)   
        self.partner.empty_all(2)      
        for i in range(8): 
            self.ipdu.set(self.ipdu.propulsioncan.EgsmPropFr01, 'DrvrGearShiftReqInv', i)
            value=3 if i>3 else i
            if i>3:
                self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "EGSMVirtualShiftReq")
            else:
                self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "EGSMVirtualShiftReq", {"gear": value})
            self.partner.send_request_and_ck_resp("ChassisService_client", "GetEGSMVirtualShiftReq", {}, {"out": value})  

    @allure.title("设置陡坡缓降开关状态_取值遍历&下行PDU校验")
    @pytest.mark.sanity
    def test_caseid_1913760(self):
        file_path, save_name = self.bgmcli.start_bgm_tcpdump() 
        for on in [False, False, True, True]:           
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetHDC", {"on": on})
            self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr05, 'HillDwnCtrlSt', int(on)) 
            sleep(2)
        # 检验TCP报文 # 列表里面为元祖（pdu的id，数据长度，信号起始bit位，信号长度，信号值），可以 是多个元祖
        data_list1 = [(10008, 1, 0, 1, 1),(10008, 1, 0, 1, 0)]
        data_list2 = [(10008, 1, 0, 1)]
        self.ck_pdu(file_path,save_name,data_list1,data_list2)
        
    @allure.title("获取&通知陡坡缓降开关状态_取值遍历")
    @pytest.mark.sanity
    def test_caseid_1980507(self):  
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetHDC", {"on": True})     
        self.partner.empty_all(2)
        for on in [ False, True]:           
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetHDC", {"on": on})
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "HDCChanged", {"on": on})
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetHDCOn", {},{"out":on})
            
    @allure.title("设置滑行能量模式_取值遍历&下行PDU校验")
    @pytest.mark.sanity
    def test_caseid_109572(self):
        file_path, save_name = self.bgmcli.start_bgm_tcpdump() 
        for on in [False, False, True, True]:   
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetCoastEnergyRegenerateMode", {"on": on})                
            self.ipdu.check(self.ipdu.chassiscan1.BgmChas1Fr02, 'CstRgnModSet', int(not on)) 
            sleep(2)  
        data_list1 = [(10004, 1, 0, 1, 0),(10004, 1, 0, 1, 1)]
        data_list2 = [(10004, 1, 0, 1)]
        self.ck_pdu(file_path,save_name,data_list1,data_list2)

    @allure.title("设置蠕行模式_取值遍历&下行PDU校验")
    @pytest.mark.sanity
    def test_caseid_111464(self): 
        file_path, save_name = self.bgmcli.start_bgm_tcpdump()
        for on in [False, False, True, True]:   
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetCreepMode", {"on": on})                
            self.ipdu.check(self.ipdu.chassiscan1.BgmChas1Fr02, 'CrpModSet', int(not on)) 
            sleep(2) 
        data_list1 = [(10010, 1, 0, 1, 1),(10010, 1, 0, 1, 0)]
        data_list2 = [(10010, 1, 0, 1)]
        self.ck_pdu(file_path,save_name,data_list1,data_list2)

    @allure.title("获取&通知蠕行模式状态_信号丢失")
    @pytest.mark.full
    def test_caseid_1980511(self):
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr09, 'CrpModAct', 1)
        self.partner.empty_all(2)
        self.ipdu.pause_bus_send("chassiscan1")
        sleep(2.5)
        self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "CreepMode") # on= Last Value
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetCreepMode", {}, {"out": False})
        self.ipdu.resume_bus_send("chassiscan1")
        self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "CreepMode")
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetCreepMode", {}, {"out": False})

    @allure.title("获取&通知蠕行模式状态_取值遍历")
    @pytest.mark.sanity
    def test_caseid_111466(self): 
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr09, 'CrpModAct', 1)
        self.partner.empty_all(2)
        for i in range(2):            
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr09, 'CrpModAct', i)
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "CreepMode", {"on": not bool(i)})
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetCreepMode", {}, {"out": not bool(i)})
            
    @allure.title("设置EPB夹紧释放_取值遍历&下行PDU校验")
    @pytest.mark.sanity
    def test_caseid_109247(self):
        file_path, save_name = self.bgmcli.start_bgm_tcpdump()        
        for operate in range(3):
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "EPBOperation", {"operate": operate})
            self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr03, 'EpbSoftSwtCtrlSt', operate+1)
            sleep(2) 
        data_list1 = [(10005, 1, 2, 3, 1), (10005, 1, 2, 3, 2), (10005, 1, 2, 3, 3)]
        data_list2 = [(10005, 1, 2, 3)]
        self.ck_pdu(file_path,save_name,data_list1,data_list2)
        
    @allure.title("获取&通知EPB功能运行状态_取值遍历")
    @pytest.mark.sanity
    def test_caseid_110765(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 6)
        self.partner.empty_all(2)
        for i in range(16):
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', i)
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "EPBOperationStatus", {"state": i})
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetEPBOperationStatus", {},{"out": i})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 15)
        self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "EPBOperationStatus")

    @allure.title("获取&通知AVH功能显示请求状态_取值遍历")
    @pytest.mark.smoke
    def test_caseid_1919161(self): # DispMsgByVehHld|avhDisplayReqSts    
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'DispMsgByVehHld', 5)  # len=3
        self.partner.send_request_and_ck_resp("ChassisService_client", "getAvhDisplayReqSts", {}, {"out": 5}, timeout=5)  
        self.partner.empty_all()
        for i in range(8):
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'DispMsgByVehHld', i) 
            value = 0 if i>5 else i
            if i>6:
                self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "avhDisplayReqSts")   
            else:                
                self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "avhDisplayReqSts",  {"sts": value}, timeout=5)        
            self.partner.send_request_and_ck_resp("ChassisService_client", "getAvhDisplayReqSts", {}, {"out": value})  
            
    @allure.title("获取&通知AVH功能显示请求状态_信号丢失")
    @pytest.mark.full
    def test_caseid_109681(self): # DispMsgByVehHld|avhDisplayReqSts   
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'DispMsgByVehHld', 0)  # len=3
        self.partner.send_request_and_ck_resp("ChassisService_client", "getAvhDisplayReqSts", {}, {"out": 0}, timeout=3)  
        self.ipdu.pause_bus_send("backbonefr")
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "avhDisplayReqSts",  {"sts": 2}, timeout=2.5)  
        self.partner.send_request_and_ck_resp("ChassisService_client", "getAvhDisplayReqSts", {}, {"out": 2})  
        self.ipdu.resume_bus_send("backbonefr") 
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "avhDisplayReqSts",  {"sts": 0})   
        self.partner.send_request_and_ck_resp("ChassisService_client", "getAvhDisplayReqSts", {}, {"out": 0})  

    @allure.title("获取&通知制动系统报警信息显示请求状态_取值遍历")
    @pytest.mark.sanity
    def test_caseid_110736(self): # fr BrkMsgWarnReq|brkSysWarnMsgDisplayReqSts
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkMsgWarnReq', 1)
        self.partner.send_request_and_ck_resp("ChassisService_client", "getBrkSysWarnMsgDisReqSts", {},{"out": 1}, timeout=5)
        self.partner.empty_all()
        for i in range(8):
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkMsgWarnReq', i)
            sleep(2)
            logger.info(f"打印当前返回值i={i}")
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "brkSysWarnMsgDisplayReqSts",{"sts": i})
            self.partner.send_request_and_ck_resp("ChassisService_client", "getBrkSysWarnMsgDisReqSts", {},{"out": i})

    @allure.title("获取&通知制动系统报警信息显示请求状态_服务启动默认值")
    @pytest.mark.full
    @pytest.mark.restart 
    def test_caseid_1979691(self):     
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkMsgWarnReq', 3)
        self.partner.send_request_and_ck_resp("ChassisService_client", "getBrkSysWarnMsgDisReqSts", {},{"out": 3}, timeout=3)
        self.restart_bgm_and_connect_service(CHASSIS_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp("ChassisService_client", "getBrkSysWarnMsgDisReqSts", {},{"out": 0})

    @allure.title("获取&通知驻车系统故障状态_信号取值遍历")
    @pytest.mark.sanity
    def test_caseid_110334(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkRelsWarnReq', 1) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkRelsWarnReqSts",{}, {"out": True}, timeout=5)
        self.partner.empty_all(1)      
        for i in range(2):  
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkRelsWarnReq', i)  
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "brkRelsWarnReqSts", {"sts": bool(i)}, timeout=5)
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkRelsWarnReqSts",{}, {"out": bool(i)}, timeout=3)

    @allure.title("获取&通知驻车系统故障状态_信号丢失")
    @pytest.mark.full
    def test_caseid_110165(self): # SOA-18929
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkRelsWarnReq', 0)  
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkRelsWarnReqSts",{}, {"out": False}, timeout=3)
        self.ipdu.pause_bus_send("backbonefr")
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "brkRelsWarnReqSts", {"sts": True}, timeout=2.5)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkRelsWarnReqSts",{}, {"out": True})
        self.ipdu.resume_bus_send("backbonefr")
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "brkRelsWarnReqSts", {"sts": False})
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkRelsWarnReqSts",{}, {"out": False})     
        
    @allure.title("获取&通知当前chassis模块故障列表_车速无效_信号丢失")
    @pytest.mark.full
    def test_caseid_1981495_1981498_1981503_1981493_1981504(self): # 1=车速无效 2=显示车速无效 3/4/5/6=轮速失效 7/8/9/10=旋转脉冲计数失效 15=车辆运动状态失效
        self.chassis_fault_default()
        self.ipdu.pause_bus_send("backbonefr") 
        self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "ChassisFault", 
                                       {"faults": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15]}, timeout=1.5)
        self.ipdu.resume_bus_send("backbonefr")
        self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "ChassisFault", {"faults": [0]})
        
    @allure.title("获取&通知当前chassis模块故障列表_车速无效_E2E校验")
    @pytest.mark.full
    def test_caseid_1981497(self): 
        self.chassis_fault_default()
        try:
            self.ipdu.set_no_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf')
            self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "ChassisFault", {"faults": [1]})
            self.partner.empty_all(3)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
            self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "ChassisFault")
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf')
            assert False, error
        else:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf') 
        self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "ChassisFault", {"faults": [0]})
        
    @allure.title("获取&通知当前chassis模块故障列表_左前轮轮速失效_E2E校验")
    @pytest.mark.full
    def test_caseid_1981501(self): 
        self.chassis_fault_default()
        try:
            self.ipdu.set_no_crc(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlFrntLeQf')
            self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "ChassisFault", {"faults": [3]})
            self.partner.empty_all(3)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlFrntLeQf', 3) 
            self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "ChassisFault")
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlFrntLeQf')
            assert False, error
        else:
            self.ipdu.restore_crc(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlFrntLeQf') 
        self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "ChassisFault", {"faults": [0]})
        
    @allure.title("获取&通知当前chassis模块故障列表_右前轮轮速失效_E2E校验")
    @pytest.mark.full
    def test_caseid_1981499(self): 
        self.chassis_fault_default()
        try:
            self.ipdu.set_no_crc(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlFrntRiQf')
            self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "ChassisFault", {"faults": [4]})
            self.partner.empty_all(3)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlFrntRiQf', 3)
            self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "ChassisFault")
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlFrntRiQf')
            assert False, error
        else:
            self.ipdu.restore_crc(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlFrntRiQf') 
        self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "ChassisFault", {"faults": [0]})
        
    @allure.title("获取&通知当前chassis模块故障列表_左后轮轮速失效_E2E校验")
    @pytest.mark.full
    def test_caseid_1981502(self): 
        self.chassis_fault_default()
        try:
            self.ipdu.set_no_crc(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlReLeQf')
            self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "ChassisFault", {"faults": [5]})
            self.partner.empty_all(3)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlReLeQf', 3) 
            self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "ChassisFault")
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlReLeQf')
            assert False, error
        else:
            self.ipdu.restore_crc(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlReLeQf') 
        self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "ChassisFault", {"faults": [0]})
        
    @allure.title("获取&通知当前chassis模块故障列表_右后轮轮速失效_E2E校验")
    @pytest.mark.full
    def test_caseid_1981500(self): 
        self.chassis_fault_default()
        try:
            self.ipdu.set_no_crc(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlReRiQf')
            self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "ChassisFault", {"faults": [6]})
            self.partner.empty_all(3)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlReRiQf', 3) 
            self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "ChassisFault")
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlReRiQf')
            assert False, error
        else:
            self.ipdu.restore_crc(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlReRiQf') 
        self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "ChassisFault", {"faults": [0]})
        
    @allure.title("获取&通知当前chassis模块故障列表_旋转脉冲计数失效_E2E校验")
    @pytest.mark.full
    def test_caseid_1981488_1981490_1981491_1981492(self): 
        self.chassis_fault_default()
        try:
            self.ipdu.set_no_crc(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlRotToothCntrFrntLe')
            self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "ChassisFault", {"faults": [7, 8, 9, 10]})
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlRotToothCntrFrntLe')
            assert False, error
        else:
            self.ipdu.restore_crc(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlRotToothCntrFrntLe') 
        self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "ChassisFault", {"faults": [0]})
        
    @allure.title("获取当前chassis模块故障列表_服务启动默认值")
    @pytest.mark.restart 
    @pytest.mark.full
    def test_caseid_1943398(self): 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 2)  # 故障列表有 1,2 
        self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "ChassisFault", {"faults": [1, 2]}) 
        self.restart_bgm_and_connect_service(CHASSIS_SERVICE_CLIENT, resume_all_bus=False)      
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetChassisFault", {},{"out": [0]},timeout=3)
        
    @allure.title("获取&通知当前chassis模块故障列表_车速无效_取值遍历")
    @allure.title("获取&通知当前chassis模块故障列表_显示车速无效_取值遍历")
    @pytest.mark.smoke
    def test_caseid_1979741_1979740(self): 
        self.chassis_fault_default()
        for i in range(4):
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', i) 
            if i == 0:
                self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "ChassisFault", {"faults": [1]})
                self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "ChassisFault", {"faults": [2]})
            elif i == 3:
                self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "ChassisFault", {"faults": [0]})
            else:
                self.partner.ck_no_event_and_ck_resp(CHASSIS_SERVICE_CLIENT, "ChassisFault", {"out": [1, 2]})

    @allure.title("获取&通知当前chassis模块故障列表_左前轮轮速失效_取值遍历")
    @pytest.mark.sanity
    def test_caseid_1979739(self): # WhlSpdCircumlFrntLeQf|ChassisFaultInfo
        self.chassis_fault_default()
        for i in range(4):
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlFrntLeQf', i) 
            value = 0 if i == 3 else 3
            if i in [0, 3]:
                self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "ChassisFault", {"faults": [value]})
            else:
                self.partner.ck_no_event_and_ck_resp(CHASSIS_SERVICE_CLIENT, "ChassisFault", {"out": [value]})

    @allure.title("获取&通知当前chassis模块故障列表_右前轮轮速失效_取值遍历")
    @pytest.mark.sanity
    def test_caseid_1979738(self):  
        self.chassis_fault_default()
        for i in range(4):
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlFrntRiQf', i) 
            value = 0 if i == 3 else 4
            if i in [0, 3]:
                self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "ChassisFault", {"faults": [value]})
            else:
                self.partner.ck_no_event_and_ck_resp(CHASSIS_SERVICE_CLIENT, "ChassisFault", {"out": [value]})

    @allure.title("获取&通知当前chassis模块故障列表_左后轮轮速失效_取值遍历")
    @pytest.mark.sanity
    def test_caseid_1979737(self):  
        self.chassis_fault_default()
        for i in range(4):
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlReLeQf', i) 
            value = 0 if i == 3 else 5
            if i in [0, 3]:
                self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "ChassisFault", {"faults": [value]})
            else:
                self.partner.ck_no_event_and_ck_resp(CHASSIS_SERVICE_CLIENT, "ChassisFault", {"out": [value]})
        
    @allure.title("获取&通知当前chassis模块故障列表_右后轮轮速失效_取值遍历")
    @pytest.mark.sanity
    def test_caseid_1979736(self):  
        self.chassis_fault_default()
        for i in range(4):
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlReRiQf', i) 
            value = 0 if i == 3 else 6
            if i in [0, 3]:
                self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "ChassisFault", {"faults": [value]})
            else:
                self.partner.ck_no_event_and_ck_resp(CHASSIS_SERVICE_CLIENT, "ChassisFault", {"out": [value]})
        
    @allure.title("获取&通知当前chassis模块故障列表_车辆运动状态失效_E2E校验")
    @pytest.mark.sanity
    def test_caseid_1979735(self):  # VehMtnStVehMtnSt|ChassisFaultInfo
        self.chassis_fault_default()
        try:
            self.ipdu.set_no_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt')  
            self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "ChassisFault", {"faults": [15]})
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt')  
            assert False, error 
        else:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt')  
        self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "ChassisFault", {"faults": [0]})
     
    @allure.title("获取&通知ESC Off指示状态_取值遍历")
    @pytest.mark.smoke
    def test_caseid_110730(self): # DrvModEscOffDrvModEscOff|EscStEscSt|escOffIndicateLightSts
        last_value=self.partner.send_request_and_return_resp(CHASSIS_SERVICE_CLIENT, "getESCOffIndicateLightSts", {})["out"]  
        logger.info(f"打印当前值：last_value={last_value}")
        for i in range(2):
            for j in range(8):      
                self.partner.empty_all(1)          
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'DrvModEscOffDrvModEscOff', i) # 信号长度为1
                sleep(1)
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', j) # 信号长度为3
                sleep(1)
                value=True if i==1 or j in [0,4] else False
                logger.info(f"打印当前值：last_value={last_value},value={value},i={i},j={j}")
                if value == last_value:
                    self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "escOffIndicateLightSts")
                else:
                    self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "escOffIndicateLightSts", {"sts": value})
                self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getESCOffIndicateLightSts", {}, {"out": value})
                last_value=value
                
    @allure.title("获取&通知ESC Off指示状态_信号丢失")
    @pytest.mark.sanity
    def test_caseid_1979622(self): # DrvModEscOffDrvModEscOff|EscStEscSt|escOffIndicateLightSts
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'DrvModEscOffDrvModEscOff', 0) # 信号长度为1 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 1) # 信号长度为3
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getESCOffIndicateLightSts", {}, {"out": False}, timeout=5)
        self.ipdu.pause_bus_send("backbonefr")
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "escOffIndicateLightSts", {"sts": True}, timeout=2.5)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getESCOffIndicateLightSts", {}, {"out": True})
        self.ipdu.resume_bus_send("backbonefr")
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "escOffIndicateLightSts", {"sts": False})
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getESCOffIndicateLightSts", {}, {"out": False})
        
    @allure.title("获取&通知ESC Off指示状态_EscOff信号E2E校验失败")
    @pytest.mark.full
    def test_caseid_1979624(self): # fr DrvModEscOffDrvModEscOff|fr EscStEscSt|escOffIndicateLightSts|DrvModEscOffDrvModEscOff_E2E|EscStEscSt_E2E
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'DrvModEscOffDrvModEscOff', 0) # 信号长度为1 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 1) # 信号长度为3
        sleep(1) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getESCOffIndicateLightSts", {}, {"out": False})
        try:
            self.ipdu.set_no_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'DrvModEscOffDrvModEscOff')  
            sleep(2)
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "escOffIndicateLightSts", {"sts": True})
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getESCOffIndicateLightSts", {}, {"out": True})  
              
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 0)  # 任何一个信号组发生进入E2E故障之后，就用故障替代值的
            self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "escOffIndicateLightSts")
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getESCOffIndicateLightSts", {}, {"out": True})
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'DrvModEscOffDrvModEscOff')  
            assert False, error
        else:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'DrvModEscOffDrvModEscOff')  
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getESCOffIndicateLightSts", {}, {"out": True})
        
    @allure.title("获取&通知ESC Off指示状态_EscStEscSt信号E2E校验失败")
    @pytest.mark.full
    def test_caseid_1979625(self): 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'DrvModEscOffDrvModEscOff', 0) # 信号长度为1 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 1) # 信号长度为3
        sleep(1) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getESCOffIndicateLightSts", {}, {"out": False})
        try:
            self.ipdu.set_no_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt')  
            sleep(2)
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "escOffIndicateLightSts", {"sts": True})
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getESCOffIndicateLightSts", {}, {"out": True})  
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt')  
            assert False, error
        else:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt')  
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getESCOffIndicateLightSts", {}, {"out": False})

    @allure.title("获取&通知EPB警示音请求状态_参数value=0")
    @pytest.mark.smoke
    def test_caseid_1980410(self):  # fr VehSpdLgtQf|fr VehSpdLgtA|fr EpbLampReqEpbLampReq|fr EpbLampReqSecEpbLampReq|epbWarnChimeReqStsEvent
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3) # 车速值有效
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 5.0) # 10<VehSpdLgtA < 20km/h
        self.partner.empty_all(2)
        last_value=self.partner.send_request_and_return_resp(CHASSIS_SERVICE_CLIENT, "getWarnChimeReqSts", {})["out"]
        for req in [1, 0, 2]: # 测 0 1 2
            for req_sec in [1, 0, 2]:                
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq', req)
                self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq', req_sec) 
                value=0 if (req==1 or req==2) and (req_sec==1 or req_sec==2) else 1
                if last_value==value:
                    self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT,"epbWarnChimeReqSts", timeout=3)
                else:
                    self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,"epbWarnChimeReqSts",{"sts":value})
                self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getWarnChimeReqSts", {}, {"out": value})       
                last_value=value                         
        
    @allure.title("获取&通知EPB警示音请求状态_EpbLampReqEpbLampReq=0取值遍历")
    @pytest.mark.sanity
    def test_caseid_1943401(self):  
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3) # 车速值有效
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getWarnChimeReqSts", {}, {"out": 0}, timeout=3)
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq',2)   
        speed=[2.0, 5.0, 6.0, 7.0] 
        value=[0, 1, 1, 2]
        for i in range(4):
            logger.info(f"i={i},speed={speed[i]},value={value[i]}")
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', speed[i])
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq',0)
            if i in [1,3]:
                self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,"epbWarnChimeReqSts",{"sts":value[i]})
            else:
                self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT,"epbWarnChimeReqSts")  # last value
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getWarnChimeReqSts", {}, {"out": value[i]})

    @allure.title("获取&通知EPB警示音请求状态_EpbLampReqSecEpbLampReq=0取值遍历")
    @pytest.mark.sanity
    def test_caseid_1959923(self):  
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3) # 车速值有效
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getWarnChimeReqSts", {}, {"out": 0}, timeout=3)    
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq',2)
        # 5km/h >1  10km/h >2  20km/h >5  25km/h >6
        # 5km/h ≤ VehSpdLgtA ≤ 10km/h，设置信号VehSpdLgtA =2.0   
        # 10<VehSpdLgtA < 20km/h，设置信号VehSpdLgtA =5.0
        # 20km/h ≤ VehSpdLgtA ≤ 25km/h，设置信号VehSpdLgtA =6.0
        # VehSpdLgtA > 25km/h，设置信号VehSpdLgtA =7.0
        speed=[2.0, 5.0, 6.0, 7.0] 
        value=[0, 1, 1, 2]
        for i in range(4):
            self.partner.empty_all(2)
            logger.info(f"i={i},speed={speed[i]},value={value[i]}")
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', speed[i])
            self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq',0)
            if i in [1,3]:
                self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,"epbWarnChimeReqSts",{"sts":value[i]})
            else:
                self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT,"epbWarnChimeReqSts")  # last value
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getWarnChimeReqSts", {}, {"out": value[i]})

    @allure.title("获取&通知EPB警示音请求状态_信号取值3")
    @pytest.mark.full
    def test_caseid_1959969(self): 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3) # 车速值有效
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getWarnChimeReqSts", {}, {"out": 0}, timeout=3)
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq',3) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq',3)
        self.partner.empty_all(2)
        speed=[2.0, 5.0, 6.0, 7.0] 
        for i in speed:
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', i) # 只有速度值变化 
            self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT,"epbWarnChimeReqSts", timeout=3)
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getWarnChimeReqSts", {}, {"out": 0})

        # 5km/h >1  10km/h >2  20km/h >5  25km/h >6
        # 5km/h ≤ VehSpdLgtA ≤ 10km/h，设置信号VehSpdLgtA =2.0   
        # 10<VehSpdLgtA < 20km/h，设置信号VehSpdLgtA =5.0
        # 20km/h ≤ VehSpdLgtA ≤ 25km/h，设置信号VehSpdLgtA =6.0
        # VehSpdLgtA > 25km/h，设置信号VehSpdLgtA =7.0

    @allure.title("获取EPB警示音请求状态_服务启动默认值")
    @pytest.mark.full
    def test_caseid_1943402(self):  
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq',0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3) # 车速值有效
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 7.0) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getWarnChimeReqSts", {}, {"out": 2}, timeout=3) 
        self.ipdu.pause_bus_send("backbonefr")   
        self.nucapp.bgm_power_off()
        sleep(2)
        self.nucapp.bgm_power_on()
        self.partner.wait_for_service_reconnect(CHASSIS_SERVICE_CLIENT)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getWarnChimeReqSts", {}, {"out": 0}, timeout=1)      

    @allure.title("获取&通知车辆静止状态_取值遍历")
    @pytest.mark.sanity
    def test_caseid_1939930(self): 
        self.ipdu.set(self.ipdu.chassiscan1.VddmChas1Fr53, 'StandStillMgrStsForHld1', 6) 
        sleep(2)
        for i in range(8):
            self.partner.empty_all()
            self.ipdu.set(self.ipdu.chassiscan1.VddmChas1Fr53, 'StandStillMgrStsForHld1', i)
            validity=1 if i==4 or i==7 else 0
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,"VehicleStandStillSts",{"sts":{"value":i,"validity":validity}})    
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,"GetVehicleStandStillSts",{},{"out":{"value":i,"validity":validity}})
            
    @allure.title("获取&通知车辆静止状态_E2E校验失败")
    @pytest.mark.full
    def test_caseid_1939946(self):  # WhlRotToothCntr_E2E result: 1  表示校验失败
        self.ipdu.set(self.ipdu.chassiscan1.VddmChas1Fr53, 'StandStillMgrStsForHld1', 3) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetVehicleStandStillSts", {}, {"out": {"value":3,"validity":0}}, timeout=3)     
        try:
            self.ipdu.set_no_crc(self.ipdu.chassiscan1.VddmChas1Fr53, 'StandStillMgrStsForHld1') 
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,"VehicleStandStillSts",{"sts":{"value":3,"validity":7}})    
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetVehicleStandStillSts", {}, {"out": {"value":3,"validity":7}})                
            self.ipdu.set(self.ipdu.chassiscan1.VddmChas1Fr53, 'StandStillMgrStsForHld1', 4) 
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,"VehicleStandStillSts",{"sts":{"value":4,"validity":7}})    
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetVehicleStandStillSts", {}, {"out": {"value":4,"validity":7}})   
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.chassiscan1.VddmChas1Fr53, 'StandStillMgrStsForHld1') 
            assert False, error
        else:
            self.ipdu.restore_crc(self.ipdu.chassiscan1.VddmChas1Fr53, 'StandStillMgrStsForHld1') 
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,"VehicleStandStillSts",{"sts":{"value":4,"validity":1}})  
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetVehicleStandStillSts", {}, {"out": {"value":4,"validity":1}})       
            
    @allure.title("获取&通知车辆静止状态_信号丢失")
    @pytest.mark.full
    def test_caseid_1939945(self):
        self.ipdu.set(self.ipdu.chassiscan1.VddmChas1Fr53, 'StandStillMgrStsForHld1', 7) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetVehicleStandStillSts", {}, {"out": {"value":7,"validity":1}}, timeout=3) 
        self.partner.empty_all() 
        self.ipdu.pause_bus_send("chassiscan1")
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,"VehicleStandStillSts",{"sts":{"value":7,"validity":4}}, timeout=2.5)    
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetVehicleStandStillSts", {}, {"out": {"value":7,"validity":4}})   
        self.ipdu.resume_bus_send("chassiscan1")
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,"VehicleStandStillSts",{"sts":{"value":7,"validity":1}}) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetVehicleStandStillSts", {}, {"out": {"value":7,"validity":1}},timeout=3) 

    @allure.title("获取&通知车辆静止状态_E2E校验失败后信号丢失再恢复")
    @pytest.mark.sanity
    def test_caseid_1979338(self): 
        self.ipdu.set(self.ipdu.chassiscan1.VddmChas1Fr53, 'StandStillMgrStsForHld1', 5) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetVehicleStandStillSts", {}, {"out": {"value":5,"validity":0}}, timeout=3) 
        self.partner.empty_all()   
        try:
            self.ipdu.set_no_crc(self.ipdu.chassiscan1.VddmChas1Fr53, 'StandStillMgrStsForHld1') 
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,"VehicleStandStillSts",{"sts":{"value":5,"validity":7}}) 
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetVehicleStandStillSts", {}, {"out": {"value":5,"validity":7}})   
            self.ipdu.pause_bus_send("chassiscan1")
            self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT,"VehicleStandStillSts", timeout=2.5)      
        except Exception as error:
            self.ipdu.resume_bus_send("chassiscan1")
            self.ipdu.restore_crc(self.ipdu.chassiscan1.VddmChas1Fr53, 'StandStillMgrStsForHld1') 
            assert False,error
        else:
            self.ipdu.resume_bus_send("chassiscan1")
            self.ipdu.restore_crc(self.ipdu.chassiscan1.VddmChas1Fr53, 'StandStillMgrStsForHld1') 
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,"VehicleStandStillSts",{"sts":{"value":5,"validity":0}}) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetVehicleStandStillSts", {}, {"out": {"value":5,"validity":0}}) 
        
    @allure.title("获取&通知EPedal单踏板模式功能状态信息_取值遍历")
    @pytest.mark.sanity
    def test_caseid_1979332(self):    # EPedlModSts|EPedlModeInfo|EPedlInhbnSts|EPedlDrvrIndcnMsg
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr07, 'EPedlModSts', 3)      
        sleep(2)   
        for i in [1,2,3]:
            for j in range(2):
                for k in range(4):   
                    self.partner.empty_all()     
                    self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr07, 'EPedlModSts', i) 
                    self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr09, 'EPedlInhbnSts', j) 
                    self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr38, 'EPedlDrvrIndcnMsg', k) 
                    self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,"EPedlModeInfo",{"info":{"mode":i-1,"inhibitSts":j,"decelerationLimitSts":k}})    
                    self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetEPedlModeInfo", {}, {"out": {"mode":i-1,"inhibitSts":j,"decelerationLimitSts":k}})   
        for i in [0, 4, 7]:
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr07, 'EPedlModSts', i)   
            self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT,"EPedlModeInfo")
    
    @allure.title("获取&通知车轮滑移率信息_取值遍历")
    @pytest.mark.sanity
    def test_caseid_1989342(self):  # can WhlSlipRate|UpdateWheelSlipRate
        signals=["WhlSlipRateFLPrpsn","WhlSlipRateFRPrpsn","WhlSlipRateRLPrpsn","WhlSlipRateRRPrpsn"]
        for rate in [-1000, -1, 0, 100, 1000]:
            for signal in signals:
                self.ipdu.set(self.ipdu.chassiscan1.VcuChas1Fr10, signal, rate) 
            info={"wheelSlipRateFL":rate* 0.1, "wheelSlipRateFR":rate* 0.1, "wheelSlipRateRL":rate* 0.1, "wheelSlipRateRR":rate* 0.1}  
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,"WheelSlipRate",{"info":info})
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetWheelSlipRate", {}, {"out": info}) 
            
    @allure.title("获取&通知车轮滑移率信息_超范围值")
    @pytest.mark.full
    def test_caseid_1989341(self): 
        signals=["WhlSlipRateFLPrpsn","WhlSlipRateFRPrpsn","WhlSlipRateRLPrpsn","WhlSlipRateRRPrpsn"]
        for signal in signals:
            self.ipdu.set(self.ipdu.chassiscan1.VcuChas1Fr10, signal, 60.9) 
        info = {"wheelSlipRateFL":60.9,"wheelSlipRateFR":60.9,"wheelSlipRateRL":60.9,"wheelSlipRateRR":60.9}
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetWheelSlipRate", {}, {"out":info}) 
        self.partner.empty_all(1)
        for signal in signals:
            self.ipdu.set(self.ipdu.chassiscan1.VcuChas1Fr10, signal, random.choice([-1023, 1023])) 
        self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT,"WheelSlipRate")
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetWheelSlipRate", {}, {"out": info}) 
        
    @allure.title("获取&通知车轮滑移率信息_服务启动默认值")
    @pytest.mark.full
    def test_caseid_1989340(self):
        signals=["WhlSlipRateFLPrpsn","WhlSlipRateFRPrpsn","WhlSlipRateRLPrpsn","WhlSlipRateRRPrpsn"]
        for signal in signals:
            self.ipdu.set(self.ipdu.chassiscan1.VcuChas1Fr10, signal, -100) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetWheelSlipRate", {}, 
                                              {"out": {"wheelSlipRateFL":-10.0, "wheelSlipRateFR":-10.0, "wheelSlipRateRL":-10.0, "wheelSlipRateRR":-10.0}}) 
        self.partner.empty_all(2)
        self.restart_bgm_and_connect_service(CHASSIS_SERVICE_CLIENT, resume_all_bus=False)                                              
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetWheelSlipRate", {}, 
                                              {"out": {"wheelSlipRateFL":255.0,"wheelSlipRateFR":255.0,"wheelSlipRateRL":255.0,"wheelSlipRateRR":255.0}}, timeout=5) # 获取车轮滑移率信息
        self.ipdu.resume_all_bus_send()
        # for signal in signals:
        #     self.ipdu.set(self.ipdu.chassiscan1.VcuChas1Fr10, signal, 0) # 不同数据库有区别，分事件帧和周期帧，需要mca数据库
        sleep(2)
        self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT,"WheelSlipRate",
                                       {"info":{"wheelSlipRateFL":-10.0, "wheelSlipRateFR":-10.0, "wheelSlipRateRL":-10.0, "wheelSlipRateRR":-10.0}})  
    ''' 
    需求未做       
    @allure.title("获取&通知手动换挡请求信息_屏幕停车请求")
    @pytest.mark.sanity
    def test_caseid_dhy4_1(self):  # CDCDrvrGearShiftParkReq1|ManualShiftRequest
        file_path, save_name = self.bgmcli.start_bgm_tcpdump() 
        self.ipdu.set(self.ipdu.infocanfd.CdcInfoCanFdFr12, 'CDCDrvrGearShiftParkReq1', 1)
        for i in range(2):         
            self.partner.empty_all(2)     
            self.ipdu.set(self.ipdu.infocanfd.CdcInfoCanFdFr12, 'CDCDrvrGearShiftParkReq1', i) # 屏幕停车请求
            sleep(2)   
            # self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "ManualShiftRequest", {"info": {"hmiParkReq": i}})   
            # self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetManualShiftRequest", {}, {"out": {"hmiParkReq": i}}) 
        sleep(2) 
        self.ck_pdu(file_path,save_name,[],[])
           
    @allure.title("获取&通知手动换挡请求信息_换挡器停车请求")
    @pytest.mark.sanity
    def test_caseid_dhy4_2(self):  
        self.ipdu.set(self.ipdu.propulsioncan.EgsmPropFr01, 'DrvrGearShiftParkReq1', 1)
        for i in range(2):   
            self.partner.empty_all()         
            self.ipdu.set(self.ipdu.propulsioncan.EgsmPropFr01, 'DrvrGearShiftParkReq1', i) # 换挡器停车请求
            # self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "ManualShiftRequest", {"info": {"shifterParkReq": i}})   
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetManualShiftRequest", {}, {"out": {"shifterParkReq": i}}) 
            
    @allure.title("获取&通知手动换挡请求信息_屏幕切换R档请求")
    @pytest.mark.sanity
    def test_caseid_dhy4_3(self):  
        self.ipdu.set(self.ipdu.infocanfd.CdcInfoCanFdFr12, 'CDCDrvrGearShiftDirReq1DwnRTipAut', 1) 
        for i in range(2): 
            self.partner.empty_all()             
            self.ipdu.set(self.ipdu.infocanfd.CdcInfoCanFdFr12, 'CDCDrvrGearShiftDirReq1DwnRTipAut', i) # 屏幕切换R档请求
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "ManualShiftRequest", {"info": {"hmiRGearReq": i}})   
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetManualShiftRequest", {}, {"out": {"hmiRGearReq": i}}) 
            
    @allure.title("获取&通知手动换挡请求信息_屏幕切换D档请求")
    @pytest.mark.sanity
    def test_caseid_dhy4_4(self):  
        self.ipdu.set(self.ipdu.infocanfd.CdcInfoCanFdFr12, 'CDCDrvrGearShiftDirReq1UpDTipAut', 1) 
        for i in range(2): 
            self.partner.empty_all()             
            self.ipdu.set(self.ipdu.infocanfd.CdcInfoCanFdFr12, 'CDCDrvrGearShiftDirReq1UpDTipAut', i) # 屏幕切换D档请求
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "ManualShiftRequest", {"info": {"hmiDGearReq": i}})   
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetManualShiftRequest", {}, {"out": {"hmiDGearReq": i}}) 

    @allure.title("获取&通知手动换挡请求信息_屏幕切换R档备份请求")
    @pytest.mark.sanity
    def test_caseid_dhy4_5(self):  
        self.ipdu.set(self.ipdu.infocanfd.CdcInfoCanFdFr12, 'CDCDrvrGearShiftDirReq2DwnRTipAut', 1) 
        for i in range(2): 
            self.partner.empty_all()             
            self.ipdu.set(self.ipdu.infocanfd.CdcInfoCanFdFr12, 'CDCDrvrGearShiftDirReq2DwnRTipAut', i) # 屏幕切换R档备份请求
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "ManualShiftRequest", {"info": {"hmiRGearReqBackup": i}})   
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetManualShiftRequest", {}, {"out": {"hmiRGearReqBackup": i}}) 
            
    @allure.title("获取&通知手动换挡请求信息_屏幕切换D档备份请求")
    @pytest.mark.sanity
    def test_caseid_dhy4_6(self):  
        self.ipdu.set(self.ipdu.infocanfd.CdcInfoCanFdFr12, 'CDCDrvrGearShiftDirReq2UpDTipAut', 1) 
        for i in range(2): 
            self.partner.empty_all()             
            self.ipdu.set(self.ipdu.infocanfd.CdcInfoCanFdFr12, 'CDCDrvrGearShiftDirReq2UpDTipAut', i) # 屏幕切换D档备份请求
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "ManualShiftRequest", {"info": {"hmiDGearReqBackup": i}})   
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetManualShiftRequest", {}, {"out": {"hmiDGearReqBackup": i}}) 
            
    @allure.title("获取&通知手动换挡请求信息_换挡器切换D档请求")
    @pytest.mark.sanity
    def test_caseid_dhy4_7(self):  
        self.ipdu.set(self.ipdu.propulsioncan.EgsmPropFr02, 'DrvrGearShiftDirReq1DwnDwnTipAut', 1) 
        for i in range(2): 
            self.partner.empty_all()             
            self.ipdu.set(self.ipdu.propulsioncan.EgsmPropFr02, 'DrvrGearShiftDirReq1DwnDwnTipAut', i) # 换挡器切换D档请求
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "ManualShiftRequest", {"info": {"shifterDGearReq": i}})   
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetManualShiftRequest", {}, {"out": {"shifterDGearReq": i}}) 
            
    @allure.title("获取&通知手动换挡请求信息_换挡器切换R档请求")
    @pytest.mark.sanity
    def test_caseid_dhy4_8(self):  
        self.ipdu.set(self.ipdu.propulsioncan.EgsmPropFr02, 'DrvrGearShiftDirReq1UpUpTipAut', 1) 
        for i in range(2): 
            self.partner.empty_all()             
            self.ipdu.set(self.ipdu.propulsioncan.EgsmPropFr02, 'DrvrGearShiftDirReq1UpUpTipAut', i) # 换挡器切换R档请求
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "ManualShiftRequest", {"info": {"shifterRGearReq": i}})   
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetManualShiftRequest", {}, {"out": {"shifterRGearReq": i}}) 
            
    @allure.title("获取&通知手动换挡请求信息_换挡器切换D档备份请求")
    @pytest.mark.sanity
    def test_caseid_dhy4_9(self):  
        self.ipdu.set(self.ipdu.propulsioncan.EgsmPropFr02, 'DrvrGearShiftDirReq2DwnDwnTipAut', 1) 
        for i in range(2): 
            self.partner.empty_all()             
            self.ipdu.set(self.ipdu.propulsioncan.EgsmPropFr02, 'DrvrGearShiftDirReq2DwnDwnTipAut', i) # 换挡器切换D档备份请求
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "ManualShiftRequest", {"info": {"shifterDGearReqBackup": i}})   
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetManualShiftRequest", {}, {"out": {"shifterDGearReqBackup": i}}) 
            
    @allure.title("获取&通知手动换挡请求信息_换挡器切换R档备份请求")
    @pytest.mark.sanity
    def test_caseid_dhy4_20(self):  
        self.ipdu.set(self.ipdu.propulsioncan.EgsmPropFr02, 'DrvrGearShiftDirReq2UpUpTipAut', 1) 
        for i in range(2): 
            self.partner.empty_all()             
            self.ipdu.set(self.ipdu.propulsioncan.EgsmPropFr02, 'DrvrGearShiftDirReq2UpUpTipAut', i) # 换挡器切换R档备份请求
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "ManualShiftRequest", {"info": {"shifterRGearReqBackup": i}})   
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetManualShiftRequest", {}, {"out": {"shifterRGearReqBackup": i}}) 
    '''         
                
    @allure.title("获取&通知驱动系统实际状态反馈_取值遍历")
    @pytest.mark.sanity
    def test_caseid_1919378(self): 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr10, 'PTStsForRace', 7) 
        self.partner.empty_all(2)
        for i in range(8):
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr10, 'PTStsForRace', i) 
            binnum,res = bin(i),[] # 变为二进制 0b1
            if i==0:
                res=[0]            
            for j in range(len(binnum)-2): # 去掉0b前缀
                if binnum[-(j+1)] == '1' and i!=0:
                    res.append(j+1) 
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,"PropulsionStatus",{"sts":res})    
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetPropulsionStatus", {}, {"out": res})   
            seq=self.partner.send_request_and_return_resp(CHASSIS_SERVICE_CLIENT, "GetPropulsionStatus", {})["out"]
            if seq!=[0] and 0 in seq:
                assert False,"列表中不应该有0"

    @allure.title("设置弹射起步功能开启关闭_取值遍历&下行PDU校验")
    @pytest.mark.sanity
    def test_caseid_1919379(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1) 
        dict1={False:2, True:1}
        for isOn in [False, False, True, True]:     
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetLaunchMode", {"isOn":isOn})
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr25, 'LnchModSwt', dict1[isOn], timeout=0.5)
            sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("LnchModSwt", [2, 2, 1, 1])

    @allure.title("设置弹射起步功能开启关闭_信号LnchModSts监听&下行PDU校验")
    @pytest.mark.sanity
    def test_caseid_1983208(self): # UpdateLaunchMode:SetLaunchMode(0)|can LnchModSts 
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1) 
        for i in range(8):          
            for j in range(8):    
                self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts',  i) 
                sleep(0.5)
                self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetLaunchMode", {"isOn":True})
                self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr25, 'LnchModSwt', 1, timeout=0.5) 
                self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts',  j) 
                logger.info(f"打印当前返回值： i={i}, j={j}")
                if i not in [0, 5] and j in [0, 5]: # !(0||5)跳变为0||5
                    self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr25, 'LnchModSwt', 2, timeout=0.5)
                else:
                    self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr25, 'LnchModSwt', 1, timeout=0.5)
                sleep(0.5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        result = self.bgm_eth_inter.get_signal_values("LnchModSwt")
        assert result.count(2) == 23, "数据下发有误"    

    @allure.title("获取&通知弹射起步功能状态信息_取值遍历")
    @pytest.mark.sanity
    def test_caseid_1919389(self): 
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr48, 'LnchModIndcnMsg',  3) 
        sleep(2)
        dict={0:4, 1:0, 2:1, 3:2, 4:3, 5:5}
        for i in range(6):            
            for j in range(16):
                self.partner.empty_all()
                self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts',  i) 
                self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr48, 'LnchModIndcnMsg',  j) 
                self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,"LaunchMode",{"info":{"status":dict[i], "fault":j}})
                self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetLaunchMode", {}, {"out": {"status":dict[i], "fault":j}}) 
        for i in [6, 7]:
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts', i) 
            self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "LaunchMode")
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetLaunchMode", {}, {"out": {"status":5, "fault":15}})
   
    @allure.title("设置赛道模式功能开启关闭_取值遍历&下行PDU校验")
    @pytest.mark.sanity
    def test_caseid_1919383(self): 
        file_path, save_name = self.bgmcli.start_bgm_tcpdump() 
        dict1={False:2, True:1}
        for isOn in [False, False, True, True]:     
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetTrackMode", {"isOn":isOn})
            self.ipdu.check(self.ipdu.propulsioncan.BgmPropulsionFr06, 'TrackModSwt', dict1[isOn], timeout=0.5)
            sleep(2)
        data_list1 = [(30011, 1, 1, 2, 2),(30011, 1, 1, 2, 1)]
        data_list2 = [(30011, 1, 1, 2)]
        self.ck_pdu(file_path,save_name,data_list1,data_list2)

    @allure.title("获取&通知制动盘过热状态_取值遍历")
    @pytest.mark.sanity
    def test_caseid_1979331(self): 
        self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr26, 'WhlBrkOvrheatd', 0) 
        self.partner.empty_all(2) 
        for state in [1, 0]:            
            self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr26, 'WhlBrkOvrheatd', state) 
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "BrakeDiscOverHeatSts", {"state":state})
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetBrakeDiscOverHeatSts", {}, {"out": state})        
  
    @allure.title("获取&通知显示车速状态_取值遍历")
    @pytest.mark.sanity
    def test_caseid_110500(self): #  VehSpdLgtQf|VehSpdLgtA|DisplaySpeedChanged|VehSpdIndcdVehSpdIndcd 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 0)  #车速值 3=有效
        self.partner.empty_all(2) 
        for signal_Qf in range(4):
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', signal_Qf)
            for signal_A in [1.0, 19.0, 30.0]:   
                if signal_Qf==3: 
                    self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', signal_A) # 总线值=signal_A//0.00391  VehSpdLgtA=[256, 4859, 7673]
                    speed=math.ceil(signal_A*1.05*3.6) #向上取整 VehSpdIndcdVehSpdIndcd=[4, 72, 114]
                    self.partner.ck_s2s_event("ChassisService_client", "DisplaySpeedChanged",{"speed":{"speed":speed,"speedUnit":0,"isvalid":True} }) 
                    self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetDisplaySpeed", {}, {"out": {"speed":speed,"speedUnit":0,"isvalid":True} })
                else:
                    self.partner.ck_no_event("ChassisService_client", "DisplaySpeedChanged") 
                    self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetDisplaySpeed", {}, {"out": {"speed":0,"speedUnit":0,"isvalid":False}}, timeout=3)
            
    @allure.title("获取&通知显示车速状态_信号丢失")
    @pytest.mark.full
    def test_caseid_1979632(self):  
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 1.0)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetDisplaySpeed", {}, {"out": {"speed":4,"speedUnit":0,"isvalid":True}}, timeout=3)
        self.ipdu.pause_bus_send("backbonefr")
        self.partner.ck_s2s_event("ChassisService_client", "DisplaySpeedChanged",{"speed":{"speed":4,"speedUnit":0,"isvalid":False}}, timeout=1.5) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetDisplaySpeed", {}, {"out": {"speed":4,"speedUnit":0,"isvalid":False}})    
        self.ipdu.resume_bus_send("backbonefr")
        self.partner.ck_s2s_event("ChassisService_client", "DisplaySpeedChanged",{"speed":{"speed":4,"speedUnit":0,"isvalid":True}})   
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetDisplaySpeed", {}, {"out": {"speed":4,"speedUnit":0,"isvalid":True}})
                    
    @allure.title("获取&通知换挡故障状态_取值遍历")
    @pytest.mark.sanity
    def test_caseid_110430(self): # GearLvrFaultIndcn|GearFaultEvent  这里的动态数组只有一个信号控制，所以始终只有一个值
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr09, 'GearLvrFaultIndcn', 3)
        self.partner.empty_all(2)
        for i in range(8):            
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr09, 'GearLvrFaultIndcn', i)
            logger.info(f"打印当前值：{i}")
            if i > 5 : 
                self.partner.ck_no_event("ChassisService_client", "GearFault")    
                self.partner.send_request_and_ck_resp("ChassisService_client", "GetGearFault", {}, {"out": [5]})     
            else:
                self.partner.ck_s2s_event("ChassisService_client", "GearFault",{"faults":[i]})            
                self.partner.send_request_and_ck_resp("ChassisService_client", "GetGearFault", {}, {"out": [i]})  
        
    @allure.title("获取&通知换挡故障状态_信号丢失")
    @pytest.mark.full
    def test_caseid_110558(self): # GearLvrFaultIndcn|GearFaultEvent|GearLvrFaultIndcn timeout   
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr09, 'GearLvrFaultIndcn', 3)          
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetGearFault", {}, {"out": [3]}, timeout=3)  
        self.partner.empty_all() 
        self.ipdu.pause_bus_send("chassiscan1")
        self.partner.ck_s2s_event("ChassisService_client", "GearFault",{"faults":[5]}, timeout=2.5)            
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetGearFault", {}, {"out": [5]})   
        self.ipdu.resume_bus_send("chassiscan1")
        self.partner.ck_s2s_event("ChassisService_client", "GearFault",{"faults":[3]})    
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetGearFault", {}, {"out": [3]})     
        
    @allure.title("获取&通知制动液位报警提示信息状态_取值遍历")
    @pytest.mark.smoke
    def test_caseid_109823(self):  # BrkFldLvl|NotifyBrkFldLvlWarnMsgStatus
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', 1)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetBrkFldLvlWarnMsgStatus", {}, {"out": 1}, timeout=5)  
        for i in range(2):  
            self.partner.empty_all(2)  
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', i)
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "NotifyBrkFldLvlWarnMsgStatus", {"msg": i}, timeout=5)
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetBrkFldLvlWarnMsgStatus", {}, {"out": i})  
            
    @allure.title("获取&通知制动液位报警提示信息状态_信号丢失")
    @pytest.mark.full
    def test_caseid_109803(self): #  BrkFldLvl | timeout|NotifyBrkFldLvlWarnMsgStatus  
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', 0)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetBrkFldLvlWarnMsgStatus", {}, {"out": 0}, timeout=3)  
        self.partner.empty_all()  
        self.ipdu.pause_bus_send("backbonefr")
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "NotifyBrkFldLvlWarnMsgStatus", {"msg": 1}, timeout=2.5)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetBrkFldLvlWarnMsgStatus", {}, {"out": 1})  
        self.ipdu.resume_bus_send("backbonefr")
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "NotifyBrkFldLvlWarnMsgStatus", {"msg": 0})
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetBrkFldLvlWarnMsgStatus", {}, {"out": 0})  
        
    @allure.title("获取制动液位报警提示信息状态_服务启动默认值")
    @pytest.mark.full
    @pytest.mark.restart 
    def test_caseid_109727_1983630(self):  
        self.ipdu.set(self.ipdu.propulsioncan.EgsmPropFr01, 'GearLvrIllmnSts', 1) # 获取触摸换挡器激活状态
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', 1)
        sleep(3)       
        self.restart_bgm_and_connect_service(CHASSIS_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetBrkFldLvlWarnMsgStatus", {}, {"out": 0}) # 获取制动液位报警提示信息状态       
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetTouchShiftActiveSts", {}, {"out": 255}) # 获取触摸换挡器激活状态
            
    @allure.title("获取&通知AVH功能激活状态_取值遍历")
    @pytest.mark.sanity
    def test_caseid_110397(self): # LampReqByVehHld|AutoHoldWorkState
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'LampReqByVehHld', 1)
        for i in range(4):     
            self.partner.empty_all(1)          
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'LampReqByVehHld', i)
            value=True if i==1 else False
            if i in [0, 1, 2]:
                self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "AutoHoldWorkState", {"sts": value})
            else:
                self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "AutoHoldWorkState")
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetAutoHoldWorkState", {},{"out": value})
            
    @allure.title("弹射起步功能状态信息_默认值")
    @pytest.mark.full 
    def test_caseid_1939932(self):   
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts',  0) 
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr48, 'LnchModIndcnMsg',  0) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetLaunchMode", {}, {"out": {"status":4, "fault":0}}, timeout=3)
        self.restart_bgm_and_connect_service(CHASSIS_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetLaunchMode", {}, {"out": {"status":255, "fault":255}}, timeout=1)
        self.partner.empty_all()
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts', 7) 
        self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "LaunchMode")
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr48, 'LnchModIndcnMsg',  13)
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,"LaunchMode",{"info":{"status":255, "fault":13}})
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetLaunchMode", {}, {"out": {"status":255, "fault":13}})
        
    @allure.title("获取AVH功能激活状态/AVH功能显示请求状态_服务启动默认值")
    @pytest.mark.full
    @pytest.mark.restart 
    def test_caseid_110582_1979641_110413_1980510_1943385_1943387_1959996(self):  
        self.ipdu.set(self.ipdu.adcanfd.AcuADCANFDFr06, 'DrvModSetFbk', 9) # 获取超级节能模式状态反馈
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'DrvModEscOffDrvModEscOff', 1) # 获取ESC Off指示状态
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'LampReqByVehHld', 1) # 获取AVH功能激活状态 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'DispMsgByVehHld', 5)  # len=3 AVH功能显示请求状态
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)  #车速值有效         
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 100) #车速值
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'AutHldSoftSwtEnaSts', 1) # 获取AVH功能使能状态   
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'SwtStsforHillDwnCtrl', 1) # 获取HDC开关可用状态
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetHDC", {"on": True}) # 设置陡坡缓降开关为True
        sleep(3)
        self.restart_bgm_and_connect_service(CHASSIS_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetAutoHoldWorkState", {},{"out": False}) # 获取AVH功能激活状态   
        self.partner.send_request_and_ck_resp("ChassisService_client", "getAvhDisplayReqSts", {}, {"out": 1}) # AVH功能显示请求状态
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetSpeed", {}, {"out": {"speed": 0, "isvalid": 0}}) # 获取实际车速状态  
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetHDCFunctionAvailable", {}, {"out": 0}) # 获取HDC开关可用状态
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetHDC", {"on": True}) # 设置陡坡缓降开关为True
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetSuperEnergySaveMode", {}, {"out": False})  # 获取超级节能模式状态反馈
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getESCOffIndicateLightSts", {}, {"out": False}) # 获取ESC Off指示状态
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetBrakeDiscOverHeatSts", {}, {"out": 255}) # 获取制动盘过热状态
                
    @allure.title("获取&通知车辆运动状态_取值遍历")
    @pytest.mark.sanity
    def test_caseid_109533(self): # VehMtnStVehMtnSt|VehicleMotionState 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 4)
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetVehicleMotionState", {}, {"out": {"motionState": 2, "isvalid": True}}, timeout=3)
        last_value=2
        dict1={0:0, 1:1, 2:1, 3:1, 4:2, 5:2, 6:3, 7:3} 
        for key,value in dict1.items():
            self.partner.empty_all(2) 
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', key)
            if last_value!=value:
                self.partner.ck_s2s_event("ChassisService_client", "VehicleMotionState", {"state":{"motionState":value,"isvalid":True}})
            else:
                self.partner.ck_no_event("ChassisService_client", "VehicleMotionState")
            self.partner.send_request_and_ck_resp("ChassisService_client", "GetVehicleMotionState", {}, {"out": {"motionState": value, "isvalid": True}})
            last_value=value
            
    @allure.title("获取&通知车辆运动状态_E2E校验失败")
    @pytest.mark.full
    def test_caseid_110507(self): # fr VehMtnStVehMtnSt|VehicleMotionState|E2E] -UpdateVehicleMotionStateEvent 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 6)
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetVehicleMotionState", {}, {"out": {"motionState": 3, "isvalid": True}})        
        try:
            self.ipdu.set_no_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt') 
            self.partner.ck_s2s_event("ChassisService_client", "VehicleMotionState", {"state":{"motionState":3,"isvalid":False}})
            self.partner.send_request_and_ck_resp("ChassisService_client", "GetVehicleMotionState", {}, {"out": {"motionState": 3, "isvalid": False}})              
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 5)
            self.partner.ck_s2s_event("ChassisService_client", "VehicleMotionState", {"state":{"motionState":2,"isvalid":False}})
            self.partner.send_request_and_ck_resp("ChassisService_client", "GetVehicleMotionState", {}, {"out": {"motionState": 2, "isvalid": False}})
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt') 
            assert False, error
        else:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt') 
        self.partner.ck_s2s_event("ChassisService_client", "VehicleMotionState", {"state":{"motionState":2,"isvalid":True}})
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetVehicleMotionState", {}, {"out": {"motionState": 2, "isvalid": True}})  
            
    @allure.title("获取&通知车辆运动状态_信号丢失")
    @pytest.mark.full
    def test_caseid_110086(self): # VehMtnStVehMtnSt|VehicleMotionState|VehMtnStVehMtnSt_TimeOut
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 2)
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetVehicleMotionState", {}, {"out": {"motionState": 1, "isvalid": True}}, timeout=3)
        self.ipdu.pause_bus_send("backbonefr")
        self.partner.ck_s2s_event("ChassisService_client", "VehicleMotionState", {"state":{"motionState":0,"isvalid":False}}, timeout=1.5)
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetVehicleMotionState", {}, {"out": {"motionState": 0, "isvalid": False}})
        self.ipdu.resume_bus_send("backbonefr")
        self.partner.ck_s2s_event("ChassisService_client", "VehicleMotionState", {"state":{"motionState":1,"isvalid":True}})
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetVehicleMotionState", {}, {"out": {"motionState": 1, "isvalid": True}})
        
    @allure.title("设置ESC运动模式_取值遍历&下行PDU校验")
    @pytest.mark.full
    def test_caseid_110176(self):
        file_path, save_name = self.bgmcli.start_bgm_tcpdump() 
        for i in range(16):
            for j in [True, False]:
                self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetEscSportMode", {"mode": {"id": i, "isOpen": j}})
                self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr14, 'EscSptModReqdByDrvrEscSptModReqdByDrvr', j)   
                self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr14, 'EscSptModReqdByDrvrPen',  i)   
                sleep(2)        
        # 检验TCP报文 # 列表里面为元祖（pdu的id，数据长度，信号起始bit位，信号长度，信号值），可以 是多个元祖
        data_list1 = [(10009, 2, 3, 4, 0),(10009, 2, 3, 4, 15),(10009, 2, 8, 1, 1),(10009, 2, 8, 1, 0)]
        data_list2 = [(10009, 2, 3, 4),(10009, 2, 8, 1)]
        self.ck_pdu(file_path,save_name,data_list1,data_list2)
        
    @allure.title("获取&通知ESC运动模式状态_取值遍历")
    @pytest.mark.sanity
    def test_caseid_110174(self):
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetEscSportMode", {"mode": {"id": random.randint(0,16), "isOpen": False}})
        self.partner.empty_all(2)        
        for i in [True, False]:
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetEscSportMode", {"mode": {"id": 0, "isOpen": i}})
            self.partner.ck_s2s_event("ChassisService_client", "NotifyEscSportModeStatus", {"sts":i})
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetEscSportModeStatus", {}, {"out": i})   
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetEscSportMode", {"mode": {"id": 15, "isOpen": i}}) 
            self.partner.ck_no_event("ChassisService_client", "NotifyEscSportModeStatus")       
            
    @allure.title("获取ESC运动模式状态_下电记忆值")
    @pytest.mark.full
    @pytest.mark.restart 
    def test_caseid_1980471(self):     
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetEscSportMode", {"mode": {"id": 0, "isOpen": True}})
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetEscSportModeStatus", {}, {"out": True})  
        self.restart_bgm_and_connect_service(CHASSIS_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetEscSportModeStatus", {}, {"out": True}, timeout=1)  

    @allure.title("获取&通知实际车速状态_取值遍历")
    @pytest.mark.sanity
    def test_caseid_110758(self): # VehSpdLgtQf|VehSpdLgtA|SpeedChanged
        for signal_Qf in range(4):            
            for signal_A in [256, 1, 7673]:
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', signal_Qf)  #车速值 3=有效         
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', signal_A) #车速值给了0 输入浮点数  /0.00391=信号值 
                isvalid=True if signal_Qf==3 else False
                self.partner.ck_s2s_event("ChassisService_client", "SpeedChanged", {"speed": {"speed": signal_A*0.00391, "isvalid": isvalid}})
                self.partner.send_request_and_ck_resp("ChassisService_client", "GetSpeed", {}, {"out": {"speed": signal_A*0.00391, "isvalid": isvalid}})
                
    @allure.title("获取&通知实际车速状态_E2E校验失败")
    @pytest.mark.full
    def test_caseid_110556(self): # VehSpdLgtQf|VehSpdLgtA|SpeedChanged
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)  #车速值 3=有效         
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 100) #车速值给了0 输入浮点数  /0.00391=信号值
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetSpeed", {}, {"out":{'speed': 0.391, 'isvalid': True}}, timeout=3)
        try:
            self.ipdu.set_no_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf')  
            self.partner.ck_s2s_event("ChassisService_client", "SpeedChanged", {"speed": {"speed": 0.391, "isvalid": 0}})
            self.partner.send_request_and_ck_resp("ChassisService_client", "GetSpeed", {}, {"out": {"speed": 0.391, "isvalid": 0}})
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 200) 
            self.partner.ck_s2s_event("ChassisService_client", "SpeedChanged", {"speed": {"speed": 0.782, "isvalid": 0}})
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf') 
            assert False, error
        else:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf') 
        self.partner.ck_s2s_event("ChassisService_client", "SpeedChanged", {"speed": {"speed": 0.782, "isvalid": 1}})

    @allure.title("获取&通知实际车速状态_信号丢失")
    @pytest.mark.full
    def test_caseid_110696(self): # VehSpdLgtQf|VehSpdLgtA|SpeedChanged
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)  #车速值 3=有效         
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 100) #车速值给了0 输入浮点数  /0.00391=信号值
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetSpeed", {}, {"out": {"speed": 0.391, "isvalid": 1}}, timeout=3)
        self.ipdu.pause_bus_send("backbonefr")
        self.partner.ck_s2s_event("ChassisService_client", "SpeedChanged", {"speed": {"speed": 0.391, "isvalid": 0}}, timeout=1.5)
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetSpeed", {}, {"out": {"speed": 0.391, "isvalid": 0}})
        self.ipdu.resume_bus_send("backbonefr")            
        self.partner.ck_s2s_event("ChassisService_client", "SpeedChanged", {"speed": {"speed": 0.391, "isvalid": 1}})
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetSpeed", {}, {"out": {"speed": 0.391, "isvalid": 1}})
       
    @allure.title("获取&通知左前轮轮速状态_取值遍历")
    @pytest.mark.sanity
    def test_caseid_109984(self):  # fr WhlSpdCircumlFrnt|WheelSpeed  轮速状态超范围值仍会映射
        for signal_Qf in range(4):            
            for signal_A in [1, 31970, 0]:  # 126.0
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlFrntLe', signal_A)
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlFrntLeQf', signal_Qf)
                isvalid=1 if signal_Qf==3 else 0
                self.partner.ck_s2s_event("ChassisService_client", "WheelSpeed", {"wheelsSpeed": [{"wheelId": 1, "speed": signal_A*0.00391, "isvalid": isvalid}]})
                self.partner.send_request_and_ck_resp("ChassisService_client", "GetWheelSpeed", {"wheels": [1]}, 
                                                      {"out": [{"wheelId": 1, "speed": signal_A*0.00391, "isvalid": isvalid}]})
                
    # @allure.title("获取&通知左前轮轮速状态_超范围值")
    # @pytest.mark.full
    # def test_caseid_1980590(self):  # fr WhlSpdCircumlFrnt|WheelSpeed
    #     speed=self.partner.send_request_and_return_resp("ChassisService_client", "GetWheelSpeed", {"wheels": [1]})["out"][0]['speed']
    #     for signal_Qf in range(4):   
    #         self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlFrntLe', 31971)
    #         self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlFrntLeQf', signal_Qf)
    #         isvalid=1 if signal_Qf==3 else 0
    #         self.partner.send_request_and_ck_resp("ChassisService_client", "GetWheelSpeed", {"wheels": [1]}, 
    #                                                   {"out": [{"wheelId": 1, "speed": speed, "isvalid": isvalid}]})
                
    @allure.title("获取&通知右前轮轮速状态_取值遍历")
    @pytest.mark.sanity
    def test_caseid_110648(self):  
        for signal_Qf in range(4):            
            for signal_A in [1, 31970, 0]:  # 125.0
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlFrntRiQf', signal_Qf)
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlFrntWhlSpdCircumlFrntRi', signal_A)
                isvalid=1 if signal_Qf==3 else 0
                self.partner.ck_s2s_event("ChassisService_client", "WheelSpeed", {"wheelsSpeed": [{"wheelId": 2, "speed": signal_A*0.00391, "isvalid": isvalid}]})
                self.partner.send_request_and_ck_resp("ChassisService_client", "GetWheelSpeed", {"wheels": [2]}, 
                                                      {"out": [{"wheelId": 2, "speed": signal_A*0.00391, "isvalid": isvalid}]})
                
    @allure.title("获取&通知左后轮轮速状态_取值遍历")
    @pytest.mark.sanity
    def test_caseid_110423(self):  
        for signal_Qf in range(4):            
            for signal_A in [1, 31970, 0]:  
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlReLe', signal_A)
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlReLeQf', signal_Qf)
                isvalid=1 if signal_Qf==3 else 0
                self.partner.ck_s2s_event("ChassisService_client", "WheelSpeed", {"wheelsSpeed": [{"wheelId": 3, "speed": signal_A*0.00391, "isvalid": isvalid}]})
                self.partner.send_request_and_ck_resp("ChassisService_client", "GetWheelSpeed", {"wheels": [3]}, 
                                                      {"out": [{"wheelId": 3, "speed": signal_A*0.00391, "isvalid": isvalid}]})
                 
    @allure.title("获取&通知右后轮轮速状态_取值遍历")
    @pytest.mark.sanity
    def test_caseid_110577(self): 
        for signal_Qf in range(4):            
            for signal_A in [1, 31970, 0]: 
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlReRiQf', signal_Qf)
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlReRi', signal_A)
                isvalid=1 if signal_Qf==3 else 0
                self.partner.ck_s2s_event("ChassisService_client", "WheelSpeed", {"wheelsSpeed": [{"wheelId": 4, "speed": signal_A*0.00391, "isvalid": isvalid}]})
                self.partner.send_request_and_ck_resp("ChassisService_client", "GetWheelSpeed", {"wheels": [4]}, 
                                                      {"out": [{"wheelId": 4, "speed": signal_A*0.00391, "isvalid": isvalid}]})
                
    @allure.title("获取&通知轮速状态_信号丢失")
    @pytest.mark.full
    def test_caseid_110746(self): # VehSpdLgtQf|VehSpdLgtA|SpeedChanged
        signal_A=100
        dict1={"WhlSpdCircumlFrntLe": "WhlSpdCircumlFrntLeQf", "WhlSpdCircumlFrntWhlSpdCircumlFrntRi": "WhlSpdCircumlFrntRiQf", 
               "WhlSpdCircumlReLe": "WhlSpdCircumlReLeQf", "WhlSpdCircumlReRi": "WhlSpdCircumlReRiQf"}
        for key, value in dict1.items():            
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, key, signal_A) 
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, value, 3)   
        sleep(1) 
        self.ipdu.pause_bus_send("backbonefr")
        self.partner.ck_s2s_event("ChassisService_client", "WheelSpeed", {"wheelsSpeed": [{"wheelId": 4, "speed": signal_A*0.00391, "isvalid": 0}]}, timeout=1.5)
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetWheelSpeed", {"wheels": [1]},
                                                  {"out": [{"wheelId": 1, "speed": signal_A*0.00391, "isvalid": 0}]})
        self.ipdu.resume_bus_send("backbonefr")            
        self.partner.ck_s2s_event("ChassisService_client", "WheelSpeed", {"wheelsSpeed": [{"wheelId": 2, "speed": signal_A*0.00391, "isvalid": 1}]})
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetWheelSpeed", {"wheels": [3]}, 
                                              {"out": [{"wheelId": 3, "speed": signal_A*0.00391, "isvalid": 1}]})
        
    @allure.title("获取&通知轮速状态_前轮E2E校验失败")
    @pytest.mark.full
    def test_caseid_1979643(self): # VehSpdLgtQf|VehSpdLgtA|SpeedChanged
        signal_A=100
        dict1={"WhlSpdCircumlFrntLe": "WhlSpdCircumlFrntLeQf", "WhlSpdCircumlFrntWhlSpdCircumlFrntRi": "WhlSpdCircumlFrntRiQf", 
               "WhlSpdCircumlReLe": "WhlSpdCircumlReLeQf", "WhlSpdCircumlReRi": "WhlSpdCircumlReRiQf"}
        for key, value in dict1.items():            
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, key, signal_A) 
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, value, 3)   
        sleep(1)   
        try:
            self.ipdu.set_no_crc(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlFrntLe')  
            self.partner.ck_s2s_event("ChassisService_client", "WheelSpeed", {"wheelsSpeed": [{"wheelId": 2, "speed": signal_A*0.00391, "isvalid": 0}]})
            self.partner.send_request_and_ck_resp("ChassisService_client", "GetWheelSpeed", {"wheels": [1, 3]},
                                                  {"out": [{"wheelId": 1, "speed": signal_A*0.00391, "isvalid": 0}, 
                                                           {"wheelId": 3, "speed": signal_A*0.00391, "isvalid": 1}]})
            self.partner.empty_all()
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, "WhlSpdCircumlFrntLeQf", 1)  
            self.partner.ck_no_event("ChassisService_client", "WheelSpeed", timeout=3)
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlFrntLe') 
            assert False, error
        else:
            self.ipdu.restore_crc(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlFrntLe') 
        self.partner.ck_s2s_event("ChassisService_client", "WheelSpeed", {"wheelsSpeed": [{"wheelId": 1, "speed": signal_A*0.00391, "isvalid": 0}]})
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetWheelSpeed", {"wheels": [2]}, 
                                              {"out": [{"wheelId": 2, "speed": signal_A*0.00391, "isvalid": 1}]})
        
    @allure.title("获取&通知轮速状态_后轮E2E校验失败")
    @pytest.mark.full
    def test_caseid_1979644(self): # VehSpdLgtQf|VehSpdLgtA|SpeedChanged
        signal_A=400
        dict1={"WhlSpdCircumlFrntLe": "WhlSpdCircumlFrntLeQf", "WhlSpdCircumlFrntWhlSpdCircumlFrntRi": "WhlSpdCircumlFrntRiQf", 
               "WhlSpdCircumlReLe": "WhlSpdCircumlReLeQf", "WhlSpdCircumlReRi": "WhlSpdCircumlReRiQf"}
        for key, value in dict1.items():            
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, key, signal_A) 
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, value, 3)   
        sleep(1)   
        try:
            self.ipdu.set_no_crc(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlReLe') 
            self.partner.ck_s2s_event("ChassisService_client", "WheelSpeed", {"wheelsSpeed": [{"wheelId": 3, "speed": signal_A*0.00391, "isvalid": 0}]})
            self.partner.send_request_and_ck_resp("ChassisService_client", "GetWheelSpeed", {"wheels": [2, 4]},
                                                  {"out": [{"wheelId": 4, "speed": signal_A*0.00391, "isvalid": 0},
                                                           {"wheelId": 2, "speed": signal_A*0.00391, "isvalid": 1}]})
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlReLe') 
            assert False, error
        else:
            self.ipdu.restore_crc(self.ipdu.backbonefr.VddmBackBoneFr40, 'WhlSpdCircumlReLe') 
        self.partner.ck_s2s_event("ChassisService_client", "WheelSpeed", {"wheelsSpeed": [{"wheelId": 4, "speed": signal_A*0.00391, "isvalid": 1}]})
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetWheelSpeed", {"wheels": [3]}, 
                                              {"out": [{"wheelId": 3, "speed": signal_A*0.00391, "isvalid": 1}]})
        
    @allure.title("获取&通知ABS激活状态_取值遍历")
    @pytest.mark.sanity
    def test_caseid_110644(self): # AbsCtrlActvForWhlFrntLe|AbsCtrlActvForWhlFrntRi|AbsCtrlActvForWhlReLe|AbsCtrlActvForWhlReRi|absActStsEvent
        dict1={"AbsCtrlActvForWhlFrntLe": "flActSts", "AbsCtrlActvForWhlFrntRi": "frActSts", 
               "AbsCtrlActvForWhlReLe": "rlActSts", "AbsCtrlActvForWhlReRi": "rrActSts"}
        for key, value in dict1.items():   
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr13, key, 0)     #防止前置case对信号值造成影响
        self.partner.empty_all(2) 
        for key, value in dict1.items():     
            for i in [1, 0]:                                 
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr13, key, i) 
                self.partner.ck_s2s_event("ChassisService_client", "absActSts",{"info": {value: i}})
                self.partner.send_request_and_ck_resp("ChassisService_client", "getABSActInfo", {}, {"out": {value: i}})

    @allure.title("获取ABS激活/失效状态_服务启动默认值")
    @pytest.mark.full
    def test_caseid_110401_109433_1939933_1939941_1980706_1939931_1939948(self): # 获取ABS激活状态, 获取ABS失效状态
        dict1={"AbsCtrlActvForWhlFrntLe": "flActSts", "AbsCtrlActvForWhlFrntRi": "frActSts", 
               "AbsCtrlActvForWhlReLe": "rlActSts", "AbsCtrlActvForWhlReRi": "rrActSts"}
        for key, value in dict1.items():   
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr13, key, 1) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'AbsSts', 1)
        self.partner.send_request_and_ck_resp("ChassisService_client", "getABSFailSts", {}, {"out": True}, timeout=3)   
        self.partner.send_request_and_ck_resp("ChassisService_client", "getABSActInfo", {}, {"out": {"flActSts": True, "frActSts": True, "rlActSts": True, "rrActSts": True}})   
        self.ipdu.set(self.ipdu.propulsioncan.EgsmPropFr01, 'DrvrGearShiftReqInv', 2) # 获取EGSM虚拟挡位请求
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr10, 'PTStsForRace', 2) # 获取驱动系统实际状态反馈
        signals=["WhlSlipRateFL","WhlSlipRateFR","WhlSlipRateRL","WhlSlipRateRR"]   
        self.ipdu.set(self.ipdu.chassiscan1.VddmChas1Fr53, 'StandStillMgrStsForHld1', 5) # 获取车辆静止状态
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr07, 'EPedlModSts', 2) # 获取EPedal单踏板模式功能状态信息 
        sleep(3)
        self.restart_bgm_and_connect_service(CHASSIS_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp("ChassisService_client", "getABSFailSts", {}, {"out": False}, timeout=1)   
        self.partner.send_request_and_ck_resp("ChassisService_client", "getABSActInfo", {}, {"out": {"flActSts": False, "frActSts": False, "rlActSts": False, "rrActSts": False}}, timeout=1)
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetEGSMVirtualShiftReq", {}, {"out": 0}, timeout=1)  # 获取EGSM虚拟挡位请求  
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetPropulsionStatus", {}, {"out": [255]}, timeout=1)  # 获取驱动系统实际状态反馈              
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetTraveledDistance", {}, {"out": -1}, timeout=1) # 获取行驶里程   
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetVehicleStandStillSts", {}, {"out": {"value":255,"validity":0}}, timeout=1) # 获取车辆静止状态
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetEPedlModeInfo", {}, 
                                              {"out": {"mode":255,"inhibitSts":255,"decelerationLimitSts":255}}, timeout=1)  # 获取EPedal单踏板模式功能状态信息

    @allure.title("获取&通知ABS失效状态_取值遍历")
    @pytest.mark.sanity
    def test_caseid_110640(self):   # fr AbsSts|absFailSts
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'AbsSts', 1)
        self.partner.empty_all(2)
        for i in range(2):
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'AbsSts', i)
            self.partner.ck_s2s_event("ChassisService_client", "absFailSts",{"sts": i})
            self.partner.send_request_and_ck_resp("ChassisService_client", "getABSFailSts", {}, {"out": i})    
        
    @allure.title("获取&通知ABS失效状态_信号丢失")
    @pytest.mark.full
    def test_caseid_1979694(self):  
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'AbsSts', 0)
        self.partner.send_request_and_ck_resp("ChassisService_client", "getABSFailSts", {}, {"out": False})   
        self.partner.empty_all(12) # 重启后15s不检测信号丢失 防止前置重启后不到15s
        self.ipdu.pause_bus_send("backbonefr")
        self.partner.ck_s2s_event("ChassisService_client", "absFailSts",{"sts": True}, timeout=2.5)
        self.partner.send_request_and_ck_resp("ChassisService_client", "getABSFailSts", {}, {"out": True})   
        self.ipdu.resume_bus_send("backbonefr")  
        self.partner.ck_s2s_event("ChassisService_client", "absFailSts",{"sts": False})
        self.partner.send_request_and_ck_resp("ChassisService_client", "getABSFailSts", {}, {"out": False})    
        
    @allure.title("获取&通知ESC运行状态_取值遍历")
    @pytest.mark.smoke
    def test_caseid_110659(self): # EscStEscSt|ESCWorkStatusEvent
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 1)
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetESCWorkStatus", {}, {"out": 1}, timeout=3) 
        self.partner.empty_all(1)
        for i in range(8):
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', i)
            if i > 4:
                self.partner.ck_no_event("ChassisService_client", "ESCWorkStatus")
                self.partner.send_request_and_ck_resp("ChassisService_client", "GetESCWorkStatus", {}, {"out": 4}) 
            else:
                self.partner.ck_s2s_event("ChassisService_client", "ESCWorkStatus", {"state": i})
                self.partner.send_request_and_ck_resp("ChassisService_client", "GetESCWorkStatus", {}, {"out": i})    
            
    @allure.title("获取&通知ESC运行状态_E2E校验失败")
    @pytest.mark.full
    def test_caseid_1979627(self): #fr EscStEscSt|ESCWorkStatusEvent| 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 1)
        self.partner.empty_all(3)
        try:
            self.ipdu.set_no_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt')   
            self.partner.ck_s2s_event("ChassisService_client", "ESCWorkStatus", {"state": 2})
            self.partner.send_request_and_ck_resp("ChassisService_client", "GetESCWorkStatus", {}, {"out": 2})  
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 3)
            self.partner.ck_no_event("ChassisService_client", "ESCWorkStatus")
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt')   
            assert False, error
        else:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt')   
        self.partner.ck_s2s_event("ChassisService_client", "ESCWorkStatus", {"state": 3})    
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetESCWorkStatus", {}, {"out": 3})

    @allure.title("获取&通知ESC运行状态_UsgMod遍历_信号丢失")
    @pytest.mark.full
    def test_caseid_1984189(self): # CR_Ver:140AN fr EscStEscSt|VehModMngtGlbSafe1UsgModSts|EscStEscSt_TimeOut|lastUM|UpdateESCWorkStatusEvent
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 0)
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetESCWorkStatus", {}, {"out": 0}, timeout=3)    
        for UsgMod in [13, 11, 2, 1, 0]:
            self.partner.empty_all()
            self.sd_tester.change_usage_mode(UsgMod)  
            value=2 if UsgMod in [2, 11, 13] else 0
            self.ipdu.pause_bus_send("backbonefr")      
            if UsgMod in [13, 11, 2]:         
                self.partner.ck_s2s_event("ChassisService_client", "ESCWorkStatus", {"state": value}, timeout=2.5)
                self.partner.send_request_and_ck_resp("ChassisService_client", "GetESCWorkStatus", {}, {"out": value})  
            else:
                self.partner.ck_no_event("ChassisService_client", "ESCWorkStatus")  
            self.ipdu.resume_bus_send("backbonefr")  
            self.partner.send_request_and_ck_resp("ChassisService_client", "GetESCWorkStatus", {}, {"out": 0}, timeout=3)  

    @allure.title("获取&通知ESC运行状态_UsgMod遍历_ESCWorkStatus=2信号丢失后无重复上报")
    @pytest.mark.full
    def test_caseid_1984190(self): # CR_Ver:140AN
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 2)
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetESCWorkStatus", {}, {"out": 2}, timeout=3)    
        self.partner.empty_all()
        for UsgMod in [13, 11, 2, 1, 0]:
            self.sd_tester.change_usage_mode(UsgMod)  
            self.ipdu.pause_bus_send("backbonefr")  
            sleep(2.2)
            self.partner.ck_no_event("ChassisService_client", "ESCWorkStatus")  
            self.partner.send_request_and_ck_resp("ChassisService_client", "GetESCWorkStatus", {}, {"out": 2})  
            self.ipdu.resume_bus_send("backbonefr")  
            self.partner.ck_no_event("ChassisService_client", "ESCWorkStatus")  
     
    @allure.title("获取&通知HDC开关可用状态_取值遍历")
    @pytest.mark.smoke
    def test_caseid_110718(self): # SwtStsforHillDwnCtrl|HDCFunctionAvailableChanged
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'SwtStsforHillDwnCtrl', 1)
        for i in range(2):
            self.partner.empty_all(1)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'SwtStsforHillDwnCtrl', i)
            self.partner.ck_s2s_event("ChassisService_client", "HDCFunctionAvailableChanged", {"on": i})
            self.partner.send_request_and_ck_resp("ChassisService_client", "GetHDCFunctionAvailable", {}, {"out": i}) 
        
    @allure.title("获取ABS/ESC/制动系统报警指示请求状态_服务启动默认值")
    @pytest.mark.full
    @pytest.mark.restart 
    def test_caseid_1980453_1979630_1979656_1980560_1980569_1980570_1980598(self):  # 获取ABS报警指示请求状态, 获取ESC报警指示请求状态, 获取制动系统报警指示请求状态
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqAbsWarnIndcnReq', 1) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq', 1) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 0) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 2) # 获取ESC运行状态
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr18, 'PrpsnModSptBlkd', 3) # 获取运动模式有效状态  
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr09, 'GearLvrFaultIndcn', 5) # 获取换挡故障状态     
        dict1={"WhlSpdCircumlFrntLe": "WhlSpdCircumlFrntLeQf", "WhlSpdCircumlFrntWhlSpdCircumlFrntRi": "WhlSpdCircumlFrntRiQf", 
               "WhlSpdCircumlReLe": "WhlSpdCircumlReLeQf", "WhlSpdCircumlReRi": "WhlSpdCircumlReRiQf"}
        for key, value in dict1.items(): # 获取轮速状态         
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, key, 3.0) 
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, value, 3)       
        self.ipdu.set(self.ipdu.passivesafetycan.SrsPassSafeCANFr04, 'ADataRawSafeALgt', 16353) # 纵向加速度
        self.ipdu.set(self.ipdu.passivesafetycan.SrsPassSafeCANFr04, 'ADataRawSafeALat', 16353) # 横向加速度
        self.ipdu.set(self.ipdu.passivesafetycan.SrsPassSafeCANFr04, 'ADataRawSafeAVert', 16353) # 垂直加速度
        sleep(3)
        self.restart_bgm_and_connect_service(CHASSIS_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getESCWarnIndicateReqSts", {}, {"out": 3}, timeout=3)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnIndicateReqSts", {}, {"out": 0}, timeout=3)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getABSWarnIndicateReqSts", {}, {"out": 0}, timeout=3)
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetESCWorkStatus", {}, {"out": 1}) # 获取ESC运行状态  
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetSportModeAvailableStatus", {}, {"out": 0}) # 获取运动模式有效状态  
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetGearFault", {}, {"out": [0]})  # 获取换挡故障状态
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetWheelSpeed", {"wheels": [1, 2, 3, 4]}, 
                                                      {"out": [{"wheelId": 1, "speed": 0.0, "isvalid": False},
                                                               {"wheelId": 2, "speed": 0.0, "isvalid": False},
                                                               {"wheelId": 3, "speed": 0.0, "isvalid": False},
                                                               {"wheelId": 4, "speed": 0.0, "isvalid": False}]}) # 获取轮速状态
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetWheelImpluseCounter", {"wheels": [1, 2, 3, 4]},
                                              {"out": [{"wheelId": 1, "wheelImpluseCounter": 0, "isvalid": False},
                                                       {"wheelId": 2, "wheelImpluseCounter": 0, "isvalid": False},
                                                       {"wheelId": 3, "wheelImpluseCounter": 0, "isvalid": False},
                                                       {"wheelId": 4, "wheelImpluseCounter": 0, "isvalid": False}]}) # 获取车轮旋转脉冲计数状态
        # 获取车辆加速度信息 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, 'GetVehicleAcceleration', {}, 
                                              {"out": {"longAcceleration": -140, "lateralAcceleration": -140, "verticalAcceleration": -140}}) # 获取车辆加速度信息 
                    
    @allure.title("获取&通知制动系统报警指示请求状态_UsgMod依次下切_所有信号取值遍历")
    @pytest.mark.full
    def test_caseid_1979792(self):   
        self.sd_tester.change_usage_mode(13)  
        sleep(2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', 0) # len=1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkSysWarnIndcnReq', 0)  # len=1
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'BrkSysWarnIndcnReqSec', 0) # len=1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 0) 
        sleep(3)
        for usgmod in [13,11,2,1,0]:
            self.sd_tester.change_usage_mode(usgmod)  
            sleep(2)
            for i in [1,0]:
                for j in [1,0]:
                    for k in [1,0]:
                        for t in [1,0]:
                            last_value=self.partner.send_request_and_return_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnIndicateReqSts", {})["out"]
                            self.partner.empty_all(1)
                            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', i)
                            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkSysWarnIndcnReq', j)
                            self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'BrkSysWarnIndcnReqSec', k)
                            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', t) 
                            sleep(2)
                            logger.info(f"打印当前循环值: BrkFldLvl={i},BrkSysWarnIndcnReq={j},BrkSysWarnIndcnReqSec={k},BrkAndAbsWarnIndcnReqBrkWarnIndcnReq={t}")
                            value = 0 
                            if t!=0 and (j==0 or k==0):
                                value = 1 
                            if t==0 or i ==1:
                                value = 2 # 红色灯优先级最高，放最后判断
                            if value!=last_value:
                                self.ck_brkSysWarnIndicateReqSts_and_getBrkSysWarnIndicateReqSts(value)
                            else:
                                self.ck_no_event_and_getBrkSysWarnIndicateReqSts(value)
    
    @allure.title("获取&通知制动系统报警指示请求状态_UsgMod切换遍历_2s计时器内维持") 
    @pytest.mark.sanity
    def test_caseid_1979805(self): # fr BrkSysWarnIndcnReq|fr BrkSysWarnIndcnReqSec|fr BrkAndAbsWarnIndcnReqBrkWarnIndcnReq|fr BrkFldLvl|brkSysWarnIndicateReqSts|lastUM
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', 0) # len=1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkSysWarnIndcnReq', 0)  # len=1
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'BrkSysWarnIndcnReqSec', 0) # len=1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 0) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnIndicateReqSts", {}, {"out": 2}, timeout=3)
        self.partner.empty_all()
        for usgmod1 in [0, 1, 2]:
            for usgmod2 in [11, 13]:
                self.partner.empty_all()
                logger.info(f"打印当前循环值： usgmod1={usgmod1},usgmod2={usgmod2}")
                self.sd_tester.change_usage_mode(usgmod1)
                self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "brkSysWarnIndicateReqSts", timeout=3)
                self.sd_tester.change_usage_mode(usgmod2) 
                self.ck_brkSysWarnIndicateReqSts_and_getBrkSysWarnIndicateReqSts(0,timeout=2)
                self.ck_brkSysWarnIndicateReqSts_and_getBrkSysWarnIndicateReqSts(2) 
            
    @allure.title("获取&通知制动系统报警指示请求状态_信号丢失")
    @pytest.mark.full
    def test_caseid_1979806(self): 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', 0) # len=1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkSysWarnIndcnReq', 0)  # len=1
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'BrkSysWarnIndcnReqSec', 0) # len=1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 1) 
        self.partner.empty_all(2)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnIndicateReqSts", {}, {"out": 1}, timeout=3)
        self.ipdu.pause_bus_send("backbonefr") 
        self.ck_brkSysWarnIndicateReqSts_and_getBrkSysWarnIndicateReqSts(2)   
        self.ipdu.resume_bus_send("backbonefr")
        self.ck_brkSysWarnIndicateReqSts_and_getBrkSysWarnIndicateReqSts(1)   
        
    @allure.title("获取&通知制动系统报警指示请求状态_EpbLampReq信号E2E校验失败")
    @pytest.mark.full
    def test_caseid_1979807(self): # fr BrkSysWarnIndcnReq|fr BrkSysWarnIndcnReqSec|fr BrkAndAbsWarnIndcnReqBrkWarnIndcnReq|fr BrkFldLvl|brkSysWarnIndicateReqSts|wti current mode|reqE2EError
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkSysWarnIndcnReq', 1)
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'BrkSysWarnIndcnReqSec', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 1) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnIndicateReqSts", {}, {"out": 0}, timeout=3)
        self.partner.empty_all()
        try:
            self.ipdu.set_no_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq')
            self.ck_brkSysWarnIndicateReqSts_and_getBrkSysWarnIndicateReqSts(1)  
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', 1)
            self.ck_brkSysWarnIndicateReqSts_and_getBrkSysWarnIndicateReqSts(2)       
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq')
            assert False, error
        else:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq')
        self.ck_no_event_and_getBrkSysWarnIndicateReqSts(2) 

    @allure.title("获取&通知制动系统报警指示请求状态_EpbLampReqSec信号E2E校验失败") 
    @pytest.mark.full
    def test_caseid_1979808(self): # fr BrkSysWarnIndcnReq|fr BrkSysWarnIndcnReqSec|fr BrkAndAbsWarnIndcnReqBrkWarnIndcnReq|fr BrkFldLvl|brkSysWarnIndicateReqSts|lastUM|reqSecE2EError|lastMod
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkSysWarnIndcnReq', 1)
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'BrkSysWarnIndcnReqSec', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 1) 
        sleep(2)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnIndicateReqSts", {}, {"out": 0}, timeout=3)
        self.partner.empty_all()
        try:
            self.ipdu.set_no_crc(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq')
            sleep(2)
            self.ck_brkSysWarnIndicateReqSts_and_getBrkSysWarnIndicateReqSts(1)   
            self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'BrkSysWarnIndcnReqSec', 1)
            self.ck_no_event_and_getBrkSysWarnIndicateReqSts(1)  
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq')
            assert False, error
        else:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq')
        self.ck_no_event_and_getBrkSysWarnIndicateReqSts(1) 
        
    @allure.title("获取&通知制动系统报警指示请求状态_UsgMod从0/1/2切至11/13_2s内下切")
    @pytest.mark.full
    def test_caseid_1979928(self): # fr BrkSysWarnIndcnReq|fr BrkSysWarnIndcnReqSec|fr BrkAndAbsWarnIndcnReqBrkWarnIndcnReq|fr BrkFldLvl|brkSysWarnIndicateReqSts|wti current mode|lastUM
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 0) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnIndicateReqSts", {}, {"out": 2}, timeout=3)
        self.partner.empty_all(2)
        for usgmod1 in [0, 1, 2]:
            for usgmod2 in [11, 13]:
                logger.info(f"打印当前循环值： usgmod1={usgmod1},usgmod2={usgmod2}")
                self.sd_tester.change_usage_mode(usgmod1)
                self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "brkSysWarnIndicateReqSts", timeout=3)
                self.sd_tester.change_usage_mode(usgmod2) 
                self.sd_tester.change_usage_mode(usgmod1)
                self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "brkSysWarnIndicateReqSts",{"sts": 0})
                self.ck_brkSysWarnIndicateReqSts_and_getBrkSysWarnIndicateReqSts(2, timeout=2)   

    @allure.title("获取&通知触摸换挡器激活状态_信号取值遍历")
    @pytest.mark.sanity
    def test_caseid_1983629(self):   # can GearLvrIllmnSts|TouchShiftActiveSts
        self.ipdu.set(self.ipdu.propulsioncan.EgsmPropFr01, 'GearLvrIllmnSts', 0) 
        sleep(1)
        for i in [1, 0]:
            self.ipdu.set(self.ipdu.propulsioncan.EgsmPropFr01, 'GearLvrIllmnSts', i) 
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "TouchShiftActiveSts",{"sts": i})
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetTouchShiftActiveSts", {}, {"out": i})
        
    @allure.title("设置AVH开关_avhEnableCmd=0_启动后调用avhEnableCmd=1")
    @pytest.mark.full
    def test_caseid_1985923(self):  # 2.0 final
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetAVHEnable", {"avhEnableCmd": 1})
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(2)
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetAVHEnable", {"avhEnableCmd": 0})
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr12, 'AutoHldSoftSwtCtrlSt', 0)             
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array("AutoHldSoftSwtCtrlStETH", [1, 0])
        self.bgm_eth_inter.ck_period_time("AutoHldSoftSwtCtrlStETH", 0.04, 1)
        self.restart_bgm_and_connect_service(CHASSIS_SERVICE_CLIENT) # 重启后记忆
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr12, 'AutoHldSoftSwtCtrlSt', 0)   
        self.bgm_eth_inter.start_bgm_tcpdump() # 重启后未调用，校验是否下发以太网报文
        sleep(2)
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetAVHEnable", {"avhEnableCmd": 1})
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr12, 'AutoHldSoftSwtCtrlSt', 1)  
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetAVHEnable", {"avhEnableCmd": 2})
        sleep(0.5)
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr12, 'AutoHldSoftSwtCtrlSt', 1)  
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array("AutoHldSoftSwtCtrlStETH", [0, 1])
        
    @allure.title("设置AVH开关_出厂默认值")
    @pytest.mark.full
    def test_caseid_1985936(self):  # 2.0 final
        self.del_s2s_db()  # 删除数据库
        sleep(2)
        self.restart_bgm_and_connect_service(CHASSIS_SERVICE_CLIENT) 
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr12, 'AutoHldSoftSwtCtrlSt', 0)          
             
    @allure.title("设置AVH开关_avhEnableCmd=1_启动后调用avhEnableCmd=0")
    @pytest.mark.full
    def test_caseid_1985930(self):  # 2.0 final
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetAVHEnable", {"avhEnableCmd": 0})
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(2)
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetAVHEnable", {"avhEnableCmd": 1})
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr12, 'AutoHldSoftSwtCtrlSt', 1)             
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array("AutoHldSoftSwtCtrlStETH", [0, 1])
        # self.bgm_eth_inter.ck_period_time("AutoHldSoftSwtCtrlStETH", 0.04, deviation=1)
        self.restart_bgm_and_connect_service(CHASSIS_SERVICE_CLIENT) # 重启后记忆
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr12, 'AutoHldSoftSwtCtrlSt', 1)   
        self.bgm_eth_inter.start_bgm_tcpdump() # 重启后未调用，校验是否下发以太网报文
        sleep(2)
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetAVHEnable", {"avhEnableCmd": 0}, timeout=1.5)
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr12, 'AutoHldSoftSwtCtrlSt', 0)  
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetAVHEnable", {"avhEnableCmd": 2})
        sleep(0.5)
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr12, 'AutoHldSoftSwtCtrlSt', 0) 
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array("AutoHldSoftSwtCtrlStETH", [1, 0])
        
    @allure.title("获取&通知AVH功能使能状态_参数enableSts取值遍历")
    @pytest.mark.sanity
    def test_caseid_1985942(self):     
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr07, 'EPedlModSts', 3)
        self.partner.empty_all(2) 
        last_value=0 
        for cmd in [1, 0]:
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetAVHEnable", {"avhEnableCmd": cmd})
            for i in [0, 3, 7]:
                self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr07, 'EPedlModSts', i) 
                value = 1 if cmd == 1 and i != 3 else 0                
                # self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetAVHEnable", {"avhEnableCmd": 2})
                if last_value != value:
                    self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "AVHStatus", 
                                                   {"sts": {"enableSts": value, "workStsValidity": 0}})
                    last_value=value
                else:
                    self.partner.ck_no_event_and_ck_resp(CHASSIS_SERVICE_CLIENT, "AVHStatus", 
                                                         {"out": {"enableSts":value, "workStsValidity": 0}})
   
    @allure.title("获取&通知AVH功能使能状态_参数workSts取值遍历")
    @pytest.mark.sanity
    def test_caseid_1985939(self):     
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'LampReqByVehHld', 1)
        self.partner.empty_all(2) 
        last_value=1     
        for i in range(4):         
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'LampReqByVehHld', i)
            value = 1 if i == 1 else 0           
            if last_value != value:
                self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "AVHStatus", 
                                               {"sts": {"workSts": bool(value), "workStsValidity": 0}})
                last_value=value
            else:
                self.partner.ck_no_event_and_ck_resp(CHASSIS_SERVICE_CLIENT, "AVHStatus", 
                                                     {"out": {"workSts": bool(value), "workStsValidity": 0}})
      
    @allure.title("获取&通知AVH功能使能状态_LampReqByVehHld信号丢失_重启后未收到backbonefr总线信号_EPedlModSts=3")
    @pytest.mark.full
    def test_caseid_1985943(self):  
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr07, 'EPedlModSts', 3) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'LampReqByVehHld', 1)
        self.partner.empty_all(2)  
        self.ipdu.pause_bus_send("backbonefr") # 重启后，不会有LampReqByVehHld 和 AutoHldSoftSwtCtrlSt
        self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "AVHStatus", 
                                       {"sts": {"enableSts": 0, "workSts": True, "workStsValidity": 4}}, timeout=1.5)  
        self.restart_bgm_and_connect_service(CHASSIS_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetEPedlModeInfo", {}, 
                                              {"out": {"mode":2}})  # 获取EPedal单踏板模式功能状态信息
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetAVHStatus",{}, 
                                              {"out":  {"enableSts": 255, "workSts": False, "workStsValidity": 10}}, timeout=3)  
        self.ipdu.resume_all_bus_send()  
        self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "AVHStatus", 
                                       {"sts": {"enableSts": 0, "workSts": True, "workStsValidity": 0}})
       
    @allure.title("获取&通知AVH功能使能状态_LampReqByVehHld信号丢失_重启后未收到backbonefr总线信号_EPedlModSts=0")
    @pytest.mark.full
    def test_caseid_1986267(self): 
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetAVHEnable", {"avhEnableCmd": 1})    
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr07, 'EPedlModSts', 0) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'LampReqByVehHld', 1)
        self.partner.empty_all(2)  
        self.ipdu.pause_bus_send("backbonefr") # 重启后，不会有LampReqByVehHld 和 AutoHldSoftSwtCtrlSt
        self.partner.empty_all(3)
        self.restart_bgm_and_connect_service(CHASSIS_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetAVHStatus",{}, 
                                              {"out":  {"enableSts": 255, "workSts": False, "workStsValidity": 10}}, timeout=3)  
        self.ipdu.resume_all_bus_send()  
        self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "AVHStatus", 
                                       {"sts": {"enableSts": 1, "workSts": True, "workStsValidity": 0}})     
                
    @allure.title("获取&通知AVH功能使能状态_EPedlModSts信号丢失_重启后未收到chassiscan2总线信号")
    @pytest.mark.full
    def test_caseid_1985944(self):     
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetAVHEnable", {"avhEnableCmd": 1})
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr07, 'EPedlModSts', 3) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'LampReqByVehHld', 0)
        sleep(2)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetAVHStatus",{}, 
                                              {"out":  {"enableSts": 0, "workSts": False, "workStsValidity": 0}}, timeout=3)
        self.partner.empty_all()  
        self.ipdu.pause_bus_send("chassiscan2")
        sleep(2)
        self.partner.ck_no_event_and_ck_resp(CHASSIS_SERVICE_CLIENT, "AVHStatus", 
                                             {"out": {"enableSts": 0, "workSts": False, "workStsValidity": 0}}, timeout=3)
        self.restart_bgm_and_connect_service(CHASSIS_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetAVHStatus",{}, 
                                              {"out":  {"enableSts": 1, "workSts": False, "workStsValidity": 0}}, timeout=3)
        self.ipdu.resume_all_bus_send()  
        self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "AVHStatus", 
                                       {"sts": {"enableSts": 0, "workSts": False, "workStsValidity": 0}})         
                
    @allure.title("获取&通知AVH功能使能状态_服务启动默认值")
    @pytest.mark.full    
    def test_caseid_1985945(self):     
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetAVHEnable", {"avhEnableCmd": 1}, timeout=1.5)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr07, 'EPedlModSts', 3) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'LampReqByVehHld', 1)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetAVHStatus",{}, 
                                              {"out":  {"enableSts": 0, "workSts": True, "workStsValidity": 0}}, timeout=3)
        self.partner.empty_all(2)  
        self.restart_bgm_and_connect_service(CHASSIS_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetAVHStatus",{}, 
                                              {"out":  {"enableSts": 255, "workSts": False, "workStsValidity": 10}})
        self.ipdu.resume_all_bus_send()   
        self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "AVHStatus", 
                                       {"sts": {"enableSts": 0, "workSts": True, "workStsValidity": 0}})
        
    @allure.title("获取&通知悬架故障状态_Mars1_信号取值遍历") 
    @pytest.mark.sanity
    def test_caseid_1980719(self): # NotifyConfigList|can SuspFailrSts|SuspensionFailureSts 
        self.reset_JiduVehicle(value=1, sleeptime=5)
        last_res=self.partner.send_request_and_return_resp("ChassisService_client", "GetSuspensionFailureSts", {})["out"]
        last_value, last_validity=last_res["value"], last_res["validity"]
        self.partner.empty_all()
        qf_dict1={0:8, 1:6, 2:2, 3:0}
        for qf,validity in qf_dict1.items():
            for sts in range(8):                
                self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsTypQf', qf)
                self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsSuspFailrSts', sts)
                value=1 if sts==3 or sts==4 else 0   
                # logger.info(f"打印当前返回值： last_value={last_value}， last_validity={last_validity}，value={value} ，sts={sts}，qf={qf}，validity={validity}")             
                if last_value!=value or last_validity!=validity:                    
                    self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "SuspensionFailureSts", {"sts": {"value": value, "validity": validity}})
                else:
                    self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "SuspensionFailureSts")
                self.partner.send_request_and_ck_resp("ChassisService_client", "GetSuspensionFailureSts", {}, {"out": {"value": value, "validity": validity}}, timeout=3)
                last_value, last_validity=value, validity
                sleep(2)

    @allure.title("获取&通知悬架故障状态_Mars1_信号丢失")
    @pytest.mark.full
    def test_caseid_1980720(self): 
        self.reset_JiduVehicle(value=1, sleeptime=15) # kCCPJiduVehicleType=1
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsTypQf', 3)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsSuspFailrSts', 0)
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetSuspensionFailureSts", {}, {"out": {"value": 0, "validity": 0}}, timeout=3)
        self.partner.empty_all()
        qf_dict1={0:8, 1:6, 2:2, 3:0}
        for qf,validity in qf_dict1.items():
            self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsTypQf', qf)
            self.partner.send_request_and_ck_resp("ChassisService_client", "GetSuspensionFailureSts", {}, {"out": {"value": 0, "validity": validity}}, timeout=3)
            self.partner.empty_all()
            self.ipdu.pause_bus_send("chassiscan2")
            if qf in range(2):
                self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "SuspensionFailureSts", timeout=3)
            else:
                self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "SuspensionFailureSts", {"sts": {"value": 0, "validity": 4}}) 
            self.ipdu.resume_bus_send("chassiscan2")
            self.partner.send_request_and_ck_resp("ChassisService_client", "GetSuspensionFailureSts", {}, {"out": {"value": 0, "validity": validity}}, timeout=3)              
              
    @allure.title("获取&通知悬架故障状态_Venus_信号取值遍历")
    @pytest.mark.sanity
    def test_caseid_1980722(self): # can SuspFailrSts3|SuspensionFailureSts 
        self.reset_JiduVehicle(value=2, sleeptime=5) # kCCPJiduVehicleType=2 为Venus
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrSts3', 1)
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetSuspensionFailureSts", {}, {"out": {"value": 2, "validity": 0}}, timeout=3) 
        last_value=1
        dict1={0:0, 1:2, 2:3, 3:3}
        for key,value in dict1.items():
            self.partner.empty_all()
            self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrSts3', key)
            if last_value!=value:
                self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "SuspensionFailureSts", {"sts": {"value": value, "validity": 0}}) 
            else:
                self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "SuspensionFailureSts", timeout=3)
            self.partner.send_request_and_ck_resp("ChassisService_client", "GetSuspensionFailureSts", {}, {"out": {"value": value, "validity": 0}}, timeout=3) 
            last_value=value

    @allure.title("获取&通知悬架故障状态_Venus_信号丢失")
    @pytest.mark.full
    def test_caseid_1980723(self):  
        self.reset_JiduVehicle(value=2, sleeptime=15) # kCCPJiduVehicleType=2 为Venus 启动15s不检测信号丢失
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrSts3', 1)      
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetSuspensionFailureSts", {}, {"out": {"value": 2, "validity": 0}}, timeout=3)
        self.partner.empty_all()
        self.ipdu.pause_bus_send("chassiscan2")  
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "SuspensionFailureSts", {"sts": {"value": 2, "validity": 4}}) 
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetSuspensionFailureSts", {}, {"out": {"value": 2, "validity": 4}})  
        self.ipdu.resume_bus_send("chassiscan2")
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "SuspensionFailureSts", {"sts": {"value": 2, "validity": 0}}) 
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetSuspensionFailureSts", {}, {"out": {"value": 2, "validity": 0}})        
           
    @allure.title("获取悬架故障状态_Mars_服务启动默认值")
    @pytest.mark.full
    def test_caseid_1980721(self):   
        self.reset_JiduVehicle(value=1, sleeptime=5)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrSts3', 1) 
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsTypQf', 0)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsSuspFailrSts', 3)
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetSuspensionFailureSts", {}, {"out": {"value": 1, "validity": 8}}, timeout=3)     
        self.restart_bgm_and_connect_service(CHASSIS_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetSuspensionFailureSts", {}, {"out": {"value": 255, "validity": 0}}, timeout=3)  
         
    @allure.title("获取悬架故障状态_Venus_服务启动默认值")
    @pytest.mark.full
    def test_caseid_1980936(self): 
        self.reset_JiduVehicle(value=2, sleeptime=10) # kCCPJiduVehicleType=2 为Venus
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrSts3', 1)        
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsTypQf', 0)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsSuspFailrSts', 3)
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetSuspensionFailureSts", {}, {"out": {"value": 2, "validity": 0}}, timeout=3)     
        self.restart_bgm_and_connect_service(CHASSIS_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetSuspensionFailureSts", {}, {"out": {"value": 255, "validity": 0}}, timeout=3)  
                
    @allure.title("获取悬架故障状态_其他车型_服务启动默认值")
    @allure.title("获取&通知悬架故障状态_其他车型")
    @pytest.mark.full
    def test_caseid_1980937_1980724(self): 
        self.reset_JiduVehicle(value=3, sleeptime=5)
        self.restart_bgm_and_connect_service(CHASSIS_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetSuspensionFailureSts", {}, {"out": {"value": 255, "validity": 0}}, timeout=3)  
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrSts3', 1)        
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsTypQf', 0)
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsSuspFailrSts', 3)
        sleep(3)
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetSuspensionFailureSts", {}, {"out": {"value": 255, "validity": 0}})  

    @allure.title("紧急制动系统状态_信号取值遍历")
    @pytest.mark.sanity
    def test_caseid_1984699(self):  
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EmgyBrkLiReqEmgyBrk', 2)
        self.partner.empty_all(2)
        for i in range(4):
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EmgyBrkLiReqEmgyBrk', i)            
            if i<3:
                self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "EmergencySystemState", {'sts':{"activeSts":i,"validity":0}})
            else:
                self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "EmergencySystemState", {'sts':{"activeSts":2,"validity":1}})

    @allure.title("紧急制动系统状态_启动场景默认值&event")
    @pytest.mark.full
    def test_caseid_1984701(self):  
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EmgyBrkLiReqEmgyBrk', 3)
        sleep(2)
        self.restart_bgm_and_connect_service(CHASSIS_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetEmergencySystemState", {}, {"out": {"activeSts":255,"validity":0}})  
        self.ipdu.resume_all_bus_send()   
        self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "EmergencySystemState", {'sts':{"activeSts":255,"validity":1}})  

    @allure.title("设置漂移模式_参数取值遍历&下行以太网校验")
    @pytest.mark.smoke
    def test_caseid_1989029(self): #  SetDriftMode|PDU30031: |modeCmd overflow: 
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        for mode in [0, 1, 1, 2]:           
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetDriftMode", {"modeCmd": {"modeCmd": mode}})
            self.ipdu.check(self.ipdu.chassiscan1.BgmChas1Fr08, 'DriftModReq', mode, timeout=0.5)
            sleep(1)
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetDriftMode", {"modeCmd": {"modeCmd": 255}})
        self.ipdu.check(self.ipdu.chassiscan1.BgmChas1Fr08, 'DriftModReq', 2, timeout=0.5)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("DriftModReq", [0, 0, 0, 
                                                            1, 1, 1, 1, 1, 1,
                                                            2, 2, 2])
        self.bgm_eth_inter.ck_period_time("DriftModReq", 0.1, permit_fail_times=4)

    @allure.title("设置漂移模式_打断逻辑")
    @pytest.mark.full
    def test_caseid_1989030(self):   
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)       
        for mode in [0, 2, 1]:     
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetDriftMode", {"modeCmd": {"modeCmd": 1}})
            sleep(0.12)
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetDriftMode", {"modeCmd": {"modeCmd": mode}})
            self.ipdu.check(self.ipdu.chassiscan1.BgmChas1Fr08, 'DriftModReq', mode, timeout=0.5)
            sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        result = self.bgm_eth_inter.get_signal_values("DriftModReq")
        assert len(result) > 9 and len(result) < 15,  "打断逻辑有误"
        
    @allure.title("获取&通知漂移模式状态_取值遍历")
    @pytest.mark.sanity
    def test_caseid_1989031(self):   
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr27, 'DriftModAct', 1) 
        last_value=1
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetDriftModeSts", {}, {"out": {"modeSts": 1}}) 
        self.partner.empty_all()
        for mode in [0, 1, 3, 2, 3]:
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr27, 'DriftModAct', mode) 
            value = mode if mode <= 2 else last_value
            if value == last_value:
                self.partner.ck_no_event_and_ck_resp(CHASSIS_SERVICE_CLIENT, "DriftModeSts", {"modeSts": {"modeSts": value}}) 
            else:
                self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "DriftModeSts", {"modeSts": {"modeSts": value}})    
            last_value = value

    @allure.title("设置蠕行车速_接口返回校验&参数取值遍历&下行以太网校验")
    @pytest.mark.smoke
    def test_caseid_1989033(self):  # SetCreepSpeedConfig|PDU30034: |SetResponse 
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        for creepSpeed in range(8):   
            self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "SetCreepSpeedConfig", {"configCmd": {"creepSpeedCmd": creepSpeed}}, {"out": 0}) 
            self.ipdu.check(self.ipdu.chassiscan1.BgmChas1Fr08, 'CrpVehSpdSet', creepSpeed, timeout=0.5)
            sleep(1)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "SetCreepSpeedConfig", {"configCmd": {"creepSpeedCmd": random.choice([8, 255])}}, {"out": 1}) 
        self.ipdu.check(self.ipdu.chassiscan1.BgmChas1Fr08, 'CrpVehSpdSet', 7, timeout=0.5)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        valuelist = [i for i in range(8) for _ in range(3)]
        self.bgm_eth_inter.ck_signal_values("CrpVehSpdSet", valuelist)
        self.bgm_eth_inter.ck_period_time("CrpVehSpdSet", 0.1, permit_fail_times=7)
        
    @allure.title("设置蠕行车速_打断逻辑")
    @pytest.mark.full
    def test_caseid_1989034(self):   
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)       
        for creepSpeed in [0, 7, 4]:     
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetCreepSpeedConfig", {"configCmd": {"creepSpeedCmd": 4}})
            sleep(0.12)
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetCreepSpeedConfig", {"configCmd": {"creepSpeedCmd": creepSpeed}})
            self.ipdu.check(self.ipdu.chassiscan1.BgmChas1Fr08, 'CrpVehSpdSet', creepSpeed, timeout=0.5)
            sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        result = self.bgm_eth_inter.get_signal_values("CrpVehSpdSet")
        assert len(result) > 9 and len(result) < 15,  "打断逻辑有误"

    @allure.title("获取&通知蠕行车速信息_取值遍历")
    @pytest.mark.sanity
    def test_caseid_1989035(self):   
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr27, 'CrpVehSpdAct', 3)  
        last_value=3
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetCreepSpeedInfo", {}, {"out": {"creepSpeedValue": 3, "validity":0}})    
        self.partner.empty_all()
        for creepSpeed in list(range(8))+[8, 15]:
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr27, 'CrpVehSpdAct', creepSpeed)  
            value = creepSpeed if creepSpeed < 8 else last_value
            if value == last_value:
                self.partner.ck_no_event_and_ck_resp(CHASSIS_SERVICE_CLIENT, "CreepSpeedInfo", {"creepSpeedInfo": {"creepSpeedValue": value, "validity":0}}) 
            else:
                self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "CreepSpeedInfo", {"creepSpeedInfo": {"creepSpeedValue": value, "validity":0}})    
            last_value = value
            
    @allure.title("获取&通知蠕行车速信息_信号丢失")
    @pytest.mark.full
    def test_caseid_1989036(self):   
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr27, 'CrpVehSpdAct', 3)  
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetCreepSpeedInfo", {}, {"out": {"creepSpeedValue": 3, "validity":0}})    
        self.partner.empty_all()            
        self.ipdu.pause_bus_send("chassiscan1")   
        self.partner.ck_coming_event_and_resp(CHASSIS_SERVICE_CLIENT, "CreepSpeedInfo", {"creepSpeedInfo": {"creepSpeedValue": 3, "validity":4}}, timeout=2.5)    
        self.ipdu.resume_bus_send("chassiscan1") 
        self.partner.ck_coming_event_and_resp(CHASSIS_SERVICE_CLIENT, "CreepSpeedInfo", {"creepSpeedInfo": {"creepSpeedValue": 3, "validity":0}}, timeout=2.5)           
            
    @allure.title("获取&通知漂移模式状态/蠕行车速信息_重启默认值")
    @pytest.mark.full
    def test_caseid_1989032_1989040(self):   
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr27, 'DriftModAct', 1)      
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr27, 'CrpVehSpdAct', 3)    
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetDriftModeSts", {}, {"out": {"modeSts": 1}})  
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetCreepSpeedInfo", {}, {"out": {"creepSpeedValue": 3, "validity":0}})    
        self.restart_bgm_and_connect_service(CHASSIS_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetDriftModeSts", {}, {"out": {"modeSts": 255}})     
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetCreepSpeedInfo", {}, {"out": {"creepSpeedValue": 255, "validity":1}})    
        self.ipdu.resume_all_bus_send() 
        self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "DriftModeSts", {"modeSts": {"modeSts": 1}}) # 漂移模式  
        self.partner.ck_event_and_resp(CHASSIS_SERVICE_CLIENT, "CreepSpeedInfo", {"creepSpeedInfo": {"creepSpeedValue": 3, "validity":0}}) # 蠕行车速                  

    @allure.title("启动场景event_Chassis[1-39]")
    @pytest.mark.full
    @pytest.mark.restart
    def test_caseid_1984254(self): 
        self.chassis_fault_default() # 通知当前chassis模块故障列表 VehSpdLgtQf|WhlSpdCircuml
        self.ipdu.set(self.ipdu.adcanfd.AcuADCANFDFr06, 'DrvModSetFbk', 0) # 通知超级节能模式状态反馈 DrvModSetFbk！=9
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'DrvModEscOffDrvModEscOff', 0) # ESC Off指示状态
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 1) # ESC Off指示状态
        self.set_DisplayReqSts() # EPB显示请求状态
        self.partner.send_request_and_ck_resp("ChassisService_client", "getDisplayReqSts", {}, 
                                              {"out": {"highPriSts": 0, "lowPriSts": 0}})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0) # EPB警示音请求状态
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 1) # 通知制动系统报警指示请求状态
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqAbsWarnIndcnReq', 3)  # 通知ABS报警指示请求状态, 通知制动系统报警指示请求状态
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'EscWarnIndcnReqEscWarnIndcnReq', 3) # 通知ESC报警指示请求状态
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', 0) # 通知制动系统报警指示请求状态，制动液位报警提示信息状态
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkSysWarnIndcnReq', 1) # 通知制动系统报警指示请求状态
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'BrkSysWarnIndcnReqSec', 1) # 通知制动系统报警指示请求状态
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrSts3', 0) # 悬架故障状态
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsTypQf', 3) # 悬架故障状态
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr05, 'SuspFailrStsSuspFailrSts', 0) # 悬架故障状态
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkMsgWarnReq', 0) # 制动系统报警信息显示请求状态
        dict1={"AbsCtrlActvForWhlFrntLe": "flActSts", "AbsCtrlActvForWhlFrntRi": "frActSts", 
               "AbsCtrlActvForWhlReLe": "rlActSts", "AbsCtrlActvForWhlReRi": "rrActSts"}
        for key, value in dict1.items():   
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr13, key, 0) # ABS激活状态
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'AbsSts', 0) # ABS失效状态
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq',1) # EPB指示灯请求状态
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq',1) # EPB指示灯请求状态
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkRelsWarnReq', 0) # 驻车系统故障状态
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'MsgReqByHillDwnCtrl', 0) # HDC功能运行状态
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'LampReqByVehHld', 2) # AVH功能激活状态 0/2/3
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'DispMsgByVehHld', 1) # AVH功能显示请求状态
        self.sd_tester.write_single_ccp(950, 1)  # Mars
        self.partner.empty_all(3) # BrkSysWarnIndcnReq|BrkFldLvl|BrkAndAbsWarnIndcnReqBrkWarnIndcnReq|BrkSysWarnIndcnReqSec
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetChassisFault", {}, {"out": [0]}) # 当前chassis模块故障列表
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetSuperEnergySaveMode", {}, {"out": False})  # 超级节能模式状态反馈
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnIndicateReqSts", {}, {"out": 0}) # 制动系统报警指示请求状态
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getABSWarnIndicateReqSts", {}, {"out": 0}) # ABS报警指示请求状态
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getESCWarnIndicateReqSts", {}, {"out": 3})  # ESC报警指示请求状态
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetBrkFldLvlWarnMsgStatus", {}, {"out": 0}) # 制动液位报警提示信息状态
        self.partner.send_request_and_ck_resp("ChassisService_client", "getBrkSysWarnMsgDisReqSts", {},{"out": 0}) # 制动系统报警信息显示请求状态
        self.partner.send_request_and_ck_resp("ChassisService_client", "getABSActInfo", {}, 
                                              {"out": {"flActSts":False,"frActSts":False,"rlActSts":False,"rrActSts":False}}) # ABS激活状态
        self.partner.send_request_and_ck_resp("ChassisService_client", "getABSFailSts", {}, {"out": 0}) # ABS失效状态   
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{},{"out":{"value":0,"validity":0}}) # EPB指示灯请求状态
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkRelsWarnReqSts",{}, {"out": False}) # 驻车系统故障状态
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetAutoHoldWorkState", {},{"out": False}) # AVH功能激活状态
        self.partner.send_request_and_ck_resp("ChassisService_client", "getAvhDisplayReqSts", {}, {"out": 1}) # AVH功能显示请求状态
        self.restart_bgm_and_connect_service(CHASSIS_SERVICE_CLIENT)
        
        # 通知当前chassis模块故障列表
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "ChassisFault", {"faults": [0]}) 
        # 通知超级节能模式状态反馈
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "SuperEnergySaveMode", {"mode": False}) 
        # ESC Off指示状态 
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "escOffIndicateLightSts", {"sts": False})
        # 通知EPB显示请求状态 
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "epbDisplayReqSts", {"sts": {"highPriSts": 0, "lowPriSts": 0}})
        # 通知EPB警示音请求状态 
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,"epbWarnChimeReqSts",{"sts":0})
        # 通知悬架故障状态
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "SuspensionFailureSts", {"sts": {"value": 0, "validity": 0}}) 
        # 通知制动液位报警提示信息状态 
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "NotifyBrkFldLvlWarnMsgStatus", {"msg": 0})
        # 通知制动系统报警信息显示请求状态 
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "brkSysWarnMsgDisplayReqSts",{"sts": 0})  
        # 通知ABS激活状态 
        self.partner.ck_s2s_event("ChassisService_client", "absActSts",
                                  {"info": {"flActSts":False,"frActSts":False,"rlActSts":False,"rrActSts":False}})
        # 通知ABS失效状态 
        self.partner.ck_s2s_event("ChassisService_client", "absFailSts",{"sts": 0})
        # 通知EPB指示灯请求状态 
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,'epbIndicatorLightReqStsValidity',{'sts':{"value":0,"validity":0}})
        # 通知驻车系统故障状态 
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "brkRelsWarnReqSts", {"sts": False})
        # 通知HDC功能运行状态 
        self.partner.ck_s2s_event("ChassisService_client", "hdcWorkSts", {"sts": 0})
        # 通知AVH功能激活状态 
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "AutoHoldWorkState", {"sts": False})
        # 通知AVH功能显示请求状态 
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "avhDisplayReqSts",  {"sts": 1})   
        # # 通知ABS报警指示请求状态 Failed
        # self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "absWarnIndicateReqSts",{"sts": 0})
        # # 通知ESC报警指示请求状态 Failed
        # self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "escWarnIndicateReqSts",{"sts": 3})
        # # 通知制动系统报警指示请求状态 Failed
        # self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "brkSysWarnIndicateReqSts", {"sts": 0})
        # 偏差接受
        self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "absWarnIndicateReqSts")
        self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "escWarnIndicateReqSts")
        self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "brkSysWarnIndicateReqSts")

    @allure.title("启动场景event_Chassis[40-109]")
    @pytest.mark.full
    @pytest.mark.restart
    def test_caseid_1984258(self): 
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 1) # 车辆Ready指示状态
        # 通知实际车速状态 VehSpdLgt|UpdateSpeedChangedEvent
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 0) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)   
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr12, 'TqModAct', 0) # 扭矩模式状态
        self.ipdu.set(self.ipdu.chassiscan2.SumChas2Fr02, 'ActModOfDampr', 0) # 悬架减震阻尼等级状态
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'AutHldSoftSwtEnaSts', 0) # 通知AVH功能使能状态
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'SwtStsforHillDwnCtrl', 0) # HDC开关可用状态
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr09, 'CrpModAct', 0) # 获取蠕行模式状态
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 0) # EPB功能运行状态
        # 档位状态 GearLvrIndcn|TrsmParkLockdTrsmParkLockd|UpdateGearEvent
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 7)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 0) # 通知车辆运动状态
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 1) # 转向系统故障状态
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 1) # ESC运行状态
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr18, 'PrpsnModSptBlkd', 0) # 运动模式有效状态
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr09, 'GearLvrFaultIndcn', 0) # 换挡故障状态
        dict1={"WhlSpdCircumlFrntLe": "WhlSpdCircumlFrntLeQf", "WhlSpdCircumlFrntWhlSpdCircumlFrntRi": "WhlSpdCircumlFrntRiQf", 
               "WhlSpdCircumlReLe": "WhlSpdCircumlReLeQf", "WhlSpdCircumlReRi": "WhlSpdCircumlReRiQf"}
        for key, value in dict1.items(): # 获取轮速状态         
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, key, 0) 
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr40, value, 0) 
        self.set_WhlRotToothCntr() # 通知车轮旋转脉冲计数状态    
        self.ipdu.set(self.ipdu.propulsioncan.EgsmPropFr01, 'DrvrGearShiftReqInv', 0) # 通知EGSM虚拟挡位请求
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr10, 'PTStsForRace', 0) # 通知驱动系统实际状态
        self.ipdu.set(self.ipdu.passivesafetycan.SrsPassSafeCANFr04, 'ADataRawSafeALgt', 0) # 通知车辆加速度信息
        self.ipdu.set(self.ipdu.passivesafetycan.SrsPassSafeCANFr04, 'ADataRawSafeALat', 0)
        self.ipdu.set(self.ipdu.passivesafetycan.SrsPassSafeCANFr04, 'ADataRawSafeAVert', 0)
        self.ipdu.set(self.ipdu.chassiscan1.VddmChas1Fr53, 'StandStillMgrStsForHld1', 0) # 车辆静止状态
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr25, 'LnchModSts',  1) # 通知弹射起步功能状态信息
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr48, 'LnchModIndcnMsg',  0) 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr07, 'EPedlModSts', 1) # 通知EPedal单踏板模式功能状态信息
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr09, 'EPedlInhbnSts', 0) 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr38, 'EPedlDrvrIndcnMsg', 0) 
        self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr26, 'WhlBrkOvrheatd', 0) # 制动盘过热状态
        self.ipdu.set(self.ipdu.propulsioncan.EgsmPropFr01, 'GearLvrIllmnSts', 0) # 触摸换挡器激活状态
        self.partner.empty_all(3)
        
        self.partner.send_request_and_ck_resp("ChassisService_client", "getVehReadySts", {}, {"out": False}) # 车辆Ready指示状态
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetSpeed", {}, {"out": {"speed": 0, "isvalid": False}}) # 实际车速状态
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetDisplaySpeed", {}, {"out": {"speed":0,"speedUnit":0,"isvalid":False}})  # 获取显示车速状态 
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetTorqueMode", {}, {"out": 0}) # 获取扭矩模式状态
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetSuspensionLevel", {}, {"out": 0}) # 获取悬架减震阻尼等级状态 
        # self.partner.send_request_and_ck_resp("ChassisService_client", "GetAutoHold", {}, {"out": False}) # AVH功能使能状态
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetHDCFunctionAvailable", {}, {"out": False}) # HDC开关可用状态
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetCreepMode", {}, {"out": True}) # 获取蠕行模式状态      
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetEPBOperationStatus", {},{"out": 0}) # 通知EPB功能运行状态
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetGear", {}, {"out": 5}) # 档位状态
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetVehicleMotionState", {}, {"out": {"motionState": 0, "isvalid": True}}) # 车辆运动状态
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetSteerErrorReqStatus", {}, {"out": 1}) # 转向系统故障状态
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetESCWorkStatus", {}, {"out": 1}) # ESC运行状态      
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetSportModeAvailableStatus", {}, {"out": 0}) # 运动模式有效状态
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetGearFault", {}, {"out": [0]})  # 换挡故障状态
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetWheelSpeed", {"wheels": [1, 2, 3, 4]}, 
                                                {"out": [{"wheelId": 1, "speed": 0.0, "isvalid": False},
                                                        {"wheelId": 2, "speed": 0.0, "isvalid": False},
                                                        {"wheelId": 3, "speed": 0.0, "isvalid": False},
                                                        {"wheelId": 4, "speed": 0.0, "isvalid": False}]}) # 获取轮速状态
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetWheelImpluseCounter", {"wheels": [1, 2, 3, 4]},
                                              {"out": [{"wheelId": 1, "wheelImpluseCounter": 0, "isvalid": True},
                                                       {"wheelId": 2, "wheelImpluseCounter": 0, "isvalid": True},
                                                       {"wheelId": 3, "wheelImpluseCounter": 0, "isvalid": True},
                                                       {"wheelId": 4, "wheelImpluseCounter": 0, "isvalid": True}]}) # 获取车轮旋转脉冲计数状态
        self.partner.send_request_and_ck_resp("ChassisService_client", "GetEGSMVirtualShiftReq", {}, {"out": 0})  # 通知EGSM虚拟挡位请求
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetPropulsionStatus", {}, {"out": [0]}) # 通知驱动系统实际状态  
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, 'GetVehicleAcceleration', {}, 
                                              {"out": {"longAcceleration": 0, "lateralAcceleration": 0, "verticalAcceleration": 0}}) # 获取车辆加速度信息 
        # 通知行驶里程
        current_travel_dist=self.partner.send_request_and_return_resp("ChassisService_client", "GetTraveledDistance", {})["out"]            
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,"GetVehicleStandStillSts",{},{"out":{"value":0,"validity":0}}) # 车辆静止状态
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetLaunchMode", {}, {"out": {"status":0, "fault":0}}) # 通知弹射起步功能状态信息
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetEPedlModeInfo", {}, 
                                              {"out": {"mode":0,"inhibitSts":0,"decelerationLimitSts":0}})  # 获取EPedal单踏板模式功能状态信息
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetBrakeDiscOverHeatSts", {}, {"out": 0}) # 制动盘过热状态
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetTouchShiftActiveSts", {}, {"out": 0}) # 触摸换挡器激活状态      
  
        self.restart_bgm_and_connect_service(CHASSIS_SERVICE_CLIENT)
        # 通知车辆Ready指示状态 
        self.partner.ck_s2s_event("ChassisService_client", "vehicleReady", {"sts": False})
        # 通知显示车速状态
        self.partner.ck_s2s_event("ChassisService_client", "DisplaySpeedChanged",
                                  {"speed":{"speed":0,"speedUnit":0,"isvalid":False}}) # 总线上 速度单位信号=0
        # 通知实际车速状态 
        self.partner.ck_s2s_event("ChassisService_client", "SpeedChanged", {"speed": {"speed": 0.0, "isvalid": False}})    
        # 通知扭矩模式状态 
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "TorqueMode", {"mode": 0})   
        # 通知悬架减震阻尼等级状态 
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "SuspensionLevel", {"level": 0})
        # 通知HDC开关可用状态 
        self.partner.ck_s2s_event("ChassisService_client", "HDCFunctionAvailableChanged", {"on": False})
        # 通知蠕行模式状态 
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "CreepMode", {"on": True})
        # 通知EPB功能运行状态 
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "EPBOperationStatus", {"state": 0})
        # 通知档位状态
        self.partner.ck_s2s_event("ChassisService_client", "Gear", {"gear": 5}) 
        # 通知车辆运动状态 
        self.partner.ck_s2s_event("ChassisService_client", "VehicleMotionState", {"state":{"motionState":0,"isvalid":True}})
        # 通知转向系统故障状态
        self.partner.ck_s2s_event("ChassisService_client", "SteerErrorReqStatus", {"state": 1})
        # 通知ESC运行状态 
        self.partner.ck_s2s_event("ChassisService_client", "ESCWorkStatus", {"state": 1})
        # 通知运动模式有效状态
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "SportModeAvailableStatus", {"state": 0})
        # 通知换挡故障状态
        self.partner.ck_s2s_event("ChassisService_client", "GearFault",{"faults":[0]})      
        # 通知轮速状态 Pass 
        self.partner.ck_s2s_event("ChassisService_client", "WheelSpeed", 
                                 {"wheelsSpeed": [{"wheelId": 1, "speed": 0.0, "isvalid": False}, 
                                                  {"wheelId": 2, "speed": 0.0, "isvalid": False},
                                                  {"wheelId": 3, "speed": 0.0, "isvalid": False}, 
                                                  {"wheelId": 4, "speed": 0.0, "isvalid": False}]})
        # 通知车轮旋转脉冲计数状态
        self.partner.ck_s2s_event("ChassisService_client", "WheelImpluseCounter", 
                                  {"wheelsImpluseCounter":[{"wheelId":1, "wheelImpluseCounter":0, "isvalid":True}, 
                                                           {"wheelId":2, "wheelImpluseCounter":0, "isvalid":True},
                                                           {"wheelId":3, "wheelImpluseCounter":0, "isvalid":True},
                                                           {"wheelId":4, "wheelImpluseCounter":0, "isvalid":True}]})  
        # 通知EGSM虚拟挡位请求
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "EGSMVirtualShiftReq", {"gear": 0})
        # 通知驱动系统实际状态
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,"PropulsionStatus",{"sts":[0]})   
        # 通知车辆加速度信息 
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, 'VehicleAcceleration', 
                                  {"info": {"longAcceleration": 0, "lateralAcceleration": 0, "verticalAcceleration": 0}})
        # 通知行驶里程
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "TraveledDistance", {"value": current_travel_dist})
        # 通知车辆静止状态
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,"VehicleStandStillSts",{"sts":{"value":0,"validity":0}})    
        # 通知弹射起步功能状态信息
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,"LaunchMode",{"info":{"status":0, "fault":0}})
        # 通知EPedal（单踏板模式）功能状态信息
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT,"EPedlModeInfo",{"info":{"mode":0,"inhibitSts":0,"decelerationLimitSts":0}})    
        # 通知制动盘过热状态
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "BrakeDiscOverHeatSts", {"state":0})
        # 通知触摸换挡器激活状态
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "TouchShiftActiveSts",{"sts": 0})
                               
    @allure.title("BGM首次下线默认配置")
    @pytest.mark.full
    @pytest.mark.restart
    def test_caseid_1943410_1943409(self):
        # 删除数据库
        bgmssh = BGM_SSH()
        bgmssh.type_commands("sudo rm -rf /data/s2s_service/s2s_service.db3", root_permission=True)
        sleep(1)
        bgmssh.type_commands("ls -l /data/s2s_service")
        sleep(5)
        self.ipdu.pause_all_bus_send()  # 停掉总线
        self.nucapp.bgm_power_off()
        sleep(7)
        self.partner.empty_all()
        self.nucapp.bgm_power_on()
        self.partner.wait_for_service_reconnect(CHASSIS_SERVICE_CLIENT)   
        # ESC运动模式状态
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetEscSportModeStatus", {}, {"out": False})
        # 陡坡缓降开关状态
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "GetHDCOn", {}, {"out": False})   
                       
######################################################################################################################################################## 

@allure.feature("SOA服务接口")
@allure.story("运动控制/ChassisService")
@pytest.mark.aqx      
class TestChassisServiceMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21", enable_inter_service=True)
        self.partner = S2sBaseClass([("ChassisService", "client")])
        self.partner.wait_for_service_reconnect(CHASSIS_SERVICE_CLIENT) 
        sleep(10)

    def after_class(self, ecu):
        try:
            self.partner.stop_operators()
        except Exception as e:
            logger.error(f"{str(e)}")
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all(5)

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()
        sleep(5)
        super().after_each_func(ecu)
        
    def set_BrkSys(self, req, req_sec, brk_and_abs_req, brk_fld_lvl, sleeptime=5):
        # 制动系统报警指示请求状态
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkSysWarnIndcnReq', req)  # len=1
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'BrkSysWarnIndcnReqSec', req_sec) # len=1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', brk_and_abs_req) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', brk_fld_lvl) # len=1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', 0)
        self.ipdu.set(self.ipdu.backbonefr.BbmVcuBackBoneFr02, 'EpbDrvrDispSec', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq',0)
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq',0)  
        sleep(sleeptime)
        
    def set_DisplayReqSts(self, signal=[0, 0, 3, 3], sleep_time=2):
        # 设置EPB显示请求状态，默认设0
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr16, 'EpbDrvrDisp', signal[0])
        self.ipdu.set(self.ipdu.backbonefr.BbmVcuBackBoneFr02, 'EpbDrvrDispSec', signal[1])
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq', signal[2])
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq', signal[3])  
        sleep(sleep_time)
    
    def ck_brkSysWarnIndicateReqSts_and_getBrkSysWarnIndicateReqSts(self, sts, timeout=3):    
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "brkSysWarnIndicateReqSts", {"sts": sts})
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnIndicateReqSts", {}, {"out": sts}, timeout)
        
    def ck_no_event_and_getBrkSysWarnIndicateReqSts(self, sts, timeout=3):    
        self.partner.ck_no_event(CHASSIS_SERVICE_CLIENT, "brkSysWarnIndicateReqSts")
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnIndicateReqSts", {}, {"out": sts}, timeout)
    
    def ck_epbDisplayReqSts_and_getDisplayReqSts(self, highPriSts, lowPriSts, timeout=3):
        self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "epbDisplayReqSts", {"sts": {"highPriSts": highPriSts, "lowPriSts": lowPriSts}}, timeout)
        self.partner.send_request_and_ck_resp("ChassisService_client", "getDisplayReqSts", {}, {"out": {"highPriSts": highPriSts, "lowPriSts": lowPriSts}})

    @allure.title("获取&通知制动系统报警指示请求状态_sts=0_仅57-1-8信号丢失")
    @pytest.mark.full
    def test_caseid_1985743(self): 
        # 1 BrkFldLvl|1 BrkSysWarnIndcnReq|1 BrkSysWarnIndcnReqSec|1 BrkAndAbsWarnIndcnReqBrkWarnIndcnReq
        # mEpbDrvrDispTimeOutFlag|UpdatebrkSysWarnIndicateReqStsEvent|mEpbDrvrDispSecTimeOutFlag
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 1) # UsgMod信号s
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 1) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', 0) # len=1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkSysWarnIndcnReq', 1)  # len=1
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'BrkSysWarnIndcnReqSec', 1) # len=1
        sleep(5)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnIndicateReqSts", {}, {"out": 0}, timeout=3)
        self.partner.empty_all()
        logger.info(f"打印信号丢失")
        self.ipdu.stop_send_pdu("backbonefr", 3735816) # EpbDrvrDisp 57-1-8  mEpbDrvrDispTimeOutFlag
        self.ck_brkSysWarnIndicateReqSts_and_getBrkSysWarnIndicateReqSts(1) 
        self.ipdu.resume_bus_send("backbonefr")
        logger.info(f"恢复信号丢失")
        self.ck_brkSysWarnIndicateReqSts_and_getBrkSysWarnIndicateReqSts(0) 

    @allure.title("获取&通知制动系统报警指示请求状态_sts=0_仅7-8-64信号丢失")
    @pytest.mark.full
    def test_caseid_1985751(self): # 7-8-64 BrkSysWarnIndcnReqSec和EpbLampReqSecEpbLampReq 
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 1) # UsgMod信号s
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 1) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', 0) # len=1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkSysWarnIndcnReq', 1)  # len=1
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'BrkSysWarnIndcnReqSec', 1) # len=1
        sleep(5)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnIndicateReqSts", {}, {"out": 0}, timeout=3)
        self.partner.empty_all()
        logger.info(f"打印信号丢失")
        self.ipdu.stop_send_pdu("backbonefr", 460864) # EpbDrvrDisp 7-8-64  BrkSysWarnIndcnReqSec_EpbLampReqSecEpbLampReq_TimeOut
        self.ck_brkSysWarnIndicateReqSts_and_getBrkSysWarnIndicateReqSts(1) 
        self.ipdu.resume_bus_send("backbonefr")
        logger.info(f"恢复信号丢失")
        self.ck_brkSysWarnIndicateReqSts_and_getBrkSysWarnIndicateReqSts(0) 

    @allure.title("获取&通知制动系统报警指示请求状态_sts=0_仅7-2-4信号丢失")
    @pytest.mark.full
    def test_caseid_1985744(self): # 459268 7-2-4 EpbDrvrDispSec
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 1) # UsgMod信号s
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 1) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', 0) # len=1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkSysWarnIndcnReq', 1)  # len=1
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'BrkSysWarnIndcnReqSec', 1) # len=1
        sleep(5)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnIndicateReqSts", {}, {"out": 0}, timeout=3)
        self.partner.empty_all()
        logger.info(f"打印信号丢失")
        self.ipdu.stop_send_pdu("backbonefr", 459268) # 7-2-4 EpbDrvrDispSec 
        self.ck_brkSysWarnIndicateReqSts_and_getBrkSysWarnIndicateReqSts(1) 
        self.ipdu.resume_bus_send("backbonefr")
        logger.info(f"恢复信号丢失")
        self.ck_brkSysWarnIndicateReqSts_and_getBrkSysWarnIndicateReqSts(0) 

    @allure.title("获取&通知制动系统报警指示请求状态_sts=0_仅57-23-64信号丢失")
    @pytest.mark.full
    def test_caseid_1985750(self): # 3741504 57-23-64 BrkSysWarnIndcnReq 
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 1) # UsgMod信号s
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 1) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', 0) # len=1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkSysWarnIndcnReq', 1)  # len=1
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'BrkSysWarnIndcnReqSec', 1) # len=1
        sleep(5)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnIndicateReqSts", {}, {"out": 0}, timeout=3)
        self.partner.empty_all()
        logger.info(f"打印信号丢失")
        self.ipdu.stop_send_pdu("backbonefr", 3741504) # 57-23-64
        self.ck_brkSysWarnIndicateReqSts_and_getBrkSysWarnIndicateReqSts(2) 
        self.ipdu.resume_bus_send("backbonefr")
        logger.info(f"恢复信号丢失")
        self.ck_brkSysWarnIndicateReqSts_and_getBrkSysWarnIndicateReqSts(0) 

    @allure.title("获取&通知制动系统报警指示请求状态_sts=0_57-23-64和7-8-64信号丢失")
    @pytest.mark.full
    def test_caseid_1985752(self): # 3741504 57-23-64 BrkSysWarnIndcnReq 
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 1) # UsgMod信号s
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 1) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', 0) # len=1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkSysWarnIndcnReq', 1)  # len=1
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'BrkSysWarnIndcnReqSec', 1) # len=1
        sleep(5)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnIndicateReqSts", {}, {"out": 0}, timeout=3)
        self.partner.empty_all()
        logger.info(f"打印信号丢失")
        self.ipdu.stop_send_pdu("backbonefr", 460864) # 7-8-64 BrkSysWarnIndcnReqSec_EpbLampReqSecEpbLampReq_TimeOut
        self.ck_brkSysWarnIndicateReqSts_and_getBrkSysWarnIndicateReqSts(1)
        self.ipdu.stop_send_pdu("backbonefr", 3741504) # 57-23-64
        self.ck_brkSysWarnIndicateReqSts_and_getBrkSysWarnIndicateReqSts(2) 
        logger.info(f"恢复信号丢失")
        self.ipdu.resume_send_pdu("backbonefr", 3741504) # 57-23-64
        self.ck_brkSysWarnIndicateReqSts_and_getBrkSysWarnIndicateReqSts(1)
        self.ipdu.resume_bus_send("backbonefr")
        self.ck_brkSysWarnIndicateReqSts_and_getBrkSysWarnIndicateReqSts(0) 

    @allure.title("获取&通知制动系统报警指示请求状态_sts=0_57-23-64和57-1-8信号丢失")
    @pytest.mark.full
    def test_caseid_1985780(self): # 3741504 57-23-64 BrkSysWarnIndcnReq 
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 1) # UsgMod信号s
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 1) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', 0) # len=1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkSysWarnIndcnReq', 1)  # len=1
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'BrkSysWarnIndcnReqSec', 1) # len=1
        sleep(5)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnIndicateReqSts", {}, {"out": 0}, timeout=3)
        self.partner.empty_all()
        logger.info(f"打印信号丢失")
        self.ipdu.stop_send_pdu("backbonefr", 3735816) # 57-1-8  mEpbDrvrDispTimeOutFlag
        self.ck_brkSysWarnIndicateReqSts_and_getBrkSysWarnIndicateReqSts(1)
        self.ipdu.stop_send_pdu("backbonefr", 3741504) # 57-23-64
        self.ck_brkSysWarnIndicateReqSts_and_getBrkSysWarnIndicateReqSts(2) 
        logger.info(f"恢复信号丢失")
        self.ipdu.resume_send_pdu("backbonefr", 3741504) # 57-23-64
        self.ck_brkSysWarnIndicateReqSts_and_getBrkSysWarnIndicateReqSts(1)
        self.ipdu.resume_bus_send("backbonefr")
        self.ck_brkSysWarnIndicateReqSts_and_getBrkSysWarnIndicateReqSts(0) 

    @allure.title("获取&通知制动系统报警指示请求状态_sts=0_57-23-64和7-2-4信号丢失")
    @pytest.mark.full
    def test_caseid_1985781(self): # 3741504 57-23-64 BrkSysWarnIndcnReq 
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 1) # UsgMod信号s
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 1) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', 0) # len=1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkSysWarnIndcnReq', 1)  # len=1
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'BrkSysWarnIndcnReqSec', 1) # len=1
        sleep(5)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnIndicateReqSts", {}, {"out": 0}, timeout=3)
        self.partner.empty_all()
        logger.info(f"打印信号丢失")
        self.ipdu.stop_send_pdu("backbonefr", 3741504) # 57-23-64
        self.ck_brkSysWarnIndicateReqSts_and_getBrkSysWarnIndicateReqSts(2) 
        self.ipdu.stop_send_pdu("backbonefr", 459268) # 7-2-4 mEpbDrvrDispSecTimeOutFlag
        self.ck_no_event_and_getBrkSysWarnIndicateReqSts(2)
        logger.info(f"恢复信号丢失")
        self.ipdu.resume_send_pdu("backbonefr", 3741504) # 57-23-64
        self.ck_brkSysWarnIndicateReqSts_and_getBrkSysWarnIndicateReqSts(1)
        self.ipdu.resume_bus_send("backbonefr")
        self.ck_brkSysWarnIndicateReqSts_and_getBrkSysWarnIndicateReqSts(0) 

    @allure.title("获取&通知制动系统报警指示请求状态_sts=0_57-1-8和7-2-4和7-8-64信号丢失")
    @pytest.mark.full
    def test_caseid_1985782(self): # 3741504 57-23-64 BrkSysWarnIndcnReq 
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 1) # UsgMod信号s
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 1) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', 0) # len=1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkSysWarnIndcnReq', 1)  # len=1
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'BrkSysWarnIndcnReqSec', 1) # len=1
        sleep(5)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnIndicateReqSts", {}, {"out": 0}, timeout=3)
        self.partner.empty_all()
        logger.info(f"打印信号丢失")
        self.ipdu.stop_send_pdu("backbonefr", 3735816) # 57-1-8
        self.ck_brkSysWarnIndicateReqSts_and_getBrkSysWarnIndicateReqSts(1) 
        self.ipdu.stop_send_pdu("backbonefr", 459268) # 7-2-4 
        self.ipdu.stop_send_pdu("backbonefr", 460864) # 7-8-64 
        self.ck_no_event_and_getBrkSysWarnIndicateReqSts(1)
        logger.info(f"恢复信号丢失")
        self.ipdu.resume_bus_send("backbonefr")
        self.ck_brkSysWarnIndicateReqSts_and_getBrkSysWarnIndicateReqSts(0)   

    @allure.title("获取&通知制动系统报警指示请求状态_sts=1_57-1-8和57-23-64和7-2-4信号丢失")
    @pytest.mark.full
    def test_caseid_1985783(self): # 3741504 57-23-64 BrkSysWarnIndcnReq 
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 1) # UsgMod信号s
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 1) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', 0) # len=1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkSysWarnIndcnReq', 0)  # len=1
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'BrkSysWarnIndcnReqSec', 1) # len=1
        sleep(5)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnIndicateReqSts", {}, {"out": 1}, timeout=3)
        self.partner.empty_all()    
        logger.info(f"打印信号丢失")
        self.ipdu.stop_send_pdu("backbonefr", 3735816) # 57-1-8
        self.ck_no_event_and_getBrkSysWarnIndicateReqSts(1) 
        self.ipdu.stop_send_pdu("backbonefr", 3741504) # 57-23-64
        self.ck_brkSysWarnIndicateReqSts_and_getBrkSysWarnIndicateReqSts(2) 
        logger.info(f"恢复信号丢失")
        self.ipdu.resume_send_pdu("backbonefr", 3741504) # 57-23-64
        self.ck_brkSysWarnIndicateReqSts_and_getBrkSysWarnIndicateReqSts(1)   
        self.ipdu.resume_bus_send("backbonefr")
        self.ck_no_event_and_getBrkSysWarnIndicateReqSts(1)  

    @allure.title("获取&通知制动系统报警指示请求状态_sts=2_57-1-8和57-23-64和7-8-64信号丢失")
    @pytest.mark.full
    def test_caseid_1985784(self): # 3741504 57-23-64 BrkSysWarnIndcnReq 
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 1) # UsgMod信号s
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 1) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkFldLvl', 1) # len=1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'BrkSysWarnIndcnReq', 0)  # len=1
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'BrkSysWarnIndcnReqSec', 1) # len=1
        sleep(5)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnIndicateReqSts", {}, {"out": 2}, timeout=3)
        self.partner.empty_all()    
        logger.info(f"打印信号丢失")
        self.ipdu.stop_send_pdu("backbonefr", 3735816) # 57-1-8
        self.ipdu.stop_send_pdu("backbonefr", 3741504) # 57-23-64
        self.ipdu.stop_send_pdu("backbonefr", 460864) # 7-8-64
        self.ck_no_event_and_getBrkSysWarnIndicateReqSts(2) 
        logger.info(f"恢复信号丢失")
        self.ipdu.resume_bus_send("backbonefr") 
        self.ck_no_event_and_getBrkSysWarnIndicateReqSts(2) 

    @allure.title("获取制动系统报警指示请求状态_模拟全部信号无数据")
    @pytest.mark.full
    def test_caseid_1979783(self): 
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 1) # UsgMod信号
        self.set_BrkSys(1, 1, 1, 0)
        self.ipdu.stop_send_pdu("backbonefr", 3741504) # 57-23-64
        self.ipdu.stop_send_pdu("backbonefr", 460864) # 7-8-64 BrkSysWarnIndcnReqSec_EpbLampReqSecEpbLampReq_TimeOut
        sleep(2)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnIndicateReqSts", {}, {"out": 2}, timeout=3)
        self.bgm_power_off_and_on(timeout=3)
        self.partner.wait_for_service_reconnect(CHASSIS_SERVICE_CLIENT)
        sleep(5)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnIndicateReqSts", {}, {"out": 0}, timeout=3)

    @allure.title("获取制动系统报警指示请求状态_模拟7-8-64无数据")
    @pytest.mark.full
    def test_caseid_1979782(self): 
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 1) # UsgMod信号
        self.set_BrkSys(1, 1, 1, 0)
        self.ipdu.stop_send_pdu("backbonefr", 460864) # 7-8-64
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnIndicateReqSts", {}, {"out": 1}, timeout=3)
        self.bgm_power_off_and_on(timeout=3)
        self.partner.wait_for_service_reconnect(CHASSIS_SERVICE_CLIENT)
        sleep(5)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnIndicateReqSts", {}, {"out": 0}, timeout=3)

    @allure.title("获取制动系统报警指示请求状态_模拟57-23-64无数据")
    @pytest.mark.full
    def test_caseid_1979781(self): 
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 1) # UsgMod信号
        self.set_BrkSys(1, 1, 1, 0)
        self.ipdu.stop_send_pdu("backbonefr", 3741504) # 57-23-64
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnIndicateReqSts", {}, {"out": 2}, timeout=3)
        self.bgm_power_off_and_on(timeout=3)
        self.partner.wait_for_service_reconnect(CHASSIS_SERVICE_CLIENT)
        sleep(5)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT, "getBrkSysWarnIndicateReqSts", {}, {"out": 0}, timeout=3)
        
    @allure.title("获取&通知行驶里程")
    @pytest.mark.sanity
    def test_caseid_1886032(self):  # fr TotDstTrvldHiResl|TraveledDistance
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr10, 'TotDstTrvldHiResl', 0)
        sleep(2)
        for dst in [1, 4294967295, 0]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr10, 'TotDstTrvldHiResl', dst)
            self.partner.send_request_and_ck_resp("ChassisService_client", "GetTraveledDistance", {}, {"out": dst}, timeout=3)   
            self.partner.ck_s2s_event(CHASSIS_SERVICE_CLIENT, "TraveledDistance", {"value": dst})
        
    @allure.title("EPB显示请求状态_EpbDrvrDisp信号丢失")
    @pytest.mark.full
    def test_caseid_1981763(self): # mEpbDrvrDispTimeOutFlag|mEpbDrvrDispSecTimeOutFlag|EpbDrvrDisp|EpbLampReq|-UpdateepbDisplayReqSts|lastUM
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 2) # UsgMod信号
        self.set_DisplayReqSts(signal=[1, 4, 3, 3],sleep_time=5)  
        self.partner.send_request_and_ck_resp("ChassisService_client", "getDisplayReqSts", {}, {"out": {"highPriSts": 2, "lowPriSts": 3}}, timeout=3)
        self.partner.empty_all()
        logger.info(f"打印信号丢失")
        self.ipdu.stop_send_pdu('backbonefr', 3735816) # 57-1-8	EpbDrvrDisp mEpbDrvrDispTimeOutFlag
        self.ck_epbDisplayReqSts_and_getDisplayReqSts(highPriSts=3, lowPriSts=5)
        self.ipdu.resume_bus_send("backbonefr")  
        self.ck_epbDisplayReqSts_and_getDisplayReqSts(highPriSts=2, lowPriSts=3)
        
    @allure.title("EPB显示请求状态_EpbDrvrDispSec信号丢失")
    @pytest.mark.full
    def test_caseid_1981765(self): 
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 11) # UsgMod信号
        self.set_DisplayReqSts(signal=[1, 4, 3, 3])      
        self.partner.send_request_and_ck_resp("ChassisService_client", "getDisplayReqSts", {}, {"out": {"highPriSts": 2, "lowPriSts": 3}}, timeout=3)
        self.ipdu.stop_send_pdu('backbonefr', 459268) # EpbDrvrDispSec  
        self.ck_epbDisplayReqSts_and_getDisplayReqSts(highPriSts=2, lowPriSts=5, timeout=2.5) 
        self.ipdu.resume_bus_send("backbonefr")   
        self.ck_epbDisplayReqSts_and_getDisplayReqSts(highPriSts=2, lowPriSts=3)

    @allure.title("EPB显示请求状态_BrkSysWarnIndcnReq&EpbLampReq信号丢失")
    @pytest.mark.full
    def test_caseid_1981766(self): # EPBDisplayReqSts,sts|EpbLampReq_E2E|mEpbLampReqSec|mEpbLampReqT
        # BrkSysWarnIndcnReqSec_EpbLampReqSecEpbLampReq_TimeOut|EpbDrvrDisp_TimeOut|EpbDrvrDispSec_TimeOut
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 13) # UsgMod信号     
        self.set_DisplayReqSts(signal=[11, 15, 3, 3])      
        self.partner.send_request_and_ck_resp("ChassisService_client", "getDisplayReqSts", {}, {"out": {"highPriSts": 4, "lowPriSts": 12}}, timeout=3)
        self.ipdu.stop_send_pdu('backbonefr', 3741504)  # BrkSysWarnIndcnReq&EpbLampReq  
        sleep(7)
        self.ck_epbDisplayReqSts_and_getDisplayReqSts(highPriSts=4, lowPriSts=5)
        self.ipdu.resume_bus_send("backbonefr")   
        sleep(5)
        self.ck_epbDisplayReqSts_and_getDisplayReqSts(highPriSts=4, lowPriSts=12)
        
    @allure.title("EPB显示请求状态_BrkSysWarnIndcnReqSec&EpbLampReqSec信号丢失")
    @pytest.mark.full
    def test_caseid_1981767(self): # todo 仅MockMCU可以停发FR单帧，但因MockMCU会使E2E失败，导致无法测试丢失
        # pass "DisplayReqSts|EpbLampReq_E2E result"
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 13) # UsgMod信号  
        self.set_DisplayReqSts(signal=[11, 11, 3, 3])      
        self.partner.send_request_and_ck_resp("ChassisService_client", "getDisplayReqSts", {}, {"out": {"highPriSts": 12, "lowPriSts": 0}}, timeout=3)
        logger.info(f"打印当前时间")
        self.ipdu.stop_send_pdu('backbonefr', 460864)  # BrkSysWarnIndcnReqSec&EpbLampReqSec
        self.ck_epbDisplayReqSts_and_getDisplayReqSts(highPriSts=5, lowPriSts=5)
        self.ipdu.resume_bus_send("backbonefr")   
        self.ck_epbDisplayReqSts_and_getDisplayReqSts(highPriSts=12, lowPriSts=0)
                