import os
import sys
import pytest
import allure

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.case_helper.test_fota_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.api.common import set_bench_vlan9_ip

@pytest.mark.ecu_mock
@pytest.mark.auto_rescue
@pytest.mark.V_2_0
@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service")])
        self.ssh.update_skip_debug([FOTA_Skip_Debug.car_mode_normal,
                                    FOTA_Skip_Debug.baseline,
                                    FOTA_Skip_Debug.fota_mode_requeset_acu,
                                    FOTA_Skip_Debug.fota_mode_requeset_cdc,
                                    FOTA_Skip_Debug.upload_version_from_debug_file,
                                    FOTA_Skip_Debug.CDC_UA,
                                    FOTA_Skip_Debug.ACU_UA,
                                    FOTA_Skip_Debug.version_collect,
                                    FOTA_Skip_Debug.cdc_acu_doip_check,
                                    FOTA_Skip_Debug.update_precondition_check
                                    ]) 
        set_bench_vlan9_ip(self.tc_config['ecu_mock_cfg']['server_ip'])
        self.ssh.update_ua_skip(DOMAIN.BGM, False)
        self.mix.update_version_debug(self.taskid,["DDM"])

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.mix.back_fota_to(FOTAMasteSts.IDLE, self.taskid)
                
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @allure.title("OTA mode及升级开始流程_ECM3 下高压失败_下高压超时 (03 09)")    
    def test_fota_caseid_1986893(self):
        self.mix.back_fota_to(FOTAMasteSts.RESCUE, taskid=self.taskid) 
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x03]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 01'], timeout=1200):
            pass
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0309"', timeout=600):
            pass  
        
    @allure.title("OTA mode及升级开始流程_ECM3 下高压失败_VMM处于driving (03 09)") 
    def test_fota_caseid_1986892(self):
        self.mix.back_fota_to(FOTAMasteSts.RESCUE, taskid=self.taskid)
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x04]}})
        with self.log_manage.check_jetlog_by_keywords(log_type='-E " fota:| obt:"', keywords=['send stack raw data, addr:1630, data::31 01 42 89 01', '"stateCode":"0309"'], timeout=1200):
            pass

    @allure.title("OTA mode及升级开始流程_ECM3 下高压失败_回复否定响应 (03 09)") 
    def test_fota_caseid_1986890(self):
        self.mix.back_fota_to(FOTAMasteSts.RESCUE, taskid=self.taskid)
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : {"NRC": 0x11}}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 01'], timeout=1200):
            pass
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0309"', timeout=600):
            pass
        
    @allure.title("FOTA解密过程_ECM3无法上高压_否定响应 (03 0B)") 
    def test_fota_caseid_1986888(self):
        self.mix.back_fota_to(FOTAMasteSts.RESCUE, taskid=self.taskid)
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x01]}})
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : {"NRC": 0x11}}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1630, data::31 01 40 00 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 40 00 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 40 00 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 40 00 01'], timeout=1200):
            pass
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"030B"', timeout=600):
            pass
        
    @allure.title("FOTA解密过程_ECM3无法上高压_回复超时 (03 0B)") 
    def test_fota_caseid_1986887(self):
        self.mix.back_fota_to(FOTAMasteSts.RESCUE, taskid=self.taskid)
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x01]}})
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4000": { 1 : {"NRC": "no_reply"}}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1630, data::31 01 40 00 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 40 00 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 40 00 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 40 00 01'], timeout=1200):
            pass
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"030B"', timeout=600):
            pass

    @allure.title("OTA mode及升级开始流程_ECM3 下高压失败_回复超时 (03 09)")    
    def test_fota_caseid_1986889(self):
        self.mix.back_fota_to(FOTAMasteSts.RESCUE, taskid=self.taskid)
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : {"NRC": "no_reply"}}})  
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                  'send stack raw data, addr:1630, data::31 01 42 89 01'], timeout=1200):
            pass
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"0309"', timeout=600):
            pass

    @allure.title("OTA mode及升级开始流程_ECM3 下高压失败_处于下高压过程中 (03 09)") 
    def test_fota_caseid_1986891(self):
        self.mix.back_fota_to(FOTAMasteSts.RESCUE, taskid=self.taskid)
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x78]}})
        with self.log_manage.check_jetlog_by_keywords(log_type='-E " fota:| obt:"', keywords=['send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                              'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                              'send stack raw data, addr:1630, data::31 01 42 89 01',
                                                                                              'send stack raw data, addr:1630, data::31 01 42 89 01', 
                                                                                              '"stateCode":"0309"'], timeout=1200):
            pass

    @allure.title("OTA mode及升级开始流程_ECM3 下高压失败_大电池SoC < 20% (03 09)") 
    def test_fota_caseid_1986894(self):
        self.mix.back_fota_to(FOTAMasteSts.RESCUE, taskid=self.taskid)
        self.diag_mock.update_0x31_data(ecu_name="ECM3", routine_control_data={"4289": { 1 : [0x10, 0x02]}})
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['31 01 42 89 01', '"stateCode":"0309"'], timeout=1200):
            pass

@pytest.mark.ecu_mock
@pytest.mark.auto_rescue
@pytest.mark.V_2_0
@allure.feature("基础架构")
@allure.story("FOTA")
class TestFotaMode(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service")])
        self.ssh.update_skip_debug([FOTA_Skip_Debug.car_mode_normal,
                                    FOTA_Skip_Debug.baseline,
                                    FOTA_Skip_Debug.fota_mode_requeset_ecm3,
                                    FOTA_Skip_Debug.fota_mode_requeset_cdc,
                                    FOTA_Skip_Debug.upload_version_from_debug_file,
                                    FOTA_Skip_Debug.CDC_UA,
                                    FOTA_Skip_Debug.ACU_UA,
                                    FOTA_Skip_Debug.version_collect,
                                    FOTA_Skip_Debug.cdc_acu_doip_check,
                                    FOTA_Skip_Debug.update_precondition_check
                                    ]) 
        set_bench_vlan9_ip(self.tc_config['ecu_mock_cfg']['server_ip'])
        self.ssh.update_ua_skip(DOMAIN.BGM, False)
        self.mix.update_version_debug(self.taskid,["DDM"])

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.mix.back_fota_to(FOTAMasteSts.IDLE, self.taskid)
                
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @allure.title("OTA mode及升级开始流程_进入FOTA mode失败_回复超时 (03 08)") 
    def test_fota_caseid_1986895(self):
        self.mix.back_fota_to(FOTAMasteSts.RESCUE, taskid=self.taskid)
        with self.log_manage.check_jetlog_by_same_keywords(log_type='-E "fota: | obt:"', keywords=['send stack raw data, addr:1401, data::31 01 a1 00 01',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 01',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 01',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 01',
                                                                                   '"stateCode":"0308"'
                                                                                   ], timeout=240):
            self.diag_mock.doip_sim_start()
            self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : {"NRC": "no_reply"}}})

    @allure.title("OTA mode及升级开始流程_进入FOTA mode失败_回复NRC (03 08)") 
    def test_fota_caseid_1986897(self):
        self.mix.back_fota_to(FOTAMasteSts.RESCUE, taskid=self.taskid)
        with self.log_manage.check_jetlog_by_same_keywords(log_type='-E "fota: | obt:"', keywords=['send stack raw data, addr:1401, data::31 01 a1 00 01',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 01',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 01',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 01',
                                                                                   '"stateCode":"0308"'
                                                                                   ], timeout=240):
            self.diag_mock.doip_sim_start()
            self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : {"NRC": 0x11}}})

    @allure.title("OTA mode及升级开始流程_进入FOTA mode失败_肯定响应状态error (03 08)") 
    def test_fota_caseid_1986896(self):
        self.mix.back_fota_to(FOTAMasteSts.RESCUE, taskid=self.taskid)
        with self.log_manage.check_jetlog_by_same_keywords(log_type='-E "fota: | obt:"', keywords=['send stack raw data, addr:1401, data::31 01 a1 00 01',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 01',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 01',
                                                                                   'send stack raw data, addr:1401, data::31 01 a1 00 01',
                                                                                   '"stateCode":"0308"'
                                                                                   ], timeout=240):
            self.diag_mock.doip_sim_start()
            self.diag_mock.update_0x31_data(ecu_name="ACU", routine_control_data={"A100": { 1 : [0x20, 0xff]}})


@pytest.mark.ecu_mock
@pytest.mark.auto_rescue
@pytest.mark.V_2_0
@allure.feature("基础架构")
@allure.story("FOTA")
class TestFotaMockCDC(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service"),
                         ("UpdateAgentService","server","CDC_UA_Service")])
        self.ssh.update_skip_debug([FOTA_Skip_Debug.car_mode_normal,
                                    FOTA_Skip_Debug.baseline,
                                    FOTA_Skip_Debug.before_group_1081,
                                    FOTA_Skip_Debug.before_group_hv_ctl,
                                    FOTA_Skip_Debug.ecm3_down_hv,
                                    FOTA_Skip_Debug.fota_mode_requeset_acu,
                                    FOTA_Skip_Debug.fota_mode_requeset_ecm3,
                                    FOTA_Skip_Debug.fota_mode_requeset_cdc,
                                    FOTA_Skip_Debug.upload_version_from_debug_file,
                                    FOTA_Skip_Debug.ACU_UA,
                                    FOTA_Skip_Debug.version_collect,
                                    FOTA_Skip_Debug.cdc_acu_doip_check,
                                    FOTA_Skip_Debug.update_precondition_check
                                    ]) 
        self.mix.update_version_debug(self.taskid,[DOMAIN.CDC])

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.mix.set_fota_rescue_condition(Gear.Park, HvSysRelaySts.Close, 230)
        self.soa.start_send_ua_response(DOMAIN.CDC)
        self.soa.start_send_ua_event(DOMAIN.CDC, self.soa.pack_ua_event_args(UA_Sts.IDLE))
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.IDLE)
        self.mix.fota_back_to_idle()
        self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, self.taskid)
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        time.sleep(2) # 防止CDC状态切太快
        self.soa.change_ua_event_and_getstatus(DOMAIN.CDC, UA_Sts.READY_TO_INSTALL)
        self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.ACTIVE.value, 100)
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        self.soa.ck_s2s_req("UpdateAgentService_server_CDC_UA_Service", "PreUpdate", timeout=180)
        self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                          ua_sts=UA_Sts.READY_TO_INSTALL,
                                                          ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                          ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_COMPLETE.value
                                                          )
        time.sleep(5) #模拟 CDC 在 PREUPDATE_RUNNING 状态，持续一段时间
        self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                        ua_sts=UA_Sts.INSTALLING,
                                                        ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                        ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_COMPLETE.value,
                                                        ua_update_sts=UA_UpdatedStatus.UPDATE_FAILED_TWICE.value,
                                                        errorCode=UA_ErrorCode.UpdateError_0x03_0x16.value
                                                        )
                
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @allure.title("FOTA解密过程_解密超时且SOA链接失败(03 30)/(03 32)") 
    def test_fota_caseid_1986883(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['ChangeState:rescue_pre_check => rescue_reset'], timeout=480):
            pass
        self.soa.change_ua_event_and_getstatus_with_error(DOMAIN.CDC, 
                                                          ua_sts=UA_Sts.READY_TO_INSTALL,
                                                          ua_download_sts=UA_DownloadStatus.DOWNLOAD_COMPLETE.value,
                                                          ua_preupdate_sts=UA_PreUpdatedStatus.PREUPDATE_COMPLETE.value
                                                          )
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="ChangeState:wait_task_info => pre_update", timeout=480):
            pass
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"0332"', '"stateCode":"0330"'], timeout=1080):
            self.soa.stop_send_ua_event(DOMAIN.CDC)
            self.soa.stop_send_ua_response(DOMAIN.CDC)
            self.soa.soa_partner.stop_single_partner("UpdateAgentService_server_CDC_UA_Service")


if __name__ == "__main__":
    pass


    




