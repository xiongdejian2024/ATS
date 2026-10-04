import os
import sys
import pytest
import allure
import time

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.case_helper.test_fota_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.interface.feishu.feishu_api import feishu_api

update_single_record  = {
            '失败次数': 0,
            '总压测次数': 0,
            '成功次数': 0,
        }
record_id = None
feishu = feishu_api()
@allure.feature("基础架构")
@allure.story("FOTA")
@pytest.mark.stress_test
class TestFota(TestABCBase):
    num = 100 #压测次数
    def before_class(self, ecu):
        # super().before_class(self, ecu)
        self.ssh.update_skip_debug([FOTA_Skip_Debug.wait_hmi,
                                    FOTA_Skip_Debug.factory_ecu_ver_collection
                                    ])
        self.super_file_name = f"factory_log"
        self.file_name = time.strftime("%m_%d_%H_%H:%M:%S", time.localtime(time.time()))
        self.cur_log_path = ""
        self.start_plane = ""
        log_folder = f"/root/log/{self.super_file_name}"
        os.makedirs(log_folder, exist_ok=True)
        os.makedirs(f"{log_folder}/{self.file_name}", exist_ok=True)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.mix.set_car_mode(CarMode.FACTORY)
        self.ssh.copy_factory_packages()
        self.ssh.clear_fota_cache()
        self.sd_tester.reset_bgm()
                
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.ssh.get_log(DeviceName.BGM, self.cur_log_path)
        global update_single_record, record_id, feishu
        if self.passed:
            update_single_record['成功次数'] += 1
        else:
            update_single_record["失败次数"] += 1
        feishu.get_tenant_access_token()
        feishu.get_app_access_token()
        feishu.get_user_access_token()
        feishu.get_bitable_app_access_token(document_id='TMhIwUiHtiseKMkJe1KcY5BNnxd')
        feishu.update_record_in_table(table_id="tblUEJJJuUSh69Ki", record_id=record_id, data=update_single_record)
        
    def after_class(self, ecu):
        # super().after_class(self, ecu)
        pass

    @pytest.mark.repeat(num)
    @allure.title("E2E_FactoryOTA_Smoke_台架全量刷写")    
    def test_fota_caseid_1983062(self):
        self.passed = False
        global record_id
        if record_id is None:
            bgm_version = self.sd_tester.get_bgm_app_soft_version()
            vin = self.tc_config.get('vin')
            single_record  = {
                                'BGM版本': bgm_version,
                                'VIN': vin,
                                '失败次数': 0,
                                '总压测次数': 0,
                                '成功次数': 0,
                                '日期': round(time.time() * 1000),
                                '环境': None,
                                '问题详情': "NA",
                                'allure报告': None
                            }
            global feishu
            feishu.get_tenant_access_token()
            feishu.get_app_access_token()
            feishu.get_user_access_token()
            feishu.get_bitable_app_access_token(document_id='TMhIwUiHtiseKMkJe1KcY5BNnxd')
            _, record_id = feishu.add_record_in_table(table_id="tblUEJJJuUSh69Ki", data=single_record)
            logger.info(record_id)
            if not record_id:
                raise Exception("record_id is None")
        global update_single_record
        update_single_record['总压测次数'] += 1
        cur_num = update_single_record['总压测次数']
        logger.info(f"当前执行第{cur_num}次厂内压测")
        self.cur_log_path = f"/root/log/{self.super_file_name}/{self.file_name}/{cur_num}"
        os.makedirs(self.cur_log_path, exist_ok=True)
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", 
                                                    keywords='FOTA Status:21',
                                                    timeout=300):
            pass
        start_time = time.time()
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", 
                                                    keywords='FOTA Status:22', 
                                                    timeout=1800):
            pass
        with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", 
                                                    keywords='get car mode ret:0 car mode:0',
                                                    timeout=300):
            pass
        with self.log_manage.check_jetlog_by_keywords(log_type="UpdateNotifyEOLCaliInfoEvent:", 
                                                    keywords= '''UpdateNotifyEOLCaliInfoEvent:{"Device":1,"Status":3,"ErrorCode":0,"NRC":0}''', 
                                                    timeout=300):
            pass
        self.passed = True
        end_time = time.time()
        if end_time - start_time >= 29 * 60:
            self.passed = False
            assert False, "厂内OTA升级超时"
if __name__ == "__main__":
    pass
