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
from xat_cases.legacy.bgm.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *

@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.vehicle_vin = 'L6T79P4N7PD000259'
        self.soft_id = 8877 # 整车软件号

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        get_skip_ecu_list(vin=self.vehicle_vin)
       
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
 
    def test_fota_caseid_007(self):
        self.tsp.create_vsp_task(vin=self.vehicle_vin,
                                 skip_ecu=get_skip_ecu_list(vin=self.vehicle_vin),
                                 target_soft_id=self.soft_id)
 
if __name__ == "__main__":
    pass

    




