# -*- coding:utf-8 -*-
"""
@File        :common_interface.py
@Author      :hui.zhao@jiduatuo.com
@Time        :2023/10/12 11:00 AM
@Description :Provide the common interface for develop automatic test case.
"""

import os
import sys
from time import sleep
from typing import Union
import pytest
import allure
from threading import Thread


from xat_ecu.legacy.common.logger import logger
from xat_cases.legacy.bgm.VehicleControl.case_helper.common_lib_bgm import *
from xat_cases.legacy.bgm.VehicleControl.case_helper.parse_excel_bgm import *

class CommonInterface:
    """为测试用例编写提供公共接口"""
    def __init__(self, tc_config, ipdu, busapp, nucapp, dk, io,sd_tester,partner="na"):
        self.ipdu = ipdu
        self.busapp = busapp
        self.nucapp = nucapp
        self.tc_config = tc_config
        self.sd_tester = sd_tester
        self.dk = dk
        self.io = io
        if partner != "na":
            self.partner = partner

    def chk_fr_carmod_usgmod(self, carmod, usgmod):
        """
        功能：检查总线上的carmode和usagemode
        @param usage_mode: 期望的usagemode值
        @param car_mode: 期望的carmode值
        """
        logger.info("\033[0;32;40m开始检测FR总线数据""\033[0m")
        retry_time = 0
        while True:
            retry_time = retry_time + 1
            if retry_time == 5:
                logger.info()
                break
            else:
                sleep(1)
                expectedvalue1 = self.ipdu.get_recent_signal_raw_value(self.ipdu.backbonefr.CemBackBoneFr02,
                                                                       'VehModMngtGlbSafe1CarModSts1_0_CEMBackBoneSignalIpdu02')
                logger.info("检查同芯Fr信号信号值为: carmod = {}".format(expectedvalue1))
                expectedvalue2 = self.ipdu.get_recent_signal_raw_value(self.ipdu.backbonefr.CemBackBoneFr02,
                                                                       'VehModMngtGlbSafe1UsgModSts_0_CEMBackBoneSignalIpdu02')
                logger.info("检查同芯Fr信号信号值为: usgmod = {}".format(expectedvalue2))
                if expectedvalue1 == carmod and expectedvalue2 == usgmod:
                    logger.info("\033[0;35;40mFR_carmod_usgmod正常\033[0m")
                    break
                else:
                    logger.info("\033[0;35;40mFR_carmod_usgmod异常尝试重新切换先等待两秒\033[0m")
                    sleep(2)
                    if expectedvalue1 != carmod:
                        logger.info("\033[0;35;40m重新切换CarMod\033[0m")
                        self.sd_tester.change_car_mode(carmod)
                    else:
                        logger.info("\033[0;35;40m重新切换UsgMod\033[0m")
                        self.sd_tester.change_usage_mode(usgmod)
        
    def set_five_door_open(self):
        """
        功能：设置5门的io状态设置为open
        """
        logger.info("")
        self.io.drvr_door_open()
        self.io.pass_door_open()
        self.io.lere_door_open()
        self.io.rire_door_open()
        self.io.trunk_door_open()
    
    def set_five_door_close(self):
        """
        功能：设置5门的io状态设置为close
        """
        self.io.drvr_door_close()
        self.io.pass_door_close()
        self.io.lere_door_close()
        self.io.rire_door_close()
        self.io.trunk_door_close()

    def set_5_door_lock_status(self, status):
        """
        功能：设置5门锁的状态,status = "lock",表示锁处于上锁状态，status = "unlock",表示锁处于解锁状态
        """
        with allure.step("设置5门锁的状态为{}".format(status)):
            logger.info("设置5门锁的状态为{}".format(status))
            if status == "lock":
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'DoorDrvrLockSts', 3)
                self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'DoorPassLockSts', 3)
                self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'DoorLeReLockSts', 3)
                self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'DoorRiReLockSts', 3)
                self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 1)
            elif status == "unlock":
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'DoorDrvrLockSts', 1)
                self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'DoorPassLockSts', 1)
                self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'DoorLeReLockSts', 1)
                self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'DoorRiReLockSts', 1)
                self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 1)
    
    def set_windows_position(self, pos_drvr = 1, pos_pass = 1, pos_lere = 1, pos_rire = 1):
        """
        模拟反馈四个车窗当前的开度, 由DM BodyCan输入
        :param pos_drvr: 左前车窗开度, can信号值, 实际开度 4 * pos - 4
        :param pos_pass: 右前车窗开度,
        :param pos_lere: 左后车窗开度
        :param pos_rire: 右后车窗开度
        :return:
        """
        with allure.step(
                f"模拟门窗开度, 左前{4 * pos_drvr - 4}%, 右前{4 * pos_pass - 4}%, 左后{4 * pos_lere - 4}%, 右后{4 * pos_rire - 4}%"):
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr_0_DdmBodySignalIPdu04', pos_drvr)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass_0_PdmBodySignalIPdu01', pos_pass)
            self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe_0_RldmBodySignalIPdu01', pos_lere)
            self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi_0_RrdmBodySignalIPdu01', pos_rire)

    def send_s2s_service_request(self,send_s2s_request_parameter: Union[tuple, list]):
        if isinstance(send_s2s_request_parameter,list):
            for send_s2s_request_parameter_tuple in send_s2s_request_parameter:
                if len(send_s2s_request_parameter_tuple) != 0:
                    logger.info("模拟发送s2s请求(服务:{},接口:{},参数:{})".format(send_s2s_request_parameter_tuple[0],send_s2s_request_parameter_tuple[1],send_s2s_request_parameter_tuple[2]))
                    
                    if len(send_s2s_request_parameter_tuple)> 3 and "timeout" in send_s2s_request_parameter_tuple[3]:
                        timeout = float(send_s2s_request_parameter_tuple[3].split("=")[-1])
                    else:
                        timeout = 2

                    if "_client" not in send_s2s_request_parameter_tuple[0]:
                        service_name = send_s2s_request_parameter_tuple[0]+"_client"
                    else:
                        service_name = send_s2s_request_parameter_tuple[0]    
                    self.partner.send_method_request(service_name,send_s2s_request_parameter_tuple[1],send_s2s_request_parameter_tuple[2],timeout)
                sleep(0.5)
        elif isinstance(send_s2s_request_parameter,tuple):
            if len(send_s2s_request_parameter) != 0:
                send_s2s_request_parameter_tuple = send_s2s_request_parameter
                logger.info("模拟发送s2s请求(服务:{},接口:{},参数:{})".format(send_s2s_request_parameter_tuple[0],send_s2s_request_parameter_tuple[1],send_s2s_request_parameter_tuple[2]))
                
                if len(send_s2s_request_parameter_tuple)> 3 and "timeout" in send_s2s_request_parameter_tuple[3]:
                        timeout = float(send_s2s_request_parameter_tuple[3].split("=")[-1])
                else:
                    timeout = 2

                if "_client" not in send_s2s_request_parameter_tuple[0]:
                    service_name = send_s2s_request_parameter_tuple[0]+"_client"
                else:
                    service_name = send_s2s_request_parameter_tuple[0]       
                self.partner.send_method_request(service_name,send_s2s_request_parameter_tuple[1],send_s2s_request_parameter_tuple[2],timeout)
        else:
            raise Exception("send_s2s_request_parameter 参数类型只能为数组和元组")
    
    def check_s2s_event(self,check_s2s_event_parameter: Union[tuple, list]):
        if isinstance(check_s2s_event_parameter,list):
            for check_s2s_event_parameter_tuple in check_s2s_event_parameter:
                if len(check_s2s_event_parameter_tuple) != 0:
                    logger.info("模拟发送s2s请求(服务:{},接口:{},参数:{})".format(check_s2s_event_parameter_tuple[0],check_s2s_event_parameter_tuple[1],check_s2s_event_parameter_tuple[2]))
                    
                    if len(check_s2s_event_parameter_tuple)> 3 and "timeout" in check_s2s_event_parameter_tuple[3]:
                        timeout = float(check_s2s_event_parameter_tuple[3].split("=")[-1])
                    else:
                        timeout = 2

                    if "_client" not in check_s2s_event_parameter_tuple[0]:
                        service_name = check_s2s_event_parameter_tuple[0]+"_client"
                    else:
                        service_name = check_s2s_event_parameter_tuple[0]    
                    self.partner.ck_s2s_event(service_name,check_s2s_event_parameter_tuple[1],check_s2s_event_parameter_tuple[2],timeout)
        elif isinstance(check_s2s_event_parameter,tuple):
            if len(check_s2s_event_parameter) != 0:
                check_s2s_event_parameter_tuple = check_s2s_event_parameter
                logger.info("模拟发送s2s请求(服务:{},接口:{},参数:{})".format(check_s2s_event_parameter_tuple[0],check_s2s_event_parameter_tuple[1],check_s2s_event_parameter_tuple[2]))
                
                if len(check_s2s_event_parameter_tuple)> 3 and "timeout" in check_s2s_event_parameter_tuple[3]:
                        timeout = float(check_s2s_event_parameter_tuple[3].split("=")[-1])
                else:
                    timeout = 2

                if "_client" not in check_s2s_event_parameter_tuple[0]:
                    service_name = check_s2s_event_parameter_tuple[0]+"_client"
                else:
                    service_name = check_s2s_event_parameter_tuple[0]       
                self.partner.ck_s2s_event(service_name,check_s2s_event_parameter_tuple[1],check_s2s_event_parameter_tuple[2],timeout)
        else:
            raise Exception("check_s2s_event_parameter 参数类型只能为数组和元组")

    def send_s2s_request_and_check_response(self,send_s2s_req_and_check_resp: Union[tuple, list]):
        if isinstance(send_s2s_req_and_check_resp,list):
            for send_s2s_req_and_check_resp_tuple in send_s2s_req_and_check_resp:
                if len(send_s2s_req_and_check_resp_tuple) != 0:
                    logger.info("模拟发送s2s请求(服务:{},接口:{},参数:{},期望返回值是{})".format(send_s2s_req_and_check_resp_tuple[0],send_s2s_req_and_check_resp_tuple[1],send_s2s_req_and_check_resp_tuple[2],send_s2s_req_and_check_resp_tuple[3]))
                    
                    if len(send_s2s_req_and_check_resp_tuple)> 4 and "timeout" in send_s2s_req_and_check_resp_tuple[3]:
                        timeout = float(send_s2s_req_and_check_resp_tuple[4].split("=")[-1])
                    else:
                        timeout = 2

                    if "_client" not in send_s2s_req_and_check_resp_tuple[0]:
                        service_name = send_s2s_req_and_check_resp_tuple[0]+"_client"
                    else:
                        service_name = send_s2s_req_and_check_resp_tuple[0]    
                    self.partner.send_request_and_ck_resp(service_name,send_s2s_req_and_check_resp_tuple[1],send_s2s_req_and_check_resp_tuple[2],send_s2s_req_and_check_resp_tuple[3],timeout)
                sleep(1)
        elif isinstance(send_s2s_req_and_check_resp,tuple):
            if len(send_s2s_req_and_check_resp) != 0:
                send_s2s_req_and_check_resp_tuple = send_s2s_req_and_check_resp
                logger.info("模拟发送s2s请求(服务:{},接口:{},参数:{},期望返回值是{})".format(send_s2s_req_and_check_resp_tuple[0],send_s2s_req_and_check_resp_tuple[1],send_s2s_req_and_check_resp_tuple[2],send_s2s_req_and_check_resp_tuple[3]))
                
                if len(send_s2s_req_and_check_resp_tuple)> 4 and "timeout" in send_s2s_req_and_check_resp_tuple[3]:
                        timeout = float(send_s2s_req_and_check_resp_tuple[3].split("=")[-1])
                else:
                    timeout = 2

                if "_client" not in send_s2s_req_and_check_resp_tuple[0]:
                    service_name = send_s2s_req_and_check_resp_tuple[0]+"_client"
                else:
                    service_name = send_s2s_req_and_check_resp_tuple[0]       
                self.partner.send_request_and_ck_resp(service_name,send_s2s_req_and_check_resp_tuple[1],send_s2s_req_and_check_resp_tuple[2],send_s2s_req_and_check_resp_tuple[3],timeout)
        else:
            raise Exception("send_s2s_req_and_check_resp 参数类型只能为数组和元组")

    def set_common_precontion(self,usage_mode:int = 1 ,car_mode:int = 0,veh_spd: Union[float, int]=0.0,vehmtnst: Union[str, int]="na" ,doors_sts:str = "na", cenlock_sts:str="na",ccp:dict = {}):
        """
        功能:提供一个设置case的前提条件的接口,目前可以设置的包括usagemode,carmode,车速，车辆移动状态（vehmtnst），5门的状态（doors_sts），中控锁状态(cenlock_sts),CCP配置。
        @param usage_mode: Usagemode状态，默认值为1
        @param car_mode: Carmode,默认值为0
        @param veh_spd: 设置车速，默认值为0
        @vehmtnst:车辆移动状态,默认没有使用，如果车速为0的时候默认vehmtnst=VehMtnSt2_StandStillVal3
        @doors_sts:5门状态，默认没有设置，doors_sts = "close"表示5门关;doors_sts = "open"表示5门开
        @cenlock_sts:中控锁状态，默认没有设置，cenlock_sts = "lock",表示中控锁处于上锁状态，cenlock_sts = "unlock",表示中控锁处于解锁状态
        @ccp:设置CCP,默认没有设置ccp，ccp={98: 0x2, 97: 0x2}表示设置CCP 98 = 2;CCP 97 = 2
        Example1:如果直接调用set_common_precontion(),表示usagemode设置为1，carmode设置为0，车速设置为0，车辆运动状态设置为VehMtnSt2_StandStillVal3
        Example1:如果直接调用set_common_precontion(usage_mode=13,veh_spd=10.0,vehmtnst = 4,ccp={98: 0x2, 97: 0x2}),表示usagemode设置为Driving，carmode设置为0，车速设置为10km/h，车辆运动状态设置为VehMtnSt2_RollgFwdVal1,设置CCP 98 = 2;CCP 97 = 2
        """
        logger.info("设置UsageMode={},CarMode={}".format(usage_mode,car_mode))
        if usage_mode==13:                
            self.sd_tester.change_car_mode(car_mode)
            sleep(0.5)
            self.sd_tester.change_usage_mode(usage_mode)
            sleep(0.5)
        else:
            self.sd_tester.change_usage_mode(usage_mode)
            sleep(0.5)
            self.sd_tester.change_car_mode(car_mode)
            sleep(0.5)

        # self.sd_tester.change_car_mode(car_mode, do_assert=1)
        # sleep(0.5)
        # self.sd_tester.change_usage_mode(usage_mode, do_assert=1)
        # sleep(0.5)
        # self.chk_fr_carmod_usgmod(carmod=car_mode, usgmod=usage_mode)
        
        logger.info("设置车速为{}".format(veh_spd))
        self.ipdu.set_vehspd(veh_spd)
        sleep(0.5)
        
        logger.info("车辆状态为{}".format(vehmtnst))
        if vehmtnst != "na":
            if isinstance(vehmtnst, int):
                # 设置车辆状态VehMtnSt
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,'VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00',vehmtnst)
                sleep(0.2)
                # 车辆处于P挡GearLvrIndcn（backbonefr.VddmBackBoneFr03)=0(GearLvrIndcn2_ParkIndcn) and TrsmParkLockd(backbonefr.VddmBackBoneFr18) = 0(TrsmParkLock1_ParkNotEngd)
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 0)
                sleep(0.1)
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 0)
            elif isinstance(vehmtnst, str):
                temp_dic = {'VehMtnSt2_Ukwn': 0, 'VehMtnSt2_StandStillVal1': 1, 'VehMtnSt2_StandStillVal2': 2, 'VehMtnSt2_StandStillVal3': 3, 'VehMtnSt2_RollgFwdVal1': 4, 'VehMtnSt2_RollgFwdVal2': 5, 'VehMtnSt2_RollgBackwVal1': 6, 'VehMtnSt2_RollgBackwVal2': 7}
                temp_list = list(temp_dic.keys())
                temp_list = [s.lower() for s in temp_list]

                for i in range(len(temp_list)):
                    if vehmtnst.lower() in temp_list[i]:
                        break
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,'VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00',i)
                sleep(0.2)
                # 车辆处于P挡GearLvrIndcn（backbonefr.VddmBackBoneFr03)=0(GearLvrIndcn2_ParkIndcn) and TrsmParkLockd(backbonefr.VddmBackBoneFr18) = 0(TrsmParkLock1_ParkNotEngd)
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 0)
                sleep(0.1)
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 0)
            sleep(0.5)
        elif veh_spd == 0.0:
            # 设置车辆状态VehMtnSt
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,'VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00',3)
                sleep(0.2)
                # 车辆处于P挡GearLvrIndcn（backbonefr.VddmBackBoneFr03)=0(GearLvrIndcn2_ParkIndcn) and TrsmParkLockd(backbonefr.VddmBackBoneFr18) = 0(TrsmParkLock1_ParkNotEngd)
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 0)
                sleep(0.1)
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 0)

        if doors_sts != 'na':
            logger.info("设置4门状态为{}".format(doors_sts))
            if doors_sts.lower() == "close":
                self.set_five_door_close()
            elif doors_sts.lower() == "open":
                self.set_five_door_open()
            else:
                raise ValueError("doors_sts 入参必须是close或者open")
        if cenlock_sts != 'na':
            logger.info("设置中控锁状态为{}".format(cenlock_sts))
            if cenlock_sts.lower() == "lock":
                self.dk.set_cenlock_sts(3)
            elif "un" in cenlock_sts.lower():
                self.dk.set_cenlock_sts(1)
            else:
                raise ValueError("cenlock_sts 入参有误")
            sleep(0.5)
        
        logger.info("设置CCP为{}".format(ccp))
        if ccp == {}:
            pass
        else:
            self.sd_tester.write_multi_ccp(ccp) 
        sleep(1)
    
    
    def send_s2s_request_and_check(self,send_s2s_request_parameter: Union[tuple, list],check_signal_parameter: Union[tuple, list]= (),check_service_response: Union[tuple, list] = (),check_s2s_event_parameter: Union[tuple, list]= ()):
        """
        功能:检测通过服务来触发BGM发出有限帧的对应总线信号,显著应用场景BGM只会发出有限次数的信号值,所以为了增加检测的准确率，采用了多线程提前开启检测线程。
        @param send_s2s_request_parameter_tuple:调用的S2S服务，参数类型是元组，例如:("WiperService", "SetWiperMode",{'wipers': [{'id': 0, 'mode': 3}]})
        @param check_signal_parameter: 要检测的BGM信号,
            如果只检测一个信号参数类型可以是元组，例如：("backbonefr.CemBackBoneFr07", 'WipgInfoWipgSpdInfo', 2),表示要检测backbonefr.CemBackBoneFr07中的WipgInfoWipgSpdInfo，
            期望的信号值为2，默认的超时时间是2秒，如果想设置检测的超时时间可以加timeout参数，例如：("backbonefr.CemBackBoneFr07", 'WipgInfoWipgSpdInfo', 2,timeout = 2)
            如果要同时检测多个信号，参数类型必须是列表，里面的每个元素是元组，例如[("bodycan.DdmBodyFr04", 'WinPosnStsAtDrvr', 26),("bodycan.PdmBodyFr01", 'WinPosnStsAtPass', 26)]
        Example: self.com_lib.send_s2s_request_and_check(( "WiperService", "SetWiperMode",{'wipers': [{'id': 0, 'mode': 0}]}),("backbonefr.CemBackBoneFr07", 'WipgInfoWipgSpdInfo', 0))
        """
        if isinstance(check_signal_parameter,list):
            for check_signal_parameter_tuple in check_signal_parameter:
                if len(check_signal_parameter_tuple) != 0:
                    bus_msg_list = check_signal_parameter_tuple[0].split(".")
                    obj_bus = getattr(self.ipdu,bus_msg_list[0])
                    obj_msg = getattr(obj_bus,bus_msg_list[1])
                    if len(check_signal_parameter_tuple)> 3 and "timeout" in check_signal_parameter_tuple[3]:
                        timeout = float(check_signal_parameter_tuple[3].split("=")[-1])
                    else:
                        timeout = 2
                    logger.info("启动检测信号{}({})的进程,期望的信号值是{}".format(check_signal_parameter_tuple[1],check_signal_parameter_tuple[0],check_signal_parameter_tuple[2]))
                    self.ipdu.check_thread_start(obj_msg, check_signal_parameter_tuple[1], check_signal_parameter_tuple[2], timeout)
                else:
                    logger.info("不需要检测总线信号")

            self.send_s2s_service_request(send_s2s_request_parameter)
            self.check_s2s_event(check_s2s_event_parameter)
            sleep(0.5)
            for check_signal_parameter_tuple in check_signal_parameter:
                if len(check_signal_parameter_tuple) != 0:
                    logger.info("结束检测信号{}({})的进程,获取实际检测结果".format(check_signal_parameter_tuple[1],check_signal_parameter_tuple[0]))
                    result = self.ipdu.check_thread_stop(check_signal_parameter_tuple[1], timeout=5)
                    logger.info("实际检测结果{}".format(result))
                    if result == None:
                        assert False
                    else:
                        assert result[0]
                else:
                    logger.info("不需要检测总线信号")

            self.ipdu.reset_check_results()
            self.send_s2s_request_and_check_response(check_service_response)

        elif isinstance(check_signal_parameter,tuple):
            check_signal_parameter_tuple = check_signal_parameter
            if len(check_signal_parameter_tuple) != 0:
                bus_msg_list = check_signal_parameter_tuple[0].split(".")
                obj_bus = getattr(self.ipdu,bus_msg_list[0])
                obj_msg = getattr(obj_bus,bus_msg_list[1])
                if len(check_signal_parameter_tuple)> 3 and "timeout" in check_signal_parameter_tuple[3]:
                    timeout = float(check_signal_parameter_tuple[3].split("=")[-1])
                else:
                    timeout = 2
                logger.info("启动检测信号{}({})的进程,期望的信号值是{}".format(check_signal_parameter_tuple[1],check_signal_parameter_tuple[0],check_signal_parameter_tuple[2]))
                self.ipdu.check_thread_start(obj_msg, check_signal_parameter_tuple[1], check_signal_parameter_tuple[2], timeout)
            else:
                logger.info("不需要检测总线信号")

            self.send_s2s_service_request(send_s2s_request_parameter)
            self.check_s2s_event(check_s2s_event_parameter)
            sleep(0.5)
            if len(check_signal_parameter_tuple) != 0:
                logger.info("结束检测信号{}({})的进程,获取实际检测结果".format(check_signal_parameter_tuple[1],check_signal_parameter_tuple[0]))
                result = self.ipdu.check_thread_stop(check_signal_parameter_tuple[1], timeout=5)
                logger.info("实际检测结果{}".format(result))
                if result == None:
                    assert False
                else:
                    assert result[0]
                self.ipdu.reset_check_results()
            else:
                logger.info("不需要检测总线信号")
            sleep(0.5)
            self.send_s2s_request_and_check_response(check_service_response)
        else:
            raise Exception("send_s2s_req_and_check_resp 参数类型只能为数组和元组")
        sleep(3)
        
    
    # def send_s2s_request_then_check(self,send_s2s_request_parameter: Union[tuple, list],check_signal_parameter: Union[tuple, list] = (),check_service_response: Union[tuple, list] = (),check_s2s_event_parameter: Union[tuple, list]= ()):
    #     """
    #     功能:发送S2S服务请求之后来检查BGM发出的总线信号值是否改变到期望值，并且还能获取服务结果，这个接口主要用于到收到服务请求之后总线上的信号值一直改变的场景
    #     @param send_s2s_request_parameter_tuple:调用的S2S服务，参数类型是元组，例如:("SteerWheelService", "SetHeat", {"status": 1})
    #     @param check_signal_parameter: 要检测的BGM信号,默认值为空，表示不需要检查总线信号。
    #         如果只检测一个信号参数类型可以是元组，例如：("backbonefr.CemBackBoneFr07", 'WipgInfoWipgSpdInfo', 2),表示要检测backbonefr.CemBackBoneFr07中的WipgInfoWipgSpdInfo，
    #             期望的信号值为2，默认的超时时间是2秒，如果想设置检测的超时时间可以加timeout参数，例如：("backbonefr.CemBackBoneFr07", 'WipgInfoWipgSpdInfo', 2,timeout = 2)
    #         如果要同时检测多个信号，参数类型必须是列表，里面的每个元素是元组，例如[("bodycan.DdmBodyFr04", 'WinPosnStsAtDrvr', 26),("bodycan.PdmBodyFr01", 'WinPosnStsAtPass', 26)]
    #     @param check_service_response： 要获取的服务状态，参数值类型为元组，默认值为空，表示不需要检查服务状态。
    #         如果需要检查服务状态，需要填入服务相关参数，例如：("SteerWheelService", "GetHeat", {}, {"out": 1})
    #     Example: self.com_lib.send_s2s_request_then_check(("SteerWheelService", "SetHeat", {"status": 1}),
    #                 check_signal_parameter=[("backbonefr.CemBackBoneFr19",'SteerWhlHeatgLvlSts',1),("connectivitycanfd.VgmConnFr03",'SteerWhlHeatgAvlSts',1)],
    #                 check_service_response = ("SteerWheelService", "GetHeat", {}, {"out": 1}))
    #     """
    #     self.send_s2s_service_request(send_s2s_request_parameter)
    #     self.check_s2s_event(check_s2s_event_parameter)
    #     self.send_s2s_request_and_check_response(check_service_response)

    #     if isinstance(check_signal_parameter,list):
    #         for check_signal_parameter_tuple in check_signal_parameter:
    #             if len(check_signal_parameter_tuple) != 0:
    #                 bus_msg_list = check_signal_parameter_tuple[0].split(".")
    #                 obj_bus = getattr(self.ipdu,bus_msg_list[0])
    #                 obj_msg = getattr(obj_bus,bus_msg_list[1])
    #                 if len(check_signal_parameter_tuple)> 3 and "timeout" in check_signal_parameter_tuple[3]:
    #                     timeout = float(check_signal_parameter_tuple[3].split("=")[-1])
    #                 else:
    #                     timeout = 2
    #                 logger.info("检测信号{}({})的信号值是否为:{}".format(check_signal_parameter_tuple[1],check_signal_parameter_tuple[0],check_signal_parameter_tuple[2]))
    #                 self.ipdu.check(obj_msg, check_signal_parameter_tuple[1], check_signal_parameter_tuple[2], timeout)
    #     elif isinstance(check_signal_parameter,tuple):
    #         check_signal_parameter_tuple = check_signal_parameter
    #         if len(check_signal_parameter_tuple) != 0:
    #                 bus_msg_list = check_signal_parameter_tuple[0].split(".")
    #                 obj_bus = getattr(self.ipdu,bus_msg_list[0])
    #                 obj_msg = getattr(obj_bus,bus_msg_list[1])
    #                 if len(check_signal_parameter_tuple)> 3 and "timeout" in check_signal_parameter_tuple[3]:
    #                     timeout = float(check_signal_parameter_tuple[3].split("=")[-1])
    #                 else:
    #                     timeout = 2
    #                 logger.info("检测信号{}({})的信号值是否为:{}".format(check_signal_parameter_tuple[1],check_signal_parameter_tuple[0],check_signal_parameter_tuple[2]))
    #                 self.ipdu.check(obj_msg, check_signal_parameter_tuple[1], check_signal_parameter_tuple[2], timeout)
    #     else:
    #         raise Exception("send_s2s_req_and_check_resp 参数类型只能为数组和元组")
        
    #     self.ipdu.reset_check_results()
    #     sleep(1)
        
    
    def check_signal_value_all_is(self,check_signal_parameter_tuple:tuple):
        """
        功能：检测信号的值是否一直为某个值。
        @param check_signal_parameter_tuple:参数类型为元组，要检测的信号以及值，例如：("backbonefr.CemBackBoneFr07",'WipgInfoWipgSpdInfo', 0,"timeout=5"),
            表示检测信号WipgInfoWipgSpdInfo再5秒钟内是否一直为0
        Example: self.com_lib.check_signal_value_all_is(("backbonefr.CemBackBoneFr07",'WipgInfoWipgSpdInfo', 0,"timeout=5"))
        """
        bus_msg_list = check_signal_parameter_tuple[0].split(".")
        obj_bus = getattr(self.ipdu,bus_msg_list[0])
        obj_msg = getattr(obj_bus,bus_msg_list[1])

        logger.info("检测信号{}({})信号值是否全部是{}".format(check_signal_parameter_tuple[1],check_signal_parameter_tuple[0],check_signal_parameter_tuple[2]))
        if len(check_signal_parameter_tuple)> 3 and "timeout" in check_signal_parameter_tuple[3]:
            timeout = float(check_signal_parameter_tuple[3].split("=")[-1])
        else:
            timeout = 2

        result_ori = self.ipdu.check_signal(obj_msg, check_signal_parameter_tuple[1],timeout)
        logger.info("{}秒内获取信号{}所有的值是:{}".format(timeout,check_signal_parameter_tuple[0],result_ori))
        result = check_all_value_is(result_ori, int(check_signal_parameter_tuple[2]))
        logger.info("期望值的统计结果:{}".format(result))
        assert result
        self.ipdu.reset_check_results()

    
    def check_signal_value_and_times(self,check_signal_parameter_tuple:tuple):
        """
        功能：检测信号的值以及发出的报文次数。
        @param check_signal_parameter_tuple:参数类型为元组，要检测的信号值以及次数，例如：("bodycan.CemBodyFr46", 'HmiClimaFrntAutReq_UB', 1, 1),
            表示2秒钟内（默认timeout = 2）检测信号HmiClimaFrntAutReq_UB值是否发出了1次值为1，如果想观察5秒内的信号值，可以改为：("bodycan.CemBodyFr46", 'HmiClimaFrntAutReq_UB', 1, 1,timeout = 5)
        Example: self.com_lib.check_signal_value_and_times(("bodycan.CemBodyFr46", 'HmiClimaFrntAutReq_UB', 1, 1))
        """
        bus_msg_list = check_signal_parameter_tuple[0].split(".")
        obj_bus = getattr(self.ipdu,bus_msg_list[0])
        obj_msg = getattr(obj_bus,bus_msg_list[1])

        logger.info("检测信号{}({})信号值{}是否发了{}次".format(check_signal_parameter_tuple[1],check_signal_parameter_tuple[0],check_signal_parameter_tuple[2],check_signal_parameter_tuple[3]))
        if len(check_signal_parameter_tuple)> 4 and "timeout" in check_signal_parameter_tuple[4]:
            timeout = float(check_signal_parameter_tuple[4].split("=")[-1])
        else:
            timeout = 2

        result_ori = self.ipdu.check_signal(obj_msg, check_signal_parameter_tuple[1],timeout)
        logger.info("{}秒内获取信号{}所有的值是:{}".format(timeout,check_signal_parameter_tuple[0],result_ori))
        result = get_signal_times_interval(result_ori, int(check_signal_parameter_tuple[2]))
        logger.info("期望值的统计结果:{}".format(result))
        assert result[0] == check_signal_parameter_tuple[3]
        self.ipdu.reset_check_results()
    
    def check_signal_value_with_detail_data(self,check_signal_parameter_tuple:tuple):
        bus_msg_list = check_signal_parameter_tuple[0].split(".")
        obj_bus = getattr(self.ipdu,bus_msg_list[0])
        obj_msg = getattr(obj_bus,bus_msg_list[1])

        logger.info("检测信号{}({})信号值是否为{}".format(check_signal_parameter_tuple[1],check_signal_parameter_tuple[0],check_signal_parameter_tuple[2]))
        if len(check_signal_parameter_tuple)> 3 and "timeout" in check_signal_parameter_tuple[3]:
            timeout = float(check_signal_parameter_tuple[3].split("=")[-1])
        else:
            timeout = 2

        result_ori = self.ipdu.check_signal(obj_msg, check_signal_parameter_tuple[1],timeout)
        logger.info("{}秒内获取信号{}所有的值是:{}".format(timeout,check_signal_parameter_tuple[0],result_ori))
        result = get_signal_times_interval(result_ori, int(check_signal_parameter_tuple[2]))
        logger.info("期望值的统计结果:{}".format(result))
        assert result[0] != 0
        self.ipdu.reset_check_results()


    def set_signal_value(self,set_signal_parameter: Union[tuple, list]):
        """
        功能：设置信号
        @param set_signal_parameter:参数类型为元组或者列表。
            如果设置单个信号参数类型可以是元组或者列表，例如：("chassiscan2.VddmChas2Fr17", 'DrvrSeatSts', 0)或者[("chassiscan2.VddmChas2Fr17", 'DrvrSeatSts', 0)]
                实现的功能就是将DrvrSeatSts值设置为0
            如果设置多个信号参数类型为列表，[("bodycan.PpodBodyFr01",'DoorPassOpenReqOutdSwt2',1),("bodycan.CemBodyFr103",'DoorPassOpenReqOutdSwt3',1)]
                实现的功能就是将DoorPassOpenReqOutdSwt2值设置为1同时将DoorPassOpenReqOutdSwt3设置为1
        Example: self.com_lib.set_signal_value([("bodycan.PpodBodyFr01",'DoorPassOpenReqOutdSwt2',1),("bodycan.CemBodyFr103",'DoorPassOpenReqOutdSwt3',1)])
        """
        if isinstance(set_signal_parameter,list):
            for set_signal_parameter_tuple in set_signal_parameter:
                if len(set_signal_parameter_tuple) !=0:
                    bus_msg_list = set_signal_parameter_tuple[0].split(".")
                    obj_bus = getattr(self.ipdu,bus_msg_list[0])
                    obj_msg = getattr(obj_bus,bus_msg_list[1])

                    logger.info("设置信号{}({})信号值为{}".format(set_signal_parameter_tuple[1],set_signal_parameter_tuple[0],set_signal_parameter_tuple[2]))
                    if len(set_signal_parameter_tuple)> 3 and "timeout" in set_signal_parameter_tuple[3]:
                        timeout = float(set_signal_parameter_tuple[3].split("=")[-1])
                    else:
                        timeout = 2
                    self.ipdu.set(obj_msg, set_signal_parameter_tuple[1],set_signal_parameter_tuple[2],timeout)
                    sleep(0.1)
        elif isinstance(set_signal_parameter,tuple):
            set_signal_parameter_tuple = set_signal_parameter
            if len(set_signal_parameter_tuple) !=0:
                bus_msg_list = set_signal_parameter_tuple[0].split(".")
                obj_bus = getattr(self.ipdu,bus_msg_list[0])
                obj_msg = getattr(obj_bus,bus_msg_list[1])

                logger.info("设置信号{}({})信号值为{}".format(set_signal_parameter_tuple[1],set_signal_parameter_tuple[0],set_signal_parameter_tuple[2]))
                if len(set_signal_parameter_tuple)> 3 and "timeout" in set_signal_parameter_tuple[3]:
                    timeout = float(set_signal_parameter_tuple[3].split("=")[-1])
                else:
                    timeout = 2
                self.ipdu.set(obj_msg, set_signal_parameter_tuple[1],set_signal_parameter_tuple[2],timeout)
                sleep(0.1)
        else:
            raise Exception("set_signal_parameter 参数类型只能为数组和元组")
        
        
    def check_singal_value(self,check_signal_parameter: Union[tuple, list]):
        """
        功能：检测信号值
        @param check_signal_parameter:参数类型为元组或者列表。
            如果检测单个信号，参数类型可以是元组或者列表，例如：("bodycan.CEMBodyFr14",'HmiHvacFanLvlFrnt',12)或者[("bodycan.CEMBodyFr14",'HmiHvacFanLvlFrnt',12)]
                实现的功能就是将检测信号"HmiHvacFanLvlFrnt"的值是否为12
            如果检测多个信号，参数类型为列表，[("bodycan.CEMBodyFr14",'HmiHvacFanLvlFrnt',12),("bodycan.CEMBodyFr14",'HmiHvacFanLvlRe',12)]
                实现的功能就是将HmiHvacFanLvlFrnt值设置为12同时将HmiHvacFanLvlRe设置为12
        Example: self.com_lib.check_singal_value([("bodycan.CEMBodyFr14",'HmiHvacFanLvlFrnt',12),("bodycan.CEMBodyFr14",'HmiHvacFanLvlRe',12)])
        """
        if isinstance(check_signal_parameter,list):
            for check_signal_parameter_tuple in check_signal_parameter:
                if len(check_signal_parameter_tuple) !=0:
                    bus_msg_list = check_signal_parameter_tuple[0].split(".")
                    obj_bus = getattr(self.ipdu,bus_msg_list[0])
                    obj_msg = getattr(obj_bus,bus_msg_list[1])

                    logger.info("Check信号{}({})信号值是否为{}".format(check_signal_parameter_tuple[1],check_signal_parameter_tuple[0],check_signal_parameter_tuple[2]))
                    if len(check_signal_parameter_tuple)> 3 and "timeout" in check_signal_parameter_tuple[3]:
                        timeout = float(check_signal_parameter_tuple[3].split("=")[-1])
                    else:
                        timeout = 2
                    
                    thread = Thread(
                        target=self.ipdu.check,
                        args=(obj_msg, check_signal_parameter_tuple[1],check_signal_parameter_tuple[2],timeout),
                    )
                    thread.setDaemon(True)
                    thread.start()

        elif isinstance(check_signal_parameter,tuple):
            check_signal_parameter_tuple = check_signal_parameter
            if len(check_signal_parameter_tuple) !=0:
                bus_msg_list = check_signal_parameter_tuple[0].split(".")
                obj_bus = getattr(self.ipdu,bus_msg_list[0])
                obj_msg = getattr(obj_bus,bus_msg_list[1])

                logger.info("Check信号{}({})信号值是否为{}".format(check_signal_parameter_tuple[1],check_signal_parameter_tuple[0],check_signal_parameter_tuple[2]))
                if len(check_signal_parameter_tuple)> 3 and "timeout" in check_signal_parameter_tuple[3]:
                    timeout = float(check_signal_parameter_tuple[3].split("=")[-1])
                else:
                    timeout = 2
                self.ipdu.check(obj_msg, check_signal_parameter_tuple[1],check_signal_parameter_tuple[2],timeout)
                self.ipdu.reset_check_results()
        else:
            raise Exception("check_signal_parameter 参数类型只能为数组和元组")
        sleep(2)
    
    
    # def set_signal_then_check_signal(self,set_signal_parameter: Union[tuple, list],check_signal_parameter: Union[tuple, list],check_service_response: Union[tuple, list] = (),check_s2s_event_parameter: Union[tuple, list]= ()):
    #     """
    #     功能：设置信号之后检测总线上的BGM发出的业务信号
    #     @param set_signal_parameter:参数类型为元组或者列表。
    #         如果设置单个信号参数类型可以是元组或者列表，例如：("chassiscan2.VddmChas2Fr17", 'DrvrSeatSts', 0)或者[("chassiscan2.VddmChas2Fr17", 'DrvrSeatSts', 0)]
    #             实现的功能就是将DrvrSeatSts值设置为0
    #         如果设置多个信号参数类型为列表，[("bodycan.PpodBodyFr01",'DoorPassOpenReqOutdSwt2',1),("bodycan.CemBodyFr103",'DoorPassOpenReqOutdSwt3',1)]
    #             实现的功能就是将DoorPassOpenReqOutdSwt2值设置为1同时将DoorPassOpenReqOutdSwt3设置为1
    #     @param check_signal_parameter:参数类型为元组或者列表。
    #         如果检测单个信号，参数类型可以是元组或者列表，例如：("bodycan.CEMBodyFr14",'HmiHvacFanLvlFrnt',12)或者[("bodycan.CEMBodyFr14",'HmiHvacFanLvlFrnt',12)]
    #             实现的功能就是将检测信号"HmiHvacFanLvlFrnt"的值是否为12
    #         如果检测多个信号，参数类型为列表，[("bodycan.CEMBodyFr14",'HmiHvacFanLvlFrnt',12),("bodycan.CEMBodyFr14",'HmiHvacFanLvlRe',12)]
    #             实现的功能就是将HmiHvacFanLvlFrnt值设置为12同时将HmiHvacFanLvlRe设置为12
    #     Example: self.com_lib.set_signal_and_check_signal(("backbonefr.SrsBackBoneFr04",'PassSeatSts', 2),("bodycan.CEMBodyFr19", 'PassSeatSts', 2))
    #     """
    #     self.set_signal_value(set_signal_parameter)
    #     self.check_s2s_event(check_s2s_event_parameter)
    #     self.send_s2s_request_and_check_response(check_service_response)
    #     self.check_singal_value(check_signal_parameter)
    #     sleep(3)
        
    
    # def set_signal_and_check_signal(self,set_signal_parameter: Union[tuple, list],check_signal_parameter: Union[tuple, list],check_service_response: Union[tuple, list] = (),check_s2s_event_parameter: Union[tuple, list]= ()):
    #     """
    #     功能:检测通过模拟总线信号来触发BGM发出有限帧的对应总线信号,显著应用场景BGM只会发出有限次数的信号值,所以为了增加检测的准确率，采用了多线程提前开启检测线程。
    #     @param set_signal_parameter:模拟发送的总线信号，参数类型为元组或者列表。
    #         如果设置单个信号参数类型可以是元组或者列表，例如：("chassiscan2.VddmChas2Fr17", 'DrvrSeatSts', 0)或者[("chassiscan2.VddmChas2Fr17", 'DrvrSeatSts', 0)]
    #             实现的功能就是将DrvrSeatSts值设置为0
    #         如果设置多个信号参数类型为列表，[("bodycan.PpodBodyFr01",'DoorPassOpenReqOutdSwt2',1),("bodycan.CemBodyFr103",'DoorPassOpenReqOutdSwt3',1)]
    #             实现的功能就是将DoorPassOpenReqOutdSwt2值设置为1同时将DoorPassOpenReqOutdSwt3设置为1
    #     @param check_signal_parameter: 要检测的BGM信号,
    #         如果只检测一个信号参数类型可以是元组，例如：("backbonefr.CemBackBoneFr07", 'WipgInfoWipgSpdInfo', 2),表示要检测backbonefr.CemBackBoneFr07中的WipgInfoWipgSpdInfo，
    #         期望的信号值为2，默认的超时时间是2秒，如果想设置检测的超时时间可以加timeout参数，例如：("backbonefr.CemBackBoneFr07", 'WipgInfoWipgSpdInfo', 2,timeout = 2)
    #         如果要同时检测多个信号，参数类型必须是列表，里面的每个元素是元组，例如[("bodycan.DdmBodyFr04", 'WinPosnStsAtDrvr', 26),("bodycan.PdmBodyFr01", 'WinPosnStsAtPass', 26)]
    #     Example: self.com_lib.set_signal_and_check_signal(( "WiperService", "SetWiperMode",{'wipers': [{'id': 0, 'mode': 0}]}),("backbonefr.CemBackBoneFr07", 'WipgInfoWipgSpdInfo', 0))
    #     """
    #     if isinstance(check_signal_parameter,list):
    #         for check_signal_parameter_tuple in check_signal_parameter:
    #             if len(check_signal_parameter_tuple) != 0:
    #                 bus_msg_list = check_signal_parameter_tuple[0].split(".")
    #                 obj_bus = getattr(self.ipdu,bus_msg_list[0])
    #                 obj_msg = getattr(obj_bus,bus_msg_list[1])
    #                 if len(check_signal_parameter_tuple)> 3 and "timeout" in check_signal_parameter_tuple[3]:
    #                     timeout = float(check_signal_parameter_tuple[3].split("=")[-1])
    #                 else:
    #                     timeout = 2
    #                 logger.info("启动检测信号{}({})的进程,期望的信号值是{}".format(check_signal_parameter_tuple[1],check_signal_parameter_tuple[0],check_signal_parameter_tuple[2]))
    #                 self.ipdu.check_thread_start(obj_msg, check_signal_parameter_tuple[1], check_signal_parameter_tuple[2], timeout)

    #         self.set_signal_value(set_signal_parameter)
    #         self.check_s2s_event(check_s2s_event_parameter)

    #         for check_signal_parameter_tuple in check_signal_parameter:
    #             if len(check_signal_parameter_tuple) != 0:
    #                 logger.info("结束检测信号{}({})的进程,获取实际检测结果".format(check_signal_parameter_tuple[1],check_signal_parameter_tuple[0]))
    #                 result = self.ipdu.check_thread_stop(check_signal_parameter_tuple[1], timeout=5)
    #                 logger.info("实际检测结果{}".format(result))
    #                 if result == None:
    #                     assert False
    #                 else:
    #                     assert result[0]

    #     elif isinstance(check_signal_parameter,tuple):
    #         check_signal_parameter_tuple = check_signal_parameter
    #         if len(check_signal_parameter_tuple) != 0:
    #             bus_msg_list = check_signal_parameter_tuple[0].split(".")
    #             obj_bus = getattr(self.ipdu,bus_msg_list[0])
    #             obj_msg = getattr(obj_bus,bus_msg_list[1])
    #             if len(check_signal_parameter_tuple)> 3 and "timeout" in check_signal_parameter_tuple[3]:
    #                 timeout = float(check_signal_parameter_tuple[3].split("=")[-1])
    #             else:
    #                 timeout = 2
    #             logger.info("启动检测信号{}({})的进程,期望的信号值是{}".format(check_signal_parameter_tuple[1],check_signal_parameter_tuple[0],check_signal_parameter_tuple[2]))
    #             self.ipdu.check_thread_start(obj_msg, check_signal_parameter_tuple[1], check_signal_parameter_tuple[2], timeout)

    #             self.set_signal_value(set_signal_parameter)
    #             self.check_s2s_event(check_s2s_event_parameter)

    #             logger.info("结束检测信号{}({})的进程,获取实际检测结果".format(check_signal_parameter_tuple[1],check_signal_parameter_tuple[0]))
    #             result = self.ipdu.check_thread_stop(check_signal_parameter_tuple[1], timeout=5)
    #             logger.info("实际检测结果{}".format(result))
    #             if result == None:
    #                 assert False
    #             else:
    #                 assert result[0]
    #     else:
    #         raise Exception("check_signal_parameter 参数类型只能为数组和元组") 

    #     self.send_s2s_request_and_check_response(check_service_response)

    #     sleep(3)
    #     self.ipdu.reset_check_results()

    
    def set_signal_and_check(self,set_signal_parameter: Union[tuple, list],check_signal_parameter: Union[tuple, list] = (),check_service_response: Union[tuple, list] = (),check_s2s_event_parameter: Union[tuple, list]= ()):
        """
        功能:检测通过模拟总线信号来触发BGM发出有限帧的对应总线信号,显著应用场景BGM只会发出有限次数的信号值,所以为了增加检测的准确率，采用了多线程提前开启检测线程。
        @param set_signal_parameter:模拟发送的总线信号，参数类型为元组或者列表。
            如果设置单个信号参数类型可以是元组或者列表，例如：("chassiscan2.VddmChas2Fr17", 'DrvrSeatSts', 0)或者[("chassiscan2.VddmChas2Fr17", 'DrvrSeatSts', 0)]
                实现的功能就是将DrvrSeatSts值设置为0
            如果设置多个信号参数类型为列表，[("bodycan.PpodBodyFr01",'DoorPassOpenReqOutdSwt2',1),("bodycan.CemBodyFr103",'DoorPassOpenReqOutdSwt3',1)]
                实现的功能就是将DoorPassOpenReqOutdSwt2值设置为1同时将DoorPassOpenReqOutdSwt3设置为1
        @param check_signal_parameter: 要检测的BGM信号,
            如果只检测一个信号参数类型可以是元组，例如：("backbonefr.CemBackBoneFr07", 'WipgInfoWipgSpdInfo', 2),表示要检测backbonefr.CemBackBoneFr07中的WipgInfoWipgSpdInfo，
            期望的信号值为2，默认的超时时间是2秒，如果想设置检测的超时时间可以加timeout参数，例如：("backbonefr.CemBackBoneFr07", 'WipgInfoWipgSpdInfo', 2,timeout = 2)
            如果要同时检测多个信号，参数类型必须是列表，里面的每个元素是元组，例如[("bodycan.DdmBodyFr04", 'WinPosnStsAtDrvr', 26),("bodycan.PdmBodyFr01", 'WinPosnStsAtPass', 26)]
        Example: self.com_lib.set_signal_and_check(( "WiperService", "SetWiperMode",{'wipers': [{'id': 0, 'mode': 0}]}),("backbonefr.CemBackBoneFr07", 'WipgInfoWipgSpdInfo', 0))
        """
        if isinstance(check_signal_parameter,list):
            if len(check_signal_parameter_tuple) != 0:
                for check_signal_parameter_tuple in check_signal_parameter:
                    bus_msg_list = check_signal_parameter_tuple[0].split(".")
                    obj_bus = getattr(self.ipdu,bus_msg_list[0])
                    obj_msg = getattr(obj_bus,bus_msg_list[1])
                    if len(check_signal_parameter_tuple)> 3 and "timeout" in check_signal_parameter_tuple[3]:
                        timeout = float(check_signal_parameter_tuple[3].split("=")[-1])
                    else:
                        timeout = 2
                    logger.info("启动检测信号{}({})的进程,期望的信号值是{}".format(check_signal_parameter_tuple[1],check_signal_parameter_tuple[0],check_signal_parameter_tuple[2]))
                    self.ipdu.check_thread_start(obj_msg, check_signal_parameter_tuple[1], check_signal_parameter_tuple[2], timeout)

            self.set_signal_value(set_signal_parameter)
            self.check_s2s_event(check_s2s_event_parameter)
            sleep(2)
            for check_signal_parameter_tuple in check_signal_parameter:
                if len(check_signal_parameter_tuple) != 0:
                    logger.info("结束检测信号{}({})的进程,获取实际检测结果".format(check_signal_parameter_tuple[1],check_signal_parameter_tuple[0]))
                    result = self.ipdu.check_thread_stop(check_signal_parameter_tuple[1], timeout=5)
                    logger.info("实际检测结果{}".format(result))
                    if result == None:
                        assert False
                    else:
                        assert result[0]

        elif isinstance(check_signal_parameter,tuple):
            check_signal_parameter_tuple = check_signal_parameter
            if len(check_signal_parameter_tuple) != 0:
                bus_msg_list = check_signal_parameter_tuple[0].split(".")
                obj_bus = getattr(self.ipdu,bus_msg_list[0])
                obj_msg = getattr(obj_bus,bus_msg_list[1])
                if len(check_signal_parameter_tuple)> 3 and "timeout" in check_signal_parameter_tuple[3]:
                    timeout = float(check_signal_parameter_tuple[3].split("=")[-1])
                else:
                    timeout = 2
                logger.info("启动检测信号{}({})的进程,期望的信号值是{}".format(check_signal_parameter_tuple[1],check_signal_parameter_tuple[0],check_signal_parameter_tuple[2]))
                self.ipdu.check_thread_start(obj_msg, check_signal_parameter_tuple[1], check_signal_parameter_tuple[2], timeout)

                self.set_signal_value(set_signal_parameter)
                self.check_s2s_event(check_s2s_event_parameter)
                sleep(2)
                logger.info("结束检测信号{}({})的进程,获取实际检测结果".format(check_signal_parameter_tuple[1],check_signal_parameter_tuple[0]))
                result = self.ipdu.check_thread_stop(check_signal_parameter_tuple[1], timeout=5)
                logger.info("实际检测结果{}".format(result))
                if result == None:
                    assert False
                else:
                    assert result[0]
            else:
                self.set_signal_value(set_signal_parameter)
                self.check_s2s_event(check_s2s_event_parameter)
        else:
            raise Exception("check_signal_parameter 参数类型只能为数组和元组") 
        self.send_s2s_request_and_check_response(check_service_response)
        sleep(3)
        self.ipdu.reset_check_results()



