#!/usr/bin/python3

import socket
import json
import time
from threading import Thread
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.soa_partner.src.state import CAN_CONSTANT, UPSTREAM, CASE_RUN

DEFAULT_PORT = 16789
MESSAGE_LENGTH_BYTES = 4
BUFFER_SIZE = 1024 * 1000
MESSAGE_LENGTH_BYTES_FMT = '%08x'
running = True
function_name = ""
func_type = ""
event_name = ""

resp = []  # 保存响应结果
resp_type = []  # 保存响应结果的类型


def send_data_to(conn, data):
    """
    发送UDP data到app client
    """
    byte_len = MESSAGE_LENGTH_BYTES_FMT % len(json.dumps(data))
    conn.sendall(bytes(byte_len + json.dumps(data), encoding='utf-8'))


def recv_data_from(conn):
    """
    监听从app client返回的UDP data
    """
    recv_data = b''
    msg_len_bcd = conn.recv(MESSAGE_LENGTH_BYTES * 2)
    msg_len = int(msg_len_bcd.decode('utf-8'), 16)
    while msg_len > len(recv_data):
        data = conn.recv(BUFFER_SIZE)
        recv_data += data
    return recv_data


def start_handler(connect_info, handler, source):
    """
    1、根据connect_info，创建conn（socket连接）并返回\n
    2、设置守护线程，方法名为handler，其参数为conn
    """
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(connect_info)

    thread = Thread(target=handler, args=(conn, source, ))
    # 设置成守护线程
    thread.setDaemon(True)
    thread.start()
    return conn, thread


def send_method_request(conn, method_name, args, is_async=False, source="up"):
    """
    通过socket方式与app client通信，请求app client向proxy发起一个具体的方法请求，方法名、参数，
    """
    req = {
        "action": "request",
        "function": f"{method_name}{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    if source == "up":
        for i in range(30):  # 先发can信号，再执行get请求
            if CAN_CONSTANT.send_can_begin:
                break
            time.sleep(0.1)
        logger.info("up 开始执行")
        for i in range(UPSTREAM.method_loop_count):  # 每0.5秒执行一次get请求，直到找到预期的结果，最多执行20次
            conn.sendall(bytes(json.dumps(req), encoding='utf-8'))
            time.sleep(UPSTREAM.method_loop_interval)
            if UPSTREAM.get_method_response:
                logger.info("获得预期的结果，up 执行结束")
                break
        else:
            logger.info(f"没有获得预期的结果，up 执行结束")
    elif source in ["set", "get"]:
        logger.info(f"{source} 开始执行")
        for i in range(10):
            conn.sendall(bytes(json.dumps(req), encoding='utf-8'))
            time.sleep(0.1)
        else:
            logger.info(f"{source} 请求执行10次后结束")
        logger.info(f"{source} 请求执行结束")
    else:  # 下行方法执行
        logger.info(f"{source} 开始执行")
        for i in range(25):
            conn.sendall(bytes(json.dumps(req), encoding='utf-8'))
            time.sleep(0.1)
            if CAN_CONSTANT.get_wanted_can:  # 下行执行set方法的过程中，总线收到想要的CAN信号值，则退出循环
                logger.info(f"{source} 执行结束")
                break
        else:
            logger.info(f"{source} 执行结束")


def signal_handler():
    """
    停止与app client的socket通信
    """
    global running
    running = False


def method_run(service_name, method_name, method_parameter=None, method_type='method', source="up"):
    logger.info("服务=>{}，方法:{}开始运行，方法类型:{}，方法参数：{}".format(service_name, method_name, method_type, method_parameter))
    global running
    running = True
    global function_name
    function_name = method_name
    global resp
    global func_type
    func_type = method_type
    if method_parameter == '无':
        method_parameter = ""

    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect(('127.0.0.1', DEFAULT_PORT))

    req = {
        "action": "request",
        "function": "start_config",
        "args": json.dumps({
            service_name: {
                "role": "client",
                "name": service_name
            }
        })
    }
    send_data_to(tcp_socket, req)  # 通过socket请求向app client发起方法执行请求
    recv_data = recv_data_from(tcp_socket)  # recv_data为阻塞知道拿到app client的响应
    resp1 = json.loads(recv_data.decode("utf-8"))  # 将响应信息转成json格式
    result = json.loads(resp1['result'])

    tcp_socket.close()
    time.sleep(0.8)

    if source in ["up", "set", "get"]:
        """thread为监听响应结果线程，window_conn为监听线程中与soa partner通信的连接"""
        window_conn, thread = start_handler(
            tuple(result[service_name+'_client']), window_handler, source)
        time.sleep(0.3)
    else:
        window_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        window_conn.connect(tuple(result[service_name+'_client']))

    if method_type == 'method':
        try:
            if len(method_parameter) > 0:
                send_method_request(window_conn, method_name, eval(method_parameter), False, source)
            else:
                send_method_request(window_conn, method_name, method_parameter, False, source)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/partner_client.py")
            logger.info(f"{method_name} 执行过程中出现异常")
            window_conn.close()
    logger.info(f"{source} {UPSTREAM.partner_main_wait_second}秒，持续等待预期的方法返回或event的下发。")
    if source in ['up', 'get']:
        thread.join(UPSTREAM.partner_main_wait_second)  # 等待“监听结果的线程”执行结束，最多等待UPSTREAM.partner_main_wait_second秒
        running = False
    elif source in ['set']:
        thread.join(UPSTREAM.partner_main_wait_second)  # 等待“监听结果的线程”执行结束，最多等待UPSTREAM.partner_main_wait_second秒
        CASE_RUN.set_finished = True
        running = False
    else:  # 如果是down方法执行，则在主线程等待2秒后，关闭conn
        # time.sleep(2)
        window_conn.close()
    logger.info(f"{source} method 或 event 执行结束！！")
    UPSTREAM.get_method_response = False  # 主线程重置获取方法请求的状态：获取到True，未获取到False
    return resp


def handle_socket_data(raw: bytes) -> list:
    """
    有时会有多个事件上报，需要数据处理成列表
    :param raw: 如 b'{"action":"event","function":"UpdatePressureEvent","args":"{\\"sts\\":{\\"id\\":3,\\"pressure\\":260.8699951171875}}","failtype":""}{"action":"event","function":"UpdateTemperatureEvent","args":"{\\"sts\\":{\\"id\\":3,\\"temperature\\":49}}","failtype":""}'
    :return:
    """
    raw_data = raw.decode('utf-8')
    if '}{' not in raw_data:
        return [json.loads(raw_data)]
    else:
        raw_datas = raw_data.replace('}{', '}|{').split('|')
        return [eval(raw) for raw in raw_datas]


def window_handler(conn, source):
    """
    设置超时时间，阻塞并从socket中获取响应结果，并将响应结果保存在全局变量"resp"中
    对于up、set、get在主线程关闭conn
    """
    conn.settimeout(2)
    global function_name
    global func_type
    if func_type == "event":
        function_name1 = "Update{}Event".format(function_name)
        key_str = "args"
    else:
        function_name1 = function_name
        key_str = "result"

    global resp
    global resp_type
    global running
    global event_name

    while running:
        try:
            recv_data = conn.recv(BUFFER_SIZE)
            response_list = []  # 保存单次从server端获取到的响应
            if len(recv_data) == 0:
                break
            else:
                response_list = handle_socket_data(recv_data)
            #logger.info("全部响应结果：{}".format(response_list))
            for response in response_list:
                if response['function'] == function_name1:
                    logger.info("匹配响应结果：{}".format(response))
                    if response[key_str] == '{"out":null}':
                        response[key_str] = '{"out":""}'
                    if response[key_str] not in resp:
                        # if func_type == "event":  # 如果是事件类型
                        #     if not CAN_CONSTANT.send_can_begin:  # CAN信号发送前收到的event通知不保存
                        #         logger.info("信号未开始发送，本次结果忽略！！")
                        #         continue
                        resp.append(response[key_str])
                        resp_type.append(response['failtype'])
                    if UPSTREAM.get_method_response:  # 如果比对成功，则监听结束
                        conn.close()
                        break
                if response['function'] == event_name:  # set 方法 event验证
                    logger.info("匹配event响应结果：{}".format(response))
                    if response["args"] not in resp:
                        resp.append(response["args"])
                        resp_type.append(response['failtype'])
                    if UPSTREAM.get_method_response:
                        conn.close()
                        break
        except BrokenPipeError as e:
            conn.close()
            break
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/partner_client.py")
            continue
    else:
        conn.close()
