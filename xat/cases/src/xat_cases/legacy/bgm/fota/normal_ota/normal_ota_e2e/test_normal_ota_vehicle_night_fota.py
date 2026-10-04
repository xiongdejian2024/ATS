import os
import sys
import pytest
import allure
import yaml
from time import sleep
import datetime
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.interface.cybertron.cybertron_api import CybertronApi
from xat_ecu.legacy.interface.feishu import feishu_api

@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.vehicle_vin = 'L6T79P2N2PP002437'
        self.soft_id = 9081 # 整车软件号

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
        cur_taskid = self.tsp.check_task_existence(vin=self.vehicle_vin, soft_id=self.soft_id)[1]
        self.BGM_vsp_version = self.tsp.get_domain_version_from_softid(self.soft_id, DOMAIN.BGM)
        self.TCAM_vsp_version = self.tsp.get_domain_version_from_softid(self.soft_id, DOMAIN.TCAM)
        Cybertron = CybertronApi()
        car_info = Cybertron.get_ecu_by_vin(vin=self.vehicle_vin)
        for ecu in car_info:
            if ecu["ecuName"] == "BGM":
                BGM_real_version = ecu["softwareMap"]["APP"]["softVersion"]
                logger.info(BGM_real_version)
            elif ecu["ecuName"] == "TCAM":
                TCAM_real_version = ecu["softwareMap"]["APP"]["softVersion"]
                logger.info(TCAM_real_version)
        
        # 获取当前时间
        current_datetime = datetime.datetime.now()
        # 计算往后一天的时间
        next_day_datetime = current_datetime + datetime.timedelta(days=1)
        # 将时间设置为凌晨3点，保留日期部分
        target_datetime = datetime.datetime(next_day_datetime.year, next_day_datetime.month, next_day_datetime.day, 3, 0, 0)
        
        single_record  = {
                                'BGM-Base版本': BGM_real_version,
                                'BGM-Target版本': self.BGM_vsp_version,
                                'TCAM-Base版本': TCAM_real_version,
                                'TCAM-Target版本': self.TCAM_vsp_version,
                                'VIN': self.vehicle_vin,
                                'task id': cur_taskid,
                                '总压测次数': 1,
                                '成功次数': 1,
                                '失败次数': 0,
                                '夜间升级': '是',
                                '升级方式_暂存' : ["夜间升级"],
                                '日期': round(target_datetime.timestamp() * 1000),
                                '问题详情': "NA"
                            }
        feishu_api.insert_record_to_feishu_table(data=single_record, table_name="常规OTA", document_id='TMhIwUiHtiseKMkJe1KcY5BNnxd')
 
if __name__ == "__main__":
    pass
