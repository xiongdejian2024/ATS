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
        assert self.soa.get_fota_status(master_event_field=MASTER_EVENT.Status) == 0    
            
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("任务触发_有zip包")
    def test_fota_caseid_1980134(self):
        self.mix.set_car_mode(car_mode=CarMode.FACTORY)
        self.ssh.copy_factory_packages()
        self.ssh.clear_fota_cache()
        self.sd_tester.reset_bgm()
        assert self.soa.get_fota_status(master_event_field=MASTER_EVENT.Status) == FOTAMasteSts.FACTORY_TASK.value and self.soa.get_fota_status(master_event_field=MASTER_EVENT.TaskId) == 1
    
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("任务触发_无zip包")    
    def test_fota_caseid_1980133(self):
        self.mix.set_car_mode(car_mode=CarMode.FACTORY)
        self.ssh.rm_factory_packages()
        self.ssh.clear_fota_cache()
        self.sd_tester.reset_bgm()
        assert self.soa.get_fota_status(master_event_field=MASTER_EVENT.Status) == FOTAMasteSts.IDLE.value and self.soa.get_fota_status(master_event_field=MASTER_EVENT.TaskId) == 0
   
    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("任务触发_有state文件")    
    def test_fota_caseid_1980132(self):
        self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_FAILED)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='CheckCarMode:get car mode ret:0 car mode:0', timeout=120):
            pass
        sleep(30) #等待标定结束
        self.ssh.copy_factory_packages()
        self.mix.set_car_mode(car_mode=CarMode.FACTORY)
        self.sd_tester.reset_bgm()
        # assert self.soa.get_fota_status(master_event_field=MASTER_EVENT.Status) == FOTAMasteSts.FACTORY_FAILED.value #SOA-27132
        assert self.soa.get_fota_status(master_event_field=MASTER_EVENT.Status) == FOTAMasteSts.IDLE.value

    @pytest.mark.V_1_4
    @pytest.mark.smoke
    @allure.title("任务触发_点击开始刷写")    
    def test_fota_caseid_1982901(self):
        self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_TASK)
        self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
        assert self.soa.get_fota_status(master_event_field=MASTER_EVENT.Status) == FOTAMasteSts.FACTORY_UPDATE.value

    @pytest.mark.V_1_4
    @pytest.mark.sanity
    @allure.title("任务触发_左转向触发_≥3S")    
    def test_fota_caseid_1980131(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='HornServiceConnectionSts:connection status:1', timeout=120):
            self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_TASK)
        self.bus_comm.trigger_steer_wheel(time_interval=3.5)
        assert self.soa.get_fota_status(master_event_field=MASTER_EVENT.Status) == FOTAMasteSts.FACTORY_UPDATE.value 

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("任务触发_左转向触发_＜3S")    
    def test_fota_caseid_1980130(self):
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='HornServiceConnectionSts:connection status:1', timeout=120):
            self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_TASK)
        self.bus_comm.trigger_steer_wheel(time_interval=2)
        time.sleep(1)
        self.bus_comm.trigger_steer_wheel(time_interval=2)
        assert self.soa.get_fota_status(master_event_field=MASTER_EVENT.Status) == FOTAMasteSts.FACTORY_TASK.value

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("任务触发_左转向触发_OTA Master状态IDLE")    
    def test_fota_caseid_1980129(self):
        self.mix.set_car_mode(car_mode=CarMode.FACTORY)
        self.ssh.clear_fota_cache()
        self.sd_tester.reset_bgm()
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords='HandlStalkStatus:', timeout=10):
            self.bus_comm.trigger_steer_wheel(time_interval=3.5)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("任务触发_左转向触发_OTA Master状态FACTORY_UPDATE")    
    def test_fota_caseid_1980128(self):
        self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_UPDATE)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords='HandlStalkStatus:', timeout=20):
            self.bus_comm.trigger_steer_wheel(time_interval=3.5) 

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("任务触发_左转向触发_OTA Master状态FACTORY_SUCCESS")  
    def test_fota_caseid_1980127(self):
        self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_SUCCESSFUL)
        assert self.soa.get_fota_status(master_event_field=MASTER_EVENT.Status) == FOTAMasteSts.FACTORY_SUCCESSFUL.value
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords='HandlStalkStatus:', timeout=20):
            self.bus_comm.trigger_steer_wheel(time_interval=3.5)

    @pytest.mark.V_1_4
    @pytest.mark.full
    @allure.title("任务触发_左转向触发_OTA Master状态FACTORY_FAILED")    
    def test_fota_caseid_1980126(self):
        self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_FAILED)
        assert self.soa.get_fota_status(master_event_field=MASTER_EVENT.Status) == FOTAMasteSts.FACTORY_FAILED.value
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", unexpect_keywords='HandlStalkStatus:', timeout=20):
            self.bus_comm.trigger_steer_wheel(time_interval=3.5)        

    @pytest.mark.V_1_4
    @pytest.mark.sanity
    @allure.title("任务触发_维持唤醒")    
    def test_fota_caseid_1980125(self):
        self.mix.back_fota_to(fota_sts=FOTAMasteSts.FACTORY_TASK)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='SetVFCReqDiagnosticCb: VfcType :23 ActState :2', timeout=20): 
            self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)                   

if __name__ == "__main__":
    pass