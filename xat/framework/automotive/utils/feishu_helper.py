#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename     :feishu_helper.py
@time         :2/8/24 17:05
@author       :dejian.xiong@jiduauto.com
@description  :
"""
import json
import os
import uuid
import traceback
from datetime import datetime
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.interface.feishu import feishu_api

from framework.automotive.utils.willow_helper import WillowConfigForFeishu
from framework.automotive.utils.data_type import EcuInfo

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class FeishuHelper:
    @staticmethod
    def sync_fail_case_result_to_feishu(willow_task_path, case_info: WillowConfigForFeishu, ecuinfo: EcuInfo):
        try:
            ecuinfo.class_case_fail_flag = True
            with open(willow_task_path, "r") as task_json:
                task = json.load(task_json)
                job_id: str = task.get("job_id")
            if case_info.job_id is None:
                case_info.job_id = job_id

            # 如果case_info.sat_path、case_info.maintainer为空，则从数据库中获取
            if case_info.sat_path.startswith("test_case/soa"):
                project_name = "SOA平台测试"
            elif case_info.sat_path.startswith("test_case/bgm"):
                project_name = "BGM_ComponentTest"
            elif case_info.sat_path.startswith("test_case/tcam"):
                project_name = "TCAM_ComponentTest"
            else:
                project_name = ""
            data = {"caseId": str(case_info.caseid)}
            if case_info.caseUnique:
                data.update({"caseUnique": case_info.caseUnique})
            elif project_name:
                data.update({"projectName": project_name})

            query_result = query_case_info_from_db(data)
            if query_result:
                case_info.ms_path = query_result['nodePath']
                if "/" in case_info.ms_path:
                    temp_arr = case_info.ms_path.split("/")
                    if len(temp_arr) > 4:
                        case_info.ms_path = "/".join(temp_arr[0:4])
                case_info.maintainer = query_result['maintainUser']

            fail_case_info = {"版本号": case_info.version_num, "Job类型": case_info.job_type,
                              "执行类型": case_info.case_type,
                              "脚本目录": case_info.sat_path, "MS目录": case_info.ms_path, "caseid": case_info.caseid}
            if case_info.maintainer:
                fail_case_info['测试owner'] = case_info.maintainer
            fail_case_info["JobID"] = job_id
            case_info.to_string()

            if hasattr(feishu_api, "add_case_fail_info_feishu_table"):
                if case_info.fail_case_sheet_name:
                    ecuinfo.bench_uuid = uuid.uuid4()
                    ecuinfo.caseid = case_info.caseid
                    logger.info(f"失败用例的uuid：{ecuinfo.bench_uuid}")
                    # SOA测试团队 接入经测试owner确认后，失败用例自动提jira bug
                    if ecuinfo.bench_uuid and case_info.sat_path.startswith("test_case/soa"):
                        fail_case_info['run_unique'] = f"{ecuinfo.bench_uuid}"
                    result, detail = feishu_api.add_case_fail_info_feishu_table(case_info.fail_case_sheet_name,
                                                                                fail_case_info,
                                                                                case_info.fail_case_document_id,
                                                                                ecuinfo.tb_config.get("wifi_localhost",
                                                                                                      None),
                                                                                case_info.feishu_rule_key)
                    logger.info(f"回填失败用例信息结果：{result}，{detail}")

                else:
                    logger.info(f"飞书数据表名称获取失败，无法回填失败用例信息，willow配置字段：fail_case_sheet_name")
            else:
                logger.info("当前的ecusimulator 不支持将失败用例回填飞书表格")
            case_info.reset()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/feishu_helper.py")
            case_info.reset()
            logger.info(e.__repr__())
            logger.info(f"同步失败用例信息{case_info.sat_path}到飞书多维表格失败")

    @staticmethod
    def sync_bench_check_result_to_feishu(report_info, is_bench_check, wifi_localhost, link_path):
        """
          执行结果同步数据库的同时，修改飞书表格: self.wifi_localhost  IP地址，link_path（报告地址）
        """
        try:
            if is_bench_check:
                logger.info(f"同步台架检查表：{report_info.total}, {report_info.passed}, {wifi_localhost}, {link_path}")
                if report_info.total == report_info.passed:
                    result = "PASS"
                else:
                    result = "FAIL"
                feishu_data = {"立即检查": "否", "最近一次检查结果": result, "最近一次allure报告": link_path}
                feishu = feishu_api.feishu_api()
                feishu.get_bitable_app_access_token(document_id="Nm6awGREhiWGPkkux9EcGYsjndd")
                table_id = feishu.get_table_id_by_table_name("标准台架信息汇总")
                if table_id:
                    res = feishu.get_all_records_in_table(table_id)
                    for item in res:
                        if item['fields']["WifiIP地址"] == wifi_localhost:
                            record_id = item['record_id']
                            feishu.update_record_in_table(table_id, record_id, feishu_data)
                            break
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/feishu_helper.py")
            exception_detail = traceback.format_exc()
            logger.info(f"台架检查结果同步飞书失败，失败信息：\n{exception_detail}")

    @staticmethod
    def update_fail_case_table_allure_report(case_info: WillowConfigForFeishu, allure_report_address):
        if case_info.fail_case_document_id and case_info.fail_case_sheet_name and case_info.job_id:
            feishu = feishu_api.feishu_api()
            feishu.get_bitable_app_access_token(document_id=case_info.fail_case_document_id)
            table_id = feishu.get_table_id_by_table_name(case_info.fail_case_sheet_name)
            if table_id:
                res = feishu.get_records_in_table(table_id)
                for item in res:
                    record_id = item['record_id']
                    if item['fields']['JobID'] == case_info.job_id:
                        if item['fields']['台架IP']:
                            if item['fields']['台架IP'] == case_info.wifi_localhost:
                                if not item['fields']['Allure报告']:  # 为空
                                    feishu.update_record_in_table(table_id, record_id,
                                                                  {"Allure报告": allure_report_address})
                        else:
                            feishu.update_record_in_table(table_id, record_id, {"Allure报告": allure_report_address})


def query_case_info_from_db(query_data):
    import requests

    headers = {'Connection': 'keep-alive',
               'Content-Type': 'application/json;charset=utf-8', 'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9'}
    url = f"http://10.80.51.28:8887/mstestcase/list"
    # query = {"projectName": "SOA平台测试", "caseId": "1985283"}  # 其中 applyCar、caseTag为模糊查询
    logger.info(f"失败用例回填，负责人查询请求参数：{query_data}")
    response = requests.post(url, json.dumps(query_data), headers=headers, timeout=30)
    resp_body = json.loads(str(response.content, 'utf-8'))
    logger.info(f"失败用例回填，负责人查询结果：{resp_body}")
    if resp_body["msg"] == "success":
        # 解析返回的数据
        if len(resp_body["data"]) > 0:
            return resp_body["data"][0]
        else:
            return {}
    else:
        # 处理错误
        return {}
    
def send_error_msg(task_desc=None, err_info=None, master_ip=None, slave_ip=None, willow_url=None, webhooks: list = None, msg_color='red'):
    if task_desc:
        # 非cicd任务无需发送消息
        if not webhooks:
            webhooks = extract_webhook_urls(file_path=os.path.join(BASE_DIR, "../", "task.json"))
        feishu_title = f'[{task_desc}] - 任务异常\n'
        feishu_content = (f"**异常信息：**{err_info}\n" +
                    (f"master台架：{master_ip}\n" if master_ip else "") +
                    (f"slave台架：{slave_ip}\n" if slave_ip else "") +
                    f"willow链接：[点击查看]({willow_url})")
        content = {
                        "elements": [
                            {
                                "tag": "markdown",
                                "content": f"{feishu_content}\n<at id=all></at>"
                            },
                        ],
                        "header": {
                            "template": msg_color,
                            "title": {
                                "content": feishu_title,
                                "tag": "plain_text"
                            }
                        }
                    }
        # 消息内容
        msg = {
            "msg_type": "interactive",
            "card": content

        }
        try:
            for webhook in webhooks:
                feishu_api.send_msg_base(msg, webhook)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/feishu_helper.py")
            logger.warning(f"飞书机器人发送失败: {str(e)}")
            
def insert_tl_test_data_to_feishu(document_id="Gj07w21Tsi1beukSZPIcWmcenic", table_name="数据表真实", start_time=None,
                                    test_software_version=None, test_task_name=None, total_case_num=0,end_time=None,
                                    current_case_num=0, case_fail_top_three=[], case_prepare_top_three=[], max_hour=None,
                                    allure_report=None):
    if test_task_name and '周提测' not in test_task_name and 'Test' not in test_task_name:
        feishu_0914 = feishu_api.feishu_api()
        feishu_0914.get_bitable_app_access_token(document_id=document_id)
        table_id = feishu_0914.get_table_id_by_table_name(table_name)
        if table_id:
            # if start_time:
            #     date_start = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            #     date_end = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            # else:
            #     date_start = ""
            #     date_end = ""
    
            cleaned_software_version = [item for item in test_software_version if item]
            # 准备一个空列表来存储结果
            combined_parts = []
            for version in cleaned_software_version:
                if version:
                    combined = version[-6:-3] + version[-2:]
                    combined_parts.append(combined)
            # 最终拼接的结果，使用'+'连接列表中的元素
            short_name = '+'.join(combined_parts)
            test_software_version = ','.join(cleaned_software_version)
            if total_case_num == current_case_num:
                run_status = "全部执行"
            elif total_case_num > current_case_num > 0:
                run_status = "部分执行"
            else:
                run_status = "未执行"
            if 'sanity' in test_task_name:
                test_scope = "Sanity"
            else:
                test_scope = "Full"
            feishu_data = {"任务名称": test_task_name,
                           "software_version": test_software_version,
                           "简写": short_name,
                           "测试范围": test_scope,
                           "执行开始时间": int(start_time * 1000) if start_time else None,
                           "执行结束时间": int(end_time * 1000) if end_time else None,
                           "执行状态": run_status,
                           "收集到的用例数": total_case_num,
                           "当前报告中的用例数": current_case_num,
                           "失败用例最多的功能Top3": case_fail_top_three,
                           "未执行用例最多的功能Top3": case_prepare_top_three,
                           "任务时长（点击可看具体任务名称）": max_hour,
                           "执行报告Link": allure_report}
            logger.info(f"插入集中化CICD数据分析表格:{feishu_data}")
            result, _ = feishu_0914.add_record_in_table(table_id, feishu_data)  # 新增数据
            if result:
                logger.info("回填飞书成功")
            else:
                logger.warning("回填飞书失败")
            logger.info("回填飞书执行完毕！！")
        return result
    else:
        logger.warning(f"{test_task_name}非脚本稳定性不回填")

def extract_webhook_urls(file_path):
    logger.debug(f"正在从{file_path}中提取飞书webhook url...")
    webhook_urls = set()
    try:
        # 尝试打开并读取 JSON 文件
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        # 安全地访问嵌套的字典键
        notices = data.get('notice', [])
        for notice in notices:
            target = notice.get('target', {})
            groups = target.get('groups', {})
            group_list = groups.get('group_list', [])
            for group in group_list:
                webhook_url = group.get('webhook_url')
                if webhook_url:
                    webhook_urls.add(webhook_url)
                    logger.debug(f"获取到的飞书webhook_url:{webhook_url}")
    except FileNotFoundError:
        logger.error(f"willow task文件：{file_path}为找到")
    except json.JSONDecodeError:
        logger.error(f"willow task文件：{file_path}解析错误")
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/feishu_helper.py")
        logger.error(f"解析willow task文件的飞书webhook异常: {e}")
    return webhook_urls