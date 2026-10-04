# -*- coding: utf-8 -*-

"""
@Time    : 2022/5/24 11:26 下午
@Author  : hanscal
@Email   : hanscal@xxx.com
"""
import base64
import datetime
import json
import os
import sys
import time
import traceback

import requests
from jira import JIRA

current_path = os.path.dirname(os.path.realpath(__file__))
from xat_ecu.legacy.common.logger import logger, Logger


class JiraConstant:
    JIRA_USERNAME = 'amlyYV9jbG91ZF9sb2c='

    JIRA_PASSWORD = __import__("os").environ.get('XAT_CREDENTIAL_ECU__UTILS_FEISHU_BUG_FIX_STATUS_AUTO_PY_JIRA_PASSWORD', "")

    JIRA_URL = 'https://jira.jiduauto.com'


class JiraApi:
    """
    基于python jira 进行的二次封装，匹配业务
    """

    def __init__(self,
                 user_name: str = base64.b64decode(JiraConstant.JIRA_USERNAME).decode(),
                 password: str = base64.b64decode(JiraConstant.JIRA_PASSWORD).decode(),
                 server: str = JiraConstant.JIRA_URL):
        self.jira = JIRA(server=server, basic_auth=(user_name, password))

    def get_projects(self):
        """获取jira项目"""
        project_list = self.jira.projects()
        project_list_json = []
        for project in project_list:
            project_list_json.append({'key': project.raw.get('key'), 'name': project.raw.get('name')})
        return project_list_json

    def get_issue(self, key):
        """获取jira信息"""
        return self.jira.issue(id=key, expand='changelog')

    def get_jira_required_meta(self, project='SOA'):
        """获取jira项目配置的必填信息"""
        jira_issue_fields = self.get_basic_issue_meta_by_project(project)
        final_issue_fields = {}
        for jira_issue_field in jira_issue_fields:
            # 这里这些字段是因为使用默认值，在端上不暴露出来
            if jira_issue_fields[jira_issue_field]['required'] == False or \
                    jira_issue_field in ['issuetype', 'reporter', 'project', 'security']:
                pass
            else:
                final_issue_fields[jira_issue_field] = jira_issue_fields[jira_issue_field]
        return final_issue_fields

    def get_issue_affects_info_by_key(self, key):
        """获取修复版本"""
        issue = self.jira.issue(key)
        return issue.raw.get('fields').get('customfield_10707')

    def get_issue_info_updated(self, key):
        """获取最后一次更新时间"""
        try:
            issue = self.jira.issue(key)
            return issue.raw.get('fields').get('updated')
        except:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/utils/feishu_bug_fix_status_auto.py")
            return None

    def get_issue_status_by_key(self, key):
        """获取jira状态信息"""
        try:
            issue = self.jira.issue(key)
            return issue.fields.status
        except:
            # 获取不到就返回无效
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/utils/feishu_bug_fix_status_auto.py")
            return 'Invalid'

    def search_users_by_name(self, user):
        """获取jira用户信息"""
        users = self.jira.search_users(user)
        user_name_list = []
        for user in users:
            user_name_list.append(user.raw.get('name'))
        return user_name_list

    def get_transition_by_key(self, key):
        """获取当前问题的可流转状态信息"""
        return self.jira.transitions(key)

    def get_basic_issue_meta_by_project(self, projectKeys='DCD'):
        """获取jira配置信息，包含字段等"""
        dcd_project_data_list = \
            self.jira.createmeta(projectKeys=projectKeys, issuetypeNames='Bug', expand='projects.issuetypes.fields')[
                'projects']
        issue_type_meta = dcd_project_data_list[0]['issuetypes'] if dcd_project_data_list and len(
            dcd_project_data_list) > 0 else None
        issue_fields = issue_type_meta[0]['fields'] if issue_type_meta and len(issue_type_meta) > 0 else None
        return issue_fields

    def get_issues_by_jql(self, jql='', startAt=0, maxResult=50):
        """通过jql来查询jira，默认50条"""
        jira_collect_list = []
        while True:
            try:

                issue_list = self.jira.search_issues(jql_str=jql, startAt=startAt, maxResults=maxResult,
                                                     fields=['summary', 'status', 'components', 'created', 'updated',
                                                             'reporter', 'assignee', 'priority', 'customfield_10707',
                                                             'resolution', 'customfield_11711'],
                                                     expand='changelog')
                for issue in issue_list:
                    issue_key = issue.raw.get('key')
                    if issue_key.startswith("JBS-"):
                        continue
                    # logger.info(issue_key)
                    # issue_summary = issue.fields.summary
                    issue_components = issue.raw.get('fields').get('components')
                    # logger.info(issue.raw.get('fields'))
                    reporter = None
                    try:
                        reporter = issue.raw.get('fields').get('reporter').get('name')
                    except Exception as e:
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/utils/feishu_bug_fix_status_auto.py")
                        pass
                    resolution = "Unresolved"
                    try:
                        resolution = issue.raw.get('fields').get('resolution').get('name')
                    except Exception as e:
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/utils/feishu_bug_fix_status_auto.py")
                        pass
                    if reporter == "jira_soa_bgm_tcam":
                        continue
                    priority = issue.raw.get('fields').get('priority').get('name').split("-")[0]
                    jira_links = f"https://jira.jiduauto.com/browse/{issue_key}"
                    affects_build = issue.raw.get('fields').get("customfield_10707")
                    create_date_str = issue.raw.get('fields').get('created')
                    create_date_obj = datetime.datetime.fromisoformat(create_date_str.replace('+0800', ''))
                    issue_created = int(create_date_obj.timestamp()) * 1000
                    frequency = issue.raw.get('fields').get('customfield_11711').get("value", "")
                    component_list = []
                    for component in issue_components:
                        if component.get('name') not in component_list:
                            component_list.append(component.get('name'))
                    # issue_change_log_history = issue.raw.get('changelog').get('histories')
                    jira_collect = {'问题发现时间': issue_created,
                                    'component': component_list
                                    if issue_components and len(issue_components) > 0 else None, 'Reporter': reporter,
                                    '问题等级': priority, 'Jira链接': jira_links,
                                    '提测版本': affects_build, "解决结果": resolution, "频次": frequency}
                    # jira_history_list = []
                    # for change_log in issue_change_log_history:
                    #     operate_item = change_log.get('items')
                    #     for item in operate_item:
                    #         # 目前只对statue更改进行记录，可拓展
                    #         if item.get('field') == 'status':
                    #             jira_history = {'jira_operate_id': change_log.get('id'),
                    #                             'jira_operate_time': change_log.get('created').replace('T', ' ').replace(
                    #                                 '+0800', ''),
                    #                             'jira_field': item.get('field'),
                    #                             'jira_from': item.get('fromString'),
                    #                             'jira_to': item.get('toString')
                    #                             }
                    #             jira_history_list.append(jira_history)
                    # jira_collect['jira_history'] = jira_history_list
                    jira_collect_list.append(jira_collect)
                    # logger.info(f"{jira_collect['Jira链接']} == {jira_collect['问题发现时间']}")
                else:
                    startAt += 50
                    print(f"当前有效的的issue总数:{len(jira_collect_list)}")
                    time.sleep(1)
                    if len(issue_list) < maxResult:
                        break
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/utils/feishu_bug_fix_status_auto.py")
                print(traceback.format_exc())
        return jira_collect_list

    def create_issues_by_json(self, issue_json):
        """通过json创建JIRABUG"""
        try:
            key = self.jira.create_issue(fields=issue_json)
            return JiraConstant.JIRA_URL + '/browse/' + str(key)
        except Exception as e:
            # 如果无法指定人员，就默认给 fangying.liu
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/utils/feishu_bug_fix_status_auto.py")
            if 'cannot be assigned issues' in str(e):
                issue_json['assignee'] = {'name': 'dejian.xiong'}
                key = self.jira.create_issue(fields=issue_json)
                return JiraConstant.JIRA_URL + '/browse/' + str(key)
            # 如果模块信息变更，就指派给上级模块 BGM/CDC/TCAM
            if 'components' in str(e):
                if 'module=bgm' in str(issue_json.get('description')):
                    module = 'BGM'
                elif 'module=tcam' in str(issue_json.get('description')):
                    module = 'TCAM'
                else:
                    module = 'CDC'
                issue_json['components'] = [{'name': module}]
                key = self.jira.create_issue(fields=issue_json)
                return JiraConstant.JIRA_URL + '/browse/' + str(key)
            return None

    def create_soa_issues_by_json(self, issue_json):
        pass

    def add_comments_by_key(self, key, comments):
        """添加comments"""
        return self.jira.add_comment(key, comments)

    def add_attachments_by_key(self, key, attachment):
        """添加附件"""
        return self.jira.add_attachment(key, attachment=attachment)

    def update_issue_assignee_by_key(self, key, user):
        """更新指派人"""
        return self.jira.assign_issue(key, user)

    def update_issue_report_by_key(self, key, user):
        """更新报告人"""
        issue = self.jira.issue(key)
        return issue.update(reporter={'name': user})

    def update_issue_affects_build(self, key, mini_version):
        """更新修复版本信息"""
        issue = self.jira.issue(key)
        return issue.update(customfield_10707=mini_version)

    def update_software_number(self, key):
        """更新customfield_11600（修复信息备注）"""
        issue = self.jira.issue(key)
        return issue.update(customfield_11600='7天未发现问题，关闭')

    def update_issue_status_by_key(self, key, status, **fieldargs):
        """如果状态更新成'To Closed', 需要增加参数 resolution={'name': 'Done'}"""
        return self.jira.transition_issue(key, transition=status, **fieldargs)

    def delete_issue(self, key):
        """删除指定jira"""
        issue = self.jira.issue(key)
        return issue.delete()


class feishu_api:
    def __init__(self, app_id="cli_a51121ad3bcad00c", app_secret=__import__("os").environ.get('XAT_CREDENTIAL_ECU__UTILS_FEISHU_BUG_FIX_STATUS_AUTO_PY_APP_SECRET', ""),
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
        logger.info(resp_body)
        if resp_body.get("code", 500) == 0:
            user_list = resp_body.get("data").get("users")
            if user_list:
                for user in user_list:
                    return user.get('open_id')
            else:
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
        if "脚本目录" in data:
            if data["脚本目录"].startswith("test_case/soa/"):
                del data["台架IP"]
        try:
            if "caseid" in data:
                if data["MS目录"].startswith("/TCAM"):  # TCAM失败自动化用例获取该用例上次的分析结果
                    data["问题分类"], data["问题描述"] = self.get_last_analysis_result(table_id, data)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/utils/feishu_bug_fix_status_auto.py")
            logger.info("获取问题分类、问题描述失败")
        url = self.server_name + path + f"{self.app_access_token}/tables/{table_id}/records"
        body_data = {"fields": data}
        response = requests.post(url, json.dumps(body_data), headers=headers, timeout=5)
        resp_body = json.loads(response.text)
        if resp_body.get("msg") == "FieldNameNotFound":
            body_data = {"fields": data}
            response = requests.post(url, json.dumps(body_data), headers=headers, timeout=5)
            resp_body = json.loads(response.text)
            if resp_body.get("code") == 0:
                return True, "表{table_id}，记录新增成功"
            else:
                return False, "表{table_id}，记录新增失败"
        if resp_body.get("code") == 0:
            return True, f"表{table_id} 新增记录：" + str(resp_body.get("msg"))
        else:
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
            return True, "执行结果更新成功"
        else:
            logger.info(f"表{table_id} 更新记录失败，返回结果：{resp_body}")
            return False, "执行结果更新失败"

    def get_spreadsheets_info(self, path="/open-apis/sheets/v3/spreadsheets/", spreadsheet_token=None):
        """
        获取电子表格的字段信息
        """
        headers = {"Authorization": f"Bearer {self.user_access_token}"}
        url = self.server_name + path + f"{spreadsheet_token}/sheets/query"
        response = requests.get(url, headers=headers, timeout=60)
        resp_body = json.loads(response.text)
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
        headers = {"Authorization": f"Bearer {self.user_access_token}",
                   "Content-Type": "application/json; charset=utf-8"}
        if end is None:
            end = start
        url = self.server_name + path + f"{spreadsheet_token}/values/{sheet_id}!{start}:{end}?valueRenderOption=ToString"
        response = requests.get(url, headers=headers, timeout=60)
        resp_body = json.loads(response.text)
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
        headers = {"Authorization": f"Bearer {self.user_access_token}",
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
        response = requests.put(url, headers=headers, data=json.dumps(data), timeout=60)
        resp_body = json.loads(response.text)
        code = resp_body.get("code")
        msg = resp_body.get("msg")
        if code == 0:
            return True, f"记录新增成功,{msg}"
        else:
            return False, f"记录新增失败,{msg}"


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


def feishu_bug_fix_status_auto(sheet_name, document_id="QpYBwQ7SiiKBJLky3bTc7DWdnfb"):
    source_feishu = feishu_api()
    source_feishu.get_app_access_token()
    source_feishu.get_user_access_token()
    source_feishu.get_bitable_app_access_token(document_id=document_id)
    table_id = source_feishu.get_table_id_by_table_name(sheet_name)
    result = source_feishu.get_all_records_in_table(table_id)
    after_filter_result = []
    bug_fix_status = {}
    jira = JiraApi()
    project = 'SOA'
    logger.info(f"{sheet_name} 共查询到{len(result)} 条数据")
    i = 0
    for item in result:
        record_id = item['record_id']
        i += 1
        if item['fields']['bug票'] is not None:
            if isinstance(item['fields']['bug票'], str):
                if "SOA-" in item['fields']['bug票']:
                    if item['fields']['bug票'].strip() not in bug_fix_status:
                        bug_status = jira.get_issue_status_by_key(item['fields']['bug票'].strip())
                        logger.info(f"--------------  {item['fields']['bug票'].strip()}, 状态：{bug_status.__str__()}")
                        if bug_status.__str__() == "Closed":
                            bug_fix_status[item['fields']['bug票'].strip()] = True
                        else:
                            bug_fix_status[item['fields']['bug票'].strip()] = False
                    if bug_fix_status.get(item['fields']['bug票'].strip()):
                        update_result = source_feishu.update_record_in_table(table_id, record_id, {"是否已修复": '是'})
                    else:
                        update_result = source_feishu.update_record_in_table(table_id, record_id, {"是否已修复": '否'})
                    status = "是" if bug_fix_status.get(item['fields']['bug票'].strip()) else "否"
                    update_feishu_result = "成功" if update_result[0] else "失败"
                    logger.info(f"第{i} 条: {item['fields']['bug票'].strip()}, 是否已修复：{status}, "
                                f"更新{update_feishu_result}")


if __name__ == "__main__":
    logger = Logger().get_logger("test")
    document_id_str = "QpYBwQ7SiiKBJLky3bTc7DWdnfb"
    sheet_name_list = ["SOA基础服务失败用例信息", "周提测失败用例信息", "性能稳定性失败用例信息"]
    for item in sheet_name_list:
        logger.info("")
        logger.info("================================")
        feishu_bug_fix_status_auto(item)
