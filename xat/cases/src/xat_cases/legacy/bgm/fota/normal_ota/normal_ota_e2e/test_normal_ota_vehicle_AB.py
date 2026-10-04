import os
import sys
import pytest
import allure
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *

cur_num = 0
@allure.feature("基础架构")
@allure.story("FOTA")
@pytest.mark.stress_test
class TestFota(TestABCBase):
    num = 20 #压测次数
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.vin = "L6T79P2N2PP002437"
        self.vid = "83c3d1e750f7f3a1675d64e05a2431a2"
        self.tel = "18221073295"
        self.taskid_down = 29164
        self.taskid_up = 29163
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        
    @pytest.mark.repeat(num)
    @allure.title("E2E_Normal_Vehicle_Base")    
    def test_fota_caseid_1983157(self):
        global cur_num
        cur_num = cur_num + 1
        self.tsp.trigger_vsp_fota(VSP.Repub, self.taskid_down, vin = self.vin)
        time.sleep(2)
        while True:
            try:
                vsp_status = self.tsp.get_vsp_fota_status(task_id = self.taskid_down, vin = self.vin) 
                if vsp_status == 15:
                    logger.info(f"===========降级{self.taskid_down}推送中 ===========")
                elif vsp_status == 4:
                    logger.info(f"===========降级{self.taskid_down}下载中 ===========")
                elif vsp_status == 5:
                    logger.info(f"===========降级{self.taskid_down}下载成功 ===========")
                    self.tsp.trigger_update_by_real_app(vid = self.vid, tel=self.tel)
                    time.sleep(180)
                elif vsp_status == 8:
                    logger.info(f"===========降级{self.taskid_down}升级中 ===========")
                elif vsp_status == 18:
                    logger.info(f"===========降级{self.taskid_down}FOTA成功 ===========")
                    time.sleep(120)
                    break
                elif vsp_status == 19:
                    logger.info(f"===========降级{self.taskid_down}FOTA失败 ===========")
                elif vsp_status == 20:
                    logger.info(f"===========降级{self.taskid_down}FOTA取消, Repub Task ===========")
                    self.tsp.trigger_vsp_fota(VSP.Repub, self.taskid_down, vin = self.vin)
                else:
                    logger.info(f"===========降级{self.taskid_down}VSP status is {vsp_status} ===========")
            except Exception as e:
                logger.error(f"{str(e)}")
                
        self.tsp.trigger_vsp_fota(VSP.Repub, self.taskid_up, vin = self.vin)
        time.sleep(2)
        while True:
            try:
                vsp_status = self.tsp.get_vsp_fota_status(task_id = self.taskid_up, vin = self.vin) 
                if vsp_status == 15:
                    logger.info(f"===========升级{self.taskid_up}推送中 ===========")
                elif vsp_status == 4:
                    logger.info(f"===========升级{self.taskid_up}下载中 ===========")
                elif vsp_status == 5:
                    logger.info(f"===========升级{self.taskid_up}下载成功 ===========")
                    self.tsp.trigger_update_by_real_app(vid = self.vid, tel=self.tel)
                    time.sleep(180)
                elif vsp_status == 8:
                    logger.info(f"===========升级{self.taskid_up}升级中 ===========")
                elif vsp_status == 18:
                    logger.info(f"===========升级{self.taskid_up}FOTA成功 ===========")
                    time.sleep(120)
                    break
                elif vsp_status == 19:
                    logger.info(f"===========升级{self.taskid_up}FOTA失败 ===========")
                elif vsp_status == 20:
                    logger.info(f"===========升级{self.taskid_up}FOTA取消, Repub Task ===========")
                    self.tsp.trigger_vsp_fota(VSP.Repub, self.taskid_up, vin = self.vin)
                else:
                    logger.info(f"===========升级{self.taskid_up}VSP status is {vsp_status} ===========")
            except Exception as e:
                logger.error(f"{str(e)}")
            
if __name__ == "__main__":
    pass

    




