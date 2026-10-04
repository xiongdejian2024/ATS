#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :digital_key_class.py
@Time         :2023/1/23 13:50
@Author       :jiabin.zhu@jiduauto.com
@Description  :
"""
import os
import sys
from xat_ecu import reporting as allure
import can
import time
import inspect
import ctypes

from time import sleep
from typing import List, Union, Optional
from queue import Queue
from threading import Thread

from xat_ecu.legacy.sdk.i_signal_i_pdu import ISignalIPdu
from xat_ecu.legacy.sdk.bus_app import BusApp
from xat_ecu.legacy.sdk.digital_key.RVCTSPMessage_pb2 import *
from xat_ecu.legacy.sdk.digital_key.digital_key_can_protocol import BncmBgmPduEncrypt
from xat_ecu.legacy.sdk.digital_key.digital_key_const import *
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding
from xat_ecu.legacy.common.logger import logger

DigKeyBLEReq = 0x166  # BNCM send
DigKeyBLEResp = 0x157  # BGM send
DigKeyBLEReq2 = 0x30  # BGM send
DigKeyBLEResp2 = 0x149  # BNCM send
DigKeyBLEReq3 = 0x176  # BNCM send
DigKeyBLEResp3 = 0x175  # BGM send


def format_assert_log(sts_name, current_key, expect_key, mapping={}):
    """格式化assert的打印信息"""
    return f"{time.time()}--当前{sts_name}为{current_key}: {mapping.get(current_key, '')}, " \
           f"不满足预期{expect_key}: {mapping.get(expect_key, '')}"


def print_msg_info(msg):
    """回调函数使用, 打印关注的msg信息"""
    logger.info(
        f"\n{' ' * 20}Rx-ID:{hex(msg[0])} Timestamp: {msg[1]} DL:{msg[2]} Data: {DataTypeHanding.to_hexstr(msg[3])}")


def _async_raise(tid, exctype):
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(tid), ctypes.py_object(exctype))
    if res == 0:
        pass
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


class DigitalKey:
    """数字钥匙测试用例类"""

    def __init__(self, ipdu: ISignalIPdu, busapp: BusApp, nucapp, tc_config, auto_start=True):
        self.ipdu = ipdu
        self.busapp = busapp
        self.nucapp = nucapp
        self.tc_config = tc_config
        self.dk_can_encrypt = BncmBgmPduEncrypt(DataTypeHanding.to_bytes(self.tc_config.get("BNCM_KEY", BNCM_KEY)))
        self.vid = self.tc_config.get('vid')

        self.auto_ack_tsp_ble_sync_cmd = True  # 默认BNCM自动响应云端的白名单控制指令
        self.last_sync_time_entity = tc_config.get('last_sync_time_entity', 1)
        self.last_sync_time_ble = tc_config.get('last_sync_time_ble', 1)
        self.bncm_keyinfo = {loc.value: [] for loc in Location}
        self.get_bgm_send_idle_count = 0  # BGM在发送错误帧后发送的空白帧次数, 达到2次后可以再次发送
        # BGM每发送一个数据包是否有收到ack应答报文(响应报文ack=发送报文header)
        self.get_dk_bgm_ack = False
        self.dk_req_header_0x166 = 0  # BNCM下发的车控报文的header
        self.dk_req_header_0x176 = 0  # BNCM下发的数据包的header
        self.dk_req_header_0x149 = 0  # BNCM下发的数据包的header
        self.header_map = {0x166: self.dk_req_header_0x166, 0x176: self.dk_req_header_0x176,
                           0x149: self.dk_req_header_0x149}
        self.dk_data_queue_internal = Queue()  # 内部使用用于获取并响应寻钥匙结果, 存储bytes的原始数据
        self.dk_data_queue_tsp = Queue()  # 接收BGM发送的云端数据
        self.dk_data_queue_key_search = Queue()  # 接收BGM发送的寻钥匙指令
        self.dk_data_queue_vehicle_control = Queue()  # 接收BGM发送的车控指令
        self.dk_raw_data = Queue()  # 接收所有的DK原始数据

        self.dk_data_0x30 = list()  # BGM发送的寻钥匙指令（密文)
        self.dk_data_0x175 = list()  # BGM发送的车控响应报文（密文)
        self.dk_data_len_0x30 = 0  # 从hello_message中获取的报文长度, 用于截取有效数据
        self.dk_data_len_0x175 = 0  # 从hello_message中获取的报文长度, 用于截取有效数据
        self.last_dk_ble_resp_header_0x30 = 0  # 记录BGM发送的0x30报文的header, 防止BGM发送相同header报文时, 代码重复截取有效数据
        self.last_dk_ble_resp_header_0x175 = 0  # 记录BGM发送的0x175报文的header, 防止BGM发送相同header报文时, 代码重复截取有效数据

        self.id_map = {DigKeyBLEReq: DigKeyBLEResp, DigKeyBLEResp: DigKeyBLEReq,
                       DigKeyBLEResp2: DigKeyBLEReq2, DigKeyBLEReq2: DigKeyBLEResp2,
                       DigKeyBLEReq3: DigKeyBLEResp3, DigKeyBLEResp3: DigKeyBLEReq3}
        if auto_start:
            self.start_dk()

    def start_dk(self):
        """
        抽象接口启动数字钥匙模块
        """
        self.ipdu.preheat_msg("connectivitycanfd", "BncmConnectivityFr07")
        self.ipdu.preheat_msg("connectivitycanfd", "BncmConnectivityFr08")
        self.ipdu.preheat_msg("connectivitycanfd", "BncmConnectivityFr16")
        sleep(2)
        self.ipdu.recv_pdu_thread_start('connectivitycanfd', 'VgmConnFr16', self.__listen_dk_bgm_ack)  # 0x157
        self.ipdu.recv_pdu_thread_start('connectivitycanfd', 'BgmConnectivityFr05', self.__listen_dk_ble_resp)  # 0x175
        self.ipdu.recv_pdu_thread_start('connectivitycanfd', 'VgmConnFr28', self.__listen_dk_ble_resp)  # 0x30
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.start_listen_dk_bgm_response()  # 启动线程监测BGM的dk数据并存入队列
    
    def stop_dk(self):
        """
        抽象接口停止数字钥匙模块
        """
        self.stop_listen_dk_bgm_response()

    def connectivity_send_pdu(self, canid, pdu):
        """封装一层Connectivity CanFD报文的发送"""
        self.ipdu.send_pdu("connectivitycanfd", canid, pdu)
        logger.info(
            f"\n{' ' * 20}Tx-ID:{hex(canid)} Timestamp: {time.time()} DL:{len(pdu)} Data: {DataTypeHanding.to_hexstr(pdu)}")

    def stop_listen_dk_bgm_response(self):
        """
        结束监视BGM和BNCM的报文交互
        """
        stop_thread(self.thread_listen_dk_bgm_response)

    def start_listen_dk_bgm_response(self):
        """
        监控BGM发出的报文, 可能是车控结果响应, 或寻钥匙指令, 或白名单更新指令, 若为寻钥匙指令, 则发送寻钥匙结果
        """
        self.thread_listen_dk_bgm_response = Thread(
            target=self.__thread_for_response_to_search_key, daemon=True)
        self.thread_listen_dk_bgm_response.start()

    def __thread_for_response_to_search_key(self):
        """
        另起一个线程将原始数据放入external队列用例获取并作进一步校验, 若是寻钥匙指令或白名单控制则自动响应
        """
        while True:
            try:
                sleep(0.005)
                data = self.dk_data_queue_internal.get()
                plain_data = self.dk_can_encrypt.decrypt_cmd(data)
                cmd_str = DataTypeHanding.intlist_to_hexstr(plain_data)
                function_id = plain_data[0]
                if function_id == 0x51:  # 寻钥匙指令
                    self.dk_data_queue_key_search.put(plain_data)
                    logger.info(f"\n{' ' * 20}接收到寻钥匙指令: {cmd_str}")
                    time.sleep(0.1)  # 等待0.1s后发送寻钥匙结果
                    self.__send_search_key_response(plain_data[1])
                else:
                    # todo: 其他车控指令
                    if function_id == 0xFF:
                        sub_id = plain_data[1]
                        if sub_id == 0x1:
                            self.dk_data_queue_tsp.put(plain_data)
                            self.last_sync_time_entity = DataTypeHanding.to_int(plain_data[4: 12])
                            logger.info(f"\n{' ' * 20}接收到云端下发实体钥匙白名单更新: {cmd_str}")
                            logger.info(f"\n{' ' * 20}last_sync_time_entity: {self.last_sync_time_entity}")
                            if self.auto_ack_tsp_ble_sync_cmd:
                                self.send_while_list_update_resp(0x11, 0x00, self.last_sync_time_entity)
                        elif sub_id == 0x2:
                            self.dk_data_queue_tsp.put(plain_data)
                            self.last_sync_time_ble = DataTypeHanding.to_int(plain_data[4: 12])
                            logger.info(f"\n{' ' * 20}接收到云端下发蓝牙钥匙白名单更新: {cmd_str}")
                            logger.info(f"\n{' ' * 20}last_sync_time_ble: {self.last_sync_time_ble}")
                            if self.auto_ack_tsp_ble_sync_cmd:
                                self.send_while_list_update_resp(0x12, 0x00, self.last_sync_time_ble)
                        elif sub_id == 0x4:
                            self.dk_data_queue_tsp.put(plain_data)
                            logger.info(f"\n{' ' * 20}接收到云端下发NFC学卡请求: {cmd_str}")
                        else:
                            self.dk_data_queue_vehicle_control.put(plain_data)
                            real_resp = RealtimeCmdResp()
                            real_resp.ParseFromString(plain_data[5:])
                            logger.info(real_resp)
                            logger.info(f"\n{' ' * 20}接收到车控结果: {cmd_str}")
                    else:
                        real_resp = RealtimeCmdResp()
                        real_resp.ParseFromString(plain_data[5:])
                        logger.info(real_resp)
                        self.dk_data_queue_vehicle_control.put(plain_data)
                        logger.info(f"\n{' ' * 20}接收到车控结果, 更新下描述: {cmd_str}")
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/digital_key/digital_key_class.py")
                logger.error(e)

    def __send_search_key_response(self, location: int, key_infos=None):
        """
        发送寻钥匙结果
        :param location: 寻钥匙区域
        :param key_infos: 需要的钥匙信息[{keyType: int, keyID: ints, status: int}...], 不填则以已存在数据响应
        :return:
        """
        if key_infos is None:
            key_infos = self.bncm_keyinfo[location]
        logger.info(f"发送寻钥匙结果, 寻钥匙区域{location}")
        key_no = len(key_infos)
        data = [0x52, key_no]
        for key_info in key_infos:
            data.extend(key_info)
        self.send_bncm_frame(
            DigKeyBLEResp2, self.dk_can_encrypt.assamble_encrypt_message(
                self.dk_can_encrypt.bgm_time + DataTypeHanding.intlist_to_hexstr(data)))

    def send_idle_three_times(self, canid=DigKeyBLEReq):
        """周期10ms发送三次空白帧, 使通信恢复正常"""
        logger.info("发送空白帧恢复通信")
        self.connectivity_send_pdu(canid, [0] * 64)
        time.sleep(0.02)
        self.connectivity_send_pdu(canid, [0] * 64)
        time.sleep(0.02)

    def wait_for_bgm_dk_data(self, msg, can_id=None):
        """
        监控BGM发送的给BNCM的所有DK数据
        :param msg: (msg_id, timestamp(报文时间戳), msg_length, msg_data(intlist类型的pdu数据))
        :param can_id: 指定canid, 若不填则监控所有报文
        :return:
        """
        if isinstance(msg, can.message.Message):
            if can_id is not None and msg.arbitration_id != can_id:
                return
            msg = (msg.arbitration_id, msg.timestamp, msg.dlc, msg.data)
        self.dk_raw_data.put(msg)
        print_msg_info(msg)

    def reset_bncm_digital_keyinfo(self):
        """重置钥匙信息, 当前任何区域无钥匙"""
        self.bncm_keyinfo = {loc.value: [] for loc in Location}  # 承载不同钥匙区域内的钥匙信息

    def update_keyinfos(self, location: Union[Location, int], keys: List[KeyInfo]):
        """
        配置不同寻钥匙区域, 返回的钥匙信息, 可以是多个钥匙
        :param location: 寻钥匙区域, int类型或者Location类型
        :param keys: 钥匙信息
        :return:
        """
        # 一个钥匙信息表示为18字节列表
        with allure.step(f"更新钥匙区域{location}的钥匙状态: {keys}"):
            if isinstance(location, Location):
                location = location.value
            self.bncm_keyinfo[location] = [key.format_key_info() for key in keys]

    def send_bncm_frame(self, canid: int, pdus: list):
        """
        模拟发送BNCM指令, 包括车控请求指令, 寻钥匙响应(发送过程中校验ack)
        :param canid: 发送的canid
        :param pdus: 发送的报文列表
        :param repeat: 发送中遇到错误是否要重发
        :return:
        """
        res = self._send_dk_frame(canid, pdus)
        assert res, "发送数字钥匙指令未获取到正响应"

    def __listen_dk_ble_resp(self, msg, can_id=None):
        """
        监控BGM发送的车控响应报文0x175和寻钥匙报文0x30, 并响应ack,将数据放入队列
        :param msg: (msg_id, timestamp(报文时间戳), msg_length, msg_data(intlist类型的pdu数据))
        :return:
        """
        if isinstance(msg, can.message.Message):
            if can_id is not None and msg.arbitration_id != can_id:
                return
            msg = (msg.arbitration_id, msg.timestamp, msg.dlc, msg.data)
        print_msg_info(msg)
        msg_id = msg[0]
        msg_data = msg[3]
        header = msg_data[0]
        if header == 0x0:  # BGM发出的响应帧
            if msg_data[-1] != self.header_map[self.id_map[msg_id]]:
                logger.info("BGM响应的ack字段和发送的BNCM发送header不一致")
            else:
                self.get_dk_bgm_ack = True  # 接收到BGM发出数据帧的正常ack应答
            return
        elif header == 0xFF:  # BGM发出的错误帧
            return
        else:  # BGM发出的数据帧
            self.connectivity_send_pdu(self.id_map[msg[0]], [0x00] * 63 + [msg_data[0]])  # 发送响应帧
            if msg_id == 0x30:
                if header == self.last_dk_ble_resp_header_0x30:
                    return
                self.last_dk_ble_resp_header_0x30 = header
                if header == 0x1:  # hello_message
                    self.dk_data_len_0x30 = (msg_data[5] << 8) + msg_data[6]
                    self.dk_data_0x30 = list()
                else:
                    rest_length = self.dk_data_len_0x30 - len(self.dk_data_0x30)
                    if rest_length <= 62:
                        self.dk_data_0x30 += msg_data[1: 1 + rest_length]
                        self.dk_data_queue_internal.put(self.dk_data_0x30)
                    else:
                        self.dk_data_0x30 += msg_data[1: 63]
            else:
                if header == self.last_dk_ble_resp_header_0x175:
                    return
                self.last_dk_ble_resp_header_0x175 = header
                # 数据帧
                if header == 0x1:  # hello_message
                    self.dk_data_len_0x175 = (msg_data[5] << 8) + msg_data[6]
                    self.dk_data_0x175 = list()
                else:
                    rest_length = self.dk_data_len_0x175 - len(self.dk_data_0x175)
                    if rest_length <= 62:
                        self.dk_data_0x175 += msg_data[1: 1 + rest_length]
                        self.dk_data_queue_internal.put(self.dk_data_0x175)
                    else:
                        self.dk_data_0x175 += msg_data[1: 63]

    def __listen_dk_bgm_ack(self, msg, can_id=None):
        """
        监控BNCM下发指令后BGM的0x157ack报文, 若异常则发送错误帧
        :param msg: (msg_id, timestamp(报文时间戳), msg_length, msg_data(intlist类型的pdu数据))
        :param can_id: 回调函数的报文id
        :return:
        """
        if isinstance(msg, can.message.Message):
            if can_id is not None and msg.arbitration_id != can_id:
                return
            msg = (msg.arbitration_id, msg.timestamp, msg.dlc, msg.data)
        print_msg_info(msg)
        msg_data = msg[3]
        header = msg_data[0]
        msg_id = msg[0]
        if header == 0xFF:  # 接收到BGM发的错误帧
            logger.error("BGM异常发送错误帧")
            self.connectivity_send_pdu(self.id_map[msg_id], [0x00] * 63 + [0xFF])
        elif header == 0x0:  # 发送报文的header强制为0
            if msg_data == [0x0] * 64:  # 接收到BGM发出空白帧
                self.get_bgm_send_idle_count += 1
            else:
                if msg_data[-1] != self.header_map[self.id_map[msg_id]]:
                    logger.info("BGM响应的ack字段和发送的BNCM发送header不一致")
                else:
                    self.get_dk_bgm_ack = True  # 接收到BGM发出数据帧的正常ack应答

    def _send_dk_frame(self, can_id: int, pdus: list) -> bool:
        """
        发送BNCM数字钥匙相关的报文
        :param can_id: 发送的can_id
        :param pdus: 发送的报文列表
        :return: 是否发送成功
        """
        for pdu in pdus:
            self.header_map[can_id] = pdu[0]
            # self.connectivity_send_pdu(can_id, pdu)
            # self.get_dk_bgm_ack = False
            # start_time = time.time()
            # while time.time() - start_time < 0.1:
            #     time.sleep(0.02)
            #     if self.get_dk_bgm_ack:  # 收到正常ack, 跳出发下一条
            #         break
            #     self.connectivity_send_pdu(can_id, pdu)
            # else:  # 超时, 发送错误帧及空白帧, 并跳出发送
            #     logger.error("发送指令后BGM未在100ms内发送ack")  # todo: 子线程内报错, 主线程感知不到, 只能打印
            #     return False
            time.sleep(0.02)
            self.connectivity_send_pdu(can_id, pdu)
        return True

    def send_approach_light_cmd(self, key_type: int = 2, key_id=key_id1):
        """
        发送靠近迎宾指令
        :param key_type: 指令触发源钥匙类型, 默认蓝牙
        :param key_id: 数字钥匙keyid
        :return:
        """
        with allure.step("模拟下发靠近迎宾指令"):
            logger.info("发送靠近迎宾指令")
            self.send_bncm_frame(DigKeyBLEReq, self.dk_can_encrypt.peps_approach(key_type, 1, key_id))
            time.sleep(0.05)  # 等待50ms, 确保BGM发出解闭锁指令

    def send_approach_unlock_cmd(self, key_type: int = 2, key_id=key_id1):
        """
        发送近车解锁指令
        :param key_type: 指令触发源钥匙类型, 默认蓝牙
        :param key_id: 数字钥匙keyid
        :return:
        """
        with allure.step("模拟下发近车解锁指令"):
            logger.info("发送近车解锁指令")
            self.send_bncm_frame(DigKeyBLEReq, self.dk_can_encrypt.peps_approach(key_type, 2, key_id))
            time.sleep(0.05)  # 等待50ms, 确保BGM发出解闭锁指令

    def send_walk_away_lock_cmd(self, key_type: int = 2):
        """
        发送离车闭锁指令
        :param key_type: 指令触发源钥匙类型, 默认蓝牙
        :return:
        """
        with allure.step("模拟下发离车闭锁指令"):
            logger.info("发送离车上锁指令")
            self.send_bncm_frame(DigKeyBLEReq, self.dk_can_encrypt.peps_approach(key_type, 3))
            time.sleep(0.05)  # 等待50ms, 确保BGM发出解闭锁指令

    def send_charge_pile_open_charge_lid_cmd(self, action: int = 1):
        with allure.step("模拟下发充电桩蓝牙充电口盖控制"):
            logger.info("发送充电桩蓝牙充电口盖控制")
            self.send_bncm_frame(DigKeyBLEReq, self.dk_can_encrypt.charge_pile_open_charge_lid(action))

    def press_door_outswitch(self, door_index: int, timeout: Union[int, float]):
        """
        按下四门或尾门外开关
        :param door_index: 1:主驾门; 2:副驾门; 3:左后门; 4:右后门; 5: 尾门
        :param timeout: 按下按钮持续时长
        :return:
        """
        tag = f"模拟按下{door_desc[door_index]}外开关, 持续{timeout}后松开"
        logger.info(tag)
        with allure.step(tag):
            if door_index == 1:
                self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrOpenReqOutdSwt2', 'PsdNotPsd3_Psd')
                self.nucapp.drvr_door_outswitch_pressed()
                time.sleep(timeout)
                self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrOpenReqOutdSwt2', 'PsdNotPsd3_NotPsd')
                self.nucapp.drvr_door_outswitch_unpressed()
            elif door_index == 2:
                self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassOpenReqOutdSwt2', 'PsdNotPsd3_Psd')
                self.nucapp.pass_door_outswitch_pressed()
                time.sleep(timeout)
                self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassOpenReqOutdSwt2', 'PsdNotPsd3_NotPsd')
                self.nucapp.pass_door_outswitch_unpressed()
            elif door_index == 3:
                self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DoorLeReOpenReqOutdSwt2', 'PsdNotPsd3_Psd')
                self.nucapp.lere_door_outswitch_pressed()
                time.sleep(timeout)
                self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DoorLeReOpenReqOutdSwt2', 'PsdNotPsd3_NotPsd')
                self.nucapp.lere_door_outswitch_unpressed()
            elif door_index == 4:
                self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorRiReOpenReqOutdSwt2', 'PsdNotPsd3_Psd')
                self.nucapp.rire_door_outswitch_pressed()
                time.sleep(timeout)
                self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorRiReOpenReqOutdSwt2', 'PsdNotPsd3_NotPsd')
                self.nucapp.rire_door_outswitch_unpressed()
            elif door_index == 5:
                self.nucapp.trunk_door_outswitch_pressed()
                time.sleep(timeout)
                self.nucapp.trunk_door_outswitch_unpressed()

    def press_door_inswitch(self, door_index: int, timeout: Union[int, float]):
        """
        按下四门或尾门内开关
        :param door_index: 1:主驾门; 2:副驾门; 3:左后门; 4:右后门; 5: 尾门
        :param timeout: 按下按钮持续时长
        :return:
        """
        tag = f"模拟按下{door_desc[door_index]}内开关, 持续{timeout}后松开"
        logger.info(tag)
        with allure.step(tag):
            if door_index == 1:
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'DoorDrvrOpenReqInsdSwt1', 'PsdNotPsd3_Psd')
                self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrOpenReqInsdSwt2', 'PsdNotPsd3_Psd')
                time.sleep(timeout)
                self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'DoorDrvrOpenReqInsdSwt1', 'PsdNotPsd3_NotPsd')
                self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrOpenReqInsdSwt2', 'PsdNotPsd3_NotPsd')
            elif door_index == 2:
                self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'DoorPassOpenReqInsdSwt1', 'PsdNotPsd3_Psd')
                self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassOpenReqInsdSwt2', 'PsdNotPsd3_Psd')
                time.sleep(timeout)
                self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'DoorPassOpenReqInsdSwt1', 'PsdNotPsd3_NotPsd')
                self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassOpenReqInsdSwt2', 'PsdNotPsd3_NotPsd')
            elif door_index == 3:
                self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'DoorLeReOpenReqInsdSwt1', 'PsdNotPsd3_Psd')
                self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DoorLeReOpenReqInsdSwt2', 'PsdNotPsd3_Psd')
                time.sleep(timeout)
                self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'DoorLeReOpenReqInsdSwt1', 'PsdNotPsd3_NotPsd')
                self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DoorLeReOpenReqInsdSwt2', 'PsdNotPsd3_NotPsd')
            elif door_index == 4:
                self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'DoorRiReOpenReqInsdSwt1', 'PsdNotPsd3_Psd')
                self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorRiReOpenReqInsdSwt2', 'PsdNotPsd3_Psd')
                time.sleep(timeout)
                self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'DoorRiReOpenReqInsdSwt1', 'PsdNotPsd3_NotPsd')
                self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorRiReOpenReqInsdSwt2', 'PsdNotPsd3_NotPsd')

    def set_door_sts(self, door_sts: List[int]):
        """
        硬线设置5门状态, {0: 关, 1: 开}
        :param door_sts: 5个门状态, 左前, 右前, 左后, 右后, 尾门: {0: 关, 1: 开}
        :return:
        """
        with allure.step(f"设置门状态{door_sts}"):
            for index in range(len(door_sts)):
                if index == 0:
                    if door_sts[index]:
                        self.nucapp.drvr_door_open()
                    else:
                        self.nucapp.drvr_door_close()
                elif index == 1:
                    if door_sts[index]:
                        self.nucapp.pass_door_open()
                    else:
                        self.nucapp.pass_door_close()
                elif index == 2:
                    if door_sts[index]:
                        self.nucapp.lere_door_open()
                    else:
                        self.nucapp.lere_door_close()
                elif index == 3:
                    if door_sts[index]:
                        self.nucapp.rire_door_open()
                    else:
                        self.nucapp.rire_door_close()
                else:
                    if door_sts[index]:
                        self.nucapp.trunk_door_open()
                    else:
                        self.nucapp.trunk_door_close()

    def cenlock_sts(self):
        """返回当前中控锁状态"""
        return self.ipdu.get_recent_signal_raw_value(self.ipdu.connectivitycanfd.VgmConnFr12,
                                                     'LockgCenStsLockSt_2_VgmConnSignalIPdu12')

    def set_cenlock_sts(self, sts: int):
        """
        设置中控锁状态
        :param sts: 1: Unlolcked, 2: TrUnlock, 3: Locked
        :return:
        """
        with allure.step(f"设置LockgCenSts = {cenlock_sts_desc[sts]}"):
            curr_sts = self.cenlock_sts()
            logger.info("设置前中控锁状态: %d %s, 目标状态:%d %s", curr_sts, cenlock_sts_desc[curr_sts],
                        sts, cenlock_sts_desc[sts])
            if sts == 2 and curr_sts != 2:
                self.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
                if curr_sts == 1:
                    self.send_nfc_cmd()
                    sleep(1)
                self.ck_cenlock_sts(3)
                logger.info("先设置整车闭锁, 再执行解锁尾门")
                self.press_door_outswitch(5, 0.5)
                self.ck_cenlock_sts(2, timeout=2)
            elif sts == 3 and curr_sts != 3:
                if curr_sts == 2:
                    self.send_nfc_cmd()
                    sleep(1)
                self.ck_cenlock_sts(1)
                logger.info("先设置整车解锁, 再执行闭锁")
                self.send_nfc_cmd()
                self.ck_cenlock_sts(3, timeout=2)
            elif sts == 1 and curr_sts != 1:
                self.send_nfc_cmd()
                self.ck_cenlock_sts(1)
            else:
                pass
            self.empty_dk_data_queue()

    def send_nfc_cmd(self, key_id: Union[int] = None):
        """
        发送NFC刷卡事件
        """
        logger.info("发送NFC刷卡事件")
        if key_id is None:
            key_id = key_id1
        self.send_bncm_frame(DigKeyBLEReq, self.dk_can_encrypt.nfc_lock_cmd(key_id))

    def send_apa_cmd(self, action: int, account_info: str):
        """
        模拟手机app发送蓝牙APA请求
        :param action: APA指令
        0 = NO_REQUEST
        1 = RPA_START
        2 = APA_QUIT
        3 = PARK_OUT_MODE
        4 = APA_PARK_OUT
        5 = PARK_OUT_FRONT_LEFT（修改)
        6 = PARK_OUT_FRONT_RIGHT（修改)
        7 = PARK_OUT_REAR_LEFT（修改)
        8 = PARK_OUT_REAR_RIGHT（修改)
        9 = PARK_OUT_LEFT_FRONT（修改)
        10 = PARK_OUT_RIGHT_FRONT（修改)
        11 = APA_PAUSING
        12 = APA_CONTINUE
        13 = QUIT_MOBILE_LOW_POWER
        14=PARK_OUT_FRONT（新增)
        15=PARK_OUT_REAR（新增)
        :param account_info: 8字节字符串
        :return:
        """
        logger.info("发送APA事件")
        self.send_bncm_frame(DigKeyBLEReq, self.dk_can_encrypt.apa_cmd(action, account_info))

    def send_avp_cmd(self, action: int, account_info: str):
        """
        模拟手机app发送蓝牙AVP请求
        :param action: avp指令
        0 = AVPFct_NoReq
        1 = AVPFct_StartPrepare
        2 = AVPFct_Start
        3 = AVPFct_Stop
        4 = AVPFct_StopRecover
        5 = AVPFct_Out
        6 = AVPFct_Reserve1
        7 = AVPFct_Reserve2
        :param account_info: 8字节字符串
        :return:
        """
        logger.info("发送AVP事件")
        self.send_bncm_frame(DigKeyBLEReq, self.dk_can_encrypt.avp_cmd(action, account_info))

    def set_central_lock(self, sts: int):
        """
        设置中控锁状态, 只能NFC解锁和闭锁
        :param sts: 1:Unlolcked, 2: TrUnlock, 3: Locked
        :return:
        """
        if self.cenlock_sts() != sts:
            self.send_nfc_cmd()
            time.sleep(0.5)
            if self.cenlock_sts() != sts:  # 本来是TrUnlock, 刷NFC卡是解锁, 如果要设置闭锁, 需要再执行刷卡
                self.send_nfc_cmd()
                time.sleep(0.5)
        curr_sts = self.cenlock_sts()
        logger.info("当前中控锁状态: %d %s", curr_sts, cenlock_sts_desc[curr_sts])

        assert curr_sts == sts, format_assert_log("NFC刷卡后中控锁状态", curr_sts, sts, cenlock_sts_desc)

    def empty_dk_data_queue(self):
        """用于测试的前置条件进行了dk的相关操作, 清除这部分数据避免后面影响校验"""
        while not self.dk_data_queue_internal.empty():
            self.dk_data_queue_internal.get_nowait()
        while not self.dk_data_queue_tsp.empty():
            self.dk_data_queue_tsp.get_nowait()
        while not self.dk_data_queue_key_search.empty():
            self.dk_data_queue_key_search.get_nowait()
        while not self.dk_data_queue_vehicle_control.empty():
            self.dk_data_queue_vehicle_control.get_nowait()

    def ck_vehicle_control_resp(self, status: int, timeout=1, function_id=0xB):
        """
        校验BGM发出的控制结果
        :param status: 0 成功, 6 控制超时, 7 控制失败
        :param timeout: 校验超时时长
        :param function_id: 0xA:HAVP, 0xB: APA
        """
        id_map = {0xA: "AVP", 0xB: "APA"}
        hint = f"校验{id_map[function_id]}控制结果为{status}"
        with allure.step(hint):
            st = time.time()
            while time.time() - st < timeout:
                try:
                    cmd_bytes = self.dk_data_queue_vehicle_control.get_nowait()
                except Exception:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/digital_key/digital_key_class.py")
                    sleep(0.01)
                else:
                    assert cmd_bytes == bytes([function_id, status]), \
                        f"{id_map[function_id]}控制结果异常: {DataTypeHanding.intlist_to_hexstr(cmd_bytes)}"
                    logger.info(f"{hint} -- True")
                    return
            else:
                assert False, f"{timeout}s内未获取到BGM发出{id_map[function_id]}控制结果"

    def ck_search_key_req(self, location: int, trigger: int, timeout=1):
        """校验BGM发出的找钥匙信息"""
        hint = f"校验寻钥匙内容为Location={location} + Trigger={trigger}"
        with allure.step(hint):
            st = time.time()
            while time.time() - st < timeout:
                try:
                    cmd_bytes = self.dk_data_queue_key_search.get_nowait()
                except Exception:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/digital_key/digital_key_class.py")
                    sleep(0.01)
                else:
                    assert cmd_bytes == bytes([0x51, location, trigger]), \
                        f"找钥匙指令异常: {DataTypeHanding.intlist_to_hexstr(cmd_bytes)}"
                    logger.info(f"{hint} -- True")
                    return
            else:
                assert False, f"{timeout}s内未获取到BGM发出寻钥匙报文"

    def ck_rke_resp(self, cmd_code: int, code: int, msg: str, slot_index: int = 1, exec_type: int = None, timeout=3):
        """
        校验BGM发出的蓝牙车控结果
        :param cmd_code: 指令编码, 1: 解闭锁；2: 车窗; 3: 寻车；4: 尾门控制；5: 充电Sco设置；10: 五门全关控制；12: 充电口盖控制；33: 主驾门控制；34: 副驾门控制；35: 左后门控制；36: 右后门控制；37: 四门控制
        :param code: 执行结果, 0 执行成功, 非0失败
        :param msg: 具体原因
        :param slot_index: 手机钥匙对应的序号
        :param exec_type: 执行结果状态, 2:  PreCondictionOK, 3: UsageModeFail, Success, DelayFail, SysBusy,
        :param timeout: 校验超时时间, 当前时间设长是因为可能白名单指令也在下发, 下行数据排队中
        :return:
        """
        cmd_code_map = {1: "解闭锁", 2: "车窗", 3: "寻车", 4: "尾门控制", 5: "充电Soc设置", 10: "五门全关控制", 12: "充电口盖控制", 33: "主驾门控制", 34: "副驾门控制", 35: "左后门控制", 36: "右后门控制", 37: "四门控制"}
        hint = f"校验{cmd_code_map.get(cmd_code, '<输入异常>')}结果为code:{code} + {msg}"
        with allure.step(hint):
            st = time.time()
            while time.time() < st + timeout:
                try:
                    cmd_bytes = self.dk_data_queue_vehicle_control.get(timeout=timeout)
                except Exception:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/digital_key/digital_key_class.py")
                    logger.info(time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time())))
                    assert False, "未获取到BGM发出车控结果报文"
                else:
                    cmd_hexstr: str = DataTypeHanding.intlist_to_hexstr(cmd_bytes)
                    function_id = cmd_bytes[0]
                    if function_id != 0xFF:
                        if function_id == 0x51:
                            logger.info(
                                f"此时获取到非预期的寻钥匙指令{cmd_hexstr}, 某些场景主驾占座会发0601")  # todo: 需要理清楚寻钥匙触发场景
                            continue
                        assert False, f"车控结果报文异常:  {cmd_hexstr}"
                    if cmd_bytes[1] in [0x1, 0x2]:  # todo: 需要解决白名单下发数据处理
                        logger.info(f"获取到白名单相关内容{cmd_hexstr}")
                        continue
                    assert cmd_bytes[1] == 0x22, f"车控结果报文subID异常:  {cmd_hexstr}"
                    len_ble_payload = (cmd_bytes[2] << 8) + cmd_bytes[3] - 1
                    assert cmd_bytes[4] == slot_index, f"车控结果报文slot_index异常:  {cmd_hexstr}"
                    resp_payload = cmd_bytes[5:]
                    assert len_ble_payload == len(resp_payload), f"车控结果报文长度异常:  {cmd_hexstr}"
                    real_resp = RealtimeCmdResp()
                    real_resp.ParseFromString(resp_payload)
                    logger.info(real_resp)
                    assert real_resp.code == code, f"车控执行结果异常:{real_resp.code}"
                    assert real_resp.msg == msg, f"车控具体结果异常: {real_resp.msg}"
                    assert real_resp.execType == exec_type, f"车控具体结果异常: {real_resp.execType}"
                    break
        logger.info(f"{hint} -- True")

    def auto_ack_tsp_update(self):  # todo: 当前白名单上报错误
        """切换usage mode后, 可能触发白名单主动上报, 此时若和云端白名单版本号不一致, 云端会触发白名单更新, 需要自动回复ack"""
        try:
            for i in range(2):
                cmd_bytes = self.dk_data_queue_tsp.get(timeout=1)
                cmd_hexstr: str = DataTypeHanding.intlist_to_hexstr(cmd_bytes)
                last_sync_time_new = DataTypeHanding.intlist_to_int(cmd_bytes[4: 12])
                if cmd_bytes[1] == 0x2:
                    self.send_while_list_update_resp(0x12, 0x00, last_sync_time_new)
                elif cmd_bytes[1] == 0x1:
                    self.send_while_list_update_resp(0x11, 0x00, last_sync_time_new)
                else:
                    logger.info(f"获取到非预期的报文 {cmd_hexstr}")
        except AssertionError as f:
            assert False, f
        except Exception:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/digital_key/digital_key_class.py")
            logger.info("应该有白名单更新请求, 但是没有, 有空就分析下")

    def ck_tsp_cmd_down(self):
        """校验有云端指令下发"""
        with allure.step(f"校验BGM发送的白名单请求"):
            try:
                cmd_bytes = self.dk_data_queue_tsp.get(timeout=2)
            except Exception:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/digital_key/digital_key_class.py")
                assert False, "未获取到BGM发出白名单控制报文"
            else:
                cmd_hexstr: str = DataTypeHanding.intlist_to_hexstr(cmd_bytes)
                function_id = cmd_bytes[0]
                if function_id != 0xFF:
                    assert False, f"云端指令异常:  {cmd_hexstr}"
                assert cmd_bytes[1] in [1, 2, 4], f"白名单控制报文subID异常:  {cmd_hexstr}"

    def ck_white_list_update_req(self, sub_id: int, keyid_list: list = None, last_sync_time: Union[int, None] = None,
                                 timeout=1):
        """
        校验BGM发出的白名单更新请求
        :param sub_id: 0x1: 更新实体卡KeyID白名单（变长)；0x2: 更新蓝牙Slot白名单（定长)；
        :param last_sync_time: 更新的白名单版本号, KeyID和Slot版本号独立
        :param keyid_list:  [inlist, inlist, ...], 当前蓝牙Slot触发后无法预期云端下发的slot_data, 因此只能打印出来手动校验日志
        :param timeout:  校验的超时时间
        :return:
        """
        with allure.step(f"校验BGM发送的白名单请求"):
            try:
                cmd_bytes = self.dk_data_queue_tsp.get(timeout=timeout)
            except Exception:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/digital_key/digital_key_class.py")
                assert False, "未获取到BGM发出白名单控制报文"
            else:
                cmd_hexstr: str = DataTypeHanding.intlist_to_hexstr(cmd_bytes)
                function_id = cmd_bytes[0]
                if function_id != 0xFF:
                    assert False, f"白名单控制报文异常:  {cmd_hexstr}"
                assert cmd_bytes[1] == sub_id, f"白名单控制报文subID异常:  {cmd_hexstr}"
                len_ble_payload = (cmd_bytes[2] << 8) + cmd_bytes[3]
                last_sync_time_new = DataTypeHanding.intlist_to_int(cmd_bytes[4: 12])
                if last_sync_time:
                    assert last_sync_time_new == last_sync_time, f"白名单控制报文last_Sync_time异常:  {cmd_hexstr}"
                logger.info(f"当前指令的last_sync_time为{last_sync_time_new}")
                if sub_id == 1:
                    if keyid_list is None:
                        return
                    if len_ble_payload > 8:
                        for i in range((len_ble_payload - 8) // 16):
                            keyid = DataTypeHanding.hexstr_to_inlist(
                                DataTypeHanding.to_hexstr(cmd_bytes[12 + i * 16: 12 + (i + 1) * 16]))
                            if keyid not in keyid_list:
                                logger.info(keyid)
                                assert False, f"BGM发送的KeyID白名单有异常{DataTypeHanding.intlist_to_hexstr(keyid)}"
                            else:
                                keyid_list.remove(keyid)
                        assert len(
                            keyid_list) == 0, f"BGM未发送预期的KeyID白名单{[DataTypeHanding.intlist_to_hexstr(x) for x in keyid_list]}"
                    else:
                        assert len(keyid_list) == 0, f"BGM发送的白名单控制报文keyID_list异常, {cmd_hexstr}"
                else:
                    logger.info(f"BGM发送的蓝牙钥匙白名单为{DataTypeHanding.intlist_to_hexstr(cmd_bytes[12:])}")
                # assert cmd_bytes[12:] == DataTypeHanding.to_bytes(keyid_list), \
                #     f"白名单控制报文keyid_list异常:  {cmd_hexstr}"

    def ck_nfc_learning_req(self, timeout=1):
        """
        校验BGM发出的NFC学卡请求
        :param timeout: 校验的超时时间
        :return:
        """
        with allure.step(f"校验BGM发出的NFC学卡请求"):
            try:
                cmd_bytes = self.dk_data_queue_tsp.get(timeout=timeout)
            except Exception:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/digital_key/digital_key_class.py")
                assert False, "未获取到BGM发NFC学卡报文"
            else:
                cmd_hexstr: str = DataTypeHanding.intlist_to_hexstr(cmd_bytes)
                function_id = cmd_bytes[0]
                if function_id != 0xFF:
                    assert False, f"白名单控制报文异常:  {cmd_hexstr}"
                assert cmd_bytes[1] == 4, f"NFC学卡报文subID异常:  {cmd_hexstr}"
                assert cmd_bytes[4] == 1, f"NFC学卡报文list_type异常:  {cmd_hexstr}"

    def send_while_list_update_resp(self, sub_id: int, status: int, last_sync_time: int):
        """
        发送数字钥匙白名单更新的结果反馈
        :param sub_id: 0x11: BNCM反馈更新KeyID白名单结果; 0x12:  BNCM反馈更新Slot白名单结果
        :param status: 0x00 Success； 0x01 Fail
        :param last_sync_time: BNCM接受更新后的版本号, 更新不成功则返回之前的版本号
        :return:
        """
        logger.info(f"发送{'蓝牙' if sub_id == 0x12 else '实体卡'}白名单更新结果")
        self.send_bncm_frame(DigKeyBLEReq, self.dk_can_encrypt.white_list_control_resp(sub_id, status, last_sync_time))

    def send_nfc_learning_resp(self, status, card_id=None):
        with allure.step("发送NFC学卡结果"):
            self.send_bncm_frame(DigKeyBLEReq, self.dk_can_encrypt.nfc_learning_resp(status, card_id))

    def ck_cenlock_sts(self, exp_sts: int, exp_trigsrc: Union[None, int] = None, timeout=1):
        """
        校验中控锁状态
        :param exp_sts: 期望的中控锁状态
        :param exp_trigsrc: 期望的中控锁触发源
        :param timeout: 校验超时时间
        """
        hint = f"校验中控锁状态={cenlock_sts_desc.get(exp_sts)} + Trigger={cenlock_sts_trigsrc_desc.get(exp_trigsrc)}"
        with allure.step(hint):
            target_msg = self.ipdu.connectivitycanfd.VgmConnFr12
            if exp_trigsrc is not None:
                self.ipdu.check_multiple_signals([(target_msg, 'LockgCenStsLockSt', exp_sts),
                                                  (
                                                      target_msg, 'LockgCenStsTrigSrc',
                                                      exp_trigsrc)],
                                                 timeout=timeout)
            else:
                self.ipdu.check(target_msg, 'LockgCenStsLockSt', exp_sts, timeout=timeout)
        logger.info(f"{hint} -- True")

    def ck_door_opener_cmd(self, door_index: int, exp_door_cmd: int, exp_trigger_src: Union[None, int] = None,
                           timeout=2):
        """校验BGM发出的门开关指令, 1:open, 2:close
        校验BGM中0xB4和0xB8和0x40发出的五门开门指令的指令
        :param door_index: 门序号, 1左前；2右前；3左后；4右后；5尾门
        :param exp_door_cmd: 门开关指令  0x0 DoorOpenerIdle; 0x1 DoorOpenerOpen; 0x2 DoorOpenerCls; 0x3 DoorOpenerIStop;
        0x4 DoorOpenerIOpenMinang
        :param exp_trigger_src: 门开关指令触发源, 详见ecu_simulator/soa_li/sdk/common/digital_key_const.py
        :param timeout: 检测超时时间
        :return:
        """
        trig_map = door_opener_trigsrc_desc if door_index != 5 else tr_opener_trigsrc_desc
        with allure.step(
                f"校验{door_desc[door_index]}开关指令为{door_opener_cmd_desc[exp_door_cmd]}, 触发源为: {trig_map.get(exp_trigger_src)}"):
            target_msg78 = self.ipdu.bodycan.CemBodyFr78
            target_msg79 = self.ipdu.bodycan.CemBodyFr79
            target_msg02 = self.ipdu.bodycan.CemBodyFr02
            if door_index == 1:
                if exp_trigger_src:
                    self.ipdu.check_multiple_signals([(target_msg78, 'DoorOpenerDrvrReqDoorOpenerReq2', exp_door_cmd),
                                                      (target_msg78, 'DoorOpenerDrvrReqTrigSrc', exp_trigger_src)],
                                                     timeout)
                else:
                    self.ipdu.check(target_msg78, 'DoorOpenerDrvrReqDoorOpenerReq2', exp_door_cmd, timeout)
            elif door_index == 2:
                if exp_trigger_src:
                    self.ipdu.check_multiple_signals([(target_msg79, 'DoorOpenerPassReqDoorOpenerReq2', exp_door_cmd),
                                                      (target_msg79, 'DoorOpenerPassReqTrigSrc', exp_trigger_src)],
                                                     timeout)
                else:
                    self.ipdu.check(target_msg79, 'DoorOpenerPassReqDoorOpenerReq2', exp_door_cmd, timeout)
            elif door_index == 3:
                if exp_trigger_src:
                    self.ipdu.check_multiple_signals([(target_msg78, 'DoorOpenerLeReReqDoorOpenerReq2', exp_door_cmd),
                                                      (target_msg78, 'DoorOpenerLeReReqTrigSrc', exp_trigger_src)],
                                                     timeout)
                else:
                    self.ipdu.check(target_msg78, 'DoorOpenerLeReReqDoorOpenerReq2', exp_door_cmd, timeout)
            elif door_index == 4:
                if exp_trigger_src:
                    self.ipdu.check_multiple_signals([(target_msg79, 'DoorOpenerRiReReqDoorOpenerReq2', exp_door_cmd),
                                                      (target_msg79, 'DoorOpenerRiReReqTrigSrc', exp_trigger_src)],
                                                     timeout)
                else:
                    self.ipdu.check(target_msg79, 'DoorOpenerRiReReqDoorOpenerReq2', exp_door_cmd, timeout)
            elif door_index == 5:
                if exp_trigger_src:
                    self.ipdu.check_multiple_signals([(target_msg02, 'TrOpenerReqTrOpenerReq', exp_door_cmd),
                                                      (target_msg02, 'TrOpenerReqTrigSrc', exp_trigger_src)],
                                                     timeout)
                else:
                    self.ipdu.check(target_msg02, 'TrOpenerReqTrOpenerReq', exp_door_cmd, timeout)
            else:
                assert False, "门序号只能是1-5"

    def ck_four_door_lock_cmd(self, sts: int, timeout=2):
        """
        校验BGM中0x20发出的四门锁的指令
        :param sts: 0x0 LockActvnOff - Idle Command
                    0x1 LockActvnUnlck - Unlock door
                    0x2 LockActvnLock - Lock door
                    0x3 LockActvnSafe - Double lock door
                    0x4, 0x8, 0xC, 0xD, 0xE LockActvnUnlckByCrash - Crash Unlock door
        :param timeout: 校验超时时间
        :return:
        """
        with allure.step(f"校验BGM发出的四门门锁开关指令: {door_lock_cmd_desc[sts]}"):
            target_msg = self.ipdu.bodycan.CemBodyFr01
            ck_func = self.ipdu.check
            self.ipdu.check_multiple_signals([(target_msg, 'DoorDrvrLockCmd', sts),
                                              (target_msg, 'DoorPassLockCmd', sts),
                                              (target_msg, 'DoorLeReLockCmd', sts),
                                              (target_msg, 'DoorRiReLockCmd', sts)], timeout)

    def set_four_door_unlock(self):
        """设置四门锁状态为开"""
        with allure.step(f"设置四门锁状态为开"):
            self.set_door_lock_sts(1, 1, 1, 1)

    def set_four_door_lock(self):
        """设置四门锁状态为关"""
        with allure.step(f"设置四门锁状态为关"):
            self.set_door_lock_sts(2, 2, 2, 2)

    def set_door_lock_sts(self, driver=0, passive=0, lere=0, rire=0):
        """
        输入四个门的锁状态
        0x0 LockStsUkwn - Lock Status Unknown
        0x1 Unlckd - Unlocked
        0x2 Lockd - Locked
        0x3 SafeLockd - Safe Locked (Double Locked)
        :param driver: 主驾门锁状态设定值
        :param passive: 副驾门锁状态设定值
        :param lere: 左后门锁状态设定值
        :param rire: 右后门锁状态设定值
        :return:
        """
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'DoorDrvrLockSts_0_DdmBodySignalIPdu04', driver)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'DoorPassLockSts_0_PdmBodySignalIPdu01', passive)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'DoorLeReLockSts_0_RldmBodySignalIPdu01', lere)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'DoorRiReLockSts_0_RrdmBodySignalIPdu01', rire)

    def set_door_opener_sts(self, lefr=1, rifr=1, lere=1, rire=1, tr=1):
        """
        设置五个门的开关状态, 默认全关
        0x0 DoorOpenerSts_Ukwn
        0x1 DoorOpenerSts_FullClsd
        0x2 DoorOpenerSts_MovgOut
        0x3 DoorOpenerSts_MovgOutBrkg
        0x4 DoorOpenerSts_StopDurgOpen
        0x5 DoorOpenerSts_FullOpend
        0x6 DoorOpenerSts_MovgIn
        0x7 DoorOpenerSts_MovgInBrkg
        0x8 DoorOpenerSts_StopDurgCls
        0x9 DoorOpenerSts_HalfClsd
        0xA DoorOpenerSts_StopMinPntForCls
        :param lefr:主驾门开关状态
        :param rifr: 副驾门开关状态
        :param lere: 左后门开关状态
        :param rire: 右后门开关状态
        :param tr: 尾门开关状态
        :return:
        """
        with allure.step(f"设置五门的开关状态"):
            self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorOpenerDrvrSts_0_DpodBodySignalIPdu01', lefr)
            self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorOpenerPassSts_0_PpodBodySignalIPdu01', rifr)
            self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DoorOpenerLeReSts_0_LpodBodySignalIPdu01', lere)
            self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorOpenerRiReSts_0_RpodBodySignalIPdu01', rire)
            self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts_0_PotBodySignalIPdu02', tr)

    def set_drvr_seat_present(self):
        with allure.step("设置主驾占位"):
            self.nucapp.driver_seat_present()

    def set_drvr_seat_notpresent(self):
        with allure.step("设置主驾未占位"):
            self.nucapp.driver_seat_notpresent()

    def set_pass_seat_present(self):
        with allure.step("设置副驾占位"):
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'PassSeatSts', 'PassSeatSts1_OccptLrg')

    def set_pass_seat_notpresent(self):
        with allure.step("设置副驾未占位"):
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'PassSeatSts', 'PassSeatSts1_Empty')

    def set_secle_seat_present(self):
        with allure.step("设置后左占位"):
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecLe', 'PassSeatSts1_OccptLrg')

    def set_secle_seat_notpresent(self):
        with allure.step("设置后左未占位"):
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecLe', 'PassSeatSts1_Empty')

    def set_secmid_seat_present(self):
        with allure.step("设置后中占位"):
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecMid', 'PassSeatSts1_OccptLrg')

    def set_secmid_seat_notpresent(self):
        with allure.step("设置后中未占位"):
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecMid', 'PassSeatSts1_Empty')

    def set_secri_seat_present(self):
        with allure.step("设置后右占位"):
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecRi', 'PassSeatSts1_OccptLrg')

    def set_secri_seat_notpresent(self):
        with allure.step("设置后右未占位"):
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecRi', 'PassSeatSts1_Empty')

    def set_window_position(self, pos_drvr: int, pos_pass: int, pos_lere: int, pos_rire: int):
        """
        模拟反馈四个车窗当前的开度, 由DM BodyCan输入
        :param pos_drvr: 左前车窗开度, can信号值, 实际开度 4 * pos - 4
        :param pos_pass: 右前车窗开度,
        :param pos_lere: 左后车窗开度
        :param pos_rire: 右后车窗开度
        :return:
        """
        with allure.step(
                f"模拟门窗开度, 左前{4 * pos_drvr - 4}%, 右前{4 * pos_pass - 4}%, 左后{4 * pos_lere - 4}%, 右后{4 * pos_rire - 4}%"):
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'WinPosnStsAtDrvr_0_DdmBodySignalIPdu04', pos_drvr)
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'WinPosnStsAtPass_0_PdmBodySignalIPdu01', pos_pass)
            self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinPosnStsAtReLe_0_RldmBodySignalIPdu01', pos_lere)
            self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinPosnStsAtReRi_0_RrdmBodySignalIPdu01', pos_rire)

    def send_rke_window_control(self, p1, p2, p3, p4, slot_index=1, exec_id=f'{1:032}', vid=f'{1:032}',
                                vehicle_model=61):
        """
        发送RKE车窗控制指令
        :param p1: 左前开度, 0-100
        :param p2: 右前开度, 0-100
        :param p3: 左后开度, 0-100
        :param p4: 右后开度, 0-100
        :param slot_index:
        :param exec_id:
        :param vid:
        :param vehicle_model:
        :return:
        """
        with allure.step(f"发送RKE车控控制指令, 开度分别为{p1}%, {p2}%, {p3}%, {p4}%"):
            self.send_bncm_frame(DigKeyBLEReq,
                                 self.dk_can_encrypt.rke_window_control_cmd(p1, p2, p3, p4, slot_index, exec_id, vid,
                                                                            vehicle_model))

    def send_rke_chargelidgate(self, op, slot_index: int = 1, exec_id: str = '', vid='', vehicle_model=61):
        """
        发送RKE充电口盖控制
        :param op: 动作, -1: 关；1: 开
        :param slot_index:
        :param exec_id:
        :param vid:
        :param vehicle_model:
        :return:
        """
        op_map = {-1: "关充电口盖", 1: "开充电口盖"}
        with allure.step(f"执行{op_map.get(op)}控制"):
            self.send_bncm_frame(DigKeyBLEReq, self.dk_can_encrypt.rke_chargelidgate(op, slot_index,
                                                                                        exec_id, vid, vehicle_model))

    def send_rke_maxsoc(self, soc, slot_index: int = 1, exec_id: str = '', vid='', vehicle_model=61):
        """
        发送RKE充电电量MaxSoc值
        :param soc: 最大值, 870代表87%
        :param slot_index:
        :param exec_id:
        :param vid:
        :param vehicle_model:
        :return:
        """
        with allure.step(f"发送充电最大电量{soc / 10}"):
            self.send_bncm_frame(DigKeyBLEReq, self.dk_can_encrypt.rke_maxsoc(soc, slot_index, exec_id, vid,
                                                                              vehicle_model))

    def send_rke_tailgate_control(self, op, position=100, slot_index: int = 1, exec_id: str = '', vid='',
                                  vehicle_model=61):
        """
        发送RKE尾门控制
        :param op: 动作, -1: 关；1: 开；2: 翘起
        :param position: 开度, 10即 10%
        :param slot_index:
        :param exec_id:
        :param vid:
        :param vehicle_model:
        :return:
        """
        op_map = {-1: "关尾门", 1: "开尾门", 2: "翘起"}
        with allure.step(f"执行{op_map.get(op)}控制, 开度{position}"):
            self.send_bncm_frame(DigKeyBLEReq, self.dk_can_encrypt.rke_tailgate_control(op, position, slot_index,
                                                                                        exec_id, vid, vehicle_model))

    def send_rke_car_locator(self, op, slot_index: int = 1, exec_id: str = '', vid='', vehicle_model=61):
        """
        发送RKE寻车控制指令
        :param op: 动作, -1, 关闭, 1, 鸣笛闪灯, 2, 仅闪灯
        :param slot_index:
        :param exec_id:
        :param vid:
        :param vehicle_model:
        :return:
        """
        op_map = {-1: "关闭", 1: "鸣笛闪灯", 2: "仅闪灯"}
        with allure.step(f"执行寻车控制: {op_map.get(op)}"):
            self.send_bncm_frame(DigKeyBLEReq, self.dk_can_encrypt.rke_panic_vehicle(op, slot_index,
                                                                                     exec_id, vid, vehicle_model))

    def send_rke_apa_close_door(self, op=1, slot_index: int = 1, exec_id: str = '', vid='', vehicle_model=61):
        """
        发送RKE APA五门全关控制
        :param op: 动作, 1全关
        :param slot_index:
        :param exec_id:
        :param vid:
        :param vehicle_model:
        :return:
        """
        with allure.step(f"执行APA五门全关控制"):
            self.send_bncm_frame(DigKeyBLEReq,
                                 self.dk_can_encrypt.rke_door_full_closing_control(op, slot_index, exec_id, vid,
                                                                                   vehicle_model))

    def ck_window_opener_req(self, p1, p2, p3, p4, timeout=1):
        """
        校验BGM发出的0xB2中车窗开度指令
        :param p1: 左前门窗开度, 十进制开度 / 4 + 1
        :param p2: 右前门窗开度, 十进制开度 / 4 + 1
        :param p3: 左后门窗开度, 十进制开度 / 4 + 1
        :param p4: 右后门窗开度, 十进制开度 / 4 + 1
        :param timeout: 检测信号超时时间
        :return:
        """
        with allure.step(f"校验BGM发出的车控控制指令, 开度分别为{hex(p1)}, {hex(p2)}, {hex(p3)}, {hex(p4)}"):
            target_msg = self.ipdu.bodycan.CemBodyFr68
            self.ipdu.check_multiple_signals([(target_msg, 'WinOpenDrvrReq', p1),
                                              (target_msg, 'WinOpenPassReq', p2),
                                              (target_msg, 'WinOpenReLeReq', p3),
                                              (target_msg, 'WinOpenReRiReq', p4)], timeout)
            
    def send_rke_driver_door(self, op, position, key_id: Union[str, list] = f'{1:032}', slot_index: int = 1, user_id: str = '',
                      exec_id: str = '', vid: str = f'{1:032}', vehicle_model: int = 61):
        """
        发送RKE主驾门控制
        :param op: 动作, 1: 设置开度; 2: 关; 3:全开（预留）
        :param position: 可动态配置0~100
        :return:
        """
        op_map = {1: "设置开度", 2: "关", 3: "全开（预留）"}
        with allure.step(f"发送RKE主驾门控制,{op_map.get(op)}"):
            self.send_bncm_frame(DigKeyBLEReq,
                                 self.dk_can_encrypt.rke_driver_door_control_cmd(op, position, DataTypeHanding.to_hexstr(key_id),
                                                                                 user_id ,slot_index, exec_id, vid, vehicle_model))
            
    def send_rke_pass_door(self, op, position, key_id: Union[str, list] = f'{1:032}', slot_index: int = 1, user_id: str = '',
                      exec_id: str = '', vid: str = f'{1:032}', vehicle_model: int = 61):
        """
        发送RKE副驾门控制
        :param op: 动作, 1: 设置开度; 2: 关; 3:全开（预留）
        :param position: 可动态配置0~100
        :return:
        """
        op_map = {1: "设置开度", 2: "关", 3: "全开（预留）"}
        with allure.step(f"发送RKE主驾门控制,{op_map.get(op)}"):
            self.send_bncm_frame(DigKeyBLEReq,
                                 self.dk_can_encrypt.rke_passenger_door_control_cmd(op, position, DataTypeHanding.to_hexstr(key_id),
                                                                                 user_id ,slot_index, exec_id, vid, vehicle_model))
            
    def send_rke_rear_left_door(self, op, position, key_id: Union[str, list] = f'{1:032}', slot_index: int = 1, user_id: str = '',
                      exec_id: str = '', vid: str = f'{1:032}', vehicle_model: int = 61):
        """
        发送RKE左后门控制
        :param op: 动作, 1: 设置开度; 2: 关; 3:全开（预留）
        :param position: 可动态配置0~100
        :return:
        """
        op_map = {1: "设置开度", 2: "关", 3: "全开（预留）"}
        with allure.step(f"发送RKE主驾门控制,{op_map.get(op)}"):
            self.send_bncm_frame(DigKeyBLEReq,
                                 self.dk_can_encrypt.rke_rear_left_door_control_cmd(op, position, DataTypeHanding.to_hexstr(key_id),
                                                                                 user_id ,slot_index, exec_id, vid, vehicle_model))
            
    def send_rke_rear_right_door(self, op, position, key_id: Union[str, list] = f'{1:032}', slot_index: int = 1, user_id: str = '',
                      exec_id: str = '', vid: str = f'{1:032}', vehicle_model: int = 61):
        """
        发送RKE右后门控制
        :param op: 动作, 1: 设置开度; 2: 关; 3:全开（预留）
        :param position: 可动态配置0~100
        :return:
        """
        op_map = {1: "设置开度", 2: "关", 3: "全开（预留）"}
        with allure.step(f"发送RKE主驾门控制,{op_map.get(op)}"):
            self.send_bncm_frame(DigKeyBLEReq,
                                 self.dk_can_encrypt.rke_rear_right_door_control_cmd(op, position, DataTypeHanding.to_hexstr(key_id),
                                                                                 user_id ,slot_index, exec_id, vid, vehicle_model))
            
    def send_rke_four_door(self, op, driverPosition, passengerPosition,  rearLeftPosition, rearRightPosition, 
                             key_id: Union[str, list] = f'{1:032}', slot_index: int = 1, user_id: str = '',
                             exec_id: str = '', vid: str = f'{1:032}', vehicle_model: int = 61):
        """
        发送RKE右后门控制
        :param op: 动作, 1: 设置开度; 2: 关; 3:全开（预留）
        :param driverPosition:      可动态配置0~100;
        :param passengerPosition:   可动态配置0~100;
        :param rearLeftPosition:    可动态配置0~100;
        :param rearRightPosition:   可动态配置0~100;
        :return:
        """
        op_map = {1: "设置开度", 2: "关", 3: "全开（预留）"}
        with allure.step(f"发送RKE主驾门控制,{op_map.get(op)}"):
            self.send_bncm_frame(DigKeyBLEReq,
                                 self.dk_can_encrypt.rke_four_door_control_cmd(op, driverPosition, passengerPosition, 
                                 rearLeftPosition, rearRightPosition, DataTypeHanding.to_hexstr(key_id),
                                 user_id ,slot_index, exec_id, vid, vehicle_model))

    def send_rke_lock(self, key_id: Union[str, list] = f'{1:032}', slot_index: int = 1, user_id: str = '',
                      exec_id: str = '', vid: str = f'{1:032}', vehicle_model: int = 61):
        """发送RKE闭锁指令"""
        with allure.step(f"发送RKE闭锁指令"):
            self.send_bncm_frame(DigKeyBLEReq,
                                 self.dk_can_encrypt.rke_lock_cmd(2, DataTypeHanding.to_hexstr(key_id), slot_index,
                                                                  user_id, exec_id, vid, vehicle_model))

    def send_rke_unlock(self, key_id: Union[str, list] = f'{1:032}', slot_index: int = 1, user_id: str = '',
                        exec_id: str = '', vid: str = f'{1:032}', vehicle_model: int = 61):
        """发送RKE闭锁指令"""
        with allure.step(f"发送RKE解锁指令"):
            self.send_bncm_frame(DigKeyBLEReq,
                                 self.dk_can_encrypt.rke_unlock_cmd(DataTypeHanding.to_hexstr(key_id), slot_index,
                                                                    user_id, exec_id, vid, vehicle_model))

    def send_rke_close_door_and_lock(self, key_id: Union[str, list] = f'{1:032}', slot_index: int = 1,
                                     user_id: str = '', exec_id: str = '', vid: str = f'{1:032}',
                                     vehicle_model: int = 61):
        """发送RKE关门+闭锁指令"""
        with allure.step(f"发送RKE关门+闭锁指令"):
            self.send_bncm_frame(DigKeyBLEReq,
                                 self.dk_can_encrypt.rke_close_door_and_lock_cmd(key_id, slot_index, user_id, exec_id,
                                                                                 vid, vehicle_model))

    def set_digital_key_connect_info(self, connect_sts1=0, keyid1=bytes([0x0] * 16), zone1=0, type1=0, battwarn1=0,
                                     connect_sts2=0, keyid2=bytes([0x0] * 16), zone2=0, type2=0, battwarn2=0,
                                     connect_sts3=0, keyid3=bytes([0x0] * 16), zone3=0, type3=0, battwarn3=0,
                                     connect_sts4=0, keyid4=bytes([0x0] * 16), zone4=0, type4=0, battwarn4=0):
        logger.info(f"{time.time()}---设置BNCM发送的0x244/0x245报文中数字钥匙连接状态")
        with allure.step("设置BNCM发送的0x244/0x245报文中数字钥匙连接状态"):
            msg_map = {1: self.ipdu.connectivitycanfd.BncmConnectivityFr18,
                       2: self.ipdu.connectivitycanfd.BncmConnectivityFr18,
                       3: self.ipdu.connectivitycanfd.BncmConnectivityFr19,
                       4: self.ipdu.connectivitycanfd.BncmConnectivityFr19}
            connect_sts_list = [connect_sts1, connect_sts2, connect_sts3, connect_sts4]
            zone_list = [zone1, zone2, zone3, zone4]
            key_type_list = [type1, type2, type3, type4]
            keyid_list = [keyid1, keyid2, keyid3, keyid4]
            battwarn_list = [battwarn1, battwarn2, battwarn3, battwarn4]
            for i in range(1, 5):
                self.ipdu.set(msg_map[i], f'DigKeyConnectInfo{i}KeyConnectSts', connect_sts_list[i - 1])
                self.ipdu.set(msg_map[i], f'DigKeyConnectInfo{i}KeyPrsntZone', zone_list[i - 1])
                self.ipdu.set(msg_map[i], f'DigKeyConnectInfo{i}KeyTyp', key_type_list[i - 1])
                self.ipdu.set(msg_map[i], f'DigKeyConnectInfo{i}_UB', 1)
                self.ipdu.set(msg_map[i], f'DigKeyConnectInfo{i}BattWarn', battwarn_list[i - 1])
                for j in range(16):
                    self.ipdu.set(msg_map[i], f'DigKeyConnectInfo{i}KeyIdByte{j}', keyid_list[i - 1][j])

    def set_single_digital_key_connect_info(self, slot, connect_sts=0, keyid=bytes([0x0] * 16),
                                            zone=0, key_type=0, battwarn=0):
        """slot仅支持1,2,3,4"""
        logger.info(f"{time.time()}---设置BNCM发送的0x244/0x245报文中单个数字钥匙{slot}连接状态")
        with allure.step("设置BNCM发送的0x244/0x245报文中数字钥匙连接状态"):
            msg_map = {1: self.ipdu.connectivitycanfd.BncmConnectivityFr18,
                       2: self.ipdu.connectivitycanfd.BncmConnectivityFr18,
                       3: self.ipdu.connectivitycanfd.BncmConnectivityFr19,
                       4: self.ipdu.connectivitycanfd.BncmConnectivityFr19}
            self.ipdu.set(msg_map[slot], f'DigKeyConnectInfo{slot}KeyConnectSts', connect_sts)
            self.ipdu.set(msg_map[slot], f'DigKeyConnectInfo{slot}KeyPrsntZone', zone)
            self.ipdu.set(msg_map[slot], f'DigKeyConnectInfo{slot}KeyTyp', key_type)
            self.ipdu.set(msg_map[slot], f'DigKeyConnectInfo{slot}_UB', 1)
            self.ipdu.set(msg_map[slot], f'DigKeyConnectInfo{slot}BattWarn', battwarn)
            for j in range(16):
                self.ipdu.set(msg_map[slot], f'DigKeyConnectInfo{slot}KeyIdByte{j}', keyid[j])

    def set_chassis_service_gear(self, gear: Union[int, str]):
        """
        测试输入ChassisService:Gear.Gear状态  todo: 1.0需求变更, GearR和GearD要求Active或Driving mode
        :param gear: //P挡 0 GearP, //R挡 1 GearR, //N挡 2 GearN, //D挡 3 GearD,M挡 4 GearM, //挡位未知 5 GearNA
        :return:
        """
        gear_map = {0: "GearP", 1: "GearR", 2: "GearN", 3: "GearD", 5: "GearNA"}
        if isinstance(gear, int):
            gear = gear_map.get(gear)
        with allure.step(f"设置ChassisService:Gear.Gear = {gear}"):
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkNotEngd')
            gearlvrindcn = gear.replace("Gear", "")
            if gearlvrindcn == 'P':
                self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
            elif gearlvrindcn == 'R':
                self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 'GearLvrIndcn2_RvsIndcn')
            elif gearlvrindcn == 'N':
                self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 'GearLvrIndcn2_NeutIndcn')
            elif gearlvrindcn == 'D':
                self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 'GearLvrIndcn2_DrvIndcn')
            elif gearlvrindcn == "NA":
                self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 'GearLvrIndcn2_ManModeIndcn')
            else:
                assert False, f"入参错误{gearlvrindcn}"

    def set_gearlvrindcn2(self, gearlvrindcn: Union[int, str]):
        """
        给BGM输入档位信号, 供mcu使用
        :param gearlvrindcn: 0: "P", 1: "R", 2: "N", 3: "D"
        :return:
        """
        gearlvrindcn_map = {0: "P", 1: "R", 2: "N", 3: "D"}
        if isinstance(gearlvrindcn, int):
            gearlvrindcn = gearlvrindcn_map.get(gearlvrindcn)
        with allure.step(f"设置ChassisService:Gear.Gear = {gearlvrindcn}"):
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
            if gearlvrindcn == 'P':
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
            elif gearlvrindcn == 'R':
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_RvsIndcn')
            elif gearlvrindcn == 'N':
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_NeutIndcn')
            elif gearlvrindcn == 'D':
                self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_DrvIndcn')
            else:
                assert False, f"入参错误{gearlvrindcn}"

    def ck_bgm_not_send_cmd(self, error_msg, queue, timeout=0.5, excluded_data='510601'):
        """
        校验BGM未发送指令给BNCM
        :param error_msg: 错误时打印的信息
        :param queue: 要查找的队列
        :param timeout: 校验时间
        :param excluded_data: 排除在外的报文, 因主驾占位会自行寻钥匙, 所以510601不在校验报文内
        :return:
        """
        with allure.step(error_msg):
            st = time.time()
            while time.time() < st + timeout:
                try:
                    cmd_bytes = queue.get(timeout=timeout)
                except Exception:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/digital_key/digital_key_class.py")
                    pass
                else:
                    data_str = DataTypeHanding.intlist_to_hexstr(cmd_bytes).upper()
                    if data_str == excluded_data.upper():
                        continue
                    assert False, error_msg + f", 指令异常: {DataTypeHanding.intlist_to_hexstr(cmd_bytes)}"

    def ck_tropen_pos_req_from_hmi(self, exp_value, timeout=1):
        with allure.step(f"校验{timeout}时间内bodycan::0x118::CemBodyFr131::TrOpenPosnReqFromHmi为{exp_value}"):
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr131, 'TrOpenPosnReqFromHmi', exp_value, timeout)

    def ck_charge_lid_open_req2(self, exp_value, timeout=0.5):
        """校验充电口盖控制信号"""
        with allure.step(f"校验{timeout}时间内CEM_LIN2::0x28::CemCem_Lin2Fr06::ChrgLidManvgDCorAcDcReq2为{exp_value}"):
            self.ipdu.check(self.ipdu.cem_lin2.CemCem_Lin2Fr06, 'ChrgLidManvgDCorAcDcReq2', exp_value, timeout)

    def ck_maxsoc(self, exp_value, timeout=1):
        """校验maxsoc信号"""
        with allure.step(f"校验{timeout}时间内BackboneFR::27-2-8::LocalBookChrgnTarVal为{exp_value}"):
            self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr12, 'LocalBookChrgnTarVal', exp_value, timeout)

    def set_external_has_key(self):
        """设置车外有钥匙"""
        self.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 6)])
        self.update_keyinfos(3, [KeyInfo(KeyType.BLE_Key, key_id2, 6)])
        self.update_keyinfos(4, [KeyInfo(KeyType.BLE_Key, key_id3, 6)])

    def set_external_no_key(self):
        """设置车外无钥匙"""
        self.update_keyinfos(2, [])
        self.update_keyinfos(3, [])
        self.update_keyinfos(4, [])

    def set_internal_has_key(self):
        """设置车内有钥匙"""
        self.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 8)])
        self.update_keyinfos(7, [KeyInfo(KeyType.BLE_Key, key_id2, 8)])
        self.update_keyinfos(8, [KeyInfo(KeyType.BLE_Key, key_id3, 8)])

    def set_internal_no_key(self):
        """设置车内无钥匙"""
        self.update_keyinfos(6, [])
        self.update_keyinfos(7, [])
        self.update_keyinfos(8, [])
