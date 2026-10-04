#!/usr/bin/python3
# coding=UTF-8
import json
import os
import requests
import time
from nextcloud_client import Client


class WebDriverTool(object):
    def __init__(self, **kwargs):
        self.remote_dir = '/CDC/soa_sdk_tools/service'
        self.host = "http://172.18.74.3"
        self.web_driver_status = False
        self.web_driver = self.init_web_driver()
        self.feishu_ai_url = "https://open.feishu.cn/open-apis/bot/v2/hook/fe939ad1-8003-43c7-935d-9eb4f7298842"
        self.user_id = "412dd94c"
        self.remote_service_list = []

    def init_web_driver(self):
        """ init web driver
        "NextCloud": {
            "HOST": "http://youzi.jidudev.com",
            "PORT": 80,
            "USER": "pyNC",
            "PASSWD": "pyNC0524."
            }
        """
        # host = "http://youzi.jidudev.com"
        port = 80
        web_driver = Client(host=self.host, port=port)
        print("init web driver")
        return web_driver

    def login(self):
        if not self.web_driver_status:
            """
            "USER": "pyNC",
            "PASSWD": "pyNC0524."
            """
            user = "pyNC"
            passwd = __import__("os").environ.get('XAT_CREDENTIAL_ECU__TOOLS_SETUP_ENV_DOWNLOAD_SERVICE_FROM_YOUZI_PY_PASSWD', "")
            try:
                requests.get(self.host, timeout=1)  # verify net
                self.web_driver.login(user=user, password=passwd)
                self.web_driver_status = True
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/tools/setup_env/download_service_from_youzi.py")
                print(f'{e}')
                self.web_driver_status = False
        else:
            print("Already login.")

    def logout(self):
        if self.web_driver_status:
            self.web_driver.logout()
            self.web_driver_status = False
        else:
            print("Already logout.")

    def get_web_driver_status(self):
        return self.web_driver_status

    def set_web_driver_status(self, web_driver_status):
        self.web_driver_status = web_driver_status

    def get_web_driver(self):
        return self.web_driver

    def _send_feishu_notice(self, message, user_id, flow_result_id=None, is_notice=True):
        if not is_notice:
            user_id = ''
        headers = {
            "Content-Type": "application/json"
        }
        if flow_result_id is None:
            url = 'https://willow.jiduprod.com/flow/flow_history?flowID=2fec7c51-3358-4efc-bf72-c4621bcc23be'
        else:
            url = f"https://willow.jiduprod.com/flow/flow_history?flowID=f4edfadf-835e-4fe0-928f-908e0e8059b6&flowHistoryTab=SonTask&pageNum=1&id={flow_result_id}"
        data = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": "soa partner编译通知",
                        "content": [
                            [{
                                "tag": "text",
                                "text": f"{message}\n"
                            },
                                {
                                    "tag": "a",
                                    "text": "请查看",
                                    "href": url
                                },
                                {
                                    "tag": "at",
                                    "user_id": f"{user_id}"
                                }
                            ]
                        ]
                    }
                }
            }
        }
        response = requests.post(self.feishu_ai_url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            print("消息发送成功")
        else:
            print("消息发送失败")

    def download_all_service(self, sdk, jidl, out_path, tag, is_notice):
        self.remote_service_list = self.web_driver.get_file_list(self.remote_dir)
        jidl_tag = jidl.strip().split("RELEASE_")[1]
        service_name = f'{sdk}_jidl{jidl_tag}'

        if service_name not in self.remote_service_list.keys():
            print(f"{service_name} is not exist")
            print('正在云端触发willow编译版本')
            self._send_feishu_notice(message=f"{service_name} is not exist", user_id=self.user_id, is_notice=is_notice)
            flow_result_id = self.willow_job_run(sdk, jidl, tag)
            if flow_result_id:
                print(flow_result_id)
                ret = self.check_willow_job_status(flow_result_id)
                if not ret:
                    self._send_feishu_notice(message=f"{service_name}编译失败", user_id=self.user_id,
                                             flow_result_id=flow_result_id, is_notice=is_notice)
                    raise Exception('编译失败')
                else:
                    return
            else:
                self._send_feishu_notice(message=f"编译{service_name}版本时，请求willow失败", user_id=self.user_id,
                                         flow_result_id=flow_result_id, is_notice=is_notice)
                raise Exception('willow云端请求失败')
        try:
            remote_service_dir = f"{self.remote_dir}/{service_name}"
            self.web_driver.get_directory_as_zip(remote_service_dir, os.path.join(out_path, f"soa.zip"))
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/tools/setup_env/download_service_from_youzi.py")
            print(f"{e}")

    def willow_job_run(self, sdk, jidl, tag):
        url = 'https://willow.jiduprod.com/api/willow-service/flow/flow/f4edfadf-835e-4fe0-928f-908e0e8059b6/run/'
        remark = f'{sdk} {jidl}'
        # X86: "bootes1.4.1r504", idl: "JIDL_RELEASE_1.4REL_12", JIDLCompiler: "bootes1.4.1r504"
        headers = {
            'Authorization': __import__("os").environ.get('XAT_CREDENTIAL_ECU__TOOLS_SETUP_ENV_DOWNLOAD_SERVICE_FROM_YOUZI_PY_AUTHORIZATION', "")
        }
        if tag is None:
            tag = sdk
        data = {
            'remark': remark,
            'token': __import__("os").environ.get('XAT_CREDENTIAL_ECU__TOOLS_SETUP_ENV_DOWNLOAD_SERVICE_FROM_YOUZI_PY_TOKEN', ""),
            'x86_tag': sdk,
            'tool_repo': 'Tools_Utils',
            'tools_tag': tag,
            'sdk_autobuild': 'false',
            'jidl_service_tag': jidl
        }
        ret = requests.post(
            url=url,
            headers=headers,
            data=data
        )
        ret_json = ret.json()
        if ret_json:
            print(ret_json)
            if ret_json.get('code') == 200:
                flow_result_id = ret_json.get('data').get('flow_result_id')
                print(f'获取云端任务:{flow_result_id}')
                return flow_result_id
        raise Exception('job触发失败')

    def check_willow_job_status(self, flow_result_id, timeout=3600):
        start_time = time.time()
        job_history = f'https://willow.jiduprod.com/flow/flow_history?flowID=f4edfadf-835e-4fe0-928f-908e0e8059b6&flowHistoryTab=SonTask&pageNum=1&id={flow_result_id}'
        while time.time() - start_time <= timeout:
            url = f'https://willow.jiduprod.com/api/willow-service/flow/results/{flow_result_id}/'
            ret = requests.get(url=url)
            ret_json = ret.json()
            if ret_json:
                if ret_json.get('code') == 200:
                    status = ret_json.get('data').get('status')
                    if status == 'IN PROGRESS':
                        print('云端正在编译中, 等待60s')
                        time.sleep(60)
                        continue
                    elif status == 'FAIL':
                        print(f'编译失败, job链接：{job_history}')
                        return False
                    elif status == 'SUCCESS':
                        print('编译成功')
                        return True
            time.sleep(60)
        if time.time() - start_time > timeout:
            print('编译超时退出')
            return False
