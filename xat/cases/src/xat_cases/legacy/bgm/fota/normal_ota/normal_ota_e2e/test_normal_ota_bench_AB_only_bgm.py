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
@allure.story("FOTA")
@pytest.mark.stress_test
class TestFota(TestABCBase):
    num = 50 #压测次数
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.soa.update([("FotaMasterService","client")])
        """
        A为低版本, B -> A需要强刷开关
        B为高版本, A -> B不需要强刷开关
        """
        self.A_version = ["6160110200 BT"]  #["BGM version，TCAM version"]
        self.B_version = ["6160110200 FE"]
        self.taskid_A = 17835   
        self.taskid_B = 17836  
        self.need_flash_domain = [DOMAIN.BGM]
        
        self.ssh.update_skip_debug([FOTA_Skip_Debug.baseline,
                                    FOTA_Skip_Debug.before_group_1081,
                                    FOTA_Skip_Debug.before_group_hv_ctl,
                                    FOTA_Skip_Debug.ecm3_down_hv,
                                    FOTA_Skip_Debug.fota_mode_requeset_acu,
                                    FOTA_Skip_Debug.fota_mode_requeset_cdc,
                                    FOTA_Skip_Debug.fota_mode_requeset_ecm3,
                                    FOTA_Skip_Debug.upload_version_from_debug_file,
                                    FOTA_Skip_Debug.CDC_UA,
                                    FOTA_Skip_Debug.ACU_UA,
                                    FOTA_Skip_Debug.version_collect,
                                    FOTA_Skip_Debug.cdc_acu_doip_check,
                                    FOTA_Skip_Debug.update_precondition_check,
                                    FOTA_Skip_Debug.start_download,
                                    FOTA_Skip_Debug.car_mode_normal
                                    ]) 
        self.mix.set_enter_boot_condition(UsageMode.CONVENIENCE, low_volt_power=14, vehspd=0)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.io.bgm_diag_line_down()
        if self.soa.get_fota_status(MASTER_EVENT.Status) == 0:
            try:
                self.allure_title = ''
                mpu_version = str(self.sd_tester.read_bgm_mpu_version())
                time.sleep(1)
                mcu_version = str(self.sd_tester.read_bgm_mcu_version())
                time.sleep(1)
                switch_version = str(self.sd_tester.read_bgm_switch_version())
                self.allure_title = mpu_version + mcu_version + switch_version
            except:
                pass
        else:
            logger.info(self.soa.get_fota_status(MASTER_EVENT.Status))
            assert False
        cur_bgm_version = self.sd_tester.get_bgm_app_soft_version()
        # cur_tcam_version = self.sd_tester.get_tcam_soft_version()
        # if [cur_bgm_version, cur_tcam_version] == self.A_version:
        if [cur_bgm_version] == self.A_version:
            # 当前A -> B，不需要强刷开关
            self.taskid = self.taskid_B
            # self.ssh.update_ua_skip(DOMAIN.BGM, allow_same_version_flash=False)
            # self.ssh.update_ua_skip(DOMAIN.TCAM, allow_same_version_flash=False)
            logger.info(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            logger.info(f"version is {self.A_version}")
            logger.info(f"taskid is {self.taskid}")
            logger.info(f"升级路径：{self.A_version} => {self.B_version}")
            logger.info(self.allure_title)
            logger.info(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # elif [cur_bgm_version, cur_tcam_version] == self.B_version:
        elif [cur_bgm_version] == self.B_version:
            # 当前B -> A，需要强刷开关
            self.taskid = self.taskid_A
            # self.ssh.update_ua_skip(DOMAIN.BGM, allow_same_version_flash=True)
            # self.ssh.update_ua_skip(DOMAIN.TCAM, allow_same_version_flash=True)
            logger.info(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            logger.info(f"version is {self.B_version}")
            logger.info(f"taskid is {self.taskid}")
            logger.info(f"升级路径：{self.B_version} => {self.A_version}")
            logger.info(self.allure_title)
            logger.info(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        else:
            logger.error(f"ERROR version !!!")        
        self.mix.update_version_debug(self.taskid,self.need_flash_domain)
        self.tsp.trigger_vsp_fota(VSP.Reset, self.taskid_A)
        self.tsp.trigger_vsp_fota(VSP.Reset, self.taskid_B)
        self.io.bgm_diag_line_down()
        try:
            if not self.sd_tester.check_mcu_whether_in_boot():
                logger.info("BGM MCU not in BOOT Mode")
                self.mix.set_enter_boot_condition(UsageMode.CONVENIENCE, low_volt_power=14, vehspd=0)
        except Exception as error:
            logger.error(error)
                
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @allure.title("A/B fota")
    @pytest.mark.repeat(num)
    @allure.title("E2E_Normal_Bench_n-3")    
    def test_fota_caseid_1985897(self):
        allure.dynamic.title(self.allure_title)
        global cur_num
        cur_num = cur_num + 1
        
        vsp_first_status = self.tsp.get_vsp_fota_status(task_id = self.taskid)
        if vsp_first_status == 18:
            self.tsp.trigger_vsp_fota(VSP.Repub, self.taskid)
        while True:
            try:
                vsp_status = self.tsp.get_vsp_fota_status(task_id = self.taskid) 
                if vsp_status == 15:
                    logger.info(f"=========== 任务id: {self.taskid}, {self.allure_title}, 推送中 ===========")
                elif vsp_status == 4:
                    logger.info(f"=========== 任务id: {self.taskid}, {self.allure_title}, 下载中 ===========")
                elif vsp_status == 5:
                    logger.info(f"=========== 任务id: {self.taskid}, {self.allure_title}, 下载成功 ===========")
                    self.soa.send_fota_request(MASTER_REQUEST.StartUpdate)
                elif vsp_status == 8:
                    logger.info(f"=========== 任务id: {self.taskid}, {self.allure_title}, 升级中 ===========")
                elif vsp_status == 18:
                    logger.info(f"=========== 任务id: {self.taskid}, {self.allure_title}, FOTA成功 ===========")
                    time.sleep(20)
                    break
                elif vsp_status == 18:
                    logger.info(f"=========== 任务id: {self.taskid}, {self.allure_title}, FOTA失败 ===========")
                elif vsp_status == 20:
                    logger.info(f"=========== 任务id: {self.taskid}, {self.allure_title}, FOTA取消, Repub Task ===========")
                    self.tsp.trigger_vsp_fota(VSP.Repub, self.taskid)
                elif vsp_status == 21:
                    logger.info(f"=========== 任务id: {self.taskid}, {self.allure_title}, FOTA 重置, Repub Task ===========")
                    self.tsp.trigger_vsp_fota(VSP.Repub, self.taskid)
                else:
                    logger.info(f"=========== 任务id: {self.taskid}, {self.allure_title}, VSP status is {vsp_status} ===========")
            except Exception as e:
                logger.error(f"{str(e)}")
            
if __name__ == "__main__":
    pass

    




