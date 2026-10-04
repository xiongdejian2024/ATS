# -*- coding: utf-8 -*-
"""
@File        : det_parser.py
@Author      : lei.tao
@Time        : 2022/12/26 22:32
@Description : 
@Examples    :
"""
import os
import argparse
import sys
import time
from typing import Union

from det_def import *
project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)


def get_info(file):
    """
    获取Response响应的16进制信息
    """
    with open(file, 'r', encoding='utf-8') as fd:
        data = fd.read()
        for i in data.split('\n'):
            if 'Response' in i:
                return i.split(': ')[1].split(' ')


def get_data(r_data, dl):
    data = r_data[:dl]
    raw_data = r_data[dl:]
    return data, raw_data


def paser_det_log(_type, file):
    data = []
    if _type == "-f":
        data = get_info(file)
    elif _type == "-s":
        data = file.strip().split(' ')
        if data[0] != '1002':
            data = ['1002', '62', 'F1', 'EE'] + data
        else:
            data = data
    else:
        return "Argparse Argument Error"

    if len(data) < 28:
        return "Response Messages Length Error"
    else:
        if data[:4] == ['1002', '62', 'F1', 'EE']:
            version = int(data[7], 16)
            parse_info_str = "log version: {}\n".format(version)
            err, raw_data = get_data(data, 8)
            j = 1
            try:
                while len(raw_data) >= 20:

                    data_log, raw_data = get_data(raw_data, 20)
                    for i in range(20):
                        if data_log[i] != '00':
                            parse_info_str += "=" * 40 + f"DET Error log {j}" + "=" * 40 + "\n"
                            parse_info_str += "original bytes: {}\n".format(' '.join(data_log))
                            Module_id = str(data_log[1]) + str(data_log[0])
                            mod_id = int(Module_id, 16)
                            Module = BswModule(mod_id).name
                            if not Module:
                                exit('Please Check Response Messages')
                            else:
                                if mod_id == 56:
                                    parse_info_str += "Module: {}, id: {}, Please Follow McuDetReserve Byte0-Byte4\n".format(Module, mod_id)
                                else:
                                    parse_info_str += "Module: {}, id: {}\n".format(Module, mod_id)
                                parse_info_str += "InstanceId: {}\n".format(int(data_log[2], 16))
                                api_id = int(data_log[3], 16)
                                error_id = int(data_log[4], 16)
                                model, api, error = paser_det_id(mod_id, api_id, error_id)
                                parse_info_str += "Api name: {}, id: {}\n".format(api, api_id)
                                parse_info_str += "Error name: {}, id: {}\n".format(error, error_id)
                                parse_info_str += "ReportType: {}\n".format(int(data_log[5], 16))
                                Occurr_Time = str(data_log[9]) + str(data_log[8]) + str(data_log[7]) + str(data_log[6])
                                parse_info_str += "OccurrTime: {}\n".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(Occurr_Time, 16))))
                                McuDet = str(data_log[11]) + str(data_log[10])
                                parse_info_str += "McuDetSpeed: {}\n".format(int(McuDet, 16))
                                parse_info_str += "McuDetVoltage: {}\n".format(int(data_log[12], 16))
                                parse_info_str += "McuDetUsgMode: {}\n".format(int(data_log[13], 16))
                                McuDetOdoMeter = str(data_log[15]) + str(data_log[14])
                                parse_info_str += "McuDetOdoMeter: {}\n".format(int(McuDetOdoMeter, 16))
                                # 解析McuDetReserve
                                parse_info_str += "McuDetReserve_Byte0: {}, McuDetReserve_Byte1: {}, McuDetReserve_Byte2: " \
                                                  "{}, McuDetReserve_Byte3: {}\n".format(data_log[16], data_log[17],
                                                                                         data_log[18], data_log[19])
                                break

                    j += 1

            except Exception:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/det_parser/det_parser.py")
                raise Exception

            finally:
                return parse_info_str

        else:
            return "Response Messages Data Error"


if __name__ == '__main__':
    """
    添加输入参数
    
    parser = argparse.ArgumentParser(description="DET Log parser from BSW Det Info")
    parser.add_argument('-f', type=str, help='f: log file path')
    parser.add_argument('-s', type=str, help='f: log data')
    args = parser.parse_args()
    log_path = args.f
    log_data = args.s
    info_str = paser_det_log(log_path)
    print(info_str)
    info_int = paser_det_log(log_data)
    print(info_int)
    """

    """
    打包成exe执行文件
    log_path = input("DET log file path: ")
    info_str = paser_det_log(log_path)
    print(info_str)
    """
    # # 与平台联调
    if len(sys.argv) == 3:
        info_file = paser_det_log(sys.argv[1], sys.argv[2])
        print(info_file)

    else:
        print("Please input the original bytes")
