import os
import sys
import pytest
import allure
import yaml
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.case_helper.test_fota_base import TestABCBase
from xat_ecu.api.abc_interface import *

@pytest.mark.auto_rescue
@pytest.mark.V_2_0
@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service"),
                         ("AcuModeManagerService","server")])
        self.ssh.update_skip_debug([FOTA_Skip_Debug.baseline,
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
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM])
        self.ssh.update_ua_skip(DOMAIN.BGM, allow_same_version_flash=False)
        self.io.bgm_diag_line_down()
        with open('config/FodConfig.yaml', 'r') as f:
            bench_data = yaml.safe_load(f)
        write_bench_ccp = bench_data['bench_ccp']
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xf106,SESSION.EXTENDED,UnLock.L5,write_bench_ccp,'6ef106',check_method=Check_Method.response,recover=False)
        self.sd_tester.reset_bgm()

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
                
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.ssh.set_airplane_mode(isOn.Off)

    @pytest.mark.full
    @allure.title("Rescue_3.0.0ONLY_救援步骤重启域控BGM1001")#JBS-49856 短期兜底方案   
    def test_fota_caseid_1999128(self):
        self.mix.set_fota_rescue_condition(Gear.Park, HVActiveSts.Close, 230)
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, self.taskid)
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        self.soa.till_UpdateProcess_event_to(MASTER_UpdateProcess_EVENT.state, target_status=Master_UpdateStatusEnum.PRE_UPDATE.value, timeout=240)
        self.sd_tester.diag_cancel()
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1011, data::10 01',
                                                                                  'send stack raw data, addr:1011, data::10 03',
                                                                                  'send stack raw data, addr:1011, data::11 03',
                                                                                  'send stack raw data, addr:1401, data::11 01',
                                                                                  'send stack raw data, addr:1201, data::11 01',
                                                                                  'send stack raw data, addr:1001, data::11 01'], timeout=600):
            pass
        sleep(30)#等待BGM重启恢复
        self.sd_tester.diag_cancel()
        

    @pytest.mark.full
    @allure.title("Rescue_3.0.0ONLY_救援type110下发后不写入F15304")#JBS-49856 短期兜底方案   
    def test_fota_caseid_1999127(self):
        self.mix.set_fota_rescue_condition(Gear.Park, HVActiveSts.Close, 230)
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, self.taskid)
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        self.soa.till_UpdateProcess_event_to(MASTER_UpdateProcess_EVENT.state, target_status=Master_UpdateStatusEnum.PRE_UPDATE.value, timeout=240)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['exit_ota => failed',
                                                                                   '"stateCode":"0329"'
                                                                                   ], timeout=240):
            self.sd_tester.diag_cancel()
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"type":110',
                                                                                   'RequestBgmToResetCb:result:'], 
                                                                        unexpect_keywords='2e f1 53 04',
                                                                        timeout=60):
            pass
        sleep(30)#等待BGM重启恢复
        self.sd_tester.diag_cancel()

    @pytest.mark.full
    @allure.title("Rescue_3.0.0ONLY_失败不可开退出FOTAMODE阶段不写F15300")#JBS-49856 短期兜底方案    
    def test_fota_caseid_1999126(self):
        self.mix.set_fota_rescue_condition(Gear.Park, HVActiveSts.Close, 230)
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, self.taskid)
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        self.soa.till_UpdateProcess_event_to(MASTER_UpdateProcess_EVENT.state, target_status=Master_UpdateStatusEnum.PRE_UPDATE.value, timeout=240)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['exit_ota => failed',
                                                                                   '"stateCode":"0329"'
                                                                                   ], timeout=240):
            self.sd_tester.diag_cancel()
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords='2e f1 53 00', timeout=60):
            pass
        sleep(30)#等待BGM重启恢复
        self.sd_tester.diag_cancel()

    @pytest.mark.V_2_1
    @pytest.mark.sanity
    @allure.title("Rescue_Reset_Other_ECU")    
    def test_fota_caseid_1989744(self):
        self.mix.update_version_debug(self.taskid,['OtherEcu'])
        self.mix.set_fota_rescue_condition(Gear.Park, HVActiveSts.Close, 230)
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE,self.taskid)
        with self.log_manage.check_jetlog_by_keywords(log_type='-E "fota: | diag_client:"', keywords=['=> rescue_query_task',
                                                                                                    'ChangeState:init => rescue_rese',
                                                                                                    'tx 1024:11 01',
                                                                                                    'tx 1025:11 01',
                                                                                                    'tx 1444:11 01',
                                                                                                    'tx 1c01:11 01',
                                                                                                    'tx 1a12:11 01',
                                                                                                    'tx 1601:11 01',
                                                                                                    'tx 1701:11 01'
                                                                                                    ], timeout=1800):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='rescue_reset => rescue_domain', timeout=180):
            pass    

    @pytest.mark.smoke
    @allure.title("Rescue_Before_Reset唤醒维持")    
    def test_fota_caseid_1987138(self):
        self.mix.set_fota_rescue_condition(Gear.Park, HVActiveSts.Close, 230)
        self.mix.back_fota_to(FOTAMasteSts.RESCUE, self.taskid)
        assert self.mix.check_fota_keep_awake(pnc29=True,
                                        acu_keep_alive=True,
                                        up_inactive=False,
                                        hv_active=True), "Not Send Awake Signal"
        
    @pytest.mark.smoke
    @allure.title("Rescue_After_Reset唤醒维持")    
    def test_fota_caseid_1987137(self):
        self.mix.set_fota_rescue_condition(Gear.Park, HVActiveSts.Close, 230)
        self.mix.back_fota_to(FOTAMasteSts.RESCUE, self.taskid)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='rescue_reset => rescue_domain', timeout=180):
            pass        
        assert self.mix.check_fota_keep_awake(pnc29=True,
                                        acu_keep_alive=True,
                                        hv_active=True), "Not Send Awake Signal"
        
    @pytest.mark.smoke
    @allure.title("Rescue_Before_Reset_Status_TaskType")    
    def test_fota_caseid_1987140(self):
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, self.taskid)
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status, target_status=FOTAMasteSts.UPDATE.value, timeout=3600)
        assert self.soa.get_fota_status(MASTER_EVENT.SerialNumber) == 1 and self.soa.get_fota_status(MASTER_EVENT.TaskType) == 0, "FOTA Status Illegal"
        self.soa.send_fota_request(MASTER_REQUEST.CancelFota)
        assert self.soa.till_fota_event_to(MASTER_EVENT.TaskType, target_status=FotaTaskType.Rescue.value, timeout=180), "TaskType Not Turn to 1"
        
    @pytest.mark.smoke
    @allure.title("Rescue_Before_Reset_StateCode_RescueStart(10F1)")    
    def test_fota_caseid_1987136(self):
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        self.mix.set_fota_rescue_condition(Gear.Park, HVActiveSts.Close, 900)
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status, target_status=FOTAMasteSts.UPDATE.value, timeout=3600)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"10F1"', timeout=180):
            self.soa.send_fota_request(MASTER_REQUEST.CancelFota)

    @pytest.mark.smoke
    @allure.title("Rescue_After_Reset_Status_SerialNumber")    
    def test_fota_caseid_1987139(self):
        self.mix.back_fota_to(FOTAMasteSts.RESCUE, taskid=self.taskid)
        with self.log_manage.check_jetlog_by_keywords(log_type="ChangeState:", keywords='rescue_reset => rescue_domain', timeout=240):
            pass
        assert self.soa.get_fota_status(MASTER_EVENT.SerialNumber) == 1, "FOTA Status Illegal"
        assert self.soa.till_fota_event_to(MASTER_EVENT.SerialNumber, target_status=2, timeout=120), "SerialNumber Not Turn to 2"
        
    @pytest.mark.smoke
    @allure.title("退出Rescue_After_Reset")    
    def test_fota_caseid_1987132(self):
        self.mix.back_fota_to(FOTAMasteSts.RESCUE, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.SerialNumber) == 1 and self.soa.get_fota_status(MASTER_EVENT.TaskType) == 1, "FOTA Status Illegal"
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.QUERY.value, timeout=300)
        assert self.soa.get_fota_status(MASTER_EVENT.SerialNumber) == 2 and self.soa.get_fota_status(MASTER_EVENT.TaskType) == 1, "FOTA Status Illegal"
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords='OnSetOutputCb Fail_Type:0', timeout=30):
            pass
        
    @pytest.mark.smoke
    @allure.title("Rescue_After_Reset_StateCode_RescueSuccess(10F2)")    
    def test_fota_caseid_1987133(self):
        self.mix.back_fota_to(FOTAMasteSts.RESCUE, taskid=self.taskid)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['rescue_reset => rescue_domain',
                                                                                   '"stateCode":"10F2"'], timeout=240):
            pass
        
    @pytest.mark.smoke
    @allure.title("Rescue_Before_Reset_F153")    
    def test_fota_caseid_1987135(self):
        self.mix.back_fota_to(FOTAMasteSts.RESCUE, taskid=self.taskid)
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1002, data::10 03',
                                                                                  'send stack raw data, addr:1002, data::27 05',
                                                                                  'send stack raw data, addr:1002, data::27 06',
                                                                                  'send stack raw data, addr:1002, data::2e f1 53 04'], timeout=240):
            pass
        
    @pytest.mark.smoke
    @allure.title("Rescue_Reset")    
    def test_fota_caseid_1987134(self):
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        self.mix.set_fota_rescue_condition(Gear.Park, HVActiveSts.Close, 230)
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status, target_status=FOTAMasteSts.UPDATE.value, timeout=3600)
        self.soa.send_fota_request(MASTER_REQUEST.CancelFota)
        with self.log_manage.check_jetlog_by_keywords(log_type=" obt:", keywords=['send stack raw data, addr:1011, data::10 01',
                                                                                  'send stack raw data, addr:1011, data::10 03',
                                                                                  'send stack raw data, addr:1011, data::11 03',
                                                                                  'send stack raw data, addr:1401, data::11 01',
                                                                                  'send stack raw data, addr:1201, data::11 01'], timeout=540):
            pass
        
    @pytest.mark.sanity
    @allure.title("Rescue_Condition_RescueDisPlaySOCError(1004)")    
    def test_fota_caseid_1987129(self):
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        self.mix.set_fota_rescue_condition(Gear.Park, HVActiveSts.Close, 220)
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status, target_status=FOTAMasteSts.UPDATE.value, timeout=3600)
        self.soa.send_fota_request(MASTER_REQUEST.CancelFota)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"1004"'], timeout=240):
            pass
        
    @pytest.mark.sanity
    @allure.title("Rescue_Condition_RescueGearError(1002)")    
    def test_fota_caseid_1987131(self):
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        self.mix.set_fota_rescue_condition(Gear.Undefd, HVActiveSts.Close, 230)
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status, target_status=FOTAMasteSts.UPDATE.value, timeout=3600)
        self.soa.send_fota_request(MASTER_REQUEST.CancelFota)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"1002"'], timeout=240):
            pass
        
    @pytest.mark.sanity
    @allure.title("Rescue_Condition_RescueHVActiceError(1003)")    
    def test_fota_caseid_1987130(self):
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        self.mix.set_fota_rescue_condition(Gear.Park, HVActiveSts.Open, 230)
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status, target_status=FOTAMasteSts.UPDATE.value, timeout=3600)
        self.soa.send_fota_request(MASTER_REQUEST.CancelFota)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"1003"'], timeout=240):
            pass
        
    @pytest.mark.fota
    @pytest.mark.full
    @allure.title("Rescue_V2T链接异常")    
    def test_fota_caseid_1987128(self):
        try:
            self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
            self.mix.set_fota_rescue_condition(Gear.Park, HVActiveSts.Close, 230)
            self.ssh.set_airplane_mode(isOn.On)
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
            assert self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status, target_status=FOTAMasteSts.UPDATE.value, timeout=3600)
            self.soa.send_fota_request(MASTER_REQUEST.CancelFota)
            with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['failed => rescue_query_task'], timeout=300):
                pass
            with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['rescue_query_task => failed_not_driving'], timeout=360):
                pass
        finally:
            self.ssh.set_airplane_mode(isOn.Off)
            
if __name__ == "__main__":
    pass

    




