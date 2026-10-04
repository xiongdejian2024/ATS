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
from xat_ecu.legacy.common.logger import logger

current_path = os.path.dirname(os.path.realpath(__file__))


def get_tx_msg_name_list(bus_obj, dut_ecu=["BGM"]):
    # return: list    [msg_obj1, msg_obj2]
    tx_msg_obj_list = []
    str_list = dir(bus_obj)
    for cls_str in str_list:
        if "__" not in cls_str and getattr(bus_obj, cls_str).tx_node not in dut_ecu:
            tx_msg_obj_list.append(getattr(bus_obj, cls_str))
    return tx_msg_obj_list


def get_sig_info(sig_obj, dataid):
    # sig_info   ---  startBit,Length,IsIntel,DataId,SignalValue,is_cntr
    startBit = sig_obj.startbit
    Length = sig_obj.length
    IsIntel = 1 if sig_obj.sig_byteorder == "Intel" else 0
    DataId = dataid
    SignalValue = sig_obj.sig_value_init
    iscntr = 1 if sig_obj.sig_name.endswith("Cntr") else 0    # endswith排除  信号名含 Cntr 的特殊情况   例如 WhlRotToothCntrFrntLe信号  和  WhlRotToothCntr 信号组
    sig_info = f"{startBit},{Length},{IsIntel},{DataId},{SignalValue},{iscntr}"
    return sig_info


def get_fr_msg_info_list(tx_msg_obj_list, pdu_dict, bus_name, HWidx, chnidx=0):
    # msg_index ---- HWidx,busType,chnidx,Msgidx
    # busType: 0-flexray 1-can 2-lin
    # chnidx: 0, 1 ,2   .....   ,9 ,10 ,11
    m = 0
    msg_infos = []
    busType = 0
    chnidx = hex(chnidx)[2:]
    for msg_obj in tx_msg_obj_list:
        FFrameID = f"FFrameID = {msg_obj.msg_slotid}"
        FBaseCycle = f"FBaseCycle = {msg_obj.msg_base_cycle}"
        FRepCycle = f"FRepCycle = {msg_obj.msg_repetition}"
        FFrameLen = f"FFrameLen = {msg_obj.msg_length}"

        ISWAKE = f"ISWAKE = 0"
        data = pdu_dict[msg_obj.msg_name]["pdu_data"]
        data_str = "DATA = "
        for i in data:
            data_str = data_str + f"{i}" + ","
        DATA = data_str.strip(",")

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

        msg_index = f"[{HWidx}{busType}{chnidx}{m}]"
        msg_info = [
            msg_index,
            FFrameID,
            FBaseCycle,
            FRepCycle,
            FFrameLen,
            ISWAKE,
            DATA,
            sig_group_info,
        ]
        msg_infos.append(msg_info)
        m += 1
    return msg_infos


def get_can_msg_info_list(tx_msg_obj_list, pdu_dict, bus_name, HWidx, chnidx):
    # busType: 0-flexray 1-can 2-lin
    PRECISE_msgs_dict = {"connectivitycanfd": [0x166, 0x149, 0x176]}
    m = 0
    msg_infos = []
    busType = 1
    chnidx = hex(chnidx)[2:]

    PRECISE_msgs_list = PRECISE_msgs_dict.get(bus_name)

    # 配置唤醒报文 0x53F
    CANID = f"CANID = 1343"
    if "canfd" in bus_name:
        ISCANFD = f"ISCANFD = 1"
        CANFDBRS = f"CANFDBRS = 1"
    else:
        ISCANFD = f"ISCANFD = 0"
        CANFDBRS = f"CANFDBRS = 0"
    # CANFDBRS = f"CANFDBRS = 0"   #  解决BGM重启问题，暂改为0

    ISSTD = f"ISSTD = 1"  # 是否标准帧
    CyclcTime = f"CyclcTime = 0.5"  # 每个通道加一个唤醒报文，目前先暴力默认唤醒
    # CyclcTime = f"CyclcTime = 0"   # 每个通道加一个单帧，确保同星通道正常打开
    CANLEN = f"CANLEN = 8"
    ISWAKE = f"ISWAKE = 1"
    DATA = f"DATA = 63,64,0,0,0,0,0,0"
    msg_index = f"[{HWidx}{busType}{chnidx}{m}]"
    sig_group_info = []
    msg_info = [
        msg_index,
        CANID,
        ISCANFD,
        CANFDBRS,
        ISSTD,
        CyclcTime,
        CANLEN,
        ISWAKE,
        DATA,
        sig_group_info,
    ]
    msg_infos.append(msg_info)
    m = 1

    # connectivitycanfd 的can 帧 集合
    connectivitycanfd_can_list = [
        0x177,
        0x10,
        0x14,
        0x18,
        0x198,
        0x191,
        0x165,
        0x164,
        0x301,
    ]

    for msg_obj in tx_msg_obj_list:
        if msg_obj.msg_cycle:
            CANID = f"CANID = {msg_obj.msg_id}"
            if msg_obj.msg_type == "can_fd":
                ISCANFD = f"ISCANFD = 1"
                CANFDBRS = f"CANFDBRS = 1"            
            elif msg_obj.msg_type == "can":
                ISCANFD = f"ISCANFD = 0"
                CANFDBRS = f"CANFDBRS = 0"
            else:
                raise Exception(f"msg_obj.msg_type error: {msg_obj.msg_type}")

            # CANFDBRS = f"CANFDBRS = 1"
            # CANFDBRS = f"CANFDBRS = 0"   #  解决BGM重启问题，暂改为0

            if bus_name == "connectivitycanfd":
                if msg_obj.msg_id in connectivitycanfd_can_list:
                    ISCANFD = f"ISCANFD = 0"
                    CANFDBRS = f"CANFDBRS = 0"

            ISSTD = f"ISSTD = 1"  # 是否标准帧
            CyclcTime = f"CyclcTime = {msg_obj.msg_cycle}"
            CANLEN = f"CANLEN = {msg_obj.msg_length}"
            ISWAKE = f"ISWAKE = 0"

            if PRECISE_msgs_list:
                if CANID in PRECISE_msgs_list:
                    ISPRECISE = "ISPRECISE = 1"
                else:
                    ISPRECISE = "ISPRECISE = 0"
            else:
                ISPRECISE = "ISPRECISE = 0"

            # if msg_obj.msg_cycle and msg_obj.msg_cycle <= 0.03:
            #     ISPRECISE = "ISPRECISE = 1"
            # else:
            #     ISPRECISE = "ISPRECISE = 0"

            data = pdu_dict[msg_obj.msg_name]["pdu_data"]
            data_str = "DATA = "
            for i in data:
                data_str = data_str + f"{i}" + ","
            DATA = data_str.strip(",")

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

            msg_index = f"[{HWidx}{busType}{chnidx}{m}]"
            msg_info = [
                msg_index,
                CANID,
                ISCANFD,
                CANFDBRS,
                ISSTD,
                CyclcTime,
                CANLEN,
                ISWAKE,
                ISPRECISE,
                DATA,
                sig_group_info,
            ]
            msg_infos.append(msg_info)
            m += 1
    return msg_infos


def write_config(
    msg_infos_list: list,
    tosun_serial: str,
    file_path: str = "./config1.ini",
    FlexRayDSTPORT=8001,
    isSaveLog=1,
):
    print("===================start============================")
    with open(file_path, "w") as f:
        f.write("[config]")
        f.write("\n")

        # if FlexRayDSTPORT == 8003:
        #     f.write("E2EConfig = 0")
        #     f.write("\n")
        # else:
        #     f.write("E2EConfig = 1")
        #     f.write("\n")

        f.write("E2EConfig = 1")
        f.write("\n")

        f.write(f"SaveLog = {isSaveLog}")
        f.write("\n")

        # f.write("DeviceSerial = E7CB383B263B8955,609C84C2E4BAF720")
        f.write(f"DeviceSerial = {tosun_serial}")
        f.write("\n")
        f.write("E2ECRCDLL = ./E2ECRCDLL.dll")
        f.write("\n")
        f.write("CRCFunc = crc8_calc")
        f.write("\n")
        f.write("FlexRaySRCIP = 127.0.0.1")
        f.write("\n")
        f.write(f"FlexRaySRCPORT = {FlexRayDSTPORT-1}")
        f.write("\n")
        f.write("FlexRayDSTIP = 127.0.0.1")
        f.write("\n")
        f.write(f"FlexRayDSTPORT = {FlexRayDSTPORT}")
        f.write("\n")

        if FlexRayDSTPORT == 8003:
            # f.write(f"Chn_AIntervalCnt = 100,100,100,100,100,100,100,100,100,500,100,100\n")   # 设置帧间距   单位us
            f.write(f"Chn_AIntervalCnt = 0,0,0,0,0,0,0,0,0,0,0,0\n")   # 设置帧间距   单位us
            f.write("\n")

        for msg_infos in msg_infos_list:
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
            f.write("\n")

        # # 临时  解决 IniMap 文件不能正常启动通道问题
        # if FlexRayDSTPORT == 8003:
        #     f.write("\n")
        #     f.write(f"[0150]\n")
        #     f.write(f"CANID = 1343\n")
        #     f.write(f"ISCANFD = 0\n")
        #     f.write(f"CANFDBRS = 1\n")
        #     f.write(f"ISSTD = 1\n")
        #     f.write(f"CyclcTime = 1\n")
        #     f.write(f"CANLEN = 8\n")
        #     f.write(f"ISWAKE = 1\n")
        #     f.write(f"DATA = 63,64,255,255,255,255,0,0\n")

    logger.info("=========== 生成同星config 完成 ============")


if __name__ == "__main__":
    # tx_msg_obj_list = get_tx_msg_name_list()
    # msg_infos = get_fr_msg_info_list(tx_msg_obj_list)
    # write_config(msg_infos)
    pass
