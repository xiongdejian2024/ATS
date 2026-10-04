#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename     : test_certificate_management.py
@time         : 2024/2/19
@author       : o_jingyuan.chen@external.jiduauto.com
@description  : 
'''

import pytest
import allure
from xat_cases.legacy.basetech.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *

@allure.feature('BGM BaseTech/数字安全')
class TestCertificateManage(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self,ecu)
        logger.info("before_class")

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        self.sd_tester.exit_muc_boot()
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        logger.info("after_class")
        super().after_class(self, ecu)

    #BGM _SOC
    @pytest.mark.smoke
    @allure.story('证书管理')
    @allure.title('1985236_BGM SK预置')
    def test_caseid_1985236(self):
        crt = self.ssh.type_commands(DeviceName.BGM,f"ls -l /app/etc/certificate/ | grep BGMSk.key" + " | awk '{print $5}' ")
        assert crt == '1218'
        logger.info(f"证书BGMSk.key安装的大小为:{crt}")

    #BGM _SOC
    @pytest.mark.smoke
    @allure.story('证书管理')
    @allure.title('1985235_OTA证书预置')
    def test_caseid_1985235(self):
        crt = self.ssh.type_commands(DeviceName.BGM,f"ls -l /app/etc/certificate/ | grep OTAService.crt" + " | awk '{print $5}' ")
        assert crt == '661'
        logger.info(f"证书OTAService.crt安装的大小为:{crt}")

    #BGM _SOC
    @pytest.mark.smoke
    @allure.story('证书管理')
    @allure.title('1985216_服务中间证书预置')
    def test_caseid_1985216(self):
        crt = self.ssh.type_commands(DeviceName.BGM,f"ls -l /app/etc/certificate/ | grep ServiceCA.crt" + " | awk '{print $5}' ")
        assert crt == '664'
        logger.info(f"证书ServiceCA.crt安装的大小为:{crt}")

    #BGM _SOC
    @pytest.mark.smoke
    @allure.story('证书管理')
    @allure.title('1985215_根证书预置')
    def test_caseid_1985215(self):
        crt = self.ssh.type_commands(DeviceName.BGM,f"ls -l /app/etc/certificate/ | grep rootCA.crt" + " | awk '{print $5}' ")
        assert crt == '615'
        logger.info(f"证书rootCA.crt安装的大小为:{crt}")

    #BGM _SOC
    @pytest.mark.sanity
    @allure.story('证书管理')
    @allure.title('1985219_数字证书颁发')
    def test_caseid_1985219(self):
        self.sd_tester.get_ecu_serial_number()
        self.sd_tester.get_vehicle_identification_number()
        self.sd_tester.read_did_and_check(TA.TCAM,0xF18C,SESSION.DEFAULT,'62f18c',check_length=14)
        self.sd_tester.read_did_and_check(TA.TCAM,0xF190,SESSION.DEFAULT,'62f190',check_length=40)

    #BGM _SOC
    @pytest.mark.full
    @allure.story('证书管理')
    @allure.title('1985218_整车环境管理_证书安装')
    def test_caseid_1985218(self):
        self.ssh.type_commands(DeviceName.BGM,"su prop")
        ENVBGM=self.ssh.type_commands(DeviceName.BGM,"/app/bin/prop.sh get | awk '/ENV/{print $3}'")[:4]
        assert ENVBGM =='Test'
        
    @pytest.mark.smoke
    @allure.story('证书管理')
    @allure.title('1994612_车辆环境Staging读取')
    def test_caseid_1994612(self):
        self.sd_tester.unlock_and_check(TA.BGM_SOC,SESSION.EXTENDED,UnLock.L7,check_data='6708')
        data_vid = self.sd_tester.read_did_and_check(TA.BGM_SOC,0xb163,SESSION.EMPTY,'62b163',check_length=38)[6:] 
        if data_vid == "ffffffffffffffffffffffffffffffff":
            logger.info(f"data_vid:{data_vid},重新读取配置文件，写入正确的VID")
            vid=self.tc_config['vid']        
            self.sd_tester.write_did_and_check(TA.BGM_SOC, 0xb163, SESSION.EXTENDED, UnLock.L7,
                                            vid, f'62b163{vid}',check_method=Check_Method.read, recover=False) 
            time.sleep(3)
            logger.info(f"VID:{vid}")
        else:
            logger.info(f"VID:{data_vid}")
        data = self.sd_tester.read_did_and_check(TA.BGM_SOC,0xb160,SESSION.DEFAULT,'62b160',check_length=8)[6:]
        assert data == '02'

    #BGM _SOC
    @pytest.mark.full
    @allure.story('证书管理')
    @allure.title('1985231_VID管理_读取')
    def test_caseid_1985231(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC,0xb163,SESSION.EXTENDED,'7f2233')

    #BGM _SOC
    @pytest.mark.full
    @allure.story('证书管理')
    @allure.title('1985234_VID管理_写入')
    def test_caseid_1985234(self):
        self.sd_tester.unlock_and_check(TA.BGM_SOC,SESSION.EXTENDED,UnLock.L7,check_data='6708')
        data=self.sd_tester.read_did_and_check(TA.BGM_SOC,0xb163,SESSION.EMPTY,'62b163',check_length=38)[6:]
        self.sd_tester.write_did_and_check(TA.BGM_SOC,0xb163,SESSION.EXTENDED,UnLock.L7,data,f'62b163{data}',check_method=Check_Method.read,recover=False)

    #BGM _SOC
    @pytest.mark.full
    @allure.story('证书管理')
    @allure.title('1985233_VID管理_L7读取')
    def test_caseid_1985233(self):
        self.sd_tester.unlock_and_check(TA.BGM_SOC,SESSION.EXTENDED,UnLock.L7,check_data='6708')
        self.sd_tester.read_did_and_check(TA.BGM_SOC,0xb163,SESSION.EMPTY,'62b163',check_length=38)

    #BGM _SOC
    @pytest.mark.full
    @allure.story('证书管理')
    @allure.title('1985232_VID管理_L5读取')
    def test_caseid_1985232(self):
        self.sd_tester.unlock_and_check(TA.BGM_SOC,SESSION.EXTENDED,UnLock.L5,check_data='6706')
        self.sd_tester.read_did_and_check(TA.BGM_SOC,0xb163,SESSION.EMPTY,'62b163',check_length=38)

    #BGM _SOC
    @pytest.mark.full
    @allure.story('证书管理')
    @allure.title('1985230_VIN码存储保护_解锁修改')
    def test_caseid_1985230(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5,check_data='6706')
        data=self.sd_tester.read_did_and_check(TA.BGM_MCU,0xf190,SESSION.EMPTY,'62f190',check_length=40)[6:]
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xf190,SESSION.EMPTY,UnLock.L0,data,f'62f190{data}',check_method=Check_Method.read,recover=False)

    #BGM _SOC
    @pytest.mark.full
    @allure.story('证书管理')
    @allure.title('1985229_VIN码存储保护_未解锁修改')
    def test_caseid_1985229(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.DEFAULT,UnLock.L0)
        data=self.sd_tester.read_did_and_check(TA.BGM_MCU,0xf190,SESSION.EMPTY,'62f190',check_length=40)[6:]
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xf190,SESSION.EXTENDED,UnLock.L0,data,'7f2e33',check_method=Check_Method.response,recover=False)

    #BGM _SOC
    @pytest.mark.full
    @allure.story('证书管理')
    @allure.title('1985214_高级安全访问解锁_解锁L7访问权限')
    def test_caseid_1985214(self):
        self.sd_tester.unlock_and_check(TA.BGM_SOC,SESSION.EXTENDED,UnLock.L7)
    
    #BGM _SOC
    @pytest.mark.full
    @allure.story('证书管理')
    @allure.title('1985212_证书写入完整性检查_参数写入大于有效字节')
    def test_caseid_1985212(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0x8020,0x01,SESSION.EXTENDED,UnLock.L7,f'{"0" * 4099}','7f3113')

    #BGM _SOC
    @pytest.mark.full
    @allure.story('证书管理')
    @allure.title('1985213_证书写入完整性检查_参数写入小于有效字节')
    def test_caseid_1985213(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0x8020,0x01,SESSION.EXTENDED,UnLock.L7,f'{"0" * 4096}','7f3113')
        
    #BGM _SOC
    @pytest.mark.full
    @allure.story('证书管理')
    @allure.title('1985211_证书写入完整性检查_校验位错误')
    def test_caseid_1985211(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0x8020,0x01,SESSION.EXTENDED,UnLock.L7,f'03000c6c6e34686969376c33616465{"f" * 4064}6760','710180202103')

#pytest BaseTech/InformationSecurity/test_certificate_management.py::TestCertificateManage::test_caseid_113077
