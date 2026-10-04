#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_
"""
@File: data_vo.py
@Time: 2024/5/28 14:03
@Author: lei.hong
@Software: vscode
@Description: vo层埋点数据查询和日志平台基础类
@Examples: 
"""
import json

import requests
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.common.singleton import SingletonMeta
from xat_ecu.legacy.common.exception_error import UnauthorizedError, ClientError, ServerError


class DataRequest(metaclass=SingletonMeta):
    def __init__(self):
        pass

    def _send_request(self, method, url, **kwargs):
        try:
            # 发送请求，可以是GET、POST等
            response = requests.request(method, url, **kwargs)

            # 检查响应状态码，并根据需要抛出异常
            if response.status_code == 401:
                raise UnauthorizedError("Unauthorized: Invalid credentials or expired token.")
            elif 400 <= response.status_code < 500:
                logger.info(f"信息为：method:{method} url:{url} k:{kwargs}")
                logger.info(f"Bad Request: response.json() = {response.json()}")
                raise ClientError(f"Client Error {response.status_code}: {response.reason}")
            elif 500 <= response.status_code < 600:
                logger.info(f"信息为：method:{method} url:{url} k:{kwargs}")
                logger.info(f"Bad Request: response.json() = {response.json()}")
                raise ServerError(f"Server Error {response.status_code}: {response.reason}")

            response.raise_for_status()  # 捕获其他非2xx状态码
            return response.json()

        except json.JSONDecodeError:
            return response.content

        except requests.exceptions.RequestException as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/vo/data_request.py")
            logger.info(f"Request failed: {e}")
            return None

    def get(self, url, headers=None, params=None, auth=None, timeout=None):
        return self._send_request('GET', url, params=params, headers=headers, auth=auth, timeout=timeout)

    def post(self, url, headers=None, data=None, auth=None, timeout=None):
        return self._send_request('POST', url, data=data, headers=headers, auth=auth, timeout=timeout)

    def put(self, url, headers=None, data=None, auth=None, timeout=None):
        return self._send_request('PUT', url, data=data, headers=headers, auth=auth, timeout=timeout)
