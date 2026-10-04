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

@allure.feature("基础架构")
@allure.story("FOTA")
class TestFota(TestABCBase):
    num = 50 #压测次数
    def before_class(self, ecu):
        # super().before_class(self, ecu)
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
        self.ssh.clear_log(DeviceName.BGM)#重新拉代码需要手动加一下
        self.ssh.update_skip_debug([FOTA_Skip_Debug.wait_hmi,
                                    FOTA_Skip_Debug.factory_ecu_ver_collection
                                    ])
        self.ssh.clear_fota_cache()#不杀进程，仅删持久化文件，
        self.sd_tester.reset_all()
                
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.ssh.get_log(DeviceName.BGM, self.cur_log_path)
        self.ssh.type_commands(DeviceName.BGM, 'rm -rf /update/skip_debug;sync')
        self.sd_tester.reset_bgm()

    def after_class(self, ecu):
        # super().after_class(self, ecu)
        pass

    @pytest.mark.repeat(num)
    @allure.title("厂内ota")    
    def test_fota_caseid_1983962(self,ecu):
        self.passed = False
        self.cur_log_path = f"/root/log/{self.super_file_name}/{self.file_name}"
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
        # with self.log_manage.check_jetlog_by_keywords(log_type=" fota:", 
        #                                             keywords='get car mode ret:0 car mode:0',
        #                                             timeout=300):
        #     pass
        with self.log_manage.check_jetlog_by_keywords(log_type='-E "UpdateNotifyEOLCaliInfoEvent:| fota:"', 
                                                    keywords= ['get car mode ret:0 car mode:0',
                                                               '''UpdateNotifyEOLCaliInfoEvent:{"Device":1,"Status":3,"ErrorCode":0,"NRC":0}'''], 
                                                                timeout=500):
            pass
        self.passed = True
        end_time = time.time()
        update_time = end_time - start_time
        update_minutes = int(update_time // 60)
        update_seconds = round(update_time % 60, 2)
        allure.dynamic.description(f"本轮厂内OTA【开始升级】=>【标定结束】耗时{update_minutes}分{update_seconds}秒")
        logger.info(f"本轮厂内OTA【开始升级】=>【标定结束】耗时{update_minutes}分{update_seconds}秒")
        if update_time >= 29 * 60:
            self.passed = False
            assert False, "厂内OTA升级超时"
if __name__ == "__main__":
    pass
