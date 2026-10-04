import subprocess
import threading
import time

from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.soa_partner.src import partner_client
from xat_ecu.legacy.soa_partner.src.Operator import SOAOperator
from xat_cases.legacy.bgm.case_helper.environment_check import partner_process_check
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import partner_client_method_request, get_result, \
    get_message_name_can_or_lin, get_message_name_fr, send_bus_signal, send_can_wake_data, \
    parse_precondition_then_action
from xat_ecu.legacy.soa_partner.src.state import CAN_CONSTANT, UPSTREAM


pause_list = []
end_time = None


def init_soa_partner():
    """
    重启SOA_Partner
    """
    partner_process_check()
    CAN_CONSTANT.get_wanted_can = False
    global partner
    partner = SOAOperator("S2S", 16789)
    partner.run_operator()
    time.sleep(1)
    UPSTREAM.get_method_response = False
    partner_client.resp.clear()
    partner_client.resp_type.clear()


def down_soa_partner():
    global partner
    partner.stop_operator()
    time.sleep(3)


class case_description:
    """
    测试用例描述信息：前置条件列表、测试步骤列表
    """
    def __init__(self, pre_condition_list, step_list):
        self.pre_condition_list = pre_condition_list  # pre_condition_signal的对象的
        self.step_list = step_list  # step_description类的对象的集合


class pre_condition_signal:
    """
    前置条件类型1：发送总线信号 数据类型
    """
    def __init__(self, bus_name, message_id, signal_name, signal_value, e2e_flag="N"):
        self.bus_name = bus_name
        self.message_id = message_id
        self.signal_name = signal_name
        self.signal_value = signal_value
        self.e2e_flag = e2e_flag

    def to_string(self):
        return f"{self.bus_name}:{self.message_id}:{self.signal_name}:{self.signal_value}:{self.e2e_flag}"


class pre_condition_usage_mode:
    """
    切换用户使用模式
    示例1：usagemode=11
    示例2：usagemode=11,13
    """
    def __init__(self, mode_str, keyword="usagemode"):
        self.keyword = keyword
        self.mode_str = mode_str

    def to_string(self):
        return f"{self.keyword}={self.mode_str}"


class pre_condition_car_mode:
    """
    切换car mode
    示例1：car_mode=0
    """
    def __init__(self, mode_str, keyword="car_mode"):
        self.keyword = keyword
        self.mode_str = mode_str

    def to_string(self):
        return f"{self.keyword}={self.mode_str}"


class pre_condition_stop_signal_then_resume:

    def __init__(self, bus, message_id, second, keyword="stop_send_pdu_then_resume"):
        self.bus = bus
        self.message_id = message_id
        self.second = second
        self.keyword = keyword

    def to_string(self):
        return f"{self.keyword}={self.bus}:{self.message_id}:{self.second}"


class pre_condition_configure_word:
    """
    配置字设置
    示例：configure_word=58:2
    """
    def __init__(self, key, value, keyword="configure_word"):
        self.keyword = keyword
        self.word_str = f"{key}:{value}"

    def to_string(self):
        return f"{self.keyword}={self.word_str}"


class pre_condition_run:
    """
    一个或者多个前置条件的数据结构描述并执行
    """
    def __init__(self, tb_config, pdu_obj, pre_condition_list, sd_test):
        self.tb_config = tb_config
        self.pdu_obj = pdu_obj
        self.pre_condition_list = pre_condition_list
        self.sd_test = sd_test

    def do_run(self):
        """
        发送一个或者多个总线信号
        """
        logger.info(f"前置条件中要求的信号：{self.pre_condition_list}")
        if len(self.pre_condition_list) > 1:
            pre_condition = "\n".join(self.pre_condition_list)
        else:
            pre_condition = self.pre_condition_list[0]
        parse_precondition_then_action(pre_condition, self.tb_config, self.pdu_obj, self.sd_test)


class step_description:
    """
    1、一个具体的测试步骤描述数据结构：action_description_list、expected_result_list
    2、action_description的长度 等于 expected_result的长度，且一一对应，每一个动作对应一个预期结果
    """
    def __init__(self, action, expected):
        self.action = action
        self.expected = expected


class action_run_partner:
    """
    step_action1: 执行soa partner的方法 数据结构 及 执行方法
    """
    def __init__(self, service_name, method_name, method_parameter, action_type="method", style="down"):
        self.service_name = service_name
        self.method_name = method_name
        self.method_parameter = method_parameter
        self.action_type = action_type
        self.style = style

    def action_run(self):
        partner_client_method_request(self.service_name, self.method_name,
                                      self.method_parameter, "method", self.style)


class action_change_usage_mode:
    def __init__(self, usage_mode, sd_test):
        self.usage_mode = usage_mode
        self.sd_test = sd_test

    def action_run(self):
        curr_mode = self.sd_test.change_usage_mode(int(self.usage_mode), do_assert=True)  # 如果切换使用模式失败，则用例停止执行
        logger.info(f"====curr_mode================ {curr_mode} ==========================")
        time.sleep(2)


class action_send_bus_signal:
    """
    step_action2: 发送总线信号 数据结构 及 执行方法
    """
    def __init__(self, tb_config, pdu_obj, bus_name, message_id, signal_name, signal_value, e2e_flag="N"):
        self.tb_config = tb_config
        self.pdu_obj = pdu_obj
        self.bus_name = bus_name  # 列表
        self.message_id = message_id  # 列表
        self.signal_name = signal_name  # 列表
        self.signal_value = signal_value  # 列表
        self.e2e_flag = e2e_flag  # 列表
        self.action_type = 'signal'

    def action_run(self):
        CAN_CONSTANT.send_can_begin = True
        for i in range(len(self.bus_name)):
            bus_name1 = self.tb_config["bus"][self.bus_name[i]]
            th1 = threading.Thread(target=send_can_wake_data, args=(bus_name1, self.bus_name[i]))
            th1.start()  # 唤醒报文持续发送1秒
            """发送一个can、lin、FR报文"""
            send_bus_signal(self.pdu_obj, self.bus_name[i], self.message_id[i],
                            self.signal_name[i], self.signal_value[i])


class action_stop_bus:
    def __init__(self, pdu_obj, bus_name):
        self.pdu_obj = pdu_obj
        self.bus_name = bus_name
        self.action_type = 'stop_bus'

    def action_run(self):
        logger.info(f"开始停止总线{self.bus_name}")
        self.pdu_obj.pause_bus_send(self.bus_name)
        pause_list.append(self.bus_name)
        time.sleep(2)


class action_ecu_restart:
    def __init__(self, nuc_app, ecu_type, sleep_time=120):
        self.nuc_app = nuc_app
        self.ecu_type = ecu_type
        self.action_type = 'ecu_restart'
        self.sleep_time = sleep_time

    def action_run(self):
        """
        重启ECU：domain为域名，可选值：bgm、tcam、cdc、acu
        """
        logger.info("ecu restart")
        if self.ecu_type == 'bgm':
            self.nuc_app.bgm_power_off()
            time.sleep(self.sleep_time)
            self.nuc_app.bgm_power_on()
        else:
            logger.info("ecu_restart not support!!!")


class expected_bus_signal:
    """
    expected_result: 收到总线信号 数据结构
    """
    def __init__(self, pdu_obj, tb_config, bus_name, message_id, signal_name, signal_value):
        self.pdu_obj = pdu_obj
        self.tb_config = tb_config
        self.bus_name = bus_name
        self.message_id = message_id
        self.signal_name = signal_name
        self.signal_value = signal_value

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
                                        int(self.signal_value[0]), 20, do_assert=False)
        if action_to_run:
            action_to_run.action_run()  # 执行对应的action行为

        result, real_value, expected_value = self.pdu_obj.check_thread_stop(self.signal_name[0], timeout=40)
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
    def __init__(self, service_name, method_name, method_parameter, expected_result, action_type="event"):
        self.service_name = service_name
        self.method_name = method_name
        self.method_parameter = method_parameter
        self.expected_result = expected_result
        self.action_type = action_type

    def expected_run(self, action_to_run):
        """
        启动总线监听后执行对应的action，返回值为监听的结果是否满足预期：True代表满足，False代表不满足；
        action_to_run为 None，则不执行任何动作
        """
        init_soa_partner()
        if action_to_run and action_to_run.action_type == 'method':
            if self.action_type == 'method':
                action_to_run.action_run()  # 执行方法请求
                th = threading.Thread(target=partner_client_method_request,
                                      args=(self.service_name, self.method_name,
                                            self.method_parameter, self.action_type))
                th.setDaemon(True)
                th.start()
                logger.info(f"期望的结果：{self.expected_result}")
                result = get_result(self.expected_result, self.action_type)
                down_soa_partner()
                return result
            else:
                partner_client.event_name = "Update{}Event".format(self.method_name)
                action_to_run.action_run()  # 执行方法请求
                logger.info(f"event_name：{partner_client.event_name}")
                logger.info(f"期望的结果：{self.expected_result}")
                result = get_result(self.expected_result, self.action_type)
                down_soa_partner()
                return result
        else:  # action 不是方法请求
            th = threading.Thread(target=partner_client_method_request,
                                  args=(self.service_name, self.method_name,
                                        self.method_parameter, self.action_type))
            th.setDaemon(True)
            th.start()
            if action_to_run:
                action_to_run.action_run()  # 执行对应的action行为
            result = get_result(self.expected_result, self.action_type)
            down_soa_partner()
            return result


def candump_check(can_bus, can_id, to_str, iter_total=400):
    """
    通过candump命令来获取帧报文发生跳变时刻的时间戳，捕获到的时间戳保存在全局变量 end_time 中，捕获失败 end_time 为None
    can_bus: 例如can4
    can_id：帧报文ID
    from_str：跳变前字符串
    to_str：跳变后字符串
    iter_total：捕获次数，默认400次
    """
    cmd = f'candump -ta {can_bus},{can_id}:7FF'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')

    iter_num = 0
    last_line = ""
    global end_time
    end_time = None
    start_time = time.time()

    while p.poll() is None:
        if iter_num > iter_total:
            p.terminate()
            p.wait()
            # os.killpg(p.pid, signal.SIGTERM)
            logger.info("执行失败，程序退出")
            break
        line = p.stdout.readline()
        line = line.strip()
        if line:
            if iter_num == 0:
                last_line = line
            curr_line = line
            if to_str not in last_line and to_str in curr_line:
                end_time = float(curr_line.split(" ")[0][1:-2])
                if end_time > start_time:
                    p.terminate()
                    p.wait()
                    logger.info("执行成功，程序退出")
                else:
                    end_time = None
            else:
                last_line = curr_line
        iter_num = iter_num + 1


if __name__ == '__main__':

    # 循环开始
    th1 = threading.Thread(target=candump_check, args=("can4", "020", "08 10 08 0B AA 00 00 61"))
    th1.stop_event = threading.Event()
    th1.start()
    # 执行soa partner的方法

    th1.join(2)
    th1.stop_event.set()

    if end_time:
        # 时间相减
        pass
    else:
        # 本次执行失败，不需要时间相减
        pass
