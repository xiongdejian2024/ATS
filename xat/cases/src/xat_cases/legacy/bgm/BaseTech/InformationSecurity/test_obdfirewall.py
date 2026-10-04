#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename     : test_obdfirewall.py
@time         : 2024/2/19
@author       : o_jingyuan.chen@external.jiduauto.com
@description  : 
'''


import pytest
import allure
from xat_cases.legacy.basetech.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *

@allure.feature('BGM BaseTech/数字安全')
class TestOBDFireWall(TestABCBase):
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
    @allure.story('OBD防火墙')
    @allure.title('1985153_OBD防火墙_开启')
    def test_caseid_1985153(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0xa040,0x01,unlock_level=UnLock.L7,write_data='01',check_data='7101a04010')
        self.sd_tester.read_did_and_check(TA.BGM_SOC,0xb165,SESSION.EMPTY,'62b16501')

    #BGM _SOC
    @pytest.mark.sanity
    @allure.story('OBD防火墙')
    @allure.title('1985151_OBD防火墙_开启_开启时间非默认值测试')
    def test_caseid_1985151(self):
        with self.log_manage.check_jetlog_by_keywords(log_type="VEHS:",keywords='Save OBD_FW_TIME:[0,0] succeed'):
            self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0xa040,0x01,unlock_level=UnLock.L7,write_data='0101',check_data='7101a04010')
        self.sd_tester.read_did_and_check(TA.BGM_SOC,0xb165,SESSION.EMPTY,'62b16501')
        
    #BGM _SOC
    @pytest.mark.sanity
    @allure.story('OBD防火墙')
    @allure.title('1985152_OBD防火墙_开启_开启时间默认值测试')
    def test_caseid_1985152(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0xa040,0x01,unlock_level=UnLock.L7,write_data='0100',check_data='7101a04010')
        self.sd_tester.read_did_and_check(TA.BGM_SOC,0xb165,SESSION.EMPTY,'62b16501')

    #BGM _SOC
    @pytest.mark.full
    @allure.story('OBD防火墙')
    @allure.title('1985150_OBD防火墙_开启_重启测试')
    def test_caseid_1985150(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0xa040,0x01,unlock_level=UnLock.L7,write_data='0100',check_data='7101a04010')
        self.sd_tester.read_did_and_check(TA.BGM_SOC,0xb165,SESSION.EMPTY,'62b16501')
        self.io.io_reset_bgm()
        time.sleep(20)
        self.sd_tester.read_did_and_check(TA.BGM_SOC,0xb165,SESSION.EMPTY,'62b16501')

    #BGM _SOC,BGM _MCU
    @pytest.mark.full
    @allure.story('OBD防火墙')
    @allure.title('1985128_OBD防火墙_开启_非黑名单UDS服务测试0x10')
    def test_caseid_1985128(self):
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x10,0x01],'5001')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x10,0x02],'5002')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x10,0x01],'5001')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x10,0x03],'5003')
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x10,0x01],'5001')
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x10,0x02],'7f1022')
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x10,0x03],'5003')
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1001',{'10 01':'5001','10 02':'5001'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1003',{'10 01':'5003','10 02':'5003'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1002',{'10 01':'5002','10 02':'7f1022'})

    #BGM _SOC,BGM _MCU
    @pytest.mark.full
    @allure.story('OBD防火墙')
    @allure.title('1985127_OBD防火墙_开启_非黑名单UDS服务测试0x14')
    def test_caseid_1985127(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x14,0xff,0xff,0xff],'54')
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x14,0xff,0xff,0xff],'54')
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1001',{'10 01':'5001','10 02':'5001'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'14ffffff',{'10 01':'7f147f','10 02':'54'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1003',{'10 01':'7f147f','10 02':'54'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'14ffffff',{'10 01':'7f147f','10 02':'54'})

    #BGM _SOC,BGM _MCU
    @pytest.mark.full
    @allure.story('OBD防火墙')
    @allure.title('1985126_OBD防火墙_开启_非黑名单UDS服务测试0x19')
    def test_caseid_1985126(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x02,0x09],'5902')
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x19,0x02,0x09],'5902')
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1001',{'10 01':'5001','10 02':'5001'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'190209',{'10 01':'7f1912','10 02':'59027f'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1003',{'10 01':'5003','10 02':'54'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'190209',{'10 01':'7f1912','10 02':'59027f'})

    #BGM _SOC,BGM _MCU
    @pytest.mark.full
    @allure.story('OBD防火墙')
    @allure.title('1985123_OBD防火墙_开启_非黑名单UDS服务测试0x22')
    def test_caseid_1985123(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC,0xf1aa,SESSION.PROGRAMMING,'62f1aa')
        self.sd_tester.read_did_and_check(TA.BGM_MCU,0xdd01,SESSION.DEFAULT,'62dd01')
        self.sd_tester.read_did_and_check(TA.BGM_MCU,0x40de,SESSION.EXTENDED,'6240de')
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1001',{'10 01':'5001','10 02':'5001'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'22f186',{'10 01':'62f18601','10 02':'62f18601'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1003',{'10 01':'5003','10 02':'5003'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'22f1ab',{'10 01':'62f1ab','10 02':'62f1ab'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1002',{'10 01':'5002','10 02':'7f1022'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'22f1aa',{'10 01':'62f1aa'})

    #BGM _SOC,BGM _MCU
    @pytest.mark.full
    @allure.story('OBD防火墙')
    @allure.title('1985122_OBD防火墙_开启_非黑名单UDS服务测试0x27')
    def test_caseid_1985122(self):
        self.sd_tester.unlock_and_check(TA.BGM_SOC,level=UnLock.L1)
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x10,0x01],'5001')
        self.sd_tester.unlock_and_check(TA.BGM_SOC,level=UnLock.L5)
        self.sd_tester.unlock_and_check(TA.BGM_SOC,level=UnLock.L7)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,level=UnLock.L3)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,level=UnLock.L5)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,level=UnLock.L11)

    #BGM _SOC,BGM _MCU
    @pytest.mark.full
    @allure.story('OBD防火墙')
    @allure.title('1985124_OBD防火墙_开启_非黑名单UDS服务测试0x3E')
    def test_caseid_1985124(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x3e,0x00],'7e00')
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x3e,0x00],'7e00')
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x3e,0x00],'7e00')
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x3e,0x00],'7e00')
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x3e,0x00],'7e00')
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1001',{'10 01':'5001','10 02':'5001'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'3e00',{'10 01':'7e00','10 02':'7e00'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1003',{'10 01':'5003','10 02':'5003'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'3e00',{'10 01':'7e00','10 02':'7e00'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1002',{'10 01':'5002','10 02':'7f1022'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'3e00',{'10 01':'7e00'})

    #BGM _SOC,BGM _MCU
    @pytest.mark.full
    @allure.story('OBD防火墙')
    @allure.title('1985125_OBD防火墙_开启_非黑名单UDS服务测试0x85')
    def test_caseid_1985125(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x85,0x01],'c501')
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1003',{'10 01':'5003','10 02':'5003'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'8501',{'10 01':'7f8512','10 02':'c501'})

    #BGM _SOC,BGM _MCU
    @pytest.mark.sanity
    @allure.story('OBD防火墙')
    @allure.title('1985131_OBD防火墙_开启_黑名单UDS服务测试0x11')
    def test_caseid_1985131(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x11],[0x7f,0x11,0x22])
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x11],[0x7f,0x11,0x22])
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x11],[0x7f,0x11,0x22])
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x11],[0x7f,0x11,0x22])
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x11],[0x7f,0x11,0x22])
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1001',{'10 01':'5001','10 02':'5001'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'11',{'1F FF':'7f1122'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1003',{'10 01':'5003','10 02':'5003'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'11',{'1F FF':'7f1122'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1002',{'10 01':'5002','10 02':'7f1022'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'11',{'1F FF':'7f1122'})

    #BGM _SOC
    @pytest.mark.full
    @allure.story('OBD防火墙')
    @allure.title('1985135_OBD防火墙_开启_黑名单UDS服务测试0x23')
    def test_caseid_1985135(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x23],[0x7f,0x23,0x22])
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x23],[0x7f,0x23,0x22])
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x23],[0x7f,0x23,0x22])
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1001',{'10 01':'5001','10 02':'5001'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'23',{'1F FF':'7f2322'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1003',{'10 01':'5003','10 02':'5003'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'23',{'1F FF':'7f2322'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1002',{'10 01':'5002','10 02':'7f1022'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'23',{'1F FF':'7f2322'})

    #BGM _SOC,BGM _MCU
    @pytest.mark.sanity
    @allure.story('OBD防火墙')
    @allure.title('1985130_OBD防火墙_开启_黑名单UDS服务测试0x28')
    def test_caseid_1985130(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x28],[0x7f,0x28,0x22])
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x28],[0x7f,0x28,0x22])
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1001',{'10 01':'5001','10 02':'5001'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'28',{'1F FF':'7f2822'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1003',{'10 01':'5003','10 02':'5003'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'28',{'1F FF':'7f2822'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1002',{'10 01':'5002','10 02':'7f1022'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'28',{'1F FF':'7f2822'})

    #BGM _SOC,BGM _MCU
    @pytest.mark.sanity
    @allure.story('OBD防火墙')
    @allure.title('1985136_OBD防火墙_开启_黑名单UDS服务测试0x2E')
    def test_caseid_1985136(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x2e],[0x7f,0x2e,0x22])
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x2e],[0x7f,0x2e,0x22])
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x2e],[0x7f,0x2e,0x22])
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x2e],[0x7f,0x2e,0x22])
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x2e],[0x7f,0x2e,0x22])
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1001',{'10 01':'5001','10 02':'5001'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'2e',{'1F FF':'7f2822'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1003',{'10 01':'5003','10 02':'5003'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'2e',{'1F FF':'7f2822'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1002',{'10 01':'5002','10 02':'7f1022'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'2e',{'1F FF':'7f2822'})

    #BGM _SOC,BGM _MCU
    @pytest.mark.sanity
    @allure.story('OBD防火墙')
    @allure.title('1985132_OBD防火墙_开启_黑名单UDS服务测试0x2F')
    def test_caseid_1985132(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x2f],[0x7f,0x2f,0x22])
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1003',{'10 01':'5003','10 02':'5003'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'2f',{'1F FF':'7f2f22'})

    #BGM _SOC,BGM _MCU
    @pytest.mark.sanity
    @allure.story('OBD防火墙')
    @allure.title('1985129_OBD防火墙_开启_黑名单UDS服务测试0x31')
    def test_caseid_1985129(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x31],[0x7f,0x31,0x22])
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x31],[0x7f,0x31,0x22])
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x31],[0x7f,0x31,0x22])
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x31],[0x7f,0x31,0x22])
        self.sd_tester.session_ctrl_and_check(TA.BGM_MCU,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x31],[0x7f,0x31,0x22])
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1001',{'10 01':'5001','10 02':'5001'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'31',{'1F FF':'7f3122'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1003',{'10 01':'5003','10 02':'5003'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'31',{'1F FF':'7f3122'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1002',{'10 01':'5002','10 02':'7f1022'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'31',{'1F FF':'7f3122'})

    #BGM _SOC
    @pytest.mark.sanity
    @allure.story('OBD防火墙')
    @allure.title('1985141_OBD防火墙_开启_黑名单UDS服务测试0x34')
    def test_caseid_1985141(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x34],[0x7f,0x34,0x22])
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x34],[0x7f,0x34,0x22])
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x34],[0x7f,0x34,0x22])
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1001',{'10 01':'5001','10 02':'5001'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'34',{'1F FF':'7f3422'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1003',{'10 01':'5003','10 02':'5003'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'34',{'1F FF':'7f3422'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1002',{'10 01':'5002','10 02':'7f1022'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'34',{'1F FF':'7f3422'})

    #BGM _SOC
    @pytest.mark.sanity
    @allure.story('OBD防火墙')
    @allure.title('1985140_OBD防火墙_开启_黑名单UDS服务测试0x35')
    def test_caseid_1985140(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x35],[0x7f,0x35,0x22])
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x35],[0x7f,0x35,0x22])
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x35],[0x7f,0x35,0x22])
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1001',{'10 01':'5001','10 02':'5001'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'35',{'1F FF':'7f3522'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1003',{'10 01':'5003','10 02':'5003'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'35',{'1F FF':'7f3522'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1002',{'10 01':'5002','10 02':'7f1022'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'35',{'1F FF':'7f3522'})

    #BGM _SOC
    @pytest.mark.sanity
    @allure.story('OBD防火墙')
    @allure.title('1985139_OBD防火墙_开启_黑名单UDS服务测试0x36')
    def test_caseid_1985139(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x36],[0x7f,0x36,0x22])
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x36],[0x7f,0x36,0x22])
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x36],[0x7f,0x36,0x22])
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1001',{'10 01':'5001','10 02':'5001'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'36',{'1F FF':'7f3622'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1003',{'10 01':'5003','10 02':'5003'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'36',{'1F FF':'7f3622'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1002',{'10 01':'5002','10 02':'7f1022'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'36',{'1F FF':'7f3622'})

    #BGM _SOC
    @pytest.mark.sanity
    @allure.story('OBD防火墙')
    @allure.title('1985138_OBD防火墙_开启_黑名单UDS服务测试0x37')
    def test_caseid_1985138(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x37],[0x7f,0x37,0x22])
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x37],[0x7f,0x37,0x22])
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x37],[0x7f,0x37,0x22])
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1001',{'10 01':'5001','10 02':'5001'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'37',{'1F FF':'7f3722'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1003',{'10 01':'5003','10 02':'5003'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'37',{'1F FF':'7f3722'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1002',{'10 01':'5002','10 02':'7f1022'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'37',{'1F FF':'7f3722'})

    #BGM _SOC
    @pytest.mark.full
    @allure.story('OBD防火墙')
    @allure.title('1985137_OBD防火墙_开启_黑名单UDS服务测试0x38')
    def test_caseid_1985137(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x38],[0x7f,0x38,0x22])
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x38],[0x7f,0x38,0x22])
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x38],[0x7f,0x38,0x22])
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1001',{'10 01':'5001','10 02':'5001'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'38',{'1F FF':'7f3822'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1003',{'10 01':'5003','10 02':'5003'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'38',{'1F FF':'7f3822'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1002',{'10 01':'5002','10 02':'7f1022'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'38',{'1F FF':'7f3822'})

    #BGM _SOC
    @pytest.mark.full
    @allure.story('OBD防火墙')
    @allure.title('1985134_OBD防火墙_开启_黑名单UDS服务测试0x3D')
    def test_caseid_1985134(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x3d],[0x7f,0x3d,0x22])
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x3d],[0x7f,0x3d,0x22])
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x3d],[0x7f,0x3d,0x22])
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1001',{'10 01':'5001','10 02':'5001'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'3d',{'1F FF':'7f3d22'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1003',{'10 01':'5003','10 02':'5003'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'3d',{'1F FF':'7f3d22'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1002',{'10 01':'5002','10 02':'7f1022'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'3d',{'1F FF':'7f3d22'})

    #BGM _SOC
    @pytest.mark.full
    @allure.story('OBD防火墙')
    @allure.title('1985133_OBD防火墙_开启_黑名单UDS服务测试0x84')
    def test_caseid_1985133(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x84],[0x7f,0x84,0x22])
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x84],[0x7f,0x84,0x22])
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.BGM_SOC,[0x84],[0x7f,0x84,0x22])
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1001',{'10 01':'5001','10 02':'5001'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'84',{'1F FF':'7f8422'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1003',{'10 01':'5003','10 02':'5003'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'84',{'1F FF':'7f8422'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1002',{'10 01':'5002','10 02':'7f1022'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'84',{'1F FF':'7f8422'})

    #BGM _SOC,BGM _MCU
    @pytest.mark.full
    @allure.story('OBD防火墙')
    @allure.title('1985120_OBD防火墙_打开_实际状态测试')
    def test_caseid_1985120(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC,0xb165,SESSION.DEFAULT,'62b16501')
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0x4170,unlock_level=UnLock.L5,write_data='03e8',check_data='7f2e22',check_method=Check_Method.response,recover=False)

    #BGM _SOC
    @pytest.mark.smoke
    @allure.story('OBD防火墙')
    @allure.title('1985149_OBD防火墙_关闭_关闭时间00测试')
    def test_caseid_1985149(self):
        self.sd_tester.session_ctrl_and_check(TA.BGM_SOC,SESSION.DEFAULT,'62f18601')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0xa040,0x01,unlock_level=UnLock.L7,write_data='0200',check_data='7f3131')
        self.sd_tester.read_did_and_check(TA.BGM_SOC,0xb165,SESSION.EMPTY,'62b16501')

    #BGM _SOC
    @pytest.mark.sanity
    @allure.story('OBD防火墙')
    @allure.title('1985148_OBD防火墙_关闭_关闭时间01测试')
    def test_caseid_1985148(self):
        with self.log_manage.check_jetlog_by_keywords(log_type="VEHS:",keywords='Save OBD_FW_TIME:[0,60] succeed'):
            self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0xa040,0x01,unlock_level=UnLock.L7,write_data='0201',check_data='7101a04010')
        self.sd_tester.read_did_and_check(TA.BGM_SOC,0xb165,SESSION.EMPTY,'62b16502')

    #BGM _SOC
    @pytest.mark.sanity
    @allure.story('OBD防火墙')
    @allure.title('1985147_OBD防火墙_关闭_关闭时间30测试')
    def test_caseid_1985147(self):
        with self.log_manage.check_jetlog_by_keywords(log_type="VEHS:",keywords='Save OBD_FW_TIME:[11,64] succeed'):
            self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0xa040,0x01,unlock_level=UnLock.L7,write_data='0230',check_data='7101a04010')
        self.sd_tester.read_did_and_check(TA.BGM_SOC,0xb165,SESSION.EMPTY,'62b16502')

    #BGM _SOC
    @pytest.mark.full
    @allure.story('OBD防火墙')
    @allure.title('1985146_OBD防火墙_关闭_关闭时间31测试')
    def test_caseid_1985146(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0xa040,0x01,unlock_level=UnLock.L7,write_data='01',check_data='7101a04010')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0xa040,0x01,unlock_level=UnLock.L7,write_data='0231',check_data='7f3131')
        self.sd_tester.read_did_and_check(TA.BGM_SOC,0xb165,SESSION.EMPTY,'62b16501')

    #BGM _SOC
    @pytest.mark.full
    @allure.story('OBD防火墙')
    @allure.title('1985145_OBD防火墙_关闭_关闭时间FE测试')
    def test_caseid_1985145(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0xa040,0x01,unlock_level=UnLock.L7,write_data='02fe',check_data='7f3131')
        self.sd_tester.read_did_and_check(TA.BGM_SOC,0xb165,SESSION.EMPTY,'62b16501')

    #BGM _SOC
    @pytest.mark.full
    @allure.story('OBD防火墙')
    @allure.title('1985144_OBD防火墙_关闭_关闭时间FF测试_staging')
    def test_caseid_1985144(self):
        with self.log_manage.check_jetlog_by_keywords(log_type="VEHS:",keywords='Save OBD_FW_TIME:[59,196] succeed'):
            self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0xa040,0x01,unlock_level=UnLock.L7,write_data='02ff',check_data='7101a04010')
        self.sd_tester.read_did_and_check(TA.BGM_SOC,0xb165,SESSION.EMPTY,'62b16502')

    #BGM _SOC
    @pytest.mark.full
    @allure.story('OBD防火墙')
    @allure.title('1985119_OBD防火墙_关闭_B165不可写')
    def test_caseid_1985119(self):
        self.sd_tester.write_did_and_check(TA.BGM_SOC,0xb165,SESSION.DEFAULT,write_data='01',check_data='7f2e7f',check_method=Check_Method.response,recover=False)
        self.sd_tester.write_did_and_check(TA.BGM_SOC,0xb165,SESSION.EXTENDED,write_data='01',check_data='7f2e31',check_method=Check_Method.response,recover=False)
        self.sd_tester.write_did_and_check(TA.BGM_SOC,0xb165,SESSION.PROGRAMMING,write_data='01',check_data='7f2e31',check_method=Check_Method.response,recover=False)

    #BGM _SOC,BGM _MCU
    @pytest.mark.full
    @allure.story('OBD防火墙')
    @allure.title('1985121_OBD防火墙_关闭_实际状态测试')
    def test_caseid_1985121(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC,0xb165,SESSION.DEFAULT,'62b16502')
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0x4170,unlock_level=UnLock.L5,write_data='03e8',check_data='6e4170',check_method=Check_Method.response,recover=False)

    #BGM _SOC
    @pytest.mark.full
    @allure.story('OBD防火墙')
    @allure.title('1985142_OBD防火墙_关闭_重启测试')
    def test_caseid_1985142(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0xa040,0x01,unlock_level=UnLock.L7,write_data='02ff',check_data='7101a04010')
        self.sd_tester.read_did_and_check(TA.BGM_SOC,0xb165,SESSION.EMPTY,'62b16502')
        self.sd_tester.reset_0x1181()
        self.sd_tester.read_did_and_check(TA.BGM_SOC,0xb165,SESSION.EMPTY,'62b16502')

    #BGM _SOC
    @pytest.mark.smoke
    @allure.story('OBD防火墙')
    @allure.title('1985155_OBD防火墙_状态读取_物理寻址')
    def test_caseid_1985155(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC,0xb165,SESSION.DEFAULT,'62b165',check_in=[0x01,0x02])
        self.sd_tester.read_did_and_check(TA.BGM_SOC,0xb165,SESSION.EXTENDED,'62b165',check_in=[0x01,0x02])
        self.sd_tester.read_did_and_check(TA.BGM_SOC,0xb165,SESSION.PROGRAMMING,'62b165',check_in=[0x01,0x02])

    #功能寻址
    @pytest.mark.smoke
    @allure.story('OBD防火墙')
    @allure.title('1985154_OBD防火墙_状态读取_功能寻址')
    def test_caseid_1985154(self):
        self.sd_tester.send_data_and_check(TA.FUNCTION,'22b165',{'10 01':'62b165'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1003',{'10 01':'5003','10 02':'5003'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'22b165',{'10 01':'62b165'})
        self.mix.init_boot_per()
        self.sd_tester.send_data_and_check(TA.FUNCTION,'1002',{'10 01':'5002','10 02':'5002'})
        self.sd_tester.send_data_and_check(TA.FUNCTION,'22b165',{'10 01':'62b165'})

#pytest BaseTech/InformationSecurity/test_obdfirewall.py::TestOBDFireWall::test_caseid_1985131 --disable_partner='true'
