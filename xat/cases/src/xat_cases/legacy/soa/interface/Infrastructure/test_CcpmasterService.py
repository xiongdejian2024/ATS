# -*- coding: utf-8 -*-
"""
@File        : test_CcpmasterService.py
@Author      : jingjing.wang
@Time        : 2024/01/19 15:00 PM
@Description : Test s2s interface about bonnet function
"""
import json
import time
import requests

from xat_cases.legacy.bgm.case_helper.test_fota_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.soa_partner.src.partner_const import *
from xat_cases.legacy.bgm.case_helper.diag_case_helper.DiagTestBase import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.common.logger import logger, Logger
from xat_ecu.api.constants.common import CCPMasterSts_Field


USAGE_MODE_MAP = {
    0: "ABANDONED",
    1: "INACTIVE",
    2: "CONVENIENCE",
    11: "ACTIVE",
    13: "DRIVING",
}

CAR_MODE_MAP = {
    0: "NORMAL",
    1: "TRANSPORT",
    2: "FACTORY",
    3: "CRASH",
    5: "DYNO",
}

@allure.feature("SOA服务接口")
@allure.story("架构基础/CCPMasterService")
class TestCcpmasterService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.partner = S2sBaseClass([("CCPMasterService", "client" ,"CcpMasterService")])
        self.partner.method_default_timeout = 0.1

    def before_each_func(self, ecu, **kwargs):
        super().before_each_func(ecu, start=False)
        self.partner.empty_all()

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def task_status_change(self, testKey: str, vid: str, status: int):
        """
        任务状态变更

        :param testKey: 测试秘钥
        :param vid:
        :param status: 整形：300或600
        """
        path = "https://fod-server.jidustaging.com/api/fod-server/test/updateVehicleServiceStatus"
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        url = path
        data = {"testKey": testKey, "vid": vid, "fodServiceId": "FOD0001", "status": status}
        response = requests.post(url, json.dumps(data), headers=headers, timeout=5)
        resp_body = json.loads(response.text)
        if resp_body.get("code") == 0:
            logger.info(f"任务状态变更成功")
            return True, "任务状态变更成功"
        else:
            logger.info(f"任务状态变更失败：{resp_body.get('msg')}")
            return False, resp_body.get('msg')


    def distribute_task(self, vid: str, userId: str,operationType: int):
        """
        下发任务

        :param vid:
        :param userId:
        """
        path = "https://fod-server.jidustaging.com/api/fod-server/change/changeService"
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        url = path
        timestamp = int(time.time() * 1000)
        sign = ""
        data = {
                "timestamp": timestamp,
                "vid": vid,
                "userId": userId,
                "thirdOrderNo": timestamp,
                "operationType": operationType,
                "fodServiceId": "FOD0001",
                "subscribe": 1,
                "validForLife": 1,
                "thirdServerCode": "bgm",
                "sign": sign,
                "secretKey": __import__("os").environ.get('XAT_CREDENTIAL____SOA_INTERFACE_INFRASTRUCTURE_TEST_CCPMASTERSERVICE_PY_SECRETKEY', "")
                }
        data["sign"] = self.get_sign_value(data)
        response = requests.post(url, json.dumps(data), headers=headers, timeout=5)
        resp_body = json.loads(response.text)
        if resp_body.get("code") == 0:
            logger.info(f"下发任务成功：{resp_body.get('data')}")
            return True, f"下发任务成功：{resp_body.get('data')}"
        else:
            logger.info(f"下发任务失败：{resp_body.get('msg')}")
            return False, resp_body.get('msg')

    def get_sign_value(self, data: dict):
        """
        生成请求body对应的MD5值
        """
        list_aa = []
        for key in data:
            if key == 'sign':
                continue
            list_aa.append(key + str(data[key]))
        else:
            list_aa.sort()  # 对列表内的元素进行默认排序
            my_str = ''.join(list_aa)
            md5_value = md5(my_str.encode('utf-8')).hexdigest()
            return md5_value   

    @allure.title("获取当前进度")
    @pytest.mark.sanity
    def test_caseid_1984131(self):
        self.restart_bgm_and_connect_service(CCPMASTER_SERVICE_CLIENT)
        self.partner.send_request_and_ck_resp(CCPMASTER_SERVICE_CLIENT,"GetCCPActiveProgress",{},{"out":{"taskInfo":{"taskId":0,"modifyBy":"","modifyExt":""},"progress":0}})

    @allure.title("获取CCPMaster条件检查结果")
    @pytest.mark.smoke
    def test_caseid_1984135(self):
        self.partner.send_request_and_ck_resp(CCPMASTER_SERVICE_CLIENT,"GetConditionCheckInfo",{},{"out":{"taskInfo":{"taskId":0,"modifyBy":"","modifyExt":""},"conditionCheck":[]}})

    @allure.title("通知当前进度/通知CCPMaster状态/通知CCPMaster 条件检查结果")
    @pytest.mark.sanity
    def test_caseid_1984340_1984341_1984342(self):
        pass
        #手动测试,ccp云端是正式环境网络隔离无法调用
        # self.task_status_change(testKey="${XAT_CREDENTIAL_SCAN_26E94F3E49C4B2A0A55A}",
        #                         vid="df3bdf5443de8963a54e6d875d65a3a3",
        #                         status=300)
        # self.distribute_task(vid= "df3bdf5443de8963a54e6d875d65a3a3",
        #                      userId="1254382316769029465",
        #                      operationType=1)
        # # self.partner.ck_s2s_event(CCPMASTER_SERVICE_CLIENT,"CCPActiveProgress",{"progressInfo":
        # #                                                                         {"progress":1,
        # #                                                                          "taskInfo":{"taskId":0,"modifyBy":"","modifyExt":""}}})
        # time.sleep(100)
        
@allure.feature("SOA服务接口")
@allure.story("架构基础/CCPMasterService")
class TestCcpmasterFotaService(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("V2TRoutingForwarder","client","V2TCcpForwarder"),
                         ("CCPMasterService", "client" ,"CcpMasterService"),
                         ("VehicleModeService_client"),("FotaMasterService","client"),
                                 ("UpdateAgentService","client","BGM_UA_Service")])
        self.ssh.ccp_skip_debug([Ccp_Skip_Debug.skip_verify,
                                 Ccp_Skip_Debug.skip_acu,
                                 Ccp_Skip_Debug.skip_cdc])

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.mix.back_ccp_status_to_Idle()#强制回到idle状态
        self.io.bgm_diag_line_down()
        self.bus_comm.set_vehspd_gear(vehspd=0.0)


    def after_each_func(self, ecu):
        self.io.bgm_diag_line_up()
        super().after_each_func(ecu)

    def after_class(self, ecu):
        super().after_class(self, ecu)
        
    @allure.title("获取CCPMaster状态")
    @pytest.mark.sanity
    def test_caseid_1984132(self):
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)#下发fod的任务
        assert self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.SUCCESS.value,timeout=120)#校验下发成功
        assert self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.IDLE.value,timeout=120)#校验idle状态
        # assert self.soa.get_ccp_status(CCPMasterSts_Field.TaskInfo) == {"taskId":66666,"modifyBy":"fod","modifyExt":'{"orderNo":"bgm@#_#@1710144934508@#_#@27@#_#@1710144934827","operationType":2,"serviceId":"FOD0001"}'}#校验任务详情
        assert self.soa.get_ccp_status(CCPMasterSts_Field.TaskInfo) != None#校验任务详情
        assert self.soa.get_ccp_status(CCPMasterSts_Field.State) == 0
        assert self.soa.get_ccp_status(CCPMasterSts_Field.ErrorCode) == 0
        self.mix.back_ccp_status_to_Idle()#执行完fod任务强制清除避免影响下一条case