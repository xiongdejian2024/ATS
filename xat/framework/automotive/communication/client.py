#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :client.py
@Time         :2024/10/28 11:31
@Author       :dejian.xiong@jiduauto.com
@Description  :
"""

from queue import Queue
from threading import Thread

import socketio

from xat_ecu.legacy.common.logger import logger

RECONNECTION_ATTEMPTS = 10  # 重连次数
RECONNECTION_DELAY_MAX = 60  # 最大重连延迟时间，单位为秒
RECONNECTION_DELAY = 10  # 重连延迟时间，单位为秒


class DistClient(Thread):
    def __init__(self, ip, port, queue: Queue, namespace='/'):
        super().__init__()
        """
        初始化DistClient对象
        :param url: Socket.IO服务器的URL
        :param namespace: Socket.IO的命名空间，默认为'/'
        """
        self.ip = ip
        self.port = port
        self.url = f'http://{self.ip}:{self.port}'
        self.queue = queue
        self.namespace = namespace
        self.sio = socketio.Client(reconnection_delay_max=RECONNECTION_DELAY_MAX,
                                   reconnection_delay=RECONNECTION_DELAY,
                                   reconnection_attempts=RECONNECTION_ATTEMPTS)
        self.ack = False

    def run(self):
        # 绑定事件处理函数
        self.sio.on('connect', self.on_connect)
        self.sio.on('disconnect', self.on_disconnect)
        self.sio.on('message', self.on_message)
        self.sio.connect(self.url)
        self.sio.wait()

    def on_connect(self):
        """
        连接成功时调用
        """
        logger.info(f'连接服务器{self.url}成功')

    def on_disconnect(self):
        """
        断开连接时调用
        """
        logger.info(f'与服务器{self.url}断开连接')

    def on_message(self, data):
        """
        接收到消息时调用
        :param data: 接收到的消息内容
        """
        logger.debug(f"接收到来自服务器{self.url}的消息：{data}")
        self.queue.put(data)

    def connect(self):
        """
        连接到Socket.IO服务器
        """
        self.sio.connect(self.url, namespaces=[self.namespace])

    def disconnect(self):
        """
        断开与Socket.IO服务器的连接
        """
        self.sio.disconnect()

    def _master_ack(self, *args):
        if args and args[0] == "success":
            self.ack = True
            logger.info(f"服务器成功接收到客户端消息")
        else:
            self.ack = False
            logger.error(f"服务器未接收到客户端的消息")

    def send_event(self, event='message', data=None):
        """
        向服务器发送事件
        :param event: 事件名称
        :param data: 发送的数据
        """
        try:
            self.sio.emit(event, data, namespace=self.namespace, callback=self._master_ack)
        except Exception as e:
            logger.exception(f"向服务器{self.url}发送事件{event}失败: {e}")
            self.ack = False
        else:
            if self.ack:
                logger.debug(f"向服务器{self.url}发送事件{event}成功，数据为{data}")
            else:
                logger.debug(f"向服务器{self.url}发送事件{event}失败，数据为{data}")
