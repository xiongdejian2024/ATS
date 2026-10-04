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

@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
       
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
 
    def test_fota_caseid_005(self):
        skip_ecu_list = ['VDDM', 'SRS', 'IPM', 'BBM', 'FLR']
        self.tsp.create_vsp_task(vin='L6T79P2N2PP002437',
                                 skip_ecu=skip_ecu_list,
                                 target_soft_id=6433)
        
if __name__ == "__main__":
    pass

    




