# -*- coding: utf-8 -*-
"""
@File        : bus_can.py
@Author      : jiabin.zhu@jiduatuo.com
@Time        : 2022/10/23 18:00 PMW
@Description : description about this file
@Examples    : example of how to use it
"""
import os
import sys
from xat_ecu import reporting as allure
current_path = os.path.dirname(os.path.realpath(__file__))
from xat_ecu.legacy.sdk.digital_key.digital_key_can_protocol import BncmBgmPduEncrypt
from xat_ecu.legacy.sdk.digital_key.digital_key_const import *
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding
from xat_ecu.legacy.common.logger import logger
import time
import can
import inspect
import ctypes
from typing import List, Union, Optional
from time import sleep
from queue import Queue
from threading import Thread
import cantools
from cantools.database import Message
from can.typechecking import CanFilters

DigKeyBLEReq = 0x166  # BNCM send
DigKeyBLEResp = 0x157
DigkeyBLEReq2 = 0x30  # BGM send
DigKeyBLEResp2 = 0x149
DigKeyBLEReq3 = 0x176  # BNCM send
DigKeyBLEResp3 = 0x175

dbc_dir = os.path.join(os.path.dirname(__file__), 'data/dbc/V1.0.0')
BodyCAN_dbc = os.path.join(dbc_dir, 'SDB22R05_BGM_BodyCAN_221125_Release.dbc')
ConnectivityCANFD_dbc = os.path.join(dbc_dir, 'SDB22R05_BGM_ConnectivityCANFD_221205_Release.dbc')
BodyExposedCanFd_dbc = os.path.join(dbc_dir, 'SDB22R05_BGM_BodyExposedCANFD_221125_Release.dbc')
ChassisCAN1_dbc = os.path.join(dbc_dir, 'SDB22R05_BGM_ChassisCAN1_221125_Release.dbc')
ChassisCAN2_dbc = os.path.join(dbc_dir, 'SDB22R05_BGM_ChassisCAN2_221125_Release.dbc')
InfoCANFD_dbc = os.path.join(dbc_dir, 'SDB22R05_BGM_InfoCANFD_221125_Release.dbc')
PassiveSafetyCAN_dbc = os.path.join(dbc_dir, 'SDB22R05_BGM_PassiveSafetyCAN_221125_Release.dbc')
PropulsionCAN_dbc = os.path.join(dbc_dir, 'SDB22R05_BGM_PropulsionCAN_221125_Release.dbc')
ADCANFD_dbc = os.path.join(dbc_dir, 'SDB22R05_BGM_ADCANFD_221205_Release.dbc')


def format_assert_log(sts_name, current_key, expect_key, mapping={}):
    """格式化assert的打印信息"""
    return f"{time.time()}--当前{sts_name}为{current_key}: {mapping.get(current_key, '')}, 不满足预期{expect_key}: {mapping.get(expect_key, '')}"


def _async_raise(tid, exctype):
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(tid), ctypes.py_object(exctype))
    if res == 0:
        pass
        # raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


class Temp(object):
    def __int__(self):
        pass


class CanBus:
    """通用的canbus报文收发，各通路的特殊函数继承后自行定义"""

    def __init__(self, interface='socketcan', channel='can1', bitrate=500000, fd=True, dbc=BodyCAN_dbc,
                 can_filters: Optional[CanFilters] = None):
        if channel is None:
            return
        self.channel = channel
        self.interface = interface
        self.fd = fd
        can.rc['interface'] = 'socketcan'
        can.rc['channel'] = channel
        can.rc['bitrate'] = bitrate
        if can_filters:
            can.rc['can_filters'] = can_filters
        if fd:
            can.rc['fd'] = True
        self.bus = can.interface.Bus()
        self.last_rx_msg_time = time.time()  # 当前bus上最后一帧报文的世界时间戳
        self.tmp = Temp()
        self.db = cantools.db.load_file(filename=dbc, database_format=None, encoding="UTF-8", frame_id_mask=None,
                                        strict=False, cache_dir=None)
        self.listen_signals = []
        self.listen_msg_ids = []
        self.notifier = can.Notifier(self.bus, [])

    def get_single_value(self, msg, value_type_is_num: bool = False) -> [dict, None]:   # 整个函数耗时15 - 30ms左右
        """
        根据包含有message_id的字典，查询当前报文的信号表示的含义
        :param msg: can.Notifier回调函数入参的msg
        :param value_type_is_num: 查询结果为数字还是值
        :return: 报文详情
        """
        select_message = self.db.get_message_by_frame_id(msg.arbitration_id)
        if value_type_is_num:
            result = select_message.decode(msg.data,
                                           decode_choices=False,  # 值为数字为 False 值为 True
                                           scaling=True,
                                           decode_containers=False)
        else:
            result = select_message.decode(msg.data,
                                           decode_choices=True,  # 值为数字为 False 值为 True
                                           scaling=True,
                                           decode_containers=False)
        logger.info(f"{msg.timestamp}--报文{hex(msg.arbitration_id)}值为：{result}")
        return result

    def get_message_by_name(self, message_name: str) -> Message:
        """
        根据报文名称获取当前dbc的报文frame_id
        :param message_name: 报文名称
        :return: 报文
        """
        message = self.db.get_message_by_name(message_name)
        return message

    def get_signal(self, msg_name, signal_name, timeout=2):
        """
        获取某个信号量，获取到第一个即退出
        """
        if not isinstance(msg_name, str):
            msg_name = msg_name.msg_name
        message: Message = self.get_message_by_name(msg_name)
        res = [None]

        def listener(msg, res1=res):
            if msg.arbitration_id != message.frame_id:
                return
            signal_dict = self.get_single_value(msg, True)
            res1[0] = signal_dict.get(signal_name)

        self.add_listener(listener)
        st = time.time()
        while time.time() - st < timeout:
            if res[0]:
                break
            time.sleep(0.01)
        self.remove_listener(listener)

        if res[0] is None:
            assert False, f"{timeout}s超时未获取到有效信号"
        else:
            return res[0]

    def ck_signal(self, msg_name, signal_name, exp_value, timeout=0.5, assert_flag=True):
        """
        校验信号量
        :param msg_name: can_msg名称, 可能为ipdu的报文
        :param signal_name: 信号名
        :param exp_value: 期望值
        :param timeout: 校验时长， 需确保超时时长内至少有一次可以获取到报文，否则会返回None
        :param assert_flag: 是否进行assert校验
        :return:
        """
        if not isinstance(msg_name, str):
            msg_name = msg_name.msg_name
        message: Message = self.get_message_by_name(msg_name)
        res1 = [False, None]  # find_tag, curr_value

        def listener(msg, res=res1):
            if msg.arbitration_id != message.frame_id:
                return
            signal_dict = self.get_single_value(msg, True)
            signal_value = signal_dict.get(signal_name)
            if signal_value is None:
                res[0] = None
            elif signal_value == exp_value:
                res[0] = True
                res[1] = signal_value
            else:
                res[1] = signal_value

        self.add_listener(listener)
        st = time.time()
        while time.time() - st < timeout:
            if res1[0]:
                break
            time.sleep(0.01)
        self.remove_listener(listener)
        find_tag, curr_value = res1[0], res1[1]
        if find_tag is None:
            assert False, f"{signal_name} not in {self.channel}::{msg_name}"
        elif find_tag:
            print(f"{msg_name}::{signal_name}为{curr_value}, 满足预期{exp_value}")
            return curr_value
        else:
            if assert_flag:
                assert False, f"{msg_name}::{signal_name}为{curr_value}, 不满足预期{exp_value}"
            return curr_value

    def bus_close(self):
        """关闭socketcan"""
        self.notifier.stop()
        self.bus.shutdown()

    def bus_send(self, can_id: int, data: Union[str, list], is_fd=None, bitrate_switch=None, print_msg=True):
        """报文发送"""
        if can_id > 0x7FF:
            is_extended_id = True
        else:
            is_extended_id = False
        if isinstance(data, str):
            data = DataTypeHanding.hexstr_to_inlist(data)
        if is_fd is None:
            is_fd = True if self.fd else False
        if bitrate_switch is None:
            bitrate_switch = True if self.fd else False
        msg = can.Message(arbitration_id=can_id, data=data, is_extended_id=is_extended_id, channel=self.channel,
                          is_fd=is_fd, bitrate_switch=bitrate_switch, is_rx=False, timestamp=time.time())
        self.bus.send(msg)
        if print_msg:
            logger.info(msg)

    # def bus_recv(self, timeout=0):
    #     """Block waiting for a message from the Bus.
    #     :param timeout:
    #         seconds to wait for a message or None to wait indefinitely
    #     :return: ``None`` on timeout or a :class:`Message` object."""
    #     return self.bus.recv(timeout)

    def listen_and_update_signal(self, func):
        """在当前bus上监测各pdu并更新常用信号量"""
        self.add_listener(func)

    def add_listener(self, func):
        """新增监视器"""
        self.notifier.add_listener(func)

    def remove_listener(self, func):
        """去除监视器"""
        self.notifier.remove_listener(func)

    def update_last_msg_time(self, msg):
        """收到任一报文(非错误帧)，更新时间戳"""
        if msg.is_rx and not msg.is_error_frame:
            self.last_rx_msg_time = time.time()

    def ck_no_communication(self, last_timeout=1):
        """校验bus处于无通讯状态，评价标准为此时距离最后一帧报文时间已超过last_timeout(unit：s)"""
        with allure.step(f"校验当前{self.channel}通道处于休眠状态"):
            if time.time() - self.last_rx_msg_time > last_timeout:
                logger.info("当前%s通道处于休眠状态", self.channel)
            else:
                assert False, f"当前{self.channel}通道不处于休眠状态，最后一帧报文时间{self.last_rx_msg_time}, 当前时间{time.time()}"

    def ck_rx_nm_detail(self, canid: int, data_str: str, exp_count: int, timeout: float):
        """校验收到的rx报文"""
        with allure.step(f"校验接收到的网络管理报文"):
            self.tmp.ck_nm_canid = canid
            self.tmp.ck_canid_nm_count = 0
            self.tmp.ck_nm_data = bytearray(
                DataTypeHanding.hexstr_to_inlist(data_str))
            self.add_listener(self.__rx_nm)
            st = time.time()
            sleep(1)
            self.remove_listener(self.__rx_nm)
            assert self.tmp.ck_canid_nm_count == exp_count, \
                f"{timeout}s内接收到期望报文的数量为{self.tmp.ck_canid_nm_count}, 不满足预期的{exp_count}"
            self.tmp.__delattr__("ck_nm_canid")
            self.tmp.__delattr__("ck_canid_nm_count")
            self.tmp.__delattr__("ck_nm_data")
            logger.info(f"在{timeout}s内获取到{exp_count}帧{hex(canid)}-{data_str}")

    def rx_nm(self, msg):
        """监控特定内容的NM报文个数"""
        # logger.info(msg)
        if msg.arbitration_id == 0x501:
            print(msg)

    def __rx_nm(self, msg):
        """监控特定内容的NM报文个数"""
        if msg.arbitration_id == self.tmp.ck_nm_canid:
            logger.info(msg)
            self.tmp.ck_canid_nm_count += 1
            assert msg.data == self.tmp.ck_nm_data, f"msg.data != case expected data : {self.tmp.ck_nm_data}"
            logger.info(time.time() - msg.timestamp)

    def __ck_exist_app_msg(self, msg):
        if msg.arbitration_id > 0x53F or msg.arbitration_id < 0x500:
            self.tmp.exist_app_msg = True

    def ck_exist_app_msg(self, timeout=1):
        """校验超时时间内存在任一应用报文， 接收到立即退出"""
        st = time.time()
        self.tmp.exist_app_msg = False
        self.add_listener(self.__ck_exist_app_msg)
        while time.time() - st < timeout:
            if self.tmp.exist_app_msg:
                self.remove_listener(self.__ck_exist_app_msg)
                return True
        else:
            self.remove_listener(self.__ck_exist_app_msg)
            assert False, f"{timeout}s超时仍未接收到任一个应用报文"

    def __ck_exist_canid_with_data(self, msg):
        if msg.arbitration_id == self.tmp.ck_canid and msg.data == self.tmp.ck_data:
            self.tmp.exist_canid_with_data = True

    def ck_exist_canid_with_data(self, canid: int, data_str: str, timeout: float):
        """校验在超时时间内收到特定报文"""
        st = time.time()
        self.tmp.ck_canid = canid
        self.tmp.ck_data = bytearray(
            DataTypeHanding.hexstr_to_inlist(data_str))
        self.tmp.exist_canid_with_data = False
        self.add_listener(self.__ck_exist_canid_with_data)
        while time.time() - st < timeout:
            if self.tmp.exist_canid_with_data:
                self.remove_listener(self.__ck_exist_canid_with_data)
                self.tmp.__delattr__("ck_canid")
                self.tmp.__delattr__("exist_canid_with_data")
                self.tmp.__delattr__("ck_data")
                logger.info(f"获取到{hex(canid)}-{data_str}")
                return True
        else:
            self.remove_listener(self.__ck_exist_canid_with_data)
            assert False, f"{timeout}s超时仍未接收期望报文{hex(canid)}-{data_str}"

    def ck_msg_period_by_canid(self, canid: int, period: int, timeout: int = 3):
        """
        校验超时时间内，接收到特定canid的报文满足特定周期上报（偏差为10%）
        :param canid: 接收的指定canid
        :param period: 校验周期，s
        :param timeout: 校验持续时间，s
        :return:
        """
        st = time.time()
        self.tmp.ck_canid = canid
        self.tmp.ck_canid_times = []
        self.add_listener(self.__ck_msg_period_by_canid)
        sleep(timeout)
        self.remove_listener(self.__ck_msg_period_by_canid)
        tmp = self.tmp.ck_canid_times
        for i in range(1, len(tmp)):
            assert 0.9 * period < tmp[i] - tmp[i - 1] < 1.1 * \
                   period, f"{tmp}周期不为{period}s"
        logger.info(f"{tmp}周期正常，为{period}s")
        self.tmp.__delattr__("ck_canid")
        self.tmp.__delattr__("ck_canid_times")

    def __ck_msg_period_by_canid(self, msg):
        if msg.arbitration_id == self.tmp.ck_canid:
            logger.info(msg)
            self.tmp.ck_canid_times.append(msg.timestamp)

    def ck_immediate_transmission(self, canid: int, pnc_msk: list):
        """
        校验触发快发机制，20ms周期发送20帧
        :param canid: 校验的NM canid
        :param pnc_msk: 快发中的pnc置位掩码[0x0，0x0, 0x0, 0x0, 0x0, 0x0]
        :return:
        """
        self.tmp.ck_immediate_transmission = {"canid": canid, "msgs": []}
        self.add_listener(self.__ck_immediate_transmission)
        sleep(1)
        self.remove_listener(self.__ck_immediate_transmission)
        msgs = self.tmp.ck_immediate_transmission["msgs"]
        assert len(msgs) == 20, f"1s内接收到期望报文的数量为{len(msgs)}, 不满足预期的20帧"
        for msg in msgs:
            cal_mask = [pnc_msk[i - 2] & msg.data[i] for i in range(2, 8)]
            assert not cal_mask == [0] * 6, f"快发报文中掩码错误， 不满足{pnc_msk}"

    def __ck_immediate_transmission(self, msg):
        if msg.arbitration_id == self.tmp.ck_immediate_transmission['canid']:
            logger.info(msg)
            self.tmp.ck_immediate_transmission['msgs'].append(msg)


class ConnectivityCanFd(CanBus):
    """定义了ConnectivityCanFd上常用的功能"""

    def __init__(self, interface='socketcan', channel='can1', bitrate=500000, fd=True, ipdu_bus_dict=None):
        super().__init__(interface, channel, bitrate, fd)
        self.ipdu_connectivitycanfd_dict = ipdu_bus_dict
        self.init_signal()

        self.dk_can_encrypt = BncmBgmPduEncrypt()
        self.reset_bncm_digital_keyinfo()

        self.last_dk_send_canid = DigKeyBLEReq  # 初始化最后一次发送的报文id
        self.exp_dk_resp_canid = DigKeyBLEResp  # 初始化当前期望接收的dk报文的id
        self.get_bgm_send_error_frame = False  # BGM是否发送了错误帧
        self.get_bgm_send_error_frame_ack = False  # 是否获取到BGM响应错误帧
        self.get_bgm_send_idle_count = 0  # BGM在发送错误帧后发送的空白帧次数，达到2次后可以再次发送
        # BGM每发送一个数据包是否有收到ack应答报文(响应报文ack=发送报文header)
        self.get_dk_bgm_ack = False
        self.dk_req_header = 0  # BNCM下发的数据包的header
        self.dk_data_queue_internal = Queue()  # 内部使用用于获取并响应寻钥匙结果，存储bytes的原始数据
        self.dk_data_queue_external = Queue()  # 接收BGM发送的数据，寻钥匙指令及车控响应报文，解析后的明文

        self.dk_data = bytearray()  # BGM发送的寻钥匙指令及车控响应报文（密文）
        self.dk_data_len = 0  # 从hello_message中获取的报文长度，用于截取有效数据
        self.last_dk_ble_resp_header = 0  # 记录BGM发送的0x30及0x175报文的header, 防止BGM发送相同header报文时，代码重复截取有效数据

        self.id_map = {DigKeyBLEReq: DigKeyBLEResp, DigKeyBLEResp: DigKeyBLEReq,
                       DigKeyBLEResp2: DigkeyBLEReq2, DigkeyBLEReq2: DigKeyBLEResp2,
                       DigKeyBLEReq3: DigKeyBLEResp3, DigKeyBLEResp3: DigKeyBLEReq3}
        self.listen_and_update_signal(self.listen_pdus_signal)  # 启动线程监测并更新BGM在body上常见信号量

    def init_signal(self):
        """初始化常用的信号量"""
        self.cenlock_sts = 0
        self.cenlock_sts_type = self.ipdu_connectivitycanfd_dict.VgmConnFr12.LockgCenStsLockSt_2_VgmConnSignalIPdu12
        self.cenlock_sts_trigsrc = 0
        self.cenlock_sts_trigsrc_type = self.ipdu_connectivitycanfd_dict.VgmConnFr12.LockgCenStsTrigSrc_2_VgmConnSignalIPdu12
        self.bgm_time_type = self.ipdu_connectivitycanfd_dict.VgmConnFr12.CarTiGlb_6_VgmConnSignalIPdu12
        # self.bgm_time_type = self.ipdu_connectivitycanfd_dict.VgmConnFr12.CarTiGlb_8_VgmConnSignalIPdu12  # 0.6.0
        self.pnc23 = 0
        # self.pnc23_type = self.ipdu_connectivitycanfd_dict.BgmConnectivityCANNmFr.

    def ck_cenlock_sts(self, exp_sts: int, exp_trigsrc: Union[None, int] = None):
        """
        校验中控锁状态
        :param exp_sts: 期望的中控锁状态
        :param exp_trigsrc: 期望的中控锁触发源
        """
        assert self.cenlock_sts == exp_sts, \
            format_assert_log("中控锁状态", self.cenlock_sts, exp_sts, cenlock_sts_desc)
        if exp_trigsrc is not None:
            assert self.cenlock_sts_trigsrc == exp_trigsrc, \
                format_assert_log("中控锁触发源", self.cenlock_sts_trigsrc, exp_trigsrc, cenlock_sts_trigsrc_desc)

    def listen_pdus_signal(self, msg):
        """监听并更新BGM在该bus上发出常用信号量"""
        if msg.arbitration_id == 0x470 and msg.is_rx:
            self.cenlock_sts = get_signal_from_bytes(
                msg.data, self.cenlock_sts_type)
            self.cenlock_sts_trigsrc = get_signal_from_bytes(msg.data, self.cenlock_sts_trigsrc_type)
            self.dk_can_encrypt.update_bgm_time(get_signal_from_bytes(msg.data, self.bgm_time_type))
        elif msg.arbitration_id == 0x533 and msg.is_rx:
            self.pnc23 = (msg.data[2] & 0x80) >> 7


class BodyCan(CanBus):
    """定义了BodyCan上常用的功能"""

    def __init__(self, interface='socketcan', channel='can4', bitrate=500000, fd=False, ipdu_bus_dict=None):
        super().__init__(interface, channel, bitrate, fd)
        self.ipdu_bodycan_dict = ipdu_bus_dict

        self.door_driver_lock_cmd = 0
        self.door_passive_lock_cmd = 0
        self.door_left_rear_lock_cmd = 0
        self.door_right_rear_lock_cmd = 0

        self.tr_opener_req_cmd = 0
        self.tr_opener_req_trigsrc = 0

        self.door_opener_driver_req_cmd = 0
        self.door_opener_passive_req_cmd = 0
        self.door_opener_left_rear_req_cmd = 0
        self.door_opener_right_rear_req_cmd = 0
        self.door_opener_driver_req_trigsrc = 0
        self.door_opener_passive_req_trigsrc = 0
        self.door_opener_left_rear_req_trigsrc = 0
        self.door_opener_right_rear_req_trigsrc = 0

        self.door_drvr_sts = 0
        self.door_pass_sts = 0
        self.door_lere_sts = 0
        self.door_rire_sts = 0
        self.door_tr_sts = 0

        self.window_drvr_pos = 0
        self.window_pass_pos = 0
        self.window_lere_pos = 0
        self.window_rire_pos = 0

        self.listen_pdus_func_map = {0x20: self.__listen_cembodyfr01,
                                     0x40: self.__listen_cembodyfr02,
                                     0xB4: self.__listen_cembodyfr78,
                                     0xB8: self.__listen_cembodyfr79,
                                     0xE0: self.__listen_cembodyfr11,
                                     0xB2: self.__listen_cembodyfr68}
        self.listen_and_update_signal(self.listen_pdus_signal)  # 启动线程监测并更新BGM在body上常见信号量

    def listen_pdus_signal(self, msg):
        """监听bodycan上BGM发出的报文，并更新到类变量中"""
        if msg.arbitration_id not in self.listen_pdus_func_map or not msg.is_rx:
            return
        self.listen_pdus_func_map[msg.arbitration_id](msg)

    def __listen_cembodyfr01(self, msg):
        """更新BGM发出的0x20四门锁开关指令到类属性，供测试用例调用
        0x0 LockActvnOff - Idle Command
        0x1 LockActvnUnlck - Unlock door
        0x2 LockActvnLock - Lock door
        0x3 LockActvnSafe - Double lock door
        0x4, 0x8, 0xC, 0xD, 0xE LockActvnUnlckByCrash - Crash Unlock door
        """
        target_msg = self.ipdu_bodycan_dict.CemBodyFr01
        self.door_driver_lock_cmd = \
            get_signal_from_bytes(
                msg.data, target_msg.DoorDrvrLockCmd_1_CemBodySignalIPdu01)
        self.door_passive_lock_cmd = get_signal_from_bytes(
            msg.data, target_msg.DoorPassLockCmd)
        self.door_left_rear_lock_cmd = get_signal_from_bytes(
            msg.data, target_msg.DoorLeReLockCmd)
        self.door_right_rear_lock_cmd = get_signal_from_bytes(
            msg.data, target_msg.DoorRiReLockCmd)

    def __listen_cembodyfr02(self, msg):
        """更新BGM发出0x40的尾门开关指令,及左前，左后门状态，供测试用例调用
        0x0 TrOpenerIdle
        0x1 TrOpenerOpen
        0x2 TrOpenerCls
        0x3 TrOpenerStop
        0x4 TrOpenerIClsDly
        """
        target_msg = self.ipdu_bodycan_dict.CemBodyFr02
        self.tr_opener_req_cmd = get_signal_from_bytes(
            msg.data, target_msg.TrOpenerReqTrOpenerReq)
        self.tr_opener_req_trigsrc = get_signal_from_bytes(
            msg.data, target_msg.TrOpenerReqTrigSrc)
        self.door_drvr_sts = get_signal_from_bytes(
            msg.data, target_msg.DoorDrvrSts_2_CemBodySignalIPdu02)
        self.door_lere_sts = get_signal_from_bytes(
            msg.data, target_msg.DoorLeReSts_1_CemBodySignalIPdu02)

    def __listen_cembodyfr11(self, msg):
        """更新BGM发出0xE0的右前，右后及尾门开关状态到类属性，供测试用例调用
        0x0 DoorSts2_Ukwn
        0x1 DoorSts2_Opend
        0x2 DoorSts2_Clsd
        """
        target_msg = self.ipdu_bodycan_dict.CEMBodyFr11
        self.door_pass_sts = get_signal_from_bytes(
            msg.data, target_msg.DoorPassSts_2_CEMBodySignalIPdu11)
        self.door_rire_sts = get_signal_from_bytes(
            msg.data, target_msg.DoorRiReSts_1_CEMBodySignalIPdu11)
        self.door_tr_sts = get_signal_from_bytes(
            msg.data, target_msg.TrSts_2_CEMBodySignalIPdu11)

    def __listen_cembodyfr78(self, msg):
        """更新BGM发出的0xB4左前门和左后门开关指令到类属性，供测试用例调用
        开关指令
        0x0 DoorOpenerIdle
        0x1 DoorOpenerOpen
        0x2 DoorOpenerCls
        0x3 DoorOpenerIStop
        0x4 DoorOpenerIOpenMinang
        指令来源
        0x0 NoTrigSrc - No trig source
        0x1 KeyRem - Remote Key
        0x2 HMI - Center stack display
        0x3 Telm - Telematics
        0x4 OutdSwt - Outer door switch
        0x5 InsdSwt - Inside door switch
        """
        target_msg = self.ipdu_bodycan_dict.CemBodyFr78
        self.door_opener_driver_req_cmd = \
            get_signal_from_bytes(
                msg.data, target_msg.DoorOpenerDrvrReqDoorOpenerReq2)
        self.door_opener_driver_req_trigsrc = \
            get_signal_from_bytes(
                msg.data, target_msg.DoorOpenerDrvrReqTrigSrc)
        self.door_opener_left_rear_req_cmd = \
            get_signal_from_bytes(
                msg.data, target_msg.DoorOpenerLeReReqDoorOpenerReq2)
        self.door_opener_left_rear_req_trigsrc = \
            get_signal_from_bytes(
                msg.data, target_msg.DoorOpenerLeReReqTrigSrc)

    def __listen_cembodyfr79(self, msg):
        """更新BGM发出0xB8的右前门和右后门开关指令到类属性，供测试用例调用
        参数同__listen_cembodyfr78
        """
        target_msg = self.ipdu_bodycan_dict.CemBodyFr79
        self.door_opener_passive_req_cmd = \
            get_signal_from_bytes(
                msg.data, target_msg.DoorOpenerPassReqDoorOpenerReq2)
        self.door_opener_passive_req_trigsrc = \
            get_signal_from_bytes(
                msg.data, target_msg.DoorOpenerPassReqTrigSrc)
        self.door_opener_right_rear_req_cmd = \
            get_signal_from_bytes(
                msg.data, target_msg.DoorOpenerRiReReqDoorOpenerReq2)
        self.door_opener_right_rear_req_trigsrc = \
            get_signal_from_bytes(
                msg.data, target_msg.DoorOpenerRiReReqTrigSrc)

    def __listen_cembodyfr68(self, msg):
        """更新BGM发出0xB2的车窗开度指令到类属性，供测试用例调用"""
        target_msg = self.ipdu_bodycan_dict.CemBodyFr68
        self.window_drvr_pos = \
            get_signal_from_bytes(
                msg.data, target_msg.WinOpenDrvrReq)
        self.window_pass_pos = \
            get_signal_from_bytes(
                msg.data, target_msg.WinOpenPassReq)
        self.window_lere_pos = \
            get_signal_from_bytes(
                msg.data, target_msg.WinOpenReLeReq)
        self.window_rire_pos = \
            get_signal_from_bytes(
                msg.data, target_msg.WinOpenReRiReq)

    def logger_door_sts(self):
        """打印5个门状态"""
        door_sts_map = {0x0: "Ukwn", 0x1: "Opend", 0x2: "Clsd"}
        logger.info(f"左前门：{door_sts_map[self.door_drvr_sts]}, \
        右前门：{door_sts_map[self.door_pass_sts]}, \
        左后门: {door_sts_map[self.door_lere_sts]}, \
        右后门: {door_sts_map[self.door_rire_sts]}, \
        尾门: {door_sts_map[self.door_tr_sts]}")

    def ck_door_lock_cmd(self, drvr_cmd, pass_cmd, lere_cmd, rire_cmd):
        """
        校验BGM中0x20发出的四门锁的指令
        0x0 LockActvnOff - Idle Command
        0x1 LockActvnUnlck - Unlock door
        0x2 LockActvnLock - Lock door
        0x3 LockActvnSafe - Double lock door
        0x4, 0x8, 0xC, 0xD, 0xE LockActvnUnlckByCrash - Crash Unlock door
        :param drvr_cmd: 左前门锁指令
        :param pass_cmd: 右前门锁指令
        :param lere_cmd: 左后门锁指令
        :param rire_cmd: 右后门锁指令
        :return:
        """
        assert self.door_driver_lock_cmd == drvr_cmd, format_assert_log("左前门锁指令", self.door_driver_lock_cmd,
                                                                        drvr_cmd, door_lock_cmd_desc)
        assert self.door_passive_lock_cmd == pass_cmd, format_assert_log("右前门锁指令", self.door_passive_lock_cmd,
                                                                         pass_cmd, door_lock_cmd_desc)
        assert self.door_left_rear_lock_cmd == lere_cmd, format_assert_log("左后门锁指令", self.door_left_rear_lock_cmd,
                                                                           lere_cmd, door_lock_cmd_desc)
        assert self.door_right_rear_lock_cmd == rire_cmd, format_assert_log("右后门锁指令",
                                                                            self.door_right_rear_lock_cmd, rire_cmd,
                                                                            door_lock_cmd_desc)

    def ck_door_opener_cmd(self, door_index: int, door_cmd: int, triggre_src: Union[None, int] = None):
        """
        校验BGM中0xB4和0xB8和0x40发出的五门开门指令的指令
        :param door_index: 门序号，1左前；2右前；3左后；4右后；5尾门
        :param door_cmd: 门开关指令  0x0 DoorOpenerIdle; 0x1 DoorOpenerOpen; 0x2 DoorOpenerCls; 0x3 DoorOpenerIStop; 0x4 DoorOpenerIOpenMinang
        :param triggre_src: 门开关指令触发源
        :return:
        """
        mapping = {1: [self.door_opener_driver_req_cmd, self.door_opener_driver_req_trigsrc],
                   2: [self.door_opener_passive_req_cmd, self.door_opener_driver_req_trigsrc],
                   3: [self.door_opener_left_rear_req_cmd, self.door_opener_left_rear_req_trigsrc],
                   4: [self.door_opener_right_rear_req_cmd, self.door_opener_right_rear_req_trigsrc],
                   5: [self.tr_opener_req_cmd, self.tr_opener_req_trigsrc]}
        assert mapping[door_index][0] == door_cmd, format_assert_log(f"当前车门{door_index}的开门指令",
                                                                     mapping[door_index][0], door_cmd,
                                                                     door_opener_cmd_desc)
        if triggre_src is not None:
            assert mapping[door_index][1] == triggre_src, format_assert_log(f"当前车门{door_index}的开门指令",
                                                                            mapping[door_index][1], triggre_src,
                                                                            door_opener_trigsrc_desc)


class PassiveSafetyCan(CanBus):
    def __init__(self, interface='socketcan', channel='can5', bitrate=500000, fd=False, ipdu_bus_dict=None):
        super().__init__(interface, channel, bitrate, fd)
        self.ipdu_passivesafetycan_dict = ipdu_bus_dict


class BodyExposedCanFd(CanBus):
    def __init__(self, interface='socketcan', channel='can0', bitrate=500000, fd=True, ipdu_bus_dict=None):
        super().__init__(interface, channel, bitrate, fd)
        self.ipdu_bodyexposedcanfd_dict = ipdu_bus_dict


class ADCanFd(CanBus):
    def __init__(self, interface='socketcan', channel='can2', bitrate=500000, fd=True, ipdu_bus_dict=None):
        super().__init__(interface, channel, bitrate, fd)
        self.ipdu_adcanfd_dict = ipdu_bus_dict


class InfoCanFd(CanBus):
    def __init__(self, interface='socketcan', channel='can', bitrate=500000, fd=True, ipdu_bus_dict=None):
        super().__init__(interface, channel, bitrate, fd)
        self.ipdu_infocanfd_dict = ipdu_bus_dict


def get_signal_from_bytes(data_bytes: bytes, signal_type: type):
    """
    从原始数据中根据起始bit位和长度获取数据, 参照调用的实例理解
    :param data_bytes: bytes类型的数据
    :param signal_type: 信号类，包含各种信息
    :return: int
    """
    start_bit = signal_type.sig_start_bit
    bit_length = signal_type.sig_length
    if signal_type.sig_byteorder == 'Motorola':
        int_data = int.from_bytes(data_bytes, 'big')
    else:
        int_data = int.from_bytes(data_bytes, 'little')
    real_start_bit = (start_bit // 8) * 8 - 1 + \
                     (start_bit // 8 + 1) * 8 - start_bit
    bytes_length = len(data_bytes)
    bin_data_str = bin(int_data).replace("0b", "").zfill(bytes_length * 8)
    return int(bin_data_str[real_start_bit: real_start_bit + bit_length], 2)


if __name__ == '__main__':
    # connectivity_bus = CanBus()
    # connectivity_bus.bus_send(
    #     DigKeyBLEReq, [0x3F, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
    from xat_ecu.legacy.sdk.data.mars1.can_lin_fr_cls.v_0_6_5.bodycan import CemBodyFr02

    a = get_signal_from_bytes(DataTypeHanding.hexstr_to_bytes(
        '6b 1a 00 40 40 19 a0 20'), CemBodyFr02.DoorDrvrSts_2_CemBodySignalIPdu02)
    print(a)
