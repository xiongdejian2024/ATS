# -*- coding: utf-8 -*-

"""
@Time    : 2022/5/24 11:26 下午
@Author  : songjian.lin
@Email   : songjian.lin@jiduauto.com
"""
import datetime
import json
import os
import sys
import time
import traceback
import requests

current_path = os.path.dirname(os.path.realpath(__file__))
from xat_ecu.legacy.common.logger import logger, Logger
from xat_ecu.legacy.sdk.decorator.exception_handler import monitor
from xat_ecu.legacy.interface.vo import data_request

user_id_dict = {}


class feishu_api:
    def __init__(self, app_id="cli_a51121ad3bcad00c", app_secret=__import__("os").environ.get('XAT_CREDENTIAL_ECU__INTERFACE_FEISHU_FEISHU_API_PY_APP_SECRET', ""),
                 server_name="https://open.feishu.cn/", request_timeout=60, retry_number=5, retry_interval=10):
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
        self.sheet_ids = []
        self.sheet_titles = []
        self.request_timeout = request_timeout
        self.retry_number = retry_number
        self.retry_interval = retry_interval
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
                    logger.info(f'获取到的user_access_token值为：{resp_body.get("data").get("access_token")}')
                    refresh_token_dict["remark"] = resp_body.get('data').get('refresh_token')
                    update_soa_platform_refresh_token(refresh_token_dict)  # 更新refresh_token的值
                    return resp_body.get("data").get("access_token")
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/feishu/feishu_api.py")
                logger.info(f"刷新 user_access_token 失败")
                logger.info(f"异常堆栈：{traceback.format_exc()}")
                return None
        else:
            return None

    def get_user_open_id(self, name, path="open-apis/search/v1/user?"):
        """
        获取多维表格的数据表信息
        """
        if name in user_id_dict:
            return user_id_dict.get(name)
        else:
            user_access_token = self.get_user_access_token()
            logger.info(f"user_access_token:{user_access_token}")
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
                                user_id_dict[name] = user.get('open_id')
                                return user.get('open_id')
                    else:
                        logger.info(f"根据{name}获取user_id为空：{resp_body}")
                        return None
                else:
                    logger.info(f"根据{name}获取user_id失败：{resp_body}")
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
            self.app_access_token = ""

    def get_bitable_table_ids(self, path="/open-apis/bitable/v1/apps/"):
        """
        获取多维表格的数据表信息
        """
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   "Authorization": f"Bearer {self.tenant_access_token}"}
        url = self.server_name + path + f"{self.app_access_token}/tables"
        response = requests.get(url, headers=headers, timeout=self.request_timeout)
        resp_body = json.loads(response.text)

        return resp_body.get("data").get("items")

    @monitor()
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

    def get_records_in_table(self, table_id, path="/open-apis/bitable/v1/apps/", retry_max_num=3):
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   "Authorization": f"Bearer {self.tenant_access_token}"}
        url = self.server_name + path + f"{self.app_access_token}/tables/{table_id}/records"
        url_base = self.server_name + path + f"{self.app_access_token}/tables/{table_id}/records"
        res = []
        while True:
            retry_num = self.retry_number
            while retry_num > 0:
                retry_num -= 1
                try:
                    response = requests.get(url, headers=headers, timeout=self.request_timeout)
                    break
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/feishu/feishu_api.py")
                    logger.info(f"飞书接口请求失败，5秒后第{self.retry_number - retry_num}重试")
                    time.sleep(self.retry_interval)
            else:
                return res
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

    def get_last_analysis_result(self, table_id, condition: dict, path="/open-apis/bitable/v1/apps/"):
        logger.info(f"查询条件: caseid={condition.get('caseid')}")
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   "Authorization": f"Bearer {self.tenant_access_token}"}
        url = self.server_name + path + f"{self.app_access_token}/tables/{table_id}/records"
        url_base = self.server_name + path + f"{self.app_access_token}/tables/{table_id}/records"
        data = {"filter": f'CurrentValue.caseid=\"{condition.get("caseid")}\"'}
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
            logger.info(resp_body)
            if resp_body["data"]["has_more"]:
                url = url_base + f"?page_token={resp_body['data']['page_token']}"
            else:
                break
        logger.info(f"表{table_id}查询到记录条数：{len(res)}")
        result_list = res
        if result_list:
            return result_list[-1]['fields'].get("问题分类"), result_list[-1]['fields'].get("问题描述")
        else:
            logger.info(f"用例{condition.get('caseid')}未查询到执行失败记录")
            return None, None

    def get_all_records_in_table(self, table_id, path="/open-apis/bitable/v1/apps/"):
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   "Authorization": f"Bearer {self.tenant_access_token}"}
        url = self.server_name + path + f"{self.app_access_token}/tables/{table_id}/records"
        url_base = self.server_name + path + f"{self.app_access_token}/tables/{table_id}/records"
        res = []
        while True:
            response = requests.get(url, headers=headers, timeout=self.request_timeout)
            resp_body = json.loads(response.text)
            if resp_body is not None:
                if resp_body.get("data") is not None:
                    if resp_body.get("data").get("items") is not None:
                        res += [record for record in resp_body.get("data").get("items") if record is not None]
            logger.debug(resp_body)
            if resp_body["data"]["has_more"]:
                url = url_base + f"?page_token={resp_body['data']['page_token']}"
            else:
                break
        return res

    @monitor()
    def add_record_in_table(self, table_id, data: dict, path="/open-apis/bitable/v1/apps/"):
        """
        新增一条记录到数据中
        """
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   "Authorization": f"Bearer {self.tenant_access_token}"}
        try:
            if "caseid" in data:
                if data["MS目录"].startswith("/TCAM"):  # TCAM失败自动化用例获取该用例上次的分析结果
                    data["问题分类"], data["问题描述"] = self.get_last_analysis_result(table_id, data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/feishu/feishu_api.py")
            logger.info("获取问题分类、问题描述失败")
        url = self.server_name + path + f"{self.app_access_token}/tables/{table_id}/records"
        body_data = {"fields": data}
        response = requests.post(url, json.dumps(body_data), headers=headers, timeout=self.request_timeout)
        resp_body = json.loads(response.text)
        if resp_body.get("msg") == "FieldNameNotFound":
            body_data = {"fields": data}
            response = requests.post(url, json.dumps(body_data), headers=headers, timeout=self.request_timeout)
            resp_body = json.loads(response.text)
            if resp_body.get("code") == 0:
                return True, "表{table_id}，记录新增成功"
            else:
                return False, "表{table_id}，记录新增失败"
        if resp_body.get("code") == 0:
            return True, resp_body.get("data").get("record").get("record_id")
        else:
            return False, f"表{table_id} 新增记录失败，失败信息：{resp_body}"

    def add_mutilple_record_in_table(self, table_id, data: list, path="/open-apis/bitable/v1/apps/"):
        """
        该接口用于在数据表中新增多条记录，单次调用最多新增 500 条记录。
        """
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

    def update_record_in_table(self, table_id, record_id, data: dict, path="/open-apis/bitable/v1/apps/"):
        """
        更新记录到数据表中
        """
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   "Authorization": f"Bearer {self.tenant_access_token}"}
        url = self.server_name + path + f"{self.app_access_token}/tables/{table_id}/records/{record_id}"
        data = {"fields": data}
        response = requests.put(url, json.dumps(data), headers=headers, timeout=self.request_timeout)
        resp_body = json.loads(response.text)
        if resp_body.get("code") == 0:
            logger.info(f"表{table_id} 更新记录{record_id}：" + str(resp_body.get("msg")))
            return True, "执行结果更新成功"
        else:
            logger.info(f"表{table_id} 更新记录失败")
            return False, "执行结果更新失败"

    def delete_records_in_table(self, table_id, record_ids: list, path="/open-apis/bitable/v1/apps/"):
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   "Authorization": f"Bearer {self.tenant_access_token}"}
        url = self.server_name + path + f"{self.app_access_token}/tables/{table_id}/records/batch_delete"
        body_data = {"records": record_ids}
        response = requests.post(url, json.dumps(body_data), headers=headers, timeout=self.request_timeout)
        resp_body = json.loads(response.text)
        logger.info(f"删除结果：{resp_body}")

    # def update_file_in_record_in_table(self, table_id, record_id, file_path):
    #     """
    #     上传附件到数据表中
    #     """
    #     headers = {'Content-Type': 'application/json; charset=utf-8',
    #                "Authorization": f"Bearer {self.tenant_access_token}"}
    #     file_size = os.path.getsize(file_path)
    #     url = "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all"
    #     form = {'file_name': os.path.basename(file_path),
    #             'parent_type': 'bitable_file',
    #             'parent_node': self.app_access_token,
    #             'size': str(file_size),
    #             'file': (open(file_path, 'rb'))}
    #     multi_form = MultipartEncoder(form)
    #     headers['Content-Type'] = multi_form.content_type
    #     response = requests.request("POST", url, headers=headers, data=multi_form)
    #     resp_body = json.loads(response.text)
    #     if resp_body['code'] == 0:
    #         logger.info(f"上传成功：{resp_body['data']['file_token']}")
    #         self.update_record_in_table(table_id, record_id, {"附件": [{"file_token": resp_body['data']['file_token']}]})

    def get_data_table_in_document_id(self, path="/open-apis/bitable/v1/apps/"):
        """
        获取该飞书文档下的数据表的名称
        """
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   "Authorization": f"Bearer {self.tenant_access_token}"}
        url = self.server_name + path + f"{self.app_access_token}/tables"
        response = requests.get(url, headers=headers, timeout=self.request_timeout)
        resp_body = json.loads(response.text)
        logger.info(resp_body)
        table_name_list = []
        if resp_body.get("code") == 0:
            for data_table in resp_body['data']['items']:
                table_name_list.append(data_table['name'])
            return True, table_name_list
        else:
            logger.info(f"失败")
            return False, table_name_list

    def add_data_table_in_document_id(self, table_name, field_list, path="/open-apis/bitable/v1/apps/"):
        """
            添加数据表
        """

        headers = {'Content-Type': 'application/json; charset=utf-8',
                   "Authorization": f"Bearer {self.tenant_access_token}"}
        url = self.server_name + path + f"{self.app_access_token}/tables"
        data = {"table": {"name": table_name, "default_view_name": "默认的表格视图", "fields": field_list}}
        response = requests.post(url, json.dumps(data), headers=headers, timeout=self.request_timeout)
        resp_body = json.loads(response.text)
        logger.info(resp_body)

    def add_field_in_data_table(self, table_id, field_dict, path="/open-apis/bitable/v1/apps/"):
        """
            添加数据表的字段
        """
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   "Authorization": f"Bearer {self.tenant_access_token}"}
        url = self.server_name + path + f"{self.app_access_token}/tables/{table_id}/fields"
        response = requests.post(url, json.dumps(field_dict), headers=headers, timeout=self.request_timeout)
        resp_body = json.loads(response.text)
        logger.info("字段添加结果：" + str(resp_body))

    def get_field_in_document_id(self, table_id: object, path: object = "/open-apis/bitable/v1/apps/") -> object:
        """
        获取数据表的字段
        """
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   "Authorization": f"Bearer {self.tenant_access_token}"}
        url = self.server_name + path + f"{self.app_access_token}/tables/{table_id}/fields"
        response = requests.get(url, headers=headers, timeout=self.request_timeout)
        resp_body = json.loads(response.text)
        logger.info(resp_body)
        if resp_body.get("code") == 0:
            return True, resp_body.get('data').get('items')
        else:
            logger.info(f"失败")
            return False, []

    def batch_update_record_in_table(self, table_id, record_id_list, data_list, path="/open-apis/bitable/v1/apps/"):
        """
        更新记录到数据表中
        data 的key为record_id
        """
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   "Authorization": f"Bearer {self.tenant_access_token}"}
        url = self.server_name + path + f"{self.app_access_token}/tables/{table_id}/records/batch_update"
        data = {"records": []}
        for item_record_id, item_row in zip(record_id_list, data_list):
            data["records"].append({"record_id": item_record_id, "fields": item_row})
        if len(data["records"]) > 0:
            response = requests.post(url, json.dumps(data), headers=headers, timeout=self.request_timeout)
            resp_body = json.loads(response.text)
            if resp_body.get("code") == 0:
                return True, "执行结果更新成功"
            else:
                logger.info(f"表{table_id} 更新记录失败")
                return False, "执行结果更新失败"

    def get_views_in_table(self, table_id, path="/open-apis/bitable/v1/apps/"):
        """
        获取数据表的视图
        """
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   "Authorization": f"Bearer {self.tenant_access_token}"}
        url = self.server_name + path + f"{self.app_access_token}/tables/{table_id}/views"
        response = requests.get(url, headers=headers, timeout=self.request_timeout)
        resp_body = json.loads(response.text)
        logger.info(resp_body)
        if resp_body.get("code") == 0:
            return True, resp_body.get('data').get('items')
        else:
            logger.info(f"失败")
            return False, []

    def add_view_in_table(self, table_id, view_name, path="/open-apis/bitable/v1/apps/"):
        """
        新增数据表的视图
        """
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   "Authorization": f"Bearer {self.tenant_access_token}"}
        url = self.server_name + path + f"{self.app_access_token}/tables/{table_id}/views"
        data = {"view_name": view_name, "view_type": "grid"}
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=self.request_timeout)
        resp_body = json.loads(response.text)
        logger.info(resp_body)
        if resp_body.get("code") == 0:
            return True, resp_body.get('data').get('view').get('view_id')
        else:
            logger.info(f"失败")
            return False, []

    def update_view_in_table(self, table_id, view_id, field_id, path="/open-apis/bitable/v1/apps/"):
        """
        更新数据表的视图
        """
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   "Authorization": f"Bearer {self.tenant_access_token}"}
        url = self.server_name + path + f"{self.app_access_token}/tables/{table_id}/views/{view_id}"
        today = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month,
                                  datetime.datetime.now().day)

        data = {
            "property": {
                "filter_info": {
                    "conditions": [
                        {
                            "field_id": field_id,
                            "operator": "is",
                            "value": f'["ExactDate",{int(today.timestamp() * 1000)}]'
                        }
                    ],
                    "conjunction": "and"
                },
            }
        }
        response = requests.patch(url, headers=headers, data=json.dumps(data), timeout=self.request_timeout)
        resp_body = json.loads(response.text)
        logger.info(resp_body)
        if resp_body.get("code") == 0:
            return True, resp_body.get('data').get('items')
        else:
            logger.info(f"失败")
            return False, []

    def search_view_in_table(self, table_id, view_id, path="/open-apis/bitable/v1/apps/"):
        """
        检索数据表的视图
        """
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   "Authorization": f"Bearer {self.tenant_access_token}"}
        url = self.server_name + path + f"{self.app_access_token}/tables/{table_id}/views/{view_id}"
        response = requests.get(url, headers=headers, timeout=self.request_timeout)
        resp_body = json.loads(response.text)
        logger.info(resp_body)
        if resp_body.get("code") == 0:
            return True, resp_body.get('data').get('view').get('property')
        else:
            logger.info(f"失败")
            return False, []

    def get_spreadsheets_info(self, path="/open-apis/sheets/v3/spreadsheets/", spreadsheet_token=None):
        """
        获取电子表格的字段信息
        """
        headers = {"Authorization": f"Bearer {self.tenant_access_token}"}
        url = self.server_name + path + f"{spreadsheet_token}/sheets/query"
        # response = requests.get(url, headers=headers, timeout=60)
        # resp_body = json.loads(response.text)
        resp_body = data_request.DataRequest().get(url, headers=headers, timeout=self.request_timeout)
        # print(resp_body)
        if resp_body.get("code") == 0:
            # 将工作表id用数组存起来
            self.sheet_ids = [sheet_info['sheet_id'] for sheet_info in resp_body['data']['sheets']]
            self.sheet_titles = [sheet_info['title'] for sheet_info in resp_body['data']['sheets']]
            logger.info(f"sheet_ids:{self.sheet_ids}")
            logger.info(f"sheet_titles:{self.sheet_titles}")

    def get_spreadsheets_signal_value(self, path="/open-apis/sheets/v2/spreadsheets/", spreadsheet_token=None,
                                      sheet_id=None, start="C2", end="J200"):
        """
        获取电子表格中指定字段的数值
        
        Args:
            path (str, optional): 电子表格API的URL路径. 默认为"/open-apis/sheets/v2/spreadsheets/".
            spreadsheet_token (str, optional): 电子表格的唯一标识. 默认为None.
            sheet_id (str, optional): 需要查询的sheet的ID. 默认为None.
            start (str, optional): 查询的起始单元格位置. 默认为"C2".
            end (str, optional): 查询的结束单元格位置. 默认为"I200".
        
        Returns:
            Any: 返回查询到的字段数值，如果未找到则返回None
        
        """
        headers = {"Authorization": f"Bearer {self.tenant_access_token}",
                   "Content-Type": "application/json; charset=utf-8"}
        if end is None:
            end = start
        url = self.server_name + path + f"{spreadsheet_token}/values/{sheet_id}!{start}:{end}?valueRenderOption=ToString"
        # response = requests.get(url, headers=headers, timeout=60)
        # resp_body = json.loads(response.text)
        resp_body = data_request.DataRequest().get(url, headers=headers, timeout=self.request_timeout)
        if resp_body.get("code") == 0:
            if resp_body.get("data") is not None:
                if resp_body.get("data").get("valueRange") is not None:
                    values = resp_body.get("data").get("valueRange").get("values")
                    return values

    def update_spreadsheets_value(self, path="/open-apis/sheets/v2/spreadsheets/", spreadsheet_token=None,
                                  sheet_id=None, start=None, end=None, value: list = [["PASS"]]):
        """
        更新电子表格中指定单元格范围的数值
        
        Args:
            path (str, optional): 电子表格API的URL路径. 默认为"/open-apis/sheets/v2/spreadsheets/".
            spreadsheet_token (str, optional): 电子表格的唯一标识. 默认为None.
            sheet_id (str, optional): 需要更新的工作表ID. 默认为None.
            start (str, optional): 起始单元格位置，格式为"A1". 默认为None.
            end (str, optional): 结束单元格位置，格式为"B2". 默认为None.
            value (list, optional): 需要更新的单元格值，二维列表，例如[["value1", "value2"], ["value3", "value4"]]. 默认为[["PASS"]].
        
        Returns:
            tuple: 包含两个元素的元组，第一个元素为bool类型，表示更新是否成功；第二个元素为str类型，表示更新操作的提示信息。
        
        """
        headers = {"Authorization": f"Bearer {self.tenant_access_token}",
                   "Content-Type": "application/json; charset=utf-8"}
        url = self.server_name + path + f"{spreadsheet_token}/values"
        if end is None:
            end = start
        data = {
            "valueRange": {
                "range": f"{sheet_id}!{start}:{end}",
                "values": value
            }
        }
        # response = requests.put(url, headers=headers, data=json.dumps(data), timeout=60)
        # resp_body = json.loads(response.text)
        resp_body = data_request.DataRequest().put(url, headers=headers, data=json.dumps(data),
                                                   timeout=self.request_timeout)
        code = resp_body.get("code")
        msg = resp_body.get("msg")
        if code == 0:
            logger.info(f"新增sheet id为：{sheet_id} sheet中{start}:{end}为: {value}成功,{msg}")
        else:
            logger.warning(f"新增sheet id为：{sheet_id} sheet中{start}:{end}为: {value}失败，请检查,{msg}")

    def get_spreadsheet_name(self, sheet_id):
        """
        获取工作表名称
        Args:
            sheet_id (str): 需要查询的工作表ID.
        Returns:
            str: 返回查询到的工作表名称，如果未找到则返回None
        """
        try:
            id_index = self.sheet_ids.index(sheet_id)
            return self.sheet_titles[id_index]
        except ValueError:
            return None


@monitor()
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


@monitor()
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


@monitor(True)
def update_or_add_feishu_table(table_name, run_result: dict, document_id="R68Ewrx0jisYdykPwTTcyOjQnIh"):
    """
    根据willow上测试任务的执行结果更新飞书的对应多维表格

    :param table_name: 多维表格的中文名称
    :param run_result: willo上job的执行结果
    :param document_id: 多维表格所在文档空间的文档ID
    """
    query_dict = {}

    if "版本号" not in run_result:
        return False, "执行结果的'版本号'字段不存在"
    elif run_result.get("版本号") is None:
        return False, "执行结果的'版本号'字段值不能为空"
    else:
        query_dict["版本号"] = run_result.get("版本号")

    if "Job类型" not in run_result:
        return False, "执行结果的'Job类型'字段不存在"
    elif run_result.get("Job类型") is None:
        return False, "执行结果的'Job类型'字段值不能为空"
    else:
        query_dict["Job类型"] = run_result.get("Job类型")

    if "执行类型" not in run_result:
        return False, "执行结果的'执行类型'字段不存在"
    elif run_result.get("执行类型") is None:
        return False, "执行结果的'执行类型'字段值不能为空"
    else:
        query_dict["执行类型"] = run_result.get("执行类型")
    if "负责人" not in run_result:
        return False, "执行结果的'负责人'字段不存在"
    elif run_result.get("负责人") is None:
        return False, "执行结果的'负责人'字段值不能为空"
    else:
        query_dict["负责人"] = run_result.get("负责人")

    feishu = feishu_api()
    dt = datetime.datetime.now().strftime('%Y-%m-%d')
    ts = int(time.mktime(time.strptime(dt, "%Y-%m-%d")))
    run_result["执行日期"] = ts * 1000
    # feishu.get_app_access_token()
    user_id = feishu.get_user_open_id(name=run_result.get("负责人").strip())
    if user_id is None:
        return False, "执行结果的'负责人'字段值无效"
    run_result['负责人'] = [{'id': user_id}]
    feishu.get_bitable_app_access_token(document_id=document_id)
    logger.info(f"feishu_api: {vars(feishu)}")

    table_id = feishu.get_table_id_by_table_name(table_name)
    if table_id:
        feishu.get_records_in_table(table_id)
        if False:
            return feishu.update_record_in_table(table_id, detail, run_result)
        else:
            return feishu.add_record_in_table(table_id, run_result)
    else:
        return False, f"根据名称 {table_name} 未找到数据表"


@monitor(True)
def add_priority_feishu_table(table_name, run_result: dict, document_id="Y9owwbum7iuOWOkxW1ecnVxKnEe"):
    """
    根据willow上测试任务的执行结果更新飞书的对应多维表格

    :param table_name: 多维表格的中文名称
    :param run_result: willo上job的执行结果
    :param document_id: 多维表格所在文档空间的文档ID
    """

    if "执行类型" not in run_result:
        return False, "执行结果的'执行类型'字段不存在"
    elif run_result.get("执行类型") is None:
        return False, "执行结果的'执行类型'字段值不能为空"

    if "分组" not in run_result:
        return False, "执行结果的'分组'字段不存在"
    elif run_result.get("分组") is None:
        return False, "执行结果的'分组'字段值不能为空"

    if "负责人" not in run_result:
        return False, "执行结果的'负责人'字段不存在"
    elif run_result.get("负责人") is None:
        return False, "执行结果的'负责人'字段值不能为空"

    feishu = feishu_api()

    feishu.get_app_access_token()
    user_id = feishu.get_user_open_id(name=run_result.get("负责人").strip())
    if user_id is None:
        return False, "执行结果的'负责人'字段值无效"
    run_result['负责人'] = [{'id': user_id}]
    feishu.get_bitable_app_access_token(document_id=document_id)
    logger.info(f"feishu_api: {vars(feishu)}")

    table_id = feishu.get_table_id_by_table_name(table_name)
    if table_id:
        feishu.get_records_in_table(table_id)
        return feishu.add_record_in_table(table_id, run_result)
    else:
        logger.info(f"根据名称 {table_name} 未找到数据表")
        return False, f"根据名称 {table_name} 未找到数据表"


@monitor(True)
def add_case_fail_info_feishu_table(table_name, run_result: dict, document_id="Ep0fw9ywSiSXqgk78a9c49U3nmh",
                                    ip_addr=None, feishu_rule_key=None):
    """
    根据willow上测试任务的执行结果更新飞书的对应多维表格

    :param table_name: 多维表格的中文名称
    :param run_result: willo上job的执行结果
    :param document_id: 多维表格所在文档空间的文档ID
    :param ip_addr: 失败用例的台架IP地址
    :param feishu_rule_key: 多维表格字段信息
    """
    query_dict = {}

    if "脚本目录" not in run_result:
        return False, "执行结果的'脚本目录'字段不存在"
    elif run_result.get("版本号") is None:
        return False, "执行结果的'版本号'字段值不能为空"
    else:
        query_dict["版本号"] = run_result.get("版本号")

    if "Job类型" not in run_result:
        return False, "执行结果的'Job类型'字段不存在"
    elif run_result.get("Job类型") is None:
        return False, "执行结果的'Job类型'字段值不能为空"
    else:
        query_dict["Job类型"] = run_result.get("Job类型")

    if "执行类型" not in run_result:
        return False, "执行结果的'执行类型'字段不存在"
    elif run_result.get("执行类型") is None:
        return False, "执行结果的'执行类型'字段值不能为空"
    else:
        query_dict["执行类型"] = run_result.get("执行类型")

    run_result["台架IP"] = ip_addr

    feishu = feishu_api()
    feishu.get_app_access_token()
    feishu.get_bitable_app_access_token(document_id=document_id)
    logger.info(f"feishu_api: {vars(feishu)}")
    # 失败用例的必填字段描述
    field_list_base = []
    # 'str'：字符串、'num'：数字、'single'：单选、"multiple"：多选，date：日期，'user'：人员
    available_field_type = {'str': 1, 'num': 2, 'single': 3, "multiple": 4, 'date': 5, 'user': 11, }
    if feishu_rule_key is not None:
        for field in feishu_rule_key:
            curr_field_list = field.split('_')
            if len(curr_field_list) == 2:
                if curr_field_list[1] in available_field_type:
                    field_list_base.append({"field_name": curr_field_list[0],
                                            "type": available_field_type[curr_field_list[1]]})
    else:
        field_list_base = [{"field_name": "MS目录", "type": 1},
                           {"field_name": "脚本目录", "type": 1},
                           {"field_name": "执行类型", "type": 1},
                           {"field_name": "Job类型", "type": 1},
                           {"field_name": "版本号", "type": 1},
                           {"field_name": "caseid", "type": 1},
                           {"field_name": "测试owner", "type": 11},
                           {"field_name": "JobID", "type": 1},
                           {"field_name": "run_unique", "type": 1},
                           {"field_name": "日期", "type": 5},
                           {"field_name": "问题分类", "type": 3},
                           {"field_name": "台架IP", "type": 1},
                           {"field_name": "Allure报告", "type": 1},
                           ]
    table_id = feishu.get_table_id_by_table_name(table_name)

    if table_id:
        result, field_list = feishu.get_field_in_document_id(table_id)
        field_list_new = []
        for field in field_list:
            field_list_new.append({'field_name': field['field_name'], 'type': field['type']})
        if result:
            for field in field_list_base:
                curr_field = {"field_name": field["field_name"], "type": field['type']}
                if curr_field not in field_list_new:
                    logger.info(f"不存在：{curr_field}")
                    if curr_field == {"field_name": "日期", "type": 5}:  # 日期列 新增时，设置日期格式及自动填充
                        curr_field = {"field_name": "日期", "type": 5,
                                      "property": {"date_formatter": "yyyy-MM-dd", "auto_fill": True}}
                    feishu.add_field_in_data_table(table_id, curr_field)
    else:
        for i in range(len(field_list_base)):
            if field_list_base[i] == {"field_name": "日期", "type": 5}:  # 日期列 新增时，设置日期格式及自动填充
                field_list_base[i] = {"field_name": "日期", "type": 5,
                                      "property": {"date_formatter": "yyyy-MM-dd", "auto_fill": True}}
        feishu.add_data_table_in_document_id(table_name, field_list_base)

    if "测试owner" in run_result:
        user_id = feishu.get_user_open_id(name=run_result.get("测试owner").strip())
        logger.info(f"获取到的user_id:{user_id}")
        if user_id is not None:
            run_result["测试owner"] = [{'id': user_id}]
        else:
            del run_result["测试owner"]
    table_id = feishu.get_table_id_by_table_name(table_name)
    if table_id:
        # 添加今日试图
        view_name = f"{datetime.datetime.now().month}/{datetime.datetime.now().day}"
        result, view_info = feishu.get_views_in_table(table_id)
        if result:
            for view in view_info:
                logger.info(f"{view['view_id']} {view['view_name']}")
                if view['view_name'] == view_name:
                    break
            else:
                result, fields = feishu.get_field_in_document_id(table_id)
                add_result, view_id = feishu.add_view_in_table(table_id, view_name)
                for field in fields:
                    if field['field_name'] == "日期":
                        feishu.update_view_in_table(table_id, view_id, field['field_id'])
                        break
        else:
            result, fields = feishu.get_field_in_document_id(table_id)
            add_result, view_id = feishu.add_view_in_table(table_id, view_name)
            for field in fields:
                if field['field_name'] == "日期":
                    feishu.update_view_in_table(table_id, view_id, field['field_id'])
        # 添加失败用例信息
        return feishu.add_record_in_table(table_id, run_result)
    else:
        logger.info(f"根据名称 {table_name} 未找到数据表")
        return False, f"根据名称 {table_name} 未找到数据表"


def insert_record_to_feishu_table(data, table_name, document_id):
    """
    插入一条记录到飞书表格
    Args:
        data (): 记录信息，类型字典
        table_name (): 数据表的名称
        document_id (): 文档ID

    Returns: 元组，包含两个元素：第一个为True代表成功，False为失败，第二个信息为插入的记录ID或失败描述信息

    """
    feishu = feishu_api()
    feishu.get_bitable_app_access_token(document_id=document_id)
    if feishu.app_access_token:
        table_id = feishu.get_table_id_by_table_name(table_name)
        if table_id:
            return feishu.add_record_in_table(table_id, data)
        else:
            return False, f"无效的数据表名称: {table_name}"
    else:
        return False, f"无效的文档ID: {document_id}"
def send_msg_base(msg, webhook):
    """
    向指定的Webhook发送消息。
    
    Args:
        msg (dict): 要发送的消息内容，必须为字典类型。
        webhook (str): 接收消息的Webhook地址。
    
    Returns:
        None
    
    """
    headers = {'Content-Type': 'application/json'}
    data_request.DataRequest().post(url=webhook, headers=headers, data=json.dumps(msg), timeout=60)
    

if __name__ == "__main__":
    logger = Logger().get_logger("test")
    # logger.info(insert_record_to_feishu_table({"caseid": "123"}, "数据表", "SectwMSPkid3qpkymtycrBIyngg"))

    feishu = feishu_api()
    feishu.get_bitable_app_access_token(document_id="GmxwwTxXtiGSCAkVyMVcj49lnuf")
    if feishu.app_access_token:
        table_id = feishu.get_table_id_by_table_name("9月30-10月6 胎压告警原始数据")
        if table_id:
            logger.info(table_id)
            res = feishu.get_records_in_table(table_id)
            for i in res:
                logger.info(i)
