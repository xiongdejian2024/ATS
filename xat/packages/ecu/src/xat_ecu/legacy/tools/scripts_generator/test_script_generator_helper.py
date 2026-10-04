# -*- coding: utf-8 -*-se
"""
@File        : test_script_generator_helper.py
@Description :
@Examples    :
"""

import os
import sys

import re
import pandas as pd
from xat_ecu.legacy.sdk.can_lin.pcan_const import *
from signal_validator import validate_signal


class TestScriptGeneratorHelper(object):
    def __init__(self):
        self.def_set_fixed_value_template = \
            '''\n\n    def {sdk_name}(self):
        self.set(self.{dbc_or_ldf}.{target_bus}.{target_msg_name}, "{target_sig_name}", "{sig_value}")'''

        self.def_set_flexible_value_template = \
            '''\n\n    def {sdk_name}(self, sig_value=0):
        self.set(self.{dbc_or_ldf}.{target_bus}.{target_msg_name}, "{target_sig_name}", sig_value)'''

        self.def_check_fixed_value_template = \
            '''\n\n    def {sdk_name}(self):
        self.check(self.{dbc_or_ldf}.{target_bus}.{target_msg_name}, "{target_sig_name}", "{sig_value}")'''

        self.def_check_flexible_value_template = \
            '''\n\n    def {sdk_name}(self, sig_value=0):
        self.check(self.{dbc_or_ldf}.{target_bus}.{target_msg_name}, "{target_sig_name}", sig_value)'''

        self.test_header_template = """# -*- coding: utf-8 -*-

import time
from sdk.interface.pcan_const import PcanConst
from project.bgm.fixture.bgm import *
from project.bgm.case_helper.test_base import TestBase

@pytest.mark.full
@pytest.mark.{test_script_mark}
class Test{test_name}(TestBase):
    def before_class(self, bgm):
        super().before_class(self, bgm)

        global pcan
        pcan = self.app.pcan

    def before_each_func(self, bgm):
        super().before_each_func(self)

    def after_class(self, bgm):
        super().after_class(self, bgm)

    def after_each_func(self, bgm):
        super().after_each_func(self)
            """
        self.smoke_mark_string = "\n    @pytest.mark.smoke"
        self.sanity_mark_string = "\n    @pytest.mark.sanity"

        self.single_precondition_template = '''\n        {func}'''
        self.single_logger_template = '''\n        logger.info("{information}")'''
        self.single_debug_template = '''\n        logger.debug("{information}")'''
        self.single_test_case_template = '''\n    def test_{summary}(self):'''
        self.single_standard_action_template = '''\n        pcan.{func_name}()'''
        self.single_flexible_action_template = '''\n        pcan.{func_name}({sig_value})'''
        self.single_wait_action_template = """\n        time.sleep({sleep_time})"""
        self.single_special_action_template = \
            '''\n        """TODO: PLEASE FILLIN SPECIAL ACTION:
        {special_action}"""'''

        self.precondition_func_dict = {
            "DSTMS-8": "assert self.app.set_veh_state(PcanConst.VehState.PARKED_COMFENA_COMFORT_ENABLED)",
            "DSTMS-9": "assert self.app.set_veh_state(PcanConst.VehState.DRIVER_PRESENT)",
            "DSTMS-10": "assert self.app.set_veh_state(PcanConst.VehState.DRIVING)",
            "DSTMS-11": "assert self.app.set_veh_state(PcanConst.VehState.PARKED_COMFENA_COMFORT_NOT_ENABLED)",
            "DSTMS-12": "assert self.app.set_veh_state(PcanConst.VehState.SW_UPDATE)",
            "DSTMS-19": "assert self.app.set_veh_state(PcanConst.VehState.PARKED)",
            "DSTMS-25": "pcan.chassis1_bcu_04_vehmovgdir_forward()",
            "DSTMS-26": "pcan.chassis1_bcu_04_vehmovgdir_backward()",
            "DSTMS-27": "pcan.chassis1_bcu_04_vehmovgdir_standstill()",
            "DSTMS-28": "pcan.bodycan_bcm_03_hoodajarsts_closed()",
            "DSTMS-29": "pcan.bodycan_bcm_03_hoodajarsts_opened()"
        }

    def load_single_action_line(self, single_action_line):
        if re.match("[0-9]+.(\s*)?set\s", single_action_line, re.IGNORECASE):
            return self.load_action_set(single_action_line)
        elif re.match("[0-9]+.(\s*)?check\s", single_action_line, re.IGNORECASE):
            return self.load_action_check(single_action_line)
        elif re.match("[0-9]+.(\s*)?wait\s", single_action_line, re.IGNORECASE):
            return self.load_action_wait(single_action_line)
        elif re.match("([0-9]*)?(.)?(\s*)?#.*", single_action_line, re.IGNORECASE):
            return self.load_action_comment(single_action_line)
        else:
            return "special", "nofound", [single_action_line]

    def load_single_check_line(self, single_check_line):
        match_pcan_check_fix_value = re.search(
            "[0-9a-z_]*[.][0-9a-z_]*[.][{]?[0-9a-z_]*[}]?(\s*)=(\s*)v_[0-9a-z_]*",
            single_check_line, re.IGNORECASE)
        match_pcan_check_flex_value = re.search(
            "[0-9a-z_]*[.][0-9a-z_]*[.][{]?[0-9a-z_]*[}]?(\s*)=(\s*)[0-9a-z_.]*",
            single_check_line, re.IGNORECASE)
        if match_pcan_check_fix_value:
            detail = match_pcan_check_fix_value.group()
            return self.load_pcan_check_fix_value(detail)
        elif match_pcan_check_flex_value:
            detail = match_pcan_check_flex_value.group()
            return self.load_pcan_check_flex_value(detail)
        else:
            return "special", "nofound", [single_check_line]

    def load_action_set(self, single_action_line):
        match_pcan_set_fix_value = re.search(
            "[0-9a-z_]*[.][0-9a-z_]*[.][{]?[0-9a-z_]*[}]?(\s*)=(\s*)v_[0-9a-z_]*",
            single_action_line, re.IGNORECASE)
        match_pcan_set_flex_value = re.search(
            "[0-9a-z_]*[.][0-9a-z_]*[.][{]?[0-9a-z_]*[}]?(\s*)=(\s*)[0-9a-z_.]*",
            single_action_line, re.IGNORECASE)
        match_set_to_target_state = re.search(
            "set(\s)*[0-9a-z_\s]*\sto\s[0-9a-z_\s]*",
            single_action_line, re.IGNORECASE)
        if match_pcan_set_fix_value:
            detail = match_pcan_set_fix_value.group()
            return self.load_pcan_set_fix_value(detail)
        elif match_pcan_set_flex_value:
            detail = match_pcan_set_flex_value.group()
            return self.load_pcan_set_flex_value(detail)
        elif match_set_to_target_state:
            detail = match_set_to_target_state.group()
            return self.load_set_to_target_state(detail)
        else:
            return "special", "nofound", [single_action_line]

    def load_pcan_set_fix_value(self, detail):
        bus_name = detail.split('=')[0].split('.')[0].lower()
        message_name = detail.split('=')[0].split('.')[1]
        if "{" in detail and "}" in detail:
            signal_name = detail.split('=')[0].split(".")[2].strip()[1:-1]
        else:
            signal_name = detail.split('=')[0].split(".")[2].strip()
        signal_value = detail.split('=')[1].strip()
        is_signal_valid, return_msg = validate_signal(bus_name=bus_name, msg_name=message_name,
                                                      signal_name=signal_name, signal_value=signal_value)
        if is_signal_valid:
            if bus_name in PcanConst.BGM_CAN_BUS_LIST:
                bus_type = "dbc"
            elif bus_name in PcanConst.BGM_LIN_BUS_LIST:
                bus_type = "ldf"
            return "pcan", "set_fix", [bus_type, bus_name, message_name, signal_name, signal_value]
        else:
            return "special", "nofound", [detail + "\n        " + str(return_msg)]

    def load_pcan_set_flex_value(self, detail):
        bus_name = detail.split('=')[0].split('.')[0].lower()
        message_name = detail.split('=')[0].split('.')[1]
        if "{" in detail and "}" in detail:
            signal_name = detail.split('=')[0].split(".")[2].strip()[1:-1]
        else:
            signal_name = detail.split('=')[0].split(".")[2].strip()
        signal_value = detail.split('=')[1].strip()
        is_signal_valid, return_msg = validate_signal(bus_name=bus_name, msg_name=message_name,
                                                      signal_name=signal_name, signal_value=signal_value)
        if is_signal_valid:
            if bus_name in PcanConst.BGM_CAN_BUS_LIST:
                bus_type = "dbc"
            elif bus_name in PcanConst.BGM_LIN_BUS_LIST:
                bus_type = "ldf"
            return "pcan", "set_flex", [bus_type, bus_name, message_name, signal_name, signal_value]
        else:
            return "special", "nofound", [detail + "\n        " + str(return_msg)]

    def load_set_to_target_state(self, detail):
        target = detail.split(" to ")[0].split()[-1]
        target_state = detail.split(" to ")[1]
        return "special", "set", [target, target_state]

    def load_action_check(self, single_action_line):
        return "special", "check", []

    def load_action_wait(self, single_action_line):
        sleep_time = 0.0
        try:
            sleep_time_min = single_action_line.split(" min")[0].split(" ")[-1]
            if sleep_time_min.startswith("("):
                sleep_time_min = sleep_time_min[1:]
            sleep_time += float(sleep_time_min) * 60
        except:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/tools/scripts_generator/test_script_generator_helper.py")
            pass
        try:
            sleep_time_sec = single_action_line.split(" sec")[0].split(" ")[-1]
            if sleep_time_sec.startswith("("):
                sleep_time_sec = sleep_time_sec[1:]
            sleep_time += float(sleep_time_sec)
        except:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/tools/scripts_generator/test_script_generator_helper.py")
            pass
        return "special", "wait", [sleep_time]

    def load_action_comment(self, single_action_line):
        return "special", "comment", [single_action_line.split("#")[1]]

    def load_pcan_check_fix_value(self, detail):
        bus_name = detail.split("=")[0].split(".")[0].lower()
        message_name = detail.split("=")[0].split(".")[1]
        if "{" in detail and "}" in detail:
            signal_name = detail.split('=')[0].split(".")[2].strip()[1:-1]
        else:
            signal_name = detail.split('=')[0].split(".")[2].strip()
        signal_value = detail.split('=')[1].strip()
        is_signal_valid, return_msg = validate_signal(bus_name=bus_name, msg_name=message_name,
                                                      signal_name=signal_name, signal_value=signal_value)
        if is_signal_valid:
            if bus_name in PcanConst.BGM_CAN_BUS_LIST:
                bus_type = "dbc"
            elif bus_name in PcanConst.BGM_LIN_BUS_LIST:
                bus_type = "ldf"
            return "pcan", "check_fix", [bus_type, bus_name, message_name, signal_name, signal_value]
        else:
            return "special", "nofound", [detail + "\n        " + str(return_msg)]

    def load_pcan_check_flex_value(self, detail):
        bus_name = detail.split('=')[0].split('.')[0].lower()
        message_name = detail.split('=')[0].split('.')[1]
        if "{" in detail and "}" in detail:
            signal_name = detail.split('=')[0].split(".")[2].strip()[1:-1]
        else:
            signal_name = detail.split('=')[0].split(".")[2].strip()
        signal_value = detail.split('=')[1].strip()
        is_signal_valid, return_msg = validate_signal(bus_name=bus_name, msg_name=message_name,
                                                      signal_name=signal_name, signal_value=signal_value)
        if is_signal_valid:
            if bus_name in PcanConst.BGM_CAN_BUS_LIST:
                bus_type = "dbc"
            elif bus_name in PcanConst.BGM_LIN_BUS_LIST:
                bus_type = "ldf"
            return "pcan", "check_flex", [bus_type, bus_name, message_name, signal_name, signal_value]
        else:
            return "special", "nofound", [detail + "\n        " + str(return_msg)]

    def sdk_pcan_set_fix_content(self, element):
        template = self.def_set_fixed_value_template
        data = element[2]
        bus_type, bus_name, msg_name, sig_name, sig_value = data[0], data[1], data[2], data[3], data[4]
        sdk_name = ("%s_%s_%s_%s" % (bus_name, msg_name, sig_name, sig_value[2:])).lower()
        sdk_func_content = template.format(sdk_name=sdk_name, dbc_or_ldf=bus_type, target_bus=bus_name,
                                           target_msg_name=msg_name, target_sig_name=sig_name, sig_value=sig_value)
        return {"sdk_name": sdk_name, "sdk_func_content": sdk_func_content}

    def sdk_pcan_set_flex_content(self, element):
        template = self.def_set_flexible_value_template
        data = element[2]
        bus_type, bus_name, msg_name, sig_name = data[0], data[1], data[2], data[3]
        sdk_name = ("%s_%s_%s" % (bus_name, msg_name, sig_name)).lower()
        sdk_func_content = template.format(sdk_name=sdk_name, dbc_or_ldf=bus_type, target_bus=bus_name,
                                           target_msg_name=msg_name, target_sig_name=sig_name)
        return {"sdk_name": sdk_name, "sdk_func_content": sdk_func_content}

    def sdk_pcan_check_fix_content(self, element):
        template = self.def_check_fixed_value_template
        data = element[2]
        bus_type, bus_name, msg_name, sig_name, sig_value = data[0], data[1], data[2], data[3], data[4]
        sdk_name = ("assert_%s_%s_%s_is_%s" % (bus_name, msg_name, sig_name, sig_value[2:])).lower()
        sdk_func_content = template.format(sdk_name=sdk_name, dbc_or_ldf=bus_type, target_bus=bus_name,
                                           target_msg_name=msg_name, target_sig_name=sig_name, sig_value=sig_value)
        return {"sdk_name": sdk_name, "sdk_func_content": sdk_func_content}

    def sdk_pcan_check_flex_content(self, element):
        template = self.def_check_flexible_value_template
        data = element[2]
        bus_type, bus_name, msg_name, sig_name = data[0], data[1], data[2], data[3]
        sdk_name = ("assert_%s_%s_%s" % (bus_name, msg_name, sig_name)).lower()
        sdk_func_content = template.format(sdk_name=sdk_name, dbc_or_ldf=bus_type, target_bus=bus_name,
                                           target_msg_name=msg_name, target_sig_name=sig_name)
        return {"sdk_name": sdk_name, "sdk_func_content": sdk_func_content}

    def write_test_header(self, test_label, component):
        template = self.test_header_template
        test_script_mark = test_label.lower().replace("-", "_").replace(" ", "")
        test_name = test_label.replace(component.replace(" ", "-"), "")[1:].capitalize().replace("-", "")
        output = template.format(test_script_mark=test_name.lower(), test_name=test_name)
        return output

    def write_proprity(self, priority):
        output = ""
        if priority == "P1 - Critical":
            output += self.smoke_mark_string
            output += self.sanity_mark_string
        elif priority == "P2 - High":
            output += self.sanity_mark_string
        return output

    def write_func_name(self, summary, test_id):
        template = self.single_test_case_template
        if ("{" in summary) and ("}" in summary):
            summary = summary[summary.find("{") + 1:summary.find("}")].replace(" ", "_") + "_" + \
                      test_id.split("_")[-1]
        else:
            summary = summary.replace(" ", "_") + "_" + test_id.split("_")[-1]
        output = template.format(summary=summary)
        return output

    def write_precondition(self, preconditon_id_list):
        output = ""
        for preconditon in preconditon_id_list:
            if not pd.isnull(preconditon):
                template = self.single_precondition_template
                preconditon_script = template.format(func=self.precondition_func_dict[preconditon])
                output += preconditon_script
        return output

    def write_pcan_set_fix(self, sdk_write_item):
        data = sdk_write_item[2]
        bus_name, message_name, signal_name, signal_value = data[1], data[2], data[3], data[4][2:]
        func_name = ("%s_%s_%s_%s" % (bus_name, message_name, signal_name,
                                      signal_value)).lower()
        template = self.single_standard_action_template
        output = template.format(func_name=func_name)
        return output

    def write_pcan_set_flex(self, sdk_write_item):
        data = sdk_write_item[2]
        bus_name, message_name, signal_name, signal_value = data[1], data[2], data[3], data[4]
        func_name = ("%s_%s_%s" % (bus_name, message_name, signal_name)).lower()
        template = self.single_flexible_action_template
        output = template.format(func_name=func_name, sig_value=signal_value)
        return output

    def write_pcan_check_fix(self, sdk_write_item):
        data = sdk_write_item[2]
        bus_name, message_name, signal_name, signal_value = data[1], data[2], data[3], data[4][2:]
        func_name = ("assert_%s_%s_%s_is_%s" % (
            bus_name, message_name, signal_name, signal_value)).lower()
        template = self.single_standard_action_template
        output = template.format(func_name=func_name)
        return output

    def write_pcan_check_flex(self, sdk_write_item):
        data = sdk_write_item[2]
        bus_name, message_name, signal_name, signal_value = data[1], data[2], data[3], data[4]
        func_name = ("assert_%s_%s_%s" % (
            bus_name, message_name, signal_name)).lower()
        template = self.single_flexible_action_template
        output = template.format(func_name=func_name, sig_value=signal_value)
        return output

    def write_wait(self, sdk_write_item):
        output = ""
        template = self.single_debug_template
        wait_debug_script = template.format(information="Wait %s seconds" % sdk_write_item[2][0])
        output += wait_debug_script
        template = self.single_wait_action_template
        output += template.format(sleep_time=sdk_write_item[2][0])
        return output

    def write_set_vehstate(self, sdk_write_item):
        set_target_state = sdk_write_item[2][1].lower()
        veh_func = ""
        if (set_target_state == "parked") or (set_target_state == "park"):
            veh_func = self.precondition_func_dict["DSTMS-19"]
        elif set_target_state == "parked comfort enable" or set_target_state == "park comfort enable":
            veh_func = self.precondition_func_dict["DSTMS-8"]
        elif set_target_state == "parked comfort disable" or set_target_state == "park comfort disable":
            veh_func = self.precondition_func_dict["DSTMS-11"]
        elif set_target_state == "driving":
            veh_func = self.precondition_func_dict["DSTMS-10"]
        elif set_target_state == "driver present":
            veh_func = self.precondition_func_dict["DSTMS-9"]
        elif set_target_state == "software update":
            veh_func = self.precondition_func_dict["DSTMS-12"]
        template = self.single_precondition_template
        output = template.format(func=veh_func)
        return output

    def write_comment(self, sdk_write_item):
        template = self.single_logger_template
        output = template.format(information=sdk_write_item[2][0])
        return output

    def write_special_line(self, sdk_write_item):
        template = self.single_special_action_template
        output = template.format(special_action=sdk_write_item[2][0])
        return output
