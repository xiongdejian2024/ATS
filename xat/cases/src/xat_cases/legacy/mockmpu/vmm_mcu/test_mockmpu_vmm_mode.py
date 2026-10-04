# -*- coding: utf-8 -*-
"""
@File        : test_nvm_storage.py
@Author      : huajie.yang@jiduauto.com
@Time        : 2024/08/24 
@Description : Test Vmm MockMpu Mode
"""

from xat_cases.legacy.mockmpu.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.interface.nuc_app import *
import time,pytest

@allure.story("MockMpu")
@pytest.mark.sanity
class TestVmmMockMpu(TestABCBase):
    def before_class(self, ecu):
        logger.info("before_class")
        super().before_class(self, ecu)
        self.mockmpu.start_heart_beat()
        time.sleep(5)   

    def before_each_func(self, ecu):
        logger.info("before_each_func")
        super().before_each_func(ecu)
        self.bus_comm.set_vehmtn()
        self.mockmpu.set_signal("UsgModDwnSwtReq",1,1)
        self.bus_comm.check_usage_mode_status(UsageMode.INACTIVE)
        self.mockmpu_change_car_mode_and_check(CarMode.NORMAL)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        logger.info("after_each_func")

    def after_class(self, ecu):
        logger.info("after_class")
        super().after_class(self, ecu)
        self.mockmpu.set_signal('CarModChgReq', 0, 1, 200)
        self.bus_comm.check('backbonefr','CemBackBoneFr02' ,'VehModMngtGlbSafe1CarModSts1_0_CEMBackBoneSignalIpdu02', 0)

    def ctrl_lock(self, lock_type: LockCmd, ctrl_type: LockSource):
        with allure.step(f"通过{ctrl_type.name}方式控制{lock_type.name}"):
            logger.info(f"通过{ctrl_type.name}方式控制{lock_type.name}")
            self.io.set_bgm_hardware_condition_to_default()
            if ctrl_type.name == "NFC":
                logger.warning(f"发送NFC请求")
                self.bus_comm.centrl_lock_pre_msg_send_ctrl(sts=MsgSendContrl.Pause)
                if lock_type.name == "UnLock":
                    cen_lock_sts = self.bus_comm.get_central_lock_sts()
                    if cen_lock_sts == 3 or cen_lock_sts == 2:
                        self.bus_comm.send_nfc_cmd()
                        self.bus_comm.check_central_lock_sts(
                            exp_sts=CenLockSts.Unlock,
                            exp_trigsrc=LockTrigerSource.NFC,
                        )
                    else:
                        logger.warning(f"中控锁状态已经是UnLock状态,无需解锁")
                elif lock_type.name == "Lock":
                    cen_lock_sts = self.bus_comm.get_central_lock_sts()
                    if cen_lock_sts == 1:
                        self.bus_comm.send_nfc_cmd()
                        self.bus_comm.check_central_lock_sts(
                            exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC
                        )
                    else:
                        logger.warning(f"中控锁状态已经是Lock状态,无需上锁")
                elif lock_type.name == "LockCompleteArm":
                    cen_lock_sts = self.bus_comm.get_central_lock_sts()
                    if cen_lock_sts == 1 or cen_lock_sts == 2:
                        self.bus_comm.send_nfc_cmd()
                        self.bus_comm.check_central_lock_sts(
                            exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC
                        )
                    else:
                        logger.warning(f"中控锁状态已经是Lock状态,无需上锁")

    def set_central_unlock(self):
        '''设置中控解锁'''
        self.mockmpu.set_signal('MobDevCenLockReq', 1, 1)
        sleep(.1)
        self.bus_comm.check('connectivitycanfd','VgmConnFr12','LockgCenStsLockSt', 1)       
    
    def set_central_lock(self):
        '''设置中控闭锁'''
        self.io.set_door(Drvr=Door.close, Pass=Door.close, RiRe=Door.close, LeRe=Door.close, Trunk=Door.close)
        self.mockmpu.set_signal('MobDevCenLockReq', 2, 1)
        sleep(.1)
        self.bus_comm.check('connectivitycanfd','VgmConnFr12','LockgCenStsLockSt', 3)
        self.bus_comm.check('connectivitycanfd','VgmConnFr12', 'LockgCenStsTrigSrc', 1)

    def set_central_unlock_and_keyprsnt(self):
        '''设置中控解锁及寻钥'''
        self.mockmpu.set_signal('MobDevCenLockReq', 1, 1)
        sleep(.1)
        self.bus_comm.check('connectivitycanfd','VgmConnFr12','LockgCenStsLockSt', 1)
        self.bus_comm.update_keyinfos(3, [KeyInfo(KeyType.BLE_Key, key_id1, 0x6)])
        sleep(1)
        self.mockmpu.set_signal('KeyReadReqFromSrv', 3, 1)
        sleep(.2)
        # self.bus_comm.check('infocanfd','BgmInfoCanFdDevFr03', 'KeyReadStsToVMMNFCNFCKeyPrsnt', 3)
        #self.bus_comm.check('connectivitycanfd','VgmConnFr12', 'LockgCenStsTrigSrc', 1)

    def mockmpu_change_car_mode_and_check(self,carmode:CarMode):
        '''服务切car mode'''
        CAR_MODE_MAP = {
        0: "NORMAL",
        1: "TRANSPORT",
        2: "FACTORY",
        3: "CRASH",
        5: "DYNO"}
        car_mode_name = CAR_MODE_MAP.get(carmode)
        logger.info(f"设置car mode 为{car_mode_name}:{carmode}")
        self.mockmpu.set_signal('CarModChgReq', carmode.value, 1, 200)
        logger.info(f"验证切换结果是否为{car_mode_name}:{carmode}")
        self.bus_comm.check_car_mode_status(car_mode_main=carmode, car_mode_sub=0)
        
    def mockmpu_change_usage_mode_and_check_result(self, usagemode:UsageMode):
        '''服务切usagmode'''
        USAGE_MODE_MAP = {
        0: "ABANDONED",
        1: "INACTIVE",
        2: "CONVENIENCE",
        11: "ACTIVE",
        13: "DRIVING"}
        curren_usage_mode = self.bus_comm.get_usage_mode_status()
        curren_usage_mode_name = USAGE_MODE_MAP.get(curren_usage_mode)
        logger.info(f"当前模式为 为{curren_usage_mode_name}:{curren_usage_mode}")
        if curren_usage_mode < usagemode.value:
            self.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
            self.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
            method_name = "UsgModKeeperReq"
        elif curren_usage_mode > usagemode.value:
            method_name = "UsgModDwnSwtReq"
        else:
            # 已经是所需要模式，无需切换，直接返回
            return 1, curren_usage_mode, usagemode.value
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
        time.sleep(1)
        self.mockmpu.set_signal(method_name, usagemode.value, 1, 200)
        time.sleep(.1)
        self.bus_comm.check_usage_mode_status(usage_mode=usagemode)
    
    def ctrl_lock(self, lock_type: LockCmd, ctrl_type: LockSource):
        with allure.step(f"通过{ctrl_type.name}方式控制{lock_type.name}"):
            logger.info(f"通过{ctrl_type.name}方式控制{lock_type.name}")
            self.io.set_bgm_hardware_condition_to_default()
        if ctrl_type.name == "NFC":
                logger.warning(f"发送NFC请求")
                self.bus_comm.centrl_lock_pre_msg_send_ctrl(sts=MsgSendContrl.Pause)
                if lock_type.name == "UnLock":
                    cen_lock_sts = self.bus_comm.get_central_lock_sts()
                    if cen_lock_sts == 3 or cen_lock_sts == 2:
                        self.bus_comm.send_nfc_cmd()
                        self.bus_comm.check_central_lock_sts(
                            exp_sts=CenLockSts.Unlock,
                            exp_trigsrc=LockTrigerSource.NFC,
                        )
                    else:
                        logger.warning(f"中控锁状态已经是UnLock状态,无需解锁")
                elif lock_type.name == "Lock":
                    cen_lock_sts = self.bus_comm.get_central_lock_sts()
                    if cen_lock_sts == 1:
                        self.bus_comm.send_nfc_cmd()
                        self.bus_comm.check_central_lock_sts(
                            exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC
                        )
                    else:
                        logger.warning(f"中控锁状态已经是Lock状态,无需上锁")
                elif lock_type.name == "LockCompleteArm":
                    cen_lock_sts = self.bus_comm.get_central_lock_sts()
                    if cen_lock_sts == 1 or cen_lock_sts == 2:
                        self.bus_comm.send_nfc_cmd()
                        self.bus_comm.check_central_lock_sts(
                            exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC
                        )
                    else:
                        logger.warning(f"中控锁状态已经是Lock状态,无需上锁")

    def trigger_usage_mode_to_abandoned(self,wait_time:Union[int,float] = 180):
        # 2 发送lin 报文 补电
        self.bus_comm.set("cem_lin6","CemCem_Lin6Fr02", "BattSnsrStReq", 1)
        self.bus_comm.send_pdu("cem_lin6", 0x06, [0x0, 0x7c, 0xc8, 0xff, 0xff, 0xff, 0xff])
        logger.info("断开诊断激活线")
        self.io.bgm_diag_line_down()
        time.sleep(5)
        self.io.bgm_power_off()
        time.sleep(1)
        self.io.bgm_power_on()
        sleep(30)
        self.bus_comm.check("infocanfd", "BgmInfoCanFdFr20", 'DiagcComActv_0_BgmInfoCanFdSignalIPdu20', 0)
        # 3. 四门两盖关闭
        logger.info("关闭四门两盖")
        self.io.set_five_door_sts(Door.close)
        self.io.set_hood_sts(HoodSts.Close)
        # 四门两盖是否关闭
        self.bus_comm.check_four_door_and_tailgate_hood_sts(Door.close)
        # 4. 闭锁
        self.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        time.sleep(1)
        # 等待一定时间
        self.bus_comm.set("connectivitycanfd", "TcamConnectivityFr35", "TelmFctReq", 0)
        logger.info(f"最长等待{wait_time}秒,让 bgm 进入abandoned 模式，超过时间未进入则退出")
        self.bus_comm.check_usage_mode_status(UsageMode.ABANDONED,timeout=wait_time)

    def set_precon_to_abandon(self):
        self.bus_comm.set("bodycan", "CcmBodyFr34", "ClimaOvrHeatPrtSts", 0)
        self.bus_comm.set("connectivitycanfd", "BncmConnectivityFr17", "UsgModChgReqFromBLE", 0)
        self.bus_comm.set("backbonefr", "VddmBackBoneFr09", "HvEgyLoadFctReq", 0)
        self.bus_comm.set("backbonefr", "VddmBackBoneFr28", "HvOnMaiReq", 0)
        self.bus_comm.set("connectivitycanfd", "TcamConnectivityFr35", "TelmFctReq", 0)
        self.bus_comm.set("bodycan", "LpodBodyFr01", "DoorLeReOpenReqOutdSwt2", 2)
        self.io.trigger_door_outswitch_sts(LeRe=OutSwitchPressSts.NoPress)
        self.bus_comm.set("backbonefr", "BbmBackBoneFr04", "EpbLampReqSecEpbLampReq", 0)
        self.bus_comm.set("backbonefr", "BcmVddmBackBoneFr39", "EpbLampReqEpbLampReq", 0)
        self.bus_comm.set("infocanfd", "CdcInfoCanFdFr03", "MmedHdPwrMod", 0)
        self.bus_comm.set("backbonefr", "VddmBackBoneFr00", "PtCoolgPostRunActv", 0)
        self.bus_comm.set("connectivitycanfd", "TcamConnectivityFr12", "RemHvStrtActvReq", 0)
        self.bus_comm.set("propulsioncan", "EgsmPropFr01", "DrvrGearShiftParkReq1", 0)
        self.bus_comm.set("bodycan", "PpodBodyFr01", "DoorPassOpenReqOutdSwt2", 2)
        self.io.trigger_door_outswitch_sts(Pass=OutSwitchPressSts.NoPress)
        self.bus_comm.set("bodycan", "RpodBodyFr01", "DoorRiReOpenReqOutdSwt2", 2)
        self.io.trigger_door_outswitch_sts(RiRe=OutSwitchPressSts.NoPress)
        self.bus_comm.set("bodycan", "DdmBodyFr04", "DoorDrvrOpenReqInsdSwt1", 0)
        self.bus_comm.set("bodycan", "DpodBodyFr01", "DoorDrvrOpenReqInsdSwt2", 0)
        self.bus_comm.set("bodycan", "RrdmBodyFr01", "DoorRiReOpenReqInsdSwt1", 0)
        self.bus_comm.set("bodycan", "RpodBodyFr01", "DoorRiReOpenReqInsdSwt2", 0)
        self.bus_comm.set("bodycan", "RldmBodyFr01", "DoorLeReOpenReqInsdSwt1", 0)
        self.bus_comm.set("bodycan", "LpodBodyFr01", "DoorLeReOpenReqInsdSwt2", 0)
        self.bus_comm.set("bodycan", "PdmBodyFr01", "DoorPassOpenReqInsdSwt1", 0)
        self.bus_comm.set("bodycan", "PpodBodyFr01", "DoorPassOpenReqInsdSwt2", 0)
        self.mockmpu.set_signal("SwtCDCLiLoBeamSw", 0, 2)
        self.mockmpu.set_signal("SwtCDCLiPosLampSw", 0, 2)
        self.mockmpu.set_signal("SwtCDCLiAutoLampSw", 0, 2)   
        self.bus_comm.check("bodycan", "CemBodyFr02", "TrOpenerReqTrOpenerReq", 0)
        self.mockmpu.set_signal("StaticLightingModeReq", 0, 2)
        self.mockmpu.set_signal("DrvrAsscSysIndcrReq", 0, 2)
        self.bus_comm.set_brake_pedal(safe=YesOrNo.No,qf=ValueQf.UndefindDataAccur,sts=YesOrNo.No)

    def trigger_usagmode_to_abandoned(self):
        """usagmode进abandon"""
        self.set_precon_to_abandon()    
        self.trigger_usage_mode_to_abandoned()

    def test_caseid_1993514(self):
        '''不存在有效钥匙时不能上切usagmode''' 
        self.mockmpu_change_usage_mode_and_check_result(UsageMode.INACTIVE)
        self.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.mockmpu.set_signal('KeyReadReqFromSrv', 3, 1)
        sleep(.2)
        self.mockmpu.set_signal("UsgModKeeperReq", 2)
        self.bus_comm.check_usage_mode_status(UsageMode.INACTIVE)

    def test_caseid_1993515(self):
        '''存在有效钥匙时上切usagmode''' 
        # self.set_central_unlock_and_keyprsnt()
        self.bus_comm.update_keyinfos(3, [KeyInfo(KeyType.BLE_Key, key_id1, 0x6)])
        self.mockmpu_change_usage_mode_and_check_result(UsageMode.INACTIVE)
        self.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.mockmpu.set_signal("UsgModKeeperReq", 2)
        self.bus_comm.check_usage_mode_status(UsageMode.CONVENIENCE)
        
    @pytest.mark.sanity
    def test_caseid_1993520(self):
        """灯光秀打开触发abandon上切inactive"""
        self.trigger_usagmode_to_abandoned()
        self.mockmpu.set_signal("StaticLightingModeReq", 1, 2)
        self.bus_comm.check('bodyexposedcanfd', 'BgmBodyExposedCANFr10', 'StaticLightingModeEn', 1)
        self.bus_comm.set(
                'bodyexposedcanfd','HcmlBodyExpoFr02', 'StsOfLedFrntLampLe1', 0
            )
        self.bus_comm.set(
            'bodyexposedcanfd','HcmlBodyExpoFr02', 'StsOfLedFrntLampLe2', 0
        )
        self.bus_comm.set(
            'bodyexposedcanfd','HcmlBodyExpoFr02', 'StsOfLedFrntLampMid1', 0
        )
        self.bus_comm.set(
            'bodyexposedcanfd','HcmrBodyExpoFr02', 'StsOfLedFrntLampRi1', 0
        )
        self.bus_comm.set(
            'bodyexposedcanfd','HcmrBodyExpoFr02', 'StsOfLedFrntLampRi2', 0
        )
        self.bus_comm.set(
            'bodyexposedcanfd','RcmlBodyExpoFr01', 'StsOfLedReLampLe1', 0
        )
        self.bus_comm.set(
            'bodyexposedcanfd','RcmlBodyExpoFr01', 'StsOfLedReLampLe2', 0
        )
        self.bus_comm.set(
            'bodyexposedcanfd','RcmrBodyExpoFr01', 'StsOfLedReLampRi1', 0
        )
        self.bus_comm.set(
            'bodyexposedcanfd','RcmrBodyExpoFr01', 'StsOfLedReLampRi2', 0)
        self.bus_comm.check('backbonefr', 'CemBackBoneFr02', 'ExtrLtgStsStaticLtgShow', 1)
        self.bus_comm.check_usage_mode_status(UsageMode.INACTIVE)

    @pytest.mark.hj
    def test_caseid_1993519(self):
        """危险报警指示灯打开触发abandon上切inactive"""       
        self.trigger_usagmode_to_abandoned()
        self.mockmpu.set_signal("DrvrAsscSysIndcrReq", 3, 2)
        self.bus_comm.check('backbonefr', 'CemBackBoneFr03', 'IndcrSts', 3)
        self.bus_comm.check_usage_mode_status(UsageMode.INACTIVE)

    def test_caseid_1993518(self):
        """锁状态改变触发abandon上切inactive"""
        self.trigger_usagmode_to_abandoned()
        self.mockmpu.set_signal("MobDevCenLockReq", 1, 1)
        self.bus_comm.check('connectivitycanfd','VgmConnFr12','LockgCenStsLockSt', 1) 
        self.bus_comm.check_usage_mode_status(UsageMode.INACTIVE)

    def test_caseid_1993517(self):
        """诊断仪连接触发abandon上切inactive"""
        self.trigger_usagmode_to_abandoned()
        self.mockmpu.set_signal("DiagcExtCom", 1, 1)
        self.mockmpu.set_signal("DiagcComActv", 1, 1)
        self.bus_comm.check('backbonefr','VgmBackBoneFr10','DiagcExtCom', 1) 
        self.bus_comm.check('backbonefr','VgmBackBoneFr00','DiagcComActv', 1) 
        self.bus_comm.check_usage_mode_status(UsageMode.INACTIVE)
   
    def test_caseid_1993516(self):
        """fota升级触发abandon上切inactive"""
        self.trigger_usagmode_to_abandoned()
        self.mockmpu.set_signal("FOTAStatus", 4, 2)
        self.bus_comm.check(
                'backbonefr','CemBackBoneFr15', 'FOTAStatus', 4
            )
        self.bus_comm.check_usage_mode_status(UsageMode.INACTIVE)


    def test_caseid_1993521(self):
        '''DoorOpenerDrvrReq变化触发abandon上切inactive'''
        self.trigger_usagmode_to_abandoned()   
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval= 0.1)
        self.bus_comm.check('bodycan', 'CemBodyFr78', 'DoorOpenerDrvrReqDoorOpenerReq2', 1)
        self.bus_comm.check_usage_mode_status(UsageMode.INACTIVE)

    def test_caseid_1993522(self):
        '''DoorOpenerLeReReq变化触发abandon上切inactive'''
        self.trigger_usagmode_to_abandoned()   
        self.mix.push_door_outer_switch(pos=DoorPos.RearLeft,time_interval= 0.1)
        self.bus_comm.check('bodycan', 'CemBodyFr78', 'DoorOpenerLeReReqDoorOpenerReq2', 1)
        self.bus_comm.check_usage_mode_status(UsageMode.INACTIVE)
    
    def test_caseid_1993523(self):
        '''DoorOpenerPassReq变化触发abandon上切inactive'''
        self.trigger_usagmode_to_abandoned()   
        self.mix.push_door_outer_switch(pos=DoorPos.Pass,time_interval= 0.1)
        self.bus_comm.check('bodycan', 'CemBodyFr79', 'DoorOpenerPassReqDoorOpenerReq2', 1)
        self.bus_comm.check_usage_mode_status(UsageMode.INACTIVE)

    def test_caseid_1993524(self):
        '''DoorOpenerRiRe变化触发abandon上切inactive'''
        self.trigger_usagmode_to_abandoned()   
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval= 0.1)
        self.bus_comm.check('bodycan', 'CemBodyFr79', 'DoorOpenerRiReReqDoorOpenerReq2', 1)
        self.bus_comm.check_usage_mode_status(UsageMode.INACTIVE)

    