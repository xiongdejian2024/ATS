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


@allure.feature("BGM车控车设")
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
        self.bus_comm.ipdu.reset_check_results()
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
        
    def after_class(self, ecu):             
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
    

    @pytest.mark.smoke
    def test_caseid_109857(self):
        '''车速满足尾翼自动展开'''
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.bus_comm.set_tailwing_pos(TailWingPos.P0)
        sleep(.5)
        self.io.set_door(Trunk=Door.close)
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.Auto)
        self.soa.get_tailwing_mode(mode=TailWindMode.Auto)
        self.bus_comm.check_signal_thread_start('cem_lin6', 'BgmCem_Lin6Fr01', 'ActvReSplrPosnCmd')  
        self.bus_comm.set_vehspd_gear(vehspd=28.0)
        result_ori = self.bus_comm.check_signal_thread_stop('ActvReSplrPosnCmd')  
        logger.info(f'获取到的原始数据ActvReSplrPosnCmd为{result_ori}')
        result = get_signal_times_interval(result_ori, 4)
        logger.info("期望值的统计结果:{}".format(result))
        assert result[0] !=0
    
    @pytest.mark.smoke
    def test_caseid_110454(self):
        '''NFC锁车自动收回尾翼'''
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC) 
        self.bus_comm.set_tailwing_pos(TailWingPos.P3)
        sleep(.5)
        self.bus_comm.check_signal_thread_start('cem_lin6', 'BgmCem_Lin6Fr01', 'ActvReSplrPosnCmd')  
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC) 
        
        result_ori = self.bus_comm.check_signal_thread_stop('ActvReSplrPosnCmd')   
        logger.info(f'获取到的原始数据ActvReSplrPosnCmd为{result_ori}')
        result = get_signal_times_interval(result_ori, 1)
        logger.info("期望值的统计结果:{}".format(result))
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        assert result[0] !=0   
    
    @pytest.mark.full
    def test_caseid_1983322(self):
        '''收回堵转_尾翼保持升起,收回到升起'''

        self.bus_comm.set_tailwing_pos(TailWingPos.P3)
        sleep(1)
        self.bus_comm.check_signal_thread_start('cem_lin6', 'BgmCem_Lin6Fr01', 'ActvReSplrPosnCmd') 
        self.bus_comm.set('cem_lin6', 'AwmCem_Lin6Fr01','ActvReSplrMotBlk',1)
        sleep(2)
        self.bus_comm.set('cem_lin6', 'AwmCem_Lin6Fr01','ActvReSplrMotBlk',0)
        sleep(1)
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.Off) 
        self.soa.get_tailwing_mode(mode=TailWindMode.Off)  
        result_ori = self.bus_comm.check_signal_thread_stop('ActvReSplrPosnCmd')  
        logger.info(f'获取到的原始数据ActvReSplrPosnCmd为{result_ori}')
        result = get_signal_times_interval(result_ori, 1)
        logger.info("期望值的统计结果:{}".format(result))
        assert result[0] !=0
    
    @pytest.mark.smoke
    def test_caseid_110443(self):
        '''尾翼打开成功,VehSpdLgtA>=95km/h and VehSpdLgtA>=92km/h持续时间不超过1s'''
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.set_tailwing_pos(TailWingPos.P0)
        sleep(.5)
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.Auto)
        self.soa.get_tailwing_mode(mode=TailWindMode.Auto)
        self.bus_comm.check_signal_thread_start('cem_lin6', 'BgmCem_Lin6Fr01', 'ActvReSplrPosnCmd')  
        self.bus_comm.set_vehspd_gear(vehspd=27.38)
        sleep(.5)
        self.bus_comm.set_vehspd_gear(vehspd=25.9)
        sleep(.5)
        result_ori = self.bus_comm.check_signal_thread_stop('ActvReSplrPosnCmd')  
        logger.info(f'获取到的原始数据ActvReSplrPosnCmd为{result_ori}')
        result = get_signal_times_interval(result_ori, 4)
        logger.info("期望值的统计结果:{}".format(result))
        assert result[0] !=0
    
    @pytest.mark.sanity
    def test_caseid_118429(self):
        '''尾翼堵转控制-破冰失败收回-->升起'''
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        ) 
        self.bus_comm.set_tailwing_pos(TailWingPos.P0)
        sleep(.5)
        self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrIceBreakFaild', 1)
        sleep(.5)
        self.bus_comm.check_signal_thread_start('cem_lin6', 'BgmCem_Lin6Fr01', 'ActvReSplrPosnCmd') 
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.On)
        self.soa.get_tailwing_mode(mode=TailWindMode.On)
        result_ori = self.bus_comm.check_signal_thread_stop('ActvReSplrPosnCmd')   
        logger.info(f'获取到的原始数据ActvReSplrPosnCmd为{result_ori}')
        result = get_signal_times_interval(result_ori, 4)
        logger.info("期望值的统计结果:{}".format(result))
        assert result[0] !=0
    
    @pytest.mark.sanity
    def test_caseid_118431(self):
        '''电动尾翼运动中收到新的档位请求'''
        self.sd_tester.write_ccp(ccp={211: 0x01, 564: 0x2})
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.check_signal_thread_start('cem_lin6', 'BgmCem_Lin6Fr01', 'ActvReSplrPosnCmd') 
        self.bus_comm.set_tailwing_pos(TailWingPos.Shifting)
        sleep(1)
        self.bus_comm.set_tailwing_pos(TailWingPos.P3)
        sleep(1)
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.Off)
        self.soa.get_tailwing_mode(mode=TailWindMode.Off)
        result_ori = self.bus_comm.check_signal_thread_stop('ActvReSplrPosnCmd')  
        logger.info(f'获取到的原始数据ActvReSplrPosnCmd为{result_ori}')
        result = get_signal_times_interval(result_ori, 1)
        logger.info("期望值的统计结果:{}".format(result))
        assert result[0] !=0

    @pytest.mark.sanity
    def test_caseid_109858(self):
        '''Normal下Driving模式车速小于65km/h,1s内不大于68尾翼自动收回'''
        self.sd_tester.write_ccp(ccp={211: 0x01, 564: 0x2})
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.set_tailwing_pos(TailWingPos.P3)
        sleep(.5)
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.Auto)
        self.bus_comm.check_signal_thread_start('cem_lin6', 'BgmCem_Lin6Fr01', 'ActvReSplrPosnCmd') 
        self.bus_comm.set_vehspd_gear(vehspd=17.05)#车速小于65km/h自动收回
        self.bus_comm.set_vehspd_gear(vehspd=18.5)
        sleep(1)
        result_ori = self.bus_comm.check_signal_thread_stop('ActvReSplrPosnCmd')   
        logger.info(f'获取到的原始数据ActvReSplrPosnCmd为{result_ori}')
        result = get_signal_times_interval(result_ori, 1)
        logger.info("期望值的统计结果:{}".format(result))        
        assert result[0] !=0

    @pytest.mark.sanity
    def test_caseid_1985540(self):
        '''尾翼处于升起状态nfc锁车后尾翼应自动收回'''
        self.bus_comm.set_tailwing_pos(TailWingPos.P3)
        sleep(.5)
        self.bus_comm.check_signal_thread_start('cem_lin6', 'BgmCem_Lin6Fr01', 'ActvReSplrPosnCmd')
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC) 
        result_ori = self.bus_comm.check_signal_thread_stop('ActvReSplrPosnCmd')   
        logger.info(f'获取到的原始数据ActvReSplrPosnCmd为{result_ori}')
        result = get_signal_times_interval(result_ori, 1)
        logger.info("期望值的统计结果:{}".format(result))
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        assert result[0] !=0
    
    @pytest.mark.sanity
    def test_caseid_1986705(self):
        '''堵转后尾翼可正常下发cmd'''
        self.bus_comm.set_tailwing_pos(TailWingPos.P3)
        sleep(1)
        self.bus_comm.check_signal_thread_start('cem_lin6', 'BgmCem_Lin6Fr01', 'ActvReSplrPosnCmd') 
        self.bus_comm.set('cem_lin6', 'AwmCem_Lin6Fr01','ActvReSplrMotBlk',1)
        sleep(1)
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.Off) 
        self.soa.get_tailwing_mode(mode=TailWindMode.Off)  
        result_ori = self.bus_comm.check_signal_thread_stop('ActvReSplrPosnCmd')  
        logger.info(f'获取到的原始数据ActvReSplrPosnCmd为{result_ori}')
        result = get_signal_times_interval(result_ori, 1)
        logger.info("期望值的统计结果:{}".format(result))
        assert result[0] !=0
        
    @pytest.mark.sanity
    def test_caseid_1986974(self):
        '''上内锁尾翼应能正常控制'''
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.set_tailwing_pos(TailWingPos.P0)
        sleep(1)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.check_signal_thread_start('cem_lin6', 'BgmCem_Lin6Fr01', 'ActvReSplrPosnCmd') 
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.On) 
        self.soa.get_tailwing_mode(mode=TailWindMode.On)  
        result_ori = self.bus_comm.check_signal_thread_stop('ActvReSplrPosnCmd')  
        logger.info(f'获取到的原始数据ActvReSplrPosnCmd为{result_ori}')
        result = get_signal_times_interval(result_ori, 4)
        logger.info("期望值的统计结果:{}".format(result))
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        assert result[0] !=0

    
    
    