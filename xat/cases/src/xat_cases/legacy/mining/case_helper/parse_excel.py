import json
import os
import pickle

import xlrd2
from xat_ecu.legacy.common.logger import logger


class SignalExcelCase:
    """
    单条测试用例封装
    """
    def __init__(self, case_id, jama_id, bus_name, message_id, message_name, signal_name, signal_value):
        self.case_id = case_id
        self.jama_id = jama_id
        self.bus_name = bus_name
        self.message_id = message_id
        self.message_name = message_name
        self.signal_name = signal_name
        self.signal_value = str(signal_value)

    def __repr__(self):
        obj = {'case_id': self.case_id, 'jama_id': self.jama_id, 'bus_name': self.bus_name,
               'message_id': self.message_id, 'message_name': self.message_name,
               'signal_name': self.signal_name, 'signal_value': self.signal_value}
        return json.dumps(obj, ensure_ascii=False, indent=4).encode('utf-8').decode('utf-8')


class ServiceExcelCase:
    """
    单条测试用例封装
    """
    def __init__(self, case_id, pre_condition, action, expect_result, service_name):
        self.case_id = case_id
        self.pre_condition = pre_condition
        self.action = action
        self.expect_result = expect_result
        self.service_name = service_name

    def __repr__(self):
        obj = {'case_id': self.case_id, 'pre_condition': self.pre_condition, 'action': self.action,
               'expect_result': self.expect_result, 'service_name': self.service_name}
        return json.dumps(obj, ensure_ascii=False, indent=4).encode('utf-8').decode('utf-8')


def get_signal_testcases_from_excel(excel_path, sheet_name, ids=False):

    current_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir = current_path.split("sat")[0] + "sat/xat_cases/legacy/test_data/mining/data_drive"
    excel_path = os.path.join(parent_dir, excel_path)
    print(excel_path)
    wb1 = xlrd2.open_workbook(excel_path, encoding_override="utf-8")
    sheet1 = wb1.sheet_by_name(sheet_name)
    testcases1 = []
    id_list = []
    num_rows = sheet1.nrows
    for j1 in range(1, num_rows):
        case_id = sheet1.cell_value(j1, 0)  # 获取case_id
        if len(str(case_id)) == 0:  # 如果case_id 为空，则跳过
            continue
        jama_id = sheet1.cell_value(j1, 1)  # 获取 “jama_id”
        if isinstance(jama_id, float):
            jama_id = int(jama_id)
        signal_name = sheet1.cell_value(j1, 2) if len(sheet1.cell_value(j1, 2)) > 0 else ""  # 获取 “信号名称”
        signal_name_alias = sheet1.cell_value(j1, 3) if len(sheet1.cell_value(j1, 3)) > 0 else signal_name
        if len(signal_name_alias) == 0:
            continue

        channel_id = sheet1.cell_value(j1, 5)   # 获取channel_id
        if isinstance(channel_id, float):
            channel_id = int(channel_id)
        if isinstance(channel_id, int):
            channel_id = get_bus_name_by_id(channel_id)
            if not channel_id:
                continue
        else:
            continue
        message_id = sheet1.cell_value(j1, 6) if len(sheet1.cell_value(j1, 6)) > 0 else ""  # 获取 “message_id”
        if len(message_id) == 0:
            continue
        message_name = sheet1.cell_value(j1, 9) if len(sheet1.cell_value(j1, 9)) > 0 else ""  # 获取 “message_name”
        tx_node = sheet1.cell_value(j1, 10) if len(sheet1.cell_value(j1, 10)) > 0 else ""  # 获取 “tx_node”
        if len(tx_node) == 0 or tx_node.strip().upper() == 'BGM':
            continue
        signal_value = sheet1.cell_value(j1, 11)
        if not isinstance(signal_value, float):
            continue
        try:
            signal_value = float(signal_value)
        except Exception as e:
            continue

        if ids:
            id_list.append(int(case_id))
        else:
            test_case = SignalExcelCase(case_id, jama_id, channel_id, message_id, message_name, signal_name_alias,
                                        signal_value)
            testcases1.append(test_case)
    if ids:
        logger.info("=============================================")
        logger.info(f"数据埋点下，信号用例个数：{len(id_list)}")
        logger.info("=============================================")
        return id_list
    else:
        return testcases1


def get_service_testcases_from_excel(excel_path, sheet_name, ids=False):

    current_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir = current_path.split("sat")[0] + "sat/xat_cases/legacy/test_data/mining/data_drive"
    excel_path = os.path.join(parent_dir, excel_path)
    print(excel_path)
    wb1 = xlrd2.open_workbook(excel_path, encoding_override="utf-8")
    sheet1 = wb1.sheet_by_name(sheet_name)
    testcases1 = []
    id_list = []
    num_rows = sheet1.nrows
    for j1 in range(1, num_rows):
        case_id = sheet1.cell_value(j1, 0)  # 获取case_id
        if len(str(case_id)) == 0:  # 如果case_id 为空，则跳过
            continue

        pre_condition = sheet1.cell_value(j1, 2) if len(sheet1.cell_value(j1, 2)) > 0 else ""  # 获取 “前置条件”

        action = sheet1.cell_value(j1, 3) if len(sheet1.cell_value(j1, 3)) > 0 else ""  # 获取“执行步骤”
        if len(action) == 0:
            continue

        expect_result = sheet1.cell_value(j1, 4) if len(sheet1.cell_value(j1, 4)) > 0 else ""  # 获取预期结果
        if len(expect_result) == 0:
            continue
        service_name = sheet1.cell_value(j1, 5) if len(sheet1.cell_value(j1, 5)) > 0 else ""  # 获取服务名称
        if len(service_name) == 0:
            continue

        if ids:
            id_list.append(int(case_id))
        else:
            test_case = ServiceExcelCase(case_id, pre_condition, action, expect_result, service_name)
            testcases1.append(test_case)
    if ids:
        logger.info("=============================================")
        logger.info(f"数据埋点下，服务用例个数：{len(id_list)}")
        logger.info("=============================================")
        return id_list
    else:
        return testcases1


def get_bus_name_by_id(channel_id):
    if channel_id == 1:
        return "backbonefr"
    if channel_id == 2:
        return "infoanfd"
    if channel_id == 3:
        return "adcanfd"
    if channel_id == 4:
        return "propulsioncan"
    if channel_id == 5:
        return "chassiscan1"
    if channel_id == 6:
        return "chassiscan2"
    if channel_id == 7:
        return "passivesafetycan"
    if channel_id == 8:
        return "connectivitycanfd"
    if channel_id == 9:
        return "bodycan"
    if channel_id == 10:
        return "bodyexposedcanfd"
    if channel_id == 41:
        return "cem_lin1"
    if channel_id == 42:
        return "cem_lin2"
    if channel_id == 43:
        return "cem_lin3"
    if channel_id == 44:
        return "cem_lin4"
    if channel_id == 45:
        return "cem_lin5"
    if channel_id == 46:
        return "cem_lin6"
    if channel_id == 47:
        return "cem_lin7"
    else:
        return False


if __name__ == '__main__':
    testcases = get_signal_testcases_from_excel(r"信号方案初稿.xlsx", "BodyCAN")
    print(testcases[0])
    print("读取到的用例总数：{}".format(len(testcases)))
