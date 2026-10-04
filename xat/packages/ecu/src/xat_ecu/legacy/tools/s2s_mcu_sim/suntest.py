"""
@File        : signal2service_Combination_pdu.py
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
        self.cspdu = S2sCombinationSendPdu(self.ipdu.bus_pdu_dict, address=("172.16.5.222", 30502))

    def test_s2s_can(self):
        for bus_name in self.ipdu.bus_pdu_dict.keys():
            pdu_info = self.ipdu.bus_pdu_dict.get(bus_name)
            self.ipdu.time_control_start(pdu_info)
        self.cspdu.continuous_combinationpdu_start()

        #  Test Local
        # self.cspdu.s2ssendpdu_start(tar_address=("127.0.0.1", 30502))

        #  Match MPU UDP Tar_address
        self.cspdu.s2ssendpdu_start(tar_address=("172.16.5.1", 30502))

        try:
            sleep(5)

            # ======= Test : Change signal value  =========================
            self.ipdu.adcanfd_acuadcanfdfr03_audwarnlvofsnsrparkassifrnt_buzzeron_4hz()

            sleep(5)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/tools/s2s_mcu_sim/suntest.py")
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
        # self.cspdu.s2ssendpdu_start(tar_address=("127.0.0.1", 30502))

        #  Match MPU UDP Tar_address
        self.cspdu.s2ssendpdu_start(tar_address=("172.16.5.1", 30502))

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
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/tools/s2s_mcu_sim/suntest.py")
            print(e)
        finally:
            self.cspdu.s2ssendpdu_stop()
            self.ipdu.time_control_stop()
            self.cspdu.continuous_combinationpdu_stop()


if __name__ == "__main__":
    # Work Path: sat/
    # Command:
    #    (Change cls_path)     python3 tools/s2s_mcu_sim/signal2service_test.py --cls_path=" ecu_simulator/sdk/data/can_lin_fr_cls/v_0_4_0"
    # or (Default cls_path)    python3 tools/s2s_mcu_sim/signal2service_test.py
    logger = Logger(log_level="INFO").get_logger('test')

    # argparser = argparse.ArgumentParser()
    # argparser.add_argument(
    #     '--cls_path', help='can lin fr cls_path', default=" ecu_simulator/sdk/data/can_lin_fr_cls/v_0_5_5")
    # argparser.add_argument(
    #     '--json_path', help='can lin fr signal config json',
    #     default="/home/sun/quansunclean/sat/tools/s2s_mcu_sim/config/sample.json")
    # # Default is All
    # args = argparser.parse_args()
    #
    # s2s_test = S2sTest(args.cls_path)
    #
    # # s2s_test.test_s2s_can()
    # s2s_test.test_s2s_cfg(args.json_path)

    from sdk.dut.data.can_lin_fr_cls import v_0_5_0
    from sdk.dut.data.can_lin_fr_cls import v_0_5_5

    v050_list = ['cem_lin1', 'bodyalmcanfd2', 'connectivitycanfd', 'smd_lin1', 'cem_lin5', 'adprivatecanfd1', 'cem_lin6', 'ccm_lin2', 'bodycan', 'propulsioncan', 'ecm_lin2', 'ecm_lin4', 'chassiscan1', 'passivesafetycan', 'adprivatecanfd2', 'ccm_lin3', 'ddm_lin1', 'bodyexposedcanfd', 'adredundancycan', 'diagnosticcan', 'cem_lin7', 'cem_lin4', 'bgmintcomm', 'ecm_lin1', 'ccm_lin4', 'backbonefr', 'privatebncmcanfd', 'bodyalmcanfd1', 'ccm_lin1', 'cem_lin3', 'smp_lin1', 'adcanfd', 'ecm_lin3', 'infocanfd', 'cem_lin2', 'chassiscan2', 'flrcanfd', 'privateinfocanfd']
    v055_list = ['cem_lin1', 'bodyalmcanfd2', 'connectivitycanfd', 'smd_lin1', 'cem_lin5', 'adprivatecanfd1', 'cem_lin6', 'ccm_lin2', 'bodycan', 'propulsioncan', 'ecm_lin2', 'ecm_lin4', 'chassiscan1', 'passivesafetycan', 'adprivatecanfd2', 'ccm_lin3', 'ddm_lin1', 'bodyexposedcanfd', 'adredundancycan', 'diagnosticcan', 'cem_lin4', 'bgmintcomm', 'ecm_lin1', 'ccm_lin4', 'backbonefr', 'privatebncmcanfd', 'bodyalmcanfd1', 'ccm_lin1', 'cem_lin3', 'smp_lin1', 'adcanfd', 'ecm_lin3', 'infocanfd', 'cem_lin2', 'chassiscan2', 'flrcanfd', 'privateinfocanfd']
    logger.info("==========  v055   VS  v050  =========")
    logger.info(" ")
    logger.info("v055 del bus: cem_lin7 ")
    for i in v055_list:
        logger.info(" ")
        logger.info("====================== bus : {} ===============================".format(i))
        v050 = getattr(v_0_5_0, i)
        v055 = getattr(v_0_5_5, i)
        v050_message = dir(v050)
        v055_message = dir(v055)
        v055_add = list(set(v055_message) - set(v050_message))
        logger.info("v055_add message : {}".format(v055_add))
        v055_del = list(set(v050_message) - set(v055_message))
        logger.info("v055_del message : {}".format(v055_del))
        v055_v050 = list(set(v050_message) & set(v055_message))
        for j in v055_v050:
            if "__" not in j:
                v050_mesobj = getattr(v050, j)
                v055_mesobj = getattr(v055, j)
                v050_sig = dir(v050_mesobj)
                v055_sig = dir(v055_mesobj)
                v055_add = list(set(v055_sig) - set(v050_sig))
                v055_del = list(set(v050_sig) - set(v055_sig))
                if v055_add == [] and v055_del == []:
                    pass
                else:
                    logger.info("    ================== message : {} =============================".format(j))
                    logger.info("v055_add signal : {}".format(v055_add))
                    logger.info("v055_del signal : {}".format(v055_del))
                # v055_v050 = list(set(v050_sig) & set(v055_sig))


