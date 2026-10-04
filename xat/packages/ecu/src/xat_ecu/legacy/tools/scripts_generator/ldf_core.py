# -*- coding: utf-8 -*-
"""
@File        : dbc_core.py
@Description : Generate cyclic LDF class file
@Examples    :
"""

from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.tools.scripts_generator.ldf_parser import *
from xat_ecu.legacy.tools.scripts_generator.bus_core_base import BusCoreBase


class LdfCore(BusCoreBase):
    def __init__(self, bus_name, ldf_file, bus_type_bus_parser_cls_obj_dicts):
        super().__init__()

        self.bus_name = bus_name.upper()
        self.ldf_file = ldf_file
        self.bus_type_bus_parser_cls_obj_dicts = bus_type_bus_parser_cls_obj_dicts

        try:
            bus_name_lower = bus_name.lower()

            # If we're being called from tools/scripts_generator/generate_cls_defs_and_cyc_json.py:
            #   generate_all_cyc_json_and_bus_cls_files_helper()
            # CgwApp() has not been called, so there is no bus_type_bus_parser_cls_obj_dicts
            # available to pass into here.
            #
            if bus_type_bus_parser_cls_obj_dicts is None:
                self.parser_obj = LdfParser({'LDF File': ldf_file})
                self.parser_obj.parse_ldf()
            else:
                if bus_name_lower in self.bus_type_bus_parser_cls_obj_dicts["parser_objs"]:
                    # Use the one that CgwApp() has already loaded.
                    self.parser_obj = self.bus_type_bus_parser_cls_obj_dicts["parser_objs"][bus_name_lower]
                else:
                    self.parser_obj = LdfParser({'LDF File': ldf_file})
                    self.parser_obj.parse_ldf()
                    self.bus_type_bus_parser_cls_obj_dicts["parser_objs"][bus_name_lower] = self.parser_obj

        except FileNotFoundError as err:
            raise RuntimeError('LdfParser cannot find: "{}":\n{}'.format(self.ldf_file, err))
        except UnicodeDecodeError as err:
            raise RuntimeError('LdfParser cannot read: "{}":\n{}'.format(self.ldf_file, err))
        except RuntimeError as err:
            err_msg = "\nBus({}): {}".format(bus_name, err.args[0])
            logger.error(err_msg)

    def get_msg_list(self):
        return self.parser_obj.lin_message_list

    def get_cyclic_msg_dict(self, ecu_under_test_name):
        # Apparently there are no JSON files for LIN buses.
        return None

    def get_msg_dict(self, m):
        """
        :param m:
        :type m:
        :return: msg_dict: message parameters
        :rtype: dict
        """
        msg_dict = {k: v for k, v in vars(m).items() if type(v) is not list}

        return msg_dict

    def get_msg_id(self, m):
        """
        :param m:
        :type m:
        :return: msg_id
        :rtype: int
        """
        return m.msg_id

    def get_signal_name(self, signal):
        """
        :param signal: signal object
        :type signal: internal data member from one of DbcCore or LdfCore
        :return: name of this signal
        :rtype: str
        """
        return signal.signal_name

    def get_cycle_time(self, m):
        return m.msg_cyc

    def get_msg_len(self, m):
        return m.msg_length

    def get_msg_name(self, m):
        return m.msg_name

    def get_send_type(self, m):
        return m.schedule

    def get_originator(self, m):
        return m.originator

    def get_signal_dict(self, s):
        """
        :param s:
        :type s:
        :return:
        :rtype:
        """
        # A this point we should summarize:
        #
        # In CAN msgs, the "remaining_bits_after_the_first_byte" are placed in the most-significant-bits
        # of the last byte.  This is confirmed in CANalyzer's very colorful display of where signals' bits
        # are located in a given msg.
        #
        # In LIN msgs, according to Table 9.1 in LIN-Spec_2.2_Rev_A.pdf:
        #   https://microchip.wdfiles.com/local--files/lin%3Aworkflow/LIN-Spec_2.2_Rev_A.PDF
        # the "remaining_bits_after_the_first_byte" are placed in the least-significant-bits of the last byte.
        #
        # That diagram draws the bits in backwards-order, so it takes a moment to get past that.  Then...
        #
        # It's clear that LIN's "remaining_bits" are placed in the last byte's LSB,
        # in contrast to CAN's "remaining_bits", which are placed in the last byte's MSB.

        # For LIN signals, For the bits remaining after the full_bytes_in_the_middle, ...
        # _subtract_ down from the MSB.
        #
        # I confirmed that this matches how Alpha2's LdfParser is placing the "remaining_bits_after_the_first_byte".
        #
        # I.e., it places them in the low-order bits of the last byte, as shown here for WdwVehSpd on LIN1:
        #   byte_lsb = 5
        #   byte_msb = 6
        #   shift_lsb = 0
        #   shift_msb = 0
        #   mask_lsb = 0b1111_1111
        #   mask_msb - 0b_0001_1111
        #
        # Table 9.1 in LIN-Spec_2.2_Rev_A.pdf shows this as well, but it _displays_ the bits in backwards order:
        #   LSB ... MSB
        # which is definitely initially confusing.  Hopefully I have it straight in my mind now(?).
        #
        # In contrast, in CAN msgs, CANalyzer shows that "left_over_bits_after_the_first_byte" are placed
        # in the most-significant-bits of the last byte, not in the least-significant-bits like LIN does it.
        #
        # Likewise, the first signal's LSbit in its msg's Bit#0, and subsequent signals are in the msg's
        # higher-order bits.
        #
        num_bits_in_signal = s.length_bits

        # In .ldf files, the "start_bit" is actually the bit_ndx in the msg of the signal's LSB, as described above.
        signal_first_byte_lsb_bit_ndx_in_first_msg_byte = s.start_bit

        first_msg_byte_msb_bit_ndx = \
            self.round_up_to_msb_bit_ndx_in_this_byte(signal_first_byte_lsb_bit_ndx_in_first_msg_byte)

        msb_bit_ndx_in_msg = min(
            signal_first_byte_lsb_bit_ndx_in_first_msg_byte + num_bits_in_signal - 1, first_msg_byte_msb_bit_ndx)

        # NOTE: for LIN msgs, msb_bit_ndx_in_msg = the bit_ndx of the lsb of the signal's first byte.

        # We'll pass the signal_first_byte_lsb_bit_ndx_in_first_msg_byte since that bit_ndx is for the signal's bits
        # which are in the lowest-numbered byte of the msg.
        #
        # This populates the signal's basic "bmuws_info":
        s_dict = self.get_signal_dict_helper(
            s.signal_name, num_bits_in_signal, msb_bit_ndx_in_msg, signal_first_byte_lsb_bit_ndx_in_first_msg_byte)

        # dbc_core.py does this:
        #   num_bits_in_signal = s.length
        #   msb_bit_ndx_in_msg = s.start
        #
        #   s_dict = self.get_signal_dict_helper(s.name, num_bits_in_signal, msb_bit_ndx_in_msg)
        #
        # instead of what we do here:
        #
        # This populates the signal's "v_" signal_value_enum_name entries:
        signal_values_dict = self.get_signal_values_dict(s)

        s_dict.update(signal_values_dict)

        return s_dict

    def get_signal_min_max_initial_value(self, s):
        # New attributes for Amit's tests.
        max_value = (1 << s.length_bits) - 1

        return {"min": 0, "max": max_value, "initial": s.initial_value}

    def get_end_bit_ndx_in_msg(self, num_remaining_bits_in_signal):
        """
        In a LIN msg the remaining bits in the last byte are stored in the least-significant-bits.

        :param num_remaining_bits_in_signal:
        :type num_remaining_bits_in_signal:
        :return:
        :rtype:
        """
        return 0
