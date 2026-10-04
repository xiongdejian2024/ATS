import os, time
import sys,logging
import pytest
from xat_ecu.legacy.sdk.digital_key.digital_key_class import DigitalKey
from xat_cases.legacy.bgm.case_helper.test_base import TestBase
import allure
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from time import sleep
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))

@allure.feature("架构基础")
@allure.story("整车模式/维修模式")
class TestDiagMaintainMode(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.sd_tester = Sd_Tester(**self.tc_config)
        self.nucapp.bgm_diag_line_up()
        self.sd_tester.diagnostic_client_sim_start()
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        with allure.step(f"Test Class Pre Step can_lin_fr 启动"):
            self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        # self.change_car_mode_to_unmaintain()
        self.nucapp.bgm_diag_line_down()
        with allure.step(f"Test Class clearup Step can_lin_fr 停止"):
            self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）
            self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        self.sd_tester.diagnostic_client_sim_close()
        super().after_class(self, ecu)

    def change_car_mode_to_maintain(self, do_assert=True, **kwargs):
        '''
        诊断切换到 维修模式
        @return: True 切换成功 False 切换失败
        '''
        result = self.set_maintain_mode(do_assert=False, ipdu=self.ipdu)
        logging.info(F"切换到维修模式 {'成功' if result else '失败'}")
        if do_assert:
            assert result, f"切换到维修模式失败 "
        return result
 
    def change_car_mode_to_unmaintain(self, do_assert=True, **kwargs):
        '''
        诊断切换到 非维修模式  退出维修模式
        @return: True 切换成功 False 切换失败
        '''
        result = self.set_unmaintain_mode(do_assert=False, ipdu=self.ipdu)
        logging.info(F"退出维修模式 {'成功' if result else '失败'}")
        if do_assert:
            assert result, f"退出维修模式失败 "
        return result
    
    def get_maintain_mode(self):
        self.sd_tester.send_data([0x22, 0xB3, 0x02])
        result = self.sd_tester.return_udsdata_and_check_and_print_response_result(
            "向1001发送  0x22, 0xB3,0x02"
        )[3:]
        curr_mode = result[0]

        if curr_mode == 1:
            return True
        else:
            return False

    def set_maintain_mode(self, do_assert=True, **kwargs):
        '''
            进入维修模式
            前置条件
                车辆处于非维修模式
            返回 True 是设置展车模式成功，返回 False 设置失败
        '''
        self.sd_tester.update_serverdoipid(0x1001)
        ret = self.get_maintain_mode()
        if ret:
            return ret
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
            self.sd_tester.security_access_level_l3()
        else:
            # 判断是否需要解锁
            self.sd_tester.client_sim.send_data([0x27, 0x05])
            result = self.sd_tester.return_udsdata_and_check_and_print_response_result("Send 0x27, 0x05 to get result")
            curr_le = result[2:]
            if curr_le != [0x00, 0x00, 0x00]:
                # 三级 27 解锁
                self.sd_tester.security_access_level_l3()
        # 设置使用模式
        self.sd_tester.client_sim.send_data([0x2e, 0xb3, 0x02, 0x01])
        result = self.sd_tester.return_udsdata_and_check_and_print_response_result("Send 2eb3 to set maintain mode")
        curr_status = result[0]
        if do_assert and curr_status != 0x6E:
            assert 0, f'设置维修模式失败'
        # sleep(0.5)
        # 接受数据
        ret = self.get_maintain_mode()
        if do_assert:
            assert ret, f'设置维修模式失败'
        return ret
    
    def set_unmaintain_mode(self, do_assert=True, **kwargs):
        '''
        退出维修模式
        返回 True 是退出维修模式成功，返回 False 退出失败
        @return:
        '''
        self.sd_tester.update_serverdoipid(0x1001)
        ret = self.get_maintain_mode()
        if ret:
            return ret
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
            self.sd_tester.security_access_level_l3()
        else:
            # 判断是否需要解锁
            self.sd_tester.client_sim.send_data([0x27, 0x05])
            result = self.sd_tester.return_udsdata_and_check_and_print_response_result("Send 0x27, 0x05 to get result")
            curr_le = result[2:]
            if curr_le != [0x00, 0x00, 0x00]:
                # 三级 27 解锁
                self.sd_tester.security_access_level_l3()
        # 设置使用模式
        self.sd_tester.client_sim.send_data([0x2e, 0xb3, 0x02, 0x00])
        result = self.sd_tester.return_udsdata_and_check_and_print_response_result("Send b302 to set maintain mode")
        curr_status = result[0]
        if do_assert and curr_status != 0x6e:
            assert 0, f'设置维修模式失败'
        # sleep(0.5)
        # 接受数据
        ret = self.get_maintain_mode()
        if do_assert:
            assert not ret, f'设置维修模式失败'
        return not ret
    
    @pytest.mark.smoke
    @pytest.mark.verify  
    def test_enter_maintain_mode_caseid_118591(self):
        '''诊断切维修模式'''
        self.change_car_mode_to_maintain()
    
    @pytest.mark.smoke
    def test_exit_maintain_mode_caseid_118590(self):
        '''诊断退维修模式'''
        self.change_car_mode_to_unmaintain()

    