import base64
import datetime
import time
import traceback

from jira import JIRA

from xat_ecu.legacy.common.constant import JiraConstant


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
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/jira/jira_api.py")
            return None

    def get_issue_status_by_key(self, key):
        """获取jira状态信息"""
        try:
            issue = self.jira.issue(key)
            return issue.fields.status
        except:
            # 获取不到就返回无效
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/jira/jira_api.py")
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
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/jira/jira_api.py")
                        pass
                    resolution = "Unresolved"
                    try:
                        resolution = issue.raw.get('fields').get('resolution').get('name')
                    except Exception as e:
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/jira/jira_api.py")
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
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/jira/jira_api.py")
                print(traceback.format_exc())
        return jira_collect_list

    def create_issues_by_json(self, issue_json):
        """通过json创建JIRABUG"""
        try:
            key = self.jira.create_issue(fields=issue_json)
            return JiraConstant.JIRA_URL + '/browse/' + str(key)
        except Exception as e:
            # 如果无法指定人员，就默认给 fangying.liu
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/jira/jira_api.py")
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


if __name__ == '__main__':
    jira = JiraApi()
    project = 'SOA'
    required_fields = jira.get_jira_required_meta(project)
    print(required_fields)
    # issue的案例
    issue_form = {'labels': ['jira测试'], 'versions': [{'name': 'v1.3'}], 'components': [{'name': 'BGM'}],
                  'customfield_10701': 'AutoTest', 'customfield_11004': {'value': 'MarsOne'},
                  'customfield_11711': {'value': '低频（<5%)'}, 'priority': {'name': 'P1-Major'},
                  'description': 'jira测试', 'summary': 'jira标题', 'issuetype': {'name': 'Bug'},
                  'project': {'key': project}, 'reporter': {'name': 'willow_jira'},
                  'assignee': {'name': 'dejian.xiong'},
                  'customfield_10707': '小版本'}
    # jira.create_issues_by_json(issue_form)
    print(jira.get_issues_by_jql('key ="SOA-22984"'))
