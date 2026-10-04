#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename     :feishu_notice_report.py
@time         :7/3/24 14:39
@author       :dejian.xiong@jiduauto.com
@description  :
"""
import json
import os
import sys
from pathlib import Path

from xat_ecu.legacy.common.logger import logger

from framework.automotive.utils.bench_helper import BenchHelper
from framework.automotive.utils.data_type import ReportInfo
from tools.feishu.feishu_notice import send_msg

logger.debug = print
logger.info = print


def parse_allure_json_get_report(path) -> ReportInfo:
    report_info = ReportInfo(**{
        "total": 0,
        "passed": 0,
        "failed": 0,
        "error": 0,
        "skipped": 0,
        "success_rate": '',
        "duration_str": '',
    })
    report_path = path
    report_files = os.listdir(path)
    logger.debug(f"当前的result.json的数量为{len(report_files)}")
    for file in report_files:
        if file.endswith('result.json'):
            with open(Path(report_path) / file) as f:
                result_json = json.load(f)
            case_result = result_json.get("status").replace('broken', 'error')
            if case_result is not None:
                report_info[case_result] += 1
    total = report_info.passed + report_info.failed + report_info.error
    report_info.total = total
    if total:
        logger.debug(f"通过用例数:{report_info.passed}, 失败用例数:{report_info.failed}, 总用例数:{total}")
        report_info.success_rate = report_info.passed / total
        report_info.success_rate = "{:.2%}".format(report_info.success_rate)
        logger.info('通过率：' + report_info.success_rate)
    else:
        report_info.success_rate = "0%"

    return report_info


def feishu_notice_case_report(
        path,
        jenkins_status,
        allure_link,
        webhook='https://open.feishu.cn/open-apis/bot/v2/hook/ec5911b4-eae1-4424-a80d-1da29927f3d3',
):
    result = parse_allure_json_get_report(path)
    total_cases = result.total
    passed_cases = result.passed
    failed_cases = result.failed
    error_cases = result.error
    skipped_cases = result.skipped
    success_rate = result.success_rate
    duration_str = result.duration_str
    bh = BenchHelper()
    version_dict = bh.get_framework_version_info()
    jenkins_build_dict = {
        "SUCCESS": ["green", "成功"],
        "FAIL": ["red", "失败"],
        "ABORTED": ["grey", "已取消"],
        "UNSTABLE": ["red", "失败"]
    }
    version_content = ""
    allure_content = f"报告链接：{allure_link}"
    for key, value in version_dict.items():
        if value != '':
            version_content += f"{key}: <font color=\"grey\">{value}</font>\n"

    case_content = f"**Total: {total_cases}**\n**Passed: <font color=\"green\">{passed_cases}</font>**\n**Failed: <font color=\"red\">{failed_cases}</font>**\nError: <font color=\"red\">{error_cases}</font>\nSkipped: <font color=\"grey\">{skipped_cases}</font>\n**通过率: <font color=\"green\">{success_rate}</font>**\n{duration_str}"
    content = {
        "elements": [
            {
                "tag": "markdown",
                "content": f"{version_content}{case_content}\n{allure_content}<at id=all></at>"
            },
        ],
        "header": {
            "template": f"{jenkins_build_dict[jenkins_status][0]}",
            "title": {
                "content": f"jenkins daily每日执行结果-{jenkins_build_dict[jenkins_status][1]}",
                "tag": "plain_text"
            }
        }
    }
    markdown_content = {
        "msg_type": "interactive",
        "card": content
    }

    markdown_content = json.dumps(markdown_content)
    send_msg(markdown_content, webhook)


if __name__ == '__main__':
    path = sys.argv[1]
    jenkins_status = sys.argv[2]
    allure_link = sys.argv[3]
    feishu_notice_case_report(path, jenkins_status, allure_link)
