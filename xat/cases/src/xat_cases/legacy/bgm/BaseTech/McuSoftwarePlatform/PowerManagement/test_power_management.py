#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_steerwheel_ctrl.py
@Author      : hui.zhao@jiduauto.com
@Time        : 2023/11/21 11:30
@Description: BGM车控车方向盘功能
"""

import os
import sys
import threading
import time

import pytest
import allure
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.BaseTech.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from datetime import datetime
from framework.automotive.utils.data_type import EcuInfo

@allure.feature("电源管理")
@allure.story("电源管理测试")
class TestBgmPowerManagement(TestABCBase):
    def before_class(self, ecu):
        self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x4})
        self.bus_comm.set_Hv_sys_relay_sts(HvSysRelaySts.Close)

        self.io.tcam_power_off()

    def before_each_func(self, ecu):
        self.io.hazard_light_close()
        self.io.io.charge_lid_close()
        self.io.io.brake_up()
        self.io.io.hood_door2_open()
        self.io.io.drvr_door_outswitch_unpressed()
        self.io.io.drvr_door_close()
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.mix.set_car_mode(CarMode.NORMAL)

    def after_each_func(self, ecu):
        self.io.bgm_diag_line_up()
        self.io.tcam_kl15_up()
        # self.io.tcam_power_off()
        self.bus_comm.resume_all_bus_send()
        sleep(3)

    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
        self.io.tcam_power_on()

    def check_keyinfo(self, log_data, key_word, **kwargs):

        if log_data.find(key_word) != -1:
            string = f"查询到关键信息：{key_word}"
            with allure.step(string):
                logger.info(string)
        else:
            string = f"未能查询到关键信息：{key_word}"
            with allure.step(string):
                logger.error(string)
            assert False, string

    @allure.title("BGM_台架_休眠_门把手开关J3-38关闭")
    def test_pm_off_caseid_111253_111256_111268_111259(self):
        self.io.io.rire_door_outswitch_pressed()
        self.mix.network_sleep()
        self.io.io.rire_door_outswitch_unpressed()

        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN1, sts=BusSendSts.Sleep)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN2, sts=BusSendSts.Sleep)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN3, sts=BusSendSts.Sleep)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN4, sts=BusSendSts.Sleep)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN5, sts=BusSendSts.Sleep)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN6, sts=BusSendSts.Sleep)

        self.io.bgm_diag_line_up()
        sleep(20)
        sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
        # key_info="stop send heart beat to mcu"
        # self.check_keyinfo(sleep_log_last, key_info)
        
                # em2 kill 所有进程111259
        key_word = "mpu send shutdown ready succeed"
        key_word2 = "Shutdown safety"
        assert sleep_log_last.find(key_word) != -1 or sleep_log_last.find(key_word2) != -1
    

    @allure.title("BGM_台架_休眠_四门未关闭_门open")
    def test_pm_off_caseid_111224(self):
        self.mix.network_sleep()
        with allure.step(f"打开门"):
            self.io.io.drvr_door_open()
            self.io.io.pass_door_open()
        time.sleep(4)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN6, sts=BusSendSts.Awakeup)
        logger.info("延时一段时间等待休眠")
        time.sleep(5 * 60)
        t = time.time()
        timeout = 7 * 60
        ret = 0
        while time.time() - t < timeout:
            time.sleep(5)
            try:
                self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN1, sts=BusSendSts.Sleep)
                self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN2, sts=BusSendSts.Sleep)
                self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN3, sts=BusSendSts.Sleep)
                self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN4, sts=BusSendSts.Sleep)
                self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN5, sts=BusSendSts.Sleep)
                self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN6, sts=BusSendSts.Sleep)
                ret = 1
                with allure.step(f"耗时{time.time()-t}秒"):
                    logger.info(f"耗时{time.time()-t}秒")
                break
            except Exception as e:
                logger.warning(f"未休眠{str(e)}")

        self.io.bgm_diag_line_up()
        time.sleep(10)
        assert ret, " 打开门后未休眠"

    @pytest.mark.smoke
    @pytest.mark.V_1_4
    def test_pm_off_caseid_111230_111274_1919191_1919208_1919273_111241(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN6, sts=BusSendSts.Awakeup)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN6, sts=BusSendSts.Awakeup)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN6, sts=BusSendSts.Awakeup)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        sleep(15)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN6, sts=BusSendSts.Awakeup)
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.mix.network_sleep()
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN6, sts=BusSendSts.Sleep)

        self.io.bgm_diag_line_up()
        sleep(40)
        self.sd_tester.start_sd_tester()
        key_info = "wakeup reason: 22"
        sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
        self.check_keyinfo(awakeup_log_last, key_info)
        key_info="stop send heart beat to mcu"
        self.check_keyinfo(sleep_log_last, key_info)


    @allure.title("Check:重启原因：reboot reason: 0 ")
    @pytest.mark.smoke
    def test_pm_on_caseid_1919208(self):

        key_info = "reboot reason: 0"
        sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
        self.check_keyinfo(awakeup_log_last, key_info)

    @allure.title("Check:MPU的启动时长：SendSlvBootCompleted")
    @pytest.mark.smoke
    def test_pm_on_caseid_1919273(self):
        key_info = "SendSlvBootCompleted"
        sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
        self.check_keyinfo(awakeup_log_last, key_info)


    @allure.title("Check:power mode: 1")
    @pytest.mark.smoke
    def test_pm_off_caseid_111276(self):

        self.sd_tester.update_serverdoipid(0x1002)
        ret_code, ret_msg = self.sd_tester.send_request_and_recv_response([0x22, 0x0F1, 0X86], recv=[0x62, 0x0F1, 0X86])
        if ret_msg[3] == 0x02:
            self.sd_tester.update_serverdoipid(0x1FFF)
            self.sd_tester.send_data([0x10, 0x01])
            sleep(40)  # 等待日志落盘

        sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
        key_info = "power mode: 1"
        self.check_keyinfo(sleep_log_last, key_info)

    @allure.title("Check:电源模式OnEvent:Received shutdown prepare")
    @pytest.mark.smoke
    def test_pm_off_caseid_111265(self):

        key_info = "Received shutdown prepare"
        sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
        self.check_keyinfo(sleep_log_last, key_info)

    @allure.title("MPU回复：SendShutdownReady")
    @pytest.mark.smoke
    def test_pm_off_caseid_111246(self):
        key_info = "SendShutdownReady"
        sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
        self.check_keyinfo(sleep_log_last, key_info)

    @allure.title("Check:关闭网络 Received shutdown2 response with nullptr")
    @pytest.mark.smoke
    def test_pm_off_caseid_111262(self):
        key_info = "Received shutdown2 response with nullptr"
        sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
        self.check_keyinfo(sleep_log_last, key_info)


    @allure.title("Check:MCU状态：MCU be in  app mode")
    @pytest.mark.smoke
    def test_pm_on_caseid_111207(self):
        self.sd_tester.update_serverdoipid(0x1002)
        ret_code, ret_msg = self.sd_tester.send_request_and_recv_response([0x22, 0x0F1, 0X86], recv=[0x62, 0x0F1, 0X86])
        if ret_msg[3] == 0x02:
            self.sd_tester.update_serverdoipid(0x1FFF)
            self.sd_tester.send_data([0x10, 0x01])
            sleep(45)  # 等待日志落盘

        key_info = "MCU be in  app mode"
        sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
        self.check_keyinfo(awakeup_log_last, key_info)

    @allure.title("Check:EM启动状态：EM state manager proxy success")
    @pytest.mark.smoke
    def test_pm_on_caseid_111215(self):

        key_info = "EM state manager proxy success"
        sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
        self.check_keyinfo(awakeup_log_last, key_info)

    @allure.title("Check:电源模式：power mode: 2 ")
    @pytest.mark.smoke
    def test_pm_on_caseid_111233(self):
        key_info = "power mode: 2"
        sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
        self.check_keyinfo(awakeup_log_last, key_info)

    @allure.title("Check:以太网正常连接：INC link status from 0 to 1")
    @pytest.mark.smoke
    def test_pm_on_caseid_1919274(self):
        key_info = "INC link status from 0 to 1"
        sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
        self.check_keyinfo(awakeup_log_last, key_info)

    @allure.title("Check:恢复发送心跳：sent heart beat to mcu ")
    @pytest.mark.smoke
    def  test_pm_on_caseid_1919275(self):
        key_info = "sent heart beat to mcu"
        sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
        self.check_keyinfo(awakeup_log_last, key_info)


    @allure.title(f"引擎盖： wakeup reason: {Wakeup_Reasons.WAKEUP_BY_HOOD2.value} ")
    @pytest.mark.sanity
    def test_pm_on_caseid_1919195(self):
        self.sleep_and_wakeup_func(Wakeup_Reasons.WAKEUP_BY_HOOD2)



    @allure.title(f"硬线刹车开关： wakeup reason: {Wakeup_Reasons.WAKEUP_BY_BRAKE.value} ")
    @pytest.mark.sanity
    def test_pm_on_caseid_111219(self):
        self.sleep_and_wakeup_func(Wakeup_Reasons.WAKEUP_BY_BRAKE)



    @allure.title(f"硬线门开关状态： wakeup reason: {Wakeup_Reasons.WAKEUP_BY_FLDOOR_LOCK_SW.value} ")
    @pytest.mark.sanity
    def test_pm_on_caseid_111239(self):
        self.sleep_and_wakeup_func(Wakeup_Reasons.WAKEUP_BY_FLDOOR_LOCK_SW)



    @allure.title(f"Check:充电口盖打开： wakeup reason: {Wakeup_Reasons.WAKEUP_BY_CHARGELID.value} ")
    @pytest.mark.sanity
    def test_pm_on_caseid_111257(self):
        self.sleep_and_wakeup_func(Wakeup_Reasons.WAKEUP_BY_CHARGELID)



    @allure.title(f"硬线门把手状态： wakeup reason: {Wakeup_Reasons.WAKEUP_BY_FLDOOR_SW.value} ")
    @pytest.mark.sanity
    def test_pm_on_caseid_111214(self):
        self.sleep_and_wakeup_func(Wakeup_Reasons.WAKEUP_BY_FLDOOR_SW)



    @allure.title(f"Check:危险报警灯打开： wakeup reason: {Wakeup_Reasons.WAKEUP_BY_HAZARD.value} ")
    @pytest.mark.sanity
    def test_pm_on_caseid_111218(self):

        self.sleep_and_wakeup_func(Wakeup_Reasons.WAKEUP_BY_HAZARD)



    @allure.title(f"BodyExposedCANFD nm ： wakeup reason: {Wakeup_Reasons.WAKEUP_BY_BODYEXPCANCANFD.value} ")
    @pytest.mark.sanity
    def test_pm_on_caseid_111204(self):
        self.sleep_and_wakeup_func(Wakeup_Reasons.WAKEUP_BY_BODYEXPCANCANFD)

    #
    @allure.title(f"DIAGCAN nm： wakeup reason: {Wakeup_Reasons.WAKEUP_BY_DIAGCAN.value} ")
    @pytest.mark.sanity
    def test_pm_on_caseid_1919212(self):
        self.sleep_and_wakeup_func(Wakeup_Reasons.WAKEUP_BY_DIAGCAN)

    #
    #
    @allure.title(f"propulsioncan nm： wakeup reason: {Wakeup_Reasons.WAKEUP_BY_PROPULSIONCAN.value} ")
    @pytest.mark.sanity
    def test_pm_on_caseid_1981898(self):
        self.mix.network_sleep()
        canid = random.randint(0x500, 0x53f + 1)
        byte0=int(hex(canid)[3:],16)
        with allure.step(f"Step:执行 propulsioncan 网络NM帧canid={hex(canid)}唤醒BGM"):
            self.bus_comm.ipdu.add_msg("propulsioncan", canid,
                                       [byte0, 0x40, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00])
            logger.info(f"仿真网络管理报文唤醒如：propulsioncan CANFD {hex(canid)} {byte0} 40 00 80 00 00 00 00 唤醒源7")
            self.bus_comm.send_awakeup_msg("propulsioncan", canid, f"{str(byte0).zfill(2)} 40 00 00 00 01 00 00", 20, 20)

        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN6, sts=BusSendSts.Awakeup)
        logger.info(f'连接诊断激活线')
        self.io.bgm_diag_line_up()
        self.io.tcam_kl15_up()
        sleep(40)  # 等待日志打印完整，否则日志获取不全
        sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
        key_info = f"wakeup reason: {Wakeup_Reasons.WAKEUP_BY_PROPULSIONCAN.value}"
        self.check_keyinfo(awakeup_log_last, key_info)

    # @allure.title(f"ALM1 nm： wakeup reason: {Wakeup_Reasons.WAKEUP_BY_ALM1.value} ")
    # @pytest.mark.full
    # def test_pm_on_caseid_1919213(self):
    #     self.sleep_and_wakeup_func(Wakeup_Reasons.WAKEUP_BY_ALM1)

    # @allure.title(f"ALM2 nm： wakeup reason: {Wakeup_Reasons.WAKEUP_BY_ALM2.value} ")
    # @pytest.mark.full
    # def test_pm_on_caseid_1919214(self):
    #     self.sleep_and_wakeup_func(Wakeup_Reasons.WAKEUP_BY_ALM2)

    # @allure.title(f"backbonefr nm： wakeup reason: {Wakeup_Reasons.WAKEUP_BY_FLEXRAY.value} ")
    # @pytest.mark.full
    # def test_pm_on_caseid_1919215(self):
    #     self.sleep_and_wakeup_func(Wakeup_Reasons.WAKEUP_BY_FLEXRAY)

    @allure.title(f"LIN1电平唤醒： wakeup reason: {Wakeup_Reasons.WAKEUP_BY_LIN1.value} ")
    @pytest.mark.smoke
    def test_pm_on_caseid_1919199(self):
        self.sleep_and_wakeup_func(Wakeup_Reasons.WAKEUP_BY_LIN1)

    @allure.title(f"LIN2电平唤醒： wakeup reason: {Wakeup_Reasons.WAKEUP_BY_LIN2.value} ")
    @pytest.mark.full
    def test_pm_on_caseid_1919201(self):
        self.sleep_and_wakeup_func(Wakeup_Reasons.WAKEUP_BY_LIN2)

    @allure.title(f"LIN3电平唤醒： wakeup reason: {Wakeup_Reasons.WAKEUP_BY_LIN3.value} ")
    @pytest.mark.full
    def test_pm_on_caseid_1919202(self):
        self.sleep_and_wakeup_func(Wakeup_Reasons.WAKEUP_BY_LIN3)

    @allure.title(f"LIN4电平唤醒： wakeup reason: {Wakeup_Reasons.WAKEUP_BY_LIN4.value} ")
    @pytest.mark.full
    def test_pm_on_caseid_1919203(self):
        self.sleep_and_wakeup_func(Wakeup_Reasons.WAKEUP_BY_LIN4)

    @allure.title(f"LIN5电平唤醒： wakeup reason: {Wakeup_Reasons.WAKEUP_BY_LIN5.value} ")
    @pytest.mark.full
    def test_pm_on_caseid_1919204(self):
        self.sleep_and_wakeup_func(Wakeup_Reasons.WAKEUP_BY_LIN5)

    @allure.title(f"LIN6电平唤醒： wakeup reason: {Wakeup_Reasons.WAKEUP_BY_LIN6.value} ")
    @pytest.mark.full
    def test_pm_on_caseid_1919205(self):
        self.sleep_and_wakeup_func(Wakeup_Reasons.WAKEUP_BY_LIN6)

    @allure.title(f"WAKEUP_BY_CLASSICCAN1 nm 唤醒： wakeup reason: {Wakeup_Reasons.WAKEUP_BY_CLASSICCAN1.value} ")
    @pytest.mark.full
    def test_pm_on_caseid_1919209(self):

        self.sleep_and_wakeup_func(Wakeup_Reasons.WAKEUP_BY_CLASSICCAN1)

    @allure.title(f"WAKEUP_BY_CLASSICCAN2 nm 唤醒： wakeup reason: {Wakeup_Reasons.WAKEUP_BY_CLASSICCAN2.value} ")
    @pytest.mark.full
    def test_pm_on_caseid_1919210(self):

        self.sleep_and_wakeup_func(Wakeup_Reasons.WAKEUP_BY_CLASSICCAN2)

    @allure.title(f"WAKEUP_BY_INFOCAN nm 唤醒： wakeup reason: {Wakeup_Reasons.WAKEUP_BY_INFOCAN.value} ")
    @pytest.mark.full
    def test_pm_on_caseid_1919211(self):

        self.sleep_and_wakeup_func(Wakeup_Reasons.WAKEUP_BY_INFOCAN)

    @allure.title(f"WAKEUP_BY_ADCAN nm 唤醒： wakeup reason: {Wakeup_Reasons.WAKEUP_BY_ADCAN.value} ")
    @pytest.mark.sanity
    def test_pm_on_caseid_111254(self):
        self.sleep_and_wakeup_func(Wakeup_Reasons.WAKEUP_BY_ADCAN)

    @allure.title(f"WAKEUP_BY_ACTIVATION_LINE 唤醒： wakeup reason: {Wakeup_Reasons.WAKEUP_BY_ACTIVATION_LINE.value} ")
    @pytest.mark.smoke
    def test_pm_on_caseid_1985480(self):
        self.sleep_and_wakeup_func(Wakeup_Reasons.WAKEUP_BY_ACTIVATION_LINE)

    @allure.title(f"WAKEUP_BY_PROPULSIONCAN 唤醒： wakeup reason: {Wakeup_Reasons.WAKEUP_BY_PROPULSIONCAN.value} ")
    @pytest.mark.full
    def test_pm_on_caseid_111273(self):
        self.sleep_and_wakeup_func(Wakeup_Reasons.WAKEUP_BY_PROPULSIONCAN)

    @allure.title(f"WAKEUP_BY_PASSIVESAFETYCAN 唤醒： wakeup reason: {Wakeup_Reasons.WAKEUP_BY_PASSIVESAFETYCAN.value} ")
    @pytest.mark.full
    def test_pm_on_caseid_111237(self):
        self.sleep_and_wakeup_func(Wakeup_Reasons.WAKEUP_BY_PASSIVESAFETYCAN)

    @allure.title(f"WAKEUP_BY_CONNCANFD nm唤醒： wakeup reason: {Wakeup_Reasons.WAKEUP_BY_CONNCANFD.value} ")
    @pytest.mark.sanity
    def test_pm_on_caseid_111269(self):
        self.sleep_and_wakeup_func(Wakeup_Reasons.WAKEUP_BY_CONNCANFD)

    @allure.title(f"WAKEUP_BY_BODYCAN nm唤醒： wakeup reason: {Wakeup_Reasons.WAKEUP_BY_BODYCAN.value} ")
    @pytest.mark.sanity
    def test_pm_on_caseid_111332(self):
        self.sleep_and_wakeup_func(Wakeup_Reasons.WAKEUP_BY_BODYCAN)

    @allure.title(f"BGM_台架_运行过程_s2s进程异常")
    @pytest.mark.full
    def test_2s2_caseid_1981893(self):

        cmd1 = 'ps -ef|grep "s2s_service"|grep -v grep'
        ret = self.ssh.type_commands(DeviceName.BGM, cmd1, timeout=30)
        logger.info(f"获取的S2S={ret}")
        data_list = [item for item in ret.split(" ") if item.strip()]
        s2s_id = int(data_list[1])
        # kill  进程
        cmd = f'kill -9 {s2s_id}'
        self.ssh.type_commands(DeviceName.BGM, cmd, timeout=30)
        sleep(3)
        cmd2 = 'ps -ef|grep "s2s_service"|grep -v grep'
        ret2 = self.ssh.type_commands(DeviceName.BGM, cmd2, timeout=30)
        logger.info(f"获取的S2S_new={ret2}")
        data_list2 = [item for item in ret2.split(" ") if item.strip()]
        s2s_id_new = int(data_list2[1])

        assert s2s_id_new > s2s_id, ""

    @allure.title(f"BGM_FED5_MCU请求重启")
    @pytest.mark.full
    def test_caseid_1919271(self):
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.send_request_and_recv_response([0x11, 0x01])
        sleep(40)  # 等日志落盘
        # 62 FE D5 00 00 00 00 00 00 00 00 00 00 01 00 00 00 00 00 00
        ret, data = self.sd_tester.send_request_and_recv_response([0x22, 0x0FE, 0XD5])
        assert data[13] == 0x01, ""
        # Received power mode: 2, wakeup reason: 1, reboot reason: 1
        sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
        assert "reboot reason: 1" in awakeup_log_last

    @allure.title(f"BGM_FED5_MPU请求重启")
    @pytest.mark.full
    def test_caseid_1919272(self):
        self.sd_tester.update_serverdoipid(0x1001)
        self.sd_tester.send_request_and_recv_response([0x11, 0x01])
        sleep(40)  # 等日志落盘
        # 62 FE D5 00 00 00 00 00 00 00 00 00 00 01 00 00 00 00 00 00
        self.sd_tester.update_serverdoipid(0x1002)
        ret, data = self.sd_tester.send_request_and_recv_response([0x22, 0x0FE, 0XD5])
        assert data[13] == 0x01, ""
        # Received power mode: 2, wakeup reason: 1, reboot reason: 1
        sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
        assert "reboot reason: 1" in awakeup_log_last or "reboot reason: 2" in awakeup_log_last

    @allure.title(f"BGM_FED5_断电重启")
    @pytest.mark.full
    def test_caseid_1919270(self):
        self.io.bgm_power_off()
        sleep(3)
        self.io.bgm_power_on()
        sleep(40)  # 等日志落盘
        # 62 FE D5 00 00 00 00 00 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        ret, data = self.sd_tester.send_request_and_recv_response([0x22, 0x0FE, 0XD5])
        assert data[11] == 0x01, ""
        # Received power mode: 2, wakeup reason: 1, reboot reason: 0
        sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
        assert "reboot reason: 0" in awakeup_log_last

    def sleep_and_wakeup_func(self, wakeup_reason: Wakeup_Reasons, **kwargs):
        '''
        休眠唤醒 并校验 唤醒源
        @param wakeup_reason:
        @return:
        '''
        wakeup_reason_value = kwargs.get("wakeup_reason_value", None)
        self.mix.network_sleep()
        logger.info("休眠结束，开始唤醒")
        self.mix.network_wakeup(wakeup_reason=wakeup_reason, **kwargs)
        sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
        if wakeup_reason_value is None:
            key_info = f"wakeup reason: {wakeup_reason.value}"
        else:
            key_info = f"wakeup reason: {wakeup_reason_value}"
        self.check_keyinfo(awakeup_log_last, key_info)




@allure.feature("电源管理")
@allure.story("电源管理测试")
class TestBgmPowerManagementSingle(TestABCBase):

    @staticmethod
    def change_bench_config(ecu: EcuInfo) -> EcuInfo:
        """子类重写该接口，自定义台架类型为单域、两域或者四域"""
        ecu.domain.single_bgm=True
        ecu.domain.two_domain=None
        ecu.tc_config['dut_ecu']=["BGM"]
        return ecu

    def before_class(self, ecu):
        self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x4})
        self.bus_comm.set_Hv_sys_relay_sts(HvSysRelaySts.Close)
        self.io.tcam_power_off()
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.send_request_and_recv_response([0x22, 0x0F1, 0X53])

    def before_each_func(self, ecu):
        self.bus_comm.resume_all_bus_send()
        self.io.tcam_power_off()
        self.io.hazard_light_close()
        self.io.io.charge_lid_close()
        self.io.io.brake_up()
        self.io.io.hood_door2_open()
        self.io.io.drvr_door_outswitch_unpressed()
        self.io.io.drvr_door_close()
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.mix.set_car_mode(CarMode.NORMAL)

    def after_each_func(self, ecu):
        self.io.bgm_diag_line_up()
        self.io.tcam_kl15_up()
        self.io.tcam_power_off()
        self.bus_comm.resume_all_bus_send()
        self.io.tcam_power_on()
        logger.info("tcam 上电 延时3min ")
        sleep(3 * 60)

    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
        self.io.tcam_power_on()

    def check_keyinfo(self, log_data, key_word, **kwargs):

        if log_data.find(key_word) != -1:
            string = f"查询到关键信息：{key_word}"
            with allure.step(string):
                logger.info(string)
        else:
            string = f"未能查询到关键信息：{key_word}"
            with allure.step(string):
                logger.error(string)
            assert False, string

    @allure.title(f"BODYEXPCAN 应用报文 ：wakeup reason: 0")
    @pytest.mark.sanity
    def test_pm_on_caseid_1919216(self):
        self.sleep_and_wakeup_func(Wakeup_Reasons.WAKEUP_BY_BODYEXPCANCANFD, mn_msg=False, wakeup_reason_value=0)

    @allure.title(f"INFOCAN 应用报文 ：wakeup reason: 0")
    @pytest.mark.sanity
    def test_pm_on_caseid_1919217(self):
        self.sleep_and_wakeup_func(Wakeup_Reasons.WAKEUP_BY_INFOCAN, mn_msg=False, wakeup_reason_value=0)

    @allure.title(f"adcan 应用报文 ：wakeup reason: 0")
    @pytest.mark.sanity
    def test_pm_on_caseid_1919218(self):
        self.sleep_and_wakeup_func(Wakeup_Reasons.WAKEUP_BY_ADCAN, mn_msg=False, wakeup_reason_value=0)

    @allure.title(f"bodyCAN 应用报文 ：wakeup reason: 0")
    @pytest.mark.sanity
    def test_pm_on_caseid_111352(self):
        self.sleep_and_wakeup_func(Wakeup_Reasons.WAKEUP_BY_BODYCAN, mn_msg=False, wakeup_reason_value=0)

    @allure.title(f"ConnectivityCANFD 应用报文 ：wakeup reason: 0")
    @pytest.mark.sanity
    def test_pm_on_caseid_111270(self):
        self.sleep_and_wakeup_func(Wakeup_Reasons.WAKEUP_BY_CONNCANFD, mn_msg=False, wakeup_reason_value=0)

    @allure.title(f"PropulsionCan 应用报文 ：wakeup reason: 0")
    @pytest.mark.sanity
    def test_pm_on_caseid_111222(self):
        self.sleep_and_wakeup_func(Wakeup_Reasons.WAKEUP_BY_PROPULSIONCAN, mn_msg=False, wakeup_reason_value=0)


    def sleep_and_wakeup_func(self, wakeup_reason: Wakeup_Reasons, **kwargs):
        '''
        休眠唤醒 并校验 唤醒源
        @param wakeup_reason:
        @return:
        '''
        wakeup_reason_value = kwargs.get("wakeup_reason_value", None)
        self.mix.network_sleep()
        logger.info("休眠结束，开始唤醒")
        self.mix.network_wakeup(wakeup_reason=wakeup_reason, **kwargs)
        sleep_log_last, awakeup_log_last = self.ssh.read_bgm_jetlog()
        if wakeup_reason_value is None:
            key_info = f"wakeup reason: {wakeup_reason.value}"
        else:
            key_info = f"wakeup reason: {wakeup_reason_value}"
        self.check_keyinfo(awakeup_log_last, key_info)

