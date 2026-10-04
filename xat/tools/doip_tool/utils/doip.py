# -*- coding: utf-8 -*-
"""
@File        : doip.py
@Author      : yu.zhang0101 & jiankai.zhang
@Time        : 2022/04/13 4:01 PM
@Description : doip basic function

"""

import time
from .doip_client import DOIPClient
from .doip_config_parser import DoIPConfigParser
from .codecs import *
import udsoncan
from udsoncan import MemoryLocation
from threading import Lock
import logging


def decorator(func):
    def wrap_function(self, *args, **kwargs):
        config = DoIPConfigParser()
        ecu_logical_address = int(config.doipconfig["target_ecu"]["ecu_logical_address"], 16)
        logical_functional_address = int(config.doipconfig["target_ecu"]["logical_functional_address"], 16)

        if kwargs.get("func_addr", False):
            for index, _client in enumerate(self._function_client_list):
                self.logger.debug(f"self.func_lock.locked() {self.func_lock.locked()}, "
                                  f"self.lock {self.lock.locked()}, index={index}")
                # 2个报文间隙内发送3e80，如果一个报文没有返回（一直回复78），则此期间，不会发送3e80
                if index == 0 and self.lock.locked():
                    continue
                elif index == 0:
                    with self.lock:
                        self.logger.debug(f"in funclock, self.func_lock.locked() {self.func_lock.locked()}, "
                                          f"self.lock {self.lock.locked()}")
                        self._client = _client
                        self._client.suppress_positive_response.enabled = False
                        self._client.conn._connection._ecu_logical_address = logical_functional_address
                        if "enable_resp" in kwargs.keys():
                            self._client.suppress_positive_response.enabled = kwargs.get("enable_resp", False)
                        try:
                            func(self, *args, **kwargs)
                        except Exception as e:
                            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/doip_tool/utils/doip.py")
                            self.logger.debug(f"[Error][{func.__name__}][{args, kwargs}]{e}")
                else:
                    with self.func_lock:
                        self.logger.debug(f"in funclock, self.func_lock.locked() {self.func_lock.locked()}, "
                                          f"self.lock {self.lock.locked()}")
                        self._client = _client
                        self._client.suppress_positive_response.enabled = False
                        self._client.conn._connection._ecu_logical_address = logical_functional_address
                        if "enable_resp" in kwargs.keys():
                            self._client.suppress_positive_response.enabled = kwargs.get("enable_resp", False)
                        try:
                            func(self, *args, **kwargs)
                        except Exception as e:
                            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/doip_tool/utils/doip.py")
                            self.logger.debug(f"[Error][{func.__name__}][{args, kwargs}]{e}")
                # 周期发送3e80
                # with self.func_lock:
                #     print(f"in funclock, self.func_lock.locked() {self.func_lock.locked()}, self.lock {self.lock.locked()}")
                #     self._client = _client
                #     self._client.suppress_positive_response.enabled = False
                #     self._client.conn._connection._ecu_logical_address = logical_functional_address
                #     if "enable_resp" in kwargs.keys():
                #         self._client.suppress_positive_response.enabled = kwargs.get("enable_resp", False)
                #     try:
                #         func(self, *args, **kwargs)
                #     except Exception as e:
                #         print(f"[Error][{func.__name__}][{args, kwargs}]{e}")
        else:
            with self.lock:
                self.logger.debug(f"in logical lock, self.func_lock.locked() {self.func_lock.locked()}, "
                                  f"self.lock {self.lock.locked()}")
                self._client = self._logical_client
                self._client.suppress_positive_response.enabled = False
                self._client.conn._connection._ecu_logical_address = ecu_logical_address
                if "enable_resp" in kwargs.keys():
                    self._client.suppress_positive_response.enabled = kwargs.get("enable_resp", False)
                return func(self, *args, **kwargs)
    return wrap_function


class DOIP:

    def __init__(self, logger=None, auto_reconnect_tcp=False):
        self.logger = logger if logger else logging.getLogger("DOIP")
        self._client = None
        self._logical_client = None
        self._function_client_list = []
        self.auto_reconnect_tcp = auto_reconnect_tcp
        self._configs = dict(udsoncan.configs.default_client_config)
        self.r_resp_did = None
        self.w_resp_did = None
        self.routing_resp = None
        self.lock = Lock()
        self.func_lock = Lock()
        self._configs['data_identifiers'] = {
            0xF190: F190Codec,
            0xF186: F186Codec,
            0xF1AA: F1AACodec,
            0xF1AE: F1AECodec,
            0xF1AB: F1ABCodec,
            0x40DE: ECMCodec,
            0x40DF: IEMCodec,
            0x40E0: MGMCodec,
            0xF1A5: F1A5Codec,
            0xF106: F106Codec,
            0xD902: D902Codec,
            0xD260: D260Codec,
            0xF18C: F18CCodec,
            0xF1A0: F1A0Codec,
            0xF1F0: F1F0Codec,
            0xF124: F124Codec,
            0xD01C: D01CCodec,
            0xF102: F102Codec,
            0xED20: ED20Codec
        }

    def conn_logical(self):
        """
        连接目标ECU
        @return:
        """
        _doip_client = DOIPClient(logger=self.logger)
        _doip_client._configs = self._configs
        config = DoIPConfigParser()
        logical_config = {
            "ecu_ip": config.doipconfig["target_ecu"]["ecu_ip"],
            "ecu_logical_address": int(config.doipconfig["target_ecu"]["ecu_logical_address"], 16),
            "tester_ip": config.doipconfig["target_ecu"]["tester_ip"],
            "tester_logical_address": int(config.doipconfig["target_ecu"]["tester_logical_address"], 16),
            "suppress_positive_response": int(config.doipconfig["target_ecu"]["suppress_positive_response"])
        }
        self._logical_client = self._client = _doip_client.connect(json_config=logical_config,
                                                                   reconnect_tcp=self.auto_reconnect_tcp)
        self._function_client_list.append(self._client)
        self.logger.info(f"conn_logical success, and get client={self._client}")
        return self._client

    def conn_function(self):
        """
        连接其他ECU
        @return:
        """
        _doip_client = DOIPClient(logger=self.logger)
        _doip_client._configs = self._configs
        config = DoIPConfigParser()
        if "other_ecu" in config.doipconfig:
            for sub_config in config.doipconfig["other_ecu"]:
                sub_func_config = {"ecu_ip": sub_config["ecu_ip"],
                                   "ecu_logical_address": int(sub_config["logical_functional_address"], 16),
                                   "tester_ip": sub_config["tester_ip"],
                                   "tester_logical_address": int(sub_config["tester_logical_address"], 16),
                                   "suppress_positive_response": int(sub_config["suppress_positive_response"])
                                   }

                _client = _doip_client.connect(json_config=sub_func_config, reconnect_tcp=self.auto_reconnect_tcp)
                self._function_client_list.append(_client)
                self.logger.info(f"conn_logical success, and get client={self._client}")

    @decorator
    def close(self):
        """
        关闭客户端
        @return:
        """
        self._client.close()

    @decorator
    def session_control(self, newsession, **kwargs):
        """
        10会话
        @param newsession: 1，2，3
        @param kwargs:  func_addr：True（功能寻址），defalut=False（物理寻址）；
                        enable_resp：True（抑制响应），defalut=False（非抑制响应）
        @return:
        """
        _response = self._client.change_session(newsession)
        self.logger.info(f"request session control 0x10{8 if self._client.suppress_positive_response.enabled else 0}"
                         f"{newsession} success, and get response:{_response.code_name}, data: "
                         f"{_response.get_payload().hex()}")

    @decorator
    def ecu_reset(self, reset_type=1, **kwargs):
        """

        @param reset_type:
        @param kwargs:  func_addr：True（功能寻址），defalut=False（物理寻址）；
                        enable_resp：True（抑制响应），defalut=False（非抑制响应）
        @return:
        """
        _response = self._client.ecu_reset(reset_type)
        self.logger.info(f"request ecu reset 0x11{8 if self._client.suppress_positive_response.enabled else 0}"
                         f"{reset_type} success, and get response: {_response.code_name}, data: "
                         f"{_response.get_payload().hex()}")

    def unlock_process(self, level):
        """
        安全解锁
        @param level: 解锁等级
        @return:
        """
        self._client.suppress_positive_response.enabled = False
        seed = self.request_seed(level)
        value = self.get_seed_from_payload(seed)
        key = self.unlock_security_access(level, value)
        self.send_key(level, key)
        self.logger.info(f"request unlock process success")

    @decorator
    def request_seed(self, level, data=bytes()):  # request seed from target ecu
        """
        发送seed
        @param level: 解锁等级
        @param data:
        @return:
        """
        seed = self._client.request_seed(level, data)
        self.logger.info(f"request seed with level={level}, get response: {seed.code_name}, data: "
                         f"{seed.get_payload().hex()}")
        return seed

    @staticmethod
    def get_seed_from_payload(seed):
        """
        获取seed payload
        @param seed: seed
        @return:
        """
        _value = bytes()
        _payload = seed.get_payload()
        _value = _payload[::-1].hex()
        _value = _value[:6]
        return _value

    @staticmethod
    def unlock_security_access(level, value):  # calculate key from seed
        """
        从seed计算得到key
        @param level: 解锁等级
        @param value: seed值
        @return:
        """
        constant_lev1 = 0xFFFFFFFFFF
        constant_lev5 = 0x8ACD946BF5
        if level == 1:
            result = SecurityAlgorithm.cal_seed(seed=int(value, 16), constant=constant_lev1)
            result = result.to_bytes(3, 'little')
            return result
        elif level == 5:
            result = SecurityAlgorithm.cal_seed(seed=int(value, 16), constant=constant_lev5)
            result = result.to_bytes(3, 'little')
            return result

    @decorator
    def send_key(self, level, key):  # send calculate key to target ecu
        """
        发送key
        @param level: 解锁等级
        @param key: key
        @return:
        """
        _resp_key = self._client.send_key(level, key)
        self.logger.info(f"request send key with level={level}, get response: {_resp_key.code_name}, data:  "
                         f"{_resp_key.get_payload().hex()}")

    @decorator
    def routing_control(self, routine_id, control_type, data=None, **kwargs):
        """
        Routing Control
        @param routine_id: Int
        @param control_type: Int
        @param data:
        @param kwargs:  func_addr：True（功能寻址），defalut=False（物理寻址）；
                        enable_resp：True（抑制响应），defalut=False（非抑制响应）
        @return:
        """
        self._client.suppress_positive_response.enabled = False
        self.routing_resp = self._client.routine_control(routine_id, control_type, data)
        self.logger.info(f"request routing control 0x31 0{control_type} {hex(routine_id)} {data}, get response: "
                         f"get response: {self.routing_resp.code_name}, data: "
                         f"{self.routing_resp.get_payload().hex()}")

    @decorator
    def get_routine_payload(self):
        """
        获取routing control payload
        @return: routing control payload
        """
        if self.routing_resp:
            payload = self.routing_resp.get_payload()
            rout_value = payload.hex()
            self.logger.info(f"get routine payload: {rout_value}")
            return rout_value
        self.logger.info("Need send routing control command first.")

    @decorator
    def read_data_by_identifier(self, did):
        """
        Read Data By Identifier
        @param did: Did
        @return:
        """
        self._client.suppress_positive_response.enabled = False
        self.r_resp_did = self._client.read_data_by_identifier(did)
        self.logger.info(f"request ReadDataByIdentifier {hex(did)}, get response: {self.r_resp_did.code_name}, data: "
                         f"{self.r_resp_did.get_payload().hex()}")

    @decorator
    def get_read_did_payload(self):
        """
        获取DID payload
        @return: did value
        """
        if self.r_resp_did:
            payload = self.r_resp_did.get_payload()
            did_value = payload.hex()
            self.logger.info(f"get read did payload: {did_value}")
            return did_value
        self.logger.info("Need send read command first.")

    @decorator
    def write_data_by_identifier(self, did, data):
        """
        Write Data By Identifier
        @param did: DID
        @param data:
        @return:
        """
        self._client.suppress_positive_response.enabled = False
        self.w_resp_did = self._client.write_data_by_identifier(did, data)
        self.logger.info(f"request WriteDataByIdentifier {hex(did)} with data {data}, get response: "
                         f"{self.w_resp_did.code_name}, data: {self.w_resp_did.get_payload().hex()}")

    @decorator
    def get_write_did_payload(self):
        """
        获取写did的返回值
        @return:
        """
        if self.w_resp_did:
            payload = self.w_resp_did.get_payload()
            did_value = payload.hex()
            self.logger.info(f"get write did payload: {did_value}")
            return did_value
        self.logger.info("Need send write command first.")

    @decorator
    def request_download(self, memory_location=None, dfi=None):
        """
        Request Download
        @param memory_location:
        @param dfi:
        @return:
        """
        if memory_location is None:
            memory_location = MemoryLocation(0, 8, address_format=16)
        _response = self._client.request_download(memory_location, dfi=dfi)
        self.logger.info(f"request download, get response: {_response.code_name}, data: "
                         f"{_response.get_payload().hex()}")

    @decorator
    def transfer_data(self, sequence_number=None, data=None):
        """
        Transfer Data
        @param sequence_number:
        @param data:
        @return:
        """
        if sequence_number is None:
            sequence_number = 1
        _response = self._client.transfer_data(sequence_number, data=data)
        self.logger.info(f"request transfer data, get response: {_response.code_name}, data: "
                         f"{_response.get_payload().hex()}")

    @decorator
    def request_transfer_exit(self, data=None):
        """
        Transfer Data Exit
        @param data:
        @return:
        """
        _response = self._client.request_transfer_exit(data=data)
        self.logger.info(f"request transfer data exit, get response: {_response.code_name}, data: "
                         f"{_response.get_payload().hex()}")

    @decorator
    def get_routine_result(self, routine_id, data=None):
        """
        get routing control result
        @param routine_id:
        @param data:
        @return:
        """
        _response = self._client.get_routine_result(routine_id, data=data)
        self.logger.info(f"request get routine result with routine_id={routine_id}, data={data}, get response: "
                         f"{_response.code_name}, data: {_response.get_payload().hex()}")
        return _response

    @decorator
    def tester_present(self, **kwargs):
        """
        Send tester present
        @param kwargs:  func_addr：True（功能寻址），defalut=False（物理寻址）；
                        enable_resp：True（抑制响应），defalut=False（非抑制响应）
        @return:
        """
        self._client.tester_present()
        self.logger.info(f"request tester present")


class SecurityAlgorithm:
    """
    Security Algorithm
    """

    def __init__(self):
        self.seed = None
        self.constant = None
        self.result = None
        self.temp = None
        self.temp_1 = None
        self.temp_2 = None
        self.temp_3 = None

    @staticmethod
    def cal_seed(seed, constant):
        seed &= 0x00FFFFFF
        result = 0x00C541A9
        constant <<= 24
        constant |= seed

        for i in range(0, 64):
            temp = constant & 0x00000001
            temp = result ^ temp
            result >>= 1
            temp <<= 23
            temp &= 0x00800000
            result |= temp  # B24
            temp >>= 3
            result = ((temp ^ result) & 0x00100000) | (result & (~0x00100000))  # B21
            temp >>= 5
            result = ((temp ^ result) & 0x00008000) | (result & (~0x00008000))  # B16
            temp >>= 3
            result = ((temp ^ result) & 0x00001000) | (result & (~0x00001000))  # B13
            temp >>= 7
            result = ((temp ^ result) & 0x00000020) | (result & (~0x00000020))  # B6
            temp >>= 2
            result = ((temp ^ result) & 0x00000008) | (result & (~0x00000008))  # B4
            constant >>= 1

        temp_1 = result | 0x00
        temp_2 = (result >> 8) | 0x00
        temp_3 = (result >> 16) | 0x00
        result >>= 4  # Response Byte1
        result &= 0xFF0000FF
        temp_2 = (temp_3 >> 4) | (temp_2 & 0xF0)
        result |= ((0x0000 | temp_2) << 8)  # Response Byte2
        result |= (((0x000000 | ((temp_1 << 4) | (temp_3 & 0x0F)))) << 16)  # Response Byte3
        result &= 0x00FFFFFF  # Discard Byte4
        return result


if __name__ == '__main__':
    d = DOIP()
    d.conn_logical()
    time.sleep(0.4)
    # d.session_control(3)
    # d.routing_control(518, 1)
    # d.request_seed(1)
    # d.unlock_security_access(1)
    # d.send_key(1, b"\x11\x22\x33\x44")
    # d.write_data_by_identifier(0xD01c, 0xFFFFFFFFFF)
    # d.write_data_by_identifier(0xf102, 0xFFFFFFFFFF)
    # d.routing_control(0xFF00, 1)
    # d.routing_control(0x0212, 1, b'\x00\x11\x22\x33\x44')
    # d.routing_control(0x0205, 1)
    d.ecu_reset(1)
    time.sleep(2)
