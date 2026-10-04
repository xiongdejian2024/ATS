"""
@File        : signal2service_local.py
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


class S2sTest:
    def __init__(self, cls_path):
        self.ipdu = ISignalIPdu(cls_path)
        self.cspdu = S2sCombinationSendPdu(self.ipdu.bus_pdu_dict, address=("127.0.0.1", 30000))

    def test_s2s_can(self):
        for bus_name in self.ipdu.bus_pdu_dict.keys():
            pdu_info = self.ipdu.bus_pdu_dict.get(bus_name)
            self.ipdu.time_control_start(pdu_info)
        self.cspdu.continuous_combinationpdu_start()

        #  Test Local
        self.cspdu.s2ssendpdu_start(tar_address=("127.0.0.1", 30502))

        #  Match MPU UDP Tar_address
        # self.cspdu.s2ssendpdu_start(tar_address=("172.16.5.1", 30502))

        try:
            sleep(5)

            # ======= Test : Change signal value  =========================
            self.ipdu.adcanfd_acuadcanfdfr03_audwarnlvofsnsrparkassifrnt_buzzeron_4hz()

            sleep(5)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/tools/s2s_mcu_sim/signal2service_local.py")
            print(e)
        finally:
            self.cspdu.s2ssendpdu_stop()
            self.ipdu.time_control_stop()
            self.cspdu.continuous_combinationpdu_stop()

    def test_s2s_cfg(self, json_path):
        for bus_name in self.ipdu.bus_pdu_dict.keys():
            pdu_info = self.ipdu.bus_pdu_dict.get(bus_name)
            self.ipdu.time_control_start(pdu_info)
        self.cspdu.continuous_combinationpdu_start()

        #  Test Local
        self.cspdu.s2ssendpdu_start(tar_address=("127.0.0.1", 30502))

        #  Match MPU UDP Tar_address
        # self.cspdu.s2ssendpdu_start(tar_address=("172.16.5.1", 30502))

        try:
            with open(json_path, "r") as f:
                json_dict = json.load(f)
            json_list = json_dict.get("payload")
            for info in json_list:
                if "sleep" in info.keys():
                    sleep_value = info.get("sleep")
                    logger.info("sleep {}s".format(sleep_value))
                    sleep(sleep_value)
                elif "signal" in info.keys():
                    signal_infos = info.get("signal")
                    busobj = getattr(self.ipdu, signal_infos[0])
                    messageobj = getattr(busobj, signal_infos[1])
                    self.ipdu.set(messageobj, signal_infos[2], signal_infos[3])
                    logger.info("Update signal value ========  {}".format(signal_infos))

        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/tools/s2s_mcu_sim/signal2service_local.py")
            print(e)
        finally:
            self.cspdu.s2ssendpdu_stop()
            self.ipdu.time_control_stop()
            self.cspdu.continuous_combinationpdu_stop()


if __name__ == "__main__":
    # Work Path: sat/
    # Command:
    #    (Change cls_path)     python3 tools/s2s_mcu_sim/signal2service_test.py --cls_path=" ecu_simulator/sdk/data/can_lin_fr_cls/v_0_5_0" --json_path="./tools/s2s_mcu_sim/config/sample.json"
    # or (Default cls_path)    python3 tools/s2s_mcu_sim/signal2service_test.py
    # logger = Logger(log_level="INFO").get_logger('test')
    os.system("mkdir ../report")
    os.system("touch ../report/report_summary.json")
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--cls_path', help='can lin fr cls_path', default="sdk/data/mars1/can_lin_fr_cls/v_0_5_5")
    argparser.add_argument(
        '--json_path', help='can lin fr signal config json',
        default="./tools/s2s_mcu_sim/config/sample.json")
    # Default is All
    args = argparser.parse_args()

    s2s_test = S2sTest(args.cls_path)

    # s2s_test.test_s2s_can()
    s2s_test.test_s2s_cfg(args.json_path)

