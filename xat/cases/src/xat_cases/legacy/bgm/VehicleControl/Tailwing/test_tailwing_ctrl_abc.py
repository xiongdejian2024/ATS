#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_tailwing_ctrl.py
@Author      : huajie.yang@jiduauto.com
@Time        : 2023/12/27 11:30
@Description: BGM车控车设尾翼功能
"""

import os
import sys
import pytest
import allure
from time import sleep
from threading import Thread
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.api.common.common import *


@allure.feature("车控车设")
@allure.story("尾翼功能")
@pytest.mark.tailwing
class TestTailWingCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["CentralLockService_client","TailWingService_client","VehicleSetStatusService_client","TailGateService_client","VehicleModeService_client"])
        sleep(1)
        self.sd_tester.write_ccp(ccp={211: 0x01, 564: 0x2})
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        self.sd_tester.send_request_and_recv_response([0x2E, 0x42, 0x00, 0x00,0xC8,0x00,0xC8])
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC) 
        sleep(1)

    def before_each_func(self, ecu):   
        self.bus_comm.set_vehspd_gear(vehspd=0.0)    
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        self.bus_comm.set('backbonefr','VddmBackBoneFr18', 'TrsmParkLockdTrsmParkLockd', 1)
        sleep(.5)

        self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )

    def after_each_func(self, ecu):
        self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrIceBreakFaild', 0)  
        self.bus_comm.set('cem_lin6', 'AwmCem_Lin6Fr01','ActvReSplrMotBlk',0)    
        pass   

    def after_class(self, ecu):             
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
    
    def reset_bgm(self):
        self.sd_tester.update_serverdoipid(0x1FFF)
        self.sd_tester.send_data([0x11, 0x81])
        sleep(25)   

    def set_manual_open_tailwing(self):
        ''''设置电动尾翼手动模式'''
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.set_tailwing_pos(TailWingPos.P0)
        sleep(.5)
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.On)
        self.soa.get_tailwing_mode(mode=TailWindMode.On)
        self.bus_comm.check_tailwing_pos_req(pos=SetTailWingPos.P3)

    @pytest.mark.smoke
    def test_caseid_110449(self):
        '''车速68km/h不超过1s,尾翼不能自动关闭'''
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.io.set_door(Trunk=Door.close)
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.Auto)

        self.bus_comm.set_tailwing_pos(TailWingPos.P3)
        self.bus_comm.check_signal_thread_start('cem_lin6', 'BgmCem_Lin6Fr01', 'ActvReSplrPosnCmd')

        self.bus_comm.set_vehspd_gear(vehspd=18.05)#车速小于65km/h自动收回
        sleep(.5)
        self.bus_comm.set_vehspd_gear(vehspd=20.88)#1s内车速大于68km/h
        result_ori = self.bus_comm.check_signal_thread_stop('ActvReSplrPosnCmd')   
        logger.info(f'获取到的原始数据ActvReSplrPosnCmd为{result_ori}')
        result = get_signal_times_interval(result_ori, 1)
        logger.info("期望值的统计结果:{}".format(result))
        assert result[0] ==0

    @pytest.mark.full
    @pytest.mark.parametrize("carmode,usage",[(CarMode.NORMAL,UsageMode.INACTIVE),(CarMode.NORMAL,UsageMode.CONVENIENCE),(CarMode.NORMAL,UsageMode.ACTIVE)],
                             ids=['109836','109839','109861'])
    def test_tailwing_ctrl_caseid(self,carmode,usage):
        '''各模式下不同车速收回和展开'''
        
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.Auto)
        self.mix.set_common_precontion(
            car_mode=carmode, usage_mode=usage
        )
        self.bus_comm.set_tailwing_pos(TailWingPos.P0)
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.set_vehspd_gear(vehspd=28.0)
        self.bus_comm.check_tailwing_pos_req(pos=SetTailWingPos.P3)
        self.bus_comm.set_tailwing_pos(TailWingPos.P3)
        self.bus_comm.set_vehspd_gear(vehspd=10.0)#车速小于65km/h自动收回
        self.bus_comm.check_tailwing_pos_req(pos=SetTailWingPos.P0)

    @pytest.mark.smoke
    def test_caseid_110463(self):
        '''
        手动打开电动尾翼
        1.cramode:normal usagemode不等于abandon
        2.后背门关闭trsts=2
        3.电动尾翼不处于P3状态ActvReSplrPosn≠4(ActvSplCmd_P3)
        4.拖车未连接（(当CC#211 TRAILER MODULE, AFTERMARKET==01时,不需要判断拖车连接信号）
        '''
        self.io.set_door(Trunk=Door.close)
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.bus_comm.set_tailwing_pos(TailWingPos.P0)
        sleep(.5)
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.On)  
        self.soa.get_tailwing_mode(mode=TailWindMode.On) 
        self.bus_comm.check_tailwing_pos_req(pos=SetTailWingPos.P3)
        #收回电动尾翼
        self.bus_comm.set_tailwing_pos(TailWingPos.P3)   
        sleep(.5) 
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.Off)        
        self.soa.get_tailwing_mode(mode=TailWindMode.Off) 
        self.bus_comm.check_tailwing_pos_req(pos=SetTailWingPos.P0)

    @pytest.mark.smoke
    def test_caseid_110456(self):
        '''
        手动打开电动尾翼
        1.cramode:normal usagemode不等于abandon
        2.后背门关闭trsts=2
        3.电动尾翼不处于P3状态ActvReSplrPosn≠4(ActvSplCmd_P3)
        4.拖车未连接（(当CC#211 TRAILER MODULE, AFTERMARKET==01时,不需要判断拖车连接信号）
        '''
        self.io.set_door(Trunk=Door.close)
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE
        )
        self.bus_comm.set_tailwing_pos(TailWingPos.P0)
        sleep(.5)
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.On)  
        self.soa.get_tailwing_mode(mode=TailWindMode.On) 
        self.bus_comm.check_tailwing_pos_req(pos=SetTailWingPos.P3)
        #收回电动尾翼
        self.bus_comm.set_tailwing_pos(TailWingPos.P3)   
        sleep(.5) 
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.Off)        
        self.soa.get_tailwing_mode(mode=TailWindMode.Off) 
        self.bus_comm.check_tailwing_pos_req(pos=SetTailWingPos.P0)
     
    @pytest.mark.smoke
    def test_caseid_110447(self):
        '''
        手动打开电动尾翼
        1.cramode:normal usagemode不等于abandon
        2.后背门关闭trsts=2
        3.电动尾翼不处于P3状态ActvReSplrPosn≠4(ActvSplCmd_P3)
        4.拖车未连接（(当CC#211 TRAILER MODULE, AFTERMARKET==01时,不需要判断拖车连接信号）
        '''
        self.io.set_door(Trunk=Door.close)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_tailwing_pos(TailWingPos.P0)
        sleep(.5)
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.On)  
        self.soa.get_tailwing_mode(mode=TailWindMode.On) 
        self.bus_comm.check_tailwing_pos_req(pos=SetTailWingPos.P3)
        #收回电动尾翼
        self.bus_comm.set_tailwing_pos(TailWingPos.P3)   
        sleep(.5) 
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.Off)        
        self.soa.get_tailwing_mode(mode=TailWindMode.Off) 
        self.bus_comm.check_tailwing_pos_req(pos=SetTailWingPos.P0)

    @pytest.mark.smoke
    def test_caseid_110442(self):
        '''
        手动打开电动尾翼
        1.cramode:normal usagemode不等于abandon
        2.后背门关闭trsts=2
        3.电动尾翼不处于P3状态ActvReSplrPosn≠4(ActvSplCmd_P3)
        4.拖车未连接（(当CC#211 TRAILER MODULE, AFTERMARKET==01时,不需要判断拖车连接信号）
        '''
        self.io.set_door(Trunk=Door.close)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_tailwing_pos(TailWingPos.P0)
        sleep(.5)
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.On)  
        self.soa.get_tailwing_mode(mode=TailWindMode.On) 
        self.bus_comm.check_tailwing_pos_req(pos=SetTailWingPos.P3)
        #收回电动尾翼
        self.bus_comm.set_tailwing_pos(TailWingPos.P3)   
        sleep(.5) 
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.Off)        
        self.soa.get_tailwing_mode(mode=TailWindMode.Off) 
        self.bus_comm.check_tailwing_pos_req(pos=SetTailWingPos.P0)

    @pytest.mark.smoke
    def test_caseid_113489(self):
        '''
        normal driving下手动打开电动尾翼
        '''
        self.io.set_door(Trunk=Door.close) 
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )       
        self.bus_comm.set_tailwing_pos(TailWingPos.P0)
        sleep(.5)
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.On) 
        self.bus_comm.check_tailwing_pos_req(pos=SetTailWingPos.P3)
        self.bus_comm.set_tailwing_pos(TailWingPos.P3)
        sleep(.5)
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.Off) 
        self.bus_comm.check_tailwing_pos_req(pos=SetTailWingPos.P0)

    @pytest.mark.smoke
    def test_tailwing_ctrl_caseid_110450(self):
        '''当尾门打开手动关闭尾翼'''
        self.bus_comm.set_tailwing_pos(TailWingPos.P3)
        self.io.set_door(Trunk=Door.open)
        sleep(.5) 
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.Off)
        self.soa.get_tailwing_mode(mode=TailWindMode.Off) 
        self.bus_comm.check_tailwing_without_close_or_open_cmd(0)
        
    @pytest.mark.full
    def test_caseid_109867(self):
        '''当尾门打开手动关闭尾翼'''
        self.bus_comm.set_tailwing_pos(TailWingPos.P3)
        sleep(.5)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE)  
        self.io.set_door(Trunk=Door.open)
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.Off) 
        self.soa.get_tailwing_mode(mode=TailWindMode.Off) 
        self.bus_comm.check_tailwing_without_close_or_open_cmd(0)

    @pytest.mark.full
    def test_caseid_109859(self):
        '''当尾门打开手动关闭尾翼'''
        self.bus_comm.set_tailwing_pos(TailWingPos.P3)
        sleep(.5)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING)  
        self.io.set_door(Trunk=Door.open)
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.Off) 
        self.soa.get_tailwing_mode(mode=TailWindMode.Off) 
        self.bus_comm.check_tailwing_without_close_or_open_cmd(0)


    @pytest.mark.smoke
    def test_tailwing_ctrl_caseid_110466(self):
        '''当尾门打开手动打开尾翼'''
        self.bus_comm.set_tailwing_pos(TailWingPos.P0)
        sleep(.5)
        self.io.set_door(Trunk=Door.open)
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.On) 
        self.soa.get_tailwing_mode(mode=TailWindMode.On)
        self.bus_comm.check_tailwing_without_close_or_open_cmd(0)

    @pytest.mark.full
    @pytest.mark.parametrize("carmode,usage",[(CarMode.CRASH,UsageMode.ACTIVE),(CarMode.CRASH,UsageMode.CONVENIENCE),(CarMode.CRASH,UsageMode.INACTIVE),
                                              (CarMode.DYNO,UsageMode.ACTIVE),(CarMode.DYNO,UsageMode.CONVENIENCE),(CarMode.DYNO,UsageMode.INACTIVE),
                                              (CarMode.FACTORY,UsageMode.ACTIVE),(CarMode.FACTORY,UsageMode.INACTIVE),
                                              (CarMode.NORMAL,UsageMode.ABANDONED),
                                              (CarMode.TRANSPORT,UsageMode.ACTIVE),(CarMode.TRANSPORT,UsageMode.INACTIVE),
                                              (CarMode.CRASH,UsageMode.DRIVING),(CarMode.DYNO,UsageMode.DRIVING)],
                                              ids=['109847','109863','109835','109871','109866','109864','109850','109845','109855','109842','109841','109862','109872'])
    def test_tailwing_ctrl_notcarmode_ctrl_tailwing(self,carmode,usage):
        '''carmode不等于normal时进入自动挡位'''
        self.set_manual_open_tailwing()
        self.mix.set_common_precontion(
            car_mode=carmode, usage_mode=usage
        )
        #电动尾翼进入自动挡      
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.Auto) 
        self.soa.get_tailwing_mode(mode=TailWindMode.On)


    @pytest.mark.sanity
    @pytest.mark.parametrize("carmode,usage",[(CarMode.NORMAL,UsageMode.ACTIVE),(CarMode.NORMAL,UsageMode.CONVENIENCE),(CarMode.NORMAL,UsageMode.DRIVING)],                                       
                                              ids=[109837,109875,109869])
    def test_tailwing_ctrl_not_ctrl_tailwing_auto(self,carmode,usage):
        '''carmode满足时进入自动挡位'''
        self.set_manual_open_tailwing()
        self.mix.set_common_precontion(
            car_mode=carmode, usage_mode=usage
        )
        #收回电动尾翼      
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.Auto)      
        self.soa.get_tailwing_mode(mode=TailWindMode.Auto)

    @pytest.mark.full
    @pytest.mark.parametrize("carmode,usage",[(CarMode.CRASH,UsageMode.ABANDONED),(CarMode.CRASH,UsageMode.INACTIVE),(CarMode.CRASH,UsageMode.CONVENIENCE),
                                              (CarMode.FACTORY,UsageMode.ABANDONED)],
                                              ids=['113458','113455','109876','109874'])
    def test_tailwing_ctrl_not_ctrl_tailwing_manu(self,carmode,usage):
        '''carmode不等于normal时无法打开'''
        self.bus_comm.set_tailwing_pos(TailWingPos.P0)
        sleep(.5)
        self.mix.set_common_precontion(
            car_mode=carmode, usage_mode=usage
        )
        self.io.set_door(Trunk=Door.close)    
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.On)
        self.bus_comm.check_tailwing_without_close_or_open_cmd(0)
        
    @pytest.mark.full
    @pytest.mark.parametrize("carmode",[(CarMode.FACTORY),(CarMode.TRANSPORT),(CarMode.DYNO)],ids=['110453','110417','110421'])
    def test_tailwing_not_close(self,carmode):
        '''当carmode不满足时不能收回尾翼'''
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.set_tailwing_pos(TailWingPos.P3)
        sleep(.5)
        self.sd_tester.change_car_mode(carmode)
        self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
           
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.Off) 
        self.bus_comm.check_tailwing_without_close_or_open_cmd(0)
    
    @pytest.mark.full
    @pytest.mark.parametrize("carmode",[(CarMode.FACTORY),(CarMode.TRANSPORT)],
                             ids=['110423','110434'])
    def test_tailwing_not_open(self,carmode):
        '''当carmode不满足时不能打开尾翼'''
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.set_tailwing_pos(TailWingPos.P0)
        sleep(.5)   
        self.sd_tester.change_car_mode(carmode)
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.On) 
        self.bus_comm.check_tailwing_without_close_or_open_cmd(0)

    @pytest.mark.sanity
    def test_caseid_118428(self):
        '''打开电动尾翼重新上下电'''
        self.bus_comm.set_tailwing_pos(TailWingPos.P3)
        sleep(1)
        self.bus_comm.check_signal_thread_start('cem_lin6', 'BgmCem_Lin6Fr01', 'ActvReSplrPosnCmd',timeout=15) 
        self.io.bgm_power_off()     
        self.io.bgm_power_on()
        sleep(15)
        result_ori = self.bus_comm.check_signal_thread_stop('ActvReSplrPosnCmd')   
        logger.info(f'获取到的原始数据ActvReSplrPosnCmd为{result_ori}')
        result = get_signal_times_interval(result_ori, 1)
        logger.info("期望值的统计结果:{}".format(result))
        assert result[0] ==0

    @pytest.mark.sanity
    def test_caseid_109444(self):
        '''收回电动尾翼重新上下电'''
        self.bus_comm.set_tailwing_pos(TailWingPos.P3)
        sleep(1)
        self.bus_comm.check_signal_thread_start('cem_lin6', 'BgmCem_Lin6Fr01', 'ActvReSplrPosnCmd',timeout=15) 
        self.io.bgm_power_off()     
        self.io.bgm_power_on()
        sleep(15)
        result_ori = self.bus_comm.check_signal_thread_stop('ActvReSplrPosnCmd')   
        logger.info(f'获取到的原始数据ActvReSplrPosnCmd为{result_ori}')
        result = get_signal_times_interval(result_ori, 4)
        logger.info("期望值的统计结果:{}".format(result))
        assert result[0] ==0


    @pytest.mark.smoke 
    def test_caseid_110461(self):
        '''尾翼关闭失败,车速VehSpdLgt大于等于65km/h,且1s内车速不大于68km/h'''
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.bus_comm.set_tailwing_pos(TailWingPos.P3)
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.Auto)
        self.bus_comm.check_signal_thread_start('cem_lin6', 'BgmCem_Lin6Fr01', 'ActvReSplrPosnCmd') 
        self.bus_comm.set_vehspd_gear(vehspd=18.0)#车速小于65km/h自动收回
        self.bus_comm.set_vehspd_gear(vehspd=19.0)
        sleep(1.5)
        result_ori = self.bus_comm.check_signal_thread_stop('ActvReSplrPosnCmd')   
        logger.info(f'获取到的原始数据ActvReSplrPosnCmd为{result_ori}')
        result = get_signal_times_interval(result_ori, 1)
        logger.info("期望值的统计结果:{}".format(result))
        assert result[0] ==0   

    @pytest.mark.smoke
    def test_caseid_110419(self):
        '''车速不满足尾翼打开失败'''
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.bus_comm.set_tailwing_pos(TailWingPos.P0)
        sleep(.5)
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.Auto)
        self.bus_comm.set_vehspd_gear(vehspd=25.83)
        self.bus_comm.check_tailwing_without_close_or_open_cmd(0)

    
    @pytest.mark.smoke
    def test_caseid_109445(self):
        '''诊断写入AWM次数'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)#过5等级
        sleep(0.1)
        self.sd_tester.send_request_and_recv_response([0x2E, 0x42, 0x00, 0x00,0x02,0x00,0x02])#写入上限值2次
        ret_code, read_date =self.sd_tester.send_request_and_recv_response([0x22, 0x42, 0x00])
        sleep(0.1)
        self.sd_tester.send_request_and_recv_response([0x2E, 0x42, 0x00, 0x00,0xC8,0x00,0xC8])#恢复
        if read_date[-1] !=2:
            assert 0,"诊断写入AWM次数失败"


    @pytest.mark.sanity
    def test_caseid_110457_110459(self):
        '''VFC_PowerClosures(ID=21) Active'''
        self.bus_comm.set_tailwing_pos(TailWingPos.P0)
        sleep(.5)
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE
        )
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.On)
        self.soa.get_tailwing_mode(mode=TailWindMode.On)
        self.bus_comm.check_PNC(BusName.connectivitycanfd,NMMsgId.x533,BGMPNC.PNC19,NMSts.valid)
        self.sd_tester.change_usage_mode(UsageMode.ABANDONED)
        self.bus_comm.check_PNC(BusName.connectivitycanfd,NMMsgId.x533,BGMPNC.PNC19,NMSts.no_valid)
    
    @pytest.mark.sanity
    def test_caseid_110451(self):
        '''VFC_PowerClosures(ID=21)Deactive_02'''
        self.bus_comm.set_tailwing_pos(TailWingPos.P0)
        sleep(.5)
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE
        )
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.On)
        self.soa.get_tailwing_mode(mode=TailWindMode.On)
        sleep(1)
        self.bus_comm.check_PNC(BusName.connectivitycanfd,NMMsgId.x533,BGMPNC.PNC19,NMSts.valid)
        sleep(10)
        self.bus_comm.check_PNC(BusName.connectivitycanfd,NMMsgId.x533,BGMPNC.PNC19,NMSts.no_valid)

    @pytest.mark.sanity
    def test_caseid_1985079(self):
        '''尾翼自学习'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)#过5等级
        self.sd_tester.send_request_and_recv_response([0x2E, 0x42, 0x00, 0x00,0x02,0x00,0x02])#写入上限值2次
        self.sd_tester.send_request_and_recv_response([0x22, 0x42, 0x00])
        
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        for i in range(3):
            self.bus_comm.set_tailwing_pos(TailWingPos.P3)
            sleep(.5)
            self.bus_comm.set_tailwing_pos(TailWingPos.Shifting)
            sleep(.5)
            self.bus_comm.set_tailwing_pos(TailWingPos.P3)
            sleep(.5)
        self.bus_comm.set('propulsioncan','EcmPropFr24', 'GearLvrIndcn_1_EcmPropSignalIPdu24', 3)
        self.bus_comm.set_vehspd_gear(vehspd=5.0)
        self.bus_comm.check('cem_lin6','BgmCem_Lin6Fr01','CalforAWMPosn', 2)
        
        self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','CalStsAWM', 1)#学习中
        sleep(1)
        self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','CalStsAWM', 2)#学习成功
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0x20,0x13],recv=[0x71, 0x01, 0x20,0x13,0x10])
        sleep(14)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1)
        self.bus_comm.set_vehspd_gear(vehspd=5.0)
        sleep(1)
        self.bus_comm.check('cem_lin6','BgmCem_Lin6Fr01','CalforAWMPosn', 0)
        self.sd_tester.send_request_and_recv_response([0x31, 0x03, 0x20,0x13],recv=[0x71, 0x03, 0x20,0x13,0x10,0x02])

    @pytest.mark.sanity
    def test_caseid_1985116(self):
        '''bgm重启后触发尾翼自学习'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)#过5等级
        self.sd_tester.send_request_and_recv_response([0x2E, 0x42, 0x00, 0x00,0x02,0x00,0x02])#写入上限值2次
        self.sd_tester.send_request_and_recv_response([0x22, 0x42, 0x00])
        for i in range(2):

            self.bus_comm.set_tailwing_pos(TailWingPos.P2)
            sleep(.5)
            self.bus_comm.set_tailwing_pos(TailWingPos.Shifting)
            sleep(.5)
            self.bus_comm.set_tailwing_pos(TailWingPos.P0)
            sleep(.5)
        self.reset_bgm()
        self.mix.set_common_precontion( usage_mode=UsageMode.DRIVING
        )
        self.bus_comm.set_tailwing_pos(TailWingPos.P2)
        sleep(1)
        self.bus_comm.set_tailwing_pos(TailWingPos.Shifting)
        sleep(1)
        self.bus_comm.set_tailwing_pos(TailWingPos.P0)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.bus_comm.set_vehspd_and_qf(vehspd=5.0)
        self.bus_comm.check('cem_lin6','BgmCem_Lin6Fr01','CalforAWMPosn', 2)
        self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','CalStsAWM', 1)
        sleep(1)
        self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','CalStsAWM', 2)
        sleep(14)
        self.bus_comm.check('cem_lin6','BgmCem_Lin6Fr01','CalforAWMPosn', 0)

    @pytest.mark.full
    def test_did_da00_caseid_1987088(self):
        '''诊断读取AWM模块在线与不在线状态'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED)
        self.sd_tester.send_request_and_recv_response([0x22, 0xDA, 0x00])
        logger.info("停发AWM,诊断读取AWM不在线")
        self.bus_comm.pause_ecu_send("cem_lin6", "AWM")
        sleep(1)
        ret_code, read_date2 = self.sd_tester.send_request_and_recv_response([0x22, 0xDA, 0x00])
        logger.info("恢复AWM,诊断读取AWM在线")
        self.bus_comm.resume_ecu_send("cem_lin6", "AWM")
        sleep(1)
        ret_code, read_date3 = self.sd_tester.send_request_and_recv_response([0x22, 0xDA, 0x00])
        if read_date2[-1] != 0 and read_date3[-1] != 1:
            assert False, "AWM模块在线或不在线时诊断读取状态不一致"
            
    @pytest.mark.sanity
    def test_caseid_110462(self):
        '''电动尾翼自动关闭失败_CCP配置'''
        self.sd_tester.write_ccp(ccp={211: 0x1, 564: 0x1})
        sleep(1)
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.set_tailwing_pos(TailWingPos.P3)
        sleep(1)
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.Auto)
        self.soa.get_tailwing_mode(mode=TailWindMode.Auto)
        self.bus_comm.set_vehspd_gear(vehspd=10.0)
        self.bus_comm.check_tailwing_without_close_or_open_cmd(0)

    @pytest.mark.sanity
    def test_caseid_110437(self):
        '''电动尾翼自动打开失败_CCP配置'''
        self.sd_tester.write_ccp(ccp={211: 0x01, 564: 0x1})
        sleep(1)
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.set_tailwing_pos(TailWingPos.P0)
        sleep(.5)
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.Auto)
        self.soa.get_tailwing_mode(mode=TailWindMode.Auto)
        self.bus_comm.set_vehspd_gear(vehspd=28.0)
        self.bus_comm.check_tailwing_without_close_or_open_cmd(0)

@allure.feature("车控车设")
@allure.story("尾翼功能")
class TestTailWingCtrl01(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["VehicleModeService_client", "TailGateService_client",
                         "TailWingService_client",
                          "VehicleSetStatusService_client", "LightService_client"])
        time.sleep(1)
        self.sd_tester.write_ccp(ccp={211: 0x01, 564: 0x2})

    def before_each_func(self, ecu):
        self.bus_comm.set_vehmtn()
        self.bus_comm.set_vehspd()
        self.bus_comm.set_singal(bus="backbonefr", msg="VddmBackBoneFr18", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
        time.sleep(1)
        self.bus_comm.set_dtc_pre()
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 1})
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)


    def after_each_func(self, ecu):
        self.soa.send_method_request( 'VehicleModeService_client','SetCarMode',{"mode": 0})
        self.bus_comm.check('bodycan','CEMBodyFr12','VehModMngtGlbSafe1CarModSts1_3_CEMBodySignalIPdu12',0)
        self.bus_comm.check(
            'bodycan','CEMBodyFr12' ,'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_3_CEMBodySignalIPdu12', 0
        )
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)
        self.io.set_five_door_sts(sts=Door.close)
        self.io.driver_seat_notpresent()
        self.bus_comm.set_secle_seat_notpresent()
        self.bus_comm.set_pass_seat_notpresent()
        self.io.hazard_light_close()
        self.io.bgm_diag_line_up()


    def after_class(self, ecu):
        self.mix.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)

    @pytest.mark.sanity
    def test_caseid_109865(self):
        '''
        cramode:transportdriving电动尾翼进入自动挡
        '''
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.On)
        self.soa.get_tailwing_mode(mode=TailWindMode.On)   
        self.mix.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
        sleep(1)
        self.soa.send_method_request( 'VehicleModeService_client','SetCarMode',{"mode": 1})
        sleep(1)
        self.bus_comm.check('bodycan','CEMBodyFr12','VehModMngtGlbSafe1CarModSts1_3_CEMBodySignalIPdu12',1)       
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check('bodycan','CEMBodyFr12','VehModMngtGlbSafe1CarModSts1_3_CEMBodySignalIPdu12',0)
        self.bus_comm.check(
            'bodycan','CEMBodyFr12' ,'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_3_CEMBodySignalIPdu12', 3
        )    
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.Auto)      
        self.soa.get_tailwing_mode(mode=TailWindMode.Auto)

    @pytest.mark.full
    def test_caseid_109844(self):
        '''
        cramode:factorydriving 电动尾翼进入自动挡
        '''
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.On)
        self.soa.get_tailwing_mode(mode=TailWindMode.On)
        self.mix.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
        sleep(1)
        self.soa.send_method_request( 'VehicleModeService_client','SetCarMode',{"mode": 2})
        sleep(1)
        self.bus_comm.check('bodycan','CEMBodyFr12','VehModMngtGlbSafe1CarModSts1_3_CEMBodySignalIPdu12',2)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check('bodycan','CEMBodyFr12','VehModMngtGlbSafe1CarModSts1_3_CEMBodySignalIPdu12',0)
        self.bus_comm.check(
            'bodycan','CEMBodyFr12' ,'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_3_CEMBodySignalIPdu12', 2
        )
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.Auto) 
        self.soa.get_tailwing_mode(mode=TailWindMode.Auto)


    @pytest.mark.full
    def test_caseid_109873(self):
        '''
        手动打开电动尾翼
        1.cramode:factorydriving, usagemode不等于abandon
        2.后背门关闭trsts=2
        3.电动尾翼不处于P3状态ActvReSplrPosn≠4(ActvSplCmd_P3)
        4.拖车未连接(当CC#211 TRAILER MODULE, AFTERMARKET==01时,不需要判断拖车连接信号）
        '''
        self.mix.service_change_usage_mode_and_check_result(UsageMode.ACTIVE)
        sleep(1)
        self.soa.send_method_request( 'VehicleModeService_client','SetCarMode',{"mode": 2})
        sleep(1)
        self.bus_comm.check('bodycan','CEMBodyFr12','VehModMngtGlbSafe1CarModSts1_3_CEMBodySignalIPdu12',2)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check('bodycan','CEMBodyFr12','VehModMngtGlbSafe1CarModSts1_3_CEMBodySignalIPdu12',0)
        self.bus_comm.check(
            'bodycan','CEMBodyFr12' ,'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_3_CEMBodySignalIPdu12', 2
        )
        self.bus_comm.set_tailwing_pos(TailWingPos.P0)
        sleep(.5)
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.On) 
        self.bus_comm.check_tailwing_pos_req(pos=SetTailWingPos.P3)
        #收回电动尾翼
        self.bus_comm.set_tailwing_pos(TailWingPos.P3)
        sleep(.5)
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.Off) 
        self.bus_comm.check_tailwing_pos_req(pos=SetTailWingPos.P0)

    @pytest.mark.full
    def test_caseid_1993310(self):
        '''KL30重启BGM4200电动尾翼标定值存储'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x42, 0x00]
        )
        sleep(.1)
        write_power_list = [
            random.randint(0, 1),
            random.randint(0, 244),
            random.randint(0, 1),
            random.randint(0, 244),
        ]
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x42, 0x00], write_power_list, do_assert=True
        )
        sleep(1)
        logger.info("bgm KL30重启重启")
        self.io.bgm_power_off()
        self.io.bgm_power_on()
        sleep(25)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x42, 0x00],
            recv=[0x62, 0x42, 0x00] + write_power_list,
            do_assert=True,
        )
        sleep(.1)
        read_power_lsit = read_date[3:]
        logger.info("恢复值")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x42, 0x00] + local_date[3:]
        )
        if read_power_lsit != write_power_list:
            log_string = f"写入电动尾翼值失败,读取结果本应为{bytes(write_power_list).hex()}实际为{bytes(read_power_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string
    
    


    @pytest.mark.full
    def test_caseid_1984490(self):
        '''4200电动尾翼'''
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        ret_code, local_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x42, 0x00]
        )
        sleep(.1)
        write_power_list = [
            random.randint(0, 1),
            random.randint(0, 244),
            random.randint(0, 1),
            random.randint(0, 244),
        ]
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x42, 0x00], write_power_list, do_assert=True
        )
        sleep(1)
        logger.info("bgm 诊断重启重启")
        self.sd_tester.reset_bgm()
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        ret_code, read_date = self.sd_tester.send_request_and_recv_response(
            [0x22, 0x42, 0x00],
            recv=[0x62, 0x42, 0x00] + write_power_list,
            do_assert=True,
        )
        sleep(.1)
        read_power_lsit = read_date[3:]
        logger.info("恢复值")
        self.sd_tester.send_request_and_recv_response(
            [0x2E, 0x42, 0x00] + local_date[3:]
        )
        if read_power_lsit != write_power_list:
            log_string = f"写入电动尾翼值失败,读取结果本应为{bytes(write_power_list).hex()}实际为{bytes(read_power_lsit).hex()}"
            logger.info(log_string)
            assert 0, log_string
    







