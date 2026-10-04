#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :feishu_task.py
@Time         :2024/8/01 11:48
@Author       :lei.hong@jiduauto.com
@Description  :
"""
import json
import os
import sys
from datetime import datetime
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

from tools.feishu.feishu_task import update_task_info
from xat_ecu.legacy.interface.feishu.feishu_api import feishu_api


def main():
    if len(sys.argv) == 2:
        task_des = sys.argv[1]
    else:
        task_des = "BGM任务1"
    source_feishu = feishu_api()
    source_feishu.get_app_access_token()
    source_feishu.get_user_access_token()
    document_id = 'U7OUwlovWiddnwkZDTwcINsrnRe'

    source_feishu.get_bitable_app_access_token(document_id=document_id)

    dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ts = int(time.mktime(time.strptime(dt, "%Y-%m-%d %H:%M:%S"))) * 1000
    update_task_info(source_feishu, "任务描述", task_des, "结束时间", ts)


if __name__ == '__main__':
    main()
