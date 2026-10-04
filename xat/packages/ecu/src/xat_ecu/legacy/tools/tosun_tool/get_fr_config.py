# -*- coding: utf-8 -*-
"""
@File        : get_fr_config.py
@Author      : quan.sun@jiduauto.com
@Time        : 2023/08/16 8:36 AM
@Description : description about this file
@Examples    : example of how to use it
"""

import os
import sys

current_path = os.path.dirname(os.path.realpath(__file__))
print(current_path)

from xat_ecu.legacy.sdk.data.mars1.can_lin_fr_cls.v_1_3_0 import backbonefr


def get_tx_msg_name_list():
    #return: list    [msg obj]
    tx_msg_obj_list = []
    str_list = dir(backbonefr)
    for cls_str in str_list:
        if "__" not in cls_str and getattr(backbonefr, cls_str).tx_node != "BGM":
            tx_msg_obj_list.append(getattr(backbonefr, cls_str))
    return tx_msg_obj_list

def get_sig_info(sig_obj, dataid):
    startBit = sig_obj.startbit
    Length = sig_obj.length
    IsIntel = 1 if sig_obj.sig_byteorder == "Intel" else 0
    DataId = dataid
    SignalValue = sig_obj.sig_value_init
    iscntr = 1 if "Cntr" in sig_obj.sig_name else 0
    sig_info = f"{startBit},{Length},{IsIntel},{DataId},{SignalValue},{iscntr}"
    return sig_info

def get_fr_msg_info_list(tx_msg_obj_list):
    m = 0
    msg_infos = []
    for msg_obj in tx_msg_obj_list:
        FFrameID = f"FFrameID = {msg_obj.msg_slotid}"
        FBaseCycle = f"FBaseCycle = {msg_obj.msg_base_cycle}"
        FRepCycle = f"FRepCycle = {msg_obj.msg_repetition}"
        FFrameLen = f"FFrameLen = {msg_obj.msg_length}"

        sig_group_dataid_dict = msg_obj.sig_group_dataid_dict
        sig_group_info = []
        if sig_group_dataid_dict:
            i = 0
            for sig_group_name, dataid in sig_group_dataid_dict.items():
                j = 0

                sig_group_ub = sig_group_name + "_UB"
                if hasattr(msg_obj, sig_group_ub):
                    sig_obj = getattr(msg_obj, sig_group_ub)
                    ubsig_info = get_sig_info(sig_obj, dataid)
                else:
                    ubsig_info = ""

                sig_group_dict = msg_obj.sig_group_dict
                sig_list = sig_group_dict.get(sig_group_name)

                if sig_list:
                    for sig_name in sig_list:
                        if "Chks" in sig_name:
                            sig_obj = getattr(msg_obj, sig_name)
                            crcsig_info = get_sig_info(sig_obj, dataid)

                    for sig_name in sig_list:
                        if "Chks" not in sig_name:
                            sig_index = f"{i}{j}"
                            sig_obj = getattr(msg_obj, sig_name)
                            sig_info = get_sig_info(sig_obj, dataid)

                            sig_group_info.append(f"{sig_index} = {sig_info}")

                            j += 1

                    sig_index_crc = f"{i}{j}"
                    sig_group_info.append(f"{sig_index_crc} = {crcsig_info}")
                    sig_index_ub = f"{i}{j+1}"
                    sig_group_info.append(f"{sig_index_ub} = {ubsig_info}")

                i += 1

        msg_index = f"[000{m}]"
        msg_info = [msg_index, FFrameID, FBaseCycle, FRepCycle, FFrameLen, sig_group_info]
        msg_infos.append(msg_info)
        m += 1
    return msg_infos


def write_config(msg_infos):
    print("===================start============================")
    with open("./config.ini", "w") as f:
        f.write("[config]")
        f.write("\n")
        f.write("E2EConfig = 1")
        f.write("\n")
        f.write("SaveLog = 1")
        f.write("\n")
        f.write("DeviceSerial = E7CB383B263B8955")
        f.write("\n")
        f.write("E2ECRCDLL = ./E2ECRCDLL.dll")
        f.write("\n")
        f.write("CRCFunc = crc8_calc")
        f.write("\n")
        f.write("FlexRaySRCIP = 127.0.0.1")
        f.write("\n")
        f.write("FlexRaySRCPORT = 8000")
        f.write("\n")
        f.write("FlexRayDSTIP = 127.0.0.1")
        f.write("\n")
        f.write("FlexRayDSTPORT = 8001")
        f.write("\n")

        f.write("\n")

        for msg_info in msg_infos:
            for msginfo in msg_info:
                if isinstance(msginfo, str):
                    f.write(msginfo)
                    f.write("\n")
                else:
                    if msginfo:
                        for sig_info in msginfo:
                            f.write(sig_info)
                            f.write("\n")

    print("===================end============================")

if __name__=="__main__":
    tx_msg_obj_list = get_tx_msg_name_list()
    msg_infos = get_fr_msg_info_list(tx_msg_obj_list)
    write_config(msg_infos)

