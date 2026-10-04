import os
import sys
import pytest
import allure
import copy
import yaml
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
        self.io.bgm_diag_line_down()
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.mix.back_ccp_status_to_Idle()
        
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.io.bgm_diag_line_up()
       
    def after_class(self, ecu):
        super().after_class(self, ecu)
    
    @pytest.mark.smoke
    @allure.title("下切VMM至Convience_当前UsageMode=Active")
    def test_FoD_caseid_1986007(self):
        self.fod_bench_config['preCheckUserIn']=2
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        with self.log_manage.check_jetlog_by_keywords(log_type=" ccp:", 
                                                    keywords='usageMode is changed, pre usageMode:11, cur usageMode: 2',timeout=120):
            self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
            self.bus_comm.check_usage_mode_status(UsageMode.CONVENIENCE)

    @pytest.mark.smoke
    @allure.title("下切VMM至Convience_当前UsageMode=Driving")
    def test_FoD_caseid_1987420(self):
        self.fod_bench_config['preCheckUserIn']=2
        self.bus_comm.set_singal(bus="backbonefr", msg="VddmBackBoneFr18", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(UsageMode.DRIVING)
        with self.log_manage.check_jetlog_by_keywords(log_type=" ccp:", 
                                                    keywords='usageMode is changed, pre usageMode:13, cur usageMode: 2',timeout=120):
            self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
            self.bus_comm.check_usage_mode_status(UsageMode.CONVENIENCE)

    @pytest.mark.sanity
    @allure.title("下切VMM至Convience_当前UsageMode≠Active，driving")
    def test_FoD_caseid_1986006(self):
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.INACTIVE)
        self.fod_bench_config['preCheckUserIn']=2
        with self.log_manage.check_jetlog_by_keywords(log_type=" ccp:", 
                                                      unexpect_keywords='usageMode is changed, pre usageMode:',
                                                      keywords='UsageMode: 1, ready next step',
                                                      timeout=120):
            self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)

    @pytest.mark.smoke
    @allure.title("下切VMM至Convience_切换Convience成功")
    def test_FoD_caseid_1986004(self):
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.fod_bench_config['preCheckUserIn']=2
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        self.bus_comm.check_usage_mode_status(UsageMode.CONVENIENCE)
        self.log_manage.check_jetlog_by_keywords(log_type=" ccp:", keywords='diag cdc into fota mode',timeout=5)

    @pytest.mark.full
    @allure.title("下切VMM至Convience_持续监控VMM切换_切换Convience失败_")
    def test_FoD_caseid_1986003(self):
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.FwdVal1)
        self.fod_bench_config['preCheckUserIn']=2
        with self.log_manage.check_jetlog_by_keywords(log_type=" ccp:", keywords=['set usagemode down, intervale_num: 5, repeat_num: 1',
                                                                                  'set usagemode down, intervale_num: 4, repeat_num: 1',
                                                                                  'set usagemode down, intervale_num: 3, repeat_num: 1',
                                                                                  'set usagemode down, intervale_num: 2, repeat_num: 1',
                                                                                  'set usagemode down, intervale_num: 1, repeat_num: 1',
                                                                                  'set usagemode down, intervale_num: 0, repeat_num: 1',
                                                                                  'set usagemode down, intervale_num: 5, repeat_num: 0',
                                                                                  'set usagemode down, intervale_num: 4, repeat_num: 0',
                                                                                  'set usagemode down, intervale_num: 3, repeat_num: 0',
                                                                                  'set usagemode down, intervale_num: 2, repeat_num: 0',
                                                                                  'set usagemode down, intervale_num: 1, repeat_num: 0',
                                                                                  'set usagemode down, intervale_num: 0, repeat_num: 0',
                                                                                  '{"code":5,"msg":"set usage down fail","taskId":66666}'],timeout=120):
            self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)        

    @pytest.mark.smoke
    @allure.title("进入Fota Mode_周期发送S2S：FotaStatus")
    def test_FoD_caseid_1986002(self):
        self.fod_bench_config['preCheckUserIn']=2
        with self.log_manage.check_jetlog_by_keywords(log_type=" ccp:", keywords=['cycle send fota update sts to s2s',
                                                                                  'mcu conntect: 1,fota sts:4'],timeout=120):
            self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)

    @pytest.mark.smoke
    @allure.title("进入Fota Mode_进fotamode成功")
    def test_FoD_caseid_1986001(self):
        self.ssh.ccp_skip_debug([Ccp_Skip_Debug.skip_verify, Ccp_Skip_Debug.skip_cdc])
        self.sd_tester.reset_bgm()
        self.fod_bench_config['preCheckUserIn']=2
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1401, data::31 01 a1 00 01',
                                                                                  'send stack raw data, addr:1002, data::10 03'],timeout=120):
            self.diag_mock.doip_sim_start()
            self.diag_mock.update_0x22_data(ecu_name="ACU", did="F186", data_info_update=[0x01])
            self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : [0x10, 0x00]}})
        self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.IDLE.value,timeout=120)
        self.diag_mock.doip_sim_close()

    @pytest.mark.Full
    @allure.title("进入Fota Mode_进fotamode失败_否定响应")
    def test_FoD_caseid_1986000(self):
        self.ssh.ccp_skip_debug([Ccp_Skip_Debug.skip_verify, Ccp_Skip_Debug.skip_cdc])
        self.sd_tester.reset_bgm()
        self.fod_bench_config['preCheckUserIn']=2
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1401, data::31 01 a1 00 01',
                                                                                  'send stack raw data, addr:1401, data::31 01 a1 00 01',
                                                                                  'send stack raw data, addr:1401, data::31 01 a1 00 01'],timeout=120):
            self.diag_mock.doip_sim_start()
            self.diag_mock.update_0x22_data(ecu_name="ACU", did="F186", data_info_update=[0x01])
            self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : {"NRC": 0x11}}})
        self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.IDLE.value,timeout=120)
        self.diag_mock.doip_sim_close()

    @pytest.mark.Full
    @allure.title("进入Fota Mode_进fotamode失败_无响应")
    def test_FoD_caseid_1987421(self):
        self.ssh.ccp_skip_debug([Ccp_Skip_Debug.skip_verify])
        self.sd_tester.reset_bgm()
        self.fod_bench_config['preCheckUserIn']=2
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1201, data::31 01 a1 00 01',
                                                                                  'send stack raw data, addr:1201, data::31 01 a1 00 01',
                                                                                  'send stack raw data, addr:1201, data::31 01 a1 00 01'],timeout=150):
            self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.IDLE.value,timeout=300)      

if __name__ == "__main__":
    pass
    




