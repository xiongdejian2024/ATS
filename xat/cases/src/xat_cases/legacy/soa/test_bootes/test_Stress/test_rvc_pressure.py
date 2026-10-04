#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time       : 2023/02/2.p8 15:00
@FileName   : test_rvc_pressure.py
@Author     : jishu.duan_ext
@Description: 远程车控压测
"""
import os
import sys
import time
import threading
import pytest
import allure
import datetime
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.soa.case_helper.test_base import *
from xat_ecu.legacy.common.logmanagment.logmanager import *
from xat_ecu.legacy.interface.nuc_app import *
from xat_ecu.legacy.sdk.ecu_simulator_app import Ecu_Sim_App
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.ecu_sim.parse_tb_config import ParseTBConfig
from xat_ecu.legacy.interface.nuc_app import *
from xat_ecu.legacy.sdk.i_signal_i_pdu import ISignalIPdu
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.sdk.bus_app import BusApp
from xat_ecu.legacy.config.path import CONFIG_DIR_PATH
from xat_ecu.legacy.interface.ecuinterface import *
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.soa_partner.src.base_partner import *


@allure.feature("性能稳定性")
@allure.story("业务稳定性/启动场景压测--休眠远控")
class TestUnLockCtrl(TestBase):
    
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.tsp = Tsp(**self.tc_config)
        self.tsp.set_bench_config(self.tb_config["vid"], self.tb_config["tel"])
        self.nucapp = NucApp(self.tc_config)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.ecu_interface = EcuInterFace(ipdu=self.ipdu,nucapp=self.nucapp, dk=self.dk, cfg=self.tc_config, io_obj=self.io)
        self.partner = S2sBaseClass([("VehicleSetStatusService","client")])
        sleep(1)
        self.partner.wait_for_service_reconnect(VEHICLESETSTATUS_CLIENT, timeout=200)
        self.partner.send_method_request(
            VEHICLESETSTATUS_CLIENT, "SetMaintenanceMode", {"isOn": True})
        sleep(0.5)
        self.partner.send_method_request(
            VEHICLESETSTATUS_CLIENT, "SetMaintenanceMode", {"isOn": False})

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        self.partner.stop_operators()
        self.dk.stop_listen_dk_bgm_response()
        super().after_class(self, ecu)
   
    @pytest.mark.full
    @allure.title("整车休眠后远程控制空调开启_5次") 
    def test_caseid_1979912(self, ecu): 
        i,j = 0,0
        s = 0
        for n in range(5): 
            self.ecu_interface.enter_network_sleep()  
            time.sleep(300) # 等待3分钟
            logger.info("已休眠")
            try:                
                with allure.step('模拟云端下发远控开启空调指令'):                
                    self.tsp.rvc_ac_control(1, 220) #1: 开空调, -1:关闭空调（0：Lo，1：Hi, 160~280）
                    start_time = time.time()
                    logger.info(f"1、{start_time}")
                    logger.info("已发送空调开启请求")
                    NMtime = time.time()
                    logger.info(f"2、{NMtime}")
                    NMT = float(NMtime - start_time)+0.7
                    logger.info("TCAM唤醒时延{}s".format(NMT))
                    result1, realvalue1, expectedvalue1 = self.ipdu.check(self.ipdu.bodycan.CemBodyFr84, 'RemStrtHvCtrlReqErsCmd', 'ErsCmd_ErsCmdOn',timeout = 20, do_assert = False)#远控上高压
                    logger.info("result1 {}, realvalue1 {}, expectedvalue1 {}".format(result1, realvalue1, expectedvalue1))
                    assert result1,"15s内是否发出远控上高压请求" 
                    time.sleep(2.5)
                    self.ipdu.set(self.ipdu.bodycan.CcmBodyFr22, 'RemClimaHvSts_0_CcmBodySignalIPdu22', 'OnOff1_On')
                    result2, realvalue2, expectedvalue2 = self.ipdu.check(self.ipdu.bodycan.CemBodyFr47, 'TelmClimaReq', 'OnOffNoReq_On',timeout = 20, do_assert = False)#远控空调开启
                    logger.info("result2 {}, realvalue2 {}, expectedvalue2 {}".format(result2, realvalue2, expectedvalue2))
                    assert result2,"20s内是否发出远控开启空调请求"
                    self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv_0_CcmBodySignalIPdu03', 1)
                    end_time = time.time()
                    t = end_time - start_time
                    s = s + t
                    i = i+1
                    logger.info("远控开启空调成功时延{}s".format(t))
                    logger.info("远控开启空调成功{}次".format(i))
                    logger.info("远控开启空调失败{}次".format(j))
                    logger.info("远控开启空调总{}次".format(i+j))
                    logger.info("远控空调执行总时间{}".format(s))
                    time.sleep(5)
                    self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 'OnOff1_Off')
                    self.ipdu.set(self.ipdu.bodycan.CcmBodyFr22, 'RemClimaHvSts', 'OnOff1_Off')
                    logger.info("空调已关闭")
                    self.nucapp.bgm_diag_line_up()  # bgm诊断激活线连接(1是连接，0是断开)
                    self.nucapp.tcam_kl15_up() # TCAM KL15电连接（1是连接，0是断开）
                    time.sleep(180)
            except:
                self.nucapp.bgm_diag_line_up()  # bgm诊断激活线连接(1是连接，0是断开)
                self.nucapp.tcam_kl15_up() # TCAM KL15电连接（1是连接，0是断开）
                time.sleep(5)
                j = j+1
                self.bgmcli = BGM_SSH('172.16.5.1')
                logger.info("用例执行失败，第 {} 次".format(j))
                assert self.bgmcli.get_ping(ip="172.16.5.31", num=4, root_permission=False)
                time.sleep(180)
                
    @pytest.mark.full
    @allure.title("整车休眠后远程控制开启充电盖_5次") 
    def test_caseid_1979915(self, ecu):
        i,j = 0,0
        s = 0
        for n in range(5):
            self.ecu_interface.enter_network_sleep(0)
            time.sleep(300) # 等待3分钟
            logger.info("已休眠")
            try:                
                with allure.step('模拟云端下发远控开启充电盖指令'):
                    self.tsp.rvc_charge_Lidgate(1) #"op充电口盖(1: 开，-1: 关)"                
                    start_time = time.time()
                    logger.info(f"1、{start_time}")
                    logger.info("已发送充电盖开启请求")
                    NMtime = time.time()
                    logger.info(f"2、{NMtime}")
                    NMT = float(NMtime - start_time)+0.2
                    logger.info("TCAM唤醒时延{}s".format(NMT))
                    rec_data = self.ipdu.recv_pdu("backbonefr", "BgmBackboneFRNmFr", timeout=20)
                    logger.info("{}".format(rec_data))
                    self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 0)
                    self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 1)
                    result1, realvalue1, expectedvalue1 =  self.ipdu.check(self.ipdu.cem_lin2.CemCem_Lin2Fr06, 'ChrgLidManvgDCorAcDcReq2', 0,timeout = 20, do_assert = False)#远控充电盖开启
                    logger.info("result1 {}, realvalue1 {}, expectedvalue1 {}".format(result1, realvalue1, expectedvalue1))
                    assert result1,"20s内是否发出远控开启充电盖请求"
                    self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcActPosn2', 100)
                    result, realvalue, expectedvalue = self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr09, 'ChrgLidRearSts_0_CEMBackBoneSignalIpdu09', 1,timeout = 20, do_assert = False) 
                    logger.info("result {}, realvalue {}, expectedvalue {}".format(result, realvalue, expectedvalue))
                    assert result,"20s内充电盖是否为开启"
                    end_time = time.time()
                    t = end_time - start_time
                    s = s + t
                    i = i+1
                    logger.info("远控开启充电盖成功时延{}s".format(t))
                    logger.info("远控开启充电盖成功{}次".format(i))
                    logger.info("远控开启充电盖失败{}次".format(j))
                    logger.info("远控开启充电盖总{}次".format(i+j))
                    logger.info("远控充电盖执行总时间{}".format(s))
                    time.sleep(5)
                    self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcActPosn2', 0)
                    logger.info("充电盖已关闭")
                    self.nucapp.bgm_diag_line_up()  # bgm诊断激活线连接(1是连接，0是断开)
                    self.nucapp.tcam_kl15_up() # TCAM KL15电连接（1是连接，0是断开）
                    time.sleep(180)
            except:
                self.nucapp.bgm_diag_line_up()  # bgm诊断激活线连接(1是连接，0是断开)
                self.nucapp.tcam_kl15_up() # TCAM KL15电连接（1是连接，0是断开）
                time.sleep(15)
                j = j+1
                self.bgmcli = BGM_SSH('172.16.5.1')
                logger.info("用例执行失败，第 {} 次".format(j))
                assert self.bgmcli.get_ping(ip="172.16.5.31", num=4, root_permission=False)
                time.sleep(60)
                
    @pytest.mark.full
    @allure.title("整车休眠后远程控制尾门打开_5次") 
    def test_caseid_1979918(self, ecu):
        i,j = 0,0
        s = 0
        for n in range(5):
            self.ecu_interface.enter_network_sleep(0)  
            time.sleep(180) # 等待3分钟 
            logger.info("已休眠")
            try:                
                with allure.step('模拟云端下发远控尾门开启指令'):
                    self.tsp.rvc_tailgate_control(1) #-1,关闭;1,开启;(全开, "position":0;翘起, "position":15)            
                    start_time = time.time()
                    logger.info(f"1、{start_time}")
                    logger.info("已发送尾门开启请求")
                    NMtime = time.time()
                    logger.info(f"2、{NMtime}")
                    NMT = float(NMtime - start_time)+0.2
                    logger.info("TCAM唤醒时延{}s".format(NMT))
                    x,y,z = self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr01, 'VehModMngtGlbSafe1UsgModSts_4_VgmConnSignalIPdu01', 'UsgModSts1_UsgModInActv', timeout = 20, do_assert = False)
                    logger.info(x)
                    assert x,"15s内是否为Inactive" 
                    #发送网络管理526报文
                    msg = [0x26, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                    self.ipdu.send_pdu("propulsioncan", 0x526, msg, cycle_time=1)
                    logger.info("已发送网络管理526")
                    time.sleep(1)
                    #设置档位为P档
                    self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
                    self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn_1_EcmPropSignalIPdu24', 'GearLvrIndcn2_ParkIndcn')
                    logger.info("已发送档位为P档")
                    #设置尾门开度为关闭
                    self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts_0_PotBodySignalIPdu02', 'TrOpenerSts1_FullClsd')
                    time.sleep(1)
                    logger.info("尾门关闭")
                    time.sleep(1)
                    a,b,c = self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 'TrOpenerReq1_TrOpenerOpen', timeout = 20, do_assert = False)
                    logger.info(a)
                    logger.info(b)
                    assert a,"20s内是否发出尾门开启请求"
                    self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts_0_PotBodySignalIPdu02', 'TrOpenerSts1_FullOpend') 
                    end_time = time.time()
                    t = end_time - start_time
                    s = s + t
                    i = i+1
                    logger.info("远控开启尾门成功时延{}s".format(t))
                    logger.info("远控开启尾门成功{}次".format(i))
                    logger.info("远控开启尾门失败{}次".format(j))
                    logger.info("远控开启尾门总{}次".format(i+j))
                    logger.info("远控尾门执行总时间{}".format(s))
                    time.sleep(1)
                    self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv_0_CcmBodySignalIPdu03', 'OnOff1_Off')
                    self.ipdu.set(self.ipdu.bodycan.CcmBodyFr22, 'RemClimaHvSts_0_CcmBodySignalIPdu22', 'OnOff1_Off')
                    logger.info("尾门已关闭") 
                    self.nucapp.bgm_diag_line_up()  # bgm诊断激活线连接(1是连接，0是断开)
                    self.nucapp.tcam_kl15_up() # TCAM KL15电连接（1是连接，0是断开）  
                    time.sleep(180) # 持续3分钟下切abandon       
                        
            except:
                self.nucapp.bgm_diag_line_up()  # bgm诊断激活线连接(1是连接，0是断开)
                self.nucapp.tcam_kl15_up() # TCAM KL15电连接（1是连接，0是断开）
                time.sleep(5)
                j = j+1
                self.bgmcli = BGM_SSH('172.16.5.1')
                logger.info("用例执行失败，第 {} 次".format(j))
                assert self.bgmcli.get_ping(ip="172.16.5.31", num=4, root_permission=False)
                time.sleep(60)  
              
    @pytest.mark.full  #case注意
    @allure.title("整车休眠后远控开启除霜_5次") 
    def test_caseid_1979923(self, ecu):
        i,j = 0,0
        s = 0
        for n in range(5):
            self.ecu_interface.enter_network_sleep()
            time.sleep(300) # 等待3分钟
            logger.info("已休眠")
            try:                
                with allure.step('模拟云端下发远控开启除霜指令'):  
                    self.tsp.rvc_defrost_control(1) #1: 开除霜, -1:关闭除霜                 
                    start_time = time.time()
                    logger.info(f"1、{start_time}")
                    logger.info("已发送除霜开启请求")
                    NMtime = time.time()
                    logger.info(f"2、{NMtime}")
                    NMT = float(NMtime - start_time)+0.7
                    logger.info("TCAM唤醒时延{}s".format(NMT))
                    result1, realvalue1, expectedvalue1 = self.ipdu.check(self.ipdu.bodycan.CemBodyFr84, 'RemStrtHvCtrlReqErsCmd', 'ErsCmd_ErsCmdOn',timeout = 20, do_assert = False)#远控上高压
                    logger.info("result1 {}, realvalue1 {}, expectedvalue1 {}".format(result1, realvalue1, expectedvalue1))
                    assert result1,"15s内是否发出远控上高压请求" 
                    time.sleep(2.5)
                    self.ipdu.set(self.ipdu.bodycan.CcmBodyFr22, 'RemClimaHvSts_0_CcmBodySignalIPdu22', 'OnOff1_On')
                    result2, realvalue2, expectedvalue2 = self.ipdu.check(self.ipdu.bodycan.CemBodyFr92, 'TelmSteerWhlHeatgReqLvl', 'TelmSeatClimaLvl_Lvl3',timeout = 20, do_assert = False)#远控除霜开启
                    logger.info("result2 {}, realvalue2 {}, expectedvalue2 {}".format(result2, realvalue2, expectedvalue2))
                    assert result2,"20s内是否发出远控开启除霜请求"
                    self.ipdu.set(self.ipdu.bodycan.CcmBodyFr31, 'RemClimaDefrstSts_0_CcmBodySignalIPdu31', 'OnOff1_On')
                    end_time = time.time()
                    t = end_time - start_time
                    s = s + t
                    i = i+1
                    logger.info("远控开启除霜成功时延{}s".format(t))
                    logger.info("远控开启除霜成功{}次".format(i))
                    logger.info("远控开启除霜失败{}次".format(j))
                    logger.info("远控开启除霜总{}次".format(i+j))
                    logger.info("远控除霜执行总时间{}".format(s))
                    time.sleep(5)
                    self.ipdu.set(self.ipdu.bodycan.CcmBodyFr11, 'RemClimaDefrstSts_0_CcmBodySignalIPdu31', 'OnOff1_Off')
                    self.ipdu.set(self.ipdu.bodycan.CcmBodyFr22, 'RemClimaHvSts_0_CcmBodySignalIPdu22', 'OnOff1_Off')
                    logger.info("除霜已关闭")
                    self.nucapp.bgm_diag_line_up()  # bgm诊断激活线连接(1是连接，0是断开)
                    self.nucapp.tcam_kl15_up() # TCAM KL15电连接（1是连接，0是断开）
                    time.sleep(180) # 持续3分钟下切abandon            
            except:
                self.nucapp.bgm_diag_line_up()  # bgm诊断激活线连接(1是连接，0是断开)
                self.nucapp.tcam_kl15_up() # TCAM KL15电连接（1是连接，0是断开）
                time.sleep(5)
                j = j+1
                self.bgmcli = BGM_SSH('172.16.5.1')
                logger.info("用例执行失败，第 {} 次".format(j))
                assert self.bgmcli.get_ping(ip="172.16.5.31", num=4, root_permission=False)   
                time.sleep(60)
                
    @pytest.mark.full
    @allure.title("整车休眠后远程控制解闭锁_5次") 
    def test_caseid_1979919(self, ecu):
        i,j = 0,0
        s = 0
        for n in range(5):
            self.ecu_interface.enter_network_sleep()
            time.sleep(300) # 等待3分钟
            logger.info("已休眠")
            try:                
                with allure.step('模拟云端下发远控解锁指令'):
                    self.tsp.rvc_lock_control(1) #1: 解锁, 2:闭锁, 3: 关门+闭锁
                    start_time = time.time()
                    logger.info(f"1、{start_time}")                  
                    start_time = time.time()
                    logger.info(f"1、{start_time}")
                    logger.info("已发送解锁请求")
                    NMtime = time.time()
                    logger.info(f"2、{NMtime}")
                    NMT = float(NMtime - start_time) + 0.7
                    logger.info("TCAM唤醒时延{}s".format(NMT))
                    a,b = self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr01, 'DoorDrvrLockCmd', 1), 
                                                    (self.ipdu.bodycan.CemBodyFr01, 'DoorPassLockCmd', 1),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'DoorLeReLockCmd', 1),
                                                    (self.ipdu.bodycan.CemBodyFr01, 'DoorRiReLockCmd', 1)],timeout = 20, do_assert = False)
                    logger.info(a)
                    logger.info(b)                
                    end_time = time.time()
                    t = end_time - start_time
                    logger.info(t)
                    s = s + t
                    assert a,"20s内是否发出解锁请求"
                    i = i + 1
                    logger.info("远控解锁成功{}次".format(i))
                    logger.info("用例执行失败，第 {} 次".format(j))
                    logger.info("用例执行总计 {} 次".format(i+j))
                    logger.info("远控解锁执行总时间{}".format(s))
                    self.nucapp.bgm_diag_line_up()  # bgm诊断激活线连接(1是连接，0是断开)
                    self.nucapp.tcam_kl15_up() # TCAM KL15电连接（1是连接，0是断开）
                    time.sleep(180) # 持续3分钟下切abandon
            except:
                self.nucapp.bgm_diag_line_up()  # bgm诊断激活线连接(1是连接，0是断开)
                self.nucapp.tcam_kl15_up() # TCAM KL15电连接（1是连接，0是断开）
                time.sleep(5)
                j = j + 1
                self.bgmcli = BGM_SSH('172.16.5.1')
                logger.info("用例执行失败，第 {0} 次".format(j))
                assert self.bgmcli.get_ping(ip="172.16.5.31", num=10, root_permission=False)   
                time.sleep(60)
    
    @pytest.mark.full
    @allure.title("整车休眠后远控寻车-闪灯鸣笛_5次") 
    def test_caseid_1979922(self, ecu):
        i,j = 0,0
        s = 0
        for n in range(5):
            self.ecu_interface.enter_network_sleep()
            time.sleep(300) # 等待3分钟
            logger.info("已休眠")
            try: 
                with allure.step('模拟云端下发远控闪灯鸣笛指令'):
                    self.tsp.rvc_find_vehicle(1) #-1,关闭;1,鸣笛闪灯;2,仅闪灯                   
                    start_time = time.time()
                    logger.info(f"1、{start_time}")
                    logger.info("已发送闪灯鸣笛请求")
                    NMtime = time.time()
                    logger.info(f"2、{NMtime}")
                    NMT = float(NMtime - start_time)+0.7
                    logger.info("TCAM唤醒时延{}s".format(NMT))
                    a,b,c = self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr05, 'CarLoctrActvnSts', 1, timeout = 20, do_assert = False)
                    logger.info(a)
                    logger.info(b)
                    end_time = time.time()
                    t = end_time - start_time
                    logger.info(t)
                    s = s + t
                    assert a,"20s内寻车状态是否为1"
                    i = i + 1
                    logger.info("远控寻车成功{}次".format(i))
                    logger.info("用例执行失败，第 {} 次".format(j))
                    logger.info("用例执行总计 {} 次".format(i+j))
                    logger.info("远控寻车执行总时间{}".format(s))
                    self.nucapp.bgm_diag_line_up()  # bgm诊断激活线连接(1是连接，0是断开)
                    self.nucapp.tcam_kl15_up() # TCAM KL15电连接（1是连接，0是断开）

                    self.ipdu.resume_all_bus_send()# 恢复报文发送

                    time.sleep(180) # 持续3分钟下切abandon
            except:
                self.nucapp.bgm_diag_line_up()  # bgm诊断激活线连接(1是连接，0是断开)
                self.nucapp.tcam_kl15_up() # TCAM KL15电连接（1是连接，0是断开）
                time.sleep(5)
                j = j + 1
                self.bgmcli = BGM_SSH('172.16.5.1')
                logger.info("用例执行失败，第 {0} 次".format(j))
                assert self.bgmcli.get_ping(ip="172.16.5.31", num=4, root_permission=False)       
                time.sleep(60)
                
    @pytest.mark.full
    @allure.title("整车休眠后远程座椅加热_5次") 
    def test_caseid_1979921(self, ecu):
        i,j = 0,0
        for n in range(5):
            self.ecu_interface.enter_network_sleep()
            time.sleep(300) # 等待3分钟
            logger.info("已休眠")
            try:                
                with allure.step('模拟云端下发远控开启主驾座椅开启3档指令'):
                    self.tsp.rvc_driver_seat_heat(3) #ShClose:-1关;ShLevel1:1档;ShLevel2:2档;ShLevel3:3档                
                    start_time = time.time()
                    logger.info(f"1、{start_time}")
                    logger.info("已发送主驾座椅加热3档请求")
                    NMtime = time.time()
                    logger.info(f"2、{NMtime}")
                    NMT = float(NMtime - start_time)+0.2
                    logger.info("TCAM唤醒时延{}s".format(NMT))
                    result1, realvalue1, expectedvalue1 = self.ipdu.check(self.ipdu.bodycan.CemBodyFr84, 'RemStrtHvCtrlReqErsCmd', 'ErsCmd_ErsCmdOn',timeout = 20, do_assert = False)#远控上高压
                    logger.info("result1 {}, realvalue1 {}, expectedvalue1 {}".format(result1, realvalue1, expectedvalue1))
                    assert result1,"15s内是否发出远控上高压请求" 
                    self.ipdu.set(self.ipdu.bodycan.CcmBodyFr22, 'RemClimaHvSts', 'OnOff1_On')
                    
                    result2, realvalue2, expectedvalue2 = self.ipdu.check(self.ipdu.bodycan.CEMBodyFr36, 'TelmSteerWhlHeatgReqLvl', 'TelmSeatClimaLvl_Lvl3',timeout = 20, do_assert = False)#远控主驾座椅加热开启
                    logger.info("result2 {}, realvalue2 {}, expectedvalue2 {}".format(result2, realvalue2, expectedvalue2))
                    assert result2,"20s内是否发出远控开启主驾座椅加热3档请求"
                    self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgAvlSts', 'StsFd_On')
                    self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgLvlSts', 'SeatClimaLvl_Lvl3')

                    time.sleep(1)
                    end_time = time.time()
                    t = float(end_time - start_time) - 1
                    i = i+1
                    logger.info("远控开启主驾座椅加热成功时延{}s".format(t))
                    logger.info("远控开启主驾座椅加热成功{}次".format(i))
                    logger.info("远控开启主驾座椅加热失败{}次".format(j))
                    logger.info("远控开启主驾座椅加热总{}次".format(i+j))
                    time.sleep(5)
                    self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgAvlSts', 'StsFd_Off')
                    self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgLvlSts', 'SeatClimaLvl_Off')
                    self.ipdu.set(self.ipdu.bodycan.CcmBodyFr22, 'RemClimaHvSts', 'OnOff1_Off')

                    logger.info('座椅加热已关闭')
                    self.nucapp.bgm_diag_line_up()  # bgm诊断激活线连接(1是连接，0是断开)
                    self.nucapp.tcam_kl15_up() # TCAM KL15电连接（1是连接，0是断开）
                    time.sleep(180) # 持续3分钟下切abandon            
            except:
                self.nucapp.bgm_diag_line_up()  # bgm诊断激活线连接(1是连接，0是断开)
                self.nucapp.tcam_kl15_up() # TCAM KL15电连接（1是连接，0是断开）
                time.sleep(5)
                j = j+1
                self.bgmcli = BGM_SSH('172.16.5.1')
                logger.info("用例执行失败，第 {} 次".format(j))
                assert self.bgmcli.get_ping(ip="172.16.5.31", num=10, root_permission=False)         
                time.sleep(60)
                
    @pytest.mark.full
    @allure.title("整车休眠后远程方向盘加热_5次") 
    def test_caseid_1979920(self, ecu):
        i,j = 0,0
        s = 0
        for n in range(5):
            self.ecu_interface.enter_network_sleep()
            time.sleep(300) # 等待3分钟
            logger.info("已休眠")
            try:                
                with allure.step('模拟云端下发远控开启方向盘加热指令'):    
                    self.tsp.rvc_steering_wheel_heat(3) #-1:关闭方向盘加热，1:1档，2:2档，3：3档                 
                    start_time = time.time()
                    logger.info(f"1、{start_time}")
                    logger.info("已发送方向盘加热开启请求")
                    NMtime = time.time()
                    logger.info(f"2、{NMtime}")
                    NMT = float(NMtime - start_time)+0.7
                    logger.info("TCAM唤醒时延{}s".format(NMT))
                    result1, realvalue1, expectedvalue1 = self.ipdu.check(self.ipdu.bodycan.CemBodyFr84, 'RemStrtHvCtrlReqErsCmd', 'ErsCmd_ErsCmdOn',timeout = 20, do_assert = False)#远控上高压
                    logger.info("result1 {}, realvalue1 {}, expectedvalue1 {}".format(result1, realvalue1, expectedvalue1))
                    assert result1,"15s内是否发出远控上高压请求" 
                    time.sleep(2.5)
                    self.ipdu.set(self.ipdu.bodycan.CcmBodyFr22, 'RemClimaHvSts_0_CcmBodySignalIPdu22', 'OnOff1_On')
                    result2, realvalue2, expectedvalue2 = self.ipdu.check(self.ipdu.bodycan.CemBodyFr92, 'TelmSteerWhlHeatgReqLvl', 'TelmSeatClimaLvl_Lvl3',timeout = 20, do_assert = False)#远控方向盘加热开启
                    logger.info("result2 {}, realvalue2 {}, expectedvalue2 {}".format(result2, realvalue2, expectedvalue2))
                    assert result2,"20s内是否发出远控开启方向盘加热请求"
                    self.ipdu.set(self.ipdu.bodycan.CcmBodyFr61, 'RemSteerWhlHeatgLvlReq_0_CcmBodySignalIPdu61', 'TelmSeatClimaLvl_Lvl3')
                    end_time = time.time()
                    t = end_time - start_time
                    s = s + t
                    i = i+1
                    logger.info("远控开启方向盘加热成功时延{}s".format(t))
                    logger.info("远控开启方向盘加热成功{}次".format(i))
                    logger.info("远控开启方向盘加热失败{}次".format(j))
                    logger.info("远控开启方向盘加热总{}次".format(i+j))
                    logger.info("远控方向盘加热执行总时间{}".format(s))
                    time.sleep(5)
                    self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'RemSteerWhlHeatgLvlReq_0_CcmBodySignalIPdu61', 'TelmSeatClimaLvl_Off')
                    self.ipdu.set(self.ipdu.bodycan.CcmBodyFr22, 'RemClimaHvSts_0_CcmBodySignalIPdu22', 'OnOff1_Off')
                    logger.info("方向盘加热已关闭")
                    self.nucapp.bgm_diag_line_up()  # bgm诊断激活线连接(1是连接，0是断开)
                    self.nucapp.tcam_kl15_up() # TCAM KL15电连接（1是连接，0是断开）
                    time.sleep(180) # 持续3分钟下切abandon            
            except:
                self.nucapp.bgm_diag_line_up()  # bgm诊断激活线连接(1是连接，0是断开)
                self.nucapp.tcam_kl15_up() # TCAM KL15电连接（1是连接，0是断开）
                time.sleep(5)
                j = j+1
                self.bgmcli = BGM_SSH('172.16.5.1')
                logger.info("用例执行失败，第 {} 次".format(j))
                assert self.bgmcli.get_ping(ip="172.16.5.31", num=4, root_permission=False)       
                time.sleep(60)
                
    @pytest.mark.full
    @allure.title("整车休眠后远程开启车窗指令_5次") 
    def test_caseid_1979916(self, ecu):
        i,j = 0,0
        for n in range(5):
            self.ecu_interface.enter_network_sleep()
            time.sleep(300) # 等待3分钟
            logger.info("已休眠")
            try:                
                with allure.step('模拟云端下发远控开启车窗指令'):
                    self.tsp.rvc_window_control(win_fl=100, win_fr=100, win_rl=100, win_rr=100) #100: 开车窗, 0:关闭车窗                
                    start_time = time.time()
                    logger.info(f"1、{start_time}")
                    logger.info("已发送车窗开启请求")
                    NMtime = time.time()
                    logger.info(f"2、{NMtime}")
                    NMT = float(NMtime - start_time)+0.2
                    logger.info("TCAM唤醒时延{}s".format(NMT))
                    NM = self.ipdu.recv_pdu("bodycan",0x501,timeout = 5)
                    logger.info("501的报文内容为{}".format(NM))
                    assert NM,"5s内是否check到501报文" 
                    self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr_0_DdmBodySignalIPdu04', 'WinAndRoofAndCurtPosnTyp_ClsFull')
                    self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass_0_PdmBodySignalIPdu01', 'WinAndRoofAndCurtPosnTyp_ClsFull')
                    self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi_0_RrdmBodySignalIPdu01', 'WinAndRoofAndCurtPosnTyp_ClsFull')
                    self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe_0_RldmBodySignalIPdu01', 'WinAndRoofAndCurtPosnTyp_ClsFull')
                    result2, realvalue2 = self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr68, 'WinOpenDrvrReq', 26), 
                                                    (self.ipdu.bodycan.CemBodyFr68, 'WinOpenPassReq', 26),
                                                    (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReLeReq', 26),
                                                    (self.ipdu.bodycan.CemBodyFr68, 'WinOpenReRiReq', 26)],timeout = 20, do_assert = False)
                    logger.info("result2 {}, realvalue2 {}".format(result2, realvalue2))
                    assert result2,"20s内是否发出远控开启车窗请求"
                    self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr_0_DdmBodySignalIPdu04', 'WinAndRoofAndCurtPosnTyp_OpenFull')
                    self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass_0_PdmBodySignalIPdu01', 'WinAndRoofAndCurtPosnTyp_OpenFull')
                    self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi_0_RrdmBodySignalIPdu01', 'WinAndRoofAndCurtPosnTyp_OpenFull')
                    self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe_0_RldmBodySignalIPdu01', 'WinAndRoofAndCurtPosnTyp_OpenFull')
                    time.sleep(1)
                    end_time = time.time()
                    t = end_time - start_time - 1
                    i = i+1
                    logger.info("远控开启车窗成功时延{}s".format(t))
                    logger.info("远控开启车窗成功{}次".format(i))
                    logger.info("远控开启车窗失败{}次".format(j))
                    logger.info("远控开启车窗总{}次".format(i+j))
                    time.sleep(5)
                    self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr_0_DdmBodySignalIPdu04', 'WinAndRoofAndCurtPosnTyp_ClsFull')
                    self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass_0_PdmBodySignalIPdu01', 'WinAndRoofAndCurtPosnTyp_ClsFull')
                    self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi_0_RrdmBodySignalIPdu01', 'WinAndRoofAndCurtPosnTyp_ClsFull')
                    self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe_0_RldmBodySignalIPdu01', 'WinAndRoofAndCurtPosnTyp_ClsFull')
                    logger.info("车窗已关闭")
                    self.nucapp.bgm_diag_line_up()  # bgm诊断激活线连接(1是连接，0是断开)
                    self.nucapp.tcam_kl15_up() # TCAM KL15电连接（1是连接，0是断开）
                    time.sleep(180) # 持续3分钟下切abandon                          
            except:
                self.nucapp.bgm_diag_line_up()  # bgm诊断激活线连接(1是连接，0是断开)
                self.nucapp.tcam_kl15_up() # TCAM KL15电连接（1是连接，0是断开）
                j = j+1
                self.bgmcli = BGM_SSH('172.16.5.1')
                logger.info("用例执行失败，第 {} 次".format(j))
                assert self.bgmcli.get_ping(ip="172.16.5.31", num=4, root_permission=False)
                time.sleep(60)
                
                
    
    
                                    
