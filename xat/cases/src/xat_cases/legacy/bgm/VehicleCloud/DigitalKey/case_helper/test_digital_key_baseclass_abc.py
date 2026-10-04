#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_peps_baseclass.py
@Time         :2024/03/13 13:56:21
@Author       :hui.zhao@jiduauto.com
@Description  :数字钥匙基础测试类
"""

import os
import sys
import httpx
import json
import pytest
import allure
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.legacy.sdk.digital_key.digital_key_const import *
from groot2.cloud.biz.digital_key.manager import DigitalKeyManager
# from test_case.bgm.VehicleCloud.DigitalKey.case_helper.digital_key_s2s import *
from xat_ecu.api.abc_interface import *

class TestDigitalKeyBase(TestABCBase):
    """数字钥匙测试用例类"""
    def before_class(self, ecu):
        self.soa.update(
            [
                "CentralLockService_client",
                "KeyService_client",
                "RPAAPAService_server",
                "TailGateService_client",
                "LightService_client",
                "VehicleModeService_client",
                "VehicleSetStatusService_client",
                "SeatService_client",
                "DoorService_client",
                ('CdcTtsService','server','cdc_a_ttsservice',600),
            ]
        )
        sleep(2)
        self.soa.soa_partner.register_callback("RPAAPAService_server", self.soa.on_GetAPAStatus)
        self.bus_comm.start_dk()
        self.uid = self.tc_config.get('uid') if self.tc_config.get('uid') != None else self.tsp.get_uid()
        self.tsp_dk = DigitalKeyManager(vid= self.tc_config.get('vid'),
                                     tel= self.tc_config.get('tel'),
                                     user_agent ="jiduapp/0.9.3 (iOS; 16.0; apple; jdcomiphone; iPhone 12; NULL; BF983636-D3F2-4805-90B4-77C3DC75D433; aVBob25l)")
        sleep(2)

    def before_each_func(self, ecu):
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.All,sts=PosnLampSts.Off)
        self.mix.set_digital_key_pre_condition()

    def after_each_func(self, ecu):
        self.soa.empty_all()
        if ecu.get("testresult") != "Pass":
            logger.info("case失败，需等待10s让环境恢复")
            sleep(3)
        else:
            sleep(3)  # 防止触发解闭锁防玩
 
    def after_class(self, ecu):
        self.bus_comm.dk.stop_dk()
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
    
    def mock_pes_sign(self,key, return_full=False):
        url = "https://sec.jidutest.com/api/dashboard-backend/whitebox/encrypt"
        user_info = {
            "user_name": "hui.zhao",
            "password": __import__("os").environ.get('XAT_CREDENTIAL____BGM_VEHICLECLOUD_DIGITALKEY_CASE_HELPER_TEST_DIGITAL_KEY_BASECLASS_ABC_PY_PASSWORD', ""),
            "client_id": "4bbc7b534a444951",
            "endpoint": "https://passport-canary.jidutest.com/api/passportb",
            "client_secret": __import__("os").environ.get('XAT_CREDENTIAL____BGM_VEHICLECLOUD_DIGITALKEY_CASE_HELPER_TEST_DIGITAL_KEY_BASECLASS_ABC_PY_CLIENT_SECRET', "")
        }
        logger.info(f"-------->self.vid:{self.tsp_dk.vid},self.uid:{self.uid}")
        res = self.tsp_dk.auth.get_vehicle_platform_token(env_name="test", userinfo=user_info)
        logger.info(f"res:{res}")
        token = res["token"]
        time_stamp = str((round((time.time() * 1000))))[:10]
        content = str(time_stamp) + ':' + key + ':' + str(self.uid)
        result = httpx.post(
            timeout=None,
            url=url,
            headers={
                "Content-Type": "application/json",
                "Authorization": token
            },
            content=json.dumps(
                {
                    "content": content,
                    "uid": self.uid
                }
            ),
        ).json()

        logger.info(f"content:{content}")
        logger.info(f"result:{result}")
        return result if return_full else result["data"]

    def nfc_learning(self):
        """NFC 卡学习"""
        pes_sign = self.mock_pes_sign(key=self.tsp_dk.vid)
        params = {"execId": self.tsp_dk.exec_id, "vid": self.tsp_dk.vid}
        headers = {"Authorization": self.tsp_dk.token, "user-agent": self.tsp_dk.user_agent,"pes-sign": pes_sign,"client": "2"}
        logger.info(f"------>请求参数：url:api/dks/client/keyEntity/nfcLearning/start, para:{params},headers:{headers}")
        json_r = httpx.post(
            url=self.tsp_dk.url_manager.get_url(
                path="api/dks/client/keyEntity/nfcLearning/start"
            ),
            json=params,
            headers=headers,
        ).json()
        logger.info(f"------>请求返回的结果:{json_r}")
        return json_r

    def key_entity_status_manage(
        self,
        key_id: str,
        key_category: int,
        action: int,
    ):
        """实体钥匙状态管理

        Args:
            action:
                5: 禁用.
                6: 恢复.
            key_category:
                1: NFC 卡.
                2: UWB 智能钥匙.
            key_id: 实体钥匙 ID.
        """
        url = self.tsp_dk.url_manager.get_url(path="api/dks/client/keyEntity/statusManage")
        pes_sign = self.mock_pes_sign(key="74680000000000000000000000000001")

        payload = json.dumps(
            {
                "keyId": key_id,
                "keyCategory": key_category,
                "vid": self.tsp_dk.vid,
                "execID": self.tsp_dk.exec_id,
                "action": action,
            }
        )
        json_r = httpx.post(
            url=url,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": self.tsp_dk.token,
                "pes-sign": pes_sign,
                "client": "2",
            },
        ).json()
        logger.debug(json_r)
        return {"code": json_r["code"], "msg": json_r["msg"]}

    def tsp_entity_slot_sync(self, nfc_card, action, key_category=1):
        """
        实体卡白名单更新, 模拟app端触发tsp下发实体卡白名单更新
        :param nfc_card: nfc卡id， intlist
        :param action: action=5-禁用/6-恢复
        :param key_category: 1: NFC 卡, 2: UWB 智能钥匙
        :return:
        """
        with allure.step("模拟App触发实体卡白名单更新"):
            self.tsp_dk.key_entity_status_manage(nfc_card, key_category, action)
    
    def tsp_rke_se_sync(self, cmd):
        """
        模拟app端触发tsp下发实体卡白名单更新
        :param cmd: 命令
        :return:
        """
        with allure.step("模拟App触发tsp_rke_se_sync"):
            self.tsp_dk.tsp_rke_se_sync(cmd)
    
    def create_bluetooth_digital_key(self, version: int = 1):
        """创建蓝牙数字钥匙

        Args:
            version (int, optional): 版本号. Defaults to 1.

        Returns:
            dict: 接口返回内容.
        """
        url = self.tsp_dk.url_manager.get_url(path="api/dks/client/keyBluetooth/createKey")
        user_key_pk = self.tsp_dk.generate_user_key_pk()
        payload = json.dumps(
            {
                "userKeyPk": user_key_pk,
                "vid": self.tsp_dk.vid,
                "version": version,
            }
        )
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.tsp_dk.token,
            "User-Agent": self.tsp_dk.user_agent,
            "requesttime": str((round((time.time() * 1000)))),
            "client": "2",
        }
        json_r = httpx.post(
            url=url,
            data=payload,
            headers=headers,
        ).json()
        self.debug(url, payload, headers, json_r)
        return json_r
