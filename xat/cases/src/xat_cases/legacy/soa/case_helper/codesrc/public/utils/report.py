#!/usr/bin/python3
# -*- coding=utf-8 -*-
'''
(C) Copyright Jidu Auto 2023-2023.
    @Author: Edison
    @Date: 2023-07-04
    @Description: 报告
    @Status: In progress
    @Docs: TODO
'''

from pathlib import Path
import requests
from .log import logger
from .utils import get_host_ip


class WechatTools(object):
    '''
    @desp: 企微工具
    '''
    # TODO robot_id 考虑放到配置文件中获取
    robot_id = '069b3299-d58f-4382-9047-b7b6ed9a961e'

    @classmethod
    def log(cls, data=None, json=None, robot_id=None):
        '''
        @desp: 在企微发送消息
        @param msg: 消息内容
        '''
        if robot_id is not None:
            cls.robot_id = robot_id

        url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={cls.robot_id}'
        return cls._request(url, data=data, json=json)

    @classmethod
    def log_by_willow(
        cls,
        msg,
        url='https://willow.jiduprod.com/api/willow-service/flow/flow/ed7d99d0-ee95-439b-a693-ad65985aaf7a/run/',
        token=__import__("os").environ.get('XAT_CREDENTIAL____SOA_CASE_HELPER_CODESRC_PUBLIC_UTILS_REPORT_PY_TOKEN', ""),
    ):
        if url is None:
            logger.error('Please set the url before use this function')
            return None

        host_ip = get_host_ip()
        if host_ip is None:
            return False, None
        headers = {'Authorization': f'Token {token}'}
        data = {'remark': f'IP:{host_ip} {msg}'}

        return cls._request(url, headers=headers, data=data)

    @classmethod
    def send(cls, file_path):
        if not Path(file_path).exists():
            logger.error(f'File not exist: {file_path}')
        send_url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={cls.robot_id}'
        upload_url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={cls.robot_id}&type=file'
        id_url = upload_url.format(cls.robot_id)
        data = {'file': open(file_path, 'rb')}
        response = requests.post(url=id_url, files=data)
        json_res = response.json()
        media_id = json_res['media_id']
        data = {
            "msgtype": "file",
            "file": {"media_id": media_id}
        }
        return cls._request(url=send_url, json=data)

    @staticmethod
    def _request(url, data=None, json=None, **kwargs):
        err = False
        res = None

        try:
            res = requests.post(url, data, json, **kwargs)
        except Exception as e:
            logger.error(f'Request error: {e}')
            err = True
        return (err, res)
