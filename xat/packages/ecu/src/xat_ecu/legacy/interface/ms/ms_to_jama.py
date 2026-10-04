#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_

"""
@File: ms_to_jama.py
@Time: 2023/01/11 11:07
@Author: lei.tao
@Software: PyCharm
@Description: 测试管理平台MeterSphere测试用例导出到jama,需要获取jama编辑权限
@Examples:
"""
import time
import json
import os
import sys
project_root = __import__("xat_ecu.resources", fromlist=["LEGACY_ROOT"]).LEGACY_ROOT.as_posix()
from xat_ecu.legacy.common.constant import MS_CONSTANT
# from ecu_simulator.common.logger import Logger
import requests
# logger = Logger().get_logger(__name__)
from xat_ecu.legacy.common.logger import logger


def cut_list(lists, cut_len):
    res_data = []
    if len(lists) > cut_len:
        for i in range(int(len(lists) / cut_len)):
            cut_a = lists[cut_len * i:cut_len * (i + 1)]
            res_data.append(cut_a)

        last_data = lists[int(len(lists) / cut_len) * cut_len:]
        if last_data:
            res_data.append(last_data)
    else:
        res_data.append(lists)
    return res_data


class meterSphere_client:
    def __init__(self, username, password, server_name='https://ms.jiduprod.com'):
        self.username = username
        self.password = password
        self.server_name = server_name
        self.csrfToken = ''
        self.lastWorkspaceId = ''
        self.lastProjectId = ''
        self.Cookie = ''
        self.signin()

    def signin(self, path="/ldap/signin"):
        """ 
        登录 ms 系统, 获取response Headers信息
        """
        # ms1.0
        # headers = {'Accept': 'application/json, text/plain, */*',
        #            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36',
        #            'Content-Type': 'application/json', 'Accept-Encoding': 'gzip, deflate',
        #            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8', 'Connection': 'keep-alive'}
        headers = {'Accept': 'application/json, text/plain, */*',
                   'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
                   'Content-Type': 'application/json;  charset=UTF-8', 'Accept-Encoding': 'gzip, deflate, br',
                   'Accept-Language': 'zh-CN', 'Connection': 'keep-alive'}
        data = {'username': self.username, 'password': self.password, 'authenticate': 'LDAP'}
        url = self.server_name + path
        response = requests.post(url, json.dumps(data), headers=headers)
        resp_body = json.loads(str(response.content, 'utf-8'))
        resp_header = response.headers
        print(resp_header)
        # list_cookie = resp_header.get("Set-Cookie").split(";")

        self.csrfToken = resp_body.get("data").get("csrfToken")
        self.lastWorkspaceId = resp_body.get("data").get("lastWorkspaceId")
        self.lastProjectId = resp_body.get("data").get("lastProjectId")
        self.Cookie = resp_body.get("data").get("sessionId")
        logger.info(self.Cookie)
        logger.info(self.csrfToken)
        logger.info(self.lastProjectId)
        logger.info(self.lastWorkspaceId)
        if  resp_body.get("success") is True:
            logger.info("登录成功")
        else:
            logger.info("登录失败")
            exit()


    def set_testcase_ms_to_jama(self, projectId="", workspaceId="", nodeIds=[], Ids=None, path="/jidu/jama/export2Jama"):
        """
        projectId: 工作空间id
        workspaceId: 工作空间中的项目id
        nodeIds: 项目中的测试用例文件夹id集合
        Ids: 测试文件夹中的测试用例id集合
        根据Ids和nodeIds导出测试用例
        """

        if not projectId:
            projectId = self.lastProjectId
        if not workspaceId:
            workspaceId = self.lastWorkspaceId
        if not Ids:
            Flag = True
        else:
            Flag = False
        
        headers = {'CSRF-TOKEN': self.csrfToken, 'PROJECT': projectId, 'WORKSPACE': workspaceId,
                   'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36',
                   'Accept-Encoding': 'gzip, deflate', 'Cookie': self.Cookie,
                   'Accept-Language': 'zh-CN,zh;q=0.9', 'Content-Type': 'application/json'}
    
        data = {
                "ids": Ids,
                "projectId": projectId,
                "condition": {
                    "components": [
                    {
                        "key": "name",
                        "name": "MsTableSearchInput",
                        "label": "commons.name",
                        "operator": {
                        "value": "like",
                        "options": [
                            {
                            "label": "commons.adv_search.operators.like",
                            "value": "like"
                            },
                            {
                            "label": "commons.adv_search.operators.not_like",
                            "value": "not like"
                            }
                        ]
                        }
                    },
                    {
                        "key": "tags",
                        "name": "MsTableSearchInput",
                        "label": "commons.tag",
                        "operator": {
                        "value": "like",
                        "options": [
                            {
                            "label": "commons.adv_search.operators.like",
                            "value": "like"
                            },
                            {
                            "label": "commons.adv_search.operators.not_like",
                            "value": "not like"
                            }
                        ]
                        }
                    },
                    {
                        "key": "module",
                        "name": "MsTableSearchInput",
                        "label": "test_track.case.module",
                        "operator": {
                        "value": "like",
                        "options": [
                            {
                            "label": "commons.adv_search.operators.like",
                            "value": "like"
                            },
                            {
                            "label": "commons.adv_search.operators.not_like",
                            "value": "not like"
                            }
                        ]
                        }
                    },
                    {
                        "key": "priority",
                        "name": "MsTableSearchSelect",
                        "label": "test_track.case.priority",
                        "operator": {
                        "options": [
                            {
                            "label": "commons.adv_search.operators.in",
                            "value": "in"
                            },
                            {
                            "label": "commons.adv_search.operators.not_in",
                            "value": "not in"
                            }
                        ]
                        },
                        "options": [
                        {
                            "label": "P0",
                            "value": "P0"
                        },
                        {
                            "label": "P1",
                            "value": "P1"
                        },
                        {
                            "label": "P2",
                            "value": "P2"
                        },
                        {
                            "label": "P3",
                            "value": "P3"
                        }
                        ],
                        "props": {
                        "multiple": True
                        }
                    },
                    {
                        "key": "createTime",
                        "name": "MsTableSearchDateTimePicker",
                        "label": "commons.create_time",
                        "operator": {
                        "options": [
                            {
                            "label": "commons.adv_search.operators.between",
                            "value": "between"
                            },
                            {
                            "label": "commons.adv_search.operators.gt",
                            "value": "gt"
                            },
                            {
                            "label": "commons.adv_search.operators.ge",
                            "value": "ge"
                            },
                            {
                            "label": "commons.adv_search.operators.lt",
                            "value": "lt"
                            },
                            {
                            "label": "commons.adv_search.operators.le",
                            "value": "le"
                            },
                            {
                            "label": "commons.adv_search.operators.equals",
                            "value": "eq"
                            }
                        ]
                        }
                    },
                    {
                        "key": "updateTime",
                        "name": "MsTableSearchDateTimePicker",
                        "label": "commons.update_time",
                        "operator": {
                        "options": [
                            {
                            "label": "commons.adv_search.operators.between",
                            "value": "between"
                            },
                            {
                            "label": "commons.adv_search.operators.gt",
                            "value": "gt"
                            },
                            {
                            "label": "commons.adv_search.operators.ge",
                            "value": "ge"
                            },
                            {
                            "label": "commons.adv_search.operators.lt",
                            "value": "lt"
                            },
                            {
                            "label": "commons.adv_search.operators.le",
                            "value": "le"
                            },
                            {
                            "label": "commons.adv_search.operators.equals",
                            "value": "eq"
                            }
                        ]
                        }
                    },
                    {
                        "key": "creator",
                        "name": "MsTableSearchSelect",
                        "label": "api_test.creator",
                        "operator": {
                        "options": [
                            {
                            "label": "commons.adv_search.operators.in",
                            "value": "in"
                            },
                            {
                            "label": "commons.adv_search.operators.not_in",
                            "value": "not in"
                            },
                            {
                            "label": "commons.adv_search.operators.current_user",
                            "value": "current user"
                            }
                        ]
                        },
                        "options": {
                        "url": "/user/ws/current/member/list",
                        "labelKey": "name",
                        "valueKey": "id"
                        },
                        "props": {
                        "multiple": True
                        }
                    },
                    {
                        "key": "reviewStatus",
                        "name": "MsTableSearchSelect",
                        "label": "test_track.review_view.execute_result",
                        "operator": {
                        "options": [
                            {
                            "label": "commons.adv_search.operators.in",
                            "value": "in"
                            },
                            {
                            "label": "commons.adv_search.operators.not_in",
                            "value": "not in"
                            }
                        ]
                        },
                        "options": [
                        {
                            "label": "test_track.review.prepare",
                            "value": "Prepare"
                        },
                        {
                            "label": "test_track.review.pass",
                            "value": "Pass"
                        },
                        {
                            "label": "test_track.review.un_pass",
                            "value": "UnPass"
                        }
                        ],
                        "props": {
                        "multiple": True
                        }
                    }
                    ],
                    "filters": {
                    "reviewStatus": [
                        "Prepare",
                        "Pass",
                        "UnPass"
                    ]
                    },
                    "planId": "",
                    "nodeIds": nodeIds,
                    "selectAll": Flag,
                    "unSelectIds": [],
                    "orders": [],
                    "versionId": None,
                    "selectThisWeedData": False,
                    "selectThisWeedRelevanceData": False,
                    "caseCoverage": None,
                    "projectId": projectId,
                    "trashEnable": False,
                    "publicEnable": False
                }
                }

        url = self.server_name + path
        response = requests.post(url, json.dumps(data), headers=headers)
        logger.info("Status Code: {}".format(response))
        resp_body = json.loads(str(response.content, 'utf-8'))
        logger.info("Response: {}".format(resp_body))
        if resp_body.get('success') is True:
            logger.info("Upload testcase to jama success!!")
            return True
        else:
            logger.info("Upload testcase to jama failed!!")
            return False
        
    def get_testcases_from_nodeIds(self, nodeIds, projectId='', path="/track/test/case/list/1/100"):
        """
        获取文件夹下所有的测试用例ids
        返回值类型: list, 包含文件夹下的测试用例的 详细信息
        """
        headers = {
            'CSRF-TOKEN': self.csrfToken,
            'PROJECT': self.lastProjectId,
            'WORKSPACE': self.lastWorkspaceId,
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-AUTH-TOKEN': self.Cookie,
            'Accept-Language': 'zh-CN',
            'Content-Type': 'application/json',
        }
        if not projectId:
            projectId = self.lastProjectId
        data = {"nodeIds": nodeIds, "projectId": projectId, "status": None}
        i = 1
        result = []
        while True:
            path = f"/track/test/case/list/{i}/50"
            url = self.server_name + path
            response = requests.post(url, json.dumps(data), headers=headers)
            resp_body = json.loads(str(response.content, 'utf-8'))
            if len(resp_body['data']["listObject"]) == 50:
                result.extend(resp_body['data']["listObject"])
                i = i + 1
            else:
                result.extend(resp_body['data']["listObject"])
                break

        logger.info("获取到的用例数：{}".format(len(result)))
        return result



class Upload():
    def __init__(self):
        user = "ldap_soa_jama"
        passWord = __import__("os").environ.get('XAT_CREDENTIAL_ECU__INTERFACE_MS_MS_TO_JAMA_PY_PASSWORD', "")
        logger.info("登录MS!!")
        self.client = meterSphere_client(user, passWord)
        logger.info("开始导入用例到jama!!")
        self.zero_time = self.get_zero_time()


    def get_cases(self, nodeIds, projectid):
        case_id = []
        jama_id_mapping = []
        res = self.client.get_testcases_from_nodeIds(nodeIds, projectid)
        #print(res[0])
        fd = open(" ecu_simulator/interface/ms/test.json","w", encoding="utf-8") 
        b = json.dumps(res[0], ensure_ascii=False)
        fd.write(b)
        fd.close()
        for i in range(len(res)) :
            case_id.append({'id': res[i].get('id'), 'jama_id': res[i].get('customNum'), 'nodeid': res[i].get('nodeId'), 'updatetime': res[i].get('updateTime')})
            for j in range(len(res[i].get("fields"))):
                if res[i].get("fields")[j].get("id") == "1ae81def-d0bd-4144-91b5-e52fff4d262c":
                    jama_id_mapping.append({"id": res[i].get("num"), "jamaid": res[i].get("fields")[j].get("value").replace("\"", "")})
        jama_id_mapping = [i for i in jama_id_mapping if "MSO" not in i.get("jamaid")]
        norepeat_jama_id_mapping = []
        jamaid = []
        for j in range(len(jama_id_mapping)):
            jamaid.append(jama_id_mapping[j].get("jamaid"))
        peat_jamaid = [i for i in jamaid if jamaid.count(i) == 1]
        for z in range(len(peat_jamaid)):
            for j in range(len(jama_id_mapping)):
                if jama_id_mapping[j].get("jamaid") == peat_jamaid[z]:
                    norepeat_jama_id_mapping.append({"id": jama_id_mapping[j].get("id"), "jamaid": peat_jamaid[z]})
        for j in range(len(jama_id_mapping)):
            if jama_id_mapping[j].get("jamaid") == '':
                norepeat_jama_id_mapping.append(jama_id_mapping[j])
        repeat_jama_id_mapping = [i for i in jama_id_mapping if i not in norepeat_jama_id_mapping]

        return case_id, norepeat_jama_id_mapping, repeat_jama_id_mapping
    
    
    def get_zero_time(self):
        from time import mktime
        from datetime import datetime, timedelta
        today = datetime.now().strftime('%Y-%m-%d')
        today_struct = time.strptime(today, '%Y-%m-%d')
        today_stamp = int(time.mktime(today_struct))
        today_zero = today_stamp - today_struct.tm_hour * 3600 - today_struct.tm_min * 60 - today_struct.tm_sec
        return today_zero*1000


    def upload_tcam(self):
        # TCAM测试用例
        global failed1
        failed1 = []
        logger.info(f"开始导入TCAM的测试用例")
        data = self.get_cases([], "f1d8bad3-4417-4e02-8b8d-28e583cd2e80")
        logger.info(f"TCAM的测试用例一共{len(data)}条!!")
        for j in range(len(data)):
            if data[j].get('updatetime') >= self.zero_time:
                logger.info(f"TCAM的测试用例jama_id:{data[j].get('jama_id')}有更新需要上传!!")
                i = 1
                while i <= 5:
                    logger.info(f"TCAM的测试用例jama_id:{data[j].get('jama_id')}第{i}次上传!!")
                    tcam = self.client.set_testcase_ms_to_jama(nodeIds=[data[j].get('nodeid')], Ids=[data[j].get('id')])
                    if tcam:
                        logger.info(f"TCAM的测试用例jama_id:{data[j].get('jama_id')}上传成功!!")
                        break
                    else:
                        logger.error(f"TCAM的测试用例jama_id:{data[j].get('jama_id')}第{i}次上传失败, 等待1s后请重试!!")
                        i += 1
                        time.sleep(1)
                        if i == 6:
                            failed1.append(f"{data[j].get('jama_id')}")
            else:
                continue

        if len(failed1) == 0:
            logger.error(f"TCAM的测试用例全部上传成功")
        else:
            logger.error(f"TCAM上传失败的测试用例id:\n{failed1}")  

                
    def upload_bgm(self):
        # BGM测试用例
        bgm_projectId = "6e14e1c5-aa15-4a44-b392-bdac2a4cc131"
        global failed2
        failed2 = []
        logger.info(f"开始导入BGM的测试用例")
        data = self.get_cases([], bgm_projectId)
        logger.info(f"BGM的测试用例一共{len(data)}条!!")
        for j in range(len(data)):
            if data[j].get('updatetime') >= self.zero_time:
                logger.info(f"BGM的测试用例jama_id:{data[j].get('jama_id')}有更新需要上传!!")
                i = 1
                while i <= 5:
                    logger.info(f"BGM的测试用例jama_id:{data[j].get('jama_id')}第{i}次上传!!")
                    bgm = self.client.set_testcase_ms_to_jama(nodeIds=[data[j].get('nodeid')], Ids=[data[j].get('id')])
                    if bgm:
                        logger.info(f"BGM的测试用例jama_id:{data[j].get('jama_id')}上传成功!!")
                        break
                    else:
                        logger.error(f"BGM的测试用例jama_id:{data[j].get('jama_id')}第{i}次上传失败, 等待1s后请重试!!")
                        i += 1
                        time.sleep(1)
                        if i == 6:
                            failed2.append(f"{data[j].get('jama_id')}")
            else:
                continue

        if len(failed2) == 0:
            logger.error(f"BGM的测试用例全部上传成功")
        else:
            logger.error(f"BGM上传失败的测试用例id:\n{failed2}") 

    
    def upload_s2s(self):
        failed = []
        with open(os.path.join(project_root, " ecu_simulator/interface/ms/s2s.json"), "r", encoding="utf-8") as fd:
            s2s_nodeIds = json.loads(fd.read())

        for k, w in s2s_nodeIds.items():
            logger.info(f"开始导入S2S的{k}模块的用例")
            i = 1
            data = self.get_cases(w)
            logger.info(f"{k}模块一共{len(data)}页需要上传!!")
            for j in range(len(data)):
                while i <= 5:
                    logger.info(f"{k}模块第{j+1}页第{i}次上传!!")
                    tcam = self.client.set_testcase_ms_to_jama(nodeIds=w, Ids=data[j])
                    if tcam:
                        logger.info(f"{k}模块第{j+1}页上传成功!!")
                        break
                    else:
                        logger.error(f"{k}模块第{j+1}页第{i}次上传失败, 等待5s后请重试!!")
                        i += 1
                        time.sleep(5)
                        if i == 6:
                            failed.append(f"{k}模块第{j+1}页上传失败")

        if len(failed) == 0:
            logger.error(f"S2S用例全部上传成功")
        else:
            logger.error(f"S2S用例上传失败的模块:\n{failed}")


    def upload_soa(self):
        global failed3
        failed3 = []
        logger.info(f"开始导入SOA的测试用例")
        data = self.get_cases([], "52c062de-78ea-41b4-8307-bed834cef1a7")
        logger.info(f"SOA的测试用例一共{len(data)}条!!")
        for j in range(len(data)):
            if data[j].get('updatetime') >= self.zero_time:
                logger.info(f"SOA的测试用例jama_id:{data[j].get('jama_id')}有更新需要上传!!")
                i = 1
                while i <= 5:
                    logger.info(f"SOA的测试用例jama_id:{data[j].get('jama_id')}第{i}次上传!!")
                    soa = self.client.set_testcase_ms_to_jama(nodeIds=[data[j].get('nodeid')], Ids=[data[j].get('id')])
                    if soa:
                        logger.info(f"SOA的测试用例jama_id:{data[j].get('jama_id')}上传成功!!")
                        break
                    else:
                        logger.error(f"SOA的测试用例jama_id:{data[j].get('jama_id')}第{i}次上传失败, 等待1s后请重试!!")
                        i += 1
                        time.sleep(1)
                        if i == 6:
                            failed3.append(f"{data[j].get('jama_id')}")
            else:
                continue

        if len(failed3) == 0:
            logger.error(f"SOA的测试用例全部上传成功")
        else:
            logger.error(f"SOA上传失败的测试用例id:\n{failed3}")  



if __name__ == '__main__':
    # 导出tcam、bgm和soa项目的所有测试用例到Jama
    up = Upload()
    logger.info("==" * 50)
    try:
        up.upload_tcam()
    except:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/ms/ms_to_jama.py")
        up.upload_tcam()
    logger.info("==" * 50)
    try:
        up.upload_bgm()
    except:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/ms/ms_to_jama.py")
        up.upload_bgm()
    logger.info("==" * 50)
    try:
        up.upload_soa()
    except:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/ms/ms_to_jama.py")
        up.upload_soa()
    logger.info("==" * 50)
    assert len(failed1) == 0
    assert len(failed2) == 0
    assert len(failed3) == 0

