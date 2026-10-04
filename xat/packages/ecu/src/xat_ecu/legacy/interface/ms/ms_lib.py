import json
import os
import sys
import time
from time import localtime, strftime, sleep

from xat_ecu.legacy.interface.feishu.feishu_api import feishu_api
from xat_ecu.legacy.interface.ms.send_result_to_soa_platform import (
    CaseResult,
    send_result_to_soa_platform,
)

current_path = os.path.dirname(os.path.realpath(__file__))
from xat_ecu.legacy.common.constant import MS_CONSTANT
from xat_ecu.legacy.common.logger import logger, Logger
import requests
import base64
import traceback

TCAM_service = ["GNSSService", "CallService", "V2TRoutingService", "update_agent_service", "RtcAlarmService",
                "NetWorkService", "RemoteCtrlService", "V2TRoutingForwarder"]
CDC_service = ['avm_service', 'account_service']
ACU_service = ['ACCService', 'ACUFaultInfoService']
ms_project_dict = {"BGM": "1fbbeb47-6cc7-48bd-aafc-24349853e9d8",
                    "TCAM": "225ebd89-8c9c-48dd-a3d8-739e52ee76e2",
                    "SOA服务": "52c062de-78ea-41b4-8307-bed834cef1a7",
                    "CDC_MCU": "c8fc5cb7-5a55-41a8-8f04-e43164e3878a"}

def get_ecu_domain_name(service_name):
    if service_name in TCAM_service:
        return "TCAM"
    elif service_name in CDC_service:
        return "CDC"
    elif service_name in ACU_service:
        return "ACU"
    else:
        return "BGM"


class meterSphere_client:
    def __init__(
            self,
            username=MS_CONSTANT.MS_USERNAME,
            password=MS_CONSTANT.MS_PASSWORD,
            server_name='https://ms.jiduprod.com',
    ):
        self.username = base64.b64decode(username.encode()).decode()
        self.password = base64.b64decode(password.encode()).decode()
        self.server_name = server_name
        self.csrfToken = ''
        self.lastWorkspaceId = ''
        self.lastProjectId = ''
        self.Cookie = ''
        self.signin_flag = None
        try:
            self.signin()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/ms/ms_lib.py")
            logger.error("登入 MS 失败: {}".format(e))

    def signin(self, path="/ldap/signin"):
        """
        登录 ms 系统，获取 response Headers信息
        """
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            'Content-Type': 'application/json',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
        }
        data = {
            'username': self.username,
            'password': self.password,
            'authenticate': 'LOCAL',
        }
        url = self.server_name + path
        retry_num = 10
        while retry_num > 0 and self.signin_flag is None:
            retry_num -= 1
            try:
                response = requests.post(url, json.dumps(data), headers=headers, timeout=5)
                resp_body = json.loads(str(response.content, 'utf-8'))
                resp_header = response.headers
                list_cookie = resp_header.get("X-AUTH-TOKEN")

                self.csrfToken = resp_body.get("data").get("csrfToken")
                self.lastWorkspaceId = resp_body.get("data").get("lastWorkspaceId")
                self.lastProjectId = resp_body.get("data").get("lastProjectId")
                self.Cookie = list_cookie.strip()
                self.signin_flag = True
                logger.info("MS登录成功")
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/ms/ms_lib.py")
                details = traceback.format_exc()
                data = {"异常类型": type(e).__name__, "执行序号": 5 - retry_num, "异常堆栈信息": details}
                if data["执行序号"] == 5:
                    add_ms_login_fail(data)
                logger.info(f"MS登录接口第{retry_num}次请求异常:{type(e).__name__}, "
                            f"异常堆栈：{details}")
                sleep(30)

    def get_testcases_in_testPlan(self, planId, projectId='', nodePath=None, retry_num=5):
        """
        执行结果可选值：Pass、Failure、Blocking、Skip
        返回值类型：list，包含测试计划下的测试用例的 详细信息
        """
        if self.signin_flag:
            headers = {
                'CSRF-TOKEN': self.csrfToken,
                'PROJECT': self.lastProjectId,
                'WORKSPACE': self.lastWorkspaceId,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                'Accept-Encoding': 'gzip, deflate',
                'X-AUTH-TOKEN': self.Cookie,
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Content-Type': 'application/json',
            }
            if not projectId:
                projectId = self.lastProjectId
            data = {
                "components": [],
                "planId": planId,
                "projectId": projectId,
                "selectAll": False,
            }
            i = 1
            result = []
            tem_data = None
            while True:
                path = f"/track/test/plan/case/list/{i}/100"
                url = self.server_name + path
                resp_body = None
                retry_num = 10
                while retry_num > 0:
                    retry_num -= 1
                    try:
                        response = requests.post(
                            url, json.dumps(data), headers=headers, timeout=30
                        )
                        resp_body = json.loads(str(response.content, 'utf-8'))
                        if resp_body['success']:
                            break
                        else:
                            data = {"planId": planId, "url": url, "异常类型": resp_body['message'],
                                    "执行序号": 10 - retry_num}
                            logger.info(f"MS获取测试计划中的用例接口第{retry_num}次请求失败，{str(response.content, 'utf-8')}")
                            if data["执行序号"] == 10:
                                add_exception_get_testcase_in_testplan(data)
                            sleep(5)
                    except Exception as e:  # 接口请求超时、返回结果转json异常、返回结果转JSON为None，则添加飞书异常表
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/ms/ms_lib.py")
                        details = traceback.format_exc()
                        data = {"planId": planId, "url": url, "异常类型": type(e).__name__, "执行序号": 10 - retry_num,
                                "异常堆栈信息": details}
                        if data["执行序号"] == 10:
                            add_exception_get_testcase_in_testplan(data)
                        logger.info(f"MS获取测试计划中的用例接口第{retry_num}次请求异常:{type(e).__name__}, "
                                    f"异常堆栈：{details}")
                        sleep(5)

                if resp_body['success']:
                    if len(resp_body['data']["listObject"]) == 100:
                        if tem_data == resp_body['data']["listObject"]:
                            # case数量恰好为 100 整数是，如 6700， 会一直返回最后一页的内容
                            break
                        else:
                            tem_data = resp_body['data']["listObject"]
                            result.extend(tem_data)
                        i = i + 1
                    elif len(resp_body['data']["listObject"]) > 0:
                        result.extend(resp_body['data']["listObject"])
                        break
                    else:
                        break
                else:
                    break
            logger.info("获取到的用例条数：{}".format(len(result)))
            new_result = []
            if nodePath:
                for current in result:
                    logger.info(current["nodePath"])
                    if nodePath in current["nodePath"]:
                        new_result.append(current)
            else:
                new_result = result

            return new_result

    def get_testplan_list_in_project(self, projectId, max_retry_num=10, retry_period=20):
        """
        获取MS上对应项目的测试计划信息

        :param projectId: 项目ID
        :param max_retry_num : 最大尝试重试次数
        :param retry_period: 失败重试前暂停的秒数
        """
        if self.signin_flag:
            headers = {
                'CSRF-TOKEN': self.csrfToken,
                'PROJECT': projectId,
                'WORKSPACE': self.lastWorkspaceId,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                'Accept-Encoding': 'gzip, deflate',
                'X-AUTH-TOKEN': self.Cookie,
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Content-Type': 'application/json',
            }

            data = {"components": [{"key": "name", "name": "MsTableSearchInput", "label": "commons.name",
                                    "operator": {"value": "like", "options": [
                                        {"label": "commons.adv_search.operators.like", "value": "like"},
                                        {"label": "commons.adv_search.operators.not_like", "value": "not like"}]}},
                                   {"key": "updateTime", "name": "MsTableSearchDateTimePicker",
                                    "label": "commons.update_time", "operator": {"options": [
                                       {"label": "commons.adv_search.operators.between", "value": "between"},
                                       {"label": "commons.adv_search.operators.gt", "value": "gt"},
                                       {"label": "commons.adv_search.operators.lt", "value": "lt"}]}},
                                   {"key": "createTime", "name": "MsTableSearchDateTimePicker",
                                    "label": "commons.create_time", "operator": {"options": [
                                       {"label": "commons.adv_search.operators.between", "value": "between"},
                                       {"label": "commons.adv_search.operators.gt", "value": "gt"},
                                       {"label": "commons.adv_search.operators.lt", "value": "lt"}]}},
                                   {"key": "principal", "name": "MsTableSearchSelect",
                                    "label": "test_track.plan.plan_principal", "operator": {
                                       "options": [{"label": "commons.adv_search.operators.in", "value": "in"},
                                                   {"label": "commons.adv_search.operators.not_in", "value": "not in"},
                                                   {"label": "commons.adv_search.operators.current_user",
                                                    "value": "current user"}]},
                                    "options": {"url": "/user/project/member/list", "labelKey": "name",
                                                "valueKey": "id"}, "props": {"multiple": True}},
                                   {"key": "status", "name": "MsTableSearchSelect",
                                    "label": "test_track.plan.plan_status", "operator": {
                                       "options": [{"label": "commons.adv_search.operators.in", "value": "in"},
                                                   {"label": "commons.adv_search.operators.not_in",
                                                    "value": "not in"}]},
                                    "options": [{"label": "test_track.plan.plan_status_prepare", "value": "Prepare"},
                                                {"label": "test_track.plan.plan_status_running", "value": "Underway"},
                                                {"label": "test_track.plan.plan_status_completed",
                                                 "value": "Completed"},
                                                {"label": "test_track.plan.plan_status_finished", "value": "Finished"},
                                                {"label": "test_track.plan.plan_status_terminated",
                                                 "value": "Terminated"},
                                                {"label": "test_track.plan.plan_status_archived", "value": "Archived"}],
                                    "props": {"multiple": True}}, {"key": "stage", "name": "MsTableSearchSelect",
                                                                   "label": "test_track.plan.plan_stage", "operator": {
                        "options": [{"label": "commons.adv_search.operators.in", "value": "in"},
                                    {"label": "commons.adv_search.operators.not_in", "value": "not in"}]},
                                                                   "options": [{"label": "Smoke", "value": "Smoke"},
                                                                               {"label": "Sanity", "value": "Sanity"},
                                                                               {"label": "Full", "value": "Full"},
                                                                               {"label": "Checklist",
                                                                                "value": "Checklist"},
                                                                               {"label": "Customized",
                                                                                "value": "Customized"}],
                                                                   "props": {"multiple": True}},
                                   {"key": "tags", "name": "MsTableSearchInputTag", "label": "commons.tag",
                                    "operator": {"value": "like", "options": [
                                        {"label": "commons.adv_search.operators.like", "value": "like"},
                                        {"label": "commons.adv_search.operators.not_like", "value": "not like"}]}},
                                   {"key": "followPeople", "name": "MsTableSearchSelect",
                                    "label": "commons.follow_people", "operator": {
                                       "options": [{"label": "commons.adv_search.operators.in", "value": "in"},
                                                   {"label": "commons.adv_search.operators.current_user",
                                                    "value": "current user"}]},
                                    "options": {"url": "/user/ws/current/member/list", "labelKey": "name",
                                                "valueKey": "id"}, "props": {"multiple": True}},
                                   {"key": "testRound", "name": "MsTableSearchInputNumber",
                                    "label": "test_track.plan.test_round", "operator": {"value": "eq", "options": [
                                       {"label": "commons.adv_search.operators.gt", "value": "gt"},
                                       {"label": "commons.adv_search.operators.ge", "value": "ge"},
                                       {"label": "commons.adv_search.operators.lt", "value": "lt"},
                                       {"label": "commons.adv_search.operators.le", "value": "le"},
                                       {"label": "commons.adv_search.operators.equals", "value": "eq"}]}},
                                   {"key": "actualStartTime", "name": "MsTableSearchDateTimePicker",
                                    "label": "test_track.plan.actual_start_time", "operator": {"options": [
                                       {"label": "commons.adv_search.operators.between", "value": "between"},
                                       {"label": "commons.adv_search.operators.gt", "value": "gt"},
                                       {"label": "commons.adv_search.operators.ge", "value": "ge"},
                                       {"label": "commons.adv_search.operators.lt", "value": "lt"},
                                       {"label": "commons.adv_search.operators.le", "value": "le"}]}},
                                   {"key": "actualEndTime", "name": "MsTableSearchDateTimePicker",
                                    "label": "test_track.plan.actual_end_time", "operator": {"options": [
                                       {"label": "commons.adv_search.operators.between", "value": "between"},
                                       {"label": "commons.adv_search.operators.gt", "value": "gt"},
                                       {"label": "commons.adv_search.operators.ge", "value": "ge"},
                                       {"label": "commons.adv_search.operators.lt", "value": "lt"},
                                       {"label": "commons.adv_search.operators.le", "value": "le"}]}},
                                   {"key": "planStartTime", "name": "MsTableSearchDateTimePicker",
                                    "label": "test_track.plan.planned_start_time", "operator": {"options": [
                                       {"label": "commons.adv_search.operators.between", "value": "between"},
                                       {"label": "commons.adv_search.operators.gt", "value": "gt"},
                                       {"label": "commons.adv_search.operators.ge", "value": "ge"},
                                       {"label": "commons.adv_search.operators.lt", "value": "lt"},
                                       {"label": "commons.adv_search.operators.le", "value": "le"}]}},
                                   {"key": "planEndTime", "name": "MsTableSearchDateTimePicker",
                                    "label": "test_track.plan.planned_end_time", "operator": {"options": [
                                       {"label": "commons.adv_search.operators.between", "value": "between"},
                                       {"label": "commons.adv_search.operators.gt", "value": "gt"},
                                       {"label": "commons.adv_search.operators.ge", "value": "ge"},
                                       {"label": "commons.adv_search.operators.lt", "value": "lt"},
                                       {"label": "commons.adv_search.operators.le", "value": "le"}]}}], "orders": [],
                    "projectId": projectId}
            result = []
            itemCount = 0  # 测试计划总数
            i = 0
            retry_num = 0
            while retry_num <= max_retry_num:
                retry_num += 1
                try:
                    while True:
                        i += 1
                        path = f"/track/test/plan/list/{i}/50"
                        url = self.server_name + path
                        response = requests.post(
                            url, json.dumps(data), headers=headers, timeout=30
                        )
                        resp_body = json.loads(str(response.content, 'utf-8'))
                        testplan_list = []
                        for item in resp_body['data']["listObject"]:
                            plan_id = item.get("id")  # 测试计划ID
                            plan_name = item.get("name", "")  # 测试计划名称
                            test_plan = {"plan_id": plan_id, "plan_name": plan_name}
                            testplan_list.append(test_plan)

                        if itemCount == 0:  # 仅赋值1次
                            itemCount = resp_body['data']['itemCount']
                        if len(resp_body['data']["listObject"]) > 0:
                            result.extend(testplan_list)
                        if len(resp_body['data']["listObject"]) < 50:
                            break
                        if len(result) >= itemCount:
                            break
                        time.sleep(0.1)
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/ms/ms_lib.py")
                    exception_detail = traceback.format_exc()
                    if retry_num == max_retry_num:
                        logger.error(f"获取项目的测试计划执行失败：{exception_detail}")
                    time.sleep(retry_period)
                else:
                    break

            logger.info(f"      预期获取测试计划总数：{itemCount}")
            logger.info(f"      实际获取计划总数：{len(result)}")
            return result

    def set_testcase_status_in_testPlan(
            self, Id, nodeId, status, case_id, projectId='', path="/track/test/plan/case/edit", retry_num=5
    ):
        """
        执行结果(status)可选值：Pass、Failure、Blocking、Skip
        根据测试用例信息的 Id、nodeId、projectId 三个字段更新 testcase run result
        """
        if self.signin_flag:
            headers = {
                'CSRF-TOKEN': self.csrfToken,
                'PROJECT': self.lastProjectId,
                'WORKSPACE': self.lastWorkspaceId,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                'Accept-Encoding': 'gzip, deflate',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'X-AUTH-TOKEN': self.Cookie,
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Content-Type': 'application/json',
            }
            if not projectId:
                projectId = self.lastProjectId
            data = {
                "actualResult": "",
                "buildNumber": "[]",
                "caseId": case_id,
                "demandId": "",
                "fileIds": [],
                "id": Id,
                "status": status,
                "results": "[{}]",
                "projectId": projectId,
                "resultDescribe": "",
                "results": "[{},{}]",
                "nodeId": nodeId,
                "buildNumber": "[]",
                "updatedFileList": [],
                "actualResult": "",
            }
            sync_ms_result = False
            url = self.server_name + path
            while retry_num > 0:
                retry_num -= 1
                try:
                    response = requests.post(url, json.dumps(data), headers=headers, timeout=30)
                    resp_body = json.loads(str(response.content, 'utf-8'))
                    logger.info(f"回填MS返回结果：{str(response.content, 'utf-8')}")
                    if resp_body and resp_body.get('success', "False") is True:
                        logger.info("MS回填成功!!")
                        sync_ms_result = True
                        break
                    else:
                        logger.warning(f"MS回填失败，1秒后重新尝试回填")
                        exception_data = {"Id": Id, "nodeId": nodeId, "status": status, "case_id": case_id,
                                          "retry_num": 5 - retry_num, "异常类型": str(response.content, 'utf-8')}
                        add_exception_set_testcase_result_in_testplan(exception_data)
                        time.sleep(5)
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/ms/ms_lib.py")
                    exception_detail = traceback.format_exc()
                    if retry_num == 0:
                        exception_data = {"Id": Id, "nodeId": nodeId, "status": status, "case_id": case_id,
                                          "retry_num": 5 - retry_num, "异常类型": type(e).__name__, "异常堆栈": exception_detail}
                        if exception_data["retry_num"] == 5:  # 只保存获取5次仍失败的记录
                            add_exception_set_testcase_result_in_testplan(exception_data)
                    logger.warning(f"MS接口响应超时或者返回结果异常：{e.__str__()}")
                    logger.warning(f"异常堆栈：{exception_detail}")
                    logger.warning(f"MS回填失败，1秒后重新尝试回填")
                    time.sleep(5)
            return sync_ms_result

    def set_testcase_status_in_testPlan_new(
            self, planId, testcaseId, status, deviceInfo, buildNumber, resultDescribe,
            path="/track/test/plan/case/third/update"
    ):
        """
        执行结果(status)可选值：Pass、Failure、Blocking、Skip
        根据测试用例信息的 Id、nodeId、projectId 三个字段更新 testcase run result
        """
        if self.signin_flag:
            headers = {
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Content-Type': 'application/json',
            }
            data = {
                "planId": planId,
                "testCaseIds": [f"{testcaseId}"],
                "result": status,
                "executor": "ldap_soa_jama",
                "comment": "",
                "buildNumber": [f"{buildNumber}"],
                "jiraIssue": [""],
                "resultDescribe": f"{resultDescribe}",
                "deviceInfo": deviceInfo
            }
            url = self.server_name + path
            response = requests.post(url, json.dumps(data), headers=headers, timeout=30)
            resp_body = json.loads(str(response.content, 'utf-8'))
            logger.info("======new======")
            logger.info(str(response.content, 'utf-8'))
            if resp_body and resp_body.get('success', "False"):
                logger.info("Update testcase status in test_plan success!!")

    def get_testcase_jira_id_in_testPlan(
            self, case_id_in_testplan, path="/issues/get/case/PLAN_FUNCTIONAL/"
    ):
        """
        执行结果(status)可选值：Pass、Failure、Blocking、Skip
        根据测试用例信息的 Id、nodeId、projectId 三个字段更新 testcase run result
        """
        if self.signin_flag:
            headers = {
                'CSRF-TOKEN': self.csrfToken,
                'PROJECT': self.lastProjectId,
                'WORKSPACE': self.lastWorkspaceId,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                'Accept-Encoding': 'gzip, deflate',
                'X-AUTH-TOKEN': self.Cookie,
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Content-Type': 'application/json',
            }

            url = self.server_name + path + case_id_in_testplan
            response = requests.get(url, headers=headers)
            resp_body = json.loads(str(response.content, 'utf-8'))
            if resp_body and resp_body.get('success', "False"):
                if len(resp_body.get('data')) > 0:
                    jira_id_0 = resp_body.get('data')[0].get('platformId')
                    return jira_id_0
            else:
                return "无"

    def get_fail_testcase_result_info_in_testPlan(
            self, case_of_id_in_testplan, path="/track/test/plan/case/get/"
    ):
        """
        获取测试计划中失败用例的resultDescribe（结果说明）、jiraIssue（Jira缺陷）
        """
        if self.signin_flag:
            headers = {
                'CSRF-TOKEN': self.csrfToken,
                'PROJECT': self.lastProjectId,
                'WORKSPACE': self.lastWorkspaceId,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                'Accept-Encoding': 'gzip, deflate',
                'X-AUTH-TOKEN': self.Cookie,
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Content-Type': 'application/json',
            }

            url = self.server_name + path + case_of_id_in_testplan
            response = requests.get(url, headers=headers)
            resp_body = json.loads(str(response.content, 'utf-8'))
            if resp_body:
                if resp_body.get('data'):
                    id = resp_body.get('data').get('customNum')
                    resultDescribe = resp_body.get('data').get('resultDescribe', "MS上无结果说明")
                    jiraIssue = resp_body.get('data').get('jiraIssue', "MS上无Jira缺陷")
                    if resultDescribe is None and jiraIssue is None:  # 如果两个字段都为空
                        return None
                    else:
                        return {id: {'resultDescribe': resultDescribe, 'jiraIssue': jiraIssue}}
                else:
                    return None
            else:
                return None

    def get_customnum_mappings_from_planid(self, planId):
        """
        planId: str  such as "ccbfb89c-68bc-4da2-bc76-548794d5fce3"
        返回值类型: dict {customnum : (id, nodeId)}
        """
        if self.signin_flag:
            if planId:
                res = self.get_testcases_in_testPlan(planId)
                jama_id_mapping = {}  # 兼容存量测试用例的jama_id
                customnum_mappings = {}
                fail_case_result_description = {}
                if res:
                    for data in res:
                        customNum = data.get("customNum")
                        ms_id = data.get("id")
                        nodeId = data.get("nodeId")
                        status = data.get("status")  # cases 执行状态
                        caseId = data.get("caseId")
                        priority = data.get("priority")
                        nodePath = data.get("nodePath")
                        maintainer = data.get("maintainer")
                        if status == 'Failure':  # 获取失败用例的结果说明和jira缺陷
                            case_fail_info = self.get_fail_testcase_result_info_in_testPlan(ms_id)
                            if case_fail_info is not None:
                                fail_case_result_description.update(case_fail_info)
                        if data.get("fields"):
                            for field in data.get("fields"):
                                if field["id"] == "1ae81def-d0bd-4144-91b5-e52fff4d262c":
                                    jama_id_mapping[(field["value"].replace("\"", ""))] = customNum
                                    customnum_mappings[field["value"].replace("\"", "")] = (
                                        ms_id, nodeId, status, caseId, priority, nodePath)
                        else:
                            continue
                        customnum_mappings[customNum] = (ms_id, nodeId, status, caseId, priority, nodePath, maintainer)
                else:
                    logger.error("从测试计划中获取cases错误")
                return customnum_mappings, jama_id_mapping, fail_case_result_description

    def get_report_info_from_planid(self, planId):
        """
        :param:  planId: str  such as "ccbfb89c-68bc-4da2-bc76-548794d5fce3"
        返回值类型: dict  such as {"数字安全_SOA服务鉴权" : {"一级模块": ["架构基础"], "status": ["Pass"], "Automation": ["Ready"] }
        """
        if self.signin_flag:
            if planId:
                res = self.get_testcases_in_testPlan(planId)

                report_info = {}
                Automation_not_match_list = []
                if res:
                    for data in res:
                        customNum = data.get("customNum")

                        nodePath = data.get("nodePath")
                        nodePath_list = nodePath.split("/")
                        first_mod = nodePath_list[1]
                        if len(nodePath_list) > 3:
                            sec_title = nodePath_list[2] + "_" + nodePath_list[3]
                        else:
                            sec_title = nodePath_list[-1]

                        if sec_title in report_info:
                            case_info = report_info[sec_title]
                        else:
                            report_info[sec_title] = {}
                            case_info = report_info[sec_title]
                            case_info["一级模块"] = []
                            case_info["status"] = []
                            case_info["Automation"] = []

                        case_info["一级模块"].append(first_mod)
                        case_info["status"].append(data.get("status"))

                        customFields = data.get("customFields")  # customFields str
                        if customFields:  # 有未 None的情况
                            customFields = json.loads(
                                customFields
                            )  # customFields 转成 dict
                        else:
                            customFields = {}
                            logger.warning(f"{customNum} has not customFields")
                        for customField in customFields:
                            if customField.get("name") == "Automation":
                                case_info["Automation"].append(customField.get("value"))

                                # "96ae3bb3" ---- Ready
                                # "06ca513d" ---- To Do
                                if data.get("status") in [
                                    "Pass",
                                    "Failure",
                                    "Blocking",
                                ] and customField.get("value") not in [
                                    "Ready",
                                    "96ae3bb3",
                                    "To Do",
                                    "06ca513d",
                                ]:
                                    Automation_not_match_list.append(customNum)
                                break

                        # ms_id = data.get("id")
                        # nodeId = data.get("nodeId")
                else:
                    logger.error("从测试计划中获取cases错误")

                logger.info(
                    "Automation not match list : {}".format(Automation_not_match_list)
                )
                return report_info
            else:
                logger.info("未登入MS 或 登入MS失败")

    def get_soa_platform_mappings_from_plan_id(self, planId, nodePath=None):
        """
        planId: str  such as "ccbfb89c-68bc-4da2-bc76-548794d5fce3"
        返回值类型: dict {customnum : (service_name, interface_name, function_name, jama_id_0, check_point, status)}
        同步“SOA 测试” 项目下对应测试计划的测试结果至SOA测试平台
        """
        if self.signin_flag:
            if planId:
                res_0 = self.get_testcases_in_testPlan(planId, '', nodePath)
                custom_mappings_0 = {}
                if res_0:
                    for data in res_0:
                        # customNum = data.get("customNum")
                        # jama_id_0 = data.get("num")  # case_id
                        case_id_uniq = data.get("num")  # case_id
                        check_point_0 = data.get("name")  # 检查点
                        service_name_0 = data.get("nodePath").split("/")[-1]
                        nodePath_list = data.get("nodePath").split("/")
                        for node in nodePath_list:
                            if "Service" in node and "_" not in node:
                                service_name_0 = node
                            elif "Service" in node and "_" in node:
                                inter_nodes = node.split("_")
                                for inter_node in inter_nodes:
                                    if "Service" in inter_node:
                                        service_name_0 = inter_node
                        status_0 = ""
                        jira_id = ""
                        if data.get("status") == "Pass":  # status
                            status_0 = "PASS"
                        elif data.get("status") == "Prepare":
                            status_0 = "NOT TEST"
                        elif data.get("status") == "Failure":
                            status_0 = "FAIL"
                            if data.get("issuesCount") != "0":  # 关联缺陷数非0， 根据id获取缺陷ID
                                fail_info = self.get_fail_testcase_result_info_in_testPlan(data.get("id"))

                                if fail_info is not None:
                                    jira_id = fail_info.get(str(data.get("num"))).get("jiraIssue")
                                else:
                                    logger.info(f"失败用例{data.get('num')}没有填写缺陷ID！")
                        else:
                            continue
                        interface_name_0 = ""
                        function_name_0 = ""
                        ss = data.get("fields")
                        for obj in ss:
                            if obj["id"] is not None:
                                if obj["id"] == "3ec58302-2c8c-4ef0-a73d-3951be7b3045":
                                    function_name_0 = obj["value"].strip('"')
                            if obj["id"] is not None:
                                if obj["id"] == "f995823c-c8c0-4aed-b4da-f736f471fe03":
                                    interface_name_0 = obj["value"].strip('"')
                        if jira_id is None:
                            jira_id = ""
                        ts = data.get('updateTime') / 1000
                        updateTime = strftime("%Y-%m-%d %H:%M:%S", localtime(ts))
                        custom_mappings_0[case_id_uniq] = (
                            service_name_0,
                            interface_name_0,
                            function_name_0,
                            case_id_uniq,
                            check_point_0,
                            status_0,
                            jira_id,
                            updateTime
                        )
                else:
                    logger.error("从测试计划中获取cases错误")
                return custom_mappings_0

    def sync_data_from_MS_to_soa_test_db(self, plan_id, bgmVersion=None, tcamVersion=None, cdcVersion=None,
                                         acuVersion=None, nodePath=None):
        """
        plan_id: MS上的测试计划ID
        bgmVersion：BGM的版本号
        tcamVersion：TCAM的版本号
        """
        # plan = "1bd1ba6f-f9fd-42ea-a45d-93ab457e4d0b"
        res = self.get_soa_platform_mappings_from_plan_id(plan_id, nodePath)
        logger.info(f"开始同步{len(res)}条数据")
        i = 0
        case_id_list = []
        for testcase in res:  # testcase为主键key
            case_id = testcase
            (
                service_name,
                interface_name,
                function_name,
                jama_id,
                check_point,
                result,
                jira_id,
                updateTime
            ) = res[case_id]

            if service_name in TCAM_service:
                ecu_version = tcamVersion
            elif service_name in CDC_service:
                ecu_version = cdcVersion
            elif service_name in ACU_service:
                ecu_version = acuVersion
            else:
                ecu_version = bgmVersion

            case_result = CaseResult(
                bgmVersion=ecu_version,
                jamaId=case_id,
                interfaceName=interface_name,
                serviceName=service_name,
                functionName=function_name,
                functionType="method",
                functionParameter="",
                expectResult="",
                realResult="",
                autoCaseResult=result,
                testcaseId=case_id,
                testcaseDescription=check_point,
                jiraLink=jira_id,
                jidlVersion='',
                updateTime=updateTime,
                domain=get_ecu_domain_name(service_name)
            )
            send_result_to_soa_platform(case_result)
            if not case_id:
                logger.info(f"case_id 为空，{check_point}")
            if case_id in case_id_list:
                logger.info(f"{case_id}已存在！！！")
            else:
                case_id_list.append(case_id)
            i = i + 1
            if i % 200 == 0:
                logger.info(f"正在同步第{i}条数据, 列表长度{len(case_id_list)}")

        logger.info(f"同步结束，共同步数据{i}条！！")

    def get_projectname_by_testPlan(self, planId):
        """
        根据测试计划ID，获取对应的项目名称
        """
        if self.signin_flag:
            headers = {
                'CSRF-TOKEN': self.csrfToken,
                'PROJECT': self.lastProjectId,
                'WORKSPACE': self.lastWorkspaceId,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                'Accept-Encoding': 'gzip, deflate',
                'X-AUTH-TOKEN': self.Cookie,
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Content-Type': 'application/json',
            }
            data = {
                "planId": planId,
                "projectId": self.lastProjectId,
                "selectAll": False,
            }

            path = f"/track/test/plan/case/list/1/100"
            url = self.server_name + path
            response = requests.post(
                url, json.dumps(data), headers=headers, timeout=30
            )
            resp_body = json.loads(str(response.content, 'utf-8'))
            for item in resp_body['data']["listObject"]:
                if "projectName" in item:
                    logger.info(f"获取到的项目名称:{item['projectName']}")
                    return item["projectName"]

    def get_testcases_in_project(self, projectId, query_condition=None):
        """
        同步MS上对应项目的测试用例信息

        :param projectId: 待同步项目的项目的项目ID
        :param query_condition: 默认为None，查询条件
        """

        if self.signin_flag:
            headers = {
                'CSRF-TOKEN': self.csrfToken,
                'PROJECT': projectId,
                'WORKSPACE': self.lastWorkspaceId,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                'Accept-Encoding': 'gzip, deflate',
                'X-AUTH-TOKEN': self.Cookie,
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Content-Type': 'application/json',
            }

            data = {"components": [{"key": "id", "name": "MsTableSearchInput", "label": "ID", "operator": {
                "options": [{"label": "commons.adv_search.operators.like", "value": "like"},
                            {"label": "commons.adv_search.operators.not_like", "value": "not like"}]}},
                                   {"key": "name", "name": "MsTableSearchInput", "label": "commons.name",
                                    "operator": {"value": "like", "options": [
                                        {"label": "commons.adv_search.operators.like", "value": "like"},
                                        {"label": "commons.adv_search.operators.not_like", "value": "not like"}]}},
                                   {"key": "tags", "name": "MsTableSearchInput", "label": "commons.tag",
                                    "operator": {"value": "like", "options": [
                                        {"label": "commons.adv_search.operators.like", "value": "like"},
                                        {"label": "commons.adv_search.operators.not_like", "value": "not like"}]}},
                                   {"key": "moduleIds", "name": "MsTableSearchNodeTree",
                                    "label": "test_track.case.module", "operator": {"value": "in", "options": [
                                       {"label": "commons.adv_search.operators.in", "value": "in"},
                                       {"label": "commons.adv_search.operators.not_in", "value": "not in"}]},
                                    "options": {"url": "/case/node/list", "type": "POST", "params": {}}},
                                   {"key": "createTime", "name": "MsTableSearchDateTimePicker",
                                    "label": "commons.create_time", "operator": {"options": [
                                       {"label": "commons.adv_search.operators.between", "value": "between"},
                                       {"label": "commons.adv_search.operators.gt", "value": "gt"},
                                       {"label": "commons.adv_search.operators.lt", "value": "lt"}]}},
                                   {"key": "updateTime", "name": "MsTableSearchDateTimePicker",
                                    "label": "commons.update_time", "operator": {"options": [
                                       {"label": "commons.adv_search.operators.between", "value": "between"},
                                       {"label": "commons.adv_search.operators.gt", "value": "gt"},
                                       {"label": "commons.adv_search.operators.lt", "value": "lt"}]}},
                                   {"key": "creator", "name": "MsTableSearchSelect", "label": "api_test.creator",
                                    "operator": {
                                        "options": [{"label": "commons.adv_search.operators.in", "value": "in"},
                                                    {"label": "commons.adv_search.operators.not_in", "value": "not in"},
                                                    {"label": "commons.adv_search.operators.current_user",
                                                     "value": "current user"}]},
                                    "options": {"url": "/user/project/member/list", "labelKey": "name",
                                                "valueKey": "id"}, "props": {"multiple": True}},
                                   {"key": "reviewStatus", "name": "MsTableSearchSelect",
                                    "label": "test_track.review_view.execute_result", "operator": {
                                       "options": [{"label": "commons.adv_search.operators.in", "value": "in"},
                                                   {"label": "commons.adv_search.operators.not_in",
                                                    "value": "not in"}]},
                                    "options": [{"label": "test_track.review.prepare", "value": "Prepare"},
                                                {"label": "test_track.review.pass", "value": "Pass"},
                                                {"label": "test_track.review.un_pass", "value": "UnPass"},
                                                {"label": "test_track.review.again", "value": "Again"},
                                                {"label": "test_track.review.underway", "value": "Underway"}],
                                    "props": {"multiple": True}}, {"key": "followPeople", "name": "MsTableSearchSelect",
                                                                   "label": "commons.follow_people", "operator": {
                        "options": [{"label": "commons.adv_search.operators.in", "value": "in"},
                                    {"label": "commons.adv_search.operators.current_user", "value": "current user"}]},
                                                                   "options": {"url": "/user/ws/current/member/list",
                                                                               "labelKey": "name", "valueKey": "id"},
                                                                   "props": {"multiple": True}},
                                   {"key": "demand", "name": "MsTableSearchMix",
                                    "label": "test_track.related_requirements", "operator": {"options": [
                                       {"label": "test_track.demand.third_platform_demand", "value": "third_platform"},
                                       {"label": "test_track.demand.other_demand", "value": "other_platform"}]},
                                    "options": {"url": "/issues/demand/list", "labelKey": "name", "valueKey": "id"},
                                    "props": {"multiple": True, "collapse-tags": True}},
                                   {"key": "priority", "name": "MsTableSearchSelect",
                                    "label": "custom_field.case_priority", "operator": {
                                       "options": [{"label": "commons.adv_search.operators.in", "value": "in"},
                                                   {"label": "commons.adv_search.operators.not_in",
                                                    "value": "not in"}]},
                                    "options": [{"value": "P0", "text": "P0", "system": True},
                                                {"value": "P1", "text": "P1", "system": True},
                                                {"value": "P2", "text": "P2", "system": True},
                                                {"value": "P3", "text": "P3", "system": True}],
                                    "props": {"multiple": True}}, {"key": "carType", "name": "MsTableSearchSelect",
                                                                   "label": "custom_field.case_car_type", "operator": {
                        "options": [{"label": "commons.adv_search.operators.like", "value": "like"},
                                    {"label": "commons.adv_search.operators.not_like", "value": "not like"}]},
                                                                   "options": {
                                                                       "url": "/test/plan/get/cartype/option/52c062de-78ea-41b4-8307-bed834cef1a7",
                                                                       "labelKey": "text", "valueKey": "text"}},
                                   {"key": "baseLine", "name": "MsTableSearchSelect",
                                    "label": "custom_field.case_base_line", "operator": {
                                       "options": [{"label": "commons.adv_search.operators.like", "value": "like"},
                                                   {"label": "commons.adv_search.operators.not_like",
                                                    "value": "not like"}]}, "options": {
                                       "url": "/test/plan/get/baseline/option/52c062de-78ea-41b4-8307-bed834cef1a7",
                                       "labelKey": "text", "valueKey": "text"}},
                                   {"key": "maintainer", "name": "MsTableSearchSelect",
                                    "label": "custom_field.case_maintainer", "operator": {
                                       "options": [{"label": "commons.adv_search.operators.in", "value": "in"},
                                                   {"label": "commons.adv_search.operators.not_in",
                                                    "value": "not in"}]},
                                    "options": {"url": "/user/project/member/list", "labelKey": "name",
                                                "valueKey": "id"}, "props": {"multiple": True}},
                                   {"key": "gitRepo", "name": "MsTableSearchInput", "label": "test_track.case.git_repo",
                                    "operator": {"value": "like", "options": [
                                        {"label": "commons.adv_search.operators.like", "value": "like"},
                                        {"label": "commons.adv_search.operators.not_like", "value": "not like"}]}},
                                   {"key": "gitModuleClassFunc", "name": "MsTableSearchInput",
                                    "label": "test_track.case.git_module_class_func", "operator": {"value": "like",
                                                                                                   "options": [{
                                                                                                       "label": "commons.adv_search.operators.like",
                                                                                                       "value": "like"},
                                                                                                       {
                                                                                                           "label": "commons.adv_search.operators.not_like",
                                                                                                           "value": "not like"}]}},
                                   {"key": "1ae81def-d0bd-4144-91b5-e52fff4d262c", "name": "MsTableSearchInput",
                                    "label": "JamaID", "operator": {"value": "like", "options": [
                                       {"label": "commons.adv_search.operators.like", "value": "like"},
                                       {"label": "commons.adv_search.operators.not_like", "value": "not like"}]},
                                    "options": [], "custom": False, "type": "input"},
                                   {"key": "2a920ef9-513d-4147-85e0-a0e8465b65e6", "name": "MsTableSearchSelect",
                                    "label": "用例类型", "operator": {
                                       "options": [{"label": "commons.adv_search.operators.in", "value": "in"},
                                                   {"label": "commons.adv_search.operators.not_in",
                                                    "value": "not in"}]},
                                    "options": [{"text": "功能可用性", "value": "功能可用性", "system": True},
                                                {"text": "性能指标", "value": "性能指标", "system": True},
                                                {"text": "场景覆盖", "value": "场景覆盖", "system": True},
                                                {"text": "接口用例", "value": "接口用例", "system": True},
                                                {"text": "效果用例", "value": "效果用例", "system": True},
                                                {"text": "鲁棒性用例", "value": "鲁棒性用例", "system": True},
                                                {"text": "安全用例", "value": "安全用例", "system": True}], "custom": False,
                                    "type": "select", "props": {"multiple": True}},
                                   {"key": "1eb8b536-ef45-41cf-b090-42624dc84c0c", "name": "MsTableSearchSelect",
                                    "label": "适用范围", "operator": {
                                       "options": [{"label": "commons.adv_search.operators.in", "value": "in"},
                                                   {"label": "commons.adv_search.operators.not_in",
                                                    "value": "not in"}]},
                                    "options": [{"value": "Smoke", "text": "Smoke", "system": True},
                                                {"value": "Sanity", "text": "Sanity", "system": True},
                                                {"text": "Full", "value": "f70ad4b6"},
                                                {"text": "Guard", "value": "a2f4822f"}], "custom": False,
                                    "type": "select", "props": {"multiple": True}},
                                   {"key": "6884d9a9-aaa2-45f6-949f-0a99691fda40", "name": "MsTableSearchSelect",
                                    "label": "业务级别", "operator": {
                                       "options": [{"label": "commons.adv_search.operators.in", "value": "in"},
                                                   {"label": "commons.adv_search.operators.not_in",
                                                    "value": "not in"}]}, "options": [
                                       {"text": "ComponentTest-CDC", "value": "ComponentTest-CDC", "system": True},
                                       {"text": "ComponentTest-BGM", "value": "ComponentTest-BGM", "system": True},
                                       {"text": "ComponentTest-TCAM", "value": "ComponentTest-TCAM", "system": True},
                                       {"text": "ComponentTest-ACU", "value": "ComponentTest-ACU", "system": True},
                                       {"text": "CloudServiceTest", "value": "CloudServiceTest", "system": True},
                                       {"text": "APP-互联", "value": "APP-互联", "system": True},
                                       {"text": "PlatformTest-BaseTech", "value": "PlatformTest-BaseTech",
                                        "system": True},
                                       {"text": "PlatformTest-SOA", "value": "PlatformTest-SOA", "system": True},
                                       {"text": "FunctionTest-舱", "value": "FunctionTest-舱", "system": True},
                                       {"text": "FunctionTest-驾", "value": "FunctionTest-驾", "system": True},
                                       {"text": "FunctionTest-互联", "value": "FunctionTest-互联", "system": True},
                                       {"text": "FunctionTest-整车控制", "value": "FunctionTest-整车控制", "system": True},
                                       {"text": "FunctionTest-运动控制", "value": "FunctionTest-运动控制", "system": True},
                                       {"text": "集成测试", "value": "集成测试", "system": True},
                                       {"text": "工业化测试", "value": "工业化测试", "system": True},
                                       {"text": "未设置", "value": "未设置", "system": True}], "custom": False,
                                    "type": "multipleSelect", "props": {"multiple": True}},
                                   {"key": "99d14839-02cc-4d5b-b18f-284329730484", "name": "MsTableSearchSelect",
                                    "label": "Automation", "operator": {
                                       "options": [{"label": "commons.adv_search.operators.in", "value": "in"},
                                                   {"label": "commons.adv_search.operators.not_in",
                                                    "value": "not in"}]},
                                    "options": [{"value": "Not Applicable", "text": "Not Applicable", "system": True},
                                                {"value": "Not Ready", "text": "Not Ready", "system": True},
                                                {"value": "Automated", "text": "Automated", "system": True}],
                                    "custom": False, "type": "select", "props": {"multiple": True}},
                                   {"key": "d64c3c5b-768b-4eb0-b6c8-483da5f72844", "name": "MsTableSearchInput",
                                    "label": "测试平台", "operator": {"value": "like", "options": [
                                       {"label": "commons.adv_search.operators.like", "value": "like"},
                                       {"label": "commons.adv_search.operators.not_like", "value": "not like"}]},
                                    "options": [], "custom": True, "type": "input"},
                                   {"key": "3ec58302-2c8c-4ef0-a73d-3951be7b3045", "name": "MsTableSearchInput",
                                    "label": "函数名称", "operator": {"value": "like", "options": [
                                       {"label": "commons.adv_search.operators.like", "value": "like"},
                                       {"label": "commons.adv_search.operators.not_like", "value": "not like"}]},
                                    "options": [], "custom": True, "type": "input"},
                                   {"key": "f995823c-c8c0-4aed-b4da-f736f471fe03", "name": "MsTableSearchInput",
                                    "label": "接口名称", "operator": {"value": "like", "options": [
                                       {"label": "commons.adv_search.operators.like", "value": "like"},
                                       {"label": "commons.adv_search.operators.not_like", "value": "not like"}]},
                                    "options": [], "custom": True, "type": "input"},
                                   {"key": "2baf795a-f164-b463-9304-484017a24170", "name": "MsTableSearchInput",
                                    "label": "JamaReqID", "operator": {"value": "like", "options": [
                                       {"label": "commons.adv_search.operators.like", "value": "like"},
                                       {"label": "commons.adv_search.operators.not_like", "value": "not like"}]},
                                    "options": [], "custom": False, "type": "input"},
                                   {"key": "6364821d-6005-4acb-ad92-ef6bbff51fea", "name": "MsTableSearchSelect",
                                    "label": "Jazz用例类型", "operator": {
                                       "options": [{"label": "commons.adv_search.operators.in", "value": "in"},
                                                   {"label": "commons.adv_search.operators.not_in",
                                                    "value": "not in"}]},
                                    "options": [{"text": "单域", "value": "c39b04cf"},
                                                {"text": "跨域", "value": "217ea208"}], "custom": True, "type": "select",
                                    "props": {"multiple": True}},
                                   {"key": "06d7ce30-43a9-44b0-835e-3d1745e6840b", "name": "MsTableSearchSelect",
                                    "label": "Jazz用例执行域", "operator": {
                                       "options": [{"label": "commons.adv_search.operators.in", "value": "in"},
                                                   {"label": "commons.adv_search.operators.not_in",
                                                    "value": "not in"}]},
                                    "options": [{"text": "BGM", "value": "cc39b3e2"},
                                                {"text": "TCAM", "value": "cea88664"},
                                                {"text": "ACU_M", "value": "6448dc7b"},
                                                {"text": "ACU_S", "value": "bf96d29d"},
                                                {"text": "CDCA", "value": "214966d9"},
                                                {"text": "CDCQ", "value": "97628888"}], "custom": True,
                                    "type": "multipleSelect", "props": {"multiple": True}}],
                    "filters": {"reviewStatus": ["Prepare", "Pass", "UnPass"]}, "custom": False, "planId": "",
                    "nodeIds": [], "selectAll": False, "unSelectIds": [], "orders": [], "versionId": None,
                    "selectThisWeedData": False, "selectThisWeedRelevanceData": False, "caseCoverage": None,
                    "projectId": projectId}
            if query_condition is not None:
                data['name'] = query_condition
            result = []
            itemCount = 0
            i = 0

            while True:
                i += 1
                path = f"/track/test/case/list/{i}/50"
                url = self.server_name + path
                response = requests.post(
                    url, json.dumps(data), headers=headers, timeout=30
                )
                resp_body = json.loads(str(response.content, 'utf-8'))

                if itemCount == 0:  # 仅赋值1次
                    itemCount = resp_body['data']['itemCount']
                if len(resp_body['data']["listObject"]) > 0:
                    result.extend(resp_body['data']["listObject"])
                logger.info(f"总数据量：{itemCount}, 已获取数据量：{len(result)}")
                if len(resp_body['data']["listObject"]) < 50:
                    break
                if len(result) >= itemCount:
                    break
            return result

    def get_case_step_by_case_jama_id(self, project_name, case_jama_id):
        """
        根据项目名称及用例的jama id获取用例的前置条件及用例步骤
        返回结果是列表形式，列表元素是字典，包含"前置条件"、"用例步骤"两个key
        """
        project_id_dict = {"BGM": "1fbbeb47-6cc7-48bd-aafc-24349853e9d8",
                           "SOA": "52c062de-78ea-41b4-8307-bed834cef1a7",
                           "TCAM": "225ebd89-8c9c-48dd-a3d8-739e52ee76e2"}
        projectId = project_id_dict.get(project_name, None)
        get_result = []
        if projectId is None:
            logger.info("project_name 仅支持BGM、TCAM、SOA")
            return get_result
        else:
            result = self.get_testcases_in_project(projectId, str(case_jama_id))
            logger.info(f"查询结果：{result}")
            for item in result:
                logger.info(f"前置条件：{item['prerequisite']}")
                for step in eval(item['steps']):
                    logger.info(f"序号：{step['num']} 用例步骤: {step['desc']}  预期结果: {step['result']}")
                get_result.append({"前置条件": item['prerequisite'], "用例步骤": eval(item['steps']),
                                   "name": item['name'], "priority": item['priority'], "tags": item["tags"],
                                   "maintainer": item["maintainer"]})
            else:
                return get_result

    def get_testplan_id_by_condition(self, project_name, target_baseline, target_version, test_type='版本提测'):
        """
        从项目的测试计划列表中获取并返回包含“目标基线”、“目标版本” 的测试计划ID

        :param project_name: 项目名称：可选值：BGM、TCAM、SOA服务
        :param target_baseline: 目标基线
        :param target_version: 目标版本
        :param test_type: 测试类型：可选值：版本提测...
        """
        # ms_project_dict = {"BGM": "1fbbeb47-6cc7-48bd-aafc-24349853e9d8",
        #                    "TCAM": "225ebd89-8c9c-48dd-a3d8-739e52ee76e2",
        #                    "SOA服务": "52c062de-78ea-41b4-8307-bed834cef1a7",
        #                    "CDC_MCU": "c8fc5cb7-5a55-41a8-8f04-e43164e3878a"}
        plan_id_list = []
        if project_name in ms_project_dict:
            testplan_query_result = self.get_testplan_list_in_project(ms_project_dict.get(project_name))
            for testplan in testplan_query_result:
                if test_type in testplan["plan_name"]:
                    if project_name in testplan["plan_name"]:
                        if target_baseline in testplan["plan_name"]:
                            if target_version in testplan["plan_name"]:
                                plan_id_list.append(testplan["plan_id"])
        else:
            logger.info(f"{project_name} 不支持，当前仅支持：BGM、TCAM、SOA服务")
        return plan_id_list
    def creat_new_testplan(self, testplan_name, project_name, test_owner='lei.hong', car_type='MarsOne', target_baseline='V2.1.0', test_level='整车集成测试', stage='Smoke', dscription='TL cici test', max_retry_num=10, retry_period=20):
        """
        在指定项目下创建新的测试计划
        :param testplan_name: 测试计划名称
        :param project_name: 项目名称：可选值：BGM、TCAM、SOA服务
        :param test_owner: 测试负责人
        :param car_type: 车型
        :param target_baseline: 目标基线
        :param test_level: 测试级别
        :param stage: 阶段
        :param dscription: 描述
        :param max_retry_num: 最大重试次数
        :param retry_period: 重试间隔时间
        :return: 测试计划ID
        """
        # ms_project_dict = {"BGM": "1fbbeb47-6cc7-48bd-aafc-24349853e9d8",
        #                    "TCAM": "225ebd89-8c9c-48dd-a3d8-739e52ee76e2",
        #                    "SOA服务": "52c062de-78ea-41b4-8307-bed834cef1a7"}
        if self.signin_flag:
            if project_name in ms_project_dict:
                headers = {
                    'CSRF-TOKEN': self.csrfToken,
                    'PROJECT': ms_project_dict.get(project_name),
                    'WORKSPACE': self.lastWorkspaceId,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                                '(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                    'Accept-Encoding': 'gzip, deflate',
                    'X-AUTH-TOKEN': self.Cookie,
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Content-Type': 'application/json',
                }
                data = {
                        "round": None,
                        "name": testplan_name,
                        "projectIds": [],
                        "principals": [test_owner],
                        "stage": stage,
                        "description": dscription,
                        "plannedStartTime": "",
                        "plannedEndTime": "",
                        "automaticStatusUpdate": False,
                        "follows": [],
                        "baseLine": target_baseline,
                        "carType": car_type,
                        "testLevel": test_level,
                        "buildNumber": "",
                        "businessName": "",
                        "moduleId": "",
                        "tags": "[]",
                        "carTypeId": "61",
                        "workspaceId": self.lastWorkspaceId,
                        "isRoboTeamNotice": False,
                        "roboWebhook": ""
                    }
                retry_num = 0
                while retry_num <= max_retry_num:
                    retry_num += 1
                    try:
                        path = f"/track/test/plan/add"
                        url = self.server_name + path
                        response = requests.post(
                            url, json.dumps(data), headers=headers, timeout=30)
                        resp_body = json.loads(str(response.content, 'utf-8'))
                        if resp_body.get("success"):
                            logger.info(f"{testplan_name}测试计划创建成功")
                            return resp_body.get("data").get("id")
                        else:
                            raise Exception(resp_body.get("message"))
                    except Exception as e:
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/ms/ms_lib.py")
                        exception_detail = traceback.format_exc()
                        if retry_num == max_retry_num:
                            logger.error(f"创建测试计划失败：{exception_detail}")
                        time.sleep(retry_period)
                    else:
                        break
            else:
                logger.info(f"{project_name} 不支持，当前仅支持：BGM、TCAM、SOA服务")
    
    def add_testcase_to_testplan(self, planId, ids, project_name, max_retry_num=10, retry_period=20):
        """
        将测试用例添加到测试计划中
        :param planId: 测试计划ID
        :param ids: 测试用例ID列表
        :param project_name: 项目名称：可选值：BGM、TCAM、SOA服务
        :param max_retry_num: 最大重试次数
        :param retry_period: 重试间隔时间
        """
        # ms_project_dict = {"BGM": "1fbbeb47-6cc7-48bd-aafc-24349853e9d8",
        #                    "TCAM": "225ebd89-8c9c-48dd-a3d8-739e52ee76e2",
        #                    "SOA服务": "52c062de-78ea-41b4-8307-bed834cef1a7"}
        if self.signin_flag:
            if project_name in ms_project_dict:
                headers = {
                    'CSRF-TOKEN': self.csrfToken,
                    'PROJECT': ms_project_dict.get(project_name),
                    'WORKSPACE': self.lastWorkspaceId,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                                '(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                    'Accept-Encoding': 'gzip, deflate',
                    'X-AUTH-TOKEN': self.Cookie,
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Content-Type': 'application/json',
                }
                data = {"ids": ids, "planId": planId, "checked": False}
                retry_num = 0
                while retry_num <= max_retry_num:
                    retry_num += 1
                    try:
                        path = f"/track/test/plan/relevance"
                        url = self.server_name + path
                        response = requests.post(
                            url, json.dumps(data), headers=headers, timeout=30
                        )
                        resp_body = json.loads(str(response.content, 'utf-8'))
                        logger.info(f"{ids} add_testcase_to_testplan {planId} 执行结果：{resp_body}")
                        if resp_body.get("success"):
                            logger.info(f"{ids} add_testcase_to_testplan {planId} 执行成功")
                        else:
                            raise Exception(resp_body.get("message"))
                    except Exception as e:
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/ms/ms_lib.py")
                        exception_detail = traceback.format_exc()
                        if retry_num == max_retry_num:
                            logger.error(f"添加测试用例失败：{exception_detail}")
                        time.sleep(retry_period)
                    else:
                        break
            else:
                logger.info(f"{project_name} 不支持，当前仅支持：BGM、TCAM、SOA服务")

    def get_testcases_from_project_by_condition(self, project_name, in_con=None, ex_con=None, max_retry_num=10):
        """
        根据条件从项目中获取测试用例
        
        Args:
            project_name (str): 项目名称
            in_con (list, optional): 包含条件列表，默认为None。如果提供，则只返回包含这些条件的测试用例
            ex_con (list, optional): 排除条件列表，默认为None。如果提供，则排除包含这些条件的测试用例
            max_retry_num (int, optional): 最大重试次数，默认为10。
        
        Returns:
            list: 满足条件的测试用例ID列表
        
        """
        
        # ms_project_dict = {"BGM": "1fbbeb47-6cc7-48bd-aafc-24349853e9d8",
        #                    "TCAM": "225ebd89-8c9c-48dd-a3d8-739e52ee76e2",
        #                    "SOA服务": "52c062de-78ea-41b4-8307-bed834cef1a7"}
        if self.signin_flag:
            if project_name in ms_project_dict:
                cases = self.get_testcases_in_project(ms_project_dict.get(project_name))
                if not cases:
                    logger.error(f"{project_name} 项目下没有测试用例")
                    return []
                case_dict = {}
                for i in cases:
                    if i.get("nodePath") in case_dict:
                        case_dict[i.get("nodePath")].append(i.get("id"))
                    else:
                        case_dict[i.get("nodePath")] = []
                        case_dict[i.get("nodePath")].append(i.get("id"))
                case_list = []
                if ex_con:
                    del_key = []
                    for k, v in case_dict.items():
                        for c in ex_con:
                            if c in k:
                                del_key.append(k)        
                    if del_key:
                        for d in del_key:
                            case_dict.pop(d)
                if in_con:
                    del_key = []
                    for k, v in case_dict.items():
                        for c in in_con:
                            if c not in k:
                                del_key.append(k)
                    if del_key:
                        for d in del_key:
                            case_dict.pop(d)
                for k, v in case_dict.items():    
                    case_list += v
                logger.debug(f"获取到{project_name} 项目下包含：{in_con}，不包含：{ex_con}的测试用例数量：{len(case_list)}")
                return case_list
    def change_testplan_status(self, project_name, planId, status='已归档', max_retry_num=10, retry_period=20):
        """
        修改测试计划状态
        
        Args:
            project_name (str): 项目名称，可选值：BGM、TCAM、SOA服务、cdc-mcu
            planId (str): 测试计划ID
            status (str, optional): 测试计划状态，默认为'已归档'. Defaults to '已归档'.
            max_retry_num (int, optional): 最大重试次数，默认为10. Defaults to 10.
            retry_period (int, optional): 重试间隔时间，默认为20秒. Defaults to 20.
        
        Returns:
            None
        
        Raises:
            Exception: 如果请求失败，将抛出异常
        
        """
        if self.signin_flag:
            if project_name in ms_project_dict:
                headers = {
                    'CSRF-TOKEN': self.csrfToken,
                    'PROJECT': ms_project_dict.get(project_name),
                    'WORKSPACE': self.lastWorkspaceId,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                                '(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                    'Accept-Encoding': 'gzip, deflate',
                    'X-AUTH-TOKEN': self.Cookie,
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Content-Type': 'application/json',
                }
                status_dict = {"未开始": "Prepare", "进行中": "Underway", 
                               "已逾期": "Finished", "已完成": "Completed", 
                               "已终止": "Terminated", "已归档": "Archived"}
                data = {"id": planId, "status": status_dict.get(status)}
                retry_num = 0
                while retry_num <= max_retry_num:
                    retry_num += 1
                    try:
                        path = f"/track/test/plan/edit"
                        url = self.server_name + path
                        response = requests.post(
                            url, json.dumps(data), headers=headers, timeout=30
                        )
                        resp_body = json.loads(str(response.content, 'utf-8'))
                        logger.info(f"{planId}测试计划修改状态 执行结果：{resp_body}")
                        if resp_body.get("success"):
                            logger.info(f"{planId}测试计划修改状态 执行成功")
                        else:
                            raise Exception(resp_body.get("message"))
                    except Exception as e:
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/ms/ms_lib.py")
                        exception_detail = traceback.format_exc()
                        if retry_num == max_retry_num:
                            logger.error(f"测试计划修改状态：{exception_detail}")
                        time.sleep(retry_period)
                    else:
                        break
            else:
                logger.info(f"{project_name} 不支持，当前仅支持：BGM、TCAM、SOA服务、cdc-mcu")
                
                
def get_soa_test_result_from_test_db(bgmVersion, jidlVersion, sync_num=0):
    """从SOA test db 获取测试数据，并将数据同步到API网站后台"""
    headers = {
        'Accept': "application/json, text/plain, */*",
        'token': __import__("os").environ.get('XAT_CREDENTIAL_ECU__INTERFACE_MS_MS_LIB_PY_TOKEN', ""),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Type': 'application/json',
    }
    url = f"http://10.80.51.28:8887/s2sAutoTestResult/query?bgmVersion={bgmVersion}"
    response = requests.post(
        url, json.dumps({}), headers=headers, timeout=30
    )
    resp_body = json.loads(str(response.content, 'utf-8'))
    data_num_sync_api = len(resp_body.get('data')) if sync_num == 0 else sync_num
    logger.info(f"需同步API网站的总数据量：{data_num_sync_api}")
    i = 0
    for case in resp_body.get("data"):
        i = i + 1
        case["functionName"] = case.get("functionName").replace('(', '').replace(')', '').replace(' ', '')
        case_result = CaseResult(
            bgmVersion=bgmVersion,
            jamaId=case.get("testcaseId"),
            interfaceName=case.get("interfaceName"),
            serviceName=case.get("serviceName"),
            functionName=case.get("functionName"),
            functionType=case.get("functionType"),
            functionParameter=case.get("functionParameter"),
            expectResult=case.get("expectResult"),
            realResult=case.get("realResult"),
            autoCaseResult=case.get("autoCaseResult"),
            testcaseId=case.get("testcaseId"),
            testcaseDescription=case.get("testcaseDescription"),
            jiraLink=case.get("jiraLink"),
            jidlVersion=jidlVersion,
            uniq_id=case.get("id"),
            updateTime=case.get('updateTime'),
            domain=get_ecu_domain_name(case.get("serviceName"))
        )
        # info_json = json.dumps(case, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False)
        if i <= data_num_sync_api:
            api_request_body_list = [case_result.get_api_request_dict()]
            """上传到API网站后台"""
            url_api = f"https://soa-portal-api.jidudev.com/case/add"
            response_api = requests.post(
                url_api, json.dumps(api_request_body_list), headers=headers, timeout=30
            )
            resp_body_api = json.loads(str(response_api.content, 'utf-8'))
            logger.info(f"API网站 {bgmVersion}，第{i}次同步的返回结果：{resp_body_api}")
            sleep(0.01)
        else:
            logger.info(f"同步结束！！")
            break


def add_exception_get_testcase_in_testplan(exception_info, document_id="GzALwge8iiOIISkkTztc3m2ynoe",
                                           table_name="获取测试计划中的测试用例"):
    """
    获取测试计划中的测试用例时，发生的异常信息
    """
    try:
        feishu = feishu_api()
        feishu.get_app_access_token()
        feishu.get_user_access_token()
        feishu.get_bitable_app_access_token(document_id=document_id)
        table_id = feishu.get_table_id_by_table_name(table_name)
        result = feishu.add_record_in_table(table_id, exception_info)
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/ms/ms_lib.py")
        logger.info(f"添加 获取测试计划中的测试用例时，发生的异常信息时发生{e.__str__()}异常:{traceback.format_exc()}")


def add_ms_login_fail(exception_info, document_id="GzALwge8iiOIISkkTztc3m2ynoe", table_name="MS登录接口失败"):
    """
    获取测试计划中的测试用例时，发生的异常信息
    """
    try:
        feishu = feishu_api()
        feishu.get_app_access_token()
        feishu.get_user_access_token()
        feishu.get_bitable_app_access_token(document_id=document_id)
        table_id = feishu.get_table_id_by_table_name(table_name)
        result = feishu.add_record_in_table(table_id, exception_info)
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/ms/ms_lib.py")
        logger.info(f"添加 获取测试计划中的测试用例时，发生的异常信息时发生{e.__str__()}异常:{traceback.format_exc()}")


def add_exception_set_testcase_result_in_testplan(exception_info, document_id="GzALwge8iiOIISkkTztc3m2ynoe",
                                                  table_name="设置测试计划中用例的执行结果"):
    """
    获取测试计划中的测试用例时，发生的异常信息
    """
    try:
        feishu = feishu_api()
        feishu.get_app_access_token()
        feishu.get_user_access_token()
        feishu.get_bitable_app_access_token(document_id=document_id)
        table_id = feishu.get_table_id_by_table_name(table_name)
        result = feishu.add_record_in_table(table_id, exception_info)
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/ms/ms_lib.py")
        logger.info(f"添加 获取测试计划中的测试用例时, 发生{e.__str__()}异常: {traceback.format_exc()}")


if __name__ == '__main__':
    logger = Logger().get_logger("test")
    """
    MS ==》soa test db
    """
    client = meterSphere_client()
    a = client.change_testplan_status(project_name='SOA服务', planId="4171f060-c45d-4d73-98d1-c2b460e4a5d5", status='已归档')
    print(a)
    # id = client.creat_new_testplan(testplan_name='lei_test1111222333322555', project_name="TCAM")
    # print(id)
    # a = client.get_testcases_in_testPlan(planId="51afb6ee-1306-47e2-ae4c-d1bc4f2db78a", projectId='225ebd89-8c9c-48dd-a3d8-739e52ee76e2')
    # print(a)
    # b = {}
    # for i in a:
    #     if i.get("nodePath") in b:
    #         b[i.get("nodePath")].append(i.get("id"))
    #     else:
    #         b[i.get("nodePath")] = []
    #         b[i.get("nodePath")].append(i.get("id"))
            
    
    # logger.info(b)
    a = client.get_testplan_id_by_condition(project_name='BGM', target_baseline='V2.2.0', target_version='AI', test_type='脚本稳定性')
    print(a)
    # client.creat_new_testplan(testplan_name='lei_test1111222333322555', project_name="BGM")
    # a = client.get_testcases_from_project_by_condition(project_name='TCAM', in_con=['未规划用例'])
    # print(a)
    # a = client.add_testcase_to_testplan(planId="51afb6ee-1306-47e2-ae4c-d1bc4f2db78a", ids=a, project_name="TCAM")
    # custom_mappings_0, _, _ = client.get_customnum_mappings_from_planid("e01fe319-663c-4deb-b8d1-1280dec0fda8")
    # logger.info(custom_mappings_0)
    # for key in custom_mappings_0:
    #     value = custom_mappings_0.get(key)
    #     logger.info(value)
    #     client.set_testcase_status_in_testPlan(value[0], value[1], "Pass", value[3])
    # client.sync_data_from_MS_to_soa_test_db('ecac20b4-0194-416e-b21d-aaf0f8100274', '6160110140AJ', '6110110140AF',
    #                                         nodePath="SOA服务接口")
    # data = {"planId": "123", "url": "/track/test/plan/case/list/{i}/100", "异常类型": "返回结果转JSON后为None", "执行序号": 5}
    # add_exception_get_testcase_in_testplan(data)

    # client.sync_data_from_MS_to_soa_test_db('7f18fb57-a33d-4adc-9169-59a065a08123', '6160110110HC')
    # client.sync_data_from_MS_to_soa_test_db('6b0f7d3b-c8b2-4872-8025-22311e93f175', '6160110110HK')

    """
       soa test db ==》API db
    """
    # get_soa_test_result_from_test_db("6160110180BB", "JIDL_RELEASE_1.3REL_M")
    # get_soa_test_result_from_test_db("6160110110HC", "JIDL_RELEASE_1.1REL_5")
    # get_soa_test_result_from_test_db("6160110110HK", "JIDL_RELEASE_1.1REL_7")
    # get_soa_test_result_from_test_db("6160110130AR", "JIDL_RELEASE_1.3REL_9")
