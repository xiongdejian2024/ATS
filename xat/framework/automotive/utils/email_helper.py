#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename     :email_helper.py
@time         :2/18/24 16:48
@author       :dejian.xiong@jiduauto.com
@description  :
"""
import json
import os, sys
import re
import smtplib
import uuid
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.common.time_handle import get_time_str_year_month
from xat_ecu.legacy.interface.feishu import feishu_api
from jinja2 import Template

from framework.automotive.utils.conftest_helper import statics_dir, convert_version_format, parent_dir
from framework.automotive.utils.data_type import EnvPropertiesInfo, PytestProcess


class EmailHelper:
    def __init__(self):
        # # 第三方 SMTP 服务  此为 outlook 邮箱
        # self.mail_host = "smtp.partner.outlook.cn"  # 设置服务器
        # self.mail_user = 'smtp_soa_cicd@jiduauto.com'  # 用户名
        # self.mail_pass = "Ssc_20221117"  # 口令
        # self.to_list = [
        #     'soa_team@jiduauto.com',
        #     'soa_qa@jiduauto.com',
        #     'o_xiaoyun.zhou@external.jiduauto.com',
        #     'soa_external@jiduauto.com',
        # ]

        # 第三方 SMTP 服务  新版转飞书邮箱 2024 5月中旬替换
        self.mail_host = "smtp.feishu.cn"  # 设置服务器

        # #  ------- 测试环境 ---------------------
        # self.mail_user = 'smtp_soa_cicd@jiyue.auto'  # 用户名
        # self.mail_pass = "Qy8JSxZMV4"  # 口令

        #  ------- 生产环境 ---------------------
        self.mail_user = 'smtp_soa_cicd@jiduauto.com'  # 用户名
        self.mail_pass = __import__("os").environ.get('XAT_CREDENTIAL_PYTEST___UTILS_EMAIL_HELPER_PY_MAIL_PASS', "")  # 口令        

        self.to_list = [
            # 'soa_team@jiduauto.com',    # 开发人员不关心报告，只需测试人员内部发送
            'soa_qa@jiduauto.com',
            'NejN3JRGP3p56@jiduauto.com',  # 飞书 SOA测试  群 对应的邮箱 （仅企业内成员可向此群发送邮件）
            'o_xiaoyun.zhou@external.jiduauto.com',
            'soa_external@jiduauto.com',
        ]

    def send_smtp_email(self, rendered_report: str, subject: str, to_email_list: list, cc_email_list: list):
        if to_email_list:
            to_list = to_email_list
        else:
            to_list = self.to_list
            # to_list = ['quan.sun@jiduauto.com']

        if cc_email_list:
            cc_list = cc_email_list
        else:
            cc_list = ['quan.sun@jiduauto.com']

        message = MIMEMultipart('related')
        message['From'] = Header("SOA测试结果通知", 'utf-8')
        # message['To'] =  Header("测试", 'utf-8')
        message['To'] = ','.join(to_list)
        message['Cc'] = ','.join(cc_list)

        message['Subject'] = Header(subject, 'utf-8')

        msgAlternative = MIMEMultipart('alternative')
        message.attach(msgAlternative)

        # 指定图片为当前目录
        with open(Path(statics_dir) / 'notice.png', 'rb') as fp:
            msgImage = MIMEImage(fp.read())

        # 定义图片 ID，在 HTML 文本中引用
        msgImage.add_header('Content-ID', '<image1>')
        message.attach(msgImage)

        msgAlternative.attach(MIMEText(rendered_report, 'html', 'utf-8'))

        receivers = to_list + cc_list

        try:
            smtpObj = smtplib.SMTP(self.mail_host)
            smtpObj.connect(self.mail_host, 587)  # 25 为 SMTP 非加密通信端口号    587等是加密通信通信时用的端口号
            # smtpObj.set_debuglevel(2)
            smtpObj.starttls()
            smtpObj.login(self.mail_user, self.mail_pass)
            smtpObj.sendmail(self.mail_user, receivers, message.as_string())
            logger.info("Successfully sent email")
            smtpObj.close()
        except smtplib.SMTPException as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/email_helper.py")
            logger.error("Error: unable to send email, reason:{}".format(e))

    @staticmethod
    def email_str_to_list(email_str: str):
        if email_str and isinstance(email_str, str):
            email_str = email_str.strip()
            email_str_list = email_str.split(";")

            # 去除空格
            email_list = []
            for i in email_str_list:
                email_list.append(i.strip())

            return email_list

    def write_report_summary(self,
                             domain_version_info: EnvPropertiesInfo,
                             willow_report_summary_path,
                             link_path,
                             report_info,
                             willow_task_path,
                             feed_back,
                             time_now_year_month=get_time_str_year_month(),
                             distributed: PytestProcess = PytestProcess.NonDist):
        subject = '测试报告'
        total_cases = report_info.get("total", 0)
        self._save_report_link_in_json(link_path)
        if willow_task_path and os.path.exists(willow_task_path):
            with open(willow_task_path, "r") as task_json:
                task = json.load(task_json)
                job_type = task.get("job_type", "")
                case_type = task.get("case_type", "")
                sheet_name = task.get("sheet_name", "")
                job_owner = task.get("job_owner", "")
                test_name = task.get("test_name", "TEST")
                job_id = task.get("job_id")
                is_email = task.get("is_email")
                to_email_str = task.get("to_email_list")
                to_email_list = self.email_str_to_list(to_email_str)
                cc_email_str = task.get("cc_email_list")
                cc_email_list = self.email_str_to_list(cc_email_str)
                willow_report_link = "https://willow.jiduprod.com/reporting/willow-flow/{}/{}/report/html/index.html".format(
                    time_now_year_month, job_id
                )
                if domain_version_info:
                    domain_version_info.software_version = task.get("ecu_ver") if task.get(
                        "ecu_ver") else domain_version_info.get('software_version')
                    domain_version_info.bootes_version = task.get("X86") if task.get(
                        "X86") else domain_version_info.get(
                        'bootes_version')
                    domain_version_info.JIDLCompiler = task.get("JIDLCompiler") if task.get(
                        "JIDLCompiler") else domain_version_info.get(
                        'JIDLCompiler')
                    domain_version_info.IDL = task.get("idl") if task.get("idl") else domain_version_info.get(
                        'IDL')
                    if domain_version_info.software_version:
                        logger.info(domain_version_info.software_version)
                        first_version = list(domain_version_info.software_version.keys())
                        if len(first_version):
                            subject = "  ".join([first_version[0], test_name, "测试报告"])

            if not total_cases:
                logger.error(f"结果不正常，total is {total_cases} ， 不去微信/飞书通知和发邮件")
                return None  # 避免 total = None 垃圾邮件 或 total = 0 分母为0错误
            else:
                if willow_report_summary_path and os.path.exists(willow_report_summary_path):
                    self._send_feishu(
                        domain_version_info=domain_version_info,
                        link_path=link_path,
                        report_info=report_info,
                        test_name=test_name,
                        willow_report_link=willow_report_link,
                        willow_report_summary_path=willow_report_summary_path)

            self._feishu_feed_back(
                case_type=case_type,
                distributed=distributed,
                domain_version_info=domain_version_info,
                report_info=report_info,
                feed_back=feed_back,
                job_owner=job_owner,
                job_type=job_type,
                link_path=link_path,
                sheet_name=sheet_name,
                willow_report_link=willow_report_link)
            if is_email:
                self._send_email(
                    cc_email_list=cc_email_list,
                    domain_version_info=domain_version_info,
                    report_info=report_info,
                    link_path=link_path,
                    subject=subject,
                    test_name=test_name,
                    to_email_list=to_email_list,
                    willow_report_link=willow_report_link)

    def _send_feishu(self, domain_version_info, link_path, report_info, test_name, willow_report_link,
                     willow_report_summary_path):
        total_cases = report_info.get("total", 0)
        passed_cases = report_info.get("passed", 0)
        failed_cases = report_info.get("failed", 0)
        skipped_cases = report_info.get("skipped", 0)
        error_cases = report_info.get("error", 0)
        success_rate = report_info.get("success_rate")
        duration_str = report_info.get("duration_str")
        num_check = report_info.get("num_check")
        with open(willow_report_summary_path, "w") as f:
            logger.info("starting write report summary")
            # logger.info(f"num_check: {num_check}")

            feishu_title = f"**{test_name:-^40}**\n"
            # case_num_check = f"**Case Num Check:** {num_check[1]}\n"
            for key, value in domain_version_info.items():
                if value != '':
                    if key == 'software_version':
                        feishu_title += f"**{key}: <font color=\"grey\">{value}</font>**\n"
                    else:
                        feishu_title += f"{key}: <font color=\"grey\">{value}</font>\n"
            if len(num_check) == 2:
                feishu_title += f"**Case Num Check:** {num_check[1]}\n"
            feishu_content = f"**Willow Report Link:** [点击这里]({willow_report_link})\n**## Local Report Link:** [这里是备份]({link_path})\n**{'Test_Summary':-^35}**\nTotal: {total_cases}\n**Passed: <font color=\"green\">{passed_cases}</font>**\n**Failed: <font color=\"red\">{failed_cases}</font>**\nError: <font color=\"red\">{error_cases}</font>\nSkipped: <font color=\"grey\">{skipped_cases}</font>\n**通过率: <font color=\"green\">{success_rate}</font>**\n{duration_str}"

            content = {
                "elements": [
                    {
                        "tag": "markdown",
                        "content": f"{feishu_title}{feishu_content}\n<at id=all></at>"
                    },
                ],
                "header": {
                    "template": "green",
                    "title": {
                        "content": "自动化测试结果",
                        "tag": "plain_text"
                    }
                }
            }
            # 飞书
            group_send_message = {
                "msg_type": "interactive",
                "card": content
            }

            text = {
                # 'group_send_message': group_send_message,
                # 'person_send_message': person_send_message,
                # "job_group_send_message": job_group_send_message,
                # "job_send_message_advanced_mode": job_send_message_advanced_mode,
                "job_group_send_message": group_send_message,
                "willow_job_success": True,
                "fail_count": failed_cases,
                "pass_count": passed_cases,
                "block_count": error_cases,
            }
            json.dump(text, f)
        logger.info("Write report summary success")

    def _send_email(self, cc_email_list, domain_version_info, report_info, link_path, subject, test_name, to_email_list,
                    willow_report_link):
        total_cases = report_info.get("total", 0)
        passed_cases = report_info.get("passed", 0)
        failed_cases = report_info.get("failed", 0)
        skipped_cases = report_info.get("skipped", 0)
        error_cases = report_info.get("error", 0)
        success_rate = report_info.get("success_rate")
        duration_str = report_info.get("duration_str")

        with open(Path(statics_dir) / 'report.html') as html_file:
            template_content = html_file.read()
            template = Template(template_content)
            rendered_report = template.render(
                test_name=test_name,
                domain_version_info=domain_version_info.to_dict(),
                willow_report_link=willow_report_link,
                link_path=link_path,
                total=total_cases,
                passed=passed_cases,
                failed=failed_cases,
                error=error_cases,
                skipped=skipped_cases,
                success_rate=success_rate,
                duration_str=duration_str
            )
        self.send_smtp_email(rendered_report, subject, to_email_list, cc_email_list)

    def _feishu_feed_back(self, case_type, distributed, domain_version_info, report_info, feed_back,
                          job_owner, job_type, link_path, sheet_name, willow_report_link):
        total_cases = report_info.get("total", 0)
        passed_cases = report_info.get("passed", 0)
        failed_cases = report_info.get("failed", 0)
        skipped_cases = report_info.get("skipped", 0)
        error_cases = report_info.get("error", 0)
        success_rate = report_info.get("success_rate")
        duration_str = report_info.get("duration_str")
        try:
            if isinstance(domain_version_info.get("software_version"), dict):
                feishu_version_bgm = domain_version_info.get("software_version").get("BGM", "")
            else:
                feishu_version_bgm = domain_version_info.get("software_version")
            if feishu_version_bgm:
                feishu_version_list_bgm = feishu_version_bgm.split(" ")
                feishu_version_bgm = "V" + feishu_version_list_bgm[0][-3:] + " " + feishu_version_list_bgm[
                    1]
                feishu_version_bgm = convert_version_format(feishu_version_bgm)
        except Exception as e1:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/email_helper.py")
            logger.warning(f"BGM 版本获取时异常：{e1.__repr__()}")
            feishu_version_bgm = ""
        try:
            if isinstance(domain_version_info.get("software_version"), dict):
                feishu_version_tcam = domain_version_info.get("software_version").get("TCAM", "")
            else:
                feishu_version_tcam = domain_version_info.get("software_version")
            if feishu_version_tcam:
                feishu_version_tcam = "V" + feishu_version_tcam.replace("6110110", "")
                feishu_version_tcam = feishu_version_tcam[:4] + " " + feishu_version_tcam[4:]
                feishu_version_tcam = convert_version_format(feishu_version_tcam)
        except Exception as e2:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/email_helper.py")
            logger.warning(f"TCAM 版本获取时异常：{e2.__repr__()}")
            feishu_version_tcam = ""
        logger.info("==================回填飞书多维表格========================")
        logger.info(f"BGM 版本：{feishu_version_bgm}")
        logger.info(f"TCAM 版本：{feishu_version_tcam}")
        logger.info(f"成功的用例数：{passed_cases}")
        logger.info(f"失败的用例数：{failed_cases}")
        logger.info(f"错误的用例数：{error_cases}")
        logger.info(f"总用例数：{total_cases}")
        logger.info(f"allure报告地址：{link_path}")
        logger.info(f"willow报告地址：{willow_report_link}")
        logger.info(f"回填数据表格名称：{sheet_name}")
        logger.info(f"Job类型：{job_type}")
        logger.info(f"执行类型：{case_type}")
        logger.info(f"负责人：{job_owner}")
        logger.info("==========================================")
        if distributed.Master:
            # master端将文件读出来，进行分数回填
            willow_run_result = {"版本号": '', "Job类型": job_type, "执行类型": case_type,
                                 "测试报告Link": {'link': willow_report_link,
                                              'text': willow_report_link},
                                 "本地报告Link": {'link': link_path,
                                              'text': link_path},
                                 "负责人": job_owner,
                                 "总数量": 0,
                                 "Pass数量": 0,
                                 "Fail数量": 0,
                                 "Error数量": 0,
                                 "备注": ""}
            report_path = Path(parent_dir) / '../report/allure_report'
            report_files = os.listdir(report_path)
            for file in report_files:
                if file.endswith('feishu.json'):
                    with open(Path(report_path) / file) as f:
                        result_json = json.load(f)
                        willow_run_result["总数量"] += result_json["总数量"]
                        willow_run_result["Pass数量"] += result_json["Pass数量"]
                        willow_run_result["Fail数量"] += result_json["Fail数量"]
                        willow_run_result["Error数量"] += result_json["Error数量"]
                        willow_run_result["版本号"] = result_json["版本号"]
            if willow_run_result["总数量"] <= 2:  # 执行结果只有1条或者2条的直接过滤掉
                logger.error(f"用例数量小于等于2， 不进行飞书回填")
            else:
                feishu_result, feishu_description = feishu_api.update_or_add_feishu_table(sheet_name,
                                                                                          willow_run_result)
                logger.info(f"回填结果：{feishu_result}，结果描述：{feishu_description}")
        else:
            version_num = feishu_version_bgm if "BGM" in sheet_name else feishu_version_tcam
            if "SOA" in sheet_name:
                if "BGM" in job_type:
                    version_num = feishu_version_bgm
                elif "TCAM" in job_type:
                    version_num = feishu_version_tcam
                else:
                    version_num = feishu_version_bgm
            if version_num:
                version_num = re.sub(r'\s+', ' ', version_num)  # 合并版本号中间的多个空格
            willow_run_result = {"版本号": version_num, "Job类型": job_type, "执行类型": case_type,
                                 "测试报告Link": {'link': willow_report_link,
                                              'text': willow_report_link},
                                 "本地报告Link": {'link': link_path,
                                              'text': link_path},
                                 "负责人": job_owner,
                                 "总数量": int(total_cases),
                                 "Pass数量": int(passed_cases),
                                 "Fail数量": int(failed_cases),
                                 "Error数量": int(error_cases),
                                 "备注": ""}
            try:
                logger.info(f"repeat的测试用例:{feed_back.case_ids_repeat_info}")
                for caseid in feed_back.case_ids_repeat_info:
                    repeat_info = feed_back.case_ids_repeat_info.get(caseid)
                    willow_run_result["总数量"] -= repeat_info["count"] - 1
                    if repeat_info["result"] == "Pass":
                        willow_run_result["Pass数量"] -= repeat_info["Pass"] - 1
                    if repeat_info["result"] == "Failure":
                        willow_run_result["Pass数量"] -= repeat_info["Pass"]
                        willow_run_result["Fail数量"] -= repeat_info["Failure"] - 1
                        willow_run_result["Error数量"] -= repeat_info["Blocking"]
                    if repeat_info["result"] == "Blocking":
                        willow_run_result["Pass数量"] -= repeat_info["Pass"]
                        willow_run_result["Fail数量"] -= repeat_info["Failure"]
                        willow_run_result["Error数量"] -= repeat_info["Blocking"] - 1
            except Exception as e2:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/email_helper.py")
                logger.info("回填飞书时，对repeat的数据进行处理时发生异常!")
                logger.info(e2)
            try:
                if version_num == "" or job_type == "" or case_type == "" or job_owner == "":
                    logger.info("必填字段为空，无法回填飞书表格")
                else:
                    if distributed.Slave:
                        # slave不进行回填，只保存文件
                        save_name = f"{uuid.uuid4()}_feishu.json"
                        with open(Path(parent_dir) / '../report/allure_report' / save_name, 'w') as f:
                            json.dump(willow_run_result, f, ensure_ascii=False, indent=4)
                        logger.info(f"飞书结果保存到文件{save_name}成功")
                    elif distributed.NonDist:
                        if willow_run_result["总数量"] <= 2:  # 执行结果只有1条或者2条的直接过滤掉
                            logger.error(f"用例数量小于等于2， 不进行飞书回填")
                        else:
                            feishu_result, feishu_description = feishu_api.update_or_add_feishu_table(sheet_name,
                                                                                                      willow_run_result)
                        logger.info(f"回填结果：{feishu_result}，结果描述：{feishu_description}")
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/email_helper.py")
                logger.warning(f"回填失败：" + e.__repr__())

    @staticmethod
    def _save_report_link_in_json(link_path):
        save_name = f"{uuid.uuid4()}_link_report.json"
        with open(Path(parent_dir) / '../report/allure_report' / save_name, 'w') as f:
            json.dump(dict(link=link_path), f, ensure_ascii=False, indent=4)
        logger.info(f"link_report保存到文件{save_name}成功")


if __name__ == "__main__":
    """
    测试邮件发送功能
    单独运行可在import处加
    current_path = os.path.dirname(os.path.realpath(__file__))







    """

    emailobj = EmailHelper()
    emailobj.send_smtp_email("测试邮件", "测试邮件", ['quan.sun@jiduauto.com'], [])
