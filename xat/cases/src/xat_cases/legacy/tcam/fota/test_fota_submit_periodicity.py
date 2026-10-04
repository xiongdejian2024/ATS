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
from xat_cases.legacy.tcam.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *

class TestFota(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.fota_version = ecu.get("fota_version")
        self.tcam_version = eval(self.fota_version)[1] + '.bin'
        logger.info(f"TCAM version is:{self.tcam_version}")
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu) 
        
    def test_fota_caseid_0x(self):
        appStatus, appId= self.tsp.check_appStatus(self.tcam_version) 
        if appStatus == 0:
            #app上库，但未提测
            self.tsp.submit_app(app_name=self.tcam_version) #提测app
            assert True
        elif appStatus == 10:
            #app上库，且已提测
            assert False, f"{self.tcam_version} 上库，且已提测"
        elif appStatus == None:
            #app未上库，直接报错
            assert False, f"{self.tcam_version} 未上库"
        else:
            assert False, f"Wrong Status with {self.tcam_version}: {appStatus}"
