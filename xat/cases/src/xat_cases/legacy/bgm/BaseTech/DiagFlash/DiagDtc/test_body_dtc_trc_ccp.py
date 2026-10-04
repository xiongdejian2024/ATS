"""
@File        : test_body_dtc_trc_ccp.py
@Author      : xiaoqiang.hu@jiduauto.com
@Time        : 2024/09/20 15:12
@Description : 车身类DTC CCP反向用例

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
    @allure.title("TRC反向_CCP_AWM-Supply电压太高_A02D17")
    def test_caseid_1994854(self):
        DTC_ID = [0xA0, 0x2D, 0x17]
        ccp_valid = [{564:0x02}]
        ccp_invalid = [{564:0x01},
                       {564:0x03}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                with allure.step('清除当前故障，恢复故障快照存储环境'):
                    self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                    time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrUFltHiVoltDetdFlt=Flt_Fault"):
                        logger.info(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrUFltHiVoltDetdFlt=Flt_Fault")
                        self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrUFltHiVoltDetdFlt', 'Flt_Fault')
                        time.sleep(1)#0.3
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
            
    @pytest.mark.full
    @allure.title("TRC反向_CCP_AWM-Supply电压太低_A02D16")
    def test_caseid_1994853(self):
        DTC_ID = [0xA0, 0x2D, 0x16]
        ccp_valid = [{564:0x02}]
        ccp_invalid = [{564:0x01},
                       {564:0x03}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                with allure.step('清除当前故障，恢复故障快照存储环境'):
                    self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                    time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrUFltLoVoltDetdFlt=Flt_Fault"):
                        logger.info(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrUFltLoVoltDetdFlt=Flt_Fault")
                        self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrUFltLoVoltDetdFlt', 'Flt_Fault')
                        time.sleep(1)#0.3
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
            
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
            
    @pytest.mark.full
    @allure.title("TRC反向_CCP_AWM-电动尾翼未学习_A02E51")
    def test_caseid_1994852(self):
        DTC_ID = [0xA0, 0x2E, 0x51]
        ccp_valid = [{564:0x02}]
        ccp_invalid = [{564:0x01},
                       {564:0x03}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                with allure.step('清除当前故障，恢复故障快照存储环境'):
                    self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                    time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin6.AwmCem_Lin6Fr01.CalStsAWM=CalStsAWM_Nocal"):
                        logger.info(f"设置cem_lin6.AwmCem_Lin6Fr01.CalStsAWM=CalStsAWM_Nocal")
                        self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','CalStsAWM', 'CalStsAWM_Nocal')
                        time.sleep(1)#0.3
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
            
    @pytest.mark.full
    @allure.title("TRC反向_CCP_AWM-输出电机-对地短路_A02E11")
    def test_caseid_1994851(self):
        DTC_ID = [0xA0, 0x2E, 0x11]
        ccp_valid = [{564:0x02}]
        ccp_invalid = [{564:0x01},
                       {564:0x03}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                with allure.step('清除当前故障，恢复故障快照存储环境'):
                    self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                    time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrIntFltActrFlt2=Flt_Fault"):
                        logger.info(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrIntFltActrFlt2=Flt_Fault")
                        self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrIntFltActrFlt2', 'Flt_Fault')
                        time.sleep(1)#0.3
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
            
    @pytest.mark.full
    @allure.title("TRC反向_CCP_AWM-输出电机-对电源短路_A02E12")
    def test_caseid_1994850(self):
        DTC_ID = [0xA0, 0x2E, 0x12]
        ccp_valid = [{564:0x02}]
        ccp_invalid = [{564:0x01},
                       {564:0x03}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                with allure.step('清除当前故障，恢复故障快照存储环境'):
                    self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                    time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrIntFltActrFlt1=Flt_Fault"):
                        logger.info(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrIntFltActrFlt1=Flt_Fault")
                        self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrIntFltActrFlt1', 'Flt_Fault')
                        time.sleep(1)#0.3
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()

    @pytest.mark.full
    @allure.title("TRC反向_CCP_AWM-输出电机-开路_A07E13")
    def test_caseid_1994849(self):
        DTC_ID = [0xA0, 0x7E, 0x13]
        ccp_valid = [{564:0x02}]
        ccp_invalid = [{564:0x01},
                       {564:0x03}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                with allure.step('清除当前故障，恢复故障快照存储环境'):
                    self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                    time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrIntFltActrFlt3=Flt_Fault"):
                        logger.info(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrIntFltActrFlt3=Flt_Fault")
                        self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrIntFltActrFlt3', 'Flt_Fault')
                        time.sleep(1)#0.3
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
            
    @pytest.mark.full
    @allure.title("TRC反向_CCP_AWM-输出电机-热保护失效_A02E4C")
    def test_caseid_1994848(self):
        DTC_ID = [0xA0, 0x2E, 0x4C]
        ccp_valid = [{564:0x02}]
        ccp_invalid = [{564:0x01},
                       {564:0x03}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                with allure.step('清除当前故障，恢复故障快照存储环境'):
                    self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                    time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrIntFltActrFlt5=Flt_Fault"):
                        logger.info(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrIntFltActrFlt5=Flt_Fault")
                        self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrIntFltActrFlt5', 'Flt_Fault')
                        time.sleep(1)#0.3
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
            
    @pytest.mark.full
    @allure.title("TRC反向_CCP_AWM-输出电机-电流过大_A02E19")
    def test_caseid_1994847(self):
        DTC_ID = [0xA0, 0x2E, 0x19]
        ccp_valid = [{564:0x02}]
        ccp_invalid = [{564:0x01},
                       {564:0x03}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                with allure.step('清除当前故障，恢复故障快照存储环境'):
                    self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                    time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrIntFltActrFlt4=Flt_Fault"):
                        logger.info(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrIntFltActrFlt4=Flt_Fault")
                        self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrIntFltActrFlt4', 'Flt_Fault')
                        time.sleep(1)#0.3
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
            
    @pytest.mark.full
    @allure.title("TRC反向_CCP_AWM-霍尔传感器对地短路_A07D11")
    def test_caseid_1994846(self):
        DTC_ID = [0xA0, 0x7D, 0x11]
        ccp_valid = [{564:0x02}]
        ccp_invalid = [{564:0x01},
                       {564:0x03}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                with allure.step('清除当前故障，恢复故障快照存储环境'):
                    self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                    time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrHallSnsrFltHallOutpFlt=Flt_Fault"):
                        logger.info(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrHallSnsrFltHallOutpFlt=Flt_Fault")
                        self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrHallSnsrFltHallOutpFlt', 'Flt_Fault')
                        time.sleep(1)#0.3
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
            
    @pytest.mark.full
    @allure.title("TRC反向_CCP_AWM的A霍尔传感器-传感器故障_A02D7C")
    def test_caseid_1994845(self):
        DTC_ID = [0xA0, 0x2D, 0x7C]
        ccp_valid = [{564:0x02}]
        ccp_invalid = [{564:0x01},
                       {564:0x03}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrHallSnsrFltHallAFlt=Flt_Fault"):
                        logger.info(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrHallSnsrFltHallAFlt=Flt_Fault")
                        self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrHallSnsrFltHallAFlt', 'Flt_Fault')
                        time.sleep(1)#0.3
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
            
    @pytest.mark.full
    @allure.title("TRC反向_CCP_AWM的B霍尔传感器-传感器故障_A02D7D")
    def test_caseid_1994844(self):
        DTC_ID = [0xA0, 0x2D, 0x7D]
        ccp_valid = [{564:0x02}]
        ccp_invalid = [{564:0x01},
                       {564:0x03}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrHallSnsrFltHallBFlt=Flt_Fault"):
                        logger.info(f"设置cem_lin6.AwmCem_Lin6Fr01.ActvReSplrHallSnsrFltHallBFlt=Flt_Fault")
                        self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrHallSnsrFltHallBFlt', 'Flt_Fault')
                        time.sleep(1)#0.3
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
                    
    @pytest.mark.full
    @allure.title("TRC反向_CCP_DSGL-LED 故障（短路或开路）_A03414")
    def test_caseid_1994843(self):
        DTC_ID = [0xA0, 0x34, 0x14]
        ccp_valid = [{1532:0x02}]
        ccp_invalid = [{1532:0x01},
                       {1532:0x03}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin3.DsglCem_Lin3Fr01.DSGLIntFltLEDsFlt=Flt_Fault"):
                        logger.info(f"设置cem_lin3.DsglCem_Lin3Fr01.DSGLIntFltLEDsFlt=Flt_Fault")
                        self.bus_comm.set('cem_lin3','DsglCem_Lin3Fr01','DSGLIntFltLEDsFlt', 'Flt_Fault')
                        time.sleep(1.2)#0.8
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
            
    @pytest.mark.full
    @allure.title("TRC反向_CCP_DSGL-Supply电压太低_A03416")
    def test_caseid_1994842(self):
        DTC_ID = [0xA0, 0x34, 0x16]
        ccp_valid = [{1532:0x02}]
        ccp_invalid = [{1532:0x01},
                       {1532:0x03}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin3.DsglCem_Lin3Fr01.DSGLIntFltLoVoltDetdFlt=Flt_Fault"):
                        logger.info(f"设置cem_lin3.DsglCem_Lin3Fr01.DSGLIntFltLoVoltDetdFlt=Flt_Fault")
                        self.bus_comm.set('cem_lin3','DsglCem_Lin3Fr01','DSGLIntFltLoVoltDetdFlt', 'Flt_Fault')
                        time.sleep(1.2)#0.8
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
            
    @pytest.mark.full
    @allure.title("TRC反向_CCP_DSGL-Supply电压太高_A03417")
    def test_caseid_1994841(self):
        DTC_ID = [0xA0, 0x34, 0x17]
        ccp_valid = [{1532:0x02}]
        ccp_invalid = [{1532:0x01},
                       {1532:0x03}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin3.DsglCem_Lin3Fr01.DSGLIntFltHiVoltDetdFlt=Flt_Fault"):
                        logger.info(f"设置cem_lin3.DsglCem_Lin3Fr01.DSGLIntFltHiVoltDetdFlt=Flt_Fault")
                        self.bus_comm.set('cem_lin3','DsglCem_Lin3Fr01','DSGLIntFltHiVoltDetdFlt', 'Flt_Fault')
                        time.sleep(1.2)#0.8
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
            
    @pytest.mark.full
    @allure.title("TRC反向_CCP_DSGL-温度太高_A0344B")
    def test_caseid_1994840(self):
        DTC_ID = [0xA0, 0x34, 0x4B]
        ccp_valid = [{1532:0x02}]
        ccp_invalid = [{1532:0x01},
                       {1532:0x03}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin3.DsglCem_Lin3Fr01.DSGLIntFltTpmFlt=Flt_Fault"):
                        logger.info(f"设置cem_lin3.DsglCem_Lin3Fr01.DSGLIntFltTpmFlt=Flt_Fault")
                        self.bus_comm.set('cem_lin3','DsglCem_Lin3Fr01','DSGLIntFltTpmFlt', 'Flt_Fault')
                        time.sleep(1.2)#0.8
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
            
    @pytest.mark.full
    @allure.title("TRC反向_CCP_FCSI 低电压_A03716")
    def test_caseid_1994839(self):
        DTC_ID = [0xA0, 0x37, 0x16]
        ccp_valid = [{1530:0x02,567:0x03}]
        ccp_invalid = [{1530:0x01,567:0x03},
                       {1530:0x03,567:0x03},
                       {1530:0x02,567:0x02},
                       {1530:0x02,567:0x04}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin2.FcsiEcm_Lin4Fr01.FCSIPwrSplyLo=OnOff1_On"):
                        logger.info(f"设置cem_lin2.FcsiEcm_Lin4Fr01.FCSIPwrSplyLo=OnOff1_On")
                        self.bus_comm.set('cem_lin2','FcsiEcm_Lin4Fr01','FCSIPwrSplyLo', 'OnOff1_On')
                        time.sleep(1)#0.5
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
            
    @pytest.mark.full
    @allure.title("TRC反向_CCP_FCSI 过电压_A03717")
    def test_caseid_1994838(self):
        DTC_ID = [0xA0, 0x37, 0x17]
        ccp_valid = [{1530:0x02,567:0x03}]
        ccp_invalid = [{1530:0x01,567:0x03},
                       {1530:0x03,567:0x03},
                       {1530:0x02,567:0x02},
                       {1530:0x02,567:0x04}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin2.FcsiEcm_Lin4Fr01.FCSIPwrSplyHi=OnOff1_On"):
                        logger.info(f"设置cem_lin2.FcsiEcm_Lin4Fr01.FCSIPwrSplyHi=OnOff1_On")
                        self.bus_comm.set('cem_lin2','FcsiEcm_Lin4Fr01','FCSIPwrSplyHi', 'OnOff1_On')
                        time.sleep(1)#0.5
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
            
    @pytest.mark.full
    @allure.title("TRC反向_CCP_FCSI充电指示灯电路对地短_A03711")
    def test_caseid_1994837(self):
        DTC_ID = [0xA0, 0x37, 0x11]
        ccp_valid = [{1530:0x02,567:0x03}]
        ccp_invalid = [{1530:0x01,567:0x03},
                       {1530:0x03,567:0x03},
                       {1530:0x02,567:0x02},
                       {1530:0x02,567:0x04}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin2.FcsiEcm_Lin4Fr01.FCSIShoCirc=OnOff1_On"):
                        logger.info(f"设置cem_lin2.FcsiEcm_Lin4Fr01.FCSIShoCirc=OnOff1_On")
                        self.bus_comm.set('cem_lin2','FcsiEcm_Lin4Fr01','FCSIShoCirc', 'OnOff1_On')
                        time.sleep(1)#0.5
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
            
    @pytest.mark.full
    @allure.title("TRC反向_CCP_FCSI充电指示灯电路开路_A03713")
    def test_caseid_1994836(self):
        DTC_ID = [0xA0, 0x37, 0x13]
        ccp_valid = [{1530:0x02,567:0x03}]
        ccp_invalid = [{1530:0x01,567:0x03},
                       {1530:0x03,567:0x03},
                       {1530:0x02,567:0x02},
                       {1530:0x02,567:0x04}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin2.FcsiEcm_Lin4Fr01.FCSIOpenCirc=OnOff1_On"):
                        logger.info(f"设置cem_lin2.FcsiEcm_Lin4Fr01.FCSIOpenCirc=OnOff1_On")
                        self.bus_comm.set('cem_lin2','FcsiEcm_Lin4Fr01','FCSIOpenCirc', 'OnOff1_On')
                        time.sleep(1)#0.5
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
      
    @pytest.mark.full
    @allure.title("TRC反向_CCP_PSGL-LED 故障（短路或开路）_A03514")
    def test_caseid_1994830(self):
        DTC_ID = [0xA0, 0x35, 0x14]
        ccp_valid = [{1531:0x02}]
        ccp_invalid = [{1531:0x01},
                       {1531:0x03}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin3.PsglCem_Lin3Fr01.PSGLIntFltLEDsFlt=Flt_Fault"):
                        logger.info(f"设置cem_lin3.PsglCem_Lin3Fr01.PSGLIntFltLEDsFlt=Flt_Fault")
                        self.bus_comm.set('cem_lin3','PsglCem_Lin3Fr01','PSGLIntFltLEDsFlt', 'Flt_Fault')
                        time.sleep(1.2)#0.8
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
            
    @pytest.mark.full
    @allure.title("TRC反向_CCP_PSGL-Supply电压太低_A03516")
    def test_caseid_1994829(self):
        DTC_ID = [0xA0, 0x35, 0x16]
        ccp_valid = [{1531:0x02}]
        ccp_invalid = [{1531:0x01},
                       {1531:0x03}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin3.PsglCem_Lin3Fr01.PSGLIntFltLoVoltDetdFlt=Flt_Fault"):
                        logger.info(f"设置cem_lin3.PsglCem_Lin3Fr01.PSGLIntFltLoVoltDetdFlt=Flt_Fault")
                        self.bus_comm.set('cem_lin3','PsglCem_Lin3Fr01','PSGLIntFltLoVoltDetdFlt', 'Flt_Fault')
                        time.sleep(1.2)#0.8
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
            
    @pytest.mark.full
    @allure.title("TRC反向_CCP_PSGL-Supply电压太高_A03517")
    def test_caseid_1994828(self):
        DTC_ID = [0xA0, 0x35, 0x17]
        ccp_valid = [{1531:0x02}]
        ccp_invalid = [{1531:0x01},
                       {1531:0x03}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin3.PsglCem_Lin3Fr01.PSGLIntFltHiVoltDetdFlt=Flt_Fault"):
                        logger.info(f"设置cem_lin3.PsglCem_Lin3Fr01.PSGLIntFltHiVoltDetdFlt=Flt_Fault")
                        self.bus_comm.set('cem_lin3','PsglCem_Lin3Fr01','PSGLIntFltHiVoltDetdFlt', 'Flt_Fault')
                        time.sleep(1.2)#0.8
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
            
    @pytest.mark.full
    @allure.title("TRC反向_CCP_PSGL-温度太高_A0354B")
    def test_caseid_1994827(self):
        DTC_ID = [0xA0, 0x35, 0x4B]
        ccp_valid = [{1531:0x02}]
        ccp_invalid = [{1531:0x01},
                       {1531:0x03}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin3.PsglCem_Lin3Fr01.PSGLIntFltTpmFlt=Flt_Fault"):
                        logger.info(f"设置cem_lin3.PsglCem_Lin3Fr01.PSGLIntFltTpmFlt=Flt_Fault")
                        self.bus_comm.set('cem_lin3','PsglCem_Lin3Fr01','PSGLIntFltTpmFlt', 'Flt_Fault')
                        time.sleep(1.2)#0.8
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
    
    @pytest.mark.full
    @allure.title("TRC反向_CCP_ALM7-RGB LED通路故障(短路或开路)_A04610")
    def test_caseid_1994863(self):
        DTC_ID = [0xA0, 0x46, 0x10]
        ccp_valid = [{950:0x02,636:0x02,964:0x00}]
        ccp_invalid = [{950:0x02,636:0x03,964:0x00},
                       {950:0x02,636:0x02,964:0x02}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin5.CemCem_Lin5Fr16.ALM7FailrStsLEDSts=1"):
                        logger.info(f"设置cem_lin5.CemCem_Lin5Fr16.ALM7FailrStsLEDSts=1")
                        self.bus_comm.set('cem_lin5','CemCem_Lin5Fr16','ALM7FailrStsLEDSts',1)
                        time.sleep(1)#100ms
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
    
    @pytest.mark.full
    @allure.title("TRC反向_CCP_ALM7-Supply电压过高或过低_A0461C")
    def test_caseid_1994862(self):
        DTC_ID = [0xA0, 0x46, 0x1C]
        ccp_valid = [{950:0x02,636:0x02,964:0x00}]
        ccp_invalid = [{950:0x02,636:0x03,964:0x00},
                       {950:0x02,636:0x02,964:0x02}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin5.CemCem_Lin5Fr16.ALM7FailrStsVltSts=1"):
                        logger.info(f"设置cem_lin5.CemCem_Lin5Fr16.ALM7FailrStsVltSts=1")
                        self.bus_comm.set('cem_lin5','CemCem_Lin5Fr16','ALM7FailrStsVltSts',1)
                        time.sleep(1)#100ms
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
    
    @pytest.mark.full
    @allure.title("TRC反向_CCP_ALM7-温度太高_A0464B")
    def test_caseid_1994861(self):
        DTC_ID = [0xA0, 0x46, 0x4B]
        ccp_valid = [{950:0x02,636:0x02,964:0x00}]
        ccp_invalid = [{950:0x02,636:0x03,964:0x00},
                       {950:0x02,636:0x02,964:0x02}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin5.CemCem_Lin5Fr16.ALM7FailrStsTmpSts=1"):
                        logger.info(f"设置cem_lin5.CemCem_Lin5Fr16.ALM7FailrStsTmpSts=1")
                        self.bus_comm.set('cem_lin5','CemCem_Lin5Fr16','ALM7FailrStsTmpSts',1)
                        time.sleep(1)#100ms
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
    
    @pytest.mark.full
    @allure.title("TRC反向_CCP_ALM8-RGB LED通路故障(短路或开路)_A04710")
    def test_caseid_1994860(self):
        DTC_ID = [0xA0, 0x47, 0x10]
        ccp_valid = [{950:0x02,636:0x02,964:0x00}]
        ccp_invalid = [{950:0x02,636:0x03,964:0x00},
                       {950:0x02,636:0x02,964:0x02},
                       {950:0x01,636:0x01,964:0x00},
                       {950:0x01,636:0x02,964:0x02}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin5.CemCem_Lin5Fr17.ALM8FailrStsLEDSts=1"):
                        logger.info(f"设置cem_lin5.CemCem_Lin5Fr17.ALM8FailrStsLEDSts=1")
                        self.bus_comm.set('cem_lin5','CemCem_Lin5Fr17','ALM8FailrStsLEDSts',1)
                        time.sleep(1)#100ms
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
    
    @pytest.mark.full
    @allure.title("TRC反向_CCP_ALM8-Supply电压过高或过低_A0471C")
    def test_caseid_1994859(self):
        DTC_ID = [0xA0, 0x47, 0x1C]
        ccp_valid = [{950:0x02,636:0x02,964:0x00}]
        ccp_invalid = [{950:0x02,636:0x03,964:0x00},
                       {950:0x02,636:0x02,964:0x02},
                       {950:0x01,636:0x01,964:0x00},
                       {950:0x01,636:0x02,964:0x02}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin5.CemCem_Lin5Fr17.ALM8FailrStsVltSts=1"):
                        logger.info(f"设置cem_lin5.CemCem_Lin5Fr17.ALM8FailrStsVltSts=1")
                        self.bus_comm.set('cem_lin5','CemCem_Lin5Fr17','ALM8FailrStsVltSts',1)
                        time.sleep(1)#100ms
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
    
    @pytest.mark.full
    @allure.title("TRC反向_CCP_ALM8-温度太高_A0474B")
    def test_caseid_1994858(self):
        DTC_ID = [0xA0, 0x47, 0x4B]
        ccp_valid = [{950:0x02,636:0x02,964:0x00}]
        ccp_invalid = [{950:0x02,636:0x03,964:0x00},
                       {950:0x02,636:0x02,964:0x02},
                       {950:0x01,636:0x01,964:0x00},
                       {950:0x01,636:0x02,964:0x02}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin5.CemCem_Lin5Fr17.ALM8FailrStsTmpSts=1"):
                        logger.info(f"设置cem_lin5.CemCem_Lin5Fr17.ALM8FailrStsTmpSts=1")
                        self.bus_comm.set('cem_lin5','CemCem_Lin5Fr17','ALM8FailrStsTmpSts',1)
                        time.sleep(1)#100ms
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()

    @pytest.mark.full
    @allure.title("TRC反向_CCP_ALM9-RGB LED通路故障(短路或开路)_A06610")
    def test_caseid_1994857(self):
        DTC_ID = [0xA0, 0x66, 0x10]
        ccp_valid = [{950:0x02,636:0x02,964:0x00}]
        ccp_invalid = [{950:0x02,636:0x01,964:0x00},
                       {950:0x02,636:0x02,964:0x02},
                       {950:0x01,636:0x01,964:0x01},
                       {950:0x01,636:0x03,964:0x01},
                       {950:0x01,636:0x02,964:0x02},
                       {950:0x01,636:0x02,964:0x03}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin5.CemCem_Lin5Fr18.ALM9FailrStsLEDSts=1"):
                        logger.info(f"设置cem_lin5.CemCem_Lin5Fr18.ALM9FailrStsLEDSts=1")
                        self.bus_comm.set('cem_lin5','CemCem_Lin5Fr18','ALM9FailrStsLEDSts',1)
                        time.sleep(1)#100ms
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
    
    @pytest.mark.full
    @allure.title("TRC反向_CCP_ALM9-Supply电压过高或过低_A0661C")
    def test_caseid_1994856(self):
        DTC_ID = [0xA0, 0x66, 0x1C]
        ccp_valid = [{950:0x02,636:0x02,964:0x00}]
        ccp_invalid = [{950:0x02,636:0x01,964:0x00},
                       {950:0x02,636:0x02,964:0x02},
                       {950:0x01,636:0x01,964:0x01},
                       {950:0x01,636:0x03,964:0x01},
                       {950:0x01,636:0x02,964:0x02},
                       {950:0x01,636:0x02,964:0x03}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin5.CemCem_Lin5Fr18.ALM9FailrStsVltSts=1"):
                        logger.info(f"设置cem_lin5.CemCem_Lin5Fr18.ALM9FailrStsVltSts=1")
                        self.bus_comm.set('cem_lin5','CemCem_Lin5Fr18','ALM9FailrStsVltSts',1)
                        time.sleep(1)#100ms
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
    
    @pytest.mark.full
    @allure.title("TRC反向_CCP_ALM9-温度太高_A0664B")
    def test_caseid_1994855(self):
        DTC_ID = [0xA0, 0x66, 0x4B]
        ccp_valid = [{950:0x02,636:0x02,964:0x00}]
        ccp_invalid = [{950:0x02,636:0x01,964:0x00},
                       {950:0x02,636:0x02,964:0x02},
                       {950:0x01,636:0x01,964:0x01},
                       {950:0x01,636:0x03,964:0x01},
                       {950:0x01,636:0x02,964:0x02},
                       {950:0x01,636:0x02,964:0x03}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin5.CemCem_Lin5Fr18.ALM9FailrStsTmpSts=1"):
                        logger.info(f"设置cem_lin5.CemCem_Lin5Fr18.ALM9FailrStsTmpSts=1")
                        self.bus_comm.set('cem_lin5','CemCem_Lin5Fr18','ALM9FailrStsTmpSts',1)
                        time.sleep(1)#100ms
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
    
    @pytest.mark.full
    @allure.title("TRC反向_CCP_ALM10-RGB LED通路故障(短路或开路)_A06710")
    def test_caseid_1994866(self):
        DTC_ID = [0xA0, 0x67, 0x10]
        ccp_valid = [{950:0x02,636:0x02,964:0x00}]
        ccp_invalid = [{950:0x02,636:0x01,964:0x00},
                       {950:0x02,636:0x03,964:0x00},
                       {950:0x02,636:0x02,964:0x02}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin5.CemCem_Lin5Fr19.ALM10FailrStsLEDSts=1"):
                        logger.info(f"设置cem_lin5.CemCem_Lin5Fr19.ALM10FailrStsLEDSts=1")
                        self.bus_comm.set('cem_lin5','CemCem_Lin5Fr19','ALM10FailrStsLEDSts',1)
                        time.sleep(1)#100ms
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
    
    @pytest.mark.full
    @allure.title("TRC反向_CCP_ALM10-Supply电压过高或过低_A0671C")
    def test_caseid_1994865(self):
        DTC_ID = [0xA0, 0x67, 0x1C]
        ccp_valid = [{950:0x02,636:0x02,964:0x00}]
        ccp_invalid = [{950:0x02,636:0x01,964:0x00},
                       {950:0x02,636:0x03,964:0x00},
                       {950:0x02,636:0x02,964:0x02}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin5.CemCem_Lin5Fr19.ALM10FailrStsVltSts=1"):
                        logger.info(f"设置cem_lin5.CemCem_Lin5Fr19.ALM10FailrStsVltSts=1")
                        self.bus_comm.set('cem_lin5','CemCem_Lin5Fr19','ALM10FailrStsVltSts',1)
                        time.sleep(1)#100ms
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
    
    @pytest.mark.full
    @allure.title("TRC反向_CCP_ALM10-温度太高_A0674B")
    def test_caseid_1994864(self):
        DTC_ID = [0xA0, 0x67, 0x4B]
        ccp_valid = [{950:0x02,636:0x02,964:0x00}]
        ccp_invalid = [{950:0x02,636:0x01,964:0x00},
                       {950:0x02,636:0x03,964:0x00},
                       {950:0x02,636:0x02,964:0x02}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin5.CemCem_Lin5Fr19.ALM10FailrStsTmpSts=1"):
                        logger.info(f"设置cem_lin5.CemCem_Lin5Fr19.ALM10FailrStsTmpSts=1")
                        self.bus_comm.set('cem_lin5','CemCem_Lin5Fr19','ALM10FailrStsTmpSts',1)
                        time.sleep(1)#100ms
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
            
    @pytest.mark.full
    @allure.title("TRC反向_CCP_HOD故障_A06596")
    def test_caseid_1994831(self):
        DTC_ID = [0xA0, 0x65, 0x96]
        ccp_valid = [{1550:0x02}]
        ccp_invalid = [{1550:0x01},
                       {1550:0x03}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin4.HodDim_Lin1Fr04.HandsOnDetectionErrorStatus=3"):
                        logger.info(f"设置cem_lin4.HodDim_Lin1Fr04.HandsOnDetectionErrorStatus=3")
                        self.bus_comm.set("cem_lin4", "HodDim_Lin1Fr04","HandsOnDetectionErrorStatus", 3)
                        time.sleep(2)#500ms
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
            
    @pytest.mark.full
    @allure.title("TRC反向_CCP_TLCM——TLCM输出电压ALM7 / ALM8太高_A05B17")
    def test_caseid_1994818(self):
        DTC_ID = [0xA0, 0x5B, 0x17]
        ccp_valid = [{1306:0x02}]
        ccp_invalid = [{1306:0x01},
                       {1306:0x03}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin4.TlcmCem_Lin4Fr01.BPlusSWVoltageError=2"):
                        logger.info(f"设置cem_lin4.TlcmCem_Lin4Fr01.BPlusSWVoltageError=2")
                        self.bus_comm.set("cem_lin4", "TlcmCem_Lin4Fr01","BPlusSWVoltageError", 2)
                        time.sleep(2)#1s
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
            
    @pytest.mark.full
    @allure.title("TRC反向_CCP_TLCM——TLCM输出电压ALM7 / ALM8太低_A05B16")
    def test_caseid_1994819(self):
        DTC_ID = [0xA0, 0x5B, 0x16]
        ccp_valid = [{1306:0x02}]
        ccp_invalid = [{1306:0x01},
                       {1306:0x03}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin4.TlcmCem_Lin4Fr01.BPlusSWVoltageError=1"):
                        logger.info(f"设置cem_lin4.TlcmCem_Lin4Fr01.BPlusSWVoltageError=1")
                        self.bus_comm.set("cem_lin4", "TlcmCem_Lin4Fr01","BPlusSWVoltageError", 1)
                        time.sleep(2)#1s
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
            
    @pytest.mark.full
    @allure.title("TRC反向_CCP_TLCM——TLCM电压电源电压太高_A05A17")
    def test_caseid_1994820(self):
        DTC_ID = [0xA0, 0x5A, 0x17]
        ccp_valid = [{1306:0x02}]
        ccp_invalid = [{1306:0x01},
                       {1306:0x03}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin4.TlcmCem_Lin4Fr01.VoltageErrorTLCM=2"):
                        logger.info(f"设置cem_lin4.TlcmCem_Lin4Fr01.VoltageErrorTLCM=2")
                        self.bus_comm.set("cem_lin4", "TlcmCem_Lin4Fr01","VoltageErrorTLCM", 2)
                        time.sleep(2)#1s
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
            
    @pytest.mark.full
    @allure.title("TRC反向_CCP_TLCM——TLCM电压电源电压太低_A05A16")
    def test_caseid_1994821(self):
        DTC_ID = [0xA0, 0x5A, 0x16]
        ccp_valid = [{1306:0x02}]
        ccp_invalid = [{1306:0x01},
                       {1306:0x03}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin4.TlcmCem_Lin4Fr01.VoltageErrorTLCM=1"):
                        logger.info(f"设置cem_lin4.TlcmCem_Lin4Fr01.VoltageErrorTLCM=1")
                        self.bus_comm.set("cem_lin4", "TlcmCem_Lin4Fr01","VoltageErrorTLCM", 1)
                        time.sleep(2)#1s
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
            
    @pytest.mark.full
    @allure.title("TRC反向_CCP_TLCM-温度太高_A05C4B")
    def test_caseid_1994822(self):
        DTC_ID = [0xA0, 0x5C, 0x4B]
        ccp_valid = [{1306:0x02}]
        ccp_invalid = [{1306:0x01},
                       {1306:0x03}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin4.TlcmCem_Lin4Fr01.TempErrorTLCM=1"):
                        logger.info(f"设置cem_lin4.TlcmCem_Lin4Fr01.TempErrorTLCM=1")
                        self.bus_comm.set("cem_lin4", "TlcmCem_Lin4Fr01","TempErrorTLCM", 1)
                        time.sleep(2)#1s
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
            
    @pytest.mark.full
    @allure.title("TRC反向_CCP_TLCM-RightMotor电路短路_A05910")
    def test_caseid_1994823(self):
        DTC_ID = [0xA0, 0x59, 0x10]
        ccp_valid = [{1306:0x02}]
        ccp_invalid = [{1306:0x01},
                       {1306:0x03}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin4.TlcmCem_Lin4Fr01.RightMotorStatus=1"):
                        logger.info(f"设置cem_lin4.TlcmCem_Lin4Fr01.RightMotorStatus=1")
                        self.bus_comm.set("cem_lin4", "TlcmCem_Lin4Fr01","RightMotorStatus", 1)
                        time.sleep(2)#1s
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
            
    @pytest.mark.full
    @allure.title("TRC反向_CCP_TLCM-RightMotor电路开路_A05913")
    def test_caseid_1994824(self):
        DTC_ID = [0xA0, 0x59, 0x13]
        ccp_valid = [{1306:0x02}]
        ccp_invalid = [{1306:0x01},
                       {1306:0x03}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin4.TlcmCem_Lin4Fr01.RightMotorStatus=2"):
                        logger.info(f"设置cem_lin4.TlcmCem_Lin4Fr01.RightMotorStatus=2")
                        self.bus_comm.set("cem_lin4", "TlcmCem_Lin4Fr01","RightMotorStatus", 2)
                        time.sleep(2)#1s
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
            
    @pytest.mark.full
    @allure.title("TRC反向_CCP_TLCM-LeftMotor电路短路_A05810")
    def test_caseid_1994825(self):
        DTC_ID = [0xA0, 0x58, 0x10]
        ccp_valid = [{1306:0x02}]
        ccp_invalid = [{1306:0x01},
                       {1306:0x03}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin4.TlcmCem_Lin4Fr01.LeftMotorStatus=1"):
                        logger.info(f"设置cem_lin4.TlcmCem_Lin4Fr01.LeftMotorStatus=1")
                        self.bus_comm.set("cem_lin4", "TlcmCem_Lin4Fr01","LeftMotorStatus",1)
                        time.sleep(2)#1s
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
            
    @pytest.mark.full
    @allure.title("TRC反向_CCP_TLCM-LeftMotor电路开路_A05813")
    def test_caseid_1994826(self):
        DTC_ID = [0xA0, 0x58, 0x13]
        ccp_valid = [{1306:0x02}]
        ccp_invalid = [{1306:0x01},
                       {1306:0x03}]
        for ccp_invalid_item in ccp_invalid:
            with allure.step('设置CCP不满足TRC或CCP无效值'):
                with allure.step(f'设置ccp:{ccp_invalid_item}'):
                    logger.info(f"设置ccp：{ccp_invalid_item}")
                    self.sd_tester.write_ccp(ccp_invalid_item)
                    time.sleep(3)
                with allure.step(f'ccp写入成功后重启bgm'):
                    self.sd_tester.reset_bgm()
                with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
                    self.sd_tester.change_usage_mode(UsageMode.DRIVING)
                    self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
                    time.sleep(5)
                # with allure.step('清除当前故障，恢复故障快照存储环境'):
                #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
                #     time.sleep(2)
                with allure.step('制造当前故障;读取当前故障快照'):
                    with allure.step(f"设置cem_lin4.TlcmCem_Lin4Fr01.LeftMotorStatus=2"):
                        logger.info(f"设置cem_lin4.TlcmCem_Lin4Fr01.LeftMotorStatus=2")
                        self.bus_comm.set("cem_lin4", "TlcmCem_Lin4Fr01","LeftMotorStatus",2)
                        time.sleep(2)#1s
                    data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2], 0x20], [
                                                        0x59, 0x04, DTC_ID[0], DTC_ID[1], DTC_ID[2]], diagnostic_action="检查故障是否制造成功")
                    logger.info(f"receive DTC statusMask is {data[10:12]}")
                    bit_0 = (int(data[10:12], 16) >> 0) & 0x01
                    bit_3 = (int(data[10:12], 16) >> 3) & 0x01
                    with allure.step(f"dtc的故障掩码为{data[10:12].upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
                        assert bit_0 != 1 and bit_3 != 1, f'dtc的故障掩码为{data[10:12]}，制造故障失败'
        
        with allure.step('设置CCP为满足TRC的默认值'):
            with allure.step(f'设置ccp:{ccp_valid[0]}'):
                    logger.info(f"设置ccp：{ccp_valid[0]}")
                    self.sd_tester.write_ccp(ccp_valid[0])
                    time.sleep(3)
            with allure.step(f'ccp写入成功后重启bgm'):
                self.sd_tester.reset_bgm()
    
            
