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
    num = 10 #压测次数
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.vin = "JDS0ATESTBENCH059"
        self.vid = "e836c4cd5719aa25e3aede3b46643b1d"
        # self.tel = "15000460518"
        self.taskid = 25468
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)
        
    @pytest.mark.repeat(num)
    @allure.title("两域FOTA压测")    
    def test_fota_caseid_1983956(self):
        global cur_num
        cur_num = cur_num + 1
        # self.tsp.trigger_vsp_fota(VSP.Reset, self.taskid, vin = self.vin)
        # time.sleep(2)
        # self.tsp.trigger_vsp_fota(VSP.Repub, self.taskid, vin = self.vin)
        # time.sleep(2)
        self.bus_comm.set_fota_download_wake_condition(display_hv_soc=100, low_volt_soc=90)
        self.mix.set_enter_boot_condition(UsageMode.CONVENIENCE, low_volt_power=14, vehspd=0)
        while True:
            try:
                vsp_status = self.tsp.get_vsp_fota_status(task_id = self.taskid, vin = self.vin) 
                if vsp_status == 15:
                    logger.info(f"=========== {self.taskid}推送中 ===========")
                elif vsp_status == 4:
                    logger.info(f"=========== {self.taskid}下载中 ===========")
                elif vsp_status == 5:
                    logger.info(f"=========== {self.taskid}下载成功 ===========")
                    # self.tsp.trigger_update_by_real_app(vid =self.vid, tel=self.tel)
                    sleep(30)
                elif vsp_status == 8:
                    logger.info(f"=========== {self.taskid}升级中 ===========")
                elif vsp_status == 18:
                    logger.info(f"=========== {self.taskid}FOTA成功 ===========")
                    sleep(70)
                    self.tsp.trigger_vsp_fota(VSP.Repub, self.taskid, vin = self.vin)
                    break
                elif vsp_status == 19:
                    logger.info(f"=========== {self.taskid}FOTA失败 ===========")
                elif vsp_status == 20:
                    logger.info(f"=========== {self.taskid}FOTA取消, Repub Task ===========")
                    time.sleep(50)
                    self.tsp.trigger_vsp_fota(VSP.Repub, self.taskid, vin = self.vin)
                else:
                    logger.info(f"=========== {self.taskid}VSP status is {vsp_status} ===========")
            except Exception as e:
                logger.error(f"{str(e)}")

    # @allure.title("E2E_Normal_Vehicle_Base")    
    # def test_fota_caseid_aaa(self):
    #     # self.bus_comm.set_batturaw(BattURaw=11.0)
    #     # pdu_data_map = {
    #     #     50: [0xF4, 0x01, 0xB4, 0x00, 0x00, 0x00, 0x00],
    #     #     69: [0xB2, 0x02, 0xB4, 0x00, 0x00, 0x00, 0x00],
    #     #     70: [0xBC, 0x02, 0xB4, 0x00, 0x00, 0x00, 0x00],
    #     #     71: [0xC6, 0x02, 0xB4, 0x00, 0x00, 0x00, 0x00],
    #     #     90: [0x84, 0x03, 0xB4, 0x00, 0x00, 0x00, 0x00]
    #     # }
    #     # self.bus_comm.ipdu.send_pdu("cem_lin6", 0x06, [0x84, 0x03, 0xB4, 0x00, 0x00, 0x00, 0x00])
    #     # logger.info(f"成功设置小电池电量SOC值为{90}")
    #     self.bus_comm.ipdu.set(self.bus_comm.ipdu.cem_lin6.BmsCem_Lin6Fr05, 'BattURaw_0_BmsCem_Lin6SignalIPdu05', 15)
    #     sleep(10)
    
    # if __name__ == "__main__":
    #     pass

    




