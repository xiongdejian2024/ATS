# -*- coding: utf-8 -*-
"""
@File        : test_flash_bgm_reverse_test.py
@Author      : xiaoqiang.hu@jiduauto.com
@Time        : 2024/8/14
@Description :

"""
import pytest
import allure
import sys, os

from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.sdk.sdk_tools import *
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
import threading
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH

flash_count=0

class TestBgm(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.sd_tester.update_serverdoipid(0x1001,ecu="BGM")
        self.doipip = 0x1001
        self.ecu = "BGM"
        self.keyinfo = __import__("os").environ['XAT_CREDENTIAL_SCAN_83D7B503FC8B6E9DCFDD'] 
        self.file_url = "https://repo.jidudev.com/artifactory/BGMSoftware/Release/v2.1.0/6160110210AO/6160110210AO.bin"
        self.file_path = self.sd_tester.flashimage_download(self.file_url)
        self.flashtime = [114,558,674]#传包时间，安装时间，刷写总时间
        self.resettime_tcam = 180#重启时间
        self.resettime_bgm = 30#重启时间
        

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        logger.info("Test running ...")
        #BGM_SSH().init_bgm_tcpdump()#推送tcpdump抓包工具，并初始化抓包工具
        self.sff = SniffPacket(iface='169.254.1.200')    
        self.sff.set_save_name('诊断升级')# 设置抓包保存名字，可以不设置，有默认值，保存的文件都会带有时间    
        self.sff.start_sniff()# 开启抓包

        with allure.step("仿真车速为0km/h,VehSpdQf=2"):
            self.bus_comm.set_vehspd_and_qf(0,VehSpdQf(2))
            self.bus_comm.get_vehicle_speed()
        with allure.step("切换UsageMode为inactive"):
            self.bus_comm.set('backbonefr','BcmVddmBackBoneFr00','VehMtnStVehMtnSt','VehMtnSt2_StandStillVal3')
            self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        with allure.step("切换EpbStsEpbSts为EpbSts_AllAppld"):    
            self.bus_comm.set('backbonefr','BcmVddmBackBoneFr00','EpbStsEpbSts','EpbSts_AllAppld')
        time.sleep(2)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        self.sff.stop_sniff()#  停止抓包
        logger.info("Test ending ...")
    
    def after_class(self, ecu):
        super().after_class(self, ecu)

    def random_power_off(self,flashtime:int):
        if self.ecu == "TCAM":
            randomtime = random.randint(10, flashtime)
            logger.info(f"{randomtime}s之后,执行断电操作")
            sleep(randomtime)
            logger.info(f"执行断电操作")
            self.io.tcam_power_off()
        elif self.ecu == "BGM":
            randomtime = random.randint(10, flashtime)
            logger.info(f"{randomtime}s之后,执行断电操作")
            sleep(randomtime)
            logger.info(f"执行断电操作")
            self.io.bgm_power_off()
    
    @pytest.mark.full
    @allure.title("刷写异常测试_车速满足但E2E失效_CRC校验错误")
    def test_caseid_1990757(self):
        with allure.step("仿真车速为0km/h,VehSpdQf=2"):
            self.bus_comm.ipdu.restore_crc(self.bus_comm.ipdu.backbonefr.BcmVddmBackBoneFr06,'VehSpdLgtChks')
            self.bus_comm.ipdu.set_no_crc(self.bus_comm.ipdu.backbonefr.BcmVddmBackBoneFr06,'VehSpdLgtCntr')
            self.bus_comm.set_vehspd_and_qf(0,VehSpdQf(2))
            self.bus_comm.get_vehicle_speed()
        time.sleep(2)
        with allure.step("刷写前置条件校验"):
            self.sd_tester.send_data_and_check(TA.FUNCTION,[0x31,0x01,0x02,0x06],{'10 01':'710102061001','10 02':'710102061002'})
        self.bus_comm.ipdu.restore_crc(self.bus_comm.ipdu.backbonefr.BcmVddmBackBoneFr06,'VehSpdLgtCntr')
        
    @pytest.mark.smoke    
    @allure.title("刷写正常测试_usagemode_active")
    def test_caseid_1990768(self,do_assert:bool=True):
        with allure.step("切换UsageMode为active"):
            self.bus_comm.set('backbonefr','BcmVddmBackBoneFr00','VehMtnStVehMtnSt','VehMtnSt2_StandStillVal3')
            self.sd_tester.change_usage_mode(UsageMode.ACTIVE)                 
        time.sleep(2)
        with allure.step("刷写前置条件校验"):
            self.sd_tester.send_data_and_check(TA.FUNCTION,[0x31,0x01,0x02,0x06],{'10 01':'710102061001','10 02':'710102061001'})

    @pytest.mark.full 
    @allure.title("刷写正常测试_usagemode_Convenience")
    def test_caseid_1990767(self):
        with allure.step("切换UsageMode为Convenience"):
            self.bus_comm.set('backbonefr','BcmVddmBackBoneFr00','VehMtnStVehMtnSt','VehMtnSt2_StandStillVal3')
            self.sd_tester.change_usage_mode(UsageMode.CONVENIENCE)
        time.sleep(2)
        with allure.step("刷写前置条件校验"):
            self.sd_tester.send_data_and_check(TA.FUNCTION,[0x31,0x01,0x02,0x06],{'10 01':'710102061001','10 02':'710102061001'})
    
    @pytest.mark.full
    @allure.title("刷写正常测试_usagemode_inactive")
    def test_caseid_1990766(self):
        with allure.step("切换UsageMode为inactive"):
            self.bus_comm.set('backbonefr','BcmVddmBackBoneFr00','VehMtnStVehMtnSt','VehMtnSt2_StandStillVal3')
            self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        time.sleep(2)
        with allure.step("刷写前置条件校验"):
            self.sd_tester.send_data_and_check(TA.FUNCTION,[0x31,0x01,0x02,0x06],{'10 01':'710102061001','10 02':'710102061001'})
       
    @pytest.mark.sanity  
    @allure.title("刷写正常测试_usagemode_Abandoned")
    def test_caseid_1990765(self):
        with allure.step("切换UsageMode为Abandoned"):
            self.bus_comm.set('backbonefr','BcmVddmBackBoneFr00','VehMtnStVehMtnSt','VehMtnSt2_StandStillVal3')
            self.sd_tester.change_usage_mode(UsageMode.ABANDONED)
        time.sleep(2)
        with allure.step("刷写前置条件校验"):
            self.sd_tester.send_data_and_check(TA.FUNCTION,[0x31,0x01,0x02,0x06],{'10 01':'710102061001','10 02':'710102061001'})
       
    # @allure.title("刷写正常测试_usagemode_Undefined")
    # def test_caseid_1990764(self):
    #     with allure.step("切换UsageMode为Undefined"):
    #         self.bus_comm.set('backbonefr','BcmVddmBackBoneFr00','VehMtnStVehMtnSt','VehMtnSt2_StandStillVal3')
    #         self.sd_tester.change_usage_mode(UsageMode.)
    #     with allure.step("刷写前置条件校验"):
    #         self.sd_tester.send_data_and_check(TA.FUNCTION,[0x31,0x01,0x02,0x06],{'10 11':'710102061001'})
       
    @pytest.mark.sanity 
    @allure.title("刷写正常测试_usagemode_Driving")
    def test_caseid_1990758(self):
        with allure.step("切换UsageMode为Driving"):
            self.bus_comm.set('backbonefr','BcmVddmBackBoneFr00','VehMtnStVehMtnSt','VehMtnSt2_StandStillVal3')
            self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        time.sleep(2)
        with allure.step("刷写前置条件校验"):
            self.sd_tester.send_data_and_check(TA.FUNCTION,[0x31,0x01,0x02,0x06],{'10 01':'710102061002','10 02':'710102061002'})

    @pytest.mark.full  
    @allure.title("刷写正常测试_车速为0")
    def test_caseid_1990763(self):
        with allure.step("仿真车速为0km/h"):
            self.bus_comm.set_vehspd_and_qf(0,VehSpdQf(2))
            self.bus_comm.get_vehicle_speed()
        with allure.step("刷写前置条件校验"):
            self.sd_tester.send_data_and_check(TA.FUNCTION,[0x31,0x01,0x02,0x06],{'10 01':'710102061001','10 02':'710102061001'})

    @pytest.mark.full 
    @allure.title("刷写正常测试_车速为1km/h")
    def test_caseid_1990762(self):
        with allure.step("仿真车速为1km/h"):
            self.bus_comm.set_vehspd_and_qf(256,VehSpdQf(2))
            self.bus_comm.get_vehicle_speed()
        with allure.step("刷写前置条件校验"):
            self.sd_tester.send_data_and_check(TA.FUNCTION,[0x31,0x01,0x02,0x06],{'10 01':'710102061001','10 02':'710102061001'})

    @pytest.mark.smoke   
    @allure.title("刷写正常测试_车速为2km/h")
    def test_caseid_1990761(self):
        with allure.step("仿真车速为2km/h"):
            self.bus_comm.set_vehspd_and_qf(512,VehSpdQf(2))
            self.bus_comm.get_vehicle_speed()
        with allure.step("刷写前置条件校验"):
            self.sd_tester.send_data_and_check(TA.FUNCTION,[0x31,0x01,0x02,0x06],{'10 01':'710102061001','10 02':'710102061001'})

    @pytest.mark.full  
    @allure.title("刷写正常测试_车速为3km/h")
    def test_caseid_1990756(self):
        with allure.step("仿真车速为3km/h"):
            self.bus_comm.set_vehspd_and_qf(770,VehSpdQf(2))
            self.bus_comm.get_vehicle_speed()
        with allure.step("刷写前置条件校验"):
            self.sd_tester.send_data_and_check(TA.FUNCTION,[0x31,0x01,0x02,0x06],{'10 01':'710102061002','10 02':'710102061002'})

    @pytest.mark.full  
    @allure.title("刷写正常测试_车速为4km/h")
    def test_caseid_1990755(self):
        with allure.step("仿真车速为4km/h"):
            self.bus_comm.set_vehspd_and_qf(1023,VehSpdQf(2))
            self.bus_comm.get_vehicle_speed()
        with allure.step("刷写前置条件校验"):
            self.sd_tester.send_data_and_check(TA.FUNCTION,[0x31,0x01,0x02,0x06],{'10 01':'710102061002','10 02':'710102061002'})

    @pytest.mark.sanity  
    @allure.title("刷写异常测试_VehSpdLgtQf=0")
    def test_caseid_1990754(self):
        with allure.step("仿真车速VehSpdQf=0"):
            self.bus_comm.set_vehspd_and_qf(0,VehSpdQf(0))
            self.bus_comm.get_vehicle_speed()
        with allure.step("刷写前置条件校验"):
            self.sd_tester.send_data_and_check(TA.FUNCTION,[0x31,0x01,0x02,0x06],{'10 01':'710102061002','10 02':'710102061002'})

    @pytest.mark.sanity 
    @allure.title("刷写异常测试_VehSpdLgtQf=1")
    def test_caseid_1990753(self):
        with allure.step("仿真车速VehSpdQf=1"):
            self.bus_comm.set_vehspd_and_qf(0,VehSpdQf(1))
            self.bus_comm.get_vehicle_speed()
        with allure.step("刷写前置条件校验"):
            self.sd_tester.send_data_and_check(TA.FUNCTION,[0x31,0x01,0x02,0x06],{'10 01':'710102061002','10 02':'710102061002'})
    
    @pytest.mark.sanity
    @allure.title("刷写异常测试_EpbStsEpbSts的值为00")
    def test_caseid_1990752(self):
        with allure.step("仿真EpbStsEpbSts=0x00"):
            self.bus_comm.set('backbonefr','BcmVddmBackBoneFr00','EpbStsEpbSts','EpbSts_Resd0')
        with allure.step("刷写前置条件校验"):
            self.sd_tester.send_data_and_check(TA.FUNCTION,[0x31,0x01,0x02,0x06],{'10 01':'710102061001','10 02':'710102061002'})
    
    @pytest.mark.full 
    @allure.title("刷写异常测试_EpbStsEpbSts的值为05")
    def test_caseid_1990751(self):
        with allure.step("仿真EpbStsEpbSts=0x05"):
            self.bus_comm.set('backbonefr','BcmVddmBackBoneFr00','EpbStsEpbSts','EpbSts_AllInTran')
        with allure.step("刷写前置条件校验"):
            self.sd_tester.send_data_and_check(TA.FUNCTION,[0x31,0x01,0x02,0x06],{'10 01':'710102061001','10 02':'710102061002'})
    
    @pytest.mark.full 
    @allure.title("刷写异常测试_EpbStsEpbSts的值为06")
    def test_caseid_1990750(self):
        with allure.step("仿真EpbStsEpbSts=0x06"):
            self.bus_comm.set('backbonefr','BcmVddmBackBoneFr00','EpbStsEpbSts','EpbSts_BrkgDynByActr')
        with allure.step("刷写前置条件校验"):
            self.sd_tester.send_data_and_check(TA.FUNCTION,[0x31,0x01,0x02,0x06],{'10 01':'710102061001','10 02':'710102061002'})
    
    @pytest.mark.full 
    @allure.title("刷写异常测试_EpbStsEpbSts的值为09")
    def test_caseid_1990749(self):
        with allure.step("仿真EpbStsEpbSts=0x09"):
            self.bus_comm.set('backbonefr','BcmVddmBackBoneFr00','EpbStsEpbSts','EpbSts_ActrAllReld')
        with allure.step("刷写前置条件校验"):
            self.sd_tester.send_data_and_check(TA.FUNCTION,[0x31,0x01,0x02,0x06],{'10 01':'710102061001','10 02':'710102061002'})
    
    @pytest.mark.full 
    @allure.title("刷写异常测试_EpbStsEpbSts的值为0A")
    def test_caseid_1990748(self):
        with allure.step("仿真EpbStsEpbSts=0x0A"):
            self.bus_comm.set('backbonefr','BcmVddmBackBoneFr00','EpbStsEpbSts','EpbSts_BrkgDynDegraded')
        with allure.step("刷写前置条件校验"):
            self.sd_tester.send_data_and_check(TA.FUNCTION,[0x31,0x01,0x02,0x06],{'10 01':'710102061001','10 02':'710102061002'})
    
    @pytest.mark.full 
    @allure.title("刷写异常测试_EpbStsEpbSts的值为0B")
    def test_caseid_1990747(self):
        with allure.step("仿真EpbStsEpbSts=0x0B"):
            self.bus_comm.set('backbonefr','BcmVddmBackBoneFr00','EpbStsEpbSts','EpbSts_Resd11')
        with allure.step("刷写前置条件校验"):
            self.sd_tester.send_data_and_check(TA.FUNCTION,[0x31,0x01,0x02,0x06],{'10 01':'710102061001','10 02':'710102061002'})
    
    @pytest.mark.full 
    @allure.title("刷写异常测试_跳过擦除内存测试")
    def test_caseid_1990743(self):
        try:
            self.sd_tester.check_program_precondition()
            time.sleep(2)
            self.sd_tester.enter_program_mode()
            time.sleep(10)#确保1082发送成功，进入reset状态
            self.sd_tester.confirm_program_mode(self.doipip)
            self.sd_tester.diagnostic_session_check(self.doipip)
            self.sd_tester.infotainment_check(self.doipip)
            time.sleep(2)
            self.sd_tester.unlocK_for_download(self.doipip,ecu=self.ecu)
            self.sd_tester.request_download(self.doipip,self.file_path,compression_encryption_method=[0x00])
            self.sd_tester.transfer_data(self.doipip,self.file_path,usr_block_length=1000000000)
            self.sd_tester.request_transfer_exit(self.doipip)
            self.sd_tester.transfer_keyinfo(self.doipip,self.keyinfo)
            self.sd_tester.verify_software_integrity(self.doipip)
        except Exception as e:
            logger.info("==================== reverse test Error ==========================")
            logger.error(e)
            self.sd_tester.reset()
            self.sff.stop_sniff()#  停止抓包
            time.sleep(self.resettime_bgm)
            result = 0
            assert result, " reverse test >>>>>>>>>>>>>>>>  Failed"
            
        self.sd_tester.reset()
        self.sff.stop_sniff()#  停止抓包
        time.sleep(self.resettime_bgm)
     
    @pytest.mark.full 
    @allure.title("刷写异常测试_跳过请求下载测试")
    def test_caseid_1990742(self):
        try:
            self.sd_tester.check_program_precondition()
            time.sleep(2)
            self.sd_tester.enter_program_mode()
            time.sleep(10)#确保1082发送成功，进入reset状态
            self.sd_tester.confirm_program_mode(self.doipip)
            self.sd_tester.diagnostic_session_check(self.doipip)
            self.sd_tester.infotainment_check(self.doipip)
            time.sleep(2)
            self.sd_tester.unlocK_for_download(self.doipip,ecu=self.ecu)
            self.sd_tester.erase_memory(self.doipip,self.file_path)
            self.sd_tester.request_download(self.doipip,self.file_path,compression_encryption_method=[0x00],reverse_test_type = "skip_request_download")
            self.sd_tester.transfer_data(self.doipip,self.file_path,usr_block_length=1000000000,reverse_test_type = "skip_request_download")
        except Exception as e:
            logger.info("==================== reverse test Error ==========================")
            logger.error(e)
            self.sd_tester.reset()
            self.sff.stop_sniff()#  停止抓包
            time.sleep(self.resettime_bgm)
            result = 0
            assert result, " reverse test >>>>>>>>>>>>>>>>  Failed"
        
        self.sd_tester.reset()
        self.sff.stop_sniff()#  停止抓包
        time.sleep(self.resettime_bgm)
        self.sd_tester.upgrade_ecu(self.ecu,self.doipip,self.keyinfo,self.file_url,standard=True,check_data=None,skip_step=[0],offline=True,save_packet=True,sniff_packet=True,save_path='.')

    @pytest.mark.full 
    @allure.title("刷写异常测试_包未传完请求退出")
    def test_caseid_1990741(self):
        try:
            self.sd_tester.check_program_precondition()
            time.sleep(2)
            self.sd_tester.enter_program_mode()
            time.sleep(10)#确保1082发送成功，进入reset状态
            self.sd_tester.confirm_program_mode(self.doipip)
            self.sd_tester.diagnostic_session_check(self.doipip)
            self.sd_tester.infotainment_check(self.doipip)
            time.sleep(2)
            self.sd_tester.unlocK_for_download(self.doipip,ecu=self.ecu)
            self.sd_tester.erase_memory(self.doipip,self.file_path)
            self.sd_tester.request_download(self.doipip,self.file_path,compression_encryption_method=[0x00])
            self.sd_tester.transfer_data(self.doipip,self.file_path,reverse_test_type = "跳过一段数据传输")
            self.sd_tester.request_transfer_exit(self.doipip,reverse_test_type = "skip_transfer_data")
            
        except Exception as e:
            logger.info("==================== reverse test Error ==========================")
            logger.error(e)
            self.sd_tester.reset()
            self.sff.stop_sniff()#  停止抓包
            time.sleep(self.resettime_bgm)
            result = 0
            assert result, " reverse test >>>>>>>>>>>>>>>>  Failed"
        
        self.sd_tester.reset()
        self.sff.stop_sniff()#  停止抓包
        time.sleep(self.resettime_bgm)
        self.sd_tester.upgrade_ecu(self.ecu,self.doipip,self.keyinfo,self.file_url,standard=True,check_data=None,skip_step=[0],offline=True,save_packet=True,sniff_packet=True,save_path='.')

    @pytest.mark.full
    @allure.title("刷写异常测试_跳过数据传输测试")
    #测试结果失败，期望是7F3724或72实际是7F3731
    #SOA是问题不解决：https://jira.jiduauto.com/browse/SOA-27814
    def test_caseid_1990739(self):
        try:
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
            self.sd_tester.request_download(self.doipip,self.file_path,compression_encryption_method=[0x00],reverse_test_type = "skip_transfer_data")
            self.sd_tester.request_transfer_exit(self.doipip,reverse_test_type = "skip_transfer_data")
        except Exception as e:
            logger.info("==================== reverse test Error ==========================")
            logger.error(e)
            self.sd_tester.reset()
            self.sff.stop_sniff()#  停止抓包
            time.sleep(self.resettime_bgm)
            result = 0
            assert result, " reverse test >>>>>>>>>>>>>>>>  Failed"
        
        self.sd_tester.reset()
        self.sff.stop_sniff()#  停止抓包
        time.sleep(self.resettime_bgm)
        self.sd_tester.upgrade_ecu(self.ecu,self.doipip,self.keyinfo,self.file_url,standard=True,check_data=None,skip_step=[0],offline=True,save_packet=True,sniff_packet=True,save_path='.')
  
    @pytest.mark.full
    @allure.title("刷写异常测试_跳过请求退出数据传输测试")
    def test_caseid_1993527(self):
        try:
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
            self.sd_tester.transfer_keyinfo(self.doipip,self.keyinfo,reverse_test_type = "skip_request_transfer_exit")
        except Exception as e:
            logger.info("==================== reverse test Error ==========================")
            logger.error(e)
            self.sd_tester.reset()
            self.sff.stop_sniff()#  停止抓包
            time.sleep(self.resettime_bgm)
            result = 0
            assert result, " reverse test >>>>>>>>>>>>>>>>  Failed"
        
        self.sd_tester.reset()
        self.sff.stop_sniff()#  停止抓包
        time.sleep(self.resettime_bgm)
        self.sd_tester.upgrade_ecu(self.ecu,self.doipip,self.keyinfo,self.file_url,standard=True,check_data=None,skip_step=[0],offline=True,save_packet=True,sniff_packet=True,save_path='.')
    
    @pytest.mark.full
    @allure.title("刷写异常测试_跳过完整性校验测试")
    def test_caseid_1990738(self):
        try:
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
        except Exception as e:
            logger.info("==================== reverse test Error ==========================")
            logger.error(e)
            self.sd_tester.reset()
            self.sff.stop_sniff()#  停止抓包
            time.sleep(self.resettime_bgm)
            result = 0
            assert result, " reverse test >>>>>>>>>>>>>>>>  Failed"
        
        self.sd_tester.reset()
        self.sff.stop_sniff()#  停止抓包
        time.sleep(self.resettime_bgm)
        self.sd_tester.upgrade_ecu(self.ecu,self.doipip,self.keyinfo,self.file_url,standard=True,check_data=None,skip_step=[0],offline=True,save_packet=True,sniff_packet=True,save_path='.')
    
    @pytest.mark.full
    @allure.title("刷写异常测试_传包完成后重启测试")
    def test_caseid_1990737(self):
        try:
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
            self.sd_tester.reset()
            self.sff.stop_sniff()#  停止抓包
            time.sleep(self.resettime_bgm)
        except Exception as e:
            logger.info("==================== reverse test Error ==========================")
            logger.error(e)
            self.sd_tester.reset()           
            self.sff.stop_sniff()#  停止抓包
            time.sleep(self.resettime_bgm)
            result = 0
            assert result, " reverse test >>>>>>>>>>>>>>>>  Failed"

        self.sd_tester.upgrade_ecu(self.ecu,self.doipip,self.keyinfo,self.file_url,standard=True,check_data=None,skip_step=[0],offline=True,save_packet=True,sniff_packet=True,save_path='.')

    @pytest.mark.full
    @allure.title("刷写异常测试_只传输一个数据块")
    def test_caseid_1990746(self):
        try:
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
            self.sd_tester.transfer_data(self.doipip,self.file_path,reverse_test_type = "只传输一个数据块")
        except Exception as e:
            logger.info("==================== reverse test Error ==========================")
            logger.error(e)
            self.sd_tester.reset()
            self.sff.stop_sniff()#  停止抓包
            time.sleep(self.resettime_bgm)
            result = 0
            assert result, " reverse test >>>>>>>>>>>>>>>>  Failed"
        
        self.sd_tester.reset()
        self.sff.stop_sniff()#  停止抓包
        time.sleep(self.resettime_bgm)
        self.sd_tester.upgrade_ecu(self.ecu,self.doipip,self.keyinfo,self.file_url,standard=True,check_data=None,skip_step=[0],offline=True,save_packet=True,sniff_packet=True,save_path='.')

    @pytest.mark.full
    @allure.title("刷写异常测试_重复传一帧数据")
    def test_caseid_1990734(self):  
        try:
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
            self.sd_tester.transfer_data(self.doipip,self.file_path,reverse_test_type = "重复传一帧数据")
            self.sd_tester.request_transfer_exit(self.doipip)
            self.sd_tester.transfer_keyinfo(self.doipip,self.keyinfo)
            self.sd_tester.verify_software_integrity(self.doipip)
        except Exception as e:
            logger.info("==================== reverse test Error ==========================")
            logger.error(e)
            self.sd_tester.reset()
            self.sff.stop_sniff()#  停止抓包
            time.sleep(self.resettime_bgm)
            result = 0
            assert result, " reverse test >>>>>>>>>>>>>>>>  Failed"
        
        self.sd_tester.reset()
        self.sff.stop_sniff()#  停止抓包
        time.sleep(self.resettime_bgm)
        
    @pytest.mark.full
    @allure.title("刷写异常测试_传包过程36的blockindex序号错误")
    def test_caseid_1990740(self): 
        try:
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
            self.sd_tester.transfer_data(self.doipip,self.file_path,reverse_test_type = "传包过程36的blockindex序号错误")
        except Exception as e:
            logger.info("==================== reverse test Error ==========================")
            logger.error(e)
            self.sd_tester.reset()
            self.sff.stop_sniff()#  停止抓包
            time.sleep(self.resettime_bgm)
            result = 0
            assert result, " reverse test >>>>>>>>>>>>>>>>  Failed"
        
        self.sd_tester.reset()
        self.sff.stop_sniff()#  停止抓包
        time.sleep(self.resettime_bgm)
        self.sd_tester.upgrade_ecu(self.ecu,self.doipip,self.keyinfo,self.file_url,standard=True,check_data=None,skip_step=[0],offline=True,save_packet=True,sniff_packet=True,save_path='.')

    @pytest.mark.full
    @allure.title("刷写异常测试_重复传一段数据")
    def test_caseid_1990733(self):   
        try:
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
            self.sd_tester.transfer_data(self.doipip,self.file_path,reverse_test_type = "重复传一段数据")
        except Exception as e:
            logger.info("==================== reverse test Error ==========================")
            logger.error(e)
            self.sd_tester.reset()
            self.sff.stop_sniff()#  停止抓包
            time.sleep(self.resettime_bgm)
            result = 0
            assert result, " reverse test >>>>>>>>>>>>>>>>  Failed"
        
        self.sd_tester.reset()
        self.sff.stop_sniff()#  停止抓包
        time.sleep(self.resettime_bgm)
        self.sd_tester.upgrade_ecu(self.ecu,self.doipip,self.keyinfo,self.file_url,standard=True,check_data=None,skip_step=[0],offline=True,save_packet=True,sniff_packet=True,save_path='.')  

    @pytest.mark.full
    @allure.title("刷写异常测试_跳过一段数据传输")
    #测试结果失败，期望是7F3772实际是7F3731
    #SOA是问题不解决：https://jira.jiduauto.com/browse/SOA-27815
    def test_caseid_1990736(self): 
        try:
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
            self.sd_tester.transfer_data(self.doipip,self.file_path,reverse_test_type = "跳过一段数据传输")
            self.sd_tester.request_transfer_exit(self.doipip,reverse_test_type = "跳过一段数据传输")
        except Exception as e:
            logger.info("==================== reverse test Error ==========================")
            logger.error(e)
            self.sd_tester.reset()
            self.sff.stop_sniff()#  停止抓包
            time.sleep(self.resettime_bgm)
            result = 0
            assert result, " reverse test >>>>>>>>>>>>>>>>  Failed"
        
        self.sd_tester.reset()
        self.sff.stop_sniff()#  停止抓包
        time.sleep(self.resettime_bgm)
        self.sd_tester.upgrade_ecu(self.ecu,self.doipip,self.keyinfo,self.file_url,standard=True,check_data=None,skip_step=[0],offline=True,save_packet=True,sniff_packet=True,save_path='.')  

    @pytest.mark.full
    @allure.title("刷写异常测试_正常刷写完成不进行重启")
    def test_caseid_1993528(self): 
        try:
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
            self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0x02, 0x06], recv=[0x7F, 0x31, 0x31])#跳过刷新流程的复位，直接进行下一轮刷写的前置条件校验
            #self.sd_tester.check_program_precondition(reverse_test_type = "上次刷写未进行复位")#跳过刷新流程的复位，直接进行下一轮刷写的前置条件校验
        except Exception as e:
            logger.info("==================== reverse test Error ==========================")
            logger.error(e)
            self.sd_tester.reset()
            self.sff.stop_sniff()#  停止抓包
            time.sleep(self.resettime_bgm)
            result = 0
            assert result, " reverse test >>>>>>>>>>>>>>>>  Failed"
        
        self.sd_tester.reset()
        self.sff.stop_sniff()#  停止抓包
        time.sleep(self.resettime_bgm)
        self.sd_tester.upgrade_ecu(self.ecu,self.doipip,self.keyinfo,self.file_url,standard=True,check_data=None,skip_step=[0],offline=True,save_packet=True,sniff_packet=True,save_path='.')  

    @pytest.mark.full
    @allure.title("刷写异常测试_keyinfo的长度不对")
    #测试结果失败，期望是710102081001实际是7F3113
    #需求中0208无例程失败的校验，修改用例 https://jira.jiduauto.com/browse/SOA-27817
    def test_caseid_1990718(self): 
        try:
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
            self.sd_tester.transfer_keyinfo(self.doipip,self.keyinfo,reverse_test_type = "keyinfo的长度错误")
        except Exception as e:
            logger.info("==================== reverse test Error ==========================")
            logger.error(e)
            self.sd_tester.reset()
            self.sff.stop_sniff()#  停止抓包
            time.sleep(self.resettime_bgm)
            result = 0
            assert result, " reverse test >>>>>>>>>>>>>>>>  Failed"
        
        self.sd_tester.reset()
        self.sff.stop_sniff()#  停止抓包
        time.sleep(self.resettime_bgm)
        self.sd_tester.upgrade_ecu(self.ecu,self.doipip,self.keyinfo,self.file_url,standard=True,check_data=None,skip_step=[0],offline=True,save_packet=True,sniff_packet=True,save_path='.')         

    @pytest.mark.full
    @allure.title("刷写异常测试_keyinfo内容错误")
    def test_caseid_1990719(self): 
        try:
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
            self.sd_tester.transfer_keyinfo(self.doipip,self.keyinfo,reverse_test_type = "keyinfo的内容错误")
            self.sd_tester.verify_software_integrity(self.doipip,reverse_test_type = "keyinfo的内容错误")
        except Exception as e:
            logger.info("==================== reverse test Error ==========================")
            logger.error(e)
            self.sd_tester.reset()
            self.sff.stop_sniff()#  停止抓包
            time.sleep(self.resettime_bgm)
            result = 0
            assert result, " reverse test >>>>>>>>>>>>>>>>  Failed"
        
        self.sd_tester.reset()
        self.sff.stop_sniff()#  停止抓包
        time.sleep(self.resettime_bgm)
        self.sd_tester.upgrade_ecu(self.ecu,self.doipip,self.keyinfo,self.file_url,standard=True,check_data=None,skip_step=[0],offline=True,save_packet=True,sniff_packet=True,save_path='.')         
   
    @pytest.mark.full
    @allure.title("刷写异常测试_错误的包")#测试结果失败，期望是710102051000000001实际是710102051000000022
    def test_caseid_1990720(self): 
        try:
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
            self.sd_tester.transfer_data(self.doipip,self.file_path,reverse_test_type = "错误的包")
            self.sd_tester.request_transfer_exit(self.doipip)
            self.sd_tester.transfer_keyinfo(self.doipip,self.keyinfo)
            self.sd_tester.verify_software_integrity(self.doipip,reverse_test_type = "错误的包")
        except Exception as e:
            logger.info("==================== reverse test Error ==========================")
            logger.error(e)
            self.sd_tester.reset()
            self.sff.stop_sniff()#  停止抓包
            time.sleep(self.resettime_bgm)
            result = 0
            assert result, " reverse test >>>>>>>>>>>>>>>>  Failed"
        
        self.sd_tester.reset()
        self.sff.stop_sniff()#  停止抓包
        time.sleep(self.resettime_bgm)
        self.sd_tester.upgrade_ecu(self.ecu,self.doipip,self.keyinfo,self.file_url,standard=True,check_data=None,skip_step=[0],offline=True,save_packet=True,sniff_packet=True,save_path='.')         

    @pytest.mark.full
    @allure.title("刷写异常测试_传输块小于最大允许的数据块长度")
    def test_caseid_1990744(self):
        try:
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
            self.sd_tester.transfer_data(self.doipip,self.file_path,usr_block_length=50000)
            self.sd_tester.request_transfer_exit(self.doipip)
            self.sd_tester.transfer_keyinfo(self.doipip,self.keyinfo)
            self.sd_tester.verify_software_integrity(self.doipip)
        except Exception as e:
            logger.info("==================== reverse test Error ==========================")
            logger.error(e)
            self.sd_tester.reset()
            self.sff.stop_sniff()#  停止抓包
            time.sleep(self.resettime_bgm)
            result = 0
            assert result, " reverse test >>>>>>>>>>>>>>>>  Failed"
        
        self.sd_tester.reset()
        self.sff.stop_sniff()#  停止抓包
        time.sleep(self.resettime_bgm)

    @pytest.mark.full
    @allure.title("刷写异常测试_传输块大于最大允许的数据块长度")
    def test_caseid_1990735(self):
        try:
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
            self.sd_tester.transfer_data(self.doipip,self.file_path,reverse_test_type = "传输块大于最大允许的数据块长度")
        except Exception as e:
            logger.info("==================== reverse test Error ==========================")
            logger.error(e)
            self.sd_tester.reset()
            self.sff.stop_sniff()#  停止抓包
            time.sleep(self.resettime_bgm)
            result = 0
            assert result, " reverse test >>>>>>>>>>>>>>>>  Failed"
        
        self.sd_tester.reset()
        self.sff.stop_sniff()#  停止抓包
        time.sleep(self.resettime_bgm)
        self.sd_tester.upgrade_ecu(self.ecu,self.doipip,self.keyinfo,self.file_url,standard=True,check_data=None,skip_step=[0],offline=True,save_packet=True,sniff_packet=True,save_path='.') 

    @pytest.mark.full
    @allure.title("刷写异常测试_传包过程中异常掉电")
    def test_caseid_1990732(self):
        try:
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
            t = threading.Thread(target=self.random_power_off,args=(self.flashtime[0],))
            t.setDaemon(True)
            t.start()
            self.sd_tester.transfer_data(self.doipip,self.file_path,reverse_test_type = "传包过程中异常掉电")
        except Exception as e:
            logger.info("==================== reverse test Error ==========================")
            logger.error(e)
            self.sff.stop_sniff()#  停止抓包
            if self.ecu == "TCAM":
                logger.info(f"执行上电操作，并等待{self.resettime_tcam}s")
                self.io.tcam_power_on()
                time.sleep(self.resettime_tcam)
                
                logger.info("BGM退出bootloader模式")
                self.io.bgm_power_off()
                time.sleep(3)
                self.io.bgm_power_on()
                time.sleep(self.resettime_bgm)
            elif self.ecu == "BGM":
                logger.info(f"执行上电操作，并等待{self.resettime_bgm}s")
                self.io.bgm_power_on()
                time.sleep(self.resettime_bgm) 
            result = 0
            assert result, " reverse test >>>>>>>>>>>>>>>>  Failed"
        
        self.sff.stop_sniff()#  停止抓包
        if self.ecu == "TCAM":
            logger.info(f"执行上电操作，并等待{self.resettime_tcam}s")
            self.io.tcam_power_on()
            time.sleep(self.resettime_tcam)
            
            logger.info("BGM退出bootloader模式")
            self.io.bgm_power_off()
            time.sleep(3)
            self.io.bgm_power_on()
            time.sleep(self.resettime_bgm)
        elif self.ecu == "BGM":
            logger.info(f"执行上电操作，并等待{self.resettime_bgm}s")
            self.io.bgm_power_on()
            time.sleep(self.resettime_bgm)
        self.sd_tester.upgrade_ecu(self.ecu,self.doipip,self.keyinfo,self.file_url,standard=True,check_data=None,skip_step=[0],offline=True,save_packet=True,sniff_packet=True,save_path='.') 
        
    @pytest.mark.full
    @allure.title("刷写异常测试_安装过程中异常掉电")
    def test_caseid_1990729(self):
        try:
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
            t = threading.Thread(target=self.random_power_off,args=(self.flashtime[1],))
            t.setDaemon(True)
            t.start()
            self.sd_tester.verify_software_integrity(self.doipip,reverse_test_type = "安装过程中异常掉电",verify_time=self.flashtime[1])
        except Exception as e:
            logger.info("==================== reverse test Error ==========================")
            logger.error(e)
            self.sff.stop_sniff()#  停止抓包
            if self.ecu == "TCAM":
                logger.info(f"执行上电操作,并等待{self.resettime_tcam}s")
                self.io.tcam_power_on()
                time.sleep(self.resettime_tcam)

                logger.info("BGM退出bootloader模式")
                self.io.bgm_power_off()
                time.sleep(3)
                self.io.bgm_power_on()
                time.sleep(self.resettime_bgm)
            elif self.ecu == "BGM":
                logger.info(f"执行上电操作,并等待{self.resettime_bgm}s")
                self.io.bgm_power_on()
                time.sleep(self.resettime_bgm)
            result = 0
            assert result, " reverse test >>>>>>>>>>>>>>>>  Failed"
        
        self.sff.stop_sniff()#  停止抓包
        if self.ecu == "TCAM":
            logger.info(f"执行上电操作,并等待{self.resettime_tcam}s")
            self.io.tcam_power_on()
            time.sleep(self.resettime_tcam)

            logger.info("BGM退出bootloader模式")
            self.io.bgm_power_off()
            time.sleep(3)
            self.io.bgm_power_on()
            time.sleep(self.resettime_bgm)
        elif self.ecu == "BGM":
            logger.info(f"执行上电操作,并等待{self.resettime_bgm}s")
            self.io.bgm_power_on()
            time.sleep(self.resettime_bgm)
        self.sd_tester.upgrade_ecu(self.ecu,self.doipip,self.keyinfo,self.file_url,standard=True,check_data=None,skip_step=[0],offline=True,save_packet=True,sniff_packet=True,save_path='.')

    @pytest.mark.full
    @allure.title("刷写异常测试_系统负载高")
    def test_caseid_1990745(self):
        self.bus_comm.send_pdu(bus_name="connectivitycanfd", msg_id=0x509, data=[0x09,0x40,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF], cycle_time=0.1)
        self.bus_comm.send_pdu(bus_name="bodycan", msg_id=0x502, data=[0x02,0x40,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF], cycle_time=0.1)
        self.bus_comm.send_pdu(bus_name="bodyexposedcanfd", msg_id=0x531, data=[0x31,0x40,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF], cycle_time=0.1)
        self.bus_comm.send_pdu(bus_name="passivesafetycan", msg_id=0x50B, data=[0x0B,0x40,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF], cycle_time=0.1)
        self.bus_comm.send_pdu(bus_name="propulsioncan", msg_id=0x526, data=[0x26,0x40,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF], cycle_time=0.1)
        self.bus_comm.send_pdu(bus_name="chassiscan1", msg_id=0x529, data=[0x29,0x40,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF], cycle_time=0.1)
        self.bus_comm.send_pdu(bus_name="chassiscan2", msg_id=0x522, data=[0x22,0x40,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF], cycle_time=0.1)
        self.bus_comm.send_pdu(bus_name="infocanfd", msg_id=0x502, data=[0x02,0x40,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF], cycle_time=0.1)
        self.bus_comm.send_pdu(bus_name="diagnosticcan", msg_id=0x502, data=[0x02,0x40,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF], cycle_time=0.1)
        self.bus_comm.send_pdu(bus_name="adcanfd", msg_id=0x502, data=[0x02,0x40,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF], cycle_time=0.1)
        self.bus_comm.send_pdu(bus_name="bodyalmcanfd1", msg_id=0x502, data=[0x02,0x40,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF], cycle_time=0.1)
        self.bus_comm.send_pdu(bus_name="bodyalmcanfd2", msg_id=0x502, data=[0x02,0x40,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF], cycle_time=0.1)
        self.bus_comm.send_pdu(bus_name="backbonefr", msg_id=0x502, data=[0x02,0x40,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF], cycle_time=0.1)
        self.sd_tester.upgrade_ecu(self.ecu,self.doipip,self.keyinfo,self.file_url,standard=True,check_data=None,skip_step=[0],offline=True,save_packet=True,sniff_packet=True,save_path='.')
        self.bus_comm.pause_all_bus_send()#暂停所有CAN总线的数据发送

#cd test_case/bgm/
#pytest BaseTech/DiagFlash/test_flash_bgm_reverse_test.py --disable_partner='true'
    
