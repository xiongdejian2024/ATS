import sys
import time
import os
import threading
from collections.abc import Iterable
from decimal import Decimal
import allure
from xat_ecu.legacy.driver.can_listener import *

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
sys.path.append(os.path.join(current_path.split("sat")[0], "sat"))
from xat_cases.legacy.bgm.s2s.case_helper.parse_excel import *
from xat_ecu.legacy.driver.socket_can import SocketCan
from xat_ecu.legacy.soa_partner.src import partner_client
sys.path.append(os.path.join(current_path.split("sat")[0], "sat/tools"))
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.soa_partner.src.state import UPSTREAM, CAN_CONSTANT, CASE_RUN, DOWNSTREAM


def parse_precondition_then_action(pre_condition, tb_config, pdu_obj, sd_test):
    """解析前置条件并完成相应动作"""
    conn_str = pre_condition.replace('\n', '、')
    if len(conn_str) > 0:
        logger.info(f"获得到的当前用例的前置条件：{conn_str}")
    """发送CAN、LIN、FR信号"""
    if len(pre_condition) > 0:
        """2、获取并设置使用模式（usage_mode）"""
        usage_mode = get_pre_condition_usage_mode(pre_condition)  # 获取前置条件中的使用模式需求
        if isinstance(usage_mode, list):  # 如果返回的是一个list类型对象
            change_usage_mode(sd_test, usage_mode)
        else:  # 如果前置条件中的使用模式为空，则默认切换到11
            change_usage_mode(sd_test, ["11"])
        """3、获取并设置car模式（car_mode）"""
        car_mode = get_pre_condition_car_mode(pre_condition)  # 获取前置条件中的使用模式需求
        if isinstance(car_mode, list):  # 如果返回的是一个list类型对象
            change_car_mode(sd_test, car_mode)
        else:  # 如果前置条件中的车辆模式为空，则默认切换到normal
            change_car_mode(sd_test, ['0'])
        """5、获取并设置需要设置的 ”配置字“ """
        configure_word_info = get_pre_condition_configure_word(pre_condition)
        if len(configure_word_info) > 0:
            configure_word_write(sd_test, configure_word_info)
        # """4、获取并设置需要停止的信号"""
        # stop_send_signals = get_pre_condition_stop_send_signals(pre_condition)
        # if len(stop_send_signals) > 0:
        #     stop_send_signals_operation(stop_send_signals, tb_config, pdu_obj)
        """1、获取并设置需要发送的信号"""
        pre_condition_case = get_pre_condition_case(pre_condition)
        send_bus_signals(tb_config, pdu_obj, pre_condition_case)
    else:  # 如果前置条件为空，则默认使用模式切换到11，车辆模式默认normal
        change_usage_mode(sd_test, ["11"])
        change_car_mode(sd_test, ['0'])


def get_pre_condition_case(pre_condition):
    """
    获取前置条件中需要发送的CAN、LIN、FR信号
    """
    channel_list = []
    message_id_list = []
    signal_name_list = []
    signal_value_list = []
    condition_list = pre_condition.split('\n')
    for condition in range(len(condition_list)):
        signal = condition_list[condition].split(":")
        if len(signal) == 4:
            channel_list.append(signal[0])
            message_id_list.append(signal[1])
            signal_name_list.append(signal[2])
            signal_value_list.append(signal[3])
    if len(channel_list) > 0:
        logger.info(f"当前用例前置条件中需要发送的信号信息：")
        logger.info(f"总线列表:{channel_list}")
        logger.info(f"报文ID：{message_id_list}")
        logger.info(f"信号名列表：{signal_name_list}")
        logger.info(f"信号值列表：{signal_value_list}")
    pre_condition_case = testCase(channel_list, message_id_list, signal_name_list, signal_value_list)
    return pre_condition_case


def get_pre_condition_usage_mode(pre_condition):
    """
    获取前置条件中需要切换的使用模式
    """
    condition_list = pre_condition.split('\n')
    for condition in range(len(condition_list)):
        usage_mode = condition_list[condition].split("=")
        if len(usage_mode) == 2:
            if usage_mode[0] == 'usagemode':
                logger.info(f"当前用例需要切换的usage mode：{usage_mode[1]}")
                return usage_mode[1].split(',')
    else:
        return False


def get_pre_condition_car_mode(pre_condition):
    """
    获取前置条件中需要切换的使用模式
    """
    condition_list = pre_condition.split('\n')
    for condition in range(len(condition_list)):
        car_mode = condition_list[condition].split("=")
        if len(car_mode) == 2:
            if car_mode[0] == 'car_mode':
                logger.info(f"当前用例需要切换的car mode：{car_mode[1]}")
                return car_mode[1].split(',')
    else:
        return False


def get_pre_condition_stop_send_signals(pre_condition):
    """
    获取前置条件中信号停发的相关诉求行
    """
    conditions_stop_send_signals = []
    condition_list = pre_condition.split('\n')
    for num in range(len(condition_list)):
        stop_send_signal = condition_list[num].split("=")
        if stop_send_signal[0] == 'continue_send_signal_seconds':
            conditions_stop_send_signals.append(condition_list[num])
        # if stop_send_signal[0] in ['stop_send_pdu', 'stop_send_pdu_then_resume']:
        if stop_send_signal[0] in ['stop_send_pdu']:
            if "can" in stop_send_signal[1].split(":")[0]:
                conditions_stop_send_signals.append(condition_list[num])
            else:
                bus_name = stop_send_signal[1].split(":")[0]
                logger.info(f"目前仅支持CAN信号的停发！！！，不支持{bus_name}")
    if len(conditions_stop_send_signals) > 0:
        logger.info(f"需要停发及恢复的信号信息：{conditions_stop_send_signals}")
    return conditions_stop_send_signals


def get_pre_condition_configure_word(pre_condition):
    """
    获取前置条件中的配置字诉求
    """
    condition_list = pre_condition.split('\n')
    for num in range(len(condition_list)):
        configure_word = condition_list[num].split("=")
        if configure_word[0] == 'configure_word':
            logger.info(f"当前用例中前置条件中的配置字为：{configure_word[1]}")
            return configure_word[1]
    else:
        return ""


class testCase:
    """
    测试用例信号部分简写
    """
    def __init__(self, channel, message_id, signal_name, signal_value=0):
        self.channel = channel
        self.message_id = message_id
        self.signal_name = signal_name
        self.signal_value = signal_value


def send_bus_signals(tb_config, pdu_obj, test_case):
    """
    测试用例中的多个总线信号发送
    """
    time.sleep(0.2)  # 确保信号已经开始发送
    for i in range(len(test_case.channel)):
        if "can" in test_case.channel[i] or "lin" in test_case.channel[i] or "backbonefr" == test_case.channel[i]:
            bus_name1 = tb_config["bus"][test_case.channel[i]]
            th1 = threading.Thread(target=send_can_wake_data, args=(bus_name1, test_case.channel[i]))
            th1.start()  # 唤醒报文持续发送1秒
            """发送一个can、lin、FR报文"""
            logger.info(f"开始发送{test_case.channel[i]}信号{test_case.signal_name[i]}，值为{test_case.signal_value[i]}")
            send_bus_signal(pdu_obj, test_case.channel[i], test_case.message_id[i],
                            test_case.signal_name[i], test_case.signal_value[i])


def send_bus_signals_V2(tb_config, pdu_obj, test_case):
    """
    测试用例中的多个总线信号发送
    """
    time.sleep(0.2)  # 确保信号已经开始发送
    if "can" in test_case.bus_name or "lin" in test_case.bus_name or "backbonefr" == test_case.bus_name:
        bus_name1 = tb_config["bus"][test_case.bus_name]
        th1 = threading.Thread(target=send_can_wake_data, args=(bus_name1, test_case.bus_name))
        th1.start()  # 唤醒报文持续发送1秒
        """发送一个can、lin、FR报文"""
        logger.info(f"开始发送{test_case.bus_name}信号{test_case.signal_name}，值为{test_case.signal_value}")
        send_bus_signal(pdu_obj, test_case.bus_name, test_case.message_id,
                        test_case.signal_name, test_case.signal_value)
        time.sleep(1)


def stop_send_signals_operation(stop_send_signals, tb_config, pdu_obj):
    """
    测试用例执行期间，停止发送总线信号一段时间或永久
    stop_send_signals：列表类型
    """
    for stop_send_signal in stop_send_signals:
        command = stop_send_signal.split("=")[0]
        detail = stop_send_signal.split("=")[1]
        info = detail.split(":")
        if command == 'continue_send_signal_seconds':
            UPSTREAM.check_count = int(info[0])+5
            UPSTREAM.check_interval = int(info[1])
            UPSTREAM.partner_main_wait_second = int(info[0])*int(info[1])
            UPSTREAM.method_loop_count = int(info[0])+5
            UPSTREAM.method_loop_interval = int(info[1])
        elif command == 'stop_send_pdu':
            if 'can' in info[0]:
                pdu_obj.stop_send_pdu(info[0], int(info[1], 16))
            else:
                logger.info("停发报文失败，当前仅支持CAN报文的停发！！！")
        else:
            if 'can' in info[0]:
                pdu_obj.pause_bus_send(info[0])
                logger.info(f"停止发送{info[0]}上的报文{info[1]}, {info[2]}秒后恢复发送！！！")
                time.sleep(int(info[2]))
                pdu_obj.resume_bus_send(info[0])
            else:
                logger.info("停发报文失败，当前仅支持CAN报文的停发及恢复！！！")


def send_bus_signal(pdu_obj, channel, message_id, signal_name, signal_value, append=True):
    """
    向指定总线上发送1个can、lin或者FR信号
    """
    if append:
        CASE_RUN.send_signal_of_last_case.append(testCase(channel, message_id, signal_name))  # 将当前用例中发送的信号添加到发送信号列表里
    obj_list = getattr(pdu_obj, str(channel))
    if message_id.startswith('0x'):
        message_id = int(message_id, 16)  # message_id 作为16进制字符串的形式转换为整形，默认10进制字符串
        message_name, msg_tx_method = get_message_name_can_or_lin(obj_list, message_id)
    else:
        message_name, msg_tx_method = get_message_name_fr(obj_list, message_id)
    signal_name_list = signal_name.split(",")
    signal_value_list = signal_value.split(",")
    for signal_name, signal_value in zip(signal_name_list, signal_value_list):
        signal_value = int(float(signal_value))
        if msg_tx_method == 'cyclic':
            pdu_obj.set(getattr((getattr(pdu_obj, str(channel))), message_name),
                        signal_name, signal_value)
        else:
            logger.info("自定义cycle_time为0.5")
            pdu_obj.set(getattr((getattr(pdu_obj, str(channel))), message_name),
                        signal_name, signal_value, True, 0.5)


def reset_bus_signals(pdu_obj):
    """重置上一条用例中的总线信号值为0"""
    if CASE_RUN.current_service in ['SeatService', 'WTIService']:
        for signal in CASE_RUN.send_signal_of_last_case:
            send_bus_signal(pdu_obj, signal.channel, signal.message_id, signal.signal_name, '0', append=False)
        CASE_RUN.current_service = ''
    CASE_RUN.send_signal_of_last_case.clear()
    time.sleep(0.2)


def reset_global_loop_control():
    """重置全局循环控制"""
    UPSTREAM.check_count = 8
    UPSTREAM.check_interval = 0.3
    UPSTREAM.partner_main_wait_second = 3
    UPSTREAM.method_loop_count = 8
    UPSTREAM.method_loop_interval = 0.3


def get_signal_value_from_pdu_data(pdu, testcase1, pdu_data):
    messages0 = getattr(pdu, testcase1.channel)
    message_name0 = ''
    for obj in dir(messages0):
        sub_obj = getattr(messages0, obj)
        if hasattr(sub_obj, "msg_id"):
            if testcase1.message_id == getattr(sub_obj, "msg_id"):
                message_name0 = getattr(sub_obj, "msg_name")
                break
    if len(message_name0) == 0:
        logger.info("根据{}没有找到对应的message_name，继续下一个用例".format(testcase1.message_id))

    logger.info("result:{}".format(pdu.check(getattr(messages0, message_name0), testcase1.signal_name, pdu_data)))


def send_can_wake_data(bus_name, channel_name):
    """
    周期性发送唤醒报文
    """
    # sender = SocketCan("can_bus", bus_name)
    # if channel_name in ['chassiscan1', 'chassiscan2']:
    #     sender.add_cyclic_msg_with_data(0x527, [0x27, 0x40, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff], 0.05)
    # elif channel_name in ['bodycan', 'connectivitycanfd', 'propulsioncan', 'passivesafetycan']:
    #     sender.add_cyclic_msg_with_data(0x512, [0x12, 0x40, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff], 0.01)
    # elif channel_name == 'adcanfd':
    #     sender.add_cyclic_msg_with_data(0x502, [0x02, 0x40, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff], 0.01)
    # elif channel_name == 'bodyexposedcanfd':
    #     sender.add_cyclic_msg_with_data(0x52A, [0x2A, 0x40, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff], 0.01)
    # elif channel_name == 'infocanfd':
    #     sender.add_cyclic_msg_with_data(0x501, [0x01, 0x40, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff], 0.01)
    # sender.start()
    # time.sleep(0.5)


def add_cyclic_msg(sender, channel_name):
    """
    添加网络唤醒周期报文
    """
    if channel_name in ['chassiscan1', 'chassiscan2']:
        sender.add_cyclic_msg_with_data(0x527, [0x27, 0x40, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff], 0.01)
    elif channel_name in ['bodycan', 'connectivitycanfd', 'propulsioncan', 'passivesafetycan']:
        sender.add_cyclic_msg_with_data(0x512, [0x12, 0x40, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff], 0.01)
    elif channel_name == 'adcanfd':
        sender.add_cyclic_msg_with_data(0x502, [0x02, 0x40, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff], 0.01)
    elif channel_name == 'bodyexposedcanfd':
        sender.add_cyclic_msg_with_data(0x52A, [0x2A, 0x40, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff], 0.01)
    elif channel_name == 'infocanfd':
        sender.add_cyclic_msg_with_data(0x501, [0x01, 0x40, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff], 0.01)


def send_can_wake_data(bus_name, channel_name):
    """
    周期性发送唤醒报文
    """
    # sender = SocketCan("can_bus", bus_name)
    # add_cyclic_msg(sender, channel_name)
    # sender.start()
    # time.sleep(0.5)


def get_signal_value_from_pdu_data2(pdu, channel, message_id, signal_name):
    """
    channel: chassiscan2
    message_id: '96'(对应的是0x060)
    signal_name： ModReqOfDampr
    pdu_data： [8, 128, 0, 0, 0, 0, 0, 0]
    """
    messages0 = getattr(pdu, channel)
    message_name0 = ''
    for obj in dir(messages0):
        sub_obj = getattr(messages0, obj)
        if hasattr(sub_obj, "msg_id"):
            if message_id == getattr(sub_obj, "msg_id"):
                message_name0 = getattr(sub_obj, "msg_name")
                break
    if len(message_name0) == 0:
        logger.info("根据{}没有找到对应的message_name，继续下一个用例".format(message_id))
    result, value, _ = pdu.check(getattr(messages0, message_name0), signal_name, 0, 5, False)
    logger.info("{} result:{}".format(value, result))
    return result, value


def partner_client_method_request(service_name, func_name, params, method_type, source="up"):
    """
    func_name：函数名
    params：参数列表
    method_type：方法类型
    """
    logger.info(f"{service_name}==》{func_name}，参数：{params}，{method_type}，{source} 开始执行...")
    return partner_client.method_run(service_name, func_name, params, method_type, source)


def get_result(json_except, function_type):
    result = False
    if json_except.startswith('{'):
        for i in range(UPSTREAM.check_count):
            if get_run_result(json_except, function_type):
                UPSTREAM.get_method_response = True
                result = True
                break
            else:
                time.sleep(UPSTREAM.check_interval)
    else:
        for i in range(UPSTREAM.check_count):
            if get_run_result_part(json_except, function_type):
                UPSTREAM.get_method_response = True
                result = True
                break
            else:
                time.sleep(UPSTREAM.check_interval)
    print_log(json_except, partner_client.resp.copy())

    return result


def get_run_result(json_except, function_type):
    """
    整体比较预期结果与SOA partner的返回结果
    """
    resp_back = partner_client.resp.copy()
    resp_back_type = partner_client.resp_type.copy()
    if function_type == 'method':
        if 'FAILTYPE_SUCCESS' not in resp_back_type:
            return False
    if not resp_back:
        return False
    else:
        if json_except.replace(" ", '') in resp_back:
            return True
        elif get_contain_result(json_except, resp_back):
            return True
        else:
            return False


def get_contain_result(json_except, resp_back):
    """
    比较方式：contains
    """
    if not resp_back:
        return False
    else:
        result = False
        for i in resp_back:
            if i:  # 非空判断
                for tmp in eval(i.replace('false', 'False').replace('true', 'True')).values():
                    if isinstance(tmp, Iterable):  # 判断是否为可迭代对象
                        for obj in tmp:
                            if eval(json_except.replace('false', 'False').replace('true', 'True')) == obj:
                                result = True
                                break
                    else:
                        if eval(i.replace('false', 'False').replace('true', 'True')) == \
                                eval(json_except.replace('false', 'False').replace('true', 'True')):
                            result = True
                            break
    return result


def get_run_result_part(json_except, function_type):
    """
    部分比较
    """
    if "!=" in json_except:
        ss = "!="
    else:
        ss = "="
    json_except = json_except.replace(" ", '')
    str_list = json_except.split(ss)
    key_list = str_list[0].split(":")

    value = str_list[1]  # 预期结果的值
    if value == 'true':
        value = True
    elif value == 'false':
        value = False
    resp_back = partner_client.resp.copy()
    resp_back_type = partner_client.resp_type.copy()
    if function_type == 'method':
        if 'FAILTYPE_SUCCESS' not in resp_back_type:
            return False
    if not resp_back:
        return False
    else:
        result = False
        result_tmp = []
        for m_resp in resp_back:  # 遍历收到的响应结果
            result_tmp.append(json_except.replace("=", '":') in m_resp)
            m_resp = m_resp.replace('false', 'False').replace('true', 'True')
            m_resp = eval(m_resp)
            tmp = m_resp  # m_resp 为第一个响应结果

            for key in key_list:  # 变量预期结果前的键列表
                if not tmp:
                    break
                if isinstance(tmp, dict):
                    if key in tmp.keys():
                        tmp = tmp[key]
                        if tmp == 'true':
                            tmp = True
                        elif tmp == 'false':
                            tmp = False
                elif isinstance(tmp, list):
                    if key in tmp[0].keys():
                        tmp = tmp[0][key]
                        if tmp == 'true':
                            tmp = True
                        elif tmp == 'false':
                            tmp = False
                        elif tmp:
                            continue
            if isinstance(tmp, list):
                tmp = str(tmp).replace(" ", "")
                result_tmp.append(str(tmp) == str_list[1].replace("false", "False").replace("true", "True"))
                if ss == "!=":
                    result_tmp.append(str_list[1] not in tmp)  # 如果预期结果的值在真实响应结果（list）内
                else:
                    result_tmp.append(str_list[1] in tmp)  # 如果预期结果的值在真实响应结果（list）内
            if tmp is True or tmp is False:
                result_tmp.append(tmp == value)
            elif isinstance(tmp, float) or isinstance(tmp, int):
                result_tmp.append(remove_exponent(Decimal(str(tmp))) == remove_exponent(Decimal(str(value))))
            else:
                result_tmp.append(tmp == value)

        if any(result_tmp):
            result = True
        return result


def print_log(json_except, resp_back):
    logger.info("=========================")
    logger.info("预期结果：{}".format(json_except))
    logger.info("实际结果：{}".format(resp_back))
    logger.info("=========================")


def print_case_description(test_case, source='up'):
    """
    打印用例描述信息
    """
    allure.dynamic.description("用例编号：{};\n监听总线：{};\n信号名称：{};\n信号的值：{};\n服务名称：{};\n函数名称：{};"
                               .format(test_case.case_id, test_case.channel, test_case.signal_name,
                                       test_case.signal_value, test_case.service_name, test_case.function_name))
    allure.dynamic.title("用例编号：{}，服务：{}，接口名称：{}，接口：{}".format(test_case.case_id, test_case.service_name,
                                                              test_case.interface_name, test_case.function_name))
    allure.dynamic.feature("数据驱动用例")
    allure.dynamic.story(f"{source}/{test_case.service_name}")
    logger.info("*************************************")
    logger.info("用例编号：{}".format(test_case.case_id))

    if source in ['up', 'down']:
        logger.info("总线名称：{}".format(", ".join(test_case.channel)))
        logger.info("服务名称：{}".format(test_case.service_name))
        logger.info("函数名称：{}".format(test_case.function_name))
        logger.info("函数类型：{}".format(test_case.function_type))

    if source == 'set_get':
        logger.info("SET服务：{}".format(test_case.channel[0]))
        logger.info("SET函数：{}".format(test_case.message_id[0]))
        logger.info("SET参数：{}".format(test_case.signal_value[0]))
        logger.info("GET服务：{}".format(test_case.service_name))
        logger.info("GET函数：{}".format(test_case.function_name))
        logger.info("函数入参：{}".format(test_case.function_input))
    logger.info("*************************************")


def change_usage_mode(sd_test,  num_list):
    """
    切换用户使用模式
    """
    sd_test.update_serverdoipid(0x1002)

    for num in num_list:
        curr_mode = sd_test.change_usage_mode(int(num), do_assert=False)  # 如果切换使用模式失败，则用例依旧继续执行
        logger.info(f"期望的使用模式：{num}，切换后的使用模式：{curr_mode}")
        time.sleep(1)


def change_car_mode(sd_test,  num_list):
    """
    切换车辆使用模式
    """
    sd_test.update_serverdoipid(0x1002)

    for num in num_list:
        curr_mode = sd_test.change_car_mode(int(num), do_assert=False)  # 如果切换车辆模式失败，则用例依旧继续执行
        logger.info(f"期望的车辆模式：{num}，切换后的车辆模式：{curr_mode}")
        time.sleep(1)


def sd_test_init(sd_test):
    """sd_tester相关资源初始化"""
    sd_test.diagnostic_client_sim_start()
    time.sleep(0.5)
    sd_test.tester_present()
    time.sleep(0.5)
    sd_test.update_serverdoipid(0x1002)


def usage_mode_change_init(sd_test, pdu_obj):
    """使用模式切换初始化"""
    sd_test_init(sd_test)
    pdu_obj.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
    time.sleep(1)


def configure_word_write(sd_test, detail):
    """配置字写入方法"""
    id_0 = detail.split(":")[0]
    data = detail.split(":")[1]
    if len(data) == 1:  # 如果长度为1，则前面加0，以补足2位
        data = "0" + data
    ccp = sd_test.make_ccp_according_id_and_data(id_0, data)
    sd_test.write_ccp(ccp)
    time.sleep(1)


def sd_test_teardown(sd_test):
    """sd_tester相关资源回收"""
    sd_test.stop_tester_present()
    time.sleep(0.5)
    sd_test.diagnostic_client_sim_close()


def wake_bus_then_listen(tb_config, channel, message_id):
    """
    唤醒总线并监听总线报文
    """
    message_id = int(message_id, 16)
    bus_name1 = tb_config["bus"][channel]
    th1 = threading.Thread(target=send_can_wake_data, args=(bus_name1, channel))
    th1.start()  # 唤醒报文持续发送1秒
    listener = CanListener("can_bus", bus_name1)
    th = threading.Thread(target=listener.get_msg_with_can_id,
                          args=(message_id, 7,))
    th.setDaemon(True)
    th.start()
    return listener


def print_down_stream_result(result, expectedvalue, realvalue):
    if result is None:
        realvalue = "未监听到信号值"
    logger.info("=========================")
    logger.info("预期结果：{}".format(expectedvalue))
    logger.info("实际结果：{}".format(realvalue))
    logger.info("=========================")


def int_to_3_str_list(int_data):
    bytes_list = [str((int_data >> 16) & 0xFF)] + [str((int_data >> 8) & 0xFF)] + [str(int_data & 0xFF)]
    return '-'.join(bytes_list)


def get_message_name_can_or_lin(obj_list, message_id):
    for attr in dir(obj_list):
        obj1 = getattr(obj_list, attr)
        if hasattr(obj1, 'msg_id'):
            obj2 = getattr(obj1, 'msg_id')
            if int(obj2) == message_id:
                return attr, getattr(obj1, 'msg_tx_method')
    else:
        logger.info("message id 不可用")


def get_message_name_fr(obj_list, message_id):
    for attr in dir(obj_list):
        obj1 = getattr(obj_list, attr)
        if hasattr(obj1, 'msg_id'):
            obj2 = getattr(obj1, 'msg_id')
            if int_to_3_str_list(int(obj2)) == message_id:
                return attr, getattr(obj1, 'msg_tx_method')
    else:
        logger.info("message id 不可用")


def remove_exponent(num):
    """
    移除数字的小数部分后面多余的 0
    """
    return int(num)
