# -*- coding: utf-8 -*-
"""
@File        : get_version.py
@Author      : dejian.xiong@jiduauto.com
@Time        : 2024/06/12 15:00
@Description : 
@Examples    :
"""
import time
from enum import Enum

from xat_ecu.legacy.sdk.ethernet.doip_client_sim_odx import Doip_Client_Sim_Odx

from framework.automotive.utils.bench_helper import BenchHelper
from framework.automotive.utils.data_type import Domain


class Target(Enum):
    bgm = 'bgm'
    tcam = 'tcam'
    cdc = 'cdc'
    acu = 'acu'
    boot = 'boot'
    mcu = 'mcu'
    switch = 'switch'


def get_uds_data(data_list):
    if data_list:
        data = data_list[0].split(' ')
        if data[0:3] == ['62', 'F1', 'AE']:
            left = data[4:9]
            mid = data[9]
            right = data[10:12]
            if mid == '20':
                return f"{''.join(left)}{chr(int(right[0], 16))}{chr(int(right[1], 16))}"
            else:
                return f"{''.join(left)}{chr(int(mid, 16))}{chr(int(right[0], 16))}{chr(int(right[1], 16))}"


def get_boot_data(data_list):
    if data_list:
        data = data_list[0].split(' ')
        if data[0:3] == ['62', 'F1', 'AE']:
            left = data[-8:-3]
            right = data[-2:]
            return f"{''.join(left)}{chr(int(right[0], 16))}{chr(int(right[1], 16))}"


def get_diag_info(version_list, ecu, server_ip):
    doip_client = Doip_Client_Sim_Odx(ecu=ecu, server_doip_id=0x1fff, server_ip=server_ip)
    doip_client.run()  # 建立TCP链接
    version_dict = {}
    doip_client.send_data([0x22, 0xF1, 0xAE])
    data_dict = doip_client.return_function_userdata_and_check_response(timeout=1)
    for target in version_list:
        if target == Target.bgm:
            version_dict[Target.bgm.value] = get_uds_data(data_dict.get('10 01'))
        if target == Target.tcam:
            version_dict[Target.tcam.value] = get_uds_data(data_dict.get('10 11'))
        if target == Target.cdc:
            version_dict[Target.cdc.value] = get_uds_data(data_dict.get('12 01'))
        if target == Target.acu:
            version_dict[Target.acu.value] = get_uds_data(data_dict.get('14 01'))
        if target == Target.boot:
            version_dict[Target.boot.value] = get_boot_data(data_dict.get('10 01'))
        if target == Target.mcu:
            doip_client.send_data([0x22, 0xF1, 0xF0])
            time.sleep(1)
            data_list = doip_client.retrun_udsdata_and_check_response()
            if data_list[0]:
                data_hex = bytes(data_list[1]).hex()
                # 第一个字节  1ASCII+5BCD+3ASCII
                fr = chr(int(data_hex[0:2], 16))
                mid = data_hex[2:12]
                ver_str = data_hex[-4:]
                ver = chr(int(ver_str[0:2], 16)) + chr(int(ver_str[2:4], 16))
                mcu_ver = (fr + mid + ver).upper()
                version_dict[Target.mcu.value] = mcu_ver
        if target == Target.switch:
            doip_client.send_data([0x22, 0xFD, 0x50])
            time.sleep(1)
            data_list = doip_client.retrun_udsdata_and_check_response()
            if data_list[0]:
                data_hex = bytes(data_list[1]).hex()
                new_data = data_hex[6:]
                ver_str = new_data[-12:]
                bytes_list = [chr(int(ver_str[i:i + 2], 16)) for i in range(0, len(ver_str), 2)]
                ver = ''.join(bytes_list)
                switch_ver = ver.upper()
                version_dict[Target.switch.value] = switch_ver
    print(version_dict)
    return version_dict


def get_version():
    # 获取当前domain
    bh = BenchHelper()
    tb_config = bh.get_tbcfg(tbcfg='')
    domain: Domain = bh.get_bench_domain_info(tb_config)
    if domain.single_bgm:
        ecu = "BGM"
        server_ip = "169.254.19.1"
        get_diag_info(version_list=[Target.bgm, Target.boot, Target.mcu, Target.switch], ecu=ecu, server_ip=server_ip)
    elif domain.single_tcam:
        ecu = "TCAM"
        server_ip = "172.16.9.31"
        get_diag_info(version_list=[Target.tcam], ecu=ecu, server_ip=server_ip)
    elif domain.two_domain:
        ecu = "BGM"
        server_ip = "169.254.19.1"
        get_diag_info(version_list=[Target.bgm, Target.mcu, Target.switch, Target.boot, Target.tcam], ecu=ecu,
                      server_ip=server_ip)
    elif domain.four_domain:
        ecu = "BGM"
        server_ip = "169.254.19.1"
        get_diag_info(
            version_list=[Target.bgm, Target.mcu, Target.switch, Target.boot, Target.tcam, Target.cdc, Target.acu],
            ecu=ecu, server_ip=server_ip)


if __name__ == '__main__':
    get_version()
