# -*- coding: utf-8 -*-
"""
@File        : pcan.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2021/03/31 3:36 AM
@Description : description about this file
@Examples    : example of how to use it
"""

import os
import sys
current_path = os.path.dirname(os.path.realpath(__file__))
from xat_ecu.legacy.sdk.driver.can_lib.socket_can import SocketCan
from xat_ecu.legacy.sdk.driver.lin_lib.lin import Lin
from abc import ABC
import os
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.sdk.driver.can_lib.can_listener import CanListener
import yaml
import importlib
from xat_ecu.legacy.sdk.can_lin.pcan_const import *
from typing import Tuple, Union
import inspect
import time
import cantools
from copy import deepcopy
from xat_ecu.legacy.tools.scripts_generator.bus_core_base import BusCoreBase


class CanListenerSignalsValuesPatternSteps:
    def __init__(self, *signal_names_and_signal_value_names_and_expected_count_range):
        self.pattern_info = []

        for pattern_step_tuple in signal_names_and_signal_value_names_and_expected_count_range:
            if isinstance(pattern_step_tuple, tuple):
                self._init_helper(pattern_step_tuple)
            else:
                self._init_helper(signal_names_and_signal_value_names_and_expected_count_range)
                break

    def _init_helper(self, pattern_step_tuple):
        num_info_entries = len(pattern_step_tuple) - 1  # Ignore the pattern_step_max_loop_time at the end.

        signal_name_ndx = None  # So PyCharm doesn't complain that this is undefined.
        pattern_step_signals_dicts = []

        for signal_name_ndx in range(0, num_info_entries, 2):
            signal_name, signal_value_name = pattern_step_tuple[signal_name_ndx:signal_name_ndx + 2]

            if not isinstance(signal_name, str):
                break

            signal_and_value_tuple = (signal_name, signal_value_name)

            signal_and_value_dict = {
                "signal_and_value": signal_and_value_tuple,
                # BusCmd._pattern_step_count_loop() will fill these two in:
                "bmuws_info": None, "signal_info": None, "expected_signal_value": None
            }

            pattern_step_signals_dicts.append(signal_and_value_dict)
        else:
            signal_name_ndx += 2  # This is used when the expected_count_info is omitted.

        expected_count_info = []

        for signal_name_ndx in range(signal_name_ndx, num_info_entries, 2):
            comparison_enum, comparison_value = pattern_step_tuple[signal_name_ndx:signal_name_ndx + 2]

            expected_count_info.append((comparison_enum, comparison_value))

        if num_info_entries > signal_name_ndx:
            signal_name_ndx += 2  # This is used when the expected_count_info is omitted.

        pattern_step_info = {
            "signal_and_value_dicts": pattern_step_signals_dicts,
            "expected_count_info": expected_count_info,
            "pattern_step_max_loop_time": pattern_step_tuple[signal_name_ndx]
        }

        self.pattern_info.append(pattern_step_info)


class CanListenerInfoBase:
    def __init__(self, signal_name, sig_value_names, max_loop_time, value_comparison):
        self.signal_name = signal_name
        self.sig_value_names = sig_value_names
        self.max_loop_time = max_loop_time
        self.value_comparison = value_comparison


class CanListenerSignalInfo(CanListenerInfoBase):
    def __init__(
            self, signal_name, sig_value_names,
            max_loop_time=PcanConst.CAN_LISTENER_SIGNAL_MAX_LOOP_TIME,
            value_comparison=0,
            expected_count=PcanConst.CAN_LISTENER_EXPECTED_COUNT,
            count_comparison=0):
        super().__init__(signal_name, sig_value_names, max_loop_time, value_comparison)

        self.expected_count = expected_count
        self.count_comparison = count_comparison


class CanListenerPreconditionInfo(CanListenerInfoBase):
    def __init__(self, signal_name, sig_value_names,
                 max_loop_time=PcanConst.CAN_LISTENER_SIGNAL_MAX_LOOP_TIME,
                 value_comparison=0):
        super().__init__(signal_name, sig_value_names, max_loop_time, value_comparison)

        self.expected_count = None
        self.count_comparison = None


class Pcan(ABC):
    """
    Pcan Abstract Base Class that serves as basic for all concrete instance
    """

    def __init__(self, **kwargs):
        __import__("os").environ['XAT_CREDENTIAL_SCAN_5B9B5EFA2166042E3BC1']
        self.cfg = kwargs  # dut configuration, include veh_type, dut_version, and so on
        # testbed configuration, virutal pcan - pcan mapping relationship, veh_type,dut_main_ver and so on
        # dictionary of bus instance
        if "dir_prefix" not in self.cfg:
            self.cfg["dir_prefix"] = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.inst_dict = {}
        self.dbc_obj_dict = {}
        self.ldf_obj_dict = {}
        self.setup_pcan_bus()

    def add_cyclic_msg_with_data_bus(self, bus_name, can_id, data, cyclic_rate):
        """
        Add cyclic message with specific data to bus
        :param bus_name: can bus name     such as "bta"
        :param can_id: can message id
        :param data: data of can cyclic message
        :param cyclic_rate: Cycle rate of new cyclic message (in seconds)
        :return:
        """
        self.inst_dict[bus_name].add_cyclic_msg_with_data(can_id, data, cyclic_rate)

    def remove_cyclic_msg_bus(self, bus_name, can_id):
        self.inst_dict[bus_name].remove_cyclic_msg(can_id)

    def setup_pcan_bus(self, with_cyclic=True):
        try:
            self.cfg['package'] = self.cfg.get('dir_prefix')
            json_folder = '%s/%s' % (self.cfg['dir_prefix'], self.cfg['dbc_cyc_json_path'])
            dbc_folder = '%s/%s' % (self.cfg['dir_prefix'], self.cfg['dbc_path'])
            ldf_folder = '%s/%s' % (self.cfg['dir_prefix'], self.cfg['ldf_path'])
            if not self.cfg.get("bus"):
                tmp = deepcopy(self.cfg.get("can_bus"))
                tmp.update(self.cfg.get("lin_bus"))
                self.cfg["bus"] = deepcopy(tmp)
            pcan_channels_info = self.cfg.get("bus")
            dbc_file_bus_dict = self.__get_dbc_ldf_file_bus(dbc_folder)
            ldf_file_bus_dict = self.__get_dbc_ldf_file_bus(ldf_folder)
            for bus_name in pcan_channels_info:
                # can
                if bus_name in dbc_file_bus_dict:
                    ecus = self.cfg["dut_ecu"]
                    bus_not_ecu = bus_name + "_not"
                    for ecu in ecus:
                        bus_not_ecu = bus_not_ecu + "_" + ecu
                    bus_not_ecu = bus_not_ecu.lower()
                    dbc_json = '%s/%s.json' % (json_folder, bus_not_ecu) if with_cyclic else None
                    dbc_file = '%s/%s' % (dbc_folder, dbc_file_bus_dict[bus_name])
                    setattr(self, bus_name, SocketCan(bus_name, pcan_channels_info.get(bus_name), dbc_json=dbc_json))
                    self.inst_dict[bus_name] = getattr(self, bus_name)
                    self.dbc_obj_dict[bus_name] = cantools.db.load_file(dbc_file)
                # lin
                else:
                    if bus_name not in ldf_file_bus_dict:
                        continue
                    ldf_file = '%s/%s' % (ldf_folder, ldf_file_bus_dict[bus_name])
                    setattr(self, bus_name, Lin(bus_name=bus_name, channel=pcan_channels_info.get(bus_name)))
                    self.inst_dict[bus_name] = getattr(self, bus_name)
                    # self.ldf_obj_dict[bus_name] = LdfParser({'LDF File': ldf_file})
                    # self.ldf_obj_dict[bus_name].parse_ldf()

            self.__setup_bus_file_ver_envvar_and_load_bus_cls_hierarchy('dbc')
            self.__setup_bus_file_ver_envvar_and_load_bus_cls_hierarchy('ldf')
        except Exception as err:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/can_lin/pcan.py")
            logger.error("when created pcan, met error:{}".format(err))

    def set(self, msg_signals_obj: type, signal_name: str, sig_value_name: Union[str, int],
            wait: int = PcanConst.BUS_DELAY_NODELAY, timeout: int = PcanConst.BUS_TIMEOUT) -> None:
        """Set a signal's value to the passed-in new value.

        Parameters
        ----------
        msg_signals_obj : type
            self.dbc.chassis.BCU_04 (= cls_signal_obj for each of this msg's signals)
        signal_name : str
            "DoorAjarFrntLeSts"             (= used to get the cls_signal_obj)
        sig_value_name : Union[str, int]
            "v_Unlocked" or 123
        wait : int
            number of msec. to wait before reading the msg.
        timeout : int
            number of sec. to wait before giving up on reading a msg.

        Returns
        -------
        None
        """
        if isinstance(sig_value_name, str):
            sig_value_name = sig_value_name.lower()
        logger.debug(f"Set {msg_signals_obj}.{signal_name}={sig_value_name}")

        bus_name, bus_obj, msg_id, cls_signal_obj, bmuws_info, captured_msg = \
            self.__get_msg_data(msg_signals_obj, signal_name, wait, timeout)

        self.__set_msg_data(bus_name, bus_obj, msg_id, cls_signal_obj, bmuws_info, captured_msg, signal_name,
                            sig_value_name)

    def check(self, msg_signals_obj: type, signal_name: str, sig_value_name: Union[str, int],
              wait: int = PcanConst.BUS_DELAY_NODELAY, timeout: int = PcanConst.BUS_TIMEOUT,
              comparison: int = 0, do_assert: bool = True) -> Tuple[bool, int, str]:
        """
        Check if a signal's current value matches the passed-in expected value.

        Parameters
        ----------
        msg_signals_obj : type
            self.dbc.bodycan.BCM_03            (= cls_signal_obj for each of this msg's signals)
        signal_name : str
            "DoorAjarFrntLeSts"             (= used to get the cls_signal_obj)
        sig_value_name : Union[str, int]
            "v_Unlocked" or 123
        wait : int
            number of msec. to wait before reading the msg.
        timeout : int
            number of sec. to wait before giving up on reading a msg.
        comparison : int
            (-1: <, 0: ==, 1: >)
        do_assert : bool
            assert if match fails.  See Returns for additional details.

        Returns
        -------
        result : bool
            True if check succeeded
        actual_signal_value : int
            numeric value of signal
        err_msg : str
            msg describing the mismatch and where it was called from
        """
        if isinstance(sig_value_name, str):
            sig_value_name = sig_value_name.lower()
        bus_name, bus_obj, msg_id, cls_signal_obj, bmuws_info, captured_msg = \
            self.__get_msg_data(msg_signals_obj, signal_name, wait, timeout)
        expected_signal_value = self.lookup_expected_signal_value_by_name(cls_signal_obj, signal_name, sig_value_name)
        # bus_obj, bmuws_info, cls_signal_obj, captured_msg, expected_signal_value = \
        #     self.get_msg_content_using_msg_signals_obj(msg_signals_obj, signal_name, sig_value_name, wait, timeout)
        #
        # bus_name = bus_obj.bus_name

        return self.__check_msg_data(bus_name, msg_signals_obj.msg_name, bmuws_info, signal_name,
                                     cls_signal_obj, captured_msg, expected_signal_value, comparison, do_assert)

    def lookup_expected_signal_value_by_name(self, cls_signal_obj, signal_name, sig_value_name):
        if isinstance(sig_value_name, str):
            new_signal_value = getattr(cls_signal_obj, sig_value_name)
        elif isinstance(sig_value_name, int) or isinstance(sig_value_name, float):
            new_signal_value = sig_value_name
        else:
            logger.error("\nWrong signal value type: {n}:{v}".format(n=signal_name, v=sig_value_name))
            return

        return new_signal_value

    def __get_msg_data(self, msg_signals_obj: type, signal_name=None, wait=0, timeout=1.0):

        fully_qualified_module_name = msg_signals_obj.__module__
        bus_name = fully_qualified_module_name.split(".")[-1]  # "bodycan"
        # Get bus_obj from inst_dict
        bus_obj = self.inst_dict.get(bus_name)

        if signal_name is None or signal_name == 0:
            cls_signal_obj = None  # This code path is used by lin_routing tests.
            bmuws_info = None
        else:
            cls_signal_obj = getattr(msg_signals_obj, signal_name)

            # bmuws == Byte, Mask, Unmask, Width, Shift.
            bmuws_info = getattr(cls_signal_obj, "bmuws_info", None)

        # Returns bmuws_info = None for signals with no bmuws_info data member.
        # use signal_obj.msg_id to fetch msg data
        captured_msg = bus_obj.read_single_msg(msg_signals_obj.msg_id, wait=wait, timeout=timeout)

        self.confirm_captured_msg_is_not_none(bus_obj.bus_name, msg_signals_obj.msg_id, msg_signals_obj.msg_name,
                                              captured_msg)

        return bus_name, bus_obj, msg_signals_obj.msg_id, cls_signal_obj, bmuws_info, captured_msg

    def get_captured_msg_using_msg_signals_obj(
            self, msg_signals_obj, sig_value_name=0, wait=PcanConst.BUS_DELAY_NODELAY,
            timeout=PcanConst.BUS_TIMEOUT):

        """
        Copied from get_msg_content_using_msg_signals_obj for simplified use in CAN & LIN routing tests.
        """
        signal_name = None
        bus_name, bus_obj, msg_id, cls_signal_obj, bmuws_info, captured_msg = self.__get_msg_data(msg_signals_obj,
                                                                                                  sig_value_name, wait,
                                                                                                  timeout)
        return captured_msg

    def __set_msg_data(self, bus_name, bus_obj, msg_id, cls_signal_obj, bmuws_info, captured_msg, signal_name,
                       sig_value_name):
        new_signal_value = self.lookup_new_signal_value_by_name(cls_signal_obj, signal_name, sig_value_name)
        if bmuws_info is None:
            # All of this signal's bits are in a single-byte.
            captured_msg.data[cls_signal_obj.byte] &= cls_signal_obj.unmask
            captured_msg.data[cls_signal_obj.byte] |= new_signal_value << cls_signal_obj.shift
        else:
            # Multi-byte or straddling-two-bytes signal.

            # First the actual_signal_value's LSbyte is copied into the signal's LSbyte.
            # Then the actual_signal_value is right-shifted, to prepare for copying its MSbyte.
            #
            if bus_name in self.dbc_obj_dict.keys():
                bmuws_info = reversed(bmuws_info)

            # The new_signal_value's LSbyte goes into the signal's first byte, and next into the signal's last byte.
            """
            The problem is that the shift must be applied to 'new_signal_value' before the mask (otherwise the bits 
            ignored by the mask will be ignored). 
            And, the 'new_signal_value' should be only shifted by the amount of bits actually encoded. 
            """
            for byte, mask, unmask, width, shift in bmuws_info:
                # Clean out the signal's existing content.
                captured_msg.data[byte] &= unmask

                # In the new_signal_value, keep only this signal_byte's bits,
                # and shift to them to the correct bit position in the msg.
                captured_msg.data[byte] |= (new_signal_value << shift) & mask

                # Throw away the LSbyte, so we pcan process the MSbyte next.
                new_signal_value >>= 8 - shift

        if bus_name not in self.dbc_obj_dict.keys():
            bus_obj.write_single_msg(msg_id, captured_msg.data, 0)
        else:
            bus_obj.modify_cyclic_data(msg_id, captured_msg.data)

    def __check_msg_data(
            self, bus_name, msg_name, bmuws_info, signal_name, cls_signal_obj, captured_msg, expected_signal_value,
            comparison, do_assert):

        if bmuws_info is None:
            # Single-byte signal.
            encoded_actual_signal_value = \
                (captured_msg.data[cls_signal_obj.byte] & cls_signal_obj.mask) >> cls_signal_obj.shift
        else:
            # Multi-byte or straddling-two-bytes signal.
            encoded_actual_signal_value = 0

            # First the encoded_actual_signal_value's LSbyte receives the signal's LSbyte.
            # Then the encoded_actual_signal_value is left-shifted, to prepare for next receiving the signals's LSbyte.
            #
            if bus_name not in self.dbc_obj_dict.keys():
                bmuws_info = reversed(bmuws_info)

            for byte, mask, unmask, width, shift in bmuws_info:
                # In the new_signal_value, keep only this signal_byte's bits,
                # and shift to them to the correct bit position in the msg.
                signal_byte_val = (captured_msg.data[byte] & mask) >> shift

                shifted_actual_signal_value = encoded_actual_signal_value << width

                encoded_actual_signal_value = shifted_actual_signal_value + signal_byte_val

        result = self.comparison_helper(encoded_actual_signal_value, comparison, expected_signal_value)

        # I.e., err_msg = "cdc.ACM_01.SeatBltFrntLeSts(1) != 0"
        err_msg = ""

        if not result:
            calling_func_info = self.find_calling_func_info()

            err_msg = "\n{}{}.{}.{}({}) not {}".format(
                calling_func_info, bus_name, msg_name, signal_name, encoded_actual_signal_value,
                self.comparison_msg_helper(comparison, cls_signal_obj, expected_signal_value))
            if do_assert:
                assert result, err_msg
        return result, encoded_actual_signal_value, err_msg

    def __setup_bus_file_ver_envvar_and_load_bus_cls_hierarchy(self, class_file_ext):
        """
        Marked static here for calling by class CgwLin.
        """
        cls_file_path = self.cfg["{}_cls_path".format(class_file_ext)]
        # cls_file_path = os.path.join(self.cfg['dbc_cls_prefix'], cls_file_path)
        cls_full_module_name = cls_file_path.replace("/", ".")

        cls_module = importlib.import_module(cls_full_module_name)
        logger.info("cls_module is {}".format(cls_module))
        cls_type_obj = getattr(cls_module, "{}Cls".format(class_file_ext.capitalize()))

        # set self.dbc  compass\ecu_simulator\sdk\dbc_cls\force\vx_x_x\dbc_cls.py DbcCls
        setattr(self, class_file_ext, cls_type_obj)

        # Export env_ver_name to system environment.
        class_file_ver = cls_file_path.split('/')[-1]
        env_ver_name = "{}_VER".format(class_file_ext.upper())
        os.environ[env_ver_name] = class_file_ver

    def lookup_new_signal_value_by_name(self, cls_signal_obj, signal_name, sig_value_name):

        if isinstance(sig_value_name, str):
            new_signal_value = getattr(cls_signal_obj, sig_value_name)
        elif isinstance(sig_value_name, int) or isinstance(sig_value_name, float):
            singal_obj_str = str(cls_signal_obj).replace('\'>', '').split(".")
            bus_name_s, message_name_s, signal_name_s = [obj for obj in singal_obj_str[-3:]]
            bus_name = bus_name_s.lower()
            if not self.dbc_obj_dict.get(bus_name):
                return sig_value_name
            scale = self.dbc_obj_dict[bus_name].get_message_by_name(message_name_s).get_signal_by_name(
                signal_name_s).scale
            offset = self.dbc_obj_dict[bus_name].get_message_by_name(message_name_s).get_signal_by_name(signal_name_s).offset

            new_signal_value = int(sig_value_name / scale) if not offset else int((sig_value_name - offset) / scale)
            # new_signal_value = int(sig_value_name / scale)
        else:
            logger.error("\nWrong signal value type: {n}:{v}".format(n=signal_name, v=sig_value_name))
            return

        return new_signal_value

    @staticmethod
    def confirm_captured_msg_is_not_none(bus_name, msg_id, msg_name, captured_msg, raise_exception=True):
        err_msg = ""

        if captured_msg is None:
            calling_func_info = Pcan.find_calling_func_info()
            err_msg = "{}Msg {}({:#05x})({}) not found on {} bus!".format(
                calling_func_info, msg_name, msg_id, msg_id, bus_name)

            if raise_exception:
                raise RuntimeError(err_msg)

        return captured_msg is not None, err_msg

    @staticmethod
    def find_calling_func_info():
        frame_info = None
        stack = inspect.stack()

        for i in range(2, 6):
            frame_info = inspect.getframeinfo(stack[i][0])

            if not (frame_info[0].endswith("bus_cmd.py") or
                    frame_info[0].endswith("vehiclechecks.py") or
                    frame_info[0].endswith("nio_dut.py")):
                break

        calling_func_info = "{}:\n{}():{}:\n{}".format(
            frame_info[0], frame_info[2], frame_info[1], frame_info[3][0])

        if calling_func_info == "pytest_pyfunc_call":
            calling_func_info = stack[1][3]

        if calling_func_info == "<module>":
            calling_func_info = stack[4][3]

        return calling_func_info

    def get_bus_obj_from_msg_signals_obj(self, msg_signals_obj):
        bus_name = self._get_bus_name_from_msg_signals_obj(msg_signals_obj)

        bus_obj = self.inst_dict.get(bus_name)  # get bus_object, pcan.bodycan type: SocketCann

        return bus_obj

    def _get_bus_name_from_msg_signals_obj(self, msg_signals_obj):
        # msg_name = msg_signals_obj.__name__                         # "BCM_04"
        # bus_dot_msg_name = msg_signals_obj.__qualname__             # "Body.BCM_04"
        # 'sdk.dut.cgw.pcan.dbc_cls.es8.v7_5_6.bodycan'
        #
        fully_qualified_module_name = msg_signals_obj.__module__

        bus_name = fully_qualified_module_name.split(".")[-1]  # "bodycan"

        return bus_name

    def init_cyclic_msg_task(self):
        pass

    def __get_dbc_ldf_file_bus(self, dbc_ldf_folder):
        """
        mapping dbc file with bus name
        :param dbc_ldf_folder:
        :return:
        """

        bus_names = list(self.cfg.get("bus").keys())
        bus_names.sort(reverse=True)
        dbc_ldf_file_bus_dict = {}

        for f in os.listdir(dbc_ldf_folder):
            if f.endswith('dbc') or f.endswith('ldf'):
                for bus in bus_names:
                    if f.lower().find(bus.lower()) > -1:
                        dbc_ldf_file_bus_dict[bus] = f
                        bus_names.remove(bus)
                        break
        return dbc_ldf_file_bus_dict

    @staticmethod
    def get_bus_names_to_bus_filename_map_dict(dbc_ldf_folder, veh_type):
        """
        Use the given dbc or ldf filename to map the corresponding bus name
        :param dbc_ldf_folder: dbc or ldf file folder location
        :param veh_type: vehicle type like 'ES6', 'FORCE'...
        :return: bus name and bus filename mapping dict
        """
        # Go to Force project branch
        if veh_type.lower() == 'force':
            return Pcan._bus_name_and_filename_mapping_dict_force(dbc_ldf_folder)
        # Go to CGW project branch
        else:
            return Pcan._bus_name_and_filename_mapping_dict_cgw(dbc_ldf_folder)

    @staticmethod
    def _bus_name_and_filename_mapping_dict_cgw(dbc_ldf_folder):
        """
        CGW project use, map the given dbc or ldf filename with the corresponding bus name
        :param dbc_ldf_folder: dbc or ldf file folder location
        :return:  bus name and bus filename mapping dict
        """
        dbc_ldf_file_bus_dict = {}

        for filename in os.listdir(dbc_ldf_folder):
            # DBC file branch
            if filename.endswith('dbc'):
                for bus in PcanConst.CAN_BUS_LIST:
                    if filename.lower().find(bus) > -1:
                        dbc_ldf_file_bus_dict[bus] = filename
            # LDF file branch
            elif filename.endswith('ldf'):
                for bus_num in PcanConst.LIN_BUS_NUMS:
                    m = BusCoreBase.lin_regexp.search(filename)
                    this_bus_num = m.group(1)
                    if bus_num == this_bus_num:
                        dbc_ldf_file_bus_dict[m.group(0).lower()] = filename

        return dbc_ldf_file_bus_dict

    @staticmethod
    def _bus_name_and_filename_mapping_dict_force(dbc_ldf_folder):
        """
        Force project use only, map the given dbc or ldf filename with the corresponding bus name
        :param dbc_ldf_folder: dbc or ldf file folder location
        :return: bus name and bus filename mapping dict
        """
        dbc_ldf_file_bus_dict = {}

        for filename in os.listdir(dbc_ldf_folder):
            if filename.endswith('dbc'):
                # Get the first item of filename split result, which is bus name
                # New filename standard after v0.3.4
                if filename.startswith('CAN'):
                    bus_name_key = filename.split("_")[1].lower().replace(".dbc", "")
                # NT2 old name standard
                else:
                    bus_name_key = filename.split("_")[2]

                if bus_name_key == "rad":
                    bus_name_key = "_".join(filename.split("_")[2:4]).lower()

                dbc_ldf_file_bus_dict[bus_name_key] = filename

            elif filename.endswith('ldf'):
                if len(filename.split("_")) > 3:
                    bus_name_key = filename.split("_")[2].lower()
                else:
                    bus_name_key = filename.split("_")[0]
                    if bus_name_key == 'vcu':
                        continue

                # if bus_name_key == "ilm":
                #     bus_name_key_list = filename.split("_")[2:5]
                #
                #     if "LIN" in bus_name_key_list:
                #         bus_name_key_list.remove("LIN")
                #
                #     bus_name_key = "_".join(bus_name_key_list).lower()

                dbc_ldf_file_bus_dict[bus_name_key] = filename

        return dbc_ldf_file_bus_dict

    def setup_bus_file_ver_envar_and_load_bus_cls_hierarchy(self, parent_obj, class_file_ext):
        """
        loading dbc class structure
        :param parent_obj:
        :param class_file_ext:
        :return:
        """
        pass

    def start_all_cyclic_msg(self):
        for name, inst in self.inst_dict.items():
            if isinstance(inst, SocketCan) and not inst._started._flag:
                inst.start()

    def stop_all_cyclic_msgs(self):
        for name, inst in self.inst_dict.items():
            if isinstance(inst, SocketCan) and inst._started._flag:
                inst.bus.socket.close()
                inst.stop()

    def pause_all_cyclic_msgs(self):
        for name, inst in self.inst_dict.items():
            if isinstance(inst, SocketCan) and inst._started._flag:
                for msg_id_obj in inst.msg_task.values():
                    msg_id_obj.stop()

    def resume_all_cyclic_msgs(self):
        for name, inst in self.inst_dict.items():
            if isinstance(inst, SocketCan) and inst._started._flag:
                for msg_id_obj in inst.msg_task.values():
                    msg_id_obj.start()

    def read_msg_cgw_02(self):
        # To watch this msg, on the NUC, run:
        #   candump can0,0x4c0:7ff -tA
        #

        self.bodycan_bus_obj = self.bodycan

        msg_cgw_02_info = self.dbc.bodycan.CGW_02

        msg_cgw_02 = self.bodycan_bus_obj.read_single_msg(
            can_id=msg_cgw_02_info.msg_id, wait=msg_cgw_02_info.msg_cyc, timeout=2)

        return msg_cgw_02_info, msg_cgw_02

    def read_msg_bgm_02(self):
        # To watch this msg, on the NUC, run:
        #   candump can0,0x4c0:7ff -tA
        #

        self.bodycan_bus_obj = self.bodycan

        msg_bgm_02_info = self.dbc.bodycan.BGM_02

        msg_bgm_02 = self.bodycan_bus_obj.read_single_msg(
            can_id=msg_bgm_02_info.msg_id, wait=msg_bgm_02_info.msg_cyc, timeout=2)

        return msg_bgm_02_info, msg_bgm_02

    def restart_can_msg_publishing(self):
        msg_cgw_02_info, msg_cgw_02 = self.read_msg_cgw_02()
        # restart can msg if msg_cgw_02 is null
        if msg_cgw_02:
            return True
        self.nm_plg_msg_id = self.dbc.bodycan.NM_PLG.msg_id

        # Thanks to Josy for this way to restart CAN msg. publishing.
        self.bodycan_bus_obj.add_cyclic_msg(can_id=self.nm_plg_msg_id, dlc=1, cyclic_rate=0.05)

        # Wait for network to turn off.
        # Believe it or not, it really does take >= 2.88 sec.
        # for all the CAN+LIN msgs to finally turn off, so let's wait 4 sec. here.
        #
        time.sleep(4)

        return True

    def restart_can_msg_publishing_bgm(self):
        msg_bgm_02_info, msg_bgm_02 = self.read_msg_bgm_02()
        # restart can msg if msg_cgw_02 is null
        if msg_bgm_02:
            return True
        self.nm_plg_msg_id = self.dbc.bodycan.NM_PLG.msg_id

        # Thanks to Josy for this way to restart CAN msg. publishing.
        self.bodycan_bus_obj.add_cyclic_msg(can_id=self.nm_plg_msg_id, dlc=1, cyclic_rate=0.05)

        # Wait for network to turn off.
        # Believe it or not, it really does take >= 2.88 sec.
        # for all the CAN+LIN msgs to finally turn off, so let's wait 4 sec. here.
        #
        time.sleep(4)

        return True

    def comparison_helper(self, actual_signal_encoded_value, comparison, expected_signal_value):
        if type(comparison) is int:
            if actual_signal_encoded_value < expected_signal_value:
                return comparison == -1
            elif actual_signal_encoded_value > expected_signal_value:
                return comparison == 1
            else:
                return comparison == 0
        elif type(comparison) is PcanConst.Count:
            return self.comparison_using_count_enum(actual_signal_encoded_value, comparison, expected_signal_value)
        else:
            raise RuntimeError('Unknown comparison type: "{}}'.format(type(comparison)))

    def get_bmuws_info_and_signal_info_from_msg_signals_obj_and_signal_name(
            self, bus_obj, msg_signals_obj, signal_name):

        bus_obj, bmuws_info, cls_signal_obj = \
            self._get_bus_obj_helper(bus_obj, msg_signals_obj, signal_name)

        return bmuws_info, cls_signal_obj

    def get_bus_obj_and_bmuws_info_and_signal_info_from_msg_signals_obj(self, msg_signals_obj, signal_name):
        bus_obj = getattr(msg_signals_obj, "bus_obj", None)

        if bus_obj is None:
            bus_obj = self.get_bus_obj_from_msg_signals_obj(msg_signals_obj)

        return self._get_bus_obj_helper(bus_obj, msg_signals_obj, signal_name)

    def _get_bus_obj_helper_get_bus_obj_helper_get_bus_obj_helper_get_bus_obj_helper(self, bus_obj, msg_signals_obj,
                                                                                     signal_name):
        if signal_name is None:
            cls_signal_obj = None  # This code path is used by lin_routing tests.
            bmuws_info = None
        else:
            cls_signal_obj = getattr(msg_signals_obj, signal_name)

            # bmuws == Byte, Mask, Unmask, Width, Shift.
            bmuws_info = getattr(cls_signal_obj, "bmuws_info", None)

        # Returns bmuws_info = None for signals with no bmuws_info data member.
        return bus_obj, bmuws_info, cls_signal_obj

    def check_with_canlistener(
            self, msg_signals_obj, canlistener_signal_info_obj: CanListenerSignalInfo,
            canlistener_precondition_info_obj: CanListenerPreconditionInfo = None,
            bus_timeout=PcanConst.BUS_TIMEOUT, do_assert=False):
        """
        Using canlistener to check specific signal and signal value with certain times
        :param msg_signals_obj: I.e.,   self.dbc.bodycan.BCM_03 (= cls_signal_obj for each of this msg's signals)
        :param canlistener_signal_info_obj: CanListenerSignalInfo
            The need-to-check msg definition of signal_name, signal value name, max_loop time, expected_count
            please refer to can_signal_info.py to see the structure of this constructor
        :param canlistener_precondition_info_obj: CanListenerPreconditionInfo
            The precondition before checking above signal, defined in can_signal_info.py
        :param bus_timeout: Max checking time allowed
        :param do_assert: Default is False, will raise assertion failure if set to True, else will return check result
        e.g:
            check_with_canlistener(
            msg_signals_obj=self.dbc.bodycan.CGW_INTR_LI, canlistener_signal_info_obj=CanListenerSignalInfo(
                "IntrLiReReaderCmd", "v_Reader_On", max_loop_time=max_time, expected_count=3))
        """
        can_listener = None
        try:
            if canlistener_precondition_info_obj is not None:
                # All this is so we can re-use the CanListener obj just below.
                #
                result, actual_count, expected_count, elapsed_time, timestamp, err_msg, can_listener = \
                    self._check_with_canlistener_helper(
                        msg_signals_obj, canlistener_signal_info_obj, bus_timeout, do_assert)

            result, actual_count, expected_count, elapsed_time, timestamp, err_msg, can_listener = \
                self._check_with_canlistener_helper(
                    msg_signals_obj, canlistener_signal_info_obj, bus_timeout, do_assert, can_listener)
            if expected_count is not None and canlistener_signal_info_obj.count_comparison is not None:
                result = self.comparison_helper(actual_count, canlistener_signal_info_obj.count_comparison, expected_count)
                if not result:
                    calling_func_info = self.find_calling_func_info()

                    err_msg = "" if result else \
                        "\n{}\nactual_count({}) is not {} expected_count({}) FAIL".format(
                            calling_func_info, actual_count,
                            self.comparison_op_strs[canlistener_signal_info_obj.count_comparison + 1], expected_count)

                    if do_assert:
                        assert result, err_msg
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/can_lin/pcan.py")
            logger.error("Met exception during run can_listener, Exception detail as below: {}".format(e))
        finally:
            can_listener.close()
        return result, actual_count, elapsed_time, timestamp, err_msg


        # vehsate ported from bus cmd

    def _get_bus_obj_and_msg_signals_obj_from_bus_name_and_msg_name(self, bus_name, msg_name):
        if bus_name not in self.dbc_obj_dict.keys():
            bus_obj = getattr(self, bus_name)  # cgw.lin type: Lin
            bus_msgs_obj = getattr(self.ldf, bus_name)
        else:
            bus_obj = getattr(self, bus_name)  # cgw.pcan type: SocketCan
            bus_msgs_obj = getattr(self.dbc, bus_name)

        msg_signals_obj = getattr(bus_msgs_obj, msg_name)

        return bus_obj, msg_signals_obj

    def check_on_bus(self, bus_name, msg_name, signal_name, sig_value_name, wait=PcanConst.BUS_DELAY_NODELAY,
                     timeout=PcanConst.BUS_TIMEOUT, comparison=0, do_assert=True):
        bus_obj, msg_signals_obj = self._get_bus_obj_and_msg_signals_obj_from_bus_name_and_msg_name(bus_name, msg_name)
        return self.check(msg_signals_obj, signal_name, sig_value_name, do_assert=do_assert)

    def _check_with_canlistener_pattern_helper(
            self, cls_signal_obj, bmuws_info, bus_obj, canlistener_signal_info_obj: CanListenerSignalInfo, signal_ndx,
            count_ndx, max_count, can_listener, msg_signals_obj, bus_timeout, do_assert):

        target_signal_value = \
            self.lookup_new_signal_value_by_name(
                cls_signal_obj, canlistener_signal_info_obj.signal_name,
                canlistener_signal_info_obj.sig_value_names[signal_ndx])

        bus_name = bus_obj.bus_name
        if can_listener is None:
            can_listener = CanListener(bus_name=bus_name, channel=bus_obj.channel, can_id=msg_signals_obj.msg_id)
        result = False
        timestamp = 0
        actual_count = 0
        elapsed_time = 0.0
        actual_signal_value = 0

        start_time = time.time()

        captured_msg = can_listener.get_all_messages_in_time_range(time_range=bus_timeout)

        captured_msg_result, err_msg = \
            self.confirm_captured_msg_is_not_none(
                bus_obj.bus_name, msg_signals_obj.msg_id, msg_signals_obj.msg_name, captured_msg)

        while captured_msg_result and not result and elapsed_time < canlistener_signal_info_obj.max_loop_time:
            captured_msg = can_listener.get_msg_with_can_id(timeout=bus_timeout, can_id=msg_signals_obj.msg_id)
            logger.info(captured_msg)
            result, actual_signal_value, err_msg = \
                self.check_signal_value_helper(
                    bus_name, msg_signals_obj.msg_name, bmuws_info, canlistener_signal_info_obj.signal_name,
                    cls_signal_obj, captured_msg, target_signal_value, canlistener_signal_info_obj.value_comparison,
                    do_assert)

            if result:
                actual_count += 1

            elapsed_time = time.time() - start_time

            # Magneto should not sleep when reading the CAN message.
            # remove by chad

            if elapsed_time >= canlistener_signal_info_obj.max_loop_time:
                err_msg = \
                    "Can listener for {}.{}[{} of {}] timeout! FAIL".format(
                        canlistener_signal_info_obj.signal_name,
                        canlistener_signal_info_obj.sig_value_names[signal_ndx], count_ndx + 1, max_count)
                if do_assert:
                    raise RuntimeError(err_msg)
                else:
                    logger.error(err_msg)

            time.sleep(0.001)

            timestamp = captured_msg.timestamp

        logger.info("\nresult({}) actual_signal_value({}) actual_count({}) elapsed_time({})\n{}".format(
            result, actual_signal_value, actual_count, elapsed_time, err_msg))

        return result, actual_count, elapsed_time, timestamp, err_msg, can_listener

    def get_msg_content_using_msg_signals_obj_helper(
            self, msg_signals_obj: type, signal_name, sig_value_name, wait, timeout):

        bus_obj, bmuws_info, cls_signal_obj = \
            self.get_bus_obj_and_bmuws_info_and_signal_info_from_msg_signals_obj(msg_signals_obj, signal_name)

        bus_obj, bmuws_info, cls_signal_obj, captured_msg, new_signal_value = \
            self._get_msg_content_helper(
                bus_obj, bmuws_info, cls_signal_obj, msg_signals_obj.msg_id,
                msg_signals_obj.msg_name, signal_name, sig_value_name, wait,
                timeout)

        captured_msg_result = captured_msg is not None
        err_msg = "captured_msg_result = {}".format(captured_msg_result)

        return bus_obj, bmuws_info, cls_signal_obj, captured_msg, new_signal_value, captured_msg_result, err_msg

    def _check_with_canlistener_helper(
            self, msg_signals_obj, canlistener_signal_info_obj: CanListenerSignalInfo, bus_timeout, do_assert,
            can_listener=None):

        bus_obj, bmuws_info, cls_signal_obj = \
            self.get_bus_obj_and_bmuws_info_and_signal_info_from_msg_signals_obj(
                msg_signals_obj, canlistener_signal_info_obj.signal_name)

        if isinstance(canlistener_signal_info_obj.sig_value_names, str):
            canlistener_signal_info_obj.sig_value_names = \
                (canlistener_signal_info_obj.sig_value_names, canlistener_signal_info_obj.expected_count)

        result = False
        elapsed_time = 0.0
        timestamp = 0
        err_msg = ""
        sig_value_count_exp = \
            list(canlistener_signal_info_obj.sig_value_names[1:len(canlistener_signal_info_obj.sig_value_names):2])

        sig_value_count_actual = sig_value_count_exp[:]

        # loop through the signal_value_name + count combination
        for i in range(0, len(canlistener_signal_info_obj.sig_value_names), 2):
            sig_value_name, sig_value_count = canlistener_signal_info_obj.sig_value_names[i:i + 2]

            for j in range(0, sig_value_count):
                result, actual_count, elapsed_time, timestamp, err_msg, can_listener = \
                    self._check_with_canlistener_pattern_helper(
                        cls_signal_obj, bmuws_info, bus_obj, canlistener_signal_info_obj, i, j, sig_value_count,
                        can_listener, msg_signals_obj, bus_timeout, do_assert)

                if not result:
                    sig_value_count_actual[i // 2] -= 1

        logger.info("Actual count for each signal value is {}.".format(sig_value_count_actual))
        logger.info("Expected count for each signal value is {}.".format(sig_value_count_exp))

        return result, sig_value_count_actual, sig_value_count_exp, elapsed_time, timestamp, err_msg, can_listener

    def _get_msg_content_helper(
            self, bus_obj, bmuws_info, cls_signal_obj, msg_id, msg_name, signal_name, sig_value_name, wait, timeout):

        captured_msg = bus_obj.read_single_msg(msg_id, wait=wait, timeout=timeout)

        captured_msg_is_not_none, err_msg = \
            self.confirm_captured_msg_is_not_none(
                bus_obj.bus_name, msg_id, msg_name, captured_msg)

        new_signal_value = self.lookup_new_signal_value_by_name(cls_signal_obj, signal_name, sig_value_name)

        return bus_obj, bmuws_info, cls_signal_obj, captured_msg, new_signal_value

    def get_msg_content_using_msg_signals_obj(
            self, msg_signals_obj: type, signal_name=None, sig_value_name=0, wait=PcanConst.BUS_DELAY_NODELAY,
            timeout=PcanConst.BUS_TIMEOUT):

        bus_obj, bmuws_info, cls_signal_obj, captured_msg, new_signal_value, captured_msg_result, err_msg = \
            self.get_msg_content_using_msg_signals_obj_helper(
                msg_signals_obj, signal_name, sig_value_name, wait, timeout)

        return bus_obj, bmuws_info, cls_signal_obj, captured_msg, new_signal_value, captured_msg_result, err_msg

    def set_with_crc(self, msg_signals_obj, signal_name, sig_value_name,
                     wait=PcanConst.BUS_DELAY_NODELAY, timeout=PcanConst.BUS_TIMEOUT):
        """
        Set a signal's value to the passed-in new value.
        :param msg_signals_obj: I.e.,   self.dbc.bodycan.BCM_03 (= cls_signal_obj for each of this msg's signals)
        :type msg_signals_obj:  I.e.,   class Body.BCM_03
        :param signal_name:     "DoorAjarFrntLeSts"          (= used to get the cls_signal_obj)
        :type signal_name:      str
        :param sig_value_name:  "v_Opened" or 123            (= used to get a new_signal_value)
        :type sig_value_name:
        :param wait:
        :type wait:
        :param timeout:
        :type timeout:
        :return: n/a
        :rtype:  n/a
        """
        if isinstance(sig_value_name, str):
            sig_value_name = sig_value_name.lower()
        bus_obj, bmuws_info, cls_signal_obj, captured_msg, new_signal_value, captured_msg_result, err_msg = \
            self.get_msg_content_using_msg_signals_obj(
                msg_signals_obj, signal_name, sig_value_name, 0, timeout)

        bus_name, bus_obj, msg_id, captured_msg = \
            self.set_new_signal_value_in_captured_msg(
                cls_signal_obj, msg_signals_obj, bmuws_info, captured_msg, new_signal_value, captured_msg_result,
                bus_obj_arg=bus_obj)

        if captured_msg is None:
            return

        if bus_name == 'lin8':
            msg_str = ''.join('{:02x}'.format(x) for x in captured_msg.data[0:7])
            crc8_byte = self.crc8(msg=msg_str)
            captured_msg.data[7] = int(crc8_byte, 16)
            logger.info(captured_msg.data)
        else:
            msg_str = ''.join('{:02x}'.format(x) for x in captured_msg.data[1:4])
            crc8_byte = self.crc8(msg=msg_str)
            captured_msg.data[0] = int(crc8_byte, 16)
            logger.info(captured_msg.data)

        self.write_bus_msg(bus_name, bus_obj, msg_id, captured_msg, wait=wait)

    def set_with_crc8(
        self,
        msg_signals_obj,
        signal_name,
        sig_value_name,
        wait=PcanConst.BUS_DELAY_NODELAY,
        timeout=PcanConst.BUS_TIMEOUT,
        counter=1,
    ):
        """
        Set a signal's value to the passed-in new value.
        :param msg_signals_obj: I.e.,   self.dbc.bodycan.BCM_03 (= cls_signal_obj for each of this msg's signals)
        :type msg_signals_obj:  I.e.,   class Body.BCM_03
        :param signal_name:     "DoorAjarFrntLeSts"          (= used to get the cls_signal_obj)
        :type signal_name:      str
        :param sig_value_name:  "v_Opened" or 123            (= used to get a new_signal_value)
        :type sig_value_name:
        :param wait:
        :param counter: Optional[int]
        :type wait:
        :param timeout:
        :type timeout:
        :return: n/a
        :rtype:  n/a
        """
        if isinstance(sig_value_name, str):
            sig_value_name = sig_value_name.lower()
        logger.info(f"Set {msg_signals_obj}.{signal_name}={sig_value_name}")
        (
            bus_obj,
            bmuws_info,
            cls_signal_obj,
            captured_msg,
            new_signal_value,
            captured_msg_result,
            err_msg,
        ) = self.get_msg_content_using_msg_signals_obj(
            msg_signals_obj, signal_name, sig_value_name, wait, timeout
        )

        (
            bus_name,
            bus_obj,
            msg_id,
            captured_msg,
        ) = self.set_new_signal_value_in_captured_msg(
            cls_signal_obj,
            msg_signals_obj,
            bmuws_info,
            captured_msg,
            new_signal_value,
            captured_msg_result,
            bus_obj_arg=bus_obj,
        )

        if captured_msg is None:
            return
        # Add counter value 1 to the signal
        try:
            captured_msg.data[1] = int(16*counter + (captured_msg.data[1]&0xF))
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/can_lin/pcan.py")
            captured_msg.data[1] = captured_msg.data[1]%16
        finally:
            msg_str = "".join("{:02x}".format(x) for x in captured_msg.data[1:])
            logger.debug("Message payload before CRC {}".format(captured_msg.data))
            crc8_byte = self.crc8(msg=msg_str)
            logger.debug("Message payload after CRC {} ".format(captured_msg.data))
            captured_msg.data[0] = int(crc8_byte, 16)
            self.write_bus_msg(bus_name, bus_obj, msg_id, captured_msg, wait=wait)

    def set_lin_with_crc8(
        self,
        msg_signals_obj,
        signal_name,
        sig_value_name,
        wait=PcanConst.BUS_DELAY_NODELAY,
        timeout=PcanConst.BUS_TIMEOUT,
        counter=1,
    ):
        """
        Set a signal's value to the passed-in new value.
        :param msg_signals_obj: I.e.,   self.dbc.bodycan.BCM_03 (= cls_signal_obj for each of this msg's signals)
        :type msg_signals_obj:  I.e.,   class Body.BCM_03
        :param signal_name:     "DoorAjarFrntLeSts"          (= used to get the cls_signal_obj)
        :type signal_name:      str
        :param sig_value_name:  "v_Opened" or 123            (= used to get a new_signal_value)
        :type sig_value_name:
        :param wait:
        :param counter: Optional[int]
        :type wait:
        :param timeout:
        :type timeout:
        :return: n/a
        :rtype:  n/a
        """
        if isinstance(sig_value_name, str):
            sig_value_name = sig_value_name.lower()
        logger.info(f"Set {msg_signals_obj}.{signal_name}={sig_value_name}")
        (
            bus_obj,
            bmuws_info,
            cls_signal_obj,
            captured_msg,
            new_signal_value,
            captured_msg_result,
            err_msg,
        ) = self.get_msg_content_using_msg_signals_obj(
            msg_signals_obj, signal_name, sig_value_name, wait, timeout
        )

        (
            bus_name,
            bus_obj,
            msg_id,
            captured_msg,
        ) = self.set_new_signal_value_in_captured_msg(
            cls_signal_obj,
            msg_signals_obj,
            bmuws_info,
            captured_msg,
            new_signal_value,
            captured_msg_result,
            bus_obj_arg=bus_obj,
        )

        if captured_msg is None:
            return
        # Add counter value 1 to the signal
        try:
            captured_msg.data[6] = int(16*counter + (captured_msg.data[6]&0xF))
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/can_lin/pcan.py")
            captured_msg.data[6] = captured_msg.data[6]%16
        finally:
            msg_str = "".join("{:02x}".format(x) for x in captured_msg.data[0:7])
            logger.debug("Message payload before CRC {}".format(captured_msg.data))
            crc8_byte = self.crc8(msg=msg_str)
            logger.debug("Message payload after CRC {} ".format(captured_msg.data))
            captured_msg.data[7] = int(crc8_byte, 16)
            self.write_bus_msg(bus_name, bus_obj, msg_id, captured_msg, wait=wait)

    @staticmethod
    def crc8(msg, div=0x1D):
        """
        Cyclic Redundancy Check == CRC8 SAE-J1850
        Generates an error detecting code based on an inputted message and divisor in the form of a polynomial
        representation.

        :param msg: The input message of which to generate the output code.
        :param div: The divisor in polynomial form. For example, if the polynomial of x^3 + x + 1 is given,
                    this should be represented as '1011' in the div argument.
                    Use a divisor that simulates: CRC8 SAE-J1850 x^8+x^4+x^3+x^2+x^0
        :return: An one-byte error-detecting code generated by the message and the given divisor.
        """
        t_crc = 0xFF
        i = 0
        while i < len(msg):
            t_crc ^= int(msg[i:i + 2], 16)
            b = 0
            while b < 8:
                if (t_crc & 0x80) != 0:
                    t_crc <<= 1
                    t_crc ^= div
                else:
                    t_crc <<= 1
                b += 1
            i += 2
        # in Python, the bit flip operator is different, so we need to construct the number
        # t_crc = bin(~t_crc)
        last_8bit = bin(t_crc)[-8::]
        last_8bit_flip = ''.join('1' if x == '0' else '0' for x in last_8bit)
        flip_int = int(last_8bit_flip, 2)
        hex_result = hex(flip_int)

        # Check the length of the CRC8. If length=1, prefix "0" to the string
        str_result = hex_result.replace('0x', '').upper()
        if len(str_result) == 1:
            return "0" + str_result
        else:
            return str_result

    def check_signal_value_helper(
            self, bus_name, msg_name, bmuws_info, signal_name, cls_signal_obj, captured_msg, expected_signal_value,
            comparison, do_assert):

        if bmuws_info is None:
            # Single-byte signal.
            encoded_actual_signal_value = \
                (captured_msg.data[cls_signal_obj.byte] & cls_signal_obj.mask) >> cls_signal_obj.shift
        else:
            # Multi-byte or straddling-two-bytes signal.
            encoded_actual_signal_value = 0

            # First the encoded_actual_signal_value's LSbyte receives the signal's LSbyte.
            # Then the encoded_actual_signal_value is left-shifted, to prepare for next receiving the signals's LSbyte.
            #
            if bus_name not in self.dbc_obj_dict.keys():
                bmuws_info = reversed(bmuws_info)

            for byte, mask, unmask, width, shift in bmuws_info:
                # In the new_signal_value, keep only this signal_byte's bits,
                # and shift to them to the correct bit position in the msg.
                signal_byte_val = (captured_msg.data[byte] & mask) >> shift

                shifted_actual_signal_value = encoded_actual_signal_value << width

                encoded_actual_signal_value = shifted_actual_signal_value + signal_byte_val

        return self.check_signal_value_helper_helper(
            encoded_actual_signal_value, comparison, expected_signal_value,
            bus_name, cls_signal_obj, msg_name, signal_name, do_assert)

    def check_signal_value_helper_helper(
            self, encoded_actual_signal_value, comparison, expected_signal_value,
            bus_name, cls_signal_obj, msg_name, signal_name, do_assert=True):

        result = self.comparison_helper(encoded_actual_signal_value, comparison, expected_signal_value)

        # I.e., err_msg = "cdc.ACM_01.SeatBltFrntLeSts(1) != 0"
        err_msg = ""

        if not result:
            calling_func_info = self.find_calling_func_info()

            err_msg = "\n{}{}.{}.{}({}) not {}".format(
                calling_func_info, bus_name, msg_name, signal_name, encoded_actual_signal_value,
                self.comparison_msg_helper(comparison, cls_signal_obj, expected_signal_value))

            if do_assert:
                assert result, err_msg

        return result, encoded_actual_signal_value, err_msg

    comparison_op_strs = ("<", "==", ">")

    def comparison_msg_helper(self, comparison, cls_signal_obj, expected_signal_value):
        if type(comparison) is int:
            msg = "{} {}".format(self.comparison_op_strs[comparison + 1], expected_signal_value)
        elif type(comparison) is PcanConst.Count:
            if comparison is PcanConst.Count.IN_RANGE:
                msg = "in range({},{})".format(cls_signal_obj.min, cls_signal_obj.max)
            else:
                msg = "{} {}".format(comparison.name, expected_signal_value)
        else:
            raise RuntimeError('Unknown comparison type: "{}}'.format(type(comparison)))

        return msg

    def comparison_using_count_enum(self, actual_signal_encoded_value, count_enum, expected_signal_value):
        if count_enum is PcanConst.Count.EQ:
            return actual_signal_encoded_value == expected_signal_value
        elif count_enum is PcanConst.Count.LE:
            return actual_signal_encoded_value <= expected_signal_value
        elif count_enum is PcanConst.Count.LT:
            return actual_signal_encoded_value < expected_signal_value
        elif count_enum is PcanConst.Count.GE:
            return actual_signal_encoded_value >= expected_signal_value
        elif count_enum is PcanConst.Count.GT:
            return actual_signal_encoded_value > expected_signal_value
        elif count_enum is PcanConst.Count.IN_RANGE:
            # Here the expected_signal_value contains:
            actual_signal_decoded_value, min_value, max_value = expected_signal_value

            # If this signal has enum_value_names, actual_signal_decoded_value will be a string,
            # which is useless to us here, so compare actual_signal_encoded_value to min and max instead of
            # actual_signal_decoded_value.
            #
            if isinstance(actual_signal_decoded_value, str):
                result = min_value <= actual_signal_encoded_value <= max_value
            else:  # Both floating_point and int values come here.
                result = min_value <= actual_signal_decoded_value <= max_value
        else:
            raise RuntimeError('Unknown Count enum: "{}"'.format(count_enum))

        return result

    @staticmethod
    def call_car_platform_dut_ver_bus_type_partial_paths_parent_dir_handler(
            handler_func, dut_path, ecu_under_test_name_only = True, return_only_default_dut_ver=False):
        """
        Called by:
            tools/scripts_generator/generate_cls_defs_and_cyc_json.py
            tools/scripts_generator/lin_v3.x_summary_file_to_test_lin-parser.py

        Parameters
        ----------
        dut_path : dut path absolute path
        handler_func :
        return_only_default_dut_ver :
        """
        parent_dir = dut_path

        car_platforms_dirs_for_all_dut_vers = \
            Pcan._collect_platform_bus_directories(return_only_default_dut_ver, dut_path)

        for car_platform, car_platform_info in car_platforms_dirs_for_all_dut_vers.items():
            for dut_ver, buses_info in car_platform_info.items():
                # partial_paths -> {'json': 'xxx', 'bus': 'xxx', 'cls': 'xxx'}
                # bus_type_enum -> BusType.CAN
                for bus_type_enum, partial_paths in buses_info.items():
                    # if bus_type_enum.value == "lin":
                    #     continue
                    handler_func(car_platform, dut_ver, bus_type_enum, partial_paths, parent_dir, ecu_under_test_name_only)

    @staticmethod
    def _collect_platform_bus_directories(return_only_default_dut_ver, dut_path):
        """
        Called by:
            Pcan.call_car_platform_dut_ver_bus_type_partial_paths_parent_dir_handler()

        This is static because its callers are called externally, thus this call tree needs to be static.

        :return:
        :rtype:
        """
        dbc_ldf_cfg_file, dbc_ldf_info_for_all_car_platforms = \
            Pcan._get_dbc_ldf_config_helper(dut_path)

        car_platforms_dirs_for_all_cgw_vers = {}

        for car_platform_enum in PcanConst.CarPlatform:
            if not dbc_ldf_info_for_all_car_platforms.get(car_platform_enum.value):
                continue
            this_car_platform_info_for_all_cgw_versions = \
                dbc_ldf_info_for_all_car_platforms[car_platform_enum.value]

            car_platforms_dirs_for_this_cgw_ver = {}

            # this_car_platform_info_for_all_cgw_versions = [{'dut_ver': '00.01'}, {'dut_ver': 'default'}]
            for this_car_platform_info_for_this_cgw_version in this_car_platform_info_for_all_cgw_versions:
                cgw_ver = this_car_platform_info_for_this_cgw_version["dut_ver"]

                if (cgw_ver == "default") ^ return_only_default_dut_ver:
                    continue

                car_platforms_dirs_for_this_cgw_ver[cgw_ver] = \
                    Pcan._collect_platform_bus_directories_helper(
                        this_car_platform_info_for_this_cgw_version)

            car_platforms_dirs_for_all_cgw_vers[car_platform_enum.value] = \
                car_platforms_dirs_for_this_cgw_ver

        return car_platforms_dirs_for_all_cgw_vers

    @staticmethod
    def _get_dbc_ldf_config_helper(dut_path):
        """
        Called by:
            CgwCan.get_dbc_ldf_config()
            CgwCan._collect_platform_bus_directories()

        This is static because its callers are called externally, thus this call tree needs to be static.

        :return:
        :rtype:
        """

        dbc_ldf_cfg_file_path = "{}/../config/dbc_ldf_config.yaml".format(dut_path)

        try:
            with open(dbc_ldf_cfg_file_path, 'rb') as f:
                cfg = list(yaml.safe_load_all(f))[0]
        except FileNotFoundError as err:
            logger.error("Load {} failed.\n{}".format(dbc_ldf_cfg_file_path, err))
            return False

        return dbc_ldf_cfg_file_path, cfg

    @staticmethod
    def create_test_file_dir_if_absent(test_file_dir):
        if os.path.isfile(test_file_dir):
            raise RuntimeError('directory "{}" is a file, not a directory!'.format(test_file_dir))

        if not os.path.isdir(test_file_dir):
            # mkdir() is for one layer directory, so we use makedirs() for multi-layer directories
            os.makedirs(test_file_dir)

    @staticmethod
    def _collect_platform_bus_directories_helper(this_car_platform_info_for_this_cgw_version):
        """
        Called by:
            Pcan._collect_platform_bus_directories()

        This is static because its callers are called externally, thus this call tree needs to be static.

        :param this_car_platform_info_for_this_cgw_version:
        :type this_car_platform_info_for_this_cgw_version:
        :return:
        :rtype:
        """
        paths_dict = this_car_platform_info_for_this_cgw_version["veh_gen"][0]

        car_platform_dirs = {}

        for bus_type_enum in PcanConst.BusType:
            bus_type_name = bus_type_enum.name

            if bus_type_name == "CAN":
                bus_type_dirs = {
                    "json": paths_dict["dbc_cyc_json_path"],
                    "bus": paths_dict["dbc_path"],
                    "cls": paths_dict["dbc_cls_path"]
                }
            else:
                bus_type_dirs = {
                    "json": None,
                    "bus": paths_dict["ldf_path"],
                    "cls": paths_dict["ldf_cls_path"]
                }

            # So Force can use "BGM" instead of "CGW" as msg sender or receiver.
            bus_type_dirs["ecu_under_test"] = paths_dict["dbc_cyc_json_ecu"]

            car_platform_dirs[bus_type_enum] = bus_type_dirs

        return car_platform_dirs

    def _get_bus_obj_helper(self, bus_obj, msg_signals_obj, signal_name):
        if signal_name is None:
            cls_signal_obj = None  # This code path is used by lin_routing tests.
            bmuws_info = None
        else:
            cls_signal_obj = getattr(msg_signals_obj, signal_name)

            # bmuws == Byte, Mask, Unmask, Width, Shift.
            bmuws_info = getattr(cls_signal_obj, "bmuws_info", None)

        # Returns bmuws_info = None for signals with no bmuws_info data member.
        return bus_obj, bmuws_info, cls_signal_obj

    # for bus_listener, we have to port it......
    # Todo will update it later......
    def check_with_bus_listener(
            self, msg_signals_obj, precondition_signals_values_pattern=None, signals_values_pattern=None,
            bus_timeout=PcanConst.BUS_TIMEOUT, do_assert=False):
        """
        See arg descriptions in:
            sdk/dut/cgw/pcan/bus_cmd-README.txt
        """

        pattern_result = True
        pattern_step_results = []
        pattern_step_err_msgs = [""]

        # Process precondition_signals_values_pattern, which is the precondition pattern to gather counts for,
        # of CAN msgs that match our (signal, value)-pairs.
        #
        if precondition_signals_values_pattern is not None:
            logger.info("")
            logger.info("Checking arg: precondition_signals_values_pattern\n")

            pattern_result, pattern_step_results, pattern_step_err_msgs = self._pattern_step_loop(
                msg_signals_obj, precondition_signals_values_pattern.pattern_info,
                bus_timeout, do_assert, non_matching_check_result_means_fail=False)

        # Process signals_values_pattern, which is the actual pattern to gather counts for,
        # of CAN msgs that match our (signal, value)-pairs.
        #
        if pattern_result:
            logger.info("Checking arg: signals_values_pattern\n")

            pattern_result, pattern_step_results, pattern_step_err_msgs = self._pattern_step_loop(
                msg_signals_obj, signals_values_pattern.pattern_info,
                bus_timeout, do_assert, non_matching_check_result_means_fail=True)

        err_msgs_summary = self._flatten_err_msgs_nested_lists(pattern_step_err_msgs)

        return pattern_result, pattern_step_results, err_msgs_summary

    def _pattern_step_loop(
            self, msg_signals_obj, signals_values_pattern, bus_timeout, do_assert,
            non_matching_check_result_means_fail=False):

        bus_obj = self.get_bus_obj_from_msg_signals_obj(msg_signals_obj)
        bus_name = bus_obj.bus_name
        # verify if can_listener is available
        if 'can_listener' not in locals():
            can_listener = CanListener(bus_name=bus_name, channel=bus_obj.channel, can_id=msg_signals_obj.msg_id)
        pattern_result = True
        pattern_step_results = []
        pattern_step_err_msgs = []

        # *** Collect all the pattern_steps' results for this pattern_step. ***
        #
        # Exit ramps for this loop:
        #   timeout
        #   (???) if non_matching_check_result_means_fail == True:
        #      if any _pattern_step_count_signal_loop() iteration returns False,
        #         exit out of this loop and return the failure.
        #
        # See the pattern_step discussion in:
        #   sdk/dut/cgw/pcan/bus_cmd-README.txt
        #
        # Successful completion of a pattern_step is:
        #   all "count"(i.e., == 4) of the specified (signal, value)-pairs matched.
        #
        # This arg:
        #   non_matching_check_result_means_fail
        #
        # controls whether or not a non-matching (signal, value)-pair check causes failure.
        #
        try:
            for pattern_step_ndx, pattern_step in enumerate(signals_values_pattern):
                loop_ndx = 0
                in_first_loop_iteration = True
                time_now = time.time()
                end_time = time_now + pattern_step["pattern_step_max_loop_time"]

                while time_now < end_time:
                    # Call _pattern_step_count_loop() inside of its wrapper:
                    #   _pattern_step_count_loop_repeat_until_timeout_helper()
                    #
                    pattern_result = self._pattern_step_count_loop_repeat_until_timeout_helper(
                        bus_obj, pattern_step_ndx, pattern_step, msg_signals_obj,
                        bus_timeout, do_assert, can_listener, end_time,
                        non_matching_check_result_means_fail, pattern_result,
                        pattern_step_results, pattern_step_err_msgs, in_first_loop_iteration)

                    # Successful completion of a pattern_step is:
                    #   all "count"(i.e., == 4) of the required (signal, value)-pairs matched.
                    # Alternatively, if failures are ok, keep trying again until timeout.
                    #
                    if pattern_result or non_matching_check_result_means_fail:
                        # All is well so move on to processing the next pattern_step.
                        break

                    # This path is for when we just want to accumulate counts until the timeout.
                    #
                    time.sleep(0.01)

                    time_now = time.time()

                    loop_ndx += 1  # For debugging.

                    in_first_loop_iteration = False

                else:  # timeout comes here.
                    # There is no time left to do any more pattern_steps, so exit our for() loop too.
                    #
                    logger.error("TIMED OUT!")
                    timeout_err_msg = \
                        "pattern_({}): after looping {} times: TIMED OUT! FAIL".format(pattern_step_ndx, loop_ndx)

                    # Let the caller know what happened.
                    pattern_step_err_msgs.append(timeout_err_msg)

                    # Just give up and return results to the caller.
                    break

                # Here we've dropped through to continue on to the next pattern_step.
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/can_lin/pcan.py")
            logger.error("Got exception {} during call listener".format(e))
        finally:
            can_listener.close()
        return pattern_result, pattern_step_results, pattern_step_err_msgs

    def comparison_using_tuple(self, actual_value, expected_value_tuple):
        comparison_enum, expected_value = expected_value_tuple

        if comparison_enum is PcanConst.Count.EQ:
            return actual_value == expected_value
        elif comparison_enum is PcanConst.Count.LE:
            return actual_value <= expected_value
        elif comparison_enum is PcanConst.Count.LT:
            return actual_value < expected_value
        elif comparison_enum is PcanConst.Count.GE:
            return actual_value >= expected_value
        elif comparison_enum is PcanConst.Count.GT:
            return actual_value > expected_value

    def _pattern_step_count_loop_repeat_until_timeout_helper(
            self, bus_obj, pattern_step_ndx, pattern_step, msg_signals_obj, bus_timeout, do_assert, can_listener,
            end_time, non_matching_check_result_means_fail, pattern_result, pattern_step_results, pattern_step_err_msgs,
            in_first_loop_iteration):

        """
        Wrap the calling of _pattern_step_count_loop(), which does:
            *** Collect the results of all of the pattern_step_counts for this pattern_step. ***

        Gather up and return the error results according to the value of:
            non_matching_check_result_means_fail
        """
        pattern_step_result, pattern_step_count_results, pattern_step_count_err_msgs = \
            self._pattern_step_count_loop(
                bus_obj, pattern_step_ndx + 1, pattern_step, msg_signals_obj, bus_timeout,
                do_assert, can_listener, end_time, non_matching_check_result_means_fail,
                in_first_loop_iteration)
        result_without_ignored_failures = \
            pattern_step_result or not non_matching_check_result_means_fail

        # If any of the signal_values were not as expected,
        # override failure if there is a lower-bound criteria that we have met.
        #
        if not result_without_ignored_failures:
            expected_count_info = pattern_step["expected_count_info"]

            if len(expected_count_info) > 1:
                pattern_step_result = self.comparison_using_tuple(pattern_step_ndx, expected_count_info[0])

        if len(pattern_step_count_err_msgs) > 0:
            pattern_step_err_msgs.append(pattern_step_count_err_msgs)

        pattern_result &= pattern_step_result
        pattern_step_results.append(pattern_step_count_results)

        return pattern_result

    def _pattern_step_count_loop(
            self, bus_obj, pattern_step_ndx, pattern_step, msg_signals_obj, bus_timeout, do_assert,
            can_listener, end_time, non_matching_check_result_means_fail, in_first_loop_iteration):

        """
        We need the max # of counts (iterations of reading CAN msgs) to check, as described in:
            _pattern_step_loop()

        Each pattern_step can have different (signal, signal_value)-pairs to check, so we need to populate:
            bmuws_info
            signal_info
        once for each (signal, signal_value)-pair, at the start of each pattern step.
        We save the values away so this function only gathers them once.
        """
        signal_and_value_dicts = \
            self._populate_pattern_step_signal_and_value_dicts(pattern_step, bus_obj, msg_signals_obj)

        max_count = signal_and_value_dicts[0]

        # logger.info("")
        if in_first_loop_iteration:
            logger.info("pattern_step({}): looping for count = 1 thru {}".format(pattern_step_ndx, max_count))

        pattern_step_result = True
        pattern_step_count_results = []
        pattern_step_count_err_msgs = []

        # *** Collect all the pattern_step_counts' results for this pattern_step. ***
        #
        # Exit ramps for this loop:
        #   timeout
        #   if non_matching_check_result_means_fail == True:
        #      any _pattern_step_count_signal_loop() iteration returning False
        #      will cause exiting out of this loop and returning the failure.
        #
        for pattern_step_count_ndx in range(1, max_count + 1):
            pattern_step_count_result, pattern_step_count_signal_results, pattern_step_count_signal_err_msgs = \
                self._pattern_step_count_signal_loop(
                    pattern_step_ndx, pattern_step_count_ndx, signal_and_value_dicts[1:], bus_timeout, do_assert,
                    can_listener, non_matching_check_result_means_fail, in_first_loop_iteration)

            # Re: err_msgs, we took care of non_matching_check_result_means_fail
            # in _pattern_step_count_signal_loop(), so we don't have to consider it here.
            if len(pattern_step_count_signal_err_msgs) > 0:
                pattern_step_count_err_msgs.append(pattern_step_count_signal_err_msgs)

            pattern_step_result &= pattern_step_count_result
            pattern_step_count_results.append(pattern_step_count_signal_results)

            result_without_ignored_failures = \
                pattern_step_count_result or not non_matching_check_result_means_fail

            # No point in continuing if any of the signal_values were not as expected.
            if not result_without_ignored_failures:
                logger.error("\nnon-matching (signal, value)-pair!:\n{}".format(pattern_step_count_err_msgs))
                break

            # We want to complete a given pattern_step before we bail out of this loop due to timeout,
            # so we can have complete err_msg data to return to the caller.
            # But if time is up, we will not do any further pattern_step_count's.
            #
            timed_out, timeout_err_msg = self._pattern_step_count_timeout_err_msg_helper(
                end_time, pattern_step_ndx, pattern_step_count_ndx)

            if timed_out:
                pattern_step_count_err_msgs.append(timeout_err_msg)
                break

        # Gather and return all the results, in case there were multiple failures to report.
        return pattern_step_result, pattern_step_count_results, pattern_step_count_err_msgs

    def _pattern_step_count_signal_loop(
            self, pattern_step_ndx, pattern_step_count_ndx, signal_and_value_dicts, bus_timeout, do_assert,
            can_listener,
            non_matching_check_result_means_fail, in_first_loop_iteration):

        pattern_step_count_result = True
        pattern_step_count_signal_results = []
        pattern_step_count_signal_err_msgs = []

        # Each pattern_step count (i.e., 2, or 3, or 4) needs its own new captured_msg, so read a new one here.
        captured_msg = can_listener.get_msg(timeout=bus_timeout)

        # TODO: Confirm that no unwanted signal_values occur.

        # *** Collect the results of all of the signal_value checks for this pattern_step_count. ***
        #
        # Exit ramps for this loop:
        #   none, because timeout has no effect here
        #
        # This is because we want to return a complete set of data for this pattern_step_count to the caller.
        #
        # Check that each of the (signal, value)-pairs match in this pattern_step_count match.
        #
        for signal_and_value_dict in signal_and_value_dicts:
            pattern_step_count_signal_result, actual_signal_value, err_msg = \
                self._pattern_step_count_signal_value_check(signal_and_value_dict, captured_msg, do_assert)

            if len(err_msg):
                # Here we only need the last line of the err_msg.
                err_msg = "\n{}".format(err_msg.split("\n")[-1])

            result_without_ignored_failures = \
                pattern_step_count_signal_result or not non_matching_check_result_means_fail

            signal_name, signal_value_name = signal_and_value_dict["signal_and_value"]
            expected_signal_value = signal_and_value_dict["expected_signal_value"]

            formatted_err_msg = self._get_formatted_err_msg(
                pattern_step_ndx, pattern_step_count_ndx, signal_name, actual_signal_value,
                pattern_step_count_signal_result, signal_value_name, expected_signal_value,
                result_without_ignored_failures, err_msg)

            # For now print this info even when all is well, for debugging purposes.
            if in_first_loop_iteration:
                logger.info("     {}".format(formatted_err_msg))

            if len(err_msg) > 0 and non_matching_check_result_means_fail:
                pattern_step_count_signal_err_msgs.append("\n{}".format(formatted_err_msg))

            pattern_step_count_signal_results.append(
                (pattern_step_count_signal_result, actual_signal_value, expected_signal_value))

            pattern_step_count_result &= pattern_step_count_signal_result

        if in_first_loop_iteration:
            logger.info("")

        # Gather and return all the results, in case there were multiple failures to report.
        return pattern_step_count_result, pattern_step_count_signal_results, pattern_step_count_signal_err_msgs

    def _pattern_step_count_signal_value_check(self, signal_and_value_dict, captured_msg, do_assert):
        """
        At this level, the captured_msg is passed in.

        All signals in this pattern_step_count get their values from the same captured_msg.

        Get the signal's value from captured_msg.

        Check if that value matches (signal, signal_value)-pair.
        """
        # Since this has no loop, replace this info with the various possible
        # return values and behaviors that can happen here, and in which situations
        # they can happen.
        #
        # Exit ramps for this loop:
        #   end_time has arrived.
        #
        #   non_matching_check_result_means_fail:
        #       True  =>
        #       False =>
        #
        bmuws_info = signal_and_value_dict["bmuws_info"]

        bus_obj = signal_and_value_dict["bus_obj"]
        msg_signals_obj = signal_and_value_dict["msg_signals_obj"]

        signal_info = signal_and_value_dict["signal_info"]
        signal_name = signal_and_value_dict["signal_and_value"][0]
        expected_signal_value = signal_and_value_dict["expected_signal_value"]

        return self.check_signal_value_helper(
            bus_obj.bus_name, msg_signals_obj.msg_name, bmuws_info, signal_name, signal_info,
            captured_msg, expected_signal_value, PcanConst.Count.EQ, do_assert)

    def _populate_pattern_step_signal_and_value_dicts(self, pattern_step, bus_obj, msg_signals_obj):
        """
        Squirrel away bmuws_info and signal_info once,
        so we don't have to keep looking them up over and over.
        """
        signal_and_value_dicts = pattern_step["signal_and_value_dicts"]
        expected_count_info = pattern_step["expected_count_info"]

        # Did we already prepend max_count into signal_and_value_dicts[0]?
        #
        if not isinstance(signal_and_value_dicts[0], int):
            self._populate_pattern_step_signal_and_value_dicts_helper(signal_and_value_dicts, bus_obj, msg_signals_obj)

            # The caller will use a array_slice to remove this where needed.
            signal_and_value_dicts.insert(0, self._get_max_count(expected_count_info))

        return signal_and_value_dicts

    def _populate_pattern_step_signal_and_value_dicts_helper(self, signal_and_value_dicts, bus_obj, msg_signals_obj):
        for signal_and_value_dict in signal_and_value_dicts:
            signal_name, signal_value_name = signal_and_value_dict["signal_and_value"]

            bmuws_info, signal_info = \
                self.get_bmuws_info_and_signal_info_from_msg_signals_obj_and_signal_name(
                    bus_obj, msg_signals_obj, signal_name)

            expected_signal_value = \
                self.lookup_new_signal_value_by_name(signal_info, signal_name, signal_value_name)

            signal_and_value_dict["bmuws_info"] = bmuws_info
            signal_and_value_dict["bus_obj"] = bus_obj
            signal_and_value_dict["msg_signals_obj"] = msg_signals_obj
            signal_and_value_dict["signal_info"] = signal_info
            signal_and_value_dict["expected_signal_value"] = expected_signal_value

    def _get_max_count(self, expected_value_tuples):
        """
        Return the maximum possible # to count up to that could still be success.
        """
        if isinstance(expected_value_tuples, tuple):
            final_comparison_enum, final_expected_value = expected_value_tuples
        elif len(expected_value_tuples) == 0:
            return 999999  # This is used when the expected_value_info is omitted.
        else:
            final_comparison_enum, final_expected_value = expected_value_tuples[-1]

        if final_comparison_enum is PcanConst.Count.EQ:
            return final_expected_value
        elif final_comparison_enum is PcanConst.Count.LT:
            return final_expected_value - 1
        elif final_comparison_enum is PcanConst.Count.LE:
            return final_expected_value
        elif final_comparison_enum is PcanConst.Count.GE:
            return final_expected_value
        elif final_comparison_enum is PcanConst.Count.GT:
            return final_expected_value + 1

    def _get_pass_fail_ok_string(self, result, filtered_result):
        if result:
            return "PASS"
        elif result != filtered_result:
            return "OK"
        else:
            return "FAIL"

    def _flatten_err_msgs_nested_lists(self, pattern_step_err_msgs):
        err_msgs_list = []

        for outer_list_entry in pattern_step_err_msgs:
            if self._flatten_err_msgs_nested_lists_helper(outer_list_entry, err_msgs_list):
                continue

            for middle_list_entry in outer_list_entry:
                if self._flatten_err_msgs_nested_lists_helper(middle_list_entry, err_msgs_list):
                    continue

                for err_msg in middle_list_entry:
                    self._flatten_err_msgs_nested_lists_helper(err_msg, err_msgs_list)

        err_msgs_summary = "\n{}".format("\n".join(err_msgs_list))

        return err_msgs_summary

    def _flatten_err_msgs_nested_lists_helper(self, entry, err_msgs_list):
        if isinstance(entry, str):
            if len(entry) > 0:
                err_msgs_list.append(entry)

            return True
        else:
            return False

    def _pattern_step_count_timeout_err_msg_helper(
            self, end_time, pattern_step_ndx, pattern_step_count_ndx):
        time_now = time.time()

        timed_out = time_now > end_time

        if time_now > end_time:
            timeout_err_msg = \
                "pattern_step, count({}, {}): TIMED OUT! FAIL".format(pattern_step_ndx, pattern_step_count_ndx)
        else:
            timeout_err_msg = ""

        return timed_out, timeout_err_msg

    def _get_formatted_err_msg(
            self, pattern_step_ndx, pattern_step_count_ndx, signal_name, actual_signal_value,
            pattern_step_count_signal_result, signal_value_name, expected_signal_value,
            result_without_ignored_failures, err_msg):

        pass_fail_string = \
            self._get_pass_fail_ok_string(pattern_step_count_signal_result, result_without_ignored_failures)

        err_msg_with_status = "{} {}".format(err_msg, pass_fail_string) if len(err_msg) > 0 else ""

        return "pattern_step, count({}, {}): {}({}) {}== {}({}) {}{}".format(
            pattern_step_ndx, pattern_step_count_ndx, signal_name, actual_signal_value,
            ("" if pattern_step_count_signal_result else "not "), signal_value_name,
            expected_signal_value, pass_fail_string, err_msg_with_status)

    @staticmethod
    def get_bus_names_to_bus_ext_filenames_map(bus_file_ext_dir, veh_type):
        can_bus_names_to_dbc_filenames_map = {}
        # Currently not sure if there are different veh_type in force project
        # for this situation, just call force.
        if veh_type in ['force']:
            bus_names = PcanConst.BGM_CAN_BUS_LIST if "dbc" in bus_file_ext_dir else PcanConst.BGM_LIN_BUS_LIST
        else:
            bus_names = PcanConst.CAN_BUS_LIST if "dbc" in bus_file_ext_dir else PcanConst.LIN_BUS_LIST
        for filename in os.listdir(bus_file_ext_dir):
            if filename.endswith('dbc') or filename.endswith('ldf'):
                for bus in bus_names:
                    # if filename.lower().find(bus+'_') > -1:
                    if filename.lower().find(bus) > -1:
                        can_bus_names_to_dbc_filenames_map[bus] = filename
                        break

        return can_bus_names_to_dbc_filenames_map

    def check_msg(self, msg_obj, timeout=1.0):
        # msg_signals_obj : type
        # self.dbc.bodycan.BCM_03
        fully_qualified_module_name = msg_obj.__module__
        bus_name = fully_qualified_module_name.split(".")[-1]  # "bodycan"
        # Get bus_obj from inst_dict
        bus_obj = self.inst_dict.get(bus_name)

        captured_msg = bus_obj.read_single_msg_from_obj(msg_obj, timeout=timeout)

        is_receive, err_msg = self.confirm_captured_msg_is_not_none(bus_obj.bus_name,msg_obj.msg_id, msg_obj.msg_name,
                                                                    captured_msg, raise_exception=False)
        if is_receive:
            return True
        else:
            return False

    def get_msg_date(self, msg_obj, timeout=1.0):
        # msg_signals_obj : type
        # self.dbc.bodycan.BCM_03
        fully_qualified_module_name = msg_obj.__module__
        bus_name = fully_qualified_module_name.split(".")[-1]  # "bodycan"
        # Get bus_obj from inst_dict
        bus_obj = self.inst_dict.get(bus_name)

        captured_msg = bus_obj.read_single_msg_from_obj(msg_obj, timeout=timeout)

        is_receive, err_msg = self.confirm_captured_msg_is_not_none(bus_obj.bus_name,
                                                                      msg_obj.msg_id, msg_obj.msg_name, captured_msg)
        if is_receive:
            return captured_msg
        else:
            return False

    def check_msg_cycle_time(self, msg_obj, timeout=1.0):
        # msg_signals_obj : type
        # self.dbc.bodycan.BCM_03
        fully_qualified_module_name = msg_obj.__module__
        bus_name = fully_qualified_module_name.split(".")[-1]  # "bodycan"
        # Get bus_obj from inst_dict
        bus_obj = self.inst_dict.get(bus_name)

        actual_cycle_time = bus_obj.read_msg_cycle_time(msg_obj, timeout=timeout)
        cycle_time = msg_obj.msg_cyc
        if actual_cycle_time is None:
            logger.error("Get cycle_Time error")
        return actual_cycle_time, cycle_time

    def resume_cyclic_msg(self, bus_name, can_id):
        self.inst_dict[bus_name].resume_cyclic_msg(can_id)

    def pause_cyclic_msg(self, bus_name, can_id):
        self.inst_dict[bus_name].pause_cyclic_msg(can_id)

    def check_msg_dlc(self, msg_obj, timeout=1.0):
        # msg_signals_obj : type
        # self.dbc.bodycan.BCM_03
        fully_qualified_module_name = msg_obj.__module__
        bus_name = fully_qualified_module_name.split(".")[-1]  # "bodycan"
        # Get bus_obj from inst_dict
        bus_obj = self.inst_dict.get(bus_name)

        actual_dlc = bus_obj.read_msg_dlc(msg_obj, timeout=timeout)
        dbc_dlc = msg_obj.dlc
        if actual_dlc == dbc_dlc:
            return True
        else:
            logger.error("dbc_dlc is {}, but actual_dlc is {}".format(dbc_dlc, actual_dlc))
            return False
