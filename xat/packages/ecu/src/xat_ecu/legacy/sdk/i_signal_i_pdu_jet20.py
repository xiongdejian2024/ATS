# -*- coding: utf-8 -*-
"""
@File        : i_signal_i_pdu_jet20.py
@Author      : quan.sun@jiduauto.com
@Time        : 2022/04/04 8:36 AM
@Description : description about this file
@Examples    : example of how to use it
"""

import os
import signal
import subprocess
import sys
import threading
from itertools import cycle
from collections import deque, defaultdict

from xat_ecu.legacy.sdk.s2spdu.signal2service_combination_and_send_pdu_jet20 import S2sCombinationSendPdu

current_path = os.path.dirname(os.path.realpath(__file__))
from typing import Tuple, Union, List
import importlib
from xat_ecu.legacy.common.file_handle import *
from xat_ecu.legacy.common.data_type_handing import *
import json
from xat_ecu.legacy.common import exception_error
from xat_ecu.legacy.common.error_code import StatusCode
from xat_ecu.legacy.common.exception_error import error_check

from threading import Thread
import time
from time import sleep
import argparse
from xat_ecu.legacy.sdk.jd_e2e import *
import re
import random


def get_message_name_can_or_lin(obj_list, message_id):
    for attr in dir(obj_list):
        obj1 = getattr(obj_list, attr)
        if hasattr(obj1, 'msg_id'):
            obj2 = getattr(obj1, 'msg_id')
            if int(obj2) == message_id:
                return attr, getattr(obj1, 'msg_tx_method')
    else:
        logger.info("message id 不可用")
        return "message id 不可用", ""


def bus_signal_varify(can_list, key, pdu, run_result):
    candump_cmd = f"candump {can_list.get(key)}"
    timeout = 2
    logger.info("candump命令为：" + candump_cmd)
    start = datetime.datetime.now()
    p = subprocess.Popen(
        candump_cmd,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
        shell=True,
        close_fds=True,
        start_new_session=True,
    )
    formats = 'utf-8'
    time_flag = True
    i = 0
    try:
        while p.poll() is None and time_flag:
            line = p.stdout.readline()
            i = i + 1
            line = line.strip()
            if line:
                line = ' '.join(line.decode(formats).strip().split())
                message_id = line.split()[1]
                if message_id == '512':
                    i = i - 1
                    continue
                # logger.info(f"message id is {line.split()[1]}.")
                # 从执行结果中过滤帧ID，并验证是否属于该总线
                obj_list = getattr(pdu, key)
                message_id = int(message_id, 16)
                message_name, _ = get_message_name_can_or_lin(obj_list, message_id)
                logger.info(message_name)
                if message_name == 'message id 不可用':
                    run_result[key] = {
                        "result": "fail",
                        "message": f"{key} 总线mapping异常，异常报文," f"{line}",
                    }
                    break
                time.sleep(0.01)
            now = datetime.datetime.now()
            if (now - start).seconds > timeout:
                time_flag = False
            if i == 10:
                time_flag = False
        else:
            run_result[key] = {"result": "pass", "message": f"{key} 总线检测正常！"}
        if p.returncode:
            code = 4
            msg = "[ERROR]执行异常"
        else:
            code = 2
            msg = "[INFO]执行成功"
    except subprocess.TimeoutExpired:
        code = 4
        msg = (
            "[ERROR]Timeout Error : Command '"
            + candump_cmd
            + "' timed out after "
            + str(timeout)
            + " seconds"
        )
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/i_signal_i_pdu_jet20.py")
        code = 4
        msg = "[ERROR]Unknown Error : " + str(e)
    finally:
        logger.info(f"结果码：{code}, 错误详细{msg}")
        logger.info("开始资源回收..........")
        p.kill()
        p.terminate()
        os.killpg(p.pid, signal.SIGTERM)


class ISignalIPdu:
    def __init__(self, cls_path, dut_ecu=[]):
        self.cls_path = os.path.join(parent_dir, cls_path)
        self.pdu_path = self.cls_path.replace(
            "can_lin_fr_cls", "can_lin_fr_init_pdu_json"
        )
        self.dut_ecu = dut_ecu

        cls_full_module_name = cls_path.replace("/", ".")
        cls_module = importlib.import_module(cls_full_module_name)
        # logger.info("dynamic cls_module_name is {}".format(cls_module.__name__))
        print("动态模块名是：{}".format(cls_module.__name__))
        for module_name in cls_module.__all__:
            module_obj = getattr(cls_module, module_name)
            setattr(self, module_name, module_obj)

        self.bus_pdu_dict = {}
        # ---------------------------------------------------
        if os.path.exists(self.pdu_path):
            file_name_and_paths = FileHandle.get_file_name_and_paths_from_dir(
                self.pdu_path
            )
            print(f"{file_name_and_paths}")
            for file_name, file_path in file_name_and_paths:
                logger.info(f"{file_name}")
                # with open(file_path.replace("/", "\\"), "r") as f: # windows 电脑
                with open(file_path, "r") as f:
                    self.bus_pdu_dict[file_name] = json.load(f)
                    print(self.bus_pdu_dict[file_name])
        else:
            logger.warning("{} is not exist".format(self.pdu_path))
        self.time_control_flag = None
        self.__check_results = {}
        self.__check_event_results = {}
        self.recv_pdu_flag = False
        self.check_event_flag = False
        self.signal_random_flag = True
        self.special_message_run_flag = False

        self.fr_resume_flag = None
        self.is_realbus = None
        self.receive_message_queue = defaultdict(deque)
        self.receive_current_message = None
        self.max_receive_number = 50
        self.lock = threading.Lock()

    def restore_bus_signal_to_default_value(self, bus_name, message_name, signal_name, set_default_value=True):
        """
        设置总线信号恢复到默认值
        @param bus_name: 通道，can lin fr
        @param message_name: 报文名称，字符串类型；或者报文ID，整型
        @param signal_name: 报文的某个信号名称
        @param set_default_value: 设置默认值，不需要用户传参
        """
        pdu_dicts = self.bus_pdu_dict.get(bus_name)
        if not pdu_dicts:
            logger.warning(f"没有发现指定通道：{bus_name}")
            raise AssertionError(f"没有发现指定通道：{bus_name}")

        for inner_message, msg_info in pdu_dicts.items():
            if isinstance(message_name, int):
                if msg_info.get("msg_id") != message_name:
                    continue
            elif isinstance(message_name, str):
                if inner_message != message_name:
                    continue
            else:
                logger.warning(f"消息类型错误，得到：{type(message_name)}")
            if msg_info.get("tx_node") not in self.dut_ecu:
                msg_obj = getattr(getattr(self, bus_name), inner_message)
                for _signal_name in dir(msg_obj):
                    if _signal_name == signal_name:
                        sig_obj = getattr(msg_obj, _signal_name)
                        if hasattr(sig_obj, "sig_value_init"):
                            value = getattr(sig_obj, "sig_value_init")
                            if not set_default_value:
                                value = 0 if value != 0 else 1
                            self.set(msg_obj, _signal_name, value)
                            logger.info(f"信号：{_signal_name} 恢复到发送默认值：{value}")
                            return
        logger.warning(f"没有发现需要设置的信号,请仔细核对输入信号是否有误")
        raise AssertionError(f"没有发现需要设置的信号,请仔细核对输入信号是否有误")

    def restore_bus_signal_to_not_default_value(self, bus_name, message_name, signal_name):
        """
        设置总线信号恢复到非默认值
        @param bus_name: 通道，can lin fr
        @param message_name: 报文名称，字符串类型；或者报文ID，整型
        @param signal_name: 报文的某个信号名称
        """
        self.restore_bus_signal_to_default_value(bus_name, message_name, signal_name, False)

    def restore_bus_message_to_default_value(self, bus_name, message_name, set_default_value=True):
        """
        设置总线message恢复到默认值
        @param bus_name: 通道，can lin fr
        @param message_name: 报文名称，字符串类型；或者报文ID，整型
        @param set_default_value: 设置默认值，不需要用户传参
        """
        pdu_dicts = self.bus_pdu_dict.get(bus_name)
        if not pdu_dicts:
            logger.warning(f"没有发现指定通道：{bus_name}")
            raise AssertionError(f"没有发现指定通道：{bus_name}")

        for inner_message, msg_info in pdu_dicts.items():
            if isinstance(message_name, int):
                if msg_info.get("msg_id") != message_name:
                    continue
            elif isinstance(message_name, str):
                if inner_message != message_name:
                    continue
            else:
                logger.warning(f"消息类型错误，得到：{type(message_name)}")
            if msg_info.get("tx_node") not in self.dut_ecu:
                if (
                        # msg_info.get("msg_cycle")
                        # and
                        ("NmFr" not in inner_message)
                        and ("Diag" not in inner_message)
                ):
                    msg_obj = getattr(getattr(self, bus_name), inner_message)
                    need_signal_list = []
                    for signal_name in dir(msg_obj):
                        need_signal_list.append(signal_name)
                        logger.info(f"需要恢复到默认值信号List是：{need_signal_list}")
                    for sig in need_signal_list:
                        sig_obj = getattr(msg_obj, sig)
                        if hasattr(sig_obj, "sig_value_init"):
                            value = getattr(sig_obj, "sig_value_init")
                            if not set_default_value:
                                value = 0 if value != 0 else 1
                            self.set(msg_obj, sig, value)
                            logger.info(f"信号：{sig} 恢复到值是：{value}")

    def restore_bus_message_to_not_default_value(self, bus_name, message_name):
        """
        设置总线message恢复到非默认值
        @param bus_name: 通道，can lin fr
        @param message_name: 报文名称，字符串类型；或者报文ID，整型
        """
        self.restore_bus_message_to_default_value(bus_name, message_name, False)

    def reset_dpu_data(self):
        """
        将can/lin发送或接受的Pud数据重置为最初始的默认数据
        """
        if os.path.exists(self.pdu_path):
            file_name_and_paths = FileHandle.get_file_name_and_paths_from_dir(
                self.pdu_path
            )
            for file_name, file_path in file_name_and_paths:
                with open(file_path, "r") as f:
                    raw_pdu_data = json.load(f)
                    for message_name, message_info in raw_pdu_data.items():
                        if self.bus_pdu_dict.get(file_name):
                            self.bus_pdu_dict[file_name][message_name]["pdu_data"] = message_info["pdu_data"]
                            self.init_control(file_name)
            time.sleep(1)

    # -------------------------------------------  常用合集  ----------------------------------------------------
    def set_vehspd(self, value=0):
        self.set(
            self.backbonefr.BcmVddmBackBoneFr06,
            'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06',
            value,
        )
        self.set(
            self.backbonefr.BcmVddmBackBoneFr06,
            'VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06',
            3,
        )

    def get_lin_scheduleTable(self, lin_bus):
        """
        获取lin的调度表信息
        
        :param lin_bus: lin bus 名    such as  "cem_lin1"
        :returns lin_scheduleTable_new: dict   such as {'Cem_Lin1_DiagResponseSchedule01': [(0, 'DiagResponse', 61, 8, 0.015)]}   (0, 'DiagResponse', 61, 8, 0.015) 解释：（lin调度表中的位置，lin msg 名字，msg id， length ，delay）
        """
        lin_obj = getattr(self, lin_bus)
        lin_scheduleTable =  getattr(lin_obj, "lin_scheduleTable")
        lin_scheduleTable_new = {}
        for lin_scheduleTable_name, lin_scheduleTable_info in lin_scheduleTable.items():
            lin_scheduleTable_info_new = []
            for lin_msg_info in lin_scheduleTable_info:
                lin_msg_name = lin_msg_info[1].split("FrTr")[-1]
                msg_id = getattr(lin_obj, lin_msg_name).msg_id
                lin_msg_length = getattr(lin_obj, lin_msg_name).msg_length
                lin_msg_info_new = (lin_msg_info[0], lin_msg_name, msg_id, lin_msg_length, lin_msg_info[2])
                lin_scheduleTable_info_new.append(lin_msg_info_new)
            lin_scheduleTable_new[lin_scheduleTable_name] = lin_scheduleTable_info_new
        return lin_scheduleTable_new

    def set_random_signal_thread_start(self, bus_name, num, interval_time=1):
        '''
        批量随机设置信号 线程启动
        #param:bus_name                  such as    bodycan
        #param:num    随机变化信号数量     sunch as    100
        #param:interval_time    多长时间间隔触发一次     sunch as    1  单位 秒
        #return
        '''
        self.signal_random_flag = True
        signal_random_thrading = Thread(
            target=self.set_random_signal,
            name="signal_random_thrading",
            args=(bus_name, num, interval_time),
            daemon=True,
        )
        signal_random_thrading.start()

    def set_random_signal_thread_all_stop(self):
        '''
        不会立马停止，最大会过set_random_signal_thread_start中的 interval_time（默认1s） 时间后停止
        '''
        self.signal_random_flag = False

    def set_random_signal(self, bus_name, num, interval_time=None):
        '''
        批量随机设置信号
        #param:bus_name                  such as    bodycan
        #param:num    随机变化信号数量     sunch as    100
        #param:interval_time    多长时间间隔触发一次     sunch as    1  单位 秒
        #return
        '''
        changesignalsinfo_list = self.get_changesignalsinfo_list(bus_name)
        if interval_time:
            while self.signal_random_flag:
                random_signalinfo_list = self.__get_random_signalinfo(
                    changesignalsinfo_list, num
                )
                for random_signalinfo in random_signalinfo_list:
                    msg_obj = random_signalinfo[0]
                    signal_name = random_signalinfo[1]
                    signal_length = random_signalinfo[2]
                    signal_value = random.randint(0, (1 << signal_length) - 1)
                    self.set(msg_obj, signal_name, signal_value)
                sleep(interval_time)
        else:
            random_signalinfo_list = self.__get_random_signalinfo(
                changesignalsinfo_list, num
            )
            for random_signalinfo in random_signalinfo_list:
                msg_obj = random_signalinfo[0]
                signal_name = random_signalinfo[1]
                signal_length = random_signalinfo[2]
                signal_value = random.randint(0, (1 << signal_length) - 1)
                self.set(msg_obj, signal_name, signal_value)

    def get_changesignalsinfo_list(self, bus_name):
        changesignalsinfo_list = []
        pdu_dict = self.bus_pdu_dict.get(bus_name)
        for message, msg_info in pdu_dict.items():
            if isinstance(message, int):
                logger.debug("此message 不需要")
                continue
            if msg_info.get("tx_node") not in self.dut_ecu:
                if (
                    msg_info.get("msg_cycle")
                    and ("NmFr" not in message)
                    and ("Diag" not in message)
                ):
                    msg_obj = getattr(getattr(self, bus_name), message)
                    for signal_name in dir(msg_obj):
                        if "__" not in signal_name and signal_name not in ('msg_cycle', 'msg_id', 'msg_length', 'msg_name', 'msg_tx_method', 'msg_type', 'rx_nodes', 'sig_group_dataid_dict', 'sig_group_dict', 'tx_node'):
                            if (
                                signal_name.endswith("_UB")
                                or signal_name.endswith("Chks")
                                or signal_name.endswith("Cntr")
                            ):
                                logger.debug("_UB , Chks, Cntr  不在changesignalsinfo_list中")
                            else:
                                signal_length = getattr(
                                    getattr(msg_obj, signal_name), "length"
                                )
                                changesignalsinfo = (msg_obj, signal_name, signal_length)
                                changesignalsinfo_list.append(changesignalsinfo)
        return changesignalsinfo_list

    def __get_random_signalinfo(self, signalsinfo_list, num):
        signalsinfo_list_num = len(signalsinfo_list)
        if num > signalsinfo_list_num:
            logger.warning(
                f"输入的随机数量超过上限，可改变数据信号数量为{signalsinfo_list_num} , 但输入数量为{num}， 以数量上限为准"
            )
            random_signalinfos = signalsinfo_list
        else:
            random_signalinfos = random.sample(signalsinfo_list, num)
        return random_signalinfos

    def send_pdu(
        self, bus_name: str, msg_id: Union[str, int], data: list, cycle_time=None
    ):
        pdu_info = self.bus_pdu_dict.get(bus_name)
        is_arxml_msg = False
        if isinstance(msg_id, str):
            msg = pdu_info.get(msg_id)
            if msg is None:
                raise ValueError(
                    "参数msg_id {} error!!  不在bus(arxml) 的msg ; 参数msg_id 必须是 int".format(
                        msg_id
                    )
                )
            is_arxml_msg = True
        elif isinstance(msg_id, int):
            for message in pdu_info.keys():
                msg = pdu_info.get(message)
                if msg.get("msg_id") == msg_id:
                    is_arxml_msg = True
                    msg_id = message
                    break

        if is_arxml_msg:
            msg["pdu_data"] = data
            msg["tx_change"] = True
            if cycle_time:
                msg["msg_cycle"] = cycle_time
            if msg.get("tx_flag") is not None:
                msg["tx_flag"] = True
        else:
            logger.info(
                "{} message is not in {} bus(arxml), New Add ...".format(
                    msg_id, bus_name
                )
            )

    def preheat_msg(self, bus_name, msg_name):
        '''
        # 预热msg发送, 让其 周期1ms 等待发送, 一般用在发送及时报文
        # 注意 预热至少要提前2s
        # 用在can bus
        '''
        pdu_info = self.bus_pdu_dict.get(bus_name)
        msg = pdu_info.get(msg_name)
        msg["pre_send"] = True

    def remove_preheating(self, bus_name, msg_name):
        pdu_info = self.bus_pdu_dict.get(bus_name)
        msg = pdu_info.get(msg_name)
        msg["pre_send"] = False

    def stop_send_pdu(self, bus_name: str, id: Union[str, int]):
        # 针对的是 can bus
        # 这个接口也就是 pause message
        # if bus_name == "backbonefr":
        #     pass
        # else:
        #     # can , lin
        #     # lin 的暂定会调用后等待一个周期再暂停
        pdu_info = self.bus_pdu_dict.get(bus_name)
        if isinstance(id, str):
            msg = pdu_info.get(id)
        elif isinstance(id, int):
            for message in pdu_info.keys():
                msg = pdu_info.get(message)
                if msg.get("msg_id") == id:
                    break
        if msg.get("tx_flag") is not None:
            msg["tx_flag"] = False
        if self.is_realbus:
            msg["tx_change"] = True
        else:
            msg["tx_change"] = False  # 适配 非真实总线情况 （模拟MCU pdu）
            
    def pause_ecu_send(self, bus_name: str, ecu_name: str):
        # 针对的是 can,lin bus； 暂停ecu节点发送;  FR暂时只能已bus为单位暂停
        pdu_info = self.bus_pdu_dict.get(bus_name)
        for message in pdu_info.keys():
            msg = pdu_info.get(message)
            if msg.get("tx_node") == ecu_name:
                if msg.get("tx_flag") is not None:
                    msg["tx_flag"] = False
                if self.is_realbus:
                    msg["tx_change"] = True
                else:
                    msg["tx_change"] = False

    def pause_bus_send(self, bus_name: str):
        # 实体bus FR 只能直接提停bus
        if bus_name == "backbonefr":
            self.fr_resume_flag = False

        pdu_info = self.bus_pdu_dict.get(bus_name)
        for message in pdu_info.keys():
            msg = pdu_info.get(message)
            if msg.get("tx_flag") == True:
                if msg.get("tx_flag") is not None:
                    msg["tx_flag"] = False
                if self.is_realbus:
                    msg["tx_change"] = True
                else:
                    msg["tx_change"] = False

    def pause_all_bus_send(self):
        # 目前只针对的是 can bus
        for bus_name in self.bus_pdu_dict.keys():
            self.pause_bus_send(bus_name)

    def resume_all_bus_send(self):
        # 目前只针对的是 can bus  ,  需要做2s的等待以确保所有的报文都恢复
        for bus_name in self.bus_pdu_dict.keys():
            self.resume_bus_send(bus_name)

    def resume_bus_send(self, bus_name: str):
        #  can bus  需要做2s的等待以确保所有的报文都恢复
        #  FR bus 需要做200ms 的等待以确保所有的报文都恢复
        if bus_name == "backbonefr":
            self.fr_resume_flag = True

        pdu_info = self.bus_pdu_dict.get(bus_name)
        for message in pdu_info.keys():
            msg = pdu_info.get(message)
            if msg.get("msg_cycle") and msg.get("tx_flag") is not None:
                msg["tx_flag"] = True
                msg["tx_change"] = True
                # if "lin" in bus_name:
                #     msg["tx_change"] = True

    def resume_ecu_send(self, bus_name: str, ecu_name: str):
        # 针对的是 can bus  需要做2s的等待以确保ECU所有的报文都恢复
        pdu_info = self.bus_pdu_dict.get(bus_name)
        for message in pdu_info.keys():
            msg = pdu_info.get(message)
            if msg.get("tx_node") == ecu_name:
                if msg.get("msg_cycle") and msg.get("tx_flag") is not None:
                    msg["tx_flag"] = True
                    msg["tx_change"] = True
                # if "lin" in bus_name:
                #     msg["tx_change"] = True

    def resume_send_pdu(self, bus_name: str, id: Union[str, int]):
        # 针对的是 can bus
        pdu_info = self.bus_pdu_dict.get(bus_name)
        if isinstance(id, str):
            msg = pdu_info.get(id)
        elif isinstance(id, int):
            for message in pdu_info.keys():
                msg = pdu_info.get(message)
                if msg.get("msg_id") == id:
                    break
        if msg.get("tx_flag") is not None:
            msg["tx_flag"] = True
        msg["tx_change"] = True
            # if "lin" in bus_name:
            #     msg["tx_change"] = True

    def check_bus_recv_message(self, bus_name, timeout=5):
        '''
        检查总线上是否收到报文, 收到了返回 True, 超时没有收到返回 None
        通常逻辑一般会搭配 resume_bus_send 使用
        '''
        self.rx_flag_reset_bus(bus_name)  # 避免之前收到消息的干扰
        pdu_info = self.bus_pdu_dict.get(bus_name)
        i = 0
        while i < timeout:
            i += 0.1
            sleep(0.1)
            for message in pdu_info.keys():
                if pdu_info[message].get("tx_node") in self.dut_ecu:
                    if pdu_info[message]["rx_flag"] == True:
                        return True

    def check_ecu_not_recv_message(self, ecu_name, timeout=5):
        """
        检查超时时间内，对应的ecu节点是否没有收到报文
        """
        for bus_name in self.bus_pdu_dict.keys():
            pdu_info = self.bus_pdu_dict.get(bus_name)
            for message in pdu_info.keys():
                if ecu_name in pdu_info[message].get("rx_nodes"):
                    pdu_info[message]["rx_flag"] = False
        else:
            logger.info(f"初始化完成，开始检验{ecu_name}在{timeout}秒内是否收不到报文")
            i = 0
            while i < timeout:
                i += 0.1
                sleep(0.1)
                for bus_name in self.bus_pdu_dict.keys():
                    pdu_info = self.bus_pdu_dict.get(bus_name)
                    for message in pdu_info.keys():
                        if ecu_name in pdu_info[message].get("rx_nodes"):
                            if pdu_info[message]["rx_flag"]:  # 接收到报文
                                return False
            else:
                return True  # 在超时时间内始终没有收到报文

    def recv_pdu(self, bus_name, id: Union[str, int], timeout=5, frame_nums: int=None):
        """
        从指定总线接收PDU数据。

        Args:
            bus_name (str): 总线名称。
            id (Union[str, int]): PDU的ID，可以是字符串或整数。
            timeout (int, optional): 接收PDU数据的超时时间，默认为5秒。
            frame_nums (int, optional): 需要捕获的帧数，默认为None，表示只捕获一帧数据。

        Returns:
            Union[tuple, List[tuple]]: 如果frame_nums为None，则返回一个包含(id, time_stamp, length, data)的元组；
            如果frame_nums指定了帧数，则返回一个包含多个(id, time_stamp, length, data)元组的列表。

        """
        pdu_info = self.bus_pdu_dict.get(bus_name)
        if frame_nums is None:
            captured_msgdata = self.capture_msgdata(pdu_info, id, timeout=timeout)
        else:
            captured_msgdata = []
            for _ in range(frame_nums):
                data = self.capture_msgdata(pdu_info, id, timeout=timeout)
                if data:
                    captured_msgdata.append(data)
                else:
                    logger.error(f"从总线{bus_name}接收PDU多帧数据超时，请检查！！")
                    break
                time.sleep(1)
        return captured_msgdata

    def __recv_pdu_thread(self, bus_name, id: Union[str, int], func, timeout=5):
        while self.recv_pdu_flag:
            captured_msgdata = self.recv_pdu(bus_name, id, timeout)
            if captured_msgdata:
                self.rx_flag_reset_msg(bus_name, id)
                func(captured_msgdata)
        logger.info("__recv_pdu_thread {} {} ==== Closed ====".format(bus_name, id))

    def recv_pdu_thread_start(self, bus_name, id: Union[str, int], func, timeout=10):
        self.recv_pdu_flag = True
        recv_pdu_thrading = Thread(
            target=self.__recv_pdu_thread,
            name="Recv_Pdu_Control",
            args=(bus_name, id, func, timeout),
            daemon=True,
        )
        recv_pdu_thrading.start()

    def recv_pdu_thread_all_stop(self):
        # 不会立马停止，最大会过recv_pdu_thread_start中的 timeout（默认5s） 时间后停止
        self.recv_pdu_flag = False

    def check_event_thread_start(
        self,
        msg_signals_obj: type,
        signal_name: str,
        base_sig_value_name: Union[str, int],
        target_sig_value_name: Union[str, int],
        timeout: Union[float, int] = 5,
        do_print=False,
    ):
        self.check_event_flag = True
        check_event_thrading = Thread(
            target=self.check_event,
            name="check_event thread",
            args=(
                msg_signals_obj,
                signal_name,
                base_sig_value_name,
                target_sig_value_name,
                timeout,
                do_print,
            ),
            daemon=True,
        )
        check_event_thrading.start()

    def check_event_thread_stop(self, signal_name, timeout=5):
        # param signal_name   要与 check_event_thread_start 里的 signal_name 一致
        # param timeout
        # return result  int   event发生的次数
        return self.got_check_event_result(signal_name, timeout=timeout)

    def reset_check_results(self):
        self.__check_results = {}

    def reset_check_event_results(self):
        self.__check_event_results = {}

    def get_check_results(self):
        # 非阻塞
        return self.__check_results

    def get_check_event_results(self):
        # 非阻塞
        return self.__check_event_results

    def get_check_result(self, signal_name):
        # 非阻塞
        # return result   None or [result, encoded_actual_signal_value, expected_signal_value]
        result = self.__check_results.get(signal_name)
        return result

    def get_check_event_result(self, signal_name):
        # 非阻塞
        # return result   int  event 发生次数
        result = self.__check_event_results.get(signal_name)
        return result

    def got_check_result(self, signal_name, timeout=30):
        # 阻塞
        # param timeout 最好是check中timeout的2倍及以上
        # return result   None or [result, encoded_actual_signal_value, expected_signal_value]
        result = self.__check_results.get(signal_name)
        if result is not None:
            return result

        i = 0
        while i < timeout:
            sleep(1)
            i += 1
            result = self.__check_results.get(signal_name)
            if result is not None:
                return result

    def got_check_event_result(self, signal_name, timeout=5):
        # 阻塞   每秒去轮询
        # param signal_name
        # param timeout   int
        # return result   int  event发生次数
        result = self.__check_event_results.get(signal_name)
        if result is not None:
            return result

        i = 0
        while i < timeout:
            sleep(1)
            i += 1
            result = self.__check_event_results.get(signal_name)
            if result is not None:
                return result

    def start_all_time_control(self, isrealbus=True):
        # 为了兼容之前的写法，名称暂不变化
        if isrealbus:
            self.is_realbus = True
            # 已经改为 init_control，非线程了, 没有start，stop 概念，即可不用调用  time_control_stop  函数
            for bus_name in self.bus_pdu_dict.keys():
                # 目前先暂时暴力唤醒can
                self.init_control(bus_name)

                if "can" in bus_name:
                    # # 暂停报文，先发唤醒帧
                    self.add_msg(
                        bus_name,
                        0x53F,
                        [0x3F, 0x40, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF],
                        0.5,
                    )
        else:
            self.is_realbus = None
            self.dut_ecu = []  # 去模拟所有ecu，包括网关
            # 这部分分支有 time_control_stop
            for bus_name in self.bus_pdu_dict.keys():
                pdu_info = self.bus_pdu_dict.get(bus_name)
                self.time_control_start(pdu_info)

    def init_control(self, bus_name):
        pdu_info = self.bus_pdu_dict.get(bus_name)
        # pdu_info   a bus info    such as self.bus_pdu_dict["adcanfd"]
        bus_obj = getattr(self, bus_name)
        for message in pdu_info.keys():

            # 防止默认有 crc 为0xFF的问题，影响tosun crc判断
            if isinstance(message, str):
                msg_obj = getattr(bus_obj, message, None)
                if msg_obj:
                    sig_group_dataid_dict = getattr(msg_obj, "sig_group_dataid_dict", None)
                    if sig_group_dataid_dict:
                        for sig_group in sig_group_dataid_dict:
                            self.restore_crc(msg_obj, sig_group)   
                
            if pdu_info[message].get("tx_node") not in self.dut_ecu:
                if pdu_info[message].get("msg_cycle"):
                    pdu_info[message]["tx_flag"] = True
                    pdu_info[message]["rx_flag"] = None
                    # pdu_info[message]["tx_change"] = False                
                else:
                    pdu_info[message]["tx_flag"] = False
                    pdu_info[message]["rx_flag"] = None
            else:
                pdu_info[message]["tx_flag"] = None
                pdu_info[message]["rx_flag"] = False

    def add_msg(self, bus_name, msg_id: int, data: list, cycle_time=None):
        # 增加bus 上不存在的 msg，该函数要用紧接着用在 init_control 后面
        # 设计目标是用在 can bus 上
        pdu_info = self.bus_pdu_dict.get(bus_name)
        pdu_info[msg_id] = {
            "msg_cycle": cycle_time,
            "msg_length": len(data),
            "msg_id": msg_id,
            "tx_flag": True,
            "rx_flag": None,
            "tx_node": None,
            "rx_nodes": None,
            "pdu_data": data,
            "tx_change": True,
        }

    def time_control(self, pdu_info):
        #: pdu_info   a bus info    such as self.bus_pdu_dict["adcanfd"]
        # 该接口目前只 非真实bus使用
        i = 0
        cycle_message = []
        for message in pdu_info.keys():
            if pdu_info[message].get("tx_node") not in self.dut_ecu:  # 默认非真实bus使用 模拟所有ecu
                cycle_message.append(message)
                if pdu_info[message].get("msg_cycle"):
                    pdu_info[message]["tx_flag"] = True
                    pdu_info[message]["time_count"] = i
                    pdu_info[message]["rx_flag"] = None
                    i += 0.001
                    if i == 0.02:
                        i = 0
                else:
                    pdu_info[message]["tx_flag"] = False
                    pdu_info[message]["time_count"] = None
                    pdu_info[message]["rx_flag"] = None
            else:
                pdu_info[message]["tx_flag"] = None
                pdu_info[message]["rx_flag"] = False
        # pdu_info["cycle_message"] = {
        #     "msg_cycle": None,
        #     "msg_length": None,
        #     "msg_id": None,
        #     "tx_flag": None,
        #     "rx_flag": None,
        #     "tx_node": None,
        #     "rx_nodes": None,
        #     "pdu_data": None,
        #     "cycle_message_list": cycle_message,
        # }

        while self.time_control_flag:
            sleep(0.001)
            for message in cycle_message:
                if pdu_info[message]["time_count"] is not None:
                    mes_dict = pdu_info[message]
                    mes_dict["time_count"] += 0.001
                    if mes_dict["time_count"] >= mes_dict["msg_cycle"]:
                        mes_dict["time_count"] = 0
                        # mes_dict["tx_flag"] = True
                        
                        # 默认为 非真实can逻辑
                        if mes_dict.get("tx_change") is None:
                            mes_dict["tx_change"] = True

    def rx_flag_reset_msg(self, bus_name, msgid: Union[str, int]):
        # msg rx_flag update to False   确保 pdu_data 有效性
        pdu_info = self.bus_pdu_dict.get(bus_name)
        if isinstance(msgid, str):
            msg = pdu_info.get(msgid)
            msg["rx_flag"] = False
        elif isinstance(msgid, int):
            for message in pdu_info.keys():
                msg = pdu_info.get(message)
                if msg.get("msg_id") == msgid:
                    msg["rx_flag"] = False
                    break

    def rx_flag_reset_bus(self, bus_name):
        # bus rx_flag update to False   确保 pdu_data 有效性
        pdu_info = self.bus_pdu_dict.get(bus_name)
        for message in pdu_info.keys():
            if pdu_info[message].get("tx_node") in self.dut_ecu:
                pdu_info[message]["rx_flag"] = False

    def rx_flag_reset_all(self):
        # all bus rx_flag update to False   确保 pdu_data 有效性
        for bus_name in self.bus_pdu_dict.keys():
            self.rx_flag_reset_bus(bus_name)

    def get_recent_signal_raw_value(self, msg_signals_obj: type, signal_name: str, pdu_data: list=[]):
        # 立马获取最近收到/发送的报文信号值，不等待，从来没有收到/发送过，返回默认信号值
        signal_name = self.__unified_signal_name(msg_signals_obj, signal_name)
        (
            bus_name,
            pdu_dicts,
            msg_name,
            cls_signal_obj,
            bmuws_info,
            pdudata,
            sig_byteorder,
            update_id_bit,
        ) = self.__get_msg_data(msg_signals_obj, signal_name)

        if pdu_data:
            if isinstance(pdu_data, list):
                pdudata = pdu_data
            else:
                logger.error(f"参数 pdu_data 输入类型 错误，应该为列表；实际输入为 {pdu_data}")

        expected_signal_value = 0  # 随意填0，只是做 __check_msg_data 参数
        (
            result,
            encoded_actual_signal_value,
            expected_signal_value,
        ) = self.__check_msg_data(
            bus_name,
            msg_name,
            bmuws_info,
            sig_byteorder,
            signal_name,
            cls_signal_obj,
            pdudata,
            expected_signal_value,
            do_assert=False,
        )
        # logger.info("{} Received {} recent_signal_raw_value is {}".format(bus_name, msg_name, encoded_actual_signal_value))
        return encoded_actual_signal_value

    def pythoncan_capture_msgdata(self, pdu_info, msgid: list, timeout=5):
        # pythoncan 风格接口
        #: pdu_info   a bus info    such as self.bus_pdu_dict["adcanfd"]
        #: msgid  type:list  列表里可以是 type:str  msg name       type:int   msg id
        i = 0
        msgids = msgid
        while i < timeout:
            for msgid in msgids:
                if isinstance(msgid, str):
                    msg = pdu_info.get(msgid)
                    if msg.get("rx_flag"):
                        return (
                            msg.get("msg_id"),
                            msg.get("time_stamp"),
                            msg.get("msg_length"),
                            msg.get("pdu_data"),
                        )
                elif isinstance(msgid, int):
                    for message in pdu_info.keys():
                        msg = pdu_info.get(message)
                        if msg.get("msg_id") == msgid:
                            if msg.get("rx_flag"):
                                return (
                                    msg.get("msg_id"),
                                    msg.get("time_stamp"),
                                    msg.get("msg_length"),
                                    msg.get("pdu_data"),
                                )
                else:
                    logger.warning(
                        "capture_msgdata parmeter ---- msgid   type is error"
                    )
            i += 0.001
            sleep(0.001)
        return None

    def capture_msgdata(self, pdu_info, msgid: Union[str, int], timeout=5):
        #: pdu_info   a bus info    such as self.bus_pdu_dict["adcanfd"]
        #: msgid   type:str  msg name       type:int   msg id

        is_msg = None
        if isinstance(msgid, str):
            msg = pdu_info.get(msgid)
            if msg:
                is_msg = True
        elif isinstance(msgid, int):
            for message in pdu_info.keys():
                msg = pdu_info.get(message)
                if msg.get("msg_id") == msgid:
                    is_msg = True
                    msgid = message
                    break
        else:
            logger.warning("capture_msgdata parmeter ---- msgid   type is error")

        if is_msg:
            i = 0
            while i < timeout:
                if msg.get("rx_flag"):
                    msg["rx_flag"] = False
                    return (
                        msg.get("msg_id"),
                        msg.get("time_stamp"),
                        msg.get("msg_length"),
                        msg.get("pdu_data"),
                    )
                i += 0.001
                sleep(0.001)

            # if isinstance(msgid, str) and hasattr(self, msgid):
            #     fr_obj = getattr(self, msgid)

            #     i = 0
            #     while i < timeout:
            #         self.fetch_shm(fr_obj, msg, 2)  #  2   main进程更新
            #         if msg.get("rx_flag"):
            #             msg["rx_flag"] = False
            #             return (
            #                 msg.get("msg_id"),
            #                 msg.get("time_stamp"),
            #                 msg.get("msg_length"),
            #                 msg.get("pdu_data"),
            #             )
            #         i += 0.001
            #         sleep(0.001)
            # else:
            #     i = 0
            #     while i < timeout:
            #         if msg.get("rx_flag"):
            #             msg["rx_flag"] = False
            #             return (
            #                 msg.get("msg_id"),
            #                 msg.get("time_stamp"),
            #                 msg.get("msg_length"),
            #                 msg.get("pdu_data"),
            #             )
            #         i += 0.001
            #         sleep(0.001)

        else:
            logger.error("MSG {} 在标准的bus中没有被找到".format(msgid))

        return None

    def time_control_start(self, pdu_info):
        self.time_control_flag = True
        time_thrading = Thread(
            target=self.time_control, name="Time_Control", args=(pdu_info,)
        )
        time_thrading.start()

    def time_control_stop(self):
        self.time_control_flag = False
        sleep(0.1)
        # self.shm_main.close()

    def __unified_signal_name(self, msg_signals_obj, signal_name):
        '''
        对 signal_name  加后缀，有的话就不加      如 DoorPassPosn 会变成 DoorPassPosn_1_BgmConnSignalIPdu12
        如果只是设置ub    就一定要把 _UB 信号填全
        '''
        result = re.search(r"_\d+_", signal_name)

        if result:
            signal_name = signal_name.split("_")[0]
            result = re.search(r"_\d+_", signal_name)

        if not result:
            signals_list = dir(msg_signals_obj)
            for signals in signals_list:
                if not signals.endswith("_UB"):
                    if signal_name in signals:
                        result_sig = re.search(r"_\d+_.+", signals)
                        if result_sig:
                            # logger.info(result_sig.group())
                            signal_name = signal_name + result_sig.group()
                            break
        return signal_name

    def set(
        self,
        msg_signals_obj: type,
        signal_name: str,
        sig_value_name: Union[str, int, float],
        ub_flag=True,
        cycle_time=None,
    ):
        """Set a signal's value to the passed-in new value.

        Parameters
        ----------
        msg_signals_obj : type
            self.dbc.chassis.BCU_04 (= cls_signal_obj for each of this msg's signals)
        signal_name : str
            "DoorAjarFrntLeSts"             (= used to get the cls_signal_obj)
        sig_value_name : Union[str, int]
            "v_Unlocked" or 123
        cycle_time : int   second  需要修改时在赋值

        Returns
        -------
        None
        """
        # logger.debug(f"Set {msg_signals_obj}.{signal_name}={sig_value_name}")
        signal_name = self.__unified_signal_name(msg_signals_obj, signal_name)

        # (
        #     bus_name,
        #     pdu_dicts,
        #     msg_name,
        #     cls_signal_obj,
        #     bmuws_info,
        #     pdudata,
        #     sig_byteorder,
        #     update_id_bit,
        # ) = self.__get_msg_data(msg_signals_obj, signal_name)

        # if bus_name == "backbonefr":  #  fr 报文，读取shm数据
        #     fr_obj = getattr(self, msg_name)
        #     self.fetch_shm(fr_obj, pdu_dicts.get(msg_name), 2)

        pdu_dicts, msg_name = self.__set(
            msg_signals_obj, signal_name, sig_value_name, ub_flag
        )

        # set tx_flag to true
        msg = pdu_dicts.get(msg_name)

        msg["tx_change"] = True
        if cycle_time:
            msg["msg_cycle"] = cycle_time
        if msg.get("tx_flag") is not None:
            msg["tx_flag"] = True    #  可以接触暂停，直接发送

        # if bus_name == "backbonefr":
        #     fr_obj = getattr(self, msg_name)
        #     self.put_shm(fr_obj, msg, 1)  # 1  FR 进程需要更新

        # if msg["tx_flag"] == True:
        #     if cycle_time:  # 情况2 只是更新周期 xx
        #         msg["msg_cycle"] = cycle_time
        #     # 情况1 默认不用处理
        # elif msg["tx_flag"] == False:
        #     # 情况4 立刻进行一次发送,
        #     if cycle_time:  # 情况3 将非周期msg ，变成周期发送
        #         msg["msg_cycle"] = cycle_time
        #     msg["tx_flag"] = True

        # if cycle_time:
        #     # 情况1 只是更新周期 xx
        #     # 情况2 从None set 周期 xx
        #     if msg.get("msg_cycle") is None:
        #         msg["tx_flag"] = True  # 情况2
        #         msg["time_count"] = 0
        #     msg["msg_cycle"] = cycle_time
        # else:
        #     # 情况3 默认不用处理
        #     # 情况4 立刻进行一次发送
        #     if msg.get("time_count") is None:
        #         msg["tx_flag"] = True  # 情况4

    def reset(self, pdu_obj, bus_name: str, msg_id: str):
        """
        bus_name: “bodycan”、“backbonefr”
        msg_id: 字符串，如"0x123"、”12-34-56“
        """
        obj_list = getattr(pdu_obj, str(bus_name), None)
        if obj_list is None:
            logger.info(f"无效的参数{bus_name}")
        else:
            message_name = ""
            message_id = None
            if msg_id.startswith('0x'):
                message_id = int(msg_id, 16)  # message_id 作为16进制字符串的形式转换为整形，默认10进制字符串
                for attr in dir(obj_list):
                    obj1 = getattr(obj_list, attr)
                    if hasattr(obj1, 'msg_id'):
                        obj2 = getattr(obj1, 'msg_id')
                        if int(obj2) == message_id:
                            message_name = attr
            else:
                for attr in dir(obj_list):
                    obj1 = getattr(obj_list, attr)
                    if hasattr(obj1, 'msg_id'):
                        message_id = getattr(obj1, 'msg_id')
                        bytes_list = (
                            [str((int(message_id) >> 16) & 0xFF)]
                            + [str((int(message_id) >> 8) & 0xFF)]
                            + [str(int(message_id) & 0xFF)]
                        )
                        if '-'.join(bytes_list) == msg_id:
                            message_name = attr

            if len(message_name) > 0:
                msg_signals_obj = getattr(obj_list, message_name)
                pdu_dicts = self.bus_pdu_dict.get(bus_name, None)
                msg_name = msg_signals_obj.msg_name
                logger.info(f"获取到的报文名称：{msg_name}")
                if pdu_dicts:
                    pdu_data = pdu_dicts.get(msg_name).get("pdu_data")
                    cycle_time = pdu_dicts.get(msg_name).get("msg_cycle", None)
                    logger.info(f"获取到的pdu_data:{pdu_data}")
                    logger.info(f"获取到的msg_cycle:{cycle_time}")
                    self.send_pdu(bus_name, message_id, pdu_data, cycle_time)
                else:
                    logger.info(f"无效的参数{bus_name}")
            else:
                logger.info(f"{msg_id}不存在")

    def can_bus_check(self, tb_config, pdu_obj):
        """
        基于tb_config 进行总线信号验证
        @param tb_config:
        @param pdu_obj:
        @return: 如果某一个can bus 验证失败，则返回False
        """
        can_list = {}
        for key in tb_config.get('bus'):
            if 'can' in key:
                can_list[key] = tb_config.get('bus').get(key)
        run_result = {}
        for key in can_list:
            run_result[key] = {"result": "fail", "message": "init"}  # 保存检测结果
            cmd = f"ifconfig | grep {can_list.get(key)}"
            result = os.popen(cmd).readlines()
            result = "".join(result).strip()
            logger.info(f"第一步命令{cmd}执行结果：{result}.")
            if 'mtu' in result:
                logger.info(f'第一步、{key} 总线启动命令已执行,{result}')
                if 'fd' in key:
                    if '72' in result:
                        logger.info(f"第二步、{key} 总线启动命令执行正确,{result}")
                        logger.info(f"第三步检查: {can_list.get(key)}")
                        bus_signal_varify(can_list, key, pdu_obj, run_result)
                    else:
                        run_result[key] = {
                            "result": "fail",
                            "message": f"{key} 总线启动命令执行错误,{result}",
                        }
                else:
                    if '16' in result:
                        logger.info(f"第二步、{key} 总线启动命令执行正确,{result}！")
                        logger.info(f"第三步检查.....{can_list.get(key)}")
                        bus_signal_varify(can_list, key, pdu_obj, run_result)
                    else:
                        run_result[key] = {
                            "result": "fail",
                            "message": f"{key} 总线启动命令执行错误,{result}",
                        }
            else:
                run_result[key] = {"result": "fail", "message": f"{key} 总线启动命令未执行"}

        info_json = json.dumps(
            run_result,
            sort_keys=False,
            indent=4,
            separators=(',', ': '),
            ensure_ascii=False,
        )
        logger.info("********************************")
        logger.info(info_json)
        return_code = True
        for key in run_result:
            can_result = run_result[key]
            if can_result["result"] == "pass":
                logger.info(f"{key} 总线检测正常")
            else:
                return_code = False
                logger.info(f"{key} 总线检测异常，异常信息：{can_result['message']}")
        logger.info("********************************")
        return return_code

    def set_multiple_signals(
        self,
        multiple_signals_info: list = [],
        ub_flag=True,
        cycle_time=None,
    ):
        """
        multiple signals 都在一个报文内
        Set a signal's value to the passed-in new value.

        Parameters
        ----------
        multiple_signals_info : int   such as  [(msg_signals_obj: type, signal_name: str, sig_value_name: Union[str, int])]
            msg_signals_obj : type
                self.dbc.chassis.BCU_04 (= cls_signal_obj for each of this msg's signals)
            signal_name : str
                "DoorAjarFrntLeSts"             (= used to get the cls_signal_obj)
            sig_value_name : Union[str, int]
                "v_Unlocked" or 123
            cycle_time : int   second  需要修改时在赋值

        Returns
        -------
        None
        """
        # if multiple_signals_info:
        #     signal_info = multiple_signals_info[0]
        #     msg_signals_obj = signal_info[0]
        #     signal_name = signal_info[1]
        #     sig_value_name = signal_info[2]

        # signal_name = self.__unified_signal_name( msg_signals_obj, signal_name)

        # pdu_dicts, msg_name = self.__set(
        #     msg_signals_obj, signal_name, sig_value_name, ub_flag
        # )

        if multiple_signals_info:
            # signal_info = multiple_signals_info[0]
            # msg_signals_obj = signal_info[0]
            # signal_name = signal_info[1]

            # signal_name = self.__unified_signal_name(msg_signals_obj, signal_name)

            # (
            #     bus_name,
            #     pdu_dicts,
            #     msg_name,
            #     cls_signal_obj,
            #     bmuws_info,
            #     pdudata,
            #     sig_byteorder,
            #     update_id_bit,
            # ) = self.__get_msg_data(msg_signals_obj, signal_name)

            # if bus_name == "backbonefr":  #  fr 报文，读取shm数据
            #     fr_obj = getattr(self, msg_name)
            #     self.fetch_shm(fr_obj, pdu_dicts.get(msg_name), 2)

            for signal_info in multiple_signals_info:
                msg_signals_obj = signal_info[0]
                signal_name = signal_info[1]
                sig_value_name = signal_info[2]

                signal_name = self.__unified_signal_name(msg_signals_obj, signal_name)

                pdu_dicts, msg_name = self.__set(
                    msg_signals_obj, signal_name, sig_value_name, ub_flag
                )

            # set tx_flag to true
            msg = pdu_dicts.get(msg_name)
            msg["tx_change"] = True

            if cycle_time:
                msg["msg_cycle"] = cycle_time
            if msg.get("tx_flag") is not None:
                msg["tx_flag"] = True    #  可以接触暂停，直接发送
            
            # if bus_name == "backbonefr":
            #     fr_obj = getattr(self, msg_name)
            #     self.put_shm(fr_obj, msg, 1)  # 1  FR 进程需要更新

        else:
            logger.error("multiple_signals_info 参数不合规")

    def __set(self, msg_signals_obj, signal_name, sig_value_name, ub_flag):
        (
            bus_name,
            pdu_dicts,
            msg_name,
            cls_signal_obj,
            bmuws_info,
            pdudata,
            sig_byteorder,
            update_id_bit,
        ) = self.__get_msg_data(msg_signals_obj, signal_name)

        self.__set_msg_data(
            bus_name,
            pdu_dicts,
            msg_name,
            cls_signal_obj,
            bmuws_info,
            pdudata,
            signal_name,
            sig_value_name,
            sig_byteorder,
            update_id_bit,
            ub_flag,
            msg_signals_obj,
        )
        return pdu_dicts, msg_name

    def get_sig_group_name(self, msg_signals_obj, signal_name):
        # 当signal_name直接为信号组时也适配
        signal_name = self.__unified_signal_name(msg_signals_obj, signal_name)
        sig_group_dict = getattr(msg_signals_obj, "sig_group_dict")
        for sig_group_name, signal_name_list in sig_group_dict.items():
            if (sig_group_name == signal_name) or (signal_name in signal_name_list):
                return sig_group_name

    def set_crc_count(self, msg_signals_obj, sig_group_name, do_cntr=True, do_crc=True):
        # sig_group_name  信号组名
        (
            is_crc,
            sig_value_length,
            crc_sig,
            cntr_sig,
            cntr_sig_value,
        ) = self.__get_sig_value_length_and_crc(msg_signals_obj, sig_group_name)

        if is_crc:
            if do_cntr != False:
                if cntr_sig_value == 14:
                    cntr_sig_value = 0
                else:
                    cntr_sig_value += 1
                self.__set(msg_signals_obj, cntr_sig, cntr_sig_value, ub_flag=None)

            if do_crc != False:
                data_id_dict = msg_signals_obj.sig_group_dataid_dict
                data_id = data_id_dict[sig_group_name]

                crc_data = get_crc_countdata(data_id, cntr_sig_value, sig_value_length)
                crc_value = crc8(crc_data)
                self.__set(msg_signals_obj, crc_sig, crc_value, ub_flag=None)
    
    def calculate_expected_crc_from_pdu(self, msg_signals_obj, sig_group_name, pdu_data: list=[]):
        # 根据信号组从pdu中自动计算出期望的CRC
        # 如果pdu_data为[]，则将会使用最近 发送/接收/默认 的pdu
        (
            is_crc,
            sig_value_length,
            crc_sig,
            cntr_sig,
            cntr_sig_value,
        ) = self.__get_sig_value_length_and_crc(msg_signals_obj, sig_group_name, pdu_data)
 
        data_id_dict = msg_signals_obj.sig_group_dataid_dict
        data_id = data_id_dict[sig_group_name]

        crc_data = get_crc_countdata(data_id, cntr_sig_value, sig_value_length)
        crc_value = crc8(crc_data)
        return crc_value

    def set_no_crc(self, msg_signals_obj, signal_name):
        signal_name = self.__unified_signal_name(msg_signals_obj, signal_name)
        sig_group_name = self.get_sig_group_name(msg_signals_obj, signal_name)
        self.update_crc_flag(msg_signals_obj, sig_group_name, do_crc=False)
        sig_group_name = self.__unified_signal_name(msg_signals_obj, sig_group_name)

        if "_" in sig_group_name:
            sig_name = sig_group_name.split("_")[0] + "Chks" + "_" + sig_group_name.split("_")[1] + "_" + sig_group_name.split("_")[2]
        else:
            # sig_name = sig_group_name + "Chks" 
            sig_group_dict = getattr(msg_signals_obj, "sig_group_dict")
            sig_group_list = sig_group_dict.get(sig_group_name)
            for sig in sig_group_list:
                if sig.endswith("Chks"):
                    sig_name = sig

        self.set(msg_signals_obj, sig_name, 0xFF)

    def restore_crc(self, msg_signals_obj, signal_name):
        signal_name = self.__unified_signal_name(msg_signals_obj, signal_name)
        sig_group_name = self.get_sig_group_name(msg_signals_obj, signal_name)
        self.update_crc_flag(msg_signals_obj, sig_group_name, do_crc=True)
        sig_group_name = self.__unified_signal_name(msg_signals_obj, sig_group_name)

        if "_" in sig_group_name:
            sig_name = sig_group_name.split("_")[0] + "Chks" + "_" + sig_group_name.split("_")[1] + "_" + sig_group_name.split("_")[2]
        else:
            # sig_name = sig_group_name + "Chks" 
            sig_group_dict = getattr(msg_signals_obj, "sig_group_dict")
            sig_group_list = sig_group_dict.get(sig_group_name)
            for sig in sig_group_list:
                if sig.endswith("Chks"):
                    sig_name = sig

        self.set(msg_signals_obj, sig_name, 0)

    def set_no_cntr(self, msg_signals_obj, signal_name):
        signal_name = self.__unified_signal_name(msg_signals_obj, signal_name)
        sig_group_name = self.get_sig_group_name(msg_signals_obj, signal_name)
        self.update_cntr_flag(msg_signals_obj, sig_group_name, do_cntr=False)
        sig_group_name = self.__unified_signal_name(msg_signals_obj, sig_group_name)

        if "_" in sig_group_name:
            sig_name = sig_group_name.split("_")[0] + "Cntr" + "_" + sig_group_name.split("_")[1] + "_" + sig_group_name.split("_")[2]
        else:
            sig_name = sig_group_name + "Cntr" 
        
        self.set(msg_signals_obj, sig_name, 0xF)

    def restore_cntr(self, msg_signals_obj, signal_name):
        signal_name = self.__unified_signal_name(msg_signals_obj, signal_name)
        sig_group_name = self.get_sig_group_name(msg_signals_obj, signal_name)
        self.update_cntr_flag(msg_signals_obj, sig_group_name, do_cntr=True)
        sig_group_name = self.__unified_signal_name(msg_signals_obj, sig_group_name)

        if "_" in sig_group_name:
            sig_name = sig_group_name.split("_")[0] + "Cntr" + "_" + sig_group_name.split("_")[1] + "_" + sig_group_name.split("_")[2]
        else:
            sig_name = sig_group_name + "Cntr" 

        self.set(msg_signals_obj, sig_name, 0)

    def check_thread_start(
        self,
        msg_signals_obj: type,
        signal_name: str,
        sig_value_name: Union[str, int],
        timeout: Union[float, int] = 5,
        do_assert=False,
        check_time=1,
    ):
        # 同一报文内的多个信号同时检测,请不要用此接口，建议使用 check_multiple_signals_thread_start  接口
        # 因为是线程,这个 do_assert 无效，目前固定是 False
        # 结果都需要通过 check_thread_stop 获取
        check_thrading = Thread(
            target=self.check_thread,
            name="Check_Thread_Control",
            args=(
                msg_signals_obj,
                signal_name,
                sig_value_name,
                timeout,
                False,  # 强行 do_assert 为False
                check_time,
            ),
        )
        check_thrading.start()

    def check_thread_stop(self, signal_name, timeout=30):
        # param signal_name   需要与 check_thread , check_thread_start  保持一致
        # param timeout 最好是check中timeout的2倍及以上
        # return result  [result, encoded_actual_signal_value, expected_signal_value]
        return self.got_check_result(signal_name, timeout=timeout)

    def check_thread(
        self,
        msg_signals_obj: type,
        signal_name: str,
        sig_value_name: Union[str, int],
        timeout: Union[float, int] = 5,
        do_assert=False,
        check_time=1,
    ):
        result, encoded_actual_signal_value, expected_signal_value = self.check(
            msg_signals_obj, signal_name, sig_value_name, timeout, do_assert, check_time
        )
        self.__check_results[signal_name] = [
            result,
            encoded_actual_signal_value,
            expected_signal_value,
        ]

    def check(
        self,
        msg_signals_obj: type,
        signal_name: str,
        sig_value_name: Union[str, int],
        timeout: Union[float, int] = 5,
        do_assert=True,
        check_time=1,
        check_ub=None,
    ) -> Tuple[bool, int, int]:
        """
        检查最近收到的报文
        Check if a signal's current value matches the passed-in expected value.

        Parameters
        ----------
        msg_signals_obj : type
            self.dbc.bodycan.BCM_03            (= cls_signal_obj for each of this msg's signals)
        signal_name : str
            "DoorAjarFrntLeSts"             (= used to get the cls_signal_obj)
        sig_value_name : Union[str, int]
            "v_Unlocked" or 123
        timeout : int
            number of sec. to wait before giving up on reading a msg.
        check_time : int
            检查成功次数
        check_ub :    默认是None 不进行检查ub值, 如果是0,1,则检查ub值是否一直为该值
                    此参数针对需要检查信号的UB位，信号组请直接检查 XXX_UB

        Returns
        -------
        result : bool
            True if check succeeded
        actual_signal_value : int
            numeric value of signal
        expected_signal_value : int
            numeric value of signal
        """
        signal_name = self.__unified_signal_name(msg_signals_obj, signal_name)
        (
            bus_name,
            pdu_dicts,
            msg_name,
            cls_signal_obj,
            bmuws_info,
            pdudata,
            sig_byteorder,
            update_id_bit,
        ) = self.__get_msg_data(msg_signals_obj, signal_name)
        expected_signal_value = self.lookup_new_signal_value_by_name(
            cls_signal_obj, signal_name, sig_value_name
        )

        result = None
        ub_value = None
        left_time = timeout
        start_time = time.time()
        i = 0
        while left_time > 0:
            captured_msgdata = self.capture_msgdata(
                pdu_dicts, msg_name, timeout=timeout
            )

            if captured_msgdata:
                captured_msgdata = captured_msgdata[3]
                (
                    result,
                    encoded_actual_signal_value,
                    expected_signal_value,
                ) = self.__check_msg_data(
                    bus_name,
                    msg_name,
                    bmuws_info,
                    sig_byteorder,
                    signal_name,
                    cls_signal_obj,
                    captured_msgdata,
                    expected_signal_value,
                    do_assert=do_assert,
                )
                if check_ub is not None:
                    # 判断update_id_bit,check_ub 是否为int类型
                    if all(isinstance(var, int) for var in [update_id_bit, check_ub]):
                        ub_value = self.__check_ub_raw(update_id_bit, captured_msgdata)
                        if ub_value != check_ub:
                            result = False
                if result:
                    i += 1
                    if i == check_time:
                        break
                elif i > 0:
                    logger.info("Check 函数获取的值不连续")
                    break

                left_time = timeout + start_time - time.time()
            else:
                encoded_actual_signal_value = None
                left_time = 0
        if do_assert:
            if check_ub is None:
                logger.info(
                    "result {}, realvalue {}, expectedvalue {}; ---- (bus:{} msg:{} sig:{})".format(
                        result,
                        encoded_actual_signal_value,
                        expected_signal_value,
                        bus_name,
                        msg_name,
                        signal_name,
                    )
                )
            else:
                logger.info(
                    "result {}, realvalue {}, expectedvalue {}, real_ub_value {},expected_ub_value {}; ---- (bus:{} msg:{} sig:{})".format(
                        result,
                        encoded_actual_signal_value,
                        expected_signal_value,
                        ub_value,
                        check_ub,
                        bus_name,
                        msg_name,
                        signal_name,
                    )
                )
            assert result
        return result, encoded_actual_signal_value, expected_signal_value
    
    def __check_ub_raw(self, update_id_bit: int, data: list):
        """
        检查给定的位是否在原始数据中设置为1。
        
        Args:
            update_id_bit (int): 需要检查的位的索引。
            data (list): 原始数据列表，每个元素表示一个字节。
        
        Returns:
            int: 如果给定的位设置为1，则返回1；否则返回0。
        
        """
        if isinstance(update_id_bit, int):
            byte_index = update_id_bit // 8
            bit_offset = update_id_bit % 8
            return data[byte_index] >> bit_offset & 1

    def check_multiple_signals(
        self,
        multiple_signals_info: list = [],
        timeout: Union[float, int] = 5,
        do_assert=True,
        check_time=1,
        do_print=False
    ) -> list:
        """
        检查最近收到的报文,multiple signals 都在一个报文内
        Check if multiple signal's current value matches the passed-in expected value.

        Parameters
        ----------
        multiple_signals_info : int   such as  [(msg_signals_obj: type, signal_name: str, sig_value_name: Union[str, int])]
            msg_signals_obj : type
                self.dbc.bodycan.BCM_03            (= cls_signal_obj for each of this msg's signals)
            signal_name : str
                "DoorAjarFrntLeSts"             (= used to get the cls_signal_obj)
            sig_value_name : Union[str, int]
                "v_Unlocked" or 123
        timeout : int
            number of sec. to wait before giving up on reading a msg.

        Returns
        -------
        result_total : bool
        result_info : []    such as    [(result : bool, actual_signal_value : int,expected_signal_value : int)]
            result : bool
                True if check succeeded
            actual_signal_value : int
                numeric value of signal
            expected_signal_value : int
                numeric value of signal
        """
        result_info = []

        if multiple_signals_info:
            signal_info = multiple_signals_info[0]
            msg_signals_obj = signal_info[0]
            signal_name = signal_info[1]
            sig_value_name = signal_info[2]

        signal_name = self.__unified_signal_name(msg_signals_obj, signal_name)
        (
            bus_name,
            pdu_dicts,
            msg_name,
            cls_signal_obj,
            bmuws_info,
            pdudata,
            sig_byteorder,
            update_id_bit,
        ) = self.__get_msg_data(msg_signals_obj, signal_name)
        expected_signal_value = self.lookup_new_signal_value_by_name(
            cls_signal_obj, signal_name, sig_value_name
        )

        pdu_dicts_confirm = pdu_dicts
        msg_name_confirm = msg_name
        result = None
        result_total = None
        left_time = timeout
        start_time = time.time()
        i = 0
        while left_time > 0:
            captured_msgdata = self.capture_msgdata(
                pdu_dicts_confirm, msg_name_confirm, timeout=timeout
            )

            if captured_msgdata:
                captured_msgdata = captured_msgdata[3]
                result_total = True
                result_info = []
                for signal_info in multiple_signals_info:
                    msg_signals_obj = signal_info[0]
                    signal_name = signal_info[1]
                    sig_value_name = signal_info[2]

                    signal_name = self.__unified_signal_name(
                        msg_signals_obj, signal_name
                    )
                    (
                        bus_name,
                        pdu_dicts,
                        msg_name,
                        cls_signal_obj,
                        bmuws_info,
                        pdudata,
                        sig_byteorder,
                        update_id_bit,
                    ) = self.__get_msg_data(msg_signals_obj, signal_name)
                    expected_signal_value = self.lookup_new_signal_value_by_name(
                        cls_signal_obj, signal_name, sig_value_name
                    )

                    (
                        result,
                        encoded_actual_signal_value,
                        expected_signal_value,
                    ) = self.__check_msg_data(
                        bus_name,
                        msg_name,
                        bmuws_info,
                        sig_byteorder,
                        signal_name,
                        cls_signal_obj,
                        captured_msgdata,
                        expected_signal_value,
                        do_assert=do_assert,
                    )

                    result_info.append(
                        (
                            result,
                            encoded_actual_signal_value,
                            expected_signal_value,
                            bus_name,
                            msg_name,
                            signal_name,
                        )
                    )
                    if do_assert or do_print:
                        logger.info(
                            "result {}, realvalue {}, expectedvalue {}; ---- (bus:{} msg:{} sig:{})".format(
                                result,
                                encoded_actual_signal_value,
                                expected_signal_value,
                                bus_name,
                                msg_name,
                                signal_name,
                            )
                        )

                    if not result:
                        result_total = False
                        break

                if result_total:
                    i += 1
                    logger.info(f'i--->{i}')
                    if i == check_time:
                        break
                    continue
                else:
                    left_time = timeout + start_time - time.time()
            else:
                encoded_actual_signal_value = None
                left_time = 0
        if do_assert:
            assert result_total
        self.__check_results[msg_name] = result_total
        return result_total, result_info

    def check_multiple_signals_thread_start(
        self,
        multiple_signals_info: list = [],
        timeout: Union[float, int] = 5,
        do_assert=False,
        check_time=1,
        do_print=False
    ):
        """
        do_assert 在线程中目前固定死为 False
        结果都需要通过 check_thread_stop 获取
        为了保持环境干净，防止上次结果干扰，请提前调用  self.reset_check_results()
        """
        check_multiple_signals_thrading = Thread(
            target=self.check_multiple_signals,
            name="check_multiple_signals",
            args=(
                multiple_signals_info,
                timeout,
                False,
                check_time,
                do_print
            ),
            daemon=True,
        )
        check_multiple_signals_thrading.start()

    def check_multiple_signals_thread_stop(self, message_name, timeout=30):
        '''
        :param message_name  报文名
        :param timeout 最好是check中timeout的2倍及以上
        :return result  type:bool
        '''
        return self.got_check_result(message_name, timeout=timeout)
    
    def get_crcinfo_from_ecu(self, bus_name: str, ecu_name: str):
        """
        获取指定ECU中所有消息的CRC信号组信息。

        Args:
            bus_name (str): 总线名称，例如'BodyCan'。
            ecu_name (str): ECU名称，例如 'CCM'。

        Returns:
            list: 包含所有消息的CRC信号组信息的列表，每个元素为一个元组，元组的第一个元素为消息名称，第二个元素为该消息所有信号组。

        """
        # 初始化一个空列表，用于存储CRC信号组信息
        crcinfo = []

        # 从指定ECU中获取发送消息列表
        txmsg_list = self.get_txmsg_list_from_ecu(bus_name, ecu_name)

        # 获取总线对象
        bus_obj = getattr(self, bus_name)

        # 遍历发送消息列表
        for txmsg in txmsg_list:
            # 获取消息对象
            msg_obj = getattr(bus_obj, txmsg)

            # 判断消息对象是否具有sig_group_dataid_dict属性
            if getattr(msg_obj, "sig_group_dataid_dict", None):
                # 如果具有sig_group_dataid_dict属性，则将消息名称和信号组信息添加到crcinfo列表中
                crcinfo.append((txmsg, msg_obj.sig_group_dataid_dict.keys()))

        return crcinfo              

    def get_txmsg_list_from_ecu(self, bus_name: str, ecu_name: str):
        """
        从总线中获取指定ECU发送消息列表

        Args:
            bus_name (str): 总线名称
            ecu_name (str): ECU名称

        Returns:
            list: 发送消息列表

        """
        # 初始化一个空列表，用于存储发送消息的名称
        msg_list = []

        # 从总线消息字典中获取指定总线的消息列表
        pdu_dict = self.bus_pdu_dict.get(bus_name)

        # 遍历消息列表
        for msg_name in pdu_dict:
            # 如果消息的发送节点是目标ECU
            if pdu_dict[msg_name].get("tx_node") == ecu_name:
                # 将消息名称添加到发送消息列表中
                msg_list.append(msg_name)

        return msg_list

    def check_crc_from_pdu(self, msg_signals_obj, signal_name: str, pdu_data: list, do_assert: bool=True):
        """
        根据pdu自动算出对应的crc，然后再pdu里的对应的crc进行比较

        :param msg_signals_obj : type
            self.dbc.bodycan.BCM_03            (= cls_signal_obj for each of this msg's signals)
        :param signal_name : str         信号或信号组都适配
            "DoorAjarFrntLeSts"             (= used to get the cls_signal_obj)
        :param pdu_data : list   需要check的pdu data
        :param do_assert : bool   是否直接进行assert判断
        :returns:   
            result : bool
                True if check succeeded
            actual_crc : int
                numeric value of signal
            expected_crc : int
                numeric value of signal

        """

        signal_name = self.__unified_signal_name(msg_signals_obj, signal_name)
        sig_group_name = self.get_sig_group_name(msg_signals_obj, signal_name)

        # 获取crc Chks 信号名
        if "_" in sig_group_name:
            sig_name = sig_group_name.split("_")[0] + "Chks" + "_" + sig_group_name.split("_")[1] + "_" + sig_group_name.split("_")[2]
        else:
            # sig_name = sig_group_name + "Chks" 
            sig_group_dict = getattr(msg_signals_obj, "sig_group_dict")
            sig_group_list = sig_group_dict.get(sig_group_name)
            for sig in sig_group_list:
                if sig.endswith("Chks"):
                    sig_name = sig

        # 获取期望的crc值
        crc_value = self.calculate_expected_crc_from_pdu(msg_signals_obj, sig_group_name, pdu_data)
        result, actual_crc, expected_crc = self.check_sig_from_pdu(msg_signals_obj, sig_name, crc_value, pdu_data, do_assert)
        return result, actual_crc, expected_crc

    def check_signal(
        self,
        msg_signals_obj: type,
        signal_name: str,
        timeout: Union[float, int] = 5,
        do_print=False,
    ) -> list:
        """
        在超时时间内检查最近收到的报文对应信号的值和对应时间戳 list

        Parameters
        ----------
        msg_signals_obj : type
            self.dbc.bodycan.BCM_03            (= cls_signal_obj for each of this msg's signals)
        signal_name : str
            "DoorAjarFrntLeSts"             (= used to get the cls_signal_obj)
        timeout : Union[float, int]
            获取信号的超时时间
            number of sec. to wait before giving up on reading a msg.
        do_print : bool
            是否打印每次获取的信号值

        Returns
        -------
        (encoded_actual_signal_value, timestamp) list : list 如 [(0,1683706326.0662186), (2, 1683706326.089834)]
        """
        signal_name_raw = signal_name
        signal_name = self.__unified_signal_name(msg_signals_obj, signal_name)
        (
            bus_name,
            pdu_dicts,
            msg_name,
            cls_signal_obj,
            bmuws_info,
            pdudata,
            sig_byteorder,
            update_id_bit,
        ) = self.__get_msg_data(msg_signals_obj, signal_name)
        expected_signal_value = 0  #  默认0，后面不做判断

        left_time = timeout
        start_time = time.time()
        encoded_actual_signal_value_timestamp_list = []
        while left_time > 0:
            captured_msgdata = self.capture_msgdata(
                pdu_dicts, msg_name, timeout=left_time
            )
            if captured_msgdata:
                msgdata = captured_msgdata[3]
                timestamp = captured_msgdata[1]
                (
                    result,
                    encoded_actual_signal_value,
                    expected_signal_value,
                ) = self.__check_msg_data(
                    bus_name,
                    msg_name,
                    bmuws_info,
                    sig_byteorder,
                    signal_name,
                    cls_signal_obj,
                    msgdata,
                    expected_signal_value,
                )

                if do_print:
                    logger.info(
                        "(timestamp: {:<7f}) (bus:{} msg:{} sig:{}) ---- get realvalue is {}".format(
                            timestamp,
                            bus_name,
                            msg_name,
                            signal_name,
                            encoded_actual_signal_value,
                        )
                    )

                encoded_actual_signal_value_timestamp_list.append(
                    (encoded_actual_signal_value, timestamp)
                )

                left_time = timeout + start_time - time.time()
            else:
                encoded_actual_signal_value = None
                left_time = 0
        self.__check_results[
            signal_name_raw
        ] = encoded_actual_signal_value_timestamp_list
        return encoded_actual_signal_value_timestamp_list

    def check_signal_thread_start(
        self,
        msg_signals_obj: type,
        signal_name: str,
        timeout: Union[float, int] = 5,
        do_print=False,
    ):
        check_signal_thrading = Thread(
            target=self.check_signal,
            name="check_signal",
            args=(
                msg_signals_obj,
                signal_name,
                timeout,
                do_print,
            ),
            daemon=True,
        )
        check_signal_thrading.start()

    def check_signal_thread_stop(self, signal_name, timeout=30):
        '''
        :param signal_name   需要与 check_signal_thread_start  保持一致
        :param timeout 最好是check中timeout的2倍及以上
        :return result  (encoded_actual_signal_value, timestamp) list : list 如 [(0,1683706326.0662186), (2, 1683706326.089834)]
        '''
        result_list = self.got_check_result(signal_name, timeout=timeout)
        delete_count = 0
        delete_list = []
        delete_flag = False
        for i in range(len(result_list)-1, -1, -1):
            if result_list[i][0] is None and delete_flag is False:
                delete_list.append(result_list[i])
                result_list.pop(i)
                delete_count += 1
                delete_flag = True
            else:
                delete_flag = False
        else:
            logger.info(f"从监控结果中删除元素个数为{delete_count}，具体为{delete_list}")

        return result_list

    def check_event(
        self,
        msg_signals_obj: type,
        signal_name: str,
        base_sig_value_name: Union[str, int],
        target_sig_value_name: Union[str, int],
        timeout: Union[float, int] = 5,
        do_print=False,
    ) -> int:
        """
        检查事件 如 在超时时间内 信号 A 值 变化 到 B 值, 发生了多少次

        Parameters
        ----------
        msg_signals_obj : type
            self.dbc.bodycan.BCM_03            (= cls_signal_obj for each of this msg's signals)
        signal_name : str
            "DoorAjarFrntLeSts"             (= used to get the cls_signal_obj)
        base_sig_value_name : Union[str, int]
            "v_Unlocked" or 123
        target_sig_value_name : Union[str, int]
            "v_locked" or 1234
        timeout : Union[float, int]
            获取信号的超时时间
            number of sec. to wait before giving up on reading a msg.
        do_print : bool
            是否打印每次获取的信号值

        Returns
        -------
        event_time : int  没有期望事件发生, 返回次数为 0
            事件发生次数
        """
        signal_name_origin = signal_name
        signal_name = self.__unified_signal_name(msg_signals_obj, signal_name)
        encoded_actual_signal_value_timestamp_list = self.check_signal(
            msg_signals_obj, signal_name, timeout, do_print
        )
        if encoded_actual_signal_value_timestamp_list:
            encoded_actual_signal_value_list = [
                encoded_actual_signal_value_timestamp[0]
                for encoded_actual_signal_value_timestamp in encoded_actual_signal_value_timestamp_list
            ]
        else:
            logger.error("没有获取到 encoded_actual_signal_value_timestamp_list")
            encoded_actual_signal_value_timestamp_list = []

        (
            bus_name,
            pdu_dicts,
            msg_name,
            cls_signal_obj,
            bmuws_info,
            pdudata,
            sig_byteorder,
            update_id_bit,
        ) = self.__get_msg_data(msg_signals_obj, signal_name)

        base_sig_value_name = self.lookup_new_signal_value_by_name(
            cls_signal_obj, signal_name, base_sig_value_name
        )
        target_sig_value_name = self.lookup_new_signal_value_by_name(
            cls_signal_obj, signal_name, target_sig_value_name
        )

        event_time = 0
        i = 0
        logger.info(
            "encoded_actual_signal_value_list {}".format(
                encoded_actual_signal_value_list
            )
        )

        for encoded_actual_signal_value in encoded_actual_signal_value_list:
            if encoded_actual_signal_value == base_sig_value_name:
                i = 1
            elif encoded_actual_signal_value == target_sig_value_name:
                if i == 1:
                    event_time += 1
                i = 0
        self.__check_event_results[signal_name_origin] = event_time
        return event_time

    def __check_msg_data(
        self,
        bus_name,
        msg_name,
        bmuws_info,
        sig_byteorder,
        signal_name,
        cls_signal_obj,
        captured_msgdata,
        expected_signal_value,
        do_assert=True,
    ):
        result = None
        encoded_actual_signal_value = None
        try:
            if bmuws_info is None:
                # Single-byte signal.
                encoded_actual_signal_value = (
                    captured_msgdata[cls_signal_obj.byte] & cls_signal_obj.mask
                ) >> cls_signal_obj.shift
            else:
                # Multi-byte or straddling-two-bytes signal.
                encoded_actual_signal_value = 0

                # First the encoded_actual_signal_value's LSbyte receives the signal's LSbyte.
                # Then the encoded_actual_signal_value is left-shifted, to prepare for next receiving the signals's LSbyte.
                #
                if sig_byteorder.lower() == "motorola":
                    pass
                elif sig_byteorder.lower() == "intel":
                    bmuws_info = reversed(bmuws_info)
                else:
                    logger.warning("sig_byteorder    is   error")

                for byte, mask, unmask, width, shift in bmuws_info:
                    # In the new_signal_value, keep only this signal_byte's bits,
                    # and shift to them to the correct bit position in the msg.
                    signal_byte_val = (captured_msgdata[byte] & mask) >> shift

                    shifted_actual_signal_value = encoded_actual_signal_value << width

                    encoded_actual_signal_value = (
                        shifted_actual_signal_value + signal_byte_val
                    )
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/i_signal_i_pdu_jet20.py")
            logger.error(e)
        result = encoded_actual_signal_value == expected_signal_value

        # logger.info("result {}, realvalue {}, expectedvalue {}; ---- (bus:{} msg:{})".format(result, encoded_actual_signal_value, expected_signal_value, bus_name, msg_name))

        return result, encoded_actual_signal_value, expected_signal_value

    def __get_msg_data(self, msg_signals_obj: type, signal_name: str):
        fully_qualified_module_name = msg_signals_obj.__module__
        bus_name = fully_qualified_module_name.split(".")[-1]  # "body"

        pdu_dicts = self.bus_pdu_dict.get(bus_name)
        msg_name = msg_signals_obj.msg_name
        pdudata = pdu_dicts.get(msg_name).get("pdu_data")

        with error_check(StatusCode.IPDU_DATABASE_ERR, exception_error.IpduError):
            cls_signal_obj = getattr(msg_signals_obj, signal_name)
        # try:
        #     cls_signal_obj = getattr(msg_signals_obj, signal_name)
        # except Exception as e:
        #     logger.info(
        #         f"输入的 msg_signals_obj is {msg_signals_obj}, signal_name is {signal_name}"
        #     )
        #     logger.error(
        #         f"获取 signal_obj 类 失败, attributes in msg_signals_obj is:  {[v for v in msg_signals_obj.__dict__ if not v.startswith('_')]}"
        #     )
        #     raise e

        sig_byteorder = cls_signal_obj.sig_byteorder
        update_id_bit = cls_signal_obj.update_id_bit

        # bmuws == Byte, Mask, Unmask, Width, Shift.
        bmuws_info = getattr(cls_signal_obj, "bmuws_info", None)

        # Returns bmuws_info = None for signals with no bmuws_info data member.
        # use signal_obj.msg_id to fetch msg data

        return (
            bus_name,
            pdu_dicts,
            msg_name,
            cls_signal_obj,
            bmuws_info,
            pdudata,
            sig_byteorder,
            update_id_bit,
        )

    def __set_ub(
        self,
        pdu_dicts,
        msg_name,
        pdudata,
        update_id_bit,
        msg_signals_obj,
        signal_name,
        ub_flag=True,
    ):
        if ub_flag is None:
            return None
        if hasattr(msg_signals_obj, "sig_group_dict"):
            signal_groups = msg_signals_obj.sig_group_dict
            if signal_groups:
                for signal_group in signal_groups:
                    if signal_name in signal_groups[signal_group]:
                        update_id_bit = signal_group
                        break

        if isinstance(update_id_bit, int):
            byte = update_id_bit // 8
            position_in_byte = update_id_bit % 8
            shift = position_in_byte
            if ub_flag:
                pdudata[byte] |= 1 << shift
            else:
                unmask = (1 << shift) ^ 0xFF
                pdudata[byte] &= unmask
            # pdu_dicts[msg_name]["pdu_data"] = pdudata
        elif isinstance(update_id_bit, str):
            signal_ub_name = update_id_bit + "_UB"
            if hasattr(msg_signals_obj, signal_ub_name):
                (
                    bus_name,
                    pdu_dicts,
                    msg_name,
                    cls_signal_obj,
                    bmuws_info,
                    pdudata,
                    sig_byteorder,
                    update_id_bit,
                ) = self.__get_msg_data(msg_signals_obj, signal_ub_name)

                byte = update_id_bit // 8
                position_in_byte = update_id_bit % 8
                shift = position_in_byte
                if ub_flag:
                    pdudata[byte] |= 1 << shift
                else:
                    unmask = (1 << shift) ^ 0xFF
                    pdudata[byte] &= unmask

    def __set_msg_data(
        self,
        bus_name,
        pdu_dicts,
        msg_name,
        cls_signal_obj,
        bmuws_info,
        pdudata,
        signal_name,
        sig_value_name,
        sig_byteorder,
        update_id_bit,
        ub_flag,
        msg_signals_obj,
    ):
        self.__set_ub(
            pdu_dicts,
            msg_name,
            pdudata,
            update_id_bit,
            msg_signals_obj,
            signal_name,
            ub_flag=ub_flag,
        )

        new_signal_value = self.lookup_new_signal_value_by_name(
            cls_signal_obj, signal_name, sig_value_name
        )

        if bmuws_info is None:
            # All of this signal's bits are in a single-byte.
            pdudata[cls_signal_obj.byte] &= cls_signal_obj.unmask
            pdudata[cls_signal_obj.byte] |= new_signal_value << cls_signal_obj.shift
        else:
            # Multi-byte or straddling-two-bytes signal.

            # First the actual_signal_value's LSbyte is copied into the signal's LSbyte.
            # Then the actual_signal_value is right-shifted, to prepare for copying its MSbyte.
            #
            if sig_byteorder.lower() == "motorola":
                bmuws_info = reversed(bmuws_info)
            elif sig_byteorder.lower() == "intel":
                pass
            else:
                print("sig_byteorder    is   error")

            # The new_signal_value's LSbyte goes into the signal's first byte, and next into the signal's last byte.
            """
            The problem is that the shift must be applied to 'new_signal_value' before the mask (otherwise the bits 
            ignored by the mask will be ignored). 
            And, the 'new_signal_value' should be only shifted by the amount of bits actually encoded. 
            """
            for byte, mask, unmask, width, shift in bmuws_info:
                # Clean out the signal's existing content.
                pdudata[byte] &= unmask

                # In the new_signal_value, keep only this signal_byte's bits,
                # and shift to them to the correct bit position in the msg.
                pdudata[byte] |= (new_signal_value << shift) & mask

                # Throw away the LSbyte, so we pcan process the MSbyte next.
                new_signal_value >>= 8 - shift
        # logger.info("Bus({} Message({}) signal_name({})  set signal rawvalue to {}   set pdudata to {}".format(bus_name, msg_name, signal_name, new_signal_value, pdudata))
        # pdu_dicts[msg_name]["pdu_data"] = pdudata
        # logger.info(pdu_dicts[msg_name]["pdu_data"])

    def lookup_new_signal_value_by_name(
        self, cls_signal_obj, signal_name, sig_value_name
    ):
        # 负数返回 补码
        if isinstance(sig_value_name, str):
            if getattr(cls_signal_obj, "sig_value_table"):
                new_signal_value = getattr(cls_signal_obj, "sig_value_table").get(
                    sig_value_name
                )
                if new_signal_value is None:
                    new_signal_value = (
                        0  # sig_value_init is "0x0" ,   Temporary treatment scheme
                    )
            else:
                new_signal_value = (
                    0  # sig_value_init has issue ,   Temporary treatment scheme
                )
        elif isinstance(sig_value_name, int):
            if sig_value_name < 0:
                length = getattr(cls_signal_obj, "length")
                inverse_code = abs(sig_value_name) ^ ((1 << (length - 1)) - 1) + (
                    1 << (length - 1)
                )
                new_signal_value = inverse_code + 1  # 负数返回 补码
            else:
                new_signal_value = sig_value_name
        elif isinstance(sig_value_name, float):
            factor = getattr(cls_signal_obj, "sig_value_factor")
            offset = getattr(cls_signal_obj, "sig_value_offset")
            new_signal_value = (sig_value_name - offset) / factor

            #  四舍五入
            if new_signal_value >= 0:
                new_signal_value = int(new_signal_value + 0.5)
            else:
                new_signal_value = int(new_signal_value - 0.5)
        else:
            logger.error(
                "\nWrong signal value type: {n}:{v}".format(
                    n=signal_name, v=sig_value_name
                )
            )
            return
        sig_value_min = getattr(cls_signal_obj, "sig_value_min")
        if (sig_value_min is not None) and sig_value_min < 0:
            length = getattr(cls_signal_obj, "length")
            if new_signal_value < 0:
                inverse_code = abs(new_signal_value) ^ ((1 << (length - 1)) - 1) + (
                    1 << (length - 1)
                )
                new_signal_value = inverse_code + 1  # 负数返回 补码
        return new_signal_value

    def __get_sig_value_length_and_crc(self, msg_signals_obj, sig_group_name, pdu_data: list=[]):
        # sig_group_name 信号组名
        # return is_crc  bool   是否需要做 e2e 校验 (做e2e校验的信号肯定在一个信号组)
        # return sig_value_length  type:list   such as   [(20,7), (311,10)]
        is_crc = None
        sig_value_length = []
        crc_sig = None
        cntr_sig = None
        cntr_sig_value = None
        signal_groups = msg_signals_obj.sig_group_dict
        crc_signal_groups = msg_signals_obj.sig_group_dataid_dict
        if crc_signal_groups:  # crc sig group (dataid)
            for signal_group_name in crc_signal_groups:
                if sig_group_name == signal_group_name:
                    is_crc = True
                    signal_group_list = signal_groups[signal_group_name]
                    # if (sig_group_name == signal_group_name) or (sig_group_name in signal_group_list):
                    #     for signal_name in signal_group_list:

                    for (
                        signal_name
                    ) in signal_group_list:  # signal_name     signal_group_list里的信号
                        signal_name_short = signal_name.split("_")[0]
                        if signal_name_short.endswith(("CRC", "Chks")):
                            crc_sig = signal_name
                        elif signal_name_short.endswith("Cntr"):
                            cntr_sig = signal_name
                            cntr_sig_value = self.get_recent_signal_raw_value(
                                msg_signals_obj, signal_name, pdu_data
                            )
                        else:
                            signal_value = self.get_recent_signal_raw_value(
                                msg_signals_obj, signal_name, pdu_data
                            )
                            cls_signal_obj = getattr(msg_signals_obj, signal_name)
                            signal_length = cls_signal_obj.sig_length
                            sig_value_length.append((signal_value, signal_length))
        return is_crc, sig_value_length, crc_sig, cntr_sig, cntr_sig_value

    def update_crc_flag(self, msg_signals_obj, sig_group, do_crc=True):
        setattr(msg_signals_obj, (sig_group + "_crc"), do_crc)

    def update_cntr_flag(self, msg_signals_obj, sig_group, do_cntr=True):
        setattr(msg_signals_obj, (sig_group + "_cntr"), do_cntr)

    def lin1_wakeup(self, **kwargs):
        '''
        唤醒 lin 1  用车速唤醒，  维持原来的状态

        要防止 fr 休眠，要先发送can 报文维持
        @param kwargs:
        @return:
        '''

        #   发送 can 0x503   0x03, 0x40,0xff,0xff,0xff,0xff,0xff  维持fr 信号 不休
        can_channel = kwargs.get("can_channel", "bodycan")
        can_id = kwargs.get("can_id", 0x503)
        can_msg = kwargs.get("can_msg", [0x03, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
        cycle_time = kwargs.get("cycle_time", 2)
        # 维持 fr 信号
        self.send_pdu(can_channel, can_id, can_msg, cycle_time=cycle_time)
        #  设置车速
        self.set_vehspd(7.0)
        logger.info(f"通过设置车速为 7 来唤醒lin1 不改变当前模式")

    def lin1_reset_wakeup(self, **kwargs):
        '''
        恢复 lin1 唤醒
        @param kwargs:
        @return:
        '''
        can_channel = kwargs.get("can_channel", "bodycan")
        can_id = kwargs.get("can_id", 0x503)
        #  恢复车速，防止影响别的
        self.set_vehspd(0.0)
        logger.info(f"恢复车速为0")
        #  收尾 停止发送 can 信号
        self.stop_send_pdu(can_channel, can_id)

    def lin2_wakeup(self, **kwargs):
        '''
        非0 一直唤醒
        在 usagemode=0 唤醒 lin 2  仿真发送FR::VDDM::VDDMBackBoneSignalIPdu29::DCChrgnHndlSts=2
        要防止 fr 休眠，要先发送can 报文维持

        sig_value_table = {'OnBdChrgrHndlSts_Disconnected': 0,
        'OnBdChrgrHndlSts_ConnectedWithoutPower': 1,
         'OnBdChrgrHndlSts_PowerAvailableButNotActivated': 2,
         'OnBdChrgrHndlSts_ConnectedWithPower': 3,
         'OnBdChrgrHndlSts_Init': 4, 'OnBdChrgrHndlSts_Fault': 5}

        @param kwargs:
        @return:
        '''
        import threading

        #   发送 can 0x503   0x03, 0x40,0xff,0xff,0xff,0xff,0xff  维持fr 信号 不休
        can_channel = kwargs.get("can_channel", "bodycan")
        can_id = kwargs.get("can_id", 0x503)
        can_msg = kwargs.get("can_msg", [0x03, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
        cycle_time = kwargs.get("cycle_time", 2)
        # 维持 fr 信号
        self.send_pdu(can_channel, can_id, can_msg, cycle_time=cycle_time)
        #  需要来回变化
        t = threading.Thread(target=self.__change_dcchrgnhndlsts)
        self.__send_dcchrgnhndlsts_flag = True
        t.setDaemon(True)
        t.start()
        logger.info(f"通过设置DCChrgnHndlSts 变化 来唤醒lin2 不改变当前模式")

    def __change_dcchrgnhndlsts(self, delay_time=2):
        '''
        设置为 0 只能唤醒 15秒 需要不断变化才可以维持唤醒
        @param delay_time:
        @return:
        '''

        while self.__send_dcchrgnhndlsts_flag:
            self.backbonefr_vddmbackbonefr29_dcchrgnhndlsts_onbdchrgrhndlsts_poweravailablebutnotactivated()
            time.sleep(delay_time)
            self.backbonefr_vddmbackbonefr29_dcchrgnhndlsts_onbdchrgrhndlsts_disconnected()

        self.backbonefr_vddmbackbonefr29_dcchrgnhndlsts_onbdchrgrhndlsts_disconnected()

    def lin2_reset_wakeup(self, **kwargs):
        '''

        @param kwargs:
        @return:
        '''
        can_channel = kwargs.get("can_channel", "bodycan")
        can_id = kwargs.get("can_id", 0x503)
        # 停止发送
        self.__send_dcchrgnhndlsts_flag = False
        #  收尾 停止发送 can 信号
        self.stop_send_pdu(can_channel, can_id)

    def lin3_wakeup(self, partner, dk, **kwargs):
        '''
        长时间唤醒 切模式
        partner = S2sBaseClass([("VehicleModeService", "client")])
        dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        @param kwargs:
        @return:
        '''
        self.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        dk.reset_bncm_digital_keyinfo()
        dk.set_internal_has_key()
        dk.set_cenlock_sts(3)
        dk.set_cenlock_sts(1)
        time.sleep(1)
        partner.send_method_request(
            'VehicleModeService_client',
            "SetUsageModeUp",
            {"mode": 1},
        )
        logger.info(f"通过设置 切换模式来唤醒lin3 ,改变当前模式")
        time.sleep(1)

    def lin3_reset_wakeup(self, partner, dk, **kwargs):
        '''
        partner = S2sBaseClass([("VehicleModeService", "client")])
        dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        @param partner:
        @param dk:
        @param kwargs:
        @return:
        '''
        try:
            dk.stop_listen_dk_bgm_response()
            partner.stop_operators()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/i_signal_i_pdu_jet20.py")
            logger.error(f"关闭 partner, dk异常{str(e)}")

    def lin4_wakeup(self, **kwargs):
        '''
        唤醒 lin 1  用车速唤醒，  维持原来的状态

        要防止 fr 休眠，要先发送can 报文维持
        @param kwargs:
        @return:
        '''
        #   发送 can 0x503   0x03, 0x40,0xff,0xff,0xff,0xff,0xff  维持fr 信号 不休
        can_channel = kwargs.get("can_channel", "bodycan")
        can_id = kwargs.get("can_id", 0x503)
        can_msg = kwargs.get("can_msg", [0x03, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
        cycle_time = kwargs.get("cycle_time", 2)
        # 维持 fr 信号
        self.send_pdu(can_channel, can_id, can_msg, cycle_time=cycle_time)
        #  设置车速
        self.set_vehspd(7.0)
        logger.info(f"通过设置车速为 7 来唤醒lin4 不改变当前模式")

    def lin4_reset_wakeup(self, **kwargs):
        '''
        恢复 lin1 唤醒
        @param kwargs:
        @return:
        '''
        can_channel = kwargs.get("can_channel", "bodycan")
        can_id = kwargs.get("can_id", 0x503)
        #  恢复车速，防止影响别的
        self.set_vehspd(0)
        logger.info(f"恢复车速为0")
        #  收尾 停止发送 can 信号
        self.stop_send_pdu(can_channel, can_id)

    def lin5_wakeup(self, **kwargs):
        '''
        长时间唤醒
        @param kwargs:
        @return:
        '''

    def lin5_reset_wakeup(self, **kwargs):
        pass

    def lin6_wakeup(self, **kwargs):
        '''
        长时间唤醒
        @param kwargs:
        @return:
        '''
        logger.info(f"通过设置cem_lin6.CemCem_Lin6Fr02, BattSnsrStReq, 1  唤醒lin6  不改变模式")
        self.set(self.cem_lin6.CemCem_Lin6Fr02, "BattSnsrStReq", 1)

    def lin6_reset_wakeup(self, **kwargs):
        self.set(self.cem_lin6.CemCem_Lin6Fr02, "BattSnsrStReq", 0)

    def lin_wakeup(self, partner, dk, **kwargs):
        '''
        partner = S2sBaseClass([("VehicleModeService", "client")])
        dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)

        唤醒所有lin 通道
        lin1       车速唤醒  或者 driving
        lin2 非0 一直唤醒  driving  或者 在0 下 1、仿真发送FR::VDDM::VDDMBackBoneSignalIPdu29::DCChrgnHndlSts=2
        lin3 非0 一直唤醒  driving 或者  必须切模式
        lin4 非0 一直唤醒  driving  或者 车速唤醒  driving
        lin5
        lin6 非0 一直唤醒  driving 或者 仿真低压LVEEM signal BattSnsrStsReq == 1

        设置车速 和 切换模式 会唤醒所有通道
        @return:
        '''
        self.lin1_wakeup()
        self.lin3_wakeup(partner, dk)
        logger.info("通过设置车速和切换模式 唤醒所有lin")

    def lin_reset_wakeup(self, partner, dk, **kwargs):
        '''
        partner = S2sBaseClass([("VehicleModeService", "client")])
        dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        复位所有lin 通道
        @return:
        '''
        self.lin1_reset_wakeup()
        self.lin3_reset_wakeup(partner, dk)
    
    def _pnc_set_quick_frame(self, bus_name: str, msg_id: int, data: list):
        for _ in range(20):
            self.send_pdu(bus_name, msg_id, data)
            time.sleep(0.02)

    def set_PNC(self, bus_name: str, msg_id: int, pnc_name_list: List[str], pin_value: int = 0, frame_type: int = 1):
        """
        设置PNC的值
        :param bus_name: 总线名
        :param msg_id: 消息id
        :param pnc_name_list: PNC名称,传入一个列表,支持设置多个PNC节点
        :param pin_value: pin值 默认为0
        :param frame_type: 0表示快帧 1表示慢帧 默认为慢帧
        :return: 
        """
        if isinstance(pnc_name_list, list):
            err_msg = 'signal_name_list必须为一个列表'
            logger.error(err_msg)
            raise exception_error.IpduError(err_msg)
        data = bytearray(8)
        data = list(data)
        # 报文id
        data[0] = int(hex(msg_id)[2:])
        # PIN
        if pin_value == 0:
            data[1] = 0x40
        if pin_value == 1:
            data[1] = 0x50
        else:
            data[1] = 0x40
        for signal_name in pnc_name_list:
            if 'PNC' in signal_name:
                try:
                    pnc_id = int(re.findall(r'PNC(\d+)_', signal_name)[0])
                except (IndexError, TypeError):
                    err_msg= f"{signal_name}不存在PNC ID"
                    logger.error(err_msg)
                    raise exception_error.IpduError(err_msg)
            else:
                data[pnc_id // 8 - 1] |= (1 << pnc_id % 8)
            logger.info(f"set PNC signal_name:{signal_name}置位")
        logger.info(f'raw data: {data}')
        # 20帧快帧
        if frame_type == 0:
            t = Thread(target=self._pnc_set_quick_frame, args=(bus_name, msg_id, data), name='pnc_set_quick_frame')
            t.setDaemon(True)
            t.start()
        # 1s一个周期的普通帧
        if frame_type == 1:
            cycle_time = 1
            self.send_pdu(bus_name, msg_id, data, cycle_time)
    
    def check_PNC_thread(self, bus_name: str, msg_id: int, signal_name: str, signal_value: int, timeout: Union[int, float], check_time: int=1):
        self.__check_results[(bus_name, msg_id, signal_name)] = self.check_PNC(bus_name, msg_id, signal_name, signal_value, timeout, check_time)

    def check_PNC_thread_stop(self, bus_name: str, msg_id: int, signal_name: str, timeout: Union[int, float]=30):
        time.sleep(timeout)
        return self.__check_results.get((bus_name, msg_id, signal_name), (False, None))

    def check_PNC_thread_start(self, bus_name: str, msg_id: int, signal_name: str, signal_value: int, timeout: Union[int, float], check_time: int=1):
        check_thrading = Thread(
            target=self.check_PNC_thread,
            name="Check_PNC_Thread",
            args=(
                bus_name,
                msg_id,
                signal_name,
                signal_value,
                timeout,
                check_time,
            ),
        )
        check_thrading.start()

    def check_PNC(self, bus_name: str, msg_id: int, signal_name: str, signal_value: int, timeout: Union[int, float], check_time: int=1):
        """
        检查PNC的值
        :param bus_name: 总线名
        :param msg_id: 消息id
        :param signal_name: PNC名称
        :param signal_value: PNC信号值
        :param timeout: 超时时间
        :param check_time: 检查到PNC的置位次数
        :return: flag,检查的结果,true和false
                 recv_data,成功时会将接收到的PNC数据放到列表中返回
        """
        self.rx_flag_reset_bus(bus_name)
        if 'PNC' in signal_name:
            try:
                pnc_id = int(re.findall(r'PNC(\d+)_', signal_name)[0])
            except (IndexError, TypeError):
                err_msg= f"{signal_name}不存在PNC ID"
                logger.error(err_msg)
                raise exception_error.IpduError(err_msg)
        flag = False
        start_time = time.time()
        end_time = time.time()
        recv_value = None
        recv_data = []
        i = 0
        while end_time - start_time < timeout:
            pdu_data = self.recv_pdu(bus_name=bus_name, id=msg_id)
            if pdu_data:
                pdu_data = pdu_data[3]
                recv_value = (pdu_data[pnc_id // 8] >> pnc_id % 8) & 1
                if recv_value == signal_value:
                    i += 1
                    logger.info(f"check PNC success times {i}")
                    if i == check_time:
                        logger.info(f"check PNC success")
                        flag = True
                        recv_data.append(pdu_data)
                        return True, recv_data
                elif i > 0:
                    logger.error(f'获取的值发生了变化, target value is {signal_value}, recv value is {recv_value}')
                    break
            elif i > 0:
                logger.error(f'获取的值发生了变化, target value is {signal_value}, recv value is {pdu_data}')
                break 
            logger.info(f"check PNC, target value is {signal_value}, recv value is {recv_value}")
            end_time = time.time()
        if not flag:
            logger.error(f"check PNC fail")
        return flag, recv_data

    def check_network_msg(self, bus_name: str, msg_id: int, timeout):
        start_time = time.time()
        end_time = time.time()
        flag = False
        while end_time - start_time < timeout:
            pdu_data = self.recv_pdu(bus_name=bus_name, id=msg_id, timeout=0.5)
            if pdu_data:
                logger.info(f"{bus_name} {msg_id} 网络管理已发出")
                flag = True
                return flag
            else:
                logger.info(f"{bus_name} {msg_id} 网络管理未发出")
            end_time = time.time()
        if not flag:
            logger.info(f"{bus_name} {msg_id} 网络管理未发出")
        return flag

    def get_current_expected_message(self, channel, recv_id: [int, list, None] = None,
                                     filter_id: [int, list, None] = None, timeout=2):
        '''
        接收 指定通道的报文，返回接受的报文信息，每次接收前，要清空buffer
        @param channel: 通道，can lin fr
        @param recv_id: 接收指定的id，可以为单个id 或者一个列表包含多个id,默认为None 接收任意id（除去过滤对的id）报文
        @param filter_id: 过滤掉id，接收到该id的报文不算,可以为单个id 或者一个列表包含多个id，默认None 不过滤id
        @param timeout: 接收的超时时间，接收到报文（除去过滤的报文）就退出，接收不到就一直等到超时退出
        @return: msg/None
        '''
        pdu_dicts = self.bus_pdu_dict.get(channel)
        if not pdu_dicts:
            logger.warning(f"没有发现指定通道：{channel}")
            raise

        self.rx_flag_reset_bus(channel)
        self.receive_current_message = None
        recv_id = [None] if recv_id is None else recv_id
        recv_id = [recv_id] if not isinstance(recv_id, list) else recv_id

        filter_id = [] if filter_id is None else filter_id
        filter_id = [filter_id] if not isinstance(filter_id, list) else filter_id

        for fil_id in recv_id:
            pdu_filter_thrading = Thread(
                target=self._pdu_filter_message,
                name="Recv_Pdu_Filter_Current",
                args=(pdu_dicts, fil_id, filter_id, timeout),
                daemon=True,
            )
            pdu_filter_thrading.start()
        time.sleep(timeout)
        if self.receive_current_message:
            return self.receive_current_message

    def _pdu_filter_message(self, pdu_dicts, recv_id, filter_id, timeout):
        while timeout > 0:
            for msg_name, msg_info in pdu_dicts.items():
                with self.lock:
                    if recv_id:
                        if msg_info.get("msg_id") == recv_id and msg_info.get("rx_flag"):
                            if msg_info["msg_id"] not in filter_id:
                                logger.info(f"收到消息：{msg_name} 数据。")
                                pdu_dicts[msg_name]["rx_flag"] = False
                                self.receive_current_message = msg_info
                                if self.receive_message_queue.get(msg_name):
                                    self.receive_message_queue[msg_name].append(msg_info)
                                else:
                                    self.receive_message_queue[msg_name] = deque([msg_info], maxlen=self.max_receive_number)
                    else:
                        if msg_info.get("rx_flag"):
                            if msg_info["msg_id"] not in filter_id:
                                logger.info(f"收到消息：{msg_name} 数据。")
                                pdu_dicts[msg_name]["rx_flag"] = False
                                self.receive_current_message = msg_info
                                if self.receive_message_queue.get(msg_name):
                                    self.receive_message_queue[msg_name].append(msg_info)
                                else:
                                    self.receive_message_queue[msg_name] = deque([msg_info], maxlen=self.max_receive_number)
            timeout -= 0.001
            sleep(0.001)
        return

    def get_designated_time_expected_message(self, channel, recv_id: [int, list, None] = None,
                                             filter_id: [int, list, None] = None, timeout=2):
        '''
        接收一段时间   指定通道的报文，返回接受的报文信息，每次接收前，要清空buffer
        @param channel: 通道，can lin fr
        @param recv_id: 接收指定的id，可以为单个id 或者一个列表包含多个id,默认为None 接收任意id（除去过滤对的id）报文
        @param filter_id: 过滤掉id，接收到该id的报文不算,可以为单个id 或者一个列表包含多个id，默认None 不过滤id
        @param timeout: 接收的一段时间，接收到报文（除去过滤的报文）就退出，接收不到就一直等到超时退出
        @return: [msg1，msg2 ....]/None
        '''
        pdu_dicts = self.bus_pdu_dict.get(channel)
        if not pdu_dicts:
            logger.warning(f"没有发现指定通道：{channel}")
            raise

        self.rx_flag_reset_bus(channel)
        self.receive_message_queue.clear()
        recv_id = [None] if recv_id is None else recv_id
        recv_id = [recv_id] if not isinstance(recv_id, list) else recv_id

        filter_id = [] if filter_id is None else filter_id
        filter_id = [filter_id] if not isinstance(filter_id, list) else filter_id
        for fil_id in recv_id:
            pdu_filter_thrading = Thread(
                target=self._pdu_filter_message,
                name="Recv_Pdu_Filter_Designated",
                args=(pdu_dicts, fil_id, filter_id, timeout),
                daemon=True,
            )
            pdu_filter_thrading.start()
        time.sleep(timeout)
        if self.receive_message_queue:
            return [message for message in self.receive_message_queue.values()]

    def stop_special_message_send(self):
        self.special_message_run_flag = False
        time.sleep(0.5)

    def filter_special_message_send(self, bus_name, message: (str, int), no_opera_signal: (list, str),
                                    cycle_value_list=None, cycle_time=None, offset=3):
        """
        把给定frame中除了给定信号以外的信号遍历0,1
        @param bus_name: 通道，can lin fr
        @param message: 报文名称，字符串类型；或者报文ID，整型
        @param no_opera_signal: 不需要遍历发送0，1的信号，类型可是str,获取多个信号list
        @param cycle_value_list: 遍历发送的循环值
        @param cycle_time: 需要设置的发送周期，不设置默认为数据库初始周期
        @param offset: 是默认周期的多少倍
        """
        if cycle_value_list is None:
            cycle_value_list = [0, 1, 0, 0]
        pdu_dicts = self.bus_pdu_dict.get(bus_name)
        if not pdu_dicts:
            logger.warning(f"没有发现指定通道：{bus_name}")
            raise AssertionError(f"没有发现指定通道：{bus_name}")
        if not isinstance(no_opera_signal, list):
            no_opera_signal = [no_opera_signal]

        no_opera_signal_list = []
        for signal_name in no_opera_signal:
            if not (
                    signal_name.endswith("_UB")
                    or signal_name.endswith("Chks")
                    or signal_name.endswith("Cntr")
            ):
                no_opera_signal_list.append(signal_name)

        for inner_message, msg_info in pdu_dicts.items():
            if isinstance(message, int):
                if msg_info.get("msg_id") != message:
                    continue
            elif isinstance(message, str):
                if inner_message != message:
                    continue
            else:
                logger.warning(f"消息类型错误，得到：{type(message)}")
            if msg_info.get("tx_node") not in self.dut_ecu:
                if (
                        # msg_info.get("msg_cycle")
                        # and
                        ("NmFr" not in inner_message)
                        and ("Diag" not in inner_message)
                ):
                    msg_obj = getattr(getattr(self, bus_name), inner_message)
                    need_signal_list = []
                    logger.debug(f"no_opera_signal_list is:{no_opera_signal_list}")
                    for signal_name in dir(msg_obj):
                        if "__" not in signal_name and signal_name not in (
                                'msg_cycle', 'msg_id', 'msg_length', 'msg_name', 'msg_tx_method', 'msg_type',
                                'rx_nodes',
                                'sig_group_dataid_dict', 'sig_group_dict', 'tx_node', 'msg_base_cycle',
                                'msg_repetition', 'msg_slotid'):
                            if (
                                    # signal_name.endswith("_UB")
                                    signal_name.endswith("Chks")
                                    or signal_name.endswith("Cntr")
                            ):
                                logger.debug("_UB , Chks, Cntr 为E2E校验信号。")
                            else:
                                if signal_name not in no_opera_signal_list:
                                    need_signal_list.append(signal_name)

                    if need_signal_list:
                        logger.info(f"need_signal_list 是：{need_signal_list}")
                        self.special_message_run_flag = True
                        pdu_filter_thrading = Thread(
                            target=self._cyc_iter_set_pdu_data,
                            name="filter_special_message_send",
                            args=(cycle_value_list, cycle_time, msg_obj, need_signal_list, pdu_dicts, inner_message,
                                  offset),
                            daemon=True,
                        )
                        pdu_filter_thrading.start()
                        # self._cyc_iter_set_pdu_data(cycle_value_list, cycle_time, msg_obj, need_signal_list, pdu_dicts, inner_message,
                        #           offset)
                        time.sleep(0.5)

    def _cyc_iter_set_pdu_data(self, cycle_value_list, cycle_time, msg_obj, need_signal_list, pdu_dicts, inner_message,
                               offset):
        if cycle_time is None:
            try:
                cycle_time = getattr(msg_obj, "msg_cycle", 0) * offset
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/i_signal_i_pdu_jet20.py")
                logger.warning(f"消息周期得到：{e}")
                cycle_time = 0
        # 信号先发0在发1，最后再循环发0
        for first_value in cycle_value_list:
            for sg_name in need_signal_list:
                signal_name = self.__unified_signal_name(msg_obj, sg_name)
                pdu_dicts, msg_name = self.__set(
                    msg_obj, signal_name, first_value, True
                )
            time.sleep(cycle_time)
            # self.set(msg_obj, sg_name, inner_message_data, cycle_time=0)
            # msg = pdu_dicts.get(inner_message)

        msg = pdu_dicts.get(inner_message)
        msg["tx_change"] = True
        msg["msg_cycle"] = 0
        if msg.get("tx_flag") is not None:
            msg["tx_flag"] = True
        # logger.info(f"设置后的pud data 是：{msg.get('pdu_data')},周期：{cycle_time}")
        time.sleep(cycle_time)

        if not isinstance(cycle_value_list, list):
            logger.error(f"需要遍历的信号值列表错误，得到：{type(cycle_value_list)}")
            raise AssertionError(f"需要遍历的信号值列表错误，得到：{type(cycle_value_list)}")

        replay_message = cycle(cycle_value_list[-2:])
        logger.info(f"需要迭代发送的信号值是：{cycle_value_list[-2:]}，周期是：{cycle_time}")
        while self.special_message_run_flag:
            # msg = None
            inner_message_data = next(replay_message)
            for sg_name in need_signal_list:
                signal_name = self.__unified_signal_name(msg_obj, sg_name)
                pdu_dicts, msg_name = self.__set(
                    msg_obj, signal_name, inner_message_data, True
                )

                # self.set(msg_obj, sg_name, inner_message_data, cycle_time=0)
                # msg = pdu_dicts.get(inner_message)

            msg = pdu_dicts.get(inner_message)
            msg["tx_change"] = True
            msg["msg_cycle"] = 0
            if msg.get("tx_flag") is not None:
                msg["tx_flag"] = True
            # logger.info(f"设置后的pud data 是：{msg.get('pdu_data')},周期：{cycle_time}")
            time.sleep(cycle_time)

    def get_signal_message(self, bus_name, message):
        """
        @param bus_name: 通道，can lin fr
        @param message: message ID
        """
        pdu_dicts = self.bus_pdu_dict.get(bus_name)
        logger.debug(f"获取信号{pdu_dicts}")
        if not pdu_dicts:
            logger.warning(f"没有发现指定通道：{bus_name}")
            raise AssertionError(f"没有发现指定通道：{bus_name}")

        for inner_message, msg_info in pdu_dicts.items():
            if '0x' in message:
                msg_id = int(message, 16)
            else:
                msg_id = int(message.split('-')[0])*256*256 + int(message.split('-')[1])*256 + int(message.split('-')[-1])
            if msg_info.get("msg_id") == msg_id:
                    logger.info(f"获取信号{inner_message}")
                    return inner_message


if __name__ == "__main__":
    # UDP 的CDD 发送demo

    # 配置信息
    udp_mcu_ip = "172.18.7.16"
    udp_mcu_port = 30508
    udp_mpu_ip = "172.18.128.7"
    udp_mpu_port = 30509

    # 数据对象
    ipdu = ISignalIPdu(cls_path="ecu_simulator/sdk/data/mars1/can_lin_fr_cls/v_3_0_0")
    ipdu.start_all_time_control(isrealbus=False)

    # 设置信号值示例
    # ipdu.set(ipdu.cem_lin6.CemCem_Lin6Fr02, "BattSnsrStReq", 1)

    # 发送UDP报文
    cspdu = S2sCombinationSendPdu(ipdu, address=(udp_mcu_ip, udp_mcu_port))
    cspdu.continuous_combinationpdu_start()
    cspdu.s2ssendpdu_start(tar_address=(udp_mpu_ip, udp_mpu_port))
    time.sleep(1000)
    cspdu.sendpdu_flag = False  # 停止发送

    ipdu.time_control_stop()  # 结束配置对象

