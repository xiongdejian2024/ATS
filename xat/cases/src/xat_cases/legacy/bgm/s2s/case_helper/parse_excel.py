import os
import pickle

import xlrd2
from xat_ecu.legacy.common.logger import logger


class excelCase:
    """
    单条测试用例封装
    """
    def __init__(self, case_id, jama_id, interface_name, pre_condition, channel, message_id, signal_name, signal_value,
                 service_name, function_name, parameters, function_type, function_input):
        self.case_id = case_id
        self.jama_id = jama_id
        self.interface_name = interface_name if len(interface_name) > 0 else '未定义'
        self.pre_condition = pre_condition
        self.channel = channel.split('\n')  # 总线名称按照 \n 分割
        self.message_id = message_id.split('\n')  # 报文ID 按照 \n 分割
        self.signal_name = signal_name.split('\n')  # 信号名称 按照 \n 分割
        self.signal_value = signal_value.split('\n')  # 信号值 按照 \n 分割
        self.service_name = service_name
        self.function_name = function_name
        self.parameters = parameters
        self.function_type = function_type
        self.function_input = function_input


def get_upstream_testcases_by_read_excel_from_ms(excel_path, sheet_name, ids=False):
    """
    读取从meterSphere中导出的excel用例，以获取excel中对应数据模型的测试用例，返回测试用例集
    ddt_type：目前支持upstream、downstream、set-get 三种
    """
    current_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir = current_path.split("sat")[0] + "sat/xat_cases/legacy/test_data/bgm/s2s/auto_test"
    excel_path = os.path.join(parent_dir, excel_path)
    wb1 = xlrd2.open_workbook(excel_path, encoding_override="utf-8")
    sheet1 = wb1.sheet_by_name(sheet_name)
    testcases1 = []
    id_list = []
    num_rows = sheet1.nrows
    for j1 in range(1, num_rows):
        ddt_type = sheet1.cell_value(j1, 16)
        if len(ddt_type) == 0:  # 如果ddt_type为空，则跳过该行
            continue
        if ddt_type != "upstream":  # 如果ddt_type与入参传过来的ddt_type_name不匹配，则跳过该行
            continue
        case_id = sheet1.cell_value(j1, 0)  # 获取case_id
        if len(str(case_id)) == 0:  # 如果case_id 为空，则跳过
            continue
        jama_id = sheet1.cell_value(j1, 1) if len(sheet1.cell_value(j1, 1)) > 0 else ""  # 获取 “用例名称”
        interface_name = sheet1.cell_value(j1, 12) if len(sheet1.cell_value(j1, 12)) > 0 else ""  # 获取 “接口名称”
        pre_condition = sheet1.cell_value(j1, 4) if len(sheet1.cell_value(j1, 4)) > 0 else ""  # 获取 “前置条件”
        if "stop_send_pdu_then_resume=backbone" in pre_condition:  # 目前暂不支持FR总线信号的暂停
            continue
        if "接负级" in pre_condition:  # 用例已转成非数据驱动脚本
            continue
        if "接地" in pre_condition:  # 用例已转成非数据驱动脚本
            continue

        """解析 步骤描述 字段 start """
        step_description = sheet1.cell_value(j1, 6) if len(sheet1.cell_value(j1, 6)) > 0 else ""  # 获取 “步骤描述”
        if len(step_description) == 0:
            continue
        if "self.ipdu" in step_description:  # 过滤无效的测试用例
            continue
        if "self.partner" in step_description:
            continue
        channel_list = []
        message_id_list = []
        signal_name_list = []
        signal_value_list = []
        if len(step_description) == 0:  # 如果步骤描述为空，则跳过该行
            continue
        else:  # 按行解析步骤描述，并封装到channel、message_id、signal_name、signal_value中
            step_description_list = step_description.split("\n")  # 按分行符分割到list中
            for step in step_description_list:
                if '.' in step[0:3]:
                    step = step[step.find('.')+1:]  # 去除每一行第一个'.'及以前的字符
                row_list = step.split(":")  # 每一行按照
                if len(row_list) != 4:  # 无效的行, 则直接跳过
                    continue
                else:
                    channel_list.append(row_list[0])
                    message_id_list.append(row_list[1])
                    signal_name_list.append(row_list[2])
                    signal_value_list.append(row_list[3])
        if len(channel_list) == 0:
            continue
        channel = "\n".join(channel_list)
        message_id = "\n".join(message_id_list)
        signal_name = "\n".join(signal_name_list)
        signal_value = "\n".join(signal_value_list)
        """解析 步骤描述 字段 end """

        """解析预期结果 字段 start """
        expected_description = sheet1.cell_value(j1, 7) if len(sheet1.cell_value(j1, 7)) > 0 else ""  # 获取 “预期结果”
        if "self.ipdu" in expected_description:  # 过滤无效的测试用例
            continue
        if "self.partner" in expected_description:
            continue
        service_name = ""
        function_name = ""
        parameters = ""
        function_type = ""
        function_input = ""
        if len(expected_description) <= 2:  # 如果预期结果为空，则跳过该行
            continue
        else:
            expected_description_list = expected_description.split("\n")
            for expected in expected_description_list:
                if '.' in expected[0:3]:
                    expected = expected[expected.find('.')+1:]  # 去除每一行第一个'.'及以前的字符
                row_list = expected.split("&")
                if len(row_list) != 5:
                    continue
                else:  # 仅保留初次适配的
                    service_name = row_list[0]
                    function_name = row_list[1]
                    function_type = row_list[2]
                    function_input = row_list[3]
                    parameters = row_list[4]
                    break
        if len(service_name) == 0:
            continue
        if ids:
            id_list.append(int(case_id))
        else:
            test_case = excelCase(case_id, jama_id, interface_name, pre_condition, channel, message_id,
                                  signal_name, signal_value, service_name, function_name, parameters,
                                  function_type, function_input)
            testcases1.append(test_case)
    if ids:
        logger.info("=============================================")
        logger.info(f"上行，case_id的个数：{len(id_list)}")
        logger.info("=============================================")
        return id_list
    else:
        return testcases1


def get_downstream_testcases_by_read_excel_from_ms(excel_path, sheet_name, ids=False):
    """
    读取从meterSphere中导出的excel用例，以获取excel中对应数据模型的测试用例，返回测试用例集
    ddt_type：目前支持upstream、downstream、set-get 三种
    """
    current_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir = current_path.split("sat")[0] + "sat/xat_cases/legacy/test_data/bgm/s2s/auto_test"
    excel_path = os.path.join(parent_dir, excel_path)
    wb1 = xlrd2.open_workbook(excel_path, encoding_override="utf-8")
    sheet1 = wb1.sheet_by_name(sheet_name)
    testcases1 = []
    id_list = []
    num_rows = sheet1.nrows
    for j1 in range(1, num_rows):
        ddt_type = sheet1.cell_value(j1, 16)
        if len(ddt_type) == 0:  # 如果ddt_type为空，则跳过该行
            continue
        if ddt_type != "downstream":  # 如果ddt_type与入参传过来的ddt_type_name不匹配，则跳过该行
            continue
        case_id = sheet1.cell_value(j1, 0)  # 获取case_id
        if len(str(case_id)) == 0:  # 如果case_id 为空，则跳过
            continue
        jama_id = sheet1.cell_value(j1, 1) if len(sheet1.cell_value(j1, 1)) > 0 else ""  # 获取 “用例名称”
        interface_name = sheet1.cell_value(j1, 12) if len(sheet1.cell_value(j1, 12)) > 0 else ""  # 获取 “接口名称”
        pre_condition = sheet1.cell_value(j1, 4) if len(sheet1.cell_value(j1, 4)) > 0 else ""  # 获取 “前置条件”
        if "stop_send_pdu_then_resume=backbone" in pre_condition:  # 目前暂不支持FR总线信号的暂停
            continue
        if "接负级" in pre_condition:  # 用例已转成非数据驱动脚本
            continue
        if "接地" in pre_condition:  # 用例已转成非数据驱动脚本
            continue

        """解析 步骤描述 字段 start """
        step_description = sheet1.cell_value(j1, 7) if len(sheet1.cell_value(j1, 7)) > 0 else ""  # 获取 “步骤描述”
        if len(step_description) == 0:
            continue
        if "self.ipdu" in step_description:  # 过滤无效的测试用例
            continue
        if "self.partner" in step_description:
            continue
        channel_list = []
        message_id_list = []
        signal_name_list = []
        signal_value_list = []
        if len(step_description) == 0:  # 如果步骤描述为空，则跳过该行
            continue
        else:  # 按行解析步骤描述，并封装到channel、message_id、signal_name、signal_value中
            step_description_list = step_description.split("\n")  # 按分行符分割到list中
            for step in step_description_list:
                if '.' in step[0:3]:
                    step = step[step.find('.')+1:]  # 去除每一行第一个'.'及以前的字符
                row_list = step.split(":")  # 每一行按照
                if len(row_list) != 4:  # 无效的行, 则直接跳过
                    continue
                else:
                    channel_list.append(row_list[0])
                    message_id_list.append(row_list[1])
                    signal_name_list.append(row_list[2])
                    signal_value_list.append(row_list[3])
        if len(channel_list) == 0:
            continue
        channel = "\n".join(channel_list)
        message_id = "\n".join(message_id_list)
        signal_name = "\n".join(signal_name_list)
        signal_value = "\n".join(signal_value_list)
        """解析 步骤描述 字段 end """

        """解析预期结果 字段 start """
        expected_description = sheet1.cell_value(j1, 6) if len(sheet1.cell_value(j1, 6)) > 0 else ""  # 获取 “预期结果”
        if "self.ipdu" in expected_description:  # 过滤无效的测试用例
            continue
        if "self.partner" in expected_description:
            continue
        service_name = ""
        function_name = ""
        parameters = ""
        function_type = ""
        function_input = ""
        if len(expected_description) <= 2:   # 如果预期结果为空，则跳过该行
            continue
        else:
            expected_description_list = expected_description.split("\n")
            for expected in expected_description_list:
                if '.' in expected[0:3]:
                    expected = expected[expected.find('.')+1:]  # 去除每一行第一个'.'及以前的字符
                row_list = expected.split("&")
                if len(row_list) != 4:
                    continue
                else:  # 仅保留初次适配的
                    service_name = row_list[0]
                    function_name = row_list[1]
                    function_type = row_list[2]
                    parameters = row_list[3]
                    break

        if len(service_name) == 0:
            continue
        if ids:
            id_list.append(int(case_id))
        else:
            test_case = excelCase(case_id, jama_id, interface_name, pre_condition, channel, message_id,
                                  signal_name, signal_value, service_name, function_name, parameters,
                                  function_type, function_input)
            testcases1.append(test_case)
    if ids:
        logger.info("=============================================")
        logger.info(f"下行，case_id的个数：{len(id_list)}")
        logger.info("=============================================")
        return id_list
    else:
        return testcases1


def get_set_get_testcases_by_read_excel_from_ms(excel_path, sheet_name, ids=False):
    """
    读取从meterSphere中导出的excel用例，以获取excel中对应数据模型的测试用例，返回测试用例集
    ddt_type：目前支持upstream、downstream、set-get 三种
    """
    current_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir = current_path.split("sat")[0] + "sat/xat_cases/legacy/test_data/bgm/s2s/auto_test"
    excel_path = os.path.join(parent_dir, excel_path)
    wb1 = xlrd2.open_workbook(excel_path, encoding_override="utf-8")
    sheet1 = wb1.sheet_by_name(sheet_name)
    testcases1 = []
    id_list = []
    num_rows = sheet1.nrows
    for j1 in range(1, num_rows):
        ddt_type = sheet1.cell_value(j1, 16)
        if len(ddt_type) == 0:  # 如果ddt_type为空，则跳过该行
            continue
        if ddt_type != "set_get":  # 如果ddt_type与入参传过来的ddt_type_name不匹配，则跳过该行
            continue
        case_id = sheet1.cell_value(j1, 0)  # 获取case_id
        if len(str(case_id)) == 0:  # 如果case_id 为空，则跳过
            continue
        jama_id = sheet1.cell_value(j1, 1) if len(sheet1.cell_value(j1, 1)) > 0 else ""  # 获取 “用例名称”
        interface_name = sheet1.cell_value(j1, 12) if len(sheet1.cell_value(j1, 12)) > 0 else ""  # 获取 “接口名称”
        pre_condition = sheet1.cell_value(j1, 4) if len(sheet1.cell_value(j1, 4)) > 0 else ""  # 获取 “前置条件”
        if "stop_send_pdu_then_resume=backbone" in pre_condition:  # 目前暂不支持FR总线信号的暂停
            continue
        if "接负级" in pre_condition:  # 用例已转成非数据驱动脚本
            continue
        if "接地" in pre_condition:  # 用例已转成非数据驱动脚本
            continue

        """解析 步骤描述 字段 start """
        step_description = sheet1.cell_value(j1, 6) if len(sheet1.cell_value(j1, 6)) > 0 else ""  # 获取 “步骤描述”
        if len(step_description) == 0:
            continue
        if "self.ipdu" in step_description:  # 过滤无效的测试用例
            continue
        if "self.partner" in step_description:
            continue
        channel_list = []
        message_id_list = []
        signal_name_list = []
        signal_value_list = []
        if len(step_description) == 0:  # 如果步骤描述为空，则跳过该行
            continue
        else:  # 按行解析步骤描述，并封装到channel、message_id、signal_name、signal_value中
            step_description_list = step_description.split("\n")  # 按分行符分割到list中
            for step in step_description_list:
                if '.' in step[0:3]:
                    step = step[step.find('.')+1:]  # 去除每一行第一个'.'及以前的字符
                row_list = step.split("&")  # 每一行按照
                if len(row_list) != 4:  # 无效的行, 则直接跳过
                    continue
                elif "Service" not in row_list[0]:  # 如果“&”分割后的列表的第一个元素 不包含“Service”，则跳过
                    continue
                else:
                    channel_list.append(row_list[0])
                    message_id_list.append(row_list[1])
                    signal_name_list.append(row_list[2])
                    signal_value_list.append(row_list[3])
                    break
        if len(channel_list) == 0:
            continue
        channel = "\n".join(channel_list)
        message_id = "\n".join(message_id_list)
        signal_name = "\n".join(signal_name_list)
        signal_value = "\n".join(signal_value_list)

        """解析 步骤描述 字段 end """

        """解析预期结果 字段 start """
        expected_description = sheet1.cell_value(j1, 7) if len(sheet1.cell_value(j1, 7)) > 0 else ""  # 获取 “预期结果”
        if "self.ipdu" in expected_description:  # 过滤无效的测试用例
            continue
        if "self.partner" in expected_description:
            continue
        service_name = ""
        function_name = ""
        parameters = ""
        function_type = ""
        function_input = ""
        if len(expected_description) <= 2:  # 如果预期结果为空，则跳过该行
            continue
        else:
            expected_description_list = expected_description.split("\n")
            for expected in expected_description_list:
                if '.' in expected[0:3]:
                    expected = expected[expected.find('.')+1:]  # 去除每一行第一个'.'及以前的字符
                row_list = expected.split("&")
                if len(row_list) != 5:
                    continue
                elif "Service" not in row_list[0]:  # 如果“&”分割后的列表的第一个元素 不包含“Service”，则跳过
                    continue
                else:
                    service_name = row_list[0]
                    function_name = row_list[1]
                    function_type = row_list[2]
                    function_input = row_list[3]
                    parameters = row_list[4]
                    break
        if len(service_name) == 0:
            continue
        if ids:
            id_list.append(int(case_id))
        else:
            test_case = excelCase(case_id, jama_id, interface_name, pre_condition, channel, message_id,
                                  signal_name, signal_value, service_name, function_name, parameters,
                                  function_type, function_input)
            testcases1.append(test_case)
    if ids:
        logger.info("=============================================")
        logger.info(f"set-get，case_id的个数：{len(id_list)}")
        logger.info("=============================================")
        return id_list
    else:
        return testcases1


if __name__ == '__main__':
    # testcases = get_upstream_testcases_by_read_excel_from_ms(r"wti_new_name.xlsx", "模版")
    # print(testcases[0].parameters)
    # print("读取到的用例总数：{}".format(len(testcases)))
    #把最近失败的用例的ID保存到本地，下次执行时仅过滤并执行失败的用例；机制启用控制：only_run_fail_of_last_time，文件名：
    # fail_case_list = ["1", "2", "3", "4"]
    # with open('data.pickle', 'wb') as f:
    #     pickle.dump(fail_case_list, f, pickle.HIGHEST_PROTOCOL)
    #
    # with open('data.pickle', 'rb') as f:
    #     data = pickle.load(f)
    print(int(25575.44757+0.5))


