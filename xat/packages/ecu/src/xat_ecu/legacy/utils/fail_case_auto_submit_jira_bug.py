# -*- coding: utf-8 -*-

"""
@Time    : 2022/6/13 10:21 下午
@Author  : songjian.lin
@Email   : songjian.lin@jiduauto.com
"""

import json
import os

import paramiko
import requests

from xat_ecu.legacy.common.logger import Logger
from xat_ecu.legacy.interface.feishu import feishu_api
from xat_ecu.legacy.interface.jira.jira_api import JiraApi
from xat_ecu.legacy.interface.ms.ms_lib import meterSphere_client


def get_ms_case_step_info(project_name123, case_id):
    """根据项目名称、用例ID，从MS上获取用例的执行步骤"""
    client123 = meterSphere_client()
    client123.get_case_step_by_case_jama_id(project_name123, case_id)


def get_case_run_ecu_info(runUniq):
    """根据失败用例的唯一标识获用例执行时的ECU版本信息"""
    headers = {'Connection': 'keep-alive', 'Content-Type': 'application/json;charset=utf-8',
               'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9'}
    url = f"http://10.80.51.28:8887/mscaserun/getEcuVersionInfo"
    query = {"runUnique": runUniq}
    response = requests.post(url, json.dumps(query), headers=headers, timeout=30)
    resp_body = json.loads(str(response.content, 'utf-8'))
    if resp_body["msg"] == "success":
        # 解析返回的数据
        return resp_body["data"]
    else:
        # 处理错误
        logger.info(response.text)
        return None


def get_case_run_info(runUniq):
    """获取case执行的详细信息"""
    headers = {'Connection': 'keep-alive', 'Content-Type': 'application/json;charset=utf-8',
               'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9'}
    url = f"http://10.80.51.28:8887/mscaserun/list"
    url += f"?runUnique={runUniq}"
    response = requests.post(url, headers=headers, timeout=30)
    resp_body = json.loads(str(response.content, 'utf-8'))
    logger.info(resp_body)
    if resp_body["msg"] == "success":
        # 解析返回的数据
        if len(resp_body["data"]) > 0:
            return resp_body["data"][0]
        else:
            return None
    else:
        # 处理错误
        logger.info(response.text)
        return None


def get_confirmed_fail_case_case_id_and_run_uniq(document_id, sheet_name):
    """
    从飞书上获取失败用例的case_id、run_uniq（前提：是否是BUG为是，BUG票为空）
    返回值：列表，
    """
    source_feishu = get_feishu_obj(document_id)
    table_id = source_feishu.get_table_id_by_table_name(sheet_name)
    result = source_feishu.get_all_records_in_table(table_id)
    after_filter_result = []
    for item in result:
        if item['fields']['BUG票'] is None and item['fields']['是否是BUG'] == "是":
            after_filter_result.append(item)
    else:
        logger.info(after_filter_result)
        return after_filter_result


def auto_set_feishu_fail_case_bug_info(document_id, sheet_name, record_id, data):
    source_feishu = get_feishu_obj(document_id)
    table_id = source_feishu.get_table_id_by_table_name(sheet_name)
    source_feishu.update_record_in_table(table_id, record_id, data)


def get_feishu_obj(document_id):
    source_feishu = feishu_api.feishu_api()
    source_feishu.get_app_access_token()
    source_feishu.get_user_access_token()
    source_feishu.get_bitable_app_access_token(document_id=document_id)
    return source_feishu


def sftp_download_file(host, server_path, local_path, password, timeout=30):
    """
    上传文件，注意：不支持文件夹
    :param host: 主机名
    :param password: 密码
    :param server_path: 远程路径，比如：/home/sdn/tmp.txt
    :param local_path: 本地路径，比如：D:/text.txt
    :param timeout: 超时时间(默认)，必须是int类型
    :return: bool
    """
    try:
        t = paramiko.Transport((host, 22))
        t.banner_timeout = timeout
        t.connect(username="root", password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        # sftp.put(local_path, server_path)
        sftp.get(server_path, local_path)
        t.close()
        return True
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/utils/fail_case_auto_submit_jira_bug.py")
        logger.info(f"向{host}上传文件的异常信息：{e}")
        return False


def ssh_command(host, password, cmd, timeout=30):
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许连接不在know_hosts文件中的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname=host, port=22, username='root', password=password)
    # 执行命令
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
    # 获取命令结果
    result = stdout.read()
    # 关闭连接
    ssh.close()

    # 打印结果
    logger.info(f"命令 {cmd} 执行结果：")
    logger.info("\n" + result.decode())
    return [x for x in result.decode().split("\n") if x is not None and len(x) > 0]


def rm_fail_case_log(log_name_list):
    for log_name in log_name_list:
        res = os.system(f"rm -rf ./{log_name}")
        if res == 0:
            logger.info(f"删除{log_name}成功")
        else:
            logger.error(f"删除{log_name}失败")


if __name__ == '__main__':
    logger = Logger().get_logger("test")
    components_dict = {"BGM": "BGM", "TCAM": "TCAM", "SOA": "BGM"}
    tag_start_name = {"BGM": "BGM - "}
    case_priority = {"P0": "P0-Critical", "P1": "P1-Major", "P2": "P2-Medium", "P3": "P3-Low"}
    project_name = "SOA"
    document_id_str = "SectwMSPkid3qpkymtycrBIyngg"
    sheet_name = "数据表1"

    # 1、从失败用例多维表格中获取 是否是BUG为“是”，BUG票为“空”的用例记录
    fail_case_record_list = get_confirmed_fail_case_case_id_and_run_uniq(document_id_str, sheet_name)
    for fail_case_record in fail_case_record_list:  # 遍历需要自动提交bug的多维表格数据
        logger.info(f"case id: {fail_case_record['fields']['caseid']}")
        logger.info(f"run_unique: {fail_case_record['fields']['run_unique']}")
        # logger.info(f"agent_ip: {fail_case_record['fields']['agent_ip']}")
        logger.info(f"测试owner: {fail_case_record['fields']['测试owner']}")
        logger.info(f"record_id: {fail_case_record['record_id']}")
        # 2、获取失败用例执行时的ecu信息
        ecu_info = get_case_run_ecu_info(fail_case_record['fields']['run_unique'])

        logger.info(f"-----ecu_info: {ecu_info}--------------")
        case_info = get_case_run_info(fail_case_record['fields']['run_unique'])
        logger.info(f"classUnique: {case_info['classUnique']}")
        logger.info(f"agentIp: {case_info['agentIp']}")
        logger.info(f"runUnique:{case_info['runUnique']}")
        # 3、获取失败用例在MS上的测试步骤
        client = meterSphere_client()
        ms_step = client.get_case_step_by_case_jama_id(project_name, fail_case_record['fields']['caseid'])
        logger.info("===============")
        logger.info(ms_step)
        logger.info("===============")
        # 4、从测试机拷贝日志文件到当前目录（先删除已有日志文件）
        class_log_list = ssh_command(case_info['agentIp'], "jidu123",
                                     f"ls /root/fail_case_log/{case_info['classUnique']}")
        class_log_list = [f"/root/fail_case_log/{case_info['classUnique']}/{x}" for x in class_log_list]
        fail_case_log_name_list = []
        short_name = ["jetlog.zip", "partner.zip", "trace.zip"]

        for name in short_name:
            fail_case_log_name_list.append(f"/root/fail_case_log/{fail_case_record['fields']['run_unique']}/{name}")
        fail_case_log_name_list.extend(class_log_list)
        for fail_case_log_name in fail_case_log_name_list:
            sftp_download_file(fail_case_record['fields']['agent_ip'], fail_case_log_name,
                               f"./{fail_case_log_name.split('/')[-1]}", "jidu123")
            if fail_case_log_name.split('/')[-1] not in short_name:
                short_name.append(fail_case_log_name.split('/')[-1])
        components = components_dict.get(project_name)
        branch_version = eval(ecu_info.get('softwareVersion')).get(components).replace(" ", "")
        summary = f"【{components_dict.get(project_name)}】【{branch_version}】【xxx模块】【xxx概率】{ms_step[0]['name']} 验证失败"
        logger.info(summary)
        priority = {'name': case_priority.get(ms_step[0]['priority'])}
        reporter = {'name': ms_step[0]['maintainer']}
        logger.info(priority)
        components = [{'name': components_dict.get(project_name)}]
        if project_name in tag_start_name:
            if isinstance(ms_step[0]['tags'], str):
                if len(ms_step[0]['tags']) > 0:
                    tags_list = eval(ms_step[0]['tags'])
                    logger.info(eval(ms_step[0]['tags']))
                    for tag_name in tags_list:
                        if tag_name.startswith(tag_start_name.get(project_name)):
                            components.append({"name": tag_name})
        logger.info(components)
        Affects_Build = branch_version
        Affects_Version = [{'name': "v2.0 Beta2"}]
        description = f"-----------------版本信息-------------\n"
        description += f"BGM boot 版本: {ecu_info.get('bgmBootVersion')}\n"
        description += f"软件版本: {ecu_info.get('softwareVersion')}\n"
        description += f"硬件版本: {ecu_info.get('hardwareVersion')}\n"
        description += f"BGM mcu 版本: {ecu_info.get('bgmMcuVersion')}\n"
        description += f"BGM Switch 版本: {ecu_info.get('bgmSwitchVersion')}\n"
        description += f"idl版本: {ecu_info.get('idlVersion')}\n"
        description += f"bootes版本: {ecu_info.get('bootesVersion')}\n"
        description += f"jidl版本: {ecu_info.get('jidlVersion')}\n"
        description += f"sdb版本: {ecu_info.get('sdbVersion')}\n"
        description += f"-----------------版本信息-------------\n"
        description += f"【用例ID】\n"
        description += f"    {case_info['caseId']}\n"
        description += f"【前提条件】\n"
        for step in ms_step[0]['前置条件'].split("\n"):
            description += f"    {step}\n"
        description += f"【用例步骤】\n"
        for step in ms_step[0]['用例步骤']:
            description += f"    第{step['num']}步：{step['desc']}，预期结果：{step['result']}，实际结果：xxxx\n"
        description += f"【影响】\n"
        description += f"    xxxx\n"
        description += f"【问题发生时间：{case_info['endTime']}】\n"
        logger.info(f"步骤信息：\n{description}")
        labels = ['automation']
        # 5、创建jira bug，并添加附件（失败用例的相关日志）
        jira = JiraApi()
        project = 'SOA'
        # issue的案例
        assign_name = fail_case_record['fields']['测试owner'][0]["en_name"]
        issue_form = {'labels': labels, 'versions': Affects_Version, 'components': components,
                      'customfield_10701': 'AutoTest', 'customfield_11004': {'value': 'MarsOne'},
                      'customfield_11711': {'value': '低频（<5%)'}, 'priority': priority,
                      'description': f"步骤信息：\n{description}", 'summary': summary, 'issuetype': {'name': 'Bug'},
                      'project': {'key': project}, 'reporter': reporter,
                      'assignee': {'name': assign_name},
                      'customfield_10707': Affects_Build}
        logger.info(issue_form)
        logger.info(fail_case_log_name_list)
        create_bug_result = jira.create_issues_by_json(issue_form)
        jira_key = create_bug_result.split("/")[-1]
        for name in short_name:
            logger.info(f"./{name}")
            with open(f"./{name}", 'rb') as file:
                jira.add_attachments_by_key(jira_key, file)
        if create_bug_result:
            # 6、回填飞书多维表格“BUG票”
            data = {'BUG票': create_bug_result}
            auto_set_feishu_fail_case_bug_info(document_id_str, sheet_name, fail_case_record['record_id'], data)
        else:
            logger.info(f"jira bug 创建失败")
