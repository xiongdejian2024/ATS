
import json
import os
import sys
import time

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
sys.path.append(os.path.join(current_path, ".."))
sys.path.append(os.path.join(current_path, "../.."))
sys.path.append(os.path.join(current_path, "../../.."))
from xat_ecu.legacy.common.constant import MS_CONSTANT
from xat_ecu.legacy.common.logger import logger, Logger
import requests
import base64


class feishu_api:
    def __init__(self, app_id="cli_a51121ad3bcad00c", app_secret=__import__("os").environ.get('XAT_CREDENTIAL____BGM_BGM_TOOLS_MS_LIB_MATCH_ID_SWRS_JAMA_PY_APP_SECRET', ""),
                 server_name="https://open.feishu.cn/"):
        """
        执行飞书多维表格相关操作

        :param app_id: 应用唯一标识，创建应用后获得
        :param app_secret: 应用秘钥，创建应用后获得
        :param server_name: 飞书服务端API的服务端地址
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.server_name = server_name
        self.tenant_access_token = ""
        self.get_tenant_access_token()
        self.app_access_token = ""
        self.user_access_token = ""

    def get_tenant_access_token(self, path="/open-apis/auth/v3/tenant_access_token/internal"):
        """
        自建应用获取 tenant_access_token

        :param path: api的请求地址
        """
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data = {'app_id': self.app_id, 'app_secret': self.app_secret}

        url = self.server_name + path
        response = requests.post(url, json.dumps(data), headers=headers, timeout=5)
        resp_body = json.loads(str(response.content, 'utf-8'))
        response_code = resp_body.get("code", 500)
        if response_code == 0:
            self.tenant_access_token = resp_body.get("tenant_access_token")

    def get_app_access_token(self, path="/open-apis/auth/v3/app_access_token/internal"):
        """
        自建应用获取 app_access_token

        :param path: api的请求地址
        """
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data = {'app_id': self.app_id, 'app_secret': self.app_secret}

        url = self.server_name + path
        response = requests.post(url, json.dumps(data), headers=headers, timeout=5)
        resp_body = json.loads(str(response.content, 'utf-8'))
        response_code = resp_body.get("code", 500)
        if response_code == 0:
            self.app_access_token = resp_body.get("tenant_access_token")

    def get_user_access_token(self, path="open-apis/authen/v1/oidc/refresh_access_token"):
        """
        刷新 user_access_token

        :param path: api的请求地址
        """
        flag, refresh_token_dict = get_soa_platform_refresh_token()
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   'Authorization': f"Bearer {self.app_access_token}"}
        data = {'grant_type': "refresh_token", 'refresh_token': refresh_token_dict.get("remark")}

        url = self.server_name + path
        response = requests.post(url, json.dumps(data), headers=headers, timeout=5)
        resp_body = json.loads(response.text)
        response_code = resp_body.get("code", 500)
        if response_code == 0:
            self.user_access_token = resp_body.get("data").get("access_token")

            refresh_token_dict["remark"] = resp_body.get('data').get('refresh_token')
            update_soa_platform_refresh_token(refresh_token_dict)  # 更新refresh_token的值

    def get_user_open_id(self, name, path="open-apis/search/v1/user?"):
        """
        获取多维表格的数据表信息
        """
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   "Authorization": f"Bearer {self.user_access_token}"}
        url = self.server_name + path + f"query={name}&page_size=20"
        response = requests.get(url, headers=headers, timeout=5)
        resp_body = json.loads(response.text)
        if resp_body.get("code", 500) == 0:
            user_list = resp_body.get("data").get("users")
            if user_list:
                for user in user_list:
                    return user.get('open_id')
            else:
                logger.info(resp_body)
                return None
        else:
            logger.info(resp_body)
            return None

    def get_bitable_app_access_token(self, document_id, path="open-apis/wiki/v2/spaces/get_node"):
        """
        根据多维表格的document_id获取其obj_token

        :param document_id: 文档的唯一标识
        :param path: api的请求地址
        """
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   "Authorization": f"Bearer {self.tenant_access_token}"}
        url = self.server_name + path
        params = {'token': document_id}

        response = requests.get(url, params=params, headers=headers, timeout=5)

        resp_body = json.loads(response.text)
        response_code = resp_body.get("code", 500)
        if response_code == 0:
            self.app_access_token = resp_body.get("data").get("node").get("obj_token")

    def get_bitable_table_ids(self, path="/open-apis/bitable/v1/apps/"):
        """
        获取多维表格的数据表信息
        """
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   "Authorization": f"Bearer {self.tenant_access_token}"}
        url = self.server_name + path + f"{self.app_access_token}/tables"
        response = requests.get(url, headers=headers, timeout=5)
        resp_body = json.loads(response.text)

        return resp_body.get("data").get("items")

    def get_table_id_by_table_name(self, table_name):
        """
        根据数据表的中文名称获取其table_id

        :param table_name: 数据表的中文名称
        """
        tables_info = self.get_bitable_table_ids()
        for table_info in tables_info:
            if table_info['name'] == table_name:
                return table_info['table_id']
        else:
            return None

    def get_records_in_table(self, table_id, path="/open-apis/bitable/v1/apps/"):
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   "Authorization": f"Bearer {self.tenant_access_token}"}
        url = self.server_name + path + f"{self.app_access_token}/tables/{table_id}/records"
        url_base = self.server_name + path + f"{self.app_access_token}/tables/{table_id}/records"
        res = []
        while True:
            response = requests.get(url, headers=headers, timeout=5)
            resp_body = json.loads(response.text)
            if resp_body is not None:
                if resp_body.get("data") is not None:
                    if resp_body.get("data").get("items") is not None:
                        res += [record for record in resp_body.get("data").get("items") if record is not None]

            if resp_body["data"]["has_more"]:
                url = url_base + f"?page_token={resp_body['data']['page_token']}"
            else:
                break
        return res

    def update_record_in_table(self, table_id, record_id, data: dict, path="/open-apis/bitable/v1/apps/"):
        """
        更新记录到数据表中
        """
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   "Authorization": f"Bearer {self.tenant_access_token}"}
        url = self.server_name + path + f"{self.app_access_token}/tables/{table_id}/records/{record_id}"
        data = {"fields": data}
        response = requests.put(url, json.dumps(data), headers=headers, timeout=5)
        resp_body = json.loads(response.text)
        print(f"----------------------->resp_body:{resp_body}")
        if resp_body.get("code") == 0:
            return True, "执行结果更新成功"
        else:
            logger.info(f"表{table_id} 更新记录失败")
            return False, "执行结果更新失败"


def get_soa_platform_refresh_token():
    """
    获取存放在数据库中的refresh_token
    """
    path = "http://10.80.51.28:8887/sysconfig/list?"
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    url = path + "pageNum=1&pageSize=10&paramCode=feishu_refresh_token"
    response = requests.post(url, headers=headers, timeout=5)
    resp_body = json.loads(response.text)
    if resp_body.get("status") == 1:
        return True, resp_body.get("data").get("data")[0]
    else:
        return False, "refresh_token获取失败"


def update_soa_platform_refresh_token(refresh_token_dict):
    """
    更新存放在数据库中的refresh_token
    """
    path = "http://10.80.51.28:8887/sysconfig/update"
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    url = path
    response = requests.post(url, json.dumps(refresh_token_dict), headers=headers, timeout=5)
    resp_body = json.loads(response.text)
    if resp_body.get("status") == 1:
        return True, "refresh_token更新成功"
    else:
        return False, "refresh_token更新失败"


class meterSphere_client:
    def __init__(
            self,
            username=MS_CONSTANT.MS_USERNAME,
            password=MS_CONSTANT.MS_PASSWORD,
            server_name='http://172.18.74.8:8080/ms',
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

    def get_testcases_in_project(self, projectId):
        """
        同步MS上对应项目的测试用例信息

        :param projectId: 待同步项目的项目的项目ID
        :param hours: 默认为None，全量的添加或更新，否则只同步hours小时内更新的测试用例
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
            logger.info(f"      预期获取用例总数：{itemCount}")
            logger.info(f"      实际获取用例总数：{len(result)}")
            return result

    def get_customnum_swrs_jamaID_from_project(self, project_name="1fbbeb47-6cc7-48bd-aafc-24349853e9d8"):
        """
        planId: str  such as "ccbfb89c-68bc-4da2-bc76-548794d5fce3"
        返回值类型: dict {customnum : (id, nodeId)}
        """
        if self.signin_flag:
            if project_name:
                swrs_dict = {}
                jama_dict = {}
                res = self.get_testcases_in_project(project_name)
                if res:
                    for data in res:
                        customNum = str(data.get("num"))
                        swrs = None
                        jama = None
                        if data.get("fields") is None:
                            logger.info(data)
                            continue
                        for field in data.get("fields"):
                            if field['id'] == "2baf795a-f164-b463-9304-484017a24170":
                                jama = field['value'].replace("\"", "")
                            if field['id'] == "db6b83f5-f6a7-468b-a1cb-af0b9b2cbcbc":
                                swrs = field['value'].replace("\"", "")
                        else:
                            if customNum is not None:
                                print(f"--------------------------------------->0 customNum:{customNum}")
                                if jama is not None:
                                    if "MSO" in jama:
                                        print(f"--------------------------------------->1 jama:{jama}")
                                        if "，" in jama:
                                            delimiter = "，"
                                        elif "&" in jama:
                                            delimiter = "&"
                                        else:
                                            delimiter = ","

                                        for kk in jama.split(delimiter):
                                            if len(kk) > 0:
                                                kk = kk.strip()
                                            if kk in jama_dict:
                                                jama_dict[kk] = jama_dict.get(kk) + "," + customNum
                                            else:
                                                jama_dict[kk] = customNum
                                if swrs is not None:
                                    if len(swrs) > 0:
                                        print(f"--------------------------------------->2 swrs:{swrs}")
                                        if "，" in swrs:
                                            delimiter = "，"
                                        elif "&" in swrs:
                                            delimiter = "&"
                                        else:
                                            delimiter = ","

                                        for jj in swrs.split(delimiter):
                                            if len(jj) > 0:
                                                jj = jj.strip()
                                                if jj in swrs_dict:
                                                    swrs_dict[jj] = swrs_dict.get(jj) + "," + customNum
                                                else:
                                                    swrs_dict[jj] = customNum
                    else:
                        logger.info(f"swrs_dict: {swrs_dict}")
                        logger.info(f"jama_dict: {jama_dict}")
                else:
                    logger.error("实际获取用例条数为0")
                return swrs_dict, jama_dict


if __name__ == '__main__':
    logger = Logger().get_logger("test")
    """
    MS ==》soa test db
    """
    # document_id = "QwOXw1HEhiBfvwkrYhocqFZgnsb"
    document_id = "GP1IwCfpViLf1Dk62j5cizWlnwf"

    client = meterSphere_client()
    swrs_dict, jama_dict = client.get_customnum_swrs_jamaID_from_project()

    # table_name = "BGM_JAMA需求"
    table_name = "BGM_SWRS需求"
    source_feishu = feishu_api()
    source_feishu.get_app_access_token()
    source_feishu.get_user_access_token()
    source_feishu.get_bitable_app_access_token(document_id=document_id)
    table_id = source_feishu.get_table_id_by_table_name(table_name)
    source_table_data = source_feishu.get_records_in_table(table_id)
    logger.info(source_table_data)
    i = 0
    for source_data in source_table_data:
        i += 1
        logger.info(f"{table_name} =行号： {i} == {source_data['fields']['需求ID']}")
        if source_data['fields']['需求ID'] in swrs_dict:
            data = {'关联Case ID': swrs_dict.get(source_data['fields']['需求ID'])}
            if source_data['fields']['需求是否需要覆盖'] == "是":
                data['需求是否覆盖'] = "是"
            logger.info(f"{table_name} =行号： {i} == {source_data['fields']['需求ID']}, true")
            source_feishu.update_record_in_table(table_id, source_data['record_id'], data)
        else:
            data = {}
            if source_data['fields']['需求是否需要覆盖'] == "是":
                data['需求是否覆盖'] = "否"
                source_feishu.update_record_in_table(table_id, source_data['record_id'], data)
            logger.info(f"{table_name} =行号： {i} == {source_data['fields']['需求ID']}, false")

    # table_name = "BGM_SWRS需求"
    table_name = "BGM_JAMA需求"
    source_feishu = feishu_api()
    source_feishu.get_app_access_token()
    source_feishu.get_user_access_token()
    source_feishu.get_bitable_app_access_token(document_id=document_id)
    table_id = source_feishu.get_table_id_by_table_name(table_name)
    source_table_data = source_feishu.get_records_in_table(table_id)
    logger.info(source_table_data)
    i = 0
    for source_data in source_table_data:
        i += 1
        if str(source_data['fields']['需求ID']) in jama_dict:
            data = {'关联Case ID': jama_dict.get(str(source_data['fields']['需求ID']))}
            if source_data['fields']['需求是否需要覆盖'] == "是":
                data['需求是否覆盖'] = "是"
            logger.info(f"{table_name} =行号： {i} == {source_data['fields']['需求ID']}, true")
            print(f"------------------------------------------->table_id, source_data['record_id'], data:  {table_id},{source_data['record_id']}, {data}")
            source_feishu.update_record_in_table(table_id, source_data['record_id'], data)
        else:
            data = {}
            if source_data['fields']['需求是否需要覆盖'] == "是":
                data['需求是否覆盖'] = "否"
                print(f"------------------------------------------->table_id, source_data['record_id'], data:  {table_id},{source_data['record_id']}, {data}")
                source_feishu.update_record_in_table(table_id, source_data['record_id'], data)
            logger.info(f"{table_name} =行号： {i} == {source_data['fields']['需求ID']}, false")
