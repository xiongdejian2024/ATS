# -*- coding: utf-8 -*-
"""
@File        : jama_test.py
@Author      : jinhui.zhao@jiduauto.com
@Time        : 2022/7/12 0:32
@Description : 测试用例自动上传jama
@Examples    : 创建用例 用post_item, 更新用put_item
"""

from jama_client import *

jama_url = "https://jama.jiduauto.com"

jama_api_username = "public_soa_bgm_tcam"
jama_api_password = __import__("os").environ.get('XAT_CREDENTIAL____JAMA_JAMA_TEST_PY_JAMA_API_PASSWORD', "")

o_jama = JamaClient(jama_url, (jama_api_username, jama_api_password))
projects = o_jama.get_projects()
print(projects)

project = 46
item_type_id = 26
child_item_type_id = 26
location = {'item': 573027}
fields = {
    'name': 'ptp_test',
    'description': '测试读取TCAM的ptp',
    'preconditions$26': '1.TCAM 唤醒',
    'test_platform$26': 760,
    'testCaseSteps': [{
        'action': '1.读取“/oemapp/bin/gptp/automotive-slave.cfg”配置文件信息',
        'expectedResult': 'just test',
        'notes': ''},
        {
            'action': '2.读取“第二步“',
            'expectedResult': '验证第二步\n应该包含时间\n更新222',
            'notes': ''
        },
        {
            'action': '2.读取“第三步“',
            'expectedResult': '验证第三步\n应该包含时间\n更新222',
            'notes': ''
        }
    ],
    'homologation$26': 498,
    'tcPriority$26': 835,
    'test_case_maturity_level$26': 1011
}

global_id = "GID-389423"
# 创建用例
# new_case_id = o_jama.post_item(project, item_type_id, child_item_type_id, location, fields, global_id=None)
# print(new_case_id)
# 更新用例
# new_case_item = o_jama.put_item(project, 573048, item_type_id, child_item_type_id,location,fields)
# print(new_case_item)


# 用new_case_id：1160509可以获取global_id

case = o_jama.get_item(1163223)
print(case['globalId'])
print(case)
