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
        self.send_type = ""   # "Cyclic-200ms"
        self.pdu_header_id = 0
        self.pdu_length_bytes = 0
        self.signal_group = {}
        self.base_type = ""
        self.sender = ""
        self.receiver = []
        self.signals = {}


class EthernetPDUSignal:
    def __init__(self):
        self.signal_name = ""
        self.signal_length = 0
        self.start_position = 0
        self.sig_ub = None
        self.layout_format = ""
        self.initial_value = 0
        self.factor = 0
        self.offset = 0
        self.value_definition = {}
        self.signal_description = ""
        self.mcu_routing = ""
        self.comments = ""


class Participant:
    def __init__(self):
        self.participant_name = ""
        self.mac_address = ""
        self.ip_address = ""
        self.vlan_id = 5
        self.socket = {}


class socketObj:
    def __init__(self):
        self.socket_name = ""
        self.transport_protocol = ""
        self.port_number = 0


def parse_excel(excel_name, sheet_name, vehicle_type, version):
    current_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir = current_path.split("tools")[0]
    excel_path = os.path.join(parent_dir, excel_name)
    wb1 = xlrd2.open_workbook(excel_path, encoding_override="utf-8")
    sheet1 = wb1.sheet_by_name(sheet_name)
    num_rows = sheet1.nrows
    ethernet_pdu_dict = {}
    for j1 in range(1, num_rows):
        if sheet1.cell_value(j1, 2) not in ethernet_pdu_dict:
            ethernet_pdu = EthernetPDU()
            ethernet_pdu_dict[sheet1.cell_value(j1, 2)] = ethernet_pdu
        else:
            ethernet_pdu = ethernet_pdu_dict.get(sheet1.cell_value(j1, 2))
        ethernet_pdu_signal = EthernetPDUSignal()
        ethernet_pdu.ethernet_pdu_name = sheet1.cell_value(j1, 2)
        ethernet_pdu.server_socket = sheet1.cell_value(j1, 3)
        ethernet_pdu.client_socket = sheet1.cell_value(j1, 4)
        ethernet_pdu.send_type = sheet1.cell_value(j1, 5)
        ethernet_pdu.pdu_header_id = sheet1.cell_value(j1, 6)
        ethernet_pdu.pdu_length_bytes = int(sheet1.cell_value(j1, 7))
        if len(sheet1.cell_value(j1, 8)) > 0:
            if sheet1.cell_value(j1, 8) not in ethernet_pdu.signal_group:
                ethernet_pdu.signal_group[sheet1.cell_value(j1, 8)] = []
            ethernet_pdu.signal_group[sheet1.cell_value(j1, 8)].append(sheet1.cell_value(j1, 9))
        ethernet_pdu_signal.signal_name = sheet1.cell_value(j1, 9)
        ethernet_pdu_signal.signal_length = int(sheet1.cell_value(j1, 10))
        ethernet_pdu_signal.start_position = int(sheet1.cell_value(j1, 11))
        ethernet_pdu_signal.sig_ub = int(sheet1.cell_value(j1, 13)) if isinstance(sheet1.cell_value(j1, 13), float) else None
        if isinstance(sheet1.cell_value(j1, 12), float):
            ethernet_pdu_signal.sig_ub = int(sheet1.cell_value(j1, 12))
        ethernet_pdu_signal.layout_format = sheet1.cell_value(j1, 14).replace("Motolora", "Motorola")
        ethernet_pdu.base_type = sheet1.cell_value(j1, 15)
        ethernet_pdu_signal.initial_value = int(sheet1.cell_value(j1, 16)) if sheet1.cell_value(j1, 16) else 0
        ethernet_pdu_signal.factor = sheet1.cell_value(j1, 17)
        ethernet_pdu_signal.offset = int(sheet1.cell_value(j1, 18))

        for key_value in sheet1.cell_value(j1, 19).strip().split("\n"):
            if ":" in key_value:
                key = key_value.split(":")[0]
                value = key_value.split(":")[1]
                ethernet_pdu_signal.value_definition[key] = value
        ethernet_pdu_signal.signal_description = sheet1.cell_value(j1, 20).replace("\n", " ")
        ethernet_pdu.sender = sheet1.cell_value(j1, 0)
        if sheet1.cell_value(j1, 1) not in ethernet_pdu.receiver:
            ethernet_pdu.receiver.append(sheet1.cell_value(j1, 1))
        ethernet_pdu_signal.mcu_routing = "N"
        ethernet_pdu.signals[ethernet_pdu_signal.signal_name] = ethernet_pdu_signal
    else:
        parent_dir = parent_dir.split("Internal_ETH")[0]
        output_path_tcp = os.path.join(parent_dir, "data", vehicle_type, "eth", version)
        output_path_udp = os.path.join(parent_dir, "data", vehicle_type, "eth", version)

        if not os.path.exists(output_path_tcp):
            create_dir_recursive(output_path_tcp)
        if not os.path.exists(output_path_udp):
            create_dir_recursive(output_path_udp)

        py_name_list = []  # py文件的列表
        for ethernet_pdu_name in ethernet_pdu_dict:
            ethernet_pdu = ethernet_pdu_dict.get(ethernet_pdu_name)
            if "UDP" in ethernet_pdu.server_socket or "UDP" in ethernet_pdu.client_socket:
                server_socket = ethernet_pdu.server_socket.replace("Socket", "")
                client_socket = ethernet_pdu.client_socket.replace("Socket", "")

                py_name = f"{server_socket}_{client_socket}.py" # 默认值
                if "Multicast" == server_socket:  # 特殊处理1，
                    py_name = f"{client_socket}_{server_socket}.py"

                if f"{client_socket}_{server_socket}.py" in py_name_list:  # 特殊处理2，如果反向在内，用存量的反向
                    py_name = f"{client_socket}_{server_socket}.py"
                else:
                    py_name_list.append(py_name)

                output_path = os.path.join(output_path_udp, py_name)
            else:
                server_socket = ethernet_pdu.server_socket.replace("Socket", "")
                client_socket = ethernet_pdu.client_socket.replace("Socket", "")
                if "Server" in server_socket:
                    py_name = f"{server_socket}_{client_socket}.py"
                elif "Server" in client_socket:
                    py_name = f"{client_socket}_{server_socket}.py"
                else:
                    if server_socket > client_socket:
                        py_name = f"{server_socket}_{client_socket}.py"
                    else:
                        py_name = f"{client_socket}_{server_socket}.py"
                output_path = os.path.join(output_path_tcp, py_name)
            print_ethernet_pdu(ethernet_pdu_dict.get(ethernet_pdu_name), output_path)


def parse_excel_channel_config(excel_name, sheet_name, vehicle_type, version):
    current_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir = current_path.split("tools")[0]
    excel_path = os.path.join(parent_dir, excel_name)
    wb1 = xlrd2.open_workbook(excel_path, encoding_override="utf-8")
    sheet1 = wb1.sheet_by_name(sheet_name)
    num_rows = sheet1.nrows
    ethernet_participant_dict = {}
    for j1 in range(1, num_rows):
        participant_name_list = sheet1.cell_value(j1, 0).split(',')
        for participant_name in participant_name_list:
            if participant_name not in ethernet_participant_dict:
                ethernet_participant = Participant()
            else:
                ethernet_participant = ethernet_participant_dict.get(participant_name)
            # 更新participant信息
            ethernet_participant_dict[participant_name] = ethernet_participant
            ethernet_participant.participant_name = participant_name
            ethernet_participant.mac_address = sheet1.cell_value(j1, 2)
            ethernet_participant.ip_address = sheet1.cell_value(j1, 3)
            ethernet_participant.vlan_id = int(sheet1.cell_value(j1, 6))
            # 创建socket对象
            ethernet_participant_socket = socketObj()
            ethernet_participant_socket.socket_name = sheet1.cell_value(j1, 1)
            ethernet_participant_socket.transport_protocol = sheet1.cell_value(j1, 4)
            ethernet_participant_socket.port_number = int(sheet1.cell_value(j1, 5))
            # 创建的socket对象关联participant对象
            ethernet_participant.socket[ethernet_participant_socket.socket_name] = ethernet_participant_socket
    else:
        parent_dir = parent_dir.split("Internal_ETH")[0]
        output_path = os.path.join(parent_dir, "data", vehicle_type, "eth", version)

        if not os.path.exists(output_path):
            create_dir_recursive(output_path)

        for ethernet_participant_name in ethernet_participant_dict:
            ethernet_participant = ethernet_participant_dict.get(ethernet_participant_name)
            py_name = f"participant_config.py"
            print_ethernet_participant(ethernet_participant, os.path.join(output_path, py_name))


def create_dir_recursive(path):
    try:
        os.makedirs(path)
        f = open(os.path.join(path, '__init__.py'), 'w')
        f.close()
    except OSError as e:
        print(e)


def print_ethernet_pdu(ethernet_pdu: EthernetPDU, output_path):

    if not os.path.exists(output_path):  # 如果文件不存在，则创建
        f = open(output_path, 'w')
        f.close()

    with open(output_path, 'a+', encoding="utf-8") as f:
        f.write("\n\n")
        f.write(f"class {getattr(ethernet_pdu, 'ethernet_pdu_name')}:" + "\n")
        for aa in dir(ethernet_pdu):
            if "__" not in aa:
                if aa == "signals":
                    for bb in getattr(ethernet_pdu, "signals"):  # 遍历当前的信号列表字典
                        ethernet_pdu_signal = getattr(ethernet_pdu, aa)[bb]
                        f.write("\n")
                        f.write(f"    class {getattr(ethernet_pdu_signal, 'signal_name')}:" + "\n")
                        for cc in dir(ethernet_pdu_signal):
                            if "__" not in cc:
                                if cc != "signal_name":
                                    value = convert_value(getattr(ethernet_pdu_signal, cc))
                                    f.write(f"        {cc} = {value}" + "\n")
                if aa not in ["ethernet_pdu_name", "signals"]:
                    value = convert_value(getattr(ethernet_pdu, aa))
                    if aa == "pdu_header_id":
                        f.write(f"    {aa} = {value}".replace('"', '') + "\n")
                    else:
                        f.write(f"    {aa} = {value}" + "\n")


def print_ethernet_participant(ethernet_participant: Participant, output_path):

    if not os.path.exists(output_path):  # 如果文件不存在，则创建
        f = open(output_path, 'w')
        f.close()

    with open(output_path, 'a+', encoding="utf-8") as f:
        f.write("\n\n")
        f.write(f"class {getattr(ethernet_participant, 'participant_name')}:" + "\n")
        for aa in dir(ethernet_participant):
            if "__" not in aa:
                if aa not in ["participant_name", "socket"]:
                    value = convert_value(getattr(ethernet_participant, aa))
                    if aa == "pdu_header_id":
                        f.write(f"    {aa} = {value}".replace('"', '') + "\n")
                    else:
                        f.write(f"    {aa} = {value}" + "\n")

        for aa in dir(ethernet_participant):
            if aa == "socket":
                for bb in getattr(ethernet_participant, "socket"):  # 遍历当前的信号列表字典
                    ethernet_pdu_signal = getattr(ethernet_participant, aa)[bb]
                    f.write("\n")
                    f.write(f"    class {getattr(ethernet_pdu_signal, 'socket_name')}:" + "\n")
                    for cc in dir(ethernet_pdu_signal):
                        if "__" not in cc:
                            if cc != "socket_name":
                                value = convert_value(getattr(ethernet_pdu_signal, cc))
                                f.write(f"        {cc} = {value}" + "\n")


def convert_value(value):
    if isinstance(value, str):
        return f'"{value}"'
    else:
        return value


import os


def get_all_files(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            # file_list.append(os.path.join(root, file))
            file_list.append(os.path.basename(file).replace(".py", ""))
    return file_list


if __name__ == '__main__':
    # parse_excel_channel_config(r"C:\project\SAT-20241025\ecu-simulator\ecu_simulator\sdk\Internal_ETH\SDBJET2V24R02_CCUETHCommMatrix_240925_Release_240925_1035.xlsx", "SoAdConfigs",
    #             "jupiter", "v_0_4_0")
    parse_excel(r"C:\project\SAT-20241025\ecu-simulator\ecu_simulator\sdk\Internal_ETH\SDBJET2V24R02_CCUETHCommMatrix_240925_Release_240925_1035.xlsx", "EthernetCommMatrix",
                "jupiter", "v_0_4_0")
