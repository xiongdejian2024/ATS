# -*- coding: utf-8 -*-
"""
@File        : test_nvm_sleep_wakeup.py
@Author      : huajie.yang@jiduauto.com
@Time        : 2024/08/30
@Description : Test NVM storage functionality
"""
import pytest
import random
from xat_cases.legacy.bgm.mcu.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.common.logger import logger

class TestNvmStoraAbc(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update(["VehicleModeService_client","LightService_client"])
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.set_hood_sts(HoodSts.Close)
        self.io.set_door(Drvr=Door.close, Pass=Door.close, RiRe=Door.close, LeRe=Door.close, Trunk=Door.close)
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
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
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)


    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        super().after_class(self, ecu)
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
    
    def not_restart_bgm_network_sleep(self):
        # 断开诊断激活线
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.io.tcam_kl15_down()
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.stop_tester_present()
        # 设置车辆静止
        self.bus_comm.set_vehspd_gear(vehspd=0, gear=Gear.Park)
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)
        # 关闭四门两盖、座椅不占座、门外开关不按、没有踩刹车、危险报警灯不亮
        self.mix.set_seats_present_sts(
            drv_seat=SeatPresSts.NoPres,
            pass_seat=SeatPresSts.NoPres,
            sec_left=SeatPresSts.NoPres,
            sec_mid=SeatPresSts.NoPres,
            sec_right=SeatPresSts.NoPres
        )
        self.io.set_bgm_hardware_condition_to_default()
        self.io.set_hood_sts(HoodSts.Close)
        # 发送lin补电
        self.bus_comm.send_pdu('cem_lin6', 0x06, data=[0xFA, 0x3c, 0xc8, 0xff, 0xff, 0xff, 0xff])
        time.sleep(10)
        # 设置NFC锁车
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_four_door_and_tailgate_hood_sts(Door.close, DoorPos.All)
        self.bus_comm.check_central_lock_sts(CenLockSts.Lock, LockTrigerSource.NFC)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC25, NMSts.no_valid)
        self.bus_comm.stop_dk()
        # 清除缓存
        time.sleep(5)
        self.bus_comm.ipdu.rx_flag_reset_all()
        # 判断车辆模式是否是ABANDONED
        start_time = time.time()
        while time.time() - start_time < 60 * 15:
            try:
                self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.ABANDONED, timeout=0.2)
            except Exception:
                logger.info(f'当前不为{UsageMode.ABANDONED.value}状态')
            else:
                break
            sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.ABANDONED, timeout=0.2)
        time.sleep(20)
        self.bus_comm.pause_all_bus_send()
        self.bus_comm.send_pdu('cem_lin6', 0x06, data=[0xFA, 0x3c, 0xc8, 0xff, 0xff, 0xff, 0xff])
        time.sleep(40)
        # 检查CAN LIN FR是否有报文发出
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN1, sts=BusSendSts.Sleep)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN2, sts=BusSendSts.Sleep)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN3, sts=BusSendSts.Sleep)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN4, sts=BusSendSts.Sleep)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN5, sts=BusSendSts.Sleep)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN6, sts=BusSendSts.Sleep)

    def reset_bgm(self):
        self.not_restart_bgm_network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)

    @pytest.mark.full
    def test_caseid_1993340(self):
        '''展车模式存储与恢复'''
        self.bus_comm.set('backbonefr','BcmVddmBackBoneFr00', 'EpbStsEpbSts', 3)
        self.soa.send_method_request(
            'VehicleModeService_client',
            'SetExhibitionMode',
            {"isOpen": True},
        )
        self.soa.send_request_and_ck_resp(
            'VehicleModeService_client',
            "GetExhibitionModeSts",
            {},
            {"out": {"isOpen": True, "isValid": True}},
        )
        self.bus_comm.check(
            'propulsioncan','BgmPropulsionFr01',
            'ExhibitionModeStsExhibitionModeSts_1_BgmPropSignalIPdu01',
            'OnOff1_On'
        )
        time.sleep(1)
        self.reset_bgm()
        self.bus_comm.check(
            'propulsioncan','BgmPropulsionFr01',
            'ExhibitionModeStsExhibitionModeSts_1_BgmPropSignalIPdu01',
            'OnOff1_On',
        )

    # @pytest.mark.full
    # def test_caseid_1993347(self):
    #     '''40E4 BMS硬件故障计数'''
    #     ret_code, local_date = self.sd_tester.send_request_and_recv_response(
    #         [0x22, 0x40, 0xE4]
    #     )
    #     self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
    #     # LIN6信号 设置为11.8 BattURaw
    #     self.bus_comm.send_pdu("cem_lin6", 0x06, [0xE8, 0x7F, 0xC8, 0xff, 0xff, 0xff, 0xff])
    #     #仿真DcDcactvd 为1 避免低压报06
    #     self.bus_comm.set('backbonefr','VddmBackBoneFr08','DcDcActvd',1)
    #     sleep(1) 
    #     self.bus_comm.set('cem_lin6','BmsCem_Lin6Fr03', 'BattSnsrHwFltRaw', 1)
    #     sleep(10)
    #     self.bus_comm.set('cem_lin6','BmsCem_Lin6Fr03', 'BattSnsrHwFltRaw', 1)
    #     sleep(10)
    #     # UsageMode 设置为13 Driving
    #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
    #     sleep(5)
    #     self.bus_comm.check('backbonefr','CemBackBoneFr06', 'LVPwrSplyErrSts', 5)
    #     self.bus_comm.set('cem_lin6','BmsCem_Lin6Fr03', 'BattSnsrHwFltRaw', 0)  
    #     sleep(1)
    #     self.reset_bgm()
    #     ret_code, read_date = self.sd_tester.send_request_and_recv_response(
    #         [0x22, 0x40, 0xE4]
    #     )
    #     if read_date[7] != local_date[7]+1:
    #         assert 0, '硬件故障未记录'

    # @pytest.mark.full
    # def test_caseid_1993336(self):
    #     '''读FOTA状态F153存储'''
    #     self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
    #     logger.info("读FOTA状态值")
    #     self.sd_tester.send_request_and_recv_response(
    #         [0x22, 0xF1, 0x53]
    #     )
    #     sleep(.1)
    #     write_f153_list = [random.randint(0, 4)]
    #     self.sd_tester.send_request_and_recv_response(
    #         [0x2E, 0xF1, 0x53], write_f153_list, do_assert=True
    #     )
    #     sleep(1)
    #     logger.info("重启bgm")
    #     self.reset_bgm()
    #     logger.info("读FOTA状态值")
    #     self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
    #     ret_code, read_date = self.sd_tester.send_request_and_recv_response(
    #         [0x22, 0xF1, 0x53],
    #         recv=[0x62, 0xF1, 0x53] + write_f153_list,
    #         do_assert=True,
    #     )
    #     sleep(1)
    #     read_f153_lsit = read_date[3:]
    #     logger.info("恢复读FOTA状态值")
    #     self.sd_tester.send_request_and_recv_response(
    #         [0x2E, 0xF1, 0x53, 0x00]
    #     )
    #     if read_f153_lsit != write_f153_list:
    #         log_string = f"写入读FOTA状态值失败,读取结果本应为{bytes(write_f153_list).hex()}实际为{bytes(read_f153_lsit).hex()}"
    #         logger.info(log_string)
    #         assert 0, log_string

    # @pytest.mark.full
    # def test_caseid_1993344(self):
    #     '''40EF闭锁命令记录'''
    #     self.sd_tester.send_data([0x22, 0x40, 0xEF])
    #     result1 = self.sd_tester.return_udsdata_and_check_and_print_response_result()
    #     sleep(1)
    #     self.io.set_door(Drvr=Door.close, Pass=Door.close, RiRe=Door.close, LeRe=Door.close, Trunk=Door.close)
    #     self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
    #     sleep(5)
    #     self.reset_bgm()
    #     self.sd_tester.send_data([0x22, 0x40, 0xEF])
    #     result2 = self.sd_tester.return_udsdata_and_check_and_print_response_result()
    #     if result1 == result2:
    #         str1 = f'此次闭锁命令未记录'
    #         logger.info(str1)
    #         assert 0, str1

    # @pytest.mark.full
    # def test_caseid_1993338(self):
    #     '''nfc闭锁状态存储'''
    #     self.io.set_door(Drvr=Door.close, Pass=Door.close, RiRe=Door.close, LeRe=Door.close, Trunk=Door.close)
    #     self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
    #     sleep(1)
    #     logger.info("重启bgm")
    #     self.reset_bgm()
    #     self.bus_comm.check(
    #         'connectivitycanfd','VgmConnFr12',
    #         'LockgCenStsLockSt_2_VgmConnSignalIPdu12',
    #         3,
    #     )

    # @pytest.mark.full
    # def test_caseid_1993364(self):
    #     '''4109方向盘加热温度补偿'''
    #     self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L0)
    #     ret_code, local_date = self.sd_tester.send_request_and_recv_response(
    #         [0x22, 0x41, 0x09]
    #     )
    #     sleep(1)
    #     write_power_list = [random.randint(1, 15)]
    #     self.sd_tester.send_request_and_recv_response(
    #         [0x2E, 0x41, 0x09], write_power_list, do_assert=True
    #     )
    #     sleep(1)
    #     logger.info("bgm重启")
    #     self.reset_bgm()
    #     self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L0)
    #     ret_code, read_date = self.sd_tester.send_request_and_recv_response(
    #         [0x22, 0x41, 0x09],
    #         recv=[0x62, 0x41, 0x09] + write_power_list,
    #         do_assert=True,
    #     )
    #     sleep(1)
    #     read_power_lsit = read_date[3:]
    #     logger.info("恢复值")
    #     self.sd_tester.send_request_and_recv_response(
    #         [0x2E, 0x41, 0x09] + local_date[3:]
    #     )
    #     if read_power_lsit != write_power_list:
    #         log_string = f"写入值失败,读取结果本应为{bytes(write_power_list).hex()}实际为{bytes(read_power_lsit).hex()}"
    #         logger.info(log_string)
    #         assert 0, log_string


    # @pytest.mark.full
    # def test_caseid_1993361(self):
    #     '''内灯模式存储'''
    #     self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
    #     self.soa.send_method_request(
    #         "LightService_client",
    #         "LightControl",
    #         {
    #             "lights": [
    #                 {
    #                     "light": {"type": 26, "zoneId": 0},
    #                     "mode": 2,
    #                     "brightness": 0,
    #                     "color": {"cRed": 0, "cGreen": 0, "cBlue": 0},
    #                 }
    #             ]
    #         },
    #     )
    #     sleep(1)
    #     self.soa.send_request_and_ck_resp(
    #         "LightService_client", "GetInternalLightMode", {}, {"out": 2}
    #     )
    #     self.reset_bgm()
    #     self.soa.send_request_and_ck_resp(
    #         "LightService_client", "GetInternalLightMode", {}, {"out": 2}
    #     )

    # @pytest.mark.full
    # def test_caseid_1993362(self):
    #     '''EE99喇叭开关触发喇叭的次数和时间'''
    #     self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L0)
    #     self.sd_tester.send_data([0x22, 0xEE, 0x99])
    #     result1 = self.sd_tester.return_udsdata_and_check_and_print_response_result()
    #     self.io.set_horn_switch_sts(isOn.Off)#打开
    #     sleep(3)
    #     self.io.set_horn_switch_sts(isOn.On)#关闭
    #     self.sd_tester.send_request_and_recv_response([0x22, 0xEE, 0x99])
    #     sleep(1)
    #     self.reset_bgm()
    #     self.sd_tester.send_data([0x22, 0xEE, 0x99])
    #     result2 = self.sd_tester.return_udsdata_and_check_and_print_response_result()
    #     if result2[3] != result1[3] + 1:
    #         assert 0, "本次开关未存储"

   