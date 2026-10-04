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
import numpy as np
import requests
current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
sys.path.append(os.path.join(current_path, ".."))
sys.path.append(os.path.join(current_path, "../.."))
sys.path.append(os.path.join(current_path, "../../.."))
from loguru import logger


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


class feishu_api:
    def __init__(self, app_id="cli_a51121ad3bcad00c", app_secret=__import__("os").environ.get('XAT_CREDENTIAL____TIREPRESSUREWARN_FEISHU_API_PY_APP_SECRET', ""),
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
        self.sheet_ids = []
        self.sheet_titles = []

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
        print(f"获取到token:{resp_body}")
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
                    if user.get('name') == name:
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
        print(f"tables_info:{tables_info}")
        for table_info in tables_info:
            if table_info['name'] == table_name:
                return table_info['table_id']
        else:
            return None

    def get_records_in_table(self, table_id, path="/open-apis/bitable/v1/apps/"):
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   "Authorization": f"Bearer {self.tenant_access_token}"}
        url = self.server_name + path + f"{self.app_access_token}/tables/{table_id}/records"
        response = requests.get(url, headers=headers, timeout=5)
        resp_body = json.loads(response.text)

        for record in resp_body.get("data").get("items"):
            pass
            # if record['fields']:
            #     logger.info(f"当前记录ID：{record['id']}")
            #     for key, value in record['fields'].items():
            #         logger.info(f"    {key} ==> {value}")
        else:
            res = [record for record in resp_body.get("data").get("items") if record['fields']]

        return res

    def get_last_analysis_result(self, table_id, condition: dict, path="/open-apis/bitable/v1/apps/"):
        logger.info(f"查询条件: caseid={condition.get('caseid')}")
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   "Authorization": f"Bearer {self.tenant_access_token}"}
        url = self.server_name + path + f"{self.app_access_token}/tables/{table_id}/records"
        data = {"filter": f'CurrentValue.caseid=\"{condition.get("caseid")}\"'}
        url += '?page_size=500'
        for key in data:
            url += f"&{key}={data.get(key)}"
        response = requests.get(url, headers=headers, timeout=5)
        resp_body = json.loads(response.text)

        logger.info(f"表{table_id}查询到记录条数：{len(resp_body.get('data').get('items'))}")
        result_list = resp_body.get('data').get('items')
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
            response = requests.get(url, headers=headers, timeout=5)
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
        return res

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
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/TirePressureWarn/feishu_api.py")
            logger.info("获取问题分类、问题描述失败")
        url = self.server_name + path + f"{self.app_access_token}/tables/{table_id}/records"
        body_data = {"fields": data}
        response = requests.post(url, json.dumps(body_data), headers=headers, timeout=5)
        # response = requests.post(url, json.dumps(body_data, cls=NpEncoder), headers=headers, timeout=5)
        resp_body = json.loads(response.text)
        if resp_body.get("msg") == "FieldNameNotFound":
            body_data = {"fields": data}
            response = requests.post(url, json.dumps(body_data), headers=headers, timeout=5)
            resp_body = json.loads(response.text)
            if resp_body.get("code") == 0:
                return True, "表{table_id}，记录新增成功"
            else:
                return False, f"表{table_id}，记录新增失败,{resp_body}"
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
        response = requests.post(url, json.dumps(body_data), headers=headers, timeout=5)
        resp_body = json.loads(response.text)

        if resp_body.get("msg") == "FieldNameNotFound":
            body_data = {"fields": data}
            response = requests.post(url, json.dumps(body_data), headers=headers, timeout=5)
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
        response = requests.put(url, json.dumps(data), headers=headers, timeout=5)
        resp_body = json.loads(response.text)
        if resp_body.get("code") == 0:
            logger.info(f"表{table_id} 更新记录{record_id}：" + str(resp_body.get("msg")))
            return True, "执行结果更新成功"
        else:
            logger.info(f"表{table_id} 更新记录失败:{resp_body}")
            return False, "执行结果更新失败"

    def delete_records_in_table(self, table_id, record_ids: list, path="/open-apis/bitable/v1/apps/"):
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   "Authorization": f"Bearer {self.tenant_access_token}"}
        url = self.server_name + path + f"{self.app_access_token}/tables/{table_id}/records/batch_delete"
        body_data = {"records": record_ids}
        response = requests.post(url, json.dumps(body_data), headers=headers, timeout=5)
        resp_body = json.loads(response.text)
        logger.info(f"删除结果：{resp_body}")

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
    feishu.get_app_access_token()
    feishu.get_user_access_token()
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
    feishu.get_user_access_token()
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


def add_case_fail_info_feishu_table(table_name, run_result: dict, document_id="Ep0fw9ywSiSXqgk78a9c49U3nmh",
                                    ip_addr=None):
    """
    根据willow上测试任务的执行结果更新飞书的对应多维表格

    :param table_name: 多维表格的中文名称
    :param run_result: willo上job的执行结果
    :param document_id: 多维表格所在文档空间的文档ID
    :param ip_addr: 失败用例的台架IP地址
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
    feishu.get_user_access_token()
    feishu.get_bitable_app_access_token(document_id=document_id)
    logger.info(f"feishu_api: {vars(feishu)}")
    if "测试owner" in run_result:
        user_id = feishu.get_user_open_id(name=run_result.get("测试owner").strip())
        if user_id is not None:
            run_result["测试owner"] = [{'id': user_id}]
        else:
            del run_result["测试owner"]
    table_id = feishu.get_table_id_by_table_name(table_name)
    if table_id:
        return feishu.add_record_in_table(table_id, run_result)
    else:
        logger.info(f"根据名称 {table_name} 未找到数据表")
        return False, f"根据名称 {table_name} 未找到数据表"


# if __name__ == "__main__":
    # fail_case_info = {'版本号': 'V2.0.0 AS', 'Job类型': 'S2S性能稳定性', '执行类型': 'Full',
    #                   '脚本目录': 'test_case/soa/performance_stability/functional_performance/test_S2S_communicate.py::TestSeatService::test_caseid_1984533',
    #                   'MS目录': '/性能稳定性/业务性能/S2S通信性能', 'caseid': '1984533', '台架IP': '172.18.128.176'}
    #
    # add_case_fail_info_feishu_table("性能稳定性失败用例信息", fail_case_info, document_id="QpYBwQ7SiiKBJLky3bTc7DWdnfb",
    #                                 ip_addr="127.0.0.1")
    # feishu = feishu_api()
    # feishu.get_app_access_token()
    # feishu.get_user_access_token()
    # feishu.get_bitable_app_access_token(document_id="RtQsw2wsTiyYaNkwTqScGQJpnre")
    # table_id = feishu.get_table_id_by_table_name("使用数据")
    # result = feishu.add_record_in_table(table_id, {"文本": "127.0.0.1"})
