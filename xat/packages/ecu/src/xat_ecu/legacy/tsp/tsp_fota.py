import json
import requests
import os,sys
current_path = os.path.dirname(os.path.realpath(__file__))
from xat_ecu.legacy.common.logger import *

BASE_URL = "https://fota.jidustaging.com/api/fota"  # 上海 fota 测试台架是 staging 环境的


class OtaPortalTask(object):
    def __init__(self, task_id) -> None:
        self.task_id = task_id

    def post(self, url, data):
        headers = {"Content-Type": "application/json"}
        r = requests.post(url=url, data=data, headers=headers)
        logger.debug(url)
        logger.debug(data)
        logger.debug(r.text)
        json_r = json.loads(r.text)
        return json_r

    def repub(self, client_id):
        logger.info("mock ota send repub cmd!")
        url = f"{BASE_URL}/automation/task/reDeployTask"
        data = json.dumps({"taskId": self.task_id, "clientId": client_id})
        return self.post(url=url, data=data)

    def cancel(self, client_id, vid):
        logger.info("mock ota send cancel cmd!")
        url = f"{BASE_URL}/automation/vehicle/cancel"
        data = json.dumps(
            {
                "taskId": self.task_id,
                "clientId": client_id,
                "vid": vid,
            }
        )
        return self.post(url=url, data=data)

if __name__ == '__main__':
    c = OtaPortalTask("1120")
    # c.cancel("a123456","9366fa1967dd7c46d10d464b2683a28a")
    c.repub("a123456")
