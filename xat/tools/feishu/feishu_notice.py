# -*- coding: utf-8 -*-
"""
@File        : feishu_notice.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2023/10/24 18:00 PM
@Description : 飞书通知
@Examples    : Example of feishu notification
"""

import os
import json
import requests
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.interface.feishu.feishu_api import feishu_api
# soa_test_webhook = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=${XAT_CREDENTIAL_SCAN_B1E5E78EC8927523BCCC}"
# test_webhook = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=${XAT_CREDENTIAL_SCAN_2903B843BE309785DAC7}"
# test_webhook = "https://open.feishu.cn/open-apis/bot/v2/hook/d66445a6-7766-44e5-9842-8648a0017dde"  # 测试解决方案群
test_webhook = "https://open.feishu.cn/open-apis/bot/v2/hook/fd8943c3-9f9d-4c9a-9cb7-37898187a9b8"    # 单群

def text_notice(content):
    text_content = {
                "msg_type": "text",
                "content": content
                }
    text_content = json.dumps(text_content)
    # text_content = '{\
    #         "msgtype": "text",\
    #         "text": {\
    #             "content": "Hello, 各位伙伴，请开会前 提前更新好自己的任务状态，并建立好需求或后续任务！ ----  测开会议",\
    #             "mentioned_mobile_list":["@all"]\
    #             }\
    #         }'
    send_msg(text_content, test_webhook)

def template_notice(content):
    content = {
        "type":"template",
        "data":{
            "template_id":"ctp_AAVwlT97V01w", 
            "template_variable":content
        }
    }
    template_content = {
                "msg_type": "interactive",
                "card": content
                }
    template_content = json.dumps(template_content)
    # template_content = {
    #     "type":"template",
    #     "data":{
    #         "template_id":"ctp_xxxxxxxxxxxx",    // 卡片id，参数必填。可在工具的我的卡片中，通过复制卡片 ID 获取。
    #         "template_variable":
    #         {    
    #             "key":"value"    // 如果卡片模板内设置了变量，则可以在此处为变量（key）赋值（value）。
    #         }       
    #     }
    # }
    send_msg(template_content, test_webhook)

def markdown_notice(content):
    content = {
            "elements": [
                {
                "tag": "markdown",
                "href": {
                    "urlVal": {
                    "url": "xxx1",
                    "pc_url": "xxx2",
                    "ios_url": "xxx3",
                    "android_url": "xxx4"
                    }
                },
                "content": "普通文本\n标准emoji😁😢🌞💼🏆❌✅\n*斜体*\n**粗体**\n~~删除线~~\n[文字链接](www.example.com)\n[差异化跳转]($urlVal)\n<at id=all></at>"
                },
                {
                "tag": "hr"
                },
                {
                "tag": "markdown",
                "content": "上面是一行分割线\n![hover_text](img_v2_16d4ea4f-6cd5-48fa-97fd-25c8d4e79b0g)\n上面是一个图片标签"
                }
            ],
            "header": {
                "template": "blue",
                "title": {
                "content": "这是卡片标题栏",
                "tag": "plain_text"
                }
            }
            }
    markdown_content = {
                "msg_type": "interactive",
                "card": content
                }
    
    markdown_content = {"msg_type": "interactive", "card": {"elements": [{"tag": "markdown", "content": "**----------A14-172\u53f0\u67b6\u6d4b\u8bd5\u5f00\u53d1webhook----------**\n\u8f6f\u4ef6\u7248\u672c: **6160110130 AQ**\nidl: <font color=\"grey\">JIDL_RELEASE_1.3REL_9</font>\nX86: <font color=\"grey\">bootes1.3.2r5</font>\nJIDLCompiler: <font color=\"grey\">JIDL_RELEASE_1.3REL_9</font>\n**Willow Report Link:** [\u70b9\u51fb\u8fd9\u91cc](https://willow.jiduprod.com/reporting/willow-flow/202311/ff7b38b7-c41c-4bef-a33f-e7e6cc13ee01/report/html/index.html)\n**## Local Report Link:** [\u8fd9\u91cc\u662f\u5907\u4efd](http://172.18.128.184:8080/2023_11_14_22_18_16)\n**-----------Test_Summary------------**\nTotal: 1\n**Passed: <font color=\"green\">1</font>**\n**Failed: <font color=\"red\">1</font>**\nError: <font color=\"red\">0</font>\nSkipped: <font color=\"grey\">0</font>\n**\u901a\u8fc7\u7387: <font color=\"green\">100.00%</font>**\nCases Run Total Times:  1\u5206 5\u79d2\n<at id=all></at>"}], "header": {"template": "green", "title": {"content": "\u81ea\u52a8\u5316\u6d4b\u8bd5\u7ed3\u679c", "tag": "plain_text"}}}}
    markdown_content = json.dumps(markdown_content)
    # {
    # "elements": [
    #     {
    #     "tag": "markdown",
    #     "href": {
    #         "urlVal": {
    #         "url": "xxx1",
    #         "pc_url": "xxx2",
    #         "ios_url": "xxx3",
    #         "android_url": "xxx4"
    #         }
    #     },
    #     "content": "普通文本\n标准emoji😁😢🌞💼🏆❌✅\n*斜体*\n**粗体**\n~~删除线~~\n[文字链接](www.example.com)\n[差异化跳转]($urlVal)\n<at id=all></at>"
    #     },
    #     {
    #     "tag": "hr"
    #     },
    #     {
    #     "tag": "markdown",
    #     "content": "上面是一行分割线\n![hover_text](img_v2_16d4ea4f-6cd5-48fa-97fd-25c8d4e79b0g)\n上面是一个图片标签"
    #     }
    # ],
    # "header": {
    #     "template": "blue",
    #     "title": {
    #     "content": "这是卡片标题栏",
    #     "tag": "plain_text"
    #     }
    # }
    # }
    send_msg(markdown_content, test_webhook)


def send_msg(msg, test_webhook):
    cmd = f"curl -X POST -H 'Content-Type: application/json' -d '{msg}' '{test_webhook}'"
    logger.info(cmd)
    res = os.system(cmd)
    if res == 0:
        logger.info("text_notice cmd success")
    else:
        logger.info("text_notice cmd res is {}, ----- run failed".format(res))


class AlertInfo:
    def __init__(self, ip_address, alert_info: dict):
        self.ip_address = ip_address
        self.alert_info = alert_info


class FeishuAlert:
    def __init__(self, alertInfo: AlertInfo):
        self.webhook = "https://open.feishu.cn/open-apis/bot/v2/hook/24d5211e-6561-4aab-acee-9eb72e87b708"
        self.webhook_test = "https://open.feishu.cn/open-apis/bot/v2/hook/729aca52-5309-4fad-8da9-f54d3981ab0b"
        self.headers = {'Content-Type': 'application/json'}
        self.alertInfo = alertInfo

    def post_to_robot(self, test_flag=False):
        webhook = self.webhook_test if test_flag else self.webhook
        headers = self.headers
        flag = False
        alert_headers = f"台架 {self.alertInfo.ip_address} 告警"
        alert_content = ""
        for key, value in self.alertInfo.alert_info.items():
            if value != "PASS":
                flag = True  # 有失败存在，需发送飞书通知
                show_value = ""
                for i, v in enumerate(value.split("\n")):
                    show_value += f"    <font color='red'>{i+1}. {v}\n</font>"

                alert_content += f"**{key}异常：**\n" + show_value  # 将失败信息添加到飞书通知正文
            # post_bench_check_result(self.alertInfo.ip_address, key, value)  # 将添加检测结果同步到测试平台
        else:
            alert_content = alert_content.rstrip("\n")

        feishu = feishu_api()
        feishu.get_app_access_token()
        feishu.get_user_access_token()
        feishu.get_bitable_app_access_token(document_id="Nm6awGREhiWGPkkux9EcGYsjndd")
        table_id = feishu.get_table_id_by_table_name("标准台架信息汇总")
        message_info = feishu.get_all_records_in_table(table_id)
        user_id = None
        for info in message_info:
            if info['fields']['WifiIP地址'] == self.alertInfo.ip_address:
                user_id = info['fields']['台架Owner'][0]['id']

        if not user_id:
            alert_content += f'\n<at id=all></at>'
        else:
            alert_content += f'\n<at id={user_id}></at>'
        message_body = {
            "msg_type": "interactive",
            "card": {
                "config": {
                    "wide_screen_mode": True
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "content": alert_content,
                            "tag": "lark_md"
                        }
                    }
                ],
                "header": {
                    "template": "red",
                    "title": {
                        "content": alert_headers,
                        "tag": "plain_text"
                    }
                }
            }}
        if flag:  # 有失败存在，需发送飞书通知
            response = requests.request("POST", webhook, headers=headers, data=json.dumps(message_body))
            logger.debug(response)
            logger.debug(type(response))


def post_bench_check_result(agentIP, checkName, checkResult,  path="/benchHealthCheck/append"):
    """
    pytest 执行的S2S自动化测试结果同步到 SOA测试平台
    """
    headers = {'Connection': 'keep-alive',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 ' \
                             '(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
               'Content-Type': 'application/json;charset=utf-8', 'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9', 'Host': '10.80.51.28:8887'}
    data = {'agentIP': agentIP, 'checkName': checkName,
            'checkResult': checkResult}
    url = "http://10.80.51.28:8887" + path
    response = requests.post(url, json.dumps(data), headers=headers)
    resp_body = json.loads(str(response.content, 'utf-8'))
    logger.info("***************获取响应结果********************")
    logger.info(resp_body)
    logger.info("***************获取响应结果********************")
    result = resp_body.get("msg")


if __name__ == "__main__":

    # content = {
    #         "text": '<at user_id="all">所有人</at> 启航！！！'
    #         }
    # text_notice(content)

    # # template_notice 样例
    # content = {"success_rate":"100%"} 
    # template_notice(content)

    # markdown_notice 样例
    # content = {}
    # markdown_notice(content)

    obj = FeishuAlert(None)
    obj.post_to_robot()
