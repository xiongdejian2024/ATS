"""
@File        : test_V2TRoutingForwarder.py
@Author      : jingjing.wang
@Time        : 2024/01/05 18:00 PM
@Description : Test s2s interface about bonnet function
"""
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.soa_partner.src.partner_const import *
from xat_cases.legacy.bgm.case_helper.diag_case_helper.DiagTestBase import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.api.constants.common import *

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
@allure.story("互联服务/V2TRoutingForwarderService")
@pytest.mark.wjj
@pytest.mark.tcam
class TestV2TRoutingForwarder(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([("V2TRoutingForwarder", "client","V2TOTAFotaForwarder")])
        self.partner.method_default_timeout = 0.1

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.partner.empty_all()

    def after_each_func(self, ecu):
        if ecu.get("testresult") != "Pass":
            logger.info("case失败，需等待5s让环境恢复")
            sleep(5)
        else:
            sleep(3)  # 避免防玩
        self.ipdu.resume_all_bus_send()
        sleep(1)
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
              
    @allure.title("RVCCmd请求调用车端服务")
    @pytest.mark.smoke
    def test_caseid_1984005(self):
        self.partner.send_request_and_return_resp("V2TRoutingForwarder_client_V2TOTAFotaForwarder","CallVehicleApi",{"api":'ota',
                                                                                                'payload': [0,1,2,3],
                                                                                                'traceId': "123"})["out"]
        

