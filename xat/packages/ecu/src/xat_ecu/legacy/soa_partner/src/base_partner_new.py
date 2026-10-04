#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :base_partner.py
@Time         :2023/4/19 22:46:14
@Author       :jiabin.zhu@jiduauto.com
@Description  :
"""
import time
import socket
import json
from enum import Enum, auto

from threading import Thread
from typing import Union
from xat_ecu.legacy.soa_partner.src.Operator import SOAOperator
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding
from xat_ecu.legacy.soa_partner.src.partner_const import *

DEFAULT_PORT = 20000
BUFFER_SIZE = 1024 * 1000


class FailType(Enum):
    FAILTYPE_SUCCESS = 0
    FAILTYPE_TIMEOUT = -1
    FAILTYPE_SERVICE_BUSY = -2
    FAILTYPE_SERVICE_UNAVAILIABLE = -3
    FAILTYPE_TIME_OUT = 600  # operation timed out
    FAILTYPE_NO_MEMORY = auto()  # memory allocatoin failure
    FAILTYPE_OBJECT_NOT_EXIST = auto()  # no such object
    FAILTYPE_NO_PERMISSION = auto()  # no permission for operation
    FAILTYPE_INITIALIZE = auto()  # initialization failure
    FAILTYPE_NO_IMPLEMENT = auto()  # implementation unavailable
    FAILTYPE_BAD_TYPECODE = auto()  # bad typecode
    FAILTYPE_BAD_OPERATION = auto()  # invalid operation
    FAILTYPE_NO_RESPONSE = auto()  # response not yet available
    FAILTYPE_BAD_PARAM = auto()  # an invalid parameter was passed
    FAILTYPE_FREE_MEM = auto()  # no permission for operation
    FAILTYPE_SERIALIZATION_FAILURE = auto()  # serialization failure
    FAILTYPE_DESERIALIZATION_FAILURE = auto()  # deserialization failure
    FAILTYPE_SEND_DATA_FAILURE = auto()  # send data failure
    FAILTYPE_RECEIVE_DATA_FAILURE = auto()  # receive data failure
    FAILTYPE_WRONG_DATA_TYPE = auto()  # wrong data type
    FAILTYPE_OTHER_ERROR = auto()  # other error


class ServiceState(Enum):
    START = 0
    STOP = auto()
    RESTART = auto()
    UPTATE = auto()
    BUSY = auto()
    ONLINE = auto()
    OFFLINE = auto()
    ERROR = 100


class PartnerStartConfig:
    def __init__(self, service, role, instance, heartbeat):
        self.start_service = role.replace('client', service) if "_" in role else service  # role可能为client_1
        self.role = role.split("_")[0]
        self.name = instance
        self.status = True  # 使能服务连接状态上报接口
        self.heartbeat = heartbeat  # 设置通道阻塞检测的心跳

    def args(self):
        """
        返回启动服务的传参
        """
        return {self.start_service: {"role": self.role,
                                     "name": self.name,
                                     "status": self.status,
                                     "heartbeat": self.heartbeat}}


class PartnerKeyInfo:
    """partner单个客户端或服务端的全部属性数据"""

    def __init__(self, service, role, instance, heartbeat) -> None:
        self.ip_port = ('127.0.0.1', 0)  # 记录socket的ip和port，用于socket监测和重连
        self.start_config = PartnerStartConfig(service, role, instance, heartbeat)
        self.start_args = self.start_config.args()
        self.running = True
        self.socket = None
        self.resp_list = []
        self.req_list = []
        self.event_list = []
        self.instance = None,  # 对端的instance名，服务端：KeyService等，客户端: VehicleModeService:1560692_8534:car_service:0,
        self.service_status = 'OFFLINE'  # 对端状态，mock 客户端：ONLINE上线，OFFLINE下线，START连接成功；mock服务端：OFFLINE下线，START连接成功
        self.callback = []  # 注册的event或req回调函数


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
    raw_data = raw_data.replace('null', "None")
    if '}{' not in raw_data:
        return [json.loads(raw_data)]
    else:
        raw_datas = raw_data.replace('}{', '}|{').split('|')
        return [eval(raw) for raw in raw_datas]


class S2sBaseClass:
    """soa_partner模拟"""

    def __init__(self, partner_members=None, logger_flag=True, domin='acu', auto_start=True):
        """
        实例化S2sBaseClass
        :param partner_members: partner需要mock的客户端或服务端
        :param logger_flag: 是否要打印partner接收到的数据
        :param domin: 表明当前partner使用的哪个域的以太网线进行通信
        """
        logger.info('Start partner operator...')
        self.sim_operator = SOAOperator("sim_op", DEFAULT_PORT)
        self.domin = domin
        self.partner_infos = {"exampleService_client": PartnerKeyInfo('exampleService', 'client', 'exampleService',
                                                                      600)}  # partner所有成员的信息
        self.logger_flag = logger_flag  # 是否打印接口数据
        if auto_start:
            self.start_soa(partner_members=partner_members)

    def start_soa(self, partner_members):
        self.partner_members = self.__pre_handle_partner_members(partner_members)
        self.__start_operators(self.domin)
        self.__start_partner_config(self.partner_members)

    def __start_operators(self, domin="acu"):
        """
        启动partner
        :param domin: 表明当前partner使用的哪个域的以太网线进行通信
        """
        self.sim_operator.run_operator(domin)
        time.sleep(2)
        self.sim_operator.create_socket()
        self.sim_operator.send_request("get_current_service_list", print_result=False)  # 获取当前已编译的服务列表
        self.sim_operator.send_request("running_service")  # 查看当前已启动的服务

    def stop_operators(self):
        """
        将所有socket关闭同时停止partner
        """
        for partner_key in self.partner_infos:
            self.partner_infos[partner_key].running = False
        # self.sim_operator.stop_operator()
        self.sim_operator.send_request("reset", print_result=True)  # 停止所有服务

    @staticmethod
    def __pre_handle_partner_members(partner_members: list) -> list:
        """
        把partner_members处理成标准4个参数的格式返回
        """
        tmp_members = []
        for item in partner_members:
            if isinstance(item, str) and item.count('_') == 1:
                item = item.split('_')
                tmp_members.append((item[0], item[1], item[0], 600))
            elif len(item) == 2:
                tmp_members.append((item[0], item[1], item[0], 600))
            elif len(item) == 3:
                # 当前InstanceName和ServiceName不一致的情况
                # 仅出现于服务端如GNSSService_HD，或TCAM_UA_Service, BGM_InterCommService, 其他识别到再处理
                tmp_members.append((item[0], item[1], item[2], 600))
            elif len(item) == 4:
                tmp_members.append(item)
            else:
                raise KeyError(f"入参错误，应该传4个参数，当前传的入参为{item}")
        return tmp_members

    @staticmethod
    def __generate_partner_key_and_cfg(service, role, instance, heartbeat):
        """根据输入返回一个partner标准的key，如KeyService_client_1"""
        if "server_" in role:
            raise KeyError("无法mock多个server端")
        if "_" in role:  # client_1, client_2
            key = f"{service}_{role}"  # KeyService_client_1
        else:  # 单个客户端或服务端
            if service != instance:
                # GNSSService_server_GNSSService_HD或InterCommService_client_BGM_InterCommService
                key = f"{service}_{role}_{instance}"
            else:
                key = f"{service}_{role}"  # KeyService_client or GNSSService_server
        return key, PartnerKeyInfo(service, role, instance, heartbeat)

    @staticmethod
    def __find_key(ip_name, start_config):
        """
        从partner代理返回的ip，端口的名称找到partner_key，
        :param ip_name: 'KeyService_client_1', 'GNSSService_server'
        :param start_config: 请求启动服务时的传参
        """
        service = ip_name.split('_')[0]
        instance = start_config[service]['name']
        if instance == service:
            return ip_name
        else:
            # GNSSService_server_GNSSService_HD或InterCommService_client_BGM_InterCommService
            return f"{ip_name}_{instance}"

    def __handle_service_status(self, partner_key, msg):
        """
        处理各个socket对端的服务状态
        :param partner_key: partner实例名
        :param msg: socket获取的method or event 例 {"state":"START","instance":"VehicleModeService:2376_629228921:pavaro:0"}
        :return:
        """
        if msg['function'] == 'ServiceStatus':
            self.partner_infos[partner_key].service_status = eval(msg['args'])['state']

    def __add_msg_to_list(self, partner_key, msg):
        """将消息存放到数据列表"""
        msg['timestamp'] = time.time()
        if msg['action'] == 'event':
            self.partner_infos[partner_key].event_list.append(msg)
            self.__handle_service_status(partner_key, msg)
        elif msg['action'] == 'request':
            self.partner_infos[partner_key].req_list.append(msg)
        else:
            self.partner_infos[partner_key].resp_list.append(msg)
        if self.logger_flag:
            logger.info(f"{partner_key}收到数据：{msg}")

    def __start_partner_config(self, partner_members: list):
        """
        以partner输入的partner_members启动相关客户端和服务端
        :param partner_members: [("KeyService", "client", "InstanceName例如KetService"， 通道阻塞心跳值:1000, 默认600)]
        :return:
        """
        single_start_partner = []  # 当前仅用于多个server端同时启动场景，如GNSSService或UAService，无法在字典中用一个Service对应多个server
        start_config_args = {}
        for member in partner_members:
            key, cfg = self.__generate_partner_key_and_cfg(member[0], member[1], member[2], member[3])
            if key in self.partner_infos:
                raise KeyError(
                    f"{key}异常，不允许实例多个相同客户端或服务端，mock多个客户端请使用client, client_1，client_2")
            self.partner_infos[key] = cfg

            start_service = cfg.start_config.start_service
            if start_service in start_config_args:
                single_start_partner.append((key, cfg))
            else:
                start_config_args.update(cfg.start_args)
        if start_config_args is not {}:
            logger.info(start_config_args)
            # 调用下方请求，不在请求列表中的服务都会被关闭
            # 返回{'KeyService_client_1': ['127.0.0.1', 8001], 'GNSSService_server': [xx, xx]}
            result = self.sim_operator.send_request("start_config", json.dumps(start_config_args))
            time.sleep(1)
            for ip_name, ip_port in result.items():
                key = self.__find_key(ip_name, start_config_args)
                self.__connect_socket(ip_port, key)
        for item in single_start_partner:
            self.__start_single_partner(*item)

    def __start_single_partner(self, key, cfg):
        """起单个服务，内部函数"""
        for service in cfg.start_args:
            cfg.start_args[service]['enable'] = 'enable'
        logger.info(cfg.start_args)
        # 调用下方请求不会操作不在请求列表的服务，返回# {'VehicleModeService_client_1': [['127.0.0.1', 20002], {'apis': XXXX
        result = self.sim_operator.send_request("start_config_get_args", json.dumps(cfg.start_args), print_result=False)
        ip_name = list(result.keys())[0]
        time.sleep(1)
        self.__connect_socket(result[ip_name][0], key)

    def __connect_socket(self, ip_port, partner_key):
        """
        建立socket连接并返回
        :param ip_port: ('127.0.0.1', 1000)
        :param partner_key: 类KeyService_client
        :return:
        """
        logger.info(f"启动{partner_key}, {ip_port}")
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(tuple(ip_port))
        self.partner_infos[partner_key].socket = conn
        self.partner_infos[partner_key].ip_port = ip_port
        thread = Thread(target=self.socket_handler,
                        args=(partner_key,),
                        name=f"{partner_key} handler")
        thread.setDaemon(True)
        self.register_callback(partner_key, self.__add_msg_to_list)
        thread.start()
        return conn

    def __reconnect_socket(self, partner_key):
        """
        在socket断链后重新连接
        :param partner_key:  partner对象的信息，从中获取ip_port
        :return: socket
        """
        socket_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_conn.connect(tuple(self.partner_infos[partner_key].ip_port))
        self.partner_infos[partner_key].socket = socket_conn
        return socket_conn

    "********************************************[以下为测试接口]**************************************************"

    def start_single_partner(self, service: str, role: str, instance: str = None, heartbeat: int = 600):
        """
        起单个服务
        :param service: GNSSService
        :param role: server
        :param instance:  用于区分不同的Server，比如GNSSService_HD表示ACU的server，GNSSService表示TCAM的server
        :param heartbeat:  通道阻塞检测的心跳
        :return:
        """
        single_partner = self.__pre_handle_partner_members([(service, role,
                                                             instance if instance else service, heartbeat)])[0]
        key, cfg = self.__generate_partner_key_and_cfg(*single_partner)
        if key in self.partner_infos:
            logger.warning(f"{key}当前已启动")
            return
        self.partner_infos[key] = cfg
        self.__start_single_partner(key, cfg)

    def stop_single_partner(self, partner_key):
        """停止某个特定服务"""
        self.partner_infos[partner_key].running = False
        time.sleep(0.1)
        tmp_start_cfg = self.partner_infos[partner_key].start_args
        for service in tmp_start_cfg:
            tmp_start_cfg[service]['enable'] = 'disable'
        logger.info(tmp_start_cfg)
        self.sim_operator.send_request("start_config_get_args", json.dumps(tmp_start_cfg), print_result=False)
        del self.partner_infos[partner_key]

    def empty_all(self, wait_time=0):
        """清空partner所有缓存数据"""
        time.sleep(wait_time)
        self.empty_req_list()
        self.empty_resp_list()
        self.empty_event_list()
        logger.info("清除partner所有缓存数据")

    def empty_event_list(self, partner_key=None):
        """清空记忆的event事件"""
        if partner_key is None:
            for partner in self.partner_infos:
                self.partner_infos[partner].event_list = []
        elif partner_key not in self.partner_infos:
            raise ValueError(f"{partner_key}未实例化或参数错误，需要类似KeyService_client")
        else:
            self.partner_infos[partner_key].event_list = []

    def empty_req_list(self, partner_key=None):
        """清空记忆的req请求"""
        if partner_key is None:
            for partner in self.partner_infos:
                self.partner_infos[partner].req_list = []
        elif partner_key not in self.partner_infos:
            raise ValueError(f"{partner_key}未实例化或参数错误，需要类似KeyService_client")
        else:
            self.partner_infos[partner_key].req_list = []

    def empty_resp_list(self, partner_key=None):
        """清空记忆的resp请求"""
        if partner_key is None:
            for partner in self.partner_infos:
                self.partner_infos[partner].resp_list = []
        elif partner_key not in self.partner_infos:
            raise ValueError(f"{partner_key}未实例化或参数错误，需要类似KeyService_client")
        else:
            self.partner_infos[partner_key].resp_list = []

    def register_callback(self, partner_key, func):
        """注册回调函数"""
        self.partner_infos[partner_key].callback.append(func)

    def unregister_callback(self, partner_key, func):
        """取消注册回调函数"""
        self.partner_infos[partner_key].callback.remove(func)

    def send_method_request(self, partner_key: str, method_name: str, args: dict, is_async=False):
        """发送request请求"""
        req = {
            "action": "request",
            "function": f"{method_name}{is_async and 'Async' or ''}",
            "args": json.dumps(args)
        }
        conn = self.partner_infos[partner_key].socket
        st = time.time()
        while self.partner_infos[partner_key].service_status != ServiceState.START.name:
            if time.time() - st > 5:
                raise TimeoutError("等待5s仍未和服务端建立连接，无法发送请求，请检测环境或用例")
            logger.error("服务端当前不为START连接状态")
            time.sleep(1)
        conn.sendall(bytes(json.dumps(req), encoding='utf-8'))
        logger.info(f"{partner_key}发送请求{method_name}：{req}")

    def send_event_notify(self, partner_key: str, event_name: str, args: dict):
        """服务端发送notify消息"""
        event = {
            "action": "event",
            "function": f"Update{event_name}Event",
            "args": json.dumps(args)
        }
        conn = self.partner_infos[partner_key].socket
        logger.info(f"{partner_key}发布事件通知：{event}")
        conn.sendall(bytes(json.dumps(event), encoding='utf-8'))

    def send_method_response(self, partner_key: str, method_name: str, args: dict):
        """服务端返回client的request请求"""
        resp = {
            "action": "response",
            "function": f"{method_name}",
            "result": json.dumps({"out": args})
        }
        conn = self.partner_infos[partner_key].socket
        conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))
        logger.info(f"{partner_key}方法返回结果：{json.dumps(resp)}")

    def socket_handler(self, partner_key):
        """client的运行函数"""
        socket_conn = self.partner_infos[partner_key].socket
        while partner_key in self.partner_infos and self.partner_infos[partner_key].running:
            try:
                recv_data = socket_conn.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    # time.sleep(0.001)
                    break
                msg = handle_socket_data(recv_data)
                for response in msg:
                    for function in self.partner_infos[partner_key].callback:
                        function(partner_key, response)
            except socket.error as e:
                if e.errno == 32:
                    logger.error(f"Broken Pipe error: {e.strerror}")
                    socket_conn = self.__reconnect_socket(partner_key)
                else:
                    logger.error(f"{partner_key} socket error: {e.strerror}")
                    break
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/base_partner_new.py")
                logger.error(e.__repr__())

    def ck_s2s_req(self, partner_key: str, interface_name: str, ck_info: dict, timeout=1):
        """
        校验被测对象发送的request内容
        :param partner_key: 类似KeyService_client
        :param interface_name: 请求接口名
        :param ck_info: 校验请求内容
        :param timeout: 默认超时1s，用于等待req事件触发
        :return:
        """
        st = time.time()
        while time.time() - st < timeout:
            while self.partner_infos[partner_key].req_list:
                req = self.partner_infos[partner_key].req_list.pop()
                logger.info(f"校验缓存req---{req}")
                if req['function'] == interface_name:
                    raw_data = eval(req['args'])
                    req_data = raw_data.get('info', raw_data)
                    assert ck_data(req_data, ck_info), f"{ck_info} not in {req_data}"
                    logger.info(f"校验{interface_name}::{ck_info}--True")
                    return
            time.sleep(0.001)
        else:
            assert False, f"未获取到期望的{interface_name}请求"

    def chk_notify(self, partner_key: str, method_name: str, ck_info: dict, timeout=1, fuzz_match=True):
        """
        检查服务返回的response结果。
        :param partner_key:  类似KeyService_client
        :param method_name:   请求接口名
        :param ck_info:  校验返回值
        :param timeout:  超时时间
        :param fuzz_match: 是否模糊匹配，模糊匹配对列表类的只需要列表内参数在event的列表中即可
        :return:
        """
        st = time.time()
        while time.time() - st < timeout:
            for resp in self.partner_infos[partner_key].event_list:
                if resp['function'] == f"Update{method_name}Event":
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
            assert False, f"wait response from {partner_key} of {method_name} timeout!"

    def chk_resp(self, partner_key: str, method_name: str, ck_info: dict, timeout=1, fuzz_match=True):
        """
        检查服务返回的response结果。
        :param partner_key:  类似KeyService_client
        :param method_name:   请求接口名
        :param ck_info:  校验返回值
        :param timeout:  超时时间
        :param fuzz_match: 是否模糊匹配，模糊匹配对列表类的只需要列表内参数在event的列表中即可
        :return:
        """
        st = time.time()
        while time.time() - st < timeout:
            while self.partner_infos[partner_key].resp_list:
                resp = self.partner_infos[partner_key].resp_list.pop()
                if resp['function'] == method_name:
                    raw_data = eval(resp['result'])  # {"out": XX}
                    if fuzz_match:
                        assert ck_data(raw_data,
                                       ck_info), f"response from {partner_key} of {method_name} not match to expected!\ngot result: {raw_data}\n expect: {ck_info}"
                    else:
                        assert raw_data == ck_info, f"response from {partner_key} of {method_name} not match to expected!\ngot result: {raw_data}\n expect: {ck_info}"
                    break
            time.sleep(0.005)
        else:
            assert False, f"wait response from {partner_key} of {method_name} timeout!"

    def send_request_and_ck_failtype(self, partner_key: str, method_name: str, args: dict,
                                     failtype: Union[FailType, str], timeout=6, is_async=False):
        """
        发送request请求并校验FailType
        在服务未连接时调用，会一直等待服务连接后再发送，因此一定可用获得返回值
        :param partner_key:  类似KeyService_client
        :param method_name:   请求接口名
        :param args:   请求参数
        :param failtype:  返回tailtype，常用：
        :param timeout:  超时时间
        :param is_async:
        :return:
        """
        self.send_method_request(partner_key, method_name, args, is_async)
        st = time.time()
        self.empty_resp_list(partner_key)
        while time.time() - st < timeout:
            while self.partner_infos[partner_key].resp_list:
                resp = self.partner_infos[partner_key].resp_list.pop()
                logger.info(resp)
                if resp['function'] != method_name:
                    continue
                assert resp['failtype'] == (failtype if isinstance(failtype, str) else failtype.name), "failtype错误"
                return True
            time.sleep(0.001)
        else:
            assert False, f"{timeout}s内未获取到期望返回"

    def send_request_and_ck_resp(self, partner_key: str, method_name: str, args: dict,
                                 ck_info: dict, timeout=1, cycle_time=0.2, is_async=False, fuzz_match=True):
        """
        发送request请求并校验结果， 超时时间内每100ms（默认值）调用一次并校验，获取到期望值退出
        在服务未连接时调用，会一直等待服务连接后再发送，因此一定可用获得返回值
        :param partner_key:  类似KeyService_client
        :param method_name:   请求接口名
        :param args:   请求参数
        :param ck_info:  校验返回值
        :param timeout:  超时时间
        :param cycle_time:  调用周期
        :param is_async:
        :param fuzz_match: 是否模糊匹配，模糊匹配对列表类的只需要列表内参数在event的列表中即可
        :return:
        """
        if partner_key not in self.partner_infos:
            assert False, f"{partner_key}当前未启动"
        st = time.time()
        self.empty_resp_list(partner_key)
        while time.time() - st < timeout:
            self.send_method_request(partner_key, method_name, args, is_async)

            while time.time() - st < max(timeout, 6):  # 此处设置最小5s来确保能至少能发送一次并校验一次结果, 至少有超时
                try:
                    resp = self.partner_infos[partner_key].resp_list.pop()
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/base_partner_new.py")
                    time.sleep(0.005)
                    continue
                else:
                    if resp['function'] != method_name:
                        continue
                    raw_data = eval(resp['result'])  # {"out": XX}
                    if (fuzz_match and ck_data(raw_data, ck_info)) or (not fuzz_match and raw_data == ck_info):
                        logger.info(f"校验{method_name}::{ck_info}--True")
                        return True
                    else:
                        break
            time.sleep(cycle_time)
        else:
            assert False, f"{timeout}s内未获取到期望返回"

    def send_request_and_return_resp(self, partner_key: str, method_name: str, args: dict,
                                     timeout=1, is_async=False):
        """
        发送请求并获取返回值
        :param partner_key:  类似KeyService_client
        :param method_name:   请求接口名
        :param args:   请求参数
        :param timeout:  超时时间
        :param is_async:
        :return: resp
        """
        if partner_key not in self.partner_infos:
            assert False, f"{partner_key}当前未启动"
        st = time.time()
        self.empty_resp_list(partner_key)
        self.send_method_request(partner_key, method_name, args, is_async)
        while time.time() - st < max(timeout, 3):
            while self.partner_infos[partner_key].resp_list:
                resp = self.partner_infos[partner_key].resp_list.pop()
                if resp['function'] != method_name:
                    continue
                if len(resp['result']) > 0:
                    return eval(resp['result'])  # {"out": XX}
                else:
                    return None
            time.sleep(0.001)

    def wait_for_service_reconnect(self, partner_key: str, timeout=20):
        """
        服务上线连接后，partner会发出ServiceStatus事件，其中state=START，以此来判断服务连接上
        :param partner_key:  指定某个服务，partner作为client和server都可以
        :param timeout:  超时时间，20s服务没连接报错
        :return:
        """
        st = time.time()
        ck_list = self.partner_infos[partner_key].event_list
        while time.time() - st < timeout:
            for event in ck_list:
                if event['function'] == 'ServiceStatus':
                    if eval(event['args'])['state'] == ServiceState.START.name:
                        return True
            time.sleep(0.001)
        else:
            raise TimeoutError(f"{timeout}s超时未有ServiceStatus事件，服务未连接")

    def ck_s2s_event(self, partner_key: str, interface_name: str, ck_info: dict, timeout=3, fuzz_match=True):
        """
        校验被测对象发送的resp内容
        :param partner_key: 类似KeyService_Server
        :param interface_name: 接口名
        :param ck_info: 校验事件内容
        :param timeout: 校验时间
        :param fuzz_match: 是否模糊匹配，模糊匹配对列表类的只需要列表内参数在event的列表中即可
        :return: raw_data，event数据内容
        """
        st = time.time()
        logger.info(f"ck_s2s_event st:{st}")
        tmp_list = []
        while time.time() - st < timeout:
            try:
                resp = self.partner_infos[partner_key].event_list.pop()
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/base_partner_new.py")
                time.sleep(0.005)
                continue
            else:
                if resp['function'] == f"Update{interface_name}Event":
                    raw_data = eval(resp['args'])
                    if (fuzz_match and ck_data(raw_data, ck_info)) or (not fuzz_match and raw_data == ck_info):
                        logger.info(f"校验{interface_name}::{ck_info}--True")
                        self.partner_infos[partner_key].event_list += tmp_list
                        return True
                    else:
                        tmp_list.append(resp)
                else:
                    tmp_list.append(resp)
        else:
            logger.info("未获取到期望事件，查询列表数据")
            self.partner_infos[partner_key].event_list += tmp_list
            for resp in self.partner_infos[partner_key].event_list:
                logger.info(resp)
            # assert False, f"未获取到期望的{interface_name}事件上报"
            return False

    def return_latest_event(self, partner_key: str, interface_name: str):
        """
        返回指定接口最近的一次event消息
        :param partner_key: 类似KeyService_Server
        :param interface_name:  接口名
        """
        st = time.time()
        tmp_list = []
        while True:
            try:
                resp = self.partner_infos[partner_key].event_list.pop()
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/base_partner_new.py")
                assert False, f"当前未接收到过{interface_name}事件"
            else:
                if resp['function'] == f"Update{interface_name}Event":
                    self.partner_infos[partner_key].event_list += tmp_list
                    return eval(resp['args'])
                else:
                    tmp_list.append(resp)

    def ck_no_event(self, partner_key: str, interface_name: str, timeout=1):
        """
        校验指定时间内无指定event事件上报
        :param partner_key: 类似KeyService_Server
        :param interface_name:  接口名
        :param timeout: 校验时间
        :return:
        """
        st = time.time()
        tmp_list = []
        while time.time() - st < timeout:
            try:
                resp = self.partner_infos[partner_key].event_list.pop()
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/base_partner_new.py")
                time.sleep(0.005)
                continue
            else:
                if resp['function'] == f"Update{interface_name}Event":
                    assert False, f"出现非预期事件上{resp}"
                else:
                    tmp_list.append(resp)
        else:
            self.partner_infos[partner_key].event_list += tmp_list

    def ck_no_specific_event(self, partner_key: str, interface_name: str, hint: str, timeout=1):
        """
        校验指定时间内无指定服务的event事件上报，当前主要用于WTI，固定列表上报，只校验列表中无value=hint
        :param partner_key: 类似KeyService_Server
        :param interface_name:  接口名
        :param hint: 告警信息
        :param timeout: 校验时间
        :return:
        """

        st = time.time()
        while time.time() - st < timeout:
            while self.partner_infos[partner_key].event_list:
                resp = self.partner_infos[partner_key].event_list.pop()
                if resp['function'] == f"Update{interface_name}Event":
                    for warn in eval(resp['args'])["list"]:
                        if warn["name"] == hint:
                            assert False, f"出现非预期事件上{resp}"
            time.sleep(0.005)

    def ck_no_req(self, partner_key: str, interface_name: str, timeout=1):
        """
        校验指定时间内无指定method请求
        :param partner_key: 类似KeyService_Server
        :param interface_name:  接口名
        :param timeout: 校验时间
        :return:
        """
        st = time.time()
        tmp_list = []
        while time.time() - st < timeout:
            try:
                req = self.partner_infos[partner_key].req_list.pop()
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/base_partner_new.py")
                time.sleep(0.005)
                continue
            else:
                if req['function'] == interface_name:
                    return False
                else:
                    tmp_list.append(req)
        else:
            self.partner_infos[partner_key].req_list += tmp_list
            return True

    def register_event(self, partner_key: str, event_list: list = [{"all": 1}]):
        """
        注册指定服务的指定event
        :param partner_key: 类似KeyService_Server
        :param event_list: 默认all，即全部event，否则给定event列表,[{"Status": 1}, {"DoorAngle": 2}], 键值对中值1: 注册后需要发送历史数据， 值2：不需要发送历史数据
        """
        event = {
            "action": "request",
            "function": "RegistEvent",
            "args": json.dumps({"event_list": event_list})
        }
        logger.info("注册event：{}".format(event_list))
        self.partner_infos[partner_key].socket.sendall(bytes(json.dumps(event), encoding='utf-8'))

    def unregister_event(self, partner_key: str, event_list: list = ["all"]):
        """
        反注册指定服务的指定event
        :param partner_key: 类似KeyService_Server
        :param event_list: 默认all，即全部event，否则给定event列表
        """
        event = {
            "action": "request",
            "function": "UnRegistEvent",
            "args": json.dumps({"event_list": event_list})
        }
        logger.info("反注册event：{}".format(event_list))
        self.partner_infos[partner_key].socket.sendall(bytes(json.dumps(event), encoding='utf-8'))


if __name__ == '__main__':
    pass
    a = {"faults": [{"fault": 7, "faultMsg": "", "tyre": 0}, {"fault": 7, "faultMsg": "", "tyre": 1},
                    {"fault": 7, "faultMsg": "", "tyre": 2}, {"fault": 7, "faultMsg": "", "tyre": 3}]}
    b = {'faults': [{'fault': 7, 'faultMsg': '', 'tyre': 3}]}
    print(ck_data(a, b))
