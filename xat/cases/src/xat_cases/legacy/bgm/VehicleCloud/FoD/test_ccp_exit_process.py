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
        self.ssh.set_airplane_mode(isOn.Off) 
    
    @pytest.mark.full
    @allure.title("激活失败流程_切换CCP状态")
    def test_FoD_caseid_1985971(self):
        error_ccp = copy.deepcopy(self.fod_bench_config)
        error_ccp['ccp'] = '1'
        self.soa.call_vehicle_api(V2T_API.FOD,payload=error_ccp)
        assert self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.FAIL.value,timeout=120)

    @pytest.mark.full
    @allure.title("激活失败流程_上报结果")
    def test_FoD_caseid_1985970(self):
        error_ccp = copy.deepcopy(self.fod_bench_config)
        error_ccp['ccp'] = '1'
        self.soa.call_vehicle_api(V2T_API.FOD,payload=error_ccp)
        with self.log_manage.check_jetlog_by_keywords(log_type=' ccp:', keywords='data: {"code":2,"msg":"write ccp, ccp size less than 1500","taskId":66666}', timeout=60):
            pass

    @pytest.mark.full
    @allure.title("激活失败流程_FotaStatus:idle")
    def test_FoD_caseid_1985969(self):
        error_ccp = copy.deepcopy(self.fod_bench_config)
        error_ccp['ccp'] = '1'
        self.soa.call_vehicle_api(V2T_API.FOD,payload=error_ccp)
        with self.log_manage.check_jetlog_by_keywords(log_type=' ccp:', keywords='mcu conntect: 1,fota sts:0', timeout=60):
            self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.FAIL.value,timeout=120)

    @pytest.mark.smoke
    @allure.title("激活成功流程_切换CCP状态")
    def test_FoD_caseid_1985968(self):
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        assert self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.SUCCESS.value,timeout=120)

    @pytest.mark.smoke
    @allure.title("激活成功流程_上报结果")
    def test_FoD_caseid_1985967(self):
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        with self.log_manage.check_jetlog_by_keywords(log_type=' ccp:', keywords='data: {"code":0,"msg":"sync ccp succ","taskId":66666}', timeout=60):
            pass

    @pytest.mark.smkoe
    @allure.title("激活成功流程_FotaStatus:idle")
    def test_FoD_caseid_1985966(self):
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        with self.log_manage.check_jetlog_by_keywords(log_type=' ccp:', keywords='mcu conntect: 1,fota sts:0', timeout=60):
            self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.SUCCESS.value,timeout=120)

    @pytest.mark.smoke
    @allure.title("激活成功流程_进度同步")
    def test_FoD_caseid_1985965(self):
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        assert self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.SUCCESS.value,timeout=120)
        assert self.soa.till_ccp_ActiveProgress_to(target_status=100,timeout=60)

    @pytest.mark.full
    @allure.title("失败影响功能流程_切换CCP状态") 
    def test_FoD_caseid_1985964(self):
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.FwdVal1)
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        assert self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.FAIL_IMPACT_DRIVING.value,timeout=120)
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)

    @pytest.mark.full
    @allure.title("失败影响功能流程_上报结果")
    def test_FoD_caseid_1985963(self):
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.FwdVal1)
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        with self.log_manage.check_jetlog_by_keywords(log_type=' ccp:', keywords=']data: {"code":5,"msg":"set usage down fail","taskId":66666}', timeout=60):
            pass
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)

    @pytest.mark.full
    @allure.title("失败影响功能流程_FotaStatus:idle")
    def test_FoD_caseid_1985962(self):
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.FwdVal1)
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        with self.log_manage.check_jetlog_by_keywords(log_type=' ccp:', keywords='mcu conntect: 1,fota sts:0', timeout=60):
            self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.FAIL_IMPACT_DRIVING.value,timeout=120)
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)

    @pytest.mark.full
    @allure.title("Fod上报结果异常处理_无网络")
    def test_FoD_caseid_1985961(self):
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        self.ssh.set_airplane_mode(isOn.On)
        with self.log_manage.check_jetlog_by_keywords(log_type=' ccp:', keywords='Send Cloud uplink is failed, wait 3s retry', timeout=120):
            pass
        time.sleep(30)    
        with self.log_manage.check_jetlog_by_keywords(log_type=' ccp:', keywords='ret: 0, uplink_flag: 1', timeout=60):
            self.ssh.set_airplane_mode(isOn.Off)

    @pytest.mark.full
    @allure.title("Fod上报结果异常处理_上下电")
    def test_FoD_caseid_1985960(self):
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        self.ssh.set_airplane_mode(isOn.On)
        with self.log_manage.check_jetlog_by_keywords(log_type=' ccp:', keywords='Send Cloud uplink is failed, wait 3s retry', timeout=120):
            pass
        self.sd_tester.reset_bgm()    
        with self.log_manage.check_jetlog_by_keywords(log_type=' ccp:', keywords='ret: 0, uplink_flag: 1', timeout=60):
            self.ssh.set_airplane_mode(isOn.Off)

if __name__ == "__main__":
    pass
    




