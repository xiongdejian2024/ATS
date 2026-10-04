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

cur_num = 0
@allure.feature("基础架构")
@allure.story("FOTA")
@pytest.mark.stress_test
class TestFota(TestABCBase):
    num = 1 #压测次数
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("FotaMasterService","client"),
                         ("V2TRoutingForwarder","client","V2TOTAFotaForwarder"),
                         ("CentralLockService","client"),
                         ("TailGateService","client"),
                         ("AcuModeManagerService","server"),
                         ("ChassisService","client")])
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
                                    FOTA_Skip_Debug.cdc_acu_doip_check
                                    ]) 
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM])
        self.super_file_name = f"#{self.taskid} #{self.tsp.get_task_name(self.taskid)}".replace(' ','_')
        self.file_name = time.strftime("%m_%d_%H_%H:%M:%S", time.localtime(time.time()))
        self.cur_log_path = ""
        self.start_plane = ""
        log_folder = f"/root/log/{self.super_file_name}"
        os.makedirs(log_folder, exist_ok=True)
        os.makedirs(f"{log_folder}/{self.file_name}", exist_ok=True)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.mix.fota_back_to_idle()
        self.io.bgm_diag_line_down()
        # self.bgm_last_boot = self.ssh.get_domian_last_boot(DOMAIN.BGM)
        # self.tcam_last_boot = self.ssh.get_domian_last_boot(DOMAIN.TCAM)
        self.ssh.clear_fota_cache()
        self.sd_tester.reset_bgm()
                
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.ssh.get_log(DeviceName.BGM, self.cur_log_path)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @pytest.mark.repeat(num)
    @allure.title("E2E_Normal_Bench_Base")    
    def test_fota_caseid_1983158(self):
        global cur_num
        cur_num = cur_num + 1
        self.cur_log_path = f"/root/log/{self.super_file_name}/{self.file_name}/{cur_num}_E2E_Normal_Bench_Base_1983158"
        os.makedirs(self.cur_log_path, exist_ok=True)
        with allure.step("【Idle】Allow Same Version Flash"):
            self.ssh.update_ua_skip(DOMAIN.BGM, True)
            self.ssh.update_ua_skip(DOMAIN.TCAM, True)
        with allure.step("【Idle】Change CarMode/Usagemode"):    
            self.mix.set_car_mode(CarMode.NORMAL)
            self.mix.set_usage_mode(UsageMode.CONVENIENCE)
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == 0 and self.soa.get_fota_status(MASTER_EVENT.TaskId) == 0, "FOTA Status or TaskId not back to Idle"
        with allure.step("【Idle】Trigger VSP Task"):    
            self.tsp.trigger_vsp_fota(VSP.Reset, self.taskid)
            self.tsp.trigger_vsp_fota(VSP.Repub, self.taskid)
        with allure.step("【Idle】Check VSP Status"):
            assert self.tsp.get_vsp_fota_status(self.taskid) == VSP_Status.Push_Success.value, "VSP Status not Change to Push_Success"
        with allure.step("【Query】Diag Arbitration judgment && Receive Task"):    
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.QUERY.value, 65) and self.soa.till_fota_event_to(MASTER_EVENT.TaskId, self.taskid, 65), "Fail to Receive Task"
        with allure.step("【Query】Version Collect"):    
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.NEW_TASK.value, 480), "Reach Version Collect Maximum Timeout: 8min"
        with allure.step("【New_Task】Set FOTA Download Wake Condition: All Meet"):
            self.bus_comm.set_fota_download_wake_condition(display_hv_soc=900, low_volt_soc=90)
        with allure.step("【New_Task】Start Download"):    
            self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.DOWNLOADING.value, "FOTA Master Fail to Enter DOWNLOADING Status"
        with allure.step("【Download】New Event: DownloadProcess"):
            assert self.soa.get_fota_DownloadProcess(MASTER_DownloadProcess_EVENT.taskId) == self.taskid, "Not Receive DownloadProcess Event"
        with allure.step("【Download】Check VSP Status"):
            assert self.tsp.get_vsp_fota_status(self.taskid) == VSP_Status.Downloading.value, "VSP Status not Change to Downloading"
        with allure.step("【Download】Change NetWork to 5G"):
            self.ssh.set_network_mode(Network_Mode.Fifth_Generation)
        with allure.step("【Download】Wait for Download Complete"):
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.ACTIVE.value, 3600), "Reach Download Maximum Wake Timeout: 60min"
        with allure.step("【Active】Meet Update Conditions"):
            self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=800, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)
        with allure.step("【Active】Start Update"):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.UPDATE.value, 10), "FOTA Master Fail to Enter UPDATE Status"
        with allure.step("【Update】Check VSP Status"):
            assert self.tsp.get_vsp_fota_status(self.taskid) == VSP_Status.Upgrading.value, "VSP Status not Change to Downloading"
        with allure.step("【Successful】Back to Idle"):
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 3600), "Reach Domain Update Maximum Timeout: 60min"
            
    @pytest.mark.repeat(num)
    @allure.title("E2E_Normal_Bench_Composite")    
    def test_fota_caseid_1983156(self):
        global cur_num
        cur_num = cur_num + 1
        self.cur_log_path = f"/root/log/{self.super_file_name}/{self.file_name}/{cur_num}_E2E_Normal_Bench_Composite_1983156"
        os.makedirs(self.cur_log_path, exist_ok=True)       
        with allure.step("【Idle】Not Allow Same Version Flash"):
            self.ssh.update_ua_skip(DOMAIN.BGM, False)
            self.ssh.update_ua_skip(DOMAIN.TCAM, False) 
        with allure.step("【Idle】Change CarMode/Usagemode"):    
            self.mix.set_car_mode(CarMode.NORMAL)
            self.mix.set_usage_mode(UsageMode.CONVENIENCE)
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == 0 and self.soa.get_fota_status(MASTER_EVENT.TaskId) == 0, "FOTA Status or TaskId not back to Idle"
        with allure.step("【Idle】CheckTask for VSP Task"):   
            self.io.bgm_diag_line_up()
            self.soa.send_fota_request(MASTER_REQUEST.CheckTask, {'cmd': 0}) 
            self.tsp.trigger_vsp_fota(VSP.Reset, self.taskid)
            self.tsp.trigger_vsp_fota(VSP.Repub, self.taskid)
        with allure.step("【Idle】Check VSP Status"):
            assert self.tsp.get_vsp_fota_status(self.taskid) == VSP_Status.Push_Success.value, "VSP Status not Change to Push_Success"
        with allure.step("【Query】Recveive Task_Id but Block by Local Diag Arbitration"):  
            time.sleep(10) # wait for task processing
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == 0 and self.soa.get_fota_status(MASTER_EVENT.TaskId) == self.taskid, "Not Block by Local Diag Arbitration"
        with allure.step("【Query】FOTA Version Collect Win Arbitration"): 
            self.io.bgm_diag_line_down()
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.QUERY.value, 65), "Fail to Enter Query"
        with allure.step("【Query】Version Collect"):    
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.NEW_TASK.value, 480), "Reach Version Collect Maximum Timeout: 8min"
        with allure.step("【New_Task】Set FOTA Download Wake Condition: Not Meet"):
            self.bus_comm.set_fota_download_wake_condition(display_hv_soc=89, low_volt_soc=90) #not meet HVSOC > 10%
        with allure.step("【New_Task】Start Download"):    
            self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.DOWNLOADING.value, "FOTA Master Fail to Enter DOWNLOADING Status"
        with allure.step("【Download】Change NetWork to 4G"):
            self.ssh.set_network_mode(Network_Mode.Fourth_Generation)
        with allure.step("【Download】New Event: DownloadProcess"):
            assert self.soa.get_fota_DownloadProcess(MASTER_DownloadProcess_EVENT.taskId) == self.taskid, "Not Receive DownloadProcess Event"
        with allure.step("【Download】Break Point Continuation"):
            self.sd_tester.reset_bgm()
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.DOWNLOADING.value, "FOTA Master Fail to Break Point continue"
        with allure.step("【Download】Check VSP Status"):
            assert self.tsp.get_vsp_fota_status(self.taskid) == VSP_Status.Downloading.value, "VSP Status not Change to Downloading"
        with allure.step("【Download】Not Meet Wake Conditions"):
            assert self.mix.check_fota_keep_awake(pnc29=False, acu_keep_alive=None, up_inactive=False), "Abnormal Send Wake Condition"
        with allure.step("【Download】Wait for Download Complete"):
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.ACTIVE.value, 3600), "Reach Download Maximum Wake Timeout: 60min"
        with allure.step("【Active】Start Update with All not Meet Conditions"):
            with allure.step("【Active】 Local Diag"):
                self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=800, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.Active)
                self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
                assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "【Local Diag】FOTA Master Fail to Back Active"
            with allure.step("【Active】 Speed"):
                self.mix.set_normal_fota_update_condition(vehspd=1000, gear=Gear.Park, display_hv_soc=800, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)
                self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
                assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "【Speed】FOTA Master Fail to Back Active"
            with allure.step("【Active】 Gear"):
                self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Undefd, display_hv_soc=800, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)
                self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
                assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "【Gear】FOTA Master Fail to Back Active"
            with allure.step("【Active】 Hv Soc"):
                self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=100, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)
                self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
                assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "【Hv Soc】FOTA Master Fail to Back Active"
            with allure.step("【Active】 Thermal"):
                self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=800, thermaloutofcontrol=True, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)
                self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
                assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "【Thermal】FOTA Master Fail to Back Active"
            with allure.step("【Active】 Low Volt Soc"):
                self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=800, thermaloutofcontrol=False, low_volt_soc=50, local_diag_sts=DiagActLineSts.DisActive)
                self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
                assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "【Low Volt Soc】FOTA Master Fail to Back Active"
            with allure.step("【Active】 All Meet"):
                self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=800, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)
                self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
                assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.UPDATE.value, 10), "FOTA Master Fail to Enter UPDATE Status"
        with allure.step("【Update】Check VSP Status"):
            assert self.tsp.get_vsp_fota_status(self.taskid) == VSP_Status.Upgrading.value, "VSP Status not Change to Downloading"
        with allure.step("【Successful】Back to Idle"):
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 3600), "Reach Domain Update Maximum Timeout: 60min"            

    @pytest.mark.repeat(num)
    @allure.title("E2E_Normal_Bench_Appointment")    
    def test_fota_caseid_1983155(self):
        global cur_num
        cur_num = cur_num + 1
        self.cur_log_path = f"/root/log/{self.super_file_name}/{self.file_name}/{cur_num}E2E_Normal_Bench_Appointment_1983155"
        os.makedirs(self.cur_log_path, exist_ok=True)
        with allure.step("【Idle】Change CarMode/Usagemode"):    
            self.mix.set_car_mode(CarMode.NORMAL)
            self.mix.set_usage_mode(UsageMode.CONVENIENCE)
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == 0 and self.soa.get_fota_status(MASTER_EVENT.TaskId) == 0, "FOTA Status or TaskId not back to Idle"
        with allure.step("【Idle】Trigger VSP Task"):    
            self.tsp.trigger_vsp_fota(VSP.Reset, self.taskid)
            self.tsp.trigger_vsp_fota(VSP.Repub, self.taskid)
        with allure.step("【Idle】Check VSP Status"):
            assert self.tsp.get_vsp_fota_status(self.taskid) == VSP_Status.Push_Success.value, "VSP Status not Change to Push_Success"
        with allure.step("【Query】Diag Arbitration judgment && Receive Task"):    
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.QUERY.value, 65) and self.soa.till_fota_event_to(MASTER_EVENT.TaskId, self.taskid, 65), "Fail to Receive Task"
        with allure.step("【Query】Version Collect"):    
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.NEW_TASK.value, 480), "Reach Version Collect Maximum Timeout: 8min"
        with allure.step("【New_Task】Set FOTA Download Wake Condition: Not Meet"):
            self.bus_comm.set_fota_download_wake_condition(display_hv_soc=900, low_volt_soc=50) #not meet low_volt_soc ＜ 70%
        with allure.step("【New_Task】Start Download"):    
            self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.DOWNLOADING.value, "FOTA Master Fail to Enter DOWNLOADING Status"
        with allure.step("【Download】New Event: DownloadProcess"):
            assert self.soa.get_fota_DownloadProcess(MASTER_DownloadProcess_EVENT.taskId) == self.taskid, "Not Receive DownloadProcess Event"
        with allure.step("【Download】Check VSP Status"):
            assert self.tsp.get_vsp_fota_status(self.taskid) == VSP_Status.Downloading.value, "VSP Status not Change to Downloading"
        with allure.step("【Download】Change NetWork to 5G"):
            self.ssh.set_network_mode(Network_Mode.Fifth_Generation)
        with allure.step("【Download】Not Meet Wake Conditions"):
            assert self.mix.check_fota_keep_awake(pnc29=False, acu_keep_alive=None, up_inactive=False), "Abnormal Send Wake Condition"
        with allure.step("【Download】Wait for Download Complete"):
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.ACTIVE.value, 3600), "Reach Download Maximum Wake Timeout: 60min"
        with allure.step("【Active】Meet Update Conditions"):
            self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=800, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)
        with allure.step("【Active】Usagemode Need to be Down"):
            self.mix.set_usage_mode(UsageMode.DRIVING)
        with allure.step("【Reach_Appointment】Enter Reach_Appiontment"):
            self.mix.back_fota_to(FOTAMasteSts.REACH_APPOINTMENT, self.taskid)
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.REACH_APPOINTMENT.value, "FOTA Master Fail to Enter REACH_APPOINTMENT Status"
        with allure.step("【Reach_Appointmen】Start Update"):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.UPDATE.value, 10), "FOTA Master Fail to Enter UPDATE Status"
        with allure.step("【Update】Check VSP Status"):
            assert self.tsp.get_vsp_fota_status(self.taskid) == VSP_Status.Upgrading.value, "VSP Status not Change to Downloading"
        with allure.step("【Successful】Back to Idle"):
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 3600), "Reach Domain Update Maximum Timeout: 60min"

    @pytest.mark.repeat(num)
    @allure.title("E2E_Normal_Bench_Appointment_Composite")    
    def test_fota_caseid_1983154(self):
        global cur_num
        cur_num = cur_num + 1
        self.cur_log_path = f"/root/log/{self.super_file_name}/{self.file_name}/{cur_num}_E2E_Normal_Bench_Appointment_Composite_1983154"
        os.makedirs(self.cur_log_path, exist_ok=True)        
        with allure.step("【Idle】Change CarMode/Usagemode"):    
            self.mix.set_car_mode(CarMode.NORMAL)
            self.mix.set_usage_mode(UsageMode.CONVENIENCE)
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == 0 and self.soa.get_fota_status(MASTER_EVENT.TaskId) == 0, "FOTA Status or TaskId not back to Idle"
        with allure.step("【Idle】CheckTask for VSP Task"):   
            self.tsp.trigger_vsp_fota(VSP.Reset, self.taskid)
            self.tsp.trigger_vsp_fota(VSP.Repub, self.taskid)
        with allure.step("【Idle】Check VSP Status"):
            assert self.tsp.get_vsp_fota_status(self.taskid) == VSP_Status.Push_Success.value, "VSP Status not Change to Push_Success"
        with allure.step("【Query】Diag Arbitration judgment && Receive Task"):    
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.QUERY.value, 65) and self.soa.till_fota_event_to(MASTER_EVENT.TaskId, self.taskid, 65), "Fail to Receive Task"
        with allure.step("【Query】Version Collect"):    
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.NEW_TASK.value, 480), "Reach Version Collect Maximum Timeout: 8min"
        with allure.step("【New_Task】Set FOTA Download Wake Condition: All Meet"):
            self.bus_comm.set_fota_download_wake_condition(display_hv_soc=900, low_volt_soc=90) 
        with allure.step("【New_Task】Start Download"):    
            self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.DOWNLOADING.value, "FOTA Master Fail to Enter DOWNLOADING Status"
        with allure.step("【Download】Change NetWork to 5G"):
            self.ssh.set_network_mode(Network_Mode.Fifth_Generation)
        with allure.step("【Download】New Event: DownloadProcess"):
            assert self.soa.get_fota_DownloadProcess(MASTER_DownloadProcess_EVENT.taskId) == self.taskid, "Not Receive DownloadProcess Event"
        with allure.step("【Download】Check VSP Status"):
            assert self.tsp.get_vsp_fota_status(self.taskid) == VSP_Status.Downloading.value, "VSP Status not Change to Downloading"
        with allure.step("【Download】Not Meet Wake Conditions"):
            assert self.mix.check_fota_keep_awake(pnc29=True, acu_keep_alive=None, up_inactive=True), "Abnormal Send Wake Condition"
        with allure.step("【Download】Wait for Download Complete"):
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.ACTIVE.value, 3600), "Reach Download Maximum Wake Timeout: 60min"
        with allure.step("【Reach_Appointment】Enter Reach_Appiontment"):
            self.mix.back_fota_to(FOTAMasteSts.REACH_APPOINTMENT, self.taskid)
        with allure.step("【Active】Start Update with All not Meet Conditions"):
            with allure.step("【Active】 Local Diag"):
                self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=800, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.Active)
                self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
                assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "【Local Diag】FOTA Master Fail to Back Active"
                self.mix.back_fota_to(FOTAMasteSts.REACH_APPOINTMENT, self.taskid)
                assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.REACH_APPOINTMENT.value, "FOTA Master Fail to Enter REACH_APPOINTMENT Status"            
            with allure.step("【Active】 Speed"):
                self.mix.set_normal_fota_update_condition(vehspd=1000, gear=Gear.Park, display_hv_soc=800, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)
                self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
                assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "【Speed】FOTA Master Fail to Back Active"
                self.mix.back_fota_to(FOTAMasteSts.REACH_APPOINTMENT, self.taskid)
                assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.REACH_APPOINTMENT.value, "FOTA Master Fail to Enter REACH_APPOINTMENT Status"
            with allure.step("【Active】 Gear"):
                self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Undefd, display_hv_soc=800, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)
                self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
                assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "【Gear】FOTA Master Fail to Back Active"
                self.mix.back_fota_to(FOTAMasteSts.REACH_APPOINTMENT, self.taskid)
                assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.REACH_APPOINTMENT.value, "FOTA Master Fail to Enter REACH_APPOINTMENT Status"
            with allure.step("【Active】 Hv Soc"):
                self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=100, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)
                self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
                assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "【Hv Soc】FOTA Master Fail to Back Active"
                self.mix.back_fota_to(FOTAMasteSts.REACH_APPOINTMENT, self.taskid)
                assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.REACH_APPOINTMENT.value, "FOTA Master Fail to Enter REACH_APPOINTMENT Status"
            with allure.step("【Active】 Thermal"):
                self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=800, thermaloutofcontrol=True, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)
                self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
                assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "【Thermal】FOTA Master Fail to Back Active"
                self.mix.back_fota_to(FOTAMasteSts.REACH_APPOINTMENT, self.taskid)
                assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.REACH_APPOINTMENT.value, "FOTA Master Fail to Enter REACH_APPOINTMENT Status"
            with allure.step("【Active】 Low Volt Soc"):
                self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=800, thermaloutofcontrol=False, low_volt_soc=50, local_diag_sts=DiagActLineSts.DisActive)
                self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
                assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "【Low Volt Soc】FOTA Master Fail to Back Active"
                self.mix.back_fota_to(FOTAMasteSts.REACH_APPOINTMENT, self.taskid)
                assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.REACH_APPOINTMENT.value, "FOTA Master Fail to Enter REACH_APPOINTMENT Status"
            with allure.step("【Active】 All Meet"):
                self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=800, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)
                self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
                assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.UPDATE.value, 10), "FOTA Master Fail to Enter UPDATE Status"
        with allure.step("【Update】Check VSP Status"):
            assert self.tsp.get_vsp_fota_status(self.taskid) == VSP_Status.Upgrading.value, "VSP Status not Change to Downloading"
        with allure.step("【Successful】Back to Idle"):
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 3600), "Reach Domain Update Maximum Timeout: 60min"            

    @pytest.mark.repeat(num)
    @allure.title("E2E_Normal_Bench_APP")    
    def test_fota_caseid_1984974(self):
        global cur_num
        cur_num = cur_num + 1
        self.cur_log_path = f"/root/log/{self.super_file_name}/{self.file_name}/{cur_num}E2E_Normal_Bench_APP_1984974"
        os.makedirs(self.cur_log_path, exist_ok=True)
        with allure.step("【Idle】Change CarMode/Usagemode"):    
            self.mix.set_car_mode(CarMode.NORMAL)
            self.mix.set_usage_mode(UsageMode.CONVENIENCE)
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == 0 and self.soa.get_fota_status(MASTER_EVENT.TaskId) == 0, "FOTA Status or TaskId not back to Idle"
        with allure.step("【Idle】Trigger VSP Task"):    
            self.tsp.trigger_vsp_fota(VSP.Reset, self.taskid)
            self.tsp.trigger_vsp_fota(VSP.Repub, self.taskid)
        with allure.step("【Idle】Check VSP Status"):
            assert self.tsp.get_vsp_fota_status(self.taskid) == VSP_Status.Push_Success.value, "VSP Status not Change to Push_Success"
        with allure.step("【Query】Diag Arbitration judgment && Receive Task"):    
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.QUERY.value, 65) and self.soa.till_fota_event_to(MASTER_EVENT.TaskId, self.taskid, 65), "Fail to Receive Task"
        with allure.step("【Query】Version Collect"):    
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.NEW_TASK.value, 480), "Reach Version Collect Maximum Timeout: 8min"
        with allure.step("【New_Task】Set FOTA Download Wake Condition: All Meet"):
            self.bus_comm.set_fota_download_wake_condition(display_hv_soc=900, low_volt_soc=90) 
        with allure.step("【New_Task】Start Download"):    
            self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.DOWNLOADING.value, "FOTA Master Fail to Enter DOWNLOADING Status"
        with allure.step("【Download】New Event: DownloadProcess"):
            assert self.soa.get_fota_DownloadProcess(MASTER_DownloadProcess_EVENT.taskId) == self.taskid, "Not Receive DownloadProcess Event"
        with allure.step("【Download】Check VSP Status"):
            assert self.tsp.get_vsp_fota_status(self.taskid) == VSP_Status.Downloading.value, "VSP Status not Change to Downloading"
        with allure.step("【Download】Change NetWork to 5G"):
            self.ssh.set_network_mode(Network_Mode.Fifth_Generation)
        with allure.step("【Download】Not Meet Wake Conditions"):
            assert self.mix.check_fota_keep_awake(pnc29=True, acu_keep_alive=None, up_inactive=True), "Abnormal Send Wake Condition"
        with allure.step("【Download】Wait for Download Complete"):
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.ACTIVE.value, 3600), "Reach Download Maximum Wake Timeout: 60min"
        with allure.step("【Active】Meet Update Conditions"):
            self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=800, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)
        with allure.step("【Remote_Update】Enter Remote_Update"):
            self.mix.back_fota_to(FOTAMasteSts.REMOTE_UPDATE, self.taskid)
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.REMOTE_UPDATE.value, "FOTA Master Fail to Enter REMOTE_UPDATE Status"
        with allure.step("【Remote_Update】Start Update"):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.UPDATE.value, 10), "FOTA Master Fail to Enter UPDATE Status"
        with allure.step("【Update】Check VSP Status"):
            assert self.tsp.get_vsp_fota_status(self.taskid) == VSP_Status.Upgrading.value, "VSP Status not Change to Downloading"
        with allure.step("【Successful】Back to Idle"):
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 3600), "Reach Domain Update Maximum Timeout: 60min"        

    @pytest.mark.repeat(num)
    @allure.title("E2E_Normal_Bench_APP_Composite")    
    def test_fota_caseid_1984975(self):
        global cur_num
        cur_num = cur_num + 1
        self.cur_log_path = f"/root/log/{self.super_file_name}/{self.file_name}/{cur_num}_E2E_Normal_Bench_APP_Composite_1984975"
        os.makedirs(self.cur_log_path, exist_ok=True)        
        with allure.step("【Idle】Change CarMode/Usagemode"):    
            self.mix.set_car_mode(CarMode.NORMAL)
            self.mix.set_usage_mode(UsageMode.CONVENIENCE)
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == 0 and self.soa.get_fota_status(MASTER_EVENT.TaskId) == 0, "FOTA Status or TaskId not back to Idle"
        with allure.step("【Idle】CheckTask for VSP Task"):   
            self.tsp.trigger_vsp_fota(VSP.Reset, self.taskid)
            self.tsp.trigger_vsp_fota(VSP.Repub, self.taskid)
        with allure.step("【Idle】Check VSP Status"):
            assert self.tsp.get_vsp_fota_status(self.taskid) == VSP_Status.Push_Success.value, "VSP Status not Change to Push_Success"
        with allure.step("【Query】Diag Arbitration judgment && Receive Task"):    
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.QUERY.value, 65) and self.soa.till_fota_event_to(MASTER_EVENT.TaskId, self.taskid, 65), "Fail to Receive Task"
        with allure.step("【Query】Version Collect"):    
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.NEW_TASK.value, 480), "Reach Version Collect Maximum Timeout: 8min"
        with allure.step("【New_Task】Set FOTA Download Wake Condition: All Meet"):
            self.bus_comm.set_fota_download_wake_condition(display_hv_soc=900, low_volt_soc=90) 
        with allure.step("【New_Task】Start Download"):
            self.soa.send_fota_request(MASTER_REQUEST.StartDownload)
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.DOWNLOADING.value, "FOTA Master Fail to Enter DOWNLOADING Status"
        with allure.step("【Download】Change NetWork to 5G"):
            self.ssh.set_network_mode(Network_Mode.Fifth_Generation)
        with allure.step("【Download】New Event: DownloadProcess"):
            assert self.soa.get_fota_DownloadProcess(MASTER_DownloadProcess_EVENT.taskId) == self.taskid, "Not Receive DownloadProcess Event"
        with allure.step("【Download】Check VSP Status"):
            assert self.tsp.get_vsp_fota_status(self.taskid) == VSP_Status.Downloading.value, "VSP Status not Change to Downloading"
        with allure.step("【Download】Not Meet Wake Conditions"):
            assert self.mix.check_fota_keep_awake(pnc29=True, acu_keep_alive=None, up_inactive=True), "Abnormal Send Wake Condition"
        with allure.step("【Download】Wait for Download Complete"):
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.ACTIVE.value, 3600), "Reach Download Maximum Wake Timeout: 60min"
        with allure.step("【Remote_Update】Enter Remote_Update"):
            self.mix.back_fota_to(FOTAMasteSts.REMOTE_UPDATE, self.taskid)
        with allure.step("【Remote_Update】Start Update with All not Meet Conditions"):
            with allure.step("【Remote_Update】 Local Diag"):
                self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=800, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.Active)
                self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
                assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "【Local Diag】FOTA Master Fail to Back Active"
                self.mix.back_fota_to(FOTAMasteSts.REMOTE_UPDATE, self.taskid)
                assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.REMOTE_UPDATE.value, "FOTA Master Fail to Enter REMOTE_UPDATE Status"            
            with allure.step("【Remote_Update】 Speed"):
                self.mix.set_normal_fota_update_condition(vehspd=1000, gear=Gear.Park, display_hv_soc=800, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)
                self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
                assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "【Speed】FOTA Master Fail to Back Active"
                self.mix.back_fota_to(FOTAMasteSts.REMOTE_UPDATE, self.taskid)
                assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.REMOTE_UPDATE.value, "FOTA Master Fail to Enter REMOTE_UPDATE Status"
            with allure.step("【Remote_Update】 Gear"):
                self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Undefd, display_hv_soc=800, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)
                self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
                assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "【Gear】FOTA Master Fail to Back Active"
                self.mix.back_fota_to(FOTAMasteSts.REMOTE_UPDATE, self.taskid)
                assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.REMOTE_UPDATE.value, "FOTA Master Fail to Enter REMOTE_UPDATE Status"
            with allure.step("【Remote_Update】 Hv Soc"):
                self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=100, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)
                self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
                assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "【Hv Soc】FOTA Master Fail to Back Active"
                self.mix.back_fota_to(FOTAMasteSts.REMOTE_UPDATE, self.taskid)
                assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.REMOTE_UPDATE.value, "FOTA Master Fail to Enter REMOTE_UPDATE Status"
            with allure.step("【Remote_Update】 Thermal"):
                self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=800, thermaloutofcontrol=True, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)
                self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
                assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "【Thermal】FOTA Master Fail to Back Active"
                self.mix.back_fota_to(FOTAMasteSts.REMOTE_UPDATE, self.taskid)
                assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.REMOTE_UPDATE.value, "FOTA Master Fail to Enter REMOTE_UPDATE Status"
            with allure.step("【Remote_Update】 Low Volt Soc"):
                self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=800, thermaloutofcontrol=False, low_volt_soc=50, local_diag_sts=DiagActLineSts.DisActive)
                self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
                assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value, "【Low Volt Soc】FOTA Master Fail to Back Active"
                self.mix.back_fota_to(FOTAMasteSts.REMOTE_UPDATE, self.taskid)
                assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.REMOTE_UPDATE.value, "FOTA Master Fail to Enter REMOTE_UPDATE Status"
            with allure.step("【Remote_Update】 All Meet"):
                self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=800, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)
                self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
                assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.UPDATE.value, 10), "FOTA Master Fail to Enter UPDATE Status"
        with allure.step("【Update】Check VSP Status"):
            assert self.tsp.get_vsp_fota_status(self.taskid) == VSP_Status.Upgrading.value, "VSP Status not Change to Downloading"
        with allure.step("【Successful】Back to Idle"):
            assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.IDLE.value, 3600), "Reach Domain Update Maximum Timeout: 60min"            
           
if __name__ == "__main__":
    pass

    




