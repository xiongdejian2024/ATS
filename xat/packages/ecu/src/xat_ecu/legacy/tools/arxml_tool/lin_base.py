# -*- coding: utf-8 -*-
"""
@File        : lin_base.py
@Author      : jinhui.zhao@jiduauto.com
@Time        : 2022/2/22 11:55
@Description :
@Examples    :
"""

from collections import OrderedDict
from xat_ecu.legacy.tools.arxml_tool.signal_core_base import SignalCoreBase


def value_convert(func):
    def wrapper(self, args):
        if isinstance(args, str):
            arg = args
            arg = arg.replace('.', '')
            arg = arg.replace('E-', '')
            arg = arg.replace('e-', '')
            arg = arg.replace('-', '')
            if args.replace('-', '').isdigit():
                args = int(args)
            elif arg.isdigit():   
                #  such as   sig_value_factor = "9.765625E-4"   "-512.0"
                args = float(args)
        return func(self, args)
    return wrapper

class LinMessage:
    def __init__(self):
        self.msg_name = None
        self.msg_id = None
        self.msg_tx_method = None
        self.msg_cycle = None
        self.msg_length = None
        self.tx_node = None
        self.rx_nodes = []
        self.lin_signals = {}
        self.sig_group_dict = {}
        self.sig_group_dataid_dict = {}

    def set_msg_name(self, name:str):
        self.msg_name = name

    def set_sig_group_dict(self, sig_group_dict:dict):
        self.sig_group_dict = sig_group_dict

    def set_sig_group_dataid_dict(self, sig_group_dataid_dict:dict):
        self.sig_group_dataid_dict = sig_group_dataid_dict

    @value_convert
    def set_msg_id(self, msg_id:int):
        self.msg_id = msg_id

    def set_msg_tx_method(self, msg_tx_method:str):
        self.msg_tx_method = msg_tx_method

    @value_convert
    def set_msg_cycle(self, cycle:int):
        self.msg_cycle = cycle

    @value_convert
    def set_msg_length(self, length:int):
        self.msg_length = length

    def set_tx_node(self, node_name:str):
        self.tx_node = node_name

    def set_rx_nodes(self, nodes:list):
        self.rx_nodes = nodes

    def add_rx_node(self, node:str):
        self.rx_nodes.append(node)

    def remove_rx_node(self, node:str):
        pass

    def set_lin_signals(self, signals:dict):
        self.lin_signals = signals

    def add_lin_signal(self, signal):
        pass

    def remove_lin_signal_by_name(self, signal_name):
        pass

    def return_in_dict(self):
        msg_dict = OrderedDict()
        msg_dict.update({"msg_name": self.msg_name})
        msg_dict.update({"msg_id": self.msg_id})
        msg_dict.update({"msg_tx_method": self.msg_tx_method})
        msg_dict.update({"msg_cycle": self.msg_cycle})
        msg_dict.update({"msg_length": self.msg_length})
        msg_dict.update({"tx_node": self.tx_node})
        msg_dict.update({"rx_nodes": self.rx_nodes})
        msg_dict.update({"sig_group_dict": self.sig_group_dict})
        msg_dict.update({"sig_group_dataid_dict": self.sig_group_dataid_dict})
        msg_dict.update({"lin_signals": self.lin_signals})
        return msg_dict


class LinSignal:
    def __init__(self):
        self.sig_name = None
        self.sig_start_bit = None
        self.update_id_bit = None
        self.sig_length = None
        self.sig_value_factor = None
        self.sig_value_offset = None
        self.sig_value_min = None
        self.sig_value_max = None
        self.sig_value_init = None
        self.sig_value_type = None
        self.sig_value_table = None
        self.compute_method = None
        self.sig_byteorder = None
        self.sig_core_dict = {}
        self.sig_core = SignalCoreBase()

    def set_sig_name(self, name: str):
        self.sig_name = name

    def set_sig_byteorder(self, byteorder: str):
        self.sig_byteorder = byteorder

    @value_convert
    def set_sig_start_bit(self, start_bit: int):
        self.sig_start_bit = start_bit

    @value_convert
    def set_update_id_bit(self, update_id_bit: int):
        self.update_id_bit = update_id_bit

    @value_convert
    def set_sig_length(self, length: int):
        self.sig_length = length

    @value_convert
    def set_sig_value_factor(self, val_factor):
        self.sig_value_factor = val_factor

    @value_convert
    def set_sig_value_offset(self, val_offset):
        self.sig_value_offset = val_offset

    @value_convert
    def set_sig_value_min(self, val_min):
        self.sig_value_min = val_min

    @value_convert
    def set_sig_value_max(self, val_max):
        self.sig_value_max = val_max

    @value_convert
    def set_sig_value_init(self, val_init):
        self.sig_value_init = val_init

    def set_sig_value_type(self, val_type):
        self.sig_value_type = val_type

    def set_sig_value_table(self, val_table):
        self.sig_value_table = val_table

    def get_sig_core_dict(self, sig_name, sig_length, sig_start_bit):
        self.set_sig_name(sig_name)
        self.set_sig_length(sig_length)
        self.set_sig_start_bit(sig_start_bit)
        self.sig_core_dict = self.sig_core.get_signal_dict_helper(self.sig_name, self.sig_length, self.sig_start_bit, self.sig_byteorder)
        return self.sig_core_dict

    def get_sig_core_dict_easy(self):
        self.sig_core_dict = self.sig_core.get_signal_dict_helper(self.sig_name, self.sig_length, self.sig_start_bit, self.sig_byteorder)
        return self.sig_core_dict

    def return_in_dict(self):
        sig_dict = OrderedDict()
        sig_dict.update({"sig_name": self.sig_name})
        sig_dict.update({"sig_start_bit": self.sig_start_bit})
        sig_dict.update({"update_id_bit": self.update_id_bit})
        sig_dict.update({"sig_length": self.sig_length})
        sig_dict.update({"sig_value_factor": self.sig_value_factor})
        sig_dict.update({"sig_value_offset": self.sig_value_offset})
        sig_dict.update({"sig_value_min": self.sig_value_min})
        sig_dict.update({"sig_value_max": self.sig_value_max})
        sig_dict.update({"sig_byteorder": self.sig_byteorder})
        sig_dict.update({"sig_value_init": self.sig_value_init})
        sig_dict.update({"sig_value_type": self.sig_value_type})
        sig_dict.update({"sig_value_table": self.sig_value_table})
        sig_dict.update({"compute_method": self.compute_method})

        self.get_sig_core_dict_easy()
        sig_dict.update(self.sig_core_dict)

        return sig_dict
