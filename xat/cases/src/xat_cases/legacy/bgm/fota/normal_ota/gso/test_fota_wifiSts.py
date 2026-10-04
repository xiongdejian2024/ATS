import os
import sys
import pytest
import allure
from time import sleep
import random
import copy
import json
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.case_helper.test_fota_base import TestABCBase
from xat_ecu.api.abc_interface import *

@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota_Code(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([
            ("FotaMasterService","client"),
            ("UpdateAgentService","client","BGM_UA_Service"),
            ("V2TRoutingForwarder","client","V2TOTAFotaForwarder"),
            ("InteractiveService","server"),
            ("InteractiveService","client")
            ])
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
                                    FOTA_Skip_Debug.start_download,
                                    FOTA_Skip_Debug.update_precondition_check
                                    ], allow_sleep=False) 
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM])
        self.taskid_tmp = 99999 #赋值个平台不存在的taskid
        time.sleep(20)
        self.soa.trigger_fota_type20(self.taskid_tmp)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords="upload_version => wait_task_info", timeout=600):
            Task_Info_Type50 = copy.deepcopy(self.Task_Info_Type50_NKR)
            Task_Info_Type50['data']['taskId'] = self.taskid_tmp
            Task_Info_Type50['data']["downloadNetType"] = 2
        self.soa.call_vehicle_api(V2T_API.OTA, payload=Task_Info_Type50)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"02FA"'], timeout=70):
            time.sleep(30) 
            assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.DOWNLOADING.value, "FOTA Status is not DOWNLOADING"    

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
                            
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)        
        
    @pytest.mark.parametrize('usage_mode, isWifiConnectHotSpot, type, hasAccessibility', [
                              pytest.param(UsageMode.ACTIVE, 1, "0", "false", id="1999067", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(UsageMode.ACTIVE, 1, "0", "true", id="1999066", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(UsageMode.ACTIVE, 1, "1", "false", id="1999065", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(UsageMode.ACTIVE, 0, "0", "false", id="1999039", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(UsageMode.ACTIVE, 0, "0", "true", id="1999069", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(UsageMode.ACTIVE, 0, "1", "false", id="1999068", marks=[pytest.mark.sanity, pytest.mark.V_2_0]),
                              pytest.param(UsageMode.DRIVING, 1, "0", "false", id="1999061", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(UsageMode.DRIVING, 1, "0", "true", id="1999060", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(UsageMode.DRIVING, 1, "1", "false", id="1999059", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(UsageMode.DRIVING, 0, "0", "false", id="1999064", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(UsageMode.DRIVING, 0, "0", "true", id="1999063", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(UsageMode.DRIVING, 0, "1", "false", id="1999062", marks=[pytest.mark.sanity, pytest.mark.V_2_0]),
                              pytest.param(UsageMode.CONVENIENCE, 1, "0", "false", id="1999055", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(UsageMode.CONVENIENCE, 1, "0", "true", id="1999054", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(UsageMode.CONVENIENCE, 1, "1", "false", id="1999053", marks=[pytest.mark.sanity, pytest.mark.V_2_0]),
                              pytest.param(UsageMode.CONVENIENCE, 0, "0", "false", id="1999058", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(UsageMode.CONVENIENCE, 0, "0", "true", id="1999057", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(UsageMode.CONVENIENCE, 0, "1", "false", id="1999056", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(UsageMode.INACTIVE, 1, "0", "false", id="1999049", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(UsageMode.INACTIVE, 1, "0", "true", id="1999048", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(UsageMode.INACTIVE, 1, "1", "false", id="1999047", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(UsageMode.INACTIVE, 0, "0", "false", id="1999052", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(UsageMode.INACTIVE, 0, "0", "true", id="1999051", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(UsageMode.INACTIVE, 0, "1", "false", id="1999050", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(UsageMode.ABANDONED, 1, "0", "false", id="1999043", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(UsageMode.ABANDONED, 1, "0", "true", id="1999042", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(UsageMode.ABANDONED, 1, "1", "false", id="1999041", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(UsageMode.ABANDONED, 0, "0", "false", id="1999046", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(UsageMode.ABANDONED, 0, "0", "true", id="1999045", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                              pytest.param(UsageMode.ABANDONED, 0, "1", "false", id="1999044", marks=[pytest.mark.full, pytest.mark.V_2_0]),
                            ])
    def test_fota_caseid_(self, usage_mode, isWifiConnectHotSpot, type, hasAccessibility):
        self.mix.set_usage_mode(usage_mode=usage_mode)
        self.soa.start_send_InteractiveService_response_gso(0)  
        time.sleep(6)
        self.soa.notify_wifiStsChanged_NetWorkAccess(type="1", hasAccessibility="false") 
        if usage_mode==UsageMode.DRIVING:
            with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"02FB"'], timeout=5):
                self.soa.notify_wifiStsChanged_NetWorkAccess(type="1", hasAccessibility="true") 
                self.mix.set_usage_mode(usage_mode=usage_mode)    
        else:
            with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"02FC"'], timeout=5):
                self.soa.notify_wifiStsChanged_NetWorkAccess(type="1", hasAccessibility="true")     
        self.soa.update_InteractiveService_get_response(isWifiConnectHotSpot=isWifiConnectHotSpot)  
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords=['"stateCode":"02FA"'], timeout=5):
            self.soa.notify_wifiStsChanged_NetWorkAccess(type=type, hasAccessibility=hasAccessibility) 
        self.soa.stop_send_InteractiveService_response_gso()