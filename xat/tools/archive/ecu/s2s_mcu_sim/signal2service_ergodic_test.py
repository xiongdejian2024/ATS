"""
@File        : signal2service_ergodic_test.py
@Author      : quan.sun@jiduauto.com
@Time        : 2022/04/05 22:51
@Description :
@Examples    :
"""

import json
import os
import sys
import argparse
import json

current_path = os.path.dirname(os.path.realpath(__file__))
from pathlib import Path
import importlib
from xat_ecu.legacy.sdk.i_signal_i_pdu import ISignalIPdu
from xat_ecu.legacy.common.logger import *
from xat_ecu.legacy.common.file_handle import FileHandle
from xat_ecu.legacy.common.time_handle import *
from xat_ecu.legacy.sdk.s2spdu.signal2service_combination_and_send_pdu import S2sCombinationSendPdu
from xat_ecu.legacy.sdk.auto.ecu_sig_auto import EcuSigAuto
from threading import Thread


sig_group_size = 500
class S2sTest:
    def __init__(self, cls_path):
        self.ipdu = ISignalIPdu(cls_path)
        self.cspdu = S2sCombinationSendPdu(self.ipdu.bus_pdu_dict, address=("172.16.5.222", 30502))  # Mock BGM MCU , IP port can change
        # self.cspdu = S2sCombinationSendPdu(self.ipdu.bus_pdu_dict, address=("127.0.0.1", 30000))  # local test

    def send_sig(self, func_str):
        func_cls = getattr(self.ipdu, func_str)
        func_cls()
        sleep(1.1)

    def send_sig_value(self, func_value):
        func_cls = getattr(self.ipdu, func_value)
        func_cls(0)
        sleep(1.3)
        func_cls(1)
        sleep(1.2)

    def send_sigs_value(self, func_value_list):
        for func_value in func_value_list:
            self.send_sig_value(func_value)
        logger.info("===================== send_sigs_value finish =================================")

    def send_sigs(self, func_str_list):
        for func_str in func_str_list:
            self.send_sig(func_str)
        logger.info("===================== send_sigs finish =================================")

    def send_sigs_thread(self, sig_group_list):
        send_thread = Thread(target=self.send_sigs, name="send_sigs_thread", args=(sig_group_list,))
        send_thread.start()

    def send_sigs_value_thread(self, sig_group_vlaue_list):
        send_thread = Thread(target=self.send_sigs_value, name="send_sigs_value_thread", args=(sig_group_vlaue_list,))
        send_thread.start()

    def get_sig_groups(self, sig_list):
        length = len(sig_list)
        i = 0
        sig_groups = []
        list_len = sig_group_size
        while length > list_len:
            sig_group = sig_list[list_len * i:list_len * (i + 1)]
            i += 1
            length -= list_len
            sig_groups.append(sig_group)
        sig_groups.append(sig_list[list_len * i:])
        return sig_groups

    def test_s2s_ergodic(self):
        for bus_name in self.ipdu.bus_pdu_dict.keys():
            pdu_info = self.ipdu.bus_pdu_dict.get(bus_name)
            self.ipdu.time_control_start(pdu_info)
        self.cspdu.continuous_combinationpdu_start()

        #  Test Local
        # self.cspdu.s2ssendpdu_start(tar_address=("127.0.0.1", 30502))

        #  Match MPU UDP Tar_address
        self.cspdu.s2ssendpdu_start(tar_address=("172.16.5.1", 30502))

        try:
            logger.info("Sleep 5 seconds")
            sleep(5)

            # ======= Test : Change signal value  =========================

            sig_lists = dir(EcuSigAuto)
            sig_list = []
            sig_list_value = []
            for sig in sig_lists:
                if "__" not in sig and "set" != sig and "_abc_" not in sig:
                    sig_info = sig.split("_")
                    if sig_info[0] in self.ipdu.bus_pdu_dict.keys():
                        if sig_info[-1] == "value":
                            sig_list_value.append(sig)
                        else:
                            sig_list.append(sig)

            sig_list_group = self.get_sig_groups(sig_list)
            logger.info("The length of sig_list_group is {}".format(len(sig_list_group)))
            sig_list_value_group = self.get_sig_groups(sig_list_value)
            logger.info("The length of sig_list_value_group is {}".format(len(sig_list_value_group)))

            for sig_group_list in sig_list_group:
                self.send_sigs_thread(sig_group_list)

            for sig_group_value_list in sig_list_value_group:
                self.send_sigs_value_thread(sig_group_value_list)

            logger.info("Sleep {} seconds".format(2.5*sig_group_size))
            sleep(2.5*sig_group_size)

            logger.info("Sleep 5 seconds")
            sleep(5)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/tools/s2s_mcu_sim/signal2service_ergodic_test.py")
            print(e)
        finally:
            self.cspdu.s2ssendpdu_stop()
            self.ipdu.time_control_stop()
            self.cspdu.continuous_combinationpdu_stop()


if __name__ == "__main__":
    # Work Path: ecu_simulator
    # Command:
    #    (Change cls_path)     python3 tools/s2s_mcu_sim/signal2service_ergodic_test.py --cls_path="sdk/data/mars1/can_lin_fr_cls/v_0_6_0"
    # or (Default cls_path)    python3 tools/s2s_mcu_sim/signal2service_ergodic_test.py
    # logger = Logger(log_level="INFO").get_logger('test')

    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--cls_path', help='can lin fr cls_path', default="sdk/data/mars1/can_lin_fr_cls/v_0_6_0")
    argparser.add_argument(
        '--json_path', help='can lin fr signal config json',
        default="./tools/s2s_mcu_sim/config/sample.json")
    # Default is All
    args = argparser.parse_args()

    s2s_test = S2sTest(args.cls_path)

    s2s_test.test_s2s_ergodic()

