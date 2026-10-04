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
class Test_factory_ota(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("FotaMasterService","client"),
                         ("UpdateAgentService","client","BGM_UA_Service"),
                         ("AcuModeManagerService","server")])
        self.ssh.update_skip_debug([
            FOTA_Skip_Debug.cdc_acu_doip_check
        ])
        time.sleep(20)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.mix.fota_back_to_idle()
        self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_TASK)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @pytest.mark.V_1_4
    @pytest.mark.sanity
    @allure.title("条件检测_升级中_FotaStatus发送")
    def test_fota_caseid_1980124(self):
        self.mix.set_factory_ota_condition(display_hv_soc=250,low_volt_power=11.5,local_diag_sts=DiagActLineSts.DisActive) 
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.bus_comm.check_InfoCan_FOTAStatus(infocanfotastatus=InfoCanFOTAStatus.Update.value)

    @pytest.mark.V_1_4
    @pytest.mark.sanity
    @allure.title("条件检测_升级结束_FotaStatus发送IDLE")
    def test_fota_caseid_1989591(self):
        self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_FAILED)
        assert self.bus_comm.check_InfoCan_FOTAStatus(infocanfotastatus=InfoCanFOTAStatus.Idle.value)

    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("满足大小电池==条件")
    def test_fota_caseid_1980123(self):
        self.mix.set_factory_ota_condition(display_hv_soc=250,low_volt_power=11.5,local_diag_sts=DiagActLineSts.DisActive) 
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert FOTA_ConditionCheck_Code.CR_SUCCESSFUL.value in self.soa.get_fota_ConditionCheckResults(MASTER_ConditionCheckResults_EVENT.Results)
  
    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("满足大小电池 > 条件")
    def test_fota_caseid_1983323(self):
        self.mix.set_factory_ota_condition(display_hv_soc=260,low_volt_power=14,local_diag_sts=DiagActLineSts.DisActive) 
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert FOTA_ConditionCheck_Code.CR_SUCCESSFUL.value in self.soa.get_fota_ConditionCheckResults(MASTER_ConditionCheckResults_EVENT.Results)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("条件检测_大电池不满足")
    def test_fota_caseid_1980122(self):
        self.mix.set_factory_ota_condition(display_hv_soc=240,low_volt_power=11.5,local_diag_sts=DiagActLineSts.DisActive) 
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert FOTA_ConditionCheck_Code.CR_HV_ERROR.value in self.soa.get_fota_ConditionCheckResults(MASTER_ConditionCheckResults_EVENT.Results)
        self.mix.set_factory_ota_condition(display_hv_soc=260,low_volt_power=11.5,local_diag_sts=DiagActLineSts.DisActive) 
        assert FOTA_ConditionCheck_Code.CR_SUCCESSFUL.value in self.soa.get_fota_ConditionCheckResults(MASTER_ConditionCheckResults_EVENT.Results)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("条件检测_小电池不满足")
    def test_fota_caseid_1980121(self):
        self.mix.set_factory_ota_condition(display_hv_soc=260,low_volt_power=11.4,local_diag_sts=DiagActLineSts.DisActive) 
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert FOTA_ConditionCheck_Code.CR_LV_ERROR.value in self.soa.get_fota_ConditionCheckResults(MASTER_ConditionCheckResults_EVENT.Results)
        self.mix.set_factory_ota_condition(display_hv_soc=260,low_volt_power=14,local_diag_sts=DiagActLineSts.DisActive) 
        assert FOTA_ConditionCheck_Code.CR_SUCCESSFUL.value in self.soa.get_fota_ConditionCheckResults(MASTER_ConditionCheckResults_EVENT.Results)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("条件检测_接入诊断仪")
    def test_fota_caseid_1980120(self):
        self.mix.set_factory_ota_condition(display_hv_soc=260,low_volt_power=14,local_diag_sts=DiagActLineSts.Active) 
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert FOTA_ConditionCheck_Code.CR_DIAGNOSTIC_ERROR.value in self.soa.get_fota_ConditionCheckResults(MASTER_ConditionCheckResults_EVENT.Results)
        self.mix.set_factory_ota_condition(display_hv_soc=260,low_volt_power=14,local_diag_sts=DiagActLineSts.DisActive) 
        assert FOTA_ConditionCheck_Code.CR_SUCCESSFUL.value in self.soa.get_fota_ConditionCheckResults(MASTER_ConditionCheckResults_EVENT.Results)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("条件检测_大电池持续不满足5min以上")
    def test_fota_caseid_1980119(self):
        self.mix.set_factory_ota_condition(display_hv_soc=240,low_volt_power=14,local_diag_sts=DiagActLineSts.DisActive) 
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status,target_status=FOTAMasteSts.FACTORY_FAILED.value, timeout=400)


    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("条件检测_小电池持续不满足5min以上")
    def test_fota_caseid_1980118(self):
        self.mix.set_factory_ota_condition(display_hv_soc=260,low_volt_power=11.4,local_diag_sts=DiagActLineSts.DisActive) 
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status,target_status=FOTAMasteSts.FACTORY_FAILED.value, timeout=400)


    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("条件检测_接入诊断仪5min以上")
    def test_fota_caseid_1980117(self):
        self.mix.set_factory_ota_condition(display_hv_soc=260,low_volt_power=14,local_diag_sts=DiagActLineSts.Active) 
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.till_fota_event_to(master_event_field=MASTER_EVENT.Status,target_status=FOTAMasteSts.FACTORY_FAILED.value, timeout=400)

if __name__ == "__main__":
    pass