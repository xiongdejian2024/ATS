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

@allure.feature("BGM BaseTech/诊断刷写/诊断DTC")
@allure.story("车身DTC")
class Test_Body_DTC(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.bus_comm.set('backbonefr','BcmVddmBackBoneFr00','VehMtnStVehMtnSt','VehMtnSt2_StandStillVal3')#切UsageMode的前置条件

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        super().after_class(self, ecu)
            
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_HOD故障_A06596")
    def test_caseid_1993785(self):
        DTC_ID = [0xA0, 0x65, 0x96]
        signalvalue = [3,4,5]
        for signal in signalvalue:
            with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
                time.sleep(5)
            with allure.step('设置满足TRC'):
                self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                with allure.step(f'设置ccp:1150:0x02'):
                        logger.info(f"设置ccp：1150:0x02")
                        self.sd_tester.write_ccp({1150:0x02})
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
                with allure.step(f"设置cem_lin4.HodDim_Lin1Fr04.HandsOnDetectionErrorStatus={signal}"):
                    logger.info(f"设置cem_lin4.HodDim_Lin1Fr04.HandsOnDetectionErrorStatus={signal}")
                    self.bus_comm.set("cem_lin4", "HodDim_Lin1Fr04","HandsOnDetectionErrorStatus", signal)
                    time.sleep(10)#500ms
                TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
                data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                logger.info(f"receive DTC statusMask is {data_1[10:12]}")
                bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
                bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
                with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                    assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
                ##assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
            with allure.step('恢复仿真快照数据为默认值'):
                self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
            with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
                with allure.step(f"设置cem_lin4.HodDim_Lin1Fr04.HandsOnDetectionErrorStatus=0"):
                    logger.info(f"设置cem_lin4.HodDim_Lin1Fr04.HandsOnDetectionErrorStatus=0")
                    self.bus_comm.set("cem_lin4", "HodDim_Lin1Fr04","HandsOnDetectionErrorStatus", 0)
                time.sleep(10)#500ms
                data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
                logger.info(f"receive DTC statusMask is {data_2[10:12]}")
                bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
                bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
                with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                    assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
                ##assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
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
    @allure.title("UDS_ReadDTCInformation(0x19)_AWM-Supply电压太高_A02D17")
    def test_caseid_1993914(self):
        DTC_ID = [0xA0, 0x2D, 0x17]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:564:0x02'):
                    logger.info(f"设置ccp：564:0x02")
                    self.sd_tester.write_ccp({564:0x02})
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
            with allure.step(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrUFltHiVoltDetdFlt=Flt_Fault"):
                logger.info(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrUFltHiVoltDetdFlt=Flt_Fault")
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrUFltHiVoltDetdFlt', 'Flt_Fault')
            time.sleep(1)#0.3
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
                # assert bit_0 == 1 and bit_3 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            # assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrUFltHiVoltDetdFlt=Flt_NoFault"):
                logger.info(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrUFltHiVoltDetdFlt=Flt_NoFault")
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrUFltHiVoltDetdFlt', 'Flt_NoFault')
            time.sleep(1)#0.3
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
    @allure.title("UDS_ReadDTCInformation(0x19)_AWM-Supply电压太低_A02D16")
    def test_caseid_1993913(self):
        DTC_ID = [0xA0, 0x2D, 0x16]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:564:0x02'):
                    logger.info(f"设置ccp：564:0x02")
                    self.sd_tester.write_ccp({564:0x02})
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
            with allure.step(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrUFltLoVoltDetdFlt=Flt_Fault"):
                logger.info(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrUFltLoVoltDetdFlt=Flt_Fault")
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrUFltLoVoltDetdFlt', 'Flt_Fault')
            time.sleep(1)#0.3
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            # #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrUFltLoVoltDetdFlt=Flt_NoFault"):
                logger.info(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrUFltLoVoltDetdFlt=Flt_NoFault")
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrUFltLoVoltDetdFlt', 'Flt_NoFault')
            time.sleep(1)#0.3
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            # #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a01',diagnostic_action="usagemode状态读取")
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            # assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_AWM-电动尾翼未学习_A02E51")
    def test_caseid_1993904(self):
        DTC_ID = [0xA0, 0x2E, 0x51]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:564:0x02'):
                    logger.info(f"设置ccp：564:0x02")
                    self.sd_tester.write_ccp({564:0x02})
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
            with allure.step(f"设置cem_lin6.AwmCem_Lin6Fr01.CalStsAWM=CalStsAWM_Nocal"):
                logger.info(f"设置cem_lin6.AwmCem_Lin6Fr01.CalStsAWM=CalStsAWM_Nocal")
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','CalStsAWM', 'CalStsAWM_Nocal')
            time.sleep(1)#0.3
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            ##assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin6.AwmCem_Lin6Fr01.CalStsAWM=CalStsAWM_Cald"):
                logger.info(f"设置cem_lin6.AwmCem_Lin6Fr01.CalStsAWM=CalStsAWM_Cald")
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','CalStsAWM', 'CalStsAWM_Cald')
            time.sleep(1)#0.3
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            ##assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_AWM-输出电机-对地短路_A02E11")
    def test_caseid_1993908(self):
        DTC_ID = [0xA0, 0x2E, 0x11]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:564:0x02'):
                    logger.info(f"设置ccp：564:0x02")
                    self.sd_tester.write_ccp({564:0x02})
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
            with allure.step(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrIntFltActrFlt2=Flt_Fault"):
                logger.info(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrIntFltActrFlt2=Flt_Fault")
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrIntFltActrFlt2', 'Flt_Fault')
            time.sleep(1)#0.3
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            # #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrIntFltActrFlt2=Flt_NoFault"):
                logger.info(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrIntFltActrFlt2=Flt_NoFault")
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrIntFltActrFlt2', 'Flt_NoFault')
            time.sleep(1)#0.3
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            # assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_AWM-输出电机-对电源短路_A02E12")
    def test_caseid_1993909(self):
        DTC_ID = [0xA0, 0x2E, 0x12]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:564:0x02'):
                    logger.info(f"设置ccp：564:0x02")
                    self.sd_tester.write_ccp({564:0x02})
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
            with allure.step(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrIntFltActrFlt1=Flt_Fault"):
                logger.info(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrIntFltActrFlt1=Flt_Fault")
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrIntFltActrFlt1', 'Flt_Fault')
            time.sleep(1)#0.3
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrIntFltActrFlt1=Flt_NoFault"):
                logger.info(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrIntFltActrFlt1=Flt_NoFault")
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrIntFltActrFlt1', 'Flt_NoFault')
            time.sleep(1)#0.3
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_AWM-输出电机-开路_A07E13")
    def test_caseid_1993907(self):
        DTC_ID = [0xA0, 0x7E, 0x13]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:564:0x02'):
                    logger.info(f"设置ccp：564:0x02")
                    self.sd_tester.write_ccp({564:0x02})
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
            with allure.step(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrIntFltActrFlt3=Flt_Fault"):
                logger.info(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrIntFltActrFlt3=Flt_Fault")
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrIntFltActrFlt3', 'Flt_Fault')
            time.sleep(1)#0.3
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrIntFltActrFlt3=Flt_NoFault"):
                logger.info(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrIntFltActrFlt3=Flt_NoFault")
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrIntFltActrFlt3', 'Flt_NoFault')
            time.sleep(1)#0.3
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_AWM-输出电机-热保护失效_A02E4C")
    def test_caseid_1993905(self):
        DTC_ID = [0xA0, 0x2E, 0x4C]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:564:0x02'):
                    logger.info(f"设置ccp：564:0x02")
                    self.sd_tester.write_ccp({564:0x02})
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
            with allure.step(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrIntFltActrFlt5=Flt_Fault"):
                logger.info(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrIntFltActrFlt5=Flt_Fault")
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrIntFltActrFlt5', 'Flt_Fault')
            time.sleep(1)#0.3
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrIntFltActrFlt5=Flt_NoFault"):
                logger.info(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrIntFltActrFlt5=Flt_NoFault")
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrIntFltActrFlt5', 'Flt_NoFault')
            time.sleep(1)#0.3
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_AWM-输出电机-电流过大_A02E19")
    def test_caseid_1993906(self):
        DTC_ID = [0xA0, 0x2E, 0x19]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:564:0x02'):
                    logger.info(f"设置ccp：564:0x02")
                    self.sd_tester.write_ccp({564:0x02})
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
            with allure.step(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrIntFltActrFlt4=Flt_Fault"):
                logger.info(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrIntFltActrFlt4=Flt_Fault")
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrIntFltActrFlt4', 'Flt_Fault')
            time.sleep(1)#0.3
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrIntFltActrFlt4=Flt_NoFault"):
                logger.info(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrIntFltActrFlt4=Flt_NoFault")
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrIntFltActrFlt4', 'Flt_NoFault')
            time.sleep(1)#0.3
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)#0.3
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_AWM-霍尔传感器对地短路_A07D11")
    def test_caseid_1993912(self):
        DTC_ID = [0xA0, 0x7D, 0x11]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:564:0x02'):
                    logger.info(f"设置ccp：564:0x02")
                    self.sd_tester.write_ccp({564:0x02})
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
            with allure.step(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrHallSnsrFltHallOutpFlt=Flt_Fault"):
                logger.info(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrHallSnsrFltHallOutpFlt=Flt_Fault")
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrHallSnsrFltHallOutpFlt', 'Flt_Fault')
            time.sleep(2)#0.3
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrHallSnsrFltHallOutpFlt=Flt_NoFault"):
                logger.info(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrHallSnsrFltHallOutpFlt=Flt_NoFault")
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrHallSnsrFltHallOutpFlt', 'Flt_NoFault')
            time.sleep(2)#0.3
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_AWM的A霍尔传感器-传感器故障_A02D7C")
    def test_caseid_1993911(self):
        DTC_ID = [0xA0, 0x2D, 0x7C]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:564:0x02'):
                    logger.info(f"设置ccp：564:0x02")
                    self.sd_tester.write_ccp({564:0x02})
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
            with allure.step(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrHallSnsrFltHallAFlt=Flt_Fault"):
                logger.info(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrHallSnsrFltHallAFlt=Flt_Fault")
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrHallSnsrFltHallAFlt', 'Flt_Fault')
            time.sleep(2)#0.3
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrHallSnsrFltHallAFlt=Flt_NoFault"):
                logger.info(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrHallSnsrFltHallAFlt=Flt_NoFault")
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrHallSnsrFltHallAFlt', 'Flt_NoFault')
            time.sleep(2)#0.3
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_AWM的B霍尔传感器-传感器故障_A02D7D")
    def test_caseid_1993910(self):
        DTC_ID = [0xA0, 0x2D, 0x7D]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:564:0x02'):
                    logger.info(f"设置ccp：564:0x02")
                    self.sd_tester.write_ccp({564:0x02})
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
            with allure.step(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrHallSnsrFltHallBFlt=Flt_Fault"):
                logger.info(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrHallSnsrFltHallBFlt=Flt_Fault")
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrHallSnsrFltHallBFlt', 'Flt_Fault')
            time.sleep(2)#0.3
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrHallSnsrFltHallBFlt=Flt_NoFault"):
                logger.info(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrHallSnsrFltHallBFlt=Flt_NoFault")
                self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrHallSnsrFltHallBFlt', 'Flt_NoFault')
            time.sleep(2)#0.3
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_BMS 硬件故障_A1DB96")
    def test_caseid_1993927(self):
        DTC_ID = [0xA1, 0xDB, 0x96]
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
            with allure.step(f"设置cem_lin6.BmsCem_Lin6Fr03.BattSnsrHwFltRaw=DevErrSts2_Flt"):
                logger.info(f"设置cem_lin6.BmsCem_Lin6Fr03.BattSnsrHwFltRaw=DevErrSts2_Flt")
                self.bus_comm.set('cem_lin6','BmsCem_Lin6Fr03','BattSnsrHwFltRaw', 'DevErrSts2_Flt')
            time.sleep(12)#10
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin6.BmsCem_Lin6Fr03.BattSnsrHwFltRaw=DevErrSts2_NoFlt"):
                logger.info(f"设置cem_lin6.BmsCem_Lin6Fr03.BattSnsrHwFltRaw=DevErrSts2_NoFlt")
                self.bus_comm.set('cem_lin6','BmsCem_Lin6Fr03','BattSnsrHwFltRaw', 'DevErrSts2_NoFlt')
            time.sleep(12)#10
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_BMS 通信故障_A1DB87")
    def test_caseid_1993928(self):
        DTC_ID = [0xA1, 0xDB, 0x87]
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
            self.bus_comm.ipdu.pause_ecu_send('cem_lin6', 'BMS')
            time.sleep(12)#10
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            self.bus_comm.ipdu.resume_ecu_send('cem_lin6', 'BMS')
            time.sleep(12)#10
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_DSGL-LED 故障（短路或开路）_A03414")
    def test_caseid_1993985(self):
        DTC_ID = [0xA0, 0x34, 0x14]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:1532:0x02'):
                    logger.info(f"设置ccp：1532:0x02")
                    self.sd_tester.write_ccp({1532:0x02})
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
            with allure.step(f"设置cem_lin3.DsglCem_Lin3Fr01.DSGLIntFltLEDsFlt=Flt_Fault"):
                logger.info(f"设置cem_lin3.DsglCem_Lin3Fr01.DSGLIntFltLEDsFlt=Flt_Fault")
                self.bus_comm.set('cem_lin3','DsglCem_Lin3Fr01','DSGLIntFltLEDsFlt', 'Flt_Fault')
            time.sleep(1.5)#0.8
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin3.DsglCem_Lin3Fr01.DSGLIntFltLEDsFlt=Flt_NoFault"):
                logger.info(f"设置cem_lin3.DsglCem_Lin3Fr01.DSGLIntFltLEDsFlt=Flt_NoFault")
                self.bus_comm.set('cem_lin3','DsglCem_Lin3Fr01','DSGLIntFltLEDsFlt', 'Flt_NoFault')
            time.sleep(1.5)#0.8
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_DSGL-Supply电压太低_A03416")
    def test_caseid_1993986(self):
        DTC_ID = [0xA0, 0x34, 0x16]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:1532:0x02'):
                    logger.info(f"设置ccp：1532:0x02")
                    self.sd_tester.write_ccp({1532:0x02})
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
            with allure.step(f"设置cem_lin3.DsglCem_Lin3Fr01.DSGLIntFltLoVoltDetdFlt=Flt_Fault"):
                logger.info(f"设置cem_lin3.DsglCem_Lin3Fr01.DSGLIntFltLoVoltDetdFlt=Flt_Fault")
                self.bus_comm.set('cem_lin3','DsglCem_Lin3Fr01','DSGLIntFltLoVoltDetdFlt', 'Flt_Fault')
            time.sleep(1.5)#0.8
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin3.DsglCem_Lin3Fr01.DSGLIntFltLoVoltDetdFlt=Flt_NoFault"):
                logger.info(f"设置cem_lin3.DsglCem_Lin3Fr01.DSGLIntFltLoVoltDetdFlt=Flt_NoFault")
                self.bus_comm.set('cem_lin3','DsglCem_Lin3Fr01','DSGLIntFltLoVoltDetdFlt', 'Flt_NoFault')
            time.sleep(1.5)#0.8
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_DSGL-Supply电压太高_A03417")
    def test_caseid_1993987(self):
        DTC_ID = [0xA0, 0x34, 0x17]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:1532:0x02'):
                    logger.info(f"设置ccp：1532:0x02")
                    self.sd_tester.write_ccp({1532:0x02})
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
            with allure.step(f"设置cem_lin3.DsglCem_Lin3Fr01.DSGLIntFltHiVoltDetdFlt=Flt_Fault"):
                logger.info(f"设置cem_lin3.DsglCem_Lin3Fr01.DSGLIntFltHiVoltDetdFlt=Flt_Fault")
                self.bus_comm.set('cem_lin3','DsglCem_Lin3Fr01','DSGLIntFltHiVoltDetdFlt', 'Flt_Fault')
            time.sleep(1.5)#0.8
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin3.DsglCem_Lin3Fr01.DSGLIntFltHiVoltDetdFlt=Flt_NoFault"):
                logger.info(f"设置cem_lin3.DsglCem_Lin3Fr01.DSGLIntFltHiVoltDetdFlt=Flt_NoFault")
                self.bus_comm.set('cem_lin3','DsglCem_Lin3Fr01','DSGLIntFltHiVoltDetdFlt', 'Flt_NoFault')
            time.sleep(1.5)#0.8
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_DSGL-温度太高_A0344B")
    def test_caseid_1993984(self):
        DTC_ID = [0xA0, 0x34, 0x4B]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:1532:0x02'):
                    logger.info(f"设置ccp：1532:0x02")
                    self.sd_tester.write_ccp({1532:0x02})
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
            with allure.step(f"设置cem_lin3.DsglCem_Lin3Fr01.DSGLIntFltTpmFlt=Flt_Fault"):
                logger.info(f"设置cem_lin3.DsglCem_Lin3Fr01.DSGLIntFltTpmFlt=Flt_Fault")
                self.bus_comm.set('cem_lin3','DsglCem_Lin3Fr01','DSGLIntFltTpmFlt', 'Flt_Fault')
            time.sleep(1.5)#0.8
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin3.DsglCem_Lin3Fr01.DSGLIntFltTpmFlt=Flt_NoFault"):
                logger.info(f"设置cem_lin3.DsglCem_Lin3Fr01.DSGLIntFltTpmFlt=Flt_NoFault")
                self.bus_comm.set('cem_lin3','DsglCem_Lin3Fr01','DSGLIntFltTpmFlt', 'Flt_NoFault')
            time.sleep(1.5)#0.8
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_FCSI 低电压_A03716")
    def test_caseid_1993894(self):
        DTC_ID = [0xA0, 0x37, 0x16]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:1530:0x02,567:0x03'):
                    logger.info(f"设置ccp：1530:0x02,567:0x03")
                    self.sd_tester.write_ccp({1530:0x02,567:0x03})
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
            with allure.step(f"设置cem_lin2.FcsiEcm_Lin4Fr01.FCSIPwrSplyLo=OnOff1_On"):
                logger.info(f"设置cem_lin2.FcsiEcm_Lin4Fr01.FCSIPwrSplyLo=OnOff1_On")
                self.bus_comm.set('cem_lin2','FcsiEcm_Lin4Fr01','FCSIPwrSplyLo', 'OnOff1_On')
            time.sleep(1)#0.5
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin2.FcsiEcm_Lin4Fr01.FCSIPwrSplyLo=OnOff1_Off"):
                logger.info(f"设置cem_lin2.FcsiEcm_Lin4Fr01.FCSIPwrSplyLo=OnOff1_Off")
                self.bus_comm.set('cem_lin2','FcsiEcm_Lin4Fr01','FCSIPwrSplyLo', 'OnOff1_Off')
            time.sleep(1)#0.5
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_FCSI 过电压_A03717")
    def test_caseid_1993895(self):
        DTC_ID = [0xA0, 0x37, 0x17]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:1530:0x02,567:0x03'):
                    logger.info(f"设置ccp：1530:0x02,567:0x03")
                    self.sd_tester.write_ccp({1530:0x02,567:0x03})
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
            with allure.step(f"设置cem_lin2.FcsiEcm_Lin4Fr01.FCSIPwrSplyHi=OnOff1_On"):
                logger.info(f"设置cem_lin2.FcsiEcm_Lin4Fr01.FCSIPwrSplyHi=OnOff1_On")
                self.bus_comm.set('cem_lin2','FcsiEcm_Lin4Fr01','FCSIPwrSplyHi', 'OnOff1_On')
            time.sleep(1)#0.5
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin2.FcsiEcm_Lin4Fr01.FCSIPwrSplyHi=OnOff1_Off"):
                logger.info(f"设置cem_lin2.FcsiEcm_Lin4Fr01.FCSIPwrSplyHi=OnOff1_Off")
                self.bus_comm.set('cem_lin2','FcsiEcm_Lin4Fr01','FCSIPwrSplyHi', 'OnOff1_Off')
            time.sleep(1)#0.5
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_FCSI充电指示灯电路对地短_A03711")
    def test_caseid_1993897(self):
        DTC_ID = [0xA0, 0x37, 0x11]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:1530:0x02,567:0x03'):
                    logger.info(f"设置ccp：1530:0x02,567:0x03")
                    self.sd_tester.write_ccp({1530:0x02,567:0x03})
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
            with allure.step(f"设置cem_lin2.FcsiEcm_Lin4Fr01.FCSIShoCirc=OnOff1_On"):
                logger.info(f"设置cem_lin2.FcsiEcm_Lin4Fr01.FCSIShoCirc=OnOff1_On")
                self.bus_comm.set('cem_lin2','FcsiEcm_Lin4Fr01','FCSIShoCirc', 'OnOff1_On')
            time.sleep(1)#0.5
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin2.FcsiEcm_Lin4Fr01.FCSIShoCirc=OnOff1_Off"):
                logger.info(f"设置cem_lin2.FcsiEcm_Lin4Fr01.FCSIShoCirc=OnOff1_Off")
                self.bus_comm.set('cem_lin2','FcsiEcm_Lin4Fr01','FCSIShoCirc', 'OnOff1_Off')
            time.sleep(1)#0.5
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_FCSI充电指示灯电路开路_A03713")
    def test_caseid_1993896(self):
        DTC_ID = [0xA0, 0x37, 0x13]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:1530:0x02,567:0x03'):
                    logger.info(f"设置ccp：1530:0x02,567:0x03")
                    self.sd_tester.write_ccp({1530:0x02,567:0x03})
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
            with allure.step(f"设置cem_lin2.FcsiEcm_Lin4Fr01.FCSIOpenCirc=OnOff1_On"):
                logger.info(f"设置cem_lin2.FcsiEcm_Lin4Fr01.FCSIOpenCirc=OnOff1_On")
                self.bus_comm.set('cem_lin2','FcsiEcm_Lin4Fr01','FCSIOpenCirc', 'OnOff1_On')
            time.sleep(1)#0.5
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin2.FcsiEcm_Lin4Fr01.FCSIOpenCirc=OnOff1_Off"):
                logger.info(f"设置cem_lin2.FcsiEcm_Lin4Fr01.FCSIOpenCirc=OnOff1_Off")
                self.bus_comm.set('cem_lin2','FcsiEcm_Lin4Fr01','FCSIOpenCirc', 'OnOff1_Off')
            time.sleep(1)#0.5
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_PRLD低电压_A03616")
    def test_caseid_1993900(self):
        DTC_ID = [0xA0, 0x36, 0x16]
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
            with allure.step(f"设置cem_lin2.PrldCem_Lin2Fr02.ChrgLidManvgDCorAcDcUnderVoltFb=Boolean_TRUE"):
                logger.info(f"设置cem_lin2.PrldCem_Lin2Fr02.ChrgLidManvgDCorAcDcUnderVoltFb=Boolean_TRUE")
                self.bus_comm.set('cem_lin2','PrldCem_Lin2Fr02','ChrgLidManvgDCorAcDcUnderVoltFb', 'Boolean_TRUE')
            time.sleep(1)#0.5
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin2.PrldCem_Lin2Fr02.ChrgLidManvgDCorAcDcUnderVoltFb=Boolean_FALSE"):
                logger.info(f"设置cem_lin2.PrldCem_Lin2Fr02.ChrgLidManvgDCorAcDcUnderVoltFb=Boolean_FALSE")
                self.bus_comm.set('cem_lin2','PrldCem_Lin2Fr02','ChrgLidManvgDCorAcDcUnderVoltFb', 'Boolean_FALSE')
            time.sleep(1)#0.5
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_PRLD温度太高_A0364B")
    def test_caseid_1993899(self):
        DTC_ID = [0xA0, 0x36, 0x4B]
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
            with allure.step(f"设置cem_lin2.PrldCem_Lin2Fr02.ChrgLidManvgDCorAcDcOverTFb=Boolean_TRUE"):
                logger.info(f"设置cem_lin2.PrldCem_Lin2Fr02.ChrgLidManvgDCorAcDcOverTFb=Boolean_TRUE")
                self.bus_comm.set('cem_lin2','PrldCem_Lin2Fr02','ChrgLidManvgDCorAcDcOverTFb', 'Boolean_TRUE')
            time.sleep(1)#0.5
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin2.PrldCem_Lin2Fr02.ChrgLidManvgDCorAcDcOverTFb=Boolean_FALSE"):
                logger.info(f"设置cem_lin2.PrldCem_Lin2Fr02.ChrgLidManvgDCorAcDcOverTFb=Boolean_FALSE")
                self.bus_comm.set('cem_lin2','PrldCem_Lin2Fr02','ChrgLidManvgDCorAcDcOverTFb', 'Boolean_FALSE')
            time.sleep(1)#0.5
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_PRLD超过行程限制_A0364C")
    def test_caseid_1993898(self):
        DTC_ID = [0xA0, 0x36, 0x4C]
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
            with allure.step(f"设置cem_lin2.PrldCem_Lin2Fr02.ChrgLidManvgDCorAcDcOverTrvlFb=Boolean_TRUE"):
                logger.info(f"设置cem_lin2.PrldCem_Lin2Fr02.ChrgLidManvgDCorAcDcOverTrvlFb=Boolean_TRUE")
                self.bus_comm.set('cem_lin2','PrldCem_Lin2Fr02','ChrgLidManvgDCorAcDcOverTrvlFb', 'Boolean_TRUE')
            time.sleep(1)#0.5
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin2.PrldCem_Lin2Fr02.ChrgLidManvgDCorAcDcOverTrvlFb=Boolean_FALSE"):
                logger.info(f"设置cem_lin2.PrldCem_Lin2Fr02.ChrgLidManvgDCorAcDcOverTrvlFb=Boolean_FALSE")
                self.bus_comm.set('cem_lin2','PrldCem_Lin2Fr02','ChrgLidManvgDCorAcDcOverTrvlFb', 'Boolean_FALSE')
            time.sleep(1)#0.5
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_PRLD过电压_A03617")
    def test_caseid_1993901(self):
        DTC_ID = [0xA0, 0x36, 0x17]
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
            with allure.step(f"设置cem_lin2.PrldCem_Lin2Fr02.ChrgLidManvgDCorAcDcOverVoltFb=Boolean_TRUE"):
                logger.info(f"设置cem_lin2.PrldCem_Lin2Fr02.ChrgLidManvgDCorAcDcOverVoltFb=Boolean_TRUE")
                self.bus_comm.set('cem_lin2','PrldCem_Lin2Fr02','ChrgLidManvgDCorAcDcOverVoltFb', 'Boolean_TRUE')
            time.sleep(1)#0.5
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin2.PrldCem_Lin2Fr02.ChrgLidManvgDCorAcDcOverVoltFb=Boolean_FALSE"):
                logger.info(f"设置cem_lin2.PrldCem_Lin2Fr02.ChrgLidManvgDCorAcDcOverVoltFb=Boolean_FALSE")
                self.bus_comm.set('cem_lin2','PrldCem_Lin2Fr02','ChrgLidManvgDCorAcDcOverVoltFb', 'Boolean_FALSE')
            time.sleep(1)#0.5
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_PSGL-LED 故障（短路或开路）_A03514")
    def test_caseid_1993981(self):
        DTC_ID = [0xA0, 0x35, 0x14]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:1531:0x02'):
                    logger.info(f"设置ccp:1531:0x02")
                    self.sd_tester.write_ccp({1531:0x02})
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
            with allure.step(f"设置cem_lin3.PsglCem_Lin3Fr01.PSGLIntFltLEDsFlt=Flt_Fault"):
                logger.info(f"设置cem_lin3.PsglCem_Lin3Fr01.PSGLIntFltLEDsFlt=Flt_Fault")
                self.bus_comm.set('cem_lin3','PsglCem_Lin3Fr01','PSGLIntFltLEDsFlt', 'Flt_Fault')
            time.sleep(1.5)#0.8
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin3.PsglCem_Lin3Fr01.PSGLIntFltLEDsFlt=Flt_NoFault"):
                logger.info(f"设置cem_lin3.PsglCem_Lin3Fr01.PSGLIntFltLEDsFlt=Flt_NoFault")
                self.bus_comm.set('cem_lin3','PsglCem_Lin3Fr01','PSGLIntFltLEDsFlt', 'Flt_NoFault')
            time.sleep(1.5)#0.8
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_PSGL-Supply电压太低_A03516")
    def test_caseid_1993982(self):
        DTC_ID = [0xA0, 0x35, 0x16]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:1531:0x02'):
                    logger.info(f"设置ccp:1531:0x02")
                    self.sd_tester.write_ccp({1531:0x02})
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
            with allure.step(f"设置cem_lin3.PsglCem_Lin3Fr01.PSGLIntFltLoVoltDetdFlt=Flt_Fault"):
                logger.info(f"设置cem_lin3.PsglCem_Lin3Fr01.PSGLIntFltLoVoltDetdFlt=Flt_Fault")
                self.bus_comm.set('cem_lin3','PsglCem_Lin3Fr01','PSGLIntFltLoVoltDetdFlt', 'Flt_Fault')
            time.sleep(1.5)#0.8
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin3.PsglCem_Lin3Fr01.PSGLIntFltLoVoltDetdFlt=Flt_NoFault"):
                logger.info(f"设置cem_lin3.PsglCem_Lin3Fr01.PSGLIntFltLoVoltDetdFlt=Flt_NoFault")
                self.bus_comm.set('cem_lin3','PsglCem_Lin3Fr01','PSGLIntFltLoVoltDetdFlt', 'Flt_NoFault')
            time.sleep(1.5)#0.8
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_PSGL-Supply电压太高_A03517")
    def test_caseid_1993983(self):
        DTC_ID = [0xA0, 0x35, 0x17]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:1531:0x02'):
                    logger.info(f"设置ccp:1531:0x02")
                    self.sd_tester.write_ccp({1531:0x02})
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
            with allure.step(f"设置cem_lin3.PsglCem_Lin3Fr01.PSGLIntFltHiVoltDetdFlt=Flt_Fault"):
                logger.info(f"设置cem_lin3.PsglCem_Lin3Fr01.PSGLIntFltHiVoltDetdFlt=Flt_Fault")
                self.bus_comm.set('cem_lin3','PsglCem_Lin3Fr01','PSGLIntFltHiVoltDetdFlt', 'Flt_Fault')
            time.sleep(1.5)#0.8
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin3.PsglCem_Lin3Fr01.PSGLIntFltHiVoltDetdFlt=Flt_NoFault"):
                logger.info(f"设置cem_lin3.PsglCem_Lin3Fr01.PSGLIntFltHiVoltDetdFlt=Flt_NoFault")
                self.bus_comm.set('cem_lin3','PsglCem_Lin3Fr01','PSGLIntFltHiVoltDetdFlt', 'Flt_NoFault')
            time.sleep(1.5)#0.8
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_PSGL-温度太高_A0354B")
    def test_caseid_1993980(self):
        DTC_ID = [0xA0, 0x35, 0x4B]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:1531:0x02'):
                    logger.info(f"设置ccp:1531:0x02")
                    self.sd_tester.write_ccp({1531:0x02})
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
            with allure.step(f"设置cem_lin3.PsglCem_Lin3Fr01.PSGLIntFltTpmFlt=Flt_Fault"):
                logger.info(f"设置cem_lin3.PsglCem_Lin3Fr01.PSGLIntFltTpmFlt=Flt_Fault")
                self.bus_comm.set('cem_lin3','PsglCem_Lin3Fr01','PSGLIntFltTpmFlt', 'Flt_Fault')
            time.sleep(1.2)#0.8
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin3.PsglCem_Lin3Fr01.PSGLIntFltTpmFlt=Flt_NoFault"):
                logger.info(f"设置cem_lin3.PsglCem_Lin3Fr01.PSGLIntFltTpmFlt=Flt_NoFault")
                self.bus_comm.set('cem_lin3','PsglCem_Lin3Fr01','PSGLIntFltTpmFlt', 'Flt_NoFault')
            time.sleep(1.2)#0.8
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_充电盖卡滞故障_A02F90")
    def test_caseid_1993902(self):
        DTC_ID = [0xA0, 0x2F, 0x90]
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
            with allure.step(f"设置cem_lin2.PrldCem_Lin2Fr02.ChrgLidManvgDCorAcDcBlkFb=Boolean_TRUE"):
                logger.info(f"设置cem_lin2.PrldCem_Lin2Fr02.ChrgLidManvgDCorAcDcBlkFb=Boolean_TRUE")
                self.bus_comm.set('cem_lin2','PrldCem_Lin2Fr02','ChrgLidManvgDCorAcDcBlkFb', 'Boolean_TRUE')
            time.sleep(1)#0.5
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin2.PrldCem_Lin2Fr02.ChrgLidManvgDCorAcDcBlkFb=Boolean_FALSE"):
                logger.info(f"设置cem_lin2.PrldCem_Lin2Fr02.ChrgLidManvgDCorAcDcBlkFb=Boolean_FALSE")
                self.bus_comm.set('cem_lin2','PrldCem_Lin2Fr02','ChrgLidManvgDCorAcDcBlkFb', 'Boolean_FALSE')
            time.sleep(1)#0.5
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_充电盖电路故障_A02F10")
    def test_caseid_1993903(self):
        DTC_ID = [0xA0, 0x2F, 0x10]
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
            with allure.step(f"设置cem_lin2.PrldCem_Lin2Fr02.ChrgLidManvgDCorAcDcElecErrFb=Boolean_TRUE"):
                logger.info(f"设置cem_lin2.PrldCem_Lin2Fr02.ChrgLidManvgDCorAcDcElecErrFb=Boolean_TRUE")
                self.bus_comm.set('cem_lin2','PrldCem_Lin2Fr02','ChrgLidManvgDCorAcDcElecErrFb', 'Boolean_TRUE')
            time.sleep(1)#0.5
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin2.PrldCem_Lin2Fr02.ChrgLidManvgDCorAcDcElecErrFb=Boolean_FALSE"):
                logger.info(f"设置cem_lin2.PrldCem_Lin2Fr02.ChrgLidManvgDCorAcDcElecErrFb=Boolean_FALSE")
                self.bus_comm.set('cem_lin2','PrldCem_Lin2Fr02','ChrgLidManvgDCorAcDcElecErrFb', 'Boolean_FALSE')
            time.sleep(1)#0.5
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_汽车电源电压过高——通用电气故障_A00F01")
    def test_caseid_1993942(self):
        DTC_ID = [0xA0, 0x0F, 0x01]
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
            self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
            self.bus_comm.send_pdu("cem_lin6", 0x06, [0x0, 0x7C, 0xFA, 0xFF, 0xFF, 0xFF, 0xFF])
            time.sleep(3)
            self.bus_comm.send_pdu("cem_lin6", 0x06, [0x0, 0x7C, 0xFA, 0xFF, 0xFF, 0xFF, 0xFF])
            time.sleep(27)#21.5
            self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts.UhiDurgDrvg)
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
            self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
            self.bus_comm.send_pdu("cem_lin6", 0x06, [0x0, 0x7C, 0xC8, 0xFF, 0xFF, 0xFF, 0xFF])
            time.sleep(3)
            self.bus_comm.send_pdu("cem_lin6", 0x06, [0x0, 0x7C, 0xC8, 0xFF, 0xFF, 0xFF, 0xFF])
            time.sleep(22)#11
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
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.smoke
    @allure.title("UDS_ReadDTCInformation(0x19)_汽车电源电压过低——通用电气故障_A01001")
    def test_caseid_1993941(self):
        DTC_ID = [0xA0, 0x10, 0x01]
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
            self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
            self.bus_comm.set_BMS_stop_req(low_sts=SocSts.LessOrEqual10Per,low_soh=1000,low_soc=1000)
            self.bus_comm.set_batturaw(BattURaw=11.0)
            self.bus_comm.set_dcdc_battary_act_sts(DcDcActvd=DcDcActvd.ConversionToLVSide)
            time.sleep(120)
            self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts.UloDurgdrvg)
            time.sleep(27)#21.5
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-4]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1 and bit_3 == 1 , f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            assert data_1[12:16] == '2005' and data_1[16:24] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            self.bus_comm.set_batturaw(BattURaw=15.0)
            self.bus_comm.set_dcdc_battary_act_sts(DcDcActvd=DcDcActvd.NoConversionToLVSide)
            # self.bus_comm.set_BMS_stop_req(low_sts=SocSts.Larger15Per,low_soh=10,low_soc=10)
            self.bus_comm.set_BMS_stop_req(low_sts=SocSts.LessOrEqual10Per,low_soh=1000,low_soc=1000)
            time.sleep(27)#11
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0 and bit_3 == 1 , f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_阳光传感器组件故障组件内部故障_90BE96")
    def test_caseid_1993788(self):
        DTC_ID = [0x90, 0xBE, 0x96]
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
            with allure.step(f"设置cem_lin1.RlsmCem_Lin1Fr03.SolarSnsrErr=1"):
                logger.info(f"设置cem_lin1.RlsmCem_Lin1Fr03.SolarSnsrErr=1")
                self.bus_comm.set('cem_lin1','RlsmCem_Lin1Fr03','SolarSnsrErr',1)
            time.sleep(1)
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin1.RlsmCem_Lin1Fr03.SolarSnsrErr=0"):
                logger.info(f"设置cem_lin1.RlsmCem_Lin1Fr03.SolarSnsrErr=0")
                self.bus_comm.set('cem_lin1','RlsmCem_Lin1Fr03','SolarSnsrErr',0)
            time.sleep(1)
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_RLSM相对湿度传感器故障(要求:477044)_970149")
    def test_caseid_1993789(self):
        DTC_ID = [0x97, 0x01, 0x49]
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
            with allure.step(f"设置cem_lin1.RlsmCem_Lin1Fr02.RelHumSnsrErr=1"):
                logger.info(f"设置cem_lin1.RlsmCem_Lin1Fr02.RelHumSnsrErr=1")
                self.bus_comm.set('cem_lin1','RlsmCem_Lin1Fr02','RelHumSnsrErr',1)
            time.sleep(2)#825ms
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin1.RlsmCem_Lin1Fr02.RelHumSnsrErr=0"):
                logger.info(f"设置cem_lin1.RlsmCem_Lin1Fr02.RelHumSnsrErr=0")
                self.bus_comm.set('cem_lin1','RlsmCem_Lin1Fr02','RelHumSnsrErr',0)
            time.sleep(2)#825ms
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_ALM1-RGB LED通路故障(短路或开路)_A04010")
    def test_caseid_1993891(self):
        DTC_ID = [0xA0, 0x40, 0x10]
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
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr10.ALM1FailrStsLEDSts=1"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr10.ALM1FailrStsLEDSts=1")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr10','ALM1FailrStsLEDSts',1)
            time.sleep(1)#100ms
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr10.ALM1FailrStsLEDSts=0"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr10.ALM1FailrStsLEDSts=0")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr10','ALM1FailrStsLEDSts',0)
            time.sleep(1)#100ms
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_ALM2-RGB LED通路故障(短路或开路)_A04110")
    def test_caseid_1993888(self):
        DTC_ID = [0xA0, 0x41, 0x10]
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
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr11.ALM2FailrStsLEDSts=1"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr11.ALM2FailrStsLEDSts=1")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr11','ALM2FailrStsLEDSts',1)
            time.sleep(1)#100ms
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr11.ALM2FailrStsLEDSts=0"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr11.ALM2FailrStsLEDSts=0")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr11','ALM2FailrStsLEDSts',0)
            time.sleep(1)#100ms
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_ALM3-RGB LED通路故障(短路或开路)_A04210")
    def test_caseid_1993885(self):
        DTC_ID = [0xA0, 0x42, 0x10]
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
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr12.ALM3FailrStsLEDSts=1"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr12.ALM3FailrStsLEDSts=1")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr12','ALM3FailrStsLEDSts',1)
            time.sleep(1)#100ms
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr12.ALM3FailrStsLEDSts=0"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr12.ALM3FailrStsLEDSts=0")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr12','ALM3FailrStsLEDSts',0)
            time.sleep(1)#100ms
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_ALM4-RGB LED通路故障(短路或开路)_A04310")
    def test_caseid_1993882(self):
        DTC_ID = [0xA0, 0x43, 0x10]
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
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr13.ALM4FailrStsLEDSts=1"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr13.ALM4FailrStsLEDSts=1")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr13','ALM4FailrStsLEDSts',1)
            time.sleep(1)#100ms
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr13.ALM4FailrStsLEDSts=0"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr13.ALM4FailrStsLEDSts=0")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr13','ALM4FailrStsLEDSts',0)
            time.sleep(1)#100ms
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_ALM5-RGB LED通路故障(短路或开路)_A04410")
    def test_caseid_1993879(self):
        DTC_ID = [0xA0, 0x44, 0x10]
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
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr14.ALM5FailrStsLEDSts=1"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr14.ALM5FailrStsLEDSts=1")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr14','ALM5FailrStsLEDSts',1)
            time.sleep(1)#100ms
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr14.ALM5FailrStsLEDSts=0"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr14.ALM5FailrStsLEDSts=0")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr14','ALM5FailrStsLEDSts',0)
            time.sleep(1)#100ms
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_ALM6-RGB LED通路故障(短路或开路)_A04510")
    def test_caseid_1993876(self):
        DTC_ID = [0xA0, 0x45, 0x10]
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
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr15.ALM6FailrStsLEDSts=1"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr15.ALM6FailrStsLEDSts=1")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr15','ALM6FailrStsLEDSts',1)
            time.sleep(1)#100ms
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr15.ALM6FailrStsLEDSts=0"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr15.ALM6FailrStsLEDSts=0")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr15','ALM6FailrStsLEDSts',0)
            time.sleep(1)#100ms
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_ALM1-Supply电压过高或过低_A0401C")
    def test_caseid_1993890(self):
        DTC_ID = [0xA0, 0x40, 0x1C]
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
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr10.ALM1FailrStsVltSts=1"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr10.ALM1FailrStsVltSts=1")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr10','ALM1FailrStsVltSts',1)
            time.sleep(1)#100ms
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr10.ALM1FailrStsVltSts=0"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr10.ALM1FailrStsVltSts=0")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr10','ALM1FailrStsVltSts',0)
            time.sleep(1)#100ms
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_ALM2-Supply电压过高或过低_A0411C")
    def test_caseid_1993887(self):
        DTC_ID = [0xA0, 0x41, 0x1C]
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
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr11.ALM2FailrStsVltSts=1"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr11.ALM2FailrStsVltSts=1")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr11','ALM2FailrStsVltSts',1)
            time.sleep(1)#100ms
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr11.ALM2FailrStsVltSts=0"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr11.ALM2FailrStsVltSts=0")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr11','ALM2FailrStsVltSts',0)
            time.sleep(1)#100ms
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_ALM3-Supply电压过高或过低_A0421C")
    def test_caseid_1993884(self):
        DTC_ID = [0xA0, 0x42, 0x1C]
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
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr12.ALM3FailrStsVltSts=1"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr12.ALM3FailrStsVltSts=1")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr12','ALM3FailrStsVltSts',1)
            time.sleep(1)#100ms
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr12.ALM3FailrStsVltSts=0"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr12.ALM3FailrStsVltSts=0")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr12','ALM3FailrStsVltSts',0)
            time.sleep(1)#100ms
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_ALM4-Supply电压过高或过低_A0431C")
    def test_caseid_1993881(self):
        DTC_ID = [0xA0, 0x43, 0x1C]
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
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr13.ALM4FailrStsVltSts=1"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr13.ALM4FailrStsVltSts=1")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr13','ALM4FailrStsVltSts',1)
            time.sleep(1)#100ms
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr13.ALM4FailrStsVltSts=0"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr13.ALM4FailrStsVltSts=0")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr13','ALM4FailrStsVltSts',0)
            time.sleep(1)#100ms
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_ALM5-Supply电压过高或过低_A0441C")
    def test_caseid_1993878(self):
        DTC_ID = [0xA0, 0x44, 0x1C]
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
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr14.ALM5FailrStsVltSts=1"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr14.ALM5FailrStsVltSts=1")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr14','ALM5FailrStsVltSts',1)
            time.sleep(1)#100ms
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr14.ALM5FailrStsVltSts=0"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr14.ALM5FailrStsVltSts=0")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr14','ALM5FailrStsVltSts',0)
            time.sleep(1)#100ms
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
            
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_ALM6-Supply电压过高或过低_A0451C")
    def test_caseid_1993875(self):
        DTC_ID = [0xA0, 0x45, 0x1C]
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
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr15.ALM6FailrStsVltSts=1"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr15.ALM6FailrStsVltSts=1")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr15','ALM6FailrStsVltSts',1)
            time.sleep(1)#100ms
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr15.ALM6FailrStsVltSts=0"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr15.ALM6FailrStsVltSts=0")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr15','ALM6FailrStsVltSts',0)
            time.sleep(1)#100ms
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
    
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_ALM1-温度太高_A0404B")
    def test_caseid_1993889(self):
        DTC_ID = [0xA0, 0x40, 0x4B]
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
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr10.ALM1FailrStsTmpSts=1"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr10.ALM1FailrStsTmpSts=1")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr10','ALM1FailrStsTmpSts',1)
            time.sleep(1)#100ms
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr10.ALM1FailrStsTmpSts=0"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr10.ALM1FailrStsTmpSts=0")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr10','ALM1FailrStsTmpSts',0)
            time.sleep(1)#100ms
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
    
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_ALM2-温度太高_A0414B")
    def test_caseid_1993886(self):
        DTC_ID = [0xA0, 0x41, 0x4B]
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
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr11.ALM2FailrStsTmpSts=1"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr11.ALM2FailrStsTmpSts=1")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr11','ALM2FailrStsTmpSts',1)
            time.sleep(1)#100ms
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr11.ALM2FailrStsTmpSts=0"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr11.ALM2FailrStsTmpSts=0")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr11','ALM2FailrStsTmpSts',0)
            time.sleep(1)#100ms
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
    
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_ALM3-温度太高_A0424B")
    def test_caseid_1993883(self):
        DTC_ID = [0xA0, 0x42, 0x4B]
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
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr12.ALM3FailrStsTmpSts=1"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr12.ALM3FailrStsTmpSts=1")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr12','ALM3FailrStsTmpSts',1)
            time.sleep(1)#100ms
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr12.ALM3FailrStsTmpSts=0"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr12.ALM3FailrStsTmpSts=0")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr12','ALM3FailrStsTmpSts',0)
            time.sleep(1)#100ms
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
    
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_ALM4-温度太高_A0434B")
    def test_caseid_1993880(self):
        DTC_ID = [0xA0, 0x43, 0x4B]
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
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr13.ALM4FailrStsTmpSts=1"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr13.ALM4FailrStsTmpSts=1")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr13','ALM4FailrStsTmpSts',1)
            time.sleep(1)#100ms
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr13.ALM4FailrStsTmpSts=0"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr13.ALM4FailrStsTmpSts=0")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr13','ALM4FailrStsTmpSts',0)
            time.sleep(1)#100ms
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
    
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_ALM5-温度太高_A0444B")
    def test_caseid_1993877(self):
        DTC_ID = [0xA0, 0x44, 0x4B]
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
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr14.ALM5FailrStsTmpSts=1"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr14.ALM5FailrStsTmpSts=1")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr14','ALM5FailrStsTmpSts',1)
            time.sleep(1)#100ms
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr14.ALM5FailrStsTmpSts=0"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr14.ALM5FailrStsTmpSts=0")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr14','ALM5FailrStsTmpSts',0)
            time.sleep(1)#100ms
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
    
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_ALM6-温度太高_A0454B")
    def test_caseid_1993874(self):
        DTC_ID = [0xA0, 0x45, 0x4B]
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
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr15.ALM6FailrStsTmpSts=1"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr15.ALM6FailrStsTmpSts=1")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr15','ALM6FailrStsTmpSts',1)
            time.sleep(1)#100ms
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin5.CemCem_Lin5Fr15.ALM6FailrStsTmpSts=0"):
                logger.info(f"设置cem_lin5.CemCem_Lin5Fr15.ALM6FailrStsTmpSts=0")
                self.bus_comm.set('cem_lin5','CemCem_Lin5Fr15','ALM6FailrStsTmpSts',0)
            time.sleep(1)#100ms
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
    
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_ALM7-RGB LED通路故障(短路或开路)_A04610")
    def test_caseid_1993873(self):
        DTC_ID = [0xA0, 0x46, 0x10]
        ccp = [{950:0x01,636:0x01,964:0x01},
               {950:0x01,636:0x02,964:0x00},
               {950:0x01,636:0x02,964:0x01},
               {950:0x02,636:0x01,964:0x00},
               {950:0x02,636:0x01,964:0x01},
               {950:0x02,636:0x02,964:0x00},
               {950:0x02,636:0x02,964:0x01}]
        for ccp_item in ccp:
            with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
                time.sleep(5)
            with allure.step('设置满足TRC'):
                self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                with allure.step(f'设置ccp:{ccp_item}'):
                    logger.info(f"设置ccp：{ccp_item}")
                    self.sd_tester.write_ccp(ccp_item)
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
                with allure.step(f"设置cem_lin5.CemCem_Lin5Fr16.ALM7FailrStsLEDSts=1"):
                    logger.info(f"设置cem_lin5.CemCem_Lin5Fr16.ALM7FailrStsLEDSts=1")
                    self.bus_comm.set('cem_lin5','CemCem_Lin5Fr16','ALM7FailrStsLEDSts',1)
                time.sleep(1)#100ms
                TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
                data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                logger.info(f"receive DTC statusMask is {data_1[10:12]}")
                bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
                bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
                with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                    assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
                #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
            with allure.step('恢复仿真快照数据为默认值'):
                self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
            with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
                with allure.step(f"设置cem_lin5.CemCem_Lin5Fr16.ALM7FailrStsLEDSts=0"):
                    logger.info(f"设置cem_lin5.CemCem_Lin5Fr16.ALM7FailrStsLEDSts=0")
                    self.bus_comm.set('cem_lin5','CemCem_Lin5Fr16','ALM7FailrStsLEDSts',0)
                time.sleep(1)#100ms
                data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
                logger.info(f"receive DTC statusMask is {data_2[10:12]}")
                bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
                bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
                with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                    assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
                #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
            # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
            #     self.mix.network_sleep()
            #     self.mix.network_wakeup()
            #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
            #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
            #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            #     time.sleep(5)
            #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
            #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
                self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
                time.sleep(1)
                self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
    
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_ALM7-Supply电压过高或过低_A0461C")
    def test_caseid_1993872(self):
        DTC_ID = [0xA0, 0x46, 0x1C]
        ccp = [{950:0x01,636:0x01,964:0x01},
               {950:0x01,636:0x02,964:0x00},
               {950:0x01,636:0x02,964:0x01},
               {950:0x02,636:0x01,964:0x00},
               {950:0x02,636:0x01,964:0x01},
               {950:0x02,636:0x02,964:0x00},
               {950:0x02,636:0x02,964:0x01}]
        for ccp_item in ccp:
            with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
                time.sleep(5)
            with allure.step('设置满足TRC'):
                self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                with allure.step(f'设置ccp:{ccp_item}'):
                    logger.info(f"设置ccp：{ccp_item}")
                    self.sd_tester.write_ccp(ccp_item)
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
                with allure.step(f"设置cem_lin5.CemCem_Lin5Fr16.ALM7FailrStsVltSts=1"):
                    logger.info(f"设置cem_lin5.CemCem_Lin5Fr16.ALM7FailrStsVltSts=1")
                    self.bus_comm.set('cem_lin5','CemCem_Lin5Fr16','ALM7FailrStsVltSts',1)
                time.sleep(1)#100ms
                TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
                data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                logger.info(f"receive DTC statusMask is {data_1[10:12]}")
                bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
                bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
                with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                    assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
                #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
            with allure.step('恢复仿真快照数据为默认值'):
                self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
            with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
                with allure.step(f"设置cem_lin5.CemCem_Lin5Fr16.ALM7FailrStsVltSts=0"):
                    logger.info(f"设置cem_lin5.CemCem_Lin5Fr16.ALM7FailrStsVltSts=0")
                    self.bus_comm.set('cem_lin5','CemCem_Lin5Fr16','ALM7FailrStsVltSts',0)
                time.sleep(1)#100ms
                data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
                logger.info(f"receive DTC statusMask is {data_2[10:12]}")
                bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
                bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
                with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                    assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
                #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
            # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
            #     self.mix.network_sleep()
            #     self.mix.network_wakeup()
            #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
            #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
            #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            #     time.sleep(5)
            #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
            #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
                self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
                time.sleep(1)
                self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
    
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_ALM7-温度太高_A0464B")
    def test_caseid_1993871(self):
        DTC_ID = [0xA0, 0x46, 0x4B]
        ccp = [{950:0x01,636:0x01,964:0x01},
               {950:0x01,636:0x02,964:0x00},
               {950:0x01,636:0x02,964:0x01},
               {950:0x02,636:0x01,964:0x00},
               {950:0x02,636:0x01,964:0x01},
               {950:0x02,636:0x02,964:0x00},
               {950:0x02,636:0x02,964:0x01}]
        for ccp_item in ccp:
            with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
                time.sleep(5)
            with allure.step('设置满足TRC'):
                self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                with allure.step(f'设置ccp:{ccp_item}'):
                    logger.info(f"设置ccp：{ccp_item}")
                    self.sd_tester.write_ccp(ccp_item)
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
                with allure.step(f"设置cem_lin5.CemCem_Lin5Fr16.ALM7FailrStsTmpSts=1"):
                    logger.info(f"设置cem_lin5.CemCem_Lin5Fr16.ALM7FailrStsTmpSts=1")
                    self.bus_comm.set('cem_lin5','CemCem_Lin5Fr16','ALM7FailrStsTmpSts',1)
                time.sleep(1)#100ms
                TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
                data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                logger.info(f"receive DTC statusMask is {data_1[10:12]}")
                bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
                bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
                with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                    assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
                #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
            with allure.step('恢复仿真快照数据为默认值'):
                self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
            with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
                with allure.step(f"设置cem_lin5.CemCem_Lin5Fr16.ALM7FailrStsTmpSts=0"):
                    logger.info(f"设置cem_lin5.CemCem_Lin5Fr16.ALM7FailrStsTmpSts=0")
                    self.bus_comm.set('cem_lin5','CemCem_Lin5Fr16','ALM7FailrStsTmpSts',0)
                time.sleep(1)#100ms
                data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
                logger.info(f"receive DTC statusMask is {data_2[10:12]}")
                bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
                bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
                with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                    assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
                #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
            # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
            #     self.mix.network_sleep()
            #     self.mix.network_wakeup()
            #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
            #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
            #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            #     time.sleep(5)
            #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
            #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
                self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
                time.sleep(1)
                self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
    
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_ALM8-RGB LED通路故障(短路或开路)_A04710")
    def test_caseid_1993870(self):
        DTC_ID = [0xA0, 0x47, 0x10]
        ccp = [{950:0x01,636:0x02,964:0x00},
               {950:0x01,636:0x02,964:0x01},
               {950:0x02,636:0x01,964:0x00},
               {950:0x02,636:0x01,964:0x01},
               {950:0x02,636:0x02,964:0x00},
               {950:0x02,636:0x02,964:0x01}]
        for ccp_item in ccp:
            with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
                time.sleep(5)
            with allure.step('设置满足TRC'):
                self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                with allure.step(f'设置ccp:{ccp_item}'):
                    logger.info(f"设置ccp：{ccp_item}")
                    self.sd_tester.write_ccp(ccp_item)
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
                with allure.step(f"设置cem_lin5.CemCem_Lin5Fr17.ALM8FailrStsLEDSts=1"):
                    logger.info(f"设置cem_lin5.CemCem_Lin5Fr17.ALM8FailrStsLEDSts=1")
                    self.bus_comm.set('cem_lin5','CemCem_Lin5Fr17','ALM8FailrStsLEDSts',1)
                time.sleep(1)#100ms
                TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
                data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                logger.info(f"receive DTC statusMask is {data_1[10:12]}")
                bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
                bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
                with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                    assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
                #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
            with allure.step('恢复仿真快照数据为默认值'):
                self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
            with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
                with allure.step(f"设置cem_lin5.CemCem_Lin5Fr17.ALM8FailrStsLEDSts=0"):
                    logger.info(f"设置cem_lin5.CemCem_Lin5Fr17.ALM8FailrStsLEDSts=0")
                    self.bus_comm.set('cem_lin5','CemCem_Lin5Fr17','ALM8FailrStsLEDSts',0)
                time.sleep(1)#100ms
                data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
                logger.info(f"receive DTC statusMask is {data_2[10:12]}")
                bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
                bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
                with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                    assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
                #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
            # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
            #     self.mix.network_sleep()
            #     self.mix.network_wakeup()
            #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
            #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
            #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            #     time.sleep(5)
            #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
            #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
                self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
                time.sleep(1)
                self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
    
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_ALM8-Supply电压过高或过低_A0471C")
    def test_caseid_1993869(self):
        DTC_ID = [0xA0, 0x47, 0x1C]
        ccp = [{950:0x01,636:0x02,964:0x00},
               {950:0x01,636:0x02,964:0x01},
               {950:0x02,636:0x01,964:0x00},
               {950:0x02,636:0x01,964:0x01},
               {950:0x02,636:0x02,964:0x00},
               {950:0x02,636:0x02,964:0x01}]
        for ccp_item in ccp:
            with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
                time.sleep(5)
            with allure.step('设置满足TRC'):
                self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                with allure.step(f'设置ccp:{ccp_item}'):
                    logger.info(f"设置ccp：{ccp_item}")
                    self.sd_tester.write_ccp(ccp_item)
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
                with allure.step(f"设置cem_lin5.CemCem_Lin5Fr17.ALM8FailrStsVltSts=1"):
                    logger.info(f"设置cem_lin5.CemCem_Lin5Fr17.ALM8FailrStsVltSts=1")
                    self.bus_comm.set('cem_lin5','CemCem_Lin5Fr17','ALM8FailrStsVltSts',1)
                time.sleep(1)#100ms
                TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
                data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                logger.info(f"receive DTC statusMask is {data_1[10:12]}")
                bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
                bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
                with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                    assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
                #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
            with allure.step('恢复仿真快照数据为默认值'):
                self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
            with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
                with allure.step(f"设置cem_lin5.CemCem_Lin5Fr17.ALM8FailrStsVltSts=0"):
                    logger.info(f"设置cem_lin5.CemCem_Lin5Fr17.ALM8FailrStsVltSts=0")
                    self.bus_comm.set('cem_lin5','CemCem_Lin5Fr17','ALM8FailrStsVltSts',0)
                time.sleep(1)#100ms
                data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
                logger.info(f"receive DTC statusMask is {data_2[10:12]}")
                bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
                bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
                with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                    assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
                #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
            # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
            #     self.mix.network_sleep()
            #     self.mix.network_wakeup()
            #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
            #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
            #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            #     time.sleep(5)
            #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
            #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
                self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
                time.sleep(1)
                self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
    
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_ALM8-温度太高_A0474B")
    def test_caseid_1993868(self):
        DTC_ID = [0xA0, 0x47, 0x4B]
        ccp = [{950:0x01,636:0x02,964:0x00},
               {950:0x01,636:0x02,964:0x01},
               {950:0x02,636:0x01,964:0x00},
               {950:0x02,636:0x01,964:0x01},
               {950:0x02,636:0x02,964:0x00},
               {950:0x02,636:0x02,964:0x01}]
        for ccp_item in ccp:
            with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
                time.sleep(5)
            with allure.step('设置满足TRC'):
                self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                with allure.step(f'设置ccp:{ccp_item}'):
                    logger.info(f"设置ccp：{ccp_item}")
                    self.sd_tester.write_ccp(ccp_item)
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
                with allure.step(f"设置cem_lin5.CemCem_Lin5Fr17.ALM8FailrStsTmpSts=1"):
                    logger.info(f"设置cem_lin5.CemCem_Lin5Fr17.ALM8FailrStsTmpSts=1")
                    self.bus_comm.set('cem_lin5','CemCem_Lin5Fr17','ALM8FailrStsTmpSts',1)
                time.sleep(1)#100ms
                TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
                data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                logger.info(f"receive DTC statusMask is {data_1[10:12]}")
                bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
                bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
                with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                    assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
                #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
            with allure.step('恢复仿真快照数据为默认值'):
                self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
            with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
                with allure.step(f"设置cem_lin5.CemCem_Lin5Fr17.ALM8FailrStsTmpSts=0"):
                    logger.info(f"设置cem_lin5.CemCem_Lin5Fr17.ALM8FailrStsTmpSts=0")
                    self.bus_comm.set('cem_lin5','CemCem_Lin5Fr17','ALM8FailrStsTmpSts',0)
                time.sleep(1)#100ms
                data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
                logger.info(f"receive DTC statusMask is {data_2[10:12]}")
                bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
                bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
                with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                    assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
                #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
            # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
            #     self.mix.network_sleep()
            #     self.mix.network_wakeup()
            #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
            #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
            #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            #     time.sleep(5)
            #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
            #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
                self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
                time.sleep(1)
                self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
    
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_ALM9-RGB LED通路故障(短路或开路)_A06610")
    def test_caseid_1993845(self):
        DTC_ID = [0xA0, 0x66, 0x10]
        ccp = [{950:0x01,636:0x02,964:0x01},
               {950:0x02,636:0x02,964:0x00},
               {950:0x02,636:0x02,964:0x01}]
        for ccp_item in ccp:
            with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
                time.sleep(5)
            with allure.step('设置满足TRC'):
                self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                with allure.step(f'设置ccp:{ccp_item}'):
                    logger.info(f"设置ccp：{ccp_item}")
                    self.sd_tester.write_ccp(ccp_item)
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
                with allure.step(f"设置cem_lin5.CemCem_Lin5Fr18.ALM9FailrStsLEDSts=1"):
                    logger.info(f"设置cem_lin5.CemCem_Lin5Fr18.ALM9FailrStsLEDSts=1")
                    self.bus_comm.set('cem_lin5','CemCem_Lin5Fr18','ALM9FailrStsLEDSts',1)
                time.sleep(1)#100ms
                TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
                data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                logger.info(f"receive DTC statusMask is {data_1[10:12]}")
                bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
                bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
                with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                    assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
                #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
            with allure.step('恢复仿真快照数据为默认值'):
                self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
            with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
                with allure.step(f"设置cem_lin5.CemCem_Lin5Fr18.ALM9FailrStsLEDSts=0"):
                    logger.info(f"设置cem_lin5.CemCem_Lin5Fr18.ALM9FailrStsLEDSts=0")
                    self.bus_comm.set('cem_lin5','CemCem_Lin5Fr18','ALM9FailrStsLEDSts',0)
                time.sleep(1)#100ms
                data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
                logger.info(f"receive DTC statusMask is {data_2[10:12]}")
                bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
                bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
                with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                    assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
                #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
            # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
            #     self.mix.network_sleep()
            #     self.mix.network_wakeup()
            #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
            #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
            #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            #     time.sleep(5)
            #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
            #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
                self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
                time.sleep(1)
                self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
    
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_ALM9-Supply电压过高或过低_A0661C")
    def test_caseid_1993844(self):
        DTC_ID = [0xA0, 0x66, 0x1C]
        ccp = [{950:0x01,636:0x02,964:0x01},
               {950:0x02,636:0x02,964:0x00},
               {950:0x02,636:0x02,964:0x01}]
        for ccp_item in ccp:
            with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
                time.sleep(5)
            with allure.step('设置满足TRC'):
                self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                with allure.step(f'设置ccp:{ccp_item}'):
                    logger.info(f"设置ccp：{ccp_item}")
                    self.sd_tester.write_ccp(ccp_item)
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
                with allure.step(f"设置cem_lin5.CemCem_Lin5Fr18.ALM9FailrStsVltSts=1"):
                    logger.info(f"设置cem_lin5.CemCem_Lin5Fr18.ALM9FailrStsVltSts=1")
                    self.bus_comm.set('cem_lin5','CemCem_Lin5Fr18','ALM9FailrStsVltSts',1)
                time.sleep(1)#100ms
                TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
                data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                logger.info(f"receive DTC statusMask is {data_1[10:12]}")
                bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
                bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
                with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                    assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
                #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
            with allure.step('恢复仿真快照数据为默认值'):
                self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
            with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
                with allure.step(f"设置cem_lin5.CemCem_Lin5Fr18.ALM9FailrStsVltSts=0"):
                    logger.info(f"设置cem_lin5.CemCem_Lin5Fr18.ALM9FailrStsVltSts=0")
                    self.bus_comm.set('cem_lin5','CemCem_Lin5Fr18','ALM9FailrStsVltSts',0)
                time.sleep(1)#100ms
                data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
                logger.info(f"receive DTC statusMask is {data_2[10:12]}")
                bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
                bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
                with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                    assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
                #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
            # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
            #     self.mix.network_sleep()
            #     self.mix.network_wakeup()
            #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
            #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
            #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            #     time.sleep(5)
            #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
            #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
                self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
                time.sleep(1)
                self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
    
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_ALM9-温度太高_A0664B")
    def test_caseid_1993843(self):
        DTC_ID = [0xA0, 0x66, 0x4B]
        ccp = [{950:0x01,636:0x02,964:0x01},
               {950:0x02,636:0x02,964:0x00},
               {950:0x02,636:0x02,964:0x01}]
        for ccp_item in ccp:
            with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
                time.sleep(5)
            with allure.step('设置满足TRC'):
                self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                with allure.step(f'设置ccp:{ccp_item}'):
                    logger.info(f"设置ccp：{ccp_item}")
                    self.sd_tester.write_ccp(ccp_item)
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
                with allure.step(f"设置cem_lin5.CemCem_Lin5Fr18.ALM9FailrStsTmpSts=1"):
                    logger.info(f"设置cem_lin5.CemCem_Lin5Fr18.ALM9FailrStsTmpSts=1")
                    self.bus_comm.set('cem_lin5','CemCem_Lin5Fr18','ALM9FailrStsTmpSts',1)
                time.sleep(1)#100ms
                TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
                data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                logger.info(f"receive DTC statusMask is {data_1[10:12]}")
                bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
                bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
                with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                    assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
                #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
            with allure.step('恢复仿真快照数据为默认值'):
                self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
            with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
                with allure.step(f"设置cem_lin5.CemCem_Lin5Fr18.ALM9FailrStsTmpSts=0"):
                    logger.info(f"设置cem_lin5.CemCem_Lin5Fr18.ALM9FailrStsTmpSts=0")
                    self.bus_comm.set('cem_lin5','CemCem_Lin5Fr18','ALM9FailrStsTmpSts',0)
                time.sleep(1)#100ms
                data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
                logger.info(f"receive DTC statusMask is {data_2[10:12]}")
                bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
                bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
                with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                    assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
                #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
            # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
            #     self.mix.network_sleep()
            #     self.mix.network_wakeup()
            #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
            #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
            #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            #     time.sleep(5)
            #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
            #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
                self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
                time.sleep(1)
                self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
    
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_ALM10-RGB LED通路故障(短路或开路)_A06710")
    def test_caseid_1993842(self):
        DTC_ID = [0xA0, 0x67, 0x10]
        ccp = [{950:0x02,636:0x02,964:0x00},
               {950:0x02,636:0x02,964:0x01}]
        for ccp_item in ccp:
            with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
                time.sleep(5)
            with allure.step('设置满足TRC'):
                self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                with allure.step(f'设置ccp:{ccp_item}'):
                    logger.info(f"设置ccp：{ccp_item}")
                    self.sd_tester.write_ccp(ccp_item)
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
                with allure.step(f"设置cem_lin5.CemCem_Lin5Fr19.ALM10FailrStsLEDSts=1"):
                    logger.info(f"设置cem_lin5.CemCem_Lin5Fr19.ALM10FailrStsLEDSts=1")
                    self.bus_comm.set('cem_lin5','CemCem_Lin5Fr19','ALM10FailrStsLEDSts',1)
                time.sleep(1)#100ms
                TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
                data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                logger.info(f"receive DTC statusMask is {data_1[10:12]}")
                bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
                bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
                with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                    assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
                #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
            with allure.step('恢复仿真快照数据为默认值'):
                self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
            with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
                with allure.step(f"设置cem_lin5.CemCem_Lin5Fr19.ALM10FailrStsLEDSts=0"):
                    logger.info(f"设置cem_lin5.CemCem_Lin5Fr19.ALM10FailrStsLEDSts=0")
                    self.bus_comm.set('cem_lin5','CemCem_Lin5Fr19','ALM10FailrStsLEDSts',0)
                time.sleep(1)#100ms
                data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
                logger.info(f"receive DTC statusMask is {data_2[10:12]}")
                bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
                bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
                with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                    assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
                #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
            # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
            #     self.mix.network_sleep()
            #     self.mix.network_wakeup()
            #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
            #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
            #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            #     time.sleep(5)
            #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
            #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
                self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
                time.sleep(1)
                self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
    
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_ALM10-Supply电压过高或过低_A0671C")
    def test_caseid_1993841(self):
        DTC_ID = [0xA0, 0x67, 0x1C]
        ccp = [{950:0x02,636:0x02,964:0x00},
               {950:0x02,636:0x02,964:0x01}]
        for ccp_item in ccp:
            with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
                time.sleep(5)
            with allure.step('设置满足TRC'):
                self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                with allure.step(f'设置ccp:{ccp_item}'):
                    logger.info(f"设置ccp：{ccp_item}")
                    self.sd_tester.write_ccp(ccp_item)
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
                with allure.step(f"设置cem_lin5.CemCem_Lin5Fr19.ALM10FailrStsVltSts=1"):
                    logger.info(f"设置cem_lin5.CemCem_Lin5Fr19.ALM10FailrStsVltSts=1")
                    self.bus_comm.set('cem_lin5','CemCem_Lin5Fr19','ALM10FailrStsVltSts',1)
                time.sleep(1)#100ms
                TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
                data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                logger.info(f"receive DTC statusMask is {data_1[10:12]}")
                bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
                bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
                with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                    assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
                #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
            with allure.step('恢复仿真快照数据为默认值'):
                self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
            with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
                with allure.step(f"设置cem_lin5.CemCem_Lin5Fr19.ALM10FailrStsVltSts=0"):
                    logger.info(f"设置cem_lin5.CemCem_Lin5Fr19.ALM10FailrStsVltSts=0")
                    self.bus_comm.set('cem_lin5','CemCem_Lin5Fr19','ALM10FailrStsVltSts',0)
                time.sleep(1)#100ms
                data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
                logger.info(f"receive DTC statusMask is {data_2[10:12]}")
                bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
                bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
                with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                    assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
                #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
            # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
            #     self.mix.network_sleep()
            #     self.mix.network_wakeup()
            #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
            #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
            #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            #     time.sleep(5)
            #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
            #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
                self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
                time.sleep(1)
                self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
    
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_ALM10-温度太高_A0674B")
    def test_caseid_1993840(self):
        DTC_ID = [0xA0, 0x67, 0x4B]
        ccp = [{950:0x02,636:0x02,964:0x00},
               {950:0x02,636:0x02,964:0x01}]
        for ccp_item in ccp:
            with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
                time.sleep(5)
            with allure.step('设置满足TRC'):
                self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                with allure.step(f'设置ccp:{ccp_item}'):
                    logger.info(f"设置ccp：{ccp_item}")
                    self.sd_tester.write_ccp(ccp_item)
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
                with allure.step(f"设置cem_lin5.CemCem_Lin5Fr19.ALM10FailrStsTmpSts=1"):
                    logger.info(f"设置cem_lin5.CemCem_Lin5Fr19.ALM10FailrStsTmpSts=1")
                    self.bus_comm.set('cem_lin5','CemCem_Lin5Fr19','ALM10FailrStsTmpSts',1)
                time.sleep(1)#100ms
                TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
                data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                logger.info(f"receive DTC statusMask is {data_1[10:12]}")
                bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
                bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
                with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                    assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
                #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
            with allure.step('恢复仿真快照数据为默认值'):
                self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
            with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
                with allure.step(f"设置cem_lin5.CemCem_Lin5Fr19.ALM10FailrStsTmpSts=0"):
                    logger.info(f"设置cem_lin5.CemCem_Lin5Fr19.ALM10FailrStsTmpSts=0")
                    self.bus_comm.set('cem_lin5','CemCem_Lin5Fr19','ALM10FailrStsTmpSts',0)
                time.sleep(1)#100ms
                data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
                logger.info(f"receive DTC statusMask is {data_2[10:12]}")
                bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
                bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
                with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                    assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
                #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
            # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
            #     self.mix.network_sleep()
            #     self.mix.network_wakeup()
            #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
            #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
            #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            #     time.sleep(5)
            #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
            #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
            #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
                self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
                time.sleep(1)
                self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                    0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
    
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_OHC 第二排左内灯按钮卡滞_A07271")
    def test_caseid_1993847(self):
        DTC_ID = [0xA0, 0x72, 0x71]
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
            with allure.step(f"设置cem_lin3.OhcCem_Lin3Fr01.BtnStsOHCRLiBtnReadingLe=1"):
                logger.info(f"设置cem_lin3.OhcCem_Lin3Fr01.BtnStsOHCRLiBtnReadingLe=1")
                self.bus_comm.set('cem_lin3','OhcCem_Lin3Fr01','BtnStsOHCRLiBtnReadingLe',1)
            time.sleep(70)#60ms
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin3.OhcCem_Lin3Fr01.BtnStsOHCRLiBtnReadingLe=0"):
                logger.info(f"设置cem_lin3.OhcCem_Lin3Fr01.BtnStsOHCRLiBtnReadingLe=0")
                self.bus_comm.set('cem_lin3','OhcCem_Lin3Fr01','BtnStsOHCRLiBtnReadingLe',0)
            time.sleep(5)#2ms
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
    
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_OHC 第二排右内灯按钮卡滞_A07371")
    def test_caseid_1993846(self):
        DTC_ID = [0xA0, 0x73, 0x71]
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
            with allure.step(f"设置cem_lin3.OhcCem_Lin3Fr01.BtnStsOHCRLiBtnReadingRi=1"):
                logger.info(f"设置cem_lin3.OhcCem_Lin3Fr01.BtnStsOHCRLiBtnReadingRi=1")
                self.bus_comm.set('cem_lin3','OhcCem_Lin3Fr01','BtnStsOHCRLiBtnReadingRi',1)
            time.sleep(70)#60ms
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin3.OhcCem_Lin3Fr01.BtnStsOHCRLiBtnReadingRi=0"):
                logger.info(f"设置cem_lin3.OhcCem_Lin3Fr01.BtnStsOHCRLiBtnReadingRi=0")
                self.bus_comm.set('cem_lin3','OhcCem_Lin3Fr01','BtnStsOHCRLiBtnReadingRi',0)
            time.sleep(5)#2ms
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
    
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_OHC 左前内灯按钮卡滞_A07071")
    def test_caseid_1993849(self):
        DTC_ID = [0xA0, 0x70, 0x71]
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
            with allure.step(f"设置cem_lin3.OhcCem_Lin3Fr04.BtnStsOHCLiBtnReadingLe=1"):
                logger.info(f"设置cem_lin3.OhcCem_Lin3Fr04.BtnStsOHCLiBtnReadingLe=1")
                self.bus_comm.set('cem_lin3','OhcCem_Lin3Fr04','BtnStsOHCLiBtnReadingLe',1)
            time.sleep(75)#60s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin3.OhcCem_Lin3Fr04.BtnStsOHCLiBtnReadingLe=0"):
                logger.info(f"设置cem_lin3.OhcCem_Lin3Fr04.BtnStsOHCLiBtnReadingLe=0")
                self.bus_comm.set('cem_lin3','OhcCem_Lin3Fr04','BtnStsOHCLiBtnReadingLe',0)
            time.sleep(5)#2s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
    
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_OHC 右前内灯按钮卡滞_A07171")
    def test_caseid_1993848(self):
        DTC_ID = [0xA0, 0x71, 0x71]
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
            with allure.step(f"设置cem_lin3.OhcCem_Lin3Fr04.BtnStsOHCLiBtnReadingRi=1"):
                logger.info(f"设置cem_lin3.OhcCem_Lin3Fr04.BtnStsOHCLiBtnReadingRi=1")
                self.bus_comm.set('cem_lin3','OhcCem_Lin3Fr04','BtnStsOHCLiBtnReadingRi',1)
            time.sleep(75)#60s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            #assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin3.OhcCem_Lin3Fr04.BtnStsOHCLiBtnReadingRi=0"):
                logger.info(f"设置cem_lin3.OhcCem_Lin3Fr04.BtnStsOHCLiBtnReadingRi=0")
                self.bus_comm.set('cem_lin3','OhcCem_Lin3Fr04','BtnStsOHCLiBtnReadingRi',0)
            time.sleep(5)#2s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            #assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
        # with allure.step('BGM休眠唤醒:检查故障NVM;检查OC周期不满足无法读取DTC;检查历史故障清除成功'):
        #     self.mix.network_sleep()
        #     self.mix.network_wakeup()
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")
     
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_主驾车门开关计数器故障_94CD97")
    def test_caseid_1993994(self):
        DTC_ID = [0x94, 0xCD, 0x97]
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
            self.sd_tester.write_did_and_check(0x1002,0x40E8,SESSION.EXTENDED,UnLock.L5,'ff','6240e8ff',check_method=Check_Method.read,recover=False)
            time.sleep(2)#500ms
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
            self.sd_tester.write_did_and_check(0x1002,0x40E8,SESSION.EXTENDED,UnLock.L5,'00','6240e800',check_method=Check_Method.read,recover=False)
            time.sleep(2)#500ms
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
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x50], diagnostic_action="检查故障无法读取")
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(5)
        #     data_3 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
        #                                           0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存住历史故障")
        #     assert data_3[12:] == data_2[12:],f'dtc的历史快照信息为{data_3[12:]},快照信息与历史不符'
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除历史故障")
            time.sleep(1)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2],0x00], diagnostic_action="检查是否清除历史故障")

    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_雨刮挡位信号有误_924E49")
    def test_caseid_1993786(self):
        DTC_ID = [0x92, 0x4E, 0x49]
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

            time.sleep(5)#1000ms
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0 and bit_3 == 0, f'dtc的故障掩码为{data_1[10:12]}，故障异常报出'

    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_雨刮挡位信号CDC和BGM通讯失败_924E87")
    def test_caseid_1993787(self):
        DTC_ID = [0x92, 0x4E, 0x87]
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

            time.sleep(5)#1000ms
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0 and bit_3 == 0, f'dtc的故障掩码为{data_1[10:12]}，故障异常报出'
            
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_TLCM——TLCM输出电压ALM7 / ALM8太高_A05B17")
    def test_caseid_1993777(self):
        DTC_ID = [0xA0, 0x5B, 0x17]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:1306:0x02'):
                    logger.info(f"设置ccp：1306:0x02")
                    self.sd_tester.write_ccp({1306:0x02})
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
            with allure.step(f"设置cem_lin4.TlcmCem_Lin4Fr01.BPlusSWVoltageError=2"):
                logger.info(f"设置cem_lin4.TlcmCem_Lin4Fr01.BPlusSWVoltageError=2")
                self.bus_comm.set("cem_lin4", "TlcmCem_Lin4Fr01","BPlusSWVoltageError", 2)
                time.sleep(2)#1s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            ##assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin4.TlcmCem_Lin4Fr01.BPlusSWVoltageError=0"):
                logger.info(f"设置cem_lin4.TlcmCem_Lin4Fr01.BPlusSWVoltageError=0")
                self.bus_comm.set("cem_lin4", "TlcmCem_Lin4Fr01","BPlusSWVoltageError", 0)
            time.sleep(2)#1s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            ##assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
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
            
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_TLCM——TLCM输出电压ALM7 / ALM8太低_A05B16")
    def test_caseid_1993778(self):
        DTC_ID = [0xA0, 0x5B, 0x16]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:1306:0x02'):
                    logger.info(f"设置ccp：1306:0x02")
                    self.sd_tester.write_ccp({1306:0x02})
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
            with allure.step(f"设置cem_lin4.TlcmCem_Lin4Fr01.BPlusSWVoltageError=1"):
                logger.info(f"设置cem_lin4.TlcmCem_Lin4Fr01.BPlusSWVoltageError=1")
                self.bus_comm.set("cem_lin4", "TlcmCem_Lin4Fr01","BPlusSWVoltageError", 1)
                time.sleep(2)#1s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            ##assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin4.TlcmCem_Lin4Fr01.BPlusSWVoltageError=0"):
                logger.info(f"设置cem_lin4.TlcmCem_Lin4Fr01.BPlusSWVoltageError=0")
                self.bus_comm.set("cem_lin4", "TlcmCem_Lin4Fr01","BPlusSWVoltageError", 0)
            time.sleep(2)#1s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            ##assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
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
            
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_TLCM——TLCM电压电源电压太高_A05A17")
    def test_caseid_1993779(self):
        DTC_ID = [0xA0, 0x5A, 0x17]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:1306:0x02'):
                    logger.info(f"设置ccp：1306:0x02")
                    self.sd_tester.write_ccp({1306:0x02})
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
            with allure.step(f"设置cem_lin4.TlcmCem_Lin4Fr01.VoltageErrorTLCM=2"):
                logger.info(f"设置cem_lin4.TlcmCem_Lin4Fr01.VoltageErrorTLCM=2")
                self.bus_comm.set("cem_lin4", "TlcmCem_Lin4Fr01","VoltageErrorTLCM", 2)
                time.sleep(2)#1s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            ##assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin4.TlcmCem_Lin4Fr01.VoltageErrorTLCM=0"):
                logger.info(f"设置cem_lin4.TlcmCem_Lin4Fr01.VoltageErrorTLCM=0")
                self.bus_comm.set("cem_lin4", "TlcmCem_Lin4Fr01","VoltageErrorTLCM", 0)
            time.sleep(2)#1s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            ##assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
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
            
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_TLCM——TLCM电压电源电压太低_A05A16")
    def test_caseid_1993780(self):
        DTC_ID = [0xA0, 0x5A, 0x16]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:1306:0x02'):
                    logger.info(f"设置ccp：1306:0x02")
                    self.sd_tester.write_ccp({1306:0x02})
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
            with allure.step(f"设置cem_lin4.TlcmCem_Lin4Fr01.VoltageErrorTLCM=1"):
                logger.info(f"设置cem_lin4.TlcmCem_Lin4Fr01.VoltageErrorTLCM=1")
                self.bus_comm.set("cem_lin4", "TlcmCem_Lin4Fr01","VoltageErrorTLCM", 1)
                time.sleep(2)#1s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            ##assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin4.TlcmCem_Lin4Fr01.VoltageErrorTLCM=0"):
                logger.info(f"设置cem_lin4.TlcmCem_Lin4Fr01.VoltageErrorTLCM=0")
                self.bus_comm.set("cem_lin4", "TlcmCem_Lin4Fr01","VoltageErrorTLCM", 0)
            time.sleep(2)#1s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            ##assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
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
            
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_TLCM-温度太高_A05C4B")
    def test_caseid_1993776(self):
        DTC_ID = [0xA0, 0x5C, 0x4B]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:1306:0x02'):
                    logger.info(f"设置ccp：1306:0x02")
                    self.sd_tester.write_ccp({1306:0x02})
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
            with allure.step(f"设置cem_lin4.TlcmCem_Lin4Fr01.TempErrorTLCM=1"):
                logger.info(f"设置cem_lin4.TlcmCem_Lin4Fr01.TempErrorTLCM=1")
                self.bus_comm.set("cem_lin4", "TlcmCem_Lin4Fr01","TempErrorTLCM", 1)
                time.sleep(2)#1s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            ##assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin4.TlcmCem_Lin4Fr01.TempErrorTLCM=0"):
                logger.info(f"设置cem_lin4.TlcmCem_Lin4Fr01.TempErrorTLCM=0")
                self.bus_comm.set("cem_lin4", "TlcmCem_Lin4Fr01","TempErrorTLCM", 0)
            time.sleep(2)#1s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            ##assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
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
            
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_TLCM-RightMotor电路短路_A05910")
    def test_caseid_1993782(self):
        DTC_ID = [0xA0, 0x59, 0x10]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:1306:0x02'):
                    logger.info(f"设置ccp：1306:0x02")
                    self.sd_tester.write_ccp({1306:0x02})
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
            with allure.step(f"设置cem_lin4.TlcmCem_Lin4Fr01.RightMotorStatus=1"):
                logger.info(f"设置cem_lin4.TlcmCem_Lin4Fr01.RightMotorStatus=1")
                self.bus_comm.set("cem_lin4", "TlcmCem_Lin4Fr01","RightMotorStatus", 1)
                time.sleep(2)#1s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            ##assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin4.TlcmCem_Lin4Fr01.RightMotorStatus=0"):
                logger.info(f"设置cem_lin4.TlcmCem_Lin4Fr01.RightMotorStatus=0")
                self.bus_comm.set("cem_lin4", "TlcmCem_Lin4Fr01","RightMotorStatus", 0)
            time.sleep(2)#1s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            ##assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
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
            
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_TLCM-RightMotor电路开路_A05913")
    def test_caseid_1993781(self):
        DTC_ID = [0xA0, 0x59, 0x13]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:1306:0x02'):
                    logger.info(f"设置ccp：1306:0x02")
                    self.sd_tester.write_ccp({1306:0x02})
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
            with allure.step(f"设置cem_lin4.TlcmCem_Lin4Fr01.RightMotorStatus=2"):
                logger.info(f"设置cem_lin4.TlcmCem_Lin4Fr01.RightMotorStatus=2")
                self.bus_comm.set("cem_lin4", "TlcmCem_Lin4Fr01","RightMotorStatus", 2)
                time.sleep(2)#1s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            ##assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin4.TlcmCem_Lin4Fr01.RightMotorStatus=0"):
                logger.info(f"设置cem_lin4.TlcmCem_Lin4Fr01.RightMotorStatus=0")
                self.bus_comm.set("cem_lin4", "TlcmCem_Lin4Fr01","RightMotorStatus", 0)
            time.sleep(2)#1s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            ##assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
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
            
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_TLCM-LeftMotor电路短路_A05810")
    def test_caseid_1993784(self):
        DTC_ID = [0xA0, 0x58, 0x10]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:1306:0x02'):
                    logger.info(f"设置ccp：1306:0x02")
                    self.sd_tester.write_ccp({1306:0x02})
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
            with allure.step(f"设置cem_lin4.TlcmCem_Lin4Fr01.LeftMotorStatus=1"):
                logger.info(f"设置cem_lin4.TlcmCem_Lin4Fr01.LeftMotorStatus=1")
                self.bus_comm.set("cem_lin4", "TlcmCem_Lin4Fr01","LeftMotorStatus",1)
                time.sleep(2)#1s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            ##assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin4.TlcmCem_Lin4Fr01.LeftMotorStatus=0"):
                logger.info(f"设置cem_lin4.TlcmCem_Lin4Fr01.LeftMotorStatus=0")
                self.bus_comm.set("cem_lin4", "TlcmCem_Lin4Fr01","LeftMotorStatus", 0)
            time.sleep(2)#1s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            ##assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
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
            
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_TLCM-LeftMotor电路开路_A05813")
    def test_caseid_1993783(self):
        DTC_ID = [0xA0, 0x58, 0x13]
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(5)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            with allure.step(f'设置ccp:1306:0x02'):
                    logger.info(f"设置ccp：1306:0x02")
                    self.sd_tester.write_ccp({1306:0x02})
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
            with allure.step(f"设置cem_lin4.TlcmCem_Lin4Fr01.LeftMotorStatus=2"):
                logger.info(f"设置cem_lin4.TlcmCem_Lin4Fr01.LeftMotorStatus=2")
                self.bus_comm.set("cem_lin4", "TlcmCem_Lin4Fr01","LeftMotorStatus",2)
                time.sleep(2)#1s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            ##assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin4.TlcmCem_Lin4Fr01.LeftMotorStatus=0"):
                logger.info(f"设置cem_lin4.TlcmCem_Lin4Fr01.LeftMotorStatus=0")
                self.bus_comm.set("cem_lin4", "TlcmCem_Lin4Fr01","LeftMotorStatus", 0)
            time.sleep(2)#1s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            ##assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
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
            
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_阳光传感器组件故障组件内部故障_90BE96")
    def test_caseid_1993788(self):
        DTC_ID = [0x90, 0xBE, 0x96]
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
            with allure.step(f"设置cem_lin1.RlsmCem_Lin1Fr03.SolarSnsrErr=1"):
                logger.info(f"设置cem_lin1.RlsmCem_Lin1Fr03.SolarSnsrErr=1")
                self.bus_comm.set("cem_lin1", "RlsmCem_Lin1Fr03","SolarSnsrErr",1)
                time.sleep(2)#1s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            ##assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin1.RlsmCem_Lin1Fr03.SolarSnsrErr=0"):
                logger.info(f"设置cem_lin1.RlsmCem_Lin1Fr03.SolarSnsrErr=0")
                self.bus_comm.set("cem_lin1", "RlsmCem_Lin1Fr03","SolarSnsrErr",0)
            time.sleep(2)#1s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            ##assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
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
            
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_刮水器过载(对应BGM swr要求450162 v13)_AD3819")
    def test_caseid_1993790(self):
        DTC_ID = [0xAD, 0x38, 0x19]
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
            with allure.step(f"设置cem_lin1.WmmCem_Lin1Fr01.WiprMotDiagcWiprMotOvldDetd=2"):
                logger.info(f"设置cem_lin1.WmmCem_Lin1Fr01.WiprMotDiagcWiprMotOvldDetd=2")
                self.bus_comm.set("cem_lin1", "WmmCem_Lin1Fr01","WiprMotDiagcWiprMotOvldDetd",2)
                time.sleep(5)#3s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            ##assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin1.WmmCem_Lin1Fr01.WiprMotDiagcWiprMotOvldDetd=1"):
                logger.info(f"设置cem_lin1.WmmCem_Lin1Fr01.WiprMotDiagcWiprMotOvldDetd=1")
                self.bus_comm.set("cem_lin1", "WmmCem_Lin1Fr01","WiprMotDiagcWiprMotOvldDetd",1)
            time.sleep(5)#3s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            ##assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
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
            
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_刮水器/电压(对应BGM swr要求450162 v13)_AD3817")
    def test_caseid_1993791(self):
        DTC_ID = [0xAD, 0x38, 0x17]
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
            with allure.step(f"设置cem_lin1.WmmCem_Lin1Fr01.WiprMotDiagcWiprMotHiVoltDetd=2"):
                logger.info(f"设置cem_lin1.WmmCem_Lin1Fr01.WiprMotDiagcWiprMotHiVoltDetd=2")
                self.bus_comm.set("cem_lin1", "WmmCem_Lin1Fr01","WiprMotDiagcWiprMotHiVoltDetd",2)
                time.sleep(5)#3s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            ##assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin1.WmmCem_Lin1Fr01.WiprMotDiagcWiprMotHiVoltDetd=1"):
                logger.info(f"设置cem_lin1.WmmCem_Lin1Fr01.WiprMotDiagcWiprMotHiVoltDetd=1")
                self.bus_comm.set("cem_lin1", "WmmCem_Lin1Fr01","WiprMotDiagcWiprMotHiVoltDetd",1)
            time.sleep(5)#3s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            ##assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
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
            
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_RLSM相对湿度传感器故障(要求:477044)_970149")
    def test_caseid_1993789(self):
        DTC_ID = [0x97, 0x01, 0x49]
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
            with allure.step(f"设置cem_lin1.RlsmCem_Lin1Fr02.RelHumSnsrErr=1"):
                logger.info(f"设置cem_lin1.RlsmCem_Lin1Fr02.RelHumSnsrErr=1")
                self.bus_comm.set("cem_lin1", "RlsmCem_Lin1Fr02","RelHumSnsrErr",1)
                time.sleep(2)#825ms
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            ##assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin1.RlsmCem_Lin1Fr02.RelHumSnsrErr=0"):
                logger.info(f"设置cem_lin1.RlsmCem_Lin1Fr02.RelHumSnsrErr=0")
                self.bus_comm.set("cem_lin1", "RlsmCem_Lin1Fr02","RelHumSnsrErr",0)
            time.sleep(2)#825ms
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            ##assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
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
            
    @pytest.mark.sanity
    @allure.title("UDS_ReadDTCInformation(0x19)_胎压传感器ID未学习_924D55")
    def test_caseid_1993893(self):
        DTC_ID = [0x92, 0x4D, 0x55]
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
            self.sd_tester.write_did_and_check(0x1002,0x281F,SESSION.EXTENDED,UnLock.L5,'00000000000000000000000000000000','62281f00000000000000000000000000000000',check_method=Check_Method.read,recover=False)
            time.sleep(2)
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            ##assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            self.sd_tester.write_did_and_check(0x1002,0x281F,SESSION.EXTENDED,UnLock.L5,'027979360279c7600279c6780279c6bf','62281f027979360279c7600279c6780279c6bf',check_method=Check_Method.read,recover=False)
            time.sleep(2)
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            ##assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
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
        
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_刮水器低压(对应BGM swr要求450162 v13)_AD3816")
    def test_caseid_1993792(self):
        DTC_ID = [0xAD, 0x38, 0x16]
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
            with allure.step(f"设置cem_lin1.WmmCem_Lin1Fr01.WiprMotDiagcWiprMotLoVoltDetd=OnOffCrit1_On"):
                logger.info(f"设置cem_lin1.WmmCem_Lin1Fr01.WiprMotDiagcWiprMotLoVoltDetd=OnOffCrit1_On")
                self.bus_comm.set('cem_lin1','WmmCem_Lin1Fr01','WiprMotDiagcWiprMotLoVoltDetd', 'OnOffCrit1_On')
            time.sleep(5)#3s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            ##assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin1.WmmCem_Lin1Fr01.WiprMotDiagcWiprMotLoVoltDetd=OnOffCrit1_Off"):
                logger.info(f"设置cem_lin1.WmmCem_Lin1Fr01.WiprMotDiagcWiprMotLoVoltDetd=OnOffCrit1_Off")
                self.bus_comm.set('cem_lin1','WmmCem_Lin1Fr01','WiprMotDiagcWiprMotLoVoltDetd', 'OnOffCrit1_Off')
            time.sleep(5)#3s
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            ##assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
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
        
    @pytest.mark.full
    @allure.title("UDS_ReadDTCInformation(0x19)_刮水器低压(对应BGM swr要求450162 v13)_AD3896")
    def test_caseid_1993793(self):
        DTC_ID = [0xAD, 0x38, 0x96]
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
            with allure.step(f"设置cem_lin1.WmmCem_Lin1Fr01.WiprMotErrSafe=OnOffCrit1_On"):
                logger.info(f"设置cem_lin1.WmmCem_Lin1Fr01.WiprMotErrSafe=OnOffCrit1_On")
                self.bus_comm.set('cem_lin1','WmmCem_Lin1Fr01','WiprMotErrSafe', 'OnOffCrit1_On')
            time.sleep(5)#3s
            TIME = self.sd_tester.send_data_and_check(0x1002,0x22DD00,'62dd00',diagnostic_action="全局时间")[6:-2]
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
            logger.info(f"receive DTC statusMask is {data_1[10:12]}")
            bit_0 = (int(data_1[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_1[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_1[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 1, f'dtc的故障掩码为{data_1[10:12]}，制造故障失败'
            ##assert data_1[12:16] == '2005' and data_1[16:26] == f'dd00{TIME}'and data_1[28:] == f'dd0a{UM}dd0c0fdd0100000cdd02{Battery_Voltage}',f'dtc的当前快照信息为{data_1[12:]},快照信息错误'
        with allure.step('恢复仿真快照数据为默认值'):
            self.sd_tester.write_did_and_check(0x1002,0xDD01,SESSION.EMPTY,UnLock.L5,'00000b','62dd0100000b',check_method=Check_Method.read,recover=False)
        with allure.step('恢复当前故障;恢复快照信息;读取历史故障快照'):
            with allure.step(f"设置cem_lin1.WmmCem_Lin1Fr01.WiprMotErrSafe=OnOffCrit1_Off"):
                logger.info(f"设置cem_lin1.WmmCem_Lin1Fr01.WiprMotErrSafe=OnOffCrit1_Off")
                self.bus_comm.set('cem_lin1','WmmCem_Lin1Fr01','WiprMotErrSafe', 'OnOffCrit1_Off')
            time.sleep(5)#3
            data_2 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                  0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查是否有存历史故障")
            logger.info(f"receive DTC statusMask is {data_2[10:12]}")
            bit_0 = (int(data_2[10:12], 16) >> 0) & 0x01
            bit_3 = (int(data_2[10:12], 16) >> 3) & 0x01
            with allure.step(f"dtc的故障掩码为{data_2[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                assert bit_0 == 0, f'dtc的故障掩码为{data_2[10:12]}，不是历史故障'
            ##assert data_2[12:] == data_1[12:],f'dtc的历史快照信息为{data_2[12:]},快照信息与当前不符'
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
