# -*- coding: utf-8 -*-
"""
@File        : dbc_parser.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2021-4-26 21:54
@Description : Generate cyclic json file and DBC class file
"""


import os
import re
import sys
import inspect
import argparse

current_path = os.path.dirname(os.path.realpath(__file__))
from pathlib import Path
from xat_ecu.legacy.tools.scripts_generator.dbc_core import DbcCore
from xat_ecu.legacy.tools.scripts_generator.ldf_core import LdfCore
from xat_ecu.legacy.tools.scripts_generator.bus_core_base import BusCoreBase
from xat_ecu.legacy.sdk.can_lin.pcan import Pcan
from xat_ecu.legacy.sdk.bus_app import PcanApp
from xat_ecu.legacy.sdk.can_lin.pcan_const import PcanConst


# # Used in get_lin_file_num() and get_cls_name().g
# lin_regexp = re.compile(r"lin(\d+)", re.IGNORECASE)

# sort_funcs = {
#     "can": lambda filename: filename,
#     "lin": lambda filename: get_lin_file_num(filename)
# }
# bus_file_ext_filenames_to_bus_names_map = None


# def get_lin_file_num(filename):
#     # Hard code here for this situation.
#     # If can be sure what's different between CGW and BGM, update it
#     if "Force" in filename or "NT2" in filename or filename.split(".")[0].endswith("lin"):
#         return bus_file_ext_filenames_to_bus_names_map[filename]

#     m = BusCoreBase.lin_regexp.search(filename)

#     lin_file_num = m.group(1)

#     return int(lin_file_num)

def generate_all_cyc_json_and_bus_cls_files_helper(
    car_platform, cgw_ver, bus_type_enum, partial_paths, parent_dir, ecu_under_test_name_only = True):

    print("\nProcessing {}[dut_ver={}].{} files:".format(car_platform.upper(), cgw_ver, bus_type_enum.name))

    if partial_paths["json"] is None:  # LIN has no .json files.
        json_dir = None
    else:
        json_dir = os.path.join(parent_dir, partial_paths["json"])

    buses_dir = os.path.join(parent_dir, partial_paths["bus"])
    cls_dir = os.path.join(parent_dir, partial_paths["cls"])
    ecu_under_test_name = partial_paths["ecu_under_test"]

    bus_files = os.listdir(buses_dir)


    bus_names_to_bus_file_ext_filenames_map = \
        Pcan.get_bus_names_to_bus_ext_filenames_map(buses_dir, car_platform)


    # We need the inverted version of the dict above, so flop everything around here.
    # Make it global for use of the sorting function up above.
    #
    global bus_file_ext_filenames_to_bus_names_map

    print(bus_names_to_bus_file_ext_filenames_map)
    bus_file_ext_filenames_to_bus_names_map = \
        {bus_file_name: bus_name.capitalize()
            for bus_name, bus_file_name in bus_names_to_bus_file_ext_filenames_map.items()}

    # TODO: Ideally somehow combine the sort_func()'s here with the ones in class BusCoreBase (?).
    #
    # for bus_file_name in sorted(bus_files, key=sort_funcs[bus_type_enum.value]):
    for bus_file_name in sorted(bus_files):
        if bus_file_name in bus_file_ext_filenames_to_bus_names_map:
            target_cls_name = bus_file_ext_filenames_to_bus_names_map[bus_file_name]
        else:
            continue

        target_cls_file_path = "{}.py".format(os.path.join(cls_dir, target_cls_name.lower()))

        if bus_type_enum.value == PcanConst.BusType.CAN.value:
            core_obj = DbcCore(target_cls_name.lower(), os.path.join(buses_dir, bus_file_name), None)
        elif bus_type_enum.value == PcanConst.BusType.LIN.value:
            core_obj = LdfCore(target_cls_name.lower(), os.path.join(buses_dir, bus_file_name), None)
        else:
            core_obj = None

        if json_dir is not None:
            
            cyc_msg_dict = core_obj.get_cyclic_msg_dict(ecu_under_test_name, ecu_under_test_name_only = ecu_under_test_name_only)
            if ecu_under_test_name.upper() == "ALL":
                json_dir = os.path.join(json_dir, target_cls_name.upper())
                PcanApp.create_test_file_dir_if_absent(json_dir)
                for tx_ecu in cyc_msg_dict.keys():
                    target_json_file_path = "{}.json".format(os.path.join(json_dir, tx_ecu.lower()))
                    core_obj.write_cyc_msg_to_file(cyc_msg_dict[tx_ecu], target_json_file_path)
            else:
                PcanApp.create_test_file_dir_if_absent(json_dir)
                if ecu_under_test_name_only:
                    target_json_file_path = "{}.json".format(os.path.join(json_dir, target_cls_name.lower() + "_" + ecu_under_test_name.lower()))
                    core_obj.write_cyc_msg_to_file(cyc_msg_dict, target_json_file_path)
                else:
                    target_json_file_path = "{}.json".format(os.path.join(json_dir, target_cls_name.lower() + "_not_" + ecu_under_test_name.lower()))
                    core_obj.write_cyc_msg_to_file(cyc_msg_dict, target_json_file_path)

        cls_dict = core_obj.get_cls_dict()

        class_hierarchy_def_file_lines = \
            core_obj.get_cls_hierarchy_def_file_content(cls_dict, target_cls_name)

        PcanApp.create_test_file_dir_if_absent(cls_dir)

        core_obj.write_cls_list_to_file(class_hierarchy_def_file_lines, target_cls_file_path)


if __name__ == "__main__":
    path_tail = "compass/xat_ecu/legacy/tools/scripts_generator"
    scripts_path = Path(os.getcwd()).as_posix()
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--pcan_type', choices=("Default"), help='pcan_type will be used.', default="Default")
    # Default is All
    args = argparser.parse_args()
    assert scripts_path.endswith(path_tail), "Before running this script:\ncd {}".format(path_tail)
    if args.pcan_type == 'Default':
        can = PcanApp
    dut_path = os.path.dirname(inspect.getfile(can))
    can.call_car_platform_dut_ver_bus_type_partial_paths_parent_dir_handler(
        generate_all_cyc_json_and_bus_cls_files_helper, dut_path, 
        ecu_under_test_name_only=False, return_only_default_dut_ver=True)

