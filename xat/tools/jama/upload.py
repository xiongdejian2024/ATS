#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_

"""
@Time: 2022/9/7 13:14  
@Author: lei.tao
@File: upload.py
@Software: PyCharm
@Description: 测试用例自动上传jama
@Examples: 创建用例 用post_item, 更新用put_item
"""
import collections
import os
import sys
import yaml

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

from tools.jama.case_reader_excel import *
from tools.jama.jama_client import *
from xat_ecu.legacy.common.logger import logger


def upload(o_file, sheet, case_id):
    """
    新增测试用例上传jama,把获取的new_case_id写入jama_file
    o_file: 源测试用例文件
    sheet: 源测试用例文件的sheet名
    jama_file: 生成jama_id后写入的文件，默认为jama_id.xlsx
    """
    o_case = CaseParser(o_file)
    testcases = o_case.parse_sheet(sheet)
    sheets = o_case.sheets
    logger.info("测试用例{0}的功能列表为: {1}".format(o_file, sheets))

    jama_id = []

    for cs in testcases:

        if cs.Case_ID == case_id:
            logger.info(
                f'row: {cs.row_num}, case_id: {cs.Case_ID}')
            # 以换行符分割测试步骤和结果，分别填入不同的行
            # steps = cs.TestSteps.split('\n')
            # for i in range(len(steps)):
            #     step_dict = collections.OrderedDict()
            #     step_dict['action'] = steps[i]
            #
            #     for j in range(len(results)):
            #         if j == i:
            #             step_dict['expectedResult'] = results[j]
            #
            #     step_dict['notes'] = None
            #     step_list.append(step_dict)
            # area_dict['testCaseSteps'] = step_list
            # 实现页面换行
            pre = cs.Preconditions.split('\n')
            pre_list = []
            for i in range(len(pre)):
                pre_list.append(pre[i])

            ExpectResult = cs.ExpectResults.split('\n')
            ExpectResult_list = []
            for j in range(len(ExpectResult)):
                ExpectResult_list.append(ExpectResult[j])

            TestStep = cs.TestSteps.split('\n')
            TestStep_list = []
            for x in range(len(TestStep)):
                TestStep_list.append(TestStep[x])

            area_dict = collections.OrderedDict()
            area_dict['name'] = cs.Name
            area_dict['description'] = cs.Case_ID
            area_dict['preconditions$26'] = "<br \>".join(pre_list)
            # Bench:760, Vehicle:759, unassign:758
            if cs.Test_Platform in ["", None]:
                plat = 758
            elif cs.Test_Platform.lower() == "bench":
                plat = 760
            else:
                plat = 759
            area_dict['test_platform$26'] = plat
            area_dict['homologation$26'] = 498
            if cs.TestCase_Priority in ["", None]:
                pro = 835
            elif cs.TestCase_Priority.lower() == "p0":
                pro = 836
            elif cs.TestCase_Priority.lower() == "p1":
                pro = 837
            else:
                pro = 838
            area_dict['tcPriority$26'] = pro   # P0:836, P1:837, P2:838
            area_dict['test_case_maturity_level$26'] = 1011
            if cs.Test_Execution_Mode in ["", None]:
                mode = 761
            elif cs.Test_Execution_Mode.lower() == "automation":
                mode = 763
            else:
                mode = 762
            area_dict['test_execution_mode$26'] = mode  # Automation:763, manual:762
            if cs.Automatable in ["", None]:
                auto = 1343
            elif cs.Automatable.upper() == "Y":
                auto = 1344
            else:
                auto = 1342
            area_dict['automation$26'] = auto    # Y:1344, N:1342
            # area_dict['testCaseStatus']: 测试结果,暂忽略
            area_dict['external_issue_id$26'] = cs.Verifies_DPMS_CR_Issue

            testcase = collections.OrderedDict()
            testcase['action'] = "<br \>".join(TestStep_list)
            testcase['expectedResult'] = "<br \>".join(ExpectResult_list)
            testcase['notes'] = None
            case_list = [testcase]
            area_dict['testCaseSteps'] = case_list

            json.dumps(area_dict, ensure_ascii=False, indent=4)

            with open("./sheet.yaml", "r", encoding='UTF-8') as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                project = data["project"]
                item_type_id = data["item_type_id"]
                child_item_type_id = data["child_item_type_id"]
                if "BGM" in o_file:
                    name = "BGM"
                elif "TCAM" in o_file:
                    name = "TCAM"
                else:
                    logger.error("测试用例的文件名不规范，请更改!!\n需要确认上传的是BGM用例还是TCAM用例，即文件名需要带有BGM或者TCAM")
                    sys.exit()
                location = {'item': data[name][sheet]}
                fields = area_dict

                o_jama = JamaClient(data["jama"]["url"], (data["jama"]["username"], data["jama"]["password"]))

                new_case_id = o_jama.post_item(project, item_type_id, child_item_type_id, location, fields,
                                               global_id=None)
                case_info = o_jama.get_item(new_case_id)
                logger.info("用例{0}的jama_id是：{1},globalId是：{2}".format(cs.Case_ID, new_case_id, case_info['globalId']))
                jama_id.append(new_case_id)

            # 增加用例标签,包括Tags、Test_Level、Release_Version
            # BGM:188, TCAM: 224, 上行: 667, 下行: 668
            # smoke:271, full:666, Sanity:623,
            # V0.6:259, V0.55:285, V0.5:140

            # 增加Tags标签
            # if cs.Tags in ["", None]:
            #     break
            # elif cs.Tags.upper() == "BGM":
            #     o_jama.post_item_tag(new_case_id, 188)
            # elif cs.Tags.upper() == "TCAM":
            #     o_jama.post_item_tag(new_case_id, 224)
            # elif cs.Tags == "上行":
            #     o_jama.post_item_tag(new_case_id, 667)
            # elif cs.Tags == "下行":
            #     o_jama.post_item_tag(new_case_id, 668)
            # else:
            #     o_jama.post_item_tag(new_case_id, 188)
            #     o_jama.post_item_tag(new_case_id, 224)
            tag_list = []
            if '，' in cs.Tags:
                tag_list.extend(cs.Tags.split('，'))
            elif '/' in cs.Tags:
                tag_list.extend(cs.Tags.split('/'))
            else:
                tag_list.append(cs.Tags)
            if len(tag_list) > 0:
                for _tag in tag_list:
                    o_jama.post_item_tag(new_case_id, o_jama.get_id_from_tag(_tag.upper()))

            # 增加Test_Level标签
            if cs.Test_Level in ["", None]:
                continue
            elif cs.Test_Level.lower() == "smoke":
                o_jama.post_item_tag(new_case_id, 271)
            elif cs.Test_Level.lower() == "sanity":
                o_jama.post_item_tag(new_case_id, 623)
            else:
                o_jama.post_item_tag(new_case_id, 666)

            # 增加Release_Version标签
            if cs.Release_Version in ["", None]:
                continue
            elif str("0.65") in cs.Release_Version:
                o_jama.post_item_tag(new_case_id, 145)
            elif str("0.6") in cs.Release_Version:
                o_jama.post_item_tag(new_case_id, 259)
            elif str("0.55") in cs.Release_Version or str("0.5.5") in cs.Release_Version:
                o_jama.post_item_tag(new_case_id, 285)
            else:
                o_jama.post_item_tag(new_case_id, 140)

            print("{}测试用例{}上传成功".format(sheet, cs.Case_ID))

    return new_case_id


if __name__ == '__main__':
    file = "SOA_BGM_测试用例.xlsx"
    data = upload(file, '诊断DID', case_id="BaseTech_NetwaorkArchitecture_DiagDID_0001")
    print(data)
