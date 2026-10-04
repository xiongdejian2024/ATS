#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_

"""
@Time: 2022/9/8 16:24  
@Author: lei.tao
@File: update.py
@Software: PyCharm
@Description: 更新jama上的测试用例
@Example: 创建用例 用post_item, 更新用put_item
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


def update(o_file, sheet, jama_id):
    o_case = CaseParser(o_file)
    testcases = o_case.parse_sheet(sheet)

    for cs in testcases:
        if cs.jama_id == jama_id:
            # 以换行符分割测试步骤和结果，分别更新不同的行
            # steps = cs.TestSteps.split('\n')
            # results = cs.ExpectResults.split('\n')
            # step_list = []
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
            area_dict['tcPriority$26'] = pro
            # draft:1011(未评审)，approved:1013(已评审)
            area_dict['test_case_maturity_level$26'] = 1013
            if cs.Test_Execution_Mode in ["", None]:
                mode = 761
            elif cs.Test_Execution_Mode.lower() == "automation":
                mode = 763
            else:
                mode = 762
            area_dict['test_execution_mode$26'] = mode
            if cs.Automatable in ["", None]:
                auto = 1343
            elif cs.Automatable.upper() == "Y":
                auto = 1344
            else:
                auto = 1342
            area_dict['automation$26'] = auto
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

            new_case_item = o_jama.put_item(project, jama_id, item_type_id, child_item_type_id, location, fields)

            # 获取jama中的标签
            case_tag_list = o_jama.get_item_tags(jama_id)
            case_tag = []
            for tag in case_tag_list:
                case_tag.append(tag["name"])
            # 获取excel中的标签
            excel_list = [cs.Test_Level]
            if '，' in cs.Tags:
                excel_list.extend(cs.Tags.split('，'))
            if '/' in cs.Tags:
                excel_list.extend(cs.Tags.split('/'))
            else:
                excel_list.append(cs.Tags)

            # 删除多余Tags标签
            for _tag in case_tag:
                if _tag.upper() not in [ele.upper() for ele in excel_list]:
                    o_jama.del_item_tag(jama_id, o_jama.get_id_from_tag(_tag))

            # 新增Tags标签
            tag_list = []
            if '，' in cs.Tags:
                tag_list.extend(cs.Tags.split('，'))
            if '/' in cs.Tags:
                tag_list.extend(cs.Tags.split('/'))
            else:
                tag_list.append(cs.Tags)
            for tag_ in tag_list:
                if tag_ not in case_tag:
                    o_jama.post_item_tag(jama_id, o_jama.get_id_from_tag(tag_.upper()))

            # 新增Test_Level标签
            if cs.Test_Level in ["", None]:
                continue
            elif cs.Test_Level.upper() not in [ele.upper() for ele in case_tag]:
                if cs.Test_Level.lower() == "smoke":
                    o_jama.post_item_tag(jama_id, 271)
                elif cs.Test_Level.lower() == "sanity":
                    o_jama.post_item_tag(jama_id, 623)
                else:
                    o_jama.post_item_tag(jama_id, 666)

            # 新增Release_Version标签
            if cs.Release_Version in ["", None]:
                continue
            elif "V0.65" not in case_tag:
                if str("V0.65") in cs.Release_Version.upper():
                    o_jama.post_item_tag(jama_id, 145)
            elif "V0.6" not in case_tag:
                if str("V0.6") in cs.Release_Version.upper():
                    o_jama.post_item_tag(jama_id, 259)
            elif "V0.55" not in case_tag:
                if str("V0.55") in cs.Release_Version.upper():
                    o_jama.post_item_tag(jama_id, 285)
                elif str("V0.5.5") in cs.Release_Version.upper():
                    o_jama.post_item_tag(jama_id, 285)

            if new_case_item == 200:
                print("{0}测试用例{1}更新成功".format(sheet, cs.Case_ID))
            else:
                print("{0}测试用例{1}更新失败，请检查jama_id{2}".format(sheet, cs.Case_ID, jama_id))


if __name__ == '__main__':
    file = "SOA_TCAM_测试用例.xlsx"
    sheetname = "EM"
    update(file, sheetname, jama_id=1198036)
