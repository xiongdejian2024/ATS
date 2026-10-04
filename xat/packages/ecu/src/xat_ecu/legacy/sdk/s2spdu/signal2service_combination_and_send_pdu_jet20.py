"""
@File        : signal2service_Combination_and_send_pdu.py
@Author      : quan.sun@jiduauto.com
@Time        : 2022/04/04 19:12
@Description :
@Examples    :
"""


import os
import sys
import argparse
from collections import deque

current_path = os.path.dirname(os.path.realpath(__file__))
from xat_ecu.legacy.common.time_handle import *
from xat_ecu.legacy.sdk.s2spdu.PDU_Const import *
from xat_ecu.legacy.common.data_type_handing import *
import threading
from threading import Thread
from xat_ecu.legacy.sdk.driver.udp_socket import UdpSocketClient
PDU_SEND_DATA_LIST_LEN = 10000


class S2sCombinationSendPdu:
    """jet2.0"""
    def __init__(self, bus_pdu_dict, address=("127.0.0.1", 30502)):
        self.bus_pdu_dict = bus_pdu_dict.bus_pdu_dict
        self.ipdu_instance = bus_pdu_dict
        del_bus = []
        for bus in self.bus_pdu_dict.keys():
            if not hasattr(BUSID, bus.upper()):
                del_bus.append(bus)
        for bus in del_bus:
            del self.bus_pdu_dict[bus]
        self.pdu_list = deque(maxlen=PDU_SEND_DATA_LIST_LEN)
        self.sendpdu = UdpSocketClient(1, "UDP Socket tx", address=address)
        self.continuous_combinationpdu_flag = None
        self.sendpdu_flag = None
        self.lock = threading.Lock()

    def continuous_combinationpdu_start(self):
        self.continuous_combinationpdu_flag = True
        time_thrading = Thread(target=self.continuous_combinationpdu, name="Continuous_Combinationpdu")
        time_thrading.setDaemon(True)
        time_thrading.start()

    def continuous_combinationpdu_stop(self):
        self.continuous_combinationpdu_flag = False
        sleep(0.1)

    def continuous_combinationpdu(self):
        sleep(1)    # Wait for 1s to update the signals before sending
        global_clock_list, global_time = get_8_list_datetime_and_current_time()
        pdu_date = []
        msg_data_lists = []
        while self.continuous_combinationpdu_flag:
            global_time, global_clock_list, pdu_date, msg_data_lists = self.combinationpdu(global_time,
                                                                                           global_clock_list, pdu_date,
                                                                                           msg_data_lists)
            sleep(0.01)

    def combinationpdu(self, global_time, global_clock_list=[], pdu_date=[], msg_data_lists=[]):
        for bus in self.bus_pdu_dict.keys():
            bus_cls_obj = getattr(self.ipdu_instance, bus)
            for message in self.bus_pdu_dict[bus]:
                msg_obj = self.bus_pdu_dict[bus][message]
                if msg_obj.get("tx_change"):
                    msg_obj["tx_change"] = None  # 还原标志位
                    if not pdu_date:
                        global_clock_list, global_time = get_8_list_datetime_and_current_time()
                        pdu_date = global_clock_list
                    busid = [getattr(BUSID, bus.upper())]
                    message_id = msg_obj.get("msg_id")

                    # 判断计算count crc
                    msg_cls_obj = getattr(bus_cls_obj, message)
                    if hasattr(msg_cls_obj, "sig_group_dataid_dict"):
                        crc_sig_groups = msg_cls_obj.sig_group_dataid_dict
                        if crc_sig_groups:  # crc sig group (dataid)
                            for sig_group in crc_sig_groups:
                                self.ipdu_instance.set_crc_count(
                                    msg_cls_obj,
                                    sig_group,
                                    do_cntr=getattr(msg_cls_obj, (sig_group + "_cntr"))
                                    if hasattr(msg_cls_obj, (sig_group + "_cntr"))
                                    else None,
                                    do_crc=getattr(msg_cls_obj, (sig_group + "_crc"))
                                    if hasattr(msg_cls_obj, (sig_group + "_crc"))
                                    else None,
                                )

                    if busid[0] > 40:
                        message_id = [message_id]
                    else:
                        message_id = int_to_2_bytes_list(message_id)
                    relative_time = int((time.time() - int(global_time))*1000)
                    relative_time = int_to_2_bytes_list(relative_time)
                    message_length = [msg_obj.get("msg_length")]
                    msg_pdu = msg_obj.get("pdu_data")
                    msg_data_list = busid + message_id + relative_time + message_length + msg_pdu
                    # print(f"{pdu_date}  {msg_data_lists}  {PDUConst.MSG_END}")
                    if len(msg_data_lists + msg_data_list) < 1393:
                        msg_data_lists += msg_data_list
                    elif len(msg_data_lists + msg_data_list) > 1393:
                        pdu_date = pdu_date + msg_data_lists + [PDUConst.MSG_END]
                        self.lock.acquire()
                        self.pdu_list.append(pdu_date)
                        self.lock.release()
                        global_clock_list, global_time = get_8_list_datetime_and_current_time()
                        pdu_date = []
                        msg_data_lists = msg_data_list
                    elif len(msg_data_lists) == 1393:
                        msg_data_lists += msg_data_list
                        pdu_date = pdu_date + msg_data_lists + [PDUConst.MSG_END]
                        self.lock.acquire()
                        self.pdu_list.append(pdu_date)
                        self.lock.release()
                        global_clock_list, global_time = get_8_list_datetime_and_current_time()
                        pdu_date = []
                        msg_data_lists = []
        return global_time, global_clock_list, pdu_date, msg_data_lists

    def s2ssendpdu_start(self, tar_address=("127.0.0.1", 30502)):
        self.sendpdu_flag = True
        time_thrading = Thread(target=self.s2ssendpdu, name="s2ssendpdu", args=(tar_address,))
        time_thrading.setDaemon(True)
        time_thrading.start()

    def s2ssendpdu(self, tar_address=("127.0.0.1", 30502)):

        while self.sendpdu_flag:
            try:
                self.lock.acquire()
                if self.pdu_list:
                    print(len(self.pdu_list))
                    udp_data = self.pdu_list.popleft()   # 需要去取第一个 to do
                    self.lock.release()
                    self.sendpdu.send(udp_data, tar_address)
                else:
                    self.lock.release()
                    sleep(0.01)
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/s2spdu/signal2service_combination_and_send_pdu_jet20.py")
                logger.warning(e)
                self.lock.release()

    def s2ssendpdu_stop(self):
        self.sendpdu.close()
        self.sendpdu_flag = False
