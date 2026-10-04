# -*- coding: utf-8 -*-
"""
@File        : pcap_reader.py
@Author      : jinhui.zhao@jiduauto.com
@Time        : 2022/5/8 21:06
@Description : 
@Examples    :
"""
import json
import os
import sys
project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

from xat_ecu.legacy.common.logger import logger
from scapy.all import rdpcap

from cdd_pdu_parser import *
import pdb

DST_MAC = '02:00:00:00:10:01'
SRC_MAC = '02:00:00:00:10:02'
DST_PORT = 30502
SRC_PORT = 30502

bus_msg_counter = {}

bus_msg_id_dict = {}
bus_mapping = {"1": "FlexRay", "2": "InfoCANFD", "3": "ADCANFD", "4": "PropulsionCAN", "5": "ChassisCAN1",
               "6": "ChassisCAN2",
               "7": "PassiveSafetyCAN", "8": "ConnectivityCANFD", "9": "BodyCAN", "10": "BodyExposedCANFD",
               "11": "BodyALMCANFD1",
               "12": "BodyALMCANFD2", "41": "CEM_LIN1", "42": "CEM_LIN2", "43": "CEM_LIN3", "44": "CEM_LIN4",
               "45": "CEM_LIN5",
               "46": "CEM_LIN6", "47": "CEM_LIN7"}

try:
    with open('bus_msg_ids.json', 'r') as f:
        bus_msg_id_dict = json.load(f)
except Exception as e:
    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/cdd_tools/pcap_reader.py")
    logger.error(str(e))
    exit()

for bus, ids in bus_msg_id_dict.items():
    msg_count_dict = {}
    for id in ids:
        msg_count_dict.update({id: 0})
    bus_msg_counter.update({bus: msg_count_dict})


def simple_print():
    for key in bus_msg_counter.keys():
        logger.info(f'{key}:{bus_msg_counter.get(key)}')


def output_statistic(p_file):
    statistic_path = os.path.join('logs', f'Statistic_{p_file}')
    if not os.path.exists(statistic_path):
        os.makedirs(statistic_path)
    try:
        for bus, count_dict in bus_msg_counter.items():
            bus_name = bus_mapping.get(bus)
            if not bus_name:
                pdb.set_trace()
            with open(os.path.join(statistic_path, f'Statistic_{bus_name}({bus}).csv'), 'w') as s:
                s.write(f'Frame_Id(hex), Frame_Id(Dec), Count\n')
                for frame, count in count_dict.items():
                    if int(bus) in range(41, 48):  # LIN
                        hex_frame_id = "0x{:0>2x}".format(frame)
                    elif int(bus) in range(2, 13):  # CAN
                        hex_frame_id = "0x{:0>4x}".format(frame)
                    elif int(bus) == 1:  # FlexRay
                        hex_frame_id = "0x{:0>8x}".format(frame)
                    s.write(f'{hex_frame_id}, {frame}, {count}\n')
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/cdd_tools/pcap_reader.py")
        logger.error(str(e))


class PKG:
    def __init__(self, line_num):
        self.line_num = line_num
        self.dst = None
        self.src = None
        self.proto = None
        self.dst_port = None
        self.src_port = None
        self.raw_data = None


def frame_id_check(bus_id, frame_id):
    # if int(bus_id, 16) in range(41, 48):  # if LIN, & 0x3f
    #     frame_id = frame_id & 0x3f
    if frame_id in bus_msg_id_dict.get(str(int(bus_id, 16))):
        # pdb.set_trace()
        bus_msg_counter.get(str(int(bus_id, 16)))[frame_id] += 1
        error_str = ""
    else:
        error_str = f"frame_id: {frame_id} not in bus: {bus_id}"
    return error_str


def ms_ts_check(ms):
    ms = int(''.join(ms), 16)
    error_str = ""
    if ms > 1010:  # ms should not larger than 1000
        error_str = f"ms time should not large than 1000, actual {ms}"
    return error_str


def frame_length_check(bus_id, f_len):
    error_str = ""
    if int(''.join(f_len), 16) == 0:
        error_str = f"frame length error: {f_len}"
    else:
        if int(bus_id, 16) in range(41, 48):  # LIN
            if int(''.join(f_len), 16) > 8:  # 暂且认为LIN长度不超过8
                error_str = f"frame length error: {f_len} for LIN: {bus_id}"
        elif int(bus_id, 16) in range(2, 13):  # CAN&CAN FD
            if int(''.join(f_len), 16) > 64:
                error_str = f"frame length error: {f_len} for CAN: {bus_id}"
        elif int(bus_id, 16) == 1:  # FlexRay
            if int(''.join(f_len), 16) > 32:
                error_str = f"frame length error: {f_len} for FlexRay: {bus_id}"
    return error_str


def check_cdd_raw_format(raw_data_str):
    check_result = True
    # raw_data = [raw_data_str[i:i + 2] for i in range(0, len(raw_data_str), 2)]
    raw_data = raw_data_str
    global start_pos
    global parse_info_str
    start_pos = 0
    # parse_info_str = f'原始数据（长度: {len(raw_data)}): {raw_data_str} \n'
    parse_info_str = f'原始数据（长度: {len(raw_data)})\n'
    time_stampe, raw_data = get_data(raw_data, 6)

    def get_position(data):  # get start & end byte position
        global start_pos
        pos = f'[{start_pos}-{len(data) + start_pos - 1}]'
        start_pos = start_pos + len(data)
        return pos

    parse_info_str += f'全局时钟{get_position(time_stampe)}: {time_stampe}\n'
    try:
        while len(raw_data) > 0:
            # print("=" * 40)
            parse_info_str += "{}\n".format("=" * 40)
            # get bus_id and check
            bus_id_raw, raw_data = get_data(raw_data, 1)  # bus id是1byte
            bus_id = bus_id_raw[0]
            if int(bus_id, 16) == 254 and len(raw_data) == 0:  # 结束符
                break
            check_str = gen_comment(bus_id_check(bus_id_raw))
            parse_info_str += f'总线编号{get_position(bus_id_raw)}:{bus_id_raw} {check_str} \n'
            if check_str != "":
                check_result = False
                break
            # fetch frame_id by bus_id and check
            global f_id
            left_length = len(raw_data)
            if int(bus_id, 16) in range(41, 48):  # lin, 报文id为1byte
                f_id, raw_data = get_data(raw_data, 1)
            elif int(bus_id, 16) in range(2, 13):  # CAN/CANFD, 报文ID为2byte
                f_id, raw_data = get_data(raw_data, 2)
            elif int(bus_id, 16) == 1:  # FR, 报文id为4byte
                f_id, raw_data = get_data(raw_data, 4)
                parse_info_str += "{}\n".format("**" * 40)
                parse_info_str += "FR 报文\n"
                parse_info_str += "{}\n".format("**" * 40)
            f_id_int = int(''.join(f_id), 16)
            check_str = gen_comment(frame_id_check(bus_id, f_id_int))
            parse_info_str += f'报文ID{get_position(f_id)}:{f_id}  {check_str} \n'
            if check_str != "":
                check_result = False
                break
            # fetch ms and check
            ms_ts, raw_data = get_data(raw_data, 2)  # ms时间戳 2 byte
            check_str = gen_comment(ms_ts_check(ms_ts))
            parse_info_str += f'毫秒时间戳{get_position(ms_ts)}: {ms_ts} \n'
            if check_str != "":
                check_result = False
                break
            # fetch frame length and check
            f_len, raw_data = get_data(raw_data, 1)  # 报文长度 1 byte
            check_str = gen_comment(frame_length_check(bus_id, f_len))
            parse_info_str += f'报文长度{get_position(f_len)}: {f_len} {check_str} \n'
            if check_str != "":
                check_result = False
                break
            f_len = int(f_len[0], 16)
            if len(raw_data) <= f_len:
                check_result = False
                parse_info_str += f'# 报文剩余长度：{len(raw_data)} 小于报文长度：{f_len}\n'
            f_data, raw_data = get_data(raw_data, f_len)
            parse_info_str += f'报文内容{get_position(f_data)}:{f_data} \n'
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/cdd_tools/pcap_reader.py")
        logger.error(str(e))
    finally:
        return check_result, parse_info_str


def dump_pkg(pkg, pkg_inst):
    # logger.info(pkg.name)
    for f in pkg.fields_desc:
        # logger.info("{}: {}".format(f.name, pkg.getfieldval(f.name)))
        if pkg.name == 'Ethernet':
            if f.name == 'dst':
                pkg_inst.dst = pkg.getfieldval(f.name)
            elif f.name == 'src':
                pkg_inst.src = pkg.getfieldval(f.name)
            else:
                pass
        if pkg.name == 'UDP':
            pkg_inst.proto = 'UDP'
            if f.name == 'sport':
                pkg_inst.src_port = pkg.getfieldval(f.name)
            elif f.name == 'dport':
                pkg_inst.dst_port = pkg.getfieldval(f.name)
            else:
                pass
        if isinstance(pkg.getfieldval(f.name), bytes):
            # 判读源mac地址、目标mac地址、源port、目标port
            if pkg_inst.dst == DST_MAC and pkg_inst.src == SRC_MAC and pkg_inst.dst_port == DST_PORT and pkg_inst.src_port == SRC_PORT and pkg_inst.proto == "UDP":
                r_data = pkg.getfieldval(f.name).hex()
                check_rslt, parse_info = check_cdd_raw_format(r_data)
                if check_rslt == False:
                    logger.error(f'CDD check error: Line-{pkg_inst.line_num}\n Parse info:{parse_info}')
                else:
                    logger.info(f'CDD check info: Line-{pkg_inst.line_num}\n Parse info:{parse_info}')
                    # logger.info(f'CDD check success: Line-{pkg_inst.line_num}')
    if pkg.payload:
        dump_pkg(pkg.payload, pkg_inst)


def read_pcap(p_file):
    logger.info(f"Parsing check check: {p_file}")
    pcaps = rdpcap(p_file)
    print(pcaps)
    for i in range(len(pcaps)):
        # for i in range(10):
        pkg_inst = PKG(i + 1)  # wireshark No.从1 开始
        # logger.info("************Line No.: {}***************".format(i))
        pkg = pcaps[i]
        dump_pkg(pkg, pkg_inst)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="CDD data parser from pcap file")
    parser.add_argument('-f', type=str, help='f: pcap file path')
    args = parser.parse_args()
    p_file = args.f
    read_pcap(p_file)
    output_statistic(p_file)
    simple_print()
