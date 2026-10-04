"""
@File        : generate_init_pdu_and_tx_cyc_json.py
@Author      : quan.sun@jiduauto.com
@Time        : 2022/04/04 19:12
@Description :
@Examples    :
"""
import json
import os
import sys
import argparse

current_path = os.path.dirname(os.path.realpath(__file__))
import importlib
from xat_ecu.legacy.sdk.i_signal_i_pdu import ISignalIPdu
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.common.file_handle import FileHandle

parent_dir = os.path.join(os.getcwd().split("ecu_simulator")[0], "ecu_simulator")


class GenerateInitPduAndTxCycJson:
    def __init__(self, cls_path):
        self.cls_init_path = cls_path
        self.cls_path = os.path.join(parent_dir, cls_path)
        self.buspdudict = {}
        self.isignalipdu = ISignalIPdu(cls_path)
        self.isignalipdu.bus_pdu_dict = self.buspdudict

        self.pdu_path = self.cls_path.replace(
            "can_lin_fr_cls", "can_lin_fr_init_pdu_json"
        )
        if not os.path.exists(self.pdu_path):
            os.makedirs(self.pdu_path)

        self.signal_auto = []

    def get_data_dict_and_write(self):
        cls_file_names = FileHandle.get_file_names_from_dir(self.cls_path)
        for cls_name in cls_file_names:
            if (
                cls_name != "__init__"
                and "-38" not in cls_name
                and "cpython" not in cls_name
            ):
                cls_path = os.path.join(self.cls_init_path, cls_name)
                cls_full_module_name = cls_path.replace("/", ".")
                cls_module = importlib.import_module(cls_full_module_name)
                logger.info("cls_module is {}".format(cls_module))

                module_names = dir(cls_module)
                message_names = []
                for module_name in module_names:
                    # if "__" not in module_name and "NmFr" not in module_name and "Diag" not in module_name:
                    if "__" not in module_name and "lin_scheduleTable" != module_name:
                        message_names.append(module_name)

                pdu_dict = {}
                for message_name in message_names:
                    mes_obj = getattr(cls_module, message_name)
                    message_info_dict = self.get_message_info_from_cls(mes_obj)
                    pdu_dict[message_name] = message_info_dict
                    self.buspdudict[cls_name] = pdu_dict
                    # if mes_obj.msg_tx_method == "cyclic":
                    #     self.update_init_pdu(mes_obj)
                    self.update_init_pdu(mes_obj, message_name, cls_name)
                if pdu_dict:
                    json_path = self.pdu_path + "/" + cls_name + ".json"
                    self.write_data_dict_into_json(json_path, pdu_dict)

    def get_message_info_from_cls(self, mes_obj, ecu="BGM"):
        message_info_dict = {}
        message_info_dict["msg_cycle"] = mes_obj.msg_cycle
        message_info_dict["msg_length"] = mes_obj.msg_length
        message_info_dict["msg_id"] = mes_obj.msg_id

        # TO DO
        # tx_node = mes_obj.tx_node
        # rx_nodes = mes_obj.rx_nodes
        # if ecu == tx_node:
        #     rx_flag = None
        #     if mes_obj.msg_cycle:
        #         tx_flag = True
        #     else:
        #         tx_flag = False
        # else:
        #     rx_flag = False
        #     tx_flag = None

        # Temporary treatment; Cycle messages are sent
        rx_flag = None
        if mes_obj.msg_cycle:
            tx_flag = True
        else:
            tx_flag = None

        message_info_dict["tx_flag"] = tx_flag
        message_info_dict["rx_flag"] = rx_flag

        message_info_dict["tx_node"] = mes_obj.tx_node
        message_info_dict["rx_nodes"] = mes_obj.rx_nodes

        if hasattr(mes_obj, "msg_slotid"):
            message_info_dict["msg_slotid"] = mes_obj.msg_slotid
        if hasattr(mes_obj, "msg_slotid"):
            message_info_dict["msg_base_cycle"] = mes_obj.msg_base_cycle
        if hasattr(mes_obj, "msg_repetition"):
            message_info_dict["msg_repetition"] = mes_obj.msg_repetition

        message_info_dict["pdu_data"] = [0x00] * mes_obj.msg_length

        return message_info_dict

    def update_init_pdu(self, mes_obj, message_name, cls_name):
        for signal_name in dir(mes_obj):
            if "__" not in signal_name:
                signal_obj = getattr(mes_obj, signal_name)
                if hasattr(signal_obj, "sig_value_init"):
                    sig_value_init = signal_obj.sig_value_init
                    if sig_value_init is not None:
                        self.isignalipdu.set(mes_obj, signal_name, sig_value_init)

                        if signal_obj.sig_value_type == "TEXTTABLE":
                            try:
                                for sig_val in signal_obj.sig_value_table.keys():
                                    self.signal_auto.append(
                                        (cls_name, message_name, signal_name, sig_val)
                                    )
                            except Exception as e:
                                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/tools/communication/generate_init_pdu_and_tx_cyc_json.py")
                                logger.warning(
                                    f"sig_value_type is TEXTTABLE, 但却 sig_value_table 为 {signal_obj.sig_value_table}；  message_name={message_name} signal_name={signal_name}"
                                )
                                sig_val = "Value"
                                self.signal_auto.append(
                                    (cls_name, message_name, signal_name, sig_val)
                                )
                        else:
                            sig_val = "Value"
                            self.signal_auto.append(
                                (cls_name, message_name, signal_name, sig_val)
                            )
                    else:
                        sig_value_init = 0
                        logger.error(
                            "sig_value_init of {} is None; mes_obj is {}".format(
                                signal_name, mes_obj
                            )
                        )

    def write_data_dict_into_json(self, file_path, data_dict):
        with open(file_path, "w") as f:
            json.dump(data_dict, f, indent=4)

    def automatic_signal_generation(self, path="sdk/auto"):
        ecu_sig_auto_dir = os.path.join(parent_dir, path)
        FileHandle.makedirs(ecu_sig_auto_dir)

        ecu_sig_auto_init_path = ecu_sig_auto_dir + "/__init__.py"
        with open(ecu_sig_auto_init_path, "w") as f_init:
            logger.info("Creat __init__.py OK")

        ecu_sig_auto_path = ecu_sig_auto_dir + "/ecu_sig_auto.py"
        with open(ecu_sig_auto_path, "w") as f:
            f.write("# -*- coding: utf-8 -*-\n")
            f.write(
                "# Automatic generation By tools/communication/generate_init_pdu_and_tx_cyc_json.py\n"
            )
            f.write("# Automatically generated code, please do not modify\n")
            f.write("\n")
            f.write("from abc import ABC, abstractmethod\n")
            f.write("\n")
            f.write("\n")
            f.write("class EcuSigAuto(ABC):\n")
            f.write("    def __init__(self):\n")
            f.write("        pass\n")

            f.write("\n")
            f.write("    @abstractmethod\n")
            f.write("    def set(self, *args):\n")
            f.write("        pass\n")

            for signal_combination in self.signal_auto:
                cls_name = signal_combination[0]
                message_name = signal_combination[1]
                mes_obj_str = "self.{}.{}".format(cls_name, message_name)
                def_name = (
                    cls_name
                    + "_"
                    + message_name
                    + "_"
                    + signal_combination[2]
                    + "_"
                    + signal_combination[3]
                ).lower()

                f.write("\n")
                if signal_combination[3] == "Value":
                    f.write("    " + "def " + def_name + "(self, value):\n")
                    f.write(
                        "        "
                        + "self.set({}, '{}', value)\n".format(
                            mes_obj_str, signal_combination[2]
                        )
                    )
                else:
                    sig_value = signal_combination[3]
                    f.write("    " + "def " + def_name + "(self):\n")
                    f.write(
                        "        "
                        + "self.set({}, '{}', '{}')\n".format(
                            mes_obj_str, signal_combination[2], sig_value
                        )
                    )

        # last_ecu_sig_auto_path = os.path.join(parent_dir, "sdk/auto/ecu_sig_auto.py")
        # cp_cmd = "cp {} {}".format(ecu_sig_auto_path, last_ecu_sig_auto_path)  # 最新备份
        # os.system(cp_cmd)


if __name__ == "__main__":
    # Work Path: ecu_simulator/
    # cmd : python3 tools/communication/generate_init_pdu_and_tx_cyc_json.py --cls_path="sdk/data/mars1/can_lin_fr_cls/v_0_6_5"

    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "--cls_path",
        help="can lin fr cls_path",
        default="sdk/data/mars1/can_lin_fr_cls/v_1_0_0",
    )
    # Default is All
    args = argparser.parse_args()

    path_list = args.cls_path.split("/")
    if path_list[0] == "sdk" and path_list[1] == "data":
        path = os.path.join("sdk/auto", path_list[2], path_list[4])
    else:
        print("==============   path parameter is error !!!!!!!!!!!!!!!!!!!!!")

    generater = GenerateInitPduAndTxCycJson(args.cls_path)
    generater.get_data_dict_and_write()

    # generater.automatic_signal_generation(path)
