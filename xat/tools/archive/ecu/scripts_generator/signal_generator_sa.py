# -*- coding: utf-8 -*-
"""
@File        : signal_generator_sa.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2021/06/25 09:25 AM
@Description : description about this file
@Examples    : example of how to use it
"""

import os
import sys
from xat_ecu.legacy.sdk.dbc_cls.force.v1_0_0.bta import Bta
import inspect
from xat_ecu.legacy.sdk.dut.sa.bta_not_sa_sim import Sa_Sim


class SignalGenerator:
    def __init__(self):
        self.bus_all_class_list = dir(Bta)
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
        self.normal_cycle_message_list = [cycle_message for cycle_message in self.all_message_list
                                   if getattr(Bta, cycle_message).msg_cyc != 0.0]
        return self.normal_cycle_message_list

    def get_normal_crc_cycle_message_list(self):
        self.normal_crc_cycle_message_list = []
        self.normal_exclude_crc_cycle_message_list = []
        self.get_normal_cycle_message_list()
        for cycle_message in self.normal_cycle_message_list:
            cycle_message_class = getattr(Bta, cycle_message)
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
            cycle_message_class = getattr(Bta, cycle_message)
            if cycle_message_class.tx_node != ['SA']:
                for signal in dir(cycle_message_class):
                    if "__" not in signal:
                        signal_class = getattr(cycle_message_class, signal)
                        for signal_value in dir(signal_class):

                            if "__" not in signal_value and "v_" in signal_value:
                                func_name = "bta" + "_" + cycle_message + "_" + signal + "_" + signal_value
                                func_name = func_name.lower()
                                self.exclude_crc_signal_combination_list.append(
                                    [cycle_message, signal, signal_value, func_name])
        return self.exclude_crc_signal_combination_list

    def get_crc_signal_combination(self):
        # crc_cycle_message Excluding SA
        self.crc_signal_combination_list = []
        self.get_normal_crc_cycle_message_list()
        for cycle_message in self.normal_crc_cycle_message_list:
            cycle_message_class = getattr(Bta, cycle_message)
            if cycle_message_class.tx_node != ['SA']:
                for signal in dir(cycle_message_class):
                    if "__" not in signal:
                        signal_class = getattr(cycle_message_class, signal)
                        for signal_value in dir(signal_class):
                            if "__" not in signal_value and "v_" in signal_value:
                                func_name = "bta" + "_" + cycle_message + "_" + signal + "_" + signal_value
                                func_name = func_name.lower()
                                self.crc_signal_combination_list.append([cycle_message, signal, signal_value, func_name])
        return self.crc_signal_combination_list

    def automatic_signal_generation(self):
        self.crc_signal_combination_list = []
        self.exclude_crc_signal_combination_list = []
        self.get_exclude_crc_signal_combination()
        self.get_crc_signal_combination()
        sa_sim_path = os.path.dirname(inspect.getfile(Sa_Sim))
        with open(sa_sim_path + "/bta_not_sa_sim.py", "a") as f:
            for exclude_crc_signal_combination in self.exclude_crc_signal_combination_list:
                exclude_crc_signal_combination[0] = "self.pcan.dbc.bta." + exclude_crc_signal_combination[0]
                f.write("\n")
                f.write("    " + "def " + exclude_crc_signal_combination[3] + "(self):\n")
                f.write("        # Automatically generated code, please do not modify\n")
                f.write("        " + "self.set({}, '{}', '{}')\n".format(exclude_crc_signal_combination[0],
                                                                        exclude_crc_signal_combination[1],
                                                                        exclude_crc_signal_combination[2]))
            for exclude_crc_signal_combination in self.crc_signal_combination_list:
                exclude_crc_signal_combination[0] = "self.pcan.dbc.bta." + exclude_crc_signal_combination[0]
                f.write("\n")
                f.write("    " + "def " + exclude_crc_signal_combination[3] + "(self):\n")
                f.write("        # Automatically generated code, please do not modify\n")
                f.write("        " + "self.set_with_crc8({}, '{}', '{}')\n".format(exclude_crc_signal_combination[0],
                                                                        exclude_crc_signal_combination[1],
                                                                        exclude_crc_signal_combination[2]))
            f.close()

    def automatic_assert_signal_generation(self):
        # To Do
        self.crc_signal_combination_list = []
        self.exclude_crc_signal_combination_list = []
        self.get_exclude_crc_signal_combination()
        self.get_crc_signal_combination()
        sa_sim_path = os.path.dirname(inspect.getfile(Sa_Sim))
        with open(sa_sim_path + "/bta_not_sa_sim.py", "a") as f:
            for exclude_crc_signal_combination in self.exclude_crc_signal_combination_list:
                exclude_crc_signal_combination[0] = "self.pcan.dbc.bta." + exclude_crc_signal_combination[0]
                f.write("\n")
                f.write("    " + "def " + exclude_crc_signal_combination[3] + "(self):\n")
                f.write("        # Automatically generated code, please do not modify\n")
                f.write("        " + "self.set({}, '{}', '{}')\n".format(exclude_crc_signal_combination[0],
                                                                         exclude_crc_signal_combination[1],
                                                                         exclude_crc_signal_combination[2]))
            f.close()

if __name__ == "__main__":
    # Note: the import path of BTA     #### Line 18
    # Running directly can generate in bta_not_sa_sim.py
    a = SignalGenerator()
    a.automatic_signal_generation()
    print("end")
