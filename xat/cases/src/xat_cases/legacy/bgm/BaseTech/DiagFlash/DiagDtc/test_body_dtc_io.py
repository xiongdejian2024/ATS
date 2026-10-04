"""
@File        : test_body_dtc.py
@Author      : xiaoqiang.hu@jiduauto.com
@Time        : 2024/08/29 15:12
@Description : 车身类DTC测试用例

"""

import pytest
import allure
from xat_cases.legacy.bgm.mcu.case_helper.test_abc_base import TestABCBase 
from xat_ecu.api.common.common import *
from xat_ecu.legacy.sdk.driver.jidutest_io.itech_io.itech_io import ItechIo

@allure.feature("BGM BaseTech/诊断刷写/诊断DTC")
@allure.story("车身DTC")
class Test_Body_DTC(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.bus_comm.set('backbonefr','BcmVddmBackBoneFr00','VehMtnStVehMtnSt','VehMtnSt2_StandStillVal3')#切UsageMode的前置条件
        self.io.start_io()
        self.itech_obj = ItechIo("/dev/USB_DO_4") 
        self.itech_obj.voltage_status_on()
        # self.itech_obj.set_volt(ch=1, value=15)
        # self.itech_obj.voltage_status_on()
        # self.itech_obj.voltage_status_off()

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.itech_obj.voltage_status_off()
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_EXT_Supply_1开路_A01613_P2")
    def test_caseid_1993939(self):
        DTC_ID = [0xA0, 0x16, 0x13]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002,0x190201,'59027f',diagnostic_action="读取当前的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190208,'59027f',diagnostic_action="读取历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190209,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022f,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022e,'59027f',diagnostic_action="读取历史的故障")
        with allure.step('设置快照信息'):
            self.sd_tester.send_data_and_check(0x1002,0x22DD0C,'62dd0c0f',diagnostic_action="供电等级")#由于429e只能是00，所以供电等级只能是0F
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000c','62dd0100000c',check_method=Check_Method.read,recover=False)
            Battery_Voltage=self.sd_tester.send_data_and_check(0x1002,0x22DD02,'62dd02',diagnostic_action="电池电压")[6:]
        with allure.step('制造当前故障;读取当前故障快照'):
            with allure.step(f"设置J1-12 KL30_1悬空持续超过21.5s"):
                logger.info(f"设置J1-12 KL30_1悬空持续超过21.5s")
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch10_switch",value=1)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch11_switch",value=0)
                time.sleep(1)
            time.sleep(25)#21.5s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-3]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
                # assert bit_0 == 1 and bit_3 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            # assert data_1[12:16] == '2005' and data_1[16:25] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置J1-12 KL30_1恢复正常持续11s"):
                logger.info(f"设置J1-12 KL30_1恢复正常持续11s")
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch10_switch",value=0)
                time.sleep(1)
            time.sleep(15)#11s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
                # assert bit_0 == 0 and bit_3 == 1, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            # assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
            # self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a01',diagnostic_action="usagemode状态读取")
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_EXT_Supply_1通用电气故障,电路电压高于阈值_A01617_P2")
    def test_caseid_1993938(self):
        DTC_ID = [0xA0, 0x16, 0x17]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002,0x190201,'59027f',diagnostic_action="读取当前的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190208,'59027f',diagnostic_action="读取历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190209,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022f,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022e,'59027f',diagnostic_action="读取历史的故障")
        with allure.step('设置快照信息'):
            self.sd_tester.send_data_and_check(0x1002,0x22DD0C,'62dd0c0f',diagnostic_action="供电等级")#由于429e只能是00，所以供电等级只能是0F
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000c','62dd0100000c',check_method=Check_Method.read,recover=False)
            Battery_Voltage=self.sd_tester.send_data_and_check(0x1002,0x22DD02,'62dd02',diagnostic_action="电池电压")[6:]
        with allure.step('制造当前故障;读取当前故障快照'):
            with allure.step(f"设置J1-12 KL30_1供电电压>=17v(=17.3v)持续超过21.5s"):
                logger.info(f"设置J1-12 KL30_1供电电压>=17v(=17.3v)持续超过21.5s")
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch10_switch",value=1)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch11_switch",value=1)
                time.sleep(1)
                self.itech_obj.set_volt(ch=1, value=18)
                time.sleep(1)
                vol = self.itech_obj.get_volt(ch=1)
                time.sleep(1)
                logger.info(f"当前电压是：{vol}")
            time.sleep(27)#21.5s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-3]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #     assert bit_0 == 1 and bit_3 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            # assert data_1[12:16] == '2005' and data_1[16:25] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置J1-12 KL30_1供电电压<=16v(=15.7v)持续11s"):
                logger.info(f"设置J1-12 KL30_1供电电压<=16v(=15.7v)持续11s")
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch10_switch",value=0)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch11_switch",value=0)
                time.sleep(1)
                self.itech_obj.set_volt(ch=1, value=0) 
                time.sleep(1) 
            time.sleep(15)#11s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #     assert bit_0 == 0 and bit_3 == 1, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            # assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
            # self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a01',diagnostic_action="usagemode状态读取")
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_EXT_Supply_1通用电气故障,电路电压低于阈值_A01616_P2")
    def test_caseid_1993940(self):
        DTC_ID = [0xA0, 0x16, 0x16]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002,0x190201,'59027f',diagnostic_action="读取当前的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190208,'59027f',diagnostic_action="读取历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190209,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022f,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022e,'59027f',diagnostic_action="读取历史的故障")
        with allure.step('设置快照信息'):
            self.sd_tester.send_data_and_check(0x1002,0x22DD0C,'62dd0c0f',diagnostic_action="供电等级")#由于429e只能是00，所以供电等级只能是0F
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000c','62dd0100000c',check_method=Check_Method.read,recover=False)
            Battery_Voltage=self.sd_tester.send_data_and_check(0x1002,0x22DD02,'62dd02',diagnostic_action="电池电压")[6:]
        with allure.step('制造当前故障;读取当前故障快照'):
            with allure.step(f"设置J1-12 KL30_1供电电压<=7v(=6.7V)持续超过21.5s"):
                logger.info(f"设置J1-12 KL30_1供电电压<=7v(=6.7V)持续超过21.5s")
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch10_switch",value=1)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch11_switch",value=1)
                time.sleep(1)
                self.itech_obj.set_volt(ch=1, value=6)
                time.sleep(1)    
            time.sleep(25)#21.5s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-3]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #     assert bit_0 == 1 and bit_3 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            # assert data_1[12:16] == '2005' and data_1[16:25] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置J1-12 KL30_1供电电压>8v(=8.3V)持续11s"):
                logger.info(f"设置J1-12 KL30_1供电电压>8v(=8.3V)持续11s")
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch10_switch",value=0)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch11_switch",value=0)
                time.sleep(1)
                self.itech_obj.set_volt(ch=1, value=0) 
                time.sleep(1)   
            time.sleep(15)#11s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #     assert bit_0 == 0 and bit_3 == 1, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            # assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
            # self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a01',diagnostic_action="usagemode状态读取")
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_EXT_Supply_2开路_A01713_P2")
    def test_caseid_1993937(self):
        DTC_ID = [0xA0, 0x17, 0x13]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002,0x190201,'59027f',diagnostic_action="读取当前的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190208,'59027f',diagnostic_action="读取历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190209,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022f,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022e,'59027f',diagnostic_action="读取历史的故障")
        with allure.step('设置快照信息'):
            self.sd_tester.send_data_and_check(0x1002,0x22DD0C,'62dd0c0f',diagnostic_action="供电等级")#由于429e只能是00，所以供电等级只能是0F
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000c','62dd0100000c',check_method=Check_Method.read,recover=False)
            Battery_Voltage=self.sd_tester.send_data_and_check(0x1002,0x22DD02,'62dd02',diagnostic_action="电池电压")[6:]
        with allure.step('制造当前故障;读取当前故障快照'):
            with allure.step(f"设置J1-11 KL30_2悬空持续超过21.5s"):
                logger.info(f"设置J1-11 KL30_2悬空持续超过21.5s")
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch8_switch",value=1)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch9_switch",value=0)
                time.sleep(1)   
            time.sleep(25)#21.5s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-3]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #     assert bit_0 == 1 and bit_3 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            # assert data_1[12:16] == '2005' and data_1[16:25] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置J1-11 KL30_2恢复正常持续11s"):
                logger.info(f"设置J1-11 KL30_2恢复正常持续11s")
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch8_switch",value=0)
                time.sleep(1)
            time.sleep(15)#11s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #     assert bit_0 == 0 and bit_3 == 1, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            # assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
            # self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a01',diagnostic_action="usagemode状态读取")
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_EXT_Supply_2通用电气故障,电路电压低于阈值_A01716_P2")
    def test_caseid_1993935(self):
        DTC_ID = [0xA0, 0x17, 0x16]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002,0x190201,'59027f',diagnostic_action="读取当前的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190208,'59027f',diagnostic_action="读取历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190209,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022f,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022e,'59027f',diagnostic_action="读取历史的故障")
        with allure.step('设置快照信息'):
            self.sd_tester.send_data_and_check(0x1002,0x22DD0C,'62dd0c0f',diagnostic_action="供电等级")#由于429e只能是00，所以供电等级只能是0F
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000c','62dd0100000c',check_method=Check_Method.read,recover=False)
            Battery_Voltage=self.sd_tester.send_data_and_check(0x1002,0x22DD02,'62dd02',diagnostic_action="电池电压")[6:]
        with allure.step('制造当前故障;读取当前故障快照'):
            with allure.step(f"设置J1-11 KL30_2供电电压<=7v(=6.7v)持续超过21.5s"):
                logger.info(f"设置J1-11 KL30_2供电电压<=7v(=6.7v)持续超过21.5s")
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch8_switch",value=1)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch9_switch",value=1)
                time.sleep(1)
                self.itech_obj.set_volt(ch=1, value=6)
                time.sleep(1)
            time.sleep(25)#21.5s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-3]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #     assert bit_0 == 1 and bit_3 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            # assert data_1[12:16] == '2005' and data_1[16:25] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置J1-11 KL30_2供电电压>8v(=8.3v)持续11s"):
                logger.info(f"设置J1-11 KL30_2供电电压>8v(=8.3v)持续11s")
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch8_switch",value=0)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch9_switch",value=0)
                time.sleep(1)
                self.itech_obj.set_volt(ch=1, value=0)
                time.sleep(1)
            time.sleep(15)#11s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #     assert bit_0 == 0 and bit_3 == 1, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            # assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
            # self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a01',diagnostic_action="usagemode状态读取")
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_EXT_Supply_2通用电气故障,电路电压高于阈值_A01717_P2")
    def test_caseid_1993936(self):
        DTC_ID = [0xA0, 0x17, 0x17]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002,0x190201,'59027f',diagnostic_action="读取当前的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190208,'59027f',diagnostic_action="读取历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190209,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022f,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022e,'59027f',diagnostic_action="读取历史的故障")
        with allure.step('设置快照信息'):
            self.sd_tester.send_data_and_check(0x1002,0x22DD0C,'62dd0c0f',diagnostic_action="供电等级")#由于429e只能是00，所以供电等级只能是0F
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000c','62dd0100000c',check_method=Check_Method.read,recover=False)
            Battery_Voltage=self.sd_tester.send_data_and_check(0x1002,0x22DD02,'62dd02',diagnostic_action="电池电压")[6:]
        with allure.step('制造当前故障;读取当前故障快照'):
            with allure.step(f"设置J1-11 KL30_2供电电压>=17v(=17.3v)持续超过21.5s"):
                logger.info(f"设置J1-11 KL30_2供电电压>=17v(=17.3v)持续超过21.5s")
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch8_switch",value=1)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch9_switch",value=1)
                time.sleep(1)
                self.itech_obj.set_volt(ch=1, value=18)
                time.sleep(1)      
            time.sleep(200)#21.5s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-3]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
                assert bit_0 == 1 and bit_3 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            assert data_1[12:16] == '2005' and data_1[16:25] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置J1-11 KL30_2供电电压<=16v(=15.7v)持续11s"):
                logger.info(f"设置J1-11 KL30_2供电电压<=16v(=15.7v)持续11s")
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch8_switch",value=0)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch9_switch",value=0)
                time.sleep(1)
                self.itech_obj.set_volt(ch=1, value=0)
                time.sleep(1)
            time.sleep(15)#11s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #     assert bit_0 == 0 and bit_3 == 1, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            # assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
            # self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a01',diagnostic_action="usagemode状态读取")
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_Internal_Supply_2开路_A01913_P2")
    def test_caseid_1993932(self):
        DTC_ID = [0xA0, 0x19, 0x13]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002,0x190201,'59027f',diagnostic_action="读取当前的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190208,'59027f',diagnostic_action="读取历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190209,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022f,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022e,'59027f',diagnostic_action="读取历史的故障")
        with allure.step('设置快照信息'):
            self.sd_tester.send_data_and_check(0x1002,0x22DD0C,'62dd0c0f',diagnostic_action="供电等级")#由于429e只能是00，所以供电等级只能是0F
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000c','62dd0100000c',check_method=Check_Method.read,recover=False)
            Battery_Voltage=self.sd_tester.send_data_and_check(0x1002,0x22DD02,'62dd02',diagnostic_action="电池电压")[6:]
        with allure.step('制造当前故障;读取当前故障快照'):
            with allure.step(f"设置J1-14 KL30_4悬空持续超过21.5s"):
                logger.info(f"设置J1-14 KL30_4悬空持续超过21.5s")
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch12_switch",value=1)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch13_switch",value=0)
                time.sleep(1)  
            time.sleep(25)#21.5s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-3]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #     assert bit_0 == 1 and bit_3 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            # assert data_1[12:16] == '2005' and data_1[16:25] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置J1-14 KL30_4恢复正常持续11s"):
                logger.info(f"设置J1-14 KL30_4恢复正常持续11s")
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch12_switch",value=0)
                time.sleep(1)
            time.sleep(15)#11s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #     assert bit_0 == 0 and bit_3 == 1, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            # assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
            # self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a01',diagnostic_action="usagemode状态读取")
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_Internal_Supply_2电路电压低于阈值_A01916_P2")
    def test_caseid_1993933(self):
        DTC_ID = [0xA0, 0x19, 0x16]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002,0x190201,'59027f',diagnostic_action="读取当前的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190208,'59027f',diagnostic_action="读取历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190209,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022f,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022e,'59027f',diagnostic_action="读取历史的故障")
        with allure.step('设置快照信息'):
            self.sd_tester.send_data_and_check(0x1002,0x22DD0C,'62dd0c0f',diagnostic_action="供电等级")#由于429e只能是00，所以供电等级只能是0F
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000c','62dd0100000c',check_method=Check_Method.read,recover=False)
            Battery_Voltage=self.sd_tester.send_data_and_check(0x1002,0x22DD02,'62dd02',diagnostic_action="电池电压")[6:]
        with allure.step('制造当前故障;读取当前故障快照'):
            with allure.step(f"设置J1-14 KL30_4供电电压<=7v(=6.7v)持续超过21.5s"):
                logger.info(f"设置J1-14 KL30_4供电电压<=7v(=6.7v)持续超过21.5s")
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch12_switch",value=1)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch13_switch",value=1)
                time.sleep(1)
                self.itech_obj.set_volt(ch=2, value=6)
                time.sleep(1)
            time.sleep(25)#21.5s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-3]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #     assert bit_0 == 1 and bit_3 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            # assert data_1[12:16] == '2005' and data_1[16:25] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置J1-14 KL30_4供电电压>8v(=8.3v)持续11s"):
                logger.info(f"设置J1-14 KL30_4供电电压>8v(=8.3v)持续11s")
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch12_switch",value=0)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch13_switch",value=0)
                time.sleep(1)
                self.itech_obj.set_volt(ch=2, value=0)
                time.sleep(1)
            time.sleep(15)#11s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #     assert bit_0 == 0 and bit_3 == 1, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            # assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
            # self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a01',diagnostic_action="usagemode状态读取")
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_Internal_Supply_2电路电压高于阈值_A01917_P2")
    def test_caseid_1993934(self):
        DTC_ID = [0xA0, 0x19, 0x17]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002,0x190201,'59027f',diagnostic_action="读取当前的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190208,'59027f',diagnostic_action="读取历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190209,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022f,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022e,'59027f',diagnostic_action="读取历史的故障")
        with allure.step('设置快照信息'):
            self.sd_tester.send_data_and_check(0x1002,0x22DD0C,'62dd0c0f',diagnostic_action="供电等级")#由于429e只能是00，所以供电等级只能是0F
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000c','62dd0100000c',check_method=Check_Method.read,recover=False)
            Battery_Voltage=self.sd_tester.send_data_and_check(0x1002,0x22DD02,'62dd02',diagnostic_action="电池电压")[6:]
        with allure.step('制造当前故障;读取当前故障快照'):
            with allure.step(f"设置J1-14 KL30_4供电电压>=17v(=17.3v)持续超过21.5s"):
                logger.info(f"设置J1-14 KL30_4供电电压>=17v(=17.3v)持续超过21.5s")
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch12_switch",value=1)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch13_switch",value=1)
                time.sleep(1)
                self.itech_obj.set_volt(ch=2, value=18)
                time.sleep(1)
            time.sleep(25)#21.5s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-3]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #     assert bit_0 == 1 and bit_3 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            # assert data_1[12:16] == '2005' and data_1[16:25] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置J1-14 KL30_4供电电压<=16v(=15.7)持续11s"):
                logger.info(f"设置J1-14 KL30_4供电电压<=16v(=15.7)持续11s")
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch12_switch",value=0)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch13_switch",value=0)
                time.sleep(1)
                self.itech_obj.set_volt(ch=2, value=0)
                time.sleep(1)
            time.sleep(15)#11s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #     assert bit_0 == 0 and bit_3 == 1, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            # assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
            # self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a01',diagnostic_action="usagemode状态读取")
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_Internal_Supply_3开路_A01A13_P2")
    def test_caseid_1993929(self):
        DTC_ID = [0xA0, 0x1A, 0x13]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002,0x190201,'59027f',diagnostic_action="读取当前的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190208,'59027f',diagnostic_action="读取历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190209,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022f,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022e,'59027f',diagnostic_action="读取历史的故障")
        with allure.step('设置快照信息'):
            self.sd_tester.send_data_and_check(0x1002,0x22DD0C,'62dd0c0f',diagnostic_action="供电等级")#由于429e只能是00，所以供电等级只能是0F
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000c','62dd0100000c',check_method=Check_Method.read,recover=False)
            Battery_Voltage=self.sd_tester.send_data_and_check(0x1002,0x22DD02,'62dd02',diagnostic_action="电池电压")[6:]
        with allure.step('制造当前故障;读取当前故障快照'):
            with allure.step(f"设置J1-28 KL30_7悬空持续超过21.5s"):
                logger.info(f"设置J1-28 KL30_7悬空持续超过21.5s")
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch18_switch",value=1)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch19_switch",value=0)
                time.sleep(1)
            time.sleep(25)#21.5s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-3]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #     assert bit_0 == 1 and bit_3 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            # assert data_1[12:16] == '2005' and data_1[16:25] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置J1-28 KL30_7恢复正常持续11s"):
                logger.info(f"设置J1-28 KL30_7恢复正常持续11s")
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch18_switch",value=0)
                time.sleep(1)
            time.sleep(15)#11s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #     assert bit_0 == 0 and bit_3 == 1, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            # assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
            # self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a01',diagnostic_action="usagemode状态读取")
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_Internal_Supply_3电路电压低于阈值_A01A16_P2")
    def test_caseid_1993930(self):
        DTC_ID = [0xA0, 0x1A, 0x16]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002,0x190201,'59027f',diagnostic_action="读取当前的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190208,'59027f',diagnostic_action="读取历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190209,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022f,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022e,'59027f',diagnostic_action="读取历史的故障")
        with allure.step('设置快照信息'):
            self.sd_tester.send_data_and_check(0x1002,0x22DD0C,'62dd0c0f',diagnostic_action="供电等级")#由于429e只能是00，所以供电等级只能是0F
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000c','62dd0100000c',check_method=Check_Method.read,recover=False)
            Battery_Voltage=self.sd_tester.send_data_and_check(0x1002,0x22DD02,'62dd02',diagnostic_action="电池电压")[6:]
        with allure.step('制造当前故障;读取当前故障快照'):
            with allure.step(f"设置J1-28 KL30_7供电电压<=7v(=6.7v)持续超过21.5s"):
                logger.info(f"设置J1-28 KL30_7供电电压<=7v(=6.7v)持续超过21.5s")
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch18_switch",value=1)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch19_switch",value=1)
                time.sleep(1)
                self.itech_obj.set_volt(ch=2, value=6)
                time.sleep(1)
            time.sleep(25)#21.5s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-3]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #     assert bit_0 == 1 and bit_3 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            # assert data_1[12:16] == '2005' and data_1[16:25] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置J1-28 KL30_7供电电压>8v(=8.3v)持续11s"):
                logger.info(f"设置J1-28 KL30_7供电电压>8v(=8.3v)持续11s")
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch18_switch",value=0)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch19_switch",value=0)
                time.sleep(1)
                self.itech_obj.set_volt(ch=2, value=0)
                time.sleep(1)
            time.sleep(15)#11s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #     assert bit_0 == 0 and bit_3 == 1, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            # assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
            # self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a01',diagnostic_action="usagemode状态读取")
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_Internal_Supply_3电路电压高于阈值_A01A17_P2")
    def test_caseid_1993931(self):
        DTC_ID = [0xA0, 0x1A, 0x17]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002,0x190201,'59027f',diagnostic_action="读取当前的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190208,'59027f',diagnostic_action="读取历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190209,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022f,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022e,'59027f',diagnostic_action="读取历史的故障")
        with allure.step('设置快照信息'):
            self.sd_tester.send_data_and_check(0x1002,0x22DD0C,'62dd0c0f',diagnostic_action="供电等级")#由于429e只能是00，所以供电等级只能是0F
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000c','62dd0100000c',check_method=Check_Method.read,recover=False)
            Battery_Voltage=self.sd_tester.send_data_and_check(0x1002,0x22DD02,'62dd02',diagnostic_action="电池电压")[6:]
        with allure.step('制造当前故障;读取当前故障快照'):
            with allure.step(f"设置J1-28 KL30_7供电电压>=17v(=17.3v)持续超过21.5s"):
                logger.info(f"设置J1-28 KL30_7供电电压>=17v(=17.3v)持续超过21.5s")
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch18_switch",value=1)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch19_switch",value=1)
                time.sleep(1)
                self.itech_obj.set_volt(ch=2, value=18)
                time.sleep(1)
            time.sleep(25)#21.5s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-3]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #     assert bit_0 == 1 and bit_3 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            # assert data_1[12:16] == '2005' and data_1[16:25] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置J1-28 KL30_7供电电压<=16v(=15.7v)持续11s"):
                logger.info(f"设置J1-28 KL30_7供电电压<=16v(=15.7v)持续11s")
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch18_switch",value=0)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch19_switch",value=0)
                time.sleep(1)
                self.itech_obj.set_volt(ch=2, value=0)
                time.sleep(1)  
            time.sleep(15)#11s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #     assert bit_0 == 0 and bit_3 == 1, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            # assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
            # self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a01',diagnostic_action="usagemode状态读取")
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_清洗供应开路_A02E13_P2")
    def test_caseid_1993951(self):
        DTC_ID = [0xA0, 0x2E, 0x13]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002,0x190201,'59027f',diagnostic_action="读取当前的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190208,'59027f',diagnostic_action="读取历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190209,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022f,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022e,'59027f',diagnostic_action="读取历史的故障")
        with allure.step('设置快照信息'):
            self.sd_tester.send_data_and_check(0x1002,0x22DD0C,'62dd0c0f',diagnostic_action="供电等级")#由于429e只能是00，所以供电等级只能是0F
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000c','62dd0100000c',check_method=Check_Method.read,recover=False)
            Battery_Voltage=self.sd_tester.send_data_and_check(0x1002,0x22DD02,'62dd02',diagnostic_action="电池电压")[6:]
        with allure.step('制造当前故障;读取当前故障快照'):
            with allure.step(f"设置J1-26 KL30_6悬空制造电路开路持续21.5s"):
                logger.info(f"设置J1-26 KL30_6悬空制造电路开路持续21.5s")
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch16_switch",value=1)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch17_switch",value=0)
                time.sleep(1)
            time.sleep(25)#21.5s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-3]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #     assert bit_0 == 1 and bit_3 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            # assert data_1[12:16] == '2005' and data_1[16:25] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置J1-26 KL30_6闭合持续11s"):
                logger.info(f"设置J1-26 KL30_6闭合持续11s")
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch16_switch",value=0)
                time.sleep(1)   
            time.sleep(15)#11s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #     assert bit_0 == 0 and bit_3 == 1, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            # assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
            # self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a01',diagnostic_action="usagemode状态读取")
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_清洗供应电路电压低于阈值_A02E16_P2")
    def test_caseid_1993952(self):
        DTC_ID = [0xA0, 0x2E, 0x16]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002,0x190201,'59027f',diagnostic_action="读取当前的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190208,'59027f',diagnostic_action="读取历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190209,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022f,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022e,'59027f',diagnostic_action="读取历史的故障")
        with allure.step('设置快照信息'):
            self.sd_tester.send_data_and_check(0x1002,0x22DD0C,'62dd0c0f',diagnostic_action="供电等级")#由于429e只能是00，所以供电等级只能是0F
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000c','62dd0100000c',check_method=Check_Method.read,recover=False)
            Battery_Voltage=self.sd_tester.send_data_and_check(0x1002,0x22DD02,'62dd02',diagnostic_action="电池电压")[6:]
        with allure.step('制造当前故障;读取当前故障快照'):
            with allure.step(f"设置J1-26 Washing Supply voltage <= 7V (=6.7V)持续21.5s"):
                logger.info(f"设置J1-26 Washing Supply voltage <= 7V (=6.7V)持续21.5s")
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch16_switch",value=1)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch17_switch",value=1)
                time.sleep(1)
                self.itech_obj.set_volt(ch=2, value=6)
                time.sleep(1)
            time.sleep(25)#21.5s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-3]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #     assert bit_0 == 1 and bit_3 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            # assert data_1[12:16] == '2005' and data_1[16:25] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置J1-26 Washing Supply voltage > 8V(=8.3V)持续11s"):
                logger.info(f"设置J1-26 Washing Supply voltage > 8V(=8.3V)持续11s")
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch16_switch",value=0)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch17_switch",value=0)
                time.sleep(1)
                self.itech_obj.set_volt(ch=2, value=6)
                time.sleep(1)
            time.sleep(15)#11s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #     assert bit_0 == 0 and bit_3 == 1, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            # assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
            # self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a01',diagnostic_action="usagemode状态读取")
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_清洗供应电路电压高于阈值_A02E17_P2")
    def test_caseid_1993953(self):
        DTC_ID = [0xA0, 0x2E, 0x17]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002,0x190201,'59027f',diagnostic_action="读取当前的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190208,'59027f',diagnostic_action="读取历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190209,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022f,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022e,'59027f',diagnostic_action="读取历史的故障")
        with allure.step('设置快照信息'):
            self.sd_tester.send_data_and_check(0x1002,0x22DD0C,'62dd0c0f',diagnostic_action="供电等级")#由于429e只能是00，所以供电等级只能是0F
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000c','62dd0100000c',check_method=Check_Method.read,recover=False)
            Battery_Voltage=self.sd_tester.send_data_and_check(0x1002,0x22DD02,'62dd02',diagnostic_action="电池电压")[6:]
        with allure.step('制造当前故障;读取当前故障快照'):
            with allure.step(f"设置Washing Supply voltage >= 17V(=17.3V)持续21.5s"):
                logger.info(f"设置Washing Supply voltage >= 17V(=17.3V)持续21.5s")
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch16_switch",value=1)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch17_switch",value=1)
                time.sleep(1)
                self.itech_obj.set_volt(ch=2, value=18)
                time.sleep(1)  
            time.sleep(25)#21.5s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-3]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #     assert bit_0 == 1 and bit_3 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            # assert data_1[12:16] == '2005' and data_1[16:25] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置Washing Supply voltage < 16V(=15.7V)持续11s"):
                logger.info(f"设置Washing Supply voltage < 16V(=15.7V)持续11s")
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch16_switch",value=0)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay1_ch17_switch",value=0)
                time.sleep(1)
                self.itech_obj.set_volt(ch=2, value=0)
                time.sleep(1)      
            time.sleep(15)#11s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #     assert bit_0 == 0 and bit_3 == 1, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            # assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
            # self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a01',diagnostic_action="usagemode状态读取")
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_右前门外面电动门打开/关闭按钮-机械故障致动器卡滞_97D671_P2")
    def test_caseid_1993996(self):
        DTC_ID = [0x97, 0xD6, 0x71]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:481:0x04'):
                    logger.info(f"设置ccp：481:0x04")
                    self.sd_tester.write_ccp({481:0x04})
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002,0x190201,'59027f',diagnostic_action="读取当前的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190208,'59027f',diagnostic_action="读取历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190209,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022f,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022e,'59027f',diagnostic_action="读取历史的故障")
        with allure.step('设置快照信息'):
            self.sd_tester.send_data_and_check(0x1002,0x22DD0C,'62dd0c0f',diagnostic_action="供电等级")#由于429e只能是00，所以供电等级只能是0F
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000c','62dd0100000c',check_method=Check_Method.read,recover=False)
            Battery_Voltage=self.sd_tester.send_data_and_check(0x1002,0x22DD02,'62dd02',diagnostic_action="电池电压")[6:]
        with allure.step('制造当前故障;读取当前故障快照'):
            with allure.step(f"制造电路故障J3-40 DoorHandFrontRightSwitch active持续超过20s"):
                logger.info(f"制造电路故障J3-40 DoorHandFrontRightSwitch active持续超过20s")
                
            time.sleep(25)#20s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-3]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1 and bit_3 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            assert data_1[12:16] == '2005' and data_1[16:25] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"恢复电路故障J3-40 DoorHandFrontRightSwitch deactive持续超过20s"):
                logger.info(f"恢复电路故障J3-40 DoorHandFrontRightSwitch deactive持续超过20s")
                
            time.sleep(25)#20s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0 and bit_3 == 1, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
            # self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a01',diagnostic_action="usagemode状态读取")
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_ECM唤醒-通用电气故障电路-对电源短路_A00912_P2")
    def test_caseid_1993945(self):
        DTC_ID = [0xA0, 0x09, 0x12]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ECM Wake Up switched OFF(1002 2F 42 53 03 00)'):
                    logger.info(f"设置ECM Wake Up switched OFF(1002 2F 42 53 03 00)")
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x53, 0x03,0x00])
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002,0x190201,'59027f',diagnostic_action="读取当前的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190208,'59027f',diagnostic_action="读取历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190209,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022f,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022e,'59027f',diagnostic_action="读取历史的故障")
        with allure.step('设置快照信息'):
            self.sd_tester.send_data_and_check(0x1002,0x22DD0C,'62dd0c0f',diagnostic_action="供电等级")#由于429e只能是00，所以供电等级只能是0F
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000c','62dd0100000c',check_method=Check_Method.read,recover=False)
            Battery_Voltage=self.sd_tester.send_data_and_check(0x1002,0x22DD02,'62dd02',diagnostic_action="电池电压")[6:]
        with allure.step('制造当前故障;读取当前故障快照'):
            with allure.step(f"设置J2-30 ECM_WakeupSupply引脚对电源短路持续3.2s"):
                logger.info(f"设置J2-30 ECM_WakeupSupply引脚对电源短路持续3.2s")
                self.io.dtc_relay_ch_switch(name="dtc_relay2_ch25_switch",value=1)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay2_ch26_switch",value=1)
                time.sleep(1)
            time.sleep(5)#3.2s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-3]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #     assert bit_0 == 1 and bit_3 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            # assert data_1[12:16] == '2005' and data_1[16:25] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置J2-30 ECM_WakeupSupply引脚恢复正常持续3.2s"):
                logger.info(f"设置J2-30 ECM_WakeupSupply引脚恢复正常持续3.2s")
                self.io.dtc_relay_ch_switch(name="dtc_relay2_ch26_switch",value=0)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay2_ch25_switch",value=0)
                time.sleep(1)
            time.sleep(5)#3.2s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #     assert bit_0 == 0 and bit_3 == 1, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            # assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
            # self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a01',diagnostic_action="usagemode状态读取")
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_ECM唤醒-通用电气故障电路-对地短路_A00911_P2")
    def test_caseid_1993946(self):
        DTC_ID = [0xA0, 0x09, 0x11]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ECM Wake Up switched ON(1002 2F 42 53 03 01)'):
                    logger.info(f"设置ECM Wake Up switched ON(1002 2F 42 53 03 01)")
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x53, 0x03,0x01])
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002,0x190201,'59027f',diagnostic_action="读取当前的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190208,'59027f',diagnostic_action="读取历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190209,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022f,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022e,'59027f',diagnostic_action="读取历史的故障")
        with allure.step('设置快照信息'):
            self.sd_tester.send_data_and_check(0x1002,0x22DD0C,'62dd0c0f',diagnostic_action="供电等级")#由于429e只能是00，所以供电等级只能是0F
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000c','62dd0100000c',check_method=Check_Method.read,recover=False)
            Battery_Voltage=self.sd_tester.send_data_and_check(0x1002,0x22DD02,'62dd02',diagnostic_action="电池电压")[6:]
        with allure.step('制造当前故障;读取当前故障快照'):
            with allure.step(f"设置J2-30 ECM_WakeupSupply引脚对地短路持续100ms"):
                logger.info(f"设置J2-30 ECM_WakeupSupply引脚对地短路持续100ms")
                self.io.dtc_relay_ch_switch(name="dtc_relay2_ch25_switch",value=1)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay2_ch26_switch",value=0)
                time.sleep(1)  
            time.sleep(1)#100ms
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-3]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #     assert bit_0 == 1 and bit_3 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            # assert data_1[12:16] == '2005' and data_1[16:25] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置J2-30 ECM_WakeupSupply引脚恢复正常持续100ms"):
                logger.info(f"设置J2-30 ECM_WakeupSupply引脚恢复正常持续100ms")
                self.io.dtc_relay_ch_switch(name="dtc_relay2_ch25_switch",value=0)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay2_ch26_switch",value=0)
                time.sleep(1)  
                self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x53, 0x03,0x00])
                time.sleep(1)
                self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x53, 0x03,0x01])
                time.sleep(1)
            time.sleep(1)#100ms
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #     assert bit_0 == 0 and bit_3 == 1, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            # assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
            # self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a01',diagnostic_action="usagemode状态读取")
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_前挡风玻璃清洗继电器控制-通用电气故障继电器控制-对电源短路_A00712_P2")
    def test_caseid_1993972(self):
        DTC_ID = [0xA0, 0x07, 0x12]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置Front Windscreen Washing switched ON(2F 41 E9 03 01控制前雨刮继电器打开)'):
                    logger.info(f"设置Front Windscreen Washing switched ON(2F 41 E9 03 01控制前雨刮继电器打开)")
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x41, 0xE9, 0x03,0x01])
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002,0x190201,'59027f',diagnostic_action="读取当前的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190208,'59027f',diagnostic_action="读取历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190209,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022f,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022e,'59027f',diagnostic_action="读取历史的故障")
        with allure.step('设置快照信息'):
            self.sd_tester.send_data_and_check(0x1002,0x22DD0C,'62dd0c0f',diagnostic_action="供电等级")#由于429e只能是00，所以供电等级只能是0F
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000c','62dd0100000c',check_method=Check_Method.read,recover=False)
            Battery_Voltage=self.sd_tester.send_data_and_check(0x1002,0x22DD02,'62dd02',diagnostic_action="电池电压")[6:]
        with allure.step('制造当前故障;读取当前故障快照'):
            with allure.step(f"设置J2-23 FrontWashRelayCtrl引脚对电源短路持续100ms"):
                logger.info(f"设置J2-23 FrontWashRelayCtrl引脚对电源短路持续100ms")
                self.io.dtc_relay_ch_switch(name="dtc_relay2_ch17_switch",value=1)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay2_ch18_switch",value=1)
                time.sleep(1) 
            time.sleep(1)#100ms
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-3]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #     assert bit_0 == 1 and bit_3 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            # assert data_1[12:16] == '2005' and data_1[16:25] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置J2-23 FrontWashRelayCtrl引脚恢复正常持续100ms,先执行2F 41 E9 03 00控制前雨刮继电器关闭，然后再执行2F 41 E9 03 01控制前雨刮继电器打开"):
                logger.info(f"设置J2-23 FrontWashRelayCtrl引脚恢复正常持续100ms,先执行2F 41 E9 03 00控制前雨刮继电器关闭，然后再执行2F 41 E9 03 01控制前雨刮继电器打开")
                self.io.dtc_relay_ch_switch(name="dtc_relay2_ch17_switch",value=0)
                time.sleep(1) 
                self.io.dtc_relay_ch_switch(name="dtc_relay2_ch18_switch",value=0)
                time.sleep(1)
                self.sd_tester.send_request_and_recv_response([0x2F, 0x41, 0xE9, 0x03,0x00])
                time.sleep(1)
                self.sd_tester.send_request_and_recv_response([0x2F, 0x41, 0xE9, 0x03,0x01])
                time.sleep(1)
            time.sleep(3)#100ms
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #     assert bit_0 == 0 and bit_3 == 1, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            # assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
            # self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a01',diagnostic_action="usagemode状态读取")
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_前挡风玻璃清洗继电器控制-通用电气故障继电器控制-开路_A00713_P2")
    def test_caseid_1993971(self):
        DTC_ID = [0xA0, 0x07, 0x13]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置Front Windscreen Washing switched OFF(2F 41 E9 03 00)灯是半灭的状态'):
                    logger.info(f"设置Front Windscreen Washing switched OFF(2F 41 E9 03 00)灯是半灭的状态")
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x41, 0xE9, 0x03,0x00])
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002,0x190201,'59027f',diagnostic_action="读取当前的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190208,'59027f',diagnostic_action="读取历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190209,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022f,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022e,'59027f',diagnostic_action="读取历史的故障")
        with allure.step('设置快照信息'):
            self.sd_tester.send_data_and_check(0x1002,0x22DD0C,'62dd0c0f',diagnostic_action="供电等级")#由于429e只能是00，所以供电等级只能是0F
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000c','62dd0100000c',check_method=Check_Method.read,recover=False)
            Battery_Voltage=self.sd_tester.send_data_and_check(0x1002,0x22DD02,'62dd02',diagnostic_action="电池电压")[6:]
        with allure.step('制造当前故障;读取当前故障快照'):
            with allure.step(f"手动拨杆控制J2-23 FrontWashRelayCtrl悬空持续3.2s"):
                logger.info(f"手动拨杆控制J2-23 FrontWashRelayCtrl悬空持续3.2s")
                self.io.dtc_relay_ch_switch(name="dtc_relay2_ch17_switch",value=1)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay2_ch18_switch",value=0)
                time.sleep(1) 
            time.sleep(5)#3.2s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-3]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #     assert bit_0 == 1 and bit_3 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            # assert data_1[12:16] == '2005' and data_1[16:25] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"手动拨杆控制J2-23 FrontWashRelayCtrl闭合持续3.2s"):
                logger.info(f"手动拨杆控制J2-23 FrontWashRelayCtrl闭合持续3.2s")
                self.io.dtc_relay_ch_switch(name="dtc_relay2_ch17_switch",value=0)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay2_ch18_switch",value=0)
                time.sleep(1) 
            time.sleep(5)#3.2s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #     assert bit_0 == 0 and bit_3 == 1, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            # assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
            # self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a01',diagnostic_action="usagemode状态读取")
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_FL门显示灯--通用电气故障电路-对电源短路-OFF状态时_A06212_P2")
    def test_caseid_1993978(self):
        DTC_ID = [0xA0, 0x62, 0x12]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:958:0x02'):
                    logger.info(f"设置ccp：958:0x02")
                    self.sd_tester.write_ccp({958:0x02})
            with allure.step(f'设置FL Door Indicate Lamp OFF(2F 41 E5 03 00 00 00 00 00 00 10)'):
                    logger.info(f"设置FL Door Indicate Lamp OFF(2F 41 E5 03 00 00 00 00 00 00 10)")
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x41, 0xE5, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10])
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002,0x190201,'59027f',diagnostic_action="读取当前的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190208,'59027f',diagnostic_action="读取历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190209,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022f,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022e,'59027f',diagnostic_action="读取历史的故障")
        with allure.step('设置快照信息'):
            self.sd_tester.send_data_and_check(0x1002,0x22DD0C,'62dd0c0f',diagnostic_action="供电等级")#由于429e只能是00，所以供电等级只能是0F
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000c','62dd0100000c',check_method=Check_Method.read,recover=False)
            Battery_Voltage=self.sd_tester.send_data_and_check(0x1002,0x22DD02,'62dd02',diagnostic_action="电池电压")[6:]
        with allure.step('制造当前故障;读取当前故障快照'):
            with allure.step(f"设置J3-1 DriverDoor_Welcom_light引脚对电源短路持续3.2s"):
                logger.info(f"设置J3-1 DriverDoor_Welcom_light引脚对电源短路持续3.2s")
                self.io.dtc_relay_ch_switch(name="dtc_relay3_ch1_switch",value=1)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay3_ch2_switch",value=1)
                time.sleep(1) 
            time.sleep(5)#3.2s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-3]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #     assert bit_0 == 1 and bit_3 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            # assert data_1[12:16] == '2005' and data_1[16:25] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置J3-1 DriverDoor_Welcom_light引脚恢复正常持续3.2s"):
                logger.info(f"设置J3-1 DriverDoor_Welcom_light引脚恢复正常持续3.2s")
                self.io.dtc_relay_ch_switch(name="dtc_relay3_ch1_switch",value=0)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay3_ch2_switch",value=0)
                time.sleep(1) 
            time.sleep(5)#3.2s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #     assert bit_0 == 0 and bit_3 == 1, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            # assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
            # self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a01',diagnostic_action="usagemode状态读取")
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_FL门显示灯-通用电气故障电路-对地短路-ON状态时_A06211_P2")
    def test_caseid_1993979(self):
        DTC_ID = [0xA0, 0x62, 0x11]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:958:0x02'):
                    logger.info(f"设置ccp：958:0x02")
                    self.sd_tester.write_ccp({958:0x02})
            with allure.step(f'设置FL Door Indicate Lamp ON(2F 41 E5 03 00 00 00 64 00 00 10)'):
                    logger.info(f"设置FL Door Indicate Lamp ON(2F 41 E5 03 00 00 00 64 00 00 10)")
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x41, 0xE5, 0x03, 0x00, 0x00, 0x00, 0x64, 0x00, 0x00, 0x10])
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002,0x190201,'59027f',diagnostic_action="读取当前的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190208,'59027f',diagnostic_action="读取历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190209,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022f,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022e,'59027f',diagnostic_action="读取历史的故障")
        with allure.step('设置快照信息'):
            self.sd_tester.send_data_and_check(0x1002,0x22DD0C,'62dd0c0f',diagnostic_action="供电等级")#由于429e只能是00，所以供电等级只能是0F
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000c','62dd0100000c',check_method=Check_Method.read,recover=False)
            Battery_Voltage=self.sd_tester.send_data_and_check(0x1002,0x22DD02,'62dd02',diagnostic_action="电池电压")[6:]
        with allure.step('制造当前故障;读取当前故障快照'):
            with allure.step(f"设置J3-1 DriverDoor_Welcom_light引脚对地短路持续100ms"):
                logger.info(f"设置J3-1 DriverDoor_Welcom_light引脚对地短路持续100ms")
                self.io.dtc_relay_ch_switch(name="dtc_relay3_ch1_switch",value=1)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay3_ch2_switch",value=0)
                time.sleep(1) 
            time.sleep(1)#100s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-3]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #     assert bit_0 == 1 and bit_3 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            # assert data_1[12:16] == '2005' and data_1[16:25] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置J3-1 DriverDoor_Welcom_light引脚恢复正常持续100ms"):
                logger.info(f"设置J3-1 DriverDoor_Welcom_light引脚恢复正常持续100ms")
                self.io.dtc_relay_ch_switch(name="dtc_relay3_ch1_switch",value=0)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay3_ch2_switch",value=0)
                time.sleep(1) 
                self.sd_tester.send_request_and_recv_response([0x2F, 0x41, 0xE5, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10])
                time.sleep(1) 
                self.sd_tester.send_request_and_recv_response([0x2F, 0x41, 0xE5, 0x03, 0x00, 0x00, 0x00, 0x64, 0x00, 0x00, 0x10])
                time.sleep(1) 
            time.sleep(1)#100ms
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #     assert bit_0 == 0 and bit_3 == 1, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            # assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
            # self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a01',diagnostic_action="usagemode状态读取")
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_FR门显示灯-通用电气故障电路-对地短路-ON状态时_A06311_P2")
    def test_caseid_1993977(self):
        DTC_ID = [0xA0, 0x63, 0x11]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:958:0x02'):
                    logger.info(f"设置ccp：958:0x02")
                    self.sd_tester.write_ccp({958:0x02})
            with allure.step(f'设置FR Door Indicate Lamp ON(2F 41 E5 03 00 00 00 00 64 00 08)'):
                    logger.info(f"设置FR Door Indicate Lamp ON(2F 41 E5 03 00 00 00 00 64 00 08)")
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x41, 0xE5, 0x03, 0x00, 0x00, 0x00, 0x00, 0x64, 0x00, 0x08])
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002,0x190201,'59027f',diagnostic_action="读取当前的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190208,'59027f',diagnostic_action="读取历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190209,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022f,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022e,'59027f',diagnostic_action="读取历史的故障")
        with allure.step('设置快照信息'):
            self.sd_tester.send_data_and_check(0x1002,0x22DD0C,'62dd0c0f',diagnostic_action="供电等级")#由于429e只能是00，所以供电等级只能是0F
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000c','62dd0100000c',check_method=Check_Method.read,recover=False)
            Battery_Voltage=self.sd_tester.send_data_and_check(0x1002,0x22DD02,'62dd02',diagnostic_action="电池电压")[6:]
        with allure.step('制造当前故障;读取当前故障快照'):
            with allure.step(f"设置J3-2 PassengerDoor_Welcom_light引脚对地短路持续100ms"):
                logger.info(f"设置J3-2 PassengerDoor_Welcom_light引脚对地短路持续100ms")
                self.io.dtc_relay_ch_switch(name="dtc_relay3_ch3_switch",value=1)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay3_ch4_switch",value=0)
                time.sleep(1) 
            time.sleep(1)#100s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-3]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #     assert bit_0 == 1 and bit_3 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            # assert data_1[12:16] == '2005' and data_1[16:25] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置J3-2 PassengerDoor_Welcom_light引脚恢复正常持续100ms"):
                logger.info(f"设置J3-2 PassengerDoor_Welcom_light引脚恢复正常持续100ms")
                self.io.dtc_relay_ch_switch(name="dtc_relay3_ch3_switch",value=0)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay3_ch4_switch",value=0)
                time.sleep(1) 
                self.sd_tester.send_request_and_recv_response([0x2F, 0x41, 0xE5, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08])
                time.sleep(1) 
                self.sd_tester.send_request_and_recv_response([0x2F, 0x41, 0xE5, 0x03, 0x00, 0x00, 0x00, 0x00, 0x64, 0x00, 0x08])
                time.sleep(1) 
            time.sleep(1)#100ms
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #     assert bit_0 == 0 and bit_3 == 1, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            # assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
            # self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a01',diagnostic_action="usagemode状态读取")
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_FR门显示灯-通用电气故障电路-对电源短路-OFF状态时_A06312_P2")
    def test_caseid_1993976(self):
        DTC_ID = [0xA0, 0x63, 0x12]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:958:0x02'):
                    logger.info(f"设置ccp：958:0x02")
                    self.sd_tester.write_ccp({958:0x02})
            with allure.step(f'设置FR Door Indicate Lamp OFF(2F 41 E5 03 00 00 00 00 00 00 08)'):
                    logger.info(f"设置FR Door Indicate Lamp OFF(2F 41 E5 03 00 00 00 00 00 00 08)")
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x41, 0xE5, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08])
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002,0x190201,'59027f',diagnostic_action="读取当前的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190208,'59027f',diagnostic_action="读取历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190209,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022f,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022e,'59027f',diagnostic_action="读取历史的故障")
        with allure.step('设置快照信息'):
            self.sd_tester.send_data_and_check(0x1002,0x22DD0C,'62dd0c0f',diagnostic_action="供电等级")#由于429e只能是00，所以供电等级只能是0F
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000c','62dd0100000c',check_method=Check_Method.read,recover=False)
            Battery_Voltage=self.sd_tester.send_data_and_check(0x1002,0x22DD02,'62dd02',diagnostic_action="电池电压")[6:]
        with allure.step('制造当前故障;读取当前故障快照'):
            with allure.step(f"设置J3-2 PassengerDoor_Welcom_light引脚对电源短路持续3.2s"):
                logger.info(f"设置J3-2 PassengerDoor_Welcom_light引脚对电源短路持续3.2s")
                self.io.dtc_relay_ch_switch(name="dtc_relay3_ch3_switch",value=1)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay3_ch4_switch",value=1)
                time.sleep(1) 
            time.sleep(5)#3.2s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-3]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #     assert bit_0 == 1 and bit_3 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            # assert data_1[12:16] == '2005' and data_1[16:25] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置J3-2 PassengerDoor_Welcom_light引脚恢复正常持续3.2s"):
                logger.info(f"设置J3-2 PassengerDoor_Welcom_light引脚恢复正常持续3.2s")
                self.io.dtc_relay_ch_switch(name="dtc_relay3_ch3_switch",value=0)
                time.sleep(1)
                self.io.dtc_relay_ch_switch(name="dtc_relay3_ch4_switch",value=0)
                time.sleep(1) 
            time.sleep(5)#3.2s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #     assert bit_0 == 0 and bit_3 == 1, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            # assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
            # self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a01',diagnostic_action="usagemode状态读取")
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_右前门外面电动门打开/关闭按钮-机械故障致动器卡滞_97D671_P2")
    def test_caseid_1993996(self):
        DTC_ID = [0x97, 0xD6, 0x71]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:481:0x04'):
                    logger.info(f"设置ccp：481:0x04")
                    self.sd_tester.write_ccp({481:0x04})
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002,0x190201,'59027f',diagnostic_action="读取当前的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190208,'59027f',diagnostic_action="读取历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190209,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022f,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022e,'59027f',diagnostic_action="读取历史的故障")
        with allure.step('设置快照信息'):
            self.sd_tester.send_data_and_check(0x1002,0x22DD0C,'62dd0c0f',diagnostic_action="供电等级")#由于429e只能是00，所以供电等级只能是0F
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000c','62dd0100000c',check_method=Check_Method.read,recover=False)
            Battery_Voltage=self.sd_tester.send_data_and_check(0x1002,0x22DD02,'62dd02',diagnostic_action="电池电压")[6:]
        with allure.step('制造当前故障;读取当前故障快照'):
            with allure.step(f"制造电路故障J3-40 DoorHandFrontRightSwitch active持续超过20s"):
                logger.info(f"制造电路故障J3-40 DoorHandFrontRightSwitch active持续超过20s")
                # self.io.dtc_relay_ch_switch(name="dtc_relay3_ch3_switch",value=1)
                time.sleep(1)
            time.sleep(25)#20s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-3]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #     assert bit_0 == 1 and bit_3 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            # assert data_1[12:16] == '2005' and data_1[16:25] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"恢复电路故障J3-40 DoorHandFrontRightSwitch deactive持续超过20s"):
                logger.info(f"恢复电路故障J3-40 DoorHandFrontRightSwitch deactive持续超过20s")
                # self.io.dtc_relay_ch_switch(name="dtc_relay3_ch3_switch",value=0)
                time.sleep(1) 
            time.sleep(25)#20s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #     assert bit_0 == 0 and bit_3 == 1, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            # assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
            # self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a01',diagnostic_action="usagemode状态读取")
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_右后门外面电动门打开/关闭按钮-机械故障致动器卡滞_97B171_P2")
    def test_caseid_1993995(self):
        DTC_ID = [0x97, 0xB1, 0x71]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:481:0x04'):
                    logger.info(f"设置ccp：481:0x04")
                    self.sd_tester.write_ccp({481:0x04})
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002,0x190201,'59027f',diagnostic_action="读取当前的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190208,'59027f',diagnostic_action="读取历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x190209,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022f,'59027f',diagnostic_action="读取当前和历史的故障")
            self.sd_tester.send_data_and_check(0x1002,0x19022e,'59027f',diagnostic_action="读取历史的故障")
        with allure.step('设置快照信息'):
            self.sd_tester.send_data_and_check(0x1002,0x22DD0C,'62dd0c0f',diagnostic_action="供电等级")#由于429e只能是00，所以供电等级只能是0F
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000c','62dd0100000c',check_method=Check_Method.read,recover=False)
            Battery_Voltage=self.sd_tester.send_data_and_check(0x1002,0x22DD02,'62dd02',diagnostic_action="电池电压")[6:]
        with allure.step('制造当前故障;读取当前故障快照'):
            with allure.step(f"制造电路故障J3-38 DoorHandRearRightSwitch active持续超过20s"):
                logger.info(f"制造电路故障J3-38 DoorHandRearRightSwitch active持续超过20s")
                # self.io.dtc_relay_ch_switch(name="dtc_relay3_ch3_switch",value=1)
                time.sleep(1)
            time.sleep(25)#20s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-3]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #     assert bit_0 == 1 and bit_3 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            # assert data_1[12:16] == '2005' and data_1[16:25] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"恢复电路故障J3-38 DoorHandRearRightSwitch deactive持续超过20s"):
                logger.info(f"恢复电路故障J3-38 DoorHandRearRightSwitch deactive持续超过20s")
                # self.io.dtc_relay_ch_switch(name="dtc_relay3_ch3_switch",value=0)
                time.sleep(1) 
            time.sleep(25)#20s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #     assert bit_0 == 0 and bit_3 == 1, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            # assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
            # self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a01',diagnostic_action="usagemode状态读取")
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")