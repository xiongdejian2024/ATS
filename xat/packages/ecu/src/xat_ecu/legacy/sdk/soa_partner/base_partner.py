
import socket
import json

from threading import Thread
from typing import Union
from xat_ecu.legacy.sdk.soa_partner.PartnerStart import StartPartnerBase
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding
from xat_ecu.legacy.sdk.soa_partner.partner_helper import *

DEFAULT_PORT = 20000
BUFFER_SIZE = 1024 * 1000
MESSAGE_LENGTH_BYTES_FMT = '%08x'
MESSAGE_LENGTH_BYTES = 4

partners = [("KeyService", "client"), ("LightService", "client"), ("RPAAPAService", "server"), ("AVPService", "server")]


def send_data_to(conn, data):
    byte_len = MESSAGE_LENGTH_BYTES_FMT % len(json.dumps(data))
    conn.sendall(bytes(byte_len + json.dumps(data), encoding='utf-8'))


def recv_data_from(conn):
    recv_data = b''
    msg_len_bcd = conn.recv(MESSAGE_LENGTH_BYTES * 2)
    msg_len = int(msg_len_bcd.decode('utf-8'), 16)
    while msg_len > len(recv_data):
        data = conn.recv(BUFFER_SIZE)
        recv_data += data
    return recv_data


def ck_in_list(data1, data2: list):
    """
    校验data1在data2内
    :param data1:  单个数据item
    :param data2:  数据列表
    :return:  True/False
    """
    for data in data2:
        if ck_data(data, data1):
            return True
    return False


def ck_data(data1, data2):
    """
    校验两个对象内容，data2需在data1内包含或完全匹配, data1和data2的type需相同
    :param data1: 大数据集合
    :param data2: 校验内容
    :return:
    """
    if str(data2) == str(data1):
        return True
    if isinstance(data1, int):
        return data1 == data2
    elif isinstance(data1, float):
        return round(data1, 3) == round(data2, 3)  # 默认保留三位小数
    elif isinstance(data1, str):
        return data1.lower() == data2.lower()
    elif isinstance(data1, list):
        if not data2:  # 如果校验对象空列表，必须单独校验
            return data1 == []
        for item in data2:
            if not ck_in_list(item, data1):
                return False
        return True
    elif isinstance(data1, bytes):
        return data1 == DataTypeHanding.to_bytes(data2)
    elif isinstance(data1, dict):
        for key, value in data2.items():
            if key not in data1:
                return False
            if not ck_data(data1[key], value):
                return False
        return True


def handle_socket_data(raw: bytes) -> list:
    """
    有时会有多个事件上报，需要数据处理成列表
    :param raw: 如 b'{"action":"event","function":"UpdatePressureEvent","args":"{\\"sts\\":{\\"id\\":3,\\"pressure\\":260.8699951171875}}","failtype":""}{"action":"event","function":"UpdateTemperatureEvent","args":"{\\"sts\\":{\\"id\\":3,\\"temperature\\":49}}","failtype":""}'
    :return:
    """
    raw_data = raw.decode('utf-8')
    raw_data = raw_data.replace('false', "False")
    raw_data = raw_data.replace('true', "True")
    if '}{' not in raw_data:
        return [json.loads(raw_data)]
    else:
        raw_datas = raw_data.replace('}{', '}|{').split('|')
        return [eval(raw) for raw in raw_datas]


class BasePartner:
    """soa_partner模拟"""

    def __init__(self, partner_members=partners, soa_version_name=None, soa_partner_base_path="/root/soa_partner"):
        self.soa_version_name = soa_version_name  # SOA_bootes1_1_2r110bootes1_1_2r110JIDL_RELEASE_1_1REL_3
        self.soa_partner_base_path = soa_partner_base_path  # 基于该目录进行部署，部署后创建或更新soa_name.txt
        logger.info('Start partner operator...')
        self.sim_operator = StartPartnerBase("sim_op", DEFAULT_PORT, self.soa_partner_base_path, self.soa_version_name)
        self.partners = partner_members
        self.socket_info = {"exampleService_client": "example_socket"}
        self.resp_list = {"exampleService_client": []}
        self.req_list = {"exampleService_client": []}
        self.event_list = {"exampleService_client": []}  # 被测Server的event事件
        self.running = True
        self.tcp_socket = None  # 和self.sim_operator建立的socket连接
        self._start_operators()
        time.sleep(2)
        self._get_service_list_and_run_service(self.sim_operator)
        self._start_partner_config(self.partners)

    def _start_operators(self):
        """我理解operator就是个转换器"""
        self.sim_operator.run_operator()

    def stop_operators(self):
        self.tcp_socket.close()
        self.sim_operator.stop_operator()

    def _get_service_list_and_run_service(self, operator_obj: StartPartnerBase):
        """获取当前支持的服务get_current_service_list，并running_service"""
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.connect(('127.0.0.1', operator_obj.operator_port))
        req1 = {
            "action": "request",
            "function": "get_current_service_list",
            "args": None
        }
        send_data_to(self.tcp_socket, req1)
        recv_data1 = recv_data_from(self.tcp_socket)
        resp1 = json.loads(recv_data1.decode("utf-8"))
        result1 = json.loads(resp1['result'])

        req2 = {
            "action": "request",
            "function": "running_service",
            "args": None
        }
        send_data_to(self.tcp_socket, req2)
        recv_data2 = recv_data_from(self.tcp_socket)
        resp2 = json.loads(recv_data2.decode("utf-8"))
        result2 = json.loads(resp2['result'])

    def _start_partner_config(self, partner_members: list):
        """
        让partner启动某个服务,或某些服务
        :param partner_members: [("KeyService", "client")]
        :return:
        """
        single_start_partner = []
        member_cfg = {}  # key: keyService， value： {'role': server or client, 'name': KeyService or GNSSService_HD}
        for item in partner_members:
            if item[0] in member_cfg:  # 相同Service已实例化，再来一个需要单独实例
                single_start_partner.append(item)
                continue
            if len(item) == 3:
                member_cfg[item[0]] = {"role": item[1], "name": item[2]}
            else:
                member_cfg[item[0]] = {"role": item[1], "name": item[0]}

        if member_cfg is {} and not single_start_partner:
            logger.error(f"入参异常{partner_members}")
            return
        if member_cfg is not {}:
            req3 = {
                "action": "request",
                "function": "start_config",  # 调用该接口，不在请求列表中的服务都会被关闭
                "args": json.dumps(member_cfg)
            }
            send_data_to(self.tcp_socket, req3)
            recv_data3 = recv_data_from(self.tcp_socket)
            resp3 = json.loads(recv_data3.decode("utf-8"))
            result3 = json.loads(resp3['result'])
            logger.info(result3)
            time.sleep(1)
            for member, ip_port in result3.items():
                service_name = member.split('_')[0]
                partner_info = member_cfg[service_name]
                if partner_info['name'] == service_name:
                    partner_name = member
                else:
                    partner_name = member + "_" + partner_info['name']
                self.socket_info[partner_name] = \
                    self._connect_socket(ip_port,
                                         self.client_socket_handler if 'client' in member else self.server_socket_handler,
                                         partner_name)
        if single_start_partner:
            for item in single_start_partner:
                self.start_single_partner(*item)

    def start_single_partner(self, service_name: str, service_role: str, instance_name: str = None):
        """
        起单个服务
        :param service_name: GNSSService
        :param service_role: server
        :param instance_name:  用于区分不同的Server，比如GNSSService_HD表示ACU的server，GNSSService表示TCAM的server
        :return:
        """
        partner_name = f"{service_name}_{service_role}"
        if instance_name is not None:
            partner_name = partner_name + "_" + instance_name
        if partner_name in self.socket_info:
            logger.info(f"{partner_name}当前已启动")
            return
        req = {
            "action": "request",
            "function": "start_config_get_args",  # 不会操作不在请求列表的服务
            "args": json.dumps({
                service_name: {
                    "enable": "enable",
                    "role": service_role,
                    "name": service_name if instance_name is None else instance_name
                }
            })
        }
        send_data_to(self.tcp_socket, req)
        recv_data = recv_data_from(self.tcp_socket)
        resp = json.loads(recv_data.decode("utf-8"))
        result = json.loads(resp['result'])
        time.sleep(1)
        self.socket_info[partner_name] = \
            self._connect_socket(tuple(result[f"{service_name}_{service_role}"][0]),
                                 self.client_socket_handler if 'client' == service_role else self.server_socket_handler,
                                 partner_name)

    @staticmethod
    def _connect_socket(ip_port, socket_handler, partner_name):
        """
        建立socket连接并返回
        :param ip_port:
        :param socket_handler:
        :param partner_name: 类KeyService_client
        :return:
        """
        logger.info(f"启动{partner_name}, {ip_port}")
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(tuple(ip_port))
        thread = Thread(target=socket_handler, args=(conn, partner_name))
        thread.setDaemon(True)
        thread.start()
        return conn

    "********************************************[以下为测试接口]**************************************************"

    def empty_all(self, wait_time=0):
        """清空partner所有缓存数据"""
        time.sleep(wait_time)
        self.empty_req_list()
        self.empty_resp_list()
        self.empty_event_list()
        logger.info("清除partner所有缓存数据")

    def empty_event_list(self, partner=None):
        """清空记忆的event事件"""
        if partner is None:
            for partner in self.event_list:
                self.event_list[partner] = []
        elif partner not in self.event_list:
            assert ValueError(f"{partner}未实例化或参数错误，需要类KeyService_client")
        else:
            self.event_list[partner] = []

    def empty_req_list(self, partner=None):
        """清空记忆的req请求"""
        if partner is None:
            for partner in self.req_list:
                self.req_list[partner] = []
        elif partner not in self.req_list:
            assert ValueError(f"{partner}未实例化或参数错误，需要类KeyService_client")
        else:
            self.req_list[partner] = []

    def empty_resp_list(self, partner=None):
        """清空记忆的resp请求"""
        if partner is None:
            for partner in self.resp_list:
                self.resp_list[partner] = []
        elif partner not in self.resp_list:
            assert ValueError(f"{partner}未实例化或参数错误，需要类KeyService_client")
        else:
            self.resp_list[partner] = []

    def send_method_request(self, conn: Union[socket.socket, str], method_name: str, args: dict, is_async=False):
        """发送request请求"""
        req = {
            "action": "request",
            "function": f"{method_name}{is_async and 'Async' or ''}",
            "args": json.dumps(args)
        }
        if isinstance(conn, str):
            conn = self.socket_info[conn]
        conn.sendall(bytes(json.dumps(req), encoding='utf-8'))
        logger.info(f"partner发送请求{method_name}：{req}")

    def send_event_notify(self, conn: Union[socket.socket, str], event_name: str, args: dict):
        """服务端发送notify消息"""
        event = {
            "action": "event",
            "function": f"Update{event_name}Event",
            "args": json.dumps(args)
        }
        if isinstance(conn, str):
            conn = self.socket_info[conn]
        logger.info("发布事件通知：{}".format(event))
        conn.sendall(bytes(json.dumps(event), encoding='utf-8'))

    def send_method_response(self, conn: Union[socket.socket, str], method_name: str, args: dict):
        """服务端返回client的request请求"""
        resp = {
            "action": "response",
            "function": f"{method_name}",
            "result": json.dumps({"out": args})
        }
        if isinstance(conn, str):
            conn = self.socket_info[conn]
        conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))
        logger.info("方法返回结果：{}".format(json.dumps(resp)))

    def client_socket_handler(self, socket_conn, partner_name):
        """client的运行函数"""
        self.event_list[partner_name] = []
        self.resp_list[partner_name] = []
        while True:
            try:
                recv_data = socket_conn.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    time.sleep(0.001)
                    break
                responses = handle_socket_data(recv_data)
                for response in responses:
                    logger.info("收到{}发送的数据：{}".format(partner_name, response))
                    if response['action'] == 'event':
                        self.event_list[partner_name].append(response)
                    else:
                        self.resp_list[partner_name].append(response)
            except OSError as e:
                logger.error(e.__repr__())
                logger.error("remote end is closed")
                break
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/soa_partner/base_partner.py")
                logger.error(e.__repr__())
                continue

    def server_socket_handler(self, socket_conn, partner_name):
        """server的运行函数"""
        self.req_list[partner_name] = []
        while True:
            try:
                recv_data = socket_conn.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    time.sleep(0.001)
                    break
                req_info = json.loads(recv_data.decode("utf-8"))
                logger.info("{}收到client发送的请求：{}".format(partner_name, req_info))
                self.req_list[partner_name].append(req_info)
            except OSError as e:
                logger.error(e.__repr__())
                logger.error("remote end is closed")
                break
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/soa_partner/base_partner.py")
                logger.error(e.__repr__())
                continue

    def ck_s2s_req(self, partner_name: str, interface_name: str, ck_info: dict, timeout=1):
        """
        校验被测对象发送的request内容
        :param partner_name: 类似KeyService_client
        :param interface_name: 请求接口名
        :param ck_info: 校验请求内容
        :param timeout: 默认超时1s，用于等待req事件触发
        :return:
        """
        st = time.time()
        while time.time() - st < timeout:
            time.sleep(0.001)
            if not self.req_list[partner_name]:
                continue
            req = self.req_list[partner_name].pop()
            logger.info(f"校验缓存req---{req}")
            if req['function'] == interface_name:
                raw_data = eval(req['args'])
                req_data = raw_data.get('info', raw_data)
                assert ck_data(req_data, ck_info), f"{ck_info} not in {req_data}"
                logger.info(f"校验{interface_name}::{ck_info}--True")
                return
        else:
            assert False, f"未获取到期望的{interface_name}请求"

    def chk_notify(self, partner_name: str, method_name: str, ck_info: dict, timeout=1, fuzz_match=True):
        """
        检查服务返回的response结果。
        :param partner_name:  类似KeyService_client
        :param method_name:   请求接口名
        :param ck_info:  校验返回值
        :param timeout:  超时时间
        :param fuzz_match: 是否模糊匹配，模糊匹配对列表类的只需要列表内参数在event的列表中即可
        :return:
        """
        st = time.time()
        while time.time() - st < timeout:
            if self.event_list.get(partner_name, None):
                for resp in self.event_list[partner_name]:
                    if resp['function'] == f"Update{method_name}Event":
                        # self.event_list[partner_name].remove(resp)
                        raw_data = eval(resp['args'])
                        if fuzz_match:
                            if ck_data(raw_data, ck_info):
                                logger.info(f"校验{method_name}::{ck_info}--True")
                                return True
                        else:
                            if raw_data == ck_info:
                                logger.info(f"校验{method_name}::{ck_info}--True")
                                return True
            time.sleep(0.005)
        else:
            assert False, f"wait response from {partner_name} of {method_name} timeout!"

    def chk_resp(self, partner_name: str, method_name: str, ck_info: dict, timeout=1, fuzz_match=True):
        """
        检查服务返回的response结果。
        :param partner_name:  类似KeyService_client
        :param method_name:   请求接口名
        :param ck_info:  校验返回值
        :param timeout:  超时时间
        :param fuzz_match: 是否模糊匹配，模糊匹配对列表类的只需要列表内参数在event的列表中即可
        :return:
        """
        st = time.time()
        while time.time() - st < timeout:
            if self.resp_list.get(partner_name, None):
                resp = self.resp_list[partner_name].pop()
                if resp['function'] == method_name:
                    raw_data = eval(resp['result'])  # {"out": XX}
                    if fuzz_match:
                        assert ck_data(raw_data,
                                       ck_info), f"response from {partner_name} of {method_name} not match to expected!\ngot result: {raw_data}\n expect: {ck_info}"
                    else:
                        assert raw_data == ck_info, f"response from {partner_name} of {method_name} not match to expected!\ngot result: {raw_data}\n expect: {ck_info}"
                    break
            time.sleep(0.005)
        else:
            assert False, f"wait response from {partner_name} of {method_name} timeout!"

    def send_request_and_ck_resp(self, partner_name: str, method_name: str, args: dict,
                                 ck_info: dict, timeout=1, cycle_time=0.2, is_async=False, fuzz_match=True):
        """
        发送request请求并校验结果， 超时时间内每100ms（默认值）调用一次并校验，获取到期望值退出
        也可用于校验服务初始化时的数据，因为partner为堵塞线程，
        在服务未连接时调用，会一直等待服务连接后再发送，因此一定可用获得返回值
        :param partner_name:  类似KeyService_client
        :param method_name:   请求接口名
        :param args:   请求参数
        :param ck_info:  校验返回值
        :param timeout:  超时时间
        :param cycle_time:  调用周期
        :param is_async:
        :param fuzz_match: 是否模糊匹配，模糊匹配对列表类的只需要列表内参数在event的列表中即可
        :return:
        """
        if partner_name not in self.socket_info:
            assert False, f"入参错误{partner_name}"
        req = {
            "action": "request",
            "function": f"{method_name}{is_async and 'Async' or ''}",
            "args": json.dumps(args)
        }
        st = time.time()
        self.empty_resp_list(partner_name)
        while time.time() - st < timeout:
            self.socket_info[partner_name].sendall(bytes(json.dumps(req), encoding='utf-8'))
            logger.info(f"partner发送请求{method_name}：{req}")
            while time.time() - st < max(timeout, 3):  # 此处设置最小3s来确保能至少能发送一次并校验一次结果
                if self.resp_list.get(partner_name, None):
                    resp = self.resp_list[partner_name].pop()
                    if resp['function'] != method_name:
                        continue
                    raw_data = eval(resp['result'])  # {"out": XX}
                    if fuzz_match:
                        if ck_data(raw_data, ck_info):
                            return True
                        else:
                            break
                    else:
                        if raw_data == ck_info:
                            return True
                        else:
                            break
                time.sleep(cycle_time)
        else:
            assert False, f"{timeout}s内未获取到期望返回"

    def send_request_and_return_resp(self, partner_name: str, method_name: str, args: dict,
                                     timeout=1, is_async=False):
        """
        发送请求并获取返回值
        :param partner_name:  类似KeyService_client
        :param method_name:   请求接口名
        :param args:   请求参数
        :param timeout:  超时时间
        :param is_async:
        :return: resp
        """
        if partner_name not in self.socket_info:
            assert False, f"入参错误{partner_name}"
        req = {
            "action": "request",
            "function": f"{method_name}{is_async and 'Async' or ''}",
            "args": json.dumps(args)
        }
        st = time.time()
        self.empty_resp_list(partner_name)
        self.socket_info[partner_name].sendall(bytes(json.dumps(req), encoding='utf-8'))
        logger.info(f"partner发送请求{method_name}：{req}")
        while time.time() - st < max(timeout, 3):
            if self.resp_list.get(partner_name, None):
                resp = self.resp_list[partner_name].pop()
                if resp['function'] != method_name:
                    continue
                return eval(resp['result'])  # {"out": XX}

    def wait_for_service_reconnect(self, partner_name: str, timeout=20):
        """
        服务连接会进行注册回调函数，一定会触发event事件，以此来判断服务连接上
        :param partner_name:  指定某个服务，仅限client
        :param timeout:  超时时间，20s服务没连接报错
        :return:
        """
        st = time.time()
        while time.time() - st < timeout:
            if self.event_list[partner_name]:
                return True
            time.sleep(1)
        else:
            raise TimeoutError(f"{timeout}s超时未有event事件，可能服务未连接")

    def ck_s2s_event(self, partner_name: str, interface_name: str, ck_info: dict, timeout=3, fuzz_match=True):
        """
        校验被测对象发送的resp内容
        :param partner_name: 类似KeyService_Server
        :param interface_name: 接口名
        :param ck_info: 校验事件内容
        :param timeout: 校验时间
        :param fuzz_match: 是否模糊匹配，模糊匹配对列表类的只需要列表内参数在event的列表中即可
        :return:
        """
        st = time.time()
        logger.info(f"st:{st}")
        while time.time() - st < timeout:
            if self.event_list.get(partner_name, None):
                for resp in self.event_list[partner_name]:
                    if resp['function'] == f"Update{interface_name}Event":
                        # self.event_list[partner_name].remove(resp)
                        raw_data = eval(resp['args'])
                        if fuzz_match:
                            if ck_data(raw_data, ck_info):
                                logger.info(f"校验{interface_name}::{ck_info}--True")
                                self.event_list[partner_name].remove(resp)
                                return True
                        else:
                            if raw_data == ck_info:
                                logger.info(f"校验{interface_name}::{ck_info}--True")
                                self.event_list[partner_name].remove(resp)
                                return True
            time.sleep(0.005)
        else:
            logger.info("未获取到期望事件，查询列表数据")
            for resp in self.event_list[partner_name]:
                logger.info(resp)
            assert False, f"未获取到期望的{interface_name}事件上报"

    def ck_no_event(self, partner_name: str, interface_name: str, timeout=1):
        """
        校验指定时间内无指定event事件上报
        :param partner_name: 类似KeyService_Server
        :param interface_name:  接口名
        :param timeout: 校验时间
        :return:
        """
        st = time.time()
        while time.time() - st < timeout:
            if self.event_list.get(partner_name, None):
                resp = self.event_list[partner_name].pop()
                if resp['function'] == f"Update{interface_name}Event":
                    assert False, f"出现非预期事件上{resp}"
            time.sleep(0.005)

    def ck_no_specific_event(self, partner_name: str, interface_name: str, hint: str, timeout=1):
        """
        校验指定时间内无指定服务的event事件上报，当前主要用于WTI，固定列表上报，只校验列表中无value=hint
        :param partner_name: 类似KeyService_Server
        :param interface_name:  接口名
        :param hint: 告警信息
        :param timeout: 校验时间
        :return:
        """
        st = time.time()
        while time.time() - st < timeout:
            if self.event_list.get(partner_name, None):
                resp = self.event_list[partner_name].pop()
                if resp['function'] == f"Update{interface_name}Event":
                    for warn in eval(resp['args'])["list"]:
                        if warn["name"] == hint:
                            assert False, f"出现非预期事件上{resp}"
            time.sleep(0.005)

    def ck_no_req(self, partner_name: str, interface_name: str, timeout=1):
        """
        校验指定时间内无指定method请求
        :param partner_name: 类似KeyService_Server
        :param interface_name:  接口名
        :param timeout: 校验时间
        :return:
        """
        st = time.time()
        while time.time() - st < timeout:
            if self.req_list.get(partner_name, None):
                req = self.req_list[partner_name].pop()
                if req['function'] == interface_name:
                    assert False, f"出现非预期请求{req}"
            time.sleep(0.005)


if __name__ == '__main__':
    pass
    a = {"faults":[{"fault":7,"faultMsg":"","tyre":0},{"fault":7,"faultMsg":"","tyre":1},{"fault":7,"faultMsg":"","tyre":2},{"fault":7,"faultMsg":"","tyre":3}]}
    b = {'faults': [{'fault': 7, 'faultMsg': '', 'tyre': 3}]}
    print(ck_data(a, b))
