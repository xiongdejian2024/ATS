import os
import sys
import pytest
import allure
import json
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
                         ("CCPMasterService","client","CcpMasterService"),
                         ("VehicleModeService_client"),
                         ("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service")])
        self.ssh.ccp_skip_debug([Ccp_Skip_Debug.skip_verify,
                                 Ccp_Skip_Debug.skip_acu,
                                 Ccp_Skip_Debug.skip_cdc])

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
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
    
    @pytest.mark.sanity
    @allure.title("CCP周期上传_72H")
    def test_FoD_caseid_1986020(self):
        ccp_persist_dict = json.loads(self.ssh.type_commands(DeviceName.BGM, "cat /data/fod/ccp_persist.json"))
        logger.info(f"ccp_persist_dict:{ccp_persist_dict}")
        modified_ccp_upload_time = ccp_persist_dict['ccpHashTime'] - 259200 # 72h = 259200
        ccp_persist_dict['ccpHashTime'] = modified_ccp_upload_time
        ccp_persist_json = json.dumps(ccp_persist_dict)
        logger.info(f"ccp_persist_json:{ccp_persist_json}")
        self.ssh.type_commands(DeviceName.BGM, f"echo -n '{ccp_persist_json}' > /data/fod/ccp_persist.json")
        with self.log_manage.check_jetlog_by_keywords(log_type=" ccp:", keywords=['upload_ccp_cycle',
                                                                                  'into upload end'], timeout=60):
            self.sd_tester.reset_bgm()
    
    @pytest.mark.full
    @allure.title("CCP周期上传_71H_不上传")
    def test_FoD_caseid_1986077(self):
        ccp_persist_dict = json.loads(self.ssh.type_commands(DeviceName.BGM, "cat /data/fod/ccp_persist.json"))
        logger.info(f"ccp_persist_dict:{ccp_persist_dict}")
        modified_ccp_upload_time = ccp_persist_dict['ccpHashTime'] - 255600 # 71h = 255600
        ccp_persist_dict['ccpHashTime'] = modified_ccp_upload_time
        ccp_persist_json = json.dumps(ccp_persist_dict)
        logger.info(f"ccp_persist_json:{ccp_persist_json}")
        self.ssh.type_commands(DeviceName.BGM, f"echo -n '{ccp_persist_json}' > /data/fod/ccp_persist.json")
        with self.log_manage.check_jetlog_by_keywords(log_type=" ccp:", unexpect_keywords=['upload_ccp_cycle',
                                                                                           'into upload end'], timeout=60):
            self.sd_tester.reset_bgm()
            
    @pytest.mark.smoke
    @allure.title("FOD激活触发_唤醒整车")
    def test_FoD_caseid_1986017(self):
        self.bus_comm.set_vehspd_gear(vehspd=10000)
        self.fod_bench_config['preCheckUserIn']=1
        with self.log_manage.check_jetlog_by_keywords(log_type=" ccp:", keywords='vfc_type: 11seconds: 60',timeout=120):
            self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
            self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.PRE_ACTIVE.value,timeout=120) 

    @pytest.mark.sanity
    @allure.title("FOD激活触发_Pending_条件不满足")
    def test_FoD_caseid_1986016(self):
        self.io.bgm_diag_line_up()
        self.fod_bench_config['preCheckUserIn']=1
        with self.log_manage.check_jetlog_by_keywords(log_type=" ccp:", keywords=['pre_check_user_in: 1',
                                                                                  'connect local diag line',
                                                                                  'connect local diag line'],timeout=120):
            self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)

    @pytest.mark.smoke
    @allure.title("FOD激活触发_条件检测满足_切状态机至Activing")
    def test_FoD_caseid_1986015(self):
        self.fod_bench_config['preCheckUserIn']=1
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        assert  self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.ACTIVING.value,timeout=120)

    @pytest.mark.smoke
    @allure.title("FOD激活触发_条件检测满足_同步激活进度0%")
    def test_FoD_caseid_1987818(self):
        self.fod_bench_config['preCheckUserIn']=1
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        assert  self.soa.till_ccp_ActiveProgress_to(target_status=0)       

    @pytest.mark.full
    @allure.title("FOD激活触发_条件检测_非pending车速不满足")
    def test_FoD_caseid_1986014(self):
        self.bus_comm.set_vehspd_gear(vehspd=10000)
        time.sleep(5)#车速生效
        self.fod_bench_config['preCheckUserIn']=2
        with self.log_manage.check_jetlog_by_keywords(log_type=" ccp:", keywords='task_id: 66666, err_code: 0101, err_msg: check pre-condition, not satisfy',timeout=120):
            self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)

    @pytest.mark.full
    @allure.title("FOD激活触发_条件检测_非pending档位不满足")
    def test_FoD_caseid_1986013(self):
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        time.sleep(5)#档位生效
        self.fod_bench_config['preCheckUserIn']=2
        with self.log_manage.check_jetlog_by_keywords(log_type=" ccp:", keywords='task_id: 66666, err_code: 0101, err_msg: check pre-condition, not satisfy',timeout=120):
            self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)

    @pytest.mark.full
    @allure.title("FOD激活触发_条件检测_非pending获取诊断令牌失败")
    def test_FoD_caseid_1986012(self):
        self.io.bgm_diag_line_up()
        self.fod_bench_config['preCheckUserIn']=2
        with self.log_manage.check_jetlog_by_keywords(log_type=" ccp:", keywords='task_id: 66666, err_code: 0101, err_msg: check pre-condition, not satisfy',timeout=120):
            self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)

    @pytest.mark.smoke
    @allure.title("CCP激活过程_唤醒_唤醒动作")
    def test_FoD_caseid_1986011(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" ccp:", keywords=['vfc_type: 11seconds: 600',
                                                                                  'cycle send to acu keep alive',
                                                                                  'cycle send 3E 80'],timeout=120):
            self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)

    @pytest.mark.full
    @allure.title("CCP激活过程_唤醒_停止唤醒动作")
    def test_FoD_caseid_1986010(self):
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.SUCCESS.value,timeout=120)
        time.sleep(1)#等待唤醒停发
        with self.log_manage.check_jetlog_by_keywords(log_type=" ccp:", unexpect_keywords=['vfc_type: 11',
                                                                                  'cycle send to acu keep alive',
                                                                                  'cycle send 3E 80'],timeout=120):
            pass

    @pytest.mark.sanity
    @allure.title("CCP激活过程_唤醒_档位监控P档")
    def test_FoD_caseid_1986009(self):
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.ACTIVING.value,timeout=120)
        with self.log_manage.check_jetlog_by_keywords(log_type=" ccp:", unexpect_keywords=['chassis conntect: 1, EPBOPera, operation0',
                                                                                  'chassis conntect: 1, EPBOPera, operation0'],timeout=60):
            pass

    @pytest.mark.sanity
    @allure.title("CCP激活过程_唤醒_档位监控非P档")
    def test_FoD_caseid_1986008(self):
        self.soa.call_vehicle_api(V2T_API.FOD,payload=self.fod_bench_config)
        self.soa.till_ccp_event_to(CCPMasterSts_Field.State,CCPMasteSts.ACTIVING.value,timeout=120)
        self.bus_comm.set_gear_pos(gear=ParkLockSts.Undefd)
        with self.log_manage.check_jetlog_by_keywords(log_type=" ccp:", keywords=['chassis conntect: 1, EPBOPera, operation0',
                                                                                  'chassis conntect: 1, EPBOPera, operation0'],timeout=120):
            pass

if __name__ == "__main__":
    pass

    




