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
from xat_ecu.api.common.common import set_bench_vlan9_ip

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
        self.tc_config['ecu_mock_cfg']['server_ip'] = '172.16.9.21'
        set_bench_vlan9_ip(self.tc_config['ecu_mock_cfg']['server_ip'])

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
    
    @pytest.mark.sanity #v2.1
    @allure.title("退FOTA MODE_诊断下切VMM至ConV")
    def test_FoD_caseid_1989092(self):
        with self.log_manage.check_jetlog_by_keywords(log_type='-E " ccp:| obt:"', keywords=['Progress: 90',
                                                                                            '2f dd 0a 03 02',
                                                                                            'vehicle mode usageMode: 2'
                                                                                            ], timeout=60):
            self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)   

    @pytest.mark.sanity #v2.1
    @allure.title("退FOTA MODE_1001退诊断 肯定响应")
    def test_FoD_caseid_1989093(self):
        with self.log_manage.check_jetlog_by_keywords(log_type='-E " ccp:| obt:"', keywords=['Progress: 90',
                                                                                            'send stack raw data, addr:1002, data::10 01',
                                                                                            'send raw data rsp addr:1002, data:50 01 00 32 01 f4',
                                                                                            'vehicle mode usageMode: 1',
                                                                                            'exit fota mode, judge seat state'
                                                                                            ], timeout=60):
            self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)   

    # @pytest.mark.sanity V2.0
    @allure.title("退FOTA MODE_诊断下切VMM至inactive")
    def test_FoD_caseid_1985976(self):
        with self.log_manage.check_jetlog_by_keywords(log_type='-E " ccp:| obt:"', keywords=['Progress: 90',
                                                                                  '2f dd 0a 03 01',], timeout=60):
            self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
  
    @pytest.mark.sanity
    @allure.title("退FOTA MODE_占位判断_主驾占位_正向流程")
    def test_FoD_caseid_1985973(self):
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        self.soa.till_ccp_ActiveProgress_to(target_status=70,timeout=120)
        with self.log_manage.check_jetlog_by_keywords(log_type='-E " ccp:| obt:"', keywords=['set usage mode to convenience is done',
                                                                                            'send stack raw data, addr:1002, data::10 01',
                                                                                            'send raw data rsp addr:1002, data:50 01',
                                                                                            'send stack raw data, addr:1002, data::10 03',
                                                                                            'send raw data rsp addr:1002, data:50 03',
                                                                                            'send stack raw data, addr:1002, data::10 01'], timeout=60):
            self.io.driver_seat_present()
        self.io.driver_seat_notpresent() 

    @pytest.mark.sanity
    @allure.title("退FOTA MODE_占位判断_副驾占位_正向流程")
    def test_FoD_caseid_1987829(self):
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        self.soa.till_ccp_ActiveProgress_to(target_status=70,timeout=120)
        with self.log_manage.check_jetlog_by_keywords(log_type='-E " ccp:| obt:"', keywords=['set usage mode to convenience is done',
                                                                                            'send stack raw data, addr:1002, data::10 01',
                                                                                            'send raw data rsp addr:1002, data:50 01',
                                                                                            'send stack raw data, addr:1002, data::10 03',
                                                                                            'send raw data rsp addr:1002, data:50 03',
                                                                                            'send stack raw data, addr:1002, data::10 01'], timeout=60):
            self.bus_comm.set_pass_seat_present()
        self.bus_comm.set_pass_seat_notpresent()
    
    @pytest.mark.sanity
    @allure.title("退FOTA MODE_占位判断_后中占位_正向流程")
    def test_FoD_caseid_1987827(self):
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        self.soa.till_ccp_ActiveProgress_to(target_status=70,timeout=120)
        with self.log_manage.check_jetlog_by_keywords(log_type='-E " ccp:| obt:"', keywords=['set usage mode to convenience is done',
                                                                                            'send stack raw data, addr:1002, data::10 01',
                                                                                            'send raw data rsp addr:1002, data:50 01',
                                                                                            'send stack raw data, addr:1002, data::10 03',
                                                                                            'send raw data rsp addr:1002, data:50 03',
                                                                                            'send stack raw data, addr:1002, data::10 01'], timeout=60):
            self.bus_comm.set_secmid_seat_present()
        self.bus_comm.set_secmid_seat_notpresent()

    @pytest.mark.sanity
    @allure.title("退FOTA MODE_占位判断_后右占位_正向流程")
    def test_FoD_caseid_1987828(self):
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        self.soa.till_ccp_ActiveProgress_to(target_status=70,timeout=120)
        with self.log_manage.check_jetlog_by_keywords(log_type='-E " ccp:| obt:"', keywords=['set usage mode to convenience is done',
                                                                                            'send stack raw data, addr:1002, data::10 01',
                                                                                            'send raw data rsp addr:1002, data:50 01',
                                                                                            'send stack raw data, addr:1002, data::10 03',
                                                                                            'send raw data rsp addr:1002, data:50 03',
                                                                                            'send stack raw data, addr:1002, data::10 01'], timeout=60):
            self.bus_comm.set_secri_seat_present()
        self.bus_comm.set_secri_seat_notpresent()

    @pytest.mark.sanity
    @allure.title("退FOTA MODE_占位判断_后左占位_正向流程")
    def test_FoD_caseid_1987826(self):
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        self.soa.till_ccp_ActiveProgress_to(target_status=70,timeout=120)
        with self.log_manage.check_jetlog_by_keywords(log_type='-E " ccp:| obt:"', keywords=['set usage mode to convenience is done',
                                                                                            'send stack raw data, addr:1002, data::10 01',
                                                                                            'send raw data rsp addr:1002, data:50 01',
                                                                                            'send stack raw data, addr:1002, data::10 03',
                                                                                            'send raw data rsp addr:1002, data:50 03',
                                                                                            'send stack raw data, addr:1002, data::10 01'], timeout=60):
            self.bus_comm.set_secle_seat_present()
        self.bus_comm.set_secle_seat_notpresent()

    @pytest.mark.full
    @allure.title("退FOTA MODE_占位判断_主驾占位_异常切VMM失败流程")
    def test_FoD_caseid_1987425(self):
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        self.soa.till_ccp_ActiveProgress_to(target_status=70,timeout=120)
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.FwdVal1)
        with self.log_manage.check_jetlog_by_keywords(log_type='-E " ccp:| obt:"', keywords=[']exit and set usage mode, retry_num : 3, ccp_rollback:0',
                                                                                  'exit and set usage mode, retry_num : 2, ccp_rollback:0',
                                                                                  'exit and set usage mode, retry_num : 1, ccp_rollback:0',
                                                                                  'send stack raw data, addr:1002, data::10 01',], timeout=60):
            self.io.driver_seat_present()
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)
        self.io.driver_seat_notpresent()         

    @pytest.mark.sanity
    @allure.title("退FOTA MODE_占位判断_无占位")
    def test_FoD_caseid_1985972(self):
        self.io.driver_seat_notpresent()
        self.bus_comm.set_secle_seat_notpresent()
        self.bus_comm.set_secri_seat_notpresent()
        self.bus_comm.set_secmid_seat_notpresent()
        self.bus_comm.set_pass_seat_notpresent()
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        self.soa.till_ccp_ActiveProgress_to(target_status=70,timeout=120)
        self.log_manage.check_jetlog_by_keywords(log_type=' ccp:', unexpect_keywords=['send stack raw data, addr:1002, data::10 01',
                                                                                    'send raw data rsp addr:1002, data:50 01',
                                                                                    'send stack raw data, addr:1002, data::10 03',
                                                                                    'send raw data rsp addr:1002, data:50 03',
                                                                                    'send stack raw data, addr:1002, data::10 01'], timeout=60)

    @pytest.mark.smoke
    @allure.title("退FOTA MODE_请求ACU CDC退出fotamode成功")
    def test_FoD_caseid_1985975(self):
        self.ssh.ccp_skip_debug([Ccp_Skip_Debug.skip_verify, Ccp_Skip_Debug.skip_cdc])
        self.sd_tester.reset_bgm()
        self.fod_bench_config['preCheckUserIn']=2
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        with self.log_manage.check_jetlog_by_keywords(log_type='-E " ccp:| obt:"', keywords=['send stack raw data, addr:1401, data::31 01 a1 00 02',
                                                                                            'exit fota mode, judge seat state,  retry_num:3'],timeout=120):
            self.diag_mock.doip_sim_start()
            self.diag_mock.update_0x22_data(ecu_name="ACU", did="F186", data_info_update=[0x01])
            self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : [0x10, 0x00]}})
        self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.IDLE.value,timeout=120)
        self.diag_mock.doip_sim_close()

    @pytest.mark.Full
    @allure.title("退FOTA MODE_请求ACU CDC退出fotamode失败_否定响应")
    def test_FoD_caseid_1985974(self):
        self.ssh.ccp_skip_debug([Ccp_Skip_Debug.skip_verify, Ccp_Skip_Debug.skip_cdc])
        self.sd_tester.reset_bgm()
        self.fod_bench_config['preCheckUserIn']=2
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1401, data::31 01 a1 00 02',
                                                                                  'send stack raw data, addr:1401, data::31 01 a1 00 02',
                                                                                  'send stack raw data, addr:1401, data::31 01 a1 00 02'],timeout=120):
            self.diag_mock.doip_sim_start()
            self.diag_mock.update_0x22_data(ecu_name="ACU", did="F186", data_info_update=[0x01])
            self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : {"NRC": 0x11}}})
        self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.IDLE.value,timeout=120)
        self.diag_mock.doip_sim_close()

    @pytest.mark.Full
    @allure.title("退FOTA MODE_请求ACU CDC退出fotamode失败_超时未响应")
    def test_FoD_caseid_1987424(self):
        self.ssh.ccp_skip_debug([Ccp_Skip_Debug.skip_verify])
        self.sd_tester.reset_bgm()
        self.fod_bench_config['preCheckUserIn']=2
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1201, data::31 01 a1 00 02',
                                                                                  'send stack raw data, addr:1201, data::31 01 a1 00 02',
                                                                                  'send stack raw data, addr:1201, data::31 01 a1 00 02'],timeout=150):
              self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.IDLE.value,timeout=300)      

if __name__ == "__main__":
    pass
    




