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
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)
        
        
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.io.bgm_diag_line_up()
       
    def after_class(self, ecu):
        super().after_class(self, ecu)
    
    @pytest.mark.smoke
    @allure.title("CCP Master状态机_Idle")
    def test_FoD_caseid_1986035(self):
        assert self.soa.get_ccp_status(CcpMaster_field=CCPMasterSts_Field.State) == CCPMasteSts.IDLE.value
 
    @pytest.mark.smoke
    @allure.title("CCP Master状态机_Pre-Active")
    def test_FoD_caseid_1986034(self):
        self.io.bgm_diag_line_up()
        self.fod_bench_config['preCheckUserIn']=1
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        assert self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.PRE_ACTIVE.value,timeout=120)

    @pytest.mark.smoke
    @allure.title("CCP Master状态机_Pre-Active > Activing")
    def test_FoD_caseid_1986033(self):
        self.fod_bench_config['preCheckUserIn']=1
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        assert self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.ACTIVING.value,timeout=120) 

    @pytest.mark.smoke
    @allure.title("CCP Master状态机_Activing > Success")
    def test_FoD_caseid_1986032(self):
        self.fod_bench_config['preCheckUserIn']=1
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        assert self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.SUCCESS.value,timeout=120)       

    @pytest.mark.full
    @allure.title("CCP Master状态机_Activing > Fail")
    def test_FoD_caseid_1986031(self):
        error_ccp = copy.deepcopy(self.fod_bench_config)
        error_ccp['ccp'] = '1'
        self.soa.call_vehicle_api(V2T_API.FOD,payload=error_ccp)
        assert self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.FAIL.value,timeout=120)   

    @pytest.mark.full
    @allure.title("CCP Master状态机_Activing_下发新任务")
    def test_FoD_caseid_1986030(self):
        self.fod_bench_config['preCheckUserIn']=1
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        assert self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.ACTIVING.value,timeout=120)
        with self.log_manage.check_jetlog_by_keywords(log_type=" ccp:", 
                                                      keywords='v2t resp: {"code":1,"msg":"current deal ccp value, processing"}',
                                                      timeout=120):
            time.sleep(2)#需等待logmanage启动
            self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)         

    @pytest.mark.full
    @allure.title("CCP Master状态机_Success_下发新任务")
    def test_FoD_caseid_1987797(self):
        self.fod_bench_config['preCheckUserIn']=1
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        assert self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.SUCCESS.value,timeout=120)
        with self.log_manage.check_jetlog_by_keywords(log_type=" ccp:", 
                                                      keywords='v2t resp: {"code":1,"msg":"current deal ccp value, processing"}',
                                                      timeout=120):
            time.sleep(2)#需等待logmanage启动
            self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)

    @pytest.mark.full
    @allure.title("CCP Master状态机_Fail_下发新任务")
    def test_FoD_caseid_1987796(self):
        error_ccp = copy.deepcopy(self.fod_bench_config)
        error_ccp['ccp'] = '1'
        self.soa.call_vehicle_api(V2T_API.FOD,payload=error_ccp)
        assert self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.FAIL.value,timeout=120)
        with self.log_manage.check_jetlog_by_keywords(log_type=" ccp:", 
                                                      keywords='v2t resp: {"code":1,"msg":"current deal ccp value, processing"}',
                                                      timeout=120):
            time.sleep(2)#需等待logmanage启动
            self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)

    @pytest.mark.full
    @allure.title("CCP Master状态机_Fail&&ImpactFunction_下发新任务")
    def test_FoD_caseid_1987795(self):
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.FwdVal1)
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        assert self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.FAIL_IMPACT_DRIVING.value,timeout=120)
        with self.log_manage.check_jetlog_by_keywords(log_type=" ccp:", 
                                                      keywords='v2t resp: {"code":1,"msg":"current deal ccp value, processing"}',
                                                      timeout=120):
            time.sleep(2)#需等待logmanage启动
            self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)

    @pytest.mark.full
    @allure.title("CCP Master状态机_Pre-Active_下发新任务")
    def test_FoD_caseid_1987794(self):
        self.io.bgm_diag_line_up()
        self.fod_bench_config['preCheckUserIn']=1
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        assert self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.PRE_ACTIVE.value,timeout=120)
        with self.log_manage.check_jetlog_by_keywords(log_type=" ccp:", 
                                                      keywords='v2t resp: {"code":1,"msg":"current deal ccp value, processing"}',
                                                      timeout=120):
            time.sleep(2)#需等待logmanage启动
            self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)

    @pytest.mark.full 
    @allure.title("CCP Master状态机_Activing > Fail&&ImpactFunction") #SOA-22430
    def test_FoD_caseid_1986029(self):
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.FwdVal1)
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        assert self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.FAIL_IMPACT_DRIVING.value,timeout=120)
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)
    
    @pytest.mark.sanity
    @allure.title("CCP Master状态机_Success > Idle") 
    def test_FoD_caseid_1986028(self):
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        assert self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.SUCCESS.value,timeout=120)
        time.sleep(11)#等待10s check suc > idle
        assert self.soa.get_ccp_status(CcpMaster_field=CCPMasterSts_Field.State) == CCPMasteSts.IDLE.value

    @pytest.mark.sanity
    @allure.title("CCP Master状态机_Fail > Idle") 
    def test_FoD_caseid_1986027(self):
        error_ccp = copy.deepcopy(self.fod_bench_config)
        error_ccp['ccp'] = '1'
        self.soa.call_vehicle_api(V2T_API.FOD,payload=error_ccp)
        assert self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.FAIL.value,timeout=120)
        time.sleep(11)#等待10s check suc > idle
        assert self.soa.get_ccp_status(CcpMaster_field=CCPMasterSts_Field.State) == CCPMasteSts.IDLE.value

    @pytest.mark.sanity
    @allure.title("CCP Master状态机_Fail&&ImpactFunction > Idle") #SOA-22430
    def test_FoD_caseid_1986026(self):
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.FwdVal1)
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        assert self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.FAIL_IMPACT_DRIVING.value,timeout=120)
        time.sleep(10)#等待10s check suc > idle
        assert self.soa.get_ccp_status(CcpMaster_field=CCPMasterSts_Field.State) == CCPMasteSts.IDLE.value
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)

    @pytest.mark.full
    @allure.title("CCP Master状态机_多个上电周期_Pre-Active") 
    def test_FoD_caseid_1986025(self):
        self.io.bgm_diag_line_up()
        self.fod_bench_config['preCheckUserIn']=1
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        assert self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.PRE_ACTIVE.value,timeout=120)
        self.sd_tester.reset_bgm()
        assert self.soa.get_ccp_status(CcpMaster_field=CCPMasterSts_Field.State) == CCPMasteSts.PRE_ACTIVE.value

    @pytest.mark.full
    @allure.title("CCP Master状态机_多个上电周期_Activing") 
    def test_FoD_caseid_1986024(self):
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        assert self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.ACTIVING.value,timeout=120)
        self.io.bgm_power_off()
        self.io.bgm_power_on()
        time.sleep(5)
        assert self.soa.get_ccp_status(CcpMaster_field=CCPMasterSts_Field.State) == CCPMasteSts.ACTIVING.value       

    @pytest.mark.full
    @allure.title("CCP Master状态机_多个上电周期_Success") 
    def test_FoD_caseid_1986023(self):
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        assert self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.SUCCESS.value,timeout=120)
        self.io.bgm_power_off()
        self.io.bgm_power_on()
        time.sleep(5)
        assert self.soa.get_ccp_status(CcpMaster_field=CCPMasterSts_Field.State) == CCPMasteSts.SUCCESS.value  

    @pytest.mark.full
    @allure.title("CCP Master状态机_多个上电周期_Fail") 
    def test_FoD_caseid_1986022(self):
        error_ccp = copy.deepcopy(self.fod_bench_config)
        error_ccp['ccp'] = '1'
        self.soa.call_vehicle_api(V2T_API.FOD,payload=error_ccp)
        assert self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.FAIL.value,timeout=120)
        self.io.bgm_power_off()
        self.io.bgm_power_on()
        time.sleep(5)
        assert self.soa.get_ccp_status(CcpMaster_field=CCPMasterSts_Field.State) == CCPMasteSts.FAIL.value  
        
    @pytest.mark.full
    @allure.title("CCP Master状态机_多个上电周期_Fail&&ImpactFunction") #SOA-22430
    def test_FoD_caseid_1986021(self):
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.FwdVal1)
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        assert self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.FAIL_IMPACT_DRIVING.value,timeout=120)
        self.io.bgm_power_off()
        self.io.bgm_power_on()
        time.sleep(5)
        assert self.soa.get_ccp_status(CcpMaster_field=CCPMasterSts_Field.State) == CCPMasteSts.FAIL_IMPACT_DRIVING.value
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3) 

    @pytest.mark.Smoke
    @allure.title("CCP Master状态机_Pre-Active > Idle")
    def test_FoD_caseid_1987389(self):
        self.fod_bench_config['preCheckUserIn']=2
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)  
        self.bus_comm.set_vehspd_gear(vehspd=10000)
        assert self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.IDLE.value,timeout=20)           

if __name__ == "__main__":
    pass