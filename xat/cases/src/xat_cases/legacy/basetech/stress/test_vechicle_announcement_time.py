import pytest
import allure
import numpy as np
from xat_cases.legacy.basetech.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_cases.legacy.basetech.case_helper.diag_case_helper.DiagTestBase import *


test_count=0
test_count_flash_boot=0
test_count_flash_app=0
test_count_sleepwakeup=0
interval_1082=0
interval_1101=0
interval_1181=0
interval_1181_flash_boot=0
interval_1181_flash_app=0
interval_sleepwakeup=0

@allure.feature('BGM BaseTech/诊断功能/车辆公告')
class TestVechicleAnnouncement(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self,ecu)
        logger.info("before_class")
        with allure.step("初始化环境"):
            self.mix.init_boot_per()    
        self.all_1082= []
        self.all_1181=[]
        self.all_1101=[]
        self.all_1181_flash_boot=[]
        self.all_1181_flash_app=[]
        self.all_sleepwakeup=[]
        
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        logger.info("===========case开始运行============")

    def after_each_func(self, ecu):
        time.sleep(5)#等待抓包，防止抓包进程被kill掉导致丢包
        super().after_each_func(ecu)
        if interval_1082 > 40 or interval_1181 > 40:
            logger.info("超时40s车辆公告未发出,保存环境")
            time.sleep(1000000000)
            
        with allure.step("等待45s"):
            logger.info('等待45s')
            time.sleep(45)
        logger.info("===========case运行结束============")
        
    def after_class(self, ecu):
        logger.info("after_class")
        super().after_class(self, ecu)
        logger.info("Test ending ...")
        logger.info(f"#############_物理寻址下获取1101重启后第一条车辆公告发出时间测试{test_count}次#############")
        logger.info(f"#############平均发出车辆公告时间{np.mean(self.all_1101)}s#############")
        logger.info(f"#############最大发出车辆公告时间{np.max(self.all_1101)}s#############")
        logger.info(f"#############最小发出车辆公告时间{np.min(self.all_1101)}s#############")
        logger.info('\n')
        logger.info(f"#############_功能寻址下获取1082进boot后第一条车辆公告发出时间测试{test_count}次#############")
        logger.info(f"#############平均发出车辆公告时间{np.mean(self.all_1082)}s#############")
        logger.info(f"#############最大发出车辆公告时间{np.max(self.all_1082)}s#############")
        logger.info(f"#############最小发出车辆公告时间{np.min(self.all_1082)}s#############")
        logger.info('\n')
        logger.info(f"#############_功能寻址下获取1181退出boot后第一条车辆公告发出时间测试{test_count}次#############")
        logger.info(f"#############平均发出车辆公告时间{np.mean(self.all_1181)}s#############")
        logger.info(f"#############最大发出车辆公告时间{np.max(self.all_1181)}s#############")
        logger.info(f"#############最小发出车辆公告时间{np.min(self.all_1181)}s#############")
        logger.info('\n')
        logger.info(f"#############_功能寻址下获取刷写boot_1181退出boot后第一条车辆公告发出时间测试{test_count_flash_boot}次#############")
        logger.info(f"#############平均发出车辆公告时间{np.mean(self.all_1181_flash_boot)}s#############")
        logger.info(f"#############最大发出车辆公告时间{np.max(self.all_1181_flash_boot)}s#############")
        logger.info(f"#############最小发出车辆公告时间{np.min(self.all_1181_flash_boot)}s#############")
        logger.info('\n')
        logger.info(f"#############_功能寻址下获取刷写app_1181退出boot后第一条车辆公告发出时间测试{test_count_flash_app}次#############")
        logger.info(f"#############平均发出车辆公告时间{np.mean(self.all_1181_flash_app)}s#############")
        logger.info(f"#############最大发出车辆公告时间{np.max(self.all_1181_flash_app)}s#############")
        logger.info(f"#############最小发出车辆公告时间{np.min(self.all_1181_flash_app)}s#############")
        logger.info('\n')
        logger.info(f"#############_休眠唤醒获取第一条车辆公告发出时间测试{test_count_sleepwakeup}次#############")
        logger.info(f"#############平均发出车辆公告时间{np.mean(self.all_sleepwakeup)}s#############")
        logger.info(f"#############最大发出车辆公告时间{np.max(self.all_sleepwakeup)}s#############")
        logger.info(f"#############最小发出车辆公告时间{np.min(self.all_sleepwakeup)}s#############")

    def exit_boot_vehicle_announcement(self):
        self.sd_tester.update_serverdoipid(0x1001,ecu="BGM")
        self.doipip = 0x1001
        self.ecu = "BGM"
        with allure.step("boot刷写"):
            self.sd_tester.check_program_precondition()
            time.sleep(2)
            self.sd_tester.enter_program_mode()
            time.sleep(10)
            self.sd_tester.confirm_program_mode(self.doipip)
            self.sd_tester.diagnostic_session_check(self.doipip)
            self.sd_tester.infotainment_check(self.doipip)
            time.sleep(2)
            self.sd_tester.unlocK_for_download(self.doipip,ecu=self.ecu)
            self.sd_tester.erase_memory(self.doipip,self.file_path)
            self.sd_tester.request_download(self.doipip,self.file_path,compression_encryption_method=[0x00])
            self.sd_tester.transfer_data(self.doipip,self.file_path)
            self.sd_tester.request_transfer_exit(self.doipip)
            self.sd_tester.transfer_keyinfo(self.doipip,self.keyinfo)
            self.sd_tester.verify_software_integrity(self.doipip)
            self.sd_tester.reset()
            before = time.time()-0.2
        with allure.step("获取1181退出boot后第一条车辆公告发出时间"):
            after = self.sd_tester.wait_vehicle_announcement()
        with allure.step("判断间隔时间是否在20s内"):
            if self.test_flag == "flash_boot":
                global interval_1181_flash_boot
                interval_1181_flash_boot = after - before
                self.all_1181_flash_boot.append(interval_1181_flash_boot)
                logger.info("本次测试:功能寻址下获取刷写boot_1181退出boot后第一条车辆公告发出时间:{}s".format(interval_1181_flash_boot))
            elif self.test_flag == "flash_app":
                global interval_1181_flash_app
                interval_1181_flash_app = after - before
                self.all_1181_flash_app.append(interval_1181_flash_app)
                logger.info("本次测试:功能寻址下获取刷写app_1181退出boot后第一条车辆公告发出时间:{}s".format(interval_1181_flash_app))
        with allure.step("检查BGM_SOC诊断进程是否使能"):
            self.sd_tester.update_serverdoipid(0x1001)
            self.sd_tester.send_data([0x22, 0xF1, 0x86])# 读取会话状态 [0x22, 0xF1, 0x86]
            result = self.sd_tester.return_udsdata_and_check_and_print_response_result()
            assert result[-1] == 0x01, "BGM_SOC诊断进程未使能"
        with allure.step("检查BGM_MCU是否在app下"):
            self.sd_tester.update_serverdoipid(0x1002)
            self.sd_tester.check_mcu_whether_in_boot()

    @pytest.mark.repeat(300)
    @allure.title("车辆公告时间测试")
    def test_caseid_1982068(self):
        global test_count
        test_count += 1
        with allure.step("物理寻址1101复位第一条车辆公告发出时间测试"):         
            with allure.step("物理寻址发送1101"):
                self.sd_tester.update_serverdoipid(0x1002)
                self.sd_tester.send_data([0x11,0x01])
                before = time.time()
            with allure.step("获取1101第一条车辆公告发出时间"):
                after = self.sd_tester.wait_vehicle_announcement()
            with allure.step("判断间隔时间是否在20s内"):
                global interval_1101
                interval_1101 = after - before
                self.all_1101.append(interval_1101) 
                logger.info("本次测试:获取物理寻址1101后第一条车辆公告发出时间:{}s".format(interval_1101))
            with allure.step("检查BGM_SOC诊断进程是否使能"):
                self.sd_tester.update_serverdoipid(0x1001)
                self.sd_tester.send_data([0x22, 0xF1, 0x86])# 读取会话状态 [0x22, 0xF1, 0x86]
                result = self.sd_tester.return_udsdata_and_check_and_print_response_result()
                assert result[-1] == 0x01, "BGM_SOC诊断进程未使能"
            with allure.step("检查BGM_MCU是否在app下"):
                self.sd_tester.update_serverdoipid(0x1002)
                self.sd_tester.check_mcu_whether_in_boot()
            time.sleep(30)

        with allure.step("功能寻址1082进boot第一条车辆公告发出时间测试"):
            with allure.step("功能寻址发送1082"):
                self.sd_tester.update_serverdoipid(0x1FFF)
                self.sd_tester.send_data([0x10,0x82])
                before = time.time()
            with allure.step("获取1082进boot后第一条车辆公告发出时间"):
                after = self.sd_tester.wait_vehicle_announcement()
            with allure.step("判断间隔时间是否在16s内"):
                global interval_1082
                interval_1082 = after - before
                self.all_1082.append(interval_1082)
                logger.info("本次测试:功能寻址下获取1082进boot后第一条车辆公告发出时间:{}s".format(interval_1082))
            with allure.step("检查BGM_SOC诊断进程是否使能"):
                self.sd_tester.update_serverdoipid(0x1001)
                self.sd_tester.send_data([0x22, 0xF1, 0x86])# 读取会话状态 [0x22, 0xF1, 0x86]
                result = self.sd_tester.return_udsdata_and_check_and_print_response_result()
                assert result[-1] == 0x02, "BGM_SOC诊断进程未使能"
            with allure.step("检查BGM_MCU是否在boot下"):
                self.sd_tester.update_serverdoipid(0x1002)
                self.sd_tester.check_mcu_whether_in_boot()

        with allure.step("功能寻址1181退出boot第一条车辆公告发出时间测试"):             
            with allure.step("功能寻址发送1181退出boot"):
                self.sd_tester.update_serverdoipid(0x1FFF)
                self.sd_tester.send_data([0x11,0x81])
                before = time.time()
            with allure.step("获取1181退出boot后第一条车辆公告发出时间"):
                after = self.sd_tester.wait_vehicle_announcement()
            with allure.step("判断间隔时间是否在20s内"):
                global interval_1181
                interval_1181 = after - before
                self.all_1181.append(interval_1181)
                logger.info("本次测试:功能寻址下获取1181退出boot后第一条车辆公告发出时间:{}s".format(interval_1181))
            with allure.step("检查BGM_SOC诊断进程是否使能"):
                self.sd_tester.update_serverdoipid(0x1001)
                self.sd_tester.send_data([0x22, 0xF1, 0x86])# 读取会话状态 [0x22, 0xF1, 0x86]
                result = self.sd_tester.return_udsdata_and_check_and_print_response_result()
                assert result[-1] == 0x01, "BGM_SOC诊断进程未使能"
            with allure.step("检查BGM_MCU是否在app下"):
                self.sd_tester.update_serverdoipid(0x1002)
                self.sd_tester.check_mcu_whether_in_boot()
        
        logger.info(f"#############_物理寻址下获取1101重启后第一条车辆公告发出时间测试{test_count}次#############")
        logger.info(f"#############平均发出车辆公告时间{np.mean(self.all_1101)}s#############")
        logger.info(f"#############最大发出车辆公告时间{np.max(self.all_1101)}s#############")
        logger.info(f"#############最小发出车辆公告时间{np.min(self.all_1101)}s#############")
        logger.info('\n')
        logger.info(f"#############_功能寻址下获取1082进boot后第一条车辆公告发出时间测试{test_count}次#############")
        logger.info(f"#############平均发出车辆公告时间{np.mean(self.all_1082)}s#############")
        logger.info(f"#############最大发出车辆公告时间{np.max(self.all_1082)}s#############")
        logger.info(f"#############最小发出车辆公告时间{np.min(self.all_1082)}s#############")
        logger.info('\n')
        logger.info(f"#############_功能寻址下获取1181退出boot后第一条车辆公告发出时间测试{test_count}次#############")
        logger.info(f"#############平均发出车辆公告时间{np.mean(self.all_1181)}s#############")
        logger.info(f"#############最大发出车辆公告时间{np.max(self.all_1181)}s#############")
        logger.info(f"#############最小发出车辆公告时间{np.min(self.all_1181)}s#############")
        logger.info('\n')
        
        with allure.step("判断物理寻址下获取1101重启后第一条车辆公告发出时间间隔时间是否在20s内"):
            assert interval_1101 < 20 , '物理寻址下获取1101重启后第一条车辆公告发出时间大于20s'   
        with allure.step("判断功能寻址下获取1082进boot后第一条车辆公告发出时间间隔时间是否在16s内"):
            assert interval_1082 < 16 , '功能寻址下获取1082进boot后第一条车辆公告发出时间大于16s'
        with allure.step("判断功能寻址下获取1181退出boot后第一条车辆公告发出时间间隔时间是否在20s内"):
            assert interval_1181 < 20 , '功能寻址下获取1181退出boot后第一条车辆公告发出时间大于20s'

    @pytest.mark.repeat(50)
    @allure.title("刷写boot_1181退出boot车辆公告时间测试")
    def test_caseid_刷写boot_1181退出boot车辆公告时间测试(self):
        global test_count_flash_boot
        test_count_flash_boot += 1
        with allure.step("刷写boot_1181退出boot车辆公告时间测试"):
            self.test_flag = "flash_boot"
            self.keyinfo = __import__("os").environ['XAT_CREDENTIAL_SCAN_074E96C9B0F7C658CEC7'] 
            self.file_url = "https://repo.jidudev.com/artifactory/BGMSoftware/Release/v2.2.0/6160110220AD/2960110205AA.bin"
            self.file_path = self.sd_tester.flashimage_download(self.file_url)
            self.exit_boot_vehicle_announcement()

            logger.info(f"#############_功能寻址下获取刷写boot_1181退出boot后第一条车辆公告发出时间测试{test_count_flash_boot}次#############")
            logger.info(f"#############平均发出车辆公告时间{np.mean(self.all_1181_flash_boot)}s#############")
            logger.info(f"#############最大发出车辆公告时间{np.max(self.all_1181_flash_boot)}s#############")
            logger.info(f"#############最小发出车辆公告时间{np.min(self.all_1181_flash_boot)}s#############")
            logger.info('\n')

        with allure.step("判断功能寻址下获取刷写boot_1181退出boot后第一条车辆公告发出时间间隔时间是否在20s内"):
            assert interval_1181_flash_boot < 20 , '功能寻址下获取1082进boot后第一条车辆公告发出时间大于20s'

    @pytest.mark.repeat(1)
    @allure.title("刷写app_1181退出boot车辆公告时间测试")
    def test_caseid_刷写_app_1181退出boot车辆公告时间测试(self):
        global test_count_flash_app
        test_count_flash_app += 1
        with allure.step("刷写app_1181退出boot车辆公告时间测试"):
            self.test_flag = "flash_app"
            self.keyinfo = __import__("os").environ['XAT_CREDENTIAL_SCAN_9BFC7C20C880A2061278'] 
            self.file_url = "https://repo.jidudev.com/artifactory/BGMSoftware/Release/v3.0.0/6160110300AJ/6160110300AJ.bin"
            self.file_path = self.sd_tester.flashimage_download(self.file_url)
            self.exit_boot_vehicle_announcement()

            logger.info(f"#############_功能寻址下获取刷写app_1181退出boot后第一条车辆公告发出时间测试{test_count_flash_app}次#############")
            logger.info(f"#############平均发出车辆公告时间{np.mean(self.all_1181_flash_app)}s#############")
            logger.info(f"#############最大发出车辆公告时间{np.max(self.all_1181_flash_app)}s#############")
            logger.info(f"#############最小发出车辆公告时间{np.min(self.all_1181_flash_app)}s#############")   
        
        with allure.step("判断功能寻址下获取刷写app_1181退出boot后第一条车辆公告发出时间间隔时间是否在20s内"):
            assert interval_1181_flash_app < 20 , '功能寻址下获取1181退出boot后第一条车辆公告发出时间大于20s'

    @pytest.mark.repeat(20)
    @allure.title("休眠唤醒车辆公告时间测试")
    def test_caseid_休眠唤醒车辆公告时间测试(self):
        global test_count_sleepwakeup
        test_count_sleepwakeup += 1
        with allure.step(f"BGM休眠"):
            self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
            self.mix.network_sleep()
        with allure.step(f"诊断激活线唤醒BGM"):
                    logger.info("诊断激活线唤醒BGM")
                    self.io.bgm_diag_line_up()
        before = time.time()
        with allure.step("BGM唤醒后第一条车辆公告发出时间"):
            after = self.sd_tester.wait_vehicle_announcement()
        with allure.step("判断间隔时间是否在16s内"):
            global interval_sleepwakeup
            interval_sleepwakeup = after - before
            self.all_sleepwakeup.append(interval_sleepwakeup)
            logger.info("本次测试:休眠唤醒后获取第一条车辆公告发出时间:{}s".format(interval_sleepwakeup))

        with allure.step("判断休眠唤醒获取第一条车辆公告发出时间间隔时间是否在16s内"):
            assert interval_sleepwakeup < 16 , '休眠唤醒获取第一条车辆公告发出时间大于16s'

#cd /root/wenyu.liang/sat/xat_cases/legacy/basetech/bgm
#nohup pytest stress/test_vechicle_announcement_time.py --disable_partner='true'
