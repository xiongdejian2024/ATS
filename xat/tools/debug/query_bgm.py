#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_

"""
@Time: 2022/11/25 17:55  
@Author: lei.tao
@File: query_bgm.py
@Software: PyCharm
@Description: 
@Example: 
"""

from doipclient import DoIPClient
import paramiko


def query_bgm(cmd):
    try:
        address, announcement = DoIPClient.await_vehicle_announcement()
        ip, port = address
        print("BGM的ip地址和端口为:".format(ip, port))
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/debug/query_bgm.py")
        print(e)

    else:
        username = 'root'
        password = __import__("os").environ.get('XAT_CREDENTIAL____DEBUG_QUERY_BGM_PY_PASSWORD', "")
        port = 22

        connection = paramiko.SSHClient()
        connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        connection.connect(ip, port, username, password)
        stdin, stdout, stderr = connection.exec_command(cmd)
        data = stdout.read().decode('utf-8')
        connection.close()
        return data
