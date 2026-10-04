# -*- coding: utf-8 -*-
"""
@File        : signal_generator_ecu.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2022/01/25 09:25 AM
@Description : description about this file
@Examples    : example of how to use it
"""

import os
import sys
import inspect
from xat_ecu.legacy.ecu_sim.ecu_sim_auto import EcuSimAuto
import importlib
from xat_ecu.legacy.sdk.can_lin.pcan_const import PcanConst


class SignalGenerator:
    def __init__(self, bus_obj, bus_name):
        # bus_obj:      such as   <class 'sdk.dbc_cls.force.bl050.bta.Bta'>
        # bus_name:     "bta"
        self.can_lin = "dbc"
        self.bus_obj = bus_obj
        self.bus_name = bus_name.lower()
        self.bus_all_class_list = dir(self.bus_obj)
        self.all_message_list = []
        # self.cycle_message_list = []
        self.normal_cycle_message_list = []
        self.normal_exclude_crc_cycle_message_list = []
        self.normal_crc_cycle_message_list = []
        self.crc_tag = None
        self.crc_signal_combination_list = []
        self.exclude_crc_signal_combination_list = []

    def get_normal_cycle_message_list(self):
        self.all_message_list = [all_message
                                 for all_message in self.bus_all_class_list if "__" not in all_message]
        if self.bus_name in PcanConst.BGM_CAN_BUS_LIST:
            self.normal_cycle_message_list = [cycle_message for cycle_message in self.all_message_list
                                       if getattr(self.bus_obj, cycle_message).msg_cyc != 0.0]
            self.can_lin = "dbc"
        elif self.bus_name in PcanConst.BGM_LIN_BUS_LIST:
            self.normal_cycle_message_list = [cycle_message for cycle_message in self.all_message_list
                                              if getattr(self.bus_obj, cycle_message).msg_cyc != 0]
            self.can_lin = "ldf"
            if self.bus_name == "ad":
                print(self.bus_name)
                print(self.all_message_list)
                print(self.bus_obj)
                print(self.normal_cycle_message_list)
        return self.normal_cycle_message_list

    def get_normal_crc_cycle_message_list(self):
        self.normal_crc_cycle_message_list = []
        self.normal_exclude_crc_cycle_message_list = []
        self.get_normal_cycle_message_list()
        for cycle_message in self.normal_cycle_message_list:
            cycle_message_class = getattr(self.bus_obj, cycle_message)
            for signal in dir(cycle_message_class):
                if "_CRC" in signal:
                    self.crc_tag = True
            if self.crc_tag:
                self.normal_crc_cycle_message_list.append(cycle_message)
            else:
                self.normal_exclude_crc_cycle_message_list.append(cycle_message)
            self.crc_tag = None
        return self.normal_crc_cycle_message_list

    def get_normal_exclude_crc_cycle_message_list(self):
        self.normal_crc_cycle_message_list = []
        self.normal_exclude_crc_cycle_message_list = []
        self.get_normal_crc_cycle_message_list()
        return self.normal_exclude_crc_cycle_message_list

    def get_exclude_crc_signal_combination(self):
        # exclude_crc_cycle_message Excluding SA
        self.exclude_crc_signal_combination_list = []
        self.get_normal_exclude_crc_cycle_message_list()
        for cycle_message in self.normal_exclude_crc_cycle_message_list:
            cycle_message_class = getattr(self.bus_obj, cycle_message)
            # if cycle_message_class.tx_node != ['BGM']:
            for signal in dir(cycle_message_class):
                if "__" not in signal:
                    signal_class = getattr(cycle_message_class, signal)
                    v_flag = False
                    for signal_value in dir(signal_class):
                        if "__" not in signal_value and "v_" in signal_value:
                            v_flag = True
                            func_name = self.bus_name + "_" + cycle_message + "_" + signal + "_" + signal_value
                            func_name = func_name.lower()
                            self.exclude_crc_signal_combination_list.append(
                                [cycle_message, signal, signal_value, func_name])
                    if not v_flag:
                        signal_value = "value"
                        func_name = self.bus_name + "_" + cycle_message + "_" + signal
                        func_name = func_name.lower()
                        self.exclude_crc_signal_combination_list.append([cycle_message, signal, signal_value, func_name])
        return self.exclude_crc_signal_combination_list

    def get_crc_signal_combination(self):
        # crc_cycle_message Excluding SA
        self.crc_signal_combination_list = []
        self.get_normal_crc_cycle_message_list()
        for cycle_message in self.normal_crc_cycle_message_list:
            cycle_message_class = getattr(self.bus_obj, cycle_message)
            # if cycle_message_class.tx_node != ['BGM']:
            for signal in dir(cycle_message_class):
                if "__" not in signal:
                    signal_class = getattr(cycle_message_class, signal)
                    v_flag = False
                    for signal_value in dir(signal_class):
                        if "__" not in signal_value and "v_" in signal_value:
                            v_flag = True
                            func_name = self.bus_name + "_" + cycle_message + "_" + signal + "_" + signal_value
                            func_name = func_name.lower()
                            self.crc_signal_combination_list.append([cycle_message, signal, signal_value, func_name])
                    if not v_flag:
                        signal_value = "value"
                        func_name = self.bus_name + "_" + cycle_message + "_" + signal
                        func_name = func_name.lower()
                        self.crc_signal_combination_list.append([cycle_message, signal, signal_value, func_name])
        return self.crc_signal_combination_list

    def automatic_signal_generation(self):
        self.crc_signal_combination_list = []
        self.exclude_crc_signal_combination_list = []
        self.get_exclude_crc_signal_combination()
        self.get_crc_signal_combination()
        ecu_sim_auto_path = os.path.dirname(inspect.getfile(EcuSimAuto))
        with open(ecu_sim_auto_path + "/ecu_sim_auto.py", "a") as f:
            for exclude_crc_signal_combination in self.exclude_crc_signal_combination_list:
                exclude_crc_signal_combination[0] = "self.pcan.{}.{}.".format(self.can_lin, self.bus_name) + exclude_crc_signal_combination[0]
                f.write("\n")
                if exclude_crc_signal_combination[2] != "value":
                    f.write("    " + "def " + exclude_crc_signal_combination[3] + "(self):\n")
                    # f.write("        # Automatically generated code, please do not modify\n")
                    f.write("        " + "self.set({}, '{}', '{}')\n".format(exclude_crc_signal_combination[0],
                                                                            exclude_crc_signal_combination[1],
                                                                            exclude_crc_signal_combination[2]))
                else:
                    f.write("    " + "def " + exclude_crc_signal_combination[3] +
                            "(self, " + exclude_crc_signal_combination[2] + "):\n")
                    # f.write("        # Automatically generated code, please do not modify\n")
                    f.write(
                        "        " + "self.set_with_crc8({}, '{}', {})\n".format(exclude_crc_signal_combination[0],
                                                                                 exclude_crc_signal_combination[1],
                                                                                 exclude_crc_signal_combination[2]))
            for exclude_crc_signal_combination in self.crc_signal_combination_list:
                exclude_crc_signal_combination[0] = "self.pcan.{}.{}.".format(self.can_lin, self.bus_name) + exclude_crc_signal_combination[0]
                f.write("\n")
                if exclude_crc_signal_combination[2] != "value":
                    f.write("    " + "def " + exclude_crc_signal_combination[3] + "(self):\n")
                    # f.write("        # Automatically generated code, please do not modify\n")
                    f.write("        " + "self.set_with_crc8({}, '{}', '{}')\n".format(exclude_crc_signal_combination[0],
                                                                        exclude_crc_signal_combination[1],
                                                                        exclude_crc_signal_combination[2]))
                else:
                    f.write("    " + "def " + exclude_crc_signal_combination[3] +
                            "(self, " + exclude_crc_signal_combination[2] + "):\n")
                    # f.write("        # Automatically generated code, please do not modify\n")
                    f.write(
                        "        " + "self.set_with_crc8({}, '{}', {})\n".format(exclude_crc_signal_combination[0],
                                                                                   exclude_crc_signal_combination[1],
                                                                                   exclude_crc_signal_combination[2]))
        f.close()

    def automatic_assert_signal_generation(self):
        # To Do  change 'set' to 'check' ?
        self.crc_signal_combination_list = []
        self.exclude_crc_signal_combination_list = []
        self.get_exclude_crc_signal_combination()
        self.get_crc_signal_combination()
        ecu_sim_auto_path = os.path.dirname(inspect.getfile(EcuSimAuto))
        with open(ecu_sim_auto_path + "/ecu_sim_auto.py", "a") as f:
            for exclude_crc_signal_combination in self.exclude_crc_signal_combination_list:
                exclude_crc_signal_combination[0] = "self.pcan.{}.{}.".format(self.can_lin, self.bus_name) + exclude_crc_signal_combination[0]
                f.write("\n")
                f.write("   " + "def " + exclude_crc_signal_combination[3] + "(self):\n")
                # f.write("        # Automatically generated code, please do not modify\n")
                f.write("        " + "self.set({}, '{}', '{}')\n".format(exclude_crc_signal_combination[0],
                                                                         exclude_crc_signal_combination[1],
                                                                         exclude_crc_signal_combination[2]))
            f.close()

if __name__ == "__main__":
    # Running directly can generate in ecu_sim_auto.py
    # work dir : current dir
    # from sdk.dbc_cls.force.bl050.bta import Bta
    # BGM automatic_signal_generation

    ecu_sim_auto_path = os.path.dirname(inspect.getfile(EcuSimAuto))
    # ecu_sim_auto_path = "ecu_simulator/ecu_sim"
    with open(ecu_sim_auto_path + "/ecu_sim_auto.py", "w") as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write("# Automatic generation By ecu_simulator/tools/scripts_generator/signal_generator_ecu.py\n")
        f.write("# Automatically generated code, please do not modify\n")
        f.write("\n")
        f.write("\n")
        f.write("class EcuSimAuto():\n")
        f.write("    def __init__(self):\n")
        f.write("        pass\n")
    f.close()

    # DBC
    cls_full_module_name = "sdk.dbc_cls.force.bl070.dbc_cls"
    cls_module = importlib.import_module(cls_full_module_name)
    cls_module_bus = dir(cls_module)
    bus_list = [bus for bus in cls_module_bus if "__" not in bus]
    bus_list.remove('DbcCls')
    for bus_name in bus_list:
        bus_obj = getattr(cls_module,bus_name)
        a = SignalGenerator(bus_obj, bus_name)
        a.automatic_signal_generation()

    # LDF
    cls_full_module_name = "sdk.ldf_cls.force.bl070.ldf_cls"
    cls_module = importlib.import_module(cls_full_module_name)
    cls_module_bus = dir(cls_module)
    bus_list = [bus for bus in cls_module_bus if "__" not in bus]
    bus_list.remove('LdfCls')
    for bus_name in bus_list:
        bus_obj = getattr(cls_module, bus_name)
        a = SignalGenerator(bus_obj, bus_name)
        a.automatic_signal_generation()



