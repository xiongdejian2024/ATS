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
    
    @pytest.mark.full
    @allure.title("CCP回滚_重新写入原先存储CCP")
    def test_FoD_caseid_1985983(self):
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.FwdVal1)
        error_ccp = copy.deepcopy(self.fod_bench_config)
        error_ccp['ccp'] = error_ccp['ccp'][0:-5] + '2a370'
        self.soa.call_vehicle_api(V2T_API.FOD,payload=error_ccp)
        self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.FAIL_IMPACT_DRIVING.value,timeout=120)
        assert self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.IDLE.value,timeout=120)
        assert self.sd_tester.check_ccp_value({1556: 0x01})
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)

    @pytest.mark.full
    @allure.title("CCP回滚_诊断下切Convience失败")
    def test_FoD_caseid_1985981(self):
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.FwdVal1)
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['2f dd 0a 03 02',
                                                                                  '2f dd 0a 03 02',
                                                                                  '2f dd 0a 03 02'], timeout=60):
            self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        assert self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.FAIL_IMPACT_DRIVING.value,timeout=120)
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)    

    @pytest.mark.full
    @allure.title("CCP回滚_上切active失败")
    def test_FoD_caseid_1985979(self):
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.FwdVal1)
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['2f dd 0a 03 0b',
                                                                                  '2f dd 0a 03 0b',
                                                                                  '2f dd 0a 03 0b'], timeout=60):
            self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        assert self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.FAIL_IMPACT_DRIVING.value,timeout=120)
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)

    @pytest.mark.full
    @allure.title("CCP回滚_写入CCP前解锁")
    def test_FoD_caseid_1987422(self):
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.FwdVal1)
        with self.log_manage.check_jetlog_by_keywords(log_type='-E " ccp:| obt:"',keywords=['set mcu usage mode to active is fail, ccp_rollback: 0',
                                                                                 'send stack raw data, addr:1002, data::10 03',
                                                                                 'send raw data rsp addr:1002, data:50 03',
                                                                                 'send stack raw data, addr:1002, data::27 05',
                                                                                 'send raw data rsp addr:1002, data:67 05',
                                                                                 'send stack raw data, addr:1002, data::27 06',
                                                                                 'send raw data rsp addr:1002, data:67 06'
                                                                                 ],timeout=120):
            self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
if __name__ == "__main__":
    pass
    




