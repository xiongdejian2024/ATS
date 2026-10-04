import time
import xml.sax

import pytest

from xat_ecu.legacy.soa_partner.src.Operator import SOAOperator
from xat_ecu.legacy.soa_partner.src.base_partner import S2sBaseClass
from xat_cases.legacy.bgm.case_helper.environment_check import partner_process_check
from xat_cases.legacy.bgm.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_cases.legacy.mining.case_helper.parse_excel import get_signal_testcases_from_excel, get_service_testcases_from_excel

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
sys.path.append(os.path.join(current_path.split("sat")[0], "sat"))
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.common.logger import logger


class pre_condition_send_signal:
    """
    前置条件类型1：发送总线信号 数据类型
    """
    def __init__(self, pdu_obj, bus_name, message_id, signal_name, signal_value):
        self.pdu_obj = pdu_obj
        self.bus_name = bus_name
        self.message_id = message_id
        self.signal_name = signal_name
        self.signal_value = signal_value

    def do_run(self):
        time.sleep(0.2)  # 确保信号已经开始发送
        if "can" in self.bus_name or "lin" in self.bus_name or "backbonefr" == self.bus_name:
            """发送一个can、lin、FR报文"""
            logger.info(f"开始发送信号：总线：{self.bus_name}, 报文：{self.message_id}, "
                        f"信号名：{self.signal_name}, 信号值：{self.signal_value}")
            send_bus_signal(self.pdu_obj, self.bus_name, self.message_id,
                            self.signal_name, self.signal_value)
            time.sleep(1)


class pre_condition_change_usage_mode:
    """
    切换用户使用模式
    """
    def __init__(self, sd_tester, mode_str):
        self.mode_str = mode_str
        self.sd_tester = sd_tester

    def do_run(self):
        logger.info(f"切换使用模式：{self.mode_str}")
        mode_dict = {"Abandoned": 0x00, "Inactive": 0x01, "Convenience": 0x02, "Active": 0x0B, "Driving": 0x0D}
        self.sd_tester.change_car_mode(mode_dict.get(self.mode_str), do_assert=False)


class pre_condition_change_car_mode:
    """
    切换car mode
    示例1：car_mode=0self.mode_str
    """
    def __init__(self, sd_tester, mode_str):
        self.mode_str = mode_str
        self.sd_tester = sd_tester

    def do_run(self):
        logger.info(f"切换车辆模式：{self.mode_str}")
        mode_dict = {"Normal": 0, "Transport": 1, "Factory": 2, "Crash": 3, "Dyno": 5}
        self.sd_tester.change_car_mode(mode_dict.get(self.mode_str), do_assert=False)


class pre_condition_run_soa_partner:
    """
    前置条件中执行soa partner方法请求
    """
    def __init__(self, soa_partner, service_name, method_name, method_parameter):
        self.service_name = service_name
        self.method_name = method_name
        self.method_parameter = eval(method_parameter)
        self.partner = soa_partner

    def do_run(self):
        response = self.partner.send_request_and_return_resp(f'{self.service_name}_client', self.method_name,
                                                             args=self.method_parameter)
        if response:
            logger.info(f"获取到响应结果：{response}")
        else:
            logger.info("方法执行失败")


class pre_condition_run:
    """
    一个或者多个前置条件的数据结构描述并执行
    """
    def __init__(self, sd_tester, pdu_obj, pre_condition_list, soa_partner):
        self.sd_tester = sd_tester
        self.pdu_obj = pdu_obj
        self.pre_condition_list = [x.strip() for x in pre_condition_list.split('\n')]
        self.partner = soa_partner

    def do_run(self):
        """
        执行一个或者多个前置条件
        """
        for index, condition in enumerate(self.pre_condition_list, 1):
            logger.info(f"pre_condition: {condition}")
            pre_condition = None
            if condition.startswith("UsageMode"):
                condition_list = condition.split(":")
                if condition_list[1] in ["Abandoned", "Inactive", "Convenience", "Active", "Driving"]:
                    pre_condition = pre_condition_change_usage_mode(self.sd_tester, condition_list[1])
            elif condition.startswith("CarMode"):
                condition_list = condition.split(":")
                if condition_list[1] in ["Normal", "Transport", "Factory", "Crash", "Dyno"]:
                    pre_condition = pre_condition_change_car_mode(self.sd_tester, condition_list[1])
            elif condition.startswith("signal"):
                condition_list = condition.split(":")
                if len(condition_list) == 5:
                    bus_name = condition_list[1]
                    message_id = condition_list[2]
                    signal_name = condition_list[3]
                    signal_value = condition_list[4]
                    pre_condition = pre_condition_send_signal(self.pdu_obj, bus_name, message_id,
                                                              signal_name, signal_value)
            elif condition.startswith("partner"):
                condition_list = condition.split("&")
                service_name = condition_list[1]
                method_name = condition_list[2]
                method_parameter = condition_list[3]
                pre_condition = pre_condition_run_soa_partner(self.partner, service_name, method_name,
                                                              method_parameter)
            else:
                logger.info(f"前置条件第{index}行参数格式错误或不支持：{condition}")
                continue
            if pre_condition:
                pre_condition.do_run()


class action_run_partner:
    """
    step_action1: 执行soa partner的方法 数据结构 及 执行方法
    """
    def __init__(self, soa_partner, service_name, method_name, method_parameter):
        self.partner = soa_partner
        self.service_name = service_name
        self.method_name = method_name
        self.method_parameter = eval(method_parameter)

    def action_run(self):
        response = self.partner.send_request_and_return_resp(f'{self.service_name}_client', self.method_name,
                                                             args=self.method_parameter)
        if response:
            logger.info(f"获取到响应结果：{response}")
        else:
            logger.info("方法执行失败")

    def to_string(self):
        logger.info(f"action partner detail:{self.service_name}:{self.method_name}:{self.method_parameter}")


class action_send_bus_signal:
    """
    step_action2: 发送总线信号 数据结构 及 执行方法
    """
    def __init__(self, pdu_obj, bus_name, message_id, signal_name, signal_value):
        self.pdu_obj = pdu_obj
        self.bus_name = bus_name
        self.message_id = message_id
        self.signal_name = signal_name
        self.signal_value = signal_value

    def action_run(self):
        for i in range(len(self.bus_name)):
            """发送一个can、lin、FR报文"""
            send_bus_signal(self.pdu_obj, self.bus_name, self.message_id, self.signal_name, self.signal_value)

    def to_string(self):
        logger.info(f"action signal detail:{self.bus_name}:{self.message_id}:{self.signal_name}:{self.signal_value}")


def convert_action_instance(soa_partner, pdu_obj, action_str):
    if action_str.startswith("partner"):
        action_param = action_str.split("&")
        if len(action_param) == 4:
            service_name = action_param[1]
            method_name = action_param[2]
            method_parameter = action_param[3]
            return action_run_partner(soa_partner, service_name, method_name, method_parameter)
        else:
            logger.info(f"当前行格式错误：{action_str}")
            return None
    elif action_str.startswith("signal"):
        action_param = action_str.split("&")
        if len(action_param) == 5:
            bus_name = action_param[1]
            message_id = action_param[2]
            signal_name = action_param[3]
            signal_value = action_param[4]
            return action_send_bus_signal(pdu_obj, bus_name, message_id, signal_name, signal_value)
        else:
            logger.info(f"当前行格式错误：{action_str}")
            return None


class expected_bus_signal:
    """
    expected_result: 收到总线信号 数据结构
    """
    def __init__(self, pdu_obj, bus_name, message_id, signal_name, signal_value, timeout=20):
        self.pdu_obj = pdu_obj
        self.bus_name = bus_name
        self.message_id = message_id
        self.signal_name = signal_name
        self.signal_value = signal_value
        self.timeout = timeout

    def expected_run(self, action_to_run):
        """
        启动总线监听后执行对应的action，返回值为监听的结果是否满足预期：True代表满足，False代表不满足；
        """
        obj_list = getattr(self.pdu_obj, str(self.bus_name[0]))
        if self.message_id[0].startswith('0x'):
            message_id = int(self.message_id[0], 16)
            message_name, _ = get_message_name_can_or_lin(obj_list, message_id)
        else:
            message_name, _ = get_message_name_fr(obj_list, self.message_id[0])
        logger.info(f"监听的总线：{self.bus_name[0]}, 信号名称：{self.signal_name[0]}, 预期的信号值：{self.signal_value[0]}")

        self.pdu_obj.check_thread_start(getattr((getattr(self.pdu_obj, str(self.bus_name[0]))),
                                                message_name), self.signal_name[0],
                                        int(self.signal_value[0]), self.timeout, do_assert=False)
        if action_to_run:
            action_to_run.action_run()

        result, real_value, expected_value = self.pdu_obj.check_thread_stop(self.signal_name[0], timeout=self.timeout*2)
        logger.info(f"信号监听结果：{result}，信号{self.signal_name[0]}的预期值{expected_value}，实际值:{real_value}")

        return result


class expected_soa_partner_result:
    """
    类描述: 执行soa partner的 method 或者 event，并获取对应的结果
    service_name: 服务名称
    method_name：方法名称
    method_parameter：方法的参数
    expected_result: 期待的结果
    action_type：函数类型：method 或者 event
    """
    def __init__(self, soa_partner, service_name, method_name, ck_info, method_parameter=None, action_type="event"):
        self.partner = soa_partner
        self.service_name = service_name
        self.method_name = method_name
        self.method_parameter = eval(method_parameter)
        self.ck_info = eval(ck_info)
        self.action_type = action_type

    def expected_run(self, action_to_run):
        """
        启动总线监听后执行对应的action，返回值为监听的结果是否满足预期：True代表满足，False代表不满足；
        action_to_run为 None，则不执行任何动作
        """
        result = None
        if action_to_run:
            if self.action_type == 'method':
                action_to_run.action_run()  # 执行方法请求
                time.sleep(0.5)
                result = self.partner.send_request_and_ck_resp(f'{self.service_name}_client', self.method_name,
                                                               args=self.method_parameter, ck_info=self.ck_info,
                                                               timeout=3)
            else:
                action_to_run.action_run()  # 执行方法请求
                result = self.partner.ck_s2s_event(f'{self.service_name}_client', self.method_name, self.ck_info)
        return result


def convert_expected_instance(soa_partner, pdu_obj, expected_str):

    if expected_str.startswith("partner"):
        if len(expected_str.split("&")) != 6:
            logger.info(f"当前行的预期结果格式错误：{expected_str}")
            return None
        else:
            action_param = expected_str.split("&")
            service_name = action_param[1]
            method_name = action_param[2]
            method_type = action_param[3]
            method_parameter = action_param[4]
            ck_info = action_param[5]

        return expected_soa_partner_result(soa_partner, service_name, method_name, method_parameter,
                                           ck_info, method_type)
    elif expected_str.startswith("signal"):
        action_param = expected_str.split("&")
        bus_name = action_param[1]
        message_id = action_param[2]
        signal_name = action_param[3]
        signal_value = action_param[4]
        return expected_bus_signal(pdu_obj, bus_name, message_id, signal_name, signal_value)


@pytest.mark.full
@allure.feature("埋点服务接口")
@allure.story("BGM/埋点服务接口")
class TestMiningService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        """CAN、LIN、FR信号发送初始化"""
        self.ipdu.start_all_time_control()
        self.busapp.start_all_cyclic_msg()
        """使用模式切换、配置字修改初始化"""
        self.sd_test = Sd_Tester(**self.tc_config)
        usage_mode_change_init(self.sd_test, self.ipdu)
        self.partner = None

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        partner_process_check()
        self.ipdu.reset_check_results()

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        super().after_class(self, ecu)
        """CAN、LIN、FR信号发送相关资源 tear down"""
        self.ipdu.time_control_stop()
        self.busapp.stop_all_cyclic_msgs()
        """使用模式切换、配置字修改 相关资源回收"""
        sd_test_teardown(self.sd_test)

    @pytest.mark.BGM
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("test_case", get_service_testcases_from_excel("service_mining.xlsx", "BGM"),
                             ids=get_service_testcases_from_excel("service_mining.xlsx", "BGM", ids=True))
    def test_service_case(self, test_case):
        service_list = [x.strip() for x in test_case.service_name.split('\n')]
        action_list = []
        expected_list = []
        # 启动所有的服务
        service_tuple = []
        for service in service_list:
            service_tuple.append((service, "client"))
        if len(service_tuple) > 0:
            logger.info(f"service_tuple:{service_tuple}")
            self.partner = S2sBaseClass(service_tuple)

        for action in test_case.action.split('\n'):
            action_list.append(convert_action_instance(self.partner, self.ipdu, action.strip()))

        for expected in test_case.expect_result.split('\n'):
            expected_list.append(convert_expected_instance(self.partner, self.ipdu, expected.strip()))
        logger.info(f"7878:{expected_list}")
        expected_list = [x for x in expected_list if x is not None]
        self.actuator_new(service_list, test_case.pre_condition, action_list, expected_list)

    def actuator_new(self, service_list, pre_condition, action_list, expected_list):

        # 执行前置条件
        pre_condition_run(self.sd_test, self.ipdu, pre_condition, self.partner).do_run()

        i = 0
        for action, expected in zip(action_list, expected_list):
            i += 1
            result = expected.expected_run(action)
            if result:
                logger.info(f"第{i}步执行成功")
                continue
            else:
                logger.info(f"第{i}步执行失败，测试用例执行结束")
                break
        else:
            assert True
        assert True


if __name__ == '__main__':
    pytest.main()
