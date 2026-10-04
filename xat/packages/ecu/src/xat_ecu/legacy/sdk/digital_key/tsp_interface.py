# # -*- coding: utf-8 -*-
import os
import sys
import requests
import uuid

from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding
from groot2.busi_lib.digital_key.manager import *


class DigitalKeyWhiteList:
    def __init__(self, vid='5bf012028724b6e18440a6c1acecb734', tokens=__import__("os").environ.get('XAT_CREDENTIAL_ECU__SDK_DIGITAL_KEY_TSP_INTERFACE_PY_TOKENS', ""),
                 entity_keys=None):
        self.key = ""
        self.tokens = tokens
        self.vid = vid
        # self.rsa = RsaEncrypt(bgm_tsp_rsa_public_key)
        self.entity_keys = [DataTypeHanding.hexstr_to_inlist(key) for key in entity_keys] if entity_keys else None

    def mock_nfc(self, keyid: list):
        # 步骤一
        url = "https://api.jidustaging.com/api/dks/client/mock/insertEntityKeyInfo"
        head = {"Authorization": self.tokens,
                "Content-Type": "application/json"
                }
        body = {
            "keyId": DataTypeHanding.intlist_to_hexstr(keyid),
            "vid": self.vid,
            "keyCategory": 1,
            "keySn": "J12345678"
        }
        req = requests.post(url=url, headers=head, json=body)
        assert req.status_code == 200, f"post请求失败, {req}    {req.text}"
        exe_id = str(uuid.uuid1()).replace("-", "")

        # 步骤二
        url = "https://api.jidustaging.com/api/dks/client/keyEntity/activate"
        head = {"Authorization": self.tokens,
                "Content-Type": "application/json"
                }
        body = {
            "keyId": DataTypeHanding.intlist_to_hexstr(keyid),
            "vid": self.vid,
            "keyCategory": 1,
            "execId": exe_id
        }
        req = requests.post(url=url, headers=head, json=body)
        assert req.status_code == 200, f"post请求失败, {req}    {req.text}"
        logger.info(req.text)

        # 步骤三
        url = "https://api.jidustaging.com/api/dks/client/mock/mockVehicleToTspSlotSync"
        head = {"Authorization": self.tokens,
                "User-Agent": "jiduapp/0.1.0 (Android; 10; HUAWEI; com.jiduauto.app; ELE-AL00; NULL; ccb38608831097736e3fd5a04118e011)"
                }
        last_sync_time = input("从输入云端日志中获取的last_sync_time")
        body = {
            "vid": self.vid,
            "exec_id": exe_id,
            "err": 0,
            "err_msg": "ok",
            "last_sync_time": last_sync_time  # last_sync_time 可以从日志中查询,估计是要手动在云端看第一步和第二步的日志获取
        }
        req = requests.post(url=url, headers=head, data=body)
        assert req.status_code == 200, f"post请求失败, {req}    {req.text}"
        logger.info(req.text)

    def tsp_ble_slot_sync(self):
        """蓝牙钥匙白名单更新，模拟app端触发tsp下发白名单更新，更新的蓝牙钥匙ID即手机app钥匙，在云端有存储钥匙ID"""
        url = "https://api.jidustaging.com/api/dks/client/keyBluetooth/createKey"
        head = {"Authorization": self.tokens,
                "User-Agent": "jiduapp/0.2.0 (iOS; 15.4.1; Apple; jdcomiphone; iPhone 12; NULL; FA7EB098-9B07-4745-87AB-494541838A71)",
                "requesttime": str((round((time.time() * 1000)))),
                "content-type": "application/json"
                }
        body = {'userKeyPk': __import__("os").environ['XAT_CREDENTIAL_SCAN_E0409D34302F0C0EAB77'],
                'vid': self.vid,
                'version': 1}
        req = requests.post(url=url, headers=head, json=body)
        assert req.status_code == 200, f"post请求失败, {req}    {req.text}"
        logger.info(req.text)

    def tsp_rke_se_sync(self, cmd='102023032220175302000005F5E100FFFF0001ED001500A40400104944554155544F20444B205353440100029000000B00CABF2106A60483021540029000000E00A404000949434345444B567631029000000B00CABF2106A60483021540049000698500CB802A1910C67F2181C2930A01851462C05915670720420491564A445F20104A4944554155544F0000000000000000950200805F2504202212095F2404202312097F4945B0400756e2cf89338bc0f5ae38805f21a82961f98e0691f1204d1efdb4f2e349676f9ba3285462c24294947a91318faa1725f6e266239b408ec9968ee2c7b102b14aF001005F37402257ec8fc77a8eba5de204820b2a3da1eb90d4d0699dae338ab2130a1963dd7b6b38abed8fb7503741b260a693ea942f99bd39071f68700cc7d9633e07d217d302900000578082401552A60D9002110395013C8001888101105F4940477d50cddfc3b76e840b7f8e0395f9b1d61f8c2c0254c6ae398226c3bee7ba0dc22aad7cd39676c7cc76541f9bb701fb9d3f17b70f8328fc42d2890acb3f1232029000006D84E2800068E63E279FE8F1B63CED97A8F1F124812F27149B141BD889368E80542C16FAA044FE0774928A8A86320B7466B777DDCB12429FAEF8D00F5C367B96BDCD42A7B1AE53122E508BEE97FAA3B9F62C8F00012EE832D9A7E240C12F716EA67ACEABDC56CF346D582587A433029000'):
        """BNCM个性化数据更新"""
        url = "https://api.jidustaging.com/api/dks/client/mock/pDataUpgradeTaskReq"
        head = {
                "content-type": "application/json"
                }
        exe_id = str(uuid.uuid1()).replace("-", "")
        se_id = str(uuid.uuid1()).replace("-", "")
        body = {'vid': self.vid,
                "execId": exe_id,
                "seId": se_id,
                "scriptId": "2023032220175302000005F5E100FFFF",
                'commands': cmd}
        req = requests.post(url=url, headers=head, json=body)
        assert req.status_code == 200, f"post请求失败, {req}    {req.text}"
        logger.info(req.text)

    def tsp_entity_slot_sync(self, entity_key: list, action: int, mock_ack=False):
        """
        实体卡白名单更新, 模拟app端触发tsp下发实体卡白名单更新
        :param entity_key: 实体钥匙id， intlist
        :param action: action=2-激活/5-禁用/6-恢复
        :param mock_ack: 是否模拟上行
        :return:
        """
        # todo
        # if entity_key not in self.entity_keys:
        #     assert False, f"测试入参错误，{entity_key}不在当前车辆的有效钥匙中"
        url = "https://api.jidustaging.com/api/dks/client/keyEntity/statusManage"
        head = {"Authorization": self.tokens,
                "client": "2",
                "user-agent": "jiduapp/0.5.0 (Android; 10; HUAWEI; com.jiduauto.app; OXF-AN00; NULL; 00000000781ad0450000000011ce64ba; SFdPWEY=)",
                "requesttime": str((round((time.time() * 1000)))),
                "content-type": "application/json"
                }
        exe_id = str(uuid.uuid1()).replace("-", "")
        body = {
            "keyId": DataTypeHanding.intlist_to_hexstr(entity_key).upper(),
            "vid": self.vid,
            "keyCategory": 1,
            "execId": exe_id,
            "action": action
        }
        logger.info(f"url:{url}")
        logger.info(f"header:{head}")
        logger.info(f"body:{body}")
        req = requests.post(url=url, headers=head, json=body)
        assert req.status_code == 200, f"post请求失败, {req}    {req.text}"
        logger.info(req.text)

        if mock_ack:
            url = "https://api.jidustaging.com/api/dks/client/mock/mockVehicleToTspSlotSync"
            head = {"Authorization": self.tokens,
                    "User-Agent": "jiduapp/0.1.0 (Android; 10; HUAWEI; com.jiduauto.app; ELE-AL00; NULL; ccb38608831097736e3fd5a04118e011)"
                    }
            last_sync_time = input("从输入云端日志中获取的last_sync_time")
            body = {
                "vid": self.vid,
                "exec_id": exe_id,
                "err": 0,
                "err_msg": "ok",
                "last_sync_time": last_sync_time
            }
            req = requests.post(url=url, headers=head, data=body)
            assert req.status_code == 200, f"post请求失败, {req}    {req.text}"
            logger.info(req.text)

    def tsp_nfc_learning(self):
        """远程NFC学卡请求"""
        url = "https://api.jidustaging.com/api/dks/client/keyEntity/nfcLearning/start"
        head = {"Authorization": self.tokens,
                "User-Agent": "jiduapp/0.2.0 (iOS; 15.4.1; Apple; jdcomiphone; iPhone 12; NULL; FA7EB098-9B07-4745-87AB-494541838A71)",
                "client": "2"
                }
        body = {
            'ExecId': str(uuid.uuid1()).replace("-", ""),
            'Vid': self.vid}
        req = requests.post(url=url, headers=head, data=body)
        assert req.status_code == 200, f"post请求失败, {req}    {req.text} {head} {body}"
        logger.info(req.text)

if __name__ == '__main__':
    # work dir: /sat/xat_cases/legacy/bgm
    dk_app = DigitalKeyWhiteList()
    # dk_app.mock_nfc(key_id1)
    # dk_app.tsp_ble_slot_sync()
    # dk_app.tsp_entity_slot_sync(key_id1, 5)
    # dk_app.tsp_entity_slot_sync(key_id1, 6)
    # dk_app.tsp_entity_slot_sync(key_id1, 6, True)
    # dk_app.tsp_nfc_learning()
    # dk_app.tsp_rke_se_sync('080102030405060708000024000D00A4040008A000000151000000029000000D80503000082FD4AC3C53DB7426029000')
    dk_app.tsp_rke_se_sync('102023032220175302000005F5E100FFFF0001ED000B00CABF2106A604830215400490006985001500A40400104944554155544F20444B205353440100029000000B00CABF2106A60483021540029000000E00A404000949434345444B56763102900000CB802A1910C67F2181C2930A01851462C05915670720420491564A445F20104A4944554155544F0000000000000000950200805F2504202212095F2404202312097F4945B0400756e2cf89338bc0f5ae38805f21a82961f98e0691f1204d1efdb4f2e349676f9ba3285462c24294947a91318faa1725f6e266239b408ec9968ee2c7b102b14aF001005F37402257ec8fc77a8eba5de204820b2a3da1eb90d4d0699dae338ab2130a1963dd7b6b38abed8fb7503741b260a693ea942f99bd39071f68700cc7d9633e07d217d302900000578082401552A60D9002110395013C8001888101105F4940477d50cddfc3b76e840b7f8e0395f9b1d61f8c2c0254c6ae398226c3bee7ba0dc22aad7cd39676c7cc76541f9bb701fb9d3f17b70f8328fc42d2890acb3f1232029000006D84E2800068E63E279FE8F1B63CED97A8F1F124812F27149B141BD889368E80542C16FAA044FE0774928A8A86320B7466B777DDCB12429FAEF8D00F5C367B96BDCD42A7B1AE53122E508BEE97FAA3B9F62C8F00012EE832D9A7E240C12F716EA67ACEABDC56CF346D582587A433029000')
    # encrypted_data = '\n\xd8\x02EELa8Pbtf+2WQFJs72EzT1+3nVWV/g6enUdKcIBkdYO1ytjiPFrT7fELgFHEHxut+Oi8FsSn9CN3/M6HyeIqOj+AMcZortWARTHj8u3iwJQ5xwf11tmFnT+WE/Uc5OzsEjgYslZy10Yi8reTnp18RZFgl4kf5+ZMkWweG7OxuEwQm9O3KDVAGaAhmIA+ZMdyijP3eHK0KQ0BYB+CVcpd/fGR/qhXIiLpQtjLVwdiaTmuUgkptexKE4nL1nd1IHnR3oQ8wAqdEZ+6MrIYnYlR7l7NVAwiEn19+SacxUmMGVGREeQRWo9GdAc81ISmUxppJA8Iymuk3AyKpmUzINHo1g=='
    # plain = dk_app.rsa.decrypt_data(encrypted_data)
    # print(plain)
    # resp = BLESlotSyncCmdResp()
    # resp.ParseFromString(DataTypeHanding.to_bytes('5C 6E 20 31 66 39 65 63 39 61 65 63 65 36 37 63 30 36 38 61 38 36 63 30 65 38 33 66 64 36 66 36 66 30 62 5C 78 31 30 5C 78 30 31 5C 78 31 61 5C 74 44 65 6C 61 79 46 61 69 6C 20 5C 78 63 30 5C 78 66 66 5C 78 61 39 5C 78 39 34 5C 78 65 31 30'))
    # resp.ParseFromString('\n ef77102c01c788ed87de5fdc4d3f0d55\x10\x01\x1a\tDelayFail \xf8̕\x95\xe10')
    # print(resp)
