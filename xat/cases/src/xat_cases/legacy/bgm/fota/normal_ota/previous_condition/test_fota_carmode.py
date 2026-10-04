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
                         ("UpdateAgentService","client","BGM_UA_Service")])
        self.ssh.update_skip_debug(["time_check","cdc_ua"])
        time.sleep(20)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
                
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @pytest.mark.smoke
    @allure.title("FOTA模式_Normal")    
    def test_fota_caseid_1979790(self):
        self.mix.set_car_mode(CarMode.NORMAL)
        self.sd_tester.reset_bgm()
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == 0

    @pytest.mark.smoke
    @allure.title("FOTA模式_Factory")    
    def test_fota_caseid_1979789(self):
        self.mix.set_car_mode(CarMode.FACTORY)
        self.sd_tester.reset_bgm()
        assert self.soa.get_fota_status(MASTER_EVENT.Status) == 0

    @pytest.mark.full
    @pytest.mark.V_1_4
    @allure.title("FOTA模式_Transport")    
    def test_fota_caseid_1979788(self):
        self.mix.set_car_mode(CarMode.TRANSPORT)
        self.sd_tester.reset_bgm()
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='get car mode ret:0 car mode:1', timeout=60):
            pass

    @pytest.mark.full
    @pytest.mark.V_1_4
    @allure.title("FOTA模式_Crash")    
    def test_fota_caseid_1979787(self):
        self.mix.set_car_mode(CarMode.CRASH)
        self.sd_tester.reset_bgm()
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='get car mode ret:0 car mode:3', timeout=60):
            pass
            
    @pytest.mark.full
    @pytest.mark.V_1_4
    @allure.title("FOTA模式_Dyno")    
    def test_fota_caseid_1979786(self):
        self.mix.set_car_mode(CarMode.DYNO)
        self.sd_tester.reset_bgm()
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", keywords='get car mode ret:0 car mode:5', timeout=60):
            pass
            
if __name__ == "__main__":
    pass

    




