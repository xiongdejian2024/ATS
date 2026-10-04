"""
@Filename     : test_canoe.py
@Time         : 2024/06/21 16:06
@Author       : junxing.pang@jiduauto.com
@Description  : this py file show how to use libCANoe.py and generate xml module file
"""
import json
import pickle
import subprocess
import traceback

import xmltodict
from libCANoe import app
from git_clone_demo import git_clone, delete_directory
# app.stop()
# app.quit()
# delete_directory(r"C:\Users\lei.an\AppData\Local\Temp\gen_py\3.9")

from typing import Generator, Tuple
import requests
import base64
import logging
import sys
import os
import datetime
import time

XML_path = "CANoeDemo_base.vxt"
logging.basicConfig(level=logging.INFO)
install_dir = r"D:\Git\soa_vector_proj"
# base_path = rf"{install_dir}\soa_vector_proj\CDC_MCU_BaseTest"
base_path = rf"{install_dir}\CDC_MCU_BaseTest"
print(base_path)
base_cfg = os.path.join(base_path, "01_CFG", "CANoeDemo.cfg")
print(base_cfg)
capl_file_path = os.path.join(base_path, "04_TestCode", "PlatformBasedTest.can")
xml_file_path = os.path.join(base_path, "04_TestCode")
print(11111, xml_file_path)
xml_file_name = "PlatformBasedTest.vxt"
env_path = os.path.join(base_path, "04_TestCode", "Test Environment.tse")
print(env_path)
env_name = "Test Environment"
save2cfg = os.path.join(base_path, "01_CFG", "BaseTest.cfg")
print(save2cfg)

ms_query_result = {}

app.stop()
class Logger(object):
    __instance = None

    def __init__(self, log_path='./logs', log_level='INFO', log_num=10):
        self.log_path = log_path
        self.origin_log_level = log_level
        self.log_num = log_num
        self.log_level = self._get_log_level(self.origin_log_level)
        self._purge_log_file(self.log_num)

    def __new__(cls, log_path='./logs', log_level='INFO', log_num=10):
        """
        Single instance.
        :param log_path:
        :param log_level:
        :return:
        """
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def get_logger(self, name=''):
        """
        Create a logger instance.
        :param name:
        :return:
        """
        log = logging.getLogger(name)
        log.setLevel(self.log_level)
        date_time = datetime.datetime.now()
        log_name = self.log_path + '/test_log_' + \
                   date_time.strftime("%Y_%m_%d_%H_%M_%S_%f") + '.log'

        fh = logging.FileHandler(log_name)
        fh.setLevel(self.log_level)

        ch = logging.StreamHandler()
        ch.setLevel(self.log_level)

        formatter = logging.Formatter(
            '%(asctime)s (%(filename)s:%(lineno)d)' + ' (%(threadName)s:%(process)d)' +
            ' %(levelname)s %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        log.addHandler(fh)
        log.addHandler(ch)
        os.environ["LOGGER"] = "logger"  # Avoid repeated printing with the logger in the ecu simulator
        return log

    def _get_log_level(self, log_level):
        if log_level.upper() == 'DEBUG':
            return 'DEBUG'
        elif log_level.upper() == 'INFO':
            return 'INFO'
        elif log_level.upper() == 'WARNING':
            return 'WARNING'
        elif log_level.upper() == 'ERROR':
            return 'ERROR'
        elif log_level.upper() == 'CRITICAL':
            return 'CRITICAL'
        else:
            print('ERROR: Input log_level parameter error: %s' % self.origin_log_level)
            sys.exit(-1)

    def _purge_log_file(self, exp_log_num=10):
        """Keep latest log files according exp_log_num value"""
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)
        else:
            try:
                log_list = os.listdir(self.log_path)
                log_list = sorted(log_list, key=lambda x:
                os.path.getmtime(os.path.join(self.log_path, x)))
                log_list.reverse()
                num = 0
                for f in log_list:
                    num += 1
                    if num >= exp_log_num:
                        log_file = self.log_path + '/' + f
                        if os.path.isfile(log_file):
                            os.remove(log_file)
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/utils/window_canoe/test_canoe.py")
                print("ERROR: Delete log files failed!!!")
                print(e)


logger = logging.getLogger('test')


class feishu_api:
    def __init__(self, app_id="cli_a51121ad3bcad00c", app_secret=__import__("os").environ.get('XAT_CREDENTIAL_ECU__UTILS_WINDOW_CANOE_TEST_CANOE_PY_APP_SECRET', ""),
                 server_name="https://open.feishu.cn/", request_timeout=60):
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
        self.app_access_token = ""
        self.user_access_token = ""
        self.request_timeout = request_timeout
        self.get_tenant_access_token()

    def get_tenant_access_token(self, path="/open-apis/auth/v3/tenant_access_token/internal"):
        """
        自建应用获取 tenant_access_token

        :param path: api的请求地址
        """
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data = {'app_id': self.app_id, 'app_secret': self.app_secret}

        url = self.server_name + path
        response = requests.post(url, json.dumps(data), headers=headers, timeout=self.request_timeout)
        resp_body = json.loads(str(response.content, 'utf-8'))

        response_code = resp_body.get("code", 500)
        if response_code == 0:
            self.tenant_access_token = resp_body.get("tenant_access_token")
        else:
            logger.info(f"  feishu==>get_tenant_access_token:{resp_body}")

    def get_app_access_token(self, path="/open-apis/auth/v3/app_access_token/internal"):
        """
        自建应用获取 app_access_token

        :param path: api的请求地址
        """
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data = {'app_id': self.app_id, 'app_secret': self.app_secret}

        url = self.server_name + path
        response = requests.post(url, json.dumps(data), headers=headers, timeout=self.request_timeout)
        resp_body = json.loads(str(response.content, 'utf-8'))
        response_code = resp_body.get("code", 500)
        if response_code == 0:
            return resp_body.get("tenant_access_token")
        else:
            return None

    def get_user_access_token(self, path="open-apis/authen/v1/oidc/refresh_access_token"):
        """
        刷新 user_access_token

        :param path: api的请求地址
        """
        app_access_token = self.get_app_access_token()
        if app_access_token:
            flag, refresh_token_dict = get_soa_platform_refresh_token()
            headers = {'Content-Type': 'application/json; charset=utf-8',
                       'Authorization': f"Bearer {app_access_token}"}
            data = {'grant_type': "refresh_token", 'refresh_token': refresh_token_dict.get("remark")}

            url = self.server_name + path
            response = requests.post(url, json.dumps(data), headers=headers, timeout=self.request_timeout)
            try:
                resp_body = json.loads(response.text)
                response_code = resp_body.get("code", 500)
                if response_code == 0:
                    refresh_token_dict["remark"] = resp_body.get('data').get('refresh_token')
                    update_soa_platform_refresh_token(refresh_token_dict)  # 更新refresh_token的值
                    return resp_body.get("data").get("access_token")
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/utils/window_canoe/test_canoe.py")
                logger.info(f"刷新 user_access_token 失败")
                logger.info(f"异常堆栈：{traceback.format_exc()}")
                return None
        else:
            return None

    def add_mutilple_record_in_table(self, table_id, data: list, path="/open-apis/bitable/v1/apps/"):
        """
        该接口用于在数据表中新增多条记录，单次调用最多新增 500 条记录。
        """
        if len(data) == 0:
            return True, "待插入数据条数为0，无需插入"

        headers = {'Content-Type': 'application/json; charset=utf-8',
                   "Authorization": f"Bearer {self.tenant_access_token}"}
        url = self.server_name + path + f"{self.app_access_token}/tables/{table_id}/records/batch_create"
        body_data = []
        for data_row in data:
            body_data.append({"fields": data_row})
        else:
            body_data = {"records": body_data}
        response = requests.post(url, json.dumps(body_data), headers=headers, timeout=self.request_timeout)
        resp_body = json.loads(response.text)

        if resp_body.get("msg") == "FieldNameNotFound":
            body_data = {"fields": data}
            response = requests.post(url, json.dumps(body_data), headers=headers, timeout=self.request_timeout)
            resp_body = json.loads(response.text)
            logger.info(resp_body)
            if resp_body.get("code") == 0:
                return True, "表{table_id}，记录新增成功"
            else:
                logger.info(resp_body)
                return False, "表{table_id}，记录新增失败"
        if resp_body.get("code") == 0:
            return True, f"表{table_id} 新增记录：" + str(resp_body.get("msg"))
        else:
            logger.info(resp_body)
            return False, f"表{table_id} 新增记录失败"

    def get_user_open_id(self, name, path="open-apis/search/v1/user?"):
        """
        获取多维表格的数据表信息
        """
        user_access_token = self.get_user_access_token()
        if user_access_token:
            headers = {'Content-Type': 'application/json; charset=utf-8',
                       "Authorization": f"Bearer {user_access_token}"}
            url = self.server_name + path + f"query={name}&page_size=20"
            response = requests.get(url, headers=headers, timeout=self.request_timeout)
            resp_body = json.loads(response.text)
            if resp_body.get("code", 500) == 0:
                user_list = resp_body.get("data").get("users")
                if user_list:
                    for user in user_list:
                        if user.get('name') == name:
                            return user.get('open_id')
                else:
                    logger.info(f"    根据{name}获取user_id为空：{resp_body}")
                    return None
            else:
                logger.info(f"    根据{name}获取user_id失败：{resp_body}")
                return None
        else:
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

        response = requests.get(url, params=params, headers=headers, timeout=self.request_timeout)
        resp_body = json.loads(response.text)

        response_code = resp_body.get("code", 500)
        if response_code == 0:
            self.app_access_token = resp_body.get("data").get("node").get("obj_token")
        else:
            logger.info(f"  feishu==>get_bitable_app_access_token:{resp_body}")

    def get_bitable_table_ids(self, path="/open-apis/bitable/v1/apps/"):
        """
        获取多维表格的数据表信息
        """
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   "Authorization": f"Bearer {self.tenant_access_token}"}
        url = self.server_name + path + f"{self.app_access_token}/tables"
        response = requests.get(url, headers=headers, timeout=5)
        resp_body = json.loads(response.text)
        # logger.info(f"  feishu==>get_table_id_by_table_name: {resp_body}")
        return resp_body.get("data").get("items")

    def get_table_id_by_table_name(self, table_name):
        """
        根据数据表的中文名称获取其table_id

        :param table_name: 数据表的中文名称
        """
        # logger.info(f"  feishu==>get_table_id_by_table_name:{table_name}")
        tables_info = self.get_bitable_table_ids()
        for table_info in tables_info:
            if table_info['name'] == table_name:
                return table_info['table_id']
        else:
            return None

    def get_records_by_JobID(self, table_id, job_id, path="/open-apis/bitable/v1/apps/"):
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   "Authorization": f"Bearer {self.tenant_access_token}"}
        retry_num = 5
        result_list = []
        while retry_num > 0:
            retry_num -= 1
            try:
                url = self.server_name + path + f"{self.app_access_token}/tables/{table_id}/records"
                url_base = self.server_name + path + f"{self.app_access_token}/tables/{table_id}/records"
                data = {"filter": f'CurrentValue.JobID=\"{job_id}\"'}
                url += '?page_size=500'
                url_base += '?page_size=500'
                for key in data:
                    url += f"&{key}={data.get(key)}"
                    url_base += f"&{key}={data.get(key)}"
                res = []
                while True:
                    response = requests.get(url, headers=headers, timeout=self.request_timeout)
                    resp_body = json.loads(response.text)
                    if resp_body is not None:
                        if resp_body.get("data") is not None:
                            if resp_body.get("data").get("items") is not None:
                                res += [record for record in resp_body.get("data").get("items") if record is not None]
                        else:
                            break
                    else:
                        break
                    if resp_body["data"]["has_more"]:
                        url = url_base + f"?page_token={resp_body['data']['page_token']}"
                    else:
                        break
                # logger.info(f"表{table_id}查询到记录条数：{len(res)}")
                result_list = res
                break
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/utils/window_canoe/test_canoe.py")
                pass
        return result_list

    def get_records_in_table(self, table_id, path="/open-apis/bitable/v1/apps/", retry_max_num=5):
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   "Authorization": f"Bearer {self.tenant_access_token}"}
        url = self.server_name + path + f"{self.app_access_token}/tables/{table_id}/records"
        url_base = self.server_name + path + f"{self.app_access_token}/tables/{table_id}/records"
        res = []
        while True:
            retry_num = retry_max_num
            while retry_num > 0:
                retry_num -= 1
                try:
                    response = requests.get(url, headers=headers, timeout=self.request_timeout)
                    break
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/utils/window_canoe/test_canoe.py")
                    logger.info(f"飞书接口请求失败，5秒后第{retry_max_num - retry_num}重试, url：{url}, headers{headers}, ")
                    logger.info(traceback.format_exc())
                    time.sleep(10)
            else:  # 3次请求都失败，直接返回当前的查询结果
                return res
            resp_body = json.loads(response.text)
            if resp_body is not None:
                if resp_body.get("data") is not None:
                    if resp_body.get("data").get("items") is not None:
                        res += [record for record in resp_body.get("data").get("items") if record is not None]
            if resp_body["data"]["has_more"]:
                url = url_base + f"?page_token={resp_body['data']['page_token']}"
            else:
                break  # 退出最外层的while循环
        logger.info(f"  {table_id}下获取到的总记录数：{len(res)}")
        return res

    def delete_records_in_table(self, table_id, record_ids: list,
                                path="/open-apis/bitable/v1/apps/"):
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   "Authorization": f"Bearer {self.tenant_access_token}"}
        url = self.server_name + path + f"{self.app_access_token}/tables/{table_id}/records/batch_delete"
        body_data = {"records": record_ids}
        response = requests.post(url, json.dumps(body_data), headers=headers, timeout=self.request_timeout)

    def get_last_analysis_result(self, table_id, condition: dict, path="/open-apis/bitable/v1/apps/"):
        logger.info(f"查询条件: caseid={condition.get('caseid')}")
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   "Authorization": f"Bearer {self.tenant_access_token}"}
        url = self.server_name + path + f"{self.app_access_token}/tables/{table_id}/records"
        data = {"filter": f'CurrentValue.caseid=\"{condition.get("caseid")}\"'}
        url += '?page_size=500'
        for key in data:
            url += f"&{key}={data.get(key)}"
        response = requests.get(url, headers=headers, timeout=self.request_timeout)
        resp_body = json.loads(response.text)

        logger.info(f"表{table_id}查询到记录条数：{len(resp_body.get('data').get('items'))}")
        result_list = resp_body.get('data').get('items')
        if result_list:
            return result_list[-1]['fields'].get("问题分类"), result_list[-1]['fields'].get("问题描述")
        else:
            logger.info(f"用例{condition.get('caseid')}未查询到执行失败记录")
            return None, None

    def get_jira_issue_exist(self, table_id, condition: dict, path="/open-apis/bitable/v1/apps/"):
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   "Authorization": f"Bearer {self.tenant_access_token}"}
        url = self.server_name + path + f"{self.app_access_token}/tables/{table_id}/records"
        data = {"filter": f'CurrentValue.Jira链接=\"{condition.get("Jira链接")}\"'}
        url += '?page_size=500'
        for key in data:
            url += f"&{key}={data.get(key)}"
        response = requests.get(url, headers=headers, timeout=self.request_timeout)
        resp_body = json.loads(response.text)
        if resp_body.get('data').get('items') is not None:
            # logger.info(f"kwkwkw： {resp_body.get('data').get('items')}")
            return True, resp_body.get('data').get('items')[0]['record_id']
        else:
            return False, "0"

    def add_record_in_table(self, table_id, data: dict, path="/open-apis/bitable/v1/apps/"):
        """
        新增一条记录到数据中
        """
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   "Authorization": f"Bearer {self.tenant_access_token}"}
        url = self.server_name + path + f"{self.app_access_token}/tables/{table_id}/records"
        body_data = {"fields": data}
        response = requests.post(url, json.dumps(body_data), headers=headers, timeout=self.request_timeout)
        resp_body = json.loads(response.text)

        if resp_body.get("msg") == "FieldNameNotFound":
            body_data = {"fields": data}
            response = requests.post(url, json.dumps(body_data), headers=headers, timeout=self.request_timeout)
            resp_body = json.loads(response.text)
            logger.info(resp_body)
            if resp_body.get("code") == 0:
                return True, "表{table_id}，记录新增成功"
            else:
                logger.info(resp_body)
                return False, "表{table_id}，记录新增失败"
        if resp_body.get("code") == 0:
            return True, f"表{table_id} 新增记录：" + str(resp_body.get("msg"))
        else:
            logger.info(data)
            logger.info(resp_body)
            return False, f"表{table_id} 新增记录失败"


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


def parse_canoe_report_xml_new(canoe_report_xml):
    """解析canoe执行完成后生产的xml报告"""
    result = {"total": 0, "pass": 0, "fail": 0}
    with open(canoe_report_xml, 'r', encoding='utf-8') as f:
        xml_file = f.read()
        json_str1 = xml_to_json(xml_file)
        python_dict = json.loads(json_str1)
        if "testmodule" in python_dict:
            if "testgroup" in python_dict.get("testmodule"):
                pass_case_list = []
                fail_case_list = []
                result_dict = {}
                if isinstance(python_dict.get("testmodule").get("testgroup"), list):
                    group_list = python_dict.get("testmodule").get("testgroup")
                    for group in group_list:
                        if "testcase" in group:
                            testcase = group
                            if isinstance(testcase.get('testcase'), list):
                                for case in testcase.get('testcase'):
                                    logger.info(f"{case.get('ident')} 执行结果：{case.get('verdict').get('@result')}")
                                    result_dict[case.get('ident')] = case.get('verdict').get('@result')
                                else:
                                    for case_id in result_dict:
                                        if result_dict[case_id] == "pass":
                                            if case_id not in pass_case_list:
                                                pass_case_list.append(case_id)
                                        else:
                                            if case_id not in fail_case_list:
                                                fail_case_list.append(case_id)
                    else:
                        logger.info(f"pass num: {len(pass_case_list)}, fail num: {len(fail_case_list)}")
                        result["total"] = len(pass_case_list) + len(fail_case_list)
                        result["pass"] = len(pass_case_list)
                        result["fail"] = len(fail_case_list)
        return result


def insert_feishu_record(test_version, xml_name):
    test_version = test_version.replace(".bin", "")[-5:]
    result_dict = parse_canoe_report_xml_new(xml_name)
    feishu = feishu_api()
    feishu.get_bitable_app_access_token(document_id="R68Ewrx0jisYdykPwTTcyOjQnIh")
    table_id = feishu.get_table_id_by_table_name("CDC-MCU自动化测试数据")
    if table_id:
        feishu_insert_data = {"版本号": test_version, "Job类型": "CDC_MCU", "执行类型": "Smoke", "Full看板统计": "否"}
        user_id = feishu.get_user_open_id("O_shengcheng.xu")
        if user_id is not None:
            feishu_insert_data['负责人'] = [{'id': user_id}]
        feishu_insert_data["总数量"] = result_dict["total"]
        feishu_insert_data["Pass数量"] = result_dict["pass"]
        feishu_insert_data["Fail数量"] = result_dict["fail"]
        feishu.add_record_in_table(table_id, data=feishu_insert_data)


class MS_CONSTANT:
    MS_USERNAME = "bGRhcF9zb2FfamFtYQ=="

    MS_PASSWORD = __import__("os").environ.get('XAT_CREDENTIAL_ECU__UTILS_WINDOW_CANOE_TEST_CANOE_PY_MS_PASSWORD', "")


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
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/utils/window_canoe/test_canoe.py")
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

    def get_testcase_car_type(
            self, case_id, path="/track/test/case/get/"
    ):
        """
        执行结果(status)可选值：Pass、Failure、Blocking、Skip
        根据测试用例信息的 Id、nodeId、projectId 三个字段更新 testcase run result
        """
        if self.signin_flag:
            headers = {
                'CSRF-TOKEN': self.csrfToken,
                'PROJECT': "52c062de-78ea-41b4-8307-bed834cef1a7",
                'WORKSPACE': self.lastWorkspaceId,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                'Accept-Encoding': 'gzip, deflate',
                'X-AUTH-TOKEN': self.Cookie,
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Content-Type': 'application/json',
            }

            url = self.server_name + path + case_id
            response = requests.get(url, headers=headers)
            resp_body = json.loads(str(response.content, 'utf-8'))
            logger.info(resp_body)
            if resp_body and resp_body.get('success', "False"):
                if len(resp_body.get('data')) > 0:
                    jira_id_0 = resp_body.get('data').get('carType')
                    return jira_id_0
            else:
                return "[]"

    def get_testcase_test_step(
            self, case_id="0e9ca21e-1659-4f22-a063-047c270da782", path="/track/test/case/get/"
    ):
        """
        执行结果(status)可选值：Pass、Failure、Blocking、Skip
        根据测试用例信息的 Id、nodeId、projectId 三个字段更新 testcase run result
        """
        if self.signin_flag:
            headers = {
                'CSRF-TOKEN': self.csrfToken,
                'PROJECT': "52c062de-78ea-41b4-8307-bed834cef1a7",
                'WORKSPACE': self.lastWorkspaceId,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                'Accept-Encoding': 'gzip, deflate',
                'X-AUTH-TOKEN': self.Cookie,
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Content-Type': 'application/json',
            }

            url = self.server_name + path + case_id
            response = requests.get(url, headers=headers)
            resp_body = json.loads(str(response.content, 'utf-8'))
            valid_check_result = True
            valid_check_description = ""
            if resp_body and resp_body.get('success', "False"):
                if len(resp_body.get('data')) > 0:
                    steps = resp_body.get('data').get('steps')
                    if steps is None:
                        valid_check_result = False
                        valid_check_description = f"没有设置测试步骤"
                    else:
                        if len(steps) > 0:
                            steps_list = eval(steps)
                            # 从列表尾部开始遍历，删除空的步骤、预期结果
                            for hh in range(len(steps_list) - 1, -1, -1):
                                desc = steps_list[hh]['desc']
                                result = steps_list[hh]['result']
                                if len(desc) == 0 and len(result) == 0:
                                    steps_list.pop(hh)
                                else:
                                    break  # 只要步骤、预期结果有一个非空，则停止遍历，退出for循环

                            for step in steps_list:
                                num = step['num']
                                desc = step['desc']
                                result = step['result']
                                if num < len(steps_list) - 1:
                                    if desc is None:
                                        valid_check_result = False
                                        valid_check_description = f"第{num}步，测试步骤为空"
                                        break
                                    else:
                                        if len(desc.strip()) == 0:
                                            valid_check_result = False
                                            valid_check_description = f"第{num}步，测试步骤为空"
                                            break

                                    if result is None:
                                        valid_check_result = False
                                        valid_check_description = f"第{num}步，预期结果为空"
                                        break
                                    else:
                                        if len(result.strip()) == 0:
                                            valid_check_result = False
                                            valid_check_description = f"第{num}步，预期结果为空"
                                            break
                                else:  # 最后一步
                                    if desc is None:
                                        if result is not None:
                                            valid_check_result = False
                                            valid_check_description = f"第{num}步，测试步骤为空"
                                            break
                                        if len(result.strip()) > 0:
                                            valid_check_result = False
                                            valid_check_description = f"第{num}步，测试步骤为空"
                                            break
                                    else:
                                        if len(desc.strip()) == 0:  # 测试步骤长度为0
                                            if result is not None:
                                                valid_check_result = False
                                                valid_check_description = f"第{num}步，测试步骤为空"
                                                break
                                            if len(result.strip()) > 0:
                                                valid_check_result = False
                                                valid_check_description = f"第{num}步，测试步骤为空"
                                                break
                                        else:  # 测试步骤非空
                                            if result is None:
                                                valid_check_result = False
                                                valid_check_description = f"第{num}步，预期结果为空"
                                                break
                                            else:
                                                if len(result.strip()) == 0:
                                                    valid_check_result = False
                                                    valid_check_description = f"第{num}步，预期结果为空"
                                                    break
                        else:
                            valid_check_result = False
                            valid_check_description = "没有测试步骤信息"
                else:
                    valid_check_result = False
                    valid_check_description = "获取用例详细信息失败"

            else:
                valid_check_result = False
                valid_check_description = "获取用例详细信息失败"

            return valid_check_result, valid_check_description

    def get_testcases_in_project(self, projectId, hours=None, caseid=None):
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
            if caseid is not None:
                data['name'] = str(caseid)
            result = []
            itemCount = 0  # 用例总数
            i = 0
            review_result = {"Prepare": "未评审", "Pass": "通过", "Underway": "评审中"}
            while True:
                i += 1
                path = f"/track/test/case/list/{i}/50"
                url = self.server_name + path
                response = requests.post(
                    url, json.dumps(data), headers=headers, timeout=30
                )
                resp_body = json.loads(str(response.content, 'utf-8'))
                case_list = []
                for item in resp_body['data']["listObject"]:
                    timestamp = item.get("updateTime") // 1000 + 3600 * 8
                    maintainUser = item.get("maintainer", "")  # 用例的责任人
                    maintainUser_null = False
                    if maintainUser is not None:
                        if len(maintainUser) == 0:
                            maintainUser_null = True
                            maintainUser = item.get("createUser", "")
                    else:
                        maintainUser_null = True
                        maintainUser = item.get("createUser", "")
                    gmtime = time.gmtime(float(timestamp))
                    # 以“/Jazz” 或者 “/历史用例” 打头的不是SOA平台测试用例
                    if item.get("nodePath", "").startswith("/Jazz") or item.get("nodePath", "").startswith("/历史用例"):
                        continue
                    ms_case = {"caseId": item.get("num", "0"), "caseName": item.get("name", ""),
                               "id": item.get("id", "0"),
                               "nodePath": item.get("nodePath", ""),  # MS用例目录
                               "createUser": item.get("createUser", ""),
                               "maintainUser": maintainUser, "casePriority": item.get("priority", ""),
                               "projectName": item.get("projectName", ""), "applyScope": "",
                               "maintainUser_null": maintainUser_null,
                               "ifAutomation": "未设置", "caseTag": item.get("tags", ""),
                               "reviewStatus": review_result.get(item.get("reviewStatus", ""))  # 评审结果
                               # "updateTime": datetime.datetime.strftime("%Y-%m-%d %H:%M:%S", gmtime)
                               }
                    if item.get("fields") is not None:
                        for field in item.get("fields"):
                            if field["id"] in ["28c2da81-2e3d-484b-9171-b442369be69f",
                                               "1eb8b536-ef45-41cf-b090-42624dc84c0c",
                                               "c82ce452-4f09-4f16-a06b-9f8784438f33"
                                               ]:
                                ms_case["applyScope"] = field["value"].replace('"', "")  # Sanity
                                if ms_case["applyScope"] == 'f0ba27c6':
                                    ms_case["applyScope"] = "Full"
                                if ms_case["applyScope"] == 'f70ad4b6':
                                    ms_case["applyScope"] = "Full"
                                if '26d14d3d' in ms_case["applyScope"]:
                                    ms_case["applyScope"] = "Full"
                                if '2af80df8' in ms_case["applyScope"]:
                                    ms_case["applyScope"] = "Guard"
                                ms_case["applyScope"] = ms_case["applyScope"].replace('"', "").replace('\\', "")

                            if field["id"] == "99d14839-02cc-4d5b-b18f-284329730484":
                                if field["value"].replace('"', "").replace('\\', ''):  # 如果为空，则不设置
                                    ms_case["ifAutomation"] = field["value"].replace('"', "").replace('\\', '')
                    case_list.append(ms_case)
                if itemCount == 0:  # 仅赋值1次
                    itemCount = resp_body['data']['itemCount']
                if len(resp_body['data']["listObject"]) > 0:
                    result.extend(case_list)
                if len(resp_body['data']["listObject"]) < 50:
                    break
                if len(result) >= itemCount:
                    break
                time.sleep(0.1)
            logger.info(f"      预期获取用例总数：{itemCount}")
            logger.info(f"      实际有效用例总数：{len(result)}")
            return result

    def get_testcases_in_testPlan(self, planId="685acc3f-40e4-488a-b6cb-53bc5a32190b", projectId='', nodePath=None):
        """
        执行结果可选值：Pass、Failure、Blocking、Skip
        返回值类型：list，包含测试计划下的测试用例的 详细信息
        planId="685acc3f-40e4-488a-b6cb-53bc5a32190b"78d2ef95-cbb2-434d-9391-fd1677304010
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
            data = {"components": [], "planId": planId, "projectId": projectId, "selectAll": False, "combine": {
                "99d14839-02cc-4d5b-b18f-284329730484": {
                    "type": "select",
                    "operator": "in",
                    "value": ["Automated"]
                }
            }}
            i = 1
            result = []
            tem_data = None
            while True:
                path = f"/track/test/plan/case/list/{i}/100"
                url = self.server_name + path
                resp_body = None
                retry_num = 5
                while retry_num > 0:
                    retry_num -= 1
                    try:
                        response = requests.post(
                            url, json.dumps(data), headers=headers, timeout=30
                        )
                        resp_body = json.loads(str(response.content, 'utf-8'))
                        if resp_body['success']:
                            break
                    except Exception as e:  # 接口请求超时、返回结果转json异常、返回结果转JSON为None，则添加飞书异常表
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/utils/window_canoe/test_canoe.py")
                        time.sleep(5)

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

    def get_customnum_mappings_from_planid(self, planId):
        """
        planId: str  such as "685acc3f-40e4-488a-b6cb-53bc5a32190b"CUCD调试计划ID
        315af560-1d63-4d0b-9e42-2731b26b5669
        返回值类型: dict {customnum : (id, nodeId)}
        """
        if self.signin_flag:
            if planId:
                res = self.get_testcases_in_testPlan(planId)
                jama_id_mapping = {}  # 兼容存量测试用例的jama_id
                customnum_mappings = {}
                if res:
                    for data in res:
                        customNum = data.get("customNum")
                        ms_id = data.get("id")
                        nodeId = data.get("nodeId")
                        status = data.get("status")  # cases 执行状态
                        caseId = data.get("caseId")
                        priority = data.get("priority")
                        nodePath = data.get("nodePath")
                        if len(nodePath.split("/")) >= 4:
                            nodePath = nodePath.split("/")[3]
                        else:
                            nodePath = nodePath.split("/")[-1]
                        maintainer = data.get("maintainer")
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
                return customnum_mappings, jama_id_mapping

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
                "nodeId": nodeId,
                "updatedFileList": [],
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

                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/utils/window_canoe/test_canoe.py")
                    logger.warning(f"MS接口响应超时或者返回结果异常：{e.__str__()}")
                    logger.warning(f"MS回填失败，1秒后重新尝试回填")
                    time.sleep(5)
            return sync_ms_result


def iter_all_files_endswith(root_dir: str,
                            suffix: str
                            ) -> Generator[Tuple[str, str], None, None]:
    """遍历根目录(root_dir)及其子目录下所有指定后缀(suffix)的文件

    Parameters
    ----------
    root_dir : str
        需要遍历的文件夹的路径
    suffix : str
        目标文件后缀

    Yields
    -------
    Tuple[str, str]
        文件所在路径和文件名
    """
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(suffix):
                yield root, file


ms_project_dict = {"BGM": "1fbbeb47-6cc7-48bd-aafc-24349853e9d8", "TCAM": "225ebd89-8c9c-48dd-a3d8-739e52ee76e2",
                   "SOA": "52c062de-78ea-41b4-8307-bed834cef1a7", "BGM-MCU": "7cf5bac0-7cee-4b73-882b-f53fd8ff859d",
                   "CDC": "c8fc5cb7-5a55-41a8-8f04-e43164e3878a"}


def get_testcase_by_tag(project_name, tag):
    client = meterSphere_client()
    query_result = []
    ms_case_query_result = client.get_testcases_in_project(ms_project_dict.get(project_name), 48)
    for case in ms_case_query_result:
        if tag in eval(case['caseTag']):
            logger.info(case)
            logger.info(f"{case['caseId']}=={case['caseTag']}")
            query_result.append(case)
    else:
        return query_result


def xml_to_json(xml_str: str):
    xml_parse = xmltodict.parse(xml_str)
    json_str = json.dumps(xml_parse, indent=4)
    return json_str


def json_to_xml(obj_dict: dict):
    # 使用 pretty=True 选项来输出格式化的 XML
    xml_str = xmltodict.unparse(obj_dict, pretty=True)
    return xml_str


def create_canoe_run_xml(canoe_vxt_module_file, plan_id, project_name="CDC", tag="canoe"):
    """根据canoe的模版文件生成对应的xml文件"""
    client = meterSphere_client()
    query_result, _ = client.get_customnum_mappings_from_planid(planId=plan_id)
    logger.info(query_result)
    global ms_query_result
    ms_query_result = query_result.copy()
    with open(canoe_vxt_module_file, 'r') as f:
        xml_file = f.read()
        json_str1 = xml_to_json(xml_file)
        python_dict = json.loads(json_str1)
        python_dict['testmodule']['testgroup'] = []
        sequence = 1000
        for case in query_result:  # 遍历从测试计划获取的用例
            sequence += 1
            for test_group in python_dict['testmodule']['testgroup']:
                if query_result[case][5] == test_group['@title']:
                    test_group["capltestcase"].append({'@name': f'Test_{case}',
                                                       '@title': f'test_{case}',
                                                       '@ident': f'TC-{sequence}'})
                    break  # 跳过else部分
            else:  # 没有找到匹配的组
                python_dict['testmodule']['testgroup'].append({'@title': query_result[case][5],
                                                               'description': f'This test group: {query_result[case][5]}',
                                                               'capltestcase': [
                                                                   {'@name': f'Test_{case}', '@title': f'test_{case}',
                                                                    '@ident': f'TC-{sequence}'}]})
        # python 字典对象转xml
        with open(os.path.join(xml_file_path, xml_file_name), 'w', encoding="utf-8") as new_file:
            new_file.write(json_to_xml(python_dict))


def parse_canoe_report_xml(canoe_report_xml):
    """解析canoe执行完成后生产的xml报告"""
    with open(canoe_report_xml, 'r') as f:
        xml_file = f.read()
        json_str1 = xml_to_json(xml_file)
        logger.info(json_str1)
        python_dict = json.loads(json_str1)
        if "testmodule" in python_dict:
            if "testgroup" in python_dict.get("testmodule"):
                for testcase in python_dict.get("testmodule").get("testgroup"):
                    if isinstance(testcase.get('testcase'), dict):
                        logger.info(f"{testcase.get('testcase').get('ident')}")
                        logger.info(f"{testcase.get('testcase').get('verdict').get('@result')}")
                    if isinstance(testcase.get('testcase'), list):
                        for case in testcase.get('testcase'):
                            logger.info(f"{case.get('ident')} 执行结果：{case.get('verdict').get('@result')}")


def _generate_xml_module(plan_id) -> None:
    create_canoe_run_xml("CANoeDemo_base.vxt", project_name="CDC", tag="canoe", plan_id=plan_id)


def _run_test() -> None:
    logging.info(app.version)
    component_list = []
    # r"C:\Users\songjian.lin\Downloads\testPOCV15\Lib"
    # for key, value in iter_all_files_endswith(os.path.join(component_base_for_add, "Lib"), 'dll'):
    #     component_list.append(os.path.join(key, value))
    # for key, value in iter_all_files_endswith(os.path.join(component_base_for_add, "Lib"), 'DLL'):
    #     component_list.append(os.path.join(key, value))
    # for key, value in iter_all_files_endswith(os.path.join(component_base_for_add, "TestCases"), 'can'):
    #     component_list.append(os.path.join(key, value))
    component_list.append(capl_file_path)  # 默认加载的can文件
    app.insert_XML_module(env_name, env_path, os.path.join(
        xml_file_path, xml_file_name), component_list)

    # 创建一个线程，启动一个socket客户端，连接sat的服务端，当需要对台架做操作时，发送对应的操作指令（操作指令的格式待定）
    # 其中socket server的IP、PORT保存在数据库里

    app.save(save2cfg)
    app.load_test_setup()
    app.start()
    app.run_test_modules()
    logging.info("< All test finished,ready to stop canoe >")
    app.stop()  # 暂不停止


def get_willow_task_json(task_dir, key):
    path = os.path.join(task_dir, "task.json")
    with open(path, 'r') as f:
        data = json.load(f)
    try:
        print(f"task.json {key}的数据为:{data[key]}")
        return str(data[key])
    except KeyError as e:
        print(f"task.json {key}的数据为不存在")
        raise Exception(e)


def main() -> None:
    global plan_id
    plan_id = '685acc3f-40e4-488a-b6cb-53bc5a32190b'
    test_version = "V3.0.0 AN"
    '''
    CICD调试：685acc3f-40e4-488a-b6cb-53bc5a32190b
    
    '''
    # 适配willow获取参数
    if 'autotest' in os.getcwd():
        plan_id = get_willow_task_json(os.getcwd(), 'plan_id')
        img_url = get_willow_task_json(os.getcwd(), 'img_url')  # to do
    else:
        img_url = "默认版本"
    target_dir = r"C:\Users\lei.an\AppData\Local\Temp\gen_py"
    # if os.path.exists(target_dir):
    #     # 使用shutil.rmtree删除目录及其所有内容
    #     # shutil.rmtree(target_dir)
    #     delete_directory(target_dir)
    #     print(f"Directory {target_dir} has been removed.")
    global install_dir
    # step1、下载最新的工程代码
    # git_clone('https://jidudev.com/soa/soa_test/soa_vector_proj.git', install_dir)
    git_pull(base_path)   # //
    # step2、从MS 更加项目的tag更新工程TestCases目录下的CANoeDemo.vxt
    _generate_xml_module(plan_id)
    # step3、 run testcases
    # 删除报告：.html、.xml
    _run_test()    # //

    # Third step, quit canoe
    # report_path = xml_file_path
    # report_name = "CANoeDemo_report.xml"
    # report = os.path.join(report_path, report_name)
    # print(f"报告信息：{report}")
    # parse_canoe_report_xml(report)
    # time.sleep(5)
    # step4、解析执行结果报告，并回填MS
    client = meterSphere_client()
    sync_ms = {"fail": "Fail", "pass": "Pass"}
    time.sleep(10)

    result_xml = r"D:\Git\soa_vector_proj\CDC_MCU_BaseTest\08_TestReport&Log\PlatformBasedTest_report.xml"
    insert_feishu_record(img_url, result_xml)

    with open(result_xml, 'r',
              encoding='utf-8') as f:
        xml_file = f.read()
        json_str1 = xml_to_json(xml_file)
        python_dict = json.loads(json_str1)
        finish_plan_id_list = []
        with open("finish.pickle", 'rb') as f:
            data_bytes = f.read()
            finish_plan_id_list = pickle.loads(data_bytes)
        # if plan_id in finish_plan_id_list:
        #     return
        # else:
        #     finish_plan_id_list.appen(plan_id)
        #logger.info(python_dict['testmodule']['testgroup']['testcase'])
        # if isinstance(python_dict['testmodule']['testgroup']['testcase'], dict):
        #     logger.info(python_dict['testmodule']['testgroup']['testcase']['verdict']['@result'])
        #     logger.info(python_dict['testmodule']['testgroup']['testcase']['title'])
        #     logger.info(f"测试结果为{ms_query_result}")
        #     case_id = python_dict['testmodule']['testgroup']['testcase']['title'].replace('test_', '')
        #     logger.info(case_id)
        #     logger.info("000000000000000")
        #     logger.info(ms_query_result.get(f"{case_id}"))
        #     client.set_testcase_status_in_testPlan(ms_query_result.get(f"{case_id}")[0],
        #                                            ms_query_result.get(f"{case_id}")[1],
        #                                            sync_ms.get(
        #                                                python_dict['testmodule']['testgroup']['testcase']['verdict'][
        #                                                    '@result']),
        #                                            ms_query_result.get(f"{case_id}")[3])
        #
        #     logger.info("------------------------")
        # if isinstance(python_dict['testmodule']['testgroup']['testcase'], list):
        #     logger.info(f"测试结果为{ms_query_result}")
        #     for item in python_dict['testmodule']['testgroup']['testcase']:
        #         logger.info(item['verdict']['@result'])
        #         logger.info(item['title'])
        #         case_id = item['title'].split("_")[1]
        #         logger.info(f"case_id: {case_id}")
        #         logger.info(ms_query_result.get(f"{case_id}"))
        #         client.set_testcase_status_in_testPlan(ms_query_result.get(f"{case_id}")[0],
        #                                                ms_query_result.get(f"{case_id}")[1],
        #                                                sync_ms.get(item['verdict']['@result']),
        #                                                ms_query_result.get(f"{case_id}")[3])
        #         logger.info("------------------------")

        if "testmodule" in python_dict:
            if "testgroup" in python_dict.get("testmodule"):
                result_dict = {}
                if isinstance(python_dict.get("testmodule").get("testgroup"), list):
                    group_list = python_dict.get("testmodule").get("testgroup")
                    for group in group_list:
                        if "testcase" in group:
                            testcase = group
                            if isinstance(testcase.get('testcase'), list):
                                for case in testcase.get('testcase'):
                                    logger.info(f"{case.get('ident')} 执行结果：{case.get('verdict').get('@result')}")
                                    result_dict[case.get('ident')] = case.get('verdict').get('@result')
                                else:
                                    for case_id in result_dict:
                                        client.set_testcase_status_in_testPlan(ms_query_result.get(f"{case_id}")[0],
                                                                               ms_query_result.get(f"{case_id}")[1],
                                                                               sync_ms.get(
                                                                                   python_dict['testmodule'][
                                                                                       'testgroup']['testcase'][
                                                                                       'verdict'][
                                                                                       '@result']),
                                                                               ms_query_result.get(f"{case_id}")[3])

        finish_plan_id_list.append(plan_id)
        data = pickle.dumps(finish_plan_id_list)
        with open("finish.pickle", 'wb') as f:
            f.write(data)

    # app.quit()

def git_pull(directory):
    """
    切换到指定目录并执行git pull操作。
    :param directory: 要切换到的目录。
    """
    try:
        logger.info(f"git pull dir: {directory}")
        # 切换目录
        os.chdir(directory)
        # 执行git pull命令
        subprocess.run(['git', 'pull'], check=True)
        print(f"已在目录 {directory} 执行git pull成功。")
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/utils/window_canoe/test_canoe.py")
        print(f"执行git pull时发生错误: {e}")
    finally:
        # 切换回原目录
        os.chdir(os.path.abspath(os.path.dirname(__file__)))


if __name__ == '__main__':
    # sat框架创建一个需window slave端任务执行的任务，同时创建一个socket server端，监听slave端需要协助执行的台架操作指令；
    main()
    # app.start()
    insert_feishu_record("test", r"D:\share\1128\PlatformBasedTest_report.xml")  # 测试使用
