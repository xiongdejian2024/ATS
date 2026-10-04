#!/usr/bin/python3
# -*- coding=utf-8 -*-
'''
(C) Copyright Jidu Auto 2023-2023.
    @Author: Edison
    @Date: 2023-06-21
    @Description: 配置文件管理
    @Status: To verify
    @Docs: TODO
'''

import os
import sys
from pathlib import Path

_forder = Path(__file__).resolve().parents[2]
sys.path.append(str(_forder))
from .utils import load_cfgs

CONF_PATH = os.path.join(str(_forder), 'components/pressure')


def load_settings(conf_name) -> dict:
    '''
    读取配置文件
    @param conf_name: 配置文件的路径
    '''
    path = os.path.join(CONF_PATH, conf_name)
    return load_cfgs(path)

def hand_userinfo(res_dict):
    import base64
    new_dict = {}
    for key, value_info in res_dict.items():
        value_info['userinfo']["user"] = base64.b64encode(value_info['userinfo']["user"].encode()).decode()
        value_info['userinfo']["passwd"] = base64.b64encode(value_info['userinfo']["passwd"].encode()).decode()
        new_dict[key] = value_info
    return new_dict

def load_custom_settings(ver_type=0) -> dict:
    '''
    获取各域配置文件
    参考：https://wiki.jiduauto.com/pages/viewpage.action?pageId=534297660
    @param ver_type: 取版本的方式
        0: 最旧版本
        -1: 最新版本
    '''

    data = load_settings(os.path.join('conf', 'custom_settings.json'))
    res = dict()
    for dev_name, dev_infos in data.items():
        res[dev_name] = dev_infos[ver_type]
        
    return res
    # return hand_userinfo(res)

