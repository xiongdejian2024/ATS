import os
import sys
import pytest
import allure
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.case_helper.test_fota_base import TestABCBase
from xat_ecu.api.abc_interface import *

@pytest.mark.V_2_0
@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota_B(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service"),
                         ("AcuModeManagerService","server")])
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM], baseline='6100000210AHO')
        self.ssh.update_ua_skip(DOMAIN.BGM, allow_same_version_flash=False)
        self.io.bgm_diag_line_down()

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.ssh.update_skip_debug(['baseline:6100000210AHO',
                                    FOTA_Skip_Debug.before_group_1081,
                                    FOTA_Skip_Debug.before_group_hv_ctl,
                                    FOTA_Skip_Debug.ecm3_down_hv,
                                    FOTA_Skip_Debug.fota_mode_requeset_acu,
                                    FOTA_Skip_Debug.fota_mode_requeset_cdc,
                                    FOTA_Skip_Debug.fota_mode_requeset_ecm3,
                                    FOTA_Skip_Debug.upload_version_from_debug_file,
                                    FOTA_Skip_Debug.CDC_UA,
                                    FOTA_Skip_Debug.ACU_UA,
                                    FOTA_Skip_Debug.version_collect,
                                    FOTA_Skip_Debug.cdc_acu_doip_check,
                                    FOTA_Skip_Debug.update_precondition_check
                                    ]) 
                
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.ssh.set_airplane_mode(isOn.Off)

    @pytest.mark.sanity
    @allure.title("RescueOTAFlag=Ture_ldle/Query")    
    def test_fota_caseid_1986915(self):
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        self.mix.set_fota_rescue_condition(Gear.Park, HVActiveSts.Close, 230)
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status, target_status=FOTAMasteSts.UPDATE.value, timeout=3600)
        self.soa.send_fota_request(MASTER_REQUEST.CancelFota)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='rescue_domain => collect_version', timeout=600):
            pass
        assert self.mix.check_fota_keep_awake(pnc29=True,acu_keep_alive=True,up_inactive=False,hv_active=False,startInhibit=True)
        self.soa.send_fota_request(MASTER_REQUEST.CancelFota)

    @pytest.mark.full
    @allure.title("Rescue_版本收集成功")    
    def test_fota_caseid_1986901(self):
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        self.mix.set_fota_rescue_condition(Gear.Park, HVActiveSts.Close, 230)
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status, target_status=FOTAMasteSts.UPDATE.value, timeout=3600)
        self.soa.send_fota_request(MASTER_REQUEST.CancelFota)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['rescue_domain => collect_version',
                                                                                    '"type":40'], timeout=600):
            pass
        self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status, target_status=FOTAMasteSts.UPDATE.value, timeout=600)
        self.soa.send_fota_request(MASTER_REQUEST.CancelFota)
        self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status, target_status=FOTAMasteSts.FAILED_NOT_DRIVING.value, timeout=600)
        
    @pytest.mark.full
    @allure.title("版本收集_v2t连接失败")    
    def test_fota_caseid_1986900(self):
        try:
            self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
            self.mix.set_fota_rescue_condition(Gear.Park, HVActiveSts.Close, 230)
            self.ssh.set_airplane_mode(isOn.On)
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
            assert self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status, target_status=FOTAMasteSts.UPDATE.value, timeout=360)
            self.soa.send_fota_request(MASTER_REQUEST.CancelFota)
            with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['rescue_query_task => failed_not_driving'], timeout=600):
                pass
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FAILED_NOT_DRIVING.value, "FOTA Update Status ≠ FAILED_NOT_DRIVING"
        finally:
            self.ssh.set_airplane_mode(isOn.Off)

    @pytest.mark.sanity
    @allure.title("自动救援_type40上报有ECU需要更新_writeDIDTask=0")    
    def test_fota_caseid_1989751(self):
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        self.mix.set_fota_rescue_condition(Gear.Park, HVActiveSts.Close, 230)
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status, target_status=FOTAMasteSts.UPDATE.value, timeout=3600)
        self.soa.send_fota_request(MASTER_REQUEST.CancelFota)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['ChangeState:rescue_pre_check => rescue_reset',
                                                                                   'ChangeState:rescue_domain => collect_version',
                                                                                   '"type":50,"writeDidTask":0'], timeout=360):
                pass
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.UPDATE.value, timeout=300)
        self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.IDLE.value, timeout=1500)

    @pytest.mark.sanity
    @allure.title("自动救援_type40上报无ECU需要更新_writeDIDTask=1_第一轮退FOTAMODE失败_正向流程")    
    def test_fota_caseid_1989750(self):
        self.mix.update_version_debug(self.taskid,['rescueErrorHWPN_BGM'], baseline='6100000210AHO') #输入与实际不一致的HWPN，以制造升级完成版本匹配不一致场景
        self.mix.set_fota_rescue_condition(Gear.Park, HVActiveSts.Close, 230)
        self.mix.back_fota_to(FOTAMasteSts.UPDATE, taskid=self.taskid)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"032A",', timeout=1000):#上报版本校验不一致
            pass
        self.mix.update_version_debug(self.taskid,['rescue_BGM'], baseline='6100000210AHO')#恢复version_debug 软硬件版本号与实际一致, 只有2.1AH以后的版本才会报writeDidTask=1
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['ChangeState:rescue_domain => collect_version',
                                                                                   '"type":50,"writeDidTask":1',
                                                                                   'GetQuitFotaModeFailFlag:quit_fota_mode_fail_flag: 1',
                                                                                   'quit_fota_mode_ecu_info, ecu_name:TCAM,ecu quit_fota_mode: 1',
                                                                                   '2e f1 53 00',
                                                                                   '14 ff ff ff',
                                                                                   'writeBaseline:set f150 succeed',
                                                                                   'writeDisplayBaseLine:set f151 succeed'], timeout=700):
            pass


    @pytest.mark.full
    @allure.title("自动救援_type40上报无ECU需要更新_writeDIDTask=1_异常_第一和二轮退ECM3恢复高压失败")    
    def test_fota_caseid_1989747(self):
        self.mix.update_version_debug(self.taskid,['rescueErrorHWPN_BGM'], baseline='6100000210AHO') #输入与实际不一致的HWPN，以制造升级完成版本匹配不一致场景
        self.mix.set_fota_rescue_condition(Gear.Park, HVActiveSts.Close, 230)
        self.mix.back_fota_to(FOTAMasteSts.UPDATE, taskid=self.taskid)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"032A",', timeout=1000):#上报版本校验不一致
            pass
        self.mix.update_version_debug(self.taskid,['rescue_BGM'], baseline='6100000210AHO')#恢复version_debug 软硬件版本号与实际一致
        self.ssh.update_skip_debug_nokill(['baseline:6100000210AHO',
                                        FOTA_Skip_Debug.before_group_1081,
                                        FOTA_Skip_Debug.fota_mode_requeset_acu,
                                        FOTA_Skip_Debug.fota_mode_requeset_cdc,
                                        FOTA_Skip_Debug.upload_version_from_debug_file,
                                        FOTA_Skip_Debug.CDC_UA,
                                        FOTA_Skip_Debug.ACU_UA,
                                        FOTA_Skip_Debug.version_collect,
                                        FOTA_Skip_Debug.cdc_acu_doip_check,
                                        FOTA_Skip_Debug.update_precondition_check
                                        ])
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"type":50,"writeDidTask":1',
                                                                                   '"stateCode":"0329",',
                                                                                   '2e f1 53 06'], timeout=700):
            pass
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FAILED_NOT_DRIVING.value     

    @pytest.mark.full
    @allure.title("自动救援_type40上报无ECU需要更新_writeDIDTask=1_异常_第一和二轮退FOTAMODE失败均失败")    
    def test_fota_caseid_1989748(self):
        self.mix.update_version_debug(self.taskid,['rescueErrorHWPN_BGM'], baseline='6100000210AHO') #输入与实际不一致的HWPN，以制造升级完成版本匹配不一致场景
        self.mix.set_fota_rescue_condition(Gear.Park, HVActiveSts.Close, 230)
        self.mix.back_fota_to(FOTAMasteSts.UPDATE, taskid=self.taskid)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"032A",', timeout=1000):#上报版本校验不一致
            pass
        self.mix.update_version_debug(self.taskid,['rescue_BGM'], baseline='6100000210AHO')#恢复version_debug 软硬件版本号与实际一致
        self.ssh.update_skip_debug_nokill(['baseline:6100000210AHO',
                                    FOTA_Skip_Debug.before_group_1081,
                                    FOTA_Skip_Debug.before_group_hv_ctl,
                                    FOTA_Skip_Debug.ecm3_down_hv,
                                    FOTA_Skip_Debug.fota_mode_requeset_cdc,
                                    FOTA_Skip_Debug.fota_mode_requeset_ecm3,
                                    FOTA_Skip_Debug.upload_version_from_debug_file,
                                    FOTA_Skip_Debug.CDC_UA,
                                    FOTA_Skip_Debug.ACU_UA,
                                    FOTA_Skip_Debug.version_collect,
                                    FOTA_Skip_Debug.cdc_acu_doip_check,
                                    FOTA_Skip_Debug.update_precondition_check
                                    ]) 
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"type":50,"writeDidTask":1',
                                                                                   '"stateCode":"0329",',
                                                                                   '2e f1 53 06'], timeout=700):
            pass
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.FAILED_NOT_DRIVING.value            


    @pytest.mark.full
    @allure.title("Rescue_type110 code = 1")    
    def test_fota_caseid_1989743(self):
        self.mix.back_fota_to(FOTAMasteSts.IDLE, taskid=self.taskid)
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM], baseline='6100000210AHO')
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        self.mix.set_fota_rescue_condition(Gear.Park, HVActiveSts.Close, 230)
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status, target_status=FOTAMasteSts.UPDATE.value, timeout=3600)
        self.soa.send_fota_request(MASTER_REQUEST.CancelFota)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"code":1,"data"',
                                                                                   'ChangeState:rescue_pre_check => rescue_reset'], timeout=360):
                pass
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.UPDATE.value, timeout=300)
        self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.IDLE.value, timeout=1500)
 
 
@pytest.mark.V_2_0
@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota_A(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service"),
                         ("AcuModeManagerService","server")])
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM], baseline='6100000140AAA')
        self.ssh.update_ua_skip(DOMAIN.BGM, allow_same_version_flash=False)
        self.io.bgm_diag_line_down()

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.ssh.update_skip_debug(['baseline:6100000140AAA',
                                    FOTA_Skip_Debug.before_group_1081,
                                    FOTA_Skip_Debug.before_group_hv_ctl,
                                    FOTA_Skip_Debug.ecm3_down_hv,
                                    FOTA_Skip_Debug.fota_mode_requeset_acu,
                                    FOTA_Skip_Debug.fota_mode_requeset_cdc,
                                    FOTA_Skip_Debug.fota_mode_requeset_ecm3,
                                    FOTA_Skip_Debug.upload_version_from_debug_file,
                                    FOTA_Skip_Debug.CDC_UA,
                                    FOTA_Skip_Debug.ACU_UA,
                                    FOTA_Skip_Debug.version_collect,
                                    FOTA_Skip_Debug.cdc_acu_doip_check,
                                    FOTA_Skip_Debug.update_precondition_check
                                    ]) 
                
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.ssh.set_airplane_mode(isOn.Off)

    @pytest.mark.full
    @allure.title("Rescue_type110 code = 0")    
    def test_fota_caseid_1989742(self):
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        self.mix.set_fota_rescue_condition(Gear.Park, HVActiveSts.Close, 230)
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status, target_status=FOTAMasteSts.UPDATE.value, timeout=3600)
        self.soa.send_fota_request(MASTER_REQUEST.CancelFota)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"code":0,"data"'], timeout=360):
                pass
                                     
if __name__ == "__main__":
    pass


    




