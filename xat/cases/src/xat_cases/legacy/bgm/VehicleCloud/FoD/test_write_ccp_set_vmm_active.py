import os
import sys
import pytest
import allure
import copy
import re
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
    
    @pytest.mark.smoke
    @allure.title("写CCP_写入成功")
    def test_FoD_caseid_1985999(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", 
                                                    keywords='send raw data rsp addr:1002, data:6e f1 06',timeout=120):
            self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)

    @pytest.mark.full
    @allure.title("写CCP_写入失败")
    def test_FoD_caseid_1985998(self):
        error_ccp = copy.deepcopy(self.fod_bench_config)
        error_ccp['ccp'] = '1'
        with self.log_manage.check_jetlog_by_keywords(log_type=" ccp:", 
                                                    keywords='write mcu cpp, retry_num: 3',timeout=120):
            self.soa.call_vehicle_api(V2T_API.FOD,payload=error_ccp)

    @pytest.mark.sanity
    @allure.title("写CCP_写入前获取存储现有CCP")
    def test_FoD_caseid_1985997(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1002, data::27 06',
                                                                                  'send raw data rsp addr:1002, data:67 06',
                                                                                  'send stack raw data, addr:1002, data::22 f1 06'],timeout=120):
            self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)

    @pytest.mark.smoke
    @allure.title("写CCP_写入前解锁")
    def test_FoD_caseid_1987412(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:",keywords=['send stack raw data, addr:1002, data::10 03',
                                                                                 'send raw data rsp addr:1002, data:50 03',
                                                                                 'send stack raw data, addr:1002, data::27 05',
                                                                                 'send raw data rsp addr:1002, data:67 05',
                                                                                 'send stack raw data, addr:1002, data::27 06',
                                                                                 'send raw data rsp addr:1002, data:67 06'
                                                                                 ],timeout=120):
            self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)

    @pytest.mark.smoke
    @allure.title("写CCP_写入FodPayload.Message值")
    def test_FoD_caseid_1987423(self):
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        jet_log = self.ssh.type_commands(DeviceName.BGM,"/app/bin/zstdcat /log/jetlog_messages |grep -E 'ccp:| obt:' | tail -n 800")
        FodPayloadMessage= re.findall(r'detail:{"ccp": "(.*?)", "cert": "-----BEGIN CERTIFICATE-----', jet_log, re.S)[-1]
        writeccpvalue = re.findall(r'send stack raw data, addr:1002, data::2e f1 06 (.*?)\n', jet_log, re.S)[-1]
        writeccpvalue = writeccpvalue.replace(" ", "").upper()
        assert FodPayloadMessage == writeccpvalue


    @pytest.mark.smoke
    @allure.title("写CCP_进度同步")
    def test_FoD_caseid_1985996(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", 
                                                    keywords='send raw data rsp addr:1002, data:6e f1 06',timeout=120):
            self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        assert self.soa.till_ccp_ActiveProgress_to(target_status=30,timeout=30)

    @pytest.mark.smoke
    @allure.title("切换VMM状态至Active_诊断切VMM至Active成功")
    def test_FoD_caseid_1985995(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", 
                                                    keywords=['send raw data rsp addr:1002, data:6e f1 06',
                                                              'send stack raw data, addr:1002, data::2f dd 0a 03 0b',
                                                              'send raw data rsp addr:1002, data:62 dd 0a 0b'],timeout=120):
            self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
            
    @pytest.mark.full
    @allure.title("切换VMM状态至Active_诊断切VMM至Active失败")
    def test_FoD_caseid_1985994(self):
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.FwdVal1)
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", 
                                                    keywords=['send stack raw data, addr:1002, data::2f dd 0a 03 02',
                                                              'send stack raw data, addr:1002, data::2f dd 0a 03 02',
                                                              'send stack raw data, addr:1002, data::2f dd 0a 03 02'],timeout=120):
            self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.FAIL_IMPACT_DRIVING.value,timeout=120)
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)

if __name__ == "__main__":
    pass
    




