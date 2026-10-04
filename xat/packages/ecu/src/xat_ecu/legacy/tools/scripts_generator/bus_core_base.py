# -*- coding: utf-8 -*-
"""
@File        : bus_core_base.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2021/05/07 13:36 AM
@Description : description about this file
@Examples    : example of how to use it
"""
# Latest update time   2022/01/30 00:36 AM

import re
import json

from abc import ABC, abstractmethod

class BusCoreBase(ABC):
    def __init__(self):
        self.bus_name = None

        self.class_hierarchy_def_file_lines = []

    def get_all_msg_dicts_on_bus(self):
        all_msgs_on_this_bus_dict = {}

        msg_list = self.get_msg_list()

        for m in msg_list:
            msg_dict = {
                "Cycle": self.get_cycle_time(m),
                "DLC": self.get_msg_len(m),
                "Id": self.get_msg_id(m),
                "Name": self.get_msg_name(m),
                "TxBus": self.get_bus_name(),
                "SendType": self.get_send_type(m),
                "Originator": self.get_originator(m),
                "RxNode": [],
                "cls_msg_obj_supplement": {}
            }

            for s in m.signals:
                # Store the new attributes so the caller can ultimately move them to their correct location.
                msg_dict["cls_msg_obj_supplement"][self.get_signal_name(s)] = self.get_signal_min_max_initial_value(s)

                for receiver in s.receivers:
                    if receiver not in msg_dict["RxNode"]:
                        msg_dict["RxNode"].append(receiver)

            all_msgs_on_this_bus_dict[self.get_msg_id(m)] = msg_dict

        return all_msgs_on_this_bus_dict

    def get_cls_dict(self):
        """
        Read Bus+Message+Signal+Signal_Value_Name info
        out of cantools obj and return it.
        :return:
        :rtype: dict[msg_name] of dict[signal_name] of dict[signal_info_name]
        """
        cls_dict = {}

        msg_list = self.get_msg_list()
        is_can = False
        if len(msg_list) > 0 and "message" in msg_list[0].__str__():
            is_can = True
        for m in msg_list:
            msg_dict = self.get_msg_dict(m)
            if is_can:
                msg_dict["rx_node"] = []
            for s in m.signals:
                sig_dict = self.get_signal_dict(s)
                msg_dict[self.get_signal_name(s)] = sig_dict
                if is_can:
                    if msg_dict.get('rx_node'):
                        msg_dict["rx_node"].extend(sig_dict.pop("receivers"))
                    else:
                        msg_dict["rx_node"] = sig_dict.pop("receivers")
            if is_can:
                # generate sorted rx_node list, so that the class file content won't be change every time
                msg_dict["rx_node"] = sorted(list(set(msg_dict["rx_node"])))
            cls_dict[msg_dict["msg_name"]] = msg_dict  # This works for both dbc and ldf files.

        return cls_dict

    def get_bus_name(self):
        return self.bus_name

    @abstractmethod
    def get_msg_list(self):
        """
        :return: dict of msgs from child class
        :rtype:
        """
        return []

    @abstractmethod
    def get_cyclic_msg_dict(self, ecu_under_test_name):
        """
        :return: bus_cyclic_list
        :rtype: list of dict
        """
        return None

    @abstractmethod
    def get_msg_dict(self, m):
        return None

    @abstractmethod
    def get_msg_id(self, m):
        return None

    @abstractmethod
    def get_signal_name(self, signal):
        """
        :param signal: signal object
        :type signal: internal data member from one of DbcCore or LdfCore
        :return: name of this signal
        :rtype: str
        """
        return None

    @abstractmethod
    def get_cycle_time(self, m):
        return None

    @abstractmethod
    def get_msg_len(self, m):
        return None

    @abstractmethod
    def get_msg_name(self, m):
        return None

    @abstractmethod
    def get_send_type(self, m):
        return None

    @abstractmethod
    def get_originator(self, m):
        return None

    @abstractmethod
    def get_signal_dict(self, s):
        """
        :param s:
        :type s:
        :return:
        :rtype: dict[signal_name]
        """
        return None

    def get_signal_dict_helper(
            self, sname, num_bits_in_signal, msb_bit_ndx_in_msg, signal_first_byte_lsb_bit_ndx_in_first_msg_byte=None):
        """
        :param sname:
        :type sname:
        :param num_bits_in_signal:
        :type num_bits_in_signal:
        :param msb_bit_ndx_in_msg:
        :type msb_bit_ndx_in_msg:
        :param signal_first_byte_lsb_bit_ndx_in_first_msg_byte:
        :type signal_first_byte_lsb_bit_ndx_in_first_msg_byte:
        :return:
        :rtype:
        """
        s_dict = {'length': num_bits_in_signal}

        byte_ndxs_in_msg, signal_msb_bit_ndx_in_msg, masks, unmasks, widths, shifts = \
            self.get_byte_ndxs_in_msg_and_msb_ndx_in_msg_and_masks_and_unmasks_and_widths_and_shifts(
                sname, num_bits_in_signal, msb_bit_ndx_in_msg, signal_first_byte_lsb_bit_ndx_in_first_msg_byte)

        num_bytes_in_signal = len(unmasks)

        s_dict['startbit'] = signal_msb_bit_ndx_in_msg

        if num_bytes_in_signal == 1:
            s_dict['byte'] = byte_ndxs_in_msg[0]

            s_dict['mask'] = masks[0]

            s_dict['unmask'] = unmasks[0]

            s_dict['shift'] = shifts[0]
        else:
            info_for_this_signal = []

            for i in range(0, num_bytes_in_signal):
                info_for_this_signal_byte = (byte_ndxs_in_msg[i], masks[i], unmasks[i], widths[i], shifts[i])

                info_for_this_signal.append(info_for_this_signal_byte)

            s_dict["bmuws_info"] = info_for_this_signal  # BMUWS == Byte, Mask, Unmask, Width, Shift.

        return s_dict

    @abstractmethod
    def get_signal_min_max_initial_value(self, s):
        return None

    # For CAN:                              1 1 1 1 1 1       2 2 2 2 1 1 1 1
    # Start bit# in mesg: 7 6 5 4 3 2 1 0   5 4 3 2 1 0 9 8   3 2 1 0 9 8 7 6
    #                    |_ _ _ _._ _ _ _| |_ _ _ _._ _ _ _| |_ _ _ _._ _ _ _| ...
    # Start bit# in byte: 7 6 5 4 3 2 1 0   7 6 5 4 3 2 1 0   7 6 5 4 3 2 1 0
    #                         Byte #0           Byte #1           Byte #2
    #
    def get_byte_ndxs_in_msg_and_msb_ndx_in_msg_and_masks_and_unmasks_and_widths_and_shifts(
            self, sname, num_bits_in_signal, msb_bit_ndx_in_msg,
            signal_first_byte_lsb_bit_ndx_in_first_msg_byte=None):
        # NOTE: for LIN msgs, msb_bit_ndx_in_msg = the bit_ndx of the lsb of the signal's first byte.
        #
        start_byte_ndx_in_msg = int(msb_bit_ndx_in_msg / 8)

        msb_ndx_in_first_byte = msb_bit_ndx_in_msg % 8

        if signal_first_byte_lsb_bit_ndx_in_first_msg_byte is None:
            lsb_ndx_in_first_byte = max(msb_ndx_in_first_byte - num_bits_in_signal + 1, 0)

            number_of_less_significant_bits_in_first_byte_starting_from_the_msb_ndx = msb_ndx_in_first_byte + 1
        else:
            lsb_ndx_in_first_byte = signal_first_byte_lsb_bit_ndx_in_first_msg_byte % 8

            number_of_less_significant_bits_in_first_byte_starting_from_the_msb_ndx = \
                msb_ndx_in_first_byte + 1 - lsb_ndx_in_first_byte

        num_signal_bits_in_first_byte = \
            min(num_bits_in_signal, number_of_less_significant_bits_in_first_byte_starting_from_the_msb_ndx)

        # 1.  Do the portion in the initial byte (may be a full byte).
        # Set the initial value of end_byte_ndx_in_msg here,
        # in case 2. or 3. below do not apply to this signal.
        #
        end_byte_ndx_in_msg = start_byte_ndx_in_msg

        byte_ndxs_in_msg = [start_byte_ndx_in_msg]

        num_remaining_bits_in_signal = num_bits_in_signal - num_signal_bits_in_first_byte

        num_bits_to_shift = lsb_ndx_in_first_byte

        shift = max(0, num_bits_to_shift)
        shifts = [shift]

        base_mask = (1 << num_signal_bits_in_first_byte) - 1

        mask = base_mask << shift
        masks = ["{:#010b}".format(mask)]

        unmask = mask ^ 0xff
        unmasks = ["{:#010b}".format(unmask)]

        widths = [num_signal_bits_in_first_byte]

        # 2.  Do the bytes-in-the-middle.
        num_full_bytes_in_the_middle = int(num_remaining_bits_in_signal / 8)

        for i in range(0, num_full_bytes_in_the_middle):
            byte_ndx = i + start_byte_ndx_in_msg + 1
            end_byte_ndx_in_msg = byte_ndx

            byte_ndxs_in_msg.append(end_byte_ndx_in_msg)

            widths.append(min(8, num_remaining_bits_in_signal))

            num_remaining_bits_in_signal -= 8

            shifts.append(0)

            masks.append("{:#010b}".format(0xff))
            unmasks.append("{:#010b}".format(0x00))

        # 3.  Do the remaining bits in the last byte, if any.
        if num_remaining_bits_in_signal > 0:
            end_byte_ndx_in_msg += 1

            byte_ndxs_in_msg.append(end_byte_ndx_in_msg)

            end_bit_ndx_in_msg = self.get_end_bit_ndx_in_msg(num_remaining_bits_in_signal)

            widths.append(min(8, num_remaining_bits_in_signal))

            shifts.append(end_bit_ndx_in_msg)

            base_mask = (1 << num_remaining_bits_in_signal) - 1

            mask = base_mask << end_bit_ndx_in_msg
            masks.append("{:#010b}".format(mask))

            unmask = mask ^ 0xff
            unmasks.append("{:#010b}".format(unmask))

        return byte_ndxs_in_msg, msb_bit_ndx_in_msg, masks, unmasks, widths, shifts

    @abstractmethod
    def get_end_bit_ndx_in_msg(self, num_remaining_bits_in_signal):
        return -9999

    def round_up_to_msb_bit_ndx_in_this_byte(self, n):
        return n + 7 - (n % 8)

    def round_down_to_lsb_bit_ndx_in_this_byte(self, n):
        return n - (n % 8)

    def get_signal_values_dict(self, s):
        """
        :param s:
        :type s:
        :return:
        :rtype: dict[signal_value]
        """
        s_dict = {}

        if s.choices is not None:
            for k, v in s.choices.items():
                if type(v) is str and ' ' in v:
                    v = v.replace(' ', '_')

                if '+' in v and 'tick' in v:
                    v = re.sub(r'[+]', "plus", v)

                if '-' in v and 'tick' in v:
                    v = re.sub(r'[-]', "minus", v)

                v = re.sub(r'%', "_percent", v)
                v = re.sub(r'<', "less_than", v)
                v = re.sub(r'>', "great_than", v)
                v = re.sub(r'&', "and", v)
                v = re.sub(r'[¡Ãï¿½ï¿½\[\]]', "", v)
                v = re.sub(r'\s+', "", v).strip()
                v = re.sub(r'\s', "_", v)
                v = re.sub(r'[~/();+=\-.\',:]', "", v)
                v = re.sub(r'}|{', "", v)
                v = 'v_%s' % v
                v = v.lower()

                for i in range(6):
                    v = re.sub(r'__', "_", v)

                    if v[-1] == '_':
                        v = v[:-1]

                s_dict[v.strip()] = "{:#x}".format(k)

        return s_dict

    def write_cyc_msg_to_file(self, cyc_msg_dict, json_file_path):
        print("Writing to file: {}".format(json_file_path))

        with open(json_file_path, "w") as f:
            f.write(json.dumps(cyc_msg_dict, sort_keys=True,
                               indent=2, separators=(",", ":")))

    def write_cls_list_to_file(self, class_hierarchy_def_file_lines, class_hierarchy_file_name):
        print("Writing to file: {}".format(class_hierarchy_file_name))

        with open(class_hierarchy_file_name, "w") as f:
            for line in class_hierarchy_def_file_lines:
                f.write(line)
                f.write("\n")

    data_members_in_order = [
        "length",
        "startbit",
        "byte",
        "mask",
        "unmask",
        "width",
        "shift",
        "min",
        "max",
        "initial",
        "bmuws_info"  # Our multi-byte signal (Byte, Mask, Unmask, Shift) info sorts to the end.
    ]

    def desired_order(self, kv):
        try:
            return self.data_members_in_order.index(kv[0])
        except ValueError:
            try:
                return 999 + int(kv[1], 16)  # All the "v_" entries sort to the end, in ascending order.
            except TypeError:
                return 9999 if kv[1] is None else 999 + kv[1]  # For "min", "max", ("initial" sometimes == None).

    # In case we want to switch to alpha order.
    def alphabetical_order(self, kv):
        return kv[0]

    def get_cls_hierarchy_def_file_content(self, cls_dict, target_cls_name):
        """
        :param cls_dict:
        :type cls_dict:
        :param target_cls_name:
        :type target_cls_name:
        :return: class hierarchy definition file contents
        :rtype: list of str
        """
        b4 = "    "
        b8 = "        "
        b12 = "            "
        b16 = "                "
        unwanted_signal_params = ("min", "max", "initial")  # Let's omit these from the generated files for now.

        self.class_hierarchy_def_file_lines.append(
            "# Auto generated by tools/scripts_generator/generate_cls_defs_and_cyc_json.py")
        self.class_hierarchy_def_file_lines.append("")
        self.class_hierarchy_def_file_lines.append("")
        self.class_hierarchy_def_file_lines.append("class {}:".format(target_cls_name))

        for msg_name, msg_dict in cls_dict.items():
            self.class_hierarchy_def_file_lines.append("{}class {}:".format(b4, msg_name))

            for signal_name, signal_dict in msg_dict.items():
                if type(signal_dict) is dict:
                    if signal_name == "class":
                        msg_value1 = "Class"
                        self.class_hierarchy_def_file_lines.append("{}class {}:".format(b8, msg_value1))
                    else:
                        self.class_hierarchy_def_file_lines.append("{}class {}:".format(b8, signal_name))

                    for signal_param_name, signal_param_value in sorted(signal_dict.items(), key=self.desired_order):
                        if type(signal_param_value) is list:
                            self.class_def_line_bmuws_helper(b12, b16, signal_param_name, signal_param_value)
                        elif signal_param_name not in unwanted_signal_params:
                            self.class_def_line_helper(b12, signal_param_name, signal_param_value)

                elif signal_name == "msg_name":
                    self.class_def_quoted_line_helper(b8, signal_name, signal_dict)
                elif signal_name == "originator":
                    self.class_def_quoted_line_helper(b8, signal_name, signal_dict)
                elif signal_name == "schedule":
                    self.class_def_quoted_line_helper(b8, signal_name, signal_dict)
                else:
                    self.class_def_line_helper(b8, signal_name, signal_dict)

        if self.class_hierarchy_def_file_lines[-1] == "class {}:".format(target_cls_name):
            # Keep it syntactically correct if there are no msgs due to an unparsable bus_file :-(.
            self.class_hierarchy_def_file_lines.append("    # The bus_file was unparseable :-(.")
            self.class_hierarchy_def_file_lines.append("    pass")

        return self.class_hierarchy_def_file_lines

    def class_def_line_helper(self, indent, signal_name, signal_value):
        self.class_hierarchy_def_file_lines.append("{}{} = {}".format(indent, signal_name, signal_value))

    def class_def_line_bmuws_helper(self, indent1, indent2, signal_param_name, signal_param_value):
        self.class_hierarchy_def_file_lines.append("{}{} = [".format(indent1, signal_param_name))

        bmuws_entries = []

        for bmuws_entry in signal_param_value:
            bmuws_entry_str_list = [str(x) for x in bmuws_entry]

            bmuws_entry_str = "({})".format(", ".join(bmuws_entry_str_list))

            bmuws_entries.append(bmuws_entry_str)

        bmuws_entry_separator = ",\n{}".format(indent2)

        bmuws_entries_str = bmuws_entry_separator.join(bmuws_entries)

        bmuws_info_str = "{}{}\n{}]".format(indent2, bmuws_entries_str, indent1)

        self.class_hierarchy_def_file_lines.append(bmuws_info_str)

    def class_def_quoted_line_helper(self, indent, signal_name, signal_value):
        self.class_hierarchy_def_file_lines.append('{}{} = "{}"'.format(indent, signal_name, signal_value))

    # Used in get_lin_file_num() and get_cls_name().
    lin_regexp = re.compile(r"lin(\d+)", re.IGNORECASE)

    sort_funcs = {
        "can": lambda filename: filename,
        "lin": lambda filename: BusCoreBase.get_lin_file_num(filename)
    }

    @staticmethod
    def get_lin_file_num(filename):
        m = BusCoreBase.lin_regexp.search(filename)

        if m is None:  # For Force.
            return filename

        lin_file_num = m.group(1)

        return int(lin_file_num)

    @staticmethod
    def get_cls_name(bus_file_name):
        cls_name = None
        bus_file_name = bus_file_name.lower()

        if "_nt2_" in bus_file_name:
            return BusCoreBase.get_force_platform_cls_name(bus_file_name)

        if "_adas_" in bus_file_name:
            cls_name = "Adas"
        elif "_bodycan_" in bus_file_name:
            cls_name = "Body"
        elif "_cdc_" in bus_file_name:
            cls_name = "Cdc"
        elif "_chassis_" in bus_file_name:
            cls_name = "Chassis"
        elif "_ept_" in bus_file_name:
            cls_name = "Ept"
        elif "_info_" in bus_file_name or "_infotainment_" in bus_file_name:
            cls_name = "Info"
        elif "_pd_" in bus_file_name:
            cls_name = "Pd"
        elif "_adc1_" in bus_file_name:
            cls_name = "Adc1"
        elif "_adc2_" in bus_file_name:
            cls_name = "Adc2"
        elif "_adc3_" in bus_file_name:
            cls_name = "Adc3"
        elif "_rf_" in bus_file_name:
            cls_name = "Rf"
        elif "_nomi_" in bus_file_name:
            cls_name = "Nomi"
        elif "_obd_" in bus_file_name:
            cls_name = "Obd"
        elif BusCoreBase.lin_regexp.search(bus_file_name) is not None:
            m = BusCoreBase.lin_regexp.search(bus_file_name)
            cls_name = "Lin{}".format(m.group(1))

        return cls_name

    @staticmethod
    def get_force_platform_cls_name(bus_file_name):
        # This is only used by the test-generating file scripts.
        # TODO: Decide if we want to keep using them or replace them with our "test_in_loop()" approach?
        cls_name = None

        # TODO: Implement this correctly a bit later...
        bus_file_ext_dir = "foo"

        bus_names_to_bus_file_ext_filenames_map = \
            CgwBusBase.get_bus_names_to_bus_ext_filenames_map(
                bus_file_ext_dir, self.veh_type)

        a = 1
