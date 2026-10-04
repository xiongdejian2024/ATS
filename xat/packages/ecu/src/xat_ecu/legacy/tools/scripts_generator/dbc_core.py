# -*- coding: utf-8 -*-
"""
@File        : dbc_core.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2021-04-26 21:54
@Description : Generate cyclic json file and DBC class file
@Examples    :
"""

import cantools
from cantools.database import Database

from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.tools.scripts_generator.bus_core_base import BusCoreBase


class DbcCore(BusCoreBase):
    def __init__(self, bus_name, dbc_file, bus_type_bus_parser_cls_obj_dicts):
        super().__init__()

        self.bus_name = bus_name.upper()
        self.dbc_file = dbc_file
        self.bus_type_bus_parser_cls_obj_dicts = bus_type_bus_parser_cls_obj_dicts

        if bus_type_bus_parser_cls_obj_dicts is None:
            self.db = cantools.db.load_file(self.dbc_file)
        try:
            bus_name_lower = bus_name.lower()

            # If we're being called from tools/scripts_generator/generate_cls_defs_and_cyc_json.py:
            #   generate_all_cyc_json_and_bus_cls_files_helper()
            # CgwApp() has not been called, so there is no bus_type_bus_parser_cls_obj_dicts
            # available to pass into here.
            #
            if bus_type_bus_parser_cls_obj_dicts is None:
                self.db = cantools.db.load_file(self.dbc_file)
            else:
                if bus_name_lower in self.bus_type_bus_parser_cls_obj_dicts["parser_objs"]:
                    # Use the one that CgwApp() has already loaded.
                    self.db = self.bus_type_bus_parser_cls_obj_dicts["parser_objs"][bus_name_lower]
                else:
                    self.db = cantools.db.load_file(self.dbc_file)
                    self.bus_type_bus_parser_cls_obj_dicts["parser_objs"][bus_name_lower] = self.db

        except FileNotFoundError as err:
            raise RuntimeError('cantools cannot find: "{}":\n{}'.format(self.dbc_file, err))
        except UnicodeDecodeError as err:
            raise RuntimeError('cantools cannot read: "{}":\n{}'.format(self.dbc_file, err))
        except Exception as err:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/tools/scripts_generator/dbc_core.py")
            err_msg = "\nBus({}): {}".format(bus_name, err.args[0])
            logger.error(err_msg)

            # Just make an empty one to keep things simple for the caller when the .dbc file is unparseable.
            self.db = Database()

    def get_msg_list(self):
        return self.db.messages

    def get_cyclic_msg_dict(self, ecu_under_test_name, ecu_under_test_name_only = True):
        """
        :return: bus_cyclic_list or bus_cyclic_dict
        :rtype: bus_cyclic_list     list of dict
        :rtype: bus_cyclic_dict     dict of list of dict
        """
        # ecu_under_test_name != ALL
        # ecu_under_test_name_only = True       Only one current ECU loop is generated
        # ecu_under_test_name_only = Flase      Generate only loops other than the current ECU
        bus_cyclic_dict = {}
        bus_cyclic_list = []
        for m in self.db.messages:
            if m.send_type == "Cyclic" and m.cycle_time != 0:
                msg_dict = {
                    "Cycle": self.get_cycle_time(m),
                    "DLC": self.get_msg_len(m),
                    "Id": self.get_msg_id(m),
                    "Name": self.get_msg_name(m),
                    "RxNode": []
                }
                msg_dict["TxBus"] = self.get_bus_name()
                for s in m.signals:
                    for receiver in s.receivers:
                        if receiver not in msg_dict["RxNode"]:
                            msg_dict["RxNode"].append(receiver)
                
                if ecu_under_test_name == "ALL":
                    for sender in m.senders:
                        if sender not in list(bus_cyclic_dict.keys()):                           
                            bus_cyclic_dict[sender] = [msg_dict]
                        else:
                            bus_cyclic_dict[sender].append(msg_dict)
                elif ecu_under_test_name_only :
                    # cyclic message is ecu_under_test_name only                   
                    if ecu_under_test_name in m.senders:
                        if m.send_type == "Cyclic":
                            bus_cyclic_list.append(msg_dict)
                elif not ecu_under_test_name_only :      
                    if ecu_under_test_name not in m.senders and \
                            "Vector__XXX" not in m.senders:

                        if m.send_type == "Cyclic":
                            bus_cyclic_list.append(msg_dict)
                            
        if  ecu_under_test_name == "ALL":                   
            return bus_cyclic_dict
        else:
            return bus_cyclic_list

    def get_msg_dict(self, m):
        """
        :param m:
        :type m:
        :return: msg_dict: message parameters
        :rtype: dict
        """
        msg_dict = {
            "msg_name": self.get_msg_name(m),
            "msg_id": hex(self.get_msg_id(m)),
            "msg_cyc": int(m.cycle_time) / 1000,
            "dlc": m.length,
            "tx_node": m.senders,

        }

        return msg_dict

    def get_msg_id(self, m):
        """
        :param m:
        :type m:
        :return: msg_id
        :rtype: int
        """
        return m.frame_id

    def get_signal_name(self, signal):
        """
        :param signal: signal object
        :type signal: internal data member from one of DbcCore or LdfCore
        :return: name of this signal
        :rtype: str
        """
        return signal.name

    def get_cycle_time(self, m):
        return m.cycle_time

    def get_msg_len(self, m):
        return m.length

    def get_msg_name(self, m):
        return m.name

    def get_send_type(self, m):
        return m.send_type

    def get_originator(self, m):
        return m.senders

    """
    BO_ 1027 RAD_FC_Obj00_A: 8 RAD_FC
     SG_ dy : 31|11@0+ (0.125,-128) [-128|127.875] "m"  ADC
     SG_ dx : 7|12@0+ (0.0625,0) [0|255.9375] "m"  ADC
    """

    # For CAN:                              1 1 1 1 1 1       2 2 2 2 1 1 1 1
    # Start bit# in mesg: 7 6 5 4 3 2 1 0   5 4 3 2 1 0 9 8   3 2 1 0 9 8 7 6
    #                    |_ _ _ _._ _ _ _| |_ _ _ _._ _ _ _| |_ _ _ _._ _ _ _| ...
    # Start bit# in byte: 7 6 5 4 3 2 1 0   7 6 5 4 3 2 1 0   7 6 5 4 3 2 1 0
    #                         Byte #0           Byte #1           Byte #2
    #
    def get_signal_dict(self, s):
        """
        :param s:
        :type s:
        :return:
        :rtype:
        """
        num_bits_in_signal = s.length
        msb_bit_ndx_in_msg = s.start
        receivers = s.receivers
        # This populates the basic "bmuws_info" for this signal:
        s_dict = self.get_signal_dict_helper(s.name, num_bits_in_signal, msb_bit_ndx_in_msg)
        s_dict["receivers"] = receivers
        # This populates the signal's "v_" signal_value_enum_name entries:
        signal_values_dict = self.get_signal_values_dict(s)

        s_dict.update(signal_values_dict)

        return s_dict

    def get_signal_min_max_initial_value(self, s):
        # Add new attributes for Amit's tests.

        return {"min": s.minimum, "max": s.maximum, "initial": s.initial}

    def get_end_bit_ndx_in_msg(self, num_remaining_bits_in_signal):
        """
        In a CAN msg the remaining bits in the last byte are stored in the most-significant-bits.

        :param num_remaining_bits_in_signal:
        :type num_remaining_bits_in_signal:
        :return:
        :rtype:
        """
        return 8 - num_remaining_bits_in_signal
