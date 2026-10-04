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
from xat_cases.legacy.bgm.case_helper.test_fota_bridge import TestABCBase
from xat_ecu.api.abc_interface import *

@pytest.mark.V_2_0
@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service"),
                         ("VehicleSetStatusService","client"),
                         ("InteractiveService","server"),
                         ("CentralLockService","client"),
                         ("VehicleModeService","client"),
                         ("HighVoltageService","client"),
                         ("V2TRoutingForwarder","client","V2TOTAFotaForwarder")
                         ])
        self.ssh.update_skip_debug([FOTA_Skip_Debug.baseline,
                                    FOTA_Skip_Debug.before_group_1081,
                                    FOTA_Skip_Debug.before_group_hv_ctl,
                                    FOTA_Skip_Debug.ecm3_down_hv,
                                    FOTA_Skip_Debug.fota_mode_requeset_acu,
                                    FOTA_Skip_Debug.fota_mode_requeset_cdc,
                                    FOTA_Skip_Debug.fota_mode_requeset_ecm3,
                                    FOTA_Skip_Debug.upload_version_from_debug_file,
                                    FOTA_Skip_Debug.ACU_UA,
                                    FOTA_Skip_Debug.CDC_UA,
                                    FOTA_Skip_Debug.version_collect,
                                    FOTA_Skip_Debug.cdc_acu_doip_check,
                                    FOTA_Skip_Debug.car_mode_normal
                                    ]) 
        self.mix.set_enter_boot_condition(UsageMode.CONVENIENCE, low_volt_power=14, vehspd=0)
        self.taskid_tmp = 99999
        self.bridgeId = 88888
        self.mix.update_version_debug(self.taskid_tmp,[DOMAIN.BGM]) 
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
        self.soa.trigger_fota_type20(self.taskid_tmp)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="upload_version => wait_task_info", timeout=600):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50)
            Task_Info_Type50['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50['data']['bridgeId'] = self.bridgeId
            Task_Info_Type50['data']['serialNumber'] = 1
            Task_Info_Type50['data']['currentFotaTask'] = 2
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.NEW_TASK.value, 20), "type50 not take effect"
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, self.taskid_tmp)
        assert self.soa.get_fota_status(MASTER_EVENT.TaskType) == 2
                
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.mix.fota_back_to_idle()
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        
    @pytest.mark.sanity
    @allure.title("一键过桥_条件检测_大电池电量不满足(0404)")    
    def test_fota_caseid_1987643(self):
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=290, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)   
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"0404"'], timeout=60):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)

    @pytest.mark.sanity
    @allure.title("一键过桥_条件检测_网络不佳(0414)")    
    def test_fota_caseid_1987642(self):
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=310, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)   
        try:
            self.ssh.set_airplane_mode(isOn.On)
            with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"0414"'], timeout=60):
                self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        finally:
            self.ssh.set_airplane_mode(isOn.Off)

    @pytest.mark.smoke
    @allure.title("一键过桥_条件检测_条件全满足")    
    def test_fota_caseid_1987644(self):
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=310, thermaloutofcontrol=False, low_volt_soc=90, local_diag_sts=DiagActLineSts.DisActive)   
        self.soa.set_maintenanceMode(False)
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.UPDATE.value, 120)

if __name__ == "__main__":
    pass

