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

@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service"),
                         ("AcuModeManagerService","server")])
        self.ssh.update_skip_debug([FOTA_Skip_Debug.car_mode_normal,
                                    FOTA_Skip_Debug.baseline,
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
                                    ], allow_sleep=False) 
        self.ssh.update_ua_skip(DOMAIN.BGM, allow_same_version_flash=False, allow_sleep=False)
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM])    
        sleep(20)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
        self.mix.fota_back_to_idle()
                
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.ssh.set_airplane_mode(isOn.Off)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.bus_comm.set_fota_download_wake_condition(display_hv_soc=900, low_volt_soc=90)
        self.ssh.set_airplane_mode(isOn.Off)

    @pytest.mark.full
    @pytest.mark.V_1_4
    @allure.title("FOTA下载大小电池电量低不维持唤醒_0x02_0xF7&&0x02_0xF8_休眠重启场景") 
    def test_fota_caseid_1986133(self):
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM,DOMAIN.TCAM]) 
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=800, thermaloutofcontrol=False, low_volt_soc=69, local_diag_sts=DiagActLineSts.DisActive)
        self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, taskid=self.taskid)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['checkUAStateAfterDownload:BGM DOWNLOAD_RUNNING',
                                                                                   '"progress":',
                                                                                   '"stateCode":"02F6"'
                                                                                   ], timeout=300):
            sleep(2)
            self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=800, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"02F7"',
                                                                                   '"stateCode":"02F6"'], timeout=60):
            self.sd_tester.reset_bgm()#重启BGM代替休眠唤醒
            self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=89, thermaloutofcontrol=False, low_volt_soc=69, local_diag_sts=DiagActLineSts.DisActive)
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=800, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords=['"stateCode":"02F7"',
                                                                                            '"stateCode":"02F6"'], timeout=120):
            self.sd_tester.reset_bgm()#重启BGM代替休眠唤醒
        self.soa.send_fota_request(MASTER_REQUEST.CancelFota)

    @pytest.mark.full
    @pytest.mark.V_1_4
    @allure.title("下载唤醒策略_UA下载速度10min累计0_无9.50_有3_无10.10") 
    def test_fota_caseid_1988130(self):
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM,DOMAIN.TCAM]) 
        self.mix.set_factory_ota_condition(display_hv_soc=260,low_volt_power=14,local_diag_sts=DiagActLineSts.Active)
        self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, taskid=self.taskid)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['checkUAStateAfterDownload:BGM DOWNLOAD_RUNNING',
                                                                                   '"progress":'
                                                                                   ], timeout=300):
            sleep(2)
            self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        self.ssh.set_airplane_mode(isOn.On)
        sleep(585) #断网下载9min50s
        assert self.mix.check_fota_keep_awake(pnc29=True, acu_keep_alive=True, up_inactive=True)
        self.ssh.set_airplane_mode(isOn.Off)
        sleep(180) #正常下载3min
        assert self.mix.check_fota_keep_awake(pnc29=True, acu_keep_alive=True, up_inactive=True)
        self.ssh.set_airplane_mode(isOn.On)
        sleep(660) #断网下载10min10s
        assert self.mix.check_fota_keep_awake(pnc29=False, acu_keep_alive=False, up_inactive=False)
        self.ssh.set_airplane_mode(isOn.Off)

    @pytest.mark.full
    @pytest.mark.V_1_4
    @allure.title("下载唤醒策略_UA下载速度10min累计0_10min持续为0") #开发实现以分钟计算，涉及到秒的会出现出差
    def test_fota_caseid_1988129(self):
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM,DOMAIN.TCAM]) 
        self.mix.set_factory_ota_condition(display_hv_soc=260,low_volt_power=14,local_diag_sts=DiagActLineSts.Active)
        self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, taskid=self.taskid)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['checkUAStateAfterDownload:BGM DOWNLOAD_RUNNING',
                                                                                   '"progress":'
                                                                                   ], timeout=300):
            sleep(2)
            self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        self.ssh.set_airplane_mode(isOn.On)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['DownloadNetWorkNotKeep:network not meet, stop wake up',
                                                                                   '"stateCode":"02F8"'
                                                                                   ], timeout=660):
            sleep(660)##断网下载10min等待超时不维持唤醒
        assert self.mix.check_fota_keep_awake(pnc29=False, acu_keep_alive=False, up_inactive=False)
        self.ssh.set_airplane_mode(isOn.Off)

    @pytest.mark.full
    @pytest.mark.V_1_4
    @allure.title("下载唤醒策略_UA下载速度10min累计0_有8.30_无10.10") 
    def test_fota_caseid_1988792(self):
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM,DOMAIN.TCAM]) 
        self.mix.set_factory_ota_condition(display_hv_soc=260,low_volt_power=14,local_diag_sts=DiagActLineSts.Active)
        self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, taskid=self.taskid)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['checkUAStateAfterDownload:BGM DOWNLOAD_RUNNING',
                                                                                   '"progress":'
                                                                                   ], timeout=300):
            sleep(2)
            self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        sleep(510) #正常下载8min30s
        assert self.mix.check_fota_keep_awake(pnc29=True, acu_keep_alive=True, up_inactive=True)
        self.ssh.set_airplane_mode(isOn.On)
        sleep(660) #断网下载10min10s
        assert self.mix.check_fota_keep_awake(pnc29=False, acu_keep_alive=False, up_inactive=False)
        self.ssh.set_airplane_mode(isOn.Off)

    @pytest.mark.full
    @pytest.mark.V_1_4
    @allure.title("下载唤醒策略_UA下载速度10min累计0_有2_无9.50_持续有") 
    def test_fota_caseid_1988793(self):
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM,DOMAIN.TCAM]) 
        self.mix.set_factory_ota_condition(display_hv_soc=260,low_volt_power=14,local_diag_sts=DiagActLineSts.Active)
        self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, taskid=self.taskid)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['checkUAStateAfterDownload:BGM DOWNLOAD_RUNNING',
                                                                                   '"progress":'
                                                                                   ], timeout=300):
            sleep(2)
            self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        sleep(120) #正常下载2min
        assert self.mix.check_fota_keep_awake(pnc29=True, acu_keep_alive=True, up_inactive=True)
        self.ssh.set_airplane_mode(isOn.On)
        sleep(570) #断网下载9min30s
        assert self.mix.check_fota_keep_awake(pnc29=True, acu_keep_alive=True, up_inactive=True)
        self.ssh.set_airplane_mode(isOn.Off)
        self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status,target_status=FOTAMasteSts.ACTIVE.value, timeout=900)
        assert self.mix.check_fota_keep_awake(pnc29=False, acu_keep_alive=False, up_inactive=False)

    @pytest.mark.full
    @pytest.mark.V_1_4
    @allure.title("下载唤醒策略_UA下载速度10min累计0_有9.30_无10.10") 
    def test_fota_caseid_1988794(self):
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM,DOMAIN.TCAM])  
        self.mix.set_factory_ota_condition(display_hv_soc=260,low_volt_power=14,local_diag_sts=DiagActLineSts.Active)
        self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, taskid=self.taskid)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['checkUAStateAfterDownload:BGM DOWNLOAD_RUNNING',
                                                                                   '"progress":'
                                                                                   ], timeout=300):
            sleep(2)
            self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        sleep(570) #正常下载9min30s
        assert self.mix.check_fota_keep_awake(pnc29=True, acu_keep_alive=True, up_inactive=True)
        self.ssh.set_airplane_mode(isOn.On)
        sleep(660) #断网下载10min10s
        assert self.mix.check_fota_keep_awake(pnc29=False, acu_keep_alive=False, up_inactive=False)
        self.ssh.set_airplane_mode(isOn.Off)

    @pytest.mark.full
    @pytest.mark.V_1_4
    @allure.title("FOTA下载网络状态异常不维持唤醒_0x02_0xF8_WakeUpNetworkError_某域控下载卡滞10min以上") 
    def test_fota_caseid_1986136(self):
        self.mix.set_factory_ota_condition(display_hv_soc=260,low_volt_power=14,local_diag_sts=DiagActLineSts.Active)
        self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, taskid=self.taskid)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['checkUAStateAfterDownload:BGM DOWNLOAD_RUNNING',
                                                                                   '"progress":'
                                                                                   ], timeout=300):
            sleep(2)
            self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        self.ssh.set_airplane_mode(isOn.On)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['DownloadNetWorkNotKeep:network not meet, stop wake up',
                                                                                   '"stateCode":"02F8"'
                                                                                   ], timeout=660):
            sleep(660)#等待超时不维持唤醒
        # self.mix.network_sleep() #台架休眠不稳定，换用重启BGM方式 验证断点续传
        self.sd_tester.reset_bgm()
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords='"stateCode":"02F8"', timeout=120):
            self.ssh.set_airplane_mode(isOn.Off)
        assert self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status,target_status=FOTAMasteSts.ACTIVE.value, timeout=900)   

    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("下载唤醒策略_唤醒行为")    
    def test_fota_caseid_1983267(self):
        self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.NEW_TASK.value
        self.bus_comm.set_fota_download_wake_condition(display_hv_soc=900, low_volt_soc=90)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['OnSetOutputCb Fail_Type:', 'SetUsageModeUp', 'KeepAlive','VfcType :23'], timeout=300):
            sleep(2)
            self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, target_status=FOTAMasteSts.DOWNLOADING.value, timeout=30)
    
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("下载唤醒策略_HVSOC低于10%")    
    def test_fota_caseid_1983266(self):
        self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.NEW_TASK.value
        self.bus_comm.set_fota_download_wake_condition(display_hv_soc=89, low_volt_soc=90)
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        sleep(5) # 等待系统处理
        assert self.mix.check_fota_keep_awake(pnc29=False, acu_keep_alive=False, up_inactive=False), "HVSOC低于10%时检查条件不满足"

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("下载唤醒策略_下载完成")    
    def test_fota_caseid_1983265(self):
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        assert self.mix.check_fota_keep_awake(pnc29=False, acu_keep_alive=False, up_inactive=False), "下载完成时检查条件不满足"

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("下载唤醒策略_LVSOC低于70%")
    def test_fota_caseid_1983263(self):
        self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.NEW_TASK.value
        self.bus_comm.set_fota_download_wake_condition(display_hv_soc=900, low_volt_soc=69)
        self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
        sleep(5) # 等待系统处理
        assert self.mix.check_fota_keep_awake(pnc29=False, acu_keep_alive=False, up_inactive=False), "HVSOC低于70%时检查条件不满足"

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("FOTA下载小电池电量低不维持唤醒_0x02_0xF6_WakeUpLowVoltageError")
    def test_fota_caseid_1986135(self):
        self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.NEW_TASK.value
        self.bus_comm.set_fota_download_wake_condition(display_hv_soc=900, low_volt_soc=69)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"02F6"', timeout=600):
            self.soa.send_fota_request(MASTER_REQUEST.StartDownload)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("FOTA下载大电池电量低不维持唤醒_0x02_0xF7_WakeUpHighVoltageError")
    def test_fota_caseid_1986134(self):
        self.mix.back_fota_to(FOTAMasteSts.NEW_TASK, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.NEW_TASK.value
        self.bus_comm.set_fota_download_wake_condition(display_hv_soc=89, low_volt_soc=90)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='"stateCode":"02F7"', timeout=600):
            self.soa.send_fota_request(MASTER_REQUEST.StartDownload)

if __name__ == "__main__":
    pass