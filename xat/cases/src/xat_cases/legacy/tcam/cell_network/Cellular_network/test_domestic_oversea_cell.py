#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_

import time
import allure
import pytest

from threading import *

from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.api.constants.config_data import *

RESET_SERVICE_CLIENT_TCAM = "ResetSOAConfigService_client_TcamResetSOAConfigService"


@allure.feature("TCAM交付")
@allure.story("蜂窝网络海外测试")
class Test_Cellular_Oversea(TestABCBase):

    def before_class(self, ecu):
        # self.soa.update(["NetStatService_client", "ResetSOAConfigService_server", "VehicleModeService_server"])
        self.soa.update(["NetStatService_client", ("ResetSOAConfigService", "client", "TcamResetSOAConfigService")])
        sleep(5)
        super().before_class(self, ecu)


    def before_each_func(self, ecu):
        self.soa.empty_all()
        logger.info("检查时间同步状态： {0}".format(self.ssh.tcam_ssh.exec("date")))
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        self.bus_comm.send_ccp_to_tcam(ccp_byte_index=948, ccp_value=0x00)
        self.soa.send_SetNetResidentSts_req(is_5G=True)
        super().after_class(self, ecu)


    @pytest.mark.sanity
    @allure.title("蜂窝网络出厂默认值")
    def test_caseid_1990370(self):
        self.bus_comm.send_ccp_to_tcam(ccp_byte_index=948, ccp_value=0x01)
        self.ssh.type_commands(DeviceName.TCAM, "pkill -f Cell", timeout=5)
        sleep(20)
        self.soa.send_method_request(RESET_SERVICE_CLIENT_TCAM, "ResetAllVehicleSOAConfig", {})
        self.soa.ck_s2s_event(RESET_SERVICE_CLIENT_TCAM, "ResetAllVehicleSOAConfigResult", {"sts":2})
        self.soa.send_Get5GNetSts_req_and_ck_resp(SA_sts.Off)

        self.bus_comm.send_ccp_to_tcam(ccp_byte_index=948, ccp_value=0x00)
        self.ssh.type_commands(DeviceName.TCAM, "pkill -f Cell", timeout=5)
        sleep(20)
        self.soa.send_method_request(RESET_SERVICE_CLIENT_TCAM, "ResetAllVehicleSOAConfig", {})
        self.soa.ck_s2s_event(RESET_SERVICE_CLIENT_TCAM, "ResetAllVehicleSOAConfigResult", {"sts":2})
        self.soa.send_Get5GNetSts_req_and_ck_resp(SA_sts.On)
    
    @pytest.mark.sanity
    @allure.title("出厂默认值_异常")
    def test_caseid_1990393(self):
        self.ssh.type_commands(DeviceName.TCAM, "pkill -f Cell", timeout=5)
        self.soa.send_method_request(RESET_SERVICE_CLIENT_TCAM, "ResetAllVehicleSOAConfig", {})
        self.soa.ck_s2s_event(RESET_SERVICE_CLIENT_TCAM, "ResetAllVehicleSOAConfigResult", {"sts":3}, 15)
    
    @pytest.mark.sanity    
    @allure.title("4、5G网络状态切换")
    def test_caseid_1990369(self): 
        self.soa.send_SetNetResidentSts_req(is_5G=False)
        sleep(5)
        self.soa.send_Get5GNetSts_req_and_ck_resp(SA_sts.Off)
        self.soa.send_SetNetResidentSts_req(is_5G=True)
        sleep(5)
        self.soa.send_Get5GNetSts_req_and_ck_resp(SA_sts.On)
        
        
    # @pytest.mark.longtime
    # def test_caseid_19780005(self):

    #     # tcam 蜂窝N28 CCP 969==0x01
    #     # self.bus_comm.send_ccp_to_tcam(ccp_byte_index=969,ccp_value=0x01)
        
    #     # tcam 蜂窝国内4、5G默认值 CCP 948==0x00
    #     # tcam 蜂窝海外4、5G默认值 CCP 948!=0x00
    #     self.bus_comm.send_ccp_to_tcam(ccp_byte_index=948,ccp_value=0x00)
    #     # self.ssh.type_commands(DeviceName.TCAM, "reboot -f", timeout=5)
    #     # sleep(240)
    #     # tcam XCALL OTTC  CCP  947==0x02
    #     # tcam XCALL 国内  CCP  947==0x00
    #     # self.bus_comm.send_ccp_to_tcam(ccp_byte_index=947,ccp_value=0x02)
    #     # sleep(200)
    

if __name__ == '__main__':
    pytest.main()
