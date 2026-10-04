import os
import sys
import pytest
import allure
import copy
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.case_helper.test_fota_base import TestABCBase
from xat_ecu.api.abc_interface import *

@pytest.mark.FoDfull
@allure.feature("基础架构")
@allure.story("FoD")
class TestFota(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("V2TRoutingForwarder","client","V2TCcpForwarder"),
                         ("CCPMasterService", "client" ,"CcpMasterService"),
                         ("VehicleModeService_client"),
                         ("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service")])
        self.ssh.ccp_skip_debug([Ccp_Skip_Debug.skip_verify,
                                 Ccp_Skip_Debug.skip_acu,
                                 Ccp_Skip_Debug.skip_cdc])

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.mix.back_ccp_status_to_Idle()
        self.io.bgm_diag_line_down()
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        
        
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.io.bgm_diag_line_up()
       
    def after_class(self, ecu):
        super().after_class(self, ecu)
    
    @pytest.mark.sanity
    @allure.title("等待激活_持续监控VMM状态")
    def test_FoD_caseid_1985993(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" ccp:", 
                                                    keywords='query mcu usage mode is active, ready monitoy 30s',timeout=120):
            self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)

    @pytest.mark.sanity
    @allure.title("等待激活_退出等待_超时30S")
    def test_FoD_caseid_1985992(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" ccp:", 
                                                    keywords='more than 30s, UsageMode is not change, notify cdc progress 90',timeout=120):
            self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)   

    @pytest.mark.fota
    @pytest.mark.smoke
    @allure.title("等待激活_进度同步")
    def test_FoD_caseid_1985990(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" ccp:", 
                                                    keywords='query mcu usage mode is active, ready monitoy 30s',timeout=120):
            self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        with self.log_manage.check_jetlog_by_keywords(log_type=" ccp:", keywords='Progress: 90',timeout=120):
            self.soa.till_ccp_ActiveProgress_to(target_status=50,timeout=13)
            self.soa.till_ccp_ActiveProgress_to(target_status=70,timeout=13)

if __name__ == "__main__":
    pass
    




