#!/usr/bin/python3
# coding=UTF-8

import os
import logging
import requests

# 文档发送到企微
send_url = __import__("os").environ['XAT_CREDENTIAL_SCAN_8A4B4CBFB5353D427424']
upload_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=e6664db4-6fb8-4e1c-8de3-020383add0d6&type=file'
MONITOR = {'robot_id': 'e6664db4-6fb8-4e1c-8de3-020383add0d6'}


def send_wechat_file(robot_id, path):
    '''
    文档发送到企微
    '''
    data = {'file': open(path, 'rb')}
    id_url = upload_url.format(MONITOR.get(robot_id))
    response = requests.post(url=id_url, files=data)
    json_res = response.json()
    media_id = json_res['media_id']

    data = {
        "msgtype": "file",
        "file": {"media_id": media_id}
    }
    try:
        result = requests.post(url=send_url.format(
            MONITOR.get(robot_id)), json=data)
        logging.info('文档已发送到企业微信群')
        return result
    except Exception as e:
        logging.info(f'文档发送企业微信群 failed:{e}')


def send_message(host_ip, version, cdca_version, tcam_version, acu_version):
    os.system(
        __import__("os").environ['XAT_CREDENTIAL_SCAN_A5086C4DB3EC7EEAB93C'])


def send_in_message(version, cdca_version, tcam_version, acu_version, index, host_ip, wiki_url):
    os.system(
        __import__("os").environ['XAT_CREDENTIAL_SCAN_DDB0A9B22141DB67F9E5'])


def send_out_message(version, cdca_version, tcam_version, acu_version, index, host_ip, wiki_url):
    os.system(
        __import__("os").environ['XAT_CREDENTIAL_SCAN_73477E90FD57F48585D1'])
