# -*- coding: utf-8 -*-
"""
@File        : get_frame_bus_ids.py.py
@Author      : jinhui.zhao@jiduauto.com
@Time        : 2022/5/12 2:27
@Description : 
@Examples    :
"""

import os
import re
import sys
import json

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

from xat_ecu.legacy.common.logger import logger


FILE_BUS_ID_MAP = {
    'FlexRay.py': 1,
    'infocanfd.py': 2,
    'adcanfd.py': 3,
    'propulsioncan.py': 4,
    'chassiscan1.py': 5,
    'chassiscan2.py': 6,
    'passivesafetycan.py': 7,
    'connectivitycanfd.py': 8,
    'bodycan.py': 9,
    'bodyexposedcanfd.py': 10,
    'bodyalmcanfd1.py': 11,
    'bodyalmcanfd2.py': 12,
    'cem_lin1.py': 41,
    'cem_lin2.py': 42,
    'cem_lin3.py': 43,
    'cem_lin4.py': 44,
    'cem_lin5.py': 45,
    'cem_lin6.py': 46,
    'cem_lin7.py': 47,
}

MSG_ID_REG = re.compile(r'msg_id = (\d+)')


def get_files(path):
    return os.listdir(path)


def get_bus_id_msg_ids(folder, file_name):
    bus_id = None
    ids = []
    file_path = os.path.join(folder, file_name)
    if file_name in FILE_BUS_ID_MAP.keys():
        bus_id = FILE_BUS_ID_MAP.get(file_name)
    else:
        logger.error(f"un-recognized file: {file_name}")
        return bus_id, ids
    try:
        with open(file_path, 'r') as fp:
            for line in fp:
                re_obj = MSG_ID_REG.search(line)
                if re_obj:
                    ids.append(int(re_obj.group(1).strip()))
                else:
                    continue
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/cdd_tools/get_frame_bus_ids.py")
        logger.error(str(e))
    logger.debug(f'{bus_id}: {ids}')
    return bus_id, ids


def get_bus_msg_id_json(f_dir):
    f_list = get_files(f_dir)
    print(f_list)
    bus_msg_map = {}
    print(FILE_BUS_ID_MAP.keys())
    for f in f_list:
        if f in FILE_BUS_ID_MAP.keys():
            bus_id, msg_id_list = get_bus_id_msg_ids(f_dir, f)
            if bus_id and msg_id_list != []:
                bus_msg_map.update({bus_id: msg_id_list})
    logger.debug(bus_msg_map)
    return bus_msg_map


if __name__ == "__main__":
    folder = 'files'
    bus_msg_dict = get_bus_msg_id_json(folder)
    print(bus_msg_dict)
    f = open('bus_msg_ids.json', 'w')
    f.write(json.dumps(bus_msg_dict, indent=4))
    f.close()
