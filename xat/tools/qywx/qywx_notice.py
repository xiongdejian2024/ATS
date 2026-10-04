# -*- coding: utf-8 -*-
"""
@File        : qywx_notice.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2022/11/29 18:00 PM
@Description : qyapi.weixin
@Examples    : Example of qiye WeChat notification
"""

import os
import json

soa_test_webhook = __import__("os").environ['XAT_CREDENTIAL_SCAN_120CBDDEB95193B27323']
test_webhook = __import__("os").environ['XAT_CREDENTIAL_SCAN_98CF2F3686E50E2C6982']

def text_notice():
    content = {
                "content": "Hello, 各位伙伴，请开会前 提前更新好自己的任务状态，并建立好需求或后续任务！ ----  测开会议",
                "mentioned_mobile_list":["@all"]
                }
    # content_jsonstr = json.dumps(content)
    content_jsonstr = content
    text_content = {
            "msgtype": "text",
            "text": content_jsonstr
            }
    text_content = json.dumps(text_content)
    # text_content = '{\
    #         "msgtype": "text",\
    #         "text": {\
    #             "content": "Hello, 各位伙伴，请开会前 提前更新好自己的任务状态，并建立好需求或后续任务！ ----  测开会议",\
    #             "mentioned_mobile_list":["@all"]\
    #             }\
    #         }'
    cmd = "curl '{}' -H 'Content-Type: application/json' -d '{}'".format(test_webhook, text_content)
    print(cmd)
    res = os.system(cmd)
    if res == 0:
        print("text_notice cmd success")
    else:
        print("text_notice cmd res is {}, ----- run failed".format(res))

if __name__=="__main__":
   # work dir: any
   # cmd: 
   text_notice()