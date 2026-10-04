import os
import sys
import pytest
import allure
from time import sleep
import random

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.case_helper.test_fota_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.api.common.common import set_bench_vlan9_ip

@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service")])
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
                                    FOTA_Skip_Debug.cdc_acu_doip_check
                                    ]) 
        self.ssh.update_ua_skip(DOMAIN.BGM, False)
        self.mix.update_version_debug(self.taskid,[DOMAIN.BGM])

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
        self.mix.back_fota_to(FOTAMasteSts.ACTIVE, taskid=self.taskid)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.ACTIVE.value
                    
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        self.mix.back_fota_to(FOTAMasteSts.IDLE, taskid=self.taskid)

    @pytest.mark.V_2_0
    @pytest.mark.sanity
    @allure.title("升级前状态检查_其他条件满足宠物模式服务连接失败_可进入升级") #once case 不需要启宠物模式相关服务
    def test_fota_caseid_1986726(self): 
        self.mix.set_normal_fota_update_condition(vehspd=0, gear=Gear.Park, display_hv_soc=250, thermaloutofcontrol=False, low_volt_soc=70, local_diag_sts=DiagActLineSts.DisActive)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='GetPetModeAsync:retry count:3,ret:613', timeout=200):
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == FOTAMasteSts.UPDATE.value
        self.soa.send_fota_request(MASTER_REQUEST.CancelFota)
        self.soa.till_fota_event_to(MASTER_EVENT.Status, FOTAMasteSts.FAILED_NOT_DRIVING.value, 300)
        
        

if __name__ == "__main__":
    pass

    




