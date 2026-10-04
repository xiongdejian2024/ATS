"""
@File        : test_trc_comunicate_chassis_ccp_notmet.py
@Author      : O_jingyuan.chen@external.jiduauto.com
@Time        : 2024/09/12
@Description : 通用类DTC_TRC不满足+通讯类DTC&底盘类DTC_CCP不满足

"""
import pytest
import allure
from xat_cases.legacy.bgm.mcu.case_helper.test_abc_base import TestABCBase 
from xat_ecu.api.common.common import *

@allure.feature("BGM BaseTech/诊断刷写/诊断DTC/TRC反向")
@allure.story("通用类")
class Test_TRC(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update(["VehicleModeService_client"])
        # self.ccp=self.sd_tester.sd_tester.make_ccp_according_id_and_data('1','A3')
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        # self.sd_tester.write_did_and_check(TA.BGM_MCU,0xf106,SESSION.EXTENDED,UnLock.L5,f'{self.ccp}','6ef106',check_method=Check_Method.response,recover=False)
        self.bus_comm.set('backbonefr','BcmVddmBackBoneFr00','VehMtnStVehMtnSt','VehMtnSt2_StandStillVal3')
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.bus_comm.resume_all_bus_send()
        self.bus_comm.set('backbonefr','BcmVddmBackBoneFr00','VehMtnStVehMtnSt','VehMtnSt2_StandStillVal3')
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)    

    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.ccp=self.sd_tester.sd_tester.make_ccp_according_id_and_data('1','A3')
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xf106,SESSION.EXTENDED,UnLock.L5,f'{self.ccp}','6ef106',check_method=Check_Method.response,recover=False)

    @pytest.mark.full
    @allure.title('TRC反向_PwrLvlElec.LvlElecMai不满足_不等于0_通用类1')
    def test_caseid_1994755(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==DRIVING'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            time.sleep(7)
        with allure.step('制造当前故障'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.bus_comm.set('cem_lin2','PrldCem_Lin2Fr02','ChrgLidManvgDCorAcDcUnderVoltFb', 'Boolean_TRUE')
            time.sleep(1)#0.5
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xA0, 0x36, 0x16, 0x20], [
                                                  0x59, 0x04, 0xA0, 0x36, 0x16,0x50], diagnostic_action="检查故障是否制造成功")

    @pytest.mark.full
    @allure.title('TRC反向_Car mode不满足_ Factory or Transport or Crash or Dynamometer_通用类1')
    def test_caseid_1994754(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==ACTIVE'):
            self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
            time.sleep(7)
        with allure.step('设置TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('制造当前故障'):
            self.mix.s2s_change_car_mode_and_check_result(CarMode.FACTORY,car_mode_sub=0) 
            time.sleep(7)
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.bus_comm.set('cem_lin2','PrldCem_Lin2Fr02','ChrgLidManvgDCorAcDcUnderVoltFb', 'Boolean_TRUE')
            time.sleep(1)#0.5
            data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xA0, 0x36, 0x16, 0x20], [
                                                0x59, 0x04, 0xA0, 0x36, 0x16,0x50], diagnostic_action="检查故障是否制造成功")
            self.mix.s2s_change_car_mode_and_check_result(CarMode.TRANSPORT,car_mode_sub=0) 
            time.sleep(7)
            self.bus_comm.set('cem_lin2','PrldCem_Lin2Fr02','ChrgLidManvgDCorAcDcUnderVoltFb', 'Boolean_TRUE')
            time.sleep(1)#0.5
            data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xA0, 0x36, 0x16, 0x20], [
                                                0x59, 0x04, 0xA0, 0x36, 0x16], diagnostic_action="检查故障是否制造成功")
            self.mix.s2s_change_car_mode_and_check_result(CarMode.DYNO,car_mode_sub=0) 
            time.sleep(7)
            self.bus_comm.set('cem_lin2','PrldCem_Lin2Fr02','ChrgLidManvgDCorAcDcUnderVoltFb', 'Boolean_TRUE')
            time.sleep(1)#0.5
            data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xA0, 0x36, 0x16, 0x20], [
                                                0x59, 0x04, 0xA0, 0x36, 0x16], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.change_car_mode(CarMode.CRASH) 
            time.sleep(7)
            self.bus_comm.set('cem_lin2','PrldCem_Lin2Fr02','ChrgLidManvgDCorAcDcUnderVoltFb', 'Boolean_TRUE')
            time.sleep(1)#0.5
            data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xA0, 0x36, 0x16, 0x20], [
                                                0x59, 0x04, 0xA0, 0x36, 0x16], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.change_car_mode(CarMode.NORMAL) 

    @pytest.mark.full
    @allure.title('TRC反向_Usage Mode切换时间不满足_ transition since 5s+/-2s_通用类1')
    def test_caseid_1994753(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==ACTIVE'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('制造当前故障;读取当前故障快照'):
            self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.bus_comm.set('cem_lin2','PrldCem_Lin2Fr02','ChrgLidManvgDCorAcDcUnderVoltFb', 'Boolean_TRUE')
            time.sleep(1)#0.5
            data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xA0, 0x36, 0x16, 0x20], [
                                                0x59, 0x04, 0xA0, 0x36, 0x16,0x50], diagnostic_action="检查故障是否制造成功")

    @pytest.mark.full
    @allure.title('TRC反向_carmode切换时间不满足_During 5 s from any transitions of Car Mode_通用类1')
    def test_caseid_1994752(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==ACTIVE'):
            self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('制造当前故障;读取当前故障快照'):
            self.mix.s2s_change_car_mode_and_check_result(CarMode.FACTORY,car_mode_sub=0) 
            # self.bus_comm.set('cem_lin2','PrldCem_Lin2Fr02','ChrgLidManvgDCorAcDcOverTFb', 'Boolean_TRUE')
            # time.sleep(1)#0.5
            # self.bus_comm.set('cem_lin2','PrldCem_Lin2Fr02','ChrgLidManvgDCorAcDcUnderVoltFb', 'Boolean_TRUE')
            # time.sleep(1)#0.5
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xA0, 0x36, 0x4B, 0x20], [
                                                0x59, 0x04, 0xA0, 0x36, 0x4B,0x50], diagnostic_action="检查故障是否制造成功")

    @pytest.mark.full
    @allure.title('TRC反向_PwrLvlElec.LvlElecMai不满足_PwrLvlElec.LvlElecMai==1_通用类2')
    def test_caseid_1994751(self):
        # self.sd_tester.reset_0x1181()
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            time.sleep(7)
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x11,0x80])
            self.sd_tester.send_data_and_check(0x1002,'22429e','62429e11')
        with allure.step('制造当前故障;读取当前故障快照'):
            # self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
            # self.bus_comm.send_pdu("cem_lin6", 0x06, [0x0, 0x7C, 0xFA, 0xFF, 0xFF, 0xFF, 0xFF])
            # time.sleep(27)#21.5
            # self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts.UhiDurgDrvg)
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xA0, 0x0F, 0x01, 0x20], [
                                                  0x59, 0x04, 0xA0, 0x0F, 0x01,0x50], diagnostic_action="检查故障是否制造成功")


    @pytest.mark.full
    @allure.title('TRC反向_UsgModSts不满足_通用类2')#active下，无法制造DTC
    def test_caseid_1994750(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==ACTIVE'):
            self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        with allure.step('制造当前故障;读取当前故障快照'):
            # self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
            # self.bus_comm.send_pdu("cem_lin6", 0x06, [0x0, 0x7C, 0xFA, 0xFF, 0xFF, 0xFF, 0xFF])
            # time.sleep(27)#21.5
            # self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts.UhiDurgDrvg)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xA0, 0x0F, 0x01, 0x20], [
                                                  0x59, 0x04, 0xA0, 0x0F, 0x01,0x50], diagnostic_action="检查故障是否制造成功")
            # self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
            # self.bus_comm.send_pdu("cem_lin6", 0x06, [0x0, 0x7C, 0xC8, 0xFF, 0xFF, 0xFF, 0xFF])
            # time.sleep(17)#11

    @pytest.mark.full
    @allure.title('TRC反向_Usage Mode切换时间不满足_ transition since 5s+/-2s_通用类2')#一定满足
    def test_caseid_1994749(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==DRIVING'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        with allure.step('制造当前故障;读取当前故障快照'):
            # self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
            # self.bus_comm.send_pdu("cem_lin6", 0x06, [0x0, 0x7C, 0xFA, 0xFF, 0xFF, 0xFF, 0xFF])
            # time.sleep(27)#21.5
            # self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts.UhiDurgDrvg)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xA0, 0x0F, 0x01, 0x20], [
                                                  0x59, 0x04, 0xA0, 0x0F, 0x01,0x50], diagnostic_action="检查故障是否制造成功")
            # self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
            # self.bus_comm.send_pdu("cem_lin6", 0x06, [0x0, 0x7C, 0xC8, 0xFF, 0xFF, 0xFF, 0xFF])
            # time.sleep(17)#11

    @pytest.mark.full
    @allure.title('TRC反向_Car mode不满足_ Factory or Transport or Crash or Dynamometer_通用类2')
    def test_caseid_1994748(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==DRIVING'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('制造当前故障;读取当前故障快照'):
            self.mix.s2s_change_car_mode_and_check_result(CarMode.FACTORY,car_mode_sub=0)  
            self.mix.s2s_change_car_mode_and_check_result(CarMode.NORMAL,car_mode_sub=0)        
            # self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
            # self.bus_comm.send_pdu("cem_lin6", 0x06, [0x0, 0x7C, 0xFA, 0xFF, 0xFF, 0xFF, 0xFF])
            # time.sleep(27)#21.5
            # self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts.UhiDurgDrvg)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xA0, 0x0F, 0x01, 0x20], [
                                                  0x59, 0x04, 0xA0, 0x0F, 0x01,0x00], diagnostic_action="检查故障是否制造成功")
            # # self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
            # # self.bus_comm.send_pdu("cem_lin6", 0x06, [0x0, 0x7C, 0xC8, 0xFF, 0xFF, 0xFF, 0xFF])
            # # time.sleep(17)#11

    @pytest.mark.full
    @allure.title('TRC反向_Car mode不满足_ Factory or Transport or Crash or Dynamometer_通用类2')#driving下，carmode无法切其他的模式
    def test_caseid_1994747(self):
        # with allure.step('设置Operational cycle start criteria:Usagmode ==DRIVING'):
        #     self.sd_tester.change_car_mode(CarMode.FACTORY)
        #     time.sleep(5)  
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(7)
        # with allure.step('设置满足TRC'):
        #     self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        # with allure.step('制造当前故障;读取当前故障快照'):
        #     # self.mix.s2s_change_car_mode_and_check_result(CarMode.FACTORY,car_mode_sub=0)  
        #     # self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        #     # self.bus_comm.send_pdu("cem_lin6", 0x06, [0x0, 0x7C, 0xFA, 0xFF, 0xFF, 0xFF, 0xFF])
        #     # time.sleep(27)#21.5
        #     # self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts.UhiDurgDrvg)
        #     self.sd_tester.send_data_and_check(0x1002,'22d134','62d13402')
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xA0, 0x0F, 0x01, 0x20], [
        #                                           0x59, 0x04, 0xA0, 0x0F, 0x01], diagnostic_action="检查故障是否制造成功")

        pass

    @pytest.mark.full
    @allure.title('TRC反向_PwrLvlElec.LvlElecMai不满足_PwrLvlElec.LvlElecMai==1_通用类3')#Driving才能制造DTC
    def test_caseid_1994746(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==ACTIVE'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            time.sleep(7)
        # with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x11,0x00])
            # self.sd_tester.send_data_and_check(0x1002,'22429e','62429e01')
            self.bus_comm.check_pwrlvlelec(mai=1, subtype=1)
            # time.sleep(5)
            # self.bus_comm.set_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1PwrLvlElecMai", 1)
            # self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1PwrLvlElecMai", 1)
        with allure.step('制造当前故障;读取当前故障快照'):
            self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
            self.bus_comm.set_BMS_stop_req(low_sts=SocSts.LessOrEqual10Per,low_soh=1000,low_soc=1000)
            self.bus_comm.set_batturaw(BattURaw=11.0)
            self.bus_comm.set_dcdc_battary_act_sts(DcDcActvd=DcDcActvd.ConversionToLVSide)
            time.sleep(120)
            self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts.UloDurgdrvg)
            time.sleep(27)#21.5
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xA0, 0x10, 0x01, 0x20], [
                                                  0x59, 0x04, 0xA0, 0x10, 0x01,0x50], diagnostic_action="检查故障是否制造成功")
            
    @pytest.mark.full
    @allure.title('TRC反向_carmode切换时间不满足_During 5 s from any transitions of Car Mode_通用类3')
    def test_caseid_1994744(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==ACTIVE'):
            self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('制造当前故障;读取当前故障快照'):
            # self.sd_tester.change_car_mode(CarMode.FACTORY)
            # self.sd_tester.change_car_mode(CarMode.NORMAL)
            self.mix.s2s_change_car_mode_and_check_result(CarMode.FACTORY,car_mode_sub=0)
            self.mix.s2s_change_car_mode_and_check_result(CarMode.NORMAL,car_mode_sub=0)        
            # self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
            # self.bus_comm.set_BMS_stop_req(low_sts=SocSts.LessOrEqual10Per,low_soh=1000,low_soc=1000)
            # self.bus_comm.set_batturaw(BattURaw=11.0)
            # self.bus_comm.set_dcdc_battary_act_sts(DcDcActvd=DcDcActvd.ConversionToLVSide)
            # time.sleep(120)
            # self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts.UloDurgdrvg)
            # time.sleep(27)#21.5
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xA0, 0x10, 0x01, 0x20], [
                                                  0x59, 0x04, 0xA0, 0x10, 0x01,0x50], diagnostic_action="检查故障是否制造成功")

    @pytest.mark.test   
    @pytest.mark.full
    @allure.title('TRC反向_Usage Mode切换时间不满足_ transition since 5s+/-2s_通用类3')
    def test_caseid_1994745(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==ACTIVE'):
            self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
        with allure.step('制造当前故障;读取当前故障快照'):
            # self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
            # self.bus_comm.set_BMS_stop_req(low_sts=SocSts.LessOrEqual10Per,low_soh=1000,low_soc=1000)
            # self.bus_comm.set_batturaw(BattURaw=11.0)
            # self.bus_comm.set_dcdc_battary_act_sts(DcDcActvd=DcDcActvd.ConversionToLVSide)
            # time.sleep(120)
            # self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts.UloDurgdrvg)
            # time.sleep(27)#21.5
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xA0, 0x10, 0x01, 0x20], [
                                                  0x59, 0x04, 0xA0, 0x10, 0x01,0x50], diagnostic_action="检查故障是否制造成功")

    @pytest.mark.full
    @allure.title('TRC反向_Car mode不满足_ Factory or Transport or Crash or Dynamometer_通用类3')
    def test_caseid_1994743(self):
        # with allure.step('设置Operational cycle start criteria:Usagmode ==ACTIVE'):
        #     self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
        #     time.sleep(7)
        # with allure.step('设置TRC'):
        #     self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        # with allure.step('制造当前故障'):
        #     self.sd_tester.change_car_mode(CarMode.FACTORY)
        #     time.sleep(7)
        #     # self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        #     # self.bus_comm.set_BMS_stop_req(low_sts=SocSts.LessOrEqual10Per,low_soh=1000,low_soc=1000)
        #     # self.bus_comm.set_batturaw(BattURaw=11.0)
        #     # self.bus_comm.set_dcdc_battary_act_sts(DcDcActvd=DcDcActvd.ConversionToLVSide)
        #     # time.sleep(120)
        #     # self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts.UloDurgdrvg)
        #     # time.sleep(27)#21.5
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xA0, 0x10, 0x01, 0x20], [
        #                                           0x59, 0x04, 0xA0, 0x10, 0x01], diagnostic_action="检查故障是否制造成功")
        #     self.sd_tester.change_car_mode(CarMode.TRANSPORT)
        #     time.sleep(7)
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xA0, 0x10, 0x01, 0x20], [
        #                                           0x59, 0x04, 0xA0, 0x10, 0x01], diagnostic_action="检查故障是否制造成功")
        #     self.sd_tester.change_car_mode(CarMode.CRASH)
        #     time.sleep(7)
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xA0, 0x10, 0x01, 0x20], [
        #                                           0x59, 0x04, 0xA0, 0x10, 0x01], diagnostic_action="检查故障是否制造成功")
        #     self.sd_tester.change_car_mode(CarMode.DYNO)
        #     time.sleep(7)
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xA0, 0x10, 0x01, 0x20], [
        #                                           0x59, 0x04, 0xA0, 0x10, 0x01], diagnostic_action="检查故障是否制造成功")
        #     self.sd_tester.change_car_mode(CarMode.NORMAL)
        pass

    @pytest.mark.full
    @allure.title('TRC反向_PwrLvlElec.LvlElecMai不满足_PwrLvlElec.LvlElecMai==1_通用类4')
    def test_caseid_1994740(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==DRIVING'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            time.sleep(7)
        with allure.step('制造当前故障'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x11,0x00])
            self.bus_comm.check_pwrlvlelec(mai=1, subtype=1)
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.bus_comm.pause_ecu_send('cem_lin1', 'WMM')
            time.sleep(4)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x53, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x53, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            


    @pytest.mark.full
    @allure.title('TRC反向_Usage Mode切换时间不满足_ transition since 5s+/-2s_通用类4')
    def test_caseid_1994738(self):
        self.sd_tester.reset_0x1181()
        with allure.step('设置Operational cycle start criteria:Usagmode ==DRIVING'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        with allure.step('制造当前故障'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            # self.bus_comm.pause_ecu_send('cem_lin1', 'WMM')
            # time.sleep(4)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x53, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x53, 0x87,0x50], diagnostic_action="检查故障是否制造成功")


    @pytest.mark.full
    @allure.title('TRC反向_UsgModSts不满足_通用类4')
    def test_caseid_1994736(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==ACTIVE'):
            self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
            time.sleep(7)
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('制造当前故障'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.bus_comm.pause_ecu_send('cem_lin1', 'WMM')
            time.sleep(4)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x53, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x53, 0x87,0x50], diagnostic_action="检查故障是否制造成功")

    @pytest.mark.full
    @allure.title('TRC反向_Car mode不满足_ Factory or Transport or Crash or Dynamometer_通用类4')#UM!=driving,才可以切carmode为crash,错了，DRIVING下carmode维持不住状态，测不了
    def test_caseid_1994739(self):
        # self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        # with allure.step('设置Operational cycle start criteria:Usagmode ==DRIVING'):
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(7)
        # with allure.step('制造当前故障'):
        #     self.mix.s2s_change_car_mode_and_check_result(CarMode.FACTORY,car_mode_sub=0)
        #     time.sleep(5)
        #     self.bus_comm.pause_ecu_send('cem_lin1', 'WMM')
        #     time.sleep(4)
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x53, 0x87, 0x20], [
        #                                           0x59, 0x04, 0xD3, 0x53, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
        #     self.mix.s2s_change_car_mode_and_check_result(CarMode.TRANSPORT,car_mode_sub=0)
        #     time.sleep(5)
        #     self.bus_comm.pause_ecu_send('cem_lin1', 'WMM')
        #     time.sleep(4)
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x53, 0x87, 0x20], [
        #                                           0x59, 0x04, 0xD3, 0x53, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
        #     self.mix.s2s_change_car_mode_and_check_result(CarMode.DYNO,car_mode_sub=0)
        #     time.sleep(5)
        #     self.bus_comm.pause_ecu_send('cem_lin1', 'WMM')
        #     time.sleep(4)
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x53, 0x87, 0x20], [
        #                                           0x59, 0x04, 0xD3, 0x53, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
        #     self.mix.s2s_change_car_mode_and_check_result(CarMode.NORMAL,car_mode_sub=0)
        pass

    @pytest.mark.full
    @allure.title('TRC反向_UsgModSts不满足_Convenience_通用类4')
    def test_caseid_1994735(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==CONVENIENCE'):
            self.sd_tester.change_usage_mode(UsageMode.CONVENIENCE)
            time.sleep(7)
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('制造当前故障'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            # self.bus_comm.pause_ecu_send('cem_lin1', 'WMM')
            # time.sleep(4)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x53, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x53, 0x87,0x50], diagnostic_action="检查故障是否制造成功")

    @pytest.mark.full
    @allure.title('TRC反向_PwrLvlElec.LvlElecMai不满足_PwrLvlElec.LvlElecMai==1_active通用类6')
    def test_caseid_1994726(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==ACTIVE'):
            self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
            time.sleep(7)
        with allure.step('制造当前故障'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x11,0x80])
            self.bus_comm.check_pwrlvlelec(mai=1, subtype=1)
            self.bus_comm.stop_send_pdu("bodycan",0x269)
            time.sleep(3)
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x51, 0x82, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x51, 0x82,0x50], diagnostic_action="检查故障是否制造成功")

    @pytest.mark.full
    @allure.title('TRC反向_PwrLvlElec.LvlElecMai不满足_PwrLvlElec.LvlElecMai==1_driving通用类6')
    def test_caseid_1994725(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==DRIVING'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            time.sleep(7)
        with allure.step('制造当前故障'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.bus_comm.stop_send_pdu("bodycan",0x269)
            time.sleep(3)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x51, 0x82, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x51, 0x82,0x50], diagnostic_action="检查故障是否制造成功")

    @pytest.mark.full
    @allure.title('TRC反向_Car mode不满足_ Factory or Transport or Crash or Dynamometer_active通用类6')
    def test_caseid_1994724(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==ACTIVE'):
            self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
            time.sleep(7)
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('制造当前故障'):
            self.mix.s2s_change_car_mode_and_check_result(CarMode.FACTORY,car_mode_sub=0)
            time.sleep(5)
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.bus_comm.stop_send_pdu("bodycan",0x269)
            time.sleep(3)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x51, 0x82, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x51, 0x82,0x50], diagnostic_action="检查故障是否制造成功")
            self.bus_comm.stop_send_pdu("bodycan",0x269)
            time.sleep(3)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x51, 0x82, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x51, 0x82,0x50], diagnostic_action="检查故障是否制造成功")
            self.mix.s2s_change_car_mode_and_check_result(CarMode.TRANSPORT,car_mode_sub=0)
            time.sleep(5)
            self.bus_comm.stop_send_pdu("bodycan",0x269)
            time.sleep(3)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x51, 0x82, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x51, 0x82,0x50], diagnostic_action="检查故障是否制造成功")
            self.mix.s2s_change_car_mode_and_check_result(CarMode.DYNO,car_mode_sub=0)
            time.sleep(5)
            self.bus_comm.stop_send_pdu("bodycan",0x269)
            time.sleep(3)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x51, 0x82, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x51, 0x82,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.change_car_mode(CarMode.CRASH)
            time.sleep(5)
            self.bus_comm.stop_send_pdu("bodycan",0x269)
            time.sleep(3)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x51, 0x82, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x51, 0x82,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.change_car_mode(CarMode.NORMAL)

    @pytest.mark.full
    @allure.title('TRC反向_Car mode不满足_ Factory or Transport or Crash or Dynamometer_driving通用类6')#UM!=driving,才可以切carmode为crash,错了，DRIVING下carmode维持不住状态，测不了
    def test_caseid_1994723(self):
        # with allure.step('设置Operational cycle start criteria:Usagmode ==DRIVING'):
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(7)
        #     self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        # with allure.step('制造当前故障'):
        #     self.mix.s2s_change_car_mode_and_check_result(CarMode.FACTORY,car_mode_sub=0)
        #     time.sleep(5)
        #     self.bus_comm.stop_send_pdu("bodycan",0x269)
        #     time.sleep(3)
        #     self.bus_comm.check_car_mode_status(car_mode_main=CarMode.FACTORY,car_mode_sub=0)
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x51, 0x82, 0x20], [
        #                                           0x59, 0x04, 0xD3, 0x51, 0x82], diagnostic_action="检查故障是否制造成功")
        #     # self.bus_comm.check_car_mode_status(car_mode_main=CarMode.NORMAL,car_mode_sub=0)
        #     # self.mix.s2s_change_car_mode_and_check_result(CarMode.TRANSPORT,car_mode_sub=0)
        #     # time.sleep(5)
        #     # self.bus_comm.stop_send_pdu("bodycan",0x269)
        #     # time.sleep(3)
        #     # self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x51, 0x82, 0x20], [
        #     #                                       0x59, 0x04, 0xD3, 0x51, 0x82], diagnostic_action="检查故障是否制造成功")
        #     # self.mix.s2s_change_car_mode_and_check_result(CarMode.DYNO,car_mode_sub=0)
        #     # time.sleep(5)
        #     # self.bus_comm.stop_send_pdu("bodycan",0x269)
        #     # time.sleep(3)
        #     # self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x51, 0x82, 0x20], [
        #     #                                       0x59, 0x04, 0xD3, 0x51, 0x82], diagnostic_action="检查故障是否制造成功")
        #     self.mix.s2s_change_car_mode_and_check_result(CarMode.NORMAL,car_mode_sub=0)
            pass


    @pytest.mark.full
    @allure.title('TRC反向_carmode切换时间不满足_During 5 s from any transitions of Car Mode_active通用类6')
    def test_caseid_1994722(self):
        # with allure.step('设置Operational cycle start criteria:Usagmode ==ACTIVE'):
        #     self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
        #     time.sleep(7)
        # with allure.step('制造当前故障'):
        #     self.mix.s2s_change_car_mode_and_check_result(CarMode.FACTORY,car_mode_sub=0)
        #     self.mix.s2s_change_car_mode_and_check_result(CarMode.NORMAL,car_mode_sub=0)
        #     # self.sd_tester.change_car_mode(CarMode.FACTORY)
        #     # self.sd_tester.change_car_mode(CarMode.NORMAL)
        #     # self.bus_comm.stop_send_pdu("bodycan",0x269)
        #     # time.sleep(3)
        #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x51, 0x82, 0x20], [
        #                                           0x59, 0x04, 0xD3, 0x51, 0x82,0x50], diagnostic_action="检查故障是否制造成功")
        pass

    @pytest.mark.full
    @allure.title('TRC反向_carmode切换时间不满足_During 5 s from any transitions of Car Mode_driving通用类6')
    def test_caseid_1994721(self):
        # with allure.step('设置Operational cycle start criteria:Usagmode ==DRIVING'):
        #     self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        #     time.sleep(7)
        #     self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        # with allure.step('制造当前故障'):
        #     self.mix.s2s_change_car_mode_and_check_result(CarMode.FACTORY,car_mode_sub=0)
        #     self.mix.s2s_change_car_mode_and_check_result(CarMode.NORMAL,car_mode_sub=0)        
        #     # self.bus_comm.stop_send_pdu("bodycan",0x269)
        #     # time.sleep(3)
        #     self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        #     self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x51, 0x82, 0x20], [
        #                                           0x59, 0x04, 0xD3, 0x51, 0x82], diagnostic_action="检查故障是否制造成功")
        pass

    @pytest.mark.full
    @allure.title('TRC反向_Usage Mode切换时间不满足_ transition since 5s+/-2s_active通用类6')
    def test_caseid_1994720(self):
        self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        with allure.step('设置Operational cycle start criteria:Usagmode ==ACTIVE'):
            self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
        with allure.step('制造当前故障'):
            self.bus_comm.stop_send_pdu("bodycan",0x269)
            time.sleep(3)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x51, 0x82, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x51, 0x82,0x50], diagnostic_action="检查故障是否制造成功")


    @pytest.mark.full
    @allure.title('TRC反向_Usage Mode切换时间不满足_ transition since 5s+/-2s_driving通用类6')
    def test_caseid_1994719(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==DRIVING'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('制造当前故障'):
            self.bus_comm.stop_send_pdu("bodycan",0x269)
            time.sleep(3)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x51, 0x82, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x51, 0x82,0x50], diagnostic_action="检查故障是否制造成功")


    @pytest.mark.full
    @allure.title('TRC反向_UsgModSts不满足_Convenience_通用类6') #failed
    def test_caseid_1994718(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==CONVENIENCE'):
            self.sd_tester.change_usage_mode(UsageMode.CONVENIENCE)
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            time.sleep(7)
        with allure.step('制造当前故障'):
            self.bus_comm.stop_send_pdu("bodycan",0x269)
            time.sleep(3)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x51, 0x82, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x51, 0x82], diagnostic_action="检查故障是否制造成功")
            self.bus_comm.stop_send_pdu("bodycan",0x268)
            time.sleep(3)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x30, 0x82, 0x20], [
                                                  0x59, 0x04, 0xD1, 0x30, 0x82], diagnostic_action="检查故障是否制造成功")

    @pytest.mark.full
    @allure.title('TRC反向_BGM 未收到WMM的信号_D35387_CCP')
    def test_caseid_1994715(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('制造当前故障;读取当前故障快照'):
            self.sd_tester.write_ccp({503:0x01})
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.bus_comm.pause_ecu_send('cem_lin1', 'WMM')
            time.sleep(4)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x53, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x53, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({503:0x03})
            self.bus_comm.pause_ecu_send('cem_lin1', 'WMM')
            time.sleep(4)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x53, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x53, 0x87,0x50], diagnostic_action="检查故障是否制造成功")

    @pytest.mark.full
    @allure.title('TRC反向_carmode切换时间不满足_During 5 s from any transitions of Car Mode_通用类4')
    def test_caseid_1994737(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==DRIVING'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            time.sleep(7)
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('制造当前故障'):
            self.mix.s2s_change_car_mode_and_check_result(CarMode.FACTORY,car_mode_sub=0)
            self.mix.s2s_change_car_mode_and_check_result(CarMode.NORMAL,car_mode_sub=0) 
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            # self.bus_comm.pause_ecu_send('cem_lin1', 'WMM')
            # time.sleep(4)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x53, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x53, 0x87,0x50], diagnostic_action="检查故障是否制造成功")

class Test_TRC_CCP(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update(["VehicleModeService_client"])
        # self.ccp=self.sd_tester.sd_tester.make_ccp_according_id_and_data('1','A3')
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        # self.sd_tester.write_did_and_check(TA.BGM_MCU,0xf106,SESSION.EXTENDED,UnLock.L5,f'{self.ccp}','6ef106',check_method=Check_Method.response,recover=False)
        self.bus_comm.set('backbonefr','BcmVddmBackBoneFr00','VehMtnStVehMtnSt','VehMtnSt2_StandStillVal3')
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.bus_comm.resume_all_bus_send()
        self.bus_comm.set('backbonefr','BcmVddmBackBoneFr00','VehMtnStVehMtnSt','VehMtnSt2_StandStillVal3')
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)    

    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.ccp=self.sd_tester.sd_tester.make_ccp_according_id_and_data('1','A3')
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xf106,SESSION.EXTENDED,UnLock.L5,f'{self.ccp}','6ef106',check_method=Check_Method.response,recover=False)


    @pytest.mark.full
    @allure.title('TRC反向_BGM和RSLM之间通信失败_D34587_CCP')
    def test_caseid_1994714(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('制造当前故障;读取当前故障快照'):
            self.sd_tester.write_ccp({401:0x01})
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.bus_comm.pause_ecu_send('cem_lin1', 'RLSM')
            time.sleep(2)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x45, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x45, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({401:0x03})
            self.bus_comm.pause_ecu_send('cem_lin1', 'RLSM')
            time.sleep(2)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x45, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x45, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({401:0x04})
            self.bus_comm.pause_ecu_send('cem_lin1', 'RLSM')
            time.sleep(2)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x45, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x45, 0x87,0x50], diagnostic_action="检查故障是否制造成功")

    @pytest.mark.full
    @allure.title('TRC反向_雨量传感器错误_D34549 _CCP')
    def test_caseid_1994713(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            self.sd_tester.write_ccp({401:0x02})
            time.sleep(3.5)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x45, 0x49, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x45, 0x49,0x00], diagnostic_action="检查故障是否制造成功")
        with allure.step('制造当前故障;读取当前故障快照'):
            self.sd_tester.write_ccp({401:0x01})
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","RainSnsrErrRainDetnErr",1)
            self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","RainSnsrErrRainDetnErrActv",1)
            time.sleep(3.5)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x45, 0x49, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x45, 0x49,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({401:0x03})
            self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","RainSnsrErrRainDetnErr",1)
            self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","RainSnsrErrRainDetnErrActv",1)
            time.sleep(3.5)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x45, 0x49, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x45, 0x49,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({401:0x04})
            self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","RainSnsrErrRainDetnErr",1)
            self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","RainSnsrErrRainDetnErrActv",1)
            time.sleep(3.5)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x45, 0x49, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x45, 0x49,0x50], diagnostic_action="检查故障是否制造成功")

    @pytest.mark.full
    @allure.title('TRC反向_雨量传感器标定故障_D34546_CCP')
    def test_caseid_1994712(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        with allure.step('制造当前故障;读取当前故障快照'):
            self.sd_tester.write_ccp({401:0x01})
            self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","RainSnsrErrCalErr",1)
            self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","RainSnsrErrCalErrActv",1)
            time.sleep(3.5)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x45, 0x46, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x45, 0x46,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({401:0x03})
            self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","RainSnsrErrCalErr",1)
            self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","RainSnsrErrCalErrActv",1)
            time.sleep(3.5)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x45, 0x46, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x45, 0x46,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({401:0x04})
            self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","RainSnsrErrCalErr",1)
            self.bus_comm.set("cem_lin1","RlsmCem_Lin1Fr01","RainSnsrErrCalErrActv",1)
            time.sleep(3.5)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x45, 0x46, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x45, 0x46,0x50], diagnostic_action="检查故障是否制造成功")

    @pytest.mark.full
    @allure.title('TRC反向_总线信号/消息失败失踪message-faulty林CRC error_FCSI response-LIN帧_D30483 _CCP')
    def test_caseid_1994705(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('制造当前故障;读取当前故障快照'):
            self.sd_tester.write_ccp({1530:0x02,567:0x01})
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x04, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x04, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({1530:0x02,567:0x02})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x04, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x04, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({1530:0x02,567:0x04})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x04, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x04, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({1530:0x01,567:0x03})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x04, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x04, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({1530:0x03,567:0x03})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x04, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x04, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            
    @pytest.mark.full
    @allure.title('TRC反向_总线信号/息失败失踪message-faulty林CRC error_AIIL_L response-LIN帧_D30583 _CCP')
    def test_caseid_1994704(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('制造当前故障;读取当前故障快照'):
            self.sd_tester.write_ccp({1327:0x01})
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x05, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x05, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({1327:0x03})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x05, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x05, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            
    @pytest.mark.full
    @allure.title('TRC反向_总线信号/消息失败失踪message-faulty林CRC error_AIIL_R response-LIN帧_D30683 _CCP')
    def test_caseid_1994703(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        with allure.step('制造当前故障;读取当前故障快照'):
            self.sd_tester.write_ccp({1328:0x01})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x06, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x06, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({1328:0x03})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x06, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x06, 0x83,0x50], diagnostic_action="检查故障是否制造成功")

    @pytest.mark.full
    @allure.title('TRC反向_总线信号/消息失败失踪message-faulty林CRC error_PSGL response-LIN帧_D30983 _CCP')
    def test_caseid_1994702(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        with allure.step('制造当前故障;读取当前故障快照'):
            self.sd_tester.write_ccp({1531:0x01})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x09, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x09, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({1531:0x03})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x09, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x09, 0x83,0x50], diagnostic_action="检查故障是否制造成功")

    @pytest.mark.full
    @allure.title('TRC反向_总线信号/消息失败失踪message-faulty林CRC error_DSGL response-LIN帧_D30A83 _CCP')
    def test_caseid_1994701(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        with allure.step('制造当前故障;读取当前故障快照'):
            self.sd_tester.write_ccp({1532:0x01})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x0A, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x0A, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({1532:0x03})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x0A, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x0A, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            
    @pytest.mark.test1
    @pytest.mark.full
    @allure.title('TRC反向_总线信号/消息失败失踪message-faulty林CRC error_ALM_7 response-LIN帧_D31483 _CCP')
    def test_caseid_1994699(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('制造当前故障;读取当前故障快照'):
            self.sd_tester.write_ccp({950:0x01,636:0x01,964:0x00})
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x14, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x14, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x01,636:0x01,964:0x02})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x14, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x14, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x01,636:0x02,964:0x02})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x14, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x14, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x01,636:0x03,964:0x01})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x14, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x14, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x02,636:0x01,964:0x02})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x14, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x14, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x02,636:0x02,964:0x02})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x14, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x14, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x02,636:0x03,964:0x00})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x14, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x14, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x02,636:0x03,964:0x01})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x14, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x14, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x03,636:0x01,964:0x01})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x14, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x14, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x03,636:0x01,964:0x00})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x14, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x14, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x03,636:0x02,964:0x01})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x14, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x14, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x03,636:0x02,964:0x00})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x14, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x14, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
    @pytest.mark.test1
    @pytest.mark.full
    @allure.title('TRC反向_总线信号/消息失败失踪message-faulty林CRC error_TLCM response-LIN帧_D30D83 _CCP')
    def test_caseid_1994700(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        with allure.step('制造当前故障;读取当前故障快照'):
            self.sd_tester.write_ccp({1306:0x01})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x0D, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x0D, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({1306:0x03})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x0D, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x0D, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            
    @pytest.mark.full
    @allure.title('TRC反向_总线信号/消息失败失踪message-faulty林CRC error_ALM_8 response-LIN帧_D31583 _CCP')
    def test_caseid_1994698(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('制造当前故障;读取当前故障快照'):
            self.sd_tester.write_ccp({950:0x01,636:0x02,964:0x02})
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x15, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x15, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x01,636:0x01,964:0x00})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x15, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x15, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x01,636:0x01,964:0x01})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x15, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x15, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x01,636:0x03,964:0x00})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x15, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x15, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x01,636:0x03,964:0x01})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x15, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x15, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x02,636:0x02,964:0x02})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x15, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x15, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x01,636:0x01,964:0x02})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x15, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x15, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x01,636:0x03,964:0x00})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x15, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x15, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x01,636:0x03,964:0x01})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x15, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x15, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x03,636:0x01,964:0x00})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x15, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x15, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x03,636:0x01,964:0x01})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x15, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x15, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x03,636:0x02,964:0x00})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x15, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x15, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x03,636:0x02,964:0x01})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x15, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x15, 0x83,0x50], diagnostic_action="检查故障是否制造成功")

    @pytest.mark.full
    @allure.title('TRC反向_总线信号/消息失败失踪message-faulty林CRC error_AWM response-LIN帧_D31683 _CCP')
    def test_caseid_1994697(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        with allure.step('制造当前故障;读取当前故障快照'):
            self.sd_tester.write_ccp({564:0x01})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x16, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x16, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({564:0x03})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x16, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x16, 0x83,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({564:0x04})
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x16, 0x83, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x16, 0x83,0x50], diagnostic_action="检查故障是否制造成功")

    @pytest.mark.full
    @allure.title('TRC反向_FCSI丢失LIN响应_D30487 _CCP')
    def test_caseid_1994696(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('制造当前故障;读取当前故障快照'):
            self.sd_tester.write_ccp({1530:0x01,567:0x03})
            self.bus_comm.pause_ecu_send('cem_lin2', 'FCSI')
            time.sleep(2)
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x04, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x04, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({1530:0x03,567:0x03})
            self.bus_comm.pause_ecu_send('cem_lin2', 'FCSI')
            time.sleep(2)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x04, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x04, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({1530:0x02,567:0x01})
            self.bus_comm.pause_ecu_send('cem_lin2', 'FCSI')
            time.sleep(2)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x04, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x04, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({1530:0x02,567:0x02})
            self.bus_comm.pause_ecu_send('cem_lin2', 'FCSI')
            time.sleep(2)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x04, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x04, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({1530:0x02,567:0x04})
            self.bus_comm.pause_ecu_send('cem_lin2', 'FCSI')
            time.sleep(2)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x04, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x04, 0x87,0x50], diagnostic_action="检查故障是否制造成功")

    @pytest.mark.full
    @allure.title('TRC反向_PSGL丢失LIN响应_D30987 _CCP')
    def test_caseid_1994695(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        with allure.step('制造当前故障;读取当前故障快照'):
            self.sd_tester.write_ccp({1531:0x01})
            self.bus_comm.pause_ecu_send('cem_lin3', 'PSGL')
            time.sleep(2)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x09, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x09, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({1531:0x03})
            self.bus_comm.pause_ecu_send('cem_lin3', 'PSGL')
            time.sleep(2)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x09, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x09, 0x87,0x50], diagnostic_action="检查故障是否制造成功")

    @pytest.mark.full
    @allure.title('TRC反向_DSGL丢失LIN响应_D30A87_CCP')
    def test_caseid_1994694(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        with allure.step('制造当前故障;读取当前故障快照'):
            self.sd_tester.write_ccp({1532:0x01})
            self.bus_comm.pause_ecu_send('cem_lin3', 'DSGL')
            time.sleep(2)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x0A, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x0A, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({1532:0x03})
            self.bus_comm.pause_ecu_send('cem_lin3', 'DSGL')
            time.sleep(2)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x0A, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x0A, 0x87,0x50], diagnostic_action="检查故障是否制造成功")

    @pytest.mark.full
    @allure.title('TRC反向_TLCM丢失LIN响应_D30D87_CCP')
    def test_caseid_1994693(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        with allure.step('制造当前故障;读取当前故障快照'):
            self.sd_tester.write_ccp({1306:0x01})
            self.bus_comm.pause_ecu_send('cem_lin4', 'TLCM')
            time.sleep(2)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x0D, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x0D, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({1306:0x03})
            self.bus_comm.pause_ecu_send('cem_lin4', 'TLCM')
            time.sleep(2)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x0D, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x0D, 0x87,0x50], diagnostic_action="检查故障是否制造成功")

    @pytest.mark.full
    @allure.title('TRC反向_ALM_7丢失LIN响应_D31487_CCP')
    def test_caseid_1994692(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        with allure.step('制造当前故障;读取当前故障快照'):
            self.sd_tester.write_ccp({950:0x01,636:0x01,964:0x00})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x14, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x14, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x01,636:0x01,964:0x02})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x14, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x14, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x01,636:0x02,964:0x02})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x14, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x14, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x01,636:0x03,964:0x01})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x14, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x14, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x02,636:0x01,964:0x02})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x14, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x14, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x02,636:0x02,964:0x02})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x14, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x14, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x02,636:0x03,964:0x00})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x14, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x14, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x02,636:0x03,964:0x01})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x14, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x14, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x03,636:0x01,964:0x01})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x14, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x14, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x03,636:0x01,964:0x00})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x14, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x14, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x03,636:0x02,964:0x01})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x14, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x14, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x03,636:0x02,964:0x00})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x14, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x14, 0x87,0x50], diagnostic_action="检查故障是否制造成功")

    @pytest.mark.full
    @allure.title('TRC反向_ALM_8丢失LIN响应_D31587_CCP')
    def test_caseid_1994691(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        with allure.step('制造当前故障;读取当前故障快照'):
            self.sd_tester.write_ccp({950:0x01,636:0x02,964:0x02})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x15, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x15, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x01,636:0x01,964:0x00})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x15, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x15, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x01,636:0x01,964:0x01})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x15, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x15, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x01,636:0x03,964:0x00})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x15, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x15, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x01,636:0x03,964:0x01})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x15, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x15, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x02,636:0x02,964:0x02})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x15, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x15, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x01,636:0x01,964:0x02})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x15, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x15, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x01,636:0x03,964:0x00})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x15, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x15, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x01,636:0x03,964:0x01})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x15, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x15, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x03,636:0x01,964:0x00})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x15, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x15, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x03,636:0x01,964:0x01})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x15, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x15, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x03,636:0x02,964:0x00})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x15, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x15, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x03,636:0x02,964:0x01})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x15, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x15, 0x87,0x50], diagnostic_action="检查故障是否制造成功")

    @pytest.mark.full
    @allure.title('TRC反向_AWM丢失LIN响应_D31687_CCP')
    def test_caseid_1994690(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        with allure.step('制造当前故障;读取当前故障快照'):
            self.sd_tester.write_ccp({564:0x01})
            self.bus_comm.pause_ecu_send('cem_lin6', 'AWM')
            time.sleep(2)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x16, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x16, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({564:0x03})
            self.bus_comm.pause_ecu_send('cem_lin6', 'AWM')
            time.sleep(2)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x16, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x16, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({564:0x04})
            self.bus_comm.pause_ecu_send('cem_lin6', 'AWM')
            time.sleep(2)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x16, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x16, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            
    # @pytest.mark.full
    # @allure.title('TRC反向_来自VDDM的TPMS总线信号系统及信息/消息数据丢失_D00C87_CCP')
    # def test_caseid_1994689(self):
    #     self.sd_tester.write_ccp({19:0x01})
    #     self.sd_tester.reset_0x1181()
    #     with allure.step('设置Operational cycle start criteria:Usagmode ==ACTIVE'):
    #         self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
    #         time.sleep(7)
    #     with allure.step('设置满足TRC'):
    #         self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
    #     with allure.step('制造当前故障;读取当前故障快照'):
    #         # self.sd_tester.write_ccp({19:0x01})
    #         # time.sleep(3.5)
    #         self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
    #         self.bus_comm.pause_ecu_send('backbonefr', 'VDDM')
    #         time.sleep(0.5)
    #         data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD0, 0x0C, 0x87, 0x20], [
    #                                               0x59, 0x04, 0xD0, 0x0C, 0x87], diagnostic_action="检查故障是否制造成功")
    #         self.sd_tester.write_ccp({19:0x07})
    #         time.sleep(3.5)
    #         self.bus_comm.pause_ecu_send('backbonefr', 'VDDM')
    #         time.sleep(0.5)
    #         data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD0, 0x0C, 0x87, 0x20], [
    #                                               0x59, 0x04, 0xD0, 0x0C, 0x87], diagnostic_action="检查故障是否制造成功")

    # @pytest.mark.full
    # @allure.title('TRC反向_MGM的IMMO管理故障_D3329A_CCP')
    # def test_caseid_1994688(self):
    #     self.sd_tester.write_ccp({1312:0x01})
    #     time.sleep(3.5)
    #     with allure.step('设置Operational cycle start criteria:Usagmode ==ACTIVE'):
    #         self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
    #         time.sleep(7)
    #     with allure.step('设置满足TRC'):
    #         self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
    #     with allure.step('制造当前故障;读取当前故障快照'):
    #         self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
    #         data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x32, 0x9A, 0x20], [
    #                                               0x59, 0x04, 0xD3, 0x32, 0x9A,0x50], diagnostic_action="检查故障是否制造成功")
    #         self.sd_tester.write_ccp({1312:0x03})
    #         time.sleep(3.5)
    #         data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x32, 0x9A, 0x20], [
    #                                               0x59, 0x04, 0xD3, 0x32, 0x9A], diagnostic_action="检查故障是否制造成功")

    @pytest.mark.full
    @allure.title('TRC反向_ALM_9丢失LIN响应_D31887_CCP')
    def test_caseid_1994686(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            UM = self.sd_tester.send_data_and_check(0x1002,0x22DD0A,'62dd0a',diagnostic_action="UM")[6:]
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        with allure.step('制造当前故障;读取当前故障快照'):
            self.sd_tester.write_ccp({950:0x01,636:0x02,964:0x00})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x18, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x18, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x01,636:0x02,964:0x02})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x18, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x18, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x01,636:0x01,964:0x01})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x18, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x18, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x01,636:0x03,964:0x01})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x18, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x18, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x02,636:0x02,964:0x02})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x18, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x18, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x02,636:0x01,964:0x00})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x18, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x18, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x02,636:0x01,964:0x01})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x18, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x18, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x02,636:0x03,964:0x00})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x18, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x18, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x02,636:0x03,964:0x01})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x18, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x18, 0x87,0x50], diagnostic_action="检查故障是否制造成功")

            self.sd_tester.write_ccp({950:0x03,636:0x02,964:0x00})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x18, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x18, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x03,636:0x02,964:0x01})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x18, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x18, 0x87,0x50], diagnostic_action="检查故障是否制造成功")

    @pytest.mark.full
    @allure.title('TRC反向_ALM_10丢失LIN响应_D31987_CCP')
    def test_caseid_1994685(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==Driving'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        with allure.step('制造当前故障;读取当前故障快照'):
            self.sd_tester.write_ccp({950:0x02,636:0x02,964:0x02})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x19, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x19, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x02,636:0x01,964:0x00})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x19, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x19, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x02,636:0x01,964:0x01})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x19, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x19, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x02,636:0x03,964:0x00})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x19, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x19, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x02,636:0x03,964:0x01})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x19, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x19, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x01,636:0x02,964:0x00})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x19, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x19, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({950:0x01,636:0x02,964:0x01})
            self.bus_comm.pause_ecu_send('cem_lin5', 'ALM1')
            time.sleep(3.5)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x19, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x19, 0x87,0x50], diagnostic_action="检查故障是否制造成功")


    @pytest.mark.full
    @allure.title('TRC反向_BodyCAN BGM和IPM丢失帧通信_D12487_CCP')
    def test_caseid_1994684(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==DRIVING'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('制造当前故障;读取当前故障快照'):
            self.sd_tester.write_ccp({1333:0x01})
            self.bus_comm.pause_ecu_send('bodycan', 'IPM')
            time.sleep(3)
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x24, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD1, 0x24, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({1333:0x03})
            self.bus_comm.pause_ecu_send('bodycan', 'IPM')
            time.sleep(3)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x24, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD1, 0x24, 0x87,0x50], diagnostic_action="检查故障是否制造成功")

    @pytest.mark.full
    @allure.title('TRC反向_BodyCAN BGM和SMB丢失帧通信_D32087_CCP')
    def test_caseid_1994683(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==DRIVING'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('制造当前故障;读取当前故障快照'):
            self.sd_tester.write_ccp({1473:0x01})
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
            # self.bus_comm.pause_ecu_send('bodycan', 'SMB')
            # time.sleep(2)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x20, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x20, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({1473:0x03})
            # self.bus_comm.pause_ecu_send('bodycan', 'SMB')
            # time.sleep(2)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x20, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD3, 0x20, 0x87,0x50], diagnostic_action="检查故障是否制造成功")

    @pytest.mark.full
    @allure.title('TRC反向_ConnectivityCANFD BGM和WPC3丢失帧通信_D12587_CCP')
    def test_caseid_1994682(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==DRIVING'):
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        with allure.step('制造当前故障;读取当前故障快照'):
            self.sd_tester.write_ccp({1439:0x01})
            self.bus_comm.pause_ecu_send('connectivitycanfd', 'WPC3')
            time.sleep(2.5)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x25, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD1, 0x25, 0x87,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({1439:0x03})
            self.bus_comm.pause_ecu_send('connectivitycanfd', 'WPC3')
            time.sleep(2.5)
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x25, 0x87, 0x20], [
                                                  0x59, 0x04, 0xD1, 0x25, 0x87,0x50], diagnostic_action="检查故障是否制造成功")

    @pytest.mark.full
    @allure.title('TRC反向_左前胎压传感器电池电量低_5A5616_CCP')
    def test_caseid_1994681(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==ACTIVE'):
            self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        with allure.step('制造当前故障;读取当前故障快照'):
            self.sd_tester.write_ccp({19:0x01})
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0x5A, 0x56, 0x16, 0x20], [
                                                  0x59, 0x04, 0x5A, 0x56, 0x16,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({19:0x07})
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0x5A, 0x56, 0x16, 0x20], [
                                                  0x59, 0x04, 0x5A, 0x56, 0x16,0x50], diagnostic_action="检查故障是否制造成功")

    @pytest.mark.full
    @allure.title('TRC反向_左前传感器信号丢失_5A568F_CCP')
    def test_caseid_1994680(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==ACTIVE'):
            self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        with allure.step('制造当前故障;读取当前故障快照'):
            self.sd_tester.write_ccp({19:0x01})
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0x5A, 0x56, 0x8F, 0x20], [
                                                  0x59, 0x04, 0x5A, 0x56, 0x8F,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({19:0x07})
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0x5A, 0x56, 0x8F, 0x20], [
                                                  0x59, 0x04, 0x5A, 0x56, 0x8F,0x50], diagnostic_action="检查故障是否制造成功")


    @pytest.mark.full
    @allure.title('TRC反向_右前胎压传感器电池电量低_5A5816_CCP')
    def test_caseid_1994679(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==ACTIVE'):
            self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        with allure.step('制造当前故障;读取当前故障快照'):
            self.sd_tester.write_ccp({19:0x01})
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0x5A, 0x58, 0x16, 0x20], [
                                                  0x59, 0x04, 0x5A, 0x58, 0x16,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({19:0x07})
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0x5A, 0x58, 0x16, 0x20], [
                                                  0x59, 0x04, 0x5A, 0x58, 0x16,0x50], diagnostic_action="检查故障是否制造成功")


    @pytest.mark.full
    @allure.title('TRC反向_右前传感器信号丢失_5A588F_CCP')
    def test_caseid_1994678(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==ACTIVE'):
            self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        with allure.step('制造当前故障;读取当前故障快照'):
            self.sd_tester.write_ccp({19:0x01})
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0x5A, 0x58, 0x8F, 0x20], [
                                                  0x59, 0x04, 0x5A, 0x58, 0x8F,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({19:0x07})
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0x5A, 0x58, 0x8F, 0x20], [
                                                  0x59, 0x04, 0x5A, 0x58, 0x8F,0x50], diagnostic_action="检查故障是否制造成功")

    @pytest.mark.full
    @allure.title('TRC反向_左后传感器信号丢失_5A608F_CCP')
    def test_caseid_1994677(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==ACTIVE'):
            self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        with allure.step('制造当前故障;读取当前故障快照'):
            self.sd_tester.write_ccp({19:0x01})
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0x5A, 0x60, 0x8F, 0x20], [
                                                  0x59, 0x04, 0x5A, 0x60, 0x8F,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({19:0x07})
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0x5A, 0x60, 0x8F, 0x20], [
                                                  0x59, 0x04, 0x5A, 0x60, 0x8F,0x50], diagnostic_action="检查故障是否制造成功")

    @pytest.mark.full
    @allure.title('TRC反向_左后胎压传感器电池电量低_5A6016_CCP')
    def test_caseid_1994676(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==ACTIVE'):
            self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        with allure.step('制造当前故障;读取当前故障快照'):
            self.sd_tester.write_ccp({19:0x01})
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0x5A, 0x60, 0x16, 0x20], [
                                                  0x59, 0x04, 0x5A, 0x60, 0x16,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({19:0x07})
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0x5A, 0x60, 0x16, 0x20], [
                                                  0x59, 0x04, 0x5A, 0x60, 0x16,0x50], diagnostic_action="检查故障是否制造成功")
    @pytest.mark.full
    @allure.title('TRC反向_右后胎压传感器电池电量低_5A6216_CCP')
    def test_caseid_1994675(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==ACTIVE'):
            self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        with allure.step('制造当前故障;读取当前故障快照'):
            self.sd_tester.write_ccp({19:0x01})
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0x5A, 0x62, 0x16, 0x20], [
                                                  0x59, 0x04, 0x5A, 0x62, 0x16,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({19:0x07})
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0x5A, 0x62, 0x16, 0x20], [
                                                  0x59, 0x04, 0x5A, 0x62, 0x16,0x50], diagnostic_action="检查故障是否制造成功")
    @pytest.mark.full
    @allure.title('TRC反向_右后传感器信号丢失_5A628F_CCP')
    def test_caseid_1994674(self):
        with allure.step('设置Operational cycle start criteria:Usagmode ==ACTIVE'):
            self.sd_tester.change_usage_mode(UsageMode.ACTIVE)
            time.sleep(7)
        with allure.step('设置满足TRC'):
            self.sd_tester.send_request_and_recv_response([0x2F, 0x42, 0x9E, 0x03,0x00,0x80])
        with allure.step('清除当前故障，恢复故障快照存储环境'):
            self.sd_tester.send_data_and_check(0x1002,0x14FFFFFF,'54',diagnostic_action="清除当前故障")
        with allure.step('制造当前故障;读取当前故障快照'):
            self.sd_tester.write_ccp({19:0x01})
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0x5A, 0x62, 0x8F, 0x20], [
                                                  0x59, 0x04, 0x5A, 0x62, 0x8F,0x50], diagnostic_action="检查故障是否制造成功")
            self.sd_tester.write_ccp({19:0x07})
            data_1 = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0x5A, 0x62, 0x8F, 0x20], [
                                                  0x59, 0x04, 0x5A, 0x62, 0x8F,0x50], diagnostic_action="检查故障是否制造成功")
            
#pytest BaseTech/DiagFlash/DiagDtc/test_trc_comunicate_chassis_ccp_notmet.py -k test_caseid_1994750 --disable_env=true

