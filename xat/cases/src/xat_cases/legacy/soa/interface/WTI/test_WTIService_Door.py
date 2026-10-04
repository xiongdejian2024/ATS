#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_WTIService_Door.py
@Time         :2023/04/08 17:20:31
@Author       :jishu.duan_ext@jiduauto.com
@Description  :
"""
# import random

import allure
import pytest
# import copy
# from time import sleep
# from random import randint
from xat_ecu.legacy.common.data_type_handing import logger
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_cases.legacy.soa.case_helper.utils import *

@allure.feature("SOA服务接口")
@allure.story("WTI/WTIService_Door")
@pytest.mark.jishu
class TestDoorWTIService(TestBase):
    
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.partner = S2sBaseClass([("WTIService", "client"),
                                     ("DoorService","client"),
                                     ("BonnetService","client"),
                                     ("ObtDiagService","client")
                                ])
        self.partner.method_default_timeout = 0.1
        time.sleep(5)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.partner.stop_operators()
        super().after_class(self, ecu)
        # 停止和删除 也在aftercase中增加进去

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set_vehspd(0)
        sleep(0.2)
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.diagnostic_client_sim_start()
        self.sd_tester.tester_present()
        self.sd_tester.change_car_mode(0)
        self.io.init_bgm_HW()
        self.set_door_fault_clear()
        self.io.hood_door1_close()
        self.io.hood_door2_open()
        self.all_door_open_close(1)
        self.partner.empty_all()
        self.set_Actv_sig_all(0)

    def after_each_func(self, ecu):
        self.sd_tester.stop_tester_present()
        self.sd_tester.diagnostic_client_sim_close()#关闭和自动回复线程
        super().after_each_func(ecu, start=False)
    
    def ck_warningmsg(self, hint, last_info, new_info, jump_trigger=False):
        """校验事件型,非0每次上次上报,为0只在跳变为0触发一次"""
        if jump_trigger:  # 信号跳变
            if last_info != new_info:
                self.partner.ck_wti_warning_and_resp(hint, new_info)
            else:
                self.partner.ck_wti_no_warning_and_ck_resp(hint, new_info)
        else:  # 不看信号跳变
            if new_info or last_info != new_info:
                self.partner.ck_wti_warning_and_resp(hint, new_info)
            else:
                self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)
                
    def tweer_hood_swith_control(self,swith):
        """
        @param door: 表示前舱盖0=open or 1=close
        """
        if swith == 0:
            self.io.hood_door1_open()
            self.io.hood_door2_open()
        else:
            self.io.hood_door1_close()
            self.io.hood_door2_open()
        sleep(1)
    
    def all_door_open_close(self,swith):
        """
        @param door: 表示四门0=open or 1=close
        """
        for door in ["drvr","pass","lere","rire"]:
            if swith == 0:
                (eval(f"self.io.{door}_door_open() "))
            else:   
                (eval(f"self.io.{door}_door_close() "))
        sleep(1)
           
    def set_door_fault(self, door: str, sig: int, signalvalue: int):
        """
        @param door: 表示门位置, All, Drvr, Pass, LeRe, RiRe
        """
        if door == "All" :
            for door in ["Drvr", "Pass", "LeRe", "RiRe"]:
                self.set_door_fault(door, sig, signalvalue)
        else:
            self.ipdu.set(eval(f"self.ipdu.bodycan.{door[0:1]}podBodyFr01"), 
                               f"DtcInfDoor{door}Boolean{sig}", signalvalue)
        sleep(1)
    
    def set_door_fault_clear(self):
        """
        @param fault: 遍历恢复四门故障
        """
        for fault in range(5):
            self.set_door_fault("All", fault + 1, 0)
        self.partner.empty_all(1)
        sleep(1)
    
    def set_Actv_sig_all(self,sigvalue):
        """
        @param fault: 遍历车门破冰四门信号
        """
        dic = {"Drvr" : 7, "Pass" : 1 , "LeRe" : 2, "RiRe" : 2}
        for key, value in dic.items():
            if key == "Drvr" or key == "Pass":
                self.ipdu.set(eval(f"self.ipdu.bodycan.{key[0:1]}dmBodyFr0{value}"),f"IceBreakDoor{key}Actv", sigvalue )
            else:
                self.ipdu.set(eval(f"self.ipdu.bodycan.R{key[0:1].lower()}dmBodyFr0{value}"),f"IceBreakDoor{key}Actv", sigvalue )
        sleep(1)
        
    @allure.title("WTI_电动门防玩和热保护提醒_全部车门防玩激活") 
    @pytest.mark.sanity
    def test_caseid_1943310(self):
        last_info = 0
        lis =[]
        for  door_sts in ["Drvr", "Pass", "LeRe", "RiRe"]:
            logger.info(f"当前门为.{door_sts}")
            for Thermal in [1, 0]:
                self.ipdu.set(eval(f"self.ipdu.bodycan.{door_sts[0:1]}podBodyFr01"), 
                               f"DtcInfDoor{door_sts}Boolean{2}", Thermal)
                new_info = Thermal 
                self.ck_warningmsg("Door AntiPlay Reminder", last_info, new_info, jump_trigger=True)
                last_info = new_info
            

    @allure.title("WTI_电动门防玩和热保护提醒_单门交叉产生故障") 
    @pytest.mark.full
    def test_caseid_1987861(self):     
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01,"DtcInfDoorDrvrBoolean2", 1)  
        self.partner.ck_wti_warning_and_resp("Door AntiPlay Reminder", "1") 
        self.partner.empty_all(0.5) 
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01,"DtcInfDoorPassBoolean1", 1) 
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01,"DtcInfDoorDrvrBoolean2", 0)
        self.partner.ck_wti_no_warning_and_ck_resp("Door AntiPlay Reminder", "1")
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01,"DtcInfDoorPassBoolean1", 0)
        sleep(0.2) 
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01,"DtcInfDoorLeReBoolean2", 1) 
        self.partner.ck_wti_warning_and_resp("Door AntiPlay Reminder", "1") 
        self.partner.empty_all(0.5) 
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01,"DtcInfDoorRiReBoolean1", 1) 
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01,"DtcInfDoorLeReBoolean2", 0) 
        self.partner.ck_wti_no_warning_and_ck_resp("Door AntiPlay Reminder", "1")
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01,"DtcInfDoorRiReBoolean1", 0)
        self.partner.ck_wti_warning_and_resp("Door AntiPlay Reminder", "0") 
        
    @allure.title("WTI_坡度过大开关门提醒_单门交叉产生故障") 
    @pytest.mark.sanity
    def test_caseid_1987869(self):  
        self.io.drvr_door_open()
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01,"DtcInfDoorDrvrBoolean3", 1)  
        self.partner.ck_wti_warning_and_resp("Door Reminder Due To Large Slope", "1") 
        self.partner.empty_all(0.5) 
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01,"DtcInfDoorPassBoolean4", 1) 
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01,"DtcInfDoorDrvrBoolean3", 0)
        self.partner.ck_wti_warning_and_resp("Door Reminder Due To Large Slope", "0") 
        self.io.pass_door_open()
        self.partner.ck_wti_warning_and_resp("Door Reminder Due To Large Slope", "1")
        self.io.pass_door_close()
        self.partner.ck_wti_warning_and_resp("Door Reminder Due To Large Slope", "0")
        sleep(0.2)
        self.io.lere_door_open() 
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01,"DtcInfDoorLeReBoolean3", 1) 
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01,"DtcInfDoorLeReBoolean4", 1) 
        self.partner.ck_wti_warning_and_resp("Door Reminder Due To Large Slope", "1") 
        self.partner.empty_all(0.5) 
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01,"DtcInfDoorLeReBoolean4", 0) 
        self.partner.ck_wti_no_warning_and_ck_resp("Door Reminder Due To Large Slope", "1")
        sleep(0.2)
        self.io.rire_door_open()
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01,"DtcInfDoorRiReBoolean3", 1) 
        self.partner.ck_wti_no_warning_and_ck_resp("Door Reminder Due To Large Slope", "1")
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01,"DtcInfDoorRiReBoolean3", 0)
        self.partner.ck_wti_no_warning_and_ck_resp("Door Reminder Due To Large Slope", "1")
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01,"DtcInfDoorLeReBoolean3", 0) 
        self.partner.ck_wti_warning_and_resp("Door Reminder Due To Large Slope", "0")      
         
                      
    @allure.title("WTI_电动门防玩和热保护提醒_全部车门热保护") 
    @pytest.mark.sanity
    def test_caseid_1943309(self):
        last_info = 0
        for  door_sts in ["Drvr", "Pass", "LeRe", "RiRe"]:
            for Thermal in [1, 0]:
                logger.info(f"当前信号为.{Thermal},当前门为.{door_sts}")
                self.ipdu.set(eval(f"self.ipdu.bodycan.{door_sts[0:1]}podBodyFr01"), 
                               f"DtcInfDoor{door_sts}Boolean{1}", Thermal)
                new_info = Thermal 
                self.ck_warningmsg("Door AntiPlay Reminder", last_info, new_info, jump_trigger=True)    
                last_info = new_info       
    
    @allure.title("WTI_坡度过大开关门提醒_全部车门车辆横摆角度不正确") 
    @pytest.mark.full
    def test_caseid_1943299(self):
        last_info = 0
        for door in ["Drvr", "Pass", "LeRe", "RiRe"]:
            for door_sts in ["open","close"]:
                if door_sts == "open":
                    (eval(f"self.io.{door.lower()}_door_open()"))
                else:
                     (eval(f"self.io.{door.lower()}_door_close()"))
                sleep(0.2)
                for Thermal in [1, 0]:
                    logger.info(f"当前门开关.{door_sts},当前门为:{door}")
                    self.ipdu.set(eval(f"self.ipdu.bodycan.{door[0:1]}podBodyFr01"), 
                                   f"DtcInfDoor{door}Boolean{3}", Thermal)
                    if door_sts == "open" and Thermal ==1:
                       new_info = 1
                    else:
                       new_info = 0 
                    self.ck_warningmsg("Door Reminder Due To Large Slope", last_info, new_info, jump_trigger=True)
                    last_info = new_info      
            self.partner.empty_all(0.5)
            
    @allure.title("坡度过大开关门提醒__全部车门道路倾斜角度不正常") 
    @pytest.mark.full
    def test_caseid_1943295(self):  
        last_info = 0
        for door in ["Drvr", "Pass", "LeRe", "RiRe"]:
            for door_sts in ["open","close"]:
                if door_sts == "open":
                    (eval(f"self.io.{door.lower()}_door_open()"))
                else:
                     (eval(f"self.io.{door.lower()}_door_close()"))
                sleep(0.2)
                for Thermal in [1, 0]:
                    self.ipdu.set(eval(f"self.ipdu.bodycan.{door[0:1]}podBodyFr01"), 
                                    f"DtcInfDoor{door}Boolean{4}", Thermal)
                    logger.info(f"当前门开关.{door_sts},当前们.{door},当前Thermal.{Thermal}")
                    if door_sts == "open" and Thermal ==1:
                       new_info = 1
                    else:
                       new_info = 0
                    self.ck_warningmsg("Door Reminder Due To Large Slope", last_info, new_info, jump_trigger=True)
                    last_info = new_info
            self.partner.empty_all(0.5)
                                  
    @allure.title("坡度过大开关门提醒_主驾驶遍历道路倾斜/横摆角度不正确故障产生恢复") 
    @pytest.mark.full
    def test_caseid_1980305(self):  
        self.io.drvr_door_open()
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01,"DtcInfDoorDrvrBoolean4", 1)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01,"DtcInfDoorDrvrBoolean3", 1)
        self.partner.ck_wti_warning_and_resp("Door Reminder Due To Large Slope", "1")
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01,"DtcInfDoorDrvrBoolean4", 0)
        self.partner.ck_wti_no_warning_and_ck_resp("Door Reminder Due To Large Slope", "1")
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01,"DtcInfDoorDrvrBoolean3", 0)
        self.partner.ck_wti_warning_and_resp("Door Reminder Due To Large Slope", "0")
        
    @allure.title("电动门防玩和热保护提醒_主驾驶遍历热保护/防玩故障产生恢复") 
    @pytest.mark.full
    def test_caseid_1979870(self):  
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01,"DtcInfDoorDrvrBoolean1", 1)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01,"DtcInfDoorDrvrBoolean2", 1)
        self.partner.ck_wti_warning_and_resp("Door AntiPlay Reminder", 1)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01,"DtcInfDoorDrvrBoolean1", 0)
        self.partner.ck_wti_no_warning_and_ck_resp("Door AntiPlay Reminder", 1)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01,"DtcInfDoorDrvrBoolean2", 0)
        self.partner.ck_wti_warning_and_resp("Door AntiPlay Reminder", 0)
        
    @allure.title("WarningMsgList_门故障接口故障组合")
    @pytest.mark.full
    def test_caseid_1987820(self): 
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01,"DtcInfDoorDrvrBoolean1", 1) 
        self.io.drvr_door_open()
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01,"DtcInfDoorDrvrBoolean4", 1)
        self.partner.ck_wti_warning_and_resp("Door AntiPlay Reminder", 1)
        self.partner.ck_wti_warning_and_resp("Door Reminder Due To Large Slope", 1)
        self.set_door_fault("Drvr", 5, 1)
        self.partner.ck_wti_warning_and_resp("Driver Electric Door Warning", 1)
        self.set_door_fault("LeRe", 5, 1)
        self.partner.ck_wti_warning_and_resp("Sec Left Electric Door Warning", 1)
        self.set_door_fault("LeRe", 5, 0)
        self.partner.ck_wti_warning_and_resp("Sec Left Electric Door Warning", 0)
        self.set_door_fault("Drvr", 5, 0)
        self.partner.ck_wti_warning_and_resp("Driver Electric Door Warning", 0)
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01,"DtcInfDoorDrvrBoolean4", 0)
        self.partner.ck_wti_warning_and_resp("Door Reminder Due To Large Slope", 0)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01,"DtcInfDoorDrvrBoolean1", 0) 
        self.partner.ck_wti_warning_and_resp("Door AntiPlay Reminder", 0)
        
    @allure.title("WarningMsgList_多门产生多故障")
    @pytest.mark.full
    def test_caseid_1987870(self): 
        self.all_door_open_close(0)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01,"DtcInfDoorDrvrBoolean1", 1) 
        self.partner.ck_wti_warning_and_resp("Door AntiPlay Reminder", 1)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01,"DtcInfDoorPassBoolean1", 1) 
        self.partner.ck_wti_no_warning_and_ck_resp("Door AntiPlay Reminder", 1)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01,"DtcInfDoorLeReBoolean1", 1) 
        self.partner.ck_wti_no_warning_and_ck_resp("Door AntiPlay Reminder", 1)
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01,"DtcInfDoorRiReBoolean1", 1) 
        self.partner.ck_wti_no_warning_and_ck_resp("Door AntiPlay Reminder", 1)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01,"DtcInfDoorDrvrBoolean4", 1) 
        self.partner.ck_wti_warning_and_resp("Door Reminder Due To Large Slope", 1)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01,"DtcInfDoorPassBoolean4", 1) 
        self.partner.ck_wti_no_warning_and_ck_resp("Door Reminder Due To Large Slope", 1)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01,"DtcInfDoorLeReBoolean4", 1) 
        self.partner.ck_wti_no_warning_and_ck_resp("Door Reminder Due To Large Slope", 1)
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01,"DtcInfDoorRiReBoolean4", 1)
        self.partner.ck_wti_no_warning_and_ck_resp("Door Reminder Due To Large Slope", 1)
        self.set_door_fault("Drvr", 5, 1)
        self.partner.ck_wti_warning_and_resp("Driver Electric Door Warning", 1)
        self.set_door_fault("Pass", 5, 1)
        self.partner.ck_wti_warning_and_resp("Passenger Electric Door Warning", 1)
        self.set_door_fault("LeRe", 5, 1)
        self.partner.ck_wti_warning_and_resp("Sec Left Electric Door Warning", 1)
        self.set_door_fault("RiRe", 5, 1)
        self.partner.ck_wti_warning_and_resp("Sec Right Electric Door Warning", 1)  
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01,"DtcInfDoorPassBoolean1", 0) 
        self.partner.ck_wti_no_warning_and_ck_resp("Door AntiPlay Reminder", 1)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01,"DtcInfDoorPassBoolean4", 0) 
        self.partner.ck_wti_no_warning_and_ck_resp("Door Reminder Due To Large Slope", 1)     
                          
    @allure.title("WarningMsgList/GetWarningMsgList_热保护故障产生&童锁故障产生")
    @pytest.mark.full
    def test_caseid_1987819(self): 
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01,"DtcInfDoorLeReBoolean1", 0) 
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'ChdPrtnLeftFailStsToHmi', 0)
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01,"DtcInfDoorLeReBoolean1", 1) 
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'ChdPrtnLeftFailStsToHmi', 1)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01,"DtcInfDoorLeReBoolean2", 1) 
        self.partner.ck_wti_warning_and_resp("Door AntiPlay Reminder", 1)
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'ChdPrtnLeftFailStsToHmi', 0)
        self.partner.ck_wti_no_warning_and_ck_resp("Door AntiPlay Reminder", 1)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01,"DtcInfDoorLeReBoolean1", 0)
        self.partner.ck_wti_no_warning_and_ck_resp("Door AntiPlay Reminder", 1)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01,"DtcInfDoorLeReBoolean2", 0)  
        self.partner.ck_wti_warning_and_resp("Door AntiPlay Reminder", 0)            
                          
    @allure.title("WTI_主驾电动门故障报警") 
    @pytest.mark.smoke
    def test_caseid_1943290(self):
        self.set_door_fault_clear()
        last_info = 0              
        for Thermal in range(2):
            self.set_door_fault("Drvr", 5, Thermal)
            new_info = Thermal 
            self.ck_warningmsg("Driver Electric Door Warning", last_info, new_info, jump_trigger=True)

    @allure.title("WTI_副驾电动门故障报警") 
    @pytest.mark.sanity
    def test_caseid_1943289(self):
        self.set_door_fault_clear()
        last_info = 0
        for Thermal in range(2):
            self.set_door_fault("Pass", 5, Thermal)
            new_info = Thermal 
            self.ck_warningmsg("Passenger Electric Door Warning", last_info, new_info, jump_trigger=True)
            last_info = new_info
 
    @allure.title("WTI_左后电动门故障报警") 
    @pytest.mark.full
    def test_caseid_1943288(self):
        self.set_door_fault_clear()
        last_info = 0
        for Thermal in range(2):
            self.set_door_fault("LeRe", 5, Thermal)
            new_info = Thermal 
            self.ck_warningmsg("Sec Left Electric Door Warning", last_info, new_info, jump_trigger=True)
            last_info = new_info

    @allure.title("WTI_右后电动门故障报警") 
    @pytest.mark.full
    def test_caseid_1943287(self):
        self.set_door_fault_clear()
        last_info = 0
        for Thermal in range(2):
            new_info = Thermal 
            self.set_door_fault("RiRe", 5, Thermal)
            self.ck_warningmsg("Sec Right Electric Door Warning", last_info, new_info, jump_trigger=True) 
            last_info = new_info

    @allure.title("主驾驶门开报警信息_设置门开关_遍历P/N/R/D")
    @pytest.mark.sanity
    def test_caseid_1979890(self):
        self.io.drvr_door_close()
        self.dk.set_chassis_service_gear("NA")
        for door_sts in ['open', 'close']: #先进行第一循环NA挡位遍历门开门关，让其last_info=0
            logger.info(f"当前门开关状态为.{door_sts}")
            if door_sts == 'open':
                self.io.drvr_door_open()
            else:
                self.io.drvr_door_close()
            self.partner.empty_all(1)
            last_info = 0
            for gear in ["P", "N", "R", "D", "NA"]:
                logger.info(f"当前挡位为.{gear}")
                if door_sts == 'open' and gear in ["P", "N"]:
                    new_info = 4
                elif door_sts == 'open' and gear in ["D", "R"]:
                    new_info = 5
                else:
                    new_info = 0
                if gear in ["R","D"]:
                    self.sd_tester.change_usage_mode(13)
                self.dk.set_chassis_service_gear(gear)
                self.ck_warningmsg("Driver Door", last_info, new_info, jump_trigger=True)#当laset_info=new_info时不看信号跳变直接get
                last_info = new_info

    @allure.title("副驾驶门开报警信息_设置门开_遍历P/N/R/D")
    @pytest.mark.full
    def test_caseid_1979895(self):
        self.io.pass_door_close()  # 设置副驾门开
        self.dk.set_chassis_service_gear("NA")
        for door_sts in ['open', 'close']:
            logger.info(f"当前门开关状态为.{door_sts}")#先进行第一循环NA挡位遍历门开门关，让其last_info=0
            if door_sts == 'open':
                self.io.pass_door_open()
            else:
                self.io.pass_door_close()
            self.partner.empty_all(1)
            last_info = 0
            for gear in ["P", "N", "R", "D", "NA"]:
                logger.info(f"当前挡位为.{gear}")
                if door_sts == 'open' and gear in ["P", "N"]:
                    new_info = 4
                elif door_sts == 'open' and gear in ["D", "R"]:
                    new_info = 5
                else:
                    new_info = 0
                if gear in ["R","D"]:
                    self.sd_tester.change_usage_mode(13)
                self.dk.set_chassis_service_gear(gear)
                self.ck_warningmsg("Passenger Door", last_info, new_info, jump_trigger=True)#当laset_info=new_info时不看信号跳变直接get
                last_info = new_info
      
    @allure.title("左后门开报警信息_设置门开_遍历P/N/R/D")
    @pytest.mark.full
    def test_caseid_1979897(self):  
        self.io.lere_door_close()
        self.dk.set_chassis_service_gear("NA")
        for door_sts in ['open', 'close']: 
            if door_sts == 'open':
                self.io.lere_door_open()
            else:
                self.io.lere_door_close()
            self.partner.empty_all(1)
            last_info = 0
            for gear in ["P", "N", "R", "D", "NA"]:
                logger.info(f"当前挡位为.{gear},当前门开关状态为.{door_sts}")
                if door_sts == 'open' and gear in ["P", "N"]:
                    new_info = 4
                elif door_sts == 'open' and gear in ["D", "R"]:
                    new_info = 5
                else:
                    new_info = 0
                if gear in ["R","D"]:
                    self.sd_tester.change_usage_mode(13)
                self.dk.set_chassis_service_gear(gear)
                self.ck_warningmsg("Rear Left Door", last_info, new_info, jump_trigger=True)#当laset_info=new_info时不看信号跳变直接get
                last_info = new_info
        
    @allure.title("右后门开报警信息_设置门开_遍历P/N/D/R")
    @pytest.mark.full
    def test_caseid_1980319 (self):
        self.io.rire_door_close()
        self.dk.set_chassis_service_gear("NA")
        for door_sts in ['open', 'close']:
            if door_sts == 'open':
                self.io.rire_door_open()
            else:
                self.io.rire_door_close()
            self.partner.empty_all(1)
            last_info = 0
            for gear in ["P", "N", "R", "D", "NA"]:
                logger.info(f"当前挡位.{gear},当前门状态.{door_sts}")
                if door_sts == 'open' and gear in ["P", "N"]:
                    new_info = 4
                elif door_sts == 'open' and gear in ["D", "R"]:
                    new_info = 5
                else:
                    new_info = 0
                if gear in ["R","D"]:
                    self.sd_tester.change_usage_mode(13)
                self.dk.set_chassis_service_gear(gear)
                self.ck_warningmsg("Rear Right Door", last_info, new_info, jump_trigger=True)#当laset_info=new_info时不看信号跳变直接get
                last_info = new_info

    @allure.title("右后门开报警信息_遍历挡位P/N/D/R_设置门开")
    @pytest.mark.full
    def test_caseid_1979900 (self):
        self.io.rire_door_close()
        for gear in ["P", "N", "R", "D", "NA"]:
            self.dk.set_chassis_service_gear(gear)
            if gear in ["R", "D"]:
                self.sd_tester.change_usage_mode(13)
            elif gear in ["P", "N"]:
                self.sd_tester.change_usage_mode(2)
            else:
                sleep(5)
            self.partner.empty_all(1)
            last_info = 0
            for door_sts in ['open', 'close']:
                logger.info(f"当前门开关状态为.{door_sts}.当前挡位.{gear}")
                if door_sts == 'open':
                    self.io.rire_door_open()
                else:
                    self.io.rire_door_close()
                if door_sts == 'open' and gear in ["P", "N"]:
                    new_info = 4
                elif door_sts == 'open' and gear in ["D", "R"]:
                    new_info = 5
                else:
                    new_info = 0    
                self.ck_warningmsg("Rear Right Door", last_info, new_info, jump_trigger=True)#当laset_info=new_info时不看信号跳变直接get
                last_info = new_info  
        
    @allure.title("前舱盖报警信息_遍历挡位P/N/D/R_设置门开")
    @pytest.mark.smoke
    def test_caseid_1979940(self):
        self.tweer_hood_swith_control(1)
        for gear in ["P", "N", "R", "D", "NA"]:
            self.dk.set_chassis_service_gear(gear)
            if gear in ["R", "D"]:
                self.sd_tester.change_usage_mode(13)
            elif gear in ["P", "N"]:
                self.sd_tester.change_usage_mode(2)
            else:
                sleep(5)
            self.partner.empty_all(1)
            last_info = 0
            for door_sts in ['open', 'close']:
                logger.info(f"当前挡位.{gear},当前门.{door_sts}")
                if door_sts == 'open':
                    self.tweer_hood_swith_control(0)
                else:
                    self.tweer_hood_swith_control(1)
                if door_sts == 'open' and gear in ["P", "N"]:
                    new_info = 4
                elif door_sts == 'open' and gear in ["D", "R"]:
                    new_info = 5
                else:
                    new_info = 0    
                self.ck_warningmsg("Hood", last_info, new_info, jump_trigger=True)#当laset_info=new_info时不看信号跳变直接get
                last_info = new_info

    @allure.title("前舱盖报警信息_设置门开_遍历挡位P/N/D/R")
    @pytest.mark.full
    def test_caseid_1980318(self):
        self.tweer_hood_swith_control(1)
        self.dk.set_chassis_service_gear("NA")
        for door_sts in ['open', 'close']:
            if door_sts == 'open':
                self.tweer_hood_swith_control(0)
            else:
                self.tweer_hood_swith_control(1)
            self.partner.empty_all(1)
            last_info = 0
            for gear in ["P", "N", "R", "D", "NA"]:
                logger.info(f"当前挡位.{gear},当前门.{door_sts}")
                if door_sts == 'open' and gear in ["P", "N"]:
                    new_info = 4
                elif door_sts == 'open' and gear in ["D", "R"]:
                    new_info = 5
                else:
                    new_info = 0
                if gear in ["D", "R"]:
                    self.sd_tester.change_usage_mode(13)
                self.dk.set_chassis_service_gear(gear)
                self.ck_warningmsg("Hood", last_info, new_info, jump_trigger=True)#当laset_info=new_info时不看信号跳变直接get
                last_info = new_info 

    @allure.title("门雷达报警,主驾_0&1&2")#左前门毫米波雷达故障/请清理左前门毫米波雷达区域
    @pytest.mark.full
    def test_caseid_1979952(self):
        self.ipdu.set(self.ipdu.connectivitycanfd.DrmflConnectivityFr07, 'RadarDrvrSts', 0)
        self.partner.empty_all(1)
        last_info = 0
        for sigvalue in range(8):
            logger.info(f"当前信号值为.{sigvalue}")
            self.ipdu.set(self.ipdu.connectivitycanfd.DrmflConnectivityFr07, 'RadarDrvrSts', sigvalue)
            if sigvalue == 4:
               new_info = 1
            elif sigvalue == 5:
               new_info = 2
            elif sigvalue in [0,1,2,3]:
               new_info = 0
            else:
               last_info = new_info
            self.ck_warningmsg("Driver Radar Warning", last_info, new_info, jump_trigger=True)        
        sleep(1)
        
    @allure.title("门雷达报警,副驾_0&1&2")
    @pytest.mark.full
    def test_caseid_1979953(self):
        self.ipdu.set(self.ipdu.connectivitycanfd.DrmfrConnectivityFr07, 'RadarPassSts', 0)
        self.partner.empty_all(1)
        last_info = 0
        for sigvalue in range(8):
            logger.info(f"当前信号值为.{sigvalue}")
            self.ipdu.set(self.ipdu.connectivitycanfd.DrmfrConnectivityFr07, 'RadarPassSts', sigvalue)
            if sigvalue == 4:
               new_info = 1
            elif sigvalue == 5:
               new_info = 2
            elif sigvalue in [0,1,2,3]:
               new_info = 0
            else:
               last_info = new_info
            self.ck_warningmsg("Passenger Radar Warning", last_info, new_info, jump_trigger=True)
            last_info = new_info
        sleep(1)

    @allure.title("门雷达报警,左后_0&1&2")
    @pytest.mark.full
    def test_caseid_1979954(self):
        self.ipdu.set(self.ipdu.connectivitycanfd.DrmrlConnectivityFr07, 'RadarLeReSts', 0)
        self.partner.empty_all(1)
        last_info = 0
        for sigvalue in range(8):
            logger.info(f"当前信号值为.{sigvalue}")
            self.ipdu.set(self.ipdu.connectivitycanfd.DrmrlConnectivityFr07, 'RadarLeReSts', sigvalue)
            if sigvalue == 4:
               new_info = 1
            elif sigvalue == 5:
               new_info = 2
            elif sigvalue in [0,1,2,3]:
               new_info = 0
            else:
               last_info = new_info
            self.ck_warningmsg("Left Rear Radar Warning", last_info, new_info, jump_trigger=True)
            last_info = new_info
        sleep(1)

    @allure.title("门雷达报警,右后_0&1&2")
    @pytest.mark.sanity
    def test_caseid_1979955(self):
        self.ipdu.set(self.ipdu.connectivitycanfd.DrmrrConnectivityFr07, 'RadarRiReSts', 0)
        self.partner.empty_all(1)
        last_info = 0
        for sigvalue in range(8):
            logger.info(f"当前信号值为.{sigvalue}")
            self.ipdu.set(self.ipdu.connectivitycanfd.DrmrrConnectivityFr07, 'RadarRiReSts', sigvalue)
            if sigvalue == 4:
               new_info = 1
            elif sigvalue == 5:
               new_info = 2
            elif sigvalue in [0,1,2,3]:
               new_info = 0
            else:
               last_info = new_info
            self.ck_warningmsg("Right Rear Radar  Warning", last_info, new_info, jump_trigger=True)
            last_info = new_info
        sleep(1)
          
    @allure.title("通知/获取车门破冰提醒_全部车门破冰提醒")
    @pytest.mark.sanity
    def test_caseid_111721(self):
        self.set_Actv_sig_all(0)
        self.partner.empty_all(1)
        last_info = 0    
        for sigvalue in range(2):
            logger.info(f"当前信号值为.{sigvalue}")
            self.set_Actv_sig_all(sigvalue)
            new_info = 1 if sigvalue else 0
            self.ck_warningmsg("Door Ice Break Reminder", last_info, new_info, jump_trigger=True)
            last_info = new_info
        sleep(1)
        
    @allure.title("通知/获取车门破冰提醒_单门车门破冰提醒")
    @pytest.mark.full
    def test_caseid_1987806(self):
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, 'IceBreakDoorDrvrActv', 0)
        self.partner.empty_all(0.1)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, 'IceBreakDoorDrvrActv', 1)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'IceBreakDoorPassActv', 0)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr02, 'IceBreakDoorLeReActv', 0)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr02, 'IceBreakDoorRiReActv', 0)
        self.partner.ck_wti_warning_and_resp("Door Ice Break Reminder", 1) 
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'IceBreakDoorPassActv', 1)
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, 'IceBreakDoorDrvrActv', 0)
        self.partner.ck_wti_no_warning_and_ck_resp("Door Ice Break Reminder", 1)
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'IceBreakDoorPassActv', 0)
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr02, 'IceBreakDoorLeReActv', 1)
        self.partner.ck_wti_warning_and_resp("Door Ice Break Reminder", 1)
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr02, 'IceBreakDoorRiReActv', 1)
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr02, 'IceBreakDoorLeReActv', 0)
        self.partner.ck_wti_no_warning_and_ck_resp("Door Ice Break Reminder", 1)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr02, 'IceBreakDoorRiReActv', 0)
        self.partner.ck_wti_warning_and_resp("Door Ice Break Reminder", 0)
   
    @allure.title("WTI_整车重启非P挡WTI提示_kNotInPark")
    @pytest.mark.smoke
    def test_caseid_1989307(self):               
        self.partner.send_method_request(OBTDIAG_SERVICE_CLIENT, "SetRestart",  {"req": {"source": 1}})
        self.sd_tester.change_usage_mode(13)
        self.dk.set_chassis_service_gear("D")
        self.partner.ck_wti_warning_and_resp("VehicleRestartUnderNotPGear", 1)
        sleep(4)
        self.partner.ck_wti_warning_and_resp("VehicleRestartUnderNotPGear", 0)
        
    @allure.title("WTI_整车重启非P挡WTI提示_4s计时器后再次切kNotInPark")
    @pytest.mark.full
    def test_caseid_1989327(self):  
        self.partner.send_method_request(OBTDIAG_SERVICE_CLIENT, "SetRestart",  {"req": {"source": 1}})
        self.sd_tester.change_usage_mode(13)
        self.dk.set_chassis_service_gear("D")
        self.partner.ck_wti_warning_and_resp("VehicleRestartUnderNotPGear", 1)
        sleep(4)
        self.partner.send_method_request(OBTDIAG_SERVICE_CLIENT, "SetRestart",  {"req": {"source": 1}})
        self.partner.ck_wti_warning_and_resp("VehicleRestartUnderNotPGear", 1)
        
    @allure.title("WTI_整车重启非P挡WTI提示_计时器内切为P档&driving")
    @pytest.mark.full
    def test_caseid_1989326(self):  
        self.partner.send_method_request(OBTDIAG_SERVICE_CLIENT, "SetRestart",  {"req": {"source": 1}})
        self.sd_tester.change_usage_mode(13)
        self.dk.set_chassis_service_gear("D")
        self.partner.ck_wti_warning_and_resp("VehicleRestartUnderNotPGear", 1)
        self.partner.empty_all(1)
        self.dk.set_chassis_service_gear("P")
        sleep(3)
        self.partner.ck_wti_warning_and_resp("VehicleRestartUnderNotPGear", 0)

@allure.feature("SOA服务接口")
@allure.story("WTIService_Door")
@pytest.mark.jishu1
class TestDoorWTIService_Remote(TestBase):
    
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.nucapp.tcam_power_off()
        time.sleep(30)
        self.partner = S2sBaseClass([
            (REMOTECTRL_SERVICE_SERVER),
            ("WTIService", "client")
        ])
        self.partner.method_default_timeout = 0.1

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.partner.stop_operators()
        self.nucapp.tcam_power_on()
        sleep(120)
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.partner.empty_all()

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)
    
    @allure.title("通知/获取无钥匙驾驶已启动_Default&Ready2R&UnlockWait&ReadyEntry&Entry&Ready2L")#beta2
    @pytest.mark.full
    def test_caseid_1985632(self):  
        self.partner.send_event_notify(REMOTECTRL_SERVICE_SERVER, "RemoteAuthStartModeSts",
                                       {"info" : {"sts" : 4, "time" : 0xFFFFFFFF}}) 
        self.partner.empty_all(1)
        self.partner.send_event_notify(REMOTECTRL_SERVICE_SERVER, "RemoteAuthStartModeSts",
                                       {"info" : {"sts" : 1, "time" : 0xFFFFFFFF}})
        self.partner.ck_wti_warning_and_resp("Remote Auth Start", 0)
        self.partner.send_event_notify(REMOTECTRL_SERVICE_SERVER, "RemoteAuthStartModeSts", 
                                       {"info" : {"sts" : 1, "time" : 0xFFFFFFFF}})
        self.partner.ck_wti_no_warning_and_ck_resp("Remote Auth Start", 0)
        self.partner.send_event_notify(REMOTECTRL_SERVICE_SERVER, "RemoteAuthStartModeSts",
                                       {"info" : {"sts" : 2, "time" : 0xFFFFFFFF}})
        self.partner.ck_wti_no_warning_and_ck_resp("Remote Auth Start", 0)
        self.partner.send_event_notify(REMOTECTRL_SERVICE_SERVER, "RemoteAuthStartModeSts", 
                                       {"info" : {"sts" : 3, "time" : 0xFFFFFFFF}})
        self.partner.ck_wti_warning_and_resp("Remote Auth Start", 1)
        self.partner.send_event_notify(REMOTECTRL_SERVICE_SERVER, "RemoteAuthStartModeSts", 
                                       {"info" : {"sts" : 4, "time" : 0xFFFFFFFF}})
        self.partner.ck_wti_no_warning_and_ck_resp("Remote Auth Start", 1)
        self.partner.send_event_notify(REMOTECTRL_SERVICE_SERVER, "RemoteAuthStartModeSts", 
                                       {"info" : {"sts" : 5, "time" : 0xFFFFFFFF}})
        self.partner.ck_wti_warning_and_resp("Remote Auth Start", 0)

    @allure.title("通知/获取无钥匙驾驶已启动_Default")#beta2
    @pytest.mark.full
    def test_caseid_1985631(self):  
        self.partner.send_event_notify(REMOTECTRL_SERVICE_SERVER, "RemoteAuthStartModeSts",
                                       {"info" : {"sts" : 4, "time" : 0xFFFFFFFF}})
        self.partner.empty_all(1)
        self.partner.send_event_notify(REMOTECTRL_SERVICE_SERVER, "RemoteAuthStartModeSts", 
                                       {"info" : {"sts" : 0, "time" : 0xFFFFFFFF}})
        self.partner.ck_wti_warning_and_resp("Remote Auth Start", 0)

    @allure.title("通知/获取无钥匙驾驶已启动_Entry&Ready2L")#beta2
    @pytest.mark.full
    def test_caseid_1985630(self):  
        self.partner.send_event_notify(REMOTECTRL_SERVICE_SERVER, "RemoteAuthStartModeSts", 
                                       {"info" : {"sts" : 2, "time" : 0xFFFFFFFF}})
        self.partner.empty_all(1)
        self.partner.send_event_notify(REMOTECTRL_SERVICE_SERVER, "RemoteAuthStartModeSts", 
                                       {"info" : {"sts" : 4, "time" : 0xFFFFFFFF}})
        self.partner.ck_wti_warning_and_resp("Remote Auth Start", 1)
        self.partner.send_event_notify(REMOTECTRL_SERVICE_SERVER, "RemoteAuthStartModeSts",
                                       {"info" : {"sts" : 5, "time" : 0xFFFFFFFF}})
        self.partner.ck_wti_warning_and_resp("Remote Auth Start", 0)

    @allure.title("通知/获取无钥匙驾驶已启动_Entry&Default")#beta2
    @pytest.mark.sanity
    def test_caseid_1985629(self):  
        self.partner.send_event_notify(REMOTECTRL_SERVICE_SERVER, "RemoteAuthStartModeSts",
                                       {"info" : {"sts" : 2, "time" : 0xFFFFFFFF}})
        self.partner.empty_all(1)
        self.partner.send_event_notify(REMOTECTRL_SERVICE_SERVER, "RemoteAuthStartModeSts", 
                                       {"info" : {"sts" : 4, "time" : 0xFFFFFFFF}})
        self.partner.ck_wti_warning_and_resp("Remote Auth Start", 1)
        self.partner.send_event_notify(REMOTECTRL_SERVICE_SERVER, "RemoteAuthStartModeSts", 
                                       {"info" : {"sts" : 0, "time" : 0xFFFFFFFF}})
        self.partner.ck_wti_warning_and_resp("Remote Auth Start", 0)      
            
    @allure.title("通知/获取无钥匙驾驶已启动_ReadyEntry")#beta2
    @pytest.mark.sanity
    def test_caseid_1985628(self):  
        self.partner.send_event_notify(REMOTECTRL_SERVICE_SERVER, "RemoteAuthStartModeSts", 
                                       {"info" : {"sts" : 2, "time" : 0xFFFFFFFF}})
        self.partner.empty_all(1)
        self.partner.send_event_notify(REMOTECTRL_SERVICE_SERVER, "RemoteAuthStartModeSts", 
                                       {"info" : {"sts" : 3, "time" : 0xFFFFFFFF}})
        self.partner.ck_wti_warning_and_resp("Remote Auth Start", 1)
        self.partner.send_event_notify(REMOTECTRL_SERVICE_SERVER, "RemoteAuthStartModeSts",
                                       {"info" : {"sts" : 3, "time" : 0xFFFFFFFF}})
        self.partner.ck_wti_no_warning_and_ck_resp("Remote Auth Start", 1)      
  
    @allure.title("通知/获取无钥匙驾驶已启动_UnlockWait")#beta2
    @pytest.mark.full
    def test_caseid_1985627(self):  
        self.partner.send_event_notify(REMOTECTRL_SERVICE_SERVER, "RemoteAuthStartModeSts",
                                       {"info" : {"sts" : 3, "time" : 0xFFFFFFFF}})
        self.partner.empty_all(1)
        self.partner.send_event_notify(REMOTECTRL_SERVICE_SERVER, "RemoteAuthStartModeSts", 
                                       {"info" : {"sts" : 2, "time" : 0xFFFFFFFF}})
        self.partner.ck_wti_warning_and_resp("Remote Auth Start", 0)             
            
    @allure.title("通知/获取无钥匙驾驶已启动_Ready2R")#beta2
    @pytest.mark.full
    def test_caseid_1985626(self):  
        self.partner.send_event_notify(REMOTECTRL_SERVICE_SERVER, "RemoteAuthStartModeSts",
                                       {"info" : {"sts" : 4, "time" : 0xFFFFFFFF}})
        self.partner.empty_all(1)
        self.partner.send_event_notify(REMOTECTRL_SERVICE_SERVER, "RemoteAuthStartModeSts", 
                                       {"info" : {"sts" : 1, "time" : 0xFFFFFFFF}})
        self.partner.ck_wti_warning_and_resp("Remote Auth Start", 0)  
        
        
@allure.feature("SOA服务接口")
@allure.story("WTIService_Door")
@pytest.mark.jishu1
class TestDoorWTIService_obt(TestBase):
    
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        for process_name in ["monitor_em2.sh", "em2", "calibration"]:
            res = command_send(
                device_name="BGM",
                cmd=f"ps -ef |grep app |grep {process_name} |grep -v grep",
                timeout=60,
            )[1]
            pid = res.split()[1]
            command_send(device_name="BGM", cmd=f"kill -9 {pid}")
        sleep(60)
        self.partner = S2sBaseClass([
            ("ObtDiagService", "server"),
            ("WTIService", "client")
        ])
        self.partner.method_default_timeout = 0.1

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.partner.stop_operators()
        self.bgm_power_off_and_on()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.partner.empty_all()
        
    @allure.title("WTI_整车重启非P挡WTI提示_kUpdating跳变kNotInPark跳变kUpdating")
    @pytest.mark.full
    def test_caseid_1989309(self):  
        self.partner.send_event_notify("ObtDiagService_server", "RestartStatus",
                                      {"status":{"mainState":2,"notification":2}})
        self.partner.ck_wti_no_warning_and_ck_resp("VehicleRestartUnderNotPGear", 0)
        self.partner.empty_all(1)
        self.partner.send_event_notify("ObtDiagService_server", "RestartStatus",
                                      {"status":{"mainState":2,"notification":1}})
        self.partner.ck_wti_warning_and_resp("VehicleRestartUnderNotPGear", 1)
        self.partner.empty_all(1)
        self.partner.send_event_notify("ObtDiagService_server", "RestartStatus",
                                      {"status":{"mainState":2,"notification":2}})
        self.partner.ck_wti_no_warning_and_ck_resp("VehicleRestartUnderNotPGear", 1)

    @allure.title("WTI_整车重启非P挡WTI提示_kUpdating跳变kNotInPark跳变kUpdating")
    @pytest.mark.sanity
    def test_caseid_1989308(self):  
        self.partner.send_event_notify("ObtDiagService_server", "RestartStatus",
                                      {"status":{"mainState":2,"notification":1,"telematicsState":0,"autoDrivingState":0,"cockpitState":0,"digitalKeyState":0}})
        self.partner.ck_wti_warning_and_resp("VehicleRestartUnderNotPGear", 1)
        self.partner.empty_all(2)
        self.partner.send_event_notify("ObtDiagService_server", "RestartStatus",
                                      {"status":{"mainState":2,"notification":2,"telematicsState":0,"autoDrivingState":0,"cockpitState":0,"digitalKeyState":0}})
        self.partner.ck_wti_no_warning_and_ck_resp("VehicleRestartUnderNotPGear", 1)
        sleep(2)
        self.partner.ck_wti_warning_and_resp("VehicleRestartUnderNotPGear", 0)