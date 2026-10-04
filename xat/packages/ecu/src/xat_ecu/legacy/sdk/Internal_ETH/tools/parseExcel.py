# -*- coding: utf-8 -*-

"""
@File        : parseExcel.py
@Author      : songjian.lin@jiduatuo.com
@Time        : 2024/02/04 10:51 AM
@Description : 解析BGM内部以太网通讯Excel表格
@Examples    : example of how to use it
"""
import os
import xlrd2


class EthernetPDU:
    def __init__(self):
        self.ethernet_pdu_name = ""
        self.server_socket = ""
        self.client_socket = ""
        self.send_type = ""
        self.pdu_header_id = 0
        self.pdu_length_bytes = 0
        self.signal_group = {}
        self.base_type = ""
        self.sender = ""
        self.receiver = ""
        self.signals = {}


class EthernetPDUSignal:
    def __init__(self):
        self.signal_name = ""
        self.signal_length = 0
        self.start_position = 0
        self.layout_format = ""
        self.initial_value = 0
        self.factor = 0
        self.offset = 0
        self.value_definition = {}
        self.signal_description = ""
        self.mcu_routing = ""
        self.comments = ""


def parse_excel(excel_name, sheet_name, vehicle_type, version):
    current_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir = current_path.split("tools")[0]
    excel_path = os.path.join(parent_dir, excel_name)
    wb1 = xlrd2.open_workbook(excel_path, encoding_override="utf-8")
    sheet1 = wb1.sheet_by_name(sheet_name)
    num_rows = sheet1.nrows
    ethernet_pdu_dict = {}  #
    for j1 in range(1, num_rows):
        if sheet1.cell_value(j1, 0) not in ethernet_pdu_dict:
            ethernet_pdu = EthernetPDU()
            ethernet_pdu_dict[sheet1.cell_value(j1, 0)] = ethernet_pdu
        else:
            ethernet_pdu = ethernet_pdu_dict.get(sheet1.cell_value(j1, 0))
        ethernet_pdu_signal = EthernetPDUSignal()
        ethernet_pdu.ethernet_pdu_name = sheet1.cell_value(j1, 0)
        ethernet_pdu.server_socket = sheet1.cell_value(j1, 1)
        ethernet_pdu.client_socket = sheet1.cell_value(j1, 2)
        ethernet_pdu.send_type = sheet1.cell_value(j1, 3)
        ethernet_pdu.pdu_header_id = int(sheet1.cell_value(j1, 4))
        ethernet_pdu.pdu_length_bytes = int(sheet1.cell_value(j1, 5))
        if len(sheet1.cell_value(j1, 6)) > 0:
            if sheet1.cell_value(j1, 6) not in ethernet_pdu.signal_group:
                ethernet_pdu.signal_group[sheet1.cell_value(j1, 6)] = []
            ethernet_pdu.signal_group[sheet1.cell_value(j1, 6)].append(sheet1.cell_value(j1, 7))
        ethernet_pdu_signal.signal_name = sheet1.cell_value(j1, 7)
        ethernet_pdu_signal.signal_length = int(sheet1.cell_value(j1, 8))
        ethernet_pdu_signal.start_position = int(sheet1.cell_value(j1, 9))
        ethernet_pdu_signal.layout_format = sheet1.cell_value(j1, 10)
        ethernet_pdu.base_type = sheet1.cell_value(j1, 11)
        ethernet_pdu_signal.initial_value = int(sheet1.cell_value(j1, 12))
        ethernet_pdu_signal.factor = sheet1.cell_value(j1, 13)
        ethernet_pdu_signal.offset = int(sheet1.cell_value(j1, 14))

        for key_value in sheet1.cell_value(j1, 15).strip().split("\n"):
            if ":" in key_value:
                key = key_value.split(":")[0]
                value = key_value.split(":")[1]
                ethernet_pdu_signal.value_definition[key] = value
        ethernet_pdu_signal.signal_description = sheet1.cell_value(j1, 16).replace("\n", " ")
        ethernet_pdu.sender = sheet1.cell_value(j1, 17)
        ethernet_pdu.receiver = sheet1.cell_value(j1, 18)
        ethernet_pdu_signal.mcu_routing = sheet1.cell_value(j1, 19)
        ethernet_pdu_signal.comments = sheet1.cell_value(j1, 20).replace("\n", " ")
        ethernet_pdu.signals[ethernet_pdu_signal.signal_name] = ethernet_pdu_signal
    else:
        parent_dir = parent_dir.split("Internal_ETH")[0]
        output_path = os.path.join(parent_dir, "data", vehicle_type, "Internal_ETH", version, "bgm_eth_internal.py")
        for ethernet_pdu_name in ethernet_pdu_dict:
            print_ethernet_pdu(ethernet_pdu_dict.get(ethernet_pdu_name), output_path)
    print(num_rows)


def print_ethernet_pdu(ethernet_pdu: EthernetPDU, output_path):
    print("=========================================")
    with open(output_path, 'a+', encoding="utf-8") as f:
        f.write("\n\n")
        f.write(f"class {getattr(ethernet_pdu, 'ethernet_pdu_name')}:" + "\n")
        for aa in dir(ethernet_pdu):
            if "__" not in aa:
                if aa == "signals":
                    print("    ------------------------------------------")
                    for bb in getattr(ethernet_pdu, "signals"):  # 遍历当前的信号列表字典
                        ethernet_pdu_signal = getattr(ethernet_pdu, aa)[bb]
                        f.write("\n")
                        f.write(f"    class {getattr(ethernet_pdu_signal, 'signal_name')}:" + "\n")
                        for cc in dir(ethernet_pdu_signal):
                            if "__" not in cc:
                                if cc != "signal_name":
                                    value = convert_value(getattr(ethernet_pdu_signal, cc))
                                    print(f"    {cc} == > {value}")
                                    f.write(f"        {cc} = {value}" + "\n")
                        else:
                            print("    ------------------------------------------")
                if aa not in ["ethernet_pdu_name", "signals"]:
                    value = convert_value(getattr(ethernet_pdu, aa))
                    f.write(f"    {aa} = {value}" + "\n")


def convert_value(value):
    if isinstance(value, str):
        return f'"{value}"'
    else:
        return value


if __name__ == '__main__':
    parse_excel("MARS1 V2.0.2 BGM Internal ETH Communicaiton_Release_20240426.xlsx", "BGM ETH Internal Communication",
                "mars1", "v_2_0_0")
