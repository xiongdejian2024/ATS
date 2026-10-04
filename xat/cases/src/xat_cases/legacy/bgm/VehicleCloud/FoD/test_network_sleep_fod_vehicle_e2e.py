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
@allure.story("FOD")
class TestFod(TestABCBase):
    num = 2 #压测次数
    def before_class(self, ecu):
        super().before_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
                
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @pytest.mark.repeat(num)
    @allure.title("Network_Sleep_FoD_Vehicle_E2E")    
    def test_fod_caseid_1985958(self):
        global cur_num
        cur_num = cur_num + 1
        with self.log_manage.check_jetlog_by_keywords(log_type=" ccp:", 
                                                      keywords='data: {"code":0,"msg":"sync ccp succ","taskId":',
                                                      timeout=1500):
            self.tsp.rvs_event_check(block=BlockName.VehicleMode, keys=["usage"], target_value="UsageModeAbandoned",timeout = 1200)
            time.sleep(60)#usagemode跳变abandoned后 约2min才能整车休眠
            self.fod_e2e_config['operationType']=2
            self.tsp.trigger_fod_task(FodConfig=self.fod_e2e_config)
            logger.info('================================激活任务下发成功===================================')
            
        with self.log_manage.check_jetlog_by_keywords(log_type=" ccp:", 
                                                      keywords='data: {"code":0,"msg":"sync ccp succ","taskId":',
                                                      timeout=1500):
            self.tsp.rvs_event_check(block=BlockName.VehicleMode, keys=["usage"], target_value="UsageModeAbandoned",timeout = 1200)
            time.sleep(60)#usagemode跳变abandoned后 约2min才能整车休眠
            self.fod_e2e_config['operationType']=1
            self.tsp.trigger_fod_task(FodConfig=self.fod_e2e_config)
            logger.info('================================取消激活任务下发成功================================')

               
if __name__ == "__main__":
    pass
