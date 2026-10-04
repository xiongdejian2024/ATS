#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :base_partner.py
@Time         :2023/4/19 22:46:14
@Author       :jiabin.zhu@jiduauto.com
@Description  :
"""
import os
import threading
import time
import socket
import json
import collections
import subprocess
import queue
from enum import Enum, auto

from threading import Thread
from typing import Union
from xat_ecu.legacy.soa_partner.src.Operator import SOAOperator
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding
from xat_ecu.legacy.soa_partner.src.partner_const import *
from xat_ecu.legacy.common.file_handle import parent_dir
from xat_ecu.legacy.common import exception_error
from xat_ecu.legacy.sdk.sdk_tools import exec_shell
from xat_ecu.legacy.soa_partner.src.soa_partner import SoaBasePartner

DEFAULT_PORT = 20000
BUFFER_SIZE = 1024 * 1000


def return_timestamp(event):
    """获取事件的时间戳"""
    return event['timestamp']


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
        self.resp_queue = queue.LifoQueue()
        self.req_queue = queue.LifoQueue()
        self.event_queue = queue.LifoQueue()
        self.instance = None,  # 对端的instance名，服务端：KeyService等，客户端: VehicleModeService:1560692_8534:car_service:0,
        self.service_status = 'OFFLINE'  # 对端状态，mock 客户端：ONLINE上线，OFFLINE下线，START连接成功；mock服务端：OFFLINE下线，START连接成功
        self.callback = []  # 注册的event或req回调函数
        self.method_timeout_ck_callback = {}  # key为method_name， value为元组(调用时间戳，接口超时)


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
        decimal_places = min(len(str(float(data2)).split('.')[1]), 4)
        return round(data1, decimal_places) == round(data2,
                                                     decimal_places)  # 按预期结果的小数位进行保留，注意预期结果给的是123.00时，按123.0计算小数位
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


def handle_socket_data(raw: bytes, last_data_str: str) -> list:
    """
    有时会有多个事件上报，需要数据处理成列表
    :param raw: 如 b'{"action":"event","function":"UpdatePressureEvent","args":"{\\"sts\\":{\\"id\\":3,\\"pressure\\":260.8699951171875}}","failtype":""}{"action":"event","function":"UpdateTemperatureEvent","args":"{\\"sts\\":{\\"id\\":3,\\"temperature\\":49}}","failtype":""}'
    :param last_data_str: 之前可能被截断的数据
    :return:
    """
    raw_data = last_data_str + raw.decode('utf-8')
    raw_data = raw_data.replace('false', "False")
    raw_data = raw_data.replace('true', "True")
    raw_data = raw_data.replace('null', "None")
    if '}{' not in raw_data:
        return [json.loads(raw_data)], ''
    else:
        raw_datas = raw_data.replace('}{', '}|{').split('|')
        if not raw_data.endswith('"}'):
            last_data_str = raw_datas.pop()
        else:
            last_data_str = ''
        return [eval(raw) for raw in raw_datas], last_data_str


class S2sBaseClass(SoaBasePartner):
    """soa_partner模拟"""

    def __init__(self, partner_members=None, logger_flag=True, domin='acu', auto_start=True, X86=None, idl=None):
        """
        实例化S2sBaseClass
        :param partner_members: partner需要mock的客户端或服务端
        :param logger_flag: 是否要打印partner接收到的数据
        :param domin: 表明当前partner使用的哪个域的以太网线进行通信
        :param X86: bootes_version(eg:bootes1_4_1r306)
        :param idl: JIDL_version(eg:JIDL_RELEASE_1_4REL_8)
        """
        logger.info('Start partner operator...')
        self.partner_members = []
        self.his_start_config_get_args_members = []
        self.operator_running = True
        self.X86 = X86
        self.idl = idl
        if self.X86 and self.idl:
            self.X86 = self.X86.replace('.', '_')
            self.idl = self.idl.replace('.', '_')
            res = exec_shell(f'cd {parent_dir};./deploy.sh {X86} {idl}')
            res_error = res["error"]
            if res_error != "":
                raise exception_error.DeploySoaPartnerError(f'deploy soa partner faild, ret code:{res_error}')
        elif X86 or idl:
            raise exception_error.DeploySoaPartnerError('X86和idl两个参数有一个为None')
        self.method_default_timeout = 5.1
        self.method_is_timeout = []
        self.sim_operator = SOAOperator("sim_op", DEFAULT_PORT)
        self.domin = domin
        self.partner_infos = {"exampleService_client": PartnerKeyInfo('exampleService', 'client', 'exampleService',
                                                                      600)}  # partner所有成员的信息
        self.logger_flag = logger_flag  # 是否打印接口数据
        if auto_start:
            self.start_soa(partner_members=partner_members)
        self.auto_response = {}

    def start_soa(self, partner_members):
        self.partner_members = self.__pre_handle_partner_members(partner_members)
        self.__start_operators(self.domin)
        self.__start_partner_config(self.partner_members)
        self.__start_operator_monitor_thread()

    def __start_operators(self, domin="acu"):
        """
        启动partner
        :param domin: 表明当前partner使用的哪个域的以太网线进行通信
        """
        self.sim_operator.run_operator(domin)
        times = 0
        error = None
        while times < 10:  # 正常300ms左右就能建立连接，但是partner偶发2s没有启动完成，因此设置超时5s
            time.sleep(0.5)
            times += 1
            try:
                self.sim_operator.create_socket()
            except ConnectionRefusedError as e:
                error = e
                logger.info(times)
                continue
            else:
                break
        else:
            raise error
        self.sim_operator.send_request("get_current_service_list", print_result=False)  # 获取当前已编译的服务列表
        self.sim_operator.send_request("running_service")  # 查看当前已启动的服务

    def stop_operators(self):
        """
        将所有socket关闭同时停止partner
        """
        self.operator_running = False
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
            elif isinstance(item, str) and item.count('_') == 3:
                item = item.split('_')
                tmp_members.append((item[0], item[1], f"{item[2]}_{item[3]}", 600))
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
        if 'server' in ip_name:
            server_client_index = ip_name.split('_').index("server")
        else:
            server_client_index = ip_name.split('_').index("client")
        service = "_".join(ip_name.split('_')[0: server_client_index])
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
        if self.logger_flag:
            logger.info(f"{partner_key}收到数据：{msg}")
        if msg['action'] == 'event':
            self.partner_infos[partner_key].event_queue.put(msg)
            self.__handle_service_status(partner_key, msg)
        elif msg['action'] == 'request':
            self.partner_infos[partner_key].req_queue.put(msg)
            # 判断是否需要自动响应client的request请求
            if partner_key in self.auto_response:
                if msg['function'] in self.auto_response[partner_key]:
                    try:
                        if hasattr(self,
                                   f"send_method_response_{partner_key.replace('_server', '')}_{msg['function']}"):
                            getattr(self,
                                    f"send_method_response_{partner_key.replace('_server', '')}_{msg['function']}")()
                        else:
                            logger.info(
                                f"方法不存在：send_method_response_{partner_key.replace('_server', '')}_{msg['function']}")
                    except Exception as e:
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/base_partner.py")
                        logger.info(f"服务{partner_key.replace('_server', '')} 的{msg['function']}的自动响应执行异常")
                        logger.info(e)
        else:
            if msg['function'].endswith('Async') and msg['result'] == 'True':  # todo: 需要ruihua改
                return  # todo: 当前partner存在异常，该响应无需回复
            self.partner_infos[partner_key].resp_queue.put(msg)
            args = self.partner_infos[partner_key].method_timeout_ck_callback.get(msg['function'], (None, None))
            self.__ck_resp_time(msg, args[0], args[1])

    def __ck_resp_time(self, resp, send_time, timeout):
        """
        校验method的响应耗时
        :param resp: method的响应
        :param send_time: 调用method的时间戳
        :param timeout: 调用method传入的超时，若不传则按self.method_default_timeout处理
        :return:
        """
        if send_time is None:
            return
        if timeout is None:
            timeout = self.method_default_timeout
        spend_time = resp['timestamp'] - send_time
        if spend_time > timeout:
            logger.error(f"{resp['timestamp']}响应的{resp['function']}花费{spend_time}，超过预期的{timeout}")
            self.method_is_timeout.append((resp['function'], resp['timestamp'], spend_time))

    def ck_method_timeout(self):
        """用于测试结束时使用该接口将过程中的超时调用暴露"""
        if self.method_is_timeout:
            assert False, f"接口调用存在超时,{self.method_is_timeout}"

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

    def __send_event_notify_cycle(self, partner_key: str, event_name: str, args: dict, cycle_time: float = 1):
        while not self.partner_infos[partner_key].start_event:
            self.send_event_notify(partner_key, event_name, args)
            time.sleep(cycle_time)

    def __start_operator_monitor_thread(self):
        """对partner整体进行监控，若异常则自动重启"""
        thread = Thread(target=self.__operator_monitor_thread,
                        name="__operator_monitor_thread")
        thread.setDaemon(True)
        thread.start()

    def __operator_monitor_thread(self):
        """operator监控进程"""
        while self.operator_running:
            time.sleep(5)  # 5s一次检测，即使出现异常，也应该只影响一个case
            ret = self.sim_operator.process.poll()
            if ret is not None:
                logger.error(f"Operator进程异常:{ret}，非0,1,-9则自动重启(0为正常退出，1为重复启动partner，-9为kill)")
                result = subprocess.run(['ip', 'addr'], capture_output=True, text=True)
                logger.info("当前网卡状态如下：")
                logger.info(str(result.stdout))
                if ret not in [0, 1, -9]:
                    self.__restart_partner_and_members()
                break

    def __restart_partner_and_members(self):
        """
        当前存在partner异常断开的情况，需要出现该情况时，自动进行处理恢复环境
        """
        self.partner_infos = {}
        self.__start_operators(self.domin)
        self.__start_partner_config(self.partner_members)
        for key, cfg in self.his_start_config_get_args_members:
            self.__start_single_partner(key, cfg)

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
        self.his_start_config_get_args_members.append((key, cfg))

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

    @staticmethod
    def _empty_queue(queue_obj: queue.Queue):
        """清空指定队列"""
        while not queue_obj.empty():
            queue_obj.get()

    @staticmethod
    def _put_items_to_queue(queue_obj: queue.Queue, items: list):
        """把列表中的数据依次放到队列中"""
        for item in items:
            queue_obj.put(item)

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
                self._empty_queue(self.partner_infos[partner].event_queue)
        elif partner_key not in self.partner_infos:
            raise ValueError(f"{partner_key}未实例化或参数错误，需要类似KeyService_client")
        else:
            self._empty_queue(self.partner_infos[partner_key].event_queue)

    def empty_req_list(self, partner_key=None):
        """清空记忆的req请求"""
        if partner_key is None:
            for partner in self.partner_infos:
                self._empty_queue(self.partner_infos[partner].req_queue)
        elif partner_key not in self.partner_infos:
            raise ValueError(f"{partner_key}未实例化或参数错误，需要类似KeyService_client")
        else:
            self._empty_queue(self.partner_infos[partner_key].req_queue)

    def empty_resp_list(self, partner_key=None):
        """清空记忆的resp请求"""
        if partner_key is None:
            for partner in self.partner_infos:
                self._empty_queue(self.partner_infos[partner].resp_queue)
        elif partner_key not in self.partner_infos:
            raise ValueError(f"{partner_key}未实例化或参数错误，需要类似KeyService_client")
        else:
            self._empty_queue(self.partner_infos[partner_key].resp_queue)

    def register_callback(self, partner_key, func):
        """注册回调函数"""
        self.partner_infos[partner_key].callback.append(func)

    def unregister_callback(self, partner_key, func):
        """取消注册回调函数"""
        self.partner_infos[partner_key].callback.remove(func)

    def send_method_request(self, partner_key: str, method_name: str, args: dict, is_async=False, timeout=None):
        """发送request请求"""
        function = f"{method_name}{is_async and 'Async' or ''}"
        req = {
            "action": "request",
            "function": function,
            "args": json.dumps(args)
        }
        conn = self.partner_infos[partner_key].socket
        st = time.time()
        while self.partner_infos[partner_key].service_status != ServiceState.START.name:
            if time.time() - st > 5:
                raise TimeoutError("等待5s仍未和服务端建立连接，无法发送请求，请检测环境或用例")
            logger.error("服务端当前不为START连接状态")
            time.sleep(1)
        if not is_async:  # 仅同步调用校验超时
            self.partner_infos[partner_key].method_timeout_ck_callback[function] = (time.time(), timeout)
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

    def send_event_notify_thread_start(self, partner_key: str, event_name: str, args: dict, cycle_time: float = 1):
        self.partner_infos[partner_key].start_event = False
        self.partner_infos[partner_key].cycle_time = cycle_time
        self.thread_event = threading.Thread(target=self.__send_event_notify_cycle,
                                             args=(partner_key, event_name, args, cycle_time))
        logger.info(f"开始{partner_key}服务发送")
        self.thread_event.setDaemon(True)
        self.thread_event.start()
        self.partner_infos[partner_key].thread_obj = self.thread_event

    def send_event_notify_thread_stop(self, partner_key):
        self.partner_infos[partner_key].start_event = True
        self.partner_infos[partner_key].thread_obj = None
        logger.info(f"停止{partner_key}服务发送")

    def send_event_notify_thread_update(self, partner_key: str, event_name: str, args: dict, cycle_time=None):
        if not self.partner_infos[partner_key].thread_obj:
            err_msg = f"{partner_key}服务线程已关闭, 无法使用update接口"
            logger.error(err_msg)
            raise AttributeError(err_msg)
        else:
            self.send_event_notify_thread_stop(partner_key)
            if cycle_time is None:
                cycle_time = self.partner_infos[partner_key].cycle_time
            time.sleep(cycle_time)
            self.send_event_notify_thread_start(partner_key, event_name, args, cycle_time)

    def send_method_response(self, partner_key: str, method_name: str, args: Union[dict, None] = None):
        """服务端返回client的request请求"""
        resp = {
            "action": "response",
            "function": f"{method_name}",
            "result": "" if args is None else json.dumps({"out": args})
        }
        conn = self.partner_infos[partner_key].socket
        conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))
        logger.info(f"{partner_key}方法返回结果：{json.dumps(resp)}")

    def socket_handler(self, partner_key):
        """client的运行函数"""
        socket_conn = self.partner_infos[partner_key].socket
        last_data_str = ''
        while partner_key in self.partner_infos and self.partner_infos[partner_key].running:
            try:
                recv_data = socket_conn.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    logger.info(f"{partner_key}连接已断开")
                    break
                msg, last_data_str = handle_socket_data(recv_data, last_data_str)
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
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/base_partner.py")
                logger.error(e.__repr__())

    def ck_s2s_req(self, partner_key: str, interface_name: str, ck_info: Union[dict, None] = None, timeout=1):
        """
        从缓存列表中校验被测对象发送的request内容
        :param partner_key: 类似KeyService_client
        :param interface_name: 请求接口名
        :param ck_info: 校验请求内容
        :param timeout: 默认超时1s，用于等待req事件触发
        :return:
        """
        st = time.time()
        logger.info(f"ck_s2s_req st:{st}")
        tmp_list = []
        while time.time() - st < timeout:
            try:
                req = self.partner_infos[partner_key].req_queue.get(timeout=max(st + timeout - time.time(), 0))
            except queue.Empty:
                assert False, "超时未获取到期望req"
            else:
                if req['function'] == interface_name:
                    if ck_info is None:
                        logger.info(f"检测到：{interface_name} 请求，不需要检测具体参数内容")
                        self._put_items_to_queue(self.partner_infos[partner_key].req_queue,
                                                 sorted(tmp_list, key=return_timestamp))
                        return
                    else:
                        raw_data = eval(req['args'])
                        req_data = raw_data.get('info', raw_data)
                        if ck_data(req_data, ck_info):
                            self._put_items_to_queue(self.partner_infos[partner_key].req_queue,
                                                     sorted(tmp_list, key=return_timestamp))
                            return
                        else:
                            tmp_list.insert(0, req)
                else:
                    tmp_list.insert(0, req)
        else:
            logger.info(f"未获取到期望请求，如下打印为{partner_key}接收到的历史请求")
            self._put_items_to_queue(self.partner_infos[partner_key].req_queue,
                                     sorted(tmp_list, key=return_timestamp))
            for req in list(self.partner_infos[partner_key].req_queue.queue):
                logger.info(f"历史数据：{req}")
            assert False, f"未获取到期望的{interface_name}请求"

    def ck_s2s_req_v20(self, partner_key: str, interface_name_list: list, ck_info_list=None, timeout=1):
        """
        校验被测对象发送的request内容
        :param partner_key: 类似KeyService_client
        :param interface_name_list: 请求接口名列表
        :param ck_info_list: 校验请求内容列表，与接口名列表一一对应
        :param timeout: 默认超时1s，用于等待req事件触发
        :return:
        """
        st = time.time()
        ck_info_list = ck_info_list if ck_info_list else [''] * len(interface_name_list)
        count = len(interface_name_list)
        result = collections.Counter(interface_name_list)
        while time.time() - st < timeout:
            if count == 0:
                return req
            while not self.partner_infos[partner_key].req_queue.empty():
                if count == 0:
                    return req
                req = self.partner_infos[partner_key].req_queue.get_nowait()
                for interface_name, ck_info in zip(interface_name_list, ck_info_list):
                    logger.info(f"校验缓存req---{req}")
                    if result[interface_name]:
                        if req['function'] == interface_name:
                            if not ck_info:
                                result[interface_name] -= 1
                                count = count - 1
                                logger.info(f"检测到：{interface_name} 请求，不需要检测具体参数内容，剩余校验次数{count}次")
                                break
                            else:
                                raw_data = eval(req['args'])
                                req_data = raw_data.get('info', raw_data)
                                if ck_data(req_data, ck_info):
                                    result[interface_name] -= 1
                                    count = count - 1
                                    logger.info(f"校验{interface_name}::{ck_info}--True，剩余校验次数{count}次")
                                    break
            time.sleep(0.001)
        else:
            for key in result:
                if result[key]:
                    assert False, f"获取到的{key}请求不满足预期"

    def _send_request_and_return_resp_atom(self, partner_key: str, method_name: str, args: dict,
                                           timeout=None, is_async=False):
        """
        发送请求返回响应的原子能力
        :return: 原始响应数据，{"action": xx, "function": xx, "result": xx, "failtype": xx, "timestamp": xx}
        """
        self.send_method_request(partner_key, method_name, args, is_async, timeout=timeout)
        st = time.time()
        tmp_list = []
        timeout = timeout if timeout else 6
        while time.time() - st < timeout:
            try:
                resp = self.partner_infos[partner_key].resp_queue.get(timeout=max(st + timeout - time.time(), 0))
            except queue.Empty:
                assert False, "超时未获取到期望resp"
            else:
                if resp['function'] == f"{method_name}{'Async' if is_async else ''}":
                    self._put_items_to_queue(self.partner_infos[partner_key].resp_queue,
                                             sorted(tmp_list, key=return_timestamp))
                    return resp
                else:
                    tmp_list.append(resp)

    def __send_request_and_ck_resp_once(self, partner_key, method_name, args, ck_info, fuzz_match, timeout=5,
                                        is_async=False):
        """
        调用method并校验响应结果，仅一次
        return: 校验结果True/False
        """
        resp = self._send_request_and_return_resp_atom(partner_key, method_name, args,
                                                       timeout=timeout, is_async=is_async)
        raw_data = eval(resp['result'])
        if (fuzz_match and ck_data(raw_data, ck_info)) or (not fuzz_match and raw_data == ck_info):
            logger.info(f"校验{method_name}::{ck_info}--True")
            return True
        else:
            return False

    def send_request_and_ck_failtype(self, partner_key: str, method_name: str, args: dict,
                                     failtype: Union[FailType, str], timeout=6, is_async=False):
        """
        发送request请求并校验FailType
        在服务未连接时调用，会一直等待服务连接后再发送，因此一定可用获得返回值
        :param partner_key:  类似KeyService_client
        :param method_name:   请求接口名
        :param args:   请求参数
        :param failtype:  返回failtype，常用：
        :param timeout:  超时时间
        :param is_async:
        :return:
        """
        self.empty_resp_list(partner_key)
        resp = self._send_request_and_return_resp_atom(partner_key, method_name, args, timeout, is_async)
        assert resp['failtype'] == (failtype if isinstance(failtype, str) else failtype.name), "failtype错误"

    def send_request_and_ck_resp(self, partner_key: str, method_name: str, args: dict,
                                 ck_info: dict, timeout=1.0, cycle_time=0.2, is_async=False, fuzz_match=True,
                                 failtype=FailType.FAILTYPE_SUCCESS):
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
        :param failtype: 返回failtype, 默认校验FailType.FAILTYPE_SUCCESS,不是则报错
        :return:
        """
        if partner_key not in self.partner_infos:
            assert False, f"{partner_key}当前未启动"
        self.empty_resp_list(partner_key)
        st = time.time()
        while time.time() - st < timeout:
            if self.__send_request_and_ck_resp_once(partner_key, method_name, args, ck_info, fuzz_match, is_async=False):
                return True
            time.sleep(cycle_time)
        else:
            assert False, f"{timeout}s内未获取到期望返回"

    def chk_notify(self, partner_key: str, method_name: str, ck_info: Union[dict, None] = None, timeout=1,
                   fuzz_match=True):
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
            for resp in list(self.partner_infos[partner_key].event_queue.queue):
                if resp['function'] == f"Update{method_name}Event":
                    if ck_info is None:
                        logger.info(f"检测到：{method_name} 事件，不需要检测具体参数内容")
                        assert True
                        return
                    else:
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
        self.empty_resp_list(partner_key)
        resp = self._send_request_and_return_resp_atom(partner_key, method_name, args, timeout, is_async)
        if len(resp['result']) > 0:
            return eval(resp['result'])  # {"out": XX}
        else:
            return None

    def wait_for_service_reconnect(self, partner_key: str, timeout=30):
        """
        服务上线连接后，partner会发出ServiceStatus事件，其中state=START，以此来判断服务连接上
        :param partner_key:  指定某个服务，partner作为client和server都可以
        :param timeout:  超时时间，30s服务没连接报错
        :return:
        """
        st = time.time()
        tmp_list = []
        while time.time() - st < timeout:
            try:
                event = self.partner_infos[partner_key].event_queue.get(timeout=max(st + timeout - time.time(), 0))
            except queue.Empty:
                raise TimeoutError(f"{timeout}s超时未有ServiceStatus事件，服务未连接")
            else:
                if event['function'] == 'ServiceStatus':
                    if eval(event['args'])['state'] == ServiceState.START.name:
                        self._put_items_to_queue(self.partner_infos[partner_key].event_queue,
                                                 sorted(tmp_list, key=return_timestamp))
                        return True
        else:
            raise TimeoutError(f"{timeout}s超时未有ServiceStatus事件，服务未连接")

    def ck_coming_event(self, partner_key: str, interface_name: str, ck_info: dict, timeout=0.3, deviation=0,
                        fuzz_match=True):
        """
        校验从接口调用开始的超时时间内有指定event发出，也可给给定偏移量，精确校验event发出的时间
        :param partner_key: 类似KeyService_Server
        :param interface_name: 接口名
        :param ck_info: 校验事件内容
        :param timeout: 校验时间
        :param deviation: 偏移量，默认0s，则只校验超时事件内有指定event即可，如果给定数值如0.2，则要求接收到的时间在指定t±0.2s时间内出现
        :param fuzz_match: 是否模糊匹配，模糊匹配对列表类的只需要列表内参数在event的列表中即可
        :return: raw_data，event数据内容
        """
        st = time.time()
        logger.info(f"ck_coming_event st:{st}")
        if deviation >= timeout:
            assert False, "入参错误，deviation需小于timeout"
        tmp_list = []  # 存所有的事件
        while time.time() - st < timeout + deviation:
            try:
                event = self.partner_infos[partner_key].event_queue.get(
                    timeout=max(st + timeout + deviation - time.time(), 0))
            except queue.Empty:
                assert False, "超时未获取到期望event"
            else:
                event_time = event['timestamp']
                if event_time < st:  # 老数据
                    tmp_list.append(event)
                    continue
                else:  # 新数据
                    if event['function'] == f"Update{interface_name}Event":
                        raw_data = eval(event['args'])

                        if (fuzz_match and ck_data(raw_data, ck_info)) or (not fuzz_match and raw_data == ck_info):
                            if deviation:  # 给定偏差即精确校验时间戳
                                assert timeout - deviation < event_time - st < timeout + deviation, f"event事件发送时间{event_time}与预期不符"
                            logger.info(f"校验{interface_name}::{ck_info}--True")
                            self._put_items_to_queue(self.partner_infos[partner_key].event_queue,
                                                     sorted(tmp_list, key=return_timestamp))
                            return raw_data
                        else:
                            tmp_list.append(event)

                    else:
                        tmp_list.append(event)
        else:
            assert False, f"超时时间内未获取到期望的{interface_name}事件上报"

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
                event = self.partner_infos[partner_key].event_queue.get(timeout=max(st + timeout - time.time(), 0))
            except queue.Empty:
                assert False, "超时未获取到期望event"
            else:
                if event['function'] == f"Update{interface_name}Event":
                    raw_data = eval(event['args'])
                    if (fuzz_match and ck_data(raw_data, ck_info)) or (not fuzz_match and raw_data == ck_info):
                        logger.info(f"校验{interface_name}::{ck_info}--True")
                        self._put_items_to_queue(self.partner_infos[partner_key].event_queue,
                                                 sorted(tmp_list, key=return_timestamp))
                        return raw_data
                    else:
                        tmp_list.append(event)
                else:
                    tmp_list.append(event)
        else:
            logger.info(f"未获取到期望事件，如下打印为{partner_key}接收到的历史事件")
            self._put_items_to_queue(self.partner_infos[partner_key].event_queue,
                                     sorted(tmp_list, key=return_timestamp))
            for resp in list(self.partner_infos[partner_key].event_queue.queue):
                logger.info(f"历史数据：{resp}")
            assert False, f"未获取到期望的{interface_name}事件上报"

    def return_latest_event(self, partner_key: str, interface_name: str, pop_event=True):
        """
        返回指定接口最近的一次event消息
        :param partner_key: 类似KeyService_Server
        :param interface_name:  接口名
        :param pop_event:  获取最新数据后是否弹出，默认弹出
        """
        tmp_list = []
        while True:
            try:
                event = self.partner_infos[partner_key].event_queue.get_nowait()
            except queue.Empty:
                assert False, f"当前未接收到过{interface_name}事件"
            else:
                if event['function'] == f"Update{interface_name}Event":
                    if not pop_event:
                        tmp_list.append(event)
                    self._put_items_to_queue(self.partner_infos[partner_key].event_queue,
                                             sorted(tmp_list, key=return_timestamp))
                    return eval(event['args'])
                else:
                    tmp_list.append(event)

    def ck_no_event(self, partner_key: str, interface_name: str, timeout=1):
        """
        校验指定时间内无指定event事件上报
        :param partner_key: 类似KeyService_Server
        :param interface_name:  接口名
        :param timeout: 校验时间
        :return:
        """
        st = time.time()
        logger.info(f"ck_no_event st:{st}")
        tmp_list = []
        while time.time() - st < timeout:
            try:
                event = self.partner_infos[partner_key].event_queue.get(timeout=max(st + timeout - time.time(), 0))
            except queue.Empty:
                break
            else:
                if event['function'] == f"Update{interface_name}Event":
                    assert False, f"出现非预期事件上{event}"
                else:
                    tmp_list.append(event)
        self._put_items_to_queue(self.partner_infos[partner_key].event_queue,
                                 sorted(tmp_list, key=return_timestamp))

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
            try:
                event = self.partner_infos[partner_key].event_queue.get(timeout=max(st + timeout - time.time(), 0))
            except queue.Empty:
                break
            else:
                if event['function'] == f"Update{interface_name}Event":
                    for warn in eval(event['args'])["list"]:
                        if warn["name"] == hint:
                            assert False, f"出现非预期事件上{event}"

    def ck_no_req(self, partner_key: str, interface_name: str, timeout=1, ck_info: dict = None):
        """
        校验指定时间内无指定method请求
        :param partner_key: 类似KeyService_Server
        :param interface_name:  接口名
        :param timeout: 校验时间
        :param ck_info: 校验请求的内容，若为None则不校验具体内容，不为None则需要完全匹配
        :return:
        """
        st = time.time()
        tmp_list = []
        while time.time() - st < timeout:
            try:
                req = self.partner_infos[partner_key].req_queue.get(timeout=max(st + timeout - time.time(), 0))
            except queue.Empty:
                continue
            else:
                if req['function'] == interface_name:
                    if ck_info is None:
                        assert False, f"出现非预期请求{req}"
                    else:
                        if ck_data(eval(req['args']), ck_info):
                            assert False, f"出现非预期请求{req}"
                        else:
                            tmp_list.insert(0, req)
                            continue
                else:
                    tmp_list.insert(0, req)
        else:
            self._put_items_to_queue(self.partner_infos[partner_key].req_queue,
                                     sorted(tmp_list, key=return_timestamp))

    def register_event(self, partner_key: str, event_names: list = [{"all": 1}]):
        """
        注册指定服务的指定event
        :param partner_key: 类似KeyService_Server
        :param event_names: 默认all，即全部event，否则给定event列表,[{"Status": 1}, {"DoorAngle": 2}], 键值对中值1: 注册后需要发送历史数据， 值2：不需要发送历史数据
        """
        event = {
            "action": "request",
            "function": "RegistEvent",
            "args": json.dumps({"event_list": event_names})
        }
        logger.info("注册event：{}".format(event_names))
        self.partner_infos[partner_key].socket.sendall(bytes(json.dumps(event), encoding='utf-8'))

    def unregister_event(self, partner_key: str, event_names: list = ["all"]):
        """
        反注册指定服务的指定event
        :param partner_key: 类似KeyService_Server
        :param event_names: 默认all，即全部event，否则给定event列表
        """
        event = {
            "action": "request",
            "function": "UnRegistEvent",
            "args": json.dumps({"event_list": event_names})
        }
        logger.info("反注册event：{}".format(event_names))
        self.partner_infos[partner_key].socket.sendall(bytes(json.dumps(event), encoding='utf-8'))

    def register_auto_response(self, partner_key: str, interface_name: str):
        if partner_key.endswith("_server"):
            if partner_key not in self.auto_response:
                self.auto_response[partner_key] = []
            if interface_name not in self.auto_response[partner_key]:
                self.auto_response[partner_key].append(interface_name)
                logger.info(f"服务{partner_key} 的{interface_name}已注册自动回复")
            else:
                logger.info(f"服务{partner_key} 的{interface_name}已注册自动回复，无需重复注册")

    def unregister_auto_response(self, partner_key: str, interface_name: str):
        if partner_key in self.auto_response:
            self.auto_response[partner_key].remove(interface_name)
            logger.info(f"服务{partner_key} 的{interface_name}的自动回复已注销")

    "********************************************[以下为SOA平台测试专用接口]**************************************************"

    def ck_event_and_resp(self, partner_key: str, event_name: str, event_info: dict,
                          method_name=None, method_args=None, resp_info=None,
                          timeout=3, fuzz_match=True):
        """
        校验历史event，并调用get获取结果
        :param partner_key: 类似KeyService_Server
        :param event_name: 待校验event接口名
        :param event_info: 待校验event的数据
        :param method_name: 请求的接口名，默认直接按event前面加Get调用调用
        :param method_args: 请求接口的入参，默认不传
        :param resp_info: 请求的预期响应结果
        :param timeout: 等待预期的event超时
        :param fuzz_match: 是否模糊匹配
        """
        self.ck_s2s_event(partner_key, event_name, event_info, timeout, fuzz_match)
        if method_name is None:
            if "Notify" in event_name:
                method_name = event_name.replace("Notify", "Get")
            else:
                method_name = f"Get{event_name}"
        if resp_info is None:
            resp_info = {"out": list(event_info.values())[0]}
        if method_args is None:
            method_args = {}
        self.__send_request_and_ck_resp_once(partner_key, method_name, method_args, resp_info, fuzz_match)

    def ck_coming_event_and_resp(self, partner_key: str, event_name: str, event_info: dict,
                                 method_name=None, method_args=None, resp_info=None,
                                 timeout=3, fuzz_match=True, deviation=0):
        """
        校验到来的event，并调用get获取结果
        :param partner_key: 类似KeyService_Server
        :param event_name: 待校验event接口名
        :param event_info: 待校验event的数据
        :param method_name: 请求的接口名，默认直接按event前面加Get调用调用
        :param method_args: 请求接口的入参，默认不传
        :param resp_info: 请求的预期响应结果
        :param timeout: 等待预期的event超时
        :param fuzz_match: 是否模糊匹配
        :param deviation: 偏移量，默认0s，则只校验超时事件内有指定event即可，如果给定数值如0.2，则要求接收到的时间在指定t±0.2s时间内出现
        """
        self.ck_coming_event(partner_key, event_name, event_info, timeout, deviation, fuzz_match)
        if method_name is None:
            if "Notify" in event_name:
                method_name = event_name.replace("Notify", "Get")
            else:
                method_name = f"Get{event_name}"
        if resp_info is None:
            resp_info = {"out": list(event_info.values())[0]}
        if method_args is None:
            method_args = {}
        self.__send_request_and_ck_resp_once(partner_key, method_name, method_args, resp_info, fuzz_match)

    def ck_no_event_and_ck_resp(self, partner_key: str, event_name: str, resp_info: dict,
                                method_name=None, method_args=None,
                                timeout=1, fuzz_match=True):
        """
        反注册指定服务的指定event
        :param partner_key: 类似KeyService_Server
        :param event_name: 待校验event接口名
        :param resp_info: 请求的预期响应结果
        :param method_name: 请求的接口名，默认直接按event前面加Get调用调用
        :param method_args: 请求接口的入参，默认不传
        :param timeout: 等待预期的event超时
        :param fuzz_match: 是否模糊匹配
        """
        self.ck_no_event(partner_key, event_name, timeout)
        if method_name is None:
            if "Notify" in event_name:
                method_name = event_name.replace("Notify", "Get")
            else:
                method_name = f"Get{event_name}"
        if method_args is None:
            method_args = {}
        self.__send_request_and_ck_resp_once(partner_key, method_name, method_args, resp_info, fuzz_match)

    def ck_wti_warning_and_resp(self, hint: str, info: Union[int, str], timeout=1, wti_auto=False):
        """
        WTI测试专用接口，校验单个wti警示信息并调用get获取特定wti警示信息当前状态
        :param hint: 警示信息
        :param info: 警示信息状态，1或0
        :param timeout: 校验event的超时，默认1s
        :param wti_auto: WTIService还是WTIAutoDriveService
        """
        self.ck_event_and_resp(WTIAUTODRIVE_SERVICE_CLIENT if wti_auto else WTI_SERVICE_CLIENT,
                               "WarningMsgList",
                               {"list": [{"name": hint, "info": str(info)}]}, timeout=timeout)

    def ck_wti_telltale_and_resp(self, hint: str, state: Union[int, str], timeout=1, wti_auto=False):
        """
        WTI测试专用接口，校验单个wti警示灯并调用get获取特定wti警示灯当前状态
        :param hint: 警示信息
        :param state: 警示信息状态，1或0
        :param timeout: 校验event的超时，默认1s
        :param wti_auto: WTIService还是WTIAutoDriveService
        """
        self.ck_event_and_resp(WTIAUTODRIVE_SERVICE_CLIENT if wti_auto else WTI_SERVICE_CLIENT,
                               "TelltaleList",
                               {"list": [{"name": hint, "state": str(state)}]}, timeout=timeout)

    def ck_wti_coming_warning_and_resp(self, hint: str, info: Union[int, str], timeout=1, deviation=0, wti_auto=False):
        """
        WTI测试专用接口，校验单个wti警示信息并调用get获取特定wti警示信息当前状态
        :param hint: 警示信息
        :param info: 警示信息状态，1或0
        :param timeout: 校验event的超时，默认1s
        :param deviation: 偏移量，默认0s，则只校验超时事件内有指定event即可，如果给定数值如0.2，则要求接收到的时间在指定t±0.2s时间内出现
        :param wti_auto: WTIService还是WTIAutoDriveService
        """
        self.ck_coming_event_and_resp(WTIAUTODRIVE_SERVICE_CLIENT if wti_auto else WTI_SERVICE_CLIENT,
                                      "WarningMsgList",
                                      {"list": [{"name": hint, "info": str(info)}]},
                                      timeout=timeout,
                                      deviation=deviation)

    def ck_wti_coming_telltale_and_resp(self, hint: str, state: Union[int, str], timeout=1, deviation=0,
                                        wti_auto=False):
        """
        WTI测试专用接口，校验单个wti警示灯并调用get获取特定wti警示灯当前状态
        :param hint: 警示信息
        :param state: 警示信息状态，1或0
        :param timeout: 校验event的超时，默认1s
        :param deviation: 偏移量，默认0s，则只校验超时事件内有指定event即可，如果给定数值如0.2，则要求接收到的时间在指定t±0.2s时间内出现
        :param wti_auto: WTIService还是WTIAutoDriveService
        """
        self.ck_coming_event_and_resp(WTIAUTODRIVE_SERVICE_CLIENT if wti_auto else WTI_SERVICE_CLIENT,
                                      "TelltaleList",
                                      {"list": [{"name": hint, "state": str(state)}]},
                                      timeout=timeout,
                                      deviation=deviation)

    def ck_wti_no_warning_and_ck_resp(self, hint: str, info: Union[int, str], timeout=1, wti_auto=False):
        """
        WTI测试专用接口，校验无特定wti警示信息并调用get获取特定wti警示信息当前状态
        :param hint: 警示信息
        :param info: 警示信息状态，1或0
        :param timeout: 校验event的超时，默认1s
        :param wti_auto: WTIService还是WTIAutoDriveService
        """
        partner_key = WTIAUTODRIVE_SERVICE_CLIENT if wti_auto else WTI_SERVICE_CLIENT
        self.ck_no_specific_event(partner_key, "WarningMsgList", hint, timeout)
        self.send_request_and_ck_resp(partner_key, "GetWarningMsgList", {},
                                      {"out": [{"name": hint, "info": str(info)}]}, 
                                      timeout=0.2)

    def ck_wti_no_telltale_and_ck_resp(self, hint: str, info: Union[int, str], timeout=1, wti_auto=False):
        """
        WTI测试专用接口，校验无特定wti警示灯并调用get获取当前特定wti警示灯状态
        :param hint: 警示信息
        :param info: 警示信息状态，1或0
        :param timeout: 校验event的超时，默认1s
        :param wti_auto: WTIService还是WTIAutoDriveService
        """
        partner_key = WTIAUTODRIVE_SERVICE_CLIENT if wti_auto else WTI_SERVICE_CLIENT
        self.ck_no_specific_event(partner_key, "TelltaleList", hint, timeout)
        self.send_request_and_ck_resp(partner_key, "GetTelltaleList", {},
                                      {"out": [{"name": hint, "state": str(info)}]}, 
                                      timeout=0.2)

    "********************************************[以下为JET2.0专用接口]**************************************************"
    def ck_field(self, partner_key: str, field_name: str, field_info: dict, timeout=1, deviation=0, fuzz_match=True):
        """
        校验field数据是否正常
        @param partner_key: 对应服务名称
        @param field_name: 字段名称
        @param field_info: 字段数据
        @param timeout: 校验event的超时，默认1s
        @param deviation: 偏移量，默认0s，则只校验超时事件内有指定event即可，如果给定数值如0.2，则要求接收到的时间在指定t±0.2s时间内出现
        @param fuzz_match: 是否模糊匹配，默认True
        """
        if deviation:
            self.ck_coming_event(partner_key, field_name, field_info, timeout, deviation, fuzz_match)
        else:
            self.ck_s2s_event(partner_key, field_name, field_info, timeout, fuzz_match)
        resp_info = {"out": list(field_info.values())[0]}
        # 下发接口的timeout 2s为与开发zhewu对齐，认为系统调度+通信时延若超过2s，则需要排查是否是bug
        resp = self._send_request_and_return_resp_atom(partner_key, f"Get{field_name}", {},
                                                       timeout=2, is_async=True)
        raw_data = eval(resp['result'])
        if (fuzz_match and ck_data(raw_data, resp_info)) or (not fuzz_match and raw_data == resp_info):
            logger.info(f"校验Get{field_name}Async::{resp_info}--True")
            return True
        else:
            return False


if __name__ == '__main__':
    a = S2sBaseClass([
        ("cockpit_perception_service", "server"),
        ("WindowAppService", "client"),
        ("VehicleModeService", "client"),
        ("VehicleModeService", "client_1")
    ])
    time.sleep(200)
    # a = {"faults": [{"fault": 7, "faultMsg": "", "tyre": 0}, {"fault": 7, "faultMsg": "", "tyre": 1},
    #                 {"fault": 7, "faultMsg": "", "tyre": 2}, {"fault": 7, "faultMsg": "", "tyre": 3}]}
    # b = {'faults': [{'fault': 7, 'faultMsg': '', 'tyre': 3}]} 
    # print(ck_data(a, b))
