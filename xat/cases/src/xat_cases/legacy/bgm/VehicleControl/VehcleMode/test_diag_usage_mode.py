import os
import sys
import time
from time import sleep
import pytest
import allure
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.case_helper.test_base import TestBase
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.interface.ecuinterface import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester

@allure.feature("车身网关测试/基础架构")
@allure.story("整车模式/使用模式")
class TestChangeUsageMode(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.nucapp.bgm_diag_line_up()
        self.sd_tester = Sd_Tester(**self.tc_config)
        self.sd_tester.update_serverdoipid(0x1002)
        time.sleep(.5)
        self.sd_tester.diagnostic_client_sim_start()
        with allure.step(f"Test Class Pre Step can_lin_fr 启动"):
            self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
        self.sd_tester.change_usage_mode(1)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        self.sd_tester.change_usage_mode(1)
        self.nucapp.bgm_diag_line_down()
        self.sd_tester.stop_tester_present()
        self.sd_tester.diagnostic_client_sim_close()
        with allure.step(f"Test Class clearup Step can_lin_fr 停止"):
            self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）
            self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        super().after_class(self, ecu)

    def check_usage_mode_status(self, expectedmode, do_assert=True, **kwargs):
        '''
        校验 usage 状态
        @param expectedmode:
        @param do_assert:
        @param timeout:
        @param kwargs:
        @return:
        '''
        timeout = kwargs.get('timeout', 5)
        # msg_signals_obj = kwargs.get('msg_signals_obj', self.ipdu.bodycan.CEMBodyFr12)
        # signal_name = kwargs.get('signal_name', 'VehModMngtGlbSafe1UsgModSts_3_CEMBodySignalIPdu12')

        msg_signals_obj = kwargs.get('msg_signals_obj', self.ipdu.backbonefr.CemBackBoneFr02)
        signal_name = kwargs.get(
            'signal_name', 'VehModMngtGlbSafe1UsgModSts_0_CEMBackBoneSignalIpdu02'
        )
        result, realvalue, expectedvalue = self.ipdu.check(msg_signals_obj=msg_signals_obj,
                                                           signal_name=signal_name,
                                                           sig_value_name=expectedmode,
                                                           do_assert=do_assert, timeout=timeout, )

        return result, realvalue, expectedvalue

    @pytest.mark.Usagemode
    @pytest.mark.smoke
    def test_usagemode_caseid_1959935(self):
        '''
        1.standstill状态
        2.从Abandoned诊断切换为Convenience
        '''
        self.sd_tester.change_usage_mode(0)
        self.check_usage_mode_status(0)
        time.sleep(.3)
        self.sd_tester.change_usage_mode(2)
        self.check_usage_mode_status(2)

    @pytest.mark.Usagemode
    @pytest.mark.smoke
    def test_usagemode_caseid_110111(self):
        '''
        1.standstill状态
        2.从Abandoned诊断切换为 Inactive
        '''
        self.sd_tester.change_usage_mode(0)
        self.check_usage_mode_status(0)
        time.sleep(.3)
        self.sd_tester.change_usage_mode(1)
        self.check_usage_mode_status(1)

    @pytest.mark.Usagemode
    @pytest.mark.smoke
    def test_usagemode_caseid_109974(self):
        '''
        1.standstill状态
        2.从Abandoned诊断切换为 ACTIVE
        '''
        self.sd_tester.change_usage_mode(0)
        self.check_usage_mode_status(0)
        time.sleep(.3)
        self.sd_tester.change_usage_mode(11)
        self.check_usage_mode_status(11)

    @pytest.mark.Usagemode
    @pytest.mark.smoke
    def test_usagemode_caseid_1959934(self):
        '''
        1.standstill状态109954
        2.从Abandoned诊断切换为 DRIVING
        '''
        self.sd_tester.change_usage_mode(0)
        self.check_usage_mode_status(0)
        time.sleep(.3)
        self.sd_tester.change_usage_mode(13)
        self.check_usage_mode_status(13)

    @pytest.mark.Usagemode
    @pytest.mark.smoke
    def test_usagemode_caseid_1959911(self):
        '''
        1.standstill状态110137
        2.从 Inactive 诊断切换为 Active
        '''
        self.sd_tester.change_usage_mode(1)
        self.check_usage_mode_status(1)
        time.sleep(.3)
        self.sd_tester.change_usage_mode(11)
        self.check_usage_mode_status(11)

    @pytest.mark.Usagemode
    @pytest.mark.smoke
    def test_usagemode_caseid_1959912(self):
        '''
        1.standstill状态110122
        2.从 Inactive 诊断切换为 ABANDONED
        '''
        self.sd_tester.change_usage_mode(1)
        self.check_usage_mode_status(1)
        time.sleep(.3)
        self.sd_tester.change_usage_mode(0)
        self.check_usage_mode_status(0)

    @pytest.mark.Usagemode
    @pytest.mark.smoke
    @pytest.mark.sanity
    def test_usagemode_caseid_110061(self):
        '''
        1.standstill状态
        2.从 Inactive 诊断切换为 DRIVING
        '''
        self.sd_tester.change_usage_mode(1)
        self.check_usage_mode_status(1)
        time.sleep(.3)
        self.sd_tester.change_usage_mode(13)
        self.check_usage_mode_status(13)

    @pytest.mark.Usagemode
    @pytest.mark.smoke
    def test_usagemode_caseid_109965(self):
        '''
        1.standstill状态
        2.从 Inactive 诊断切换为 CONVENIENCE
        '''
        self.sd_tester.change_usage_mode(1)
        self.check_usage_mode_status(1)
        time.sleep(.3)
        self.sd_tester.change_usage_mode(2)
        self.check_usage_mode_status(2)

    @pytest.mark.Usagemode
    @pytest.mark.smoke
    def test_usagemode_caseid_110109(self):
        '''
        1.standstill状态
        2.从Convenience 诊断切换为 Inactive
        '''
        self.sd_tester.change_usage_mode(2)
        self.check_usage_mode_status(2)
        time.sleep(.3)
        self.sd_tester.change_usage_mode(1)
        self.check_usage_mode_status(1)

    @pytest.mark.Usagemode
    @pytest.mark.smoke
    def test_usagemode_caseid_1959928(self):
        '''
        1.standstill状态
        2.从Convenience 诊断切换为 ABANDONED
        '''
        self.sd_tester.change_usage_mode(2)
        self.check_usage_mode_status(2)
        time.sleep(.3)
        self.sd_tester.change_usage_mode(0)
        self.check_usage_mode_status(0)

    @pytest.mark.Usagemode
    @pytest.mark.smoke
    def test_usagemode_caseid_1959927(self):
        '''
        1.standstill状态110058
        2.从Convenience 诊断切换为 ACTIVE
        '''
        self.sd_tester.change_usage_mode(2)
        self.check_usage_mode_status(2)
        time.sleep(.3)
        self.sd_tester.change_usage_mode(11)
        self.check_usage_mode_status(11)

    @pytest.mark.Usagemode
    @pytest.mark.smoke
    def test_usagemode_caseid_1959925(self):
        '''
        1.standstill状态
        2.从Convenience 诊断切换为 DRIVING
        '''
        self.sd_tester.change_usage_mode(2)
        self.check_usage_mode_status(2)
        time.sleep(.3)
        self.sd_tester.change_usage_mode(13)
        self.check_usage_mode_status(13)

    @pytest.mark.Usagemode
    @pytest.mark.smoke
    def test_usagemode_caseid_110108(self):
        '''
        1.standstill状态
        2.从 DRIVING 诊断切换为 INACTIVE
        '''
        self.sd_tester.change_usage_mode(13)
        self.check_usage_mode_status(13)
        time.sleep(.3)
        self.sd_tester.change_usage_mode(1)
        self.check_usage_mode_status(1)

    @pytest.mark.Usagemode
    @pytest.mark.smoke
    def test_usagemode_caseid_110027(self):
        '''
        1.standstill状态
        2.从 DRIVING 诊断切换为 ACTIVE
        '''
        self.sd_tester.change_usage_mode(13)
        self.check_usage_mode_status(13)
        time.sleep(.3)
        self.sd_tester.change_usage_mode(11)
        self.check_usage_mode_status(11)

    @pytest.mark.Usagemode
    @pytest.mark.smoke
    def test_usagemode_caseid_1959919(self):
        '''
        1.standstill状态109932
        2.从 DRIVING 诊断切换为 ABANDONED
        '''
        self.sd_tester.change_usage_mode(13)
        self.check_usage_mode_status(13)
        time.sleep(.3)
        self.sd_tester.change_usage_mode(0)
        self.check_usage_mode_status(0)

    @pytest.mark.Usagemode
    @pytest.mark.smoke
    def test_usagemode_caseid_110022(self):
        '''
        1.standstill状态
        2.从 ACTIVE 诊断切换为 INACTIVE
        '''
        self.sd_tester.change_usage_mode(11)
        self.check_usage_mode_status(11)
        time.sleep(.3)
        self.sd_tester.change_usage_mode(1)
        self.check_usage_mode_status(1)

    @pytest.mark.Usagemode
    @pytest.mark.smoke
    def test_usagemode_caseid_110003(self):
        '''
        1.standstill状态
        2.从 ACTIVE 诊断切换为 DRIVING
        '''
        self.sd_tester.change_usage_mode(11)
        self.check_usage_mode_status(11)
        time.sleep(.3)
        self.sd_tester.change_usage_mode(13)
        self.check_usage_mode_status(13)

    @pytest.mark.Usagemode
    @pytest.mark.smoke
    def test_usagemode_caseid_1959930(self):
        '''
        1.standstill状态109957
        2.从 ACTIVE 诊断切换为 CONVENIENCE
        '''
        self.sd_tester.change_usage_mode(11)
        self.check_usage_mode_status(11)
        time.sleep(.3)
        self.sd_tester.change_usage_mode(2)
        self.check_usage_mode_status(2)

    @pytest.mark.Usagemode
    @pytest.mark.smoke
    def test_usagemode_caseid_1959932(self):
        '''
        1.standstill状态
        2.从 ACTIVE 诊断切换为 ABANDONED
        '''
        self.sd_tester.change_usage_mode(11)
        self.check_usage_mode_status(11)
        time.sleep(.3)
        self.sd_tester.change_usage_mode(0)
        self.check_usage_mode_status(0)

# #################### Usagemode_诊断切换   结束####################################################################
# #################### Usagemode_不满足条件诊断切换  开始 ###########################################################

@allure.feature("车身网关测试/基础架构")
@allure.story("整车模式/使用模式")
class TestNotChangeUsageMode(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.nucapp.bgm_diag_line_up()
        self.sd_tester = Sd_Tester(**self.tc_config)
        self.sd_tester.update_serverdoipid(0x1002)
        time.sleep(2)
        self.sd_tester.diagnostic_client_sim_start()
        with allure.step(f"Test Class Pre Step can_lin_fr 启动"):
            self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
        time.sleep(.5)
        #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
        self.sd_tester.change_usage_mode(1)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
        time.sleep(.3)
        #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
        self.sd_tester.change_usage_mode(1)
        self.nucapp.bgm_diag_line_down()
        self.sd_tester.stop_tester_present()
        self.sd_tester.diagnostic_client_sim_close()
        with allure.step(f"Test Class clearup Step can_lin_fr 停止"):
            self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）
            self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        super().after_class(self, ecu)

    def check_usage_mode_status(self, expectedmode, do_assert=True, **kwargs):
        '''
        校验 usage 状态
        @param expectedmode:
        @param do_assert:
        @param timeout:
        @param kwargs:
        @return:
        '''
        timeout = kwargs.get('timeout', 5)
        msg_signals_obj = kwargs.get('msg_signals_obj', self.ipdu.bodycan.CEMBodyFr12)
        signal_name = kwargs.get('signal_name', 'VehModMngtGlbSafe1UsgModSts_3_CEMBodySignalIPdu12')

        result, realvalue, expectedvalue = self.ipdu.check(msg_signals_obj=msg_signals_obj,
                                                           signal_name=signal_name,
                                                           sig_value_name=expectedmode,
                                                           do_assert=do_assert, timeout=timeout, )

        return result, realvalue, expectedvalue
    
    def not_change_usage_mode(self, mode_type: int, do_assert=True, **kwargs):
        '''
          切换usage mode为XX,
        @param mode_type:
             /** 废弃 */ @value(0) ABANDONED,
            /** 未激活 */ @value(1) INACTIVE,
            /** 充电 */ @value(2) CONVENIENCE,
            /** 激活 */ @value(11) ACTIVE,
            /** 驾驶 */ @value(13) DRIVING
        @param do_assert: 若为True 则表示切换失败则会报错，否则返回切换后的模式
        @return:
        '''
        # 读取did
        self.sd_tester.information_check_dd0a()
        # 接受数据
        result = self.sd_tester.return_udsdata_and_check_and_print_response_result("Send dd0a to get result")[3:]
        #
        curr_mode = result[0]
        if curr_mode == mode_type:
            return curr_mode
        # 检查当前会话，判断是否需要重新进入
        self.sd_tester.diagnostic_session_check()
        result = self.sd_tester.return_udsdata_and_check_and_print_response_result("Send f186 to get result")[3:]
        curr_status = result[-1]
        if curr_status != 0x03:
            # 进入扩展会话
            self.sd_tester.enter_extended_session()
            result = self.sd_tester.return_udsdata_and_check_and_print_response_result("Send 1003 to get result")
            if do_assert and result[0] != 0x50:
                assert 0, f'enter_extended_session 失败'
            self.sd_tester.security_access_level_l2()
        else:
            # 判断是否需要解锁
            self.sd_tester.client_sim.send_data([0x27, 0x03])
            result = self.sd_tester.return_udsdata_and_check_and_print_response_result("Send 0x27, 0x03 to get result")
            curr_le = result[2:]
            if curr_le != [0x00, 0x00, 0x00]:
                # 三级 27 解锁
                self.sd_tester.security_access_level_l2()
        # 设置使用模式
        self.sd_tester.io_control_usage_mode_control(mode_type)
        result = self.sd_tester.return_udsdata_and_check_and_print_response_result("Send dd0a to set usage mode")
        assert result[0] != 0x6F, '不应切换成功'
            

    @pytest.mark.full
    def test_usagemode_caseid_110000(self):
        '''
        1.非standstill状态
        2.从 Abandoned 诊断切换为 Inactive
        '''
        self.sd_tester.change_usage_mode(0)
        self.check_usage_mode_status(0)
        # self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 4)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00', 4)
        time.sleep(.3)
        self.not_change_usage_mode(1)
        self.check_usage_mode_status(0)

    @pytest.mark.Usagemode
    @pytest.mark.full
    def test_usagemode_caseid_109983(self):
        '''
        1.非standstill状态
        2.从 Abandoned 诊断切换为 DRIVING
        '''
        self.sd_tester.change_usage_mode(0)
        self.check_usage_mode_status(0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 4)
        time.sleep(.3)
        self.not_change_usage_mode(13)
        self.check_usage_mode_status(0)

    @pytest.mark.full
    def test_usagemode_caseid_109940(self):
        '''
        1.非standstill状态
        2.从 Abandoned 诊断切换为 ACTIVE
        '''
        self.sd_tester.change_usage_mode(0)
        self.check_usage_mode_status(0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 4)
        time.sleep(.3)
        self.not_change_usage_mode(11)
        self.check_usage_mode_status(0)

    @pytest.mark.full
    def test_usagemode_caseid_109917(self):
        '''
        1.非standstill状态
        2.从 Abandoned 诊断切换为 Convenience
        '''
        self.sd_tester.change_usage_mode(0)
        self.check_usage_mode_status(0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 4)
        time.sleep(.3)
        self.not_change_usage_mode(2)
        self.check_usage_mode_status(0)

    # @pytest.mark.xfail
    @pytest.mark.smoke
    @pytest.mark.verify
    def test_usagemode_caseid_109980(self):
        '''
        1.非standstill状态
        2.从 Inactive 诊断切换为 Convenience
        3.如果车辆状态从3变为0，则可以从inactive切到convenience
        '''
        self.sd_tester.change_usage_mode(1)
        self.check_usage_mode_status(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 4)
        time.sleep(.3)
        self.not_change_usage_mode(2)
        self.check_usage_mode_status(1)

    # @pytest.mark.xfail
    @pytest.mark.smoke
    def test_usagemode_caseid_110063(self):
        '''
        1.非standstill状态
        2.从Inactive诊断切换为 Active
        '''
        self.sd_tester.change_usage_mode(1)
        self.check_usage_mode_status(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 4)
        time.sleep(.3)
        self.not_change_usage_mode(11)
        self.check_usage_mode_status(1)

    @pytest.mark.sanity
    def test_usagemode_caseid_109920(self):
        '''
        1.非standstill状态
        2.从Inactive诊断切换为 Driving
        '''
        self.sd_tester.change_usage_mode(1)
        self.check_usage_mode_status(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 4)
        time.sleep(.3)
        self.not_change_usage_mode(13)
        self.check_usage_mode_status(1)

    @pytest.mark.sanity
    def test_usagemode_caseid_110144(self):
        '''
        1.非standstill状态
        2.从Inactive诊断切换为Abandoned
        '''
        self.sd_tester.change_usage_mode(1)
        self.check_usage_mode_status(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 4)
        time.sleep(.3)
        self.not_change_usage_mode(0)
        self.check_usage_mode_status(1)
        

    @pytest.mark.full
    def test_usagemode_caseid_109916(self):
        '''
        1.非standstill状态
        2.从Convenience诊断切换为Abandoned
        '''
        self.sd_tester.change_usage_mode(2)
        self.check_usage_mode_status(2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 4)
        time.sleep(.3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 4)
        self.not_change_usage_mode(0)
        self.check_usage_mode_status(2)

    @pytest.mark.full
    def test_usagemode_caseid_110077(self):
        '''
        1.非standstill状态
        2.从Convenience诊断切换为 Inactive
        '''
        self.sd_tester.change_usage_mode(2)
        self.check_usage_mode_status(2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 4)
        time.sleep(.3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 4)
        self.not_change_usage_mode(1)
        self.check_usage_mode_status(2)

    @pytest.mark.full
    def test_usagemode_caseid_110102(self):
        '''
        1.非standstill状态
        2.从Convenience诊断切换为 active
        '''
        self.sd_tester.change_usage_mode(2)
        self.check_usage_mode_status(2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 4)
        time.sleep(.3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 4)
        self.not_change_usage_mode(11)
        self.check_usage_mode_status(2)

    @pytest.mark.full
    def test_usagemode_caseid_110095(self):
        '''
        1.非standstill状态
        2.从Convenience诊断切换为 driving
        '''
        self.sd_tester.change_usage_mode(2)
        self.check_usage_mode_status(2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 4)
        time.sleep(.3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 4)
        self.not_change_usage_mode(13)
        self.check_usage_mode_status(2)

    @pytest.mark.full
    def test_usagemode_caseid_109950(self):
        '''
        1.非standstill状态
        2.从 Active 诊断切换为 Abandoned
        '''
        self.sd_tester.change_usage_mode(11)
        self.check_usage_mode_status(11)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 4)
        time.sleep(.3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 4)
        self.not_change_usage_mode(0)
        self.check_usage_mode_status(11)

    @pytest.mark.full
    def test_usagemode_caseid_110089(self):
        '''
        1.非standstill状态
        2.从Active诊断切换为Inactive
        '''
        self.sd_tester.change_usage_mode(11)
        self.check_usage_mode_status(11)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 4)
        time.sleep(.3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 4)
        self.not_change_usage_mode(1)
        self.check_usage_mode_status(11)

    @pytest.mark.full
    def test_usagemode_caseid_109964(self):
        '''
        1.非standstill状态
        2.从Active诊断切换为 CONVENIENCE
        '''
        self.sd_tester.change_usage_mode(11)
        self.check_usage_mode_status(11)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 4)
        time.sleep(.3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 4)
        self.not_change_usage_mode(2)
        self.check_usage_mode_status(11)

    @pytest.mark.full
    def test_usagemode_caseid_110133(self):
        '''
        "1.非standstill状态
        2.从Active诊断切换为 Driving "

        '''
        self.sd_tester.change_usage_mode(11)
        self.check_usage_mode_status(11)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 4)
        time.sleep(.3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 4)
        self.not_change_usage_mode(13)
        self.check_usage_mode_status(11)

    @pytest.mark.full
    def test_usagemode_caseid_109901(self):
        '''
        "1.非standstill状态
        2.从Driving诊断切换为Abandoned

        '''
        self.sd_tester.change_usage_mode(13)
        self.check_usage_mode_status(13)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 4)
        time.sleep(.3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 4)
        self.not_change_usage_mode(0)
        time.sleep(.5)
        self.check_usage_mode_status(13)

    @pytest.mark.full
    def test_usagemode_caseid_110123(self):
        '''
        "1.非standstill状态
        2.从Driving诊断切换为 inactive

        '''
        self.sd_tester.change_usage_mode(13)
        self.check_usage_mode_status(13)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 4)
        time.sleep(.3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 4)
        self.not_change_usage_mode(1)
        self.check_usage_mode_status(13)

    @pytest.mark.full
    def test_usagemode_caseid_110072(self):
        '''
        "1.非standstill状态
        2.从Driving诊断切换为 Active

        '''
        self.sd_tester.change_usage_mode(13)
        self.check_usage_mode_status(13)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 4)
        time.sleep(.3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt", 4)
        self.not_change_usage_mode(11)
        self.check_usage_mode_status(13)
# #################### Usagemode_不满足条件诊断切换  结束 ###########################################################
# ####################Usagemode诊断切换 退出#########################################################################

# @allure.feature("架构基础")
# @allure.story("整车模式")
# class TestChangeUsageMode2(TestBase):
#     def before_class(self, ecu):
#         super().before_class(self, ecu)
#         self.nucapp.bgm_diag_line_up()
#         # self.sd_tester = Sd_Tester(**self.tc_config)
#         # self.sd_tester.update_serverdoipid(0x1002)
#         # time.sleep(1)
#         # self.sd_tester.diagnostic_client_sim_start()
#         with allure.step(f"Test Class Pre Step can_lin_fr 启动"):
#             self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
#             self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
        
#     def before_each_func(self, ecu):
#         super().before_each_func(ecu)
#         #self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)


#     def after_each_func(self, ecu):
#         super().after_each_func(ecu)

#     def after_class(self, ecu):
#         self.sd_tester.change_usage_mode(1)
#         self.nucapp.bgm_diag_line_down()
#         self.sd_tester.stop_tester_present()
#         self.sd_tester.diagnostic_client_sim_close()
#         with allure.step(f"Test Class clearup Step can_lin_fr 停止"):
#             self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）
#             self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
#         super().after_class(self, ecu)

#     def check_usage_mode_status(self, expectedmode, do_assert=True, **kwargs):
#         '''
#         校验 usage 状态
#         @param expectedmode:
#         @param do_assert:
#         @param timeout:
#         @param kwargs:
#         @return:
#         '''
#         timeout = kwargs.get('timeout', 5)
#         # msg_signals_obj = kwargs.get('msg_signals_obj', self.ipdu.bodycan.CEMBodyFr12)
#         # signal_name = kwargs.get('signal_name', 'VehModMngtGlbSafe1UsgModSts_3_CEMBodySignalIPdu12')
#         msg_signals_obj = kwargs.get('msg_signals_obj', self.ipdu.backbonefr.CemBackBoneFr02)
#         signal_name = kwargs.get(
#             'signal_name', 'VehModMngtGlbSafe1UsgModSts_0_CEMBackBoneSignalIpdu02'
#         )
#         result, realvalue, expectedvalue = self.ipdu.check(msg_signals_obj=msg_signals_obj,
#                                                            signal_name=signal_name,
#                                                            sig_value_name=expectedmode,
#                                                            do_assert=do_assert, timeout=timeout, )

#         return result, realvalue, expectedvalue

    @pytest.mark.Usagemode_Quit
    @pytest.mark.sanity
    def test_usagemode_caseid_110071(self):
        '''
        1.standstill状态
        2.从 Abandoned 退出诊断
        '''
        self.sd_tester.change_usage_mode(0)
        self.check_usage_mode_status(0)
        self.sd_tester.quit_usage_mode()
        self.check_usage_mode_status(1)

    @pytest.mark.Usagemode_Quit
    @pytest.mark.sanity
    def test_usagemode_caseid_110078(self):
        '''
        1.standstill状态
        2.从 Inactive 退出诊断
        '''
        self.sd_tester.change_usage_mode(1)
        self.check_usage_mode_status(1)
        self.sd_tester.quit_usage_mode()
        self.check_usage_mode_status(1)

    @pytest.mark.Usagemode_Quit
    @pytest.mark.sanity
    def test_usagemode_caseid_110105(self):
        '''
        1.standstill状态
        2.从Convenience退出诊断
        '''
        self.sd_tester.change_usage_mode(2)
        self.check_usage_mode_status(2)
        self.sd_tester.quit_usage_mode()
        self.check_usage_mode_status(1)

    @pytest.mark.Usagemode_Quit
    @pytest.mark.sanity
    def test_usagemode_caseid_110057(self):
        '''
        1.standstill状态
        2.从 Active 退出诊断

        '''
        self.sd_tester.change_usage_mode(11)
        self.check_usage_mode_status(11)
        self.sd_tester.quit_usage_mode()
        self.check_usage_mode_status(1)

    @pytest.mark.Usagemode_Quit
    @pytest.mark.sanity
    def test_usagemode_caseid_109967(self):
        '''
        1.standstill状态
        2.从Driving退出诊断
        '''
        self.sd_tester.change_usage_mode(13)
        self.check_usage_mode_status(13)
        self.sd_tester.quit_usage_mode()
        self.check_usage_mode_status(1)


# #################### Usagemode_诊断切换退出  结束 ###########################################################


# pytest vmm/test_usage_mode.py
