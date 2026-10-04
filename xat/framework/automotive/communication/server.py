#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :server.py
@Time         :2024/10/28 11:31
@Author       :dejian.xiong@jiduauto.com
@Description  :
"""
import socket
from pathlib import Path

from threading import Thread

from flask import request, jsonify

from framework.automotive.utils.conftest_helper import parent_dir
from xat_ecu.legacy.common.logger import logger


def find_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))  # 绑定到一个随机的空闲端口
    free_port = s.getsockname()[1]  # 获取刚刚绑定的端口
    s.close()  # 关闭socket
    return free_port


class DistServer(Thread):
    def __init__(self, service_ip='0.0.0.0', service_port=9999):
        super().__init__()
        self.service_ip = service_ip
        self.service_port = service_port
        self.client_dict = {}
        self.socketio = None
        self.callback = None

    def run(self):
        self.server_start()

    def set_callback(self, callback):
        self.callback = callback

    def server_start(self):
        from flask import Flask
        from flask_socketio import SocketIO
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'secret!'
        self.socketio = SocketIO(app)

        @app.route('/stop', methods=['POST'])
        def stop_task():
            req = request.json
            client_ip = req.get('client_ip')
            message = {}
            message['client_ip'] = client_ip
            message['title'] = 'handle_stop_task'
            message['socket_io'] = self.socketio
            logger.info(f"接收到[{client_ip}]的消息:stop {client_ip}的任务")
            logger.debug(f"self.client_dict:{self.client_dict}")
            if client_ip in self.client_dict.keys():
                message['sid'] = self.client_dict[client_ip]['sid']
                message['req'] = req
                self.callback(message)
                return jsonify({'status': 'success', 'code': 200})
            else:
                return jsonify({'status': 'fail', 'code': 200})

        @app.route('/start', methods=['POST'])
        def start_task():
            client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
            req = request.json
            logger.info(f"接收到[{client_ip}]的消息:{req}")
            message = {}
            message['client_ip'] = client_ip
            message['title'] = 'handle_start_task'
            message['req'] = req
            self.callback(message)
            return jsonify({'status': 'success', 'code': 200})

        @app.route('/upload', methods=['POST'])
        def upload_file():
            file = request.files['file']
            file_path = Path(parent_dir) / '../report/allure_report' / file.filename
            try:
                # 将文件保存到指定目录
                with open(f'{file_path}', 'wb') as f:
                    f.write(file.stream.read())
                logger.debug(f"{file_path}文件保存成功")
                return jsonify({'status': 'success', 'code': 200})
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/communication/server.py")
                logger.error(f"{file_path}文件保存失败，失败原因:{str(e)}")
                return jsonify({'status': 'fail', 'code': 200})

        @app.route('/tasks', methods=['GET'])
        def list_all_tasks():
            message = {}
            message['title'] = 'list_all_tasks'
            data = self.callback(message)
            return jsonify({'status': 'success', 'code': 200, 'data': data})

        @app.route('/status', methods=['GET'])
        def list_all_slave_status():
            message = {}
            message['title'] = 'list_all_slave_status'
            data = self.callback(message)
            return jsonify({'status': 'success', 'code': 200, 'data': data})

        @self.socketio.on('message')
        def handle_message(message):
            """处理客户端发送的消息"""
            client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
            sid = request.sid
            logger.debug(f'接收到[{client_ip}_{sid}]的消息: {message}')
            message['client_ip'] = client_ip
            message['sid'] = sid
            self.callback(message)
            return 'success'

        @self.socketio.on('connect')
        def connect():
            """处理连接事件"""
            client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
            logger.info(f"{client_ip}已上线")
            sid = request.sid
            message = {}
            message['client_ip'] = client_ip
            message['sid'] = sid
            self.client_dict[client_ip] = dict(sid=sid, ip=client_ip)
            self.callback(message)

        @self.socketio.on('disconnect')
        def disconnect():
            """处理断开连接事件"""
            client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
            sid = request.sid
            message = {}
            message['client_ip'] = client_ip
            message['sid'] = sid
            if client_ip in self.client_dict.keys():
                del self.client_dict[client_ip]
                self.callback(message)
                logger.info(f"{client_ip}已断开")

        self.socketio.run(app, host=self.service_ip, port=self.service_port, allow_unsafe_werkzeug=True)
